import os
import sys

import numpy as np

from src.logger import logger
from src.exception import CustomException
from src.entity.artifact_entity import ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
    ExtraTreesClassifier
)
from src.utils.common import save_object

from sklearn.metrics import accuracy_score

class ModelTrainer:

    def __init__(
        self,
        config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact
    ):

        self.config = config
        self.data_transformation_artifact = data_transformation_artifact
    def _load_data(self):

        logger.info("Loading transformed training and testing arrays")

        train_arr = np.load(
            self.data_transformation_artifact.transformed_train_file_path
        )

        test_arr = np.load(
            self.data_transformation_artifact.transformed_test_file_path
        )

        logger.info("Training and testing arrays loaded successfully")

        return train_arr, test_arr
    def _split_features_target(self, train_arr, test_arr):

        logger.info("Splitting input features and target column")
        X_train = train_arr[:, :-1]
        y_train = train_arr[:, -1]

        X_test = test_arr[:, :-1]
        y_test = test_arr[:, -1]
        logger.info("Feature-target split completed successfully")
        return X_train, y_train, X_test, y_test

    def _train_models(self, X_train, y_train):

        logger.info("Initializing machine learning models")

        models = {
            "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "Random Forest": RandomForestClassifier(random_state=42),
            "Gradient Boosting": GradientBoostingClassifier(random_state=42),
            "AdaBoost": AdaBoostClassifier(random_state=42),
            "Extra Trees": ExtraTreesClassifier(random_state=42)
        }

        logger.info("Training models...")

        for model_name, model in models.items():

            logger.info(f"Training {model_name}")

            model.fit(X_train, y_train)

        logger.info("All models trained successfully.")

        return models

    def _evaluate_models(
        self,
        models,
        X_train,
        y_train,
        X_test,
        y_test
    ):

        logger.info("Evaluating trained models")
        model_report = {}
        for model_name, model in models.items():
            train_prediction = model.predict(X_train)
            test_prediction = model.predict(X_test)
            train_accuracy = accuracy_score(
                y_train,
                train_prediction
            )
            test_accuracy = accuracy_score(
                y_test,
                test_prediction
            )
            model_report[model_name] = {
                "model": model,
                "train_accuracy": train_accuracy,
                "test_accuracy": test_accuracy
            }
            logger.info(
                f"{model_name} | "
                f"Train Accuracy: {train_accuracy:.4f} | "
                f"Test Accuracy: {test_accuracy:.4f}"
            )
        logger.info("Model evaluation completed.")
        return model_report
    
    def _select_best_model(self, model_report):

        logger.info("Selecting the best model")

        best_model_name = None
        best_model = None
        best_test_accuracy = -1
        for model_name, model_info in model_report.items():
            test_accuracy = model_info["test_accuracy"]
            if test_accuracy > best_test_accuracy:
                best_test_accuracy = test_accuracy
                best_model_name = model_name
                best_model = model_info["model"]
        logger.info(
            f"Best Model: {best_model_name}"
        )
        logger.info(
            f"Best Test Accuracy: {best_test_accuracy:.4f}"
        )
        return (
            best_model_name,
            best_model,
            best_test_accuracy
        )
    def _save_model(self, model):

        logger.info("Saving the trained model")

        model_path = os.path.join(
            self.config.artifacts_dir,
            self.config.trained_model_dir,
            self.config.trained_model_name
        )

        save_object(
            file_path=model_path,
            obj=model
        )

        logger.info(
            f"Model saved successfully at: {model_path}"
        )

        return model_path


    def initiate_model_trainer(self):

        try:

            logger.info("Starting Model Training")

            train_arr, test_arr = self._load_data()
            X_train, y_train, X_test, y_test = (
            self._split_features_target(train_arr,test_arr))
            
            models = self._train_models(X_train,y_train)

            model_report = self._evaluate_models(
                models,
                X_train,
                y_train,
                X_test,
                y_test
            )

            best_model_name, best_model, best_test_accuracy = (
        self._select_best_model(
        model_report
        )
    )
            model_path = self._save_model(best_model)

            logger.info(f"X_train Shape: {X_train.shape}")
            logger.info(f"y_train Shape: {y_train.shape}")

            logger.info(f"X_test Shape: {X_test.shape}")
            logger.info(f"y_test Shape: {y_test.shape}")

            #logger.info(f"Train Array Shape: {train_arr.shape}")
            #logger.info(f"Test Array Shape: {test_arr.shape}")
            return ModelTrainerArtifact(
                trained_model_file_path=model_path,
                best_model_name=best_model_name,
                train_accuracy=model_report[best_model_name]["train_accuracy"],
                test_accuracy=best_test_accuracy
            )
        except Exception as e:

            logger.exception("Error occurred during model training")

            raise CustomException(e, sys)