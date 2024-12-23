# Use the Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set Airflow home directory
ENV AIRFLOW_HOME=/app/airflow

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Initialize Airflow database
RUN airflow db init

# Create a new Airflow user
RUN airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Copy DAGs
COPY solar_anomaly_dag.py $AIRFLOW_HOME/dags/

# Copy all datasets at once
COPY ./sensor_wise_data $AIRFLOW_HOME/dags/Datasets/sensor_wise_data/

# Expose the Airflow webserver port
EXPOSE 8080

# Command to start the Airflow scheduler and webserver
CMD ["bash", "-c", "airflow webserver & airflow scheduler"]
