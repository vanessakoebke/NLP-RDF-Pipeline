from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)

class token_tab(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.info_label = QLabel()
        self.layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def set_result(self, tokens):
        self.info_label.setText(
            f"Der Input-Text enthält {len(tokens)} Tokens."
        )

        self.table.setRowCount(len(tokens))
        self.table.setColumnCount(1)

        self.table.setHorizontalHeaderLabels(
            ["Token"]
        )

        for i, tok in enumerate(tokens):

            self.table.setItem(
                i, 0,
                QTableWidgetItem(str(tok))
            )
