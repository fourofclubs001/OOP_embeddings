class MessageNotUnderstood(Exception):

    def __init__(self, receptor_variable_name, selector, receptor_class_name):

        super().__init__(f"Message {selector} not understood by {receptor_variable_name} object instance of {receptor_class_name}")

class Environment:

    def __init__(self):

        self.id_counter = 0

        self.objects = {}

        self.objects["Nil"] = {
            
            "class_methods":{
                "name":([],[],"Nil_name")
            },
            "id": self.assign_id()
        }

        self.objects["Object"] = {}
        self.objects["Class"] = {}

        self.objects["Class"]["class_methods"] = {
        
            "class": ([],[],"Class"), 
            "super": ([],[], "Object"),
            "name": ([],[],"Class_name"), 
            "new": ""
        
        }
        
        self.objects["Class"]["instance_methods"] = {
            
            "class": ([],[],"Class"), 
            "super":([],[],"Object"),
            "name":"",
            "new":""
            
        }

        self.objects["Object"]["class_methods"] = {
            
            "class":([],[],"Class"),
            "super":([],[],"Nil"), 
            "name":([],[],"Object_name"), 
            "new":""
            
        }
        
        self.objects["Object"]["instance_methods"] = {}
        
        self.objects["Object"]["id"] = self.assign_id()
        self.objects["Class"]["id"] = self.assign_id()

        self.virtual_machine_implementations = {
            
            "new": self.new_method_implementation,
            "value": self.value_method_implementation,
            "set": self.set_method_implementation,
            "get": self.get_method_implementation
            
        }

        self.send_message("Class", "new", [], "String")
        self.declare_virtual_machine_method("String", "value")

        self.send_message("String", "new", ["Nil"], "Nil_name")
        self.send_message("String", "new", ["Object"], "Object_name")
        self.send_message("String", "new", ["Class"], "Class_name")

        self.send_message("Class", "new", [], "Dictionary")
        self.declare_virtual_machine_method("Dictionary", "set")
        self.declare_virtual_machine_method("Dictionary", "get")

    def assign_id(self):
        
        id = self.id_counter
        self.id_counter += 1
        return id
    
    def are_equals(self, object1, object2):
        
        return self.objects[object1]["id"] == self.objects[object2]["id"]

    def raise_message_not_understood_error(self, receptor, selector):
        
        self.send_message(receptor, "class", [], "tmp")
        self.send_message("tmp", "name", [], "tmp")
        
        receptor_class_name = self.get_value("tmp")
        
        raise MessageNotUnderstood(receptor, selector, receptor_class_name)

    def fill_new_object_fields_at_objects_dictionary(self, receptor, result):
        
        self.objects[result] = {}
        self.objects[result]["id"] = self.assign_id()
            
        self.objects[result]["class_methods"] = self.objects[receptor]["instance_methods"].copy()
        self.objects[result]["instance_methods"] = {}
        self.objects[result]["instance_methods"]["class"] = ([],[],result)

    def assign_name_to_object(self, receptor, colaborators, result):
        
        if receptor == "String": # base case
                
            self.objects[result]["class_methods"]["name"] = ([],[],result)
            self.objects[result]["value"] = colaborators[0]
            
        else: # inductive case
            
            self.send_message("String", "new", [result], f"{result}_name")
            self.objects[result]["class_methods"]["name"] = ([],[],f"{result}_name")

    def assign_Object_as_super_and_name_when_creating_class(self, receptor, colaborators, result):
        
        if self.objects[receptor]["class_methods"]["class"][2] == "Class":

            self.assign_name_to_object(receptor, colaborators, result)

    def send_message(self, receptor, selector, colaborators, result):

        if not selector in self.objects[receptor]["class_methods"]: 
            
            self.raise_message_not_understood_error(receptor, selector)

        elif selector in self.virtual_machine_implementations.keys():
            
            self.virtual_machine_implementations[selector](receptor, colaborators, result)

        else: self.objects[result] = self.execute_method(receptor, selector, colaborators)

    def get_value(self, object):

        return self.objects[object]["value"]
    
    def define_method(self, class_name, method_name, colaborators,
                      method_implementation, result):
        
        self.objects[class_name]["instance_methods"][method_name] = (colaborators,
                                                                     method_implementation,
                                                                     result)
        
    def initialize_dictionary_for_Dictionary_instance(self, receptor, result):
        
        if receptor == "Dictionary": self.objects[result]["dictionary"] = {}
        
    def declare_virtual_machine_method(self, receptor, selector):
        
        self.define_method(receptor, selector, [], [], None)

    def new_method_implementation(self, receptor, colaborators, result):
        
        self.fill_new_object_fields_at_objects_dictionary(receptor, result)
        self.assign_Object_as_super_and_name_when_creating_class(receptor, colaborators, result)
        self.initialize_dictionary_for_Dictionary_instance(receptor, result)
        
    def value_method_implementation(self, receptor, colaborators, result):
        
        self.objects[result] = self.objects[receptor]["value"]
        
    def set_method_implementation(self, receptor, colaborators, result):
        
        self.objects[result] = self.objects[receptor].copy()
        self.objects[result]["dictionary"][colaborators[0]] = self.objects[colaborators[1]]
        
    def get_method_implementation(self, receptor, colaborators, result):
        
        self.objects[result] = self.objects[receptor]["dictionary"][colaborators[0]]
      
    def execute_method(self, receptor, selector, colaborators):
            
        colaborators_rename, method_implementation, result = self.objects[receptor]["class_methods"][selector]
        
        method_dictionary = {}
        
        for idx in range(len(colaborators)):
            
            method_dictionary[colaborators_rename[idx]] = colaborators[idx]
        
        for message in method_implementation:
            
            message_receptor, message_selector, message_colaborators_rename, message_result = message
            
            message_colaborators = []
            
            for idx in range(len(message_colaborators_rename)):
                
                message_colaborators.append(method_dictionary[message_colaborators_rename[idx]])
            
            self.send_message(message_receptor, message_selector, message_colaborators, message_result)
            
        return self.objects[result]
    
    # Utils
    
    def get_classes(self):
        
        classes = []
        
        for object_name in list(self.objects.keys()):
            
            if "class" in self.objects[object_name]["class_methods"]:
                
                if self.objects[object_name]["class_methods"]["class"][2] == "Class":
                
                    name_object = self.objects[object_name]["class_methods"]["name"][2]
                
                    classes.append(self.get_value(name_object))
            
        return set(classes)
    
    def get_class_method_pairs(self):
        
        class_method_pairs = []
        
        classes = self.get_classes()
        
        for class_ in classes:
            
            for method in self.objects[class_]["instance_methods"]:
                
                class_method_pairs.append((class_, method))
                
        return class_method_pairs