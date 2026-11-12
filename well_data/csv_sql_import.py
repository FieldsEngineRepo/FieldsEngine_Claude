import csv
import os
import pandas as pd
from globaldata import *
from sqlalchemy import create_engine

# D:\GlobalData\Data\wells\csv

US_WELL_DATA_DIR = 'D:\\GlobalData\\Data\\wells\\csv\\'
PROD_DATA_DIR = US_WELL_DATA_DIR + 'Load\\'
# 'D:\GlobalData\Data\well_data\PDQ_DSV'
DSV_IMPORT_DIR = 'D:\\GlobalData\\Data\\well_data\\PDQ_DSV\\PDQ_DSV_split_\\'
# @D:\GlobalData\Data\well_data\PDQ_DSV\PDQ_DSV_split
CSV_IMPORT_DIR = DATA_DIR + 'import_csv\\'
US_WELLS_IMPORT_DIR = 'Z:\\Users\\Titan II\\Desktop\\US Wells Data\\'
TABLE_NAME_TEMP = '{}_Well_Production_Data'
TABLE_NAME = 'OH_2017_Production'
CSV_PROD_DIR = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\CO_Well_Data\\prod_reports\\add_source_year\\'
CA_ACCESS_DIR = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\CA_Well_Data\\prod_data\\unprocessed\\'
MONTH_NUMS = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10,
              'NOV': 11, 'DEC': 12}


def load_access_databases(data_dir):
    conn = get_connection(database='globaldata')
    curr = conn.cursor()
    tbl_templates = {
        '{}CaliforniaOilandGasWellInjection' : 'ca_well_injection_data',
        '{}CaliforniaOilandGasWellProduction': 'ca_well_production_data',
        '{}CaliforniaOilandGasWells'         : 'ca_well_data'
    }
    sql_insert = 'INSERT INTO {} VALUES ({})'
    for db_file in [dbfile for dbfile in os.listdir(data_dir) if dbfile[-5:] == 'accdb']:
        print db_file
        file_year = db_file[:4]
        acc_conn = get_connection(server='access', access_file=data_dir + db_file)
        acc_curr = acc_conn.cursor()
        for tbl_name in tbl_templates.keys():
            print tbl_name.format(file_year)
            sql_tbl = tbl_templates[tbl_name]
            acc_curr.execute('SELECT * FROM {}'.format(tbl_name.format(file_year)))
            for datarow in acc_curr.fetchall():
                var_str = ','.join(['%s'] * len(datarow))
                # print sql_insert.format(sql_tbl, var_str) % datarow
                curr.execute(sql_insert.format(sql_tbl, var_str), datarow)
            commit(curr)
        acc_curr.close()
        acc_conn.close()
    curr.close()
    conn.close()


def add_source_year(data_dir=CSV_PROD_DIR):
    headers = 'SOURCE_YEAR,REPORT_MONTH,REPORT_YEAR,ST,API_COUNTY_CODE,API_SEQ_NUM,SIDETRACK_NUM,FORMATION_CODE,WELL_STATUS,PROD_DAYS,WATER_DISP_CODE,WATER_VOL,WATER_PRESS_TBG,WATER_PRESS_CSG,BOM_INVENT,OIL_VOL,OIL_SALES,ADJUSTMENT,EOM_INVENT,GRAVITY_SALES,GAS_SALES,FLARED,GAS_VOL,SHRINK,GAS_PROD,BTU_SALES,GAS_PRESS_TBG,GAS_PRESS_CSG,OPERATOR_NUM,OPERATOR,FACILITY_NAME,FACILITY_NUM,ACCEPTED_DATE\n'
    for filename in os.listdir(data_dir):
        file_year = filename[:4]
        print filename
        data_rows = []
        with open(data_dir + filename, 'r+') as csv_infile:
            csv_reader = csv.reader(csv_infile)
            for row in csv_reader:
                row = [file_year] + row
                data_rows.append(row)
        with open(PROD_DATA_DIR + filename, 'a') as csv_outfile:
            csv_outfile.write(headers)
            line_num = 1
            for data_row in data_rows:
                print line_num
                data_str = ','.join(data_row)
                csv_outfile.write(data_str + '\n')
                line_num += 1


def load_co_prod(curr):
    # sql_insert = \
    # '''
    # INSERT INTO CO_well_production (well_id, formation_id, prod_month, prod_year) SELECT DISTINCT WELL_ID, FORMATION_CODE, REPORT_MONTH, REPORT_YEAR FROM co_well_production_ ORDER BY well_id, report_year, report_month, formation_code
    # '''
    # print sql_insert
    # curr.execute(sql_insert)
    # commit(curr)
    ##sql_update = \
    ##'''
    ##UPDATE CO_well_prod_lite AS a, CO_well_production_ AS b SET a.OIL_PROD_BBL=b.OIL_VOL, a.GAS_PROD_MCF=b.GAS_PROD, a.WATER_PROD_BBL=b.WATER_VOL
    ##WHERE a.WELL_ID=b.WELL_ID AND a.FORMATION_ID=b.FORMATION_CODE AND a.PROD_MONTH=b.REPORT_MONTH AND a.PROD_YEAR=b.REPORT_YEAR AND b.SOURCE_YEAR={};
    ##'''
    sql_update = \
        '''
		UPDATE CO_well_prod_lite AS a, CO_well_production_ AS b, us_ref_formation AS c
		SET a.GAS_{0}_MCF=IFNULL(b.GAS_PROD,0),
			a.OIL_{0}_BBL=IFNULL(b.OIL_VOL,0),
		  a.WATER_{0}_BBL=IFNULL(b.WATER_VOL,0)
		WHERE a.PROD_YEAR=b.REPORT_YEAR AND a.WELL_API=b.WELL_API AND a.FORMATION_ID=c.FORMATION_ID AND b.FORMATION_CODE=c.STATE_FORMATION_ID AND c.STATE_ID=5 AND b.REPORT_MONTH={1} AND b.SOURCE_YEAR={2}
		'''
    for source_year in range(1999, 2020):
        for prod_month in MONTH_NUMS.keys():
            month_num = MONTH_NUMS[prod_month]
            print sql_update.format(prod_month, month_num, source_year)
            curr.execute(sql_update.format(prod_month, month_num, source_year))
            commit(curr)
    if 0:
        sql_select = 'SELECT PROD_YEAR, SUM(OIL_PROD_BBL) AS TOTAL_OIL_BBL, SUM(GAS_PROD_MCF) AS TOTAL_GAS_MCF, SUM(WATER_PROD_BBL) AS TOTAL_WATER_BBL FROM CO_well_production GROUP BY PROD_YEAR ORDER BY PROD_YEAR'
        print sql_select
        curr.execute(sql_select)
        print 'YEAR\tOIL_BBL\tGAS_MCF\tWATER_BBL'
        for year, oil, gas, water in curr.fetchall():
            print '{}:\t{}\t{}\t{}'.format(year, oil, gas, water)


def load_production_to_sql(data_dir=PROD_DATA_DIR, table_name='', database='globaldata', header_row=0, header_names=[],
                           column_nums=[], delimiter=','):
    total_rows = 0
    dframes = []
    for data_sheet in os.listdir(data_dir):
        print data_sheet
        # df = pd.read_csv(data_dir+data_sheet, low_memory=False, header=header_row, names=header_names, usecols=column_nums)
        df = pd.read_csv(data_dir + data_sheet, delimiter=delimiter, low_memory=False)
        
        dframes.append(df)
    
    prod_data = pd.concat(dframes)
    print prod_data.shape[0], 'rows in table'
    
    engine = create_engine("mysql+pymysql://root:OilAndGas321@localhost/{}".format(database))
    prod_data.to_sql(name=table_name, con=engine, if_exists="append", chunksize=10000, index=False)


def csv_to_sql(data_dir, data_file, database='globaldata', table_name=None, delimiter=',', header_names=None):
    if not table_name:
        table_name = data_file[:-15]
    total_rows = 0
    dframes = []
    if header_names:
        df = pd.read_csv(data_dir + data_file, delimiter=delimiter, low_memory=False, names=header_names)
    else:
        df = pd.read_csv(data_dir + data_file, delimiter=delimiter, low_memory=False)
    dframes.append(df)
    
    prod_data = pd.concat(dframes)
    print prod_data.shape[0], 'rows in table'
    
    engine = create_engine("mysql+pymysql://root:OilAndGas321@localhost/{}".format(database))
    prod_data.to_sql(name=table_name, con=engine, if_exists="append", chunksize=10000, index=False)


def convert_ky_prod():
    data_dir = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\unprocessed\\'
    for prod_file in os.listdir(data_dir):
        filename = prod_file[:-4]
        os.rename(data_dir + prod_file, data_dir + filename + '.csv')


def finish_ky_records():
    unprocessed_files = os.listdir(
        'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\unprocessed\\')
    processed_files = os.listdir('D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\processed\\')
    no_wells_files = os.listdir('D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\no_wells\\')
    collected_files = unprocessed_files + processed_files + no_wells_files
    collected_wells = sorted(list(set([filename[4:-4] for filename in collected_files if filename[:3] == 'gas'])))
    uncollected_wells = [well_record for well_record in ky_wells if not well_record in collected_wells]
    for well in uncollected_wells:
        print well
    print len(uncollected_wells), 'wells left to download'


def check_ky_prod():
    unprocessed_dir = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\unprocessed\\'
    processed_dir = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\processed\\'
    no_wells_dir = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\no_wells\\'
    no_wells = []
    file_count = 1
    total_file_count = len(os.listdir(unprocessed_dir))
    for prod_file in os.listdir(unprocessed_dir):
        print '{}/{}: {}'.format(file_count, total_file_count, prod_file)
        with open(unprocessed_dir + prod_file) as csv_file:
            csv_lines = csv_file.readlines()
            if 'NO WELLS' in csv_lines[0]:
                no_wells.append(prod_file)
        file_count += 1
    
    for no_well_file in no_wells:
        shutil.move(unprocessed_dir + no_well_file, no_wells_dir + no_well_file)
    
    for well_file in os.listdir(unprocessed_dir):
        shutil.move(unprocessed_dir + well_file, processed_dir + well_file)


def main(combine=False, state_list=[], all_files=False, data_file='', data_dir=PROD_DATA_DIR, table_name=TABLE_NAME,
         database='globaldata', header_row=0, header_names=[], column_nums=[], delimiter=',', file_ext='csv',
         add_year=False, load_prod=False, load_db=False):
    conn = get_connection()
    curr = conn.cursor()
    if load_db:
        load_access_databases(data_dir)
    elif load_prod:
        load_co_prod(curr)
    elif add_year:
        add_source_year()
    elif all_files and not combine:
        data_files = [datafile for datafile in os.listdir(data_dir) if datafile[-4:] == '.{}'.format(file_ext)]
        for data_file in data_files:
            # table_name = data_file[:-18].lower()
            print '\nProcessing {} ...'.format(data_file)
            csv_to_sql(data_dir, data_file, database, table_name, delimiter, header_names)
            print '{} complete'.format(data_file)
    elif state_list:
        well_prod_states = state_list
        for state_name in well_prod_states:
            state_data_dir = US_PROD_DATA_DIR.format(state_name)
            state_table_name = TABLE_NAME_TEMP.format(state_name)
            load_production_to_sql(state_data_dir, state_table_name)
    elif all_files and combine:
        load_production_to_sql(data_dir, table_name, database, header_row, header_names, column_nums)
    else:
        csv_to_sql(data_dir, data_file, database, table_name, delimiter)
    curr.close()
    conn.close()


def binary_test():
    with open(DATA_DIR + "test.txt", "wb") as binary_file:
        binary_file.write("Write text by encoding\n".encode('utf8'))
        num_bytes_written = binary_file.write(b'\xDE\xAD\xBE\xEF')
        print "Wrote %d bytes." % num_bytes_written


if __name__ == '__main__':
    '''
        header_names = [
        'OIL_GAS_CODE',
        'DISTRICT_NO',
        'LEASE_NO',
        'CYCLE_YEAR',
        'CYCLE_MONTH',
        'CYCLE_YEAR_MONTH',
        'LEASE_NO_DISTRICT_NO',
        'OPERATOR_NO',
        'FIELD_NO',
        'FIELD_TYPE',
        'GAS_WELL_NO',
        'PROD_REPORT_FILED_FLAG',
        'LEASE_OIL_PROD_VOL',
        'LEASE_OIL_ALLOW',
        'LEASE_OIL_ENDING_BAL',
        'LEASE_GAS_PROD_VOL',
        'LEASE_GAS_ALLOW',
        'LEASE_GAS_LIFT_INJ_VOL',
        'LEASE_COND_PROD_VOL',
        'LEASE_COND_LIMIT',
        'LEASE_COND_ENDING_BAL',
        'LEASE_CSGD_PROD_VOL',
        'LEASE_CSGD_LIMIT',
        'LEASE_CSGD_GAS_LIFT',
        'LEASE_OIL_TOT_DISP',
        'LEASE_GAS_TOT_DISP',
        'LEASE_COND_TOT_DISP',
        'LEASE_CSGD_TOT_DISP',
        'DISTRICT_NAME',
        'LEASE_NAME',
        'OPERATOR_NAME',
        'FIELD_NAME'
    ]
    '''
    header_names = [
        'OIL_GAS_CODE',
        'DISTRICT_NO',
        'LEASE_NO',
        'CYCLE_YEAR',
        'CYCLE_MONTH',
        'OPERATOR_NO',
        'FIELD_NO',
        'CYCLE_YEAR_MONTH',
        'LEASE_OIL_DISPCD00_VOL',
        'LEASE_OIL_DISPCD01_VOL',
        'LEASE_OIL_DISPCD02_VOL',
        'LEASE_OIL_DISPCD03_VOL',
        'LEASE_OIL_DISPCD04_VOL',
        'LEASE_OIL_DISPCD05_VOL',
        'LEASE_OIL_DISPCD06_VOL',
        'LEASE_OIL_DISPCD07_VOL',
        'LEASE_OIL_DISPCD08_VOL',
        'LEASE_OIL_DISPCD09_VOL',
        'LEASE_OIL_DISPCD99_VOL',
        'LEASE_GAS_DISPCD01_VOL',
        'LEASE_GAS_DISPCD02_VOL',
        'LEASE_GAS_DISPCD03_VOL',
        'LEASE_GAS_DISPCD04_VOL',
        'LEASE_GAS_DISPCD05_VOL',
        'LEASE_GAS_DISPCD06_VOL',
        'LEASE_GAS_DISPCD07_VOL',
        'LEASE_GAS_DISPCD08_VOL',
        'LEASE_GAS_DISPCD09_VOL',
        'LEASE_GAS_DISPCD99_VOL',
        'LEASE_COND_DISPCD00_VOL',
        'LEASE_COND_DISPCD01_VOL',
        'LEASE_COND_DISPCD02_VOL',
        'LEASE_COND_DISPCD03_VOL',
        'LEASE_COND_DISPCD04_VOL',
        'LEASE_COND_DISPCD05_VOL',
        'LEASE_COND_DISPCD06_VOL',
        'LEASE_COND_DISPCD07_VOL',
        'LEASE_COND_DISPCD08_VOL',
        'LEASE_COND_DISPCD99_VOL',
        'LEASE_CSGD_DISPCDE01_VOL',
        'LEASE_CSGD_DISPCDE02_VOL',
        'LEASE_CSGD_DISPCDE03_VOL',
        'LEASE_CSGD_DISPCDE04_VOL',
        'LEASE_CSGD_DISPCDE05_VOL',
        'LEASE_CSGD_DISPCDE06_VOL',
        'LEASE_CSGD_DISPCDE07_VOL',
        'LEASE_CSGD_DISPCDE08_VOL',
        'LEASE_CSGD_DISPCDE99_VOL',
        'DISTRICT_NAME',
        'LEASE_NAME',
        'OPERATOR_NAME',
        'FIELD_NAME'
    ]
    # main(load_db=False, load_prod=False, all_files=True, combine=False, table_name='og_lease_cycle_disp', database='us_wells', data_dir=DSV_IMPORT_DIR, delimiter='}', file_ext='txt', header_names=header_names)
    main(load_db=False, load_prod=False, all_files=True, combine=False, table_name='development_start_year',
         database='globaldata', data_dir=CSV_IMPORT_DIR)
