

import unittest

from src.Environment import Environment


class BooleanTest(unittest.TestCase):
    
    def setUp(self):
        
        self.environment = Environment()

    def test_reflexivity(self):
        self.environment.send_message("Dictionary", "new", [], "dict")
        self.environment.send_message("dict", "==", ["dict"], "val")
        self.assertTrue(self.environment.is_true("val"))
    
    def test_difference(self):
        self.environment.send_message("Dictionary", "new", [], "dict1")
        self.environment.send_message("Dictionary", "new", [], "dict2")
        self.environment.send_message("dict1", "==", ["dict2"], "val")
        self.assertTrue(self.environment.is_false("val"))
    
    def test_string_equality(self):
        self.environment.send_message("String", "new", ["characters"], "string1")
        self.environment.send_message("String", "new", ["characters"], "string2")
        self.environment.send_message("string1", "==", ["string2"], "val")
        self.assertTrue(self.environment.is_true("val"))
        
    def test_string_inequality(self):
        self.environment.send_message("String", "new", ["characters2"], "string1")
        self.environment.send_message("String", "new", ["characters"], "string2")
        self.environment.send_message("string1", "==", ["string2"], "val")
        self.assertTrue(self.environment.is_false("val"))

    def test_string_simmetry(self):
        self.environment.send_message("String", "new", ["characters"], "string1")
        self.environment.send_message("String", "new", ["characters"], "string2")
        self.environment.send_message("string1", "==", ["string2"], "val1")
        self.environment.send_message("string2", "==", ["string1"], "val2")
        self.assertTrue(self.environment.is_true("val1"))
        self.assertTrue(self.environment.is_true("val2"))


    def test_inequality_of_different_types(self):
        self.environment.send_message("String", "new", ["characters"], "string")
        self.environment.send_message("Dictionary", "new", [], "dict")
        self.environment.send_message("string", "==", ["dict"], "val")
        self.assertTrue(self.environment.is_false("val"))


