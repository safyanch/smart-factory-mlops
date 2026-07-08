import yaml

from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig
)
class ConfigurationManager:

    def __init__(self,
                 config_filepath="config/config.yaml"):

        with open(config_filepath,"r") as yaml_file:

            self.config = yaml.safe_load(yaml_file)
    def get_data_ingestion_config(self):

        config = self.config

        return DataIngestionConfig(

        dataset_dir=config["data_ingestion"]["dataset_dir"],

        dataset_name=config["data_ingestion"]["dataset_name"],

        artifacts_dir=config["artifacts_dir"],

        raw_data_dir=config["data_ingestion"]["raw_data_dir"],

        train_dir=config["data_ingestion"]["train_dir"],

        test_dir=config["data_ingestion"]["test_dir"]

        )
    
    def get_data_validation_config(self):

        config = self.config

        return DataValidationConfig(

        artifacts_dir=config["artifacts_dir"],

        schema_file=config["data_validation"]["schema_file"],

        validation_report_dir=config["data_validation"]["validation_report_dir"],

        validation_report_file=config["data_validation"]["validation_report_file"]

        )
    def get_data_transformation_config(self) -> DataTransformationConfig:

        config = self.config

        return DataTransformationConfig(

        artifacts_dir=config["artifacts_dir"],

        preprocessor_dir=config["data_transformation"]["preprocessor_dir"],

        preprocessor_name=config["data_transformation"]["preprocessor_name"],

        transformed_dir=config["data_transformation"]["transformed_dir"],

        train_array_name=config["data_transformation"]["train_array_name"],

        test_array_name=config["data_transformation"]["test_array_name"],
        schema_file=config["data_validation"]["schema_file"]

    )