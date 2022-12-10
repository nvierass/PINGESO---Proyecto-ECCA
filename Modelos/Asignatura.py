
class Asignatura():

    def __init__(self, codigo, nombre, tipo):
        self.codigo = codigo
        self.nombre = nombre
        self.tipoAsignatura = tipo
        self.asignaturasRequisitos = {}
        self.asignaturasEquivalentes = []
        self.estadisticasAsignatura = {}
        self.requisitoPrioritario = 0
        self.cuposTeoria = 30
        self.cuposLaboratorio = 10

    def getCodigo(self):
        return self.codigo

    def getNombre(self):
        return self.nombre

    def getTipoAsignatura(self):
        return self.tipoAsignatura

    def getAsignaturasRequisitos(self):
        return self.asignaturasRequisitos.copy()

    def getAsignaturasEquivalentes(self):
        return self.asignaturasEquivalentes.copy()

    def getEstadisticasAsignatura(self):
        return self.estadisticasAsignatura

    def getRequisitoPrioritario(self):
        return self.requisitoPrioritario

    def getCuposTeoria(self):
        return self.cuposTeoria
    
    def getCuposLaboratorio(self):
        return self.cuposLaboratorio

    def setCodigo(self, codigo):
        self.codigo = codigo

    def setNombre(self, nombre):
        self.nombre = nombre

    def setTipoAsignatura(self, tipoAsignatura):
        self.tipoAsignatura = tipoAsignatura

    def setAsignaturasRequisitos(self, asignaturasRequisitos):
        self.asignaturasRequisitos = asignaturasRequisitos.copy()

    def setAsignaturasEquivalentes(self, asignaturasEquivalentes):
        self.asignaturasEquivalentes = asignaturasEquivalentes.copy()

    def setEstadisticasAsignatura(self, estadisticasAsignatura):
        self.estadisticasAsignatura = estadisticasAsignatura

    def setRequisitoPrioritario(self, requisitoPrioritario):
        self.requisitoPrioritario = requisitoPrioritario

    def setCuposTeoria(self, cuposTeoria):
        self.cuposTeoria = cuposTeoria

    def setCuposLaboratorio(self, cuposLaboratorio):
        self.cuposLaboratorio = cuposLaboratorio

    def agregarAsignaturaRequisito(self, codigoRequisito, nivelRequisito):
        if nivelRequisito not in self.asignaturasRequisitos:
            self.asignaturasRequisitos[nivelRequisito] = [codigoRequisito]
        else:
            self.asignaturasRequisitos[nivelRequisito].append(codigoRequisito)

    def agregarAsignaturaEquivalente(self, codigoAsignaturaEquivalente):
        self.asignaturasEquivalentes.append(codigoAsignaturaEquivalente)

    def getCodigosRequisitos(self):
        codigos = []
        for nivel in self.asignaturasRequisitos:
            requisitosNivel = self.asignaturasRequisitos[nivel]
            for requisito in requisitosNivel:
                codigos.append(requisito)
        return codigos

    