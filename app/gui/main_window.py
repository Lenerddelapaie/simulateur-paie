from PyQt5.QtWidgets import QMainWindow, QTabWidget
from app.gui.tabs.horaires_tab import HorairesTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulateur de Paie - Anthony Roca")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_tab_horaires()

    def init_tab_horaires(self):
        self.tab_horaires = HorairesTab()
        self.tabs.addTab(self.tab_horaires, "Horaires établissement")
