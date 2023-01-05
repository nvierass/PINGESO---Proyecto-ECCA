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
        asignatura = controladorEstimacion.definirRequisitoPrioritario( codigoAsignatura, asignatura, self.datosPeriodoActual, self.datosHistoricos)
        resultado = controladorEstimacion.estimarAsignaturaPriori(asignatura, self.asignaturas, self.datosHistoricos, self.datosPeriodoActual, self.datosPeriodoAnterior, 0.5, 0.5)
        self.vistaMalla.agregarResultado(codigoAsignatura, resultado)
        self.vistaMalla.mostrarResultado(resultado)

    def realizarEstimacionPosteriori(self):
        codigoAsignatura = self.vistaMalla.getAsignaturaSeleccionada()
        asignatura = self.asignaturas[codigoAsignatura]
        controladorEstimacion = ControladorEstimacion(None, None, None, True)
        controladorEstimacion.asignaturas = self.asignaturas
        asignatura = controladorEstimacion.definirRequisitoPrioritario( codigoAsignatura, asignatura, self.datosPeriodoAnterior, self.datosHistoricos)
        resultado = controladorEstimacion.estimarAsignaturaPosteriori(asignatura, self.asignaturas, self.datosHistoricos, self.datosPeriodoActual)
        self.vistaMalla.agregarResultado(codigoAsignatura, resultado)
        self.vistaMalla.mostrarResultado(resultado)

    def actualizarDatosActuales(self):
        codigoAsignatura = self.vistaMalla.getAsignaturaEdicion()
        inscritosTeoria = self.vistaMalla.getInscritosTeoria()
        cuposTeoria = self.vistaMalla.getCuposTeoria()
        inscritosLaboratorio = self.vistaMalla.getInscritosLaboratorio()
        cuposLaboratorio = self.vistaMalla.getCuposLaboratorio()
        if not self.cantidadValida(inscritosTeoria, 0, 200):
            self.vistaMalla.mostrarAlerta("Advertencia", "El valor indicado para alumnos inscritos en teoría es invalido. (Valores permitidos [0-200])")
            return
        if not self.cantidadValida(cuposTeoria, 5, 80):
            self.vistaMalla.mostrarAlerta("Advertencia", "El valor indicado para coordinaciones de teoría es invalido. (Valores permitidos [5-80])")
            return
        if not self.cantidadValida(inscritosLaboratorio, 0, 200):
            self.vistaMalla.mostrarAlerta("Advertencia", "El valor indicado para alumnos inscritos en laboratorio es invalido. (Valores permitidos [0-200])")
            return
        if not self.cantidadValida(cuposLaboratorio, 5, 80):
            self.vistaMalla.mostrarAlerta("Advertencia", "El valor indicado para coordinaciones de laboratorio es invalido. (Valores permitidos [5-80])")
            return
        inscritosTeoria = int(inscritosTeoria)
        cuposTeoria = int(cuposTeoria)
        inscritosLaboratorio = int(inscritosLaboratorio)
        cuposLaboratorio = int(cuposLaboratorio)
        if codigoAsignatura in self.datosPeriodoActual:
            self.datosPeriodoActual[codigoAsignatura]["inscritosTeoria"] = inscritosTeoria
            self.asignaturas[codigoAsignatura].setCuposTeoria(cuposTeoria)
            self.datosPeriodoActual[codigoAsignatura]["inscritosLaboratorio"] = inscritosLaboratorio
            self.asignaturas[codigoAsignatura].setCuposLaboratorio(cuposLaboratorio)
        else:
            self.datosPeriodoActual[codigoAsignatura] = {}
            self.datosPeriodoActual[codigoAsignatura]["inscritosTeoria"] = inscritosTeoria
            self.datosPeriodoActual[codigoAsignatura]["inscritosLaboratorio"] = inscritosLaboratorio

        self.vistaMalla.datosPeriodoActual = self.datosPeriodoActual
        self.vistaMalla.asignaturas = self.asignaturas
        self.vistaMalla.restaurarBotones()

    def cantidadValida(self, cantidad, min, max):
        if not cantidad.isnumeric():
            return False
        cantidad = int(cantidad)
        if cantidad >= min and cantidad <= max:
            return True