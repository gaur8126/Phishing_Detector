import os 
import sys
from phishing.logging.custom_logger import logging
from phishing.exception.exception import PhishingException
from phishing.config.configuration import ConfigurationManager
from phishing.components.data_transformation import DataTransformation
from pathlib import Path

Stage_name = "Data Transformation Stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"),'r') as f:
                status = f.read().split(" ")[-1]
            if status=="True":
                config  = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(data_transformation_config)
                data_transformation.train_test_spliting()
            else: 
                raise Exception("your data schema is not valid")
        except Exception as e :
            raise PhishingException(e,sys)
        

if __name__ == "__main__":
    try:
        logging.info(f">>>> {Stage_name} started <<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.initiate_data_transformation()
        logging.info(f">>>>{Stage_name} completed <<<<")
    except Exception as e:
        raise PhishingException(e,sys)