import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class ModelTrainer:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.decoder_model = None

    def train(self, historical_data):
        X = historical_data[['density', 'size', 'activity', 'atypical_cells']]
        y = historical_data['label']
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_scaled, y)

        # Compute complex_param for each historical row using the trained model
        params = []
        for _, row in historical_data.iterrows():
            attrs = {
                'density': row['density'],
                'size': row['size'],
                'activity': row['activity'],
                'atypical_cells': row['atypical_cells']
            }
            p = self.compute_complex_param(attrs)
            params.append(p)
        decoder_df = pd.DataFrame({'param': params, 'label': y})

        # Fit decoder_model on param -> label
        self.decoder_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.decoder_model.fit(decoder_df[['param']], decoder_df['label'])

    def compute_complex_param(self, attributes):
        if self.model is None:
            density = int(attributes['density'])
            size = int(attributes['size'])
            activity = int(attributes['activity'])
            atypical_cells = int(attributes['atypical_cells'])
            binary = f"{density}{bin(size)[2:].zfill(2)}{bin(activity)[2:].zfill(2)}{atypical_cells}"
            return int(binary, 2)
        else:
            features = pd.DataFrame([[
                attributes['density'],
                attributes['size'],
                attributes['activity'],
                attributes['atypical_cells']
            ]], columns=['density', 'size', 'activity', 'atypical_cells'])
            scaled_features = self.scaler.transform(features)
            score = self.model.predict_proba(scaled_features)[0][1]
            return int(score * 100)

    # Use decoder_model to predict label and probability from complex_param.
    # Returns (severity (0-1 float), diagnosis (str)).
    def decode_complex_param(self, param):
        severity = float(np.clip(param / 100.0, 0.0, 1.0))

        proba = None
        if hasattr(self.decoder_model, 'predict_proba'):
            proba_arr = self.decoder_model.predict_proba([[param]])[0]
            if len(proba_arr) == 2:
                proba = proba_arr[1]
            else:
                proba = float(max(proba_arr))
        label = self.decoder_model.predict([[param]])[0]
        if proba is not None:
            severity = float(np.clip(proba, 0.0, 1.0))
        return severity, str(label)