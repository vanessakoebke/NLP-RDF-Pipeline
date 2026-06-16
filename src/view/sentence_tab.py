from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)
from PySide6.QtCore import Qt

class sentence_tab(QWidget):

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

    def set_result(self, sentences):
        if len(sentences) == 1:
            label = "Der eingegebene Text enthält einen Satz."
        else:
            label = f"Der eingegebene Text enthält {len(sentences)} Sätze."        
        self.info_label.setText(label)

        self.table.setRowCount(len(sentences))
        self.table.setColumnCount(1)
        self.table.setColumnWidth(0, 800)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.setHorizontalHeaderLabels(
            ["Sätze"]
        )

        for i, sent in enumerate(sentences):
            item = QTableWidgetItem(str(sent.get("text")))

            item.setData(Qt.UserRole, sent["start"])
            item.setData(Qt.UserRole + 1, sent["end"])
            self.table.setItem(
                i, 0, item
            )

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