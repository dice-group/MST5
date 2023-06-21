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
        self.ref_name = None
        self.ref_file = None
        self.experiment_id = None

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
        pred_file = Pred_file(name, file_path)
        self.pred_files[language] = pred_file

    def set_ref_data(self, name: str) -> dict:
        return {
            'name': name,
            'URI': '',
            'multiselect': 'DBpedia Entity INEX',
            'qlang': ''
        }

    def set_pred_data(self, name: str) -> dict:
        ref_file_name = self.ref_file.split('/')[-1]
        return {
            'name': name,
            'URI': '',
            'multiselect': f'AFDS_{ref_file_name}',
            'qlang': ''
        }

    def set_files(self, file_path: str) -> dict:
        file_content = open(file_path, 'rb').read()
        file_obj = io.BytesIO(file_content)
        return {
            'files[]': (file_path, file_obj, 'application/json'),
        }

    def upload_file(self, data, file):
        try:
            response = self.send_post_request_for_upload(data, file)
            response.raise_for_status()
            print(f"Upload {file} successfully")
            return True
        except requests.exceptions.HTTPError as error:
            print(f'Error: {error}')
            return False

    def send_post_request_for_upload(self, data, file):
        return requests.post(
                url='https://gerbil-qa.aksw.org/gerbil/file/upload',
                headers=UPLOAD_HEADERS,
                data=data,
                files=file
            )

    def upload_ref(self):
        data = self.set_ref_data(self.ref_name)
        file = self.set_files(self.ref_file)
        self.upload_file(data, file)

    def upload_pred(self):
        pred_file: Pred_file
        for pred_file in self.pred_files.values():
            data = self.set_pred_data(pred_file.name)
            file = self.set_files(pred_file.file_path)
            self.upload_file(data, file)

    def submit_experiment(self):
        self.upload_ref()
        self.upload_pred()
        experiment_data = self.set_experiment_data()
        execute_url = execute_url_prefix + experiment_data

        try:
            response = self.send_get_request(execute_url)
            response.raise_for_status()
            self.experiment_id = response.text
            print("GERBIL experiment is submitted successfully")
            print(f"Experiment id: {self.experiment_id}")
            return response
        except requests.exceptions.HTTPError as error:
            print(f'Error: {error}')

    def send_get_request(self, execute_url):
        return requests.get(execute_url, headers=SUBMIT_HEADERS)

    def set_experiment_data(self):
        ref_file_name = self.ref_file.split('/')[-1]
        answer_file_names = self.get_answer_file_names(ref_file_name)
        ref_dataset = [f'NIFDS_{self.ref_name}({ref_file_name})']

        experiment_data = {
            'type': 'QA',
            'matching': 'STRONG_ENTITY_MATCH',
            'annotator': [],
            'dataset': ref_dataset,
            'answerFiles': answer_file_names,
            'questionLanguage': 'en'
        }

        experiment_data_encoded = urllib.parse.quote(
            json.dumps(experiment_data))
        return experiment_data_encoded

    def export_results(self, output_file,  max_retry: int = 10):
        gerbil_html = self.get_experiment_results(max_retry)
        if gerbil_html:
            gerbil_results_table = self.clean_gerbil_table(gerbil_html)
            gerbil_results_table.to_csv(output_file, index=False)
            print("Experiment results is saved to " + output_file)
        else:
            print(f"Try later with {self.experiment_id}")

    def get_experiment_results(self, max_retry):
        if not self.experiment_id:
            print("Please add an experiment id or submit an experiment.")
            return
        experiment_url = experiment_url_prefix + self.experiment_id
        retry = 0

        while retry < max_retry:
            retry += 1
            try:
                response = self.send_get_request(experiment_url)
                content = response.text
                if self.is_error_in_experiment(content):
                    print(f"Experiment {id} could not be executed.")
                    return
                elif self.is_experiment_running(content):
                    print("The experiment is still running.")
                    time.sleep(30)
                else:
                    return content
            except requests.exceptions.RequestException as e:
                print('Error: ', e)
                time.sleep(30)
        print("Experiment " + id + " takes too much time.")

    def is_error_in_experiment(self, content):
        return "The annotator caused too many single errors." in content or "The dataset couldn't be loaded." in content

    def is_experiment_running(self, content):
        return "The experiment is still running." in content

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

    def get_answer_file_names(self, ref_file_name):
        answer_files = []
        for lang, pred_file in self.pred_files.items():
            file_name = pred_file.file_path.split('/')[-1]
            answer_files.append(
                f"AF_{pred_file.name}({file_name})(undefined)(AFDS_{ref_file_name})"
            )

        return answer_files

    def clean_gerbil_table(self, html: str) -> str:
        html = self.rename_unnamed_column_to_benchmark(html)
        if "Benchmark" in html.columns:
            html = self.select_where_benckmark_is_na(html)
        for index, row in html.iterrows():
            language = row["Annotator"][-13:-11]
            html.at[index, "Language"] = language
        html = self.drop_unnecessary_columns(html)
        return html

    def drop_unnecessary_columns(self, html):
        columns_to_drop = [
            'Dataset',
            'Annotator',
            'Error Count',
            'avg millis/doc',
            'Timestamp',
            'GERBIL version',
            'Benchmark'
        ]
        for column_name in columns_to_drop:
            html = self.drop_column_by_name(html, column_name)
        return html

    def drop_column_by_name(self, df, column_name):
        try:
            return df.drop(column_name, axis=1)
        except:
            return df

    def select_where_benckmark_is_na(self, html):
        return html[html['Benchmark'].isna()]

class Pred_file:
    def __init__(self, name: str, file_path: str) -> None:
        self.name = name
        self.file_path = file_path
    
