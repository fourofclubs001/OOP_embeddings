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
        self.environment.send_message("String", "new", ["first_key"], "main_dictionary_first_key")

    def send_message_create_identity_dictionary(self, trace, base_case):

        return self.environment.send_message(
            
            "main_dictionary", 
            "create_identity_dictionary", 
            ["main_dictionary_first_key"], 
            "main_dictionary", 
            trace, base_case
        )

    def test_can_get_trace(self):

        self.define_create_identity_dictionary()
        self.define_dictionary_instance_and_key()
        trace = self.send_message_create_identity_dictionary(trace=True, base_case=True)
        
        expected_trace = [

            ("Dictionary", ("Class", "new"), [], "dictionary"),
            ("dictionary", ("Dictionary", "set"), 
             ["main_dictionary_first_key", "main_dictionary_first_key"], 
             "dictionary"),
        ]

        self.assertListEqual(trace, expected_trace)

    def test_can_get_multilevel_trace(self):

        self.environment.define_method(
            "Dictionary", "create_identity_dictionary_with_reference", 
            ["reference_dictionary", "key_and_value_reference"],
            [("reference_dictionary", "get", ["key_and_value_reference"], "key_and_value"),
             ("dictionary", "create_identity_dictionary", ["key_and_value"], "dictionary")],
              "dictionary"
        )