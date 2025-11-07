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