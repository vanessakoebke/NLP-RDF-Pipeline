from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from view.base_table_tab import ResultTab

class sentence_tab(ResultTab):

    def __init__(self, mainwindow):
        super().__init__(mainwindow=mainwindow, highlight_column=0)

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

            self.set_highlight(item, sent["start"], sent["end"])
            self.table.setItem(
                i, 0, item
            )
