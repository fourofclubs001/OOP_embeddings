from mini_smalltalk.src.Environment import Environment
from dataset.dataset_utils import DatasetUtils

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

use_case_00_implementation = [
    ("String", "new", ["first_main_key"], "first_main_key"),
    ("String", "new", ["second_main_key"], "second_main_key"),
    ("String", "new", ["first_main_value"], "first_main_value"),
    ("String", "new", ["second_main_value"], "second_main_value"),
    ("Dictionary", "new", [], "main_dictionary"),
    ("main_dictionary", "set", ["first_main_key", "first_main_value"], "main_dictionary"),
    ("main_dictionary", "set", ["second_main_key", "second_main_value"], "main_dictionary"),
    ("main_dictionary", "get_two_values", ["first_main_key", "second_main_key"], "result_dictionary")
]
use_case_00_return = "result_dictionary"

environment.define_method(
    "UseCase", "use_case_00", [],
    use_case_00_implementation,
    use_case_00_return
)

environment.send_message("UseCase", "new", [], "use_case")
virtual_trace = environment.send_message("use_case", "use_case_00", [], "use_case_result",
                                 trace=True, base_case=True)

full_virtual_trace = initialization_trace + virtual_trace

print("Virtual Trace \n")

for line in full_virtual_trace:

    print(line)

print("")

dataset_utils = DatasetUtils(environment)

implementation_trace = dataset_utils.implementation_to_trace(use_case_00_implementation, use_case_00_return)

full_implementation_trace = initialization_trace + implementation_trace

print("Implementation trace \n")

for line in full_implementation_trace:

    print(line)