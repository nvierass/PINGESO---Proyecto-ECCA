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
        
        self.estadisticas = {}
        self.asignaturas = self.databaseContext.obtenerAsignaturas()
        if self.asignaturas == None:
            self.vistaEstimacion.mostrarAlerta("Error", "Error en la conexión a la base de datos, el programa terminará su ejecución inmediatamente.")
            sys.exit()
        self.vistaGestionEstadisticas.montarVista(self.asignaturas)
        self.mostrarVistaGestionEstadisticas()


    def mostrarVistaGestionEstadisticas(self):
        self.GUI.addWidget(self.vistaGestionEstadisticas)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)

    def actualizarTabla(self):
        self.vistaGestionEstadisticas.limpiarGrid()
        codigo, nombre = self.vistaGestionEstadisticas.getCodigoNombreSeleccionado()
        if codigo not in self.estadisticas:
            estadisticasAsignatura = self.databaseContext.obtenerEstadisticasAsignatura(codigo)
            self.estadisticas[codigo] = estadisticasAsignatura
        estadisticas= self.estadisticas[codigo]
        self.vistaGestionEstadisticas.setCodigo(codigo)
        self.vistaGestionEstadisticas.setNombre(nombre)
        if len(estadisticas) == 0:
            self.vistaGestionEstadisticas.mostrarAlerta("Advertencia", "No existen estadísticas curriculares de la asignatura seleccionada.")
        self.vistaGestionEstadisticas.agregarEstadisticas(estadisticas)

    def setNombre(self, nombre):
        self.labelNombre.setText(nombre)

    def setCodigo(self, codigo):
        self.labelCodigo.setText(str(codigo))

    def volverContextoPrincipal(self):
        self.controladorPrincipal.mostrarVistaPrincipal()
    
    def botonEliminarClicked(self, index):
        codigo = self.vistaGestionEstadisticas.getCodigo()
        estadistica = self.estadisticas[codigo][index]
        del self.estadisticas[codigo][index]
        print("estadistica a eliminar corresponde a ", codigo, estadistica.getAno(),"-",estadistica.getSemestre())

        self.actualizarTabla()