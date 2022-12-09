import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class VistaRegistroAsignatura(QMainWindow):

    def __init__(self, controladorRegistroPlan):
        super(VistaRegistroAsignatura, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/registrar_asignatura.ui"), self)

        self.controladorRegistroPlan = controladorRegistroPlan

        self.button_volver.clicked.connect(self.controladorRegistroPlan.mostrarVistaRegistroPlan)

        
    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)