import os
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAbstractSpinBox

class VistaGestionEstadisticas(QMainWindow):
    
    def __init__(self, controladorGestionEstadisticas):
        super(VistaGestionEstadisticas, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/vistaGestionEstadisticas.ui"), self)

        self.controladorGestionEstadisticas = controladorGestionEstadisticas
        self.label.setText("Gestión de estadísticas curriculares")


    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)