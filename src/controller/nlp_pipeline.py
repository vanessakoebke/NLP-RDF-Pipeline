from spacy import displacy

class NlpPipeline:
    def __init__(self):
        import spacy

        self.spacy = spacy.load("en_core_web_sm")


        

    def analyze(self, input_text: str, progress_callback=None):
        result = {
            "sentences": [],
            "tokens": [],
            "ner": [],
            "dependencies": [],
            "dependency_html": [],
            "embeddings": [],
            "relations": []
        }

        total_steps = 8
        step = 0

        processed_text = self.spacy(input_text)

        # --- Satzsegmentierung ---
        sentences = [
            {
                "text": sent.text,
                "start": sent.start_char,
                "end": sent.end_char
            }
            for sent in processed_text.sents
        ]
        result["sentences"] = sentences

        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))

        # --- 1. Tokenisierung ---
        tokens = [token.text for token in processed_text]
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

        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))


        # --- 3. NER ---
        entities = [
            {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            }
            for ent in processed_text.ents
        ]
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

        # --- Embeddings ---
        result["embeddings"] = {
            "type": "doc",
            "text": processed_text.text,
            "vector": processed_text.vector.tolist()
            }

        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))
        

        # --- Relation extraction ---
        result["relations"] = self.extract_relations(processed_text)


        step += 1
        if progress_callback:
            progress_callback(int(step / total_steps * 100))


        # --- 4. RDF-Tripel bauen ---

        return result

    
    
    def extract_relations(self, doc):
        relations = []

        for sent in doc.sents:
            root = sent.root

            # --------------------------------------------------
            # 1. X are Y / X is Y
            # Panic attacks are discrete episodes ...
            # --------------------------------------------------
            if root.lemma_ == "be":
                subj = None
                attr = None

                for token in root.children:
                    if token.dep_ in ("nsubj", "nsubjpass"):
                        subj = token
                        subj_phrase = ""
                        for chunk in sent.noun_chunks:
                            if subj.i >= chunk.start and subj.i < chunk.end:
                                subj_phrase = chunk.text

                    elif token.dep_ in ("attr", "acomp"):
                        attr = token
                        attr_phrase = ""
                        for chunk in sent.noun_chunks:
                            if attr.i >= chunk.start and attr.i < chunk.end:
                                attr_phrase = chunk.text

                if subj and attr:
                    desc = sent[subj.i:sent.end].text
                    desc = desc.split(root.text, 1)[-1].strip()

                    relations.append({
                        "subject": subj_phrase,
                        "predicate": "description",
                        "object": attr_phrase,
                        "start": token.sent.start_char,
                        "end": token.sent.end_char
                    })

            # --------------------------------------------------
            # 2. have / has
            # Panic attacks ... have an unexpected quality
            # --------------------------------------------------
            elif root.lemma_ == "have":
                subj = None
                obj = None

                for token in root.children:
                    if token.dep_ == "nsubj":
                        subj = token
                        subj_phrase = ""
                        for chunk in sent.noun_chunks:
                            if subj.i >= chunk.start and subj.i < chunk.end:
                                subj_phrase = chunk.text
                    elif token.dep_ in ("dobj", "obj", "attr"):
                        obj = token
                        subj_phrase = ""
                        for chunk in sent.noun_chunks:
                            if obj.i >= chunk.start and obj.i < chunk.end:
                                obj_phrase = chunk.text

                if subj and obj:
                    relations.append({
                        "subject": subj_phrase,
                        "predicate": "has",
                        "object": obj_phrase,
                        "start": token.sent.start_char,
                        "end": token.sent.end_char
                    })

            # --------------------------------------------------
            # 3. accompanied by ...
            # accompanied by physical and cognitive symptoms
            # --------------------------------------------------
            for token in sent:
                if token.lemma_ == "accompany":

                    symptoms = []

                    for child in token.children:
                        if child.lemma_ == "by":
                            for obj in child.children:
                                if obj.dep_ == "pobj":
                                    obj_phrase = ""
                                    for chunk in sent.noun_chunks:
                                        if obj.i >= chunk.start and obj.i < chunk.end:
                                            obj_phrase = chunk.text
                                    symptoms.append(obj_phrase)

                                    for mod in obj.children:
                                        if mod.dep_ == "amod":
                                            mod_phrase = ""
                                            for chunk in sent.noun_chunks:
                                                if mod.i >= chunk.start and mod.i < chunk.end:
                                                    mod_phrase = chunk.text
                                            relations.append({
                                                "subject": "panic attacks",
                                                "predicate": "has_symptom_type",
                                                "object": mod_phrase,
                                                "start": token.sent.start_char,
                                                "end": token.sent.end_char
                                            })

                    if symptoms:
                        relations.append({
                            "subject": "panic attacks",
                            "predicate": "has_symptoms",
                            "object": ", ".join(symptoms),
                            "start": token.sent.start_char,
                            "end": token.sent.end_char
                        })

            # --------------------------------------------------
            # 4. listed in ...
            # listed in the DSM-5 panic attack checklist
            # --------------------------------------------------
            for token in sent:
                if token.lemma_ == "list":

                    for child in token.children:
                        if child.dep_ == "prep" and child.lemma_ == "in":

                            for pobj in child.children:
                                if pobj.dep_ == "pobj":

                                    pobj_phrase = ""
                                    for chunk in sent.noun_chunks:
                                        if pobj.i >= chunk.start and pobj.i < chunk.end:
                                            pobj_phrase = chunk.text

                                    relations.append({
                                        "subject": "panic attacks",
                                        "predicate": "checklist",
                                        "object": pobj_phrase,
                                        "start": token.sent.start_char,
                                        "end": token.sent.end_char
                                    })

            # --------------------------------------------------
            # 5. defined by ...
            # diagnosis ... is defined by recurrent panic attacks
            # --------------------------------------------------
            for token in sent:
                if token.lemma_ == "define":

                    subj = None

                    for child in token.children:
                        if child.dep_ in ("nsubjpass", "nsubj"):
                            subj = child
                            subj_phrase = ""
                            for chunk in sent.noun_chunks:
                                if subj.i >= chunk.start and subj.i < chunk.end:
                                    subj_phrase = chunk.text

                        elif child.dep_ == "prep" and child.lemma_ == "by":

                            for pobj in child.children:
                                if pobj.dep_ == "pobj":

                                    phrase = sent[
                                        pobj.left_edge.i :
                                        pobj.right_edge.i + 1
                                    ].text

                                    relations.append({
                                        "subject": subj_phrase,
                                        "predicate": "defined_by",
                                        "object": phrase,
                                        "start": token.sent.start_char,
                                        "end": token.sent.end_char
                                    })

        return relations