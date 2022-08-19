# IMPORT MODULES QT
from PySide6 import QtCore
from PySide6.QtCore import Signal


# IMPORT MODULES EMBALSE
from MyUtils.modules.ENERGIA_NIVEL_VARIABLE.CalculosFallas import CalculosFallas
from MyUtils.modules.ENERGIA_NIVEL_VARIABLE.CalculosTotales import CalculosTotales
from MyUtils.modules.ENERGIA_NIVEL_VARIABLE.CurvasGarantias import CurvasGarantias
from MyUtils.help import extract_excel_data

class ThreadCalculoTotalENNV(QtCore.QThread):

    # Signals to send Data
    resultado = Signal(object)
    error = Signal(str)

    def __init__(self,data):
        super(ThreadCalculoTotalENNV, self).__init__()
        self.is_running = True
        self.nivel_min = data[0]
        self.potencia_firme = data[1]
        self.rendimiento = data[2]

    def run(self):
        print("Running new 'Calculo Falla'...")
        try:
            calculo_total = CalculosTotales(
                input_data=extract_excel_data("input_energia_variable.xlsx"),
                nivel_min=self.nivel_min,
                potencia_firme = self.potencia_firme,
                rendimiento = self.rendimiento
                )
            print("Emiting results...")
            self.resultado.emit(calculo_total)
        except Exception as e:
            print(str(e))
            self.error.emit(str(e))
        self.quit()

class ThreadCalculoFallaENNV(QtCore.QThread):

    # Signals to send Data
    resultado = Signal(object)
    error = Signal(str)

    def __init__(self,data):
        super(ThreadCalculoFallaENNV, self).__init__()
        self.is_running = True
        self.nivel_min = data[0]
        self.falla_buscada = data[1]
        self.rendimiento = data[2]

    def run(self):
        print("Running new 'Calculo Falla'...")
        try:
            calculo_falla = CalculosFallas(
                input_data=extract_excel_data("input_energia_variable.xlsx"),
                falla_buscada = self.falla_buscada,
                nivel_min = self.nivel_min,
                rendimiento = self.rendimiento
            )
            print("Emiting results...")
            self.resultado.emit(calculo_falla)
        except Exception as e:
            print(str(e))
            self.error.emit(str(e))
        self.quit()

class ThreadCurvaGarantiaENNV(QtCore.QThread):

    # Signals to send Data
    resultado = Signal(object)
    error = Signal(str)

    def __init__(self,data):
        super(ThreadCurvaGarantiaENNV, self).__init__()
        self.is_running = True
        self.falla_buscada = data[1]
        self.paso_calculo = data[2]
        self.rendimiento = data[3]

        if data[0][0] == 0:
            self.nivel_min_limite = [None]
        else:
            self.nivel_min_limite = data[0]

    def run(self):
        print("Running new 'Calculo Falla'...")
        try:
            curva_garantia = CurvasGarantias(
                paso_calculo=self.paso_calculo,
                falla_buscada=self.falla_buscada,
                rendimiento = self.rendimiento,
                nivel_min_limite=self.nivel_min_limite
            )
            print("Emiting results...")
            self.resultado.emit(curva_garantia)
        except Exception as e:
            print(str(e))
            self.error.emit(str(e))
        self.quit()