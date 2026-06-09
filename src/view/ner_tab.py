from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)

class ner_tab(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.info_label = QLabel()
        self.layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def set_result(self, ner):
        self.info_label.setText(
            f"Der eingegebene Text enthält {len(ner)} Named Entities."
        )

        self.table.setRowCount(len(ner))
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(
            ["Token", "Entity"]
        )

        for i, tupel in enumerate(ner):

            self.table.setItem(
                i, 0,
                QTableWidgetItem(str(tupel[0]))
            )
            self.table.setItem(
                i, 1,
                QTableWidgetItem(str(tupel[1]))
            )


