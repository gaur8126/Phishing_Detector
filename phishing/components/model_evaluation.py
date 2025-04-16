import os 
import pandas as pd 
from sklearn.metrics import accuracy_score,confusion_matrix
import numpy as  np 
import joblib 
from pathlib import Path
from phishing.utils.common import save_json
from phishing.logging.custom_logger import logging
from phishing.exception.exception import PhishingException
from phishing.config.configuration import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self,actual, pred):
        acc_score = accuracy_score(actual, pred)
        confusion = confusion_matrix(actual, pred)
        return acc_score, confusion
    
    def evaluate(self):

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]]



        predicted_qualities = model.predict(test_x)

        (acc_score, confusion) = self.eval_metrics(test_y, predicted_qualities)
            
            # Saving metrics as local
        scores = {"accuracy":acc_score }
        save_json(path=Path(self.config.metric_file_name), data=scores)

        return scores



        
