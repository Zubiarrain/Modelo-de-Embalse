from datetime import timedelta
from logging import raiseExceptions
import time
from .CalculoFallaPotencia import CalculoFalla
from MyUtils.help import create_plot,extract_excel_data

class CurvaGarantia:

    """
    Esta clase nos dará una lista de niveles máximos para una serie de caudales objetivos.
    Como datos de entrada tenemos un caudal minimo, uno máximo, un paso de calculo, una falla y un nivel minimo. A partir de estos datos comienza con el caudal minimo, la falla y el nivel minimo para crear una instancia de CalculoFalla y obtener el nivel máximo para un determinado caudal y una determianada falla.
    Luego sigue creando instancias con distintos caudales a un paso determinado entre el caudal minimo y el maximo hasta llegar al último caudal que pueda cumplir con la falla que se pide.
    """

    def __init__(self,paso_calculo,falla_buscada,rendimiento,nivel_min_limite=None) -> None:

        self._paso_calculo = paso_calculo
        self._falla_buscada = falla_buscada
        self.nivel_min_limite = nivel_min_limite
        self.rendimiento = rendimiento

        self.input_data = extract_excel_data("input_energia_variable.xlsx")
        self.nivel_max = min(self.input_data['Nivel_max[m]'])
        self.nivel_min =self.nivel_max
        self.nivel_min_absoluto = self.input_data["Nivel[m]"][0]
        self.nivel_max_absoluto = self.input_data["Nivel[m]"][-1]

        if nivel_min_limite:
            self.nivel_min_limite = nivel_min_limite
        else:
            self.nivel_min_limite = self.nivel_min_absoluto

        if self.nivel_min_limite < self.nivel_min_absoluto:
            raise Exception(f'Nivel mínimo límite {self.nivel_min_limite} no puede ser menor al mínimo absoluto {self.nivel_min_absoluto} ')
        if self.nivel_min < self.nivel_min_limite:
            raise Exception(f'Nivel máximo {self.nivel_min} no puede ser menor al límite {self.nivel_min_limite} ')

        
        self.tiempo_inicial_corrida = time.time()
        self.tiempo_corrida_minutos = 0
        self.iteraciones_falla = []
        self.data = {"Potencias":[],"Energias":[],"Niveles min":[]}
        self.limite_alcanzado = False
        self._potencia_calculo()

        self.maxima_potencia = max(self.data["Potencias"])
        index = self.data["Potencias"].index(self.maxima_potencia)
        self.nivel_min_optimo = self.data["Niveles min"][index]
        print('Potencia máxima:',self.maxima_potencia)
        
    
    def _potencia_calculo(self):
        contador = 0
        while True:

            if self.nivel_min<self.nivel_min_limite:
                self.nivel_min = self.nivel_min_limite
                if self.limite_alcanzado or self.nivel_min == self.data["Niveles min"][-1]:
                    break
                self.limite_alcanzado = True

            potencia_firme = self.data["Potencias"][-1] if contador>0  else 0
            
            calculo_falla = CalculoFalla(
                input_data=self.input_data,
                falla_buscada = self._falla_buscada,
                nivel_min= self.nivel_min,
                rendimiento= self.rendimiento,
                potencia_firme=potencia_firme
                )
            if calculo_falla.error:
                break
            self.data["Niveles min"].append(self.nivel_min)
            self.data["Potencias"].append(calculo_falla.potencia_firme)
            self.data["Energias"].append(calculo_falla.energia_firme)
            self.iteraciones_falla.append(calculo_falla.iteraciones)
            self.nivel_min -= self._paso_calculo
            contador += 1


        self.tiempo_corrida_minutos = round((time.time() - self.tiempo_inicial_corrida)/60,4)
            
            
                

            

    def _curva_pot_nmn(self):
        create_plot(self.data["Energias"],self.data["Niveles min"],'Garantía','Energia [MW/h]','NmN [m]','o')
        



if __name__ == '__main__':

    falla_buscada = 5
    nivel_max = 170
    #caudal_modulo = 730.5
    paso_calculo = 1

    curva_garantia = CurvaGarantia(
        paso_calculo=paso_calculo,
        falla_buscada=falla_buscada,
        nivel_max=nivel_max,
        rendimiento = 0.9
    )
