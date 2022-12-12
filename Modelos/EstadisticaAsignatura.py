import math

class EstadisticaAsignatura:
    def __init__(self, ano, semestre, codigo):
        self.ano = ano
        self.semestre = semestre
        self.codigo = codigo
        self.inscritosTeoria = 0
        self.aprobadosTeoria = 0
        self.reprobadosTeoria = 0
        self.inscritosLaboratorio = 0
        self.aprobadosLaboratorio = 0
        self.reprobadosLaboratorio = 0
        self.tasaAprobacionTeoria = 0
        self.tasaAprobacionLaboratorio = 0
        self.tasaDesinscripcion = 0


    def agregarInscritos(self, coord, cantidad):
        valorValido,valor = self.validarCantidad(cantidad)
        if valorValido:
            if self.tipoCoordinacion(coord) == "Laboratorio":
                self.inscritosLaboratorio = self.inscritosLaboratorio + valor
            elif self.tipoCoordinacion(coord) == "Teoría":
                self.inscritosTeoria = self.inscritosTeoria + valor

    def agregarAprobados(self, coord, cantidad):
        valorValido,valor = self.validarCantidad(cantidad)
        if valorValido:
            if self.tipoCoordinacion(coord) == "Laboratorio":
                self.aprobadosLaboratorio = self.aprobadosLaboratorio + valor
            if self.tipoCoordinacion(coord) == "Teoría":
                self.aprobadosTeoria = self.aprobadosTeoria + valor

    def agregarReprobados(self, coord, cantidad):
        valorValido,valor = self.validarCantidad(cantidad)
        if valorValido:
            if self.tipoCoordinacion(coord) == "Laboratorio":
                self.reprobadosLaboratorio = self.reprobadosLaboratorio + valor
            if self.tipoCoordinacion(coord) == "Teoría":
                self.reprobadosTeoria = self.reprobadosTeoria + valor

    def calcularTasas(self):
        if self.inscritosTeoria != 0:
            self.tasaAprobacionTeoria = self.aprobadosTeoria / self.inscritosTeoria
        if self.inscritosLaboratorio != 0:
            self.tasaAprobacionLaboratorio = self.aprobadosLaboratorio / self.inscritosLaboratorio
        if (self.aprobadosTeoria + self.reprobadosTeoria > 0):
            self.tasaDesinscripcion = (self.inscritosTeoria - self.aprobadosTeoria - self.reprobadosTeoria) / self.inscritosTeoria  

    def __str__(self):
        return f"Código:{self.codigo}\nPeriodo: {self.ano}-{self.semestre}\nTéoria:\tAprobados:{self.aprobadosTeoria}\tInscritos:{self.inscritosTeoria}\tTasa de aprobación:{self.tasaAprobacionTeoria*100}%\nLaboratorio:\n\tAprobados:{self.aprobadosLaboratorio}\tInscritos:{self.inscritosLaboratorio}\tTasa de aprobación:{self.tasaAprobacionLaboratorio}%\n"

    def validarCantidad(self, cantidad):
        if isinstance(cantidad, int):
            return True, cantidad
        if isinstance(cantidad, str):
            try:
                valor = int(cantidad)
                return True, valor
            except:
                return False, 0
        if math.isnan(cantidad):
            return True, 0
        if isinstance(cantidad, float):
            return True, cantidad
        
        return False, 0

    def tipoCoordinacion(self, coordinacion):
        if isinstance(coordinacion,str):
            if coordinacion[0] == 'L':
                return "Laboratorio"
            else:
                return "Teoría"
        return None

    def getAno(self):
        return self.ano

    def getSemestre(self):
        return self.semestre

    def getCodigo(self):
        return self.codigo
        
    def getInscritosTeoria(self):
        return self.inscritosTeoria  

    def getAprobadosTeoria(self):
        return self.aprobadosTeoria
                
    def getReprobadosTeoria(self):
        return self.reprobadosTeoria
                
    def getInscritosLaboratorio(self):
        return self.inscritosLaboratorio
                
    def getAprobadosLaboratorio(self):
        return self.aprobadosLaboratorio
                
    def getReprobadosLaboratorio(self):
        return self.reprobadosLaboratorio
                
    def getTasaAprobacionTeoria(self):
        return self.tasaAprobacionTeoria
                
    def getTasaAprobacionLaboratorio(self):
        return self.tasaAprobacionLaboratorio
                
    def getTasaDesinscripcion(self):
        return self.tasaDesinscripcion

    def setAno(self, ano):
        self.ano = ano

    def setSemestre(self, semestre):
        self.semestre = semestre

    def setCodigo(self, codigo):
        self.codigo = codigo

    def setInscritosTeoria(self, inscritosTeoria):
        self.inscritosTeoria = inscritosTeoria

    def setAprobadosTeoria(self, aprobadosTeoria):
        self.aprobadosTeoria = aprobadosTeoria

    def setReprobadosTeoria(self, reprobadosTeoria):
        self.reprobadosTeoria = reprobadosTeoria

    def setInscritosLaboratorio(self, inscritosLaboratorio):
        self.inscritosLaboratorio = inscritosLaboratorio

    def setAprobadosLaboratorio(self, aprobadosLaboratorio):
        self.aprobadosLaboratorio = aprobadosLaboratorio

    def setReprobadosLaboratorio(self, reprobadosLaboratorio):
        self.reprobadosLaboratorio = reprobadosLaboratorio

    def setTasaAprobacionTeoria(self, tasaAprobacionTeoria):
        self.tasaAprobacionTeoria = tasaAprobacionTeoria

    def setTasaAprobacionLaboratorio(self, tasaAprobacionLaboratorio):
        self.tasaAprobacionLaboratorio = tasaAprobacionLaboratorio

    def setTasaDesinscripcion(self, tasaDesinscripcion):
        self.tasaDesinscripcion = tasaDesinscripcion



