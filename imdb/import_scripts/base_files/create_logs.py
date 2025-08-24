"""
Set up logging to write to a file and display logs in the console (CMD)
Helps track the flow of execution and understand how the code is working
"""
import logging
import os

class CreateLoggingFile:
    def __init__(self, table_name):
        self.table_name = str(table_name)
    
    def create_log_file(self)->None:
        base_path = os.path.dirname(os.path.abspath(__file__))
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(os.path.join(base_path,"../","logs/",f"{self.table_name}.log"), "w")
        file_formatter = logging.Formatter("%(asctime)s  - %(levelname)s  -  %(message)s  ")
        file_handler.setFormatter(file_formatter)

        consol_handler = logging.StreamHandler()
        consol_formatter = logging.Formatter("%(asctime)s  - %(levelname)s  -  %(message)s  ")
        consol_handler.setFormatter(consol_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(consol_handler)

