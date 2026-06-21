from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QTextEdit, QTabWidget, QPushButton, QHBoxLayout, QProgressBar, QMessageBox, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from view.sentence_tab import sentence_tab
from view.lemma_pos_tab import LemmaPosTab
from view.ner_tab import NerTab
from view.dependency_tab import dependency_tab
from view.dependency_tree_tab import dependency_tree_tab
from view.embeddings_tab import embeddings_tab
from PySide6.QtGui import QTextCursor, QTextCharFormat
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication
from view.relations_tab import RelationTab

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

        self.set_tabs()


        self.splitter.addWidget(self.tabs)

        # Button-Panel
        self.button_layout = QHBoxLayout()

        self.analyze_button = QPushButton("Analyse starten")
        self.export_button = QPushButton("Ergebnisse exportieren")
        self.clear_button = QPushButton("Zurücksetzen")

        self.button_layout.addWidget(self.analyze_button)
        self.button_layout.addWidget(self.export_button)
        self.button_layout.addWidget(self.clear_button)

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
    
    def lock_text(self):
        self.input_text.setReadOnly(True)
    
    def set_progress(self, value: int):
        self.progress.setValue(value)

    def show_error(self, msg: str):
        QMessageBox.critical(self, "Fehler", msg)
    
    def show_message(self, msg: str):
        QMessageBox.information(self, "Info", msg)

    def get_export_path(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Ergebnisse exportieren",
            "analysis_results.json",
            "JSON-Dateien (*.json);;Alle Dateien (*)"
        )
        return path

    def clear_all(self):
        self.input_text.clear()
        self.input_text.setReadOnly(False)
        self.set_progress(0)
        self.set_tabs()
    
    def show_results(self, result: dict):
        self.tabs.clear()

        # --- Sätze Tab ---
        tab_sentences = sentence_tab(self)
        tab_sentences.set_result(result.get("sentences"))
        self.tabs.addTab(tab_sentences, "Sätze")


        # --- Tokens, Lemmata und POS Tab ---
        tab_lemmas = LemmaPosTab(self)
        tab_lemmas.set_result(result.get("tokens"))
        self.tabs.addTab(tab_lemmas, "Token, Lemmata und POS")

        # --- NER Tab ---
        tab_ner = NerTab(self)
        tab_ner.set_result(result.get("ner"))
        self.tabs.addTab(tab_ner, "NER")

        # --- Dependency Tab ---
        tab_dependencies = dependency_tab()
        tab_dependencies.set_result(result.get("dependencies"))
        self.tabs.addTab(tab_dependencies, "Abhängigkeiten")

        # --- Dependency Tree Tab ---
        tab_dependency_tree = dependency_tree_tab()
        tab_dependency_tree.set_result(result.get("dependency_trees"))
        self.tabs.addTab(tab_dependency_tree, "Abhängigkeitenbaum")

        # --- Embeddings Tab ---
        tab_embeddings = embeddings_tab()
        tab_embeddings.set_result(result.get("embeddings"))
        self.tabs.addTab(tab_embeddings, "Embeddings")

        # --- Relations Tab ---
        tab_relations = RelationTab(self)
        tab_relations.set_result(result.get("relations"))
        self.tabs.addTab(tab_relations, "Relationen")


    def highlight_text(self, start: int, end: int):
        cursor = self.input_text.textCursor()

        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)


        color = QApplication.palette().color(QPalette.Highlight)
        fmt = QTextCharFormat()
        fmt.setBackground(color)

        selection = QTextEdit.ExtraSelection()
        selection.cursor = cursor
        selection.format = fmt

        self.input_text.setExtraSelections([selection])

    def clear_highlight(self):
        self.input_text.setExtraSelections([])

    def set_tabs(self):
        self.tabs.clear()
        self.tab_sents = sentence_tab(self)
        self.tab_lemmas = LemmaPosTab(self)
        self.tab_dependencies = dependency_tab()
        self.tab_ner = NerTab(self)
        self.tab_embeddings = embeddings_tab()
        self.tab_rdf = QWidget()
        self.tab_relations = RelationTab(self)

        self.tabs.addTab(self.tab_sents, "Sätze")
        self.tabs.addTab(self.tab_lemmas, "Tokens, Lemmata und POS")
        self.tabs.addTab(self.tab_dependencies, "Abhängigkeiten")
        self.tabs.addTab(self.tab_ner, "NER")
        self.tabs.addTab(self.tab_embeddings, "Embeddings")
        self.tabs.addTab(self.tab_rdf, "RDF Tripel")
        self.tabs.addTab(self.tab_relations, "Relationen")
        
        
