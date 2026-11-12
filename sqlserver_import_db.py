from globaldata import *


def import_mining_tables(update=True):
    command = 'sqlcmd -S localhost -d MiningEngineextract -i %s'
    os.system('cd %s' % MINING_DB_DIR)
    for sql_file in [filename for filename in os.listdir(MINING_DB_DIR) if filename[-3:] == 'sql']:
        filename = sql_file[:-4]
        new_filename = filename.replace('.', '_')
        sql_filename = new_filename + '.sql'
        os.rename(MINING_DB_DIR+sql_file, MINING_DB_DIR+sql_filename)
        print command % (MINING_DB_DIR + sql_filename)
        if update:
            os.system(command % (MINING_DB_DIR + sql_filename))

def import_oilgas_tables(update=True):
    command = 'sqlcmd -S localhost -d OGEngineDataExtract -i %s'
    os.system('cd %s' % OILGAS_DB_DIR)
    for sql_file in [filename for filename in os.listdir(OILGAS_DB_DIR) if filename[-3:] == 'sql']:
        filename = sql_file[:-4]
        new_filename = filename.replace('.', '_')
        sql_filename = new_filename + '.sql'
        os.rename(OILGAS_DB_DIR+sql_file, OILGAS_DB_DIR+sql_filename)
        print command % (OILGAS_DB_DIR + sql_filename)
        if update:
            os.system(command % (OILGAS_DB_DIR + sql_filename))

def import_test_oilgas_tables(update=True):
    command = 'sqlcmd -S localhost -d OGEngineDataExtract_Effuah -i %s'
    os.system('cd %s' % OILGAS_DB_DIR)
    for sql_file in [filename for filename in os.listdir(OILGAS_DB_DIR) if filename[-3:] == 'sql']:
        filename = sql_file[:-4]
        new_filename = filename.replace('.', '_')
        sql_filename = new_filename + '.sql'
        os.rename(OILGAS_DB_DIR+sql_file, OILGAS_DB_DIR+sql_filename)
        print command % (OILGAS_DB_DIR + sql_filename)
        if update:
            os.system(command % (OILGAS_DB_DIR + sql_filename))

def import_us_wells_tables(update=True):
    command = 'sqlcmd -S localhost -d US_Wells -i %s'
    os.system('cd %s' % OILGAS_DB_DIR)
    for sql_file in [filename for filename in os.listdir(OILGAS_DB_DIR) if filename[-3:] == 'sql']:
        filename = sql_file[:-4]
        new_filename = filename.replace('.', '_')
        sql_filename = new_filename + '.sql'
        os.rename(OILGAS_DB_DIR+sql_file, OILGAS_DB_DIR+sql_filename)
        print command % (OILGAS_DB_DIR + sql_filename)
        if update:
            os.system(command % (OILGAS_DB_DIR + sql_filename))

def import_data_tables(database, database_dir, update=True):
    command = 'sqlcmd -S localhost -d {} -i %s'.format(database)
    os.system('cd %s' % database_dir)
    for sql_file in [filename for filename in os.listdir(database_dir) if filename[-3:] == 'sql']:
        filename = sql_file[:-4]
        new_filename = filename.replace('.', '_')
        sql_filename = new_filename + '.sql'
        os.rename(database_dir+sql_file, database_dir+sql_filename)
        print command % (database_dir + sql_filename)
        if update:
            os.system(command % (database_dir + sql_filename))

def import_tables(database_name='', database_dir=OILGAS_DB_DIR, databases=None, update_mining=True, update_oilgas=True, update_us_wells=True, test_data=False):
    if databases:
        if 'mining' in databases:
            print 'Importing MiningEngineExtract tables ...'
            import_mining_tables(update=update_mining)

        if 'oilgas' in databases:
            if test_data:
                print 'Importing Test OGEngineDataExtract tables ...'
                import_test_oilgas_tables(update=update_oilgas)
            else:
                print 'Importing OGEngineDataExtract tables ...'
                import_oilgas_tables(update=update_oilgas)

        if 'us_wells' in databases:
            print 'Importing US_Wells tables ...'
            import_us_wells_tables(update=update_us_wells)
    else:
        import_data_tables(database_name, database_dir, True)

if __name__=='__main__':
    #databases = ['oilgas']
    import_tables(databases=['oilgas'], update_us_wells=False, test_data=False)
    #import_tables('US_Wells_DataExtract')