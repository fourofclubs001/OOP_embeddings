import unittest
from mini_smalltalk.src.Environment import Environment

class StringTest(unittest.TestCase):
    
    def setUp(self):
        
        self.environment = Environment()
    
    def test_can_add_key(self):
        
        self.environment.send_message("String", "new", ["characters"], "string")
        response = self.environment.get_value("string")
        
        self.assertEqual(response, "characters")