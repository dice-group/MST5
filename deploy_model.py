'''
Example usage: 

python deploy_model.py --model fine-tuned_models/qald9plus-finetune \
    --knowledge_graph Wikidata \
    --linguistic_context \
    --entity_knowledge \
    --question_padding_length 32 \
    --entity_padding_length 5 \
    --port 8181
'''
import sys
sys.path.append('./code/')

from components.Summarizer import Summarizer
from components.Question import Question
from components.Knowledge_graph import Knowledge_graph
from components.Language import Language
from components.Query import Query

import argparse
import logging
import json
import os
# importing the flask Module
from flask import request
from flask import Flask

# Variable to store the input attributes unique to the model
model_attr_kwargs = {}
sparql_model = None
port = 8989

# configuring logging
log_filename = 'logs/server.log'
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
logging.basicConfig(filename=log_filename, level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s', filemode='w')

def get_wikidata_entities(question: Question):
        ner = Language.get_supported_ner(question.language)
        if ner == "no_ner":
            entity_knowledge = []
        else:
            entity_knowledge = question.recognize_entities(ner, "mgenre_el")
        return entity_knowledge

def get_dbpedia_entities(question: Question):
        return question.recognize_entities("babelscape_ner" ,"mag_el")

# Function to prepare input
def prep_input(input_str, lang, linguistic_context, entity_knowledge, question_padding_length, entity_padding_length, kg):
    lang = Language(lang)
    question = Question(input_str, lang)
    question_string = question.question_string
    if linguistic_context:
        question_string = question.get_question_string_with_lingtuistic_context(question_padding_length)
    if entity_padding_length:
        if kg==Knowledge_graph.Wikidata:
            entity_knowledge = get_wikidata_entities(question)
        elif kg==Knowledge_graph.DBpedia:
            entity_knowledge = get_dbpedia_entities(question)
    question_string = question.add_entity_knowledge(question_string, entity_knowledge, entity_padding_length)
    return question_string

# Initiate the flask app
app = Flask(__name__)

@app.route('/fetch-sparql', methods=['POST'])
def convert_question_to_sparql():
    req_data = request.form
    logging.info('Query received for SPARQL generation: %s' % str(req_data))
    global model_attr_kwargs
    global sparql_model
    
    lang = req_data['lang']
    question_str = req_data['query']
    processed_question_string = prep_input(question_str, lang, **model_attr_kwargs)
    pred_sparql = sparql_model.predict_sparql(processed_question_string)
    query = Query(pred_sparql, model_attr_kwargs['kg'])
    
    logging.info('Generated SPARQL: %s' % str(query.sparql))
    
    return query.sparql

@app.route('/check-service', methods=['GET'])
def check_service():
    return 'Service is online.'


# Confguring model
parser = argparse.ArgumentParser(
    description="A program to use model to predict query and build qald dataset")

parser.add_argument("--model", type=str,
                    help="model path", required=True)
parser.add_argument("--knowledge_graph", type=str,
                    help="type of knowledge_graph", required=True)
parser.add_argument("--linguistic_context", action=argparse.BooleanOptionalAction,
                    help='With or without linguistic context in question string')
parser.add_argument("--entity_knowledge", action=argparse.BooleanOptionalAction,
                    help='With or without entity knowledge in question string')
parser.add_argument("--question_padding_length", type=int, 
                    help="length of question string and every linguistic context after padding. \
                    If not provided, no padding will be added.",
                    default=0)
parser.add_argument("--entity_padding_length", type=int,
                    help="length of entity knowledge after padding. \
                    If not provided, no padding will be added.",
                    default=0)

parser.add_argument("--port", type=int, default=8989, help="Port for the Flask app")

args = parser.parse_args()

# path to model
model_path = args.model

# Set global model attributes
# KG to use
knowledge_graph=args.knowledge_graph
# to extract & utilize linguistic information or not
model_attr_kwargs['linguistic_context'] = args.linguistic_context
# to extract & utilize entity knowledge or not
model_attr_kwargs['entity_knowledge'] = args.entity_knowledge
# Padding length for the question
model_attr_kwargs['question_padding_length'] = args.question_padding_length
# Padding length for the entity
model_attr_kwargs['entity_padding_length'] = args.entity_padding_length

model_attr_kwargs['kg'] = Knowledge_graph[knowledge_graph]

port = args.port

print('Input attributes are set, initializing model...')
# Initialize the model
sparql_model = Summarizer(model_path)
print('Model initialized, starting server...')

if __name__ == "__main__":
    # Run flask application
    app.run(host="0.0.0.0", port=port, threaded=True)
    