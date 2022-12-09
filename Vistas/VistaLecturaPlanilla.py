import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QFileDialog


class VistaLecturaPlanilla(QDialog):

    def __init__(self, controladorLecturaPlanilla):
        super(VistaLecturaPlanilla, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/load.ui"), self)

        self.controladorLecturaPlanilla = controladorLecturaPlanilla

        self.button_examinar.clicked.connect(self.examinarArchivo)
        self.button_cancel.clicked.connect(self.controladorLecturaPlanilla.volverContextoPrincipal)
        self.button_ok.clicked.connect(self.controladorLecturaPlanilla.ingresarPlanilla)


    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)

    def examinarArchivo(self):
        fname = QFileDialog.getOpenFileName(self, "Cargar Archivo", "", "Planillas Excel (*.xls*)")
        if fname:
            self.input_archivo.setText(fname[0])

    def getAnoEstimacion(self):
        return self.input_ano.text()

    def getPeriodoEstimacion(self):
        periodoSeleccionado = 0
        if self.radioButton_1.isChecked():
            periodoSeleccionado = 1
        if self.radioButton_2.isChecked():
            periodoSeleccionado = 2
        return periodoSeleccionado

    def getNombreArchivo(self):
        return self.input_archivo.text()
    
    def setErrorAno(self,texto):
        self.label_error_ano.setText(texto)

    def setErrorPeriodo(self,texto):
        self.label_error_periodo.setText(texto)

    def setErrorNombreArchivo(self,texto):
        self.label_error_archivo.setText(texto)