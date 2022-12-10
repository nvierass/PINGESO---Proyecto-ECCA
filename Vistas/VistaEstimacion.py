import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog


class VistaEstimacion(QDialog):

    def __init__(self, controladorEstimacion):
        super(VistaEstimacion, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/estimar.ui"), self)       

        self.button_cancel.clicked.connect(controladorEstimacion.volverContextoPrincipal)
        self.button_ok.clicked.connect(controladorEstimacion.inicializarEstimacion)

    def setErrorAno(self,texto):
        self.label_error_ano.setText(texto)

    def setErrorPlan(self,texto):
        self.label_error_plan.setText(texto)

    def setErrorPeriodo(self,texto):
        self.label_error_periodo.setText(texto)

    def setErrorTipoEstimacion(self,texto):
        self.label_error_tipo_estimacion.setText(texto)

    def setErrorPonderaciones(self,texto):
        self.label_error_datos_historicos.setText(texto)

    def getAno(self):
        return self.input_ano.text()
    
    def getPeriodo(self):
        periodo = 0
        if self.radioButton_1.isChecked():
            periodo = 1
        elif self.radioButton_2.isChecked():
            periodo = 2
        return periodo

    def getTipoEstimacion(self):
        tipoEstimacion = 0
        if self.radioButton_3.isChecked():
            tipoEstimacion = 1
        elif self.radioButton_4.isChecked():
            tipoEstimacion = 2
        return tipoEstimacion

    def getPonderacionValoresHistoricos(self):
        return self.input_datos_historicos.text()

    def getPonderacionValoresPeriodoAnterior(self):
        return self.input_datos_periodo_anterior.text()
        

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)
