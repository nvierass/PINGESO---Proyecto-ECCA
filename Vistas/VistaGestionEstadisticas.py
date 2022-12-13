import os
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAbstractSpinBox, QGridLayout
from functools import partial

class VistaGestionEstadisticas(QMainWindow):
    
    def __init__(self, controladorGestionEstadisticas):
        super(VistaGestionEstadisticas, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/vistaGestionEstadisticas.ui"), self)

        self.controladorGestionEstadisticas = controladorGestionEstadisticas
        self.comboBoxAsignaturas.currentIndexChanged.connect(self.controladorGestionEstadisticas.actualizarTabla)
        self.button_home.clicked.connect(self.controladorGestionEstadisticas.volverContextoPrincipal)
        self.codigo = None
        self.cantidadEstadisticas = 0
               
    def getCodigoNombreSeleccionado(self):
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
        indexFila = 1
        for estadistica in estadisticasAsignatura:
            input_ano = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_ano.setObjectName("ano_"+str(indexFila))
            input_ano.setAlignment(QtCore.Qt.AlignCenter)
            input_ano.setText(str(estadistica.getAno()))
            input_ano.setEnabled(False)
            self.grid_estadisticas.addWidget(input_ano, indexFila, 0)

            input_semestre = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_semestre.setObjectName("semestre_"+str(indexFila))
            input_semestre.setAlignment(QtCore.Qt.AlignCenter)
            input_semestre.setText(str(estadistica.getSemestre()))
            input_semestre.setEnabled(False)
            self.grid_estadisticas.addWidget(input_semestre, indexFila, 1)

            input_inscritosTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_inscritosTeoria.setObjectName("inscritosTeoria_"+str(indexFila))
            input_inscritosTeoria.setAlignment(QtCore.Qt.AlignCenter)
            input_inscritosTeoria.setText(str(estadistica.getInscritosTeoria()))
            input_inscritosTeoria.setEnabled(False)
            self.grid_estadisticas.addWidget(input_inscritosTeoria, indexFila, 2)

            input_aprobadosTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_aprobadosTeoria.setObjectName("aprobadosTeoria_"+str(indexFila))
            input_aprobadosTeoria.setAlignment(QtCore.Qt.AlignCenter)
            input_aprobadosTeoria.setText(str(estadistica.getAprobadosTeoria()))
            input_aprobadosTeoria.setEnabled(False)
            self.grid_estadisticas.addWidget(input_aprobadosTeoria, indexFila, 3)

            input_reprobadosTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_reprobadosTeoria.setObjectName("reprobadosTeoria_"+str(indexFila))
            input_reprobadosTeoria.setAlignment(QtCore.Qt.AlignCenter)
            input_reprobadosTeoria.setText(str(estadistica.getReprobadosTeoria()))
            input_reprobadosTeoria.setEnabled(False)
            self.grid_estadisticas.addWidget(input_reprobadosTeoria, indexFila, 4)

            input_inscritosLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_inscritosLaboratorio.setObjectName("inscritosLaboratorio_"+str(indexFila))
            input_inscritosLaboratorio.setAlignment(QtCore.Qt.AlignCenter)
            input_inscritosLaboratorio.setText(str(estadistica.getInscritosLaboratorio()))
            input_inscritosLaboratorio.setEnabled(False)
            self.grid_estadisticas.addWidget(input_inscritosLaboratorio, indexFila, 5)

            input_aprobadosLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_aprobadosLaboratorio.setObjectName("aprobadosLaboratorio_"+str(indexFila))
            input_aprobadosLaboratorio.setAlignment(QtCore.Qt.AlignCenter)
            input_aprobadosLaboratorio.setText(str(estadistica.getAprobadosLaboratorio()))
            input_aprobadosLaboratorio.setEnabled(False)
            self.grid_estadisticas.addWidget(input_aprobadosLaboratorio, indexFila, 6)
            
            input_reprobadosLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_reprobadosLaboratorio.setObjectName("reprobadosLaboratorio_"+str(indexFila))
            input_reprobadosLaboratorio.setAlignment(QtCore.Qt.AlignCenter)
            input_reprobadosLaboratorio.setText(str(estadistica.getReprobadosLaboratorio()))
            input_reprobadosLaboratorio.setEnabled(False)
            self.grid_estadisticas.addWidget(input_reprobadosLaboratorio, indexFila, 7)

            input_tasaAprobacionTeoria= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_tasaAprobacionTeoria.setObjectName("tasaAprobacionTeoria_"+str(indexFila))
            input_tasaAprobacionTeoria.setAlignment(QtCore.Qt.AlignCenter)
            input_tasaAprobacionTeoria.setText(str(estadistica.getTasaAprobacionTeoria()))
            input_tasaAprobacionTeoria.setEnabled(False)
            self.grid_estadisticas.addWidget(input_tasaAprobacionTeoria, indexFila, 8)

            input_tasaAprobacionLaboratorio= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_tasaAprobacionLaboratorio.setObjectName("tasaAprobacionLaboratorio_"+str(indexFila))
            input_tasaAprobacionLaboratorio.setAlignment(QtCore.Qt.AlignCenter)
            input_tasaAprobacionLaboratorio.setText(str(estadistica.getTasaAprobacionLaboratorio()))
            input_tasaAprobacionLaboratorio.setEnabled(False)
            self.grid_estadisticas.addWidget(input_tasaAprobacionLaboratorio, indexFila, 9)

            input_tasaDesinscripcion= QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            input_tasaDesinscripcion.setObjectName("tasaDesinscripcion_"+str(indexFila))
            input_tasaDesinscripcion.setAlignment(QtCore.Qt.AlignCenter)
            input_tasaDesinscripcion.setText(str(estadistica.getTasaDesinscripcion()))
            input_tasaDesinscripcion.setEnabled(False)
            self.grid_estadisticas.addWidget(input_tasaDesinscripcion, indexFila, 10)

            button_editar = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            button_editar.setMinimumSize(QtCore.QSize(0, 20))
            button_editar.setAccessibleName("button_editar_"+str(indexFila))
            button_editar.setText("Editar")
            #button_editar.clicked.connect(partial(self.botonEditarClicked, self.pushButton))
            self.grid_estadisticas.addWidget(button_editar, indexFila, 11)

            button_eliminar = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            button_eliminar.setMinimumSize(QtCore.QSize(0, 20))
            button_eliminar.setAccessibleName("button_eliminar_"+str(indexFila))
            button_eliminar.setText("Eliminar")
            button_eliminar.clicked.connect(partial(self.controladorGestionEstadisticas.botonEliminarClicked, indexFila - 1))
            self.grid_estadisticas.addWidget(button_eliminar, indexFila, 12)
            

            indexFila += 1
        self.cantidadEstadisticas = len(estadisticasAsignatura)

    def limpiarGrid(self):
        """Elimina las últimas filas del grid hasta que la CantidadActual y CantidadNueva son iguales
        Parameters
        """
        grid = self.grid_estadisticas
        cantidadActual = self.cantidadEstadisticas
        cantidadNueva = 0
        if cantidadActual == 0:
            print("No hay botones")
            return 0
        while cantidadNueva < cantidadActual:
            self.eliminarFila(cantidadActual, grid)
            cantidadActual -= 1
        self.cantidadEstadisticas = cantidadActual
        return 1

    def eliminarFila(self, fila, grid):
        """Elimina la fila entregada del grid de la vista
        Parameters
        ----------
        fila: int
            La fila a eliminar del grid
        
        grid: QGridLayout
            El grid del cual se va a eliminar la fila
        """
        for columna in range(0,13):
            item = grid.itemAtPosition(fila, columna)
            if item != None :
                widget = item.widget()
                if widget != None:
                    grid.removeWidget(widget)
                    widget.deleteLater()
        print("Fila eliminada")
        return 1