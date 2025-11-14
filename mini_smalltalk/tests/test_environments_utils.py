import unittest
from src.Environment import *

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

    def define_create_identity_dictionary(self):

        self.environment.define_method(
            "Dictionary", "create_identity_dictionary", ["key_and_value"],
            [("Dictionary", "new", [], "dictionary"),
             ("dictionary", "set", ["key_and_value", "key_and_value"], "dictionary")],
              "dictionary"
        )

    def define_dictionary_instance_and_key(self):

        self.environment.send_message("Dictionary", "new", [], "main_dictionary")
        self.environment.send_message("String", "new", ["key"], "main_key")

    def send_message_create_identity_dictionary(self, trace, base_case):

        return self.environment.send_message(
            
            "main_dictionary", 
            "create_identity_dictionary", 
            ["main_key"], 
            "main_dictionary", 
            trace, base_case
        )

    def test_can_get_trace(self):

        self.define_create_identity_dictionary()
        self.define_dictionary_instance_and_key()
        trace = self.send_message_create_identity_dictionary(trace=True, base_case=True)
        
        expected_trace = [

            (
                self.environment.objects["Dictionary"]["id"], 
                ("Class", "new"), 
                [], 
                self.environment.objects["dictionary"]["id"]
            ),
            (
                self.environment.objects["dictionary"]["id"], 
                ("Dictionary", "set"), 
                [
                    self.environment.objects["main_key"]["id"], 
                    self.environment.objects["main_key"]["id"]
                ], 
                self.environment.objects["dictionary"]["id"]
            ),
            self.environment.objects["dictionary"]["id"]
        ]

        self.assertListEqual(trace, expected_trace)

    def test_can_get_multilevel_trace(self):

        self.environment.define_method(
            "Dictionary", "create_identity_dictionary", ["key_and_value"],
            [("Dictionary", "new", [], "dictionary"),
             ("dictionary", "set", ["key_and_value", "key_and_value"], "dictionary")],
              "dictionary"
        )

        self.environment.define_method(
            "Dictionary", "create_identity_dictionary_with_reference", 
            ["reference_dictionary", "key_and_value_reference"],
            [("reference_dictionary", "get", ["key_and_value_reference"], "key_and_value"),
             ("reference_dictionary", "create_identity_dictionary", ["key_and_value"], "dictionary")],
              "dictionary"
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
            trace=True, base_case=True
        )

        # Secuential Execution
        expected_trace = [

            (
                self.environment.objects["reference_dictionary"]["id"], 
                ("Dictionary", "get"), 
                [self.environment.objects["reference_key"]["id"]],
                self.environment.objects["main_key"]["id"]    
            ),
            (
                self.environment.objects["Dictionary"]["id"],
                ("Class", "new"),
                [],
                self.environment.objects["dictionary"]["id"]
            ),
            (
                self.environment.objects["dictionary"]["id"],
                ("Dictionary", "set"),
                [
                    self.environment.objects["main_key"]["id"],
                    self.environment.objects["main_key"]["id"]
                ],
                self.environment.objects["dictionary"]["id"]
            ),
            self.environment.objects["dictionary"]["id"]
        ]
        
        self.assertListEqual(trace, expected_trace)