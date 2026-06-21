from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea
from PySide6.QtWebEngineWidgets import QWebEngineView
from spacy import displacy


class dependency_tree_tab(QWidget):

    def __init__(self):
        super().__init__()

        # --- Hauptlayout (WICHTIG: explizit setzen) ---
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # =========================
        # Scroll Area (Satzliste)
        # =========================
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(150)

        self.button_container = QWidget()
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(6)

        self.scroll_area.setWidget(self.button_container)

        # =========================
        # WebView (Dependency Tree)
        # =========================
        self.web_view = QWebEngineView()

        # =========================
        # Layout zusammensetzen
        # =========================
        self.main_layout.addWidget(self.scroll_area, stretch=1)
        self.main_layout.addWidget(self.web_view, stretch=4)

        # Daten
        self.dependency_trees = []

    # -------------------------
    # Daten setzen
    # -------------------------
    def set_result(self, dependency_trees):
        self.dependency_trees = dependency_trees or []
        self.set_sentences()

    # -------------------------
    # Buttons erzeugen
    # -------------------------
    def set_sentences(self):

        # alte Buttons entfernen (sauber!)
        while self.button_layout.count():
            item = self.button_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # neue Buttons
        for i, item in enumerate(self.dependency_trees):

            btn = QPushButton(
                f"{item['sentence'][:100]}..."
            )

            # stabiler Signal-Handler (kein Lambda-Bug)
            btn.clicked.connect(self.make_handler(item))

            self.button_layout.addWidget(btn)

    # -------------------------
    # Click Handler
    # -------------------------
    def make_handler(self, dependency_tree):
        return lambda checked=False: self.show_dependency_tree(dependency_tree)

    # -------------------------
    # HTML anzeigen
    # -------------------------
    def show_dependency_tree(self, dependency_tree):
        html = displacy.render(
            dependency_tree,
            style="dep",
            manual=True,
            page=True
        )
        self.web_view.setHtml(html)
