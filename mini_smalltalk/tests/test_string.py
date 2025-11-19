import unittest
from mini_smalltalk.src.Environment import Environment

class StringTest(unittest.TestCase):
    
    def setUp(self):
        
        self.environment = Environment()
    
    def test_can_add_key(self):
        
        self.environment.send_message("String", "new", ["characters"], "string")
        response = self.environment.get_value("string")
        
        self.assertEqual(response, "characters")
        
    def test_can_create_string_inside_method(self):
        
        self.environment.define_method(
            "String", "new_string", [],
            [("String", "new", ["string_value"], "string")],
            "string")
        
        self.environment.send_message("String", "new", [""], "some_string")
        self.environment.send_message("some_string", "new_string", [], "another_string")
        
        another_string_value = self.environment.get_value("another_string")
        
        self.assertEqual(another_string_value, "string_value")