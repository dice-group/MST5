import requests
import io
import json
import urllib.parse
import urllib.request
import pandas as pd
import time


def upload_file(name: str, file_path: str, source: str) -> bool:
    if source == "ref":
        data = set_ref_data(name)
    elif source == "pred":
        data = set_pred_data(name, file_path.split("/")[-1])
    else:
        print("Error in create headers")
        return False

    files = set_files(file_path)

    # set headers
    headers = {
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

    try:
        response = requests.post(
            url='https://gerbil-qa.aksw.org/gerbil/file/upload',
            headers=headers,
            data=data,
            files=files
        )
        response.raise_for_status()
        print(f"Upload {file_path} successfully")
        return True
    except requests.exceptions.HTTPError as error:
        print(f'Error: {error}')
        return False


def set_files(file_path: str) -> dict:
    file_content = open(file_path, 'rb').read()
    file_obj = io.BytesIO(file_content)
    return {
        'files[]': (file_path, file_obj),
    }


def set_ref_data(name: str) -> dict:
    return {
        'name': name,
        'multiselect': 'DBpedia Entity INEX',
        'qlang': '',
    }


def set_pred_data(name: str, pred_file: str) -> dict:
    return {
        'name': name,
        'multiselect': 'AFDS_'+pred_file,
        'qlang': '',
    }


def upload_pred_by_lang(exp_setting: str, pred_pfad_prefix: str, languages: str):
    for lang in languages:
        pred_file_path = pred_pfad_prefix + lang + ".json"
        upload_file(exp_setting+lang, pred_file_path, "pred")


def submit_experiment(ref: dict, pred: dict) -> requests.Response:
    headers = {
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

    for key in ref:
        ref_name = key
        ref_file = ref[key]

    answer_files = []
    for key in pred:
        answer_files.append(
            'AF_'+key+'('+pred[key]+')(undefined)(AFDS_'+ref_file+')')

    experiment_data = {
        'type': 'QA',
        'matching': 'STRONG_ENTITY_MATCH',
        'annotator': [],
        'dataset': ['NIFDS_'+ref_name+'('+ref_file+')'],
        'answerFiles': answer_files,
        'questionLanguage': 'en'
    }

    experiment_data_encoded = urllib.parse.quote(json.dumps(experiment_data))

    execute_url = f'https://gerbil-qa.aksw.org/gerbil/execute?experimentData={experiment_data_encoded}'

    try:
        response = requests.get(execute_url, headers=headers)
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


def clean_gerbil_table(html: str) -> str:
    html = pd.read_html(html)[0].rename(columns={
        "Unnamed: 3": "Benchmark",
    })
    if "Benchmark" in html.columns:
        html = html[html['Benchmark'].isna()]
        html = html.drop(
            columns=["Benchmark"]
        )
    for index, row in html.iterrows():
        html.at[index, "Language"] = row["Annotator"][-13:-11]
    html = html.drop(
        columns=[
            'Dataset',
            'Annotator',
            'Error Count',
            'avg millis/doc',
            'Timestamp',
            'GERBIL version',
        ]
    )
    return html
