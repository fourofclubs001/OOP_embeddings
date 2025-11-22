import unittest
from dataset.dataset_utils import DatasetUtils
from mini_smalltalk.src.Environment import Environment

class TestDatsetUtils(unittest.TestCase):

    def setUp(self):

        self.environment = Environment()
        self.dataset_utils = DatasetUtils(self.environment)

    def test_can_write_implementation_as_trace(self):

        self.environment.send_message("Class", "new", [], "UseCase")

        self.environment.define_method(
            "Dictionary", "get_two_values", 
            ["first_key", "second_key"],
            [
                ("self", "get", ["first_key"], "first_value"),
                ("self", "get", ["second_key"], "second_value"),
                ("Dictionary", "new", [], "dictionary"),
                ("dictionary", "set", ["first_key", "first_value"], "dictionary"),
                ("dictionary", "set", ["second_key", "second_value"], "dictionary")
            ], 
            "dictionary"
        )

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

        self.environment.define_method(
            "UseCase", "use_case_00", [],
            use_case_00_implementation,
            use_case_00_return
        )

        self.environment.send_message("UseCase", "new", [], "use_case")
        self.environment.send_message("use_case", "use_case_00", [], "use_case_result")

        trace = self.dataset_utils.implementation_to_trace(use_case_00_implementation, use_case_00_return)

        expected_trace = [
            (self.environment.objects["String"]["id"], ("Class", "new"), ["first_main_key"], self.environment.objects["first_main_key"]["id"]),
            (self.environment.objects["String"]["id"], ("Class", "new"), ["second_main_key"], self.environment.objects["second_main_key"]["id"]),
            (self.environment.objects["String"]["id"], ("Class", "new"), ["first_main_value"], self.environment.objects["first_main_value"]["id"]),
            (self.environment.objects["String"]["id"], ("Class", "new"), ["second_main_value"], self.environment.objects["second_main_value"]["id"]),
            (self.environment.objects["Dictionary"]["id"], ("Class", "new"), [], self.environment.objects["main_dictionary"]["id"]),
            (self.environment.objects["main_dictionary"]["id"], ("Dictionary", "set"), [self.environment.objects["first_main_key"]["id"], self.environment.objects["first_main_value"]["id"]], self.environment.objects["main_dictionary"]["id"]),
            (self.environment.objects["main_dictionary"]["id"], ("Dictionary", "set"), [self.environment.objects["second_main_key"]["id"], self.environment.objects["second_main_value"]["id"]], self.environment.objects["main_dictionary"]["id"]),
            (self.environment.objects["main_dictionary"]["id"], ("Dictionary", "get_two_values"), [self.environment.objects["first_main_key"]["id"], self.environment.objects["second_main_key"]["id"]], self.environment.objects["result_dictionary"]["id"]),
            self.environment.objects["result_dictionary"]["id"]
        ]

        self.assertEqual(trace, expected_trace)