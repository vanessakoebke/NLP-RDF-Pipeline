import json


class ResultExporter:
    def export(self, result, path):
        with open(path, "w", encoding="utf-8") as export_file:
            json.dump(result, export_file, ensure_ascii=False, indent=2)
