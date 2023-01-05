import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog

class VistaResultados(QMainWindow):

    def __init__(self, controladorEstimacion):
        super(VistaResultados, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/layoutVistaResultados.ui"), self)

        self.controladorEstimacion = controladorEstimacion
        self.label_titulo.setText("Resultados de la estimación")
        self.button_home.clicked.connect(self.controladorEstimacion.volverContextoPrincipal)
        self.button_exportar.clicked.connect(self.controladorEstimacion.exportarResultados)

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)

    def getPathResultados(self):
        option = QFileDialog.Options()
        fname = QFileDialog.getSaveFileName(self, "Exportar archivo", "Resultados Estimación", "Planilla Excel (*.xlsx);;Todos los archivos (*)", options=option)[0]
        return fname
            
    def montarVista(self, resultados):
        self.tableWidget.setColumnWidth(0, 50)  #Codigo
        self.tableWidget.setColumnWidth(1, 250) #Nombre asignatura
        self.tableWidget.setColumnWidth(2, 120) #Cant. alum. teo
        self.tableWidget.setColumnWidth(3, 120) #Cant. alum. lab
        self.tableWidget.setColumnWidth(4, 150) #Cant. coor. teo
        self.tableWidget.setColumnWidth(5, 150) #Cant. coor. teo
        self.tableWidget.setColumnWidth(6, 600)
        
        indexFila = 0
        self.tableWidget.setRowCount(len(resultados))
        for codigoAsignatura in resultados:
            if not self.controladorEstimacion.perteneceMBI(codigoAsignatura):
                resultado = resultados[codigoAsignatura]
                self.tableWidget.setItem(indexFila, 0, QtWidgets.QTableWidgetItem(str(resultado["codigo"])))
                self.tableWidget.setItem(indexFila, 1, QtWidgets.QTableWidgetItem(resultado["nombre"]))
                self.tableWidget.setItem(indexFila, 2, QtWidgets.QTableWidgetItem(str(resultado["estimadosTeoria"])))
                self.tableWidget.setItem(indexFila, 3, QtWidgets.QTableWidgetItem(str(resultado["estimadosLaboratorio"])))
                self.tableWidget.setItem(indexFila, 4, QtWidgets.QTableWidgetItem(str(resultado["coordinacionesTeoria"])))
                self.tableWidget.setItem(indexFila, 5, QtWidgets.QTableWidgetItem(str(resultado["coordinacionesLaboratorio"])))
                self.tableWidget.setItem(indexFila, 6, QtWidgets.QTableWidgetItem(resultado["observaciones"]))
                indexFila += 1
        
    def setTitulo(self, titulo):
        self.titulo = titulo
        self.label_titulo.setText(titulo)

    def getTitulo(self, titulo):
        return self.titulo