import os
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAbstractSpinBox
from functools import partial

class VistaCupos(QMainWindow):
    
    def __init__(self, controladorEstimacion):
        super(VistaCupos, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/layoutVistaCupos.ui"), self)

        self.controladorEstimacion = controladorEstimacion
        self.label.setText("Cupos de coordinaciones")
        self.button_home.clicked.connect(controladorEstimacion.volverContextoPrincipal)
        self.button_estimar.clicked.connect(controladorEstimacion.realizarEstimacion)

    def montarVista(self, asignaturas):
        fila = 1
        for codigoAsignatura in asignaturas:
            asignatura = asignaturas[codigoAsignatura]
            if not self.controladorEstimacion.perteneceMBI(codigoAsignatura):
                self.agregarFila(fila, asignatura.getNombre(), asignatura.getCodigo())
                fila = fila + 1
        self.filas = fila

    def actualizarCuposAsignaturas(self, asignaturas):
        filasTotales = self.filas
        indexFila = 1
        while indexFila < filasTotales:
            cuposTeoria = self.gridLayout.itemAtPosition(indexFila, 2).widget().value()
            cuposLaboratorio = self.gridLayout.itemAtPosition(indexFila, 3).widget().value()
            codigoAsignatura = int(self.gridLayout.itemAtPosition(indexFila, 0).widget().text())
            asignaturas[codigoAsignatura].setCuposTeoria(cuposTeoria)
            asignaturas[codigoAsignatura].setCuposLaboratorio(cuposLaboratorio)
            indexFila += 1
        return asignaturas

    def agregarFila(self, indexFila, nombreAsignatura, codigoAsignatura):
        self.label_codigo = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_codigo.setObjectName("label_"+str(indexFila)+"_1")
        self.label_codigo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_codigo.setText(str(codigoAsignatura))
        self.gridLayout.addWidget(self.label_codigo, indexFila, 0)
        
        self.label_asignatura = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_asignatura.setObjectName("label_"+str(indexFila)+"_0")
        self.label_asignatura.setAlignment(QtCore.Qt.AlignCenter)
        self.label_asignatura.setText(nombreAsignatura)
        self.gridLayout.addWidget(self.label_asignatura, indexFila, 1)
        
        self.spinBox1 = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.spinBox1.setMaximum(1000)
        self.spinBox1.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox1.setProperty("value", 30)
        self.spinBox1.setObjectName("spinBox_"+str(indexFila)+"_0")
        self.spinBox1.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox1.setReadOnly(True)
        self.gridLayout.addWidget(self.spinBox1, indexFila, 2)
        
        self.spinBox2 = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.spinBox2.setMaximum(1000)
        self.spinBox2.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox2.setProperty("value", 10)
        self.spinBox2.setObjectName("spinBox_"+str(indexFila)+"_1")
        self.spinBox2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox2.setReadOnly(True)
        self.gridLayout.addWidget(self.spinBox2, indexFila, 3)
        
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 20))
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton.setAccessibleName("button_editar_"+str(indexFila))
        self.pushButton.setAccessibleDescription("0")
        self.pushButton.setText("Editar")
        self.pushButton.setStyleSheet('QPushButton {color: black}')
        self.pushButton.clicked.connect(partial(self.botonEditarClicked, self.pushButton))
        self.gridLayout.addWidget(self.pushButton, indexFila, 4)
    
    def botonEditarClicked(self, idBoton):
        nombre = idBoton.accessibleName()
        estado = int(idBoton.accessibleDescription())

        numero_fila = int(nombre.replace("button_editar_", ""))
        spinbox_1 = self.gridLayout.itemAtPosition(numero_fila, 2).widget()
        spinbox_2 = self.gridLayout.itemAtPosition(numero_fila, 3).widget()
        
        label_nombre = self.gridLayout.itemAtPosition(numero_fila, 0).widget()
        label_codigo = self.gridLayout.itemAtPosition(numero_fila, 1).widget()

        if estado == 0:
            label_nombre.setStyleSheet("color: white;"
                                       "border-radius: 10px;"
                                       "background-color: #083C87;")
            label_codigo.setStyleSheet("color: white;"
                                       "border-radius: 10px;"
                                       "background-color: #083C87;")
            idBoton.setStyleSheet(".QPushButton {\n"
                                "    background: #FF7A00;\n"
                                "    border-radius: 10px;\n"
                                "}\n"
                                "\n"
                                ".QPushButton:hover {\n"
                                "    background: #083C87;\n"
                                "}\n"
                                "\n"
                                ".QPushButton:pressed {\n"
                                "    background: #E6E6E6;\n"
                                "}")
            idBoton.setText("Guardar")
            spinbox_1.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
            spinbox_1.setReadOnly(False)
            spinbox_2.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
            spinbox_2.setReadOnly(False)
            idBoton.setAccessibleDescription("1")

        elif estado == 1:
            label_nombre.setStyleSheet("")
            label_codigo.setStyleSheet("")
            idBoton.setStyleSheet("")
            idBoton.setText("Editar")
            idBoton.setStyleSheet('QPushButton {color: black}')
            spinbox_1.setButtonSymbols(QAbstractSpinBox.NoButtons)
            spinbox_1.setReadOnly(True)
            spinbox_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
            spinbox_2.setReadOnly(True)
            idBoton.setAccessibleDescription("0")


    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)

    