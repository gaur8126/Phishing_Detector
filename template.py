import os
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO,format='[%(asctime)s] : %(message)s:')


project_name = "phishing_detector"


list_of_files = [
    f"phishing/__init__.py",
    f"phishing/components/__init__.py",
    f"phishing/pipeline/__init__.py",
    f"phishing/logging/__init__.py",
    f"phishing/exception/__init__.py",
    f"phishing/entity/__init__.py",
    f"phishing/utils/__init__.py",
    f"phishing/constant/__init__.py",
    "main.py",
    "setup.py",

]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)
    
    if filedir != "":
      os.makedirs(filedir,exist_ok=True)
      logging.info(f"Creating directory: {filedir} for the file {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,"w") as f:
          pass
          logging.info(f"Creating emptyfile {filepath}")
    else:
        logging.info(f"{filename} is already exists")
    
