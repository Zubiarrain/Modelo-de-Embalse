from MyUtils.help import create_plot, export_excel
from .CurvaGarantia import CurvaGarantia


class CurvasGarantias:

    def __init__(self,paso_calculo,falla_buscada,nivel_min,nivel_max_limite=[None]):
        # ------------ INIT VARS ------------------

        self.paso_calculo = paso_calculo
        self.nivel_min = nivel_min
        self.nivel_max_limite = nivel_max_limite
        self.falla_buscada = falla_buscada

        # ------------ DATA ------------------
        self.calculos_totales = []
        self.niveles_maximos = []
        self.resultados = []
        self.info = []
        self.caudales = []
        self.data = []

        # ------------ CALC ------------------
        self.calculo()
        
    def calculo(self):

        variables = [self.paso_calculo,self.nivel_min,self.nivel_max_limite,self.falla_buscada]
        rango = [len(self.paso_calculo),len(self.nivel_min),len(self.nivel_max_limite),len(self.falla_buscada)]
        casos = max(rango)

        for i in range(casos):
            datos=[self.paso_calculo[0],self.nivel_min[0],self.nivel_max_limite[0],self.falla_buscada[0]]
            for variable in variables:
                if len(variable) != 1:
                    index = variables.index(variable)
                    datos[index] = variable[i]
            curva_garantia = CurvaGarantia(
                paso_calculo=datos[0],
                falla_buscada=datos[3],
                nivel_min=datos[1],
                nivel_max_limite=datos[2]
            )
            self.calculos_totales.append(curva_garantia)
            resultado = [
                    "Déficit [%]: " + str(curva_garantia._falla_buscada),
                    "Nivel Mínimo [m]: " + str(curva_garantia._nivel_min),
                    "Tiempo de corrida [min]: " + str(curva_garantia.tiempo_corrida_minutos)
                    ]
            for i in range(len(curva_garantia.data["Caudales"])):
                text = f"Caudal [m³/s]: {curva_garantia.data['Caudales'][i]} - Nivel Máximo [m]: {curva_garantia.data['Niveles max'][i]} - Iteraciones: {curva_garantia.iteraciones_falla[i]} "
                resultado.append(text)

            self.data.append(curva_garantia.data)
            self.caudales.append(curva_garantia.data["Caudales"])
            self.niveles_maximos.append(curva_garantia.data["Niveles max"])
            info = f"Nm= {curva_garantia._nivel_min} - Déficit= {curva_garantia._falla_buscada} "
            self.info.append(info)
            self.resultados.append(resultado)

    def curva_garantia(self):
        create_plot(self.caudales,self.niveles_maximos,self.info,'Garantía','Q objetivo [m³/s]','NMN [m]','o')
        
    def exportar_excel(self):
        for dict in self.data:
            index = self.data.index(dict)
            export_excel(dict,f"Garantia - {self.info[index]}")
            