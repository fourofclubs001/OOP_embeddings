class DatasetUtils:

    def __init__(self, environment):

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