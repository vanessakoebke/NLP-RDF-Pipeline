from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from view.base_table_tab import ResultTab

class RelationTab(ResultTab):

    def __init__(self, mainwindow):
        super().__init__(mainwindow=mainwindow, highlight_column=0)

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


            self.set_highlight(self.table.item(i, 0), tupel["start"], tupel["end"])
