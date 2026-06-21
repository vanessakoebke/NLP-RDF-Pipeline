from model.relation_extractor import RelationExtractor


class NlpPipeline:
    def __init__(self, relation_extractor=None):
        import spacy

        self.spacy = spacy.load("en_core_web_sm")
        self.relation_extractor = relation_extractor or RelationExtractor()

    def analyze(self, input_text: str, progress_callback=None):
        result = {
            "sentences": [],
            "tokens": [],
            "ner": [],
            "dependencies": [],
            "dependency_trees": [],
            "embeddings": {},
            "relations": []
        }

        total_steps = 7
        step = 0

        processed_text = self.spacy(input_text)

        result["sentences"] = [
            {
                "text": sent.text,
                "start": sent.start_char,
                "end": sent.end_char
            }
            for sent in processed_text.sents
        ]
        step = self._report_progress(step, total_steps, progress_callback)

        result["tokens"] = [
            {
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_,
                "start": token.idx,
                "end": token.idx + len(token.text)
            }
            for token in processed_text
        ]
        step = self._report_progress(step, total_steps, progress_callback)

        result["ner"] = [
            {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            }
            for ent in processed_text.ents
        ]
        step = self._report_progress(step, total_steps, progress_callback)

        result["dependencies"] = [
            (token.text, token.dep_, token.head.text)
            for token in processed_text
        ]
        step = self._report_progress(step, total_steps, progress_callback)

        result["dependency_trees"] = [
            self._build_dependency_tree(sent)
            for sent in processed_text.sents
        ]
        step = self._report_progress(step, total_steps, progress_callback)

        result["embeddings"] = {
            "type": "doc",
            "text": processed_text.text,
            "vector": processed_text.vector.tolist()
        }
        step = self._report_progress(step, total_steps, progress_callback)

        result["relations"] = self.relation_extractor.extract(processed_text)
        self._report_progress(step, total_steps, progress_callback)

        return result

    def _build_dependency_tree(self, sent):
        words = [
            {
                "text": token.text,
                "tag": token.tag_
            }
            for token in sent
        ]

        arcs = []
        for token in sent:
            if token.i == token.head.i:
                continue

            start = min(token.i, token.head.i) - sent.start
            end = max(token.i, token.head.i) - sent.start
            direction = "left" if token.i < token.head.i else "right"

            arcs.append({
                "start": start,
                "end": end,
                "label": token.dep_,
                "dir": direction
            })

        return {
            "sentence": sent.text,
            "words": words,
            "arcs": arcs
        }

    def _report_progress(self, step, total_steps, progress_callback):
        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))

        return step
