
from phishing.logging.custom_logger import logging
from phishing.exception.exception import PhishingException
from phishing.config.configuration import ConfigurationManager
from phishing.components.data_validation import DataValidation
import sys


Stage_Name = "Date Validation Stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(data_validation_config)
        data_validation.validate_all_columns()


if __name__ == "__main__":
    try:
        logging.info(f">>>> Stage {Stage_Name} started <<<")
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()
        logging.info(f">>>>> Stage {Stage_Name} Completed <<<<")

    except Exception as e:
        raise PhishingException(e,sys)
