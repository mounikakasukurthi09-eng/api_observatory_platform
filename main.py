from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Add the parent directory to the python path to allow imports when running uvicorn
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.detector import APIDetector
from monitoring.metrics import metrics_tracker
from utils.logger import get_logger
from simulation.dataset import generate_training_data

logger = get_logger(__name__)

app = FastAPI(
    title="API Predictive Observability Platform",
    description="AI-Powered Anomaly Detection for API Failures",
    version="1.0.0"
)

detector = APIDetector()

class APIRequestData(BaseModel):
    latency: float
    cpu_usage: float
    error_count: int

@app.on_event("startup")
async def startup_event():
    """
    On startup, check if the model is trained. If not, generate sample data and train it.
    """
    logger.info("Initializing API Predictive Observability Platform...")
    if not detector.load_model():
        logger.info("No pre-trained model found. Generating sample data and training a new model...")
        X_train = generate_training_data(num_samples=2000, anomaly_fraction=0.1)
        detector.train(X_train)
        logger.info("Model training complete.")
    else:
        logger.info("Loaded pre-trained Isolation Forest model.")

@app.post("/predict_failure")
async def predict_failure(data: APIRequestData):
    """
    Predicts the failure risk of an API based on latency, CPU usage, and error count.
    """
    try:
        risk_level = detector.predict_risk(
            latency=data.latency,
            cpu_usage=data.cpu_usage,
            error_count=data.error_count
        )
        
        # Record the prediction in our metrics tracker
        metrics_tracker.record_prediction(risk_level)
        
        return {
            "latency": data.latency,
            "cpu_usage": data.cpu_usage,
            "error_count": data.error_count,
            "prediction": risk_level
        }
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during prediction.")

@app.get("/metrics")
async def get_metrics():
    """
    Returns the current statistics of API predictions.
    """
    return metrics_tracker.get_stats()
