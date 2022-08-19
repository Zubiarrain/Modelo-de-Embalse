from .CalculoFallaCaudal import CalculoFalla
from MyUtils.help import create_plot,extract_excel_data
import time

class CurvaGarantia:

    """
    Esta clase nos dará una lista de niveles máximos para una serie de caudales objetivos.
    Como datos de entrada tenemos un caudal minimo, uno máximo, un paso de calculo, una falla y un nivel minimo. A partir de estos datos comienza con el caudal minimo, la falla y el nivel minimo para crear una instancia de CalculoFalla y obtener el nivel máximo para un determinado caudal y una determianada falla.
    Luego sigue creando instancias con distintos caudales a un paso determinado entre el caudal minimo y el maximo hasta llegar al último caudal que pueda cumplir con la falla que se pide.
    """

    def __init__(self,paso_calculo,falla_buscada,nivel_min,nivel_max_limite=None) -> None:

        self._paso_calculo = paso_calculo
        self._falla_buscada = falla_buscada
        self._nivel_min = nivel_min
        
        
        self.input_data = extract_excel_data("input_caudal_constante.xlsx")
        self.nivel_max = self._nivel_min
        self.nivel_min_absoluto = self.input_data["Nivel[m]"][0]
        self.nivel_max_absoluto = self.input_data["Nivel[m]"][-1]
        if nivel_max_limite:
            self.nivel_max_limite = nivel_max_limite
        else:
            self.nivel_max_limite = self.nivel_max_absoluto

        if self.nivel_max_limite > self.nivel_max_absoluto:
            raise Exception(f'Nivel máximo límite {self.nivel_max_limite} no puede ser mayor al máximo absoluto {self.nivel_max_absoluto} ')
        if self._nivel_min > self.nivel_max_limite:
            raise Exception(f'Nivel mínimo {self._nivel_min} no puede ser mayor al límite {self.nivel_max_limite} ')
        if self._nivel_min < self.nivel_min_absoluto:
            raise Exception(f'Nivel mínimo {self._nivel_min} no puede ser menor al absoluto {self.nivel_min_absoluto} ')

        self.limite_alcanzado = False
        self.tiempo_inicial_corrida = time.time()
        self.tiempo_corrida_minutos = 0
        self.data = {"Caudales":[],"Niveles max":[]}
        self.iteraciones_falla = []
        self._caudal_calculo()
    
    def _caudal_calculo(self):
        contador = 0
        while True:
            if self.nivel_max>self.nivel_max_limite:
                self.nivel_max = self.nivel_max_limite
                if self.limite_alcanzado or self.nivel_max ==self.data["Niveles max"][-1] :
                    break
                self.limite_alcanzado = True

            caudal_objetivo = self.data["Caudales"][-1] if contador>0  else 0

            calculo_falla = CalculoFalla(
                input_data=self.input_data,
                falla_buscada = self._falla_buscada,
                nivel_min = self._nivel_min,
                nivel_max= self.nivel_max,
                caudal_objetivo=caudal_objetivo
                )
            if calculo_falla.error:
                break
            self.data["Niveles max"].append(self.nivel_max)
            self.data["Caudales"].append(calculo_falla.caudal_objetivo)
            self.iteraciones_falla.append(calculo_falla.iteraciones)
            self.nivel_max += self._paso_calculo
            contador += 1

        self.tiempo_corrida_minutos = round((time.time() - self.tiempo_inicial_corrida)/60,4)

    """ def curva_garantia(self):
        create_plot(self.data["Caudales"],self.data["Niveles max"],'Garantía','Q objetivo [m³/s]','NMN [m]','o') """



if __name__ == '__main__':

    falla_buscada = 5
    nivel_min = 140
    #caudal_modulo = 730.5
    paso_calculo = 5

    curva_garantia = CurvaGarantia(
        paso_calculo=paso_calculo,
        falla_buscada=falla_buscada,
        nivel_min=nivel_min
    )