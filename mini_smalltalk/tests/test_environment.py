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

    def test_object_has_no_superclass(self):

        self.environment.send_message("Object", "super", [], "Object_super")
        
        self.assertTrue(self.environment.are_equals("Object_super", "Nil"))

    def test_can_define_method_that_uses_message_result_as_colaborator(self):

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

    def test_can_define_method_that_uses_colaborator_as_internal_message_receptor(self):
        
        self.environment.define_method("Dictionary", "second_set",
                                       ["dictionary", "key", "value"],
                                       [("dictionary", "set", ["key", "value"], "dictionary")],
                                       "dictionary")
        
        self.environment.send_message("String", "new", ["key"], "main_key")
        self.environment.send_message("String", "new", ["value"], "main_value")
        self.environment.send_message("Dictionary", "new", [], "main_dictionary")
        
        self.environment.send_message("main_dictionary", "second_set", 
                                      ["main_dictionary", "main_key", "main_value"],
                                      "main_dictionary")
        
        self.environment.send_message("main_dictionary", "get", ["main_key"], "result")
        
        self.environment.are_equals("result", "main_value")
    
    def test_can_define_method_that_uses_colaborator_as_internal_message_result(self): pass

    def test_can_define_internal_colaborator(self):

        """
        
        self.environment.send_message("Class", "new", [], "Tupla")
        
        self.environment.define_internal_colab("Tupla", "primero")
        self.environment.define_internal_colab("Tupla", "segundo")
        
        self.environment.send_message("String", "new", ["string_primero"], "string_primero")
        self.environment.send_message("String", "new", ["string_segundo"], "string_segundo")
        
        self.environment.define_method("Tupla", "set_primero", ["string_primero"], 
                                       [("primero", "", [], "string_primero")], "Tupla")
                                       
        """
        
        pass

    def test_can_reference_self_on_method_implementation(self): pass

    def test_can_reference_instance_as_self_inside_method_implementation(self): pass

    def test_implement_class_hierarchies(self): pass