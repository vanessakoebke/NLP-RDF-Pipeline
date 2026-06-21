from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QTableWidget, QVBoxLayout, QWidget


class ResultTab(QWidget):
    def __init__(self, mainwindow=None, show_info_label=True, highlight_column=None):
        super().__init__()
        self.main_window = mainwindow
        self.highlight_column = highlight_column

        self.layout = QVBoxLayout(self)

        self.info_label = None
        if show_info_label:
            self.info_label = QLabel()
            self.layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        if self.highlight_column is not None:
            self.table.setMouseTracking(True)
            self.table.viewport().setMouseTracking(True)
            self.table.cellEntered.connect(self.on_hover)
            self.table.leaveEvent = self.on_leave

    def set_highlight(self, item, start, end):
        item.setData(Qt.UserRole, start)
        item.setData(Qt.UserRole + 1, end)

    def on_hover(self, row, col):
        if self.main_window is None or self.highlight_column is None:
            return

        item = self.table.item(row, self.highlight_column)
        if not item:
            return

        start = item.data(Qt.UserRole)
        end = item.data(Qt.UserRole + 1)

        if start is None or end is None:
            return

        self.main_window.highlight_text(start, end)

    def on_leave(self, event):
        if self.main_window is not None:
            self.main_window.clear_highlight()

        super().leaveEvent(event)
