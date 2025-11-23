from mini_smalltalk.src.Environment import Environment
from dataset.src.dataset_utils import DatasetUtils

environment = Environment()

initialization_trace = [
    (
        environment.objects["Class"]["id"], 
        ("Class", "new"), 
        [],
        environment.objects["Class"]["id"]    
    ),
    (
        environment.objects["Class"]["id"], 
        ("Class", "new"), 
        [],
        environment.objects["String"]["id"]    
    ),
    (
        environment.objects["Class"]["id"], 
        ("Class", "new"), 
        [],
        environment.objects["Dictionary"]["id"]    
    )
]

environment.send_message("Class", "new", [], "UseCase")

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
    ("String", "new", ["first_main_key"], "first_main_key"),
    ("String", "new", ["second_main_key"], "second_main_key"),
    ("String", "new", ["first_main_value"], "first_main_value"),
    ("String", "new", ["second_main_value"], "second_main_value"),
    ("Dictionary", "new", [], "main_dictionary"),
    ("main_dictionary", "set", ["first_main_key", "first_main_value"], "main_dictionary"),
    ("main_dictionary", "set", ["second_main_key", "second_main_value"], "main_dictionary"),
    ("main_dictionary", "get_two_values", ["first_main_key", "second_main_key"], "result_dictionary"),
    "result_dictionary"
]

dataset_utils = DatasetUtils(environment)

traces = dataset_utils.get_use_cases([use_case_implementation])

implementation_trace = traces[0]["implementation"]
virtual_trace = traces[0]["virtual"]

for line in implementation_trace:

    print(line)

print("")

for line in virtual_trace:

    print(line)