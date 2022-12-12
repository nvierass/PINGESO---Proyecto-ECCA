from Vistas.VistaMalla import VistaMalla

from Controladores.ControladorEstimacion import ControladorEstimacion

class ControladorMallaInteractiva():

    def __init__(self, controladorPrincipal, databaseContext, GUI, plan, ano, semestre):
        self.GUI = GUI
        self.databaseContext = databaseContext
        self.controladorPrincipal = controladorPrincipal

        self.vistaMalla = VistaMalla(self)

        self.plan = plan
        self.ano = ano
        self.semestre = semestre

        anoAnterior, semestreAnterior = self.periodoAnterior(self.ano, self.semestre)
        self.datosHistoricos = self.databaseContext.obtenerTasasHistoricas()
        self.datosPeriodoActual = self.databaseContext.obtenerEstadisticasPeriodo(self.ano, self.semestre)
        self.datosPeriodoAnterior = self.databaseContext.obtenerEstadisticasPeriodo(anoAnterior, semestreAnterior)
        self.asignaturas = self.databaseContext.obtenerAsignaturas()

        self.vistaMalla.setDatosVista(self.ano, self.semestre, self.plan, self.asignaturas, self.datosPeriodoActual, self.datosHistoricos, self.datosPeriodoAnterior)
        self.mostrarVistaMalla()

    def mostrarVistaMalla(self):
        self.GUI.addWidget(self.vistaMalla)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)

    def volverContextoPrincipal(self):
        self.controladorPrincipal.mostrarVistaPrincipal()

    def periodoAnterior(self, ano, periodo):
        if periodo != 1 and periodo != 2:
            return None,None
        if periodo == 2:
            return ano, periodo - 1
        elif periodo == 1:
            return ano - 1, 2

    def realizarEstimacionPriori(self):
        codigoAsignatura = self.vistaMalla.getAsignaturaSeleccionada()
        asignatura = self.asignaturas[codigoAsignatura]
        controladorEstimacion = ControladorEstimacion(None, None, None, True)
        controladorEstimacion.asignaturas = self.asignaturas
        asignatura = controladorEstimacion.definirRequisitoPrioritario( codigoAsignatura, asignatura, self.datosPeriodoAnterior, self.datosHistoricos)
        resultado = controladorEstimacion.estimarAsignaturaPriori(asignatura, self.asignaturas, self.datosHistoricos, self.datosPeriodoAnterior, 0, 1).copy()
        self.vistaMalla.agregarResultado(codigoAsignatura, resultado)
        self.vistaMalla.mostrarResultado(resultado)

    def realizarEstimacionPosteriori(self):
        codigoAsignatura = self.vistaMalla.getAsignaturaSeleccionada()
        asignatura = self.asignaturas[codigoAsignatura]
        controladorEstimacion = ControladorEstimacion(None, None, None, True)
        controladorEstimacion.asignaturas = self.asignaturas
        asignatura = controladorEstimacion.definirRequisitoPrioritario( codigoAsignatura, asignatura, self.datosPeriodoAnterior, self.datosHistoricos)
        resultado = controladorEstimacion.estimarAsignaturaPosteriori(asignatura, self.asignaturas, self.datosHistoricos, self.datosPeriodoAnterior).copy()
        self.vistaMalla.agregarResultado(codigoAsignatura, resultado)
        self.vistaMalla.mostrarResultado(resultado)