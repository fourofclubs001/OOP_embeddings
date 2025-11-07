from src.Environment import Environment
import unittest

class DictiornayTest(unittest.TestCase):
    
    def setUp(self):
        
        self.environment = Environment()
    
    def test_can_add_key(self):
        
        self.environment.send_message("Dictionary", "new", [], "dictionary")
        self.environment.send_message("Dictionary", "new", [], "sub_dictionary")
        
        self.environment.send_message("String", "new", ["key"], "key_name")
        self.environment.send_message("dictionary", "set", ["key_name", "sub_dictionary"], "dictionary")
    
        self.environment.send_message("dictionary", "get", ["key_name"], "dictionary_a")
        
        self.assertTrue(self.environment.are_equals("sub_dictionary", "dictionary_a"))