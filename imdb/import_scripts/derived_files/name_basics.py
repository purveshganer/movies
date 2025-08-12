import os
import sys
import logging
import common as bootstrap

# 3. Now you can import your base script
from imdb.import_scripts.base_files.import_script_base_file import BaseImportScript
from imdb.models import NameBasics
import argparse
from typing import Optional, Any, Dict
"""
A file which is responsible for importing a tsv file nameBasic.
"""

class TitleBasicImportScript(BaseImportScript):
    def __init__(self, file_path)->None:
        self.file_name = "Name_Basics"
        self.file_path = file_path
        super().__init__(NameBasics)
        self.records = super().base_reader(file_path=self.file_path, offset=0)
        self.record_to_model = {
            "nconst" : "nconst",
            "primaryName" : "primary_name",
            "birthYear" : "birth_year",
            "deathYear" : "death_year",
            "primaryProfession" : "primary_profession",
            "knownForTitles" : "known_for_titles",
        }
    
    def reader(self)->Optional[Dict[str,Any]]:
        try:
            return next(self.records)
        except Exception as e:
            return None

    def preprocess(self, record)->dict:
        record = {self.record_to_model[key]:value for key, value in record.items()}
        if not record.get("primary_name") :
            logging.error(f"Got a record without PRIMARY NAME {record}")
            return None
        record["primary_name"] = record.get("primary_name").upper()
        birth_year = record.get("birth_year")
        if birth_year is not None and birth_year.strip() == r"\N":  
            record["birth_year"] = None
        death_year = record.get("death_year")
        if death_year is not None and death_year.strip() == r"\N":
            record["death_year"] = None
        primary_profession = record.get("primary_profession")
        if primary_profession is not None and primary_profession.strip() == r"\N":
            record["primary_profession"] = None
        known_for_titles = record.get("known_for_titles")
        if known_for_titles is not None and known_for_titles.strip() == r"\N":
            record["known_for_titles"] = None
        return record
    
    def import_rows(self, records:list, n:int):
        super().base_importer(records=records, n = n)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="To take the dataset file path using CLI.")
    parser.add_argument("-f","--file_path",
                        required=True, 
                        help="Provide the path for the NAme Basic tsv file.")
    args = parser.parse_args()
    importer = TitleBasicImportScript(file_path=args.file_path)
    importer.run()