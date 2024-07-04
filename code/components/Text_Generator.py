from transformers import pipeline

class Text_Generator:
    def __init__(self, model_path):
        self.generator = self.init_generator(model_path)

    def init_generator(self, model_path):
        # add device= to specify a GPU or -1 to run on CPU
        return pipeline("text2text-generation", model=model_path, max_length=256)

    def predict_sparql(self, question_string):
        return self.generator(question_string)[0]['generated_text']