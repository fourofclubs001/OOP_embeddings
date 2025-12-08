import copy
import torch
import matplotlib.pyplot as plt


class Tester:
    def __init__(self, trainer, class_id_to_name_mapper):
        self.class_token_codification = trainer.class_token_codification.copy()
        self.method_token_codification = trainer.method_token_codification.copy()
        self.token_net = copy.deepcopy(trainer.token_net)
        self.application_net = copy.deepcopy(trainer.application_net)
        self.embedding_size = trainer.embedding_size

        self.class_id_to_name_mapper = class_id_to_name_mapper

        self.token_net.eval()
        self.application_net.eval()

    def cosine_distance_between_class_and_list(self, reference_class_id, list_of_classes_ids):

        return self.cosine_distance_between_token_and_list_of_tokens(reference_class_id, list_of_classes_ids, self.class_token_codification)

    def cosine_distance_between_method_and_list(self, reference_method, list_of_methods):

        return self.cosine_distance_between_token_and_list_of_tokens(reference_method, list_of_methods, self.method_token_codification)

    def cosine_distance_between_token_and_list_of_tokens(self, reference_token, list_of_tokens, mapper):
        reference_embedding = self.token_net(torch.tensor(mapper[reference_token]))
        other_embeddings = {token_id: self.token_net(torch.tensor(mapper[token_id])) for
                                    token_id in list_of_tokens}

        distances = {token_id: 1 - torch.nn.functional.cosine_similarity(reference_embedding, other_embedding, dim=0)
                     for token_id, other_embedding in other_embeddings.items()}

        return distances

    def get_instance_embedding_of(self, receiver_class_id):
        receiver_embedding = self.token_net(torch.tensor(self.class_token_codification[receiver_class_id]))
        method_embedding = self.token_net(torch.tensor(self.method_token_codification[("Class", "new")]))
        application_embedding = self.application_net(receiver_embedding.view(1,self.embedding_size), method_embedding.view(1,self.embedding_size), torch.tensor([[]]), torch.tensor([[]]))
        return application_embedding


    def plot_class_distances(self, reference_token, list_of_tokens):
        distance_to_OperationsDictionary = self.cosine_distance_between_class_and_list(reference_token, list_of_tokens)
        classes_ids = list(distance_to_OperationsDictionary.keys())
        classes = [str(self.class_id_to_name_mapper[class_id]) for class_id in classes_ids]

        class_distances = list(distance_to_OperationsDictionary.values())
        class_distances = [distance.detach().numpy() for distance in class_distances]

        fig, ax = plt.subplots()

        ax.bar(range(len(classes)), class_distances, tick_label=classes)
        fig.autofmt_xdate()
        ax.set_title("Cosine distance between classes")
        ax.set_xlabel("Classes")
        ax.set_ylabel("Distance")
        ax.grid()

        plt.savefig('result_class.png')

        plt.show()

    def plot_method_distances(self, reference_token, list_of_tokens):
        distance_to_impose = self.cosine_distance_between_method_and_list(reference_token, list_of_tokens)
        methods = list(distance_to_impose.keys())
        methods = [str(method_tuple) for method_tuple in methods]

        methods_distances =  list(distance_to_impose.values())
        methods_distances = [distance.detach().numpy() for distance in methods_distances]

        fig, ax = plt.subplots()
        ax.bar(range(len(methods)), methods_distances, tick_label=methods)
        fig.autofmt_xdate()
        ax.set_title("Cosine distance between methods")
        ax.set_xlabel("Methods")
        ax.set_ylabel("Distance")
        ax.grid()

        plt.savefig('result_methods.png')

        plt.show()

    def load_models(self, token_net_path, application_net_path):
        self.token_net.load_state_dict(torch.load(token_net_path, weights_only=False))
        self.application_net.load_state_dict(torch.load(application_net_path, weights_only=False))
