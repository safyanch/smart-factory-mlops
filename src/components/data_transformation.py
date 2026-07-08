import os
import sys
import joblib
import numpy as np
import pandas as pd

from src.logger import logger
from src.exception import CustomException

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import (
    DataValidationArtifact,
    DataTransformationArtifact,
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder
)
from src.utils.common import read_yaml, save_object
class DataTransformation:

    def __init__(
        self,
        config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact
    ):
        self.config = config
        self.data_validation_artifact = data_validation_artifact

    def _get_data_transformer_object(self):
        logger.info("Creating preprocessing pipeline")
        schema = read_yaml(self.config.schema_file)
        numerical_columns = schema["numerical_columns"]
        categorical_columns = schema["categorical_columns"]
        
        numerical_pipeline = Pipeline(
            steps=[
                (
                    "scaler",
                    StandardScaler()
                )
            ]
        )
        categorical_pipeline = Pipeline(
            steps=[
                (
                    "encoder",
                    OneHotEncoder(handle_unknown="ignore")
                )
            ]
        )
        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "numerical",
                    numerical_pipeline,
                    numerical_columns
                ),
                (
                    "categorical",
                    categorical_pipeline,
                    categorical_columns
                )
            ]
        )
        return preprocessor
            
    def _save_preprocessor(self,    preprocessor):

        preprocessor_dir = os.path.join(
        self.config.artifacts_dir,
        self.config.preprocessor_dir
    )

        os.makedirs(
            preprocessor_dir,
            exist_ok=True
        )

        preprocessor_path = os.path.join(
            preprocessor_dir,
            self.config.preprocessor_name
        )

        joblib.dump(
            preprocessor,
            preprocessor_path
        )

        logger.info(
            f"Preprocessor saved at: {preprocessor_path}"
        )

        return preprocessor_path

    def _save_transformed_data(
        self,
        train_array,
        test_array
    ):
        transformed_dir = os.path.join(
            self.config.artifacts_dir,
            self.config.transformed_dir
        )
        os.makedirs(
            transformed_dir,
            exist_ok=True
        )
        train_path = os.path.join(
            transformed_dir,
            self.config.train_array_name
        )
        test_path = os.path.join(
            transformed_dir,
            self.config.test_array_name
        )
        np.save(
            train_path,
            train_array
        )

        np.save(
            test_path,
            test_array
        )

        logger.info(
            f"Train array saved at: {train_path}"
        )

        logger.info(
            f"Test array saved at: {test_path}"
        )

        return train_path, test_path

    def initiate_data_transformation(self):
        try:
            logger.info("Starting Data Transformation")
            # ============================
            # Read Train & Test Datasets
            # ============================
            train_df = pd.read_csv(
                self.data_validation_artifact.train_file_path
            )
            test_df = pd.read_csv(
                self.data_validation_artifact.test_file_path
            )
            logger.info("Train and Test datasets loaded successfully.")

            # ============================
            # Separate Features & Target
            # ============================
            schema = read_yaml(self.config.schema_file)
            target_column = schema["target_column"]
            target_column = "Machine failure"
            X_train = train_df.drop(
                columns=[target_column]
            )
            y_train = train_df[target_column]

            X_test = test_df.drop(
                columns=[target_column]
            )
            y_test = test_df[target_column]
            logger.info("Separated input features and target column.")
            # ============================
            # Build Preprocessor
            # ============================

            preprocessor = (
                self._get_data_transformer_object()
            )

            logger.info("Preprocessor object created.")
            # ============================
            # Transform Training Data
            # ============================
            X_train_transformed = (
                preprocessor.fit_transform(X_train)
            )
            logger.info("Training data transformed.")
           # ============================
            # Transform Testing Data
            # ============================
            X_test_transformed = (
                preprocessor.transform(X_test)
            )
            logger.info("Testing data transformed.")
            # ============================
            # Combine Features + Target
            # ============================
            train_array = np.c_[
                X_train_transformed,
                np.array(y_train)
            ]
            test_array = np.c_[
                X_test_transformed,
                np.array(y_test)
            ]

            logger.info("Train and Test arrays created successfully.")
            # Step 8 will save these objects.
            preprocessor_path = self._save_preprocessor(preprocessor)

            train_path, test_path = (
                self._save_transformed_data(
                    train_array,
                    test_array
                )
            )

            logger.info(
                "Creating DataTransformationArtifact"
            )

            return DataTransformationArtifact(

                transformed_train_file_path=train_path,

                transformed_test_file_path=test_path,

                preprocessor_file_path=preprocessor_path

            )
        except Exception as e:
            logger.exception(
                "Error occurred during Data Transformation."
            )
            raise CustomException(e, sys)