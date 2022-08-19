import sys
import os
import time

# IMPORT MODULES QT
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal
from ThreadCaudalConstante import *
from ThreadEnergia import *
from ThreadEnergiaNivelVariable import *

# Main Window Class
class MainWindow(QObject):
    def __init__(self,):
        QObject.__init__(self)
        self.myThread = []

    # Signals to send Data
    #--------------------------------------------------------
    #--------------------- CAUDAL CONSTANTE -----------------

    # CAUDAL CONSTANTE: CALCULO TOTAL
    signalResultadosTotalCC = Signal(list)
    signalErrorTotalCC = Signal(str)
    signalFinishCC = Signal(str)

    # CAUDAL CONSTANTE: CALCULO FALLA
    signalResultadosFallaCC = Signal(list)
    signalErrorFallaCC = Signal(str)

    # CAUDAL CONSTANTE: CURVA GARANTIA
    signalResultadosGarantiaCC = Signal(list)
    signalErrorGarantiaCC = Signal(str)

    #--------------------------------------------------------
    #--------------------- CALCULO ENERGIA -----------------

    # CALCULO ENERGIA: CALCULO TOTAL
    signalResultadosTotalEN = Signal(list)
    signalErrorTotalEN = Signal(str)
    signalFinishEN = Signal(str)

    # CALCULO ENERGIA: CALCULO FALLA
    signalResultadosFallaEN = Signal(list)
    signalErrorFallaEN = Signal(str)

    # CALCULO ENERGIA: CURVA GARANTIA
    signalResultadosGarantiaEN = Signal(list)
    signalErrorGarantiaEN = Signal(str)

    #--------------------------------------------------------
    #---------CALCULO ENERGIA NIVEL VARIABLE -----------------

    # CALCULO ENERGIA NIVEL VARIABLE: CALCULO TOTAL
    signalResultadosTotalENNV = Signal(list)
    signalErrorTotalENNV = Signal(str)
    signalFinishENNV = Signal(str)

    # CALCULO ENERGIA NIVEL VARIABLE: CALCULO FALLA
    signalResultadosFallaENNV = Signal(list)
    signalErrorFallaENNV = Signal(str)

    # CALCULO ENERGIA NIVEL VARIABLE: CURVA GARANTIA
    signalResultadosGarantiaENNV = Signal(list)
    signalErrorGarantiaENNV = Signal(str)


    #----------- CAUDAL CONSTANTE -------------------------------

    # ---------- CAUDAL CONSTANTE: CALCULO TOTAL ---------------

    @Slot(list)
    def calculo_total_cc(self,data):
        print(data)
        self.thread_calculo_total = ThreadCalculoTotalCC(data)
        self.thread_calculo_total.start()
        self.thread_calculo_total.resultado.connect(self.show_total_cc)
        self.thread_calculo_total.error.connect(self.signalErrorTotalCC.emit)
    
    def show_total_cc(self,info):
        self.calculos_totales = info
        self.signalResultadosTotalCC.emit(self.calculos_totales.resultados)
        self.signalFinishCC.emit("total")

    @Slot()
    def curva_duracion_total_cc(self):
        #self.calculos_totales.duracion()
        self.thread_calculo_total.duracion()
    
    @Slot()
    def stop_total_cc(self):
        self.thread_calculo_total.terminate()
    @Slot()
    def export_excel_total_cc(self):
        self.calculos_totales.exportar_excel()

    # ---------- CAUDAL CONSTANTE: CALCULO FALLA ---------------

    @Slot(list)
    def calculo_falla_cc(self,data):
        print(data)
        self.thread_calculo_falla = ThreadCalculoFallaCC(data)
        self.thread_calculo_falla.start()
        self.thread_calculo_falla.resultado.connect(self.show_falla_cc)
        self.thread_calculo_falla.error.connect(self.signalErrorFallaCC.emit)
    
    def show_falla_cc(self,info):
        self.calculo_falla = info
        self.signalResultadosFallaCC.emit(self.calculo_falla.resultados)
        self.signalFinishCC.emit("falla")

    @Slot()
    def curva_duracion_falla_cc(self):
        self.calculo_falla.duracion()
    @Slot()
    def stop_falla_cc(self):
        self.thread_calculo_falla.terminate()
    @Slot()
    def export_excel_falla_cc(self):
        self.calculo_falla.exportar_excel()

    # ---------- CAUDAL CONSTANTE: CURVA GARANTIA ---------------

    @Slot(list)
    def calculo_garantia_cc(self,data):
        print(data)
        self.thread_curva_garantia = ThreadCurvaGarantiaCC(data)
        self.thread_curva_garantia.start()
        self.thread_curva_garantia.resultado.connect(self.show_garantia_cc)
        self.thread_curva_garantia.error.connect(self.signalErrorGarantiaCC.emit)
    
    def show_garantia_cc(self,info):
        self.curva_garantia = info
        self.signalResultadosGarantiaCC.emit(self.curva_garantia.resultados)
        self.signalFinishCC.emit("garantia")
        

    @Slot()
    def curva_garantia_cc(self):
        self.curva_garantia.curva_garantia()
    @Slot()
    def stop_garantia_cc(self):
        self.thread_curva_garantia.terminate()
    @Slot()
    def export_excel_garantia_cc(self):
        self.curva_garantia.exportar_excel()

    #---------------------------------------------------------------------------------------------
    #---------------------------------    ENERGIA     -------------------------------------
    #---------------------------------------------------------------------------------------------

    # ---------- CALCULO ENERGIA: CALCULO TOTAL ---------------
    @Slot(list)
    def calculo_total_en(self,data):
        print(data)
        self.thread_calculo_total = ThreadCalculoTotalEN(data)
        self.thread_calculo_total.start()
        self.thread_calculo_total.resultado.connect(self.show_total_en)
        self.thread_calculo_total.error.connect(self.signalErrorTotalEN.emit)
    
    def show_total_en(self,info):
        self.calculo_total = info
        self.signalResultadosTotalEN.emit(self.calculo_total.resultados)
        self.signalFinishEN.emit("total")

    @Slot()
    def curva_duracion_total_en(self):
        self.calculo_total.duracion()
    
    @Slot()
    def stop_total_en(self):
        self.thread_calculo_total.terminate()
    @Slot()
    def export_excel_total_en(self):
        self.calculo_total.exportar_excel()

    # ---------- CALCULO ENERGIA: CALCULO FALLA ---------------

    @Slot(list)
    def calculo_falla_en(self,data):
        print(data)
        self.thread_calculo_falla = ThreadCalculoFallaEN(data)
        self.thread_calculo_falla.start()
        self.thread_calculo_falla.resultado.connect(self.show_falla_en)
        self.thread_calculo_falla.error.connect(self.signalErrorFallaEN.emit)
    
    def show_falla_en(self,info):
        self.calculo_falla = info
        self.signalResultadosFallaEN.emit(self.calculo_falla.resultados)
        self.signalFinishEN.emit("falla")

    @Slot()
    def curva_duracion_falla_en(self):
        self.calculo_falla.duracion()
    @Slot()
    def stop_falla_en(self):
        self.thread_calculo_falla.terminate()
    @Slot()
    def export_excel_falla_en(self):
        self.calculo_falla.exportar_excel()

    # ---------- CALCULO ENERGIA: CURVA GARANTIA ---------------

    @Slot(list)
    def calculo_garantia_en(self,data):
        print(data)
        self.thread_curva_garantia = ThreadCurvaGarantiaEN(data)
        self.thread_curva_garantia.start()
        self.thread_curva_garantia.resultado.connect(self.show_garantia_en)
        self.thread_curva_garantia.error.connect(self.signalErrorGarantiaEN.emit)
    
    def show_garantia_en(self,info):
        self.curva_garantia = info
        self.signalResultadosGarantiaEN.emit(self.curva_garantia.resultados)
        self.signalFinishEN.emit("garantia")

    @Slot()
    def curva_garantia_en(self):
        self.curva_garantia.curva_garantia()
    @Slot()
    def stop_garantia_en(self):
        self.thread_curva_garantia.terminate()
    @Slot()
    def export_excel_garantia_en(self):
        self.curva_garantia.exportar_excel()


    #---------------------------------------------------------------------------------------------
    #---------------------------------    ENERGIA NIVEL VARIABLE     -----------------------------
    #---------------------------------------------------------------------------------------------

    # ---------- CALCULO ENERGIA NIVEL VARIABLE: CALCULO TOTAL ---------------
    @Slot(list)
    def calculo_total_ennv(self,data):
        print(data)
        self.thread_calculo_total = ThreadCalculoTotalENNV(data)
        self.thread_calculo_total.start()
        self.thread_calculo_total.resultado.connect(self.show_total_ennv)
        self.thread_calculo_total.error.connect(self.signalErrorTotalENNV.emit)
    
    def show_total_ennv(self,info):
        self.calculo_total = info
        self.signalResultadosTotalENNV.emit(self.calculo_total.resultados)
        self.signalFinishENNV.emit("total")

    @Slot()
    def curva_duracion_total_ennv(self):
        self.calculo_total.duracion()
    
    @Slot()
    def stop_total_ennv(self):
        self.thread_calculo_total.terminate()
    @Slot()
    def export_excel_total_ennv(self):
        self.calculo_total.exportar_excel()

    # ---------- CALCULO ENERGIA NIVEL VARIABLE: CALCULO FALLA ---------------

    @Slot(list)
    def calculo_falla_ennv(self,data):
        print(data)
        self.thread_calculo_falla = ThreadCalculoFallaENNV(data)
        self.thread_calculo_falla.start()
        self.thread_calculo_falla.resultado.connect(self.show_falla_ennv)
        self.thread_calculo_falla.error.connect(self.signalErrorFallaENNV.emit)
    
    def show_falla_ennv(self,info):
        self.calculo_falla = info
        self.signalResultadosFallaENNV.emit(self.calculo_falla.resultados)
        self.signalFinishENNV.emit("falla")

    @Slot()
    def curva_duracion_falla_ennv(self):
        self.calculo_falla.duracion()
    @Slot()
    def stop_falla_ennv(self):
        self.thread_calculo_falla.terminate()
    @Slot()
    def export_excel_falla_ennv(self):
        self.calculo_falla.exportar_excel()

    # ---------- CALCULO ENERGIA NIVEL VARIABLE: CURVA GARANTIA ---------------

    @Slot(list)
    def calculo_garantia_ennv(self,data):
        print(data)
        self.thread_curva_garantia = ThreadCurvaGarantiaENNV(data)
        self.thread_curva_garantia.start()
        self.thread_curva_garantia.resultado.connect(self.show_garantia_ennv)
        self.thread_curva_garantia.error.connect(self.signalErrorGarantiaENNV.emit)
    
    def show_garantia_ennv(self,info):
        self.curva_garantia = info
        self.signalResultadosGarantiaENNV.emit(self.curva_garantia.resultados)
        self.signalFinishENNV.emit("garantia")

    @Slot()
    def curva_garantia_ennv(self):
        self.curva_garantia.curva_garantia()
    @Slot()
    def stop_garantia_ennv(self):
        self.thread_curva_garantia.terminate()
    @Slot()
    def export_excel_garantia_ennv(self):
        self.curva_garantia.exportar_excel()

# INSTANCE CLASS
if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Get Context
    main = MainWindow()
    engine.rootContext().setContextProperty("backend", main)

    # Load QML File
    engine.load(os.path.join(os.path.dirname(__file__),"qml/main.qml"))

    # CHECK EXIT APP
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
    
    """ from MyUtils.modules.ENERGIA_NIVEL_VARIABLE.CalculosTotales import CalculosTotales
    from MyUtils.modules.ENERGIA_NIVEL_VARIABLE.CalculosFallas import CalculosFallas
    from MyUtils.modules.ENERGIA_NIVEL_VARIABLE.CurvasGarantias import CurvasGarantias
    from MyUtils.modules.ENERGIA.CalculosFallas import CalculosFallas as CalculosFallasE
    from MyUtils.modules.ENERGIA.CalculoFallaPotencia import CalculoFalla as CalculoFallaE

    from MyUtils.modules.ENERGIA.CalculoTotal import CalculoTotal as CalculoTotalE
    #from MyUtils.modules.CAUDAL_CONSTANTE.CalculosTotales import CalculosTotales """

    """ calculo_total = CalculosTotales(
                input_data=extract_excel_data("input_energia_variable.xlsx"),
                nivel_min=[140],
                potencia_firme = [150],
                rendimiento = [0.9]
                ) """

    """ calculos_totales = CalculosFallas(
        extract_excel_data("input_energia_variable.xlsx"),
        falla_buscada=[2.65],
        nivel_min=[140],
        rendimiento=[0.9]
    ) """
    """ curva_garantia = CurvasGarantias(
                paso_calculo=[5],
                falla_buscada=[5],
                rendimiento = [0.9],
                nivel_min_limite=[140]
            )
    curva_garantia.curva_garantia() """

    """ calculos_totales = CalculosFallasE(
        extract_excel_data("input_energia.xlsx"),
        falla_buscada=[2.65],
        nivel_min=[140],
        nivel_max=[160],
        rendimiento=[0.9]
    ) """
    """ calculos_totales = CalculoFallaE(
        extract_excel_data("input_energia.xlsx"),
        falla_buscada=2.65,
        nivel_min=140,
        nivel_max=160,
        rendimiento=0.9
    ) """
    """ calculos_totales = CalculosTotales(
        extract_excel_data("input_caudal_constante.xlsx"),
        nivel_min=[140],
        nivel_max=[160],
        caudal_objetivo=[500]
    )
    #calculos_totales.exportar_excel()
    calculos_totales.grafico_niveles() """
