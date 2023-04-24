import csv
import json

def export_csv(output_file, dataset):
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows(dataset)
    f.close()


def export_json(output_file, dataset):
    with open(output_file, 'w') as f:
        json.dump(dataset, f)
    print("json file saved to ", output_file)