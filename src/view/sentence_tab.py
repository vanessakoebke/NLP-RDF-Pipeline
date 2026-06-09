from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)

class sentence_tab(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.info_label = QLabel()
        self.layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def set_result(self, sentences):
        if len(sentences) == 1:
            label = "Der eingegebene Text enthält einen Satz."
        else:
            label = f"Der eingegebene Text enthält {len(sentences)} Sätze."        
        self.info_label.setText(label)

        self.table.setRowCount(len(sentences))
        self.table.setColumnCount(1)

        self.table.setHorizontalHeaderLabels(
            ["Sätze"]
        )

        for i, sent in enumerate(sentences):

            self.table.setItem(
                i, 0,
                QTableWidgetItem(str(sent))
            )
