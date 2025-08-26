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
from abc import ABC, abstractmethod
from common import bootstrap

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
            self.model.objects.bulk_create(data_objects, ignore_conflicts=True)

            logging.info(f"Successfully imported {n} records.")
        except Exception as e:
            # Always log Exception as e or use logging.exception(...) to get the traceback in logs.
            logging.exception(f"Unable to import records.")
    
    @abstractmethod
    def reader(self):
        """Return the next record, or None if no more records."""
        pass

    @abstractmethod
    def preprocess(self, record):
        """Return processed record, or None to skip."""
        pass

    @abstractmethod
    def import_rows(self, records, n: int):
        """Import `n` records from `records` list."""
        pass

    def run(self) -> None:
        self.create_logging(name=self.file_name)
        i = 0
        records = []

        while True:
            record = self.reader()
            if record is None:
                break

            preprocessed_record = self.preprocess(record)
            if preprocessed_record is None:
                continue

            records.append(preprocessed_record)
            i += 1

            if i % 5000 == 0:
                self.import_rows(records=records, n=5000)
                records = []

        if records:
            self.import_rows(records=records, n=len(records))

        logging.info(f"Successfully imported {i} records.")
