from flask import Flask, render_template, request, jsonify
import requests
import os 
import numpy as np 
import pandas as pd
from phishing.pipeline.prediction_pipeline import PredictionPipeline 
from feature_extaction import URLFeatureExtractor

app = Flask(__name__)

# Initialize your pipeline
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
        
        # Create feature extractor with the URL
        feature_extractor = URLFeatureExtractor(url)
        
        # Extract features
        features = feature_extractor.get_features()
        
        # Make prediction (adjust based on your model's input requirements)
        prediction = predictor.predict([features])  # Wrap in list if expecting 2D array
        
        # Prepare response
        result = {
            'is_phishing': bool(prediction[0]),
            'risk_level': 'High' if prediction[0] else 'Low',
            'domain_info': str(features.get('domain_info', '')),
            'threats': ', '.join(features.get('threats', [])),
            'features': features
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')