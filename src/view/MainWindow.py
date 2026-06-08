from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QTextEdit, QTabWidget, QPushButton, QHBoxLayout, QProgressBar
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("NLP-RDF-Pipeline")
        self.resize(1200, 800)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setSizes([600, 600])

        # Central Widget
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.splitter)
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)


        # Linke Seite
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Text hier einfügen.")
        self.splitter.addWidget(self.text_input)


        # Rechte Seite
        self.tabs = QTabWidget()

        self.tab_tokens = QWidget()
        self.tab_lemmas = QWidget()
        self.tab_rdf = QWidget()

        self.tabs.addTab(self.tab_tokens, "Tokens")
        self.tabs.addTab(self.tab_lemmas, "Lemmata")
        self.tabs.addTab(self.tab_rdf, "RDF Tripel")

        self.splitter.addWidget(self.tabs)

        # Button-Panel
        self.button_layout = QHBoxLayout()

        self.btn_analyze = QPushButton("Analyse starten")
        self.btn_export = QPushButton("Ergebnisse exportieren")

        self.button_layout.addWidget(self.btn_analyze)
        self.button_layout.addWidget(self.btn_export)

        self.main_layout.addLayout(self.button_layout)

        # Fortschrittsbalken für Analyse
        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.main_layout.addWidget(self.progress)

        self.setCentralWidget(central_widget)

        