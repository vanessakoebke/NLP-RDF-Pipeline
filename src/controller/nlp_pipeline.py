from spacy import displacy

class nlp_pipeline:
    def __init__(self, model_name="en_core_web_sm"):
        import spacy

        self.spacy = spacy.load(model_name)

    def analyze(self, input_text: str, progress_callback=None):
        result = {
            "sentences": [],
            "tokens": [],
            "lemmas": [],
            "pos": [],
            "ner": [],
            "dependencies": [],
            "dependency_html": []
        }

        total_steps = 7
        step = 0

        processed_text = self.spacy(input_text)

        # --- Satzsegmentierung ---
        sentences = [sent.text for sent in processed_text.sents]
        result["sentences"] = sentences

        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))

        # --- 1. Tokenisierung ---
        tokens = [token.text for token in processed_text]
        result["tokens"] = tokens

        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))

        # --- 2. Lemmatisierung ---
        lemmas = [(token.text, token.lemma_) for token in processed_text]
        result["lemmas"] = lemmas

        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))

        # --- POS tagging ---
        pos = [(token.text, token.pos_, token.tag_) for token in processed_text]

        result["pos"] = pos

        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))

        # --- 3. NER ---
        entities = [(ent.text, ent.label_) for ent in processed_text.ents]
        result["ner"] = entities

        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))

        # --- Dependency parsing ---
        dependencies = [(token.text, token.dep_, token.head.text) for token in processed_text]
        result["dependencies"] = dependencies

        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))

        # --- Dependency HTML erstellen ---
        dependency_html = []
        for sent in processed_text.sents:
            dependency_html.append({
                "sentence": sent.text,
                "html": displacy.render(sent, style="dep", page=True)
                })
        result["dependency_html"] = dependency_html

        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))
        

        # --- 4. RDF-Tripel bauen ---

        return result
