import os
import sys
import logging
import common as bootstrap

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="To take the dataset file path using CLI.")
    parser.add_argument("-f","--file_path",
                        required=True, 
                        help="Provide the path for the TitleRatings tsv file.")
    args = parser.parse_args()
    importer = TitleRatingsImportScript(file_path=args.file_path)
    importer.run()