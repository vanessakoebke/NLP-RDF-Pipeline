from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt

class LemmaPosTab(QWidget):

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

        self.POS_DESCRIPTIONS = {
            "ADJ": "Adjektiv",
            "ADP": "Adposition",
            "ADV": "Adverb",
            "AUX": "Hilfsverb",
            "CONJ": "Konjunktion",
            "CCONJ": "Koordinierende Konjunktion",
            "DET": "Determinierer",
            "INTJ": "Interjektion",
            "NOUN": "Substantiv",
            "NUM": "Zahlwort",
            "PART": "Partikel",
            "PRON": "Pronomen",
            "PROPN": "Eigenname",
            "PUNCT": "Interpunktion",
            "SCONJ": "Subordinierende Konjunktion",
            "SYM": "Symbol",
            "VERB": "Verb",
            "X": "Sonstiges / unbekannt"
        }
        self.TAG_DESCRIPTIONS = {
            "NN": "Substantiv",
            "NNS": "Substantiv, Plural",
            "NNP": "Eigenname, Singular",
            "NNPS": "Eigennamen, Plural",

            "VB": "Verb",
            "VBD": "Verb, Vergangenheit",
            "VBG": "Verb, Gerundium/Partizip Präsens",
            "VBN": "Verb, Partizip Perfekt",
            "VBP": "Verb, Präsens (nicht 3. Person)",
            "VBZ": "Verb, Präsens 3. Person",

            "JJ": "Adjektiv",
            "JJR": "Adjektiv, Komparativ",
            "JJS": "Adjektiv, Superlativ",

            "RB": "Adverb",
            "RBR": "Adverb, Komparativ",
            "RBS": "Adverb, Superlativ",

            "DT": "Artikel / Determinierer",
            "IN": "Präposition oder subordinierende Konjunktion",
            "PRP": "Personalpronomen",
            "PRP$": "Possessivpronomen",
            "WP": "WH-Pronomen (who, what)",
            "WP$": "Possessives WH-Pronomen (whose)",
            "WRB": "WH-Adverb (where, when, why)",

            "CC": "Koordinierende Konjunktion",
            "CD": "Kardinalzahl",
            "EX": "Expletives Subjekt",
            "FW": "Fremdwort",
            "LS": "Listen-Markierung",
            "MD": "Modalverb",
            "POS": "Possessivsuffix ('s)",
            "RP": "Partikel",
            "SYM": "Symbol",
            "TO": "Infinitivmarker",
            "UH": "Interjektion",
        }

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
            item.setToolTip(self.POS_DESCRIPTIONS.get(tupel["pos"], tupel["pos"]))
            self.table.setItem(
                i, 2, item
            )

            item = QTableWidgetItem(str(tupel["tag"]))
            item.setToolTip(self.TAG_DESCRIPTIONS.get(tupel["tag"], tupel["tag"]))
            self.table.setItem(
                i, 3, item
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