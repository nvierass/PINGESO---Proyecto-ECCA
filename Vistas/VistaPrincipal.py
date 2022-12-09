import os
from PyQt5 import uic, QtWidgets
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

        self.ano = 2022
        self.periodo = 2

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)

    def mostrarPlanesRegistrados(self):
        aux = 0

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
            self.gridLayout.addWidget(self.boton, columna, fila)
            self.boton.setText(nombre+"\n"+version)
            self.boton.clicked.connect(partial(self.controladorPrincipal.goMallaInteractiva,planesRegistrados[index], self.ano, self.periodo))
            columna = columna + 1
""" 


        for index in planesRegistrados:
            plan = planesRegistrados[index]
            referenciaBotonPlan = self.agregarBotonPlan(plan)
            self.controladorPrincipal 

            
    def agregarBotonPlan(self,plan):

        self.button_name.clicked.connect()
"""
        