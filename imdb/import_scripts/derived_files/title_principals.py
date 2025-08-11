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
from imdb.models import TitlePrincipals, TitleBasics, NameBasics
import argparse
from typing import Optional, Any, Dict
"""
A file which is responsible for importing a tsv file TitlePrincipals.
"""

class TitlePrincipalsImportScript(BaseImportScript):
    def __init__(self, file_path)->None:
        self.file_name = "Title_Principals"
        self.file_path = file_path
        super().__init__(TitlePrincipals)
        self.records = super().base_reader(file_path=self.file_path, offset=0)
        self.record_to_model = {
            "tconst" : "title",
            "nconst" : "name",
            "ordering" : "ordering",
            "category" : "category",
            "job" : "job",
            "characters" : "characters",
        }
    
    def reader(self)->Optional[Dict[str,Any]]:
        try:
            return next(self.records)
        except Exception as e:
            return None

    def preprocess(self, record)->dict:
        record = {self.record_to_model[key]:value for key, value in record.items()}
        if (record.get("title") == None or record.get("title") == r"\N") and \
            (record.get("name") == None or record.get("name") == r"\N"):
            return None
        try:
            record["title"] = TitleBasics.objects.get(tconst = record.get("title"))
        except Exception as e:
            logging.exception(f"tconst was not found for {record}")
            return None
        try:
            record["name"] = NameBasics.objects.get(nconst = record.get("name"))
        except Exception as e:
            logging.exception(f"nconst was not found for {record}")
            return None
        job = record.get("job")
        if job is not None and job.strip() == r"\N":
            record["job"] = None
        characters = record.get("characters")
        if characters is not None and characters.strip() == r"\N":
            record["characters"] = None
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
        logging.info(f"Successfully imported {i} records.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="To take the dataset file path using CLI.")
    parser.add_argument("-f","--file_path",
                        required=True, 
                        help="Provide the path for the TitlePrincipals tsv file.")
    args = parser.parse_args()
    importer = TitlePrincipalsImportScript(file_path=args.file_path)
    importer.run()