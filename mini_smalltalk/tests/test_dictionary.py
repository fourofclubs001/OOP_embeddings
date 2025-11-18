from src.Environment import Environment
import unittest

class DictiornayTest(unittest.TestCase):
    
    def setUp(self):
        
        self.environment = Environment()
    
    def test_can_add_and_get_with_key(self):
        
        self.environment.send_message("Dictionary", "new", [], "dictionary")
        self.environment.send_message("Dictionary", "new", [], "sub_dictionary")
        
        self.environment.send_message("String", "new", ["key"], "key_name")
        self.environment.send_message("dictionary", "set", ["key_name", "sub_dictionary"], "dictionary")

        self.environment.send_message("dictionary", "get", ["key_name"], "dictionary_a")
        
        self.assertTrue(self.environment.are_equals("sub_dictionary", "dictionary_a"))

    def test_can_add_and_get_with_different_object_same_value_key(self):
        
        key_value = "key"

        self.environment.send_message("Dictionary", "new", [], "dictionary")
        self.environment.send_message("Dictionary", "new", [], "sub_dictionary")
        
        self.environment.send_message("String", "new", [key_value], "key_name")
        self.environment.send_message("dictionary", "set", ["key_name", "sub_dictionary"], "dictionary")
    
        self.environment.send_message("String", "new", [key_value], "same_key_name")

        self.environment.send_message("dictionary", "get", ["same_key_name"], "dictionary_a")
        
        self.assertTrue(self.environment.are_equals("sub_dictionary", "dictionary_a"))