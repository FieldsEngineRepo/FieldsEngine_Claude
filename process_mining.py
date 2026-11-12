import sys
import os
import shutil

from mining_v5 import *
from mining_complexity_report import *
from mining_error_report import *

MINING_TABLES = [
    'Mine_Ore_Quality',
    'Mining_Assets_Daily',
    'Mining_Capacity_Daily',
    'Mining_compounds',
    'Mining_Equity_Daily',
    'Mining_Model_Rules',
    'Mining_Model_RulesPending',
    'Mining_Operator_Daily',
    'Mining_Production_Daily',
    'Mining_Reserves_Daily',
    'Mining_Resource_Daily'
]

def archive_extracts():
    for extract_file in [exfile for exfile in os.listdir(DATA_DIR + 'mining\\mining_db\\') if exfile[-3:] in ['txt', 'sql']]:
        shutil.move(DATA_DIR + 'mining\\mining_db\\'+extract_file, DATA_DIR + 'mining\\mining_db\\archive\\'+extract_file)

def copy_ext_tables():
    server   = '115.112.83.122\energy,1450'
    database = 'MiningEngineExtract'
    username = 'ogtest '
    password = 'Pass@3$58'
    filepath = DATA_DIR + 'mining\\mining_db\\'
    tables   = ' '.join(['dbo.{}'.format(mining_table) for mining_table in MINING_TABLES])
    cmd = "mssql-scripter -S {} -d {} -U {} -P {} --schema-and-data --script-drop-create --file-path {} --file-per-object --include-objects {}".format(server, database, username, password, filepath, tables)
    print cmd
    os.system(cmd)

def process_mining_data(export_data=False):
    mining_main(export_data)

def process_mining_main(archive=False, copy_tables=False, process_data=False, export_data=False, gen_reports=False):
    if archive:
        archive_extracts()
    if copy_tables:
        copy_ext_tables()
    if process_data:
        process_mining_data(export_data)
    if gen_reports:
        mining_complexity_main()
        mining_error_main()

if __name__=='__main__':
    process_mining_main(archive=True, copy_tables=True, process_data=True, export_data=True, gen_reports=True)




