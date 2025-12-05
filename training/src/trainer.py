import itertools
from sys import implementation

import torch
import matplotlib.pyplot as plt
from rnn.rnn_colabs_fijos import ObjectEmbedding

# Los ids de los objetos/tokens que tienen embedding se organizan tal que: 
#      1.tokens de métodos 2.clases 3.objetos dinámicamente creados


class Trainer():
    def __init__(self, list_of_method_tokens, list_of_class_id_tokens, embedding_dim, number_of_ext_collabs=2, app_net_class=ObjectEmbedding):
        
        self.number_of_method_tokens = len(list_of_method_tokens)
        self.number_of_class_tokens = len(list_of_class_id_tokens)
        self.max_token_id = max(list_of_class_id_tokens)
        self.embedding_size = embedding_dim

        self.list_of_class_id_tokens = list_of_class_id_tokens

        self.class_token_codification = {class_token: i for i, class_token in enumerate(list_of_class_id_tokens)}
        self.method_token_codification =  {method_token: i + self.number_of_class_tokens for i, method_token in enumerate(list_of_method_tokens)}
        self.method_token_embeddings = {}
        self.embedding_dictionary = {}

        self.token_net = torch.nn.Embedding(self.number_of_method_tokens + self.number_of_class_tokens , embedding_dim)
        self.application_net = app_net_class(embedding_dim, 0, number_of_ext_collabs, embedding_dim)

        self.optimizer = torch.optim.SGD(itertools.chain(self.token_net.parameters(), self.application_net.parameters()), lr=0.01)
        self.loss_function = torch.nn.MSELoss()
        self.losses_record = []
    
    def get_embedding_for_object_id(self, object_id):
        if object_id not in self.embedding_dictionary.keys():
            return None
        return self.embedding_dictionary[object_id]

    def get_embedding_for_method_token(self, method_token):
        if method_token not in self.method_token_codification.keys():
            return None

        method_token_id = self.method_token_codification[method_token]
        if method_token_id not in self.method_token_embeddings.keys():
            return None

        return self.method_token_embeddings[method_token_id]

    def __get_embedding_for_method_token(self, raw_token):
        token = self.method_token_codification[raw_token]
        if raw_token in self.method_token_embeddings.keys():
            return self.method_token_embeddings[token]
        embedding = self.token_net(torch.tensor([token]))
        self.method_token_embeddings[token] = embedding
        return embedding

    def __get_embeddings_for_object_id_list(self, list_of_ids):
        if any(type(id) is str for id in list_of_ids):
            return []
        return [self.__get_embedding_for_object_id(object_id) for object_id in list_of_ids]

    def is_class_id(self, object_id):
        return object_id in self.list_of_class_id_tokens

    def __get_embedding_for_object_id(self, object_id):
        if self.is_class_id(object_id):
            class_internal_token = self.class_token_codification[object_id]
            embedding = self.token_net(torch.tensor([class_internal_token]))
            self.embedding_dictionary[object_id] = embedding
        return self.embedding_dictionary[object_id]
    
    def __set_embedding_for_object_id(self, object_id, embedding):
        self.embedding_dictionary[object_id] = embedding

    def __application_net_result(self, receiver_embedding, message_embedding, collaborators_embeddings):
       torch_collaborators_embeddings = collaborators_embeddings
       if len(collaborators_embeddings) == 0:
           torch_collaborators_embeddings = torch.tensor([[]])
       else:
           torch_collaborators_embeddings = torch.stack(collaborators_embeddings)
       return self.application_net(message_embedding.view(1,self.embedding_size), receiver_embedding.view(1,self.embedding_size), torch.tensor([[]]), torch_collaborators_embeddings.view(1, len(collaborators_embeddings), self.embedding_size))

    def __reset_embeddings(self):
        self.method_token_embeddings.clear()
        self.embedding_dictionary.clear()

    def get_result_embedding_for_trace(self, trace):
        instruction_trace = trace[:-1]

        for instruction in instruction_trace:
            receiver = instruction[0]
            message_token = instruction[1]
            collaborators = instruction[2]
            result_variable = instruction[3]

            receiver_embedding = self.__get_embedding_for_object_id(receiver)
            message_embedding = self.__get_embedding_for_method_token(message_token)
            collaborators_embeddings = self.__get_embeddings_for_object_id_list(collaborators)

            result_embedding = self.__application_net_result(receiver_embedding, message_embedding, collaborators_embeddings)
            self.__set_embedding_for_object_id(result_variable, result_embedding)

        embedding_of_returned_value = self.__get_embedding_for_object_id(trace[-1])
        return embedding_of_returned_value


    def show_loss_results(self):
        fig, ax = plt.subplots()

        ax.plot(self.losses_record, marker='o')
        ax.set_title("Loss for all traces")
        ax.set_xlabel("Number of epochs")
        ax.set_ylabel("Loss")
        ax.grid()

        plt.show()

    def train_for(self, pair_of_traces):
        virtual_trace = pair_of_traces["virtual"]
        implementation_trace = pair_of_traces["implementation"]
        virtual_result_embedding = self.get_result_embedding_for_trace(virtual_trace)

        self.method_token_embeddings.clear()
        self.embedding_dictionary.clear()

        implementation_result_embedding = self.get_result_embedding_for_trace(implementation_trace)

        loss = self.loss_function(virtual_result_embedding, implementation_result_embedding)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        print(f"Loss: {loss:.3f}")

        return loss.item()

    def train_for_multiple_traces(self, list_of_traces):
        number_of_steps = 0
        self.losses_record = []
        for trace in list_of_traces:
            print(f"--- Method {number_of_steps} ---")
            self.losses_record.append(self.train_for(trace))

            self.method_token_embeddings.clear()
            self.embedding_dictionary.clear()
            print(f"--- End of Step ---")
            number_of_steps += 1

        return self.losses_record

    def save_models(self, dir_path):
        torch.save(self.token_net.state_dict(), dir_path + "token_net.pth")
        torch.save(self.application_net.state_dict(), dir_path + "application_net.pth")

    def load_models(self, token_net_path, application_net_path):
        self.token_net.load_state_dict(torch.load(token_net_path, weights_only=False))
        self.application_net.load_state_dict(torch.load(application_net_path, weights_only=False))
    


