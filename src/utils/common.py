import yaml
import joblib
import os
import pickle

from src.logger import logger

def save_object(file_path, obj):

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as file_obj:

        pickle.dump(obj, file_obj)

def read_yaml(file_path):
    with open(file_path, "r") as yaml_file:
        return yaml.safe_load(yaml_file)


def save_object(file_path, obj):

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    joblib.dump(obj, file_path)

    logger.info(f"Object saved at: {file_path}")


def load_object(file_path):

    logger.info(f"Loading object: {file_path}")

    return joblib.load(file_path)