from MyUtils.help import create_plot, export_excel
from .CalculoTotal import CalculoTotal


class CalculosTotales:

    def __init__(self,input_data, nivel_min, nivel_max, caudal_objetivo):
        # ------------ INIT VARS ------------------

        self.input_data = input_data
        self.nivel_min = nivel_min
        self.nivel_max = nivel_max
        self.caudal_objetivo = caudal_objetivo

        # ------------ DATA ------------------
        self.calculos_totales = []
        self.resultados = []
        self.info = []
        self.duracion_acumulada = []
        self.caudales = []
        self.dicts = []
        self.total_data = []
        self.niveles = []
        self.tiempos = []

        # ------------ CALC ------------------
        self.calculo()
        
    def calculo(self):

        variables = [self.nivel_min,self.nivel_max,self.caudal_objetivo]
        rango = [len(self.nivel_min),len(self.nivel_max),len(self.caudal_objetivo)]
        casos = max(rango)

        for i in range(casos):
            datos=[self.nivel_min[0],self.nivel_max[0],self.caudal_objetivo[0]]
            for variable in variables:
                if len(variable) != 1:
                    index = variables.index(variable)
                    datos[index] = variable[i]

            calculo_total = CalculoTotal(
                input_data=self.input_data,
                nivel_min=datos[0],
                nivel_max=datos[1],
                caudal_objetivo=datos[2]
                )
            self.calculos_totales.append(calculo_total)
            resultado = [
                    "Caudal Objetivo [m³/s]: "+str(calculo_total.caudal_objetivo),
                    "Déficit [%]: " + str(round(calculo_total.falla,2)),
                    "Nivel Inicial [m]: " + str(calculo_total.nivel_inicial),
                    "Nivel Mínimo [m]: " + str(calculo_total.nivel_min),
                    "Nivel Máximo [m]: " + str(calculo_total.nivel_max),
                    "Días del modelo: " + str(calculo_total.total_time)
                    ]
            info = f"NM= {calculo_total.nivel_max} - Nm= {calculo_total.nivel_min} - Q= {calculo_total.caudal_objetivo} - Déficit= {round(calculo_total.falla,2)} "
            self.info.append(info)
            self.dicts.append(calculo_total.duracion_data)
            self.duracion_acumulada.append(calculo_total.duracion_data['Duracion Acumulada'])
            self.caudales.append(calculo_total.duracion_data['Caudal'])
            self.resultados.append(resultado)
            self.total_data.append(calculo_total.total_data)
            self.niveles.append(calculo_total.niveles)
            self.tiempos.append(calculo_total.tiempos)
            print(resultado,'\n')

    def duracion(self):
        create_plot(self.duracion_acumulada,self.caudales,self.info, 'Curva Duración','Duración[%]','Q[m³/s]','')
        
    def grafico_niveles(self):
        for i in range(len(self.niveles)):
            create_plot(self.tiempos[i],self.niveles[i],["Nivel","Nivel min","Nivel max"], 'Niveles','Tiempo [días]','Niveles [m]','')

    def exportar_excel(self):
        for dict in self.dicts:
            index = self.dicts.index(dict)
            export_excel(dict,f"Duracion - {self.info[index]}")
            export_excel(self.total_data[index],f"Embalse Caudal Constante - {self.info[index]}")
            