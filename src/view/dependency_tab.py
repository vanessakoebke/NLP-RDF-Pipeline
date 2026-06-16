from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)

class dependency_tab(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.DEP_DESCRIPTIONS = {
            "ROOT": "Hauptverb",

            "nsubj": "Nominales Subjekt",
            "nsubjpass": "Subjekt im Passivsatz",
            "csubj": "Satz als Subjekt",
            "csubjpass": "Satz als Subjekt im Passiv",

            "obj": "Objekt",
            "dobj": "Direktes Objekt",
            "iobj": "Indirektes Objekt",
            "pobj": "Präpositionalobjekt",

            "attr": "Attribut",
            "oprd": "Objektsprädikativ",

            "amod": "Adjektivattribut",
            "advmod": "Adverbiale Bestimmung",
            "npadvmod": "Nominale adverbiale Bestimmung",
            "quantmod": "Quantifizierende Bestimmung",

            "det": "Artikel oder Determinierer",
            "predet": "Vorangestellter Determinierer",
            "poss": "Possessivbestimmung",
            "possessive": "Possessivmarker",

            "compound": "Teil eines zusammengesetzten Begriffs",
            "prt": "Verbpartikel",
            "case": "Kasusmarker oder Präposition",

            "prep": "Präpositionale Beziehung",
            "agent": "Handelnder im Passivsatz",

            "acl": "Attributiver Nebensatz",
            "relcl": "Relativsatz",
            "advcl": "Adverbialer Nebensatz",

            "xcomp": "Offene Satzergänzung ohne eigenes Subjekt",
            "ccomp": "Satzergänzung mit eigenem Subjekt",

            "aux": "Hilfsverb",
            "auxpass": "Hilfsverb im Passiv",
            "cop": "Kopulaverb",

            "mark": "Einleitendes Wort eines Nebensatzes",
            "expl": "Expletives Subjekt",

            "cc": "Koordinierende Konjunktion",
            "conj": "Durch Konjunktion verbundenes Element",
            "preconj": "Vorangestellte Konjunktion",

            "punct": "Satzzeichen",

            "appos": "Apposition (erläuternder Zusatz)",
            "nmod": "Nominale Ergänzung",
            "obl": "Adverbiale Ergänzung",

            "parataxis": "Nebenordnung von Satzteilen",
            "dep": "Nicht genauer spezifizierte Abhängigkeit",

            "intj": "Interjektion",
            "discourse": "Diskursmarker",
            "vocative": "Anrede",

            "meta": "Metasprachliches Element",
            "reparandum": "Korrigierter Versprecher oder Fehler",

            "list": "Listenelement",
            "orphan": "Verwaister Satzteil",
            "goeswith": "Zusammengehöriges Wortfragment",
            "fixed": "Feste Wortverbindung",
            "flat": "Flache mehrteilige Benennung",

            "neg": "Negation",
            "number": "Zahlenmodifikator",
            "npmod": "Nominale Modifikation"
        }

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
            item.setToolTip(self.DEP_DESCRIPTIONS.get(tupel[1], tupel[1]))
            self.table.setItem(
                i, 1,
                item
            )
            self.table.setItem(
                i, 2,
                QTableWidgetItem(str(tupel[2]))
            )

