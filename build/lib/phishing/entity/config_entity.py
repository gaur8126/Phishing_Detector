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