import datetime as dt

from globaldata import *
from globaldata.constants import TABLE_CONFIG, TABLE_COLUMNS




def get_connection(connection_type, external=False):
    if connection_type == 'ext':
        if external:
            conn = pypyodbc.connect('Driver={SQL Server}; Server=10.55.22.78; Database=OGEngineDataExtract; uid=uswellsdata; pwd=uswellsdata')
        else:
            conn = pypyodbc.connect('Driver={SQL Server}; Server=localhost; Database=OGEngineDataExtract; Trusted_Connection=True; unicode_results=True;')
    elif connection_type == 'int':
        # conn = pymysql.connect(host='localhost', db='globaldata', user='root', passwd='OilAndGas321', charset='utf8', use_unicode=True)
        conn = pymysql.connect(host='10.8.114.14', db='globaldata', user='titan', passwd='}2Ek}dTd*Z)k_dCI_Pm%', charset='utf8',
                               use_unicode=True)
    return conn


def get_dates():
    dtime_today = dt.datetime.now()
    today = dtime_today.strftime('%Y-%m-%d')
    dtime_tomorrow = dt.date.today() + dt.timedelta(days=1)
    tomorrow = dtime_tomorrow.strftime('%Y-%m-%d')
    dtime_yesterday = dt.date.today() + dt.timedelta(days=-1)
    yesterday = dtime_yesterday.strftime('%Y-%m-%d')
    return yesterday, today, tomorrow


def clear_table(curr_int, int_table):
    sql_truncate = 'TRUNCATE %s'
    sql_truncate = sql_truncate % int_table
    curr_int.execute(sql_truncate)
    curr_int.execute('COMMIT')


def get_conv_factor(curr, commodity, unit):
    conv_factor = 1.0
    sql_select = "SELECT factor FROM unit_equals WHERE commodity='{}' and unit='{}' and base_unit='Boe'"
    prod_comm = commodity.lower().strip()
    comm_unit = unit.lower().strip()
    if prod_comm == 'ngl': prod_comm = 'ngls'
    if curr.execute(sql_select.format(prod_comm, comm_unit)):
        conv_factor = float(curr.fetchone()[0])
    return conv_factor


def find_peak_year(curr, asset_id):
    prod_start, capex_end = get_data('prod_start_year, capex_end_year', 'asset_prod_data', cursor=curr, datatype='plural', single_value=True, sql_where='asset_id={}'.format(asset_id))
    peak_sourced_year = prod_start
    peak_prod_val = 0
    sql_where = 'period={} AND casetype="Base Case" AND sources!="EST: Forecast Engine" AND asset_id={} AND IFNULL(production,0) > 0'
    for prod_year in range(prod_start, capex_end + 1):
        prod_year_val = 0
        prod_data = get_data('commodity, production, unit', 'production', cursor=curr, datatype='plural', sql_where=sql_where.format(prod_year, asset_id))
        if prod_data:
            for prod_comm, prod_value, prod_unit in prod_data:
                conv_factor = get_conv_factor(curr, prod_comm, prod_unit)
                prod_value *= conv_factor
                prod_year_val += prod_value
        if prod_year_val > peak_prod_val:
            peak_prod_val = prod_year_val
            peak_sourced_year = prod_year
    return peak_sourced_year


def update_peak_prod_year(curr):
    sql_update = 'UPDATE asset_prod_data SET peak_prod_year={} WHERE asset_id={}'
    asset_ids = get_data('asset_id', 'projects_extract', cursor=curr, datatype='int') #Uncomment After Debug
    # asset_ids=(736815,739076)
    asset_count = len(asset_ids)
    asset_num = 1
    for asset_id in asset_ids:
        print '{}/{}: {}'.format(asset_num, asset_count, asset_id)
        try:
            peak_prod_year = find_peak_year(curr, asset_id)
            curr.execute(sql_update.format(peak_prod_year, asset_id))
            commit(curr)
        except:
            pass
        asset_num += 1

def format_data(entry):
    if isinstance(entry, str):
        if '"' in entry:
            entry = entry.replace('"', '')
        if entry[-1] == '\\':
            entry += '\\'
    entry = unicode(str(entry), errors='ignore')
    return entry


def format_import_data(data_row, int_table):
    formatted_data = ()
    for i in range(len(data_row)):
        entry = format_data(data_row[i])
        if not entry.isnumeric():
            entry = str(entry)
        if entry in [None, 'None', 'NULL'] and (i in TABLE_CONFIG[int_table]['date_cols']):
            entry = get_add_date()
        if entry in [None, 'None', 'NULL'] and (i in TABLE_CONFIG[int_table]['num_cols']):
            entry = 0.0
        if isinstance(entry, str):
            if (len(entry) == 10 and entry[2] == '/' and entry[5] == '/'):
                entry = dt.datetime.strptime(entry, '%m/%d/%Y')
        formatted_data += (entry,)
    return formatted_data


def process_import_data(curr_int, import_data, int_table, ext_table, user_name, add_date):
    if int_table == 'sourced_expend':
        column_list_int = ['asset_id','asset_name','country','constituent','region','expend_type','expend_year','expend_period','currency','unit','expend_value','extract_date']
    elif int_table == 'currency_exchange':
        column_list_int = ['currency_id', 'exchange_year', 'from_currency', 'to_currency', 'exchange_factor']
    elif int_table == 'projects_extract':
        column_list_int = ['asset_id','project_name','project_segment','project_country','project_region','project_type','project_stage','project_active_year','project_cost','project_asset_id','epc_contractor','stage_change_quarter','fid']
    elif int_table == 'assets':
        column_list_int = ['asset_id',	'asset_name',	'country',	'constituent',	'region',	'status',	'terrain',	'basin',	'resource_type',	'prod_phase',	'recover_factor',	'assoc_asset_id',	'assoc_asset_name',	'assoc_region',	'assoc_country',	'assoc_area',	'trap_type',	'api_gravity',	'sulfer',	'lic_no',	'county',	'calorific',	'hsulfer',	'gor',	'ablock',	'ablock_region',	'ablock_country',	'ablock_constituent',	'asset_relation',	'irr',	'payback_years',	'capex',	'opex',	'reserve_status',	'npv',	'bc_npv',	'lc_npv',	'hc_npv',	'facility_type',	'formation',	'water_depth',	'discovery_date',	'license_num',	'license_effective',	'license_expire',	'porosity',	'permeability',	'measured_depth',	'carbon_dioxide',	'form_rock_type',	'data_source',	'fiscal_regime',	'last_update','add_by','add_date']
    elif int_table == 'equity':
        column_list_int = ['asset_id',	'asset_name',	'country',	'constituent',	'region',	'entity_name',	'equity_pct',	'equity_date',	'operator',	'last_update',	'top_parent_company',	'profit_share',	'cost_share',	'add_by',	'add_date']
    elif int_table == 'production':
        column_list_int = ['asset_id',	'asset_name',	'country',	'constituent',	'region',	'commodity',	'period',	'production',	'unit',	'casetype',	'asset_relationship',	'sources',	'data_source',	'last_update',	'add_by',	'add_date']
    elif int_table == 'reserves':
        column_list_int = ['asset_id',	'asset_name',	'country',	'constituent',	'region',	'field_status',	'reserve_status',	'reserve_type',	'commodity',	'reserve_pub_date',	'reserve_volume',	'unit',	'reserve_source',	'casetype',	'data_source',	'last_update',	'add_by',	'add_date']
    else:
        column_list_int = get_column_list_(curr_int, 'globaldata', int_table, 'globaldata')[1:-2]
    num_cols = len(column_list_int)
    column_str_int = ','.join(column_list_int)
    params_int = (int_table,)
    count = 0
    for data_row in import_data:
        null_indxs = []
        param_vals = ()
        for i in range(len(data_row)):
            if data_row[i] in [None, 'None']:
                param_vals += ('NULL',)
            else:
                param_vals += (data_row[i],)
        if int_table in ['sourced_expend', 'currency_exchange', 'projects_extract']:
            param_count = len(TABLE_CONFIG[int_table]['cols'])
        else:
            param_count = len(TABLE_CONFIG[int_table]['cols']) + 2
        format_list = ['%s']*param_count
        format_str = ', '.join(format_list)
        params_int = (int_table, column_str_int, format_str)
        sql_insert = 'INSERT INTO %s (%s) VALUES (%s)'
        sql_insert = sql_insert % params_int
        formatted_data = format_import_data(param_vals, int_table)
        if int_table in ['sourced_expend', 'currency_exchange', 'projects_extract']:
            params = formatted_data
        else:
            params = formatted_data + (user_name, add_date)
        curr_int.execute(sql_insert, params)
        count += 1
        if count % 1000 == 0:
            processed_pct = round(float(count)/float(len(import_data)), 4) * 100
            print str(processed_pct) + '% ' + ext_table + ' data processed'


def get_column_list_(curr, database, table_name, schema_name):
    col_list = []
    curr.execute('USE %s' % database)
    ordering_by='ORDINAL_POSITION'
    sql_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND TABLE_SCHEMA='%s'" % (table_name, schema_name)
    # sql_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND TABLE_SCHEMA='%s' ORDER BY '%s' " % (table_name, schema_name ,ordering_by)
    curr.execute(sql_query)
    col_names = curr.fetchall()
    for col_name in col_names:
        col_list.append(unicode(str(col_name[0]), errors='ignore'))
    return col_list


def get_import_data(curr_ext, ext_table, current):
    print 'Retrieving import data...'
    if 'Production' in ext_table:
        table_ref = 'tblFieldProductionExtract'
    else:
        table_ref = ext_table
    column_list_ext = TABLE_COLUMNS[table_ref]
    column_str_ext = '],['.join(column_list_ext)
    column_str_ext = '[' + column_str_ext + ']'
    yesterday, today, tomorrow = get_dates()
    if current:
        # day_1 = today
        ###To facilitate data import when required
        day_1 = (dt.date.today() + dt.timedelta(days=-6)).strftime('%Y-%m-%d')
        day_2 = tomorrow

    else:
        day_1 = yesterday
        day_2 = today
    if ext_table in ['tblGESourcedExpenditureDataExtract', 'tblGECurrency', 'tblFieldProjectsExtract']:
        sql_query = "SELECT {} FROM {}".format(column_str_ext, 'dbo.' + ext_table)
    else:
        params_ext = (column_str_ext, 'dbo.' + ext_table, day_1, day_2)
        print 'day 1:', day_1
        print 'day 2:', day_2
        sql_query = "SELECT %s FROM %s WHERE ExtractDate BETWEEN '%s' AND '%s'"
        sql_query = sql_query % params_ext
    print sql_query
    curr_ext.execute(sql_query)
    import_data = curr_ext.fetchall()
    print import_data[:10]
    return import_data


def update_tables(curr_int, external=False, int_table='', regions=None, current=True):
    user_name = getpass.getuser()
    time_stamp = time.time()
    add_date = dt.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    if regions:
        ext_tables = ['tblFieldProductionExtract_' + region for region in regions]
    else:
        ext_tables = TABLE_CONFIG[int_table]['ext_tables']

    conn_ext = get_connection('ext', external)
    curr_ext = conn_ext.cursor()
    ext_record_count = 0
    int_record_count = 0

    for ext_table in ext_tables:
        table_record_count = get_record_count(curr_ext, ext_table)
        ext_record_count += table_record_count

    if ext_record_count:
        clear_table(curr_int, int_table)
        ext_record_count = 0
        int_record_count = 0
        for ext_table in ext_tables:
            table_record_count = get_record_count(curr_ext, ext_table)
            ext_record_count += table_record_count
            print ext_record_count, 'records found'
            print 'Processing ' + ext_table
            import_data = get_import_data(curr_ext, ext_table, current)
            process_import_data(curr_int, import_data, int_table, ext_table, user_name, add_date)
            curr_int.execute('COMMIT')
            int_record_count += get_record_count(curr_int, int_table)
            print int_record_count, 'records received'
    curr_ext.close()
    conn_ext.close()


def data_record_check(curr, int_record_count, ext_record_count, int_table):
    if ext_record_count == int_record_count:
        print 'All records received'
    else:
        print 'Data Record Error:'
        print ext_record_count, 'records found'
        print int_record_count, 'records received'
        print 'Deleting records from', int_table, '...'
        curr.execute('TRUNCATE TABLE %s' % int_table)
        curr.execute('COMMIT')
        sys.exit(1)


def get_record_count(curr, table):
    sql_query = 'SELECT COUNT(*) FROM %s'
    curr.execute(sql_query % table)
    record_count = curr.fetchone()[0]
    return record_count


def update_projects_extract(curr_int, debug=False):
    sql_update_1 = \
    '''
    DELETE FROM projects_extract WHERE project_cost='NULL'
    '''

    sql_update_1a = \
    '''
    UPDATE projects_extract SET stage_change_quarter=CONCAT('Q1 ',SUBSTRING(stage_change_quarter,1,4)) 
      WHERE LENGTH(stage_change_quarter)=10 AND SUBSTRING(stage_change_quarter,6,2) IN ('01', '02', '03');
    '''
    sql_update_1b = \
    '''
    UPDATE projects_extract SET stage_change_quarter=CONCAT('Q2 ',SUBSTRING(stage_change_quarter,1,4)) 
      WHERE LENGTH(stage_change_quarter)=10 AND SUBSTRING(stage_change_quarter,6,2) IN ('04', '05', '06');
    '''
    sql_update_1c = \
    '''
    UPDATE projects_extract SET stage_change_quarter=CONCAT('Q3 ',SUBSTRING(stage_change_quarter,1,4)) 
      WHERE LENGTH(stage_change_quarter)=10 AND SUBSTRING(stage_change_quarter,6,2) IN ('07', '08', '09');
    '''
    sql_update_1d = \
    '''
    UPDATE projects_extract SET stage_change_quarter=CONCAT('Q4 ',SUBSTRING(stage_change_quarter,1,4)) 
      WHERE LENGTH(stage_change_quarter)=10 AND SUBSTRING(stage_change_quarter,6,2) IN ('10', '11', '12');
    '''


    sql_update_2a = \
    '''
    UPDATE projects_extract SET fid=CONCAT('Q1 ',SUBSTRING(fid,1,4)) 
      WHERE LENGTH(fid)=10 AND SUBSTRING(fid,6,2) IN ('01', '02', '03');    
    '''
    sql_update_2b = \
    '''
    UPDATE projects_extract SET fid=CONCAT('Q2 ',SUBSTRING(fid,1,4)) 
      WHERE LENGTH(fid)=10 AND SUBSTRING(fid,6,2) IN ('04', '05', '06');    
    '''
    sql_update_2c = \
    '''
    UPDATE projects_extract SET fid=CONCAT('Q3 ',SUBSTRING(fid,1,4)) 
      WHERE LENGTH(fid)=10 AND SUBSTRING(fid,6,2) IN ('07', '08', '09');    
    '''
    sql_update_2d = \
    '''
    UPDATE projects_extract SET fid=CONCAT('Q4 ',SUBSTRING(fid,1,4)) 
      WHERE LENGTH(fid)=10 AND SUBSTRING(fid,6,2) IN ('10', '11', '12');    
    '''

    sql_update_2 = \
    '''
    DELETE FROM projects_extract WHERE project_type != 'New'
    '''
    sql_update_3 = \
    '''
    TRUNCATE TABLE asset_prod_data
    '''
    sql_update_4 = \
    '''
    INSERT INTO asset_prod_data (asset_id, prod_start_year, capex_end_year)
     (SELECT asset_id, MIN(period) AS prod_start_year, MIN(period)+5 AS capex_end_year FROM production
      WHERE IFNULL(production,0) > 0 AND casetype='Base Case' AND sources!='EST: Forecast Engine' AND asset_id IN (SELECT DISTINCT asset_id FROM projects_extract) GROUP BY asset_id)
    '''


    sql_update_5 = \
    '''
    INSERT INTO sourced_expend (asset_id, asset_name, country, region, expend_type, expend_year, start_year, end_year, expend_period, currency, unit, expend_value)
     (SELECT DISTINCT a.asset_id, a.project_name, a.project_country, a.project_region, 'Dev Capex', b.prod_start_year-5, b.prod_start_year-5, b.peak_prod_year, (b.peak_prod_year-b.prod_start_year)+6,'USD','Million',a.project_cost
      FROM projects_extract AS a, asset_prod_data AS b WHERE a.asset_id=b.asset_id AND a.project_type='New' AND a.project_cost!='NULL')
    '''


    #curr_int.execute(sql_update_1)
    #commit(curr_int)
    print sql_update_1a
    curr_int.execute(sql_update_1a)
    commit(curr_int)
    print sql_update_1b
    curr_int.execute(sql_update_1b)
    commit(curr_int)
    print sql_update_1c
    curr_int.execute(sql_update_1c)
    commit(curr_int)
    print sql_update_1d
    curr_int.execute(sql_update_1d)
    commit(curr_int)
    print sql_update_2a
    curr_int.execute(sql_update_2a)
    commit(curr_int)
    print sql_update_2b
    curr_int.execute(sql_update_2b)
    commit(curr_int)
    print sql_update_2c
    curr_int.execute(sql_update_2c)
    commit(curr_int)
    print sql_update_2d
    curr_int.execute(sql_update_2d)
    commit(curr_int)
    
    #curr_int.execute(sql_update_2)
    #commit(curr_int)
    print sql_update_3
    curr_int.execute(sql_update_3)
    commit(curr_int)
    print sql_update_4
    curr_int.execute(sql_update_4)
    commit(curr_int)
    print sql_update_1a
    update_peak_prod_year(curr_int)
    print sql_update_5
    curr_int.execute(sql_update_5)
    commit(curr_int)


def update_overlap_data(curr):
    for expend_type in ['Operating', 'Dev Capex']:
        sql_where = \
            '''
			asset_id IN (SELECT DISTINCT asset_id FROM sourced_expend WHERE expend_type='{0}' AND expend_period='1') AND
			asset_id IN (SELECT DISTINCT asset_id FROM sourced_expend WHERE expend_type='{0}' AND expend_period>1)
			'''
        sourced_ids = get_data('asset_id', 'sourced_expend', cursor=curr, datatype='int',
                               sql_where=sql_where.format(expend_type))
        for asset_id in sourced_ids:
            sql_where = \
                '''
				expend_type='{0}' AND expend_period>1 AND asset_id={1}
				'''
            sourced_range = get_data('start_year, end_year, expend_period, usd_value', 'sourced_expend', cursor=curr,
                                     datatype='plural', sql_where=sql_where.format(expend_type, asset_id))
            for start_year, end_year, expend_period, period_usd_value in sourced_range:
                expend_period = int(expend_period)
                # Resolve Start Year Overlap Periods
                sql_where = \
                    '''
					expend_period='1' AND expend_type='{0}' AND asset_id={1} AND expend_year='{2}'
					'''
                sourced_data = get_data('expend_year, usd_value', 'sourced_expend', cursor=curr, datatype='plural',
                                        sql_where=sql_where.format(expend_type, asset_id, start_year))
                for expend_year, usd_value in sourced_data:
                    expend_year = int(expend_year)
                    sql_update = \
                        '''
						UPDATE sourced_expend SET expend_period='{4}', start_year={5}, usd_value={6}, currency='USD', unit='Million', expend_value={7}
						  WHERE expend_type='{0}' AND asset_id={1} AND expend_period='{2}' AND start_year={3}
						'''
                    curr.execute(sql_update.format(expend_type, asset_id, expend_period, start_year, expend_period - 1,
                                                   start_year + 1, period_usd_value - usd_value,
                                                   round((period_usd_value - usd_value) / 1000000.0, 1)))
                    commit(curr)
                    expend_period -= 1
                    period_usd_value -= usd_value
                    start_year += 1
                
                # Resolve End Year Overlap Periods
                sql_where = \
                    '''
					expend_period='1' AND expend_type='{0}' AND asset_id={1} AND expend_year='{2}'
					'''
                sourced_data = get_data('expend_year, usd_value', 'sourced_expend', cursor=curr, datatype='plural',
                                        sql_where=sql_where.format(expend_type, asset_id, end_year))
                for expend_year, usd_value in sourced_data:
                    sql_update = \
                        '''
						UPDATE sourced_expend SET expend_period='{4}', end_year={5}, usd_value={6}, currency='USD', unit='Million', expend_value={7}
						  WHERE expend_type='{0}' AND asset_id={1} AND expend_period='{2}' AND end_year={3}
						'''
                    curr.execute(sql_update.format(expend_type, asset_id, expend_period, end_year, expend_period - 1,
                                                   end_year - 1, period_usd_value - usd_value,
                                                   round((period_usd_value - usd_value) / 1000000.0, 1)))
                    commit(curr)
                    expend_period -= 1
                    period_usd_value -= usd_value
                    end_year -= 1


def update_sourced_expend(curr_int, debug=False):
    sql_update_0 = \
        '''
		DELETE FROM sourced_expend WHERE NOT expend_type IN ('Operating', 'Dev Capex', 'Other');
		'''
    sql_update_1 = \
        '''
		UPDATE sourced_expend SET expend_period='1' WHERE expend_period='NULL'
		'''
    sql_update_2 = \
        '''
		UPDATE sourced_expend SET start_year=CAST(expend_year AS UNSIGNED), end_year=CAST(expend_year AS UNSIGNED) + CAST(expend_period AS UNSIGNED) - 1
		'''
    sql_update_3 = \
        '''
		UPDATE sourced_expend AS a, currency_exchange AS b
		  SET a.usd_value=ROUND((a.expend_value + 0.0)*b.exchange_factor,5)
		  WHERE a.currency!='USD' AND a.unit IN ('Per boe', 'Per bbl') AND a.start_year=b.exchange_year AND a.currency=b.from_currency
		'''
    sql_update_4 = \
        '''
		UPDATE sourced_expend AS a, currency_exchange AS b
		  SET a.usd_value=ROUND(((a.expend_value + 0.0)*1000000)*b.exchange_factor,5)
		  WHERE a.currency!='USD' AND a.unit='Million' AND a.start_year=b.exchange_year AND a.currency=b.from_currency
		'''
    sql_update_5 = \
        '''
		UPDATE sourced_expend AS a, currency_exchange AS b
		  SET a.usd_value=ROUND(((a.expend_value + 0.0)*1000000000)*b.exchange_factor,5)
		  WHERE a.currency!='USD' AND a.unit='Billion' AND a.start_year=b.exchange_year AND a.currency=b.from_currency
		'''
    sql_update_6 = \
    '''
    UPDATE sourced_expend SET usd_value=ROUND((expend_value + 0.0)*1000000,5) WHERE currency='USD' AND unit='Million'
    '''
    sql_update_7 = \
    '''
    UPDATE sourced_expend SET usd_value=ROUND((expend_value + 0.0)*1000000000,5) WHERE currency='USD' AND unit='Billion'
    '''
    sql_update_8 = \
    '''
    UPDATE sourced_expend SET usd_value=ROUND((expend_value + 0.0),5) WHERE currency='USD' AND unit IN ('Per boe', 'Per bbl')
    '''
    sql_update_9a = \
    '''
    UPDATE projects_extract SET total_sourced_expend=0;
    '''
    sql_update_9b = \
    '''
    UPDATE projects_extract SET project_cost_exceeded=-1;
    '''
    sql_update_9c = \
    '''
    UPDATE projects_extract SET project_cost=0 WHERE project_cost='NULL';
    '''
    sql_update_9d = \
    '''
    UPDATE projects_extract AS a,
           (SELECT DISTINCT asset_id, (SUM(usd_value)/1000000.0) AS total_sourced_expend FROM sourced_expend WHERE extract_date IS NOT NULL AND expend_type='Dev Capex' GROUP BY asset_id) AS b
      SET a.total_sourced_expend=b.total_sourced_expend
      WHERE a.asset_id=b.asset_id;
    '''
    sql_update_9e = \
    '''
    UPDATE projects_extract SET project_cost_exceeded=0 WHERE project_type='New' AND total_sourced_expend=0 AND project_cost > 0;
    '''
    sql_update_9f = \
        '''
		UPDATE projects_extract SET project_cost_exceeded=1 WHERE project_type='New' AND total_sourced_expend > 0 AND total_sourced_expend < project_cost;
		'''
    sql_update_9g = \
        '''
		UPDATE sourced_expend AS a,
		  projects_extract AS b,
		  (SELECT DISTINCT asset_id, expend_type, MAX(end_year) AS last_expend_year
		    FROM sourced_expend WHERE extract_date IS NOT NULL AND asset_id IN (SELECT DISTINCT asset_id FROM projects_extract WHERE project_cost_exceeded=1) GROUP BY asset_id, expend_type) AS c
		  SET a.expend_value=(b.project_cost-b.total_sourced_expend), a.usd_value=ROUND((b.project_cost-b.total_sourced_expend)*1000000.0,2), a.start_year=(c.last_expend_year+1), a.expend_year=(c.last_expend_year+1)
		  WHERE b.project_cost_exceeded=1 AND a.extract_date IS NULL AND a.asset_id=b.asset_id AND a.asset_id=c.asset_id AND a.expend_type=c.expend_type;
		'''
    sql_update_10 = \
        '''
		DELETE FROM sourced_expend WHERE extract_date IS NULL AND asset_id IN (SELECT DISTINCT asset_id FROM projects_extract WHERE project_cost_exceeded=-1 AND project_cost!='NULL' AND project_type='New')
		'''
    # Added this on Feb10-2026 by Sunil to remove zero values in Dev Capex and Opex Values from Sourced_expenditure table
    sql_update_11 = \
        '''
        DELETE FROM sourced_expend WHERE expend_type= 'Dev Capex' and usd_value = 0 ;
        '''
    curr_int.execute(sql_update_0)
    print sql_update_0
    commit(curr_int)
    curr_int.execute(sql_update_1)
    print sql_update_1
    commit(curr_int)
    curr_int.execute(sql_update_2)
    print sql_update_2
    commit(curr_int)
    curr_int.execute(sql_update_3)
    print sql_update_3
    commit(curr_int)
    curr_int.execute(sql_update_4)
    print sql_update_4
    commit(curr_int)
    curr_int.execute(sql_update_5)
    print sql_update_5
    commit(curr_int)
    curr_int.execute(sql_update_6)
    print sql_update_6
    commit(curr_int)
    curr_int.execute(sql_update_7)
    print sql_update_7
    commit(curr_int)
    curr_int.execute(sql_update_8)
    print sql_update_8
    commit(curr_int)
    curr_int.execute(sql_update_9a)
    print sql_update_9a
    commit(curr_int)
    curr_int.execute(sql_update_9b)
    print sql_update_9b
    commit(curr_int)
    curr_int.execute(sql_update_9c)
    print sql_update_9c
    commit(curr_int)
    curr_int.execute(sql_update_9d)
    print sql_update_9d
    commit(curr_int)
    curr_int.execute(sql_update_9e)
    print sql_update_9e
    commit(curr_int)
    curr_int.execute(sql_update_9f)
    print sql_update_9f
    commit(curr_int)
    curr_int.execute(sql_update_9g)
    print sql_update_9g
    commit(curr_int)
    curr_int.execute(sql_update_10)
    print sql_update_10
    commit(curr_int)
    print sql_update_11 #Added this on Feb10-2026 by Sunil to remove zero values in Dev Capex and Opex Values from Sourced_expenditure table
    commit(curr_int)

    print 'Updating Overlap Data ...'
    update_overlap_data(curr_int)

def server_data_import(current_day, external=False, assets=False, equity=False, production=False, reserves=False, expenditure=False, debug=False):
    conn_int = get_connection('int')
    curr_int = conn_int.cursor()
    if assets:
        update_tables(curr_int, external, 'assets', current=current_day)
    if equity:
        update_tables(curr_int, external, 'equity', current=current_day)
    if production:
        update_tables(curr_int, external, 'production', regions=None, current=current_day)
    if reserves:
        update_tables(curr_int, external, 'reserves', current=current_day)
    if expenditure:
        curr_int.execute('TRUNCATE TABLE sourced_expend')
        commit(curr_int)
        curr_int.execute('TRUNCATE TABLE currency_exchange')
        commit(curr_int)
        curr_int.execute('TRUNCATE TABLE projects_extract')
        commit(curr_int)
        curr_int.execute('TRUNCATE TABLE capex_start')
        commit(curr_int)
        update_tables(curr_int, external, 'sourced_expend', current=current_day)
        update_tables(curr_int, external, 'currency_exchange', current=current_day)
        update_tables(curr_int, external, 'projects_extract', current=current_day)
        update_projects_extract(curr_int, debug=debug)
        update_sourced_expend(curr_int, debug=debug)
        print 'Sourced Expenditure Update Complete'
    curr_int.close()
    conn_int.close()

    
if __name__=='__main__':
    server_data_import(current_day=True, assets=True, external=True)


