import os 
import pandas as pd 
from sklearn.metrics import accuracy_score,f1_score,precision_score
import numpy as  np 
import joblib 
import mlflow
from pathlib import Path
from phishing.utils.common import save_json
from xgboost import XGBClassifier
from phishing.logging.custom_logger import logging
from phishing.exception.exception import PhishingException
from phishing.config.configuration import ModelEvaluationConfig,ConfigurationManager

import dagshub
dagshub.init(repo_owner='gaur8126', repo_name='Phishing_Detector', mlflow=True)

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self,actual, pred):
        acc_score = accuracy_score(actual, pred)
        precision = precision_score(actual, pred)
        f1score = f1_score(actual, pred)
        return acc_score, precision,f1score
    
    def track_mlflow(self,best_model,acc_score,precision,f1score):
        with mlflow.start_run():
            f1_score = f1score
            precision_score = precision
            accu_score = acc_score

            mlflow.log_metric("accuracy_score",accu_score)
            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.sklearn.log_model(best_model,"model")
    
    def evaluate(self):

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]].replace(-1,0)

        lr = XGBClassifier()

        predicted_qualities = model.predict(test_x)

        (acc_score, precision,f1score) = self.eval_metrics(test_y, predicted_qualities)
        self.track_mlflow(best_model=lr,acc_score=acc_score,f1score=f1score,precision=precision)
            
        # Saving metrics as local
        scores = {"accuracy":acc_score }
        save_json(path=Path(self.config.metric_file_name), data=scores)

        return scores
    

# if __name__ == "__main__":
#     config = ConfigurationManager()
#     model_evaluate_configuration = config.get_model_evaluation_config()
#     model_evaluate = ModelEvaluation(model_evaluate_configuration)
#     print(model_evaluate.evaluate())



        
