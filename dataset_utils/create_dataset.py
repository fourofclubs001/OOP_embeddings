import json
from mini_smalltalk.src.Environment import Environment
from dataset_utils.src.dataset_utils import DatasetUtils

environment = Environment()

dataset_utils = DatasetUtils(environment)

dataset_utils.define_method_environment("dataset_utils/methods_register.json")

def define_dictionary_equivalent():
    environment.send_message("Class", "new", [], "OperatorDictionary")
    environment.define_method("OperatorDictionary", "obtain",["key", "dictionary"],[
        ("String", "new", ["name"], "name"),
        ("dictionary", "get", ["key"], "result"),
        ("String", "new", ["text"], "text")
    ], "result")
    environment.define_method("OperatorDictionary", "impose", ["key", "value", "dictionary"], [
        ("dictionary", "set", ["key", "value"], "result"),
        ("dictionary", "get", ["key"], "saved_value"),
        ("String", "new", ["text"], "text")
    ], "result")

    use_case_additional_implementations = [
        [
            ("Dictionary", "new", [], "main_dictionary"),
            ("OperatorDictionary", "new", [], "operator_dictionary"),
            ("String", "new", ["first_main_key"], "first_main_key"),
            ("String", "new", ["first_main_value"], "first_main_value"),
            ("operator_dictionary", "impose", ["first_main_key", "first_main_value", "main_dictionary"], "main_dictionary"),
            "main_dictionary"
         ],
        [
            ("Dictionary", "new", [], "main_dictionary"),
            ("OperatorDictionary", "new", [], "operator_dictionary"),
            ("String", "new", ["first_main_key"], "first_main_key"),
            ("String", "new", ["first_main_value"], "first_main_value"),
            ("operator_dictionary", "impose", ["first_main_key", "first_main_value", "main_dictionary"], "main_dictionary"),
            ("operator_dictionary" , "obtain", ["first_main_key", "main_dictionary"], "result"),
            "result"
        ],
        [
            ("Dictionary", "new", [], "main_dictionary"),
            ("OperatorDictionary", "new", [], "operator_dictionary"),
            ("String", "new", ["first_main_key"], "first_main_key"),
            ("String", "new", ["first_main_value"], "first_main_value"),
            ("String", "new", ["second_main_value"], "second_main_value"),
            ("operator_dictionary", "impose", ["first_main_key", "first_main_value", "main_dictionary"], "main_dictionary"),
            ("operator_dictionary", "impose", ["first_main_key", "second_main_value", "main_dictionary"], "main_dictionary"),
            ("operator_dictionary", "obtain", ["first_main_key", "main_dictionary"], "result"),
            "result"
        ]
    ]
    return use_case_additional_implementations


traces = dataset_utils.get_use_case_traces("dataset_utils/use_case_register.json")

dataset_utils.write_traces(traces, "dataset_utils/traces.txt")