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
            "tconst" : "tconst",
            "parentTconst" : "parent",
            "seasonNumber" : "season_number",
            "episodeNumber" : "episode_number",
        }
    
    def reader(self)->Optional[Dict[str,Any]]:
        try:
            return next(self.records)
        except Exception as e:
            return None

    def preprocess(self, record)->dict:
        record = {self.record_to_model[key]:value for key, value in record.items()}
        if not record.get("tconst") and record.get('tconst') == r"\N":
            return None
        tconst = TitleBasics.objects.get(tconst = record.get("tconst"))
        record["tconst"] = tconst 
        if not record.get("parent") and record.get('parent') == r"\N":
            return None
        parent = TitleBasics.objects.get(tconst = record.get("parent"))
        record["parent"] = parent
        season_number = record.get("season_number")
        if season_number is not None and season_number.strip() == r"\N":
            record["season_number"] = None
        episode_number = record.get("episode_number")
        if episode_number is not None and episode_number.strip() == r"\N":
            record["episode_number"] = None
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