from transformers import pipeline

class Summarizer:
    def __init__(self, model_path):
        self.summarizer = self.init_summarizer(model_path)

    def init_summarizer(self, model_path):
        return pipeline("summarization", model=model_path, max_length=128, device=1)

    def predict_query(self, question_string):
        return self.summarizer(question_string)[0]['summary_text']