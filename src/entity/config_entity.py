from dataclasses import dataclass
@dataclass
class DataIngestionConfig:

    dataset_dir: str

    dataset_name: str

    artifacts_dir: str
    
    raw_data_dir: str

    train_dir: str

    test_dir: str
@dataclass
class DataValidationConfig:

    artifacts_dir: str

    schema_file: str

    validation_report_dir: str

    validation_report_file: str
@dataclass
class DataTransformationConfig:

    artifacts_dir: str

    preprocessor_dir: str

    preprocessor_name: str

    transformed_dir: str

    train_array_name: str

    test_array_name: str

    schema_file: str

@dataclass
class ModelTrainerConfig:
    artifacts_dir: str
    trained_model_dir: str
    trained_model_name: str
    expected_accuracy: float
    overfitting_underfitting_threshold: float
@dataclass
class ModelTrainerConfig:
    artifacts_dir: str
    trained_model_dir: str
    trained_model_name: str