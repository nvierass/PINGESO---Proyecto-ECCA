import sys

from PyQt5 import QtWidgets

from Vistas.VistaPrincipal import VistaPrincipal
from Vistas.VistaActualizarPeriodo import VistaActualizarPeriodo
from Controladores.ControladorRegistroPlan import ControladorRegistroPlan
from Controladores.ControladorLecturaPlanilla import ControladorLecturaPlanilla
from Controladores.ControladorEstimacion import ControladorEstimacion
from Controladores.ControladorMallaInteractiva import ControladorMallaInteractiva
from Controladores.ControladorGestionEstadisticas import ControladorGestionEstadisticas
from DatabaseDriver.DatabaseContext import DatabaseContext

class ControladorPrincipal():

    def __init__(self, GUI, databaseContext):
        self.GUI = GUI
        self.databaseContext = databaseContext
        self.vistaPrincipal = VistaPrincipal(self)
        if self.databaseContext.conn == None:
            self.vistaPrincipal.mostrarAlerta("Error","No se ha establecido una conexión a la base de datos.\nFinalizando ejecución.")
            sys.exit()
        self.ano = 2022
        self.semestre = 2
        self.iniciarVistaPrincipal()
        

    def iniciarVistaPrincipal(self):
        planesRegistrados = self.databaseContext.obtenerPlanes()
        self.vistaPrincipal.setAno(self.ano)
        self.vistaPrincipal.setSemestre(self.semestre)
        self.vistaPrincipal.actualizarTitulo()
        self.vistaPrincipal.setPlanesRegitrados(planesRegistrados)
        self.GUI.addWidget(self.vistaPrincipal)
        self.GUI.showMaximized()

    def actualizarVista(self):
        planesRegistrados = self.databaseContext.obtenerPlanes()
        self.vistaPrincipal.setPlanesRegitrados(planesRegistrados)
        
    def mostrarVistaPrincipal(self):
        self.GUI.addWidget(self.vistaPrincipal)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)

    def goRegistroPlan(self):
        self.controladorRegistroPlan  = ControladorRegistroPlan(self, self.databaseContext, self.GUI)

    def goLecturaPlanilla(self):
        self.controladorLecturaPlanilla = ControladorLecturaPlanilla(self, self.databaseContext, self.GUI)

    def goEstimacion(self):
        self.controladorEstimacion = ControladorEstimacion(self, self.databaseContext, self.GUI, False)

    def goActualizacion(self):
        self.vistaActualizarPeriodo = VistaActualizarPeriodo(self)
        self.GUI.addWidget(self.vistaActualizarPeriodo)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)

    def goMallaInteractiva(self, planSeleccionado):
        self.controladorMallaInteractiva = ControladorMallaInteractiva(self, self.databaseContext, self.GUI, planSeleccionado,self.ano, self.semestre)

    def goGestionEstadisticas(self):
        self.controladorGestionEstadisticas = ControladorGestionEstadisticas(self, self.databaseContext, self.GUI)

    def actualizarPeriodo(self):
        self.vistaActualizarPeriodo.setErrorPeriodo("")
        self.vistaActualizarPeriodo.setErrorAno("")
        ano = self.vistaActualizarPeriodo.getAno()
        semestre = self.vistaActualizarPeriodo.getPeriodo()
        if not self.anoValido(ano):
            self.vistaActualizarPeriodo.setErrorAno("El valor ingresado es invalido, año debe ser un valor numérico.\n(Periodos admitidos corresponden al intervalo 2015-2050).")
            return False
        self.vistaActualizarPeriodo.setErrorAno("")
        if not self.semestreValido(semestre):
            self.vistaActualizarPeriodo.setErrorPeriodo("Debe seleccionar un periodo lectivo.")
            return False
        self.vistaActualizarPeriodo.setErrorPeriodo("")
        ano = int(ano) 
        self.ano = ano
        self.semestre = semestre
        self.vistaPrincipal.setAno(self.ano)
        self.vistaPrincipal.setSemestre(self.semestre)
        self.vistaPrincipal.actualizarTitulo()
        self.mostrarVistaPrincipal()

    def anoValido(self,ano):
        if not ano.isnumeric():
            return False
        ano = int(ano)
        if ano >= 2015 and ano <= 2050:
            return True

    def semestreValido(self, semestre):
        if semestre == 1 or semestre == 2:
            return True
    