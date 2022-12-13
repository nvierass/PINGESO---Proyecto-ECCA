from Vistas.VistaRegistroPlan import VistaRegistroPlan
from Vistas.VistaRegistroAsignatura import VistaRegistroAsignatura
from Modelos.Asignatura import Asignatura
from Modelos.Plan import Plan

class ControladorRegistroPlan():

    def __init__(self, controladorPrincipal, databaseContext, GUI):
        self.GUI = GUI
        self.databaseContext = databaseContext
        self.controladorPrincipal = controladorPrincipal

        self.vistaRegistroPlan = VistaRegistroPlan(self)
        self.vistaRegistroAsignatura = VistaRegistroAsignatura(self)

        self.asignaturasRegistradas = self.databaseContext.obtenerAsignaturas()

        self.inicializarRegistroPlan()

        

    def mostrarVistaRegistroPlan(self):
        self.GUI.addWidget(self.vistaRegistroPlan)
        self.GUI.setCurrentIndex(self.GUI.currentIndex() + 1)

    def mostrarVistaRegistroAsignatura(self):
        self.GUI.addWidget(self.vistaRegistroAsignatura)
        self.GUI.setCurrentIndex(self.GUI.currentIndex() + 1)

    def volverContextoPrincipal(self):
        self.controladorPrincipal.mostrarVistaPrincipal()

    def inicializarRegistroPlan(self):
        self.vistaRegistroPlan.montarVista(self.asignaturasRegistradas)
        self.mostrarVistaRegistroPlan()

    def descripcionTipoAsignatura(self, tipo):
        if tipo == 1:
            return "Teoría"
        if tipo == 2:
            return "Laboratorio"
        if tipo == 3:
            return "Teoría y Laboratorio"
        return "Electivo"

    def convertirCodigosNivel(self, codigosNivelRequisitos):
        nivelesRequisitos = {}
        for nivel in codigosNivelRequisitos:
            for codigoAsignatura in codigosNivelRequisitos[nivel]:
                valorNivel = int(nivel)
                valorCodigo = int(codigoAsignatura)
                if valorNivel in nivelesRequisitos:
                    nivelesRequisitos[valorNivel].append(valorCodigo)
                else:
                    nivelesRequisitos[valorNivel] = [valorCodigo]
        return nivelesRequisitos

    def convertirCodigosEquivalentes(self, codigosEquivalentes):
        codigosNumericos = []
        for codigo in codigosEquivalentes:
            codigosNumericos.append(int(codigo))
        return codigosNumericos

    def inicializarRegistroAsignatura(self):
        self.vistaRegistroAsignatura.montarVista(self.asignaturasRegistradas)
        self.mostrarVistaRegistroAsignatura()

    def parametrosValidosNuevaAsignatura(self, codigo, nombre, tipo, nivelesIndicados):
        if not codigo.isnumeric():
            self.vistaRegistroAsignatura.mostrarAlerta("Error", "El código ingresado de la nueva asignatura debe ser un valor numérico.")
            return False
        valor = int(codigo)
        if valor in self.asignaturasRegistradas:
            self.vistaRegistroAsignatura.mostrarAlerta("Error", "Ya existe una asignatura registrada con ese código.")
            return False
        if valor < 13000 or valor >= 14000:
            self.vistaRegistroPlan.mostrarAlerta("Error", "El código ingresado para la nueva asignatura debe pertenecer al intervalo [13000 - 13999].")
            return False
        if nombre == "":
            self.vistaRegistroAsignatura.mostrarAlerta("Error", "Debe ingresar un nombre para la nueva asignatura.")
            return False
        if tipo <= 0 or tipo >= 5:
            self.vistaRegistroPlan.mostrarAlerta("Error", "Debe seleccionar un tipo de asignatura.")
            return False
        if not nivelesIndicados:
            self.vistaRegistroAsignatura.mostrarAlerta("Error", "Debe asignar el nivel de todos los requisitos seleccionados.")
            return False
        return True

    def registrarAsignatura(self):
        codigoAsignatura = self.vistaRegistroAsignatura.getCodigoNuevaAsignatura()
        nombre = self.vistaRegistroAsignatura.getNombreNuevaAsignatura()
        tipo = self.vistaRegistroAsignatura.getTipoNuevaAsignatura()
        nivelesIndicados = self.vistaRegistroAsignatura.nivelesIngresados()
        if not self.parametrosValidosNuevaAsignatura(codigoAsignatura, nombre, tipo, nivelesIndicados):
            return
        codigoAsignatura = int(codigoAsignatura)
        tipo = self.descripcionTipoAsignatura(tipo)
        nuevaAsignatura = Asignatura(codigoAsignatura, nombre, tipo)
        codigosEquivalentes = self.vistaRegistroAsignatura.getCodigosEquivalentes()
        codigosEquivalentes = self.convertirCodigosEquivalentes(codigosEquivalentes)
        codigosNivelRequisitos = self.vistaRegistroAsignatura.getCodigosNivelRequisitos()
        codigosNivelRequisitos = self.convertirCodigosNivel(codigosNivelRequisitos)
        nuevaAsignatura.setAsignaturasEquivalentes(codigosEquivalentes)
        nuevaAsignatura.setAsignaturasRequisitos(codigosNivelRequisitos)
        self.asignaturasRegistradas[codigoAsignatura] = nuevaAsignatura
        registroExitoso = self.databaseContext.insertarNuevaAsignatura(nuevaAsignatura)
        if registroExitoso:
            self.vistaRegistroAsignatura.mostrarAlerta("Registro exitoso.","La asignatura se ha registrado correctamente.")
        else:
            self.vistaRegistroAsignatura.mostrarAlerta("Error","La asignatura no se ha registrado correctamente.")
        self.inicializarRegistroPlan()

    def registrarPlan(self):
        nombre = self.vistaRegistroPlan.getNombre()
        version = self.vistaRegistroPlan.getVersion()
        duracion = self.vistaRegistroPlan.getDuracion()
        nivelesIndicados = self.vistaRegistroPlan.nivelesIngresados()
        if not self.parametrosValidosNuevoPlan(nombre, version, duracion, nivelesIndicados):
            return
        duracion = int(duracion)
        codigosNivelAsignaturas = self.vistaRegistroPlan.getCodigosNivelNuevoPlan()
        codigosNivelAsignaturas= self.convertirCodigosNivel(codigosNivelAsignaturas)
        nivelesIndicadosValidos = self.validarNivelesIndicados(duracion, codigosNivelAsignaturas)
        if not nivelesIndicadosValidos:
            return
        nuevoPlan = Plan(0, nombre, version, duracion)
        for nivel in codigosNivelAsignaturas:
            for codigo in codigosNivelAsignaturas[nivel]:
                nuevoPlan.agregarAsignatura(codigo, nivel)
        registroExitoso = self.databaseContext.insertarNuevoPlan(nuevoPlan)
        if not registroExitoso:
            self.vistaRegistroPlan.mostrarAlerta("Error","El nuevo plan de estudios no se ha registrado correctamente.")
            return
        idPlan = self.databaseContext.getIdPlan(nuevoPlan)
        if not idPlan:
            self.vistaRegistroPlan.mostrarAlerta("Error","El nuevo plan de estudios no se ha registrado correctamente.")
            return
        nuevoPlan.setId(idPlan)
        registroExitoso = self.databaseContext.insertarAsignaturasPlan(nuevoPlan)
        if not registroExitoso:
            self.vistaRegistroPlan.mostrarAlerta("Error","El nuevo plan de estudios no se ha registrado correctamente.")
            return
        self.vistaRegistroPlan.mostrarAlerta("Exito","El nuevo plan de estudios se ha registrado correctamente.")
        self.controladorPrincipal.actualizarVista()
        self.volverContextoPrincipal()

    def validarNivelesIndicados(self, duracion, codigosNivel):
        if len(codigosNivel) != duracion:
            self.vistaRegistroPlan.mostrarAlerta("Error", "Existen niveles incompletos dentro del nuevo plan que aún no poseen asignaturas.")
            return False
        for nivel in codigosNivel:
            if nivel > duracion:
                erroneas = ""
                for codigo in codigosNivel[nivel]:
                    erroneas += str(codigo) + ","
                self.vistaRegistroPlan.mostrarAlerta("Error", "Las asignaturas "+ erroneas + " se encuentran en un nivel invalido.")
                return False
        return True

    def parametrosValidosNuevoPlan(self, nombre, version, duracion, nivelesIndicados):
        if nombre == "":
            self.vistaRegistroPlan.mostrarAlerta("Error", "Debe ingresar un nombre para el nuevo plan de estudios.")
            return False
        if version == "":
            self.vistaRegistroPlan.mostrarAlerta("Error", "Debe ingresar la versión del nuevo plan de estudios.")
            return False
        if duracion == "":
            self.vistaRegistroPlan.mostrarAlerta("Error", "Debe ingresar la duración formal del nuevo plan de estudios.")
            return False
        if not duracion.isnumeric():
            self.vistaRegistroPlan.mostrarAlerta("Error", "La duración semestral debe ser un valor numérico.")
            return False
        valor = int(duracion)
        if valor <= 0 or valor > 16:
            self.vistaRegistroPlan.mostrarAlerta("Error", "La duración semestral ingresada del nuevo plan de estudios debe pertenecer al intervalo [1 - 16].")
            return False
        if not nivelesIndicados:
            self.vistaRegistroPlan.mostrarAlerta("Error", "Debe asignar el nivel de todas las asignaturas seleccionadas para el plan de estudios.")
            return False
        return True