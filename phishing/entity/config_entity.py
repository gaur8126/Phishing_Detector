from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    feature_store_file_path : Path
    training_file_path : Path
    testing_file_path : Path

@dataclass
class DataValidationConfig:
    root_dir:Path
    data_dir : Path
    STATUS_FILE:str
    all_schema: dict

@dataclass
class DataTransformationConfig:
    root_dir : Path
    data_path : Path

@dataclass
class ModelTrainerConfig:
    root_dir: Path
    train_data_path : Path
    test_data_path :Path
    model_name: str
    target_column: str


@dataclass
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    metric_file_name : Path
    target_column : str