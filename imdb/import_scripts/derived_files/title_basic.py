import os
import sys

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
            return None
        record["primary_title"] = record.get("primary_title").upper()
        record["original_title"] = record.get("original_title").upper()
        record["end_year"] = None if record.get("end_year") == '\\N' else record.get("end_year")
        return record
    
    def import_rows(self, records:list, n:int):
        super().base_importer(records=records, n = n)
    
    def run(self)->None:
        i = 0
        records = []
        while True:
            record = self.reader()
            if record == None:
                break
            preprossed_record = self.preprocess(record)
            records.append(preprossed_record)
            i += 1
            if i % 500 == 0:
                self.import_rows(records=records, n = 500)
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