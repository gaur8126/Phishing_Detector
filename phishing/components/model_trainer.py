import pandas as pd 
import os 
from phishing.logging.custom_logger import logging
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
from phishing.logging.custom_logger import logging
from phishing.exception.exception import PhishingException
from phishing.entity.config_entity import ModelTrainerConfig
import sys 

class ModelTrainer:
    def __init__(self,config= ModelTrainerConfig):
        self.config = config

    def train(self):
        try: 
            train_data = pd.read_csv(self.config.train_data_path)
            test_data = pd.read_csv(self.config.test_data_path)

            train_x = train_data.drop([self.config.target_column],axis=1)
            test_x = test_data.drop([self.config.target_column],axis=1)
            train_y = train_data[[self.config.target_column]].replace(-1,0)
            test_y = test_data[[self.config.target_column]].replace(-1,0)

            lr = XGBClassifier()
            lr.fit(train_x,train_y)

            joblib.dump(lr,os.path.join(self.config.root_dir,self.config.model_name))

        except Exception as e:
            raise PhishingException(e,sys)
    