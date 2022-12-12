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
        if self.asignaturasRegistradas == None:
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
        self.ano = int(ano)
        self.semestre = semestre
        self.datosExistentesPeriodo = self.databaseContext.obtenerEstadisticasPeriodo(ano, semestre)
        ingresoExitoso = self.leerDatosPlanilla(nombreArchivo)
        if ingresoExitoso:
            self.vistaLecturaPlanilla.mostrarAlerta("Ingreso exitoso","Se ha ingresado correctamente la información de planificación docente del periodo indicado.")
        self.volverContextoPrincipal()

    def validarParametrosIngresoPlanilla(self, ano, semestre, nombreArchivo):
        if not self.anoValido(ano):
            self.vistaLecturaPlanilla.setErrorAno("El valor ingresado es invalido, año debe ser un valor numérico.\n(Periodos admitidos corresponden al intervalo 2015-2050).")
            return False
        self.vistaLecturaPlanilla.setErrorAno("")
        if not self.semestreValido(semestre):
            self.vistaLecturaPlanilla.setErrorPeriodo("Debe seleccionar un periodo lectivo.")
            return False
        self.vistaLecturaPlanilla.setErrorPeriodo("")
        if not self.nombreArchivoValido(nombreArchivo):
            self.vistaLecturaPlanilla.setErrorNombreArchivo("Debe seleccionar un archivo.")
            return False
        self.vistaLecturaPlanilla.setErrorNombreArchivo("")
        return True

    def leerDatosPlanilla(self, nombreArchivo):
        tipo = self.identificarTipoPlanilla(nombreArchivo)
        estadisticasArchivo = None
        if not (tipo == 1 or tipo == 2):
            self.vistaLecturaPlanilla.mostrarAlerta("Error","El archivo ingresado no cumple con el formato esperado.")
            return False
        if tipo == 1:
            estadisticasArchivo = self.leerPlanillaTipo1(nombreArchivo)
            estadisticasComplementadas = self.complementarEstadisticasArchivo(estadisticasArchivo)
            self.databaseContext.ingresarEstadisticasAsignaturas(self.ano, self.semestre, estadisticasComplementadas)
            return True
        elif tipo == 2:
            estadisticasArchivo = self.leerPlanillaTipo2(nombreArchivo)
            estadisticasComplementadas = self.complementarEstadisticasArchivo(estadisticasArchivo)
            self.databaseContext.ingresarEstadisticasAsignaturas(self.ano, self.semestre, estadisticasComplementadas)
            return True
        
    def complementarEstadisticasArchivo(self, estadisticasArchivo):
        for codigo in estadisticasArchivo:
            if codigo in self.datosExistentesPeriodo:
                estadisticaExistente = EstadisticaAsignatura(self.ano, self.semestre, codigo)
                estadisticaExistente.setInscritosTeoria(datosExistentesPeriodo[codigo]["inscritosTeoria"])
                estadisticaExistente.setAprobadosTeoria(datosExistentesPeriodo[codigo]["aprobadosTeoria"])
                estadisticaExistente.setReprobadosTeoria(datosExistentesPeriodo[codigo]["reprobadosTeoria"])
                estadisticaExistente.setInscritosLaboratorio(datosExistentesPeriodo[codigo]["inscritosLaboratorio"])
                estadisticaExistente.setAprobadosLaboratorio(datosExistentesPeriodo[codigo]["aprobadosLaboratorio"])
                estadisticaExistente.setReprobadosLaboratorio(datosExistentesPeriodo[codigo]["reprobadosLaboratorio"])
                estadisticaExistente.setTasaAprobacionTeoria(datosExistentesPeriodo[codigo]["tasaAprobacionTeoria"])
                estadisticaExistente.setTasaAprobacionLaboratorio(datosExistentesPeriodo[codigo]["tasaAprobacionLaboratorio"])
                estadisticaExistente.setTasaDesinscripcion(datosExistentesPeriodo[codigo]["tasaDesinscripcion"])
                estadisticaComplementada = self.complementarEstadisticas(estadisticaExistente, estadisticasArchivo[codigo])
                estadisticasArchivo[codigo] = estadisticaComplementada
        return estadisticasArchivo

    def complementarEstadisticas(self, estadisticaExistente, estadisticaNueva): 
        if estadisticaExistente.inscritosTeoria == 0:
            estadisticaExistente.inscritosTeoria = estadisticaNueva.inscritosTeoria
        if estadisticaExistente.aprobadosTeoria == 0:
            estadisticaExistente.aprobadosTeoria = estadisticaNueva.aprobadosTeoria
        if estadisticaExistente.reprobadosTeoria == 0:
            estadisticaExistente.reprobadosTeoria = estadisticaNueva.reprobadosTeoria
        if estadisticaExistente.inscritosLaboratorio == 0:
            estadisticaExistente.inscritosLaboratorio = estadisticaNueva.inscritosLaboratorio
        if estadisticaExistente.aprobadosLaboratorio == 0:
            estadisticaExistente.aprobadosLaboratorio = estadisticaNueva.aprobadosLaboratorio
        if estadisticaExistente.reprobadosLaboratorio == 0:
            estadisticaExistente.reprobadosLaboratorio = estadisticaNueva.reprobadosLaboratorio
        estadisticaExistente.calcularTasas()
        return estadisticaExistente

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

    def semestreValido(self, semestre):
        if semestre == 1 or semestre == 2:
            return True
    
    def nombreArchivoValido(self, nombreArchivo):
        if nombreArchivo == "":
            return False
        return True

    def identificarTipoPlanilla(self, nombreArchivo):
        try:
            data = pd.read_excel(nombreArchivo,skiprows=2)
            columns = data.columns.values.tolist()
            if  'Código Ejecución' in columns and 'Código Civil' in columns and 'COORD.' in columns and 'INSCRITOS' in columns and 'APROBADOS' in columns and 'REPROBADOS' in columns:
                return 2
            elif 'Código Ejecución' in columns and 'Código Civil' in columns and 'COORD.' in columns and 'INSCRITOS' in columns:
                return 1
        except:
            return 0

    def leerPlanillaTipo1(self, nombreArchivo):
        data = pd.read_excel(nombreArchivo,usecols="A,B,D,S",skiprows=2)
        data = data.T
        estadisticas = {}
        cantidadFilas = data.shape[1]
        for i in range(cantidadFilas):
            fila = data.iloc[:, i]
            codigoEjecucionValido, codigoEjecucion= self.validarCodigo(fila["Código Ejecución"])
            codigoCivilValido, codigoCivil= self.validarCodigo(fila["Código Civil"])
            coordinacion = fila["COORD."]
            inscritos = fila["INSCRITOS"]
            if codigoEjecucionValido:
                estadisticas = self.agregarInscritosEstadisticas(estadisticas, codigoEjecucion, coordinacion, inscritos)
            elif codigoCivilValido:
                estadisticas = self.agregarInscritosEstadisticas(estadisticas, codigoCivil, coordinacion, inscritos)
        for codigo in estadisticas:
            estadisticas[codigo].calcularTasas()
        return estadisticas

    def leerPlanillaTipo2(self, nombreArchivo):
        data = pd.read_excel(nombreArchivo,usecols="A,B,D,S,AB,AC",skiprows=2)
        data = data.T
        estadisticas = {}
        cantidadFilas = data.shape[1]
        for i in range(cantidadFilas):
            fila = data.iloc[:, i]
            codigoEjecucionValido, codigoEjecucion= self.validarCodigo(fila["Código Ejecución"])
            codigoCivilValido, codigoCivil= self.validarCodigo(fila["Código Civil"])
            coordinacion = fila["COORD."]
            inscritos = fila["INSCRITOS"]
            aprobados = fila["APROBADOS"]
            reprobados = fila["REPROBADOS"]
            if codigoEjecucionValido:
                estadisticas = self.agregarInscritosEstadisticas(estadisticas, codigoEjecucion, coordinacion, inscritos)
                estadisticas = self.agregarAprobadosEstadisticas(estadisticas, codigoEjecucion, coordinacion, aprobados)
                estadisticas = self.agregarReprobadosEstadisticas(estadisticas, codigoEjecucion, coordinacion, reprobados)
            elif codigoCivilValido:
                estadisticas = self.agregarInscritosEstadisticas(estadisticas, codigoCivil, coordinacion, inscritos)
                estadisticas = self.agregarAprobadosEstadisticas(estadisticas, codigoCivil, coordinacion, aprobados)
                estadisticas = self.agregarReprobadosEstadisticas(estadisticas, codigoCivil, coordinacion, reprobados)
        for codigo in estadisticas:
            estadisticas[codigo].calcularTasas()
        return estadisticas

    def validarCodigo(self, codigo):

        valor = 0
        if isinstance(codigo,int):
            valor = codigo
        elif isinstance(codigo,str):
            valores = re.split(' |/', codigo)
            i = 0
            while i < len(valores):
                if valores[i].isnumeric():
                    i = i+1
                else:
                    del valores[i]
            if len(valores)>= 1:
                valor = int(valores[0])
        if valor in self.asignaturasRegistradas:
            return True,valor
        else:
            return False,valor

    def agregarInscritosEstadisticas(self, estadisticas, codigo ,coordinacion, inscritos):
        if codigo in estadisticas:
            estadisticas[codigo].agregarInscritos(coordinacion, inscritos)
            return estadisticas
        nuevaAsignatura = EstadisticaAsignatura(self.ano, self.semestre, codigo)
        nuevaAsignatura.agregarInscritos(coordinacion, inscritos)
        estadisticas[codigo] = nuevaAsignatura
        return estadisticas

    def agregarAprobadosEstadisticas(self, estadisticas, codigo, coordinacion, aprobados):
        if codigo in estadisticas:
            estadisticas[codigo].agregarAprobados(coordinacion, aprobados)
            return estadisticas
        nuevaAsignatura = EstadisticaAsignatura(self.ano, self.semestre, codigo)
        nuevaAsignatura.agregarAprobados(coordinacion, aprobados)
        estadisticas[codigo] = nuevaAsignatura
        return estadisticas

    def agregarReprobadosEstadisticas(self, estadisticas, codigo, coordinacion, reprobados):
        if codigo in estadisticas:
            estadisticas[codigo].agregarReprobados(coordinacion, reprobados)
            return estadisticas
        nuevaAsignatura = EstadisticaAsignatura(self.ano, self.semestre, codigo)
        nuevaAsignatura.agregarReprobados(coordinacion, reprobados)
        estadisticas[codigo] = nuevaAsignatura
        return estadisticas