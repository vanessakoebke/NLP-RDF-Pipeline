from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from model.label_descriptions import NER_LABELS
from view.base_table_tab import ResultTab

class NerTab(ResultTab):

    def __init__(self, mainwindow):
        super().__init__(mainwindow=mainwindow, highlight_column=0)

    def set_result(self, ner):
        self.info_label.setText(
            f"Der eingegebene Text enthält {len(ner)} Named Entities."
        )

        self.table.setRowCount(len(ner))
        self.table.setColumnCount(2)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setColumnWidth(0, 100)
        self.table.setHorizontalHeaderLabels(
            ["Entity", "Typ"]
        )

        for i, tupel in enumerate(ner):

            self.table.setItem(
                i, 0,
                QTableWidgetItem(str(tupel["text"]))
            )

            item = QTableWidgetItem(str(tupel["label"]))
            item.setToolTip(NER_LABELS.get(tupel["label"], tupel["label"]))
            self.table.setItem(
                i, 1, item
            )

            self.set_highlight(self.table.item(i, 0), tupel["start"], tupel["end"])
