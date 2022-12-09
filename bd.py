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
            '''

rs = db.obtenerAsignaturas()

for codigo in rs:
    print("\nAsignatura:", rs[codigo].getCodigo())
    print("\tNombre:",rs[codigo].getNombre())
    print("\tRequisitos:")
    requisitos = rs[codigo].getAsignaturasRequisitos()
    for nivel in requisitos:
        print("\t\tNivel: ",nivel , "Requisitos: ",requisitos[nivel])
    print("\t\tEquivalentes: ", rs[codigo].getAsignaturasEquivalentes())
