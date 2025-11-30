from trainer import Trainer
from dataset_utils.create_dataset import environment, traces
import os

def train():
    dir_output = os.path.normpath("../resulting_models") + os.path.normpath("/")
    environment_classes_ids = environment.get_classes_ids()
    environment_method_pairs = environment.get_class_method_pairs()
    trainer = Trainer(environment_method_pairs, environment_classes_ids, 10, 2)
    trainer.train_for_multiple_traces(traces)

    trainer.save_models(dir_output)
    trainer.show_loss_results()



train()