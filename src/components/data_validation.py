import os
import sys
import yaml
import pandas as pd

from src.logger import logger
from src.exception import CustomException

from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import (
    DataValidationArtifact,
    DataIngestionArtifact
)

class DataValidation:

    def __init__(
        self,
        config: DataValidationConfig,
        data_ingestion_artifact: DataIngestionArtifact
    ):
        self.config = config
        self.data_ingestion_artifact = data_ingestion_artifact
    
    def _read_schema(self):
        logger.info("Reading schema file")
        with open(self.config.schema_file, "r") as yaml_file:
            schema = yaml.safe_load(yaml_file)
        logger.info("Schema file loaded successfully")
        return schema
    
    def _validate_single_file(self, file_path, schema):
        logger.info(f"Validating file: {file_path}")
        df = pd.read_csv(file_path)

        expected_columns = list(schema["columns"].keys())
        actual_columns = list(df.columns)

        missing_columns = [col for col in expected_columns if col not in actual_columns]
        extra_columns = [col for col in actual_columns if col not in expected_columns]

        validation_status = (len(missing_columns) == 0 and len(extra_columns) == 0)
        return validation_status, missing_columns, extra_columns
    
    def _validate_columns(self, schema):
        logger.info("Validating Train Dataset")
        train_status, train_missing, train_extra = self._validate_single_file(
            self.data_ingestion_artifact.train_file_path, schema
        )

        logger.info("Validating Test Dataset")
        test_status, test_missing, test_extra = self._validate_single_file(
            self.data_ingestion_artifact.test_file_path, schema
        )

        validation_status = train_status and test_status
        missing_columns = list(set(train_missing + test_missing))
        extra_columns = list(set(train_extra + test_extra))

        return validation_status, missing_columns, extra_columns

    def _validate_datatypes(self, file_path, schema):
        logger.info(f"Validating datatypes for: {file_path}")
        df = pd.read_csv(file_path)
        expected_schema = schema["columns"]
        datatype_errors = {}

        for column, expected_dtype in expected_schema.items():
            # Safeguard: Skip datatype check if the column doesn't even exist
            if column not in df.columns:
                datatype_errors[column] = {
                    "expected": expected_dtype,
                    "actual": "Missing Column"
                }
                continue

            actual_dtype = str(df[column].dtype)
            # Normalize string datatypes across pandas versions
            if expected_dtype == "object" and actual_dtype == "str":
                actual_dtype = "object"

            if actual_dtype != expected_dtype:
                datatype_errors[column] = {
                    "expected": expected_dtype,
                    "actual": actual_dtype
                }
        datatype_status = len(datatype_errors) == 0
        if datatype_status:
            logger.info("Datatype validation passed.")
        else:
            logger.warning(f"Datatype validation failed. Errors: {datatype_errors}")
        return datatype_status, datatype_errors
    
    def _validate_missing_values(self, file_path):
        logger.info(f"Checking missing values in: {file_path}")
        df = pd.read_csv(file_path)
        missing_value_errors = {}
        missing_counts = df.isnull().sum()

        for column, count in missing_counts.items():
            if count > 0:
                missing_value_errors[column] = int(count)

        missing_value_status = len(missing_value_errors) == 0
        if missing_value_status:
            logger.info("Missing value validation passed.")
        else:
            logger.warning(f"Missing value validation failed. Errors: {missing_value_errors}")

        return missing_value_status, missing_value_errors
    
    def _validate_duplicates(self, file_path):
        logger.info(f"Checking duplicate records in: {file_path}")
        df = pd.read_csv(file_path)
        duplicate_count = int(df.duplicated().sum())
        duplicate_status = duplicate_count == 0
        if duplicate_status:
            logger.info("Duplicate validation passed.")
        else:
            logger.warning(
                f"Duplicate validation failed. "
                f"Duplicate rows: {duplicate_count}"
            )
        return duplicate_status, duplicate_count
    def _validate_target_column(self, file_path):

        logger.info(
        f"Validating target column in: {file_path}"
        )
        df = pd.read_csv(file_path)
        target_column = "Machine failure"
        if target_column not in df.columns:
            logger.warning("Target column not found."
        )
            return False, "Target column missing"
        if df[target_column].isnull().sum() > 0:
            logger.warning( "Target column contains missing values."
        )
            return False, "Missing values in target column"
        
        allowed_values = {0, 1}
        actual_values = set(df[target_column].unique())
        
        if not actual_values.issubset(allowed_values):
            logger.warning(f"Invalid target values: {actual_values}"
        )
            return False, actual_values
        
        logger.info("Target column validation passed."
        )
        return True, None
    
    def _run_all_validations(self, schema):
        # 1. Validate Columns
        
        column_validation_status, missing_columns, extra_columns = (self._validate_columns(schema))

        # 2. Validate Datatypes
        train_datatype_status, train_datatype_errors = self._validate_datatypes(
            self.data_ingestion_artifact.train_file_path, schema
        )
        test_datatype_status, test_datatype_errors = self._validate_datatypes(
            self.data_ingestion_artifact.test_file_path, schema
        )

        # 3. Validate Missing Values
        train_missing_status, train_missing_errors = self._validate_missing_values(
            self.data_ingestion_artifact.train_file_path
        )
        test_missing_status, test_missing_errors = self._validate_missing_values(
            self.data_ingestion_artifact.test_file_path
        )
        # duplicate values
        train_duplicate_status, train_duplicate_count = (
            self._validate_duplicates(
                self.data_ingestion_artifact.train_file_path
                )
        )
        test_duplicate_status, test_duplicate_count = (
            self._validate_duplicates(
                self.data_ingestion_artifact.test_file_path
            )
        )
        # validate Target Column
        train_target_status, train_target_error = (
            self._validate_target_column(
                self.data_ingestion_artifact.train_file_path
            )
        )
        test_target_status, test_target_error = (
            self._validate_target_column(
                self.data_ingestion_artifact.test_file_path
            )
        )

        # Combine statuses
        missing_value_status = train_missing_status and test_missing_status
        datatype_status = train_datatype_status and test_datatype_status
        duplicate_status = train_duplicate_status and test_duplicate_status
        target_status = (train_target_status  and test_target_status)

        overall_validation_status = (column_validation_status  and datatype_status and missing_value_status and duplicate_status and target_status)

        logger.info(f"Column Validation Status: {column_validation_status}")
        logger.info(f"Datatype Validation Status: {datatype_status}")
        logger.info(f"Missing Value Validation Status: {missing_value_status}")
        logger.info(f"Duplicate Validation Status: {duplicate_status}")
        logger.info(f"Target Validation Status: {target_status}")
        logger.info(f"Overall Validation Status: {overall_validation_status}")

        validation_results = {

            "validation_status": overall_validation_status,

            "column_validation": {

                "missing_columns": missing_columns,

                "extra_columns": extra_columns

            },

            "datatype_validation": {

                "train": train_datatype_errors,

                "test": test_datatype_errors

            },

            "missing_value_validation": {

                "train": train_missing_errors,

                "test": test_missing_errors

            },

            "duplicate_validation": {

                "train": train_duplicate_count,

                "test": test_duplicate_count

            },

            "target_validation": {

                "train": train_target_error,

                "test": test_target_error

            }

        }
        return overall_validation_status, validation_results



    def _write_validation_report(
        self,validation_results
    ):

        report = validation_results

        report_dir = os.path.join(
        self.config.artifacts_dir,
        self.config.validation_report_dir
        )
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, self.config.validation_report_file)

        with open(report_path, "w") as yaml_file:
            yaml.dump(report, yaml_file, default_flow_style=False)

        logger.info(f"Validation report saved at {report_path}")
        return report_path
        
    def initiate_data_validation(self):
        try:
            logger.info("Starting Data Validation")
            schema = self._read_schema()

            validation_status, validation_results = (
            self._run_all_validations(schema)
            )

            report_path = self._write_validation_report(
                validation_results
            )

            logger.info(f"Validation Report Path: {report_path}")

            return DataValidationArtifact(
                validation_status=validation_status,
                validation_report_file_path=report_path,
                train_file_path=self.data_ingestion_artifact.train_file_path,
                test_file_path=self.data_ingestion_artifact.test_file_path
            )

        except Exception as e:
            logger.exception("Error occurred during data validation")
            raise CustomException(e, sys)