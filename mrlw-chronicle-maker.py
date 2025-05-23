import datetime
import os
import glob
import shutil
import time
import pymysql

import mrlw_chron_2_textile

LOG_FILE = ""
JEKYLL_DIR = ""
CHRONICLE_PATH = ""
CONVERTER_PATH = ""
CHRONICLE_ARCHIVE = ""


def connect_database():
    return pymysql.connect(host="localhost",
                           user="user",
                           password="pwd",
                           database="db")


def add_log(content):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    with open(LOG_FILE, "a") as filepath:
        filepath.write(timestamp + " " + content + "\n")


def get_last_textile_file_name():
    return max(glob.iglob(JEKYLL_DIR + "/*.textile"), key=os.path.getctime)


def get_last_textile_date():
    """extract date from last textile filename"""
    file_name = os.path.split(get_last_textile_file_name())[1]

    return datetime.date.fromisoformat(file_name[:10])


def get_last_txt_chronicle_date():
    """extract date from last chronicle content"""
    with open(CHRONICLE_PATH, 'rb') as txt_chronicle_file:
        first_line = txt_chronicle_file.readline().decode('cp1252')

    only_date = first_line[:10]
    day, month, year = only_date.split("/")

    return datetime.date(int(year), int(month), int(day))


def write_textile(date_string, chronicle_final):
    """write textile chronicle for jekyll"""
    chronicle_file_name = f"{date_string}-chronique_mrlw.textile"
    chronicle_file_path = os.path.join(JEKYLL_DIR, chronicle_file_name)
    with open(chronicle_file_path, 'w') as handle:
        handle.write(chronicle_final)


if __name__ == '__main__':
    add_log("##########################")
    latest_file_date = get_last_textile_date()
    add_log(f"latest file date {latest_file_date}")

    txt_chronicle_date = get_last_txt_chronicle_date()
    add_log(f"latest chronicle date {txt_chronicle_date}")

    """wait for chronicle to be available"""
    while txt_chronicle_date <= latest_file_date:
        if time.localtime().tm_hour == 1:
            add_log(f"Giving up")
            break

        add_log(f"Waiting 5 minutes")
        time.sleep(360)
        txt_chronicle_date = get_last_txt_chronicle_date()
    else:
        txt_chronicle_date_string = get_last_txt_chronicle_date().strftime('%Y-%m-%d')

        add_log("Archiving")
        archive_file_name = txt_chronicle_date_string + "-" + os.path.split(CHRONICLE_PATH)[1]
        shutil.copy(CHRONICLE_PATH, os.path.join(CHRONICLE_ARCHIVE, archive_file_name))

        add_log("Converting")

        with open(CHRONICLE_PATH, 'rb') as txt_chronicle_file_handle:
            txt_chronicle = txt_chronicle_file_handle.read()

        database = connect_database()
        converter = mrlw_chron_2_textile.ChroniqueParser(txt_chronicle, database)
        database.close()
        write_textile(txt_chronicle_date_string, converter.chronique)

