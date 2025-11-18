import unittest
from src.Environment import *

class EnvironmentTest(unittest.TestCase):

    def setUp(self):

        self.environment = Environment()
        self.environment.send_message("Class", "new", [], "Lista")

    def test_are_equals_with_same_object(self):
        
        self.assertTrue(self.environment.are_equals("Class", "Class"))
        
    def test_are_not_equals_with_different_objects(self):
        
        self.assertFalse(self.environment.are_equals("Class", "Object"))

    def test_Object_is_Class_superclass(self):

        self.environment.send_message("Class", "super", [], "Class_superclass")
        
        self.assertTrue(self.environment.are_equals("Class_superclass", "Object"))

    def test_Class_is_Object_class(self):

        self.environment.send_message("Object", "class", [], "Object_class")

        self.assertTrue(self.environment.are_equals("Object_class", "Class"))

    def test_Class_class_is_Class(self):

        self.environment.send_message("Class", "class", [], "Class_class")

        self.assertTrue(self.environment.are_equals("Class", "Class_class"))

    def test_Class_can_create_instances(self):

        self.environment.send_message("Lista", "class", [], "Lista_class")
        
        self.assertTrue(self.environment.are_equals("Lista_class", "Class"))

    def test_Class_instance_can_create_instance(self):

        self.environment.send_message("Lista", "new", [], "lista")
        self.environment.send_message("lista", "class", [], "lista_class")

        self.assertTrue(self.environment.are_equals("lista_class", "Lista"))

    def test_class_instance_can_not_create_instance(self):

        self.environment.send_message("Lista", "new", [], "lista")

        with self.assertRaises(MessageNotUnderstood) as error:

            self.environment.send_message("lista", "new", [], "_")

        selector = "new"
        receptor_variable_name = "lista"
        receptor_class_name = "Lista"

        self.assertEqual(error.exception.args[0], 
                         f"Message {selector} not understood by {receptor_variable_name} object instance of {receptor_class_name}")

    def test_class_name_does_not_change_when_creating_new_class(self):
        
        self.environment.send_message("Class", "new", [], "Lista1")
        
        self.environment.send_message("Lista1", "name", [], "result") 
        self.assertEqual("Lista1", self.environment.get_value("result"))
        
        self.environment.send_message("Class", "new", [], "Lista2")
        
        self.environment.send_message("Lista1", "name", [], "result") 
        self.assertEqual("Lista1", self.environment.get_value("result"))

    def test_class_superclass_is_Object(self):

        self.environment.send_message("Lista", "super", [], "Lista_superclass")
        
        self.assertTrue(self.environment.are_equals("Lista_superclass", "Object"))

    def test_class_instance_has_not_superclass(self):

        self.environment.send_message("Lista", "new", [], "lista")

        with self.assertRaises(MessageNotUnderstood) as error:

            self.environment.send_message("lista", "super", [], "_")

        self.assertEqual(error.exception.args[0], "Message super not understood by lista object instance of Lista")

    def test_object_has_no_superclass(self):

        self.environment.send_message("Object", "super", [], "Object_super")
        
        self.assertTrue(self.environment.are_equals("Object_super", "Nil"))

    def test_can_define_method_for_class_instances(self):
        
        self.environment.define_method("Lista", "get_another_Lista", [],
                                       [("Lista", "new", [], "another_lista_temp")],
                                       "another_lista_temp")
        
        self.environment.send_message("Lista", "new", [], "lista")
        self.environment.send_message("lista", "get_another_Lista", [], "another_lista")
        self.environment.send_message("another_lista", "class", [], "another_lista_class")
        self.environment.send_message("another_lista_class", "name", [], "another_lista_class_name")
        
        another_lista_class_name = self.environment.get_value("another_lista_class_name")
        
        self.assertEqual(another_lista_class_name, "Lista")

    def test_can_define_method_for_class_instances_with_colaborator(self):
        
        self.environment.define_method("Dictionary", "create_identity_dictionary", ["key_and_value"],
                                       [("Dictionary", "new", [], "dictionary"),
                                        ("dictionary", "set", ["key_and_value", "key_and_value"], "dictionary")],
                                       "dictionary")
        
        self.environment.send_message("Dictionary", "new", [], "main_dictionary")
        self.environment.send_message("String", "new", ["key"], "main_dictionary_first_key")
        self.environment.send_message("main_dictionary", "create_identity_dictionary", 
                                      ["main_dictionary_first_key"], "main_dictionary")

        self.environment.send_message("main_dictionary", "get", ["main_dictionary_first_key"], "result_value")

        self.assertTrue(self.environment.are_equals("result_value", "main_dictionary_first_key"))

    def test_can_define_method_with_self(self):
        
        self.environment.define_method("Dictionary", "second_set",
                                       ["key", "value"],
                                       [("self", "set", ["key", "value"], "self")],
                                       "self")
        
        self.environment.send_message("String", "new", ["key"], "main_key")
        self.environment.send_message("String", "new", ["value"], "main_value")
        self.environment.send_message("Dictionary", "new", [], "main_dictionary")
        
        self.environment.send_message("main_dictionary", "second_set", 
                                      ["main_key", "main_value"],
                                      "main_dictionary")
        
        self.environment.send_message("main_dictionary", "get", ["main_key"], "result")
        
        self.environment.are_equals("result", "main_value")
    
    def test_can_define_method_that_uses_receptor_as_internal_message_colaborator(self):

        self.environment.define_method(
            "Dictionary", "set_as_sub_dictionary_of", 
            ["another_dictionary", "dictionary_key"],
            [("another_dictionary", "set", ["dictionary_key", "self"], "another_dictionary")],
            "another_dictionary"
        )

        self.environment.send_message("Dictionary", "new", [], "main_dictionary")
        self.environment.send_message("Dictionary", "new", [], "secondary_dictionary")
        self.environment.send_message("String", "new", [""], "main_key")

        self.environment.send_message(
            "main_dictionary", "set_as_sub_dictionary_of",
            ["secondary_dictionary", "main_key"], "result_dictionary"
        )

        self.environment.send_message("result_dictionary", "get", ["main_key"], 
                                      "result_sub_dictionary")

        self.assertTrue(self.environment.are_equals("result_dictionary", "secondary_dictionary"))
        self.assertTrue(self.environment.are_equals("result_sub_dictionary", "main_dictionary"))

    def test_can_define_method_that_uses_colaborator_as_internal_message_result(self):

        self.environment.send_message("String", "new", ["key_value"], "key_value")

        self.environment.define_method(
            "Dictionary", "fill_colaborator_dictionary",
            ["result_dictionary", "key_value"],
            [("self", "set", ["key_value", "key_value"], "result_dictionary")],
            "result_dictionary"
        )

        self.environment.send_message("Dictionary", "new", [], "main_dictionary")
        self.environment.send_message("Dictionary", "new", [], "secondary_dictionary")

        self.environment.send_message(
            "main_dictionary", "fill_colaborator_dictionary",
            ["secondary_dictionary", "key_value"], "result"
        )

        self.environment.send_message(
            "secondary_dictionary", "get",
            ["key_value"], "result_value"
        )

        self.assertTrue(self.environment.are_equals("result_value", "key_value"))

    def test_can_define_method_that_uses_internal_message_result_as_receptor(self):

        self.environment.define_method(
            "Dictionary", "get_by_reference",
            ["main_key", "reference_key"],
            [("self", "get", ["main_key"], "result_dictionary"),
             ("result_dictionary", "get", ["reference_key"], "result_value")],
             "result_value")

        self.environment.send_message("String", "new", ["main_key"], "main_key")
        self.environment.send_message("Dictionary", "new", [], "main_dictionary")

        self.environment.send_message("String", "new", ["reference_value"], "reference_value")
        self.environment.send_message("String", "new", ["reference_key"], "reference_key")
        self.environment.send_message("Dictionary", "new", [], "reference_dictionary")

        self.environment.send_message("reference_dictionary", "set",
                                      ["reference_key", "reference_value"],
                                      "reference_dictionary")

        self.environment.send_message("main_dictionary", "set", 
                                      ["main_key", "reference_dictionary"], 
                                      "main_dictionary")
        
        self.environment.send_message("main_dictionary", "get_by_reference",
                                      ["main_key", "reference_key"], "result")

        self.assertTrue(self.environment.are_equals("result", "reference_value"))

    def test_can_define_method_that_uses_internal_message_result_as_colaborator(self):

        self.environment.define_method(
            "Dictionary", "create_identity_dictionary", ["key_and_value"],
            [("Dictionary", "new", [], "dictionary_0"),
             ("dictionary_0", "set", ["key_and_value", "key_and_value"], "dictionary_0")],
              "dictionary_0"
        )

        self.environment.define_method(
            "Dictionary", "create_identity_dictionary_with_reference", 
            ["reference_dictionary", "key_and_value_reference"],
            [("reference_dictionary", "get", ["key_and_value_reference"], "key_and_value"),
             ("reference_dictionary", "create_identity_dictionary", ["key_and_value"], "dictionary_1")],
              "dictionary_1"
        )

        self.environment.send_message("Dictionary", "new", [], "main_dictionary")
        self.environment.send_message("String", "new", ["main_key"], "main_key")
        self.environment.send_message("Dictionary", "new", [], "reference_dictionary")
        self.environment.send_message("String", "new", [""], "reference_key")

        self.environment.send_message(
            "reference_dictionary", "set", 
            ["reference_key", "main_key"], "reference_dictionary"
        )

        self.environment.send_message(
            "main_dictionary", "create_identity_dictionary_with_reference",
            ["reference_dictionary", "reference_key"], "main_dictionary"
        )

        self.environment.send_message("main_dictionary", "get", ["main_key"], "result")

        self.assertTrue(self.environment.are_equals("result", "main_key"))

    def test_can_define_method_that_uses_internal_message_result_as_result(self):

        self.environment.define_method(
            "Dictionary", "overwrite_result",
            ["key_1", "key_2"],
            [("self", "get", ["key_1"], "final_value"),
             ("self", "get", ["key_2"], "final_value")],
             "final_value"
        )

        self.environment.send_message("String", "new", ["key_1"], "key_1")
        self.environment.send_message("String", "new", ["value_1"], "value_1")

        self.environment.send_message("String", "new", ["key_2"], "key_2")
        self.environment.send_message("String", "new", ["value_2"], "value_2")

        self.environment.send_message("Dictionary", "new", [], "main_dictionary")
        self.environment.send_message("main_dictionary", "set",
                                      ["key_1", "value_1"], "main_dictionary")
        self.environment.send_message("main_dictionary", "set",
                                      ["key_2", "value_2"], "main_dictionary")

        self.environment.send_message("main_dictionary", "overwrite_result",
                                      ["key_1", "key_2"], "result")

        self.assertTrue(self.environment.are_equals("result", "value_2"))

    def test_can_define_internal_colaborator(self): pass

    def test_implement_class_hierarchies(self): pass