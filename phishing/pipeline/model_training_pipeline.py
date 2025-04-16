import os 
import sys
from phishing.logging.custom_logger import logging
from phishing.exception.exception import PhishingException
from phishing.config.configuration import ConfigurationManager
from phishing.components.model_trainer import ModelTrainer

Stage_Name = "Model Trainer Stage"

class ModelTrianerPipeline:
    def __init__(self):
        pass

    def initiate_model_trainer(self):
        try:
            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(model_trainer_config)
            model_trainer.train()

        except Exception as e:
            raise PhishingException(e,sys)
        
    
if __name__ == "__main__":
    try:
        logging.info(f">>>> {Stage_Name} started <<<<<")
        obj = ModelTrianerPipeline()
        obj.initiate_model_trainer()
        logging.info(f">>>>>> {Stage_Name} completed <<<<<")
    except Exception as e:
        raise PhishingException(e,sys)
