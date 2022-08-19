from MyUtils.help import create_plot, export_excel
from .CurvaGarantia import CurvaGarantia


class CurvasGarantias:

    def __init__(self,paso_calculo,falla_buscada,nivel_max,rendimiento,nivel_min_limite=[None]):
        # ------------ INIT VARS ------------------

        self.paso_calculo = paso_calculo
        self.nivel_max = nivel_max
        self.nivel_min_limite = nivel_min_limite
        self.falla_buscada = falla_buscada
        self.rendimiento = rendimiento

        # ------------ DATA ------------------
        self.calculos_totales = []
        self.niveles_minimos = []
        self.resultados = []
        self.info = []
        self.potencias = []
        self.data = []

        # ------------ CALC ------------------
        self.calculo()
        
    def calculo(self):

        variables = [self.paso_calculo,self.nivel_max,self.nivel_min_limite,self.falla_buscada,self.rendimiento]
        rango = [len(self.paso_calculo),len(self.nivel_max),len(self.nivel_min_limite),len(self.falla_buscada),len(self.rendimiento)]
        casos = max(rango)

        for i in range(casos):
            datos=[self.paso_calculo[0],self.nivel_max[0],self.nivel_min_limite[0],self.falla_buscada[0],self.rendimiento[0]]
            for variable in variables:
                if len(variable) != 1:
                    index = variables.index(variable)
                    datos[index] = variable[i]
            curva_garantia = CurvaGarantia(
                paso_calculo=datos[0],
                falla_buscada=datos[3],
                nivel_max=datos[1],
                rendimiento=datos[4],
                nivel_min_limite=datos[2]
            )
            self.calculos_totales.append(curva_garantia)
            resultado = [
                    "Déficit [%]: " + str(curva_garantia._falla_buscada),
                    "Nivel Máximo [m]: " + str(curva_garantia._nivel_max),
                    "Tiempo de corrida [min]: " + str(curva_garantia.tiempo_corrida_minutos)
                    ]
            for i in range(len(curva_garantia.data["Potencias"])):
                text = f"Energía Firme [GWh]: {curva_garantia.data['Energias'][i]} - Potencia Firme [MW]: {curva_garantia.data['Potencias'][i]} - Nivel Mínimo [m]: {curva_garantia.data['Niveles min'][i]} - Iteraciones: {curva_garantia.iteraciones_falla[i]} "
                resultado.append(text)

            self.data.append(curva_garantia.data)
            self.potencias.append(curva_garantia.data["Potencias"])
            self.niveles_minimos.append(curva_garantia.data["Niveles min"])
            info = f"NM= {curva_garantia._nivel_max} - Déficit= {curva_garantia._falla_buscada} "
            self.info.append(info)
            self.resultados.append(resultado)

    def curva_garantia(self):
        create_plot(self.potencias,self.niveles_minimos,self.info,'Garantía','P firme [MW]','NmN [m]','o')
        
    def exportar_excel(self):
        for dict in self.data:
            index = self.data.index(dict)
            export_excel(dict,f"Pot-NmN - {self.info[index]}")
            