import sys

from PySide6.QtWidgets import QApplication

from view.MainWindow import MainWindow
from controller.nlp_pipeline import nlp_pipeline
from controller.controller import Controller

app = QApplication(sys.argv)

pipeline = nlp_pipeline()
view = MainWindow()
controller = Controller(view, pipeline)
view.show()

sys.exit(app.exec())