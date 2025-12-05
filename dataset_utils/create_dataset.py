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

use_case_implementation = [
    [
        ("String", "new", ["first_main_key"], "first_main_key"),
        ("String", "new", ["second_main_key"], "second_main_key"),
        ("String", "new", ["first_main_value"], "first_main_value"),
        ("String", "new", ["second_main_value"], "second_main_value"),
        ("Dictionary", "new", [], "main_dictionary"),
        ("main_dictionary", "set", ["first_main_key", "first_main_value"], "main_dictionary"),
        ("main_dictionary", "set", ["second_main_key", "second_main_value"], "main_dictionary"),
        ("main_dictionary", "get_two_values", ["first_main_key", "second_main_key"], "result_dictionary"),
        "result_dictionary"
    ],
    [
        ("String", "new", ["first_main_key"], "first_main_key"),
        ("String", "new", ["second_main_key"], "second_main_key"),
        ("String", "new", ["third_main_key"], "third_main_key"),
        ("String", "new", ["first_main_value"], "first_main_value"),
        ("String", "new", ["second_main_value"], "second_main_value"),
        ("String", "new", ["third_main_value"], "third_main_value"),
        ("Dictionary", "new", [], "main_dictionary"),
        ("main_dictionary", "set", ["first_main_key", "first_main_value"], "main_dictionary"),
        ("main_dictionary", "set", ["second_main_key", "second_main_value"], "main_dictionary"),
        ("main_dictionary", "set", ["third_main_key", "third_main_value"], "main_dictionary"),
        ("main_dictionary", "get_two_values", ["first_main_key", "second_main_key"], "result_dictionary"),
        "result_dictionary"
    ],
    [
        ("String", "new", ["first_main_key"], "first_main_key"),
        ("String", "new", ["second_main_key"], "second_main_key"),
        ("String", "new", ["third_main_key"], "third_main_key"),
        ("String", "new", ["first_main_value"], "first_main_value"),
        ("String", "new", ["second_main_value"], "second_main_value"),
        ("String", "new", ["third_main_value"], "third_main_value"),
        ("Dictionary", "new", [], "main_dictionary"),
        ("main_dictionary", "set", ["first_main_key", "first_main_value"], "main_dictionary"),
        ("main_dictionary", "set", ["second_main_key", "second_main_value"], "main_dictionary"),
        ("main_dictionary", "set", ["third_main_key", "third_main_value"], "main_dictionary"),
        ("main_dictionary", "get_two_values", ["first_main_key", "third_main_key"], "result_dictionary"),
        "result_dictionary"
    ]
]

dataset_utils = DatasetUtils(environment)

traces = dataset_utils.get_use_cases(use_case_implementation)

with open("traces.txt", "w") as file:

    print_traces(traces, file)