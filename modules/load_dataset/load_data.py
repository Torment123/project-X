import pandas as pd
import tarfile
import json
import zlib
from io import StringIO

# In order to load a dataset, you need to locate it into keras\docker\datasets\
# The you could be able to load it in the way of datasets.load("dataset")
# e.g data = datasets.load("r_30")


class Dataset:
    def __init__(self, name, data_schema, data_description, test_data,
                 train_data, train_targets):
        self.name = name
        self.data_schema = data_schema
        self.data_description = data_description
        self.test_data = test_data
        self.train_data = train_data
        self.train_targets = train_targets


class ProblemInfo:
    def __init__(self, name, problem_description, problem_schema):
        self.name = name
        self.problem_description = problem_description
        self.problem_schema = problem_schema


class Primitive:
    def __init__(self, path):
        pass

    def get_function(self):
        pass

    def get_code(self):
        pass


def load_dataset(path, name):
    """This function loads from a dataset file into a instance of Dataset.
    
    Args:
        path: The path to the file. File name should not be included.
        name: The file name. Extension should not be included.
    
    Returns:
        An instance of Dataset.
    """
    extension = '.tar.gz'

    tar = tarfile.open(path + name + extension, 'r:gz')
    files = tar.getmembers()

    data_schema = tar.extractfile(name + '/data/dataSchema.json').read()
    data_schema = data_schema.decode("utf-8")
    data_schema = json.loads(data_schema)

    data_description = tar.extractfile(name + '/data/dataDescription.txt').read()
    data_description = data_description.decode("utf-8")

    test_data = tar.extractfile(name + '/data/testData.csv.gz')
    test_data = test_data.read()
    test_data = zlib.decompress(bytes(test_data), 15 + 32).decode("utf-8")
    test_data = StringIO(test_data)
    test_data = pd.read_csv(test_data)

    train_data = tar.extractfile(name + '/data/trainData.csv.gz')
    train_data = train_data.read()
    train_data = zlib.decompress(bytes(train_data), 15 + 32).decode("utf-8")
    train_data = StringIO(train_data)
    train_data = pd.read_csv(train_data)

    train_targets = tar.extractfile(name + '/data/trainTargets.csv.gz')
    train_targets = train_targets.read()
    train_targets = zlib.decompress(bytes(train_targets), 15 + 32).decode("utf-8")
    train_targets = StringIO(train_targets)
    train_targets = pd.read_csv(train_targets)

    tar.close()
    return Dataset(name, data_schema, data_description, test_data,
                   train_data, train_targets)


def load_problem_info(path, name):
    extension = '.tar.gz'

    tar = tarfile.open(path + name + extension, 'r:gz')

    problem_description = tar.extractfile(name + '/problemDescription.txt').read()
    problem_description = problem_description.decode("utf-8")

    problem_schema = tar.extractfile(name + '/problemSchema.json').read()
    problem_schema = problem_schema.decode("utf-8")
    problem_schema = json.loads(problem_schema)

    tar.close()
    return ProblemInfo(name, problem_description, problem_schema)

# data = load_dataset('r_30')
# problem_info = load_problem_info('r_30')
