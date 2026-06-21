from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from view.base_table_tab import ResultTab

class token_tab(ResultTab):

    def __init__(self):
        super().__init__()

    def set_result(self, tokens):
        self.info_label.setText(
            f"Der Input-Text enthält {len(tokens)} Tokens."
        )

        self.table.setRowCount(len(tokens))
        self.table.setColumnCount(1)

        self.table.setHorizontalHeaderLabels(
            ["Token"]
        )

        for i, tok in enumerate(tokens):

            self.table.setItem(
                i, 0,
                QTableWidgetItem(str(tok))
            )
