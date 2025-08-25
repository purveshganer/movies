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
        crew_obj, _ = TitleCrew.objects.get_or_create(tconst=tconst)

        writers_list = record.pop("writers", None)
        directors_list = record.pop("directors", None)

        if writers_list and writers_list.strip() != r"\N":
            writer_ids = [w.strip() for w in writers_list.split(",") if w.strip()]
            writer_objs = NameBasics.objects.filter(nconst__in=writer_ids)
            crew_obj.writers.set(writer_objs)   # overwrite
        else:
            crew_obj.writers.clear()  # optional, if you want empty
            
        # Directors
        if directors_list and directors_list.strip() != r"\N":
            director_ids = [d.strip() for d in directors_list.split(",") if d.strip()]
            director_objs = NameBasics.objects.filter(nconst__in=director_ids)
            crew_obj.directors.set(director_objs)
        else:
            crew_obj.directors.clear()
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