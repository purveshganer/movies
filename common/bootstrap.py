# bootstrap.py
import os
import sys
import django

def find_project_root():
    """
    Walk up from this file's directory until we find 'manage.py'.
    This works no matter how deep the importing file is.
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while True:
        if 'manage.py' in os.listdir(current_dir):
            return current_dir
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        if parent_dir == current_dir:  # reached filesystem root
            raise FileNotFoundError("Could not find manage.py in any parent directory.")
        current_dir = parent_dir

# 1. Add project root to sys.path
project_root = find_project_root()
sys.path.insert(0, project_root)

# 2. Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movies.settings")
django.setup()
