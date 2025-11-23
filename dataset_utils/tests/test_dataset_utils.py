import unittest
from dataset_utils.src.dataset_utils import DatasetUtils
from mini_smalltalk.src.Environment import Environment

class TestDatsetUtils(unittest.TestCase):

    def init_environment(self):

        self.environment = Environment()

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

    def setUp(self):

        self.init_environment()

        self.dataset_utils = DatasetUtils(self.environment)

    def test_can_write_implementation_as_trace(self):

        self.environment.send_message("Class", "new", [], "UseCase")

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

    def test_can_write_use_case_pair_on_dictionary(self):

        implementations = [
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
            ]
        ]

        traces_pairs = self.dataset_utils.get_use_cases(implementations)

        expected_implementation_trace = self.dataset_utils.implementation_to_trace(implementations[0][:-1], 
                                                                                   implementations[0][-1])

        self.init_environment()
        
        self.environment.send_message("Class", "new", [], "UseCase")

        self.environment.define_method(
            "UseCase", "use_case_selector", [], 
            implementations[0][:-1], implementations[0][-1]
        )

        self.environment.send_message("UseCase", "new", [], "use_case")

        expected_virtual_trace = self.environment.send_message("use_case", "use_case_selector", [], "", trace=True, base_case=True)

        self.assertEqual(traces_pairs[0]["implementation"], expected_implementation_trace)
        self.assertEqual(traces_pairs[0]["virtual"], expected_virtual_trace)