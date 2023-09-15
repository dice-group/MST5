from utils.data_io import read_json
from dataset.Qald import Qald

def update_qald_dataset(input_file_path, output_file_path, languages, kg):
    test_file = read_json(input_file_path)
    test_qald = Qald(test_file, kg)
    test_qald.update_answers()
    test_qald.export_qald_json(languages, output_file_path)