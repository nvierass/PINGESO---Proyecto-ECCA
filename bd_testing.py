from DatabaseDriver.DatabaseContext import DatabaseContext

db = DatabaseContext()
'''
rs = db.obtenerPlanes()

for index in rs:
    print("Nombre:",rs[index].getNombre())
    print("Version:",rs[index].getVersion())
    print("ID:",rs[index].getId())
    print("Niveles:",len(rs[index].getAsignaturas()))
    asignaturas = rs[index].getAsignaturas()
    for nivel in asignaturas:
        print("Nivel ",nivel,":")
        asignaturasNivel = asignaturas[nivel]
        for codigo in asignaturasNivel:
            print(codigo)
            

rs = db.obtenerAsignaturas()

for codigo in rs:
    print("\nAsignatura:", rs[codigo].getCodigo())
    print("\tNombre:",rs[codigo].getNombre())
    print("\tRequisitos:")
    requisitos = rs[codigo].getAsignaturasRequisitos()
    for nivel in requisitos:
        print("\t\tNivel: ",nivel , "Requisitos: ",requisitos[nivel])
    print("\t\tEquivalentes: ", rs[codigo].getAsignaturasEquivalentes())


rs = db.obtenerPlan(4)
if rs:
    print("Nombre:",rs.getNombre())
    print("Version:",rs.getVersion())
    print("ID:",rs.getId())
    print("Niveles:",len(rs.getAsignaturas()))
    asignaturas = rs.getAsignaturas()
    for nivel in asignaturas:
        print("Nivel ",nivel,":")
        asignaturasNivel = asignaturas[nivel]
        for codigo in asignaturasNivel:
            print(codigo)
else:
    print("No existe plan")


rs = db.obtenerEstadisticasAsignatura(13204)
for estadistica in rs:
    print(estadistica)
'''

print(db.obtenerEstadisticasAsignatura(10101))