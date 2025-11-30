import itertools

import torch
import matplotlib.pyplot as plt
from training.tests.object_embeddings_stub import ObjectEmbedding

# Los ids de los objetos/tokens que tienen embedding se organizan tal que: 
#      1.tokens de métodos 2.clases 3.objetos dinámicamente creados


class Trainer():
    def __init__(self, list_of_method_tokens, list_of_class_id_tokens, embedding_dim):
        
        self.number_of_method_tokens = len(list_of_method_tokens)
        self.number_of_class_tokens = len(list_of_class_id_tokens)

        self.list_of_class_id_tokens = list_of_class_id_tokens

        self.method_token_codification =  {method_token: i + self.number_of_class_tokens for i, method_token in enumerate(list_of_method_tokens)}
        self.method_token_embeddings = {}
        self.embedding_dictionary = {}

        self.token_net = torch.nn.Embedding(self.number_of_method_tokens + self.number_of_class_tokens , embedding_dim)
        self.application_net = ObjectEmbedding(embedding_dim, 1, 0, embedding_dim)

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
    
    def __get_embedding_for_object_id(self, object_id):
        if object_id in self.list_of_class_id_tokens and object_id not in self.embedding_dictionary.keys():
            embedding = self.token_net(torch.tensor([object_id]))
            self.embedding_dictionary[object_id] = embedding
        return self.embedding_dictionary[object_id]
    
    def __set_embedding_for_object_id(self, object_id, embedding):
        self.embedding_dictionary[object_id] = embedding

    def __application_net_result(self, receiver_embedding, message_embedding, collaborators_embeddings):
        return self.application_net(message_embedding, receiver_embedding, torch.tensor(collaborators_embeddings), torch.tensor([]))

    def __reset_embeddings(self):
        self.method_token_embeddings.clear()
        self.embedding_dictionary.clear()

    def train_for(self, trace):
        instruction_trace = trace[1:-1]
        objective_method_token = trace[0][1]
        print("Training for execution: " + str(objective_method_token))

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

        objective_method_embedding = self.__get_embedding_for_method_token(objective_method_token)
        embedding_of_returned_value = self.__get_embedding_for_object_id(trace[-1])
        

        loss = self.loss_function(objective_method_embedding, embedding_of_returned_value)
        
        self.optimizer.zero_grad() 
        loss.backward()
        self.optimizer.step()


        print(f"Loss: {loss:.3f}")

        return loss.item()

    def show_loss_results(self):
        fig, ax = plt.subplots()

        ax.plot(self.losses_record)
        ax.set_title("Loss for all traces")
        ax.set_xlabel("Number of epochs")
        ax.set_ylabel("Loss")

        plt.show()
    
    def train_for_multiple_traces(self, list_of_traces):
        number_of_steps = 0
        self.losses_record = []
        for trace in list_of_traces:
            print(f"--- Method {number_of_steps} ---")
            self.losses_record.append(self.train_for(trace))
            self.__reset_embeddings()
            print(f"--- End of Step ---")
            number_of_steps += 1

        return self.losses_record

    def save_models(self, dir_path):
        torch.save(self.token_net.state_dict(), dir_path + "token_net.pth")
        torch.save(self.application_net.state_dict(), dir_path + "application_net.pth")

    def load_models(self, token_net_path, application_net_path):
        self.token_net.load_state_dict(torch.load(token_net_path, weights_only=False))
        self.application_net.load_state_dict(torch.load(application_net_path, weights_only=False))
    


