from PyQt5 import QtWidgets

from Vistas.VistaLecturaPlanilla import VistaLecturaPlanilla

class ControladorLecturaPlanilla():

    def __init__(self, controladorPrincipal, databaseContext, GUI):
        self.GUI = GUI
        self.databaseContext = databaseContext
        self.controladorPrincipal = controladorPrincipal

        self.vistaLecturaPlanilla = VistaLecturaPlanilla(self)

        self.mostrarVistaLecturaPlanilla()
        

    def mostrarVistaLecturaPlanilla(self):
        self.GUI.addWidget(self.vistaLecturaPlanilla)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)

    def volverContextoPrincipal(self):
        self.controladorPrincipal.mostrarVistaPrincipal()

    def ingresarPlanilla(self):
        print("Inicio guardado")




        self.vistaLecturaPlanilla.mostrarAlerta("Ingreso exitoso", "Se ha ingresado correctamente la información de la planificación semestral. ")
        self.volverContextoPrincipal()