import json
from mini_smalltalk.src.Environment import Environment

class DatasetUtils:

    def __init__(self, environment: Environment):

        self.environment = environment

    def define_method_environment(self, methods_register_file_dir):

        with open(methods_register_file_dir, 'r') as file:
        
            data = json.load(file)

            for method_definition in data:

                self.environment.define_method(
                    method_definition[0], 
                    method_definition[1], 
                    method_definition[2], 
                    method_definition[3], 
                    method_definition[4]
                )

    def get_use_case_traces(self):

        with open("dataset_utils/use_case_register.json", 'r') as file:

            use_case_implementation = json.load(file)

            traces = self.get_use_case_implementation_traces(use_case_implementation)

        return traces

    def implementation_to_trace(self, implementation, return_variable):

        trace = []

        for receptor, selector, colaborators, result in implementation:

            if receptor == "String" and selector == "new":

                trace.append((
                    self.environment.objects[receptor]["id"], 
                    (self.environment.objects[receptor]["class_methods"]["class"][2], selector),
                    [colaborators[0]], 
                    self.environment.objects[result]["id"]))

            else:

                trace.append((
                    self.environment.objects[receptor]["id"], 
                    (self.environment.objects[receptor]["class_methods"]["class"][2], selector),
                    [self.environment.objects[colaborator]["id"] for colaborator in colaborators], 
                    self.environment.objects[result]["id"]))
                
        trace.append(self.environment.objects[return_variable]["id"])

        return trace
    
    def get_use_case_implementation_traces(self, implementations):

        self.environment.send_message("Class", "new", [], "UseCase")

        traces = []

        for implementation in implementations:

            self.environment.define_method(
                "UseCase", "use_case_selector", [], 
                implementation[:-1], implementation[-1]
            )

            self.environment.send_message("UseCase", "new", [], "use_case")

            virtual_trace = self.environment.send_message("use_case", "use_case_selector", 
                                                          [], "", trace=True, base_case=True)
            
            implementation_trace = self.implementation_to_trace(implementation[:-1],
                                                                implementation[-1])

            traces.append({
                "implementation": implementation_trace,
                "virtual": virtual_trace
            })
            
        return traces