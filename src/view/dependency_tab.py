from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from model.label_descriptions import DEP_DESCRIPTIONS
from view.base_table_tab import ResultTab

class dependency_tab(ResultTab):

    def __init__(self):
        super().__init__(show_info_label=False)

    def set_result(self, dependencies):

        self.table.setRowCount(len(dependencies))
        self.table.setColumnCount(3)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.setHorizontalHeaderLabels(
            ["Token", "Abhängigkeit", "Bezugswort"]
        )

        for i, tupel in enumerate(dependencies):

            self.table.setItem(
                i, 0,
                QTableWidgetItem(str(tupel[0]))
            )
            item = QTableWidgetItem(str(tupel[1]))
            item.setToolTip(DEP_DESCRIPTIONS.get(tupel[1], tupel[1]))
            self.table.setItem(
                i, 1,
                item
            )
            self.table.setItem(
                i, 2,
                QTableWidgetItem(str(tupel[2]))
            )
