from pandas.io.sas.sasreader import FilePath
import requests
import io
import json
import urllib.parse
import urllib.request
import pandas as pd
import time

UPLOAD_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cookie': 'JSESSIONID=265042E6F0ECFC6AEEA55C409FB7168F',
    'Origin': 'https://gerbil-qa.aksw.org',
    'Referer': 'https://gerbil-qa.aksw.org/gerbil/config',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

SUBMIT_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=265042E6F0ECFC6AEEA55C409FB7168F',
    'Referer': 'https://gerbil-qa.aksw.org/gerbil/config',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

experiment_url_prefix = "https://gerbil-qa.aksw.org/gerbil/experiment?id="
execute_url_prefix = "https://gerbil-qa.aksw.org/gerbil/execute?experimentData="


class Gerbil:
    def __init__(self) -> None:
        self.pred_files = {}

    def add_experiment_id(self, experiment_id):
        self.experiment_id = experiment_id

    def add_ref_file(self, name, file_path, replace=False):
        if (self.ref_name or self.ref_file) and not replace:
            print("Reference file already exists")
        self.ref_name = name
        self.ref_file = file_path

    def add_pred_file(self, name, file_path, language, replace=False):
        if language in self.pred_files and not replace:
            print("Prediction file already exists")
        self.pred_files[language] = [name, file_path]

    def set_ref_data(self, name: str) -> dict:
        return {
            'name': name,
            'multiselect': 'DBpedia Entity INEX',
            'qlang': '',
        }

    def set_pred_data(self, name: str, pred_file: str) -> dict:
        return {
            'name': name,
            'multiselect': 'AFDS_'+pred_file,
            'qlang': '',
        }

    def set_files(self, file_path: str) -> dict:
        file_content = open(file_path, 'rb').read()
        file_obj = io.BytesIO(file_content)
        return {
            'files[]': (file_path, file_obj),
        }

    def upload_file(self, data, file):
        try:
            response = requests.post(
                url='https://gerbil-qa.aksw.org/gerbil/file/upload',
                headers=UPLOAD_HEADERS,
                data=data,
                files=file
            )
            response.raise_for_status()
            print(f"Upload {file} successfully")
            return True
        except requests.exceptions.HTTPError as error:
            print(f'Error: {error}')
            return False

    def upload_ref(self):
        data = self.set_ref_data(self.ref_name)
        file = self.set_files(self.ref_file)
        self.upload_file(data, file)

    def upload_pred(self):
        for lang, [name, file_path] in self.pred_files.items():
            data = self.set_pred_data(name, f"{lang}.json")
            file = self.set_files(file_path)
        self.upload_file(data, file)

    def submit_experiment(self):
        self.upload_ref()
        self.upload_pred()
        experiment_data = self.set_experiment_data()
        execute_url = execute_url_prefix + experiment_data

        try:
            response = requests.get(execute_url, headers=SUBMIT_HEADERS)
            response.raise_for_status()
            print("GERBIL experiment is submitted successfully")
            return response
        except requests.exceptions.HTTPError as error:
            print(f'Error: {error}')

    def set_experiment_data(self):
        ref_name, ref_file = self.get_ref_name_and_file(ref)

        answer_file_names = self.get_answer_file_names(pred, ref_file)

        dataset_name = ['NIFDS_'+ref_name+'('+ref_file+')']
        ref_dataset = [f'NIFDS_{self.ref}()']

        experiment_data = {
            'type': 'QA',
            'matching': 'STRONG_ENTITY_MATCH',
            'annotator': [],
            'dataset': dataset_name,
            'answerFiles': answer_file_names,
            'questionLanguage': 'en'
        }

        experiment_data_encoded = urllib.parse.quote(
            json.dumps(experiment_data))
        return experiment_data_encoded

    def export_experiment_results(self, max_retry: int = 10):
        if not self.experiment_id:
            print("Please add an experiment id or submit an experiment.")
            return
        experiment_url = experiment_url_prefix + self.experiment_id
        retry = 0

        while retry < max_retry:
            retry += 1
            try:
                response = requests.get(experiment_url)
                content = response.text
                if "The annotator caused too many single errors." in content:
                    print(f"Experiment {id} could not be executed.")
                    return
                elif "The experiment is still running." in content:
                    print("The experiment is still running.")
                    time.sleep(30)
                else:
                    return content
            except requests.exceptions.RequestException as e:
                print('Error: ', e)
                time.sleep(30)
        print("Experiment " + id + " takes too much time.")

    def clean_gerbil_table(self, html: str) -> str:
        html = self.rename_unnamed_column_to_benchmark(html)
        if "Benchmark" in html.columns:
            html = self.select_where_benckmark_is_na(html)
            html = self.drop_benckmark_column(html)
        for index, row in html.iterrows():
            language = row["Annotator"][-13:-11]
            html.at[index, "Language"] = language
        html = self.drop_unnecessary_columns(html)
        return html

    def drop_unnecessary_columns(self, html):
        return html.drop(
            columns=[
                'Dataset',
                'Annotator',
                'Error Count',
                'avg millis/doc',
                'Timestamp',
                'GERBIL version',
            ]
        )

    def select_where_benckmark_is_na(self, html):
        return html[html['Benchmark'].isna()]

    def drop_benckmark_column(self, html):
        return html.drop(
            columns=["Benchmark"]
        )

    def rename_unnamed_column_to_benchmark(self, html):
        html = pd.read_html(html)[0].rename(columns={
            "Unnamed: 3": "Benchmark",
        })

        return html

    def get_ref_name_and_file(self, ref):
        for name in ref:
            ref_name = name
            ref_file_name = ref[name]
        return ref_name, ref_file_name

    def get_answer_file_names(self, pred, ref_file_name):
        answer_files = []
        for name in pred:
            answer_files.append(
                f'AF_{name}({pred[name]}))(undefined)(AFDS_{ref_file_name})'
                )

        return answer_files


def upload_pred_by_lang(exp_setting: str, pred_pfad_prefix: str, languages: str):
    for lang in languages:
        pred_file_path = pred_pfad_prefix + lang + ".json"
        upload_file(exp_setting+lang, pred_file_path, "pred")


def submit_experiment(ref: dict, pred: dict) -> requests.Response:
    ref_name, ref_file = get_ref_name_and_file(ref)

    answer_file_names = get_answer_file_names(pred, ref_file)

    dataset_name = ['NIFDS_'+ref_name+'('+ref_file+')']

    experiment_data = {
        'type': 'QA',
        'matching': 'STRONG_ENTITY_MATCH',
        'annotator': [],
        'dataset': dataset_name,
        'answerFiles': answer_file_names,
        'questionLanguage': 'en'
    }

    experiment_data_encoded = urllib.parse.quote(json.dumps(experiment_data))

    execute_url = f'https://gerbil-qa.aksw.org/gerbil/execute?experimentData={experiment_data_encoded}'

    try:
        response = requests.get(execute_url, headers=SUBMIT_HEADERS)
        response.raise_for_status()
        print("GERBIL experiment is submitted successfully")
        return response
    except requests.exceptions.HTTPError as error:
        print(f'Error: {error}')


def get_exp_result_content(id: str, max_retry: int = 10) -> str:
    experiment_url = "https://gerbil-qa.aksw.org/gerbil/experiment?id=" + id
    retry = 0

    while retry < max_retry:
        retry += 1
        try:
            response = requests.get(experiment_url)
            content = response.text
            if "The annotator caused too many single errors." in content:
                print(f"Experiment {id} could not be executed.")
                return
            elif "The experiment is still running." in content:
                print("The experiment is still running.")
                time.sleep(30)
            else:
                return content
        except requests.exceptions.RequestException as e:
            print('Error: ', e)
            time.sleep(30)
    print("Experiment " + id + " takes too much time.")
