# PROJECT_ROADMAP.md

# Smart Factory MLOps Project Roadmap

## Project Overview

**Project Title:** Smart Factory Predictive Maintenance System

### Objective

Build a production-grade end-to-end Machine Learning system capable of predicting machine failures using sensor data. The project will evolve from an offline ML pipeline into a complete MLOps system with cloud deployment, real-time streaming, automated retraining, monitoring, logging, and CI/CD.

The project is designed to simulate how a real ML Engineering team develops, deploys, and maintains production Machine Learning systems.

---

# Final Architecture (Target)

The completed system will include:

* Offline Machine Learning Pipeline
* FastAPI Prediction Service
* Docker & Docker Compose
* Kafka Streaming
* Spark Structured Streaming
* PostgreSQL
* Data Lake
* Apache Airflow
* MLflow
* AWS Deployment
* GitHub Actions (CI/CD)
* Prometheus
* Grafana
* Data Drift Detection
* Model Drift Detection
* Automated Retraining
* Production Monitoring
* Logging & Alerting

---

# Overall Roadmap

## Month 1 — Offline ML Pipeline

* Project Setup
* Configuration Management
* Logging
* Exception Handling
* Data Ingestion
* Data Validation
* Data Transformation
* Model Training
* Model Evaluation

## Month 2 — API & Packaging

* FastAPI
* Pydantic
* Docker
* Docker Compose
* Local Deployment

## Month 3 — Real-Time Streaming

* Kafka
* Spark Structured Streaming
* Real-Time Predictions
* PostgreSQL
* Data Lake

## Month 4 — Cloud & Orchestration

* AWS (AWS Academy)
* Airflow
* MLflow
* Model Registry
* Automated Retraining

## Month 5 — Production Monitoring

* Prometheus
* Grafana
* Data Drift
* Model Drift
* Logging
* Alerting

## Month 6 — CI/CD & Production Deployment

* GitHub Actions
* Automated Testing
* Automated Docker Build
* Automated Deployment
* Production MLOps Pipeline

---

# Project Structure

```text
smart-factory-mlops/

artifacts/
config/
data/
logs/
src/

main.py
requirements.txt
README.md
PROJECT_ROADMAP.md
```

---

# Source Structure

```text
src/

components/
config/
entity/
pipeline/
utils/

logger.py
exception.py
```

---

# Configuration Philosophy

The project follows **configuration-driven development**.

Configuration values should be stored in YAML files instead of hardcoded inside Python code.

Current configuration files:

```text
config/

config.yaml
schema.yaml
```

---

# Development Principles

The project follows:

* Modular Design
* Single Responsibility Principle (SRP)
* Configuration Driven Development
* Artifact-Based Pipeline
* Logging First
* Custom Exception Handling
* Object-Oriented Design
* Production-Level Folder Structure

---

# Month 1

---

# Week 1 ✅ Completed

## Objective

Create the project foundation.

## Completed Tasks

* Created Python virtual environment
* Installed project dependencies
* Created Git repository
* Connected GitHub repository
* Created project folder structure
* Implemented logging
* Implemented custom exception handling
* Created configuration folder
* Created `config.yaml`
* Added `requirements.txt`
* Implemented `ConfigurationManager`
* Created basic project entry point (`main.py`)

## Concepts Learned

* Virtual Environments
* Git Workflow
* Project Organization
* Logging
* Exception Handling
* YAML Configuration
* Configuration Manager

---

# Week 2 ✅ Completed

## Objective

Build a production-style Data Ingestion component.

## Components Developed

### Configuration

* ConfigurationManager
* DataIngestionConfig

### Entities

* DataIngestionArtifact

### Component

* DataIngestion

---

## Implemented Features

* Read dataset using Pandas
* Validate dataset existence
* Logging
* Custom Exception Handling
* Train/Test Split
* Save raw dataset
* Save training dataset
* Save testing dataset
* Return DataIngestionArtifact

---

## Current Artifact Structure

```text
artifacts/

raw_data/
    predictive_maintenance.csv

train/
    train.csv

test/
    test.csv
```

---

## DataIngestionArtifact

Current outputs:

* raw_data_file_path
* train_file_path
* test_file_path

---

## Current Configuration

```yaml
artifacts_dir: artifacts

data_ingestion:

  dataset_dir: data

  dataset_name: predictive_maintenance.csv

  raw_data_dir: raw_data

  train_dir: train

  test_dir: test
```

---

## Current Pipeline

```text
Dataset
    │
    ▼
ConfigurationManager
    │
    ▼
DataIngestionConfig
    │
    ▼
DataIngestion
    │
    ▼
Read Dataset
    │
    ▼
Save Raw Dataset
    │
    ▼
Train/Test Split
    │
    ├────────► train.csv
    │
    └────────► test.csv
    │
    ▼
DataIngestionArtifact
```

---

# Folder Status

## Completed

```text
artifacts/

raw_data/
train/
test/
```

## Not Yet Created

```text
validation/
preprocessor/
model/
metrics/
prediction_logs/
```

These folders will be created in later stages of the project.

---

# Technologies Used So Far

* Python
* Pandas
* Scikit-learn
* YAML
* Dataclasses
* Logging
* Git
* GitHub

---

# Current Progress

Month 1

Week 1 — ✅ Completed

Week 2 — ✅ Completed

Week 3 — ⏳ Ready to Start

---

---

# Week 3 ✅ Completed

## Objective

Design and implement a production-style Data Validation component to ensure the quality and integrity of data before it enters the preprocessing and model training stages.

---

## Components Developed

### Configuration

* DataValidationConfig

### Entities

* DataValidationArtifact

### Component

* DataValidation

---

## Validation Checks Implemented

### Schema Validation

* Load schema from `config/schema.yaml`
* Validate expected columns
* Detect missing columns
* Detect unexpected (extra) columns

### Datatype Validation

* Validate each column datatype against the schema
* Handle Pandas string/object compatibility (`str` ↔ `object`)
* Generate detailed datatype error reports

### Missing Value Validation

* Validate training dataset
* Validate testing dataset
* Report missing values for every affected column

### Duplicate Record Validation

* Detect duplicate rows
* Report duplicate counts separately for train and test datasets

### Target Column Validation

* Verify target column exists
* Verify target column contains no missing values
* Validate binary target values (`0` and `1`)

---

## Validation Report

Implemented automatic generation of:

```text
artifacts/

validation/
    validation_report.yaml
```

Example report structure:

```yaml
validation_status: true

column_validation:
  missing_columns: []
  extra_columns: []

datatype_validation:
  train: {}
  test: {}

missing_value_validation:
  train: {}
  test: {}

duplicate_validation:
  train: 0
  test: 0

target_validation:
  train: null
  test: null
```

---

## Logging Improvements

Implemented detailed logging for every validation stage:

* Schema loading
* Column validation
* Datatype validation
* Missing value validation
* Duplicate validation
* Target validation
* Validation report generation

---

## Exception Handling

Integrated `CustomException` across the Data Validation component to ensure clear and consistent error reporting.

---

## Refactoring

Improved the architecture by separating responsibilities into dedicated methods:

* `_read_schema()`
* `_validate_columns()`
* `_validate_datatypes()`
* `_validate_missing_values()`
* `_validate_duplicates()`
* `_validate_target_column()`
* `_run_all_validations()`
* `_write_validation_report()`
* `initiate_data_validation()`

This refactoring makes the component easier to maintain, extend, and test.

---

## Current Artifact Structure

```text
artifacts/

raw_data/
    predictive_maintenance.csv

train/
    train.csv

test/
    test.csv

validation/
    validation_report.yaml
```

---

## DataValidationArtifact

Current outputs:

* validation_status
* validation_report_file_path

---

## Updated Pipeline

```text
Dataset
    │
    ▼
Data Ingestion
    │
    ▼
Train/Test Split
    │
    ├────────► train.csv
    │
    └────────► test.csv
    │
    ▼
Data Validation
    │
    ├── Schema Validation
    ├── Column Validation
    ├── Datatype Validation
    ├── Missing Value Validation
    ├── Duplicate Validation
    ├── Target Validation
    │
    ▼
validation_report.yaml
    │
    ▼
DataValidationArtifact
```

---

## Concepts Learned

* Data Validation Pipeline
* Schema-Driven Validation
* YAML Schema Management
* Datatype Validation
* Missing Value Detection
* Duplicate Detection
* Target Validation
* Validation Reporting
* Production Logging
* Refactoring
* Single Responsibility Principle (SRP)

---

## Folder Status

### Completed

```text
artifacts/

raw_data/
train/
test/
validation/
```

### Not Yet Created

```text
preprocessor/
model/
metrics/
prediction_logs/
```

These folders will be created during the Data Transformation, Model Training, and Deployment phases.

---

## Technologies Used So Far

* Python
* Pandas
* NumPy
* Scikit-learn
* YAML
* Dataclasses
* Logging
* Git
* GitHub

---
# Week 4 ✅ Completed

## Objective

Build a production-grade Data Transformation component that prepares validated data for Machine Learning model training.

---

## Components Developed

### Configuration

* DataTransformationConfig

### Entities

* DataTransformationArtifact

### Component

* DataTransformation

---

## Implemented Features

### Data Loading

* Read validated train dataset
* Read validated test dataset

### Schema Driven Transformation

* Read target column from `schema.yaml`
* Read numerical feature list from `schema.yaml`
* Read categorical feature list from `schema.yaml`

### Feature Engineering

* Separate input features (X)
* Separate target variable (y)

### Numerical Pipeline

* StandardScaler

### Categorical Pipeline

* OneHotEncoder

### ColumnTransformer

* Combined numerical and categorical preprocessing
* Configuration-driven feature selection

### Preprocessor Serialization

* Saved fitted preprocessing pipeline as:

  * `preprocessor.pkl`

### Dataset Transformation

Generated:

* `train.npy`
* `test.npy`

---

## Utility Functions Added

Created reusable utilities in:

`src/utils/common.py`

Functions:

* read_yaml()
* save_object()
* load_object()

---

## Artifact Structure

Current artifacts:

```text
artifacts/

raw_data/
    predictive_maintenance.csv

train/
    train.csv

test/
    test.csv

validation/
    validation_report.yaml

preprocessor/
    preprocessor.pkl

transformed/
    train.npy
    test.npy
```

---

## DataTransformationArtifact

Current outputs:

* transformed_train_file_path
* transformed_test_file_path
* preprocessor_file_path

---

## Architecture Improvements

* Removed hardcoded target column
* Removed hardcoded feature lists
* Configuration-driven preprocessing
* Introduced reusable utility functions
* Improved component modularity
* Reused YAML configuration across components

---

## Technologies Used

* Pandas
* NumPy
* Scikit-learn
* Pipeline
* ColumnTransformer
* StandardScaler
* OneHotEncoder
* Joblib
* YAML
* Logging
* Dataclasses

---

# Current Progress

Month 1

* Week 1 — ✅ Completed
* Week 2 — ✅ Completed
* Week 3 — ✅ Completed
* Week 4 — ✅ Completed
* Week 5 — ⏳ Ready to Start
* Week 6 — ⏳ Pending

---

# Next Milestone

## Month 1 — Week 5

### Model Training

Topics to implement:

* ModelTrainerConfig
* ModelTrainerArtifact
* ModelTrainer Component
* Load transformed datasets
* Train multiple ML models
* Compare model performance
* Select best model
* Save trained model
* Generate ModelTrainerArtifact

---

## Current Status

**Project Phase:** Offline ML Pipeline

**Current Month:** Month 1

**Current Week:** Week 5

**Next Task:** Design and implement the Model Training component.

