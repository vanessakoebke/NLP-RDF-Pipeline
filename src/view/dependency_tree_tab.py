from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea
from PySide6.QtWebEngineWidgets import QWebEngineView


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
        self.dependency_html = []

    # -------------------------
    # Daten setzen
    # -------------------------
    def set_result(self, dependency_html):
        self.dependency_html = dependency_html
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
        for i, item in enumerate(self.dependency_html):

            btn = QPushButton(
                f"{item['sentence'][:100]}..."
            )

            # stabiler Signal-Handler (kein Lambda-Bug)
            btn.clicked.connect(self.make_handler(item["html"]))

            self.button_layout.addWidget(btn)

    # -------------------------
    # Click Handler
    # -------------------------
    def make_handler(self, html):
        return lambda checked=False: self.show_html(html)

    # -------------------------
    # HTML anzeigen
    # -------------------------
    def show_html(self, html):
        self.web_view.setHtml(html)