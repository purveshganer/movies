import os
import sys
import logging
import common as bootstrap

# 3. Now you can import your base script
from imdb.import_scripts.base_files.import_script_base_file import BaseImportScript
from imdb.models import TitleAkas, TitleBasics
import argparse
from typing import Optional, Any, Dict
"""
A file which is responsible for importing a tsv file TitleAkas.
"""

class TitleAkasImportScript(BaseImportScript):
    def __init__(self, file_path)->None:
        self.file_name = "Title_Akas"
        self.file_path = file_path
        super().__init__(TitleAkas)
        self.records = super().base_reader(file_path=self.file_path, offset=0)
        self.record_to_model = {
            "titleId" : "title",
            "ordering" : "ordering",
            "title" : "title_text",
            "region" : "region",
            "language" : "language",
            "types" : "types",
            "attributes" : "attributes",
            "isOriginalTitle" : "is_original_title",
        }
        self.tconst_value = list(TitleBasics.objects.all())
        self.title_dict = {t.tconst: t for t in self.tconst_value}

    def reader(self)->Optional[Dict[str,Any]]:
        try:
            return next(self.records)
        except Exception as e:
            return None

    def preprocess(self, record)->dict:
        record = {self.record_to_model[key]:value for key, value in record.items()}
        if not record.get("title_text") and record.get('title_text') == r"\N":
            return None
        if not record.get("title") and record.get('title') == r"\N":
            return None
        if len(record.get("title_text")) > 500:
            logging.error(f"Got an abnormal record {record}")
            return None
        record["title"] = self.title_dict.get(record["title"])
        record["title_text"] = record.get("title_text").upper()
        region = record.get("region")
        if region is not None and region.strip() == r"\N":
            record["region"] = None
        language = record.get("language")
        if language is not None and language.strip() == r"\N":
            record["language"] = None
        attributes = record.get("attributes")
        if attributes is not None and attributes.strip() == r"\N":
            record["attributes"] = None
        types = record.get("types")
        if types is not None and types.strip() == r"\N":
            record["types"] = None
        return record
    
    def import_rows(self, records:list, n:int):
        super().base_importer(records=records, n = n)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="To take the dataset file path using CLI.")
    parser.add_argument("-f","--file_path",
                        required=True, 
                        help="Provide the path for the TitleAkas tsv file.")
    args = parser.parse_args()
    importer = TitleAkasImportScript(file_path=args.file_path)
    importer.run()