from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class embeddings_tab(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text = QTextEdit()
        self.text.setReadOnly(True)

        self.layout.addWidget(self.text)

    def set_result(self, vecto):
        vector = vecto["vector"]

        html = "<h3>Doc Embedding</h3>"
        html += f"<p>Dimensionen: {len(vector)}</p>"
        html += "<table border='1' cellpadding='4'>"

        html += "<tr><th>Index</th><th>Wert</th></tr>"

        for i, val in enumerate(vector):
            html += f"<tr><td>{i}</td><td>{val:.4f}</td></tr>"

        html += "</table>"

        self.text.setHtml(html)