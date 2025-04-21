from flask import Flask, render_template, request, jsonify
import requests
import os 
import numpy as np 
import pandas as pd
from phishing.pipeline.prediction_pipeline import PredictionPipeline 
from feature_extaction import URLFeatureExtractor
app = Flask(__name__)

# # Initialize your pipeline
predictor = PredictionPipeline()

@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/train', methods=['GET'])
def training():
    os.system("python main.py")
    return "Training Successful"

@app.route("/predict", methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data['url']
        print("data-------",data)
        print("url-----------",url)
        
        # Create feature extractor with the URL
        feature_extractor = URLFeatureExtractor(url)
        domain_info = feature_extractor._check_domain_registration()
        
        # Extract features
        features = feature_extractor.get_features()
        features_value = list(features.values())
        print("feature values ---------\n",features_value)
        
        # Make prediction (adjust based on your model's input requirements)
        prediction = predictor.predict([features_value])  # Wrap in list if expecting 2D array
        print("pre -------- ",prediction)
        
        # Prepare response
        result = {
            'is_phishing': bool(prediction),
            # 'risk_level': 'High' if prediction[0] else 'Low',
            # 'domain_info': str(features.get('domain_info', domain_info)),
            # 'threats': ', '.join(features.get('threats', [])),
            # 'features': features
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
