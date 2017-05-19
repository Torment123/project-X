from modules.load_dataset.load_data import *


def test_load_dataset():
    data = load_dataset('datasets/', 'r_30')
    assert data.data_schema['datasetId'] == 'r_30_dataset'
