import xlsxwriter as xl
import math
import sys

from Vistas.VistaEstimacion import VistaEstimacion
from Vistas.VistaCupos import VistaCupos
from Vistas.VistaResultados import VistaResultados

class ControladorEstimacion():

    def __init__(self, controladorPrincipal, databaseContext, GUI):
        self.GUI = GUI
        self.databaseContext = databaseContext
        self.controladorPrincipal = controladorPrincipal
        self.vistaEstimacion = VistaEstimacion(self)
        self.vistaCupos = VistaCupos(self)
        self.vistaResultados = VistaResultados(self)
        self.mostrarVistaEstimacion()

        self.asignaturas = self.databaseContext.obtenerAsignaturas()
        if self.asignaturas == None:
            self.vistaEstimacion.mostrarAlerta("Error", "Error en la conexión a la base de datos, el programa terminará su ejecución inmediatamente.")
            sys.exit()
        self.resultadosEstimacion = {}


    def definirRequisitoPrioritario(self, codigo, datosPeriodoActual, datosHistoricos):
        requisitoEncontrado, requisito = self.aplicarCriterioPrioritarioNivel(codigo)
        if not requisitoEncontrado:
            requisitosMayorNivel = requisito
            requisitoEncontrado, requisito = self.aplicarCriterioPrioritarioDificultad(requisitosMayorNivel, datosHistoricos)
        if not requisitoEncontrado:
            requisitosCandidatos = requisito
            requisitoEncontrado, requisito = self.aplicarCriterioPrioritarioCantidadAlumnos(requisitosCandidatos, datosPeriodoActual)
        self.asignaturas[codigo].setRequisitoPrioritario(requisito)

    def aplicarCriterioPrioritarioNivel(self, codigo):
        nivelesRequisitos = self.asignaturas[codigo].getAsignaturasRequisitos()
        if len(nivelesRequisitos) == 0:
            return True, None
        nivelMayor = max(nivelesRequisitos)
        requisitosMayorNivel = nivelesRequisitos[nivelMayor]
        if len(requisitosMayorNivel) == 0:
            return True, None
        elif len(requisitosMayorNivel) == 1:
            requisito = requisitosMayorNivel[0]
            return True, requisito
        return False, requisitosMayorNivel

    def aplicarCriterioPrioritarioDificultad(self, requisitosMayorNivel, datosHistoricos):
        requisitosCandidatos = []
        menorTasaAprobacion = 1
        for requisitoCandidato in requisitosMayorNivel:
            if (not self.perteneceMBI(requisitoCandidato)) and (requisitoCandidato in datosHistoricos):
                tasaAprobacionCandidato = datosHistoricos[requisitoCandidato]["tasaAprobacionTeoria"]
                if tasaAprobacionCandidato == menorTasaAprobacion:
                    requisitosCandidatos.append(requisitoCandidato)
                elif tasaAprobacionCandidato < menorTasaAprobacion:
                    requisitosCandidatos = [requisitoCandidato]
                    menorTasaAprobacion = tasaAprobacionCandidato
        if len(requisitosCandidatos) == 1:
            return True, requisitosCandidatos[0]
        return False, requisitosCandidatos

    def aplicarCriterioPrioritarioCantidadAlumnos(self, requisitosPotenciales, datosPeriodoActual):
        requisitosCandidatos = []
        menorCantidadAlumnos = 1000
        for requisitoCandidato in requisitosPotenciales:
            if (not self.perteneceMBI(requisitoCandidato)) and (requisitoCandidato in datosPeriodoActual):
                alumnosInscritos = datosPeriodoActual[requisitoCandidato]["tasaAprobacionTeoria"]
                if alumnosInscritos <= menorCantidadAlumnos:
                    requisitosCandidatos = [requisitoCandidato]
                    menorCantidadAlumnos = alumnosInscritos
        if len(requisitosCandidatos) == 1:
            return True, requisitosCandidatos[0]
        return True, None
        


    def mostrarVistaEstimacion(self):
        self.GUI.addWidget(self.vistaEstimacion)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)
        
    def mostrarVistaCupos(self):
        self.GUI.addWidget(self.vistaCupos)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)

    def mostrarVistaResultados(self):
        self.GUI.addWidget(self.vistaResultados)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)

    def volverContextoPrincipal(self):
        self.controladorPrincipal.mostrarVistaPrincipal()

    def exportarResultados(self):
        nombreArchivoSalida = self.vistaResultados.getPathResultados()
        guardadoExitoso = self.generarReporte(nombreArchivoSalida, self.resultadosEstimacion)
        if not guardadoExitoso:
            self.vistaResultados.mostrarAlerta("Error","No se ha logrado exportar los resultados.")
    

    def generarReporte(self, nombre,data):
        try:
            workbook = xl.Workbook(nombre)
            worksheet = workbook.add_worksheet()
            columnas = ["Código","Nombre Asignatura","Nivel","Estimados Alumnos Cátedra","Estimados Alumnos Laboratorio","Estimados Coordinaciones Cátedra","Estimados Coordinaciones Laboratorio","Observaciones"]
            column = 0
            for columna in columnas:
                worksheet.write(0,column,columna)
                column = column + 1
            row = 1
            for index in self.resultadosEstimacion:
                worksheet.write(row,0,self.resultadosEstimacion[index].codigo)
                worksheet.write(row,1,self.resultadosEstimacion[index].nombre)
                worksheet.write(row,2,self.resultadosEstimacion[index].nivel)
                worksheet.write(row,3,self.resultadosEstimacion[index].estimadosTeoria)
                worksheet.write(row,4,self.resultadosEstimacion[index].estimadosLaboratorio)
                worksheet.write(row,5,self.resultadosEstimacion[index].coorinacionesEstimadasTeoria)
                worksheet.write(row,6,self.resultadosEstimacion[index].coorinacionesEstimadasLaboratorio)
                worksheet.write(row,7,self.resultadosEstimacion[index].observaciones)
            workbook.close()
            return True
        except:
            return False
            
    def realizarEstimacion(self):
        ano = self.vistaEstimacion.getAno()
        semestre = self.vistaEstimacion.getPeriodo()
        tipoEstimacion = self.vistaEstimacion.getTipoEstimacion()
        ponderacionValoresHistoricos = self.vistaEstimacion.getPonderacionValoresHistoricos()
        ponderacionValoresPeriodoAnterior = self.vistaEstimacion.getPonderacionValoresPeriodoAnterior()

        parametrosValidos = self.validarParametrosEstimacion(ano, semestre, tipoEstimacion, ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior)
        if not parametrosValidos:
            return 
        #self.obtenerCuposAsignaturas() ver con linko
        ano = int(ano)
        ponderacionValoresHistoricos = int(ponderacionValoresHistoricos)
        ponderacionValoresPeriodoAnterior = int(ponderacionValoresPeriodoAnterior)
        anoPeriodoActual, semestrePeriodoActual = self.periodoAnterior(ano, semestre) 
        anoPeriodoAnterior, semestrePeriodoAnterior = self.periodoAnterior(anoPeriodoActual, semestrePeriodoActual)
        tipoEstimacion = self.vistaEstimacion.getTipoEstimacion()
        
        datosHistoricos = self.databaseContext.obtenerTasasHistoricas()
        datosPeriodoActual = self.databaseContext.obtenerEstadisticasPeriodo(anoPeriodoActual, semestrePeriodoActual)
        datosPeriodoAnterior = self.databaseContext.obtenerEstadisticasPeriodo(anoPeriodoAnterior, semestrePeriodoAnterior)
        self.determinarRequisitosPrioritarios(datosPeriodoActual, datosHistoricos)
        self.mostrarAsignaturas()
        if tipoEstimacion == 1:
            self.realizarEstimacionPriori()
        elif tipoEstimacion == 2:
            self.realizarEstimacionPosteriori()

    def determinarRequisitosPrioritarios(self, datosPeriodoActual, datosHistoricos):
        for codigoAsignatura in self.asignaturas:
            self.definirRequisitoPrioritario(codigoAsignatura, datosPeriodoActual, datosHistoricos)

    def mostrarAsignaturas(self):
        rs = self.asignaturas
        for codigo in rs:
            print("\nAsignatura:", rs[codigo].getCodigo())
            print("\tNombre:",rs[codigo].getNombre())
            print("\tRequisitos:")
            requisitos = rs[codigo].getAsignaturasRequisitos()
            for nivel in requisitos:
                print("\t\tNivel: ",nivel , "Requisitos: ",requisitos[nivel])
            print("\tRequisito Prooritario:",rs[codigo].getRequisitoPrioritario())
            print("\t\tEquivalentes: ", rs[codigo].getAsignaturasEquivalentes())

    def obtenerCuposAsignaturas(self):
        self.mostrarVistaCupos()

    def realizarEstimacionPriori(self):
        aux = 0

    def realizarEstimacionPosteriori(self):
        aux = 0

    def validarParametrosEstimacion(self, ano, periodo, tipoEstimacion, ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior):
        if not self.anoValido(ano):
            self.vistaEstimacion.setErrorAno("El valor ingresado es invalido, año debe ser un valor numérico (2015-2050).")
            return False
        self.vistaEstimacion.setErrorAno("")
        if not self.periodoValido(periodo):
            self.vistaEstimacion.setErrorPeriodo("Debe seleccionar un periodo lectivo.")
            return False
        self.vistaEstimacion.setErrorPeriodo("")
        if not self.tipoEstimacionValida(tipoEstimacion):
            self.vistaEstimacion.setErrorTipoEstimacion("Debe seleccionar un tipo de estimación.")
            return False
        self.vistaEstimacion.setErrorPeriodo("")
        if not self.ponderacionesValidas(ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior):
            self.vistaEstimacion.setErrorPonderaciones("Debe ingresar valores numéricos en porcentajes para las ponderaciones (0-100).")
            return False
        self.vistaEstimacion.setErrorPonderaciones("")
        return True

    def estimarCoordinaciones(self, alumnos, cupos):
        if not isinstance(alumnos,int):
            return None,None
        if not isinstance(cupos,int):
            return None,None
        if alumnos < 0:
            return None,None
        if cupos <= 0:
            return None,None
        if alumnos == 0:
            return 0,0
        coords = math.ceil(alumnos/cupos)
        coordsMargen = coords-1
        margen = math.floor(cupos * 1.1)
        if coords == 1:
            return 1,alumnos
        else:
            alumnosMargen = math.ceil(alumnos/coordsMargen)
            if alumnosMargen <= margen:
                return coordsMargen,alumnosMargen
            return coords,math.ceil(alumnos/coords)

    def periodoAnterior(self, ano, periodo):
        if periodo != 1 and periodo != 2:
            return None,None
        if periodo == 2:
            return ano, periodo - 1
        elif periodo == 1:
            return ano - 1, 2

    def anoValido(self,ano):
        if not ano.isnumeric():
            return False
        ano = int(ano)
        if ano >= 2015 and ano <= 2050:
            return True
    
    def periodoValido(self, periodo):
        if periodo == 1 or periodo == 2:
            return True

    def tipoEstimacionValida(self, tipoEstimacion):
        if tipoEstimacion == 1 or tipoEstimacion == 2:
            return True

    def ponderacionesValidas(self, ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior):
        if not ponderacionValoresHistoricos.isnumeric() or not ponderacionValoresPeriodoAnterior.isnumeric():
            return False
        valorHistorico = int(ponderacionValoresHistoricos)
        valorPeriodoAnterior = int(ponderacionValoresPeriodoAnterior)
        if valorHistorico + valorPeriodoAnterior != 100:
            return False
        return True

    def perteneceMBI(self, codigo):
        codigosInvalidos = [13300, 13302, 13303, 13305, 13307]
        if codigo < 13000 or codigo in codigosInvalidos:
            return True
        return False