import os
import sys
import logging
# 1. Add project root to sys.path (go from this file up to manage.py folder)
current_file = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file, "../../../.."))
sys.path.insert(0, project_root)

# 2. Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movies.settings")
import django
django.setup()

# 3. Now you can import your base script
from imdb.import_scripts.base_files.import_script_base_file import BaseImportScript
from imdb.models import TitleBasics
import argparse
from typing import Optional, Any, Dict
"""
A file which is responsible for importing a tsv file titleBasic.
"""

class TitleBasicImportScript(BaseImportScript):
    def __init__(self, file_path)->None:
        self.file_name = "Title_Basics"
        self.file_path = file_path
        super().__init__(TitleBasics)
        self.records = super().base_reader(file_path=self.file_path, offset=0)
        self.record_to_model = {
            'tconst': 'tconst', 
            'titleType': 'title_type', 
            'primaryTitle': 'primary_title', 
            'originalTitle': 'original_title', 
            'isAdult': 'is_adult', 
            'startYear': 'start_year', 
            'endYear': 'end_year', 
            'runtimeMinutes': 'runtime_minutes', 
            'genres': 'genres'
        }
    
    def reader(self)->Optional[Dict[str,Any]]:
        try:
            return next(self.records)
        except Exception as e:
            return None

    def preprocess(self, record)->dict:
        record = {self.record_to_model[key]:value for key, value in record.items()}
        if not record.get("primary_title") and not record.get("original_title"):
            logging.error(f"Got a record without PRIMARY TITLE and ORIGINAL TITLE {record}")
            return None
        if (
            (record.get("is_adult").strip() == r"\N" or int(record.get("is_adult")) > 1) and
            record.get("runtime_minutes") is not None and 
            not record.get("runtime_minutes").isdigit()
            ):
            logging.error(f"Changed the record {record} \n To the following.")
            record["genres"] = record.get("runtime_minutes")
            record["runtime_minutes"] = record.get("end_year")
            record["end_year"] = record.get("start_year")
            record["start_year"] = record.get("is_adult")
            record["is_adult"] = record.get("original_title")
            record["original_title"] = ""
            logging.error(record)
        record["primary_title"] = record.get("primary_title").upper()
        record["original_title"] = record.get("original_title").upper()
        end_year = record.get("end_year")
        if end_year is not None and end_year.strip() == r"\N":
            record["end_year"] = None
        start_year = record.get("start_year")
        if start_year is not None and start_year.strip() == r"\N":
            record["start_year"] = None
        runtime_minutes = record.get("runtime_minutes")
        if runtime_minutes is not None and runtime_minutes.strip() == r"\N":
            record["runtime_minutes"] = None
            
        return record
    
    def import_rows(self, records:list, n:int):
        super().base_importer(records=records, n = n)
    
    def run(self)->None:
        super().create_logging(name = self.file_name)
        i = 0
        records = []
        while True:
            record = self.reader()
            if record == None:
                break
            preprossed_record = self.preprocess(record)
            if preprossed_record == None:
                continue
            records.append(preprossed_record)
            i += 1
            if i % 5000 == 0:
                self.import_rows(records=records, n = 5000)
                records = []
        self.import_rows(records=records, n = len(records))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="To take the dataset file path using CLI.")
    parser.add_argument("-f","--file_path",
                        required=True, 
                        help="Provide the path for the Title Basic tsv file.")
    args = parser.parse_args()
    importer = TitleBasicImportScript(file_path=args.file_path)
    importer.run()