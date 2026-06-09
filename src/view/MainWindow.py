from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QTextEdit, QTabWidget, QPushButton, QHBoxLayout, QProgressBar, QMessageBox
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QGuiApplication
from view.token_tab import token_tab
from view.sentence_tab import sentence_tab
from view.lemma_pos_tab import lemma_pos_tab
from view.ner_tab import ner_tab
from view.dependency_tab import dependency_tab
from view.dependency_tree_tab import dependency_tree_tab

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.center_window()

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
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Text hier einfügen.")
        self.splitter.addWidget(self.input_text)


        # Rechte Seite
        self.tabs = QTabWidget()

        self.tab_sents = sentence_tab()
        self.tab_tokens = token_tab()
        self.tab_lemmas = lemma_pos_tab()
        self.tab_dependencies = dependency_tab()
        self.tab_ner = ner_tab()
        self.tab_rdf = QWidget()

        self.tabs.addTab(self.tab_sents, "Sätze")
        self.tabs.addTab(self.tab_tokens, "Tokens")
        self.tabs.addTab(self.tab_lemmas, "Lemmata und POS")
        self.tabs.addTab(self.tab_dependencies, "Abhängigkeiten")
        self.tabs.addTab(self.tab_ner, "NER")
        self.tabs.addTab(self.tab_rdf, "RDF Tripel")


        self.splitter.addWidget(self.tabs)

        # Button-Panel
        self.button_layout = QHBoxLayout()

        self.analyze_button = QPushButton("Analyse starten")
        self.export_button = QPushButton("Ergebnisse exportieren")

        self.button_layout.addWidget(self.analyze_button)
        self.button_layout.addWidget(self.export_button)

        self.main_layout.addLayout(self.button_layout)

        # Fortschrittsbalken für Analyse
        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.main_layout.addWidget(self.progress)

        self.setCentralWidget(central_widget)

    def center_window(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()

        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def get_input_text(self) -> str:
        return self.input_text.toPlainText()
    
    def set_progress(self, value: int):
        self.progress.setValue(value)

    def show_error(self, msg: str):
        QMessageBox.critical(self, "Fehler", msg)
    
    def show_message(self, msg: str):
        QMessageBox.information(self, "Info", msg)
    
    def show_results(self, result: dict):
        self.current_results = result

        self.tabs.clear()

        # --- Sätze Tab ---
        tab_sentences = sentence_tab()
        tab_sentences.set_result(result.get("sentences"))
        self.tabs.addTab(tab_sentences, "Sätze")


        # --- Tokens Tab ---
        tab_tokens = token_tab()
        tab_tokens.set_result(result.get("tokens"))
        self.tabs.addTab(tab_tokens, "Tokens")

        # --- Lemmata und POS Tab ---
        tab_lemmas = lemma_pos_tab()
        tab_lemmas.set_result(result.get("lemmas"), result.get("pos"))
        self.tabs.addTab(tab_lemmas, "Lemmata und POS")

        # --- NER Tab ---
        tab_ner = ner_tab()
        tab_ner.set_result(result.get("ner"))
        self.tabs.addTab(tab_ner, "NER")

        # --- Dependency Tab ---
        tab_dependencies = dependency_tab()
        tab_dependencies.set_result(result.get("dependencies"))
        self.tabs.addTab(tab_dependencies, "Abhängigkeiten")

        # --- Dependency Tree Tab ---
        tab_dependency_tree = dependency_tree_tab()
        tab_dependency_tree.set_result(result.get("dependency_html"))
        self.tabs.addTab(tab_dependency_tree, "Abhängigkeitenbaum")

        
        
