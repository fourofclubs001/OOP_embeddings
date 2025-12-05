import unittest
import os
from training.src.trainer import Trainer
from training.tests.object_embeddings_stub import ObjectEmbedding

class TrainingTest(unittest.TestCase):
    
    def setUp(self):
        list_of_method_tokens = [("Class","doNothing"),("Class", "pass"),("Class", "doSomething"),("Class", "act1"),("Class", "act2"),("Class", "actWithCollabs")]
        list_of_class_tokens = [1]
        self.trainer = Trainer(list_of_method_tokens, list_of_class_tokens, 1, 2, ObjectEmbedding)
    
    def test_trainer_assigns_id_correct_embedding(self):
        trace = [(1,("Class", "doNothing"), [], 2), (1,("Class", "pass"),[],2), 2]
        self.trainer.get_result_embedding_for_trace(trace)
        self.assertEqual(0, self.trainer.get_embedding_for_object_id(2))
        self.assertTrue(self.trainer.get_embedding_for_method_token(("Class", "doNothing")) is not None)
        self.assertTrue(self.trainer.get_embedding_for_method_token(("Class", "pass")) is not None)


    def test_multiple_assigns_id_correct_embedding(self):
        trace = [(1, ("Class", "doSomething"), [], 3), (1, ("Class", "act1"), [], 2), (2, ("Class", "act2"), [], 3), 3]
        self.trainer.get_result_embedding_for_trace(trace)
        self.assertTrue(self.trainer.get_embedding_for_object_id(2) is not None)
        self.assertTrue(self.trainer.get_embedding_for_object_id(3) is not None)
        self.assertTrue(self.trainer.get_embedding_for_method_token(("Class", "doSomething")) is not None)
        self.assertTrue(self.trainer.get_embedding_for_method_token(("Class", "act1")) is not None)
        self.assertTrue(self.trainer.get_embedding_for_method_token(("Class", "act2")) is not None)

    def test_collaborators_with_a_string_get_all_ignored(self):
        trace = [(1, ("Class", "doNothing"), [], 2), (1, ("Class", "actWithCollabs"), ["stringToIgnore"], 2), 2]
        self.trainer.get_result_embedding_for_trace(trace)

        self.assertTrue(self.trainer.get_embedding_for_object_id(2) is not None)
        self.assertTrue(self.trainer.get_embedding_for_object_id("stringToIgnore") is None)
        self.assertTrue(self.trainer.get_embedding_for_method_token("stringToIgnore") is None)

    def test_multiple_traces_produce_multiple_losses(self):
        trace1 = [(1, ("Class", "doNothing"), [], 2), (1, ("Class", "actWithCollabs"), [], 2), 2]
        trace2 = [(1, ("Class", "doSomething"), [], 3), (1, ("Class", "act1"), [], 2), (2, ("Class", "act2"), [], 3), 3]
        losses = self.trainer.train_for_multiple_traces([trace1, trace2])

        self.assertEqual(2, len(losses))

    def test_trace_with_external_collaborators(self):
        trace = [(1, ("Class", "doSomething"), [], 3), (1, ("Class", "act1"), [], 2), (1, ("Class", "actWithCollabs"), [2], 3), 3]

        self.trainer.get_result_embedding_for_trace(trace)

        self.assertTrue(self.trainer.get_embedding_for_object_id(2) is not None)
        self.assertEqual(1, self.trainer.get_embedding_for_object_id(3).item())
        self.assertTrue(self.trainer.get_embedding_for_method_token(("Class", "doSomething")) is not None)
        self.assertTrue(self.trainer.get_embedding_for_method_token(("Class", "act1")) is not None)
        self.assertTrue(self.trainer.get_embedding_for_method_token(("Class", "actWithCollabs")) is not None)

    def test_neural_nets_are_saved(self):
        trace = [(1, ("Class", "doNothing"), [], 2), (1, ("Class", "pass"), [], 2), 2]
        self.trainer.get_result_embedding_for_trace(trace)
        self.trainer.save_models("")
        self.assertTrue(os.path.exists("token_net.pth"))
        self.assertTrue(os.path.exists("application_net.pth"))
