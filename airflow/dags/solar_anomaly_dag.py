from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import os

# Constants
DATA_PATH = "Datasets/sensor_wise_data/"
LOCATION_A_SENSORS = [
    "A1_df", "A2_df", "A3_df", "A5_df", "A12_df", "A19_df", "A20_df", 
    "A23_df", "A24_df", "A25_df", "A26_df", "A27_df", "A28_df", 
    "A32_df", "A34_df", "A36_df", "A37_df", "A39_df", "A42_df", 
    "A43_df", "A44_df", "A45_df"
]

LOCATION_B_SENSORS = [
    "B4_df", "B6_df", "B8_df", "B9_df", "B10_df", "B11_df", "B13_df", 
    "B14_df", "B15_df", "B16_df", "B17_df", "B18_df", "B21_df", 
    "B29_df", "B30_df", "B31_df", "B33_df", "B35_df", "B38_df", 
    "B40_df", "B41_df"
]

def preprocess_data(**context):
    """
    Preprocesses solar panel data by:
    1. Loading sensor data
    2. Cleaning and standardizing features
    3. Storing processed data for anomaly detection
    """
    processed_data = {}
    
    # Process both locations
    for sensor_id in LOCATION_A_SENSORS + LOCATION_B_SENSORS:
        try:
            # Load sensor data
            df = pd.read_csv(f"{DATA_PATH}{sensor_id}.csv")
            
            # Drop non-numerical columns and select relevant features
            features = ['DC_POWER', 'AC_POWER', 'DAILY_YIELD', 'AMBIENT_TEMPERATURE', 
                       'MODULE_TEMPERATURE', 'IRRADIATION']
            df_clean = df[features]
            
            # Handle missing values
            df_clean = df_clean.fillna(method='ffill')
            
            # Store processed data
            processed_data[sensor_id] = df_clean
            
            print(f"Processed {sensor_id} successfully")
            
        except Exception as e:
            print(f"Error processing {sensor_id}: {str(e)}")
    
    # Pass processed data to the next task
    context['task_instance'].xcom_push(key='processed_data', value=processed_data)
    print("Data preprocessing completed.")

def detect_anomalies(**context):
    """
    Detects anomalies in solar panel data using Isolation Forest:
    1. Retrieves processed data
    2. Applies Isolation Forest algorithm
    3. Labels anomalies and stores results
    """
    # Retrieve processed data
    processed_data = context['task_instance'].xcom_pull(key='processed_data')
    anomaly_results = {}
    
    for sensor_id, data in processed_data.items():
        try:
            # Initialize and fit Isolation Forest
            iso_forest = IsolationForest(
                contamination=0.1,  # Expected percentage of anomalies
                random_state=42
            )
            
            # Standardize features
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data)
            
            # Detect anomalies
            anomaly_labels = iso_forest.fit_predict(scaled_data)
            
            # Store results (-1 for anomalies, 1 for normal data)
            anomaly_results[sensor_id] = {
                'data': data,
                'anomaly_labels': anomaly_labels
            }
            
            print(f"Detected anomalies for {sensor_id}")
            
        except Exception as e:
            print(f"Error detecting anomalies for {sensor_id}: {str(e)}")
    
    # Pass results to the next task
    context['task_instance'].xcom_push(key='anomaly_results', value=anomaly_results)
    print("Anomaly detection completed.")

def load_to_db(**context):
    """
    Saves anomaly detection results:
    1. Retrieves anomaly results
    2. Formats results for storage
    3. Saves to database or file system
    """
    # Retrieve anomaly results
    anomaly_results = context['task_instance'].xcom_pull(key='anomaly_results')
    
    for sensor_id, results in anomaly_results.items():
        try:
            # Create results DataFrame
            df_results = results['data'].copy()
            df_results['is_anomaly'] = results['anomaly_labels'] == -1
            
            # Save results (modify this part based on your storage requirements)
            output_path = f"output/anomalies_{sensor_id}.csv"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df_results.to_csv(output_path, index=False)
            
            print(f"Saved results for {sensor_id}")
            
        except Exception as e:
            print(f"Error saving results for {sensor_id}: {str(e)}")
    
    print("Results saved successfully.")

# Default arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='solar_anomaly_detection',
    default_args=default_args,
    description='A DAG for solar anomaly detection',
    schedule_interval='@daily',
    start_date=datetime(2023, 12, 1),
    catchup=False,
) as dag:
    
    # Define tasks
    task_preprocess = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data
    )
    
    task_detect = PythonOperator(
        task_id='detect_anomalies',
        python_callable=detect_anomalies
    )
    
    task_load = PythonOperator(
        task_id='load_to_db',
        python_callable=load_to_db
    )

    # Set task dependencies
    task_preprocess >> task_detect >> task_load
