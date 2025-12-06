import copy
import torch


class Tester:
    def __init__(self, trainer):
        self.class_token_codification = trainer.class_token_codification.copy()
        self.method_token_codification = trainer.method_token_codification.copy()
        self.token_net = copy.deepcopy(trainer.token_net)
        self.application_net = copy.deepcopy(trainer.application_net)

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

        distances = {token_id: torch.nn.functional.cosine_similarity(reference_embedding, other_embedding, dim=0)
                     for token_id, other_embedding in other_embeddings.items()}

        return distances

    def load_models(self, token_net_path, application_net_path):
        self.token_net.load_state_dict(torch.load(token_net_path, weights_only=False))
        self.application_net.load_state_dict(torch.load(application_net_path, weights_only=False))
