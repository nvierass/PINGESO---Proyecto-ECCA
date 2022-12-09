import math

class EstadisticaAsignatura:
    def __init__(self, ano, semestre, codigo,it,at,rt,il,al,rl,tat,tal,td):
        self.ano = ano
        self.semestre = semestre
        self.codigo = codigo
        self.inscritosTeoria = it
        self.aprobadosTeoria = at
        self.reprobadosTeoria = rt
        self.inscritosLaboratorio = il
        self.aprobadosLaboratorio = al
        self.reprobadosLaboratorio = rl
        self.tasaAprobacionTeoria = tat
        self.tasaAprobacionLaboratorio = tal
        self.tasaDesinscripcion = td


    def agregarInscritos(self,coord,cantidad):
        valorValido,valor = self.validarCantidad(cantidad)
        if self.tipoCoordinacion(coord) == "Laboratorio":
            self.inscritosLaboratorio = self.inscritosLaboratorio + valor
        elif self.tipoCoordinacion(coord) == "Teoria":
            self.inscritosTeoria = self.inscritosTeoria + valor

    def agregarAprobados(self,coord,cantidad):
        cantidad = 0
        if not math.isnan(cantidad):
            cantidad = int(cantidad)
            if coord[0] == 'L':
                self.aprobadosLaboratorio = self.aprobadosLaboratorio + cantidad
            else:
                self.aprobadosTeoria = self.aprobadosTeoria + cantidad

    def agregarReprobados(self,coord,cantidad):
        cantidad = 0
        if not math.isnan(cantidad):
            cantidad = int(cantidad)
            if coord[0] == 'L':
                self.reprobadosLaboratorio =  self.reprobadosLaboratorio + cantidad
            else:
                self.reprobadosTeoria = self.reprobadosTeoria + cantidad

    def calcularTasas(self):
        if self.inscritosTeoria != 0:
            self.tasaAprobacionTeoria = self.aprobadosTeoria/self.inscritosTeoria
        if self.inscritosLaboratorio != 0:
            self.tasaAprobacionLaboratorio = self.aprobadosLaboratorio/self.inscritosLaboratorio
        if self.inscritosTeoria + self.inscritosLaboratorio > 0:
            self.tasaDesinscripcion = 1 - (self.aprobadosTeoria + self.aprobadosLaboratorio)/(self.inscritosTeoria + self.inscritosLaboratorio)

    def __str__(self):
        return f"Código:{self.codigo}\nPeriodo: {self.ano}-{self.semestre}\nTéoria:\tAprobados:{self.aprobadosTeoria}\tInscritos:{self.inscritosTeoria}\tTasa de aprobación:{self.tasaAprobacionTeoria*100}%\nLaboratorio:\n\tAprobados:{self.aprobadosLaboratorio}\tInscritos:{self.inscritosLaboratorio}\tTasa de aprobación:{self.tasaAprobacionLaboratorio}%\n"

    def validarCantidad(self, cantidad):
        if isinstance(cantidad,int):
            return True,cantidad
        elif isinstance(cantidad,str):
            try:
                valor = int(cantidad)
                return True,valor
            except:
                return False,0
        elif math.isnan(cantidad):
            return True,0
        else:
            return False,0

    def tipoCoordinacion(self, coordinacion):
        if isinstance(coordinacion,str):
            if coordinacion[0] == 'L':
                return "Laboratorio"
            else:
                return "Teoria"
        else:
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









