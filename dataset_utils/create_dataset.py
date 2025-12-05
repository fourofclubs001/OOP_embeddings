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

with open("dataset_utils/methods_register.json", 'r') as file:
        
    data = json.load(file)

    for method_definition in data:

        environment.define_method(
            method_definition[0], 
            method_definition[1], 
            method_definition[2], 
            method_definition[3], 
            method_definition[4]
        )

dataset_utils = DatasetUtils(environment)

with open("dataset_utils/use_case_register.json", 'r') as file:

    use_case_implementation = json.load(file)

    traces = dataset_utils.get_use_cases(use_case_implementation)

with open("traces.txt", "w") as file:

    print_traces(traces, file)