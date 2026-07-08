import os
import sys


from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.logger import logger
from src.exception import CustomException

import pandas as pd
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self):

        try:

            logger.info("Starting Data Ingestion")

            # Build source path
            dataset_path = os.path.join(
                self.config.dataset_dir,
                self.config.dataset_name
            )

            logger.info(f"Source dataset: {dataset_path}")

            # Verify source file exists
            if not os.path.exists(dataset_path):
                raise FileNotFoundError(
                    f"Dataset not found at: {dataset_path}"
                )

            # -----------------------------
            # Read Dataset
            # -----------------------------
            logger.info("Reading dataset")

            df = pd.read_csv(dataset_path)

            # -----------------------------
            # Save Raw Dataset
            # -----------------------------
            raw_data_path = os.path.join(
                self.config.artifacts_dir,
                self.config.raw_data_dir,
                self.config.dataset_name
            )

            os.makedirs(
                os.path.dirname(raw_data_path),
                exist_ok=True
            )

            df.to_csv(
                raw_data_path,
                index=False
            )

            logger.info(f"Raw dataset saved at: {raw_data_path}")

            # -----------------------------
            # Train/Test Split
            # -----------------------------
            logger.info("Splitting dataset into train and test")

            train_df, test_df = train_test_split(
                df,
                test_size=0.2,
                random_state=42
            )

            # -----------------------------
            # Train and Test File Paths
            # -----------------------------
            train_path = os.path.join(
                self.config.artifacts_dir,
                self.config.train_dir,
                "train.csv"
            )

            test_path = os.path.join(
                self.config.artifacts_dir,  
                self.config.test_dir,
                "test.csv"
            )

            os.makedirs(
                os.path.dirname(train_path),
                exist_ok=True
            )

            os.makedirs(
                os.path.dirname(test_path),
                exist_ok=True
            )

            # -----------------------------
            # Save Train/Test Data
            # -----------------------------
            train_df.to_csv(
                train_path,
                index=False
            )

            test_df.to_csv(
                test_path,
                index=False
            )

            logger.info(f"Train dataset saved at: {train_path}")
            logger.info(f"Test dataset saved at: {test_path}")

            logger.info("Creating DataIngestionArtifact")

            return DataIngestionArtifact(
                raw_data_file_path=raw_data_path,
                train_file_path=train_path,
                test_file_path=test_path
            )

        except Exception as e:

            logger.error(str(e))

            raise CustomException(e, sys)