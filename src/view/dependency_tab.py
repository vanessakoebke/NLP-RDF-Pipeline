from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)

class dependency_tab(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def set_result(self, dependencies):

        self.table.setRowCount(len(dependencies))
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(
            ["Token", "Abhängigkeit", "Kopf"]
        )

        for i, tupel in enumerate(dependencies):

            self.table.setItem(
                i, 0,
                QTableWidgetItem(str(tupel[0]))
            )
            self.table.setItem(
                i, 1,
                QTableWidgetItem(str(tupel[1]))
            )
            self.table.setItem(
                i, 2,
                QTableWidgetItem(str(tupel[2]))
            )

