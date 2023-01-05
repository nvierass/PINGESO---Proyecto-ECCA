import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from Vistas.resources.recursos import *

from DatabaseDriver.DatabaseContext import DatabaseContext

from Controladores.ControladorPrincipal import ControladorPrincipal

if __name__ == '__main__':

    app = QApplication(sys.argv)
    GUI = QtWidgets.QStackedWidget()
    GUI.setWindowTitle("ECCA - Departamento de Ingeniería Informática")
    GUI.setWindowIcon(QtGui.QIcon('./Vistas/resources/assets/Logo-DIINF-2022.png'))
    GUI.setMinimumSize(1536,864)
    databaseContext = DatabaseContext()
    controladorPrincipal = ControladorPrincipal(GUI, databaseContext)

    try:
        sys.exit(app.exec_())
    except:
        databaseContext.disconnect()
        print("Exiting")
    
   

