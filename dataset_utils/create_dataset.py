from mini_smalltalk.src.Environment import Environment
from dataset_utils.src.dataset_utils import DatasetUtils

def print_traces(traces):

    for idx, trace in enumerate(traces):

        print(f"Trace {idx} \n")

        for line in trace["implementation"]:

            print(line)

        print("")

        for line in trace["virtual"]:

            print(line)

        print("")

environment = Environment()

environment.define_method(
    "Dictionary", "get_two_values", 
    ["first_key", "second_key"],
    [
        ("self", "get", ["first_key"], "first_value"),
        ("self", "get", ["second_key"], "second_value"),
        ("Dictionary", "new", [], "dictionary"),
        ("dictionary", "set", ["first_key", "first_value"], "dictionary"),
        ("dictionary", "set", ["second_key", "second_value"], "dictionary")
    ], 
    "dictionary")

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

print_traces(traces)