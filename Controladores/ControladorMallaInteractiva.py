from Vistas.VistaMalla import VistaMalla

class ControladorMallaInteractiva():

    def __init__(self, databaseContext, GUI, plan, ano, periodo):

        self.databaseContext = databaseContext
        self.vistaMalla = VistaMalla(self)
        self.GUI = GUI

        self.idPlan = plan.getId()
        self.ano = ano
        self.periodo = periodo
        self.iniciarVistaMalla()

    def iniciarVistaMalla(self):
        print("Inicio con id: ", self.idPlan)
        self.GUI.addWidget(self.vistaMalla)
        self.GUI.setCurrentIndex(self.GUI.currentIndex()+1)
