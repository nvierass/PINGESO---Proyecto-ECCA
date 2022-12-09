import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class VistaCupos(QMainWindow):
    
    def __init__(self, controladorEstimacion):
        super(VistaCupos, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/cupos.ui"), self)

        self.controladorEstimacion = controladorEstimacion

        self.button_home.clicked.connect(controladorEstimacion.volverContextoPrincipal)
        self.button_estimar.clicked.connect(controladorEstimacion.mostrarVistaResultados)

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)