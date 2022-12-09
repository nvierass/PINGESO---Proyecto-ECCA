import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog

class VistaResultados(QMainWindow):

    def __init__(self, controladorEstimacion):
        super(VistaResultados, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/table.ui"), self)

        self.controladorEstimacion = controladorEstimacion

        self.button_home.clicked.connect(self.controladorEstimacion.volverContextoPrincipal)
        self.button_exportar.clicked.connect(self.controladorEstimacion.exportarResultados)

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)

    def getPathResultados(self):
        option = QFileDialog.Options()
        fname = QFileDialog.getSaveFileName(self, "Exportar archivo", "Resultados Estimación", "Planilla Excel (*.xlsx);;Todos los archivos (*)", options=option)[0]
        return fname
            

    def setTitulo(self, titulo):
        self.titulo = titulo