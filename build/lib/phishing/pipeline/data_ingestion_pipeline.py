from phishing.logging.custom_logger import logging
from phishing.exception.exception import PhishingException
from phishing.config.configuration import ConfigurationManager
from phishing.components.data_ingestion import DataIngestion
import sys

Stage_Name  = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_ingestion_pipline(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion.initiate_data_ingestion()

if __name__ == "__main__":
    try:
        logging.info(f">>>>>Stage {Stage_Name} started <<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion_pipline()
        logging.info(f">>> Stage {Stage_Name} completed <<<<")

    except Exception as e:
        raise PhishingException(e,sys)