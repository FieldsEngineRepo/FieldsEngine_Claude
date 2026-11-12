import globaldata as gd
import os

MYSQL_DATA_DIR = "C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Data\\"
MYSQL_SCHEMAS  = ["us_wells\\", "globaldata\\"]

def get_create_statements():
    for mysql_schema in MYSQL_SCHEMAS:
        frm_files = [dbfile for dbfile in os.listdir(MYSQL_DATA_DIR+mysql_schema) if dbfile[-3:] == 'frm']
        for frm_file in frm_files:
            os.system('mysqlfrm --diagnostic "{}{}"'.format(MYSQL_DATA_DIR+mysql_schema, frm_file))


if __name__=='__main__':
    get_create_statements()