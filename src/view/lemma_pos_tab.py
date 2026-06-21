from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from model.label_descriptions import POS_DESCRIPTIONS, TAG_DESCRIPTIONS
from view.base_table_tab import ResultTab

class LemmaPosTab(ResultTab):

    def __init__(self, mainwindow):
        super().__init__(mainwindow=mainwindow, highlight_column=0)

    def set_result(self, tokens):
        distinct_lemmas = len({tupel["lemma"] for tupel in tokens})
        self.info_label.setText(
            f"Der Input-Text enthält {len(tokens)} Token und {distinct_lemmas} verschiedene Lemmata."
        )

        self.table.setRowCount(len(tokens))
        self.table.setColumnCount(4)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.setHorizontalHeaderLabels(
            ["Token", "Lemma", "Wortart", "Tag"]
        )

        for i, tupel in enumerate(tokens):

            self.table.setItem(
                i, 0,
                QTableWidgetItem(str(tupel["text"]))
            )

            self.table.setItem(
                i, 1,
                QTableWidgetItem(str(tupel["lemma"]))
            )

            item = QTableWidgetItem(str(tupel["pos"]))
            item.setToolTip(POS_DESCRIPTIONS.get(tupel["pos"], tupel["pos"]))
            self.table.setItem(
                i, 2, item
            )

            item = QTableWidgetItem(str(tupel["tag"]))
            item.setToolTip(TAG_DESCRIPTIONS.get(tupel["tag"], tupel["tag"]))
            self.table.setItem(
                i, 3, item
            )

            self.set_highlight(self.table.item(i, 0), tupel["start"], tupel["end"])
