import unittest
from mini_smalltalk.src.Environment import *

class EnvironmentUtilsTest(unittest.TestCase):

    def setUp(self):

        self.environment = Environment()
        self.environment.send_message("Class", "new", [], "Lista")
        
    def test_can_get_every_class(self):
        
        classes = self.environment.get_classes()
        
        expected_classes = set(["Object", "Class", "String", "Dictionary", "Lista"])
        
        self.assertSetEqual(expected_classes, classes)
        
    def test_can_get_every_class_method_pair(self):
        
        class_method_pairs = self.environment.get_class_method_pairs()

        expected_pairs = []
            
        expected_pairs.append(("Class", "name"))
        expected_pairs.append(("Class", "new"))
        expected_pairs.append(("Class", "super"))
        
        expected_pairs.append(("Class", "class"))        
        expected_pairs.append(("Dictionary", "class"))
        expected_pairs.append(("String", "class"))
        expected_pairs.append(("Lista", "class"))
        
        expected_pairs.append(("Dictionary", "set"))
        expected_pairs.append(("Dictionary", "get"))
        expected_pairs.append(("String", "value"))
        
        self.assertSetEqual(set(expected_pairs), set(class_method_pairs))

    def test_can_get_trace(self):

        self.environment.define_method(
            "Dictionary", "create_identity_dictionary", ["key_and_value"],
            [("self", "set", ["key_and_value", "key_and_value"], "self")],
              "self"
        )

        self.environment.send_message("Dictionary", "new", [], "main_dictionary")
        self.environment.send_message("String", "new", ["key"], "main_key")

        trace = self.environment.send_message(
            
            "main_dictionary", 
            "create_identity_dictionary", 
            ["main_key"], 
            "main_dictionary", 
            trace = True, base_case = True
        )
        
        expected_trace = [

            (
                self.environment.objects["main_dictionary"]["id"], 
                ("Dictionary", "set"), 
                [
                    self.environment.objects["main_key"]["id"], 
                    self.environment.objects["main_key"]["id"]
                ], 
                self.environment.objects["main_dictionary"]["id"]
            ),
            self.environment.objects["main_dictionary"]["id"]
        ]

        self.assertListEqual(trace, expected_trace)

    def test_can_get_multilevel_trace(self):

        self.environment.define_method(
            "Dictionary", "create_identity_dictionary", ["key_and_value"],
            [("self", "set", ["key_and_value", "key_and_value"], "self")],
              "self"
        )

        self.environment.define_method(
            "Dictionary", "create_identity_dictionary_with_reference", 
            ["reference_dictionary", "key_and_value_reference"],
            [("reference_dictionary", "get", ["key_and_value_reference"], "key_and_value"),
             ("self", "create_identity_dictionary", ["key_and_value"], "self")],
              "self"
        )

        self.environment.send_message("Dictionary", "new", [], "main_dictionary")
        self.environment.send_message("String", "new", ["main_key"], "main_key")
        self.environment.send_message("Dictionary", "new", [], "reference_dictionary_")
        self.environment.send_message("String", "new", [""], "reference_key")

        self.environment.send_message(
            "reference_dictionary_", "set", 
            ["reference_key", "main_key"], "reference_dictionary_"
        )

        trace = self.environment.send_message(
            "main_dictionary", "create_identity_dictionary_with_reference",
            ["reference_dictionary_", "reference_key"], "main_dictionary",
            trace = True, base_case = True
        )

        # Secuential Execution
        expected_trace = [

            (
                self.environment.objects["reference_dictionary_"]["id"], 
                ("Dictionary", "get"), 
                [self.environment.objects["reference_key"]["id"]],
                self.environment.objects["main_key"]["id"]    
            ),
            (
                self.environment.objects["main_dictionary"]["id"],
                ("Dictionary", "set"),
                [
                    self.environment.objects["main_key"]["id"],
                    self.environment.objects["main_key"]["id"]
                ],
                self.environment.objects["main_dictionary"]["id"]
            ),
            self.environment.objects["main_dictionary"]["id"]
        ]
        
        self.assertListEqual(trace, expected_trace)

    def test_can_trace_with_string_new_method(self):

        self.environment.define_method("Dictionary", "create_identity_dictionary", ["key_and_value"],
                                [("self", "set", ["key_and_value", "key_and_value"], "self")],
                                "self")

        self.environment.define_method(
                    "Dictionary", "create_identity_dictionary_with_reference", 
                    ["reference_dictionary", "key_and_value_reference"],
                    [("reference_dictionary", "get", ["key_and_value_reference"], "key_and_value_value"),
                    ("self", "create_identity_dictionary", ["key_and_value_value"], "self")],
                    "self"
                )

        self.environment.send_message("Class", "new", [], "UseCase")
        self.environment.define_method(
            
            "UseCase", "use_case_00", [],
            [
                ("Dictionary", "new", [], "main_dictionary"),
                ("String", "new", ["first_key"], "main_dictionary_key"),
                ("Dictionary", "new", [], "reference_dictionary"),
                ("String", "new", [""], "reference_dictionary_key"),
                ("reference_dictionary", "set", 
                ["reference_dictionary_key", "main_dictionary_key"], 
                "reference_dictionary"),
                ("main_dictionary", "create_identity_dictionary_with_reference",
                ["reference_dictionary", "reference_dictionary_key"], "main_dictionary")
            ],
            "main_dictionary"
        )

        self.environment.send_message("UseCase", "new", [], "use_case")

        trace = self.environment.send_message("use_case", "use_case_00", [], "use_case_result", trace=True, base_case=True)

        expected_trace = [
            (5, ('Class', 'new'), [], 14),
            (3, ('Class', 'new'), ['first_key'], 16),
            (5, ('Class', 'new'), [], 17),
            (3, ('Class', 'new'), [''], 19),
            (17, ('Dictionary', 'set'), [19, 16], 17),
            (17, ('Dictionary', 'get'), [19], 16),
            (14, ('Dictionary', 'set'), [16, 16], 14),
            14
        ]

        self.assertEqual(trace, expected_trace)