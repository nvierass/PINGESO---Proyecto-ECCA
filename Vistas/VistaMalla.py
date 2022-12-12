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
        self.codigoAsignaturaSeleccionada = None
        self.resultados = {}

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
                self.boton = QtWidgets.QPushButton()
                self.boton.setObjectName(str(codigoAsignatura))
                self.Malla.addWidget(self.boton, fila, columna)
                self.boton.setText(str(codigoAsignatura)+"\n"+nombre)
                if self.perteneceMBI(codigoAsignatura):
                    self.boton.setEnabled(False)
                    self.boton.setStyleSheet("background-color: #c1c1c0")
                else:
                    self.boton.clicked.connect(partial(self.mostrarDatosAsignatura, codigoAsignatura, self.boton))
                    self.setTabOrder(botonReferencial,self.boton)
                    botonReferencial = self.boton
                fila += 1
            columna += 1
            fila = 1
        self.setTabOrder(self.boton, self.button_editar_pa_tai)
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
        self.seleccionado.setStyleSheet(".QPushButton {background: #FF7A00}")
        self.codigoAsignaturaSeleccionada = int(boton.objectName())
        self.label_nombre_codigo.setText(asignatura.getNombre() + " ("+str(codigoAsignatura)+")")

        self.value_ps_tce.setText(str(asignatura.getCuposTeoria()))
        self.value_ps_lce.setText(str(asignatura.getCuposLaboratorio()))
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
            self.value_pa_tai.setText(str(self.datosPeriodoActual[codigoAsignatura]["inscritosTeoria"]))
            self.value_pa_lai.setText(str(self.datosPeriodoActual[codigoAsignatura]["inscritosLaboratorio"]))
        else:
            self.value_pa_tai.setText("No existen datos")
            self.value_pa_lai.setText("No existen datos")
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