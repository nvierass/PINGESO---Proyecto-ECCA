from Vistas.VistaRegistroPlan import VistaRegistroPlan
from Vistas.VistaRegistroAsignatura import VistaRegistroAsignatura
from Modelos.Asignatura import Asignatura

class ControladorRegistroPlan():

    def __init__(self, controladorPrincipal, databaseContext, GUI):
        self.GUI = GUI
        self.databaseContext = databaseContext
        self.controladorPrincipal = controladorPrincipal

        self.vistaRegistroPlan = VistaRegistroPlan(self)
        self.vistaRegistroAsignatura = VistaRegistroAsignatura(self)

        self.asignaturasRegistradas = self.databaseContext.obtenerAsignaturas()


        self.mostrarVistaRegistroPlan()
        

    def mostrarVistaRegistroPlan(self):
        self.GUI.addWidget(self.vistaRegistroPlan)
        self.GUI.setCurrentIndex(self.GUI.currentIndex() + 1)

    def mostrarVistaRegistroAsignatura(self):
        self.GUI.addWidget(self.vistaRegistroAsignatura)
        self.GUI.setCurrentIndex(self.GUI.currentIndex() + 1)

    def volverContextoPrincipal(self):
        self.controladorPrincipal.mostrarVistaPrincipal()


    def registrarAsignatura(self):
        codigoAsignatura = self.vistaRegistroAsignatura.getCodigoNuevaAsignatura()
        nombre = self.vistaRegistroAsignatura.getNombreNuevaAsignatura()
        tipo = self.vistaRegistroAsignatura.getTipoNuevaAsignatura()
        if not self.parametrosValidos(codigoAsignatura, nombre, tipo):
            return
        codigoAsignatura = int(codigoAsignatura)
        nuevaAsignatura = Asignatura(codigoAsignatura, nombre, tipo)
        codigosEquivalentes = self.vistaRegistroAsignatura.getCodigosEquivalentes()
        codigosNivelRequisitos = self.vistaRegistroAsignatura.getCodigosNivelRequisitos()

    def inicializarRegistroAsignatura(self):
        self.vistaRegistroAsignatura.montarVista(self.asignaturasRegistradas)
        self.mostrarVistaRegistroAsignatura()

    def parametrosValidos(self, codigo, nombre, tipo):
        if not codigo.isnumeric():
            self.vistaRegistroAsignatura.mostrarAlerta("Error", "El código ingresado debe ser un valor numérico.")
            return False
        valor = int(codigo)
        if nombre == "":
            self.vistaRegistroAsignatura.mostrarAlerta("Error", "Debe ingresar un nombre para la asignatura.")
            return False
        if valor < 13000 or valor >= 14000:
            self.vistaRegistroPlan.mostrarAlerta("Error", "El código ingresado debe pertenecer al intervalo [13000 - 13999].")
            return False
        if tipo <= 0 or tipo >= 5:
            self.vistaRegistroPlan.mostrarAlerta("Error", "Debe seleccionar un tipo de asignatura.")
            return False
        return True