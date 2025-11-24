import unittest
import os
from training.train import Trainer

class TrainingTest(unittest.TestCase):
    
    def setUp(self):
        list_of_method_tokens = [("Class","doNothing"),("Class", "pass"),("Class", "doSomething"),("Class", "act1"),("Class", "act2")]
        list_of_class_tokens = [1]
        self.trainer = Trainer(list_of_method_tokens, list_of_class_tokens, 1)
    
    def test_trainer_assigns_id_correct_embedding(self):
        trace = [(1,("Class", "doNothing"), [], 2), (1,("Class", "pass"),[],2), 2]
        self.trainer.train_for(trace)
        self.assertTrue(self.trainer.get_embedding_for_object_id(2) is not None)

    def test_multiple_assigns_id_correct_embedding(self):
        trace = [(1, ("Class", "doSomething"), [], 3), (1, ("Class", "act1"), [], 2), (2, ("Class", "act2"), [], 3), 3]
        self.trainer.train_for(trace)
        self.assertTrue(self.trainer.get_embedding_for_object_id(2) is not None)
        self.assertTrue(self.trainer.get_embedding_for_object_id(3) is not None)

    def test_neural_nets_are_saved(self):
        trace = [(1, ("Class", "doNothing"), [], 2), (1, ("Class", "pass"), [], 2), 2]
        self.trainer.train_for(trace)
        self.trainer.save_models("")
        self.assertTrue(os.path.exists("token_net.pth"))
        self.assertTrue(os.path.exists("application_net.pth"))