import xlsxwriter as xl
import math
import sys

from Vistas.VistaGestionEstadisticas import VistaGestionEstadisticas

class ControladorGestionEstadisticas():

    def __init__(self, controladorPrincipal, databaseContext, GUI):
        self.GUI = GUI
        self.databaseContext = databaseContext
        self.controladorPrincipal = controladorPrincipal

        self.vistaGestionEstadisticas = VistaGestionEstadisticas(self)
        self.mostrarVistaGestionEstadisticas()

        self.asignaturas = self.databaseContext.obtenerAsignaturas()
        if self.asignaturas == None:
            self.vistaEstimacion.mostrarAlerta("Error", "Error en la conexión a la base de datos, el programa terminará su ejecución inmediatamente.")
            sys.exit()


    def mostrarVistaGestionEstadisticas(self):
        self.GUI.addWidget(self.vistaGestionEstadisticas)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)