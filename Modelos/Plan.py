

class Plan():
    
    def __init__(self, id, nombre, version, duracion):
        self.id = id
        self.nombre = nombre
        self.version = version
        self.duracion = duracion
        self.asignaturas = {}
        for i in range(0,duracion):
            self.asignaturas[i+1] = []

    def getId(self):
        return self.id

    def getNombre(self):
        return self.nombre

    def getVersion(self):
        return self.version

    def getAsignaturas(self):
        return self.asignaturas

    def setId(self, id):
        self.id = id

    def setNombre(self, nombre):
        self.nombre = nombre

    def setVersion(self, version):
        self.version = version
    
    def setAsignaturas(self, asignaturas):
        self.asignaturas = asignaturas

    def agregarAsignatura(self, codigoAsignatura, nivelAsignatura):
        self.asignaturas[nivelAsignatura].append(codigoAsignatura)


                