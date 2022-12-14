import xlsxwriter as xl
import math
import sys

from Vistas.VistaEstimacion import VistaEstimacion
from Vistas.VistaCupos import VistaCupos
from Vistas.VistaResultados import VistaResultados

class ControladorEstimacion():

    def __init__(self, controladorPrincipal, databaseContext, GUI, flagInteractiva):
        if not flagInteractiva:
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

    def definirRequisitoPrioritario(self, codigo, asignatura, datosPeriodoAnterior, datosHistoricos):
        requisitoEncontrado, requisito = self.aplicarCriterioPrioritarioNivel(codigo)
        if not requisitoEncontrado:
            requisitosMayorNivel = requisito
            requisitoEncontrado, requisito = self.aplicarCriterioPrioritarioDificultad(requisitosMayorNivel, datosHistoricos)
        if not requisitoEncontrado:
            requisitosCandidatos = requisito
            requisitoEncontrado, requisito = self.aplicarCriterioPrioritarioCantidadAlumnos(requisitosCandidatos, datosPeriodoAnterior)
        asignatura.setRequisitoPrioritario(requisito)
        return asignatura

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

    def aplicarCriterioPrioritarioCantidadAlumnos(self, requisitosPotenciales, datosPeriodoAnterior):
        requisitosCandidatos = []
        menorCantidadAlumnos = 1000
        for requisitoCandidato in requisitosPotenciales:
            if (not self.perteneceMBI(requisitoCandidato)) and (requisitoCandidato in datosPeriodoAnterior):
                alumnosInscritos = datosPeriodoAnterior[requisitoCandidato]["inscritosTeoria"]
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
        guardadoExitoso = self.generarReporte(nombreArchivoSalida)
        if not guardadoExitoso:
            self.vistaResultados.mostrarAlerta("Error","No se ha logrado exportar los resultados.")

    def generarReporte(self, nombre):
        try:
            workbook = xl.Workbook(nombre)
            worksheet = workbook.add_worksheet()
            columnas = ["Código","Nombre Asignatura","Alumnos estimados teoría","Alumnos estimados laboratorio","Coordinaciones estimadas teoría","Coordinaciones estimadas laboratorio","Observaciones"]
            formatoHeader = workbook.add_format(
                {
                    "bg_color": "#95B3D7",
                    "border": 1,
                    "align": "center",
                    "bold": True
                }
            )
            formatoFila = workbook.add_format(
                {
                    "bg_color": "#D9D9D9",
                    "align": "center",
                    "border": 1
                }
            )
            worksheet.set_column(0, 0, 15)
            worksheet.set_column(1, 1, 70)
            worksheet.set_column(2, 2, 30)
            worksheet.set_column(3, 3, 30)
            worksheet.set_column(4, 4, 35)
            worksheet.set_column(5, 5, 35)
            worksheet.set_column(6, 6, 100)
            column = 0
            for columna in columnas:
                worksheet.write(0,column,columna,formatoHeader)
                column = column + 1
            row = 1
            for codigoAsignatura in self.resultadosEstimacion:
                if not self.perteneceMBI(codigoAsignatura):
                    worksheet.write(row,0,self.resultadosEstimacion[codigoAsignatura]["codigo"],formatoFila)
                    worksheet.write(row,1,self.resultadosEstimacion[codigoAsignatura]["nombre"],formatoFila)
                    worksheet.write(row,2,self.resultadosEstimacion[codigoAsignatura]["estimadosTeoria"],formatoFila)
                    worksheet.write(row,3,self.resultadosEstimacion[codigoAsignatura]["estimadosLaboratorio"],formatoFila)
                    worksheet.write(row,4,self.resultadosEstimacion[codigoAsignatura]["coordinacionesTeoria"],formatoFila)
                    worksheet.write(row,5,self.resultadosEstimacion[codigoAsignatura]["coordinacionesLaboratorio"],formatoFila)
                    worksheet.write(row,6,self.resultadosEstimacion[codigoAsignatura]["observaciones"],formatoFila)
                    row += 1
            workbook.close()
            return True
        except:
            return False

    def inicializarEstimacion(self):
        ano = self.vistaEstimacion.getAno()
        semestre = self.vistaEstimacion.getPeriodo()
        tipoEstimacion = self.vistaEstimacion.getTipoEstimacion()
        ponderacionValoresHistoricos = self.vistaEstimacion.getPonderacionValoresHistoricos()
        ponderacionValoresPeriodoAnterior = self.vistaEstimacion.getPonderacionValoresPeriodoAnterior()
        parametrosValidos = self.validarParametrosEstimacion(ano, semestre, tipoEstimacion, ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior)
        if not parametrosValidos:
            return 
        ano = int(ano)
        self.ponderacionValoresHistoricos = int(ponderacionValoresHistoricos) / 100
        self.ponderacionValoresPeriodoAnterior = int(ponderacionValoresPeriodoAnterior) / 100
        self.tipoEstimacion = tipoEstimacion
        anoPeriodoAnterior, semestrePeriodoAnterior = self.periodoAnterior(ano, semestre)        
        self.datosHistoricos = self.databaseContext.obtenerTasasHistoricas()
        self.datosPeriodoAnterior = self.databaseContext.obtenerEstadisticasPeriodo(anoPeriodoAnterior, semestrePeriodoAnterior)
        self.asignaturas = self.determinarRequisitosPrioritarios(self.asignaturas, self.datosPeriodoAnterior, self.datosHistoricos)
        self.vistaCupos.montarVista(self.asignaturas)
        self.mostrarVistaCupos()
        
    def realizarEstimacion(self):
        self.asignaturas = self.vistaCupos.actualizarCuposAsignaturas(self.asignaturas)
        self.resultadosEstimacion = self.estimarAsignaturas(self.asignaturas, self.tipoEstimacion, self.datosHistoricos, self.datosPeriodoAnterior, self.ponderacionValoresHistoricos, self.ponderacionValoresPeriodoAnterior)
        self.vistaResultados.montarVista(self.resultadosEstimacion)
        self.mostrarVistaResultados()
        self.mostrarAsignaturas()

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

    def estimarAsignaturas(self, asignaturas, tipoEstimacion, datosHistoricos, datosPeriodoAnterior, ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior):
        resultados = {}
        for codigoAsignatura in asignaturas:
            asignatura = asignaturas[codigoAsignatura]
            resultado = {}
            estimadaAnteriormente, codigoEstimada = self.estimadaAnteriormente(asignatura, self.resultadosEstimacion)
            if estimadaAnteriormente:
                resultado = {
                    "codigo": codigoAsignatura,
                    "nombre": asignatura.getNombre(),
                    "estimadosTeoria": 0,
                    "estimadosLaboratorio": 0,
                    "coordinacionesTeoria": 0,
                    "coordinacionesLaboratorio": 0,
                    "observaciones": "Asignatura ya ha sido estimada en la asignatura equivalente con codigo: " + str(codigoEstimada)
                    } 
            else:
                if tipoEstimacion == 1:
                    resultado = self.estimarAsignaturaPriori(asignatura, self.asignaturas, datosHistoricos, datosPeriodoAnterior, ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior)
                else:
                    resultado = self.estimarAsignaturaPosteriori(asignatura, self.asignaturas, datosHistoricos, datosPeriodoAnterior)
            resultados[codigoAsignatura] = resultado
        return resultados

    def estimarAsignaturaPriori(self, asignatura, asignaturas, datosHistoricos, datosPeriodoAnterior, ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior):
        codigoAsignatura = asignatura.getCodigo()
        nombreAsignatura = asignatura.getNombre()
        requisitoPrioritario = asignatura.getRequisitoPrioritario()
        if self.esElectivo(asignatura):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, asignaturas de naturaleza electivos o tópicos no son considerados validos para estimación."
                } 
            return resultado
        if self.perteneceMBI(codigoAsignatura):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, asignatura pertenece al módulo básico de ingeniería."
                } 
            return resultado    
        if self.perteneceMBI(requisitoPrioritario):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, requisito prioritario pertenece al módulo básico de ingeniería."
                } 
            return resultado
        if (requisitoPrioritario not in datosPeriodoAnterior) or (requisitoPrioritario not in datosHistoricos):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, faltan estadísticas curriculares de los requisitos para estimar esta asignatura."
                } 
            return resultado
        if (codigoAsignatura not in datosPeriodoAnterior) or (codigoAsignatura not in datosHistoricos):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, faltan estadísticas curriculares para estimar esta asignatura."
                } 
            return resultado

        alumnosDisponiblesInscripcion = self.obtenerDisponiblesInscripcion(codigoAsignatura, asignaturas, datosPeriodoAnterior, datosHistoricos)

        inscritosTeoria = self.obtenerCantidadAlumnoPeriodo(codigoAsignatura, asignaturas, datosPeriodoAnterior, "inscritosTeoria")
        tasaReprobacionTeoria = ponderacionValoresHistoricos * (1 - datosHistoricos[codigoAsignatura]["tasaAprobacionTeoria"]) + ponderacionValoresPeriodoAnterior * (1 - datosPeriodoAnterior[codigoAsignatura]["tasaAprobacionTeoria"])
        inscritosTeoriaRequisitos= self.obtenerCantidadAlumnoPeriodo(requisitoPrioritario, asignaturas, datosPeriodoAnterior, "inscritosTeoria")
        tasaAprobacionTeoriaRequisito = ponderacionValoresHistoricos * datosHistoricos[requisitoPrioritario]["tasaAprobacionTeoria"] + ponderacionValoresPeriodoAnterior * datosPeriodoAnterior[requisitoPrioritario]["tasaAprobacionTeoria"]

        alumnosReprobadosAsignaturaTeoria = inscritosTeoria * tasaReprobacionTeoria
        alumnosAprobadosRequisitoPrioritarioTeoria = inscritosTeoriaRequisitos * tasaAprobacionTeoriaRequisito

        inscritosLaboratorio = self.obtenerCantidadAlumnoPeriodo(codigoAsignatura, asignaturas, datosPeriodoAnterior, "inscritosLaboratorio")
        tasaReprobacionLaboratorio = ponderacionValoresHistoricos * (1 - datosHistoricos[codigoAsignatura]["tasaAprobacionLaboratorio"]) + ponderacionValoresPeriodoAnterior * (1 - datosPeriodoAnterior[codigoAsignatura]["tasaAprobacionLaboratorio"])
        inscritosLaboratorioRequisitos= self.obtenerCantidadAlumnoPeriodo(requisitoPrioritario, asignaturas, datosPeriodoAnterior, "inscritosLaboratorio")
        tasaAprobacionLaboratorioRequisito = ponderacionValoresHistoricos * datosHistoricos[requisitoPrioritario]["tasaAprobacionLaboratorio"] + ponderacionValoresPeriodoAnterior * datosPeriodoAnterior[requisitoPrioritario]["tasaAprobacionLaboratorio"]

        alumnosReprobadosAsignaturaLaboratorio = inscritosLaboratorio * tasaReprobacionLaboratorio
        alumnosAprobadosRequisitoPrioritarioLaboratorio = inscritosLaboratorioRequisitos * tasaAprobacionLaboratorioRequisito

        estimadosTeoria = math.ceil(alumnosDisponiblesInscripcion + alumnosReprobadosAsignaturaTeoria + alumnosAprobadosRequisitoPrioritarioTeoria)
        estimadosLaboratorio = math.ceil(alumnosDisponiblesInscripcion + alumnosReprobadosAsignaturaLaboratorio + alumnosAprobadosRequisitoPrioritarioLaboratorio)

        coordinacionesTeoria, _ = self.estimarCoordinaciones(estimadosTeoria, asignatura.getCuposTeoria())
        coordinacionesLaboratorio, _ = self.estimarCoordinaciones(estimadosLaboratorio, asignatura.getCuposLaboratorio())
        resultado = {
            "codigo": codigoAsignatura,
            "nombre": nombreAsignatura,
            "estimadosTeoria": estimadosTeoria,
            "estimadosLaboratorio": estimadosLaboratorio,
            "coordinacionesTeoria": coordinacionesTeoria,
            "coordinacionesLaboratorio": coordinacionesLaboratorio,
            "observaciones":    "Contribuciones Teoría: Disponibles = " + str(math.ceil(alumnosDisponiblesInscripcion)) + ", Reprobados = " + str(math.ceil(alumnosReprobadosAsignaturaTeoria)) + ", Aprobados Requisito = " + str(math.ceil(alumnosAprobadosRequisitoPrioritarioTeoria)) + ".\n" + \
                                "Contribuciones Laboratorio: Disponibles = " + str(math.ceil(alumnosDisponiblesInscripcion)) + ", Reprobados = " + str(math.ceil(alumnosReprobadosAsignaturaLaboratorio)) + ", Aprobados Requisito = " + str(math.ceil(alumnosAprobadosRequisitoPrioritarioLaboratorio)) + "."
            } 
        return resultado

    def estimadaAnteriormente(self, asignatura, resultados):
        asignaturasEquivalentes = asignatura.getAsignaturasEquivalentes()
        for codigoAsignatura in asignaturasEquivalentes:
            if codigoAsignatura in resultados:
                return True, codigoAsignatura
        return False, None

    def estimarAsignaturaPosteriori(self, asignatura, asignaturas, datosHistoricos, datosPeriodoAnterior):
        codigoAsignatura = asignatura.getCodigo()
        nombreAsignatura = asignatura.getNombre()
        requisitoPrioritario = asignatura.getRequisitoPrioritario()
        if self.esElectivo(asignatura):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, asignaturas de naturaleza electivos o tópicos no son considerados validos para estimación."
                } 
            return resultado
        if self.perteneceMBI(codigoAsignatura):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, asignatura pertenece al módulo básico de ingeniería."
                } 
            return resultado    
        if self.perteneceMBI(requisitoPrioritario):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, requisito prioritario pertenece al módulo básico de ingeniería."
                } 
            return resultado
        if (requisitoPrioritario not in datosPeriodoAnterior) or (requisitoPrioritario not in datosHistoricos):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, faltan estadísticas curriculares de los requisitos para estimar esta asignatura."
                } 
            return resultado
        if (codigoAsignatura not in datosPeriodoAnterior) or (codigoAsignatura not in datosHistoricos):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, faltan estadísticas curriculares para estimar esta asignatura."
                } 
            return resultado
        if ("aprobadosTeoria" not in datosPeriodoAnterior[codigoAsignatura]) or ("aprobadosLaboratorio" not in datosPeriodoAnterior[codigoAsignatura]):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, faltan estadísticas curriculares de aprobación para estimar esta asignatura."
                } 
            return resultado
        if ("aprobadosTeoria" not in datosPeriodoAnterior[requisitoPrioritario]) or ("aprobadosLaboratorio" not in datosPeriodoAnterior[requisitoPrioritario]):
            resultado = {
                "codigo": codigoAsignatura,
                "nombre": nombreAsignatura,
                "estimadosTeoria": 0,
                "estimadosLaboratorio": 0,
                "coordinacionesTeoria": 0,
                "coordinacionesLaboratorio": 0,
                "observaciones": "Estimación no realizada, faltan estadísticas curriculares de aprobación de los requisitos para estimar esta asignatura."
                } 
            return resultado

        alumnosDisponiblesInscripcion = self.obtenerDisponiblesInscripcion(codigoAsignatura, asignaturas,  datosHistoricos, datosPeriodoAnterior)

        alumnosReprobadosAsignaturaTeoria = self.obtenerCantidadAlumnoPeriodo(codigoAsignatura, asignaturas, datosPeriodoAnterior, "reprobadosTeoria")
        alumnosAprobadosTeoriaRequisito = self.obtenerCantidadAlumnoPeriodo(codigoAsignatura, asignaturas, datosPeriodoAnterior, "aprobadosTeoria")

        alumnosReprobadosAsignaturaLaboratorio = self.obtenerCantidadAlumnoPeriodo(codigoAsignatura, asignaturas, datosPeriodoAnterior, "reprobadosLaboratorio")
        alumnosAprobadosLaboratorioRequisito = self.obtenerCantidadAlumnoPeriodo(codigoAsignatura, asignaturas, datosPeriodoAnterior, "aprobadosLaboratorio")

        estimadosTeoria = math.ceil(alumnosDisponiblesInscripcion + alumnosReprobadosAsignaturaTeoria + alumnosAprobadosTeoriaRequisito)
        estimadosLaboratorio = math.ceil(alumnosDisponiblesInscripcion + alumnosReprobadosAsignaturaLaboratorio + alumnosAprobadosLaboratorioRequisito)

        coordinacionesTeoria, _ = self.estimarCoordinaciones(estimadosTeoria, asignatura.getCuposTeoria())
        coordinacionesLaboratorio, _ = self.estimarCoordinaciones(estimadosLaboratorio, asignatura.getCuposLaboratorio())
        resultado = {
            "codigo": codigoAsignatura,
            "nombre": nombreAsignatura,
            "estimadosTeoria": estimadosTeoria,
            "estimadosLaboratorio": estimadosLaboratorio,
            "coordinacionesTeoria": coordinacionesTeoria,
            "coordinacionesLaboratorio": coordinacionesLaboratorio,
            "observaciones": ""
            } 
        return resultado

    def obtenerCantidadAlumnoPeriodo(self, codigoAsignatura, asignaturas, datosPeriodoAnterior, flagTipo):
        asignatura = asignaturas[codigoAsignatura]
        if self.perteneceMBI(codigoAsignatura):
            return 0
        asignaturasEquivalentes = asignatura.getAsignaturasEquivalentes()
        asignaturasEquivalentes.append(codigoAsignatura)
        total = 0
        for codigoAsignaturaEquivalente in asignaturasEquivalentes:
            total += datosPeriodoAnterior[codigoAsignaturaEquivalente][flagTipo]
        return total
        
    def obtenerDisponiblesInscripcion(self, codigoAsignatura, asignaturas, datosPeriodoAnterior, datosHistoricos):
        asignatura = asignaturas[codigoAsignatura]
        if self.perteneceMBI(codigoAsignatura):
            return 0
        asignaturasEquivalentes = asignatura.getAsignaturasEquivalentes()
        asignaturasEquivalentes.append(codigoAsignatura)
        disponibles = 0
        for codigoAsignatura in asignaturasEquivalentes:
            if not (codigoAsignatura in datosPeriodoAnterior and codigoAsignatura in datosHistoricos):
                disponibles += 0
            if not ("inscritosTeoria" in datosPeriodoAnterior[codigoAsignatura] and "tasaDesinscripcion" in datosHistoricos[codigoAsignatura]):
                disponibles += 0
            else:
                cantidadDesinscribe = datosPeriodoAnterior[codigoAsignatura]["inscritosTeoria"] * datosHistoricos[codigoAsignatura]["tasaDesinscripcion"]
                disponibles += cantidadDesinscribe
        return disponibles

    def determinarRequisitosPrioritarios(self, asignaturas, datosPeriodoAnterior, datosHistoricos):
        asignaturasRequisitoDefinido = {}
        for codigoAsignatura in asignaturas:
            asignatura = asignaturas[codigoAsignatura]
            asignaturasRequisitoDefinido[codigoAsignatura] = self.definirRequisitoPrioritario(codigoAsignatura, asignatura, datosPeriodoAnterior, datosHistoricos)
        return asignaturasRequisitoDefinido

    def validarParametrosEstimacion(self, ano, periodo, tipoEstimacion, ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior):
        if not self.anoValido(ano):
            self.vistaEstimacion.setErrorAno("El valor ingresado es invalido, año debe ser un valor numérico.\n(Periodos admitidos corresponden al intervalo 2015-2050).")
            return False
        self.vistaEstimacion.setErrorAno("")
        if not self.periodoValido(periodo):
            self.vistaEstimacion.setErrorPeriodo("Debe seleccionar un periodo lectivo.")
            return False
        self.vistaEstimacion.setErrorPeriodo("")
        if not self.tipoEstimacionValida(tipoEstimacion):
            self.vistaEstimacion.setErrorTipoEstimacion("Debe seleccionar un tipo de estimación.")
            return False
        self.vistaEstimacion.setErrorTipoEstimacion("")
        if not self.ponderacionesValidas(ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior):
            self.vistaEstimacion.setErrorPonderaciones("Debe ingresar valores numéricos en porcentajes para las ponderaciones.\n(Valores entre 1 y 100, la suma debe ser 100).")
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
        if codigo == None:
            return False
        codigosMBI = [13300, 13303, 13305, 13307]
        if codigo < 13000:
            return True
        if codigo in codigosMBI:
            return True
        return False

    def esElectivo(self, asignatura):
        if asignatura.getTipoAsignatura() == "Electivo":
            return True
        return False