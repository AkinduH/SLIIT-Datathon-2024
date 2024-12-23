# Solar Power Generation Anomaly Detection

## Project Overview
This project implements anomaly detection for solar power generation systems across two locations (A and B), analyzing sensor data to identify irregular patterns and potential system issues.

## Data Description
The project uses two main datasets:
- `solar_sensor_data.csv`: Contains power generation metrics
- `weather_sensor_data.csv`: Contains environmental measurements

### Key metrics include:
- DC/AC Power
- Daily/Total Yield
- Ambient Temperature
- Module Temperature
- Irradiation

## Features

### 1. Data Preprocessing
- Data preprocessing: Addition of seasonal and time period columns
- Feature engineering: Creation of dummy variables for categorical data
- Sensor-specific analysis: Separate handling for sensors from Locations A and B
- Anomaly detection: Calculations based on z-scores for flagging anomalous readings

### 2. Model Implementation
Four machine learning models were implemented:
- Linear Regression
- Random Forest Regression
- Gradient Boosting Regression
- Convolutional Neural Network (CNN) Autoencoder
    - Used for anomaly detection through reconstruction error
    - Separate models for each sensor
    - Capable of capturing complex temporal patterns in power generation

### 3. Anomaly Detection
- Uses multiple approaches:
    - Z-score based calculations
    - CNN Autoencoder reconstruction error
    - Flags readings that deviate by more than 3 standard deviations
- Separate analysis for each sensor location

## Model Performance

### Linear Regression
- **Location A**  
    - Average Mean Squared Error (MSE): 986.0062 
    - Average R² Score: 0.9923 
- **Location B**  
    - Average Mean Squared Error (MSE): 15839.6510  
    - Average R² Score: 0.8606  

### Random Forest Regression
- **Location A**  
    - Average Mean Squared Error (MSE): 417.4443 
    - Average R² Score: 0.9967 
- **Location B**  
    - Average Mean Squared Error (MSE): 317.8780  
    - Average R² Score: 0.9974  

### Gradient Boosting Regression
- **Location A**  
    - Average Mean Squared Error (MSE): 425.1359  
    - Average R² Score: 0.9966  
- **Location B**  
    - Average Mean Squared Error (MSE): 223.5140 
    - Average R² Score: 0.9982

### CNN Autoencoder
- Implemented in separate notebooks for each sensor
- Uses reconstruction error to identify anomalies
- Features:
    - Input: Time series of power generation data
    - Architecture: Multiple convolutional layers for feature extraction
    - Output: Reconstructed power generation patterns
    - Anomaly Detection: Based on reconstruction error threshold

## Key Findings
1. Location A generally showed better model performance than Location B
2. Random Forest and Gradient Boosting models outperformed Linear Regression
3. Multiple anomalies were detected across different sensors
4. Weather conditions significantly impact power generation patterns

## Project Structure
- `Data_Preparation.ipynb`: Initial data processing and cleaning
- `CNN_Autoencoders sensor*.ipynb`: Sensor-specific analysis
- `Models and results/`: Contains model implementations and analysis reports
- `LR-RF-GBR.ipynb`: Implementation of the three main regression models

## Usage
1. Load and preprocess the data using `Data_Preparation.ipynb`
2. Run individual sensor analysis notebooks:
    - Traditional models: `LR-RF-GBR.ipynb`
    - CNN models: `CNN_Autoencoders sensor*.ipynb`
3. Review results in the Reports directory

## Results
The project successfully identified anomalies using multiple approaches:
- Traditional Models:
    - Best performance: Gradient Boosting (R² > 0.99)
- CNN Autoencoder:
    - Effective at capturing complex patterns
    - Visual confirmation of anomaly detection through reconstruction plots
    - Sensor-specific analysis providing detailed insights
