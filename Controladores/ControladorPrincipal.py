import sys

from PyQt5 import QtWidgets

from Vistas.VistaPrincipal import VistaPrincipal
from Controladores.ControladorRegistroPlan import ControladorRegistroPlan
from Controladores.ControladorLecturaPlanilla import ControladorLecturaPlanilla
from Controladores.ControladorEstimacion import ControladorEstimacion
from Controladores.ControladorMallaInteractiva import ControladorMallaInteractiva
from DatabaseDriver.DatabaseContext import DatabaseContext

class ControladorPrincipal():

    def __init__(self, GUI):
        self.GUI = GUI
        self.databaseContext = DatabaseContext()
        self.vistaPrincipal = VistaPrincipal(self)
        if self.databaseContext.conn == None:
            self.vistaPrincipal.mostrarAlerta("Error","No se ha establecido una conexión a la base de datos.\nFinalizando ejecución.")
            sys.exit()
        self.iniciarVistaPrincipal()

    def iniciarVistaPrincipal(self):
        planesRegistrados = self.databaseContext.obtenerPlanes()
        self.vistaPrincipal.setPlanesRegitrados(planesRegistrados)
        self.GUI.addWidget(self.vistaPrincipal)
        self.GUI.show()

    def mostrarVistaPrincipal(self):
        self.GUI.addWidget(self.vistaPrincipal)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)

    def goRegistroPlan(self):
        self.controladorRegistroPlan  = ControladorRegistroPlan(self, self.databaseContext, self.GUI)

    def goLecturaPlanilla(self):
        self.controladorLecturaPlanilla = ControladorLecturaPlanilla(self, self.databaseContext, self.GUI)

    def goEstimacion(self):
        self.controladorEstimacion = ControladorEstimacion(self, self.databaseContext, self.GUI)

    def goMallaInteractiva(self, PlanSeleccionado, ano, periodo):
        self.controladorMallaInteractiva = ControladorMallaInteractiva(self.databaseContext, self.GUI, PlanSeleccionado,ano,periodo)
