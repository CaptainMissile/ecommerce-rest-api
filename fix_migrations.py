import os
from pathlib import Path


BASE_DIR = Path(__file__).parent
dir_list = os.listdir('apps/')

# DELETE ALL MIGRATION FILES
for dir_name in dir_list:
    cur_dir = BASE_DIR / 'apps' / dir_name / 'migrations'
    file_list = os.listdir(cur_dir)

    for file in file_list:
        if file.startswith('0'):
            os.remove(cur_dir / file)


# DELETE db.sqlite3
os.remove(BASE_DIR / 'db.sqlite3')
