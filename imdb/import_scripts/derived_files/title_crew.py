import os
import sys
import logging
import common as bootstrap

# 3. Now you can import your base script
from imdb.import_scripts.base_files.import_script_base_file import BaseImportScript
from imdb.models import TitleCrew, TitleBasics, NameBasics
import argparse
from typing import Optional, Any, Dict
"""
A file which is responsible for importing a tsv file TitleCrew.
"""

class TitleCrewImportScript(BaseImportScript):
    def __init__(self, file_path)->None:
        self.file_name = "Title_Crew"
        self.file_path = file_path
        super().__init__(TitleCrew)
        self.records = super().base_reader(file_path=self.file_path, offset=0)
        self.record_to_model = {
            "tconst" : "tconst",
            "directors" : "directors",
            "writers" : "writers",
        }
    
    def reader(self)->Optional[Dict[str,Any]]:
        try:
            return next(self.records)
        except Exception as e:
            return None

    def preprocess(self, record)->dict:
        record = {self.record_to_model[key]:value for key, value in record.items()}
        tconst = TitleBasics.objects.get(tconst=record.get("tconst"))
        record["tconst"] = tconst
        writers = record.get("writers")
        if writers is not None and writers.strip() == r"\N":
            record["writers"] = None
        directors = record.get("directors")
        if directors is not None and directors.strip() == r"\N":
            record["directors"] = None
        crew_obj, _ = TitleCrew.objects.get_or_create(title=tconst)
        directors_list = record.get("directors")
        if directors_list:
            for director_id in directors_list:
                if director_id and director_id != r"\N":
                    try:
                        director_obj = NameBasics.objects.get(nconst=director_id)
                        crew_obj.directors.add(director_obj)
                    except NameBasics.DoesNotExist:
                        pass 
        writers_list = record.get("writers")
        if writers_list:
            for writer_id in writers_list:
                if writer_id and writer_id != r"\N":
                    try:
                        writer_obj = NameBasics.objects.get(nconst=writer_id)
                        crew_obj.writers.add(writer_obj)
                    except NameBasics.DoesNotExist:
                        pass
        record.pop("directors", None)
        record.pop("writers", None)
        
        return record
    
    def import_rows(self, records:list, n:int):
        super().base_importer(records=records, n = n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="To take the dataset file path using CLI.")
    parser.add_argument("-f","--file_path",
                        required=True, 
                        help="Provide the path for the TitleCrew tsv file.")
    args = parser.parse_args()
    importer = TitleCrewImportScript(file_path=args.file_path)
    importer.run()