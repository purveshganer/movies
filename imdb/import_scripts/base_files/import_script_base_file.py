"""
Creating a base class which will be used to create import script.
its work will be to create a session.

"""
import os
import sys
import csv
import logging
from datetime import datetime
from typing import Generator
import django

# Set up Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies.settings')
django.setup()

from .create_logs import CreateLoggingFile

class BaseImportScript:
    """
    how to initiate the class
    first create a object with model.
    then call the create_logging function to create the logging file.
    if you do wish for a specific name of the log file then give a name when calling the function.
    """
    def __init__(self, model):
        self.model = model
    
    def create_logging(self, name:str = None):
        if name == None:
            name = self.model
        log = CreateLoggingFile(name)
        log.create_log_file()
    
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

    def base_importer(self, records:list, n:int)->None:
        logging.info(f"Starting Importing Records in {self.model} table.")
        try:
            data_objects = []

            for record in records:
                # Make sure record keys match the model fields exactly (e.g., 'name', 'age', etc.).
                data_objects.append(self.model(**record))
            self.model.objects.bulk_create(data_objects)

            logging.info(f"Successfully imported {n} records.")
        except Exception as e:
            # Always log Exception as e or use logging.exception(...) to get the traceback in logs.
            logging.exception(f"Unable to import records.")