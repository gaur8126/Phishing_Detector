import joblib
import numpy as np 
import pandas as pd 
from pathlib import Path

class PredictionPipeline:
    def __init__(self):
        self.model = joblib.load(Path("artifacts/model_trainer/model.joblib"))

    def predict(self,data):
        prediction = self.model.predict(data)

        return prediction
    
if __name__ == "__main__":
    obj = PredictionPipeline()
    predict = obj.predict([[1,0,-1,1,1,-1,1,1,-1,1,1,1,1,0,0,-1,1,1,0,-1,1,-1,1,-1,-1,0,-1,1,1,1]])
    print(predict)