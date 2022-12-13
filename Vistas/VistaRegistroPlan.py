import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem

class VistaRegistroPlan(QMainWindow):

    def __init__(self, controladorRegistroPlan):
        super(VistaRegistroPlan, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "resources/registrar_plan.ui"), self)

        self.controladorRegistroPlan = controladorRegistroPlan

        self.button_home.clicked.connect(self.controladorRegistroPlan.volverContextoPrincipal)
        self.button_registrar_asignatura.clicked.connect(self.controladorRegistroPlan.inicializarRegistroAsignatura)
        self.button_guardar.clicked.connect(self.controladorRegistroPlan.registrarPlan)

        self.button_agregar.clicked.connect(self.agregarAsignatura)
        self.button_quitar.clicked.connect(self.quitarAsignatura)

    def mostrarAlerta(self,titulo,texto):
        QMessageBox.information(self, titulo, texto)

    def getNombre(self):
        return self.input_nombre.text()

    def getVersion(self):
        return self.input_version.text()

    def getDuracion(self):
        return self.input_duracion.text()

    def montarVista(self, asignaturasRegistradas):
        self.table_registradas.setColumnWidth(0, 60)
        self.table_registradas.setColumnWidth(1, 200)
        self.poblarAsignaturasRegistradas(asignaturasRegistradas)
    
    def poblarAsignaturasRegistradas(self, asignaturas):
        fila = 0
        self.table_registradas.setRowCount(len(asignaturas))
        for codigo in asignaturas:
            asignatura = asignaturas[codigo]
            self.table_registradas.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(codigo)))
            self.table_registradas.setItem(fila, 1, QtWidgets.QTableWidgetItem(asignatura.getNombre()))
            fila += 1

    def quitarFila(self, tabla, fila):
        if tabla.rowCount() > 0:
            tabla.removeRow(fila)

    def nivelesIngresados(self):
        tabla = self.table_nuevo_plan
        total_filas = tabla.rowCount()
        for fila in range(0,total_filas):
            nivel = tabla.item(fila,2).text()
            if not nivel.isnumeric():
                return False
        return True

    def agregarFila(self, codigo, asignatura):
        tabla = self.table_nuevo_plan
        fila = tabla.rowCount()
        tabla.insertRow(fila)
        tabla.setItem(fila,0, QTableWidgetItem(codigo))
        tabla.setItem(fila,1, QTableWidgetItem(asignatura))
        tabla.setItem(fila,2, QTableWidgetItem("Doble click para ingresar nivel."))

    def agregarAsignatura(self):
        codigosNuevoPlan = self.getCodigosNuevoPlan()
        seleccionados = self.table_registradas.selectedItems()
        if seleccionados != []:
            lista_filas = map(lambda item:item.row(), seleccionados)
            lista_filas = list(set(lista_filas))
            
            for fila in lista_filas:
                codigo =  self.table_registradas.item(fila,0).text()
                nombreAsignatura = self.table_registradas.item(fila,1).text()
                if not codigo in codigosNuevoPlan:
                    self.agregarFila(codigo, nombreAsignatura)
                else:
                    self.mostrarAlerta("Advertencia", "Una o mas asignaturas seleccionadas ya han sido incluidas al nuevo plan de estudios.")
                    return
            #Se ordenan automaticamente en base al nivel
            self.table_nuevo_plan.sortItems(2)
        
        else:
            QMessageBox.information(self, "Atención", "Seleccione las asignaturas que desea agregar al nuevo plan de estudios.")
    
    def quitarAsignatura(self):
        lista_seleccionados = self.table_nuevo_plan.selectedItems()
        pasos = 0
        while lista_seleccionados!=[]:
            num_fila = lista_seleccionados[0].row()
            self.quitarFila(self.table_nuevo_plan, num_fila)
            lista_seleccionados = self.table_nuevo_plan.selectedItems()
            pasos = pasos + 1

        if pasos == 0:
            QMessageBox.information(self, "Atención", "Seleccione las asignaturas que desea quitar del nuevo plan de estudios.")

    def getCodigosNuevoPlan(self):
        tabla = self.table_nuevo_plan
        codigos = []
        total_filas = tabla.rowCount()
        for fila in range(0,total_filas):
            codigo = tabla.item(fila,0).text()
            codigos.append(codigo)
        return codigos

    def getCodigosNivelNuevoPlan(self):
        tabla = self.table_nuevo_plan
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