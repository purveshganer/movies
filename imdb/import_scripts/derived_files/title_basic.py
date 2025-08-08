from import_scripts.base_files.import_script_base_file import BaseImportScript
from models import TitleBasics
import argparse
import os

"""
A file which is responsible for importing a tsv file titleBasic.
"""

class TitleBasicImportScript(BaseImportScript):
    def __init__(self, file_path)->None:
        self.file_name = "Title_Basics"
        self.file_path = file_path
        super.__init__(self, model = TitleBasics)
    
    def reader(self)->None:
        self.base_reader(file_path=self.file_path, offset=0)

    def preprocess(self, record)->dict:
        breakpoint()
        d = {}
        return record

    def run(self)->None:
        record = self.reader()
        preprossed_record = self.preprocess(record)

if __name__ == '__main__':
    """
    You can use the commented part if you wish to download the database to a different directory.
    """
    # parser = argparse.ArgumentParser(description="To take the dataset file path using CLI.")
    # parser.add_argument("-f","--file_path",
    #                     required=True, 
    #                     help="Provide the path for the Title Basic tsv file.")
    # args = parser.parse_args()
    # importer = TitleBasicImportScript(file_path=args.file_path)
    path = os.path.join(os.getcwd(), "../../data_import/dataset/title.basics.tsv")
    importer = TitleBasicImportScript(file_path=path)
    importer.run()