import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class VistaRegistroPlan(QMainWindow):

    def __init__(self, controladorRegistroPlan):
        super(VistaRegistroPlan, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/registrar_plan.ui"), self)

        self.controladorRegistroPlan = controladorRegistroPlan

        self.button_home.clicked.connect(self.controladorRegistroPlan.volverContextoPrincipal)
        self.button_registrar_asignatura.clicked.connect(self.controladorRegistroPlan.mostrarVistaRegistroAsignatura)

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)