from utils.logger import get_logger

logger = get_logger(__name__)

class MetricsTracker:
    """
    Tracks API metrics and anomaly predictions.
    Contains placeholders for Prometheus and Grafana integration.
    """
    def __init__(self):
        self.total_requests = 0
        self.high_risk_requests = 0
        self.medium_risk_requests = 0
        self.normal_requests = 0

    def record_prediction(self, risk_level: str):
        """
        Updates internal counters based on the prediction.
        """
        self.total_requests += 1
        if risk_level == "HIGH FAILURE RISK":
            self.high_risk_requests += 1
        elif risk_level == "MEDIUM RISK":
            self.medium_risk_requests += 1
        elif risk_level == "NORMAL API":
            self.normal_requests += 1
            
        # [PLACEHOLDER] Prometheus Metrics
        # e.g., prometheus_client.Counter('api_requests_total', '...').inc()
        # e.g., prometheus_client.Counter('api_anomalies_total', '...', ['risk_level']).labels(risk_level).inc()
        
        logger.info(f"Recorded prediction: {risk_level} | Total Requests: {self.total_requests}")

    def get_stats(self):
        """
        Returns the current statistics.
        """
        return {
            "total_requests": self.total_requests,
            "high_risk_requests": self.high_risk_requests,
            "medium_risk_requests": self.medium_risk_requests,
            "normal_requests": self.normal_requests
        }

# Global instance for the FastAPI app to use
metrics_tracker = MetricsTracker()
