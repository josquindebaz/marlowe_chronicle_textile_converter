import datetime
import os
import glob
import shutil
import time

import mrlw_chron_2_textile

LOG_FILE = ""
JEKYLL_DIR = ""
CHRONICLE_PATH = ""
CONVERTER_PATH = ""
CHRONICLE_ARCHIVE = ""

def add_log(content):
    timestamp = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
    with open(LOG_FILE, "a") as filepath:
        filepath.write(timestamp + " " + content + "\n")

def get_last_textile_file_name():
    return max(glob.iglob(JEKYLL_DIR + "/*.textile"), key=os.path.getctime)

def get_last_textile_date():
    """extract date from last textile filename"""
    file_name = os.path.split(get_last_textile_file_name())[1]

    return datetime.date.fromisoformat(file_name[:10])

def get_last_chronicle_date():
    """extract date from last chronicle content"""
    with open(CHRONICLE_PATH, 'rb') as chronicle_file:
        first_line = chronicle_file.readline().decode('cp1252')

    only_date = first_line.split(" ")[0]
    day, month, year = only_date.split("/")

    return datetime.date(int(year), int(month), int(day))


if __name__ == '__main__':
    add_log("######\#####\#####\#####\#####")
    latest_file_date = get_last_textile_date()
    add_log(f"latest file date {latest_file_date}")
    chronicle_date = get_last_chronicle_date()
    add_log(f"latest chronicle date {chronicle_date}")

    """wait for chronicle to be available"""
    while chronicle_date <= latest_file_date:
        actual_time = time.localtime()

        if actual_time.tm_hour == 1:
            add_log(f"Giving up")
            break

        add_log(f"Waiting 5 minutes")
        time.sleep(360)
    else:
        archive_file_name = time.strftime('%Y-%m-%d-', time.localtime()) + os.path.split(CHRONICLE_PATH)[1]
        shutil.copy(CHRONICLE_PATH, os.path.join(CHRONICLE_ARCHIVE, archive_file_name))
        shutil.copy(CHRONICLE_PATH, CHRONICLE_ARCHIVE)

        add_log(f"Launching converter")

        with open(CHRONICLE_PATH, 'rb') as chronicle_file:
            chronicle = chronicle_file.read().decode('cp1252')
        mrlw_chron_2_textile.ChroniqueParser(chronicle)