import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class VistaMalla(QMainWindow):

    def __init__(self, controladorMallaInteractiva):
        super(VistaMalla, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/malla.ui"), self)



    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)