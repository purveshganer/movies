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
from imdb.models import TitleRatings, TitleBasics
import argparse
from typing import Optional, Any, Dict
"""
A file which is responsible for importing a tsv file TitleRatings.
"""

class TitleRatingsImportScript(BaseImportScript):
    def __init__(self, file_path)->None:
        self.file_name = "Title_Rating"
        self.file_path = file_path
        super().__init__(TitleRatings)
        self.records = super().base_reader(file_path=self.file_path, offset=0)
        self.record_to_model = {
            "tconst" : "title",
            "averageRating" : "average_rating",
            "numVotes" : "num_votes",
        }
    
    def reader(self)->Optional[Dict[str,Any]]:
        try:
            return next(self.records)
        except Exception as e:
            return None

    def preprocess(self, record)->dict:
        record = {self.record_to_model[key]:value for key, value in record.items()}
        if not record.get("title") and record.get('title') == r"\N":
            return None
        tconst = TitleBasics.objects.get(tconst = record.get("title"))
        record["title"] = tconst 
        average_rating = record.get("average_rating")
        if average_rating is not None and average_rating.strip() == r"\N":
            record["average_rating"] = None
        num_votes = record.get("num_votes")
        if num_votes is not None and num_votes.strip() == r"\N":
            record["num_votes"] = None
        else:
            record["num_votes"] = int(record.get("num_votes"))
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
                        help="Provide the path for the TitleRatings tsv file.")
    args = parser.parse_args()
    importer = TitleRatingsImportScript(file_path=args.file_path)
    importer.run()