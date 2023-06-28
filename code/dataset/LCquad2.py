from utils.data_io import export_csv

nlp_en = spacy.load("en_core_web_sm")


class LCquad:
    def __init__(self, lcquad_file) -> None:
        self.lcquad = self.init_lcquad_list(lcquad_file)

    def init_lcquad_list(self, lcquad_file: list):
        lcquad_list = []
        for lcquad in lcquad_file:
            lcquad_entry = LCquad_entry(
                lcquad["NNQT_question"],
                lcquad["uid"],
                lcquad["question"],
                lcquad["sparql_wikidata"]
            )
            lcquad_list.append(lcquad_entry)
        return lcquad_list

    def export_train_csv(self, output_file, include_linguistic_context: bool = False, include_entity_knowledge: bool = False):
        csv_dataset = [["question", "query"]]
        lcquad_entry: LCquad_entry
        for lcquad_entry in self.lcquad:
            query = lcquad_entry.preprossed_query
            question = lcquad_entry.get_question_string(
                include_linguistic_context, include_entity_knowledge)
            csv_dataset.append([question, query])
        export_csv(output_file, csv_dataset)


class LCquad_entry:
    def __init__(self, NNQT_question, uid, question, sparql_wikidata) -> None:
        self.NNQT_question = self.preprocess_nnqt_question(NNQT_question)
        self.uid = uid
        self.question = question
        self.query = sparql_wikidata
        self.preprossed_query = preprocess_sparql(sparql_wikidata)

    def get_question_string(self, include_linguistic_context, include_entity_knowledge) -> str:
        question_string = self.NNQT_question
        if include_linguistic_context:
            question_string += self.get_linguistic_context_string()
        if include_entity_knowledge:
            question_string += self.get_entity_knowledge()
        return question_string

    def get_linguistic_context_string(self) -> str:
        _, pos, dep, depth_list = get_linguistic_context(nlp_en, self.NNQT_question)
        return " <pad> " + " ".join(pos) \
                + " <pad> " + " ".join(dep) \
                + " <pad> " + " ".join(map(str, depth_list))

    def get_entity_knowledge(self) -> str:
        pattern = r'\bwd_\w+\b'
        entities = re.findall(pattern, self.preprossed_query)
        return " <pad> " + (" ").join(entities)

    def preprocess_nnqt_question(self, NNQT_ques):
        NNQT_ques = NNQT_ques.translate(str.maketrans('<>{},()', '       '))
        NNQT_ques = re.sub(' +', ' ', NNQT_ques)
        return NNQT_ques
