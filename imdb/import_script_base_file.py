"""
Set up logging to write to a file and display logs in the console (CMD)
Helps track the flow of execution and understand how the code is working
"""
import logging
import os

base_path = os.getcwd()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(base_path,"data_import","dataset/","import_script.log"), "w")
file_formatter = logging.Formatter("%(asctime)s  - %(levelname)s  -  %(message)s  ")
file_handler.setFormatter(file_formatter)

consol_handler = logging.StreamHandler()
consol_formatter = logging.Formatter("%(asctime)s  - %(levelname)s  -  %(message)s  ")
consol_handler.setFormatter(consol_formatter)

logger.addHandler(file_handler)
logger.addHandler(consol_handler)


"""
Creating a base class which will be used to create import script.
its work will be to create a session.

"""
class Importing:
    def __init__(self):
        pass