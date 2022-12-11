from PyQt5 import QtWidgets
import pandas as pd
import math
import re

from Vistas.VistaLecturaPlanilla import VistaLecturaPlanilla
from Modelos.EstadisticaAsignatura import EstadisticaAsignatura

class ControladorLecturaPlanilla():

    def __init__(self, controladorPrincipal, databaseContext, GUI):
        self.GUI = GUI
        self.databaseContext = databaseContext
        self.controladorPrincipal = controladorPrincipal
        self.vistaLecturaPlanilla = VistaLecturaPlanilla(self)
        self.asignaturasRegistradas = self.databaseContext.obtenerAsignaturas()
        if self.asignaturas == None:
            self.vistaLecturaPlanilla.mostrarAlerta("Error", "Error en la conexión a la base de datos, el programa terminará su ejecución inmediatamente.")
            sys.exit()
        self.mostrarVistaLecturaPlanilla()
        
    def iniciarIngresoPlanilla(self):
        ano = self.vistaLecturaPlanilla.getAno()
        semestre = self.vistaLecturaPlanilla.getSemestre()
        nombreArchivo = self.vistaLecturaPlanilla.getNombreArchivo()
        parametrosValidos = self.validarParametrosIngresoPlanilla(ano, semestre, nombreArchivo)
        if not parametrosValidos:
            return
        ano = int(ano)
        self.datosExistentesPeriodo = self.databaseContext.obtenerEstadisticasPeriodo(ano, semestre)
        ingresoExitoso = self.leerDatosPlanilla(ano, semestre, nombreArchivo)
        if ingresoExitoso:
            self.vistaLecturaPlanilla.mostrarAlerta("Ingreso exitoso","Se ha ingresado correctamente la información de planificación docente del periodo indicado.")
        self.volverContextoPrincipal()

    
    def validarParametrosIngresoPlanilla(self, ano, periodo, nombreArchivo):
        if not self.anoValido(ano):
            self.vistaLecturaPlanilla.setErrorAno("El valor ingresado es invalido, año debe ser un valor numérico.\n(Periodos admitidos corresponden al intervalo 2015-2050).")
            return False
        self.vistaLecturaPlanilla.setErrorAno("")
        if not self.periodoValido(periodo):
            self.vistaLecturaPlanilla.setErrorPeriodo("Debe seleccionar un periodo lectivo.")
            return False
        self.vistaLecturaPlanilla.setErrorPeriodo("")
        if not self.nombreArchivoValido(nombreArchivo):
            self.vistaLecturaPlanilla.setErrorNombreArchivo("Debe seleccionar un archivo.")
            return False
        self.vistaLecturaPlanilla.setErrorNombreArchivo("")
        return True

    def leerDatosPlanilla(nombreArchivo,ano,periodo):
        tipo = self.identificarTipoPlanilla(nombreArchivo)
        if tipo == 1:
            datosAsignaturas = leerPlanillaTipo1(db,nombreArchivo,ano,periodo)
            datosExistentes = db.obtenerEstadisticasPeriodo(ano,periodo)
            estadisticas = complementarEstadisticasAsignaturas(db,ano,periodo,datosAsignaturas,datosExistentes)
            db.ingresarEstadisticasAsignaturas(ano,periodo,estadisticas)
            db.disconnect()
            return True
        elif tipo == 2:
            print("tipo 2")
            return True
        self.vistaLecturaPlanilla.mostrarAlerta("Error","El archivo ingresado no cumple con el formato esperado.")
        return False

    def mostrarVistaLecturaPlanilla(self):
        self.GUI.addWidget(self.vistaLecturaPlanilla)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)

    def volverContextoPrincipal(self):
        self.controladorPrincipal.mostrarVistaPrincipal()
    
    def anoValido(self,ano):
        if not ano.isnumeric():
            return False
        ano = int(ano)
        if ano >= 2015 and ano <= 2050:
            return True

    def periodoValido(self, periodo):
        if periodo == 1 or periodo == 2:
            return True
    
    def nombreArchivoValido(self, nombreArchivo):
        if nombreArchivo == "":
            return False
        return True

    def identificarTipoPlanilla(self, nombreArchivo):
        data = pd.read_excel(nombreArchivo,skiprows=2)
        columns = data.columns.values.tolist()
        if  'Código Ejecución' in columns and 'Código Civil' in columns and 'COORD.' in columns and 'INSCRITOS' in columns and 'APROBADOS' in columns and 'REPROBADOS' in columns:
            return 2
        elif 'Código Ejecución' in columns and 'Código Civil' in columns and 'COORD.' in columns and 'INSCRITOS' in columns:
            return 1
        return 0