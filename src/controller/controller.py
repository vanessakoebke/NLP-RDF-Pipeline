class Controller:
    def __init__(self, view, pipeline, exporter):
        self.view = view
        self.pipeline = pipeline
        self.exporter = exporter
        self.current_result = None

        self._connect_signals()
    
    def _connect_signals(self):
        self.view.analyze_button.clicked.connect(self.analyze)
        self.view.export_button.clicked.connect(self.export)
        self.view.clear_button.clicked.connect(self.clear_text_field)

    def clear_text_field(self):
        self.current_result = None
        self.view.clear_all()

    def analyze(self):
        text = self.view.get_input_text()
        if not text.strip():
            self.view.show_error("Kein Text eingegeben.")
            return

        self.view.lock_text()
        self.view.set_progress(0)

        result = self.pipeline.analyze(
            text,
            progress_callback=self.update_progressbar
        )

        self.current_result = result
        self.view.show_results(result)
        self.view.set_progress(100)

    def update_progressbar(self, value: int):
        self.view.set_progress(value)

    def export(self):
        if not self.current_result:
            self.view.show_error("Keine Ergebnisse zu exportieren.")
            return

        export_path = self.view.get_export_path()
        if not export_path:
            return

        self.exporter.export(self.current_result, export_path)
        self.view.show_message("Export erfolgreich.")
