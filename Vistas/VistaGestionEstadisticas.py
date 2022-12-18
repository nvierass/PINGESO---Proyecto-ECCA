import os
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAbstractSpinBox, QGridLayout
from functools import partial

class VistaGestionEstadisticas(QMainWindow):
    
    def __init__(self, controladorGestionEstadisticas):
        super(VistaGestionEstadisticas, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/layoutVistaGestionEstadisticas.ui"), self)
        
        self.controladorGestionEstadisticas = controladorGestionEstadisticas
        self.comboBoxAsignaturas.currentIndexChanged.connect(self.controladorGestionEstadisticas.actualizarTabla)
        self.button_home.clicked.connect(self.controladorGestionEstadisticas.volverContextoPrincipal)
        self.boton_agregar_estadistica.clicked.connect(self.controladorGestionEstadisticas.iniciarIngreso)
        self.codigo = None
        self.cantidadEstadisticas = 0
        self.referenciasFilas = {}
        self.referenciaRegistro = []
        self.editandoEstadistica = False
        self.codigoAsignaturaEdicion = None
        self.boton_agregar_estadistica.setVisible(False)

    def getCodigoAsignaturaEdicion(self):
        return self.codigoAsignaturaEdicion  

    def getCodigoNombreSeleccionado(self):
        if self.comboBoxAsignaturas.currentIndex() == 0:
            return None, None
        textoSeleccionado = self.comboBoxAsignaturas.currentText()
        [codigo, nombre] = textoSeleccionado.split(" - ")
        return int(codigo), nombre

    def setCodigo(self, codigo):
        self.codigo = codigo
        self.labelCodigo.setText(str(codigo))

    def getCodigo(self):
        return self.codigo

    def setNombre(self, nombre):
        self.labelNombre.setText(nombre)

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)

    def agregarAsignatura(self, codigo, nombre):
        texto = str(codigo) + " - " + nombre
        self.comboBoxAsignaturas.addItem(texto)

    def montarVista(self, asignaturas):
        self.asignaturasRegistradas = asignaturas
        for codigoAsignatura in asignaturas:
            asignatura = asignaturas[codigoAsignatura]
            self.agregarAsignatura(codigoAsignatura, asignatura.getNombre())

    def agregarEstadisticas(self, estadisticasAsignatura):
        self.boton_agregar_estadistica.setVisible(True)
        self.cantidadEstadisticas = len(estadisticasAsignatura)
        self.referenciasFilas = {}
        indexFila = 1
        for estadistica in estadisticasAsignatura:
            referencia = []

            input_ano = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_ano.setObjectName("ano_"+str(indexFila))
            input_ano.setAlignment(QtCore.Qt.AlignCenter)
            input_ano.setText(str(estadistica.getAno()))
            input_ano.setEnabled(False)
            self.grid_estadisticas.addWidget(input_ano, indexFila, 0)
            referencia.append(input_ano)

            input_semestre = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_semestre.setObjectName("semestre_"+str(indexFila))
            input_semestre.setAlignment(QtCore.Qt.AlignCenter)
            input_semestre.setText(str(estadistica.getSemestre()))
            input_semestre.setEnabled(False)
            self.grid_estadisticas.addWidget(input_semestre, indexFila, 1)
            referencia.append(input_semestre)

            input_inscritosTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_inscritosTeoria.setObjectName("inscritosTeoria_"+str(indexFila))
            input_inscritosTeoria.setAlignment(QtCore.Qt.AlignCenter)
            input_inscritosTeoria.setText(str(estadistica.getInscritosTeoria()))
            input_inscritosTeoria.setEnabled(False)
            self.grid_estadisticas.addWidget(input_inscritosTeoria, indexFila, 2)
            referencia.append(input_inscritosTeoria)

            input_aprobadosTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_aprobadosTeoria.setObjectName("aprobadosTeoria_"+str(indexFila))
            input_aprobadosTeoria.setAlignment(QtCore.Qt.AlignCenter)
            input_aprobadosTeoria.setText(str(estadistica.getAprobadosTeoria()))
            input_aprobadosTeoria.setEnabled(False)
            self.grid_estadisticas.addWidget(input_aprobadosTeoria, indexFila, 3)
            referencia.append(input_aprobadosTeoria)

            input_reprobadosTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_reprobadosTeoria.setObjectName("reprobadosTeoria_"+str(indexFila))
            input_reprobadosTeoria.setAlignment(QtCore.Qt.AlignCenter)
            input_reprobadosTeoria.setText(str(estadistica.getReprobadosTeoria()))
            input_reprobadosTeoria.setEnabled(False)
            self.grid_estadisticas.addWidget(input_reprobadosTeoria, indexFila, 4)
            referencia.append(input_reprobadosTeoria)

            input_inscritosLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_inscritosLaboratorio.setObjectName("inscritosLaboratorio_"+str(indexFila))
            input_inscritosLaboratorio.setAlignment(QtCore.Qt.AlignCenter)
            input_inscritosLaboratorio.setText(str(estadistica.getInscritosLaboratorio()))
            input_inscritosLaboratorio.setEnabled(False)
            self.grid_estadisticas.addWidget(input_inscritosLaboratorio, indexFila, 5)
            referencia.append(input_inscritosLaboratorio)

            input_aprobadosLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_aprobadosLaboratorio.setObjectName("aprobadosLaboratorio_"+str(indexFila))
            input_aprobadosLaboratorio.setAlignment(QtCore.Qt.AlignCenter)
            input_aprobadosLaboratorio.setText(str(estadistica.getAprobadosLaboratorio()))
            input_aprobadosLaboratorio.setEnabled(False)
            self.grid_estadisticas.addWidget(input_aprobadosLaboratorio, indexFila, 6)
            referencia.append(input_aprobadosLaboratorio)

            input_reprobadosLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_reprobadosLaboratorio.setObjectName("reprobadosLaboratorio_"+str(indexFila))
            input_reprobadosLaboratorio.setAlignment(QtCore.Qt.AlignCenter)
            input_reprobadosLaboratorio.setText(str(estadistica.getReprobadosLaboratorio()))
            input_reprobadosLaboratorio.setEnabled(False)
            self.grid_estadisticas.addWidget(input_reprobadosLaboratorio, indexFila, 7)
            referencia.append(input_reprobadosLaboratorio)
            
            input_tasaAprobacionTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_tasaAprobacionTeoria.setObjectName("tasaAprobacionTeoria_"+str(indexFila))
            input_tasaAprobacionTeoria.setAlignment(QtCore.Qt.AlignCenter)
            input_tasaAprobacionTeoria.setText(str(estadistica.getTasaAprobacionTeoria()))
            input_tasaAprobacionTeoria.setEnabled(False)
            self.grid_estadisticas.addWidget(input_tasaAprobacionTeoria, indexFila, 8)
            referencia.append(input_tasaAprobacionTeoria)

            input_tasaAprobacionLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_tasaAprobacionLaboratorio.setObjectName("tasaAprobacionLaboratorio_"+str(indexFila))
            input_tasaAprobacionLaboratorio.setAlignment(QtCore.Qt.AlignCenter)
            input_tasaAprobacionLaboratorio.setText(str(estadistica.getTasaAprobacionLaboratorio()))
            input_tasaAprobacionLaboratorio.setEnabled(False)
            self.grid_estadisticas.addWidget(input_tasaAprobacionLaboratorio, indexFila, 9)
            referencia.append(input_tasaAprobacionLaboratorio)
            
            input_tasaDesinscripcion= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_tasaDesinscripcion.setObjectName("tasaDesinscripcion_"+str(indexFila))
            input_tasaDesinscripcion.setAlignment(QtCore.Qt.AlignCenter)
            input_tasaDesinscripcion.setText(str(estadistica.getTasaDesinscripcion()))
            input_tasaDesinscripcion.setEnabled(False)
            self.grid_estadisticas.addWidget(input_tasaDesinscripcion, indexFila, 10)
            referencia.append(input_tasaDesinscripcion)

            button_editar = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            button_editar.setMinimumSize(QtCore.QSize(0, 20))
            button_editar.setAccessibleName("button_editar_"+str(indexFila))
            button_editar.setText("Editar")
            button_editar.clicked.connect(partial(self.controladorGestionEstadisticas.botonEditarClicked, indexFila - 1))
            self.grid_estadisticas.addWidget(button_editar, indexFila, 11)
            referencia.append(button_editar)

            button_eliminar = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            button_eliminar.setMinimumSize(QtCore.QSize(0, 20))
            button_eliminar.setAccessibleName("button_eliminar_"+str(indexFila))
            button_eliminar.setText("Eliminar")
            button_eliminar.clicked.connect(partial(self.controladorGestionEstadisticas.botonEliminarClicked, indexFila - 1))
            self.grid_estadisticas.addWidget(button_eliminar, indexFila, 12)
            referencia.append(button_eliminar)

            button_guardar= QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            button_guardar.setMinimumSize(QtCore.QSize(0, 20))
            button_guardar.setAccessibleName("button_guardar_"+str(indexFila))
            button_guardar.setText("Guardar")
            button_guardar.setVisible(False)
            button_guardar.clicked.connect(partial(self.controladorGestionEstadisticas.botonGuardarClicked, indexFila - 1))
            referencia.append(button_guardar)

            button_cancelar = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            button_cancelar.setMinimumSize(QtCore.QSize(0, 20))
            button_cancelar.setAccessibleName("button_cancelar_"+str(indexFila))
            button_cancelar.setText("Cancelar")
            button_guardar.setVisible(False)
            button_cancelar.clicked.connect(partial(self.controladorGestionEstadisticas.botonCancelarClicked, indexFila - 1))
            referencia.append(button_cancelar)
            self.referenciasFilas[indexFila] = referencia
            indexFila += 1

    def confirmarEliminacion(self , codigo, nombre, ano, semestre):
        dialogo = QMessageBox()
        pregunta = "¿Confirma que desea eliminar las estadísticas correspondientes al periodo " + str(ano) + "-" +str(semestre) + " de la asignatura " + nombre +" (Código: " + (str(codigo)) + ")?"
        dialogo.setInformativeText(pregunta)
        dialogo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        respuesta = dialogo.exec()
        if respuesta == QMessageBox.Yes:
            return True
        return False 

    def limpiarGrid(self):
        grid = self.grid_estadisticas
        cantidadFilasActual = self.cantidadEstadisticas
        cantidadNueva = 0
        if cantidadFilasActual == 0:
            return 
        while cantidadFilasActual > 0:
            self.eliminarFila(cantidadFilasActual)
            cantidadFilasActual -= 1
        self.cantidadEstadisticas = 0

    def eliminarFila(self, fila):
        grid = self.grid_estadisticas
        for columna in range(0,13):
            item = grid.itemAtPosition(fila, columna)
            if item != None :
                widget = item.widget()
                if widget != None:
                    grid.removeWidget(widget)
                    widget.deleteLater()

    def habilitarEdicion(self, fila):
        self.comboBoxAsignaturas.setEnabled(False)
        self.editandoEstadistica = True
        self.codigoAsignaturaEdicion = self.codigo
        referenciaInputs = self.referenciasFilas[fila]
        for i in range(2,11):
            referenciaInputs[i].setEnabled(True)
        botonEditar = referenciaInputs[11]
        botonEliminar = referenciaInputs[12]
        botonGuardar = referenciaInputs[13]
        botonCancelar = referenciaInputs[14]

        botonEditar.setVisible(False)
        botonEditar.setVisible(False)
        botonGuardar.setVisible(True)
        botonCancelar.setVisible(True)

        self.grid_estadisticas.addWidget(botonGuardar, fila, 11)
        self.grid_estadisticas.addWidget(botonCancelar, fila, 12)

    def deshabilitarEdicion(self, fila):
        self.comboBoxAsignaturas.setEnabled(True)
        self.editandoEstadistica = False
        referenciaInputs = self.referenciasFilas[fila]
        for i in range(2,11):
            referenciaInputs[i].setEnabled(False)
        botonEditar = referenciaInputs[11]
        botonEliminar = referenciaInputs[12]
        botonGuardar = referenciaInputs[13]
        botonCancelar = referenciaInputs[14]

        botonEditar.setVisible(True)
        botonEditar.setVisible(True)
        botonGuardar.setVisible(False)
        botonCancelar.setVisible(False)

        self.grid_estadisticas.addWidget(botonEditar, fila, 11)
        self.grid_estadisticas.addWidget(botonEliminar, fila, 12)

    def edicionActiva(self):
        return self.editandoEstadistica

    def restaurarEstadistica(self, fila, estadistica):
        referenciaInputs = self.referenciasFilas[fila]
        referenciaInputs[0].setText(str(estadistica.getAno()))
        referenciaInputs[1].setText(str(estadistica.getSemestre()))
        referenciaInputs[2].setText(str(estadistica.getInscritosTeoria()))
        referenciaInputs[3].setText(str(estadistica.getAprobadosTeoria()))
        referenciaInputs[4].setText(str(estadistica.getReprobadosTeoria()))
        referenciaInputs[5].setText(str(estadistica.getInscritosLaboratorio()))
        referenciaInputs[6].setText(str(estadistica.getAprobadosLaboratorio()))
        referenciaInputs[7].setText(str(estadistica.getReprobadosLaboratorio()))
        referenciaInputs[8].setText(str(estadistica.getTasaAprobacionTeoria()))
        referenciaInputs[9].setText(str(estadistica.getTasaAprobacionLaboratorio()))
        referenciaInputs[10].setText(str(estadistica.getTasaDesinscripcion()))

    def obtenerEstadistica(self, fila):
        referenciaInputs = self.referenciasFilas[fila]
        datos = []
        for i in range(0,11):
            datos.append(referenciaInputs[i].text())
        return datos.copy()

    def obtenerEstadisticaRegistro(self):
        datos = []
        for i in range(0,11):
            datos.append(self.referenciaRegistro[i].text())
        return datos.copy()

    def agregarFilaIngreso(self):
        self.editandoEstadistica = True
        self.comboBoxAsignaturas.setEnabled(False)
        self.boton_agregar_estadistica.setVisible(False)

        referencias = []
        indexFila = self.cantidadEstadisticas + 1

        input_ano = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_ano, indexFila, 0)
        referencias.append(input_ano)

        input_semestre = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_semestre, indexFila, 1)
        referencias.append(input_semestre)

        input_inscritosTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_inscritosTeoria, indexFila, 2)
        referencias.append(input_inscritosTeoria)

        input_aprobadosTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_aprobadosTeoria, indexFila, 3)
        referencias.append(input_aprobadosTeoria)

        input_reprobadosTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_reprobadosTeoria, indexFila, 4)
        referencias.append(input_reprobadosTeoria)

        input_inscritosLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_inscritosLaboratorio, indexFila, 5)
        referencias.append(input_inscritosLaboratorio)

        input_aprobadosLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_aprobadosLaboratorio, indexFila, 6)
        referencias.append(input_aprobadosLaboratorio)

        input_reprobadosLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_reprobadosLaboratorio, indexFila, 7)
        referencias.append(input_reprobadosLaboratorio)

        input_tasaAprobacionTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_tasaAprobacionTeoria, indexFila, 8)
        referencias.append(input_tasaAprobacionTeoria)

        input_tasaAprobacionLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_tasaAprobacionLaboratorio, indexFila, 9)
        referencias.append(input_tasaAprobacionLaboratorio)

        input_tasaDesinscripcion= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.grid_estadisticas.addWidget(input_tasaDesinscripcion, indexFila, 10)
        referencias.append(input_tasaDesinscripcion)

        button_insertar = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        button_insertar.setMinimumSize(QtCore.QSize(0, 20))
        button_insertar.setAccessibleName("button_insertar"+str(indexFila))
        button_insertar.setText("Guardar")
        button_insertar.setVisible(True)
        button_insertar.clicked.connect(partial(self.controladorGestionEstadisticas.botonGuardarNuevaClicked))
        self.grid_estadisticas.addWidget(button_insertar, indexFila, 11)
        referencias.append(button_insertar)

        button_cancelar_ingreso = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        button_cancelar_ingreso.setMinimumSize(QtCore.QSize(0, 20))
        button_cancelar_ingreso.setAccessibleName("button_cancelar_"+str(indexFila))
        button_cancelar_ingreso.setText("Cancelar")
        button_cancelar_ingreso.setVisible(True)
        button_cancelar_ingreso.clicked.connect(partial(self.controladorGestionEstadisticas.botonCancelarIngresoClicked))
        self.grid_estadisticas.addWidget(button_cancelar_ingreso, indexFila, 12)
        referencias.append(button_cancelar_ingreso)

        self.referenciaRegistro = referencias.copy()


    def eliminarFilaRegistro(self):
        grid = self.grid_estadisticas
        for referencia in self.referenciaRegistro:
            self.grid_estadisticas.removeWidget(referencia)
            referencia.deleteLater()
