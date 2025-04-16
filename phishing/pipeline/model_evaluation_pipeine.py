import os 
import sys
from phishing.logging.custom_logger import logging
from phishing.exception.exception import PhishingException
from phishing.config.configuration import ConfigurationManager
from phishing.components.model_evaluation import ModelEvaluation

Stage_Name = "Model Evaluate Stage"

class ModelEvaluationTrainingPieline:
    def __init__(self):
        pass

    def model_evaluate(self):
        try:
            logging.info(f">>>> {Stage_Name} Staeted <<<<<<<")
            config = ConfigurationManager()
            model_evaluate_configuration = config.get_model_evaluation_config()
            model_evaluate = ModelEvaluation(model_evaluate_configuration)
            model_evaluate.evaluate()
            logging.info(f">>>>>{Stage_Name} completed <<<<<<")
        except Exception as e:
            raise PhishingException(e,sys)
        

if __name__ == "__main__":
    try:
        obj = ModelEvaluationTrainingPieline()
        obj.model_evaluate()
    except Exception as e :
        raise e