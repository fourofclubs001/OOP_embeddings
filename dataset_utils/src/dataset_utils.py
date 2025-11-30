from mini_smalltalk.src.Environment import Environment

class DatasetUtils:

    def __init__(self, environment: Environment):

        self.environment = environment

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
    
    def get_use_cases(self, implementations):

        self.environment.send_message("Class", "new", [], "UseCase")

        traces = []

        for implementation in implementations:

            self.environment.define_method(
                "UseCase", "use_case_selector", [], 
                implementation[:-1], implementation[-1]
            )

            self.environment.send_message("UseCase", "new", [], "use_case")

            #TODO: FALTA DEFINIR QUIEN INVOCA LA IMPLEMENTACIÓN PROPUESTA
            first_tuple = (self.environment.objects["UseCase"]["id"], ("UseCase", "use_case_selector"), [], 10000)

            virtual_trace = self.environment.send_message("use_case", "use_case_selector", 
                                                          [], "", trace=True, base_case=True)
            
            implementation_trace = self.implementation_to_trace(implementation[:-1],
                                                                implementation[-1])

            implementation_trace.insert(0, first_tuple)
            virtual_trace.insert(0, first_tuple)
            traces.append({
                "implementation": implementation_trace,
                "virtual": virtual_trace
            })
            
        return traces