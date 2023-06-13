import csv
import json
import os


def read_json(json_file):
    with open(json_file) as f:
        return json.load(f)


def export_csv(output_file, dataset):
    check_and_makedir_if_not_exist(output_file)
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows(dataset)
    f.close()
    print("csv file is exported to ", output_file)


def export_json(output_file, dataset):
    check_and_makedir_if_not_exist(output_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False)
    print("json file is exported to ", output_file)


def check_and_makedir_if_not_exist(output_file):
    dir_path = os.path.dirname(output_file)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
