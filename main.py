from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

def main():

    configuration = ConfigurationManager()

    # ==================================
    # Data Ingestion
    # ==================================

    data_ingestion_config = (
        configuration.get_data_ingestion_config()
    )

    data_ingestion = DataIngestion(
        data_ingestion_config
    )

    data_ingestion_artifact = (
        data_ingestion.initiate_data_ingestion()
    )

    print(data_ingestion_artifact)

    # ==================================
    # Data Validation
    # ==================================

    data_validation_config = (
        configuration.get_data_validation_config()
    )

    data_validation = DataValidation(
        config=data_validation_config,
        data_ingestion_artifact=data_ingestion_artifact
    )

    data_validation_artifact = (
        data_validation.initiate_data_validation()
    )

    print(data_validation_artifact)

    # ==================================
    # Data Transformation
    # ==================================

    data_transformation_config = (
        configuration.get_data_transformation_config()
    )

    data_transformation = DataTransformation(
        config=data_transformation_config,
        data_validation_artifact=data_validation_artifact
    )

    data_transformation_artifact = (
        data_transformation.initiate_data_transformation()
    )

    print(data_transformation_artifact)

    # --------------------------
# Model Training
# --------------------------

    model_trainer_config = (
        configuration.get_model_trainer_config()
    )
    model_trainer = ModelTrainer(
    config=model_trainer_config,
    data_transformation_artifact=data_transformation_artifact
    )
    model_trainer_artifact = (
    model_trainer.initiate_model_trainer()
    )
    print(model_trainer_artifact)


if __name__ == "__main__":
    main()