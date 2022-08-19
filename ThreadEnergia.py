# IMPORT MODULES QT
from PySide6 import QtCore
from PySide6.QtCore import Signal


# IMPORT MODULES EMBALSE
from MyUtils.modules.ENERGIA.CalculosFallas import CalculosFallas
from MyUtils.modules.ENERGIA.CalculosTotales import CalculosTotales
from MyUtils.modules.ENERGIA.CurvasGarantias import CurvasGarantias
from MyUtils.help import extract_excel_data

class ThreadCalculoTotalEN(QtCore.QThread):

    # Signals to send Data
    resultado = Signal(object)
    error = Signal(str)

    def __init__(self,data):
        super(ThreadCalculoTotalEN, self).__init__()
        self.is_running = True
        self.nivel_min = data[0]
        self.nivel_max = data[1]
        self.potencia_firme = data[2]
        self.rendimiento = data[3]

    def run(self):
        print("Running new 'Calculo Falla'...")
        try:
            calculo_total = CalculosTotales(
                input_data=extract_excel_data("input_energia.xlsx"),
                nivel_min=self.nivel_min,
                nivel_max=self.nivel_max,
                potencia_firme = self.potencia_firme,
                rendimiento = self.rendimiento
                )
            print("Emiting results...")
            self.resultado.emit(calculo_total)
        except Exception as e:
            print(str(e))
            self.error.emit(str(e))
        self.quit()

class ThreadCalculoFallaEN(QtCore.QThread):

    # Signals to send Data
    resultado = Signal(object)
    error = Signal(str)

    def __init__(self,data):
        super(ThreadCalculoFallaEN, self).__init__()
        self.is_running = True
        self.nivel_min = data[0]
        self.nivel_max = data[1]
        self.falla_buscada = data[2]
        self.rendimiento = data[3]

    def run(self):
        print("Running new 'Calculo Falla'...")
        try:
            calculo_falla = CalculosFallas(
                input_data=extract_excel_data("input_energia.xlsx"),
                falla_buscada = self.falla_buscada,
                nivel_min = self.nivel_min,
                nivel_max=self.nivel_max,
                rendimiento = self.rendimiento
            )
            print("Emiting results...")
            self.resultado.emit(calculo_falla)
        except Exception as e:
            print(str(e))
            self.error.emit(str(e))
        self.quit()

class ThreadCurvaGarantiaEN(QtCore.QThread):

    # Signals to send Data
    resultado = Signal(object)
    error = Signal(str)

    def __init__(self,data):
        super(ThreadCurvaGarantiaEN, self).__init__()
        self.is_running = True
        self.nivel_max = data[0]
        self.falla_buscada = data[2]
        self.paso_calculo = data[3]
        self.rendimiento = data[4]

        if data[1][0] == 0:
            self.nivel_min_limite = [None]
        else:
            self.nivel_min_limite = data[1]

    def run(self):
        print("Running new 'Calculo Falla'...")
        try:
            curva_garantia = CurvasGarantias(
                paso_calculo=self.paso_calculo,
                falla_buscada=self.falla_buscada,
                nivel_max=self.nivel_max,
                rendimiento = self.rendimiento,
                nivel_min_limite=self.nivel_min_limite
            )
            print("Emiting results...")
            self.resultado.emit(curva_garantia)
        except Exception as e:
            print(str(e))
            self.error.emit(str(e))
        self.quit()