import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog


class VistaActualizarPeriodo(QDialog):

    def __init__(self, controladorPrincipal):
        super(VistaActualizarPeriodo, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/actualizacionPeriodo.ui"), self)       

        self.button_cancel.clicked.connect(controladorPrincipal.mostrarVistaPrincipal)
        self.button_ok.clicked.connect(controladorPrincipal.actualizarPeriodo)

    def setErrorAno(self, texto):
        self.label_error_ano.setText(texto)

    def setErrorPeriodo(self, texto):
        self.label_error_periodo.setText(texto)

    def getAno(self):
        return self.input_ano.text()
    
    def getPeriodo(self):
        periodo = 0
        if self.radioButton_1.isChecked():
            periodo = 1
        elif self.radioButton_2.isChecked():
            periodo = 2
        return periodo


    def mostrarAlerta(self, titulo, texto):
        QMessageBox.information(self, titulo, texto)