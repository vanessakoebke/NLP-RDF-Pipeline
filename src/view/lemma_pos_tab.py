from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)

class lemma_pos_tab(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.info_label = QLabel()
        self.layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def set_result(self, lemmas, pos):
        distinct_lemmas = len({tupel[1] for tupel in lemmas})
        self.info_label.setText(
            f"Der Input-Text enthält {len(lemmas)} Token und {distinct_lemmas} verschiedene Lemmata."
        )

        self.table.setRowCount(len(lemmas))
        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            ["Token", "Lemma", "Wortart", "Tag"]
        )

        for i, tupel in enumerate(lemmas):

            self.table.setItem(
                i, 0,
                QTableWidgetItem(str(tupel[0]))
            )
            self.table.setItem(
                i, 1,
                QTableWidgetItem(str(tupel[1]))
            )
        for i, tupel in enumerate(pos):

            self.table.setItem(
                i, 2,
                QTableWidgetItem(str(tupel[1]))
            )
            self.table.setItem(
                i, 3,
                QTableWidgetItem(str(tupel[2]))
            )

