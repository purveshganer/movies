import os
import sys
import logging
import common.bootstrap as bootstrap

from imdb.import_scripts.base_files.import_script_base_file import BaseImportScript
from imdb.models import TitleEpisode, TitleBasics
import argparse
from typing import Optional, Any, Dict
"""
A file which is responsible for importing a tsv file TitleEpisode.
"""

class TitleEpisodeImportScript(BaseImportScript):
    def __init__(self, file_path)->None:
        self.file_name = "Title_Episode"
        self.file_path = file_path
        super().__init__(TitleEpisode)
        self.records = super().base_reader(file_path=self.file_path, offset=0)
        self.record_to_model = {
            "" : "tconst",
            "" : "parent",
            "" : "season_number",
            "" : "episode_number",
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
        writers = record.get("writers")
        if writers is not None and writers.strip() == r"\N":
            record["writers"] = None
        directors = record.get("directors")
        if directors is not None and directors.strip() == r"\N":
            record["directors"] = None
        return record
    
    def import_rows(self, records:list, n:int):
        super().base_importer(records=records, n = n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="To take the dataset file path using CLI.")
    parser.add_argument("-f","--file_path",
                        required=True, 
                        help="Provide the path for the TitleEpisode tsv file.")
    args = parser.parse_args()
    importer = TitleEpisodeImportScript(file_path=args.file_path)
    importer.run()