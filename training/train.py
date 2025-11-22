import torch

# Los ids de los objetos/tokens que tienen embedding se organizan tal que: 
#      1.tokens de métodos 3.objetos dinámicamente creados


class Trainer():
    def __init__(self, list_of_method_tokens, embedding_dim):
        
        self.number_of_method_tokens = len(list_of_method_tokens)

        self.method_token_codification =  {method_token: i for i, method_token in enumerate(list_of_method_tokens)}
        self.method_token_embeddings = {}
        self.embedding_dictionary = {}

        self.token_net = torch.nn.Embedding(self.number_of_method_tokens , embedding_dim)
        self.application_net = "ObjectEmbedding()"

        self.optimizer = torch.optim.SGD([self.token_net.parameters(), self.application_net.parameters()], lr=0.01)
        self.loss_function = torch.nn.MSELoss()

    def __offset_object_id(self, object_id):
        return object_id + self.number_of_method_tokens

    def get_embedding_for_method_token(self, raw_token):
        token = self.method_token_codification[raw_token]
        if raw_token in self.method_token_embeddings.keys():
            return self.method_token_embeddings[token]
        embedding = self.token_net(token)
        self.method_token_embeddings[token] = embedding
        return embedding

    def get_embeddings_for_object_id_list(self, list_of_ids):
        return [self.get_embedding_for_object_id(object_id) for object_id in list_of_ids]
    
    # Asumo que las clases vienen como numeros y se dividen los objetos según sean clases o no
    def get_embedding_for_object_id(self, number_of_object):
        index_in_embedding_dictionary = self.__offset_object_id(number_of_object)
        return self.embedding_dictionary[index_in_embedding_dictionary]
    
    def set_embedding_for_object_id(self, number_of_object, embedding):
        self.embedding_dictionary[self.__offset_object_id(number_of_object)] = embedding

    def application_net_result(self, receiver_embedding, message_embedding, collaborators_embeddings):
        return self.application_net(message_embedding, self.__offset_object_id(receiver_embedding), map(self.__offset_object_id, collaborators_embeddings))

    def train_for(self, trace):
        instruction_trace = trace[1:-1]
        for instruction in instruction_trace:
            receiver = instruction[0]
            message_token = instruction[1]
            collaborators = instruction[2]
            result_variable = instruction[3]

            receiver_embedding = self.get_embedding_for_object_id(receiver)
            message_embedding = self.get_embedding_for_method_token(message_token)
            collaborators_embeddings = self.get_embeddings_for_object_id_list(collaborators)

            result_embedding = self.application_net_result(receiver_embedding, message_embedding, collaborators_embeddings)
            self.set_embedding_for_object_id(result_variable, result_embedding)

        embedding_of_returned_value = self.get_embedding_for_object_id(trace[-1])
        objective_method_token = trace[0][1]

        loss = self.loss_function(self.get_embedding_for_method_token(objective_method_token), embedding_of_returned_value)

        self.optimizer.zero_grad() 
        loss.backward()

        self.optimizer.step()

    def save_models(self, dir_path):
        torch.save(self.token_net.state_dict(), dir_path + "token_net.pth")
        torch.save(self.application_net.state_dict(), dir_path + "application_net.pth")

    def load_models(self, token_net_path, application_net_path):
        self.token_net.load_state_dict(torch.load(token_net_path))
        self.application_net.load_state_dict(torch.load(application_net_path))
    


