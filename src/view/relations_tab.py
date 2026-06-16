from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt

class RelationTab(QWidget):

    def __init__(self, mainwindow):
        super().__init__()
        self.main_window = mainwindow
        self.layout = QVBoxLayout(self)

        self.info_label = QLabel()
        self.layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.table.setMouseTracking(True)
        self.table.viewport().setMouseTracking(True)
        self.table.cellEntered.connect(self.on_hover)
        self.table.leaveEvent = self.on_leave
        self.layout.addWidget(self.table)

        

    def set_result(self, relations):
        

        self.table.setRowCount(len(relations))
        self.table.setColumnCount(3)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.setHorizontalHeaderLabels(
            ["Subjekt", "Relation", "Objekt"]
        )

        for i, tupel in enumerate(relations):

            self.table.setItem(
                i, 0,
                QTableWidgetItem(str(tupel["subject"]))
            )

            self.table.setItem(
                i, 1,
                QTableWidgetItem(str(tupel["predicate"]))
            )

            item = QTableWidgetItem(str(tupel["object"]))
            self.table.setItem(
                i, 2, item
            )


            self.table.item(i, 0).setData(Qt.UserRole, tupel["start"])
            self.table.item(i, 0).setData(Qt.UserRole + 1, tupel["end"])

    def on_hover(self, row, col):
        item = self.table.item(row, 0)
        if not item:
            return

        start = item.data(Qt.UserRole)
        end = item.data(Qt.UserRole + 1)

        if start is None or end is None:
            return

        self.main_window.highlight_text(start, end)
    
    def on_leave(self, event):
        self.main_window.clear_highlight()
        super().leaveEvent(event)