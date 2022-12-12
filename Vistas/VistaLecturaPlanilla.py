import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog


class VistaLecturaPlanilla(QMainWindow):

    def __init__(self, controladorLecturaPlanilla):
        super(VistaLecturaPlanilla, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/load.ui"), self)

        self.controladorLecturaPlanilla = controladorLecturaPlanilla

        self.button_examinar.clicked.connect(self.examinarArchivo)
        self.button_cancel.clicked.connect(self.controladorLecturaPlanilla.volverContextoPrincipal)
        self.button_ok.clicked.connect(self.controladorLecturaPlanilla.iniciarIngresoPlanilla)


    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)

    def examinarArchivo(self):
        fname = QFileDialog.getOpenFileName(self, "Cargar Archivo", "", "Planillas Excel (*.xls*)")
        if fname:
            self.input_archivo.setText(fname[0])

    def getAno(self):
        return self.input_ano.text()

    def getSemestre(self):
        semestre = 0
        if self.radioButton_1.isChecked():
            semestre = 1
        if self.radioButton_2.isChecked():
            semestre = 2
        return semestre

    def getNombreArchivo(self):
        return self.input_archivo.text()
    
    def setErrorAno(self,texto):
        self.label_error_ano.setText(texto)

    def setErrorPeriodo(self,texto):
        self.label_error_periodo.setText(texto)

    def setErrorNombreArchivo(self,texto):
        self.label_error_archivo.setText(texto)
