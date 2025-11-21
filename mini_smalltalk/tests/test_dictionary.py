from src.Environment import Environment
import unittest

class DictiornayTest(unittest.TestCase):
    
    def setUp(self):
        
        self.environment = Environment()
        self.environment.define_method("Dictionary", "add_twice", ["key1", "key2", "value"], [
            ("self", "set", ["key1", "value"], "tmp"),
            ("self", "set", ["key2", "value"], "tmp")
        ],"self")

        self.environment.define_method("Dictionary", "add_thrice", ["key1", "key2", "key3", "value"],[
            ("self", "set", ["key1", "value"], "tmp"),
            ("self", "set", ["key2", "value"], "tmp"),
            ("self", "set", ["key3", "value"], "tmp")
        ], "self")

        self.environment.define_method("Dictionary", "is_element_in_dict_equal", ["key", "object"], [
            ("self", "get", ["key"], "value_of_key"),
            ("value_of_key", "==", ["object"], "val")
        ], "val")

        self.environment.define_method("Dictionary", "add_with_depth_one", ["key", "object"], [
            ("Dictionary", "new", [], "dict"),
            ("dict", "set", ["key", "object"], "dict"),
            ("String", "new", ["first"], "str"),
            ("self", "set", ["str", "dict"], "tmp")
        ],"dict")
    
    def test_can_add_key(self):
        
        self.environment.send_message("Dictionary", "new", [], "dictionary")
        self.environment.send_message("Dictionary", "new", [], "sub_dictionary")
        
        self.environment.send_message("String", "new", ["key"], "key_name")
        self.environment.send_message("dictionary", "set", ["key_name", "sub_dictionary"], "dictionary")
    
        self.environment.send_message("dictionary", "get", ["key_name"], "dictionary_a")
        
        self.assertTrue(self.environment.are_equals("sub_dictionary", "dictionary_a"))

    def test_is_element_in_dict_equal(self):
        self.environment.send_message("Dictionary", "new", [], "dictionary")
        self.environment.send_message("String", "new", ["key"], "key_name")
        self.environment.send_message("String", "new", ["value"], "value_name")
        self.environment.send_message("dictionary", "set", ["key_name", "value_name"], "dictionary")
        self.environment.send_message("dictionary", "is_element_in_dict_equal",["key_name", "value_name"], "res")

        self.assertTrue(self.environment.is_true("res"))

    def test_dict_in_dict(self):
        self.environment.send_message("Dictionary", "new", [], "dictionary")
        self.environment.send_message("String", "new", ["key1"], "key1_name")
        self.environment.send_message("String", "new", ["value1"], "value1_name")

        self.environment.send_message("dictionary", "add_with_depth_one", ["key1_name", "value1_name"], "dict_interno")
        
        self.environment.send_message("dict_interno", "is_element_in_dict_equal",["key1_name", "value1_name"], "res")
        self.assertTrue(self.environment.is_true("res"))
