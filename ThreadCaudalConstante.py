# IMPORT MODULES QT
from PySide6 import QtCore
from PySide6.QtCore import Signal


# IMPORT MODULES EMBALSE
from MyUtils.modules.CAUDAL_CONSTANTE.CalculoFallaCaudal import CalculoFalla
from MyUtils.modules.CAUDAL_CONSTANTE.CalculosFallas import CalculosFallas
from MyUtils.modules.CAUDAL_CONSTANTE.CalculosTotales import CalculosTotales
from MyUtils.modules.CAUDAL_CONSTANTE.CurvaGarantia import CurvaGarantia
from MyUtils.help import extract_excel_data
from MyUtils.modules.CAUDAL_CONSTANTE.CurvasGarantias import CurvasGarantias

class ThreadCalculoTotalCC(QtCore.QThread):

    # Signals to send Data
    resultado = Signal(object)
    error = Signal(str)

    def __init__(self,data):
        super(ThreadCalculoTotalCC, self).__init__()
        self.is_running = True
        self.nivel_min = data[0]
        self.nivel_max = data[1]
        self.caudal_objetivo = data[2]

    def run(self):
        print("Running new 'Calculo Falla'...")
        try:
            self.calculos_totales = CalculosTotales(
                input_data=extract_excel_data("input_caudal_constante.xlsx"),
                nivel_min=self.nivel_min,
                nivel_max=self.nivel_max,
                caudal_objetivo=self.caudal_objetivo
                )
            print("Emiting results...")
            self.resultado.emit(self.calculos_totales)
        except Exception as e:
            print(str(e))
            self.error.emit(str(e))
        #self.wait()
    def duracion(self):
        self.calculos_totales.duracion()

class ThreadCalculoFallaCC(QtCore.QThread):

    # Signals to send Data
    resultado = Signal(object)
    error = Signal(str)

    def __init__(self,data):
        super(ThreadCalculoFallaCC, self).__init__()
        self.is_running = True
        self.nivel_min = data[0]
        self.nivel_max = data[1]
        self.falla_buscada = data[2]
        print(self.nivel_min,self.nivel_max,self.falla_buscada)

    def run(self):
        print("Running new 'Calculo Falla'...")
        try:
            calculo_falla = CalculosFallas(
                input_data=extract_excel_data("input_caudal_constante.xlsx"),
                falla_buscada = self.falla_buscada,
                nivel_min = self.nivel_min,
                nivel_max=self.nivel_max
            )
            print("Emiting results...")
            self.resultado.emit(calculo_falla)
        except Exception as e:
            print(str(e))
            self.error.emit(str(e))
        self.quit()

class ThreadCurvaGarantiaCC(QtCore.QThread):

    # Signals to send Data
    resultado = Signal(object)
    error = Signal(str)

    def __init__(self,data):
        super(ThreadCurvaGarantiaCC, self).__init__()
        self.is_running = True
        self.nivel_min = data[0]
        self.falla_buscada = data[2]
        self.paso_calculo = data[3]
        if data[1][0] == 0:
            self.nivel_max_limite = [None]
        else:
            self.nivel_max_limite = data[1]

    def run(self):
        print("Running new 'Calculo Falla'...")
        """ curva_garantia = CurvasGarantias(
            paso_calculo=self.paso_calculo,
            falla_buscada=self.falla_buscada,
            nivel_min=self.nivel_min,
            nivel_max_limite=self.nivel_max_limite
        ) """

        try:
            curva_garantia = CurvasGarantias(
                paso_calculo=self.paso_calculo,
                falla_buscada=self.falla_buscada,
                nivel_min=self.nivel_min,
                nivel_max_limite=self.nivel_max_limite
            )
            print("Emiting results...")
            self.resultado.emit(curva_garantia)
        except Exception as e:
            print(str(e))
            self.error.emit(str(e))
        self.quit()