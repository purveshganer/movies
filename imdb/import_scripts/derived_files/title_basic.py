from base_files.import_script_base_file import BaseImportScript
from models import TitleBasics

class TitleBasicImportScript(BaseImportScript):
    def __init__(self):
        self.file_name = "Title_Basics"
        super.__init__(self, model = TitleBasics)
    
    def run():
        pass

if __name__ == '__main__':
    importer = TitleBasicImportScript()
    importer.run()