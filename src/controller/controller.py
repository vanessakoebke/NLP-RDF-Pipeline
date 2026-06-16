class Controller:
    def __init__(self, view, pipeline):
        self.view = view
        self.pipeline = pipeline

        self._connect_signals()
    
    def _connect_signals(self):
        self.view.analyze_button.clicked.connect(self.analyze)
        self.view.export_button.clicked.connect(self.export)
        self.view.clear_button.clicked.connect(self.clear_text_field)

    def clear_text_field(self):
        self.view.clear_all()

    def analyze(self):
        text = self.view.get_input_text()
        self.view.lock_text()
        if not text.strip():
            self.view.show_error("Kein Text eingegeben.")
            return

        self.view.set_progress(0)

        result = self.pipeline.analyze(
            text,
            progress_callback=self.update_progressbar
        )

        self.view.show_results(result)
        self.view.set_progress(100)

    def update_progressbar(self, value: int):
        self.view.set_progress(value)

    def export(self):
        result = self.view.get_current_results()

        if not result:
            self.view.show_error("Keine Ergebnisse zu exportieren.")
            return

        self.pipeline.export(result)
        self.view.show_message("Export erfolgreich.")