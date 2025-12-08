import json
import os
from mini_smalltalk.src.Environment import Environment
from dataset_utils.src.dataset_utils import DatasetUtils

current_directory = os.path.abspath(os.path.abspath(__file__))
dataset_utils_absolute_path = os.path.abspath(os.path.join(current_directory, ".."))

environment = Environment()

dataset_utils = DatasetUtils(environment)

environment.send_message("Class", "new", [], "OperatorDictionary")

dataset_utils.define_method_environment(os.path.join(dataset_utils_absolute_path,"methods_register.json"))

traces = dataset_utils.get_use_case_traces(os.path.join(dataset_utils_absolute_path, "use_case_register.json"))

dataset_utils.write_traces(traces, os.path.join(dataset_utils_absolute_path, "traces.txt"))