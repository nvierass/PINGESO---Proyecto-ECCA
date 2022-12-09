from Vistas.VistaRegistroPlan import VistaRegistroPlan
from Vistas.VistaRegistroAsignatura import VistaRegistroAsignatura

class ControladorRegistroPlan():

    def __init__(self, controladorPrincipal, databaseContext, GUI):
        self.GUI = GUI
        self.databaseContext = databaseContext
        self.controladorPrincipal = controladorPrincipal

        self.vistaRegistroPlan = VistaRegistroPlan(self)
        self.vistaRegistroAsignatura = VistaRegistroAsignatura(self)

        self.mostrarVistaRegistroPlan()
        

    def mostrarVistaRegistroPlan(self):
        self.GUI.addWidget(self.vistaRegistroPlan)
        self.GUI.setCurrentIndex(self.GUI.currentIndex() + 1)

    def mostrarVistaRegistroAsignatura(self):
        self.GUI.addWidget(self.vistaRegistroAsignatura)
        self.GUI.setCurrentIndex(self.GUI.currentIndex() + 1)

    def volverContextoPrincipal(self):
        self.controladorPrincipal.mostrarVistaPrincipal()