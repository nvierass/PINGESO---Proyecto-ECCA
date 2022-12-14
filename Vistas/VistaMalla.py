import os
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from functools import partial
import math

class VistaMalla(QMainWindow):

    def __init__(self, controladorMallaInteractiva):
        super(VistaMalla, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/malla.ui"), self)

        self.controladorMallaInteractiva = controladorMallaInteractiva
        self.button_volver.clicked.connect(self.controladorMallaInteractiva.volverContextoPrincipal)
        self.button_estimar_1.clicked.connect(self.controladorMallaInteractiva.realizarEstimacionPriori)
        self.button_estimar_2.clicked.connect(self.controladorMallaInteractiva.realizarEstimacionPosteriori)
        self.button_editar_pa.clicked.connect(self.clickBotonEditar)
        self.button_guardar.clicked.connect(self.controladorMallaInteractiva.actualizarDatosActuales)
        self.codigoAsignaturaSeleccionada = None
        self.codigoAsignaturaEdicion = None
        self.resultados = {}
        self.botones = {}
        self.requisitos_seleccionado = []
        self.botones_deshabilitados = []

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)

    def getAsignaturaSeleccionada(self):
        return self.codigoAsignaturaSeleccionada

    def setDatosVista(self, ano, semestre, plan, asignaturas, datosPeriodoActual, datosHistoricos, datosPeriodoAnterior):
        self.ano = ano
        self.semestre = semestre
        self.plan = plan
        self.asignaturas = asignaturas
        self.datosPeriodoActual = datosPeriodoActual
        self.datosHistoricos = datosHistoricos
        self.datosPeriodoAnterior = datosPeriodoAnterior
        self.resultados = {}
        self.inicializarVista()
        
    def agregarResultado(self, codigoAsignatura, resultado):
        if codigoAsignatura in self.resultados:
            self.mostrarAlerta("Advertencia", "Volver a estimar la asignatura elimina los resultados obtenidos en alguna estimación anterior.")
            self.resultados[codigoAsignatura] = resultado
        self.resultados[codigoAsignatura] = resultado
    
    def inicializarVista(self):
        self.setTitulo()
        self.table_prerrequisitos.setColumnWidth(0, 70)
        self.table_prerrequisitos.setColumnWidth(1, 70)
        self.table_prerrequisitos.setColumnWidth(2, 300)
        self.table_prerrequisitos.setColumnWidth(3, 220)
        self.table_prerrequisitos.setColumnWidth(4, 200)
        self.table_prerrequisitos.setColumnWidth(5, 220)
        self.table_prerrequisitos.setColumnWidth(6, 200)
        
        self.agregarBotones()
        self.button_guardar.setVisible(False)
        self.button_editar_pa.setVisible(False)

        self.seleccionado = self.button_invisible
        self.button_invisible.setVisible(False)

    def setTitulo(self):
        nombre = self.plan.getNombre()
        version = self.plan.getVersion()
        periodo = str(self.ano) + "-" + str(self.semestre)
        titulo = nombre + " " + version + ".\n(" + periodo + ")"
        self.label_nombre_carrera.setText(titulo)

    def ajustarNombreAsignatura(self, nombre):
        largo = len(nombre.split())
        if(largo > 4):
            lista = nombre.split()
            lista.insert(2, "\n")
            lista.insert(4, "\n")
            aux = ""
            for i in range(0,len(lista)):
                aux += lista[i]
                if(i != len(lista)-1 and i != 2 and i != 4):
                    aux += " "
            return aux

        elif(largo > 2):
            lista = nombre.split()
            lista.insert(2, "\n")
            aux = ""
            for i in range(0,len(lista)):
                aux += lista[i]
                if(i != len(lista)-1 and i != 2):
                    aux += " "
            return aux

        return nombre

    def agregarBotones(self):
        nivelesPlan = self.plan.getDuracion()
        botonReferencial = self.button_volver
        niveles = self.plan.getAsignaturas()
        fila = 1
        columna = 0
        for nivel in niveles:
            asignaturas = niveles[nivel]
            for codigoAsignatura in asignaturas:
                nombre = self.asignaturas[codigoAsignatura].getNombre()
                nombreAux = nombre
                nombre = self.ajustarNombreAsignatura(nombre)
                boton = QtWidgets.QPushButton()
                boton.setObjectName(str(codigoAsignatura))
                self.Malla.addWidget(boton, fila, columna)
                boton.setText(str(codigoAsignatura)+"\n"+nombre)
                if self.perteneceMBI(codigoAsignatura):
                    boton.setEnabled(False)
                    boton.setStyleSheet("background-color: #c1c1c0")
                    self.botones_deshabilitados.append(boton)
                else:
                    boton.clicked.connect(partial(self.mostrarDatosAsignatura, codigoAsignatura, boton))
                    self.setTabOrder(botonReferencial,boton)
                    botonReferencial = boton
                # Se agrega el boton al diccionario de botones de asignaturas de la vista
                if nivel not in self.botones:
                    self.botones[nivel] = []
                self.botones[nivel].append(boton)
                
                fila += 1
            columna += 1
            fila = 1
        self.setTabOrder(boton, self.button_editar_pa)
        for x in range(0, nivelesPlan):
            self.label = QtWidgets.QLabel()
            self.Malla.addWidget(self.label, 0, x)
            self.label.setText("Nivel "+str(x+1))
            self.label.setAlignment(QtCore.Qt.AlignCenter)

    def perteneceMBI(self, codigo):
        if codigo == None:
            return False
        codigosMBI = [13300, 13303, 13305, 13307]
        if codigo < 13000:
            return True
        if codigo in codigosMBI:
            return True
        return False

    
    def mostrarDatosAsignatura(self, codigoAsignatura, boton):
        self.seleccionado.setStyleSheet("")
        self.seleccionado = boton
        self.seleccionado.setStyleSheet(".QPushButton {\n"
                                "    color: white;\n"
                                "    background: #FF7A00;\n"
                                "}")
        self.button_editar_pa.setVisible(True)
        if(codigoAsignatura == self.codigoAsignaturaSeleccionada):
            return
        if codigoAsignatura in self.resultados:
            resultado = self.resultados[codigoAsignatura]
            self.value_ps_tai.setText(str(resultado["estimadosTeoria"]))
            self.value_ps_lai.setText(str(resultado["estimadosLaboratorio"]))
            self.value_ps_tci.setText(str(resultado["coordinacionesTeoria"]))
            self.value_ps_lcpc.setText(str(resultado["coordinacionesLaboratorio"]))
            self.label_observaciones.setText(resultado["observaciones"])
        else:
            self.value_ps_tai.setText("--")
            self.value_ps_lai.setText("--")
            self.value_ps_tci.setText("--")
            self.value_ps_lcpc.setText("--")
            self.label_observaciones.setText("")
        asignatura = self.asignaturas[codigoAsignatura]
        self.resaltarRequisitos(asignatura)
        self.codigoAsignaturaSeleccionada = int(boton.objectName())
        self.label_nombre_codigo.setText(asignatura.getNombre() + " ("+str(codigoAsignatura)+")")

        
        #Datos historicos
        if codigoAsignatura in self.datosHistoricos:
            self.value_tath.setText(str(math.floor(self.datosHistoricos[codigoAsignatura]["tasaAprobacionTeoria"]*100)) + "%")
            self.value_talh.setText(str(math.floor(self.datosHistoricos[codigoAsignatura]["tasaAprobacionLaboratorio"]*100)) + "%")
            self.value_tddh.setText(str(math.floor(self.datosHistoricos[codigoAsignatura]["tasaDesinscripcion"]*100)) + "%")
        else:
            self.value_tath.setText("No existen datos")
            self.value_talh.setText("No existen datos")
            self.value_tddh.setText("No existen datos")
        #Datos periodo actual
        if codigoAsignatura in self.datosPeriodoActual:
            self.input_inscritosTeoria.setText(str(self.datosPeriodoActual[codigoAsignatura]["inscritosTeoria"]))
            self.input_inscritosLaboratorio.setText(str(self.datosPeriodoActual[codigoAsignatura]["inscritosLaboratorio"]))
        else:
            self.input_inscritosTeoria.setText("NA")
            self.input_inscritosLaboratorio.setText("NA")
        self.input_cuposTeoria.setText(str(asignatura.getCuposTeoria()))
        self.input_cuposLaboratorio.setText(str(asignatura.getCuposLaboratorio()))
        #Datos ultimo periodo
        if codigoAsignatura in self.datosPeriodoAnterior:
            self.value_tatup.setText(str(math.floor(self.datosPeriodoAnterior[codigoAsignatura]["tasaAprobacionTeoria"]*100))+"%")
            self.value_talup.setText(str(math.floor(self.datosPeriodoAnterior[codigoAsignatura]["tasaAprobacionLaboratorio"]*100)) + "%")
            self.value_tddup.setText(str(math.floor(self.datosPeriodoAnterior[codigoAsignatura]["tasaDesinscripcion"]*100)) + "%")
        else:
            self.value_tatup.setText("No existen datos")
            self.value_talup.setText("No existen datos")
            self.value_tddup.setText("No existen datos")
        #Requisitos
        self.table_prerrequisitos.setRowCount(0)
        requisitosNivel = asignatura.getAsignaturasRequisitos()
        cantidadRequisitos = asignatura.getCantidadRequisitos()
        fila = 0
        self.table_prerrequisitos.setRowCount(cantidadRequisitos)
        for nivel in requisitosNivel:
            for codigoRequisito in requisitosNivel[nivel]: 
                self.table_prerrequisitos.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(codigoRequisito)))
                self.table_prerrequisitos.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(nivel)))
                requisito = self.asignaturas[codigoRequisito]
                self.table_prerrequisitos.setItem(fila, 2, QtWidgets.QTableWidgetItem(requisito.getNombre()))
                if codigoRequisito in self.datosPeriodoActual:
                    self.table_prerrequisitos.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(self.datosPeriodoActual[codigoRequisito]["inscritosTeoria"])))
                    self.table_prerrequisitos.setItem(fila, 5, QtWidgets.QTableWidgetItem(str(self.datosPeriodoActual[codigoRequisito]["inscritosLaboratorio"])))
                if codigoRequisito in self.datosHistoricos:
                    self.table_prerrequisitos.setItem(fila, 4, QtWidgets.QTableWidgetItem(str(math.floor(self.datosHistoricos[codigoRequisito]["tasaAprobacionTeoria"]*100)) + "%"))
                    self.table_prerrequisitos.setItem(fila, 6, QtWidgets.QTableWidgetItem(str(math.floor(self.datosHistoricos[codigoRequisito]["tasaAprobacionLaboratorio"]*100)) + "%"))
                fila += 1

    def mostrarResultado(self, resultado):
        self.value_ps_tai.setText(str(resultado["estimadosTeoria"]))
        self.value_ps_lai.setText(str(resultado["estimadosLaboratorio"]))
        self.value_ps_tci.setText(str(resultado["coordinacionesTeoria"]))
        self.value_ps_lcpc.setText(str(resultado["coordinacionesLaboratorio"]))
        self.label_observaciones.setText(resultado["observaciones"])

    def getInscritosTeoria(self):
        return self.input_inscritosTeoria.text()
    
    def getCuposTeoria(self):
        return self.input_cuposTeoria.text()

    def getInscritosLaboratorio(self):
        return self.input_inscritosLaboratorio.text()

    def getCuposLaboratorio(self):
        return self.input_cuposLaboratorio.text()
    
    def getAsignaturaEdicion(self):
        return self.codigoAsignaturaEdicion

    def clickBotonEditar(self):
        self.button_editar_pa.setVisible(False)
        self.button_guardar.setVisible(True)
        self.codigoAsignaturaEdicion = self.codigoAsignaturaSeleccionada
        self.input_inscritosTeoria.setEnabled(True)
        self.input_cuposTeoria.setEnabled(True)
        self.input_inscritosLaboratorio.setEnabled(True)
        self.input_cuposLaboratorio.setEnabled(True)

    def alternarBotones(self):
        self.button_guardar.setVisible(False)
        self.button_editar_pa.setVisible(True)
        self.input_inscritosTeoria.setEnabled(False)
        self.input_cuposTeoria.setEnabled(False)
        self.input_inscritosLaboratorio.setEnabled(False)
        self.input_cuposLaboratorio.setEnabled(False)
        

    def resaltarRequisitos(self, asignatura):
        # Se quita el resalte anteriormente dado a los botones
        for boton in self.requisitos_seleccionado:
            if boton != self.seleccionado:
                boton.setStyleSheet("")
            if boton in self.botones_deshabilitados:
                boton.setStyleSheet("background-color: #c1c1c0")
        self.requisitos_seleccionado = []
        # Se resaltan los botones requisitos
        botones = self.botones
        requisitos_por_nivel = asignatura.getAsignaturasRequisitos()
        for nivel in requisitos_por_nivel:
            for boton in botones[nivel]:
                codigo = int(boton.objectName())
                if codigo in requisitos_por_nivel[nivel]:
                    self.requisitos_seleccionado.append(boton)
                    if boton not in self.botones_deshabilitados:
                        boton.setStyleSheet(".QPushButton {\n"
                                    "    color: white;\n"
                                    "    background: #083C87;\n"
                                    "}")
                    else:
                        boton.setStyleSheet(".QPushButton {\n"
                                    "    background: #083C87;\n"
                                    "}")