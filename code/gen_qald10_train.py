import json

qald9plus_train_path = "../datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json"
qald9plus_test_path = "../datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json"

qald10_train_path = "../datasets/qald10/qald_9_plus_train_wikidata.json"

output_file = "../datasets/qald10/qald10_train.json"

# Load both qald 9 plus test and train
with open(qald9plus_train_path) as train_file, open(qald9plus_test_path) as test_file:
    qald9plus_train = json.load(train_file)
    qald9plus_test = json.load(test_file)
    qald_objects = [qald9plus_train, qald9plus_test]
# Map English question against Chinese, Japanese and Spanish translations
q_map = {}
lang_arr = ['zh', 'ja', 'es']
for qald_json in qald_objects:
    questions = qald_json['questions']
    for ques in questions:
        translations = []
        for q_pair in ques['question']:
            lang = q_pair['language']
            if lang  == 'en':
                cur_key = q_pair['string']
            elif lang in lang_arr:
                translations.append(q_pair)
        q_map[cur_key] = translations
# Load qald 10 train
with open(qald10_train_path) as train_file:
    qald10_train = json.load(train_file)
# for each question find and update translations
questions = qald10_train['questions']
for ques in questions:
    translations = []
    for q_pair in ques['question']:
        lang = q_pair['language']
        if lang  == 'en':
            translations = q_map[q_pair['string']]
            break
    ques['question'].extend(translations)
# export csv
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(qald10_train, f, ensure_ascii=False, indent=4)