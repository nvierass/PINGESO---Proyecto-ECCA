import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem

class VistaRegistroAsignatura(QMainWindow):

    def __init__(self, controladorRegistroPlan):
        super(VistaRegistroAsignatura, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/layoutVistaRegistroAsignatura.ui"), self)

        self.controladorRegistroPlan = controladorRegistroPlan
        self.button_volver.clicked.connect(self.controladorRegistroPlan.mostrarVistaRegistroPlan)
        self.button_guardar.clicked.connect(self.controladorRegistroPlan.registrarAsignatura)
    
        self.button_quitar_requisito.clicked.connect(self.quitarRequisito)
        self.button_agregar_requisito.clicked.connect(self.agregarRequisito)
        
        self.button_quitar_equivalente.clicked.connect(self.quitarEquivalente)
        self.button_agregar_equivalente.clicked.connect(self.agregarEquivalente)

    
    def montarVista(self, asignaturasRegistradas):
        self.table_prerrequisitos.setColumnWidth(1, 200)
        self.table_prerrequisitos.setColumnWidth(0, 60)
        self.poblarAsignaturasRegistradas(asignaturasRegistradas)

    def quitarFila(self, tabla, fila):
        if tabla.rowCount() > 0:
            tabla.removeRow(fila)

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)

    def poblarAsignaturasRegistradas(self, asignaturas):
        fila = 0
        self.table_registradas.setRowCount(len(asignaturas))
        for codigo in asignaturas:
            asignatura = asignaturas[codigo]
            self.table_registradas.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(codigo)))
            self.table_registradas.setItem(fila, 1, QtWidgets.QTableWidgetItem(asignatura.getNombre()))
            fila += 1

    def getCodigoNuevaAsignatura(self):
        return self.input_codigo.text()

    def getNombreNuevaAsignatura(self):
        return self.input_nombre.text()
    
    def getTipoNuevaAsignatura(self):
        tipo = 0
        if self.radio_teoria.isChecked():
            tipo = 1
        if self.radio_laboratorio.isChecked():
            tipo = 2
        if self.radio_teoriaLaboratorio.isChecked():
            tipo = 3
        if self.radio_topicoElectivo.isChecked():
            tipo = 4
        return tipo

    def getCodigosEquivalentes(self):
        tabla = self.table_analogas
        codigos = []
        total_filas = tabla.rowCount()
        for fila in range(0,total_filas):
            codigo = tabla.item(fila,0).text()
            codigos.append(codigo)
        return codigos

    def getCodigosRequisitos(self):
        tabla = self.table_prerrequisitos
        codigos = []
        total_filas = tabla.rowCount()
        for fila in range(0,total_filas):
            codigo = tabla.item(fila,0).text()
            codigos.append(codigo)
        return codigos
    
    def nivelesIngresados(self):
        tabla = self.table_prerrequisitos
        total_filas = tabla.rowCount()
        for fila in range(0,total_filas):
            nivel = tabla.item(fila,2).text()
            if not nivel.isnumeric():
                return False
        return True

    def getCodigosNivelRequisitos(self):
        tabla = self.table_prerrequisitos
        codigosNivel = {}
        total_filas = tabla.rowCount()
        for fila in range(0,total_filas):
            stringNivel = tabla.item(fila,2).text()
            if stringNivel.isnumeric():
                nivel = tabla.item(fila,2).text()
                codigo = tabla.item(fila,0).text()
                if nivel in codigosNivel:
                    codigosNivel[nivel].append(codigo)
                else:
                    codigosNivel[nivel] = [codigo]
        return codigosNivel

    def agregarFila(self, tabla, codigo, asignatura):
        fila = tabla.rowCount()
        tabla.insertRow(fila)
        tabla.setItem(fila,0, QTableWidgetItem(codigo))
        tabla.setItem(fila,1, QTableWidgetItem(asignatura))
        if tabla == self.table_prerrequisitos:
            tabla.setItem(fila,2, QTableWidgetItem("Doble click para ingresar nivel."))

    def agregarRequisito(self):
        requisitosAgregados = self.getCodigosRequisitos()
        seleccionados = self.table_registradas.selectedItems()
        if seleccionados != []:
            lista_filas = map(lambda item:item.row(), seleccionados)
            lista_filas = list(set(lista_filas))
            
            for fila in lista_filas:
                codigo =  self.table_registradas.item(fila,0).text()
                nombreAsignatura = self.table_registradas.item(fila,1).text()
                if not codigo in requisitosAgregados:
                    self.agregarFila(self.table_prerrequisitos, codigo, nombreAsignatura)
                else:
                    self.mostrarAlerta("Advertencia", "Una o mas asignaturas seleccionadas ya han sido incluidas como requisitos.")
                    return
            #Se ordenan automaticamente en base al nivel
            self.table_prerrequisitos.sortItems(2)
        
        else:
            QMessageBox.information(self, "Atención", "Seleccione las asignaturas que desea agregar como requisitos")
    
    def agregarEquivalente(self):
        equivalentesAgregadas = self.getCodigosEquivalentes()
        seleccionados = self.table_registradas.selectedItems()
        if seleccionados != []:
            lista_filas = map(lambda item:item.row(), seleccionados)
            lista_filas = list(set(lista_filas))
            for fila in lista_filas:
                codigo =  self.table_registradas.item(fila,0).text()
                nombreAsignatura = self.table_registradas.item(fila,1).text()
                if codigo in equivalentesAgregadas:
                    print(codigo, "Ya existe")
                    self.mostrarAlerta("Error", "La asignatura ya ha sido agregada como equivalente.")
                    return
                else:
                    print(codigo, "No existe, se agrega",equivalentesAgregadas)
                    self.agregarFila(self.table_analogas, codigo, nombreAsignatura)
            self.table_analogas.sortItems(2)
        else:
            QMessageBox.information(self, "Atención", "Seleccione las asignaturas que desea agregar como análogas")

    def quitarRequisito(self):
        lista_seleccionados = self.table_prerrequisitos.selectedItems()
        pasos = 0
        while lista_seleccionados!=[]:
            num_fila = lista_seleccionados[0].row()
            self.quitarFila(self.table_prerrequisitos, num_fila)
            lista_seleccionados = self.table_prerrequisitos.selectedItems()
            pasos = pasos + 1
            
        if pasos == 0:
            QMessageBox.information(self, "Atención", "Seleccione las asignaturas que desea quitar de la lista de prerrequisitos")

    def quitarEquivalente(self):
        lista_seleccionados = self.table_analogas.selectedItems()
        pasos = 0
        while lista_seleccionados!=[]:
            num_fila = lista_seleccionados[0].row()
            self.quitarFila(self.table_analogas, num_fila)
            lista_seleccionados = self.table_analogas.selectedItems()
            pasos = pasos + 1
        if pasos == 0:
            QMessageBox.information(self, "Atención", "Seleccione las asignaturas que desea quitar de la lista de análogas")

