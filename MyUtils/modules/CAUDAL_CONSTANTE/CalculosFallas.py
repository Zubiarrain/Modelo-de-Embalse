from MyUtils.help import create_plot, export_excel
from .CalculoFallaCaudal import CalculoFalla


class CalculosFallas:

    def __init__(self,input_data,falla_buscada, nivel_min,nivel_max):
        # ------------ INIT VARS ------------------

        self.input_data = input_data
        self.nivel_min = nivel_min
        self.nivel_max = nivel_max
        self.falla_buscada = falla_buscada

        # ------------ DATA ------------------
        self.calculos_totales = []
        self.resultados = []
        self.info = []
        self.duracion_acumulada = []
        self.caudales = []
        self.dicts = []
        self.total_data = []

        # ------------ CALC ------------------
        self.calculo()
        
    def calculo(self):

        variables = [self.nivel_min,self.nivel_max,self.falla_buscada]
        rango = [len(self.nivel_min),len(self.nivel_max),len(self.falla_buscada)]
        casos = max(rango)

        for i in range(casos):
            datos=[self.nivel_min[0],self.nivel_max[0],self.falla_buscada[0]]
            for variable in variables:
                if len(variable) != 1:
                    index = variables.index(variable)
                    datos[index] = variable[i]

            calculo_falla = CalculoFalla(
                input_data=self.input_data,
                falla_buscada=datos[2],
                nivel_min=datos[0],
                nivel_max=datos[1]
                )
            self.calculos_totales.append(calculo_falla)
            resultado = [
                    "Caudal Objetivo [m³/s]: "+str(round(calculo_falla.calculo_total.caudal_objetivo)),
                    "Déficit [%]: " + str(round(calculo_falla.calculo_total.falla,2)),
                    "Nivel Inicial [m]: " + str(calculo_falla.calculo_total.nivel_inicial),
                    "Nivel Mínimo [m]: " + str(calculo_falla.calculo_total.nivel_min),
                    "Nivel Máximo [m]: " + str(calculo_falla.calculo_total.nivel_max),
                    "Días del modelo: " + str(calculo_falla.calculo_total.total_time),
                    "Iteraciones: " + str(calculo_falla.iteraciones),
                    "Tiempo de corrida [min]: " + str(calculo_falla.tiempo_corrida_minutos)
                    ]
            info = f"NM= {calculo_falla.calculo_total.nivel_max} - Nm= {calculo_falla.calculo_total.nivel_min} - Q= {calculo_falla.calculo_total.caudal_objetivo} - Deficit= {round(calculo_falla.calculo_total.falla,2)} "
            self.info.append(info)
            self.dicts.append(calculo_falla.calculo_total.duracion_data)
            self.duracion_acumulada.append(calculo_falla.calculo_total.duracion_data['Duracion Acumulada'])
            self.caudales.append(calculo_falla.calculo_total.duracion_data['Caudal'])
            self.resultados.append(resultado)
            self.total_data.append(calculo_falla.calculo_total.total_data)
            print(resultado,'\n')


    def duracion(self):
        create_plot(self.duracion_acumulada,self.caudales,self.info, f'Curva Duración','Duración[%]','Q[m³/s]','')
        
    def exportar_excel(self):
        for dict in self.dicts:
            index = self.dicts.index(dict)
            export_excel(dict,f"Duracion - {self.info[index]}")
            export_excel(self.total_data[index],f"Embalse Caudal Constante - {self.info[index]}")
            