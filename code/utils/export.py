import csv
import json
import os

def export_csv(output_file, dataset):
    dir_path = os.path.dirname(output_file)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows(dataset)
    f.close()
    print("csv file is exported to ", output_file)
    

def export_json(output_file, dataset):
    dir_path = os.path.dirname(output_file)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(output_file, 'w') as f:
        json.dump(dataset, f)
    print("json file is exported to ", output_file)
