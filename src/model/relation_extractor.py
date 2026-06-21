class RelationExtractor:
    def extract(self, doc):
        relations = []

        for sent in doc.sents:
            root = sent.root

            if root.lemma_ == "be":
                subj = None
                attr = None
                subj_phrase = ""
                attr_phrase = ""

                for token in root.children:
                    if token.dep_ in ("nsubj", "nsubjpass"):
                        subj = token
                        subj_phrase = self._noun_chunk_text(sent, subj)

                    elif token.dep_ in ("attr", "acomp"):
                        attr = token
                        attr_phrase = self._noun_chunk_text(sent, attr)

                if subj and attr:
                    relations.append({
                        "subject": subj_phrase,
                        "predicate": "description",
                        "object": attr_phrase,
                        "start": sent.start_char,
                        "end": sent.end_char
                    })

            elif root.lemma_ == "have":
                subj = None
                obj = None
                subj_phrase = ""
                obj_phrase = ""

                for token in root.children:
                    if token.dep_ == "nsubj":
                        subj = token
                        subj_phrase = self._noun_chunk_text(sent, subj)

                    elif token.dep_ in ("dobj", "obj", "attr"):
                        obj = token
                        obj_phrase = self._noun_chunk_text(sent, obj)

                if subj and obj:
                    relations.append({
                        "subject": subj_phrase,
                        "predicate": "has",
                        "object": obj_phrase,
                        "start": sent.start_char,
                        "end": sent.end_char
                    })

            for token in sent:
                if token.lemma_ == "accompany":
                    symptoms = []

                    for child in token.children:
                        if child.lemma_ == "by":
                            for obj in child.children:
                                if obj.dep_ == "pobj":
                                    obj_phrase = self._noun_chunk_text(sent, obj)
                                    symptoms.append(obj_phrase)

                                    for mod in obj.children:
                                        if mod.dep_ == "amod":
                                            mod_phrase = self._noun_chunk_text(sent, mod)
                                            relations.append({
                                                "subject": "panic attacks",
                                                "predicate": "has_symptom_type",
                                                "object": mod_phrase,
                                                "start": sent.start_char,
                                                "end": sent.end_char
                                            })

                    if symptoms:
                        relations.append({
                            "subject": "panic attacks",
                            "predicate": "has_symptoms",
                            "object": ", ".join(symptoms),
                            "start": sent.start_char,
                            "end": sent.end_char
                        })

            for token in sent:
                if token.lemma_ == "list":
                    for child in token.children:
                        if child.dep_ == "prep" and child.lemma_ == "in":
                            for pobj in child.children:
                                if pobj.dep_ == "pobj":
                                    relations.append({
                                        "subject": "panic attacks",
                                        "predicate": "checklist",
                                        "object": self._noun_chunk_text(sent, pobj),
                                        "start": sent.start_char,
                                        "end": sent.end_char
                                    })

            for token in sent:
                if token.lemma_ == "define":
                    subj_phrase = ""

                    for child in token.children:
                        if child.dep_ in ("nsubjpass", "nsubj"):
                            subj_phrase = self._noun_chunk_text(sent, child)

                        elif child.dep_ == "prep" and child.lemma_ == "by":
                            for pobj in child.children:
                                if pobj.dep_ == "pobj":
                                    phrase = pobj.doc[
                                        pobj.left_edge.i : pobj.right_edge.i + 1
                                    ].text

                                    relations.append({
                                        "subject": subj_phrase,
                                        "predicate": "defined_by",
                                        "object": phrase,
                                        "start": sent.start_char,
                                        "end": sent.end_char
                                    })

        return relations

    def _noun_chunk_text(self, sent, token):
        for chunk in sent.noun_chunks:
            if chunk.start <= token.i < chunk.end:
                return chunk.text

        return token.text
