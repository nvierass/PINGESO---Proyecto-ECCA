import xlsxwriter as xl
import math
import sys

from Vistas.VistaGestionEstadisticas import VistaGestionEstadisticas
from Modelos.EstadisticaAsignatura import EstadisticaAsignatura

class ControladorGestionEstadisticas():

    def __init__(self, controladorPrincipal, databaseContext, GUI):
        self.GUI = GUI
        self.databaseContext = databaseContext
        self.controladorPrincipal = controladorPrincipal

        self.vistaGestionEstadisticas = VistaGestionEstadisticas(self)
        
        self.estadisticas = {}
        self.asignaturas = self.databaseContext.obtenerAsignaturas()
        if self.asignaturas == None:
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "Error en la conexión a la base de datos, el programa terminará su ejecución inmediatamente.")
            sys.exit()
        self.vistaGestionEstadisticas.montarVista(self.asignaturas)
        self.mostrarVistaGestionEstadisticas()


    def mostrarVistaGestionEstadisticas(self):
        self.GUI.addWidget(self.vistaGestionEstadisticas)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)

    def actualizarTabla(self):
        if self.vistaGestionEstadisticas.edicionActiva():
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "Debe finalizar o cancelar la edición antes de consultar otra asignatura.")
            return
        codigo, nombre = self.vistaGestionEstadisticas.getCodigoNombreSeleccionado()
        if codigo == None:
            self.vistaGestionEstadisticas.setNombre("--")
            self.vistaGestionEstadisticas.setCodigo("--")
            return
        self.vistaGestionEstadisticas.limpiarGrid()
        if codigo not in self.estadisticas:
            estadisticasAsignatura = self.databaseContext.obtenerEstadisticasAsignatura(codigo)
            self.estadisticas[codigo] = estadisticasAsignatura
        estadisticas= self.estadisticas[codigo]
        self.vistaGestionEstadisticas.setCodigo(codigo)
        self.vistaGestionEstadisticas.setNombre(nombre)
        if len(estadisticas) == 0:
            self.vistaGestionEstadisticas.mostrarAlerta("Advertencia", "No existen estadísticas curriculares de la asignatura seleccionada.")
        self.vistaGestionEstadisticas.agregarEstadisticas(estadisticas)

    def volverContextoPrincipal(self):
        self.controladorPrincipal.mostrarVistaPrincipal()
    
    def botonEliminarClicked(self, index):
        if self.vistaGestionEstadisticas.edicionActiva():
            self.vistaGestionEstadisticas.mostrarAlerta("Advertencia", "Debe finalizar la edición actual antes de eliminar otra estadística.")
            return
        [codigo, nombre] = self.vistaGestionEstadisticas.getCodigoNombreSeleccionado()
        estadistica = self.estadisticas[codigo][index]
        ano = estadistica.getAno()
        semestre = estadistica.getSemestre()
        if not self.vistaGestionEstadisticas.confirmarEliminacion(codigo, nombre, ano, semestre):
            return
        eliminacionExitosa = self.databaseContext.eliminarEstadistica(estadistica)
        if not eliminacionExitosa:
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "No se ha logrado eliminar la estadística.")
            return
        self.vistaGestionEstadisticas.mostrarAlerta("Exito", "La estadística ha sido eliminada.")
        del self.estadisticas[codigo][index]
        self.actualizarTabla()

    def botonCancelarClicked(self, index):
        fila = index + 1
        self.vistaGestionEstadisticas.deshabilitarEdicion(fila)
        codigoAsignaturaEdicion = self.vistaGestionEstadisticas.getCodigoAsignaturaEdicion()
        self.vistaGestionEstadisticas.restaurarEstadistica(fila, self.estadisticas[codigoAsignaturaEdicion][index])
    
    def botonEditarClicked(self, index):
        if self.vistaGestionEstadisticas.edicionActiva():
            self.vistaGestionEstadisticas.mostrarAlerta("Advertencia", "Debe finalizar la edición actual antes de editar otra estadística.")
            return
        fila = index + 1 
        self.vistaGestionEstadisticas.habilitarEdicion(fila)

    def botonGuardarClicked(self, index):
        [codigo, nombre] = self.vistaGestionEstadisticas.getCodigoNombreSeleccionado()
        fila = index + 1
        datosEstadistica = self.vistaGestionEstadisticas.obtenerEstadistica(fila)
        datosValidos = self.validarDatos(datosEstadistica)
        if not datosValidos:
            return
        self.vistaGestionEstadisticas.deshabilitarEdicion(fila)
        ano = int(datosEstadistica[0])
        semestre = int(datosEstadistica[1])
        inscritosTeoria = int(datosEstadistica[2])
        aprobadosTeoria = int(datosEstadistica[3])
        reprobadosTeoria = int(datosEstadistica[4])
        inscritosLaboratorio = int(datosEstadistica[5])
        aprobadosLaboratorio = int(datosEstadistica[6])
        reprobadosLaboratorio = float(datosEstadistica[7])
        tasaAprobacionTeoria = float(datosEstadistica[8])
        tasaAprobacionLaboratorio = float(datosEstadistica[9])
        tasaDesinscripcion = float(datosEstadistica[10])
        estadisticaAnterior = self.estadisticas[codigo][index]
        estadisticaActualizada = EstadisticaAsignatura(ano, semestre, codigo)
        estadisticaActualizada.setInscritosTeoria(inscritosTeoria)
        estadisticaActualizada.setAprobadosTeoria(aprobadosTeoria)
        estadisticaActualizada.setReprobadosTeoria(reprobadosTeoria)
        estadisticaActualizada.setInscritosLaboratorio(inscritosLaboratorio)
        estadisticaActualizada.setAprobadosLaboratorio(aprobadosLaboratorio)
        estadisticaActualizada.setReprobadosLaboratorio(reprobadosLaboratorio)
        estadisticaActualizada.setTasaAprobacionTeoria(tasaAprobacionTeoria)
        estadisticaActualizada.setTasaAprobacionLaboratorio(tasaAprobacionLaboratorio)
        estadisticaActualizada.setTasaDesinscripcion(tasaDesinscripcion)
        actualizacionExitosa = self.databaseContext.actualizarEstadisticaAsignatura(estadisticaActualizada)
        if actualizacionExitosa:
            self.vistaGestionEstadisticas.mostrarAlerta("Exito", "La estadística se ha actualizado correctamente.")
            self.estadisticas[codigo][index] = estadisticaActualizada
            self.actualizarTabla()
            return
        else:
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "La estadística no se ha actualizado correctamente.")
            self.actualizarTabla()

    def botonGuardarNuevaClicked(self):
        [codigo, nombre] = self.vistaGestionEstadisticas.getCodigoNombreSeleccionado()
        datosEstadistica = self.vistaGestionEstadisticas.obtenerEstadisticaRegistro()
        datosValidos = self.validarDatos(datosEstadistica)
        if not datosValidos:
            return
        ano = int(datosEstadistica[0])
        semestre = int(datosEstadistica[1])
        inscritosTeoria = int(datosEstadistica[2])
        aprobadosTeoria = int(datosEstadistica[3])
        reprobadosTeoria = int(datosEstadistica[4])
        inscritosLaboratorio = int(datosEstadistica[5])
        aprobadosLaboratorio = int(datosEstadistica[6])
        reprobadosLaboratorio = float(datosEstadistica[7])
        tasaAprobacionTeoria = float(datosEstadistica[8])
        tasaAprobacionLaboratorio = float(datosEstadistica[9])
        tasaDesinscripcion = float(datosEstadistica[10])
        if codigo in self.estadisticas:
            for estadistica in self.estadisticas[codigo]:
                anoEstadistica = estadistica.getAno()
                semestreEstadistica = estadistica.getSemestre()
                if anoEstadistica == ano and semestreEstadistica == semestre:
                    self.vistaGestionEstadisticas.mostrarAlerta("Error", "Ya existe una estadística correspondiente al periodo que se esta tratando de ingresar.")
                    self.vistaGestionEstadisticas.editandoEstadistica = False
                    self.vistaGestionEstadisticas.comboBoxAsignaturas.setEnabled(True)
                    self.vistaGestionEstadisticas.boton_agregar_estadistica.setVisible(True)
                    self.vistaGestionEstadisticas.eliminarFilaRegistro()
                    self.actualizarTabla()
                    return
        estadisticaNueva = EstadisticaAsignatura(ano, semestre, codigo)
        estadisticaNueva.setInscritosTeoria(inscritosTeoria)
        estadisticaNueva.setAprobadosTeoria(aprobadosTeoria)
        estadisticaNueva.setReprobadosTeoria(reprobadosTeoria)
        estadisticaNueva.setInscritosLaboratorio(inscritosLaboratorio)
        estadisticaNueva.setAprobadosLaboratorio(aprobadosLaboratorio)
        estadisticaNueva.setReprobadosLaboratorio(reprobadosLaboratorio)
        estadisticaNueva.setTasaAprobacionTeoria(tasaAprobacionTeoria)
        estadisticaNueva.setTasaAprobacionLaboratorio(tasaAprobacionLaboratorio)
        estadisticaNueva.setTasaDesinscripcion(tasaDesinscripcion)
        ingresoExitoso = self.databaseContext.registrarEstadisticaAsignatura(estadisticaNueva)
        if not ingresoExitoso:
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "La estadística no se ha ingresado correctamente.")
            self.vistaGestionEstadisticas.editandoEstadistica = False
            self.vistaGestionEstadisticas.comboBoxAsignaturas.setEnabled(True)
            self.vistaGestionEstadisticas.boton_agregar_estadistica.setVisible(True)
            self.vistaGestionEstadisticas.eliminarFilaRegistro()
            self.actualizarTabla()
            return
        if codigo in self.estadisticas:
            self.estadisticas[codigo].append(estadisticaNueva)
        else:
            self.estadisticas[codigo] = [estadisticaNueva]
        self.vistaGestionEstadisticas.mostrarAlerta("Exito", "La estadística se ha ingresado correctamente.")
        self.vistaGestionEstadisticas.editandoEstadistica = False
        self.vistaGestionEstadisticas.comboBoxAsignaturas.setEnabled(True)
        self.vistaGestionEstadisticas.boton_agregar_estadistica.setVisible(True)
        self.vistaGestionEstadisticas.eliminarFilaRegistro()
        self.actualizarTabla()

    def iniciarIngreso(self):
        if self.vistaGestionEstadisticas.edicionActiva():
            self.vistaGestionEstadisticas.mostrarAlerta("Advertencia", "Debe finalizar la edición actual antes de agregar nuevas estadísticas.")
            return
        self.vistaGestionEstadisticas.agregarFilaIngreso()

    def botonCancelarIngresoClicked(self):
        self.vistaGestionEstadisticas.editandoEstadistica = False
        self.vistaGestionEstadisticas.comboBoxAsignaturas.setEnabled(True)
        self.vistaGestionEstadisticas.boton_agregar_estadistica.setVisible(True)
        self.vistaGestionEstadisticas.eliminarFilaRegistro()
        self.actualizarTabla()

    def validarDatos(self, datos):
        nombreColumnas = ["año", "semestre","inscritos teoría", "aprobados teoría", "reprobados teoría", "inscritos laboratorio", "aprobados laboratorio", "reprobados laboratorio", "tasa aprobación teoría", "tasa aprobación laboratorio", "tasa desinscripcion"]
        ano = datos[0]
        semestre = datos[1]
        inscritosTeoria = datos[2]
        aprobadosTeoria = datos[3]
        reprobadosTeoria = datos[4]
        inscritosLaboratorio = datos[5]
        aprobadosLaboratorio = datos[6]
        reprobadosLaboratorio = datos[7]
        tasaAprobacionTeoria = datos[8]
        tasaAprobacionLaboratorio = datos[9]
        tasaDesinscripcion = datos[10]
        for i in range(0,11):
            if datos[i] == "":
                self.vistaGestionEstadisticas.mostrarAlerta("Error", "No ha ingresado un valor para la columna " + nombreColumnas[i] + ".")
                return
        for i in range(0,8):
            if not datos[i].isnumeric():
                self.vistaGestionEstadisticas.mostrarAlerta("Error", "El valor ingresado para la columna " + nombreColumnas[i] + " debe ser un valor númerico.")
                return
        for i in range(8,11):
            if not self.esFloat(datos[i]):
                self.vistaGestionEstadisticas.mostrarAlerta("Error", "El valor ingresado para la columna " + nombreColumnas[i] + " debe ser un número decimal con punto.")
                return
        ano = int(ano)
        semestre = int(semestre)
        inscritosTeoria = int(inscritosTeoria)
        aprobadosTeoria = int(aprobadosTeoria)
        reprobadosTeoria = int(reprobadosTeoria)
        inscritosLaboratorio = int(inscritosLaboratorio)
        aprobadosLaboratorio = int(aprobadosLaboratorio)
        reprobadosLaboratorio = int(reprobadosLaboratorio)
        tasaAprobacionTeoria = float(tasaAprobacionTeoria)
        tasaAprobacionLaboratorio = float(tasaAprobacionLaboratorio)
        tasaDesinscripcion = float(tasaDesinscripcion)
        if not self.anoValido(ano):
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "El año ingresado debe pertenecer al intervalo [2000-2050].")
            return
        if not self.periodoValido(semestre):
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "El semestre ingresado debe ser 1 para primer semestre o 2 para segundo semestre.")
            return
        for i in range(2,8):
            if not self.cantidadValida(datos[i]):
                self.vistaGestionEstadisticas.mostrarAlerta("Error", "El valor ingresado para la columna " + nombreColumnas[i] + "debe ser un número en el intervalo [0-200].")
                return
        if aprobadosTeoria + reprobadosTeoria > inscritosTeoria:
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "La cantidad de inscritos en teoría debe ser mayor o igual a la suma de aprobados de teoría y reprobados de teoría.")
            return
        if aprobadosLaboratorio + reprobadosLaboratorio > inscritosLaboratorio:
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "La cantidad de inscritos en laboratorio debe ser mayor o igual a la suma de aprobados de laboratorio y reprobados de laboratorio.")
            return
        if not self.tasaValida(tasaAprobacionTeoria):
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "La tasa de aprobación de teoría es invalida, debe ser un número decimal entre 0 y 1.")
            return
        if not self.tasaValida(tasaAprobacionLaboratorio):
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "La tasa de aprobación de laboratorio es invalida, debe ser un número decimal entre 0 y 1.")
            return
        if not self.tasaValida(tasaDesinscripcion):
            self.vistaGestionEstadisticas.mostrarAlerta("Error", "La tasa de desinscripción es invalida, debe ser un número decimal entre 0 y 1.")
            return
        return True

    def esFloat(self, valor):
        try:
            x = float(valor)
            return True
        except:
            return False

    def anoValido(self,ano):
        if ano >= 2000 and ano <= 2050:
            return True
    
    def periodoValido(self, periodo):
        if periodo == 1 or periodo == 2:
            return True

    def cantidadValida(self, valor):
        cantidad = int(valor)
        if cantidad < 0 or cantidad >=200:
            return False
        return True

    def tasaValida(self, valor):
        if valor < 0 or valor > 1:
            return False
        return True 