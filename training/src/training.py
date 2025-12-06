from trainer import Trainer
from tester import Tester
from dataset_utils.create_dataset import environment, traces
import os

def train():
    dir_output = os.path.normpath("../resulting_models") + os.path.normpath("/")
    classes_with_ids = environment.get_classes_with_ids()
    environment_classes_ids = set(classes_with_ids.values())
    environment_method_pairs = environment.get_class_method_pairs()
    trainer = Trainer(environment_method_pairs, environment_classes_ids, 10, 2, 400)
    trainer.train_for_multiple_traces(traces)

    tester = Tester(trainer)
    distance_to_OperationsDictionary = tester.cosine_distance_between_class_and_list(classes_with_ids["OperatorDictionary"], set(classes_with_ids.values()))
    distance_to_obtain = tester.cosine_distance_between_method_and_list(("OperatorDictionary", "obtain"), environment_method_pairs)
    trainer.save_models(dir_output)
    trainer.show_loss_results()



train()