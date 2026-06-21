import sys

from PySide6.QtWidgets import QApplication

from view.MainWindow import MainWindow
from model.nlp_pipeline import NlpPipeline
from model.result_exporter import ResultExporter
from controller.controller import Controller

app = QApplication(sys.argv)

pipeline = NlpPipeline()
exporter = ResultExporter()
view = MainWindow()
controller = Controller(view, pipeline, exporter)
view.show()

sys.exit(app.exec())
