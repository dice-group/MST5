import csv
import json

def export_csv(output_file, dataset):
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows(dataset)
    f.close()
    print("csv file is saved to ", output_file)
    


def export_json(output_file, dataset):
    with open(output_file, 'w') as f:
        json.dump(dataset, f)
    f.close()
    print("json file is saved to ", output_file)