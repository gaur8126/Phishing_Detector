import os
import json 
import sys 
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL =  os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

from phishing.exception.exception import PhishingException
from phishing.logging.custom_logger import logging
import pandas as pd
import numpy as np
import pymongo

class PhishingDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise PhishingException(e,sys)
        
    def csv_convert_to_json(self,filepath):

        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise PhishingException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection 
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records) 
            return len(self.records)

        except Exception as e: 
            raise PhishingException(e,sys)
        
if __name__ == "__main__":
    FILEPATH = "phishing_data/NetworkData.csv"
    DATABASE = "MYDATABASE"
    Collection = "phishing_data"
    obj = PhishingDataExtract()
    Records = obj.csv_convert_to_json(filepath=FILEPATH)
    print(Records)
    no_of_records = obj.insert_data_mongodb(records=Records,collection=Collection,database=DATABASE)
    print(no_of_records)