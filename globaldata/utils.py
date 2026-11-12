import os
import getpass
import random
import platform
from decline_obj import DeclineObj
import time
import json
import openpyxl
import pymysql
import pandas as pd
import shutil
import csv

from random import randint
from time import strftime
from datetime import datetime
from constants import *
import numpy as np
from collections import *
import math

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
try:
    import pypyodbc
except:
    pass

try:
    from oilgas_field import Field
except:
    pass

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def start_database(server='mysql', database='globaldata', external=False):
    # conn = pymysql.connect(user='root', passwd='OilAndGas321', host='localhost', db=database, charset='utf8', use_unicode=True)
    conn = pymysql.connect(user='titan', passwd='}2Ek}dTd*Z)k_dCI_Pm%', host='10.8.114.14', db=database, charset='utf8',
                           use_unicode=True)
    curr = conn.cursor()
    curr.execute('USE %s' % database)
    curr.close()
    return conn

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_connection(server='mysql', database='globaldata', external=False, access_file='', server_name='', username='', password='', us_wells=False, debug=False):
    if server == 'sql_server':
        if external:
            if not server_name:
                server_name = '10.55.22.78'
            if not username:
                username='uswellsdata'
            if not password:
                password='uswellsdata'
            conn_str = 'Driver={SQL Server}; Server=%s; Database=%s; uid=%s; pwd=%s' % (server_name, database, username, password)
        elif us_wells:
            conn_str = 'Driver={SQL Server}; Server=DIGITALSTORM-PC; Database=%s; uid=globaldata; pwd=OilAndGas321' % database
        else:
            # conn_str = 'Driver={SQL Server}; Server=(local); Database=%s; Trusted_Connection=True; unicode_results=True;' % database
            conn_str = 'Driver={SQL Server}; Server=10.55.22.78; Database=%s;UID=uswellsdata;PWD=uswellsdata; Trusted_Connection=No' % database
        conn = pypyodbc.connect(conn_str)
        if debug: print conn_str
    elif server == 'access':
        conn_str = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=%s;' % access_file
        conn = pypyodbc.connect(conn_str)
    elif server == 'mysql':
        # conn = pymysql.connect(host='localhost', db=database, user='root', passwd='OilAndGas321', charset='utf8', use_unicode=True)
        conn = pymysql.connect(host='10.8.114.14', db=database, user='titan', passwd='}2Ek}dTd*Z)k_dCI_Pm%', charset='utf8',
                               use_unicode=True)
    return conn


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def is_value(param):
    param_is_value = True
    try:
        if str(param).upper() == 'NULL' or param is None or len(str(param)) == 0 or param == 'None':
            param_is_value = False
    except:
        param_is_value = False
    return param_is_value

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def round_value(data_val):
    try:
        ret_val = float(data_val)
    except ValueError:
        ret_val = data_val
    else:
        ret_val = round(ret_val, 3)
    return ret_val

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def pws(thisChar ,numLen ,align = 'L'):
    ret_val = ""
    outputStr = thisChar
    if thisChar is None:
        outputStr = ""
    if align == 'R':
        ret_val = ( ' ' * numLen +outputStr.strip())[- 1 *(numLen):]
    else:
        ret_val = (outputStr.strip( ) + ' ' *numLen)[:numLen]
    return ret_val

def fwc(cNum):
    pos = 0
    minusLoops = 0
    if cNum.count(".") > 0:
        pos = cNum.index(".")
    else:
        pos = len(cNum)
    beforeDecimal = cNum[:pos]
    afterDecimal = cNum[pos:]
    newXLen = int(len(beforeDecimal ) /3)
    newStr = beforeDecimal
    pos = 3
    if len(beforeDecimal ) %3 == 0:
        minusLoops = 1
    for i in range(0 ,newXLen - minusLoops):
        newStr = newStr[:-pos] + ","+ newStr[-pos:]
        pos += 3 + 1
    return newStr + afterDecimal

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def is_numeric(cNumber):
    retVal = True
    cNumb = cNumber.strip()
    validChars = "0123456789."
    if cNumb.count(".") > 1:
        retVal = False
    else:
        for i in range(len(cNumb)):
            ch = cNumb[i:i + 1]
            if validChars.count(ch) == 0:
                retVal = False
                break
    return retVal

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def encode_str(ascii_str):
    encoded = ''
    try:
        encoded = unicode(ascii_str.encode('utf-8').strip(), errors='ignore')
    except:
        pass
    return encoded

def decode_str(encoded_str, encoding='utf-8'):
    try:
        decoded = encoded_str.encode(encoding).strip()
    except:
        decoded = encode_str(encoded_str).encode(encoding).strip()
    return decoded

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_julian_date():
    timeStarted = datetime.now()
    dt = timeStarted.timetuple()
    return str(dt[0]) + format_dt(dt[1], 2) + format_dt(dt[2], 2)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_date():
    dtime = datetime.now()
    dtime.strftime('%Y-%m-%d')
    date_str = str(dtime)[:4] + str(dtime)[5:7] + str(dtime)[8:10]
    return date_str

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_time(dt):
    dt_hour = str(dt[3])
    am_pm = " am "
    if dt[3] >= 12:
        dt_hour = str(dt[3]-12)
        am_pm = " pm "
    return format_dt(dt_hour,2)+":"+format_dt(dt[4],2)+":"+format_dt(dt[5],2)+am_pm

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_datetime():
    dtime = datetime.now()
    dtime.strftime('%Y-%m-%d %H:%M:%S')
    return str(dtime)[:19]

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_add_date(with_time=True):
    if with_time:
        date_str = '%Y-%m-%d %H:%M:%S'
    else:
        date_str = '%Y-%m-%d'
    time_stamp = time.time()
    add_date = datetime.fromtimestamp(time_stamp).strftime(date_str)
    return add_date

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def elapsed_time(start_datetime, end_datetime):
    elapsed_hour = 0
    elapsed_min = 0
    elapsed_sec = 0

    start_date = start_datetime.split()[0]
    start_time = start_datetime.split()[1]

    start_hour = int(start_time.split(':')[0])
    start_min = int(start_time.split(':')[1])
    start_sec = int(start_time.split(':')[2])

    end_date = end_datetime.split()[0]
    end_time = end_datetime.split()[1]

    end_hour = int(end_time.split(':')[0])
    end_min = int(end_time.split(':')[1])
    end_sec = int(end_time.split(':')[2])

    if start_date != end_date:
        end_hour += 24

    elapsed_sec = end_sec - start_sec
    if elapsed_sec < 0:
        elapsed_sec += 60
        end_min -= 1

    elapsed_min = end_min - start_min
    if elapsed_min < 0:
        elapsed_min += 60
        end_hour -= 1

    elapsed_hour = end_hour - start_hour
    elapsed_times = [elapsed_hour, elapsed_min, elapsed_sec]

    if len(str(elapsed_hour)) == 1:
        elapsed_hour = str(0)+str(elapsed_hour)
    else:
        elapsed_hour = str(elapsed_hour)

    if len(str(elapsed_min)) == 1:
        elapsed_min = str(0)+str(elapsed_min)
    else:
        elapsed_min = str(elapsed_min)

    if len(str(elapsed_sec)) == 1:
        elapsed_sec = str(0)+str(elapsed_sec)
    else:
        elapsed_sec = str(elapsed_sec)

    return str(elapsed_hour) + ':' + str(elapsed_min) + ':' + str(elapsed_sec)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def format_dt(numData, numLen):
    return ("0000000" + str(numData))[-numLen:]

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_param_str(param_list):
    return ','.join(param_list)

def param_str(param_list):
    return get_param_str(param_list)

def get_update_str(param_list):
    if param_list:
        update_str = ' AND '.join(['{}=%s'.format(param) for param in param_list])
    else:
        update_str = 'id > 0 '
    return update_str

def get_set_str(param_list):
    set_str = ''
    if param_list:
        set_str = ','.join(['{}=%s'.format(param) for param in param_list])
    else:
        set_str = 'id=id'
    return set_str

def buildMySQLin(loops, symb):
    outP = "("
    for i in range(loops):
        outP += " " + symb + ","
    outP = outP[:-1] + ") "
    return outP

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_user_name():
    ret_val = ""
    if platform.system().upper() == "WINDOWS":
        ret_val = os.environ.get("USERNAME")
    else:
        ret_val = getpass.getuser()
    ret_val = ret_val.replace('.', '_')
    return ret_val

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_random_num(nMin, nMax):
    return format_dt(random.uniform(nMin, nMax), 5)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_time_string():
    timeStarted = datetime.now()
    dt = timeStarted.timetuple()
    return format_dt(dt[3], 2) + format_dt(dt[4], 2) + format_dt(dt[5], 2)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_session_key(with_username=True):
    session_key = ''
    if with_username:
        session_key += '%s_' % get_user_name()
    session_key += '%s_' % get_julian_date()
    session_key += '%s_' % get_time_string()
    session_key += '%s' % get_random_num(1, 1000)
    return session_key

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_run_id(cursor=None):
    run_id = ""
    if cursor:
        curr = cursor
    else:
        conn = get_connection()
        curr = conn.cursor()
    try:
        sql_query = 'SELECT run_id FROM global_variables WHERE id=1'
        curr.execute(sql_query)
        run_id = curr.fetchone()[0]
    except:
        time_string = get_datetime()
        time_string = '_'.join(''.join(''.join(time_string.split('-')).split(':')).split(' '))
        run_id = time_string
    if not cursor:
        curr.close()
        conn.close()
    return run_id

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_discount_year(cursor=None):
    discount_year = 0
    if cursor:
        curr = cursor
    else:
        conn = get_connection()
        curr = conn.cursor()
    try:
        sql_select = 'SELECT discount_year FROM global_variables WHERE id=1'
        curr.execute(sql_select)
        discount_year = int(curr.fetchone()[0])
    except:
        discount_year = int(get_date()[:4])
    return discount_year

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def last_mod_time(file_path):
    return os.stat(file_path).st_mtime

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def format_time(epoch_time):
    return strftime('%Y-%m-%d %H:%M:%S', epoch_time)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def restart_server():
    os.system('D:\\Users\\Jason\\Desktop\\Applications\\restart_mysql_server.lnk')

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def drop_table(cursor=None, table=''):
    if not cursor:
        conn = get_connection()
        curr = conn.cursor()
    else:
        curr = cursor
    sql_drop = 'DROP TABLE IF EXISTS %s' % table
    curr.execute(sql_drop)
    curr.execute('COMMIT')
    if not cursor:
        curr.close()
        conn.close()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_cmd_args(task_config, region=''):
    cmd_args = ()
    check_process = task_config['check_process']
    if check_process == 'check_breakeven':
        cmd_args = (REGIONS[region], region)
    elif check_process == 'check_disc_fields':
        cmd_args = (REGIONS[region])
    elif check_process == 'temp_log':
        cmd_args = (region,)
    return cmd_args

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_subtask_args(task_config, cmd_name, region=''):
    subtask_args = ()
    if cmd_name == 'create_model':
        if region in ['North_America_1', 'North_America_2']:
            subtask_args = (region.lower())
        elif region == 'Rest_of_World_2':
            subtask_args = ','.join([region_name.lower() for region_name in task_config['region_chains'][region]]) + ' -delt-e'
        else:
            subtask_args = (region.lower() + ' -delt-e')

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_columns(table_name, server='mysql', database='globaldata', external=False, no_id=False, data_only=False, and_str=''):
    table_columns = []
    if server == 'sql_server':
        sql_select = 'SELECT COLUMN_NAME FROM %s.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA="%s" AND TABLE_NAME="%s" ' % (database, SCHEMAS[table_name], table_name)
        sql_select += and_str
        if external:
            conn_str = 'Driver={SQL Server}; Server=10.55.22.78; Database=%s; uid=uswellsdata; pwd=uswellsdata' % database
        else:
            conn_str = 'Driver={SQL Server}; Server=(local); Database=%s; Trusted_Connection=True; unicode_results=True;' % database
        conn = pypyodbc.connect(conn_str)

    elif server == 'mysql':
        sql_select = 'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA="%s" AND TABLE_NAME="%s" ' % (database, table_name)
        sql_select += and_str
        # conn = pymysql.connect(host='localhost', db=database, user='root', passwd='OilAndGas321', charset='utf8',use_unicode=True)
        conn = pymysql.connect(host='10.8.114.14', db=database, user='titan', passwd='}2Ek}dTd*Z)k_dCI_Pm%', charset='utf8',
                               use_unicode=True)

    curr = conn.cursor()
    if curr.execute(sql_select):
        table_columns = [decode_str(data[0]) for data in curr.fetchall()]

    if no_id:
        table_columns = [column for column in table_columns if not column in ['id', 'RecNo']]

    if data_only:
        table_columns = [column for column in table_columns if not column.lower() in ['add_by', 'add_date', 'edit_by', 'edit_date', 'createddate', 'createdon', 'extractdate', 'notes', 'sources', 'data_source']]

    curr.close()
    conn.close()
    return table_columns

def set_to_null(table):
    print 'Setting empty table entries to NULL ...'
    conn = get_connection()
    curr = conn.cursor()

    sql_update = 'UPDATE {0} SET {1}=NULL WHERE ({1}="NULL" OR LENGTH({1}) < 1 OR {1}="None")'
    and_str = 'AND NOT DATA_TYPE IN ("double", "int", "float", "tinyint", "date", "datetime", "timestamp", "year") '
    col_names = get_columns(table, and_str=and_str)
    for col_name in col_names:
        sql_command = sql_update.format(table, col_name)
        curr.execute(sql_command)
    commit(curr)
    curr.close()
    conn.close()

def set_to_zero(table):
    print 'Setting empty table values to 0 ...'
    conn = get_connection()
    curr = conn.cursor()

    sql_update = 'UPDATE {0} SET {1}=0 WHERE ({1} IS NULL OR {1} IN (-4293652562, -2146826281)) '
    and_str = 'AND DATA_TYPE IN ("double", "int", "float") '
    col_names = get_columns(table, no_id=True, and_str=and_str)
    for col_name in col_names:
        sql_command = sql_update.format(table, col_name)
        curr.execute(sql_command)
    commit(curr)
    curr.close()
    conn.close()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_month_name(month_num, short=False):
    month_name = ''
    months = {
        '01': {'long': 'January',
                     'short': 'Jan'},
        '02': {'long' : 'February',
               'short': 'Feb'},
        '03': {'long' : 'March',
               'short': 'Mar'},
        '04': {'long' : 'April',
               'short': 'Apr'},
        '05': {'long' : 'May',
               'short': 'May'},
        '06': {'long' : 'June',
               'short': 'Jun'},
        '07': {'long' : 'July',
               'short': 'Jul'},
        '08': {'long' : 'August',
               'short': 'Aug'},
        '09': {'long' : 'September',
               'short': 'Sep'},
        '10': {'long' : 'October',
               'short': 'Oct'},
        '11': {'long' : 'November',
               'short': 'Nov'},
        '12': {'long' : 'December',
             'short': 'Dec'}}
    if short:
        month_name = months[month_num]['short']
    else:
        month_name = months[month_num]['long']
    return month_name

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def commit(curr):
    curr.execute('COMMIT')

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def date_diff(start, end, sep='/'):
    if isinstance(start,str):
        if sep == '/':
            start_date = datetime.strptime(start, '%m/%d/%Y')
        else:
            start_date = datetime.strptime(start, '%Y-%m-%d')
    else:
        start_date = start
    if isinstance(end, str):
        if sep == '/':
            end_date = datetime.strptime(end, '%m/%d/%Y')
        else:
            end_date = datetime.strptime(end, '%Y-%m-%d')
    else:
        end_date = end
    return abs((end_date - start_date).days)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_param(param, table, asset_id=None, cur=None, sql_where='1=1', data_type='str', debug=False):
    conn = None
    param_val = None
    if cur:
        curr = cur
    else:
        conn = get_connection()
        curr = conn.cursor()
    if asset_id:
        sql_where += ' AND asset_id={}'.format(asset_id)
    sql_select = 'SELECT {} FROM {} WHERE {} '.format(param, table, sql_where)
    if debug:
        print sql_select
    if curr.execute(sql_select):
        param_val = curr.fetchone()[0]
        if param_val:
            if data_type == 'str':
                param_val = str(param_val)
            elif data_type == 'int':
                param_val = int(param_val)
            elif data_type == 'float':
                param_val = float(param_val)
            elif data_type == 'bool':
                param_val = bool(param_val)
    if not cur:
        curr.close()
        conn.close()
    return param_val

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_conversion_factor(commodity,from_unit,to_unit,time_unit='year',cur=None):
    conn              = None
    conversion_factor = 1.0
    sql_statement = 'SELECT factor FROM unit_equals WHERE commodity=%s and unit=%s and base_unit=%s'
    if cur:
        curr = cur
    else:
        conn = get_connection()
        curr = conn.cursor()
    commodity = commodity.lower().strip()
    if commodity == 'ngl':
        commodity = 'ngls'
    if curr.execute(sql_statement,(commodity.strip(),from_unit.strip(),to_unit.strip())):
        conversion_factor = float(curr.fetchone()[0])
    if from_unit.lower() in ['bd', 'mmcfd'] and time_unit == 'month':
        conversion_factor = float(conversion_factor/12.0)
    if not cur:
        curr.close()
        conn.close()
    return conversion_factor

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_assumption_points(table):
    conn = get_connection()
    curr = conn.cursor()
    set_to_null(table)
    print 'Updating assumption points ...'
    main_cols = PARAM_LISTS[table]['main']
    main_param_str = get_update_str(main_cols)

    scored_cols = PARAM_LISTS[table]['scored']

    sql_update = 'UPDATE {} SET points=%s WHERE {} '.format(table, main_param_str)

    all_cols = PARAM_LISTS[table]['scored'] + PARAM_LISTS[table]['main']
    param_str = get_param_str(all_cols)
    sql_select = 'SELECT %s FROM %s' % (param_str, table)
    curr.execute(sql_select)
    row_num = 1
    for datarow in curr.fetchall():
        sql_command = sql_update
        params = ()
        main_count = len(main_cols)
        param_vals = ()
        if main_count:
            param_vals = datarow[-main_count:]
        assumption_points = 0
        for i in range(len(scored_cols)):
            param_name = scored_cols[i]
            data_val = datarow[i]
            if data_val is None:
                sql_command += 'AND {} IS NULL '.format(param_name)
            else:
                sql_command += 'AND {}=%s '.format(param_name)
                param_vals += (data_val,)
                if data_val and data_val != 'None':
                    assumption_points += PARAM_POINTS[param_name]
                    if (param_name in ['production_peak', 'production_total']) and (table in ['capex_alloc', 'capex_redev_alloc', 'abandonment_alloc']):
                        assumption_points += 1920
        param_vals = (assumption_points,) + param_vals
        try:
            curr.execute(sql_command, param_vals)
            curr.execute('COMMIT')
        except:
            print sql_select
            print sql_command
            print param_vals
            print sql_command % param_vals
        row_num += 1
    set_to_zero(table)
    curr.close()
    conn.close()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def export_table(table):
    date = get_date()
    password= '}2Ek}dTd*Z)k_dCI_Pm%'
    export_file = '%s_%s.sql' % (table, date)
    # export_cmd = 'mysqldump -utitan -p}2Ek}dTd*Z)k_dCI_Pm% -h10.8.114.14 globaldata {0} > D:/TitanJobs/Titan1/Globaldata/Data/{1}'.format(table, export_file)
    export_cmd = 'mysqldump -utitan -p%s -h10.8.111.11 globaldata %s > D:/TitanJobs/Titan1/Globaldata/Data/%s' % (
    password, table, export_file)
    print export_cmd
    print 'Exporting %s table to Data folder...' % table
    os.system(export_cmd)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def truncate_table(curr=None, table=''):
    export_table(table)
    if not curr:
        conn = get_connection()
        curr_ = conn.cursor()
    else:
        curr_ = curr
    sql_truncate = 'TRUNCATE TABLE %s' % table
    curr_.execute(sql_truncate)
    curr_.execute('COMMIT')
    if not curr:
        curr_.close()
        conn.close()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_assets(table, sql_where='1=1'):
    conn = get_connection()
    curr = conn.cursor()
    sql_select = 'SELECT DISTINCT asset_id FROM {} WHERE {} ORDER BY asset_id'.format(table, sql_where)
    curr.execute(sql_select)
    assets = [int(data[0]) for data in curr.fetchall()]
    curr.close()
    conn.close()
    return assets

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_param_list(param, table, sql_where='1=1', datatype='str', database='globaldata', debug=False):
    param_list = []
    conn = get_connection(database=database)
    curr = conn.cursor()
    sql_select = 'SELECT DISTINCT {0} FROM {1} WHERE {2} ORDER BY {0}'.format(param, table, sql_where)
    if debug:
        print 'sql_select: {}'.format(sql_select)
    curr.execute(sql_select)
    if datatype == 'int':
        param_list = [int(data[0]) for data in curr.fetchall()]
    elif datatype == 'str':
        param_list = [str(data[0]) for data in curr.fetchall()]
    elif datatype == 'float':
        param_list = [float(data[0]) for data in curr.fetchall()]
    curr.close()
    conn.close()
    return param_list

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def format_num(number, decimals=2, commas=True, financial=False):
    if 0:
        print 'number: {} decimals:{} commas: {} financial: {}'.format(number,decimals,commas,financial)
    formatted_num = 0
    if commas:
        if decimals == 0:
            formatted_num = str("{:,}".format(int(number)))
        else:
            formatted_num = str("{:,}".format(round(float(number), decimals)))
    else:
        formatted_num = round(number, decimals)
    if financial:
        dollars = str(formatted_num).split('.')[0]
        cents = str(formatted_num).split('.')[1]
        if len(cents) > 2:
            formatted_num = '{}.{}'.format(dollars, cents[:2])
        elif len(cents) < 2:
            add_zero = '0'*(2-len(cents))
            formatted_num = '{}.{}'.format(dollars, cents+add_zero)
    return formatted_num

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def decode_hex(hex_input):
    hex_chars = hex_input.split(':')
    hex_str = ''.join(hex_chars)
    hex_output = hex_str.decode('hex')
    return hex_output

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_cols(init_cols, col_span, group_offset, group_count):
    xl_cols = []
    for i in range(group_count):
        xl_cols.append(XL_COLS[((col_span * i) + group_offset) + init_cols])
    return xl_cols

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def convert_to_days(datetime_interval):
    total_days = float(datetime_interval.days)
    total_days += float(datetime_interval.seconds/(24.0*60.0*60.0))
    return round(total_days,4)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_new_typewell_id(curr=None):
    type_well_id = '9000001-01'
    if not curr:
        conn = get_connection()
        curr = conn.cursor()
    curr.execute('SELECT MAX(well_id) FROM type_well_production WHERE LENGTH(well_id)=10')
    max_well_id = curr.fetchone()[0]
    if max_well_id[0] == '9':
        type_well_id = str(int(max_well_id.split('-')[0]) + 1) + '-01'
    if not curr:
        curr.close()
        conn.close()
    return type_well_id

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def max_row(excel_filepath, sheet_name):
    df = pd.read_excel(excel_filepath, sheet_name=sheet_name)
    return len(df)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def breakeven_config(setting, scenario_num='', region_num=''):
    print 'Configuring breakeven macros ...'
    config = {
     'Calculate Breakevens': {        'cell': 'E10',
                                   'full be': True,
                                   'base be': True,
                                    'engine': True,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': True,
                               'disc fields': True},

      'Calculate Base Case': {        'cell': 'E11',
                                   'full be': True,
                                   'base be': True,
                                    'engine': True,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': True,
                               'disc fields': True},

      'Calculate High Case': {        'cell': 'E12',
                                   'full be': True,
                                   'base be': False,
                                    'engine': True,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': True,
                               'disc fields': False},

       'Calculate Low Case': {        'cell': 'E13',
                                   'full be': True,
                                   'base be': False,
                                    'engine': True,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': True,
                               'disc fields': False},

         'Update Econ Data': {        'cell': 'E15',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': True,
                                 'full econ': True,
                                     'uncon': True,
                               'disc fields': True},

          'Update All Econ': {        'cell': 'E16',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': True,
                                     'uncon': False,
                               'disc fields': False},

    'Connected to Database': {        'cell': 'E18',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': True,
                                 'full econ': True,
                                     'uncon': False,
                               'disc fields': True},

           'Unconventional': {        'cell': 'E19',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': True,
                               'disc fields': False},

       'Calculate Min Econ': {       'cell': 'E21',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': False,
                               'disc fields': True},

        'Calculate Max Dev': {       'cell': 'E22',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': False,
                               'disc fields': True},

        'Update Asset Data': {       'cell': 'E23',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': False,
                               'disc fields': True},

          'Remove Formulas': {          'cell': 'E24',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': False,
                               'disc fields': False},

            'Set comms = 0': {            'cell': 'E25',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': False,
                               'disc fields': True},

             'Scenario Num': {        'cell': 'C2',
                                   'full be': scenario_num,
                                   'base be': scenario_num,
                                    'engine': scenario_num,
                               'econ report': scenario_num,
                                 'full econ': scenario_num,
                                     'uncon': scenario_num,
                               'disc fields': scenario_num},

               'Region Num': {        'cell': 'C4',
                                   'full be': region_num,
                                   'base be': region_num,
                                    'engine': region_num,
                               'econ report': region_num,
                                 'full econ': region_num,
                                     'uncon': region_num,
                               'disc fields': region_num}
    }

    macro_dir = BREAKEVEN_DIR
    if setting == 'full econ':
        macro_dir = ECON_MACRO_DIR
    elif setting == 'disc fields':
        macro_dir = DISC_FIELD_DIR
    elif scenario_num:
        macro_dir = SCENARIO_DIR+'scenario_{}\\'.format(scenario_num)
    for macro_filename in [file for file in os.listdir(macro_dir) if file[-4:] == 'xlsm' and file[:9] in ['Breakeven', 'EconData_', 'DiscField']]:
        wb = openpyxl.load_workbook(macro_dir + macro_filename, read_only=False, keep_vba=True)
        try:
            ws = wb['Sheet1']
        except:
            ws = wb.get_sheet_by_name('Sheet1')
        for option in config.keys():
            ws[config[option]['cell']].value = str(config[option][setting]).upper()
        wb.save(macro_dir + macro_filename)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def gen_prod_periods(start_period, end_period, with_index=False):
    start_year  = int(start_period[:4])
    start_month = start_period[-2:]
    end_year    = int(end_period[:4])
    end_month   = end_period[-2:]
    prod_months = [('0')*(2-len(str(i)))+str(i) for i in range(1,13)]
    month_strs = []
    for prod_year in range(start_year, end_year+1):
        month_strs += ['{}{}'.format(prod_year, prod_month) for prod_month in prod_months]
    start_indx = month_strs.index(decode_str(start_period))
    end_indx   = month_strs.index(decode_str(end_period))
    prod_periods = month_strs[start_indx:end_indx+1]
    if with_index:
        prod_periods = [(prod_periods.index(prod_period), decode_str(prod_period)) for prod_period in prod_periods]
    return prod_periods

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_min_max_periods(sql_where):
    conn = get_connection()
    curr = conn.cursor()
    sql_select = 'SELECT MIN(period) AS start_period, MAX(period) AS end_period FROM well_production WHERE {}'.format(sql_where)
    curr.execute(sql_select)
    start_period, end_period = curr.fetchone()
    curr.close()
    conn.close()
    return start_period, end_period

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def prod_period_list(sql_where):
    start_period, end_period = get_min_max_periods(sql_where)
    prod_periods = gen_prod_periods(start_period, end_period)
    return prod_periods

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_sql_where(prod_config={}, prod_limit_type='any', debug=False):
    conn = get_connection()
    curr = conn.cursor()
    comm = prod_config['commodity']
    sql_where_list = ['commodity="{}"'.format(comm)]
    for filter_param in ['well_id', 'NOT well_id', 'well_name', 'operator', 'region', 'constituent', 'country', 'county', 'basin','formation']:
        if prod_config[filter_param]:
            sql_where_list.append('{} IN ({})'.format(filter_param, ','.join(['"{}"'.format(param_val) for param_val in prod_config[filter_param]])))

    if prod_config['period range'][0]:
        sql_where_list.append('period>="{}"'.format(prod_config['period range'][0]))
    if prod_config['period range'][1]:
        sql_where_list.append('period<="{}"'.format(prod_config['period range'][1]))

    if prod_config['latitude range'][0]:
        sql_where_list.append('latitude>={}'.format(prod_config['latitude range'][0]))
    if prod_config['latitude range'][1]:
        sql_where_list.append('latitude<={}'.format(prod_config['latitude range'][1]))
    if prod_config['longitude range'][0]:
        sql_where_list.append('longitude>={}'.format(prod_config['longitude range'][0]))
    if prod_config['longitude range'][1]:
        sql_where_list.append('longitude<={}'.format(prod_config['longitude range'][1]))

    sql_where = ' AND '.join(sql_where_list)

    if comm == 'Crude Oil':
        if prod_config['oil prod range'][0]:
            sql_where_list.append('production>={} AND commodity="Crude Oil"'.format(prod_config['oil prod range'][0]))
        if prod_config['oil prod range'][1]:
            sql_where_list.append('(production<={0} AND commodity="Crude Oil" AND NOT well_id IN (SELECT DISTINCT well_id WHERE {1} AND production>{0}))'.format(prod_config['oil prod range'][1], sql_where))
    elif comm == 'Natural Gas':
        if prod_config['gas prod range'][0]:
            sql_where_list.append('production>={} AND commodity="Natural Gas"'.format(prod_config['gas prod range'][0]))
        if prod_config['gas prod range'][1]:
            sql_where_list.append('(production<={0} AND commodity="Natural Gas" AND NOT well_id IN (SELECT DISTINCT well_id WHERE {1} AND production>{0}))'.format(prod_config['gas prod range'][1], sql_where))

    sql_where = ' AND '.join(sql_where_list)
    return sql_where

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_lin_vals(p1,p2,seg_pts=100):
    (x1, y1) = p1
    (x2, y2) = p2
    x_seg = np.linspace(x1, x2, seg_pts, endpoint=True)
    m = (y2-y1)/(x2-x1)
    b = y1 - (m*x1)

    def mx_b(x):
        return (m*x) + b

    return mx_b(x_seg).tolist(),m,b

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def to_json(data, filename):
    with open(filename, 'w') as json_file: json.dump(data, json_file)

def from_json(filename):
    data = None
    with open(filename) as json_file: data = json.load(json_file)
    return data

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_data(param, table, sql_where='1=1', sql_limit='', datatype='str', database='globaldata', server='mysql', debug=False, single_value=False, distinct=True, cursor=None, us_wells=False):
    param_values = []
    conn = None
    if cursor is None:
        conn = get_connection(server=server, database=database, us_wells=us_wells)
        curr = conn.cursor()
    else:
        curr = cursor

    if sql_limit:
        sql_where += (' {}'.format(sql_limit))

    distinct_str = ''
    if distinct:
        distinct_str = 'DISTINCT '

    sql_select = 'SELECT {0}{1} FROM {2} WHERE {3} '.format(distinct_str, param, table, sql_where)

    if debug:
        print 'sql_select: {}'.format(sql_select)
    if curr.execute(sql_select):
        data_points = curr.fetchall()
        if debug:
            print ','.join(['{}']*len(data_points)).format(*data_points)
        if datatype == 'int':
            param_values = [int(data[0]) for data in data_points]
        elif datatype == 'str':
            param_values = [str(data[0]) for data in data_points]
        elif datatype == 'float':
            # param_values = [float(data[0]) for data in data_points]
            param_values = [float(data[0]) if data[0] is not None else 0.0 for data in data_points]
        elif datatype == 'plural':
            param_values = list(data_points)
    else:
        param_values = []
    if single_value:
        if len(param_values):
            param_values = param_values[0]
        else:
            param_values = None
    if cursor is None:
        curr.close()
        conn.close()
    return param_values

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def execute(params, table, sql_where='1=1'):
    conn = get_connection()
    curr = conn.cursor()
    datapoints = namedtuple('datapoints', params)
    sql_select = 'SELECT {} FROM {} WHERE {}'.format(','.join(params),table, sql_where)
    curr.execute(sql_select)
    data = map(datapoints._make, curr.fetchall())[:]
    curr.close()
    conn.close()
    return data

def query(query_text):
    query = 'sqlcmd -S 10.55.22.78 -U uswellsdata -P uswellsdata -d US_Wells -Q "{}"'
    os.system(query.format(query_text))

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_typewell_data(well_id, debug=False):
    prod_comms = ['Crude Oil', 'Natural Gas', 'Condensate', 'NGLs', 'LNG', 'Water']
    typewell_data = {comm: {} for comm in prod_comms}
    prod_data = get_data('month, oil_prod_bd, gas_prod_mmcfd, condensate_prod_bd, ngls_prod_bd, lng_prod_mmcfd, water_prod_bd', 'type_well_production', sql_where='well_id="{}"'.format(well_id), datatype='plural')
    for prod_datarow in prod_data:
        if debug:
            print 'prod_datarow: {}'.format(prod_datarow)
        for i in range(len(prod_comms)):
            typewell_data[prod_comms[i]][int(prod_datarow[0])] = float(prod_datarow[i+1])
    if debug:
        print 'typewell_data: {}'.format(typewell_data)
    return typewell_data

def forecast_well_production(well_id='', typewell_data={}, curve_params=None, month_type="num", asset_id=None, well_life=20, debugMode=False):
    days_in_year = 365.242
    max_decline_pct = 0.9999
    if not well_life:
        if asset_id:
            well_life = get_param("well_life", "type_well_inputs", asset_id)
        elif well_id:
            well_life = int(get_param('well_life', 'type_well_inputs', sql_where='well_id="{}"'.format(well_id)))

    if not typewell_data and well_id:
        typewell_data = get_typewell_data(well_id=well_id, debug=debugMode)

    well_comm_list = typewell_data.keys()
    init_prod_start = min([sorted(typewell_data[comm].keys())[0] for comm in well_comm_list])
    init_prod_end = max([sorted(typewell_data[comm].keys())[-1] for comm in well_comm_list])
    init_prod_months = range(1, init_prod_end + 1)

    start_period = init_prod_end
    end_period = int(well_life * 12) + 1
    period_range = range(start_period, end_period)
    prod_periods = sorted(list(set(init_prod_months + period_range)))
    well_prod_data = {comm: {period: 0 for period in prod_periods} for comm in well_comm_list}

    for comm_name in well_comm_list:
        x_new = []
        y_new = []
        for month in sorted(typewell_data[comm_name].keys()):
            y_new.append(typewell_data[comm_name][month])
            x_new.append(init_prod_months.index(month))
            well_prod_data[comm_name][month] = typewell_data[comm_name][month]
        y_new = [typewell_data[comm_name][month] for month in sorted(typewell_data[comm_name].keys())]
        x_new = sorted(typewell_data[comm_name].keys())
        if debugMode:
            print "y_new: {}".format(y_new)
            print "x_new: {}".format(x_new)

        if y_new:
            peak_num = max(y_new)
            peak_index = y_new.index(peak_num)
            peak_month = x_new[peak_index]
            z_new = []
            for iii in range(len(y_new)):
                z_new.append(iii + 1)
            y_prime = y_new[peak_index:]
            x_prime = x_new[peak_index:]
            z_prime = z_new[peak_index:]
            arps_output = DeclineObj(np.array(z_prime), np.array(y_prime))
            # --------------------------------------------------------------------
            results = arps_output()
            curve_type = results[0]
            if debugMode:
                print ""
                print 'TOTAL RESULTS ARRAY'
                print "results:", results
                print "curve_type:", curve_type + ' CURVE TYPE <--------------------------'

            if not curve_params:
                Qi = y_prime[-1]
                b = round(results[1][1], 5)
                Di = round(results[1][-1], 5)
                if Di < 0:
                    Di = -1 * Di
                if b < .05:
                    b = .05
                elif b > .99:
                    b = .9
                else:
                    pass
                # ----------------------------------------
                p = max_decline_pct
                if p < .001:
                    p = .01
                elif p > .999:
                    p = .9
                else:
                    pass
                if days_in_year > 0:
                    Dlim = np.log(1 - p) / (days_in_year)
                else:
                    Dlim = 0
                timeVar = abs(round(((((Di / Dlim) - 1) / b) / Di), 0))
                Qi = y_new[-1]
            else:
                curve_params[comm_name]["Qi"] = Qi
                curve_params[comm_name]["b"] = b
                curve_params[comm_name]["p"] = p
                curve_params[comm_name]["Di"] = Di
                curve_params[comm_name]["Dlim"] = Dlim
                curve_params[comm_name]["timeVar"] = timeVar

            if debugMode:
                print "Curve Parameters------"
                print "comm_name:", comm_name
                print "Qi       :", Qi
                print "b        :", b
                print "p        :", p
                print "Di       :", Di
                print "Dlim     :", Dlim
                print "timeVar  :", timeVar
            ij = 1
            tVar = 0
            firstTime = 1
            firstQx = Qi
            if debugMode:
                print "--- Well Forecast ---"
            for month in period_range:
                if firstTime:
                    power_var = round(-tVar * Dlim, 0)
                    if power_var > 100:
                        power_var = 100
                    if tVar >= timeVar:
                        Qx = Qexp * (math.e ** (power_var))
                    else:
                        if (1 + b * Di * tVar) < 0:
                            exp_base = abs(1 + b * Di * tVar)
                            Qx = (Qi / ((exp_base) ** (1 / b)))
                        else:
                            Qx = (Qi / ((1 + b * Di * tVar) ** (1 / b)))
                    firstTime = 0
                    firstQx = Qx
                else:
                    power_var = round(-tVar * Dlim, 0)
                    if power_var > 100:
                        power_var = 100
                    if tVar >= timeVar:
                        Qexp = (Qi / ((1 + b * Di * timeVar) ** (1 / b))) * (1 / (math.e ** power_var))
                        Qx = Qexp * (math.e ** (power_var))
                    else:
                        Qx = (Qi / ((1 + b * Di * tVar) ** (1 / b)))
                        """
                        if ((1 - b) * Di) * (1 - (1 + b * Di * tVar) ** (1 - (1 / b))) == 0:
                            area = 0
                        else:
                            area = Qi / ((1 - b) * Di) * (1 - (1 + b * Di * tVar) ** (1 - (1 / b)))
                        """

                if Qx != firstQx:
                    if np.isnan(Qx):
                        Qx = 0
                    well_prod_data[comm_name][month] = Qx
                tVar += 1
    return well_prod_data

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def move_files(src_dir, dst_dir, file_extn='xlsx', outfile_code='', asset_list=None, debug=False):
    for asset_model in [filename for filename in os.listdir(src_dir) if filename.endswith(file_extn)]:
        if debug:
            print src_dir + asset_model
        if asset_list:
            asset_id = int(asset_model.split('_')[1])
            if asset_id in asset_list:
                shutil.move(src_dir + asset_model, dst_dir + outfile_code + asset_model)
        else:
            shutil.move(src_dir + asset_model, dst_dir + asset_model)

def copy_files(src_dir, dst_dir, in_ext='', out_ext='', out_format='{}.{}', fname_indx=None, fname_incr=False, debug=False):
    if fname_indx == None:
        fname_indx = -(len(in_ext)+1)
    input_files = [filename for filename in os.listdir(src_dir) if filename.endswith(in_ext)]
    input_file_num = 0
    input_file_count = len(input_files)
    for input_file in input_files:
        input_filename = input_file[:fname_indx]
        if fname_incr:
            output_file = out_format.format(input_filename, input_file_num, out_ext)
        else:
            output_file = out_format.format(input_filename,out_ext)
        if debug:
            print '({}/{}): {} ---> {}'.format(input_file_num, input_file_count, src_dir + input_file, dst_dir + output_file)
        shutil.copy2(src_dir+input_file, dst_dir+output_file)
        input_file_num += 1

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def generate_model_list(asset_list, list_name, split=1):
    if split > 1:
        split_len = len(asset_list)/split
        for i in range(split):
            start_indx = i*split_len
            end_indx   = (i+1)*split_len
            assets = asset_list[start_indx:min(end_indx,len(asset_list))]
            split_list_name = '{}_{}.csv'.format(list_name,i+1)
            with open(TEST_DIR + split_list_name, 'w') as csvfile:
                fieldnames = ['ASSET_ID', 'COUNTRY', 'CONSTITUENT', 'REGION', 'STATUS', 'TERRAIN', 'RESOURCE', 'FACILITY', 'BASIN', 'OPERATOR']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
                writer.writeheader()
                for asid in assets:
                    writer.writerow({'ASSET_ID': asid})
            shutil.copy2(TEST_DIR + split_list_name, MODEL_TASK_DIR + split_list_name)

    else:
        with open(TEST_DIR + '{}.csv'.format(list_name), 'w') as csvfile:
            fieldnames = ['ASSET_ID', 'COUNTRY', 'CONSTITUENT', 'REGION', 'STATUS', 'TERRAIN', 'RESOURCE', 'FACILITY', 'BASIN', 'OPERATOR']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for asid in asset_list:
                writer.writerow({'ASSET_ID': asid})
        shutil.copy2(TEST_DIR + 'DT_1.csv', MODEL_TASK_DIR+'DT_1.csv')

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------




def send_update_email(send_to=[], subject='Engine Update {}', message='', attach_files=[]):
    run_id = get_run_id()
    msg = MIMEMultipart()
    if subject == 'Engine Update {}':
        msg['Subject'] = subject.format(run_id)
    else:
        msg['Subject'] = subject
    msg['From'] = 'titaniiglobaldata@gmail.com'
    msg['To'] = ', '.join(send_to)
    msg.preamble = '{}'.format(get_datetime())

    for filename in attach_files:
        with open(filename) as txt_file:
            txt = MIMEText(txt_file.read())
            txt.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(txt)

    if subject == 'Engine Update {}':
        body = '{} Engine Update for "{}":\n'.format(COMPUTER, run_id)
        body += (message + '\n')
    else:
        body = (message + '\n')
    body_text = MIMEText(body, 'plain')
    msg.attach(body_text)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('titaniiglobaldata@gmail.com', 'Welcome2018')
    server.sendmail('titaniiglobaldata@gmail.com', send_to, msg.as_string())
    server.close()


def send_engine_email():
    message = \
'''
Hello Raja Sekhar and Vasu,

The engine run has been processed and is available for upload from the SQL server.  
Engine files on the SQL server are dated from SQL server files {0}.  
Please upload the data to the staging analytics (http://10.55.22.78/ogicstaging/) and staging dashboard (http://10.55.22.78/OGStagingdashboard_NY/) for review by UA team.   

Data is available for:

1)      Engine Run (including unconventional data) - SQL server files {0}

2)      Automated Project Outlooks (automated panorama) - {0}

3)      Implied Oil and Gas price - {0}
'''
    subject = 'Engine Global Upload, Automated Project Outlook, Implied Prices - {}'
    created_dates = get_data('CreatedDate', 'Engine.tblEngineCommodityPriceSourceData', server='sql_server', database='OGEngineDataExtract')
    if not created_dates:
        engine_date = get_date()
    elif len(created_dates) > 1:
        engine_date = '/'.join(created_dates)
    else:
        engine_date = created_dates[0]
    print 'created_dates: {}'.format(created_dates)
    print 'engine_date: {}'.format(engine_date)
    sql_where = '1=1 GROUP BY Region ORDER BY Region'
    engine_region_counts = get_data('Region, COUNT(*) AS Asset_Count', 'Engine.tblEngineCommodityPriceSourceData', server='sql_server', database='OGEngineDataExtract', sql_where=sql_where, datatype='plural')
    region_counts = '\n'
    print 'engine_region_counts: {}'.format(engine_region_counts)
    for region, asset_count in engine_region_counts:
        region_counts += '{}:\t\t\t{}\n'.format(region, asset_count)
    message += region_counts
    print 'subject: {}'.format(subject)
    print 'message: {}'.format(message)
    email_list = [
        'jason.skophammer@gmail.com',
        'anbabu@gdresearchcenter.com',
        'dbikshapathi@gdresearchcenter.com',
        'rravi@gdresearchcenter.com',
        'asia_dba@gdresearchcenter.com',
        'ealleyne@globaldata.com',
        'abelova@globaldata.com',
        'adrian.lara@globaldata.com',
        'svetlana.doh@globaldata.com',
        'gbosunga@globaldata.com',
        'steven.ho@globaldata.com',
        'andrew.folse@globaldata.com',
        'wscargill@globaldata.com',
        'toya.latham@globaldata.com',
        'daniel.rogers@globaldata.com',
        'joseph.wisdom@globaldata.com',
        'somayeh.davodi@globaldata.com',
        'cao.chai@globaldata.com',
        'conor.ward@globaldata.com',
        'jason.skophammer@globaldata.com',
        'syadav@globaldata.com',
        'swsingh@gdresearchcenter.com'
    ]
    send_update_email(send_to=email_list,subject=subject.format(engine_date), message=message.format(engine_date), attach_files=[])

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_median(value_list):
    sorted_vals = sorted(value_list)
    list_half = len(sorted_vals)/2
    indx1 = list_half
    indx2 = -(indx1 + 1)
    median_val = float(sorted_vals[indx1] + sorted_vals[indx2])/2.0
    return median_val

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
CREATE TABLE US_Wells.dbo.Well_Engine_Variables (
  current_year           INT         DEFAULT NULL,
  well_engine_group      INT         DEFAULT NULL,
  well_forecast_code     INT         DEFAULT NULL,
  well_details_updated   VARCHAR(25) DEFAULT NULL,
  last_package_id        INT         DEFAULT NULL,
  non_tx_forecast_id     VARCHAR(25) DEFAULT NULL,
  tx_forecast_id         VARCHAR(25) DEFAULT NULL,
  non_tx_engine_start    VARCHAR(25) DEFAULT NULL,
  tx_engine_start        VARCHAR(25) DEFAULT NULL);

CREATE TABLE US_Wells.dbo.Well_Engine_Stats (
  non_tx_forecast_id     VARCHAR(25) DEFAULT NULL,
  tx_forecast_id         VARCHAR(25) DEFAULT NULL,
  non_tx_prod_updated    VARCHAR(25) DEFAULT NULL,
  non_tx_well_count      INT         DEFAULT NULL,
  non_tx_engine_start    INT         DEFAULT NULL,
  non_tx_export_date     INT         DEFAULT NULL,
  tx_prod_updated        VARCHAR(25) DEFAULT NULL,
  tx_api_updated         VARCHAR(25) DEFAULT NULL,
  tx_wellbore_updated    VARCHAR(25) DEFAULT NULL,
  tx_permit_updated      VARCHAR(25) DEFAULT NULL,
  tx_sched_updated       VARCHAR(25) DEFAULT NULL,
  tx_comp_updated        VARCHAR(25) DEFAULT NULL,
  tx_details_updated     VARCHAR(25) DEFAULT NULL,
  tx_oil_well_count      INT         DEFAULT NULL,
  tx_gas_well_count      INT         DEFAULT NULL,
  tx_gas_engine_start    VARCHAR(25) DEFAULT NULL,
  tx_gas_export_date     VARCHAR(25) DEFAULT NULL,
  tx_gas_engine_time     VARCHAR(25) DEFAULT NULL,
  tx_oil_engine_start    VARCHAR(25) DEFAULT NULL,
  tx_oil_export_date     VARCHAR(25) DEFAULT NULL,
  tx_oil_engine_time     VARCHAR(25) DEFAULT NULL,
  non_tx_engine_time     VARCHAR(25) DEFAULT NULL,
  total_tx_engine_time   VARCHAR(25) DEFAULT NULL,
  total_engine_time      VARCHAR(25) DEFAULT NULL);

CREATE TABLE US_Wells.dbo.Well_Engine_Process_Log (
  log_id         INT IDENTITY,
  forecast_id    VARCHAR(25) DEFAULT NULL,
  state_group    VARCHAR(25) DEFAULT NULL,
  stage_code     INT         DEFAULT NULL,
  stage_name     VARCHAR(90) DEFAULT NULL,
  process_code   FLOAT       DEFAULT NULL,
  process_name   VARCHAR(90) DEFAULT NULL,
  engine_start   VARCHAR(25) DEFAULT NULL,
  engine_export  VARCHAR(25) DEFAULT NULL,
  stage_start    VARCHAR(25) DEFAULT NULL,
  stage_end      VARCHAR(25) DEFAULT NULL,
  process_start  VARCHAR(25) DEFAULT NULL,
  process_end    VARCHAR(25) DEFAULT NULL,
  PRIMARY KEY(log_id));

"""
def get_engine_start(state_group):
    pass


def get_stage_start(forecast_id, stage_code):
    pass


def update_well_engine_variables(curr):
    pass


def create_process_log_entry(curr, forecast_id, state_group, process_code, process_start):
    sql_insert = \
    """
    INSERT INTO US_Wells.dbo.Well_Engine_Process_Log (forecast_id, state_group, stage_code, stage_name, process_code, process_name, engine_start, stage_start, process_start)
      VALUES ('{}', '{}', {}, '{}', {}, '{}', '{}', '{}', '{}')
    """
    process_start = get_datetime()
    stage_code    = int(process_code//1)
    stage_name    = WELL_ENGINE_STAGE_CODES[stage_code]
    process_name  = WELL_ENGINE_PROCESS_CODES[process_code]
    if process_code - float(stage_code) == 0.1:
        stage_start = process_start
        if stage_code == 1:
            engine_start = process_start
            if state_group == 'tx':
                engine_start_col = 'tx_engine_start'
            else:
                engine_start_col = 'non_tx_engine_start'
            update_well_engine_variables(curr, engine_start_col, engine_start)
        else:
            engine_start = get_engine_start(state_group)
    else:
        engine_start = get_engine_start(state_group)
        stage_start = get_stage_start(forecast_id, stage_code)
    curr.execute(sql_insert.format(forecast_id, state_group, stage_code, stage_name, process_code, process_name, engine_start, stage_start, process_start))
    commit(curr)


def update_process_log_entry(curr):
    pass

def get_engine_group():
    engine_group = get_data('well_engine_group', 'dbo.Well_Engine_Variables', server='sql_server', database='US_Wells', datatype='int', single_value=True, us_wells=True)
    print 'engine group: {}'.format(engine_group)
    return engine_group

def set_engine_group(new_engine_group):
    conn = get_connection(server='sql_server', database='US_Wells', us_wells=True)
    curr = conn.cursor()
    curr.execute('UPDATE US_Wells.dbo.Well_Engine_Variables SET well_engine_group={}'.format(new_engine_group))
    commit(curr)
    curr.close()
    conn.close()

    print 'new engine group: {}'.format(new_engine_group)


def incr_engine_group():
    curr_engine_group = get_engine_group()
    new_engine_group = (curr_engine_group + 1) % 5
    set_engine_group(new_engine_group)


def reset_engine_group():
    set_engine_group(0)

def get_forecast_code():
    forecast_code = get_data('well_forecast_code', 'dbo.Well_Engine_Variables', server='sql_server', database='US_Wells', datatype='int', single_value=True, us_wells=True)
    return forecast_code

def set_forecast_code(new_forecast_code):
    conn = get_connection(server='sql_server', database='US_Wells', us_wells=True)
    curr = conn.cursor()

    curr.execute('UPDATE US_Wells.dbo.Well_Engine_Variables SET well_forecast_code={}'.format(new_forecast_code))
    commit(curr)

    curr.close()
    conn.close()

def incr_forecast_code():
    set_forecast_code((get_forecast_code() % 4)+1)

def reset_forecast_code():
    set_forecast_code(1)

def create_forecast_id(state_group='non_tx', debug=False):
    assert state_group in ['non_tx', 'tx']
    conn = get_connection(server='sql_server', database='US_Wells', us_wells=True)
    curr = conn.cursor()
    forecast_id = '{}_{}'.format(get_date(), randint(100000,999999))
    if debug: print "UPDATE Well_Engine_Variables SET {}_forecast_id='{}'".format(state_group, forecast_id)
    curr.execute("UPDATE Well_Engine_Variables SET {}_forecast_id='{}'".format(state_group, forecast_id))
    commit(curr)
    curr.close()
    conn.close()
    return forecast_id

def get_forecast_id(state_group='non_tx'):
    assert state_group in ['non_tx', 'tx']
    forecast_id = get_data('{}_forecast_id'.format(state_group), 'dbo.Well_Engine_Variables', server='sql_server', database='US_Wells', single_value=True, us_wells=True)
    return forecast_id

def get_session_count():
    session_count = get_data('session_count', 'dbo.Well_Engine_Variables', server='sql_server', database='US_Wells', datatype='int', single_value=True, us_wells=True)
    print 'session count: {}'.format(session_count)
    return session_count

def set_session_count(new_session_count):
    conn = get_connection(server='sql_server', database='US_Wells', us_wells=True)
    curr = conn.cursor()
    curr.execute('UPDATE US_Wells.dbo.Well_Engine_Variables SET session_count={}'.format(new_session_count))
    commit(curr)
    curr.close()
    conn.close()

    print 'new session count: {}'.format(new_session_count)

def incr_session_count():
    curr_session_count = get_session_count()
    new_session_count = (curr_session_count % 5) + 1
    set_session_count(new_session_count)

def reset_session_count():
    set_session_count(0)

def check_well_engine_session():
    process_complete = False
    incr_session_count()
    new_session_count = get_session_count()
    if new_session_count == 5:
        process_complete = True
        reset_session_count()
    return process_complete

def set_engine_list(engine_list):
    conn = get_connection(server='sql_server', database='US_Wells', us_wells=True)
    curr = conn.cursor()
    curr.execute("UPDATE US_Wells.dbo.Well_Engine_Variables SET engine_list='{}'".format(engine_list))
    commit(curr)
    curr.close()
    conn.close()

def get_engine_list():
    engine_list = get_data('engine_list', 'dbo.Well_Engine_Variables', server='sql_server', database='US_Wells', single_value=True, us_wells=True)
    return engine_list

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------




if __name__=='__main__':
    conn = get_connection(server='sql_server', database='US_Wells', us_wells=True)
    curr = conn.cursor()

    reset_engine_group()

    curr.close()
    conn.close()