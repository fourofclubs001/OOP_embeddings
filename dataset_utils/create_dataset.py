import json
from mini_smalltalk.src.Environment import Environment
from dataset_utils.src.dataset_utils import DatasetUtils

environment = Environment()

dataset_utils = DatasetUtils(environment)

dataset_utils.define_method_environment("dataset_utils/methods_register.json")

traces = dataset_utils.get_use_case_traces("dataset_utils/use_case_register.json")

dataset_utils.write_traces(traces, "dataset_utils/traces.txt")