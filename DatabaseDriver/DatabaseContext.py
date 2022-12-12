import psycopg2 as pc

from Modelos.Plan import Plan
from Modelos.Asignatura import Asignatura

class DatabaseContext():

    def __init__(self):
        self.conn,self.cursor = self.connection()

    def connection(self):
        try:
            conn = pc.connect(database="ECCA",host="157.230.5.30",user="postgres",password="postgres",port=5432)
            #conn = pc.connect(database="ECCA",host="localhost",user="postgres",password="postgres",port=5432)
            cursor = conn.cursor()
            return conn,cursor
        except:
            print("Error en la conexión a la base de datos")
            return None,None

    def disconnect(self):
        try:
            self.conn.close()
        except:
            print("Error al cerrar la conexión a la base de datos")

    def obtenerPlanes(self):
        if self.conn != None:
            planes = {}
            query = "SELECT plan.id, nombre, version, duracion_semestres, cod_asignatura, nivel FROM plan INNER JOIN plan_asignatura ON plan.id = plan_asignatura.id_plan ORDER BY plan.id,nivel;" 
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            for resultado in resultados:
                idPlan = resultado[0]
                nombre = resultado[1]
                version = resultado[2]
                duracion = resultado[3]
                codigoAsignatura = resultado[4]
                nivelAsignatura = resultado[5]
                if idPlan in planes:
                    planes[idPlan].agregarAsignatura(codigoAsignatura,nivelAsignatura)
                else:
                    plan = Plan(idPlan, nombre, version, duracion)
                    plan.agregarAsignatura(codigoAsignatura, nivelAsignatura)
                    planes[idPlan] = plan
            return planes
        else:
            return None

    def existeAsignatura(self,codigo):
        existe = False
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "SELECT * FROM asignatura where codigo = " + str(codigo) + ";"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                existe = True
        return existe

        
    def obtenerAsignaturasPorIdPlan(self,idPlan):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select Asig.codigo from asignatura as Asig, plan_asignatura as PA where Asig.codigo = PA.cod_asignatura and PA.id_plan = " + str(idPlan) + ";"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            return resultados

    def obtenerEstadisticasTeoriaAsignatura(self,codigo,ano,periodo):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select inscritos_teoria,aprobados_teoria,tasa_aprobacion_teoria from estadistica_asignatura where cod_asignatura = " + str(codigo) + "and ano = " + str(ano) + "and semestre = "+ str(periodo) +";"
            self.cursor.execute(query)
            resultado = self.cursor.fetchone()
            return resultado

    def obtenerEstadisticasLaboratorioAsignatura(self,codigo,ano,periodo):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select inscritos_laboratorio,aprobados_laboratorio,tasa_aprobacion_laboratorio from estadistica_asignatura where cod_asignatura = " + str(codigo) + "and ano = " + str(ano) + "and semestre = "+ str(periodo) +";"
            self.cursor.execute(query)
            resultado = self.cursor.fetchone()
            return resultado

    def buscarEstadisticaAsignatura(self,ano,periodo,codigo):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select * from estadistica_asignatura where cod_asignatura = " + str(codigo) + "and ano =" + str(ano) + " and semestre =" + str(periodo) + ";"
            self.cursor.execute(query)
            resultado = self.cursor.fetchone()
            if resultado:
                return True,resultado
            else:
                return False,None

    def ingresarEstadisticasAsignaturas(self, ano, periodo, asignaturas):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            estadisticasExistentes = self.obtenerEstadisticasPeriodo(ano, periodo)
            query = ""
            for codigo in asignaturas:
                if codigo in estadisticasExistentes:
                    updateQuery = "UPDATE estadistica_asignatura SET " + \
                    "inscritos_teoria = " + str(asignaturas[codigo].inscritosTeoria) + \
                    ",aprobados_teoria = " + str(asignaturas[codigo].aprobadosTeoria) + \
                    ",reprobados_teoria = " + str(asignaturas[codigo].reprobadosTeoria) + \
                    ",inscritos_laboratorio = " + str(asignaturas[codigo].inscritosLaboratorio) + \
                    ",aprobados_laboratorio = " + str(asignaturas[codigo].aprobadosLaboratorio) + \
                    ",reprobados_laboratorio = " + str(asignaturas[codigo].reprobadosLaboratorio) + \
                    ",tasa_aprobacion_teoria = " + str(asignaturas[codigo].tasaAprobacionTeoria) + \
                    ",tasa_aprobacion_laboratorio = " + str(asignaturas[codigo].tasaAprobacionLaboratorio) + \
                    ",tasa_desinscripcion = " + str(asignaturas[codigo].tasaDesinscripcion) + \
                    "WHERE cod_asignatura = " + str(codigo) + " and ano = " + str(ano) + " and semestre = " + str(periodo) + ";"
                    query = query + updateQuery
                else:
                    insertQuery = "INSERT INTO estadistica_asignatura " + \
                    "(cod_asignatura, ano, semestre,inscritos_teoria,aprobados_teoria,reprobados_teoria,inscritos_laboratorio,aprobados_laboratorio,reprobados_laboratorio,tasa_aprobacion_teoria,tasa_aprobacion_laboratorio,tasa_desinscripcion) "+ \
                    "VALUES (" + str(codigo)+"," + str(ano)+"," + str(periodo)+"," + str(asignaturas[codigo].inscritosTeoria)+","+ str(asignaturas[codigo].aprobadosTeoria)+","+ str(asignaturas[codigo].reprobadosTeoria) + \
                    "," + str(asignaturas[codigo].inscritosLaboratorio)+","+ str(asignaturas[codigo].aprobadosLaboratorio)+"," + str(asignaturas[codigo].reprobadosLaboratorio) + \
                    "," + str(asignaturas[codigo].tasaAprobacionTeoria)+","+ str(asignaturas[codigo].tasaAprobacionLaboratorio)+","+ str(asignaturas[codigo].tasaDesinscripcion) + ");"
                    query = query + insertQuery
            self.cursor.execute(query)
            self.conn.commit()
        return

    def obtenerRequisitosAsignatura(self,codigo):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select cod_asignatura_requisito from requisito where cod_asignatura =" + str(codigo) + ";" 
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            if resultados:
                return True,resultados
            else:
                return False,None

    def obtenerNombreAsignatura(self,codigo):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select nombre from asignatura where codigo = " + str(codigo) + ";"
            self.cursor.execute(query)
            resultado = self.cursor.fetchone()
            return resultado
    
    def obtenerTipoAsignatura(self,codigo):#version si es lab o teoria etc
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select tipo from asignatura where codigo = " + str(codigo) + ";"
            self.cursor.execute(query)
            resultado = self.cursor.fetchone()
            return resultado
        
    # Para interactuar con la vista

    def obtenerDatosParaMostrarEnTabla(self, num):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select pa.id_plan, asn.codigo, asn.nombre, asn.tipo, asn.nivel, e.aprobados_teoria from asignatura as asn inner join estadistica_asignatura as e on asn.codigo = e.cod_asignatura inner join plan_asignatura as pa on pa.cod_asignatura = asn.codigo where pa.id_plan ="+str(num)+";"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            if resultados:
                return resultados
            else:
                return None

    def obtenerDatosParaMostrarEnMalla(self, idPlan):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select asn.codigo, asn.nivel, asn.nombre, pa.id_plan from asignatura as asn inner join plan_asignatura as pa on pa.cod_asignatura = asn.codigo where id_plan ="+str(idPlan)+" order by asn.nivel asc;" 
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            if resultados:
                return resultados
            else:
                return None

    def obtenerPlanFromId(self, idPlan):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select * from plan where id="+str(idPlan)+";"
            self.cursor.execute(query)
            resultados = self.cursor.fetchone()
            if resultados:
                return resultados
            else:
                return None

    def obtenerDatosDeAsignaturaParaMostrar(self, codigo):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select * from estadistica_asignatura as ea inner join asignatura as asn on asn.codigo = ea.cod_asignatura where asn.codigo="+str(codigo)+";" 
            self.cursor.execute(query)
            resultado = self.cursor.fetchone() #ojo que se toma solo el primer valor, podria verse para mas valores eventualemente
            if resultado:
                return resultado
            else:
                return None

    #Esta es muy similar a obtenerAsignaturasPorIdPlan, solo que también obtiene el nombre de la asignatura
    def obtenerDatosAsignaturasPorIdPlan(self, idPlan):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select Asig.codigo, Asig.nombre from asignatura as Asig, plan_asignatura as PA where Asig.codigo = PA.cod_asignatura and PA.id_plan = " + str(idPlan) + ";"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            return resultados

    def obtenerTasasHistoricas(self):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select cod_asignatura,avg(tasa_aprobacion_teoria),avg(tasa_aprobacion_laboratorio),avg(tasa_desinscripcion) from estadistica_asignatura group by cod_asignatura;"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            diccionario = {}
            for resultado in resultados:
                diccionario[resultado[0]] = {
                                            "tasaAprobacionTeoria": resultado[1],
                                            "tasaAprobacionLaboratorio": resultado[2],
                                            "tasaDesinscripcion": resultado[3]
                                            }
            return diccionario

    def obtenerEstadisticasPeriodo(self, ano, semestre):
        if self.conn == None:
            print("Error en la conexión a la base de datos")
        else:
            query = "select cod_asignatura,inscritos_teoria,aprobados_teoria,reprobados_teoria,inscritos_laboratorio,aprobados_laboratorio,reprobados_laboratorio,tasa_aprobacion_teoria,tasa_aprobacion_laboratorio,tasa_desinscripcion from estadistica_asignatura where ano =" + str(ano) + "and semestre ="+ str(semestre) + ";"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            diccionario = {}
            for resultado in resultados:
                diccionario[resultado[0]] = {   
                                            "inscritosTeoria": resultado[1],
                                            "aprobadosTeoria": resultado[2],
                                            "reprobadosTeoria": resultado[3],
                                            "inscritosLaboratorio": resultado[4],
                                            "aprobadosLaboratorio": resultado[5],
                                            "reprobadosLaboratorio": resultado[6],
                                            "tasaAprobacionTeoria": resultado[7],
                                            "tasaAprobacionLaboratorio": resultado[8],
                                            "tasaDesinscripcion": resultado[9]
                                             }
            return diccionario


    def obtenerAsignaturas(self):
        if self.conn == None:
            return None
        else:
            queryAsignaturas = "select * from asignatura;"
            self.cursor.execute(queryAsignaturas)
            resultados = self.cursor.fetchall()
            asignaturas = {}
            for resultado in resultados:
                codigoAsignatura = resultado[0]
                nombre = resultado[1]
                tipo = resultado[2]
                asignaturas[codigoAsignatura] = Asignatura(codigoAsignatura, nombre, tipo)

            queryRequisitos = "select cod_asignatura,cod_asignatura_requisito,nivel_requisito from requisito;"
            self.cursor.execute(queryRequisitos)
            resultados = self.cursor.fetchall()
            for resultado in resultados:
                codigoAsignatura = resultado[0]
                codigoRequisito = resultado[1]
                nivelRequisito = resultado[2]
                asignaturas[codigoAsignatura].agregarAsignaturaRequisito(codigoRequisito, nivelRequisito)

            queryEquivalentes = "select cod_asignatura, cod_asignatura_analoga from analoga;"
            self.cursor.execute(queryEquivalentes)
            resultados = self.cursor.fetchall()
            for resultado in resultados:
                codigoAsignatura = resultado[0]
                codigoAsignaturaEquivalente = resultado[1]
                asignaturas[codigoAsignatura].agregarAsignaturaEquivalente(codigoAsignaturaEquivalente)
            return asignaturas

    def obtenerPlan(self, idPlan):
        try:
            if self.conn != None:
                query = "SELECT nombre, version, duracion_semestres, cod_asignatura, nivel FROM plan INNER JOIN plan_asignatura ON plan.id = plan_asignatura.id_plan where plan.id = " + str(idPlan) + "ORDER BY nivel;" 
                self.cursor.execute(query)
                resultados = self.cursor.fetchall()
                resultado = resultados[0]
                nombre = resultado[0]
                version = resultado[1]
                duracion = resultado[2]
                plan = Plan(idPlan, nombre, version, duracion)
                for resultado in resultados:
                    codigoAsignatura = resultado[3]
                    nivelAsignatura = resultado[4]
                    plan.agregarAsignatura(codigoAsignatura, nivelAsignatura)
                return plan
        except:
            return None