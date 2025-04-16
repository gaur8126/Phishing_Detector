import os 
import sys
from phishing.logging.custom_logger import logging
from phishing.exception.exception import PhishingException
from phishing.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from phishing.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from phishing.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline
from phishing.pipeline.model_training_pipeline import ModelTrianerPipeline
from phishing.pipeline.model_evaluation_pipeine import ModelEvaluationTrainingPieline

STAGE_NAME = "Data Ingestion Stage"


try:
    logging.info(f">>>>>>> Stage {STAGE_NAME} started")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.initiate_data_ingestion_pipline()
    logging.info(f">>>>> stage {STAGE_NAME} completed <<<<<<\n\nx========x")
except Exception as e:
    logging.exception(e)
    raise e 


STAGE_NAME = "Data Validation Stage"

try:
    logging.info(f">>>>>>> Stage {STAGE_NAME} started")
    data_validation = DataValidationTrainingPipeline()
    data_validation.initiate_data_validation()
    logging.info(f">>>>> stage {STAGE_NAME} completed <<<<<<\n\nx========x")
except Exception as e:
    logging.exception(e)
    raise e 

STAGE_NAME = "Transformation Stage"

try:
    logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_transformation = DataTransformationTrainingPipeline()
    data_transformation.initiate_data_transformation()
    logging.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    raise e 

STAGE_NAME = "Model Training Stage"

try:
    logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    model_trainer = ModelTrianerPipeline()
    model_trainer.initiate_model_trainer()
    logging.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    raise e 


STAGE_NAME = "Model Evaluation Stage"

try:
    logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    model_evaluation = ModelEvaluationTrainingPieline()
    model_evaluation.model_evaluate()
    logging.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    raise e 
