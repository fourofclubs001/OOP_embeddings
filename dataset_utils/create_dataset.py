import json
from mini_smalltalk.src.Environment import Environment
from dataset_utils.src.dataset_utils import DatasetUtils

def print_traces(traces, file = None):

    for idx, trace in enumerate(traces):

        print(f"Trace {idx} \n", file=file)

        for line in trace["implementation"]:

            print(line, file=file)

        print("", file=file)

        for line in trace["virtual"]:

            print(line, file=file)

        print("", file=file)

environment = Environment()

dataset_utils = DatasetUtils(environment)

dataset_utils.define_method_environment("dataset_utils/methods_register.json")

traces = dataset_utils.get_use_case_traces()

with open("traces.txt", "w") as file:

    print_traces(traces, file)