import globaldata as gd
import os

DATE = gd.get_date()
print DATE
DATE = '20190706'

SQL_SERVER_ADMIN = {
   'oilgas'  : {
       'server':'10.8.35.40',
       'database': {
           'oilgas_main': 'OGEngineDataExtract',
           'oilgas_test': 'OGEngineDataExtract_Effuah',
           'mining_main': 'MiningEngineDataExtract'
       },
       'username': 'uswellsdata',
       'password': 'uswellsdata'
   },
   'us_wells': {
       'server':'10.8.35.40',
       'database': {
           'us_wells_main': 'US_Wells',
           'us_wells_data': 'US_Wells_DataExtract'
       },
       'username': 'uswellsdata',
       'password': 'uswellsdata'
   }
}


def remote_export_to_txt(server, database, schema, table, username, password, data_dir):
    export_cmd_temp = 'bcp %s.%s.%s %s %s%s_%s.txt -n -S %s -U %s -P %s'
    print 'Exporting {}.{}.{} table ...'.format(database, schema, table)
    export_cmd = export_cmd_temp % (database, schema, table, 'out', data_dir, table, DATE, server, username, password)
    print export_cmd
    os.system(export_cmd)


def import_from_txt(int_server, database, schema, table, truncate=False, data_dir=gd.OILGAS_DB_DIR):
    import_cmd_temp = 'bcp %s.%s.%s %s %s%s_%s.txt -n -S %s -T'
    if truncate:
        truncate_cmd = gd.TRUNCATE_CMD_INT % (database, database, schema, table)
        os.system(truncate_cmd)
        print '%s table clear\n' % table
    print 'Importing {}.{}.{} table ...'.format(database, schema, table)
    import_cmd = import_cmd_temp % (database, schema, table, 'in', data_dir, table, DATE, int_server)
    print import_cmd
    os.system(import_cmd)

def import_data_tables(database, database_dir, update=True):
    print 1
    command = 'sqlcmd -S localhost -d {} -i %s'.format(database)
    print command
    os.system('cd %s' % database_dir)
    print [filename for filename in os.listdir(database_dir) if filename[-3:] == 'sql']
    for sql_file in [filename for filename in os.listdir(database_dir) if filename[-3:] == 'sql']:
        filename = sql_file[:-4]
        new_filename = filename.replace('.', '_')
        sql_filename = new_filename + '.sql'
        os.rename(database_dir+sql_file, database_dir+sql_filename)
        print command % (database_dir + sql_filename)
        if update:
            os.system(command % (database_dir + sql_filename))

def import_data(ext_server, database, schema, table, username, password, int_server, data_dir=gd.OILGAS_DB_DIR, truncate=False, debug=False):
    remote_export_to_txt(ext_server, database, schema, table, username, password, data_dir)
    import_from_txt(truncate, database, data_dir)

if __name__=='__main__':
    #import_data_tables(database='US_Wells', database_dir=gd.OILGAS_DB_DIR, update=True)
    #import_from_txt(int_server='HAL-2017', database='US_Wells', schema='dbo', table='tbl_USWell_Production__')
    #import_data(ext_server='10.8.35.40', database='US_Wells', schema='dbo', table='tblUSWell_Details_', username='teamlead', password='gdleads', int_server='HAL-2017')
    import_from_txt(int_server=gd.SERVER_NAME, database='OGEngineDataExtract', schema='Engine', table='tblEngineDataPoints')




'''

def remote_export_to_txt(server, database, schema, table, username, password, data_dir):
    export_cmd_temp = 'bcp %s.%s.%s %s %s%s_%s.txt -n -S %s -U %s -P %s'
    print 'Exporting {}.{}.{} table ...'.format(database, schema, table)
    export_cmd = export_cmd_temp % (database, schema, table, 'out', data_dir, table, DATE, server, username, password)
    print export_cmd
    os.system(export_cmd)
    print '%s table export complete\n' % table

def import_from_txt(int_server, database, schema, table, truncate, data_dir):
    if truncate:
        truncate_cmd = gd.TRUNCATE_CMD_INT % (database, database, schema, table)
        os.system(truncate_cmd)
        print '%s table clear\n' % table
    print 'Importing {}.{}.{} table ...'.format(database, schema, table)
    import_cmd = gd.IMPORT_CMD_INT % (database, schema, table, 'in', data_dir, table, DATE, int_server)
    print import_cmd
    os.system(import_cmd)
    print '%s table import complete\n' % table
'''