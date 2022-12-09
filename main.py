import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from Controladores.ControladorPrincipal import ControladorPrincipal

if __name__ == '__main__':

    app = QApplication(sys.argv)
    GUI = QtWidgets.QStackedWidget()
    GUI.setWindowTitle("ECCA - Departamento de Ingeniería Informática")
    GUI.setMinimumSize(1536,864)
    controladorPrincipal = ControladorPrincipal(GUI)

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
    
   

