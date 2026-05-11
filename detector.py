import numpy as np
from pyod.models.iforest import IForest
import joblib
import os

class APIDetector:
    def __init__(self, contamination=0.1, random_state=42):
        """
        Initializes the Anomaly Detector using Isolation Forest.
        :param contamination: The amount of contamination of the data set, i.e. the proportion of outliers in the data set.
        """
        self.model = IForest(contamination=contamination, random_state=random_state)
        self.is_trained = False
        self.model_path = os.path.join(os.path.dirname(__file__), 'iforest_model.joblib')

    def train(self, X_train):
        """
        Trains the Isolation Forest model on historical data.
        :param X_train: numpy array of shape (n_samples, n_features)
        """
        self.model.fit(X_train)
        self.is_trained = True
        self._save_model()

    def _save_model(self):
        """Saves the trained model to disk."""
        joblib.dump(self.model, self.model_path)

    def load_model(self):
        """Loads a trained model from disk if it exists."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            return True
        return False

    def predict_risk(self, latency: float, cpu_usage: float, error_count: int) -> str:
        """
        Predicts the failure risk of a given API request.
        Returns 'HIGH FAILURE RISK', 'MEDIUM RISK', or 'NORMAL API'.
        """
        if not self.is_trained:
            # Try loading it
            if not self.load_model():
                raise ValueError("Model is not trained yet. Please train or provide pre-trained model.")

        # Prepare data for prediction
        X = np.array([[latency, cpu_usage, error_count]])
        
        # Get the anomaly probability. 
        # predict_proba returns array of shape (n_samples, 2), where second column is outlier probability
        outlier_prob = self.model.predict_proba(X)[0][1]

        if outlier_prob >= 0.75:
            return "HIGH FAILURE RISK"
        elif outlier_prob >= 0.50:
            return "MEDIUM RISK"
        else:
            return "NORMAL API"
