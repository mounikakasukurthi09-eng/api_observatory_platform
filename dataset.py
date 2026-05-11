import numpy as np
import os

def generate_training_data(num_samples=1000, anomaly_fraction=0.1):
    """
    Generates a sample dataset of API monitoring metrics.
    Metrics: [latency (ms), cpu_usage (%), error_count]
    
    Returns:
        X: numpy array of shape (num_samples, 3)
    """
    np.random.seed(42)
    
    num_anomalies = int(num_samples * anomaly_fraction)
    num_normal = num_samples - num_anomalies
    
    # Generate normal traffic
    # latency: normal around 50ms-150ms
    # cpu_usage: normal around 20%-50%
    # error_count: 0 or 1
    normal_latency = np.random.normal(100, 20, num_normal)
    normal_cpu = np.random.normal(35, 10, num_normal)
    normal_errors = np.random.poisson(0.5, num_normal)
    
    normal_data = np.column_stack((normal_latency, normal_cpu, normal_errors))
    
    # Generate anomalous traffic (latency spikes, high cpu, high errors)
    # latency: 500ms - 2000ms
    # cpu_usage: 80% - 100%
    # error_count: 5 - 50
    anom_latency = np.random.uniform(500, 2000, num_anomalies)
    anom_cpu = np.random.uniform(80, 100, num_anomalies)
    anom_errors = np.random.randint(5, 50, num_anomalies)
    
    anomaly_data = np.column_stack((anom_latency, anom_cpu, anom_errors))
    
    # Combine and shuffle
    X = np.vstack((normal_data, anomaly_data))
    np.random.shuffle(X)
    
    # Save to CSV for reference
    data_path = os.path.join(os.path.dirname(__file__), 'sample_monitoring_dataset.csv')
    np.savetxt(data_path, X, delimiter=',', header='latency,cpu_usage,error_count', comments='')
    print(f"Generated {num_samples} samples and saved to {data_path}")
    
    return X

if __name__ == "__main__":
    generate_training_data()
