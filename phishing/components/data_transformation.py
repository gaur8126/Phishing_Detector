import os
from phishing.logging.custom_logger import logging
from sklearn.model_selection import train_test_split
import pandas as pd 
from phishing.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self,config:DataTransformationConfig):
        self.config = config 

    def train_test_spliting(self):
        data = pd.read_csv(self.config.data_path)

        train,test = train_test_split(data)

        train.to_csv(os.path.join(self.config.root_dir,"train.csv"),index = False)
        test.to_csv(os.path.join(self.config.root_dir,"test.csv"),index = False)

        logging.info('Splited data training and test sets')
        logging.info(train.shape)
        logging.info(test.shape)

        print(train.shape)
        print(test.shape)