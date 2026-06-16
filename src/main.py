import sys

from PySide6.QtWidgets import QApplication

from view.MainWindow import MainWindow
from controller.nlp_pipeline import NlpPipeline
from controller.controller import Controller

app = QApplication(sys.argv)

pipeline = NlpPipeline()
view = MainWindow()
controller = Controller(view, pipeline)
view.show()

sys.exit(app.exec())