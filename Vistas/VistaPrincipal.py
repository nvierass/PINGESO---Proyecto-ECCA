import os
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from functools import partial

class VistaPrincipal(QMainWindow):
  
    def __init__(self, controladorPrincipal):
        super(VistaPrincipal, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/main.ui"), self)

        self.controladorPrincipal = controladorPrincipal

        self.button_registrar.clicked.connect(self.controladorPrincipal.goRegistroPlan)
        self.button_cargar.clicked.connect(self.controladorPrincipal.goLecturaPlanilla)
        self.button_estimar.clicked.connect(self.controladorPrincipal.goEstimacion)
        self.button_actualizar_periodo.clicked.connect(self.controladorPrincipal.goActualizacion)
        self.button_gestion_estadisticas.clicked.connect(self.controladorPrincipal.goGestionEstadisticas)
        self.ano = 0
        self.periodo = 0

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)
    
    def actualizarTitulo(self):
        titulo = "Periodo actual: ("+ str(self.ano) + "-" + str(self.periodo) + ")"
        self.label_titulo.setText(titulo)

    def setPlanesRegitrados(self, planesRegistrados):
        fila = 0
        columna = 0
        for index in planesRegistrados:
            if columna > 2:
                fila = fila + 1
                columna = 0
            id = planesRegistrados[index].getId()
            nombre = planesRegistrados[index].getNombre()
            version = planesRegistrados[index].getVersion() 
            self.boton = QtWidgets.QPushButton()
            self.boton.setObjectName("plan_"+str(id))
            self.boton.setMinimumSize(QtCore.QSize(0, 100))
            self.boton.setMaximumSize(QtCore.QSize(16777215, 60)) 
            self.gridLayout.addWidget(self.boton, fila, columna) 
            self.boton.setText(nombre+"\n"+version)
            self.boton.clicked.connect(partial(self.controladorPrincipal.goMallaInteractiva,planesRegistrados[index]))
            columna = columna + 1

    def setAno(self, ano):
        self.ano = ano

    def setSemestre(self, semestre):
        self.periodo = semestre