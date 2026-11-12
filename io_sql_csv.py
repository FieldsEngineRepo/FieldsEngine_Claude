from globaldata import *
import pandas as pd
import os

FROM_SQL_DIR   = 'D:\\GlobalData\\Data\\database\\us_well_data_tables_20190311\\state_well_data_tables\\'
CSV_DIR        = 'D:/GlobalData/Data/import_csv/'
TEST_CSV_DIR   = 'D:\\GlobalData\\Data\\well_data\\well_details_tables\\test\\'
IMPORT_CSV_DIR = 'D:\\GlobalData\\Data\\import_csv\\'
EXPORT_CSV_DIR = 'D:\\GlobalData\\Data\\export_csv\\'
#sql_export     = """SELECT {} UNION ALL SELECT {} FROM {} WHERE {} INTO OUTFILE '{}' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'"""
sql_export     = """SELECT {} FROM {}.{} WHERE {} INTO OUTFILE '{}' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'"""

def get_param_str(table, database='globaldata', quoted=False):
    col_names = get_columns(table_name=table, database=database)
    if quoted:
        param_str = ','.join(["'{}'".format(col) for col in col_names])
    else:
        param_str = ','.join(["IFNULL(`{}`,'')".format(col) for col in col_names])
    #print param_str
    return param_str

def export_data(cursor, param_str='*', table='global_variables', sql_where='1=1', outfile='output.csv', database='globaldata'):
    print 'Exporting {} >> {} ...'.format(table, outfile)
    #quoted_param_str = get_param_str(table=table, database=database, quoted=True)
    param_str        = get_param_str(table=table, database=database, quoted=False)
    #print sql_export.format(quoted_param_str, param_str, table, sql_where, outfile)
    print sql_export.format(param_str, database, table, sql_where, outfile)
    #cursor.execute(sql_export.format(quoted_param_str, param_str, table, sql_where, outfile.replace('\\','\\\\')))
    cursor.execute(sql_export.format(param_str, database, table, sql_where, outfile.replace('\\','\\\\')))


def export_mysql_to_csv(database='well_data', table_list=[], input_dir=FROM_SQL_DIR, output_dir=EXPORT_CSV_DIR, sql_where=''):
    conn = get_connection(server='mysql', database=database)
    curr = conn.cursor()
    if not table_list:
        table_list = [table[len(database)+1:-4] for table in os.listdir(input_dir)]
    for data_table in table_list:
        outfile_name = '{}{}.csv'.format(output_dir, data_table.replace('.','_'))
        export_data(cursor=curr, table=data_table, outfile=outfile_name, database=database, sql_where=sql_where)
    curr.close()
    conn.close()

def import_data(server, database, schema, table, csv_file, username=None, password=None):
    print 'Importing {} to {}.{}.{} on {} ...'.format(csv_file, database, schema, table, server)
    if username or password:
        import_cmd = 'bcp {}.{}.{} in "{}" -t, -S {} -U {} -P {}'.format(database, schema, table, csv_file, server, username, password)
    else:
        import_cmd = 'bcp {}.{}.{} in "{}" -t, -S {} -T'.format(database, schema, table, csv_file, server)
    os.system(import_cmd)

def import_csv_to_sql_server(csv_dir, server, database, schema, username=None, password=None):
    for csv_filename in os.listdir(csv_dir):
        csv_file = csv_dir + csv_filename
        table = csv_filename[:-4]
        import_data(server, database, schema, table, csv_file, username, password)

def main(export_from_database='well_data', export_from_dir=FROM_SQL_DIR, export_to_dir=EXPORT_CSV_DIR, export_from_tables=[], import_from_dir=CSV_DIR, import_to_server='10.8.35.40', import_to_database='US_Wells_DataExtract',  import_to_schema='dbo',  username=None, password=None, export_table_data=False, sql_where='1=1', import_csv_data=False):
    if export_table_data:
        export_mysql_to_csv(database=export_from_database, table_list=export_from_tables, input_dir=export_from_dir, output_dir=export_to_dir, sql_where=sql_where)
    if import_csv_data:
        import_csv_to_sql_server(import_from_dir, import_to_server, import_to_database, import_to_schema, username=username, password=password)

if __name__=='__main__':
    export_tables = ['tx_wellbore_data']
    main(export_table_data=True, export_from_database='us_wells', export_from_tables=export_tables, import_csv_data=False, export_to_dir=EXPORT_CSV_DIR, import_from_dir=EXPORT_CSV_DIR, import_to_server='HAL-2017', import_to_schema='tx_data', username=None, password=None)