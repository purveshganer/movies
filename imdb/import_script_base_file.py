"""
Set up logging to write to a file and display logs in the console (CMD)
Helps track the flow of execution and understand how the code is working
"""
import logging
import os

base_path = os.getcwd()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(base_path,"data_import","dataset/","import_script.log"), "w")
file_formatter = logging.Formatter("%(asctime)s  - %(levelname)s  -  %(message)s  ")
file_handler.setFormatter(file_formatter)

consol_handler = logging.StreamHandler()
consol_formatter = logging.Formatter("%(asctime)s  - %(levelname)s  -  %(message)s  ")
consol_handler.setFormatter(consol_formatter)

logger.addHandler(file_handler)
logger.addHandler(consol_handler)


"""
Creating a base class which will be used to create import script.
its work will be to create a session.

"""
from datetime import datetime
import csv
from typing import Generator
from imdb.models import TitleAkas, TitleBasics, TitleCrew, TitleEpisode, TitlePrincipals, TitleRatings, NameBasics

class Importing:
    def __init__(self):
        pass
    
    def base_reader(self, file_path:str, offset:int = 0) -> Generator[dict, None, None]:

        now = datetime.now()
        readable_time = now.strftime("%Y-%m-%d %H:%M:%S")

        logging.info(f"Started data importing at {readable_time}")
        logging.info(f"Reading file: {file_path.split('/')[-1]}")
        
        try:
            assert offset >= 0, "Offset should not be negative number."
        except AssertionError as e:
            logging.exception(f"Assertion failed {e}")

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for i, row in enumerate(reader):
                if i < offset:
                    continue
                yield row
        
        logging.info(f"Finished reading file: {file_path.split('/')[-1]}")

    def base_importer(self, record:dict, table_name:str):
        num_of_lines = 0
