from analogue_score_calc import analogue_score_calc
from globaldata import *

params = ['asset_id','asset_name','country','constituent','region','status','operator','terrain','basin','ablock','formation','form_rock_type','trap_type','facility_type','asset_relation',
          'pipeline','data_source','gas_processing','oil_storage','gas_storage','peak_commodity','resource_type','in_place_reserves','api_gravity','total_init_prod','init_crude','init_ng',
          'init_condensate','init_lng','init_ngl','peak_prod_boed','total_peak_prod','peak_crude','peak_ng','peak_condensate','peak_lng','peak_ngl','capex_per_boe','opex_per_boe','fixed_opex',
          'variable_opex_per_mmcf','variable_opex_per_b','abandonment','capex_tangible_pct','capex_redev','opex_capacity_factor','opex_capacity_target','capex_capacity_factor','peak_year',
          'capex_capacity_target','last_error_count','model_status','param_track_key','first_production','hsulfer','sulfer','calorific','carbon_dixoide']


assets = ['asset_id','asset_name','country','constituent','region','status','terrain','basin','ablock','formation','form_rock_type','trap_type','facility_type','discovery_date','hsulfer','sulfer','calorific','carbon_dioxide','resource_type','api_gravity', 'asset_relation', 'data_source']
operators = ['operator','asset_id']
infrastructure = ['pipeline','gas_processing','oil_storage','gas_storage','asset_id']
param_track = ['peak_commodity','peak_prod','capex_per_boe','fixed_opex','variable_opex_per_mmcf','variable_opex_per_b','abandonment','capex_tangible_pct','capex_redev','peak_year','first_production','asset_id']
production = ['total_init_prod','init_crude','init_ng','init_condensate','init_lng','init_ngl','total_peak_prod','peak_crude','peak_ng','peak_condensate','peak_lng','peak_ngl','asset_id']
error_log = ['last_error_count','asset_id']
in_place_reserves = ['in_place_reserves','asset_id']
get_param_fn = ['opex_capacity_factor','opex_capacity_target','capex_capacity_factor','capex_capacity_target']

prod_phases = {'init': 'first_production',
               'peak': 'peak_year'}

commodities = {'crude': 'Crude Oil',
               'ng': 'Natural Gas',
               'lng': 'LNG',
               'ngl': 'NGL',
               'condensate': 'Condensate'}

comm_groups = {'Crude Oil': 'Crude Oil',
               'NGL': 'Crude Oil',
               'Condensate': 'Crude Oil',
               'Natural Gas': 'Natural Gas',
               'LNG': 'Natural Gas'}

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def process_data(data_row):
    return_val = ()
    for data in data_row:
        if isinstance(data, str):
            data = data.encode('utf-8').strip()
        return_val += (data,)
    return return_val


def clear_asset_data_tbl(curr):
    print 'Clearing asset_data table ...'
    truncate_table(table='asset_data')
    # sql_update = 'Alter table asset_data drop column CO2_factor'


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_param_str(param_list, debug=False):
    param_str = ', '.join(param_list)
    if debug:
        print 'parameter string:', param_str
    return param_str


def get_tbl_data(curr, param_str, table_name, sql_where=None, debug=False):
    sql_query = 'SELECT %s FROM %s '
    params = (param_str, table_name)
    if sql_where:
        sql_query += 'WHERE %s'
        params += (sql_where,)
    sql_query = sql_query % params
    if debug:
        print 'get_tbl_data() sql_query:', sql_query
    curr.execute(sql_query)
    tbl_data = curr.fetchall()
    return tbl_data

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_disc_date(curr):
    curr.execute('ALTER TABLE asset_data ADD COLUMN dummy VARCHAR(50)')
    curr.execute('UPDATE asset_data SET dummy=discovery_date WHERE NOT discovery_date IS NULL')
    curr.execute('UPDATE asset_data SET discovery_date=NULL WHERE dummy="NULL" AND id > 0')
    curr.execute('ALTER TABLE asset_data DROP COLUMN dummy')
    curr.execute('COMMIT')


def update_field_age(curr):
    field_age = 0
    discount_year = get_discount_year(curr)
    discovery_year = discount_year
    curr.execute('SELECT DISTINCT asset_id FROM asset_data WHERE NOT discovery_date IS NULL')
    disc_asset_ids = [int(data[0]) for data in curr.fetchall()]
    for asset_id in disc_asset_ids:
        curr.execute('SELECT discovery_date FROM asset_data WHERE asset_id=%s' % asset_id)
        discovery_date = str(curr.fetchone()[0])
        if '/' in discovery_date:
            discovery_year = [int(date_component) for date_component in discovery_date.split('/') if len(date_component) == 4][0]
        elif '-' in discovery_date:
            discovery_year = [int(date_component) for date_component in discovery_date.split('-') if len(date_component) == 4][0]
        field_age = discount_year - discovery_year
        curr.execute('UPDATE asset_data SET field_age=%s WHERE asset_id=%s' % (field_age, asset_id))
    curr.execute('COMMIT')


def update_asset_data_assets(curr, debug=False):
    print 'Entering data from assets table ...'
    param_str = get_param_str(assets, debug)
    sql_insert = 'INSERT INTO asset_data (%s) SELECT %s FROM assets' % (param_str, param_str)
    curr.execute(sql_insert)
    curr.execute('COMMIT')
    update_disc_date(curr)
    update_field_age(curr)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_operators(curr):
    print 'Updating operators table ...'
    curr.execute('TRUNCATE operators')
    sql_update  = 'INSERT INTO operators (asset_id, operator) SELECT eq_max.ast_id, eq.operator FROM equity AS eq, '
    sql_update += '(SELECT asset_id as ast_id, MAX(equity_date) AS max_date FROM equity GROUP BY asset_id) AS eq_max '
    sql_update += 'WHERE eq.asset_id = eq_max.ast_id AND eq.equity_date = eq_max.max_date GROUP BY eq_max.ast_id;'
    print sql_update
    try:
        curr.execute(sql_update)
    except:
        restart_server()
        curr.execute(sql_update)
    curr.execute('COMMIT')


def update_asset_data_operators(curr, update=False, debug=False):
    if update:
        update_operators(curr)
    print 'Entering data from operators table ...'
    curr.execute('SET sql_safe_updates=0')
    curr.execute('COMMIT')
    sql_update = 'UPDATE asset_data, operators SET asset_data.operator=operators.operator WHERE asset_data.asset_id=operators.asset_id'
    curr.execute(sql_update)
    curr.execute('COMMIT')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def import_nearest_infra(curr, file_date):
    print 'Importing infrastructure data from file ...'
    file_name = 'discovered_fields\\nearest_infra_%s.xlsx' % file_date
    file_path = DATA_DIR + file_name
    wb = openpyxl.load_workbook(file_path)
    try:
        ws = wb['nearest_infra']
    except:
        ws = wb.get_sheet_by_name('nearest_infra')
    max_row = ws.max_row
    table_ids = []
    row_count = 0
    for row_num in range(2, max_row + 1):
        asset_id   = ws['A' + str(row_num)].value
        infra_type = ws['B' + str(row_num)].value
        distance   = ws['C' + str(row_num)].value
        infra_type = '_'.join(infra_type.lower().split())
        if asset_id in table_ids:
            sql_update = 'UPDATE infrastructure SET %s=%s WHERE asset_id=%s'
            sql_update = sql_update % (infra_type, distance, asset_id)
            curr.execute(sql_update)
        else:
            sql_insert = 'INSERT INTO infrastructure (asset_id, %s) VALUES (%s, %s)'
            sql_insert = sql_insert % (infra_type, asset_id, distance)
            curr.execute(sql_insert)
            table_ids.append(asset_id)
        curr.execute('COMMIT')
        row_count += 1
        if row_count % 10000 == 0:
            print str(round((float(row_count)/float(max_row))*100,2)) + '% processed'
    wb.save(file_path)


def update_asset_data_infrastructure(curr, import_date=None, debug=False):
    if import_date:
        import_nearest_infra(curr, import_date)
    print 'Entering data from infrastructure table ...'
    curr.execute('SET sql_safe_updates=0')
    curr.execute('COMMIT')
    curr.execute('SELECT * FROM infrastructure')
    param_str = get_param_str(infrastructure, debug)
    format_str = get_param_str(['asset_data.'+param+'=infrastructure.'+param for param in infrastructure[:-1]], debug)
    sql_update = 'UPDATE asset_data, infrastructure SET %s WHERE asset_data.asset_id=infrastructure.asset_id' % format_str
    if debug:
        print sql_update
    curr.execute(sql_update)
    curr.execute('COMMIT')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def enter_param_track_key(curr):
    print 'Entering param_track_key ...'
    curr.execute('SET sql_safe_updates=0')
    # sql_update = \
    # """
    # UPDATE asset_data AS ad,
    # (SELECT pt_max.asset_id, pt.session_key FROM param_track AS pt,
    # (SELECT asset_id, session_key, MAX(id) AS max_id FROM param_track GROUP BY asset_id) AS pt_max
    # WHERE pt.id = pt_max.max_id GROUP BY pt_max.asset_id) AS param_keys
    # SET ad.param_track_key=param_keys.session_key WHERE ad.asset_id = param_keys.asset_id;
    # """
    sql_update = '''UPDATE asset_data AS ad, 
(SELECT pt_max.asset_id, ANY_VALUE(pt.session_key) AS session_key FROM param_track AS pt, 
(SELECT asset_id, MAX(id) AS max_id FROM param_track GROUP BY asset_id) AS pt_max
WHERE pt.id = pt_max.max_id GROUP BY pt_max.asset_id) AS param_keys
SET ad.param_track_key=param_keys.session_key WHERE ad.asset_id = param_keys.asset_id;
'''
    curr.execute(sql_update)
    curr.execute('COMMIT')

def enter_param_track_data(curr, debug=False):
    sql_update = 'UPDATE asset_data AS a, param_track AS b SET a.total_capex=b.total_capex_real, a.last_production=b.cutoff_year WHERE a.asset_id=b.asset_id AND a.param_track_key=b.session_key'
    if debug: print sql_update
    curr.execute(sql_update)
    commit(curr)

def update_asset_data_param_track(curr, debug=False):
    enter_param_track_key(curr)
    enter_param_track_data(curr, debug=debug)
    print 'Entering data from param_track table ...'
    param_str = get_param_str(['ad.'+param+'=pt.'+param for param in param_track[:-1]], debug)
    sql_update = 'UPDATE asset_data as ad, param_track as pt SET %s WHERE ad.asset_id=pt.asset_id AND ad.param_track_key=pt.session_key' % param_str
    curr.execute(sql_update)
    curr.execute('COMMIT')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def enter_error_log_key(curr):
    print 'Entering error_log_key ...'
    curr.execute('SELECT DISTINCT asset_id FROM error_log WHERE NOT session_key LIKE "analogue%"')
    asset_ids = [data[0] for data in curr.fetchall()]
    for asset_id in asset_ids:
        sql_select = 'SELECT MAX(SUBSTRING(session_key,IF(SUBSTRING(session_key,-5,1)="_", -20, -21), 15)) FROM error_log WHERE asset_id=%s' % asset_id
        curr.execute(sql_select)
        run_id = curr.fetchone()[0]
        sql_update = 'UPDATE asset_data SET error_log_key="%s" WHERE asset_id=%s' % (run_id, asset_id)
        curr.execute(sql_update)
        curr.execute('COMMIT')


def update_asset_data_error_log(curr, debug=False):
    enter_error_log_key(curr)
    print 'Entering last_error_count ...'
    curr.execute('SET sql_safe_updates=0')
    curr.execute('COMMIT')
    curr.execute('SELECT asset_id, error_log_key FROM asset_data WHERE NOT error_log_key IS NULL ORDER BY asset_id')
    for asset_id, error_key in curr.fetchall():
        if debug: print asset_id
        sql_update = \
        """
        UPDATE asset_data SET last_error_count=(SELECT COUNT(*) AS errors FROM error_log
        WHERE errortype IN ('ERROR TYPE 02', 'ERROR TYPE 03', 'ERROR TYPE 13', 'ERROR TYPE 18')
        AND session_key LIKE '%%%s%%' AND asset_id=%s) WHERE asset_id=%s
        """
        sql_update = sql_update % (error_key, asset_id, asset_id)
        try:
            curr.execute(sql_update)
        except:
            restart_server()
            curr.execute(sql_update)
    curr.execute('COMMIT')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_in_place_reserves_tbl(curr):
    print 'Creating in_place_reserves table ...'
    curr.execute('DROP TABLE in_place_reserves')
    sql_create = \
    """
    CREATE TABLE in_place_reserves (
        id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        asset_id int(11) DEFAULT NULL,
        commodity varchar(50) DEFAULT NULL,
        reserve_year int(11) DEFAULT NULL,
        reserve_type varchar(50) DEFAULT NULL,
        reserve_volume double DEFAULT NULL,
        unit varchar(50) DEFAULT NULL,
        boe_reserves double DEFAULT NULL,
        reserve_pct double DEFAULT NULL,
        boe_total double DEFAULT NULL
    )
    """
    curr.execute(sql_create)
    curr.execute('COMMIT')


def update_commodity_in_place_reserves(curr):
    print 'Updating in_place_reserves table for each commodity...'
    commodities = ['Crude Oil', 'Condensate', 'NGL', 'Natural Gas']
    for commodity in commodities:
        sql_insert = \
        """
        INSERT INTO in_place_reserves (asset_id, commodity, reserve_year, reserve_type, reserve_volume, unit)
          SELECT RM.asset_id, R.commodity, YEAR(R.reserve_pub_date), R.reserve_type, R.reserve_volume, R.unit 
            FROM reserves AS R,
                 (SELECT asset_id, MAX(reserve_pub_date) AS max_date FROM reserves
                  WHERE reserve_type IN ('Oil in place', 'Gas in place', 'Prospective')
                  AND commodity='{0}' AND casetype='Base Case'
                  AND reserve_volume > 0
                  GROUP BY asset_id) AS RM
            WHERE RM.asset_id=R.asset_id AND R.reserve_pub_date=RM.max_date
            AND R.commodity='{0}' AND R.reserve_type IN ('Oil in place', 'Gas in place', 'Prospective')
        """
        try:
            curr.execute(sql_insert.format(commodity))
        except:
            restart_server()
            curr.execute(sql_insert.format(commodity))
    curr.execute('COMMIT')


def calculate_in_place_reserve_totals(curr):
    print 'Calculating reserve totals ...'
    sql_update = 'UPDATE in_place_reserves AS r, unit_equals AS u SET r.boe_reserves=(r.reserve_volume*u.factor) WHERE r.unit=u.unit AND r.commodity=u.commodity AND u.base_unit IN ("Barrels", "Boe") '
    curr.execute(sql_update)
    sql_update  = 'UPDATE in_place_reserves AS r, (SELECT SUM(boe_reserves) AS boe_total, asset_id FROM in_place_reserves WHERE reserve_type IN ("Oil in Place", "Gas in Place") GROUP BY asset_id) AS s '
    sql_update += 'SET r.boe_total=s.boe_total WHERE r.asset_id=s.asset_id AND r.reserve_type IN ("Oil in Place", "Gas in Place")'
    print sql_update
    curr.execute(sql_update)
    sql_update  = 'UPDATE in_place_reserves AS r, (SELECT SUM(boe_reserves) AS boe_total, asset_id FROM in_place_reserves WHERE reserve_type="Prospective" GROUP BY asset_id) AS s '
    sql_update += 'SET r.boe_total=s.boe_total WHERE r.asset_id=s.asset_id AND r.reserve_type="Prospective"'
    print sql_update
    curr.execute(sql_update)
    curr.execute('COMMIT')


def update_in_place_reserves_tbl(curr):
    print 'Updating in_place_reserves table ...'
    create_in_place_reserves_tbl(curr)
    #_ = raw_input('continue?')
    update_commodity_in_place_reserves(curr)
    #_ = raw_input('continue?')
    calculate_in_place_reserve_totals(curr)
    #_ = raw_input('continue?')
# ['Prospective', 'Oil in place', 'Gas in place']
#  ['Contingent', '3p', '2p', '1p']



def update_asset_data_in_place_reserves(curr, debug=False):
    update_in_place_reserves_tbl(curr)
    print 'Entering data from in_place_reserves table ...'
    for reserve_type in ['Prospective', 'Oil in place', 'Gas in place']:
        sql_update = 'UPDATE asset_data AS ad, in_place_reserves AS r SET ad.in_place_volume=r.boe_total, ad.in_place_vol_type="{0}" WHERE ad.asset_id=r.asset_id AND r.reserve_type="{0}" '.format(reserve_type)
        if debug: print sql_update
        curr.execute(sql_update)
        curr.execute('COMMIT')
        #_ = raw_input('continue?')
    sql_update = 'Alter table asset_data add column CO2_factor float'
    curr.execute(sql_update) #Added this to creat column CO2 factor in asset_data table which is missing . ( on 12-18-2024 )
    curr.execute('COMMIT')
    sql_update1 = \
    """
    UPDATE asset_data SET CO2_factor = (1 - (IF(carbon_dioxide='NULL',0,carbon_dioxide)/100.0)) WHERE in_place_vol_type='Gas in Place';
    """
    curr.execute(sql_update1)
    commit(curr)
    #_ = raw_input('continue?')
    sql_update2 = \
    """
    UPDATE asset_data SET in_place_volume=(CO2_factor*in_place_volume) WHERE in_place_vol_type='Gas in Place';
    """
    curr.execute(sql_update2)
    commit(curr)
    #_ = raw_input('continue?')
    #sql_update = 'UPDATE asset_data AS ad, in_place_reserves AS r SET ad.in_place_volume=r.boe_total, ad.in_place_vol_type=r.reserve_type WHERE ad.asset_id=r.asset_id'
    #print sql_update
    #curr.execute(sql_update)
    #curr.execute('COMMIT')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_reserve_volumes_tbl(curr, debug=False):
    print 'Creating reserve_volumes table ...'
    curr.execute('DROP TABLE reserve_volumes')
    sql_create = \
    """
    CREATE TABLE reserve_volumes (
        id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        asset_id int(11) DEFAULT NULL,
        commodity varchar(50) DEFAULT NULL,
        volume_type varchar(25) DEFAULT NULL,
        reserve_type varchar(50) DEFAULT NULL,
        reserve_year int(11) DEFAULT NULL,
        reserve_volume double DEFAULT NULL,
        unit varchar(50) DEFAULT NULL,
        boe_reserves double DEFAULT NULL,
        reserve_pct double DEFAULT NULL,
        boe_total double DEFAULT NULL
    )
    """
    curr.execute(sql_create)
    curr.execute('COMMIT')


def update_commodity_reserves(curr, debug=False):
    print 'Updating commodity reserves ...'
    commodities = ['Crude Oil', 'Condensate', 'NGL', 'Natural Gas', 'Crude Oil & Natural Gas']
    for commodity in commodities:
        sql_insert = \
        """
        INSERT INTO reserve_volumes (asset_id, commodity, volume_type, reserve_type, reserve_year, reserve_volume, unit)
          SELECT RM.asset_id, R.commodity, 'recov', R.reserve_type, YEAR(R.reserve_pub_date), R.reserve_volume, R.unit
            FROM reserves AS R,
               (SELECT asset_id, reserve_type, MAX(reserve_pub_date) AS max_date FROM reserves
                  WHERE reserve_type IN ('1p', '2p', '3p', 'Contingent')
                  AND reserve_volume > 0 GROUP BY asset_id, reserve_type) AS RM
            WHERE RM.asset_id = R.asset_id AND R.reserve_pub_date=RM.max_date AND R.reserve_type=RM.reserve_type
              AND R.commodity = %s AND R.reserve_type IN ('1p', '2p', '3p', 'Contingent');
        """
        try:
            if debug: print sql_insert % commodity
            curr.execute(sql_insert, (commodity,))
        except:
            restart_server()
            if debug: print sql_insert % commodity
            curr.execute(sql_insert, (commodity,))
    curr.execute('COMMIT')
   
   
def calculate_reserve_pcts(curr, debug=False):
    sql_update_a = "UPDATE asset_data SET reserve_type=in_place_vol_type, reserve_volume=in_place_volume WHERE IFNULL(in_place_volume,0) > 0 AND IFNULL(recov_volume,0) = 0"
    sql_update_b = "UPDATE asset_data SET reserve_type=recov_vol_type, reserve_volume=recov_volume WHERE IFNULL(recov_volume,0) > 0"
    sql_update_c = "UPDATE asset_data SET reserve_volume=NULL WHERE reserve_type='Prospective'"
    curr.execute(sql_update_a)
    commit(curr)
    ##_ = raw_input('continue?')
    curr.execute(sql_update_b)
    commit(curr)
    #_ = raw_input('continue?')
    curr.execute(sql_update_c)
    commit(curr)
    
    for reserves_table, sql_where in [('reserve_volumes', 'IFNULL(a.recov_volume,0) > 0'), ('in_place_reserves', 'IFNULL(a.in_place_volume,0) > 0 AND IFNULL(a.recov_volume,0) = 0')]:
        sql_update_1 = \
            '''
            UPDATE {0} AS a,
                   (SELECT DISTINCT asset_id, reserve_type, SUM(boe_reserves) AS type_reserves FROM {0} GROUP BY asset_id, reserve_type) AS b
              SET a.reserve_pct=ROUND(a.boe_reserves/b.type_reserves,4)
              WHERE a.asset_id=b.asset_id
                AND a.reserve_type=b.reserve_type;
            '''
        print sql_update_1.format(reserves_table)
        curr.execute(sql_update_1.format(reserves_table))
        commit(curr)
        #_ = raw_input('continue?')
        sql_update_2 = \
            '''
            UPDATE asset_data SET crude_reserve_pct=0, ng_reserve_pct=0, condensate_reserve_pct=0, ngl_reserve_pct=0, lng_reserve_pct=0 WHERE {};
            '''
        print sql_update_2.format(sql_where.replace('a.',''))
        curr.execute(sql_update_2.format(sql_where.replace('a.','')))
        commit(curr)
        #_ = raw_input('continue?')
        sql_update_3 = \
            '''
            UPDATE asset_data AS a, {} AS b SET a.crude_reserve_pct=(b.reserve_pct+a.crude_reserve_pct) WHERE a.asset_id=b.asset_id AND b.commodity='Crude Oil' AND a.reserve_type=b.reserve_type AND {};
            '''
        curr.execute(sql_update_3.format(reserves_table, sql_where))
        commit(curr)
        #_ = raw_input('continue?')
        sql_update_4 = \
            '''
            UPDATE asset_data AS a, {} AS b SET a.ng_reserve_pct=(b.reserve_pct+a.ng_reserve_pct) WHERE a.asset_id=b.asset_id AND b.commodity='Natural Gas' AND a.reserve_type=b.reserve_type AND {};
            '''
        curr.execute(sql_update_4.format(reserves_table, sql_where))
        commit(curr)
        #_ = raw_input('continue?')
        sql_update_5 = \
            '''
            UPDATE asset_data AS a, {} AS b SET a.condensate_reserve_pct=(b.reserve_pct+a.condensate_reserve_pct) WHERE a.asset_id=b.asset_id AND b.commodity='Condensate' AND a.reserve_type=b.reserve_type AND {};
            '''
        curr.execute(sql_update_5.format(reserves_table, sql_where))
        commit(curr)
        #_ = raw_input('continue?')
        sql_update_6 = \
            '''
            UPDATE asset_data AS a, {} AS b SET a.ngl_reserve_pct=(b.reserve_pct+a.ngl_reserve_pct) WHERE a.asset_id=b.asset_id AND b.commodity='NGL' AND a.reserve_type=b.reserve_type AND {};
            '''
        curr.execute(sql_update_6.format(reserves_table, sql_where))
        commit(curr)
        #_ = raw_input('continue?')
        sql_update_7 = \
            '''
            UPDATE asset_data AS a, {} AS b SET a.lng_reserve_pct=(b.reserve_pct+a.lng_reserve_pct) WHERE a.asset_id=b.asset_id AND b.commodity='LNG' AND a.reserve_type=b.reserve_type AND {};
            '''
        curr.execute(sql_update_7.format(reserves_table, sql_where))
        commit(curr)
        #_=raw_input('continue?')
        sql_update_8 = \
            '''
            UPDATE asset_data AS a, {} AS b SET a.crude_reserve_pct=(a.crude_reserve_pct+(b.reserve_pct/2)), a.ng_reserve_pct=(a.ng_reserve_pct+(b.reserve_pct/2))
              WHERE a.asset_id=b.asset_id AND b.commodity='Crude Oil & Natural Gas' AND a.reserve_type=b.reserve_type AND {};
            '''
        curr.execute(sql_update_8.format(reserves_table, sql_where))
        commit(curr)
        '''

        '''

def calculate_reserve_totals(curr, debug=False):
    print 'Calculating reserve totals ...'
    sql_update = 'UPDATE reserve_volumes AS r, unit_equals AS u SET r.boe_reserves=(r.reserve_volume*u.factor) WHERE r.unit=u.unit AND u.base_unit IN ("Barrels", "Boe")'
    curr.execute(sql_update)
    #_ = raw_input('continue?')
    sql_update  = 'UPDATE reserve_volumes AS r, (SELECT SUM(boe_reserves) AS boe_total, asset_id, reserve_type FROM reserve_volumes GROUP BY asset_id, reserve_type) AS s '
    sql_update += 'SET r.boe_total=s.boe_total WHERE r.asset_id=s.asset_id AND r.reserve_type=s.reserve_type'
    if debug: print sql_update
    curr.execute(sql_update)
    curr.execute('COMMIT')
    #_ = raw_input('continue?')


def update_reserve_volumes_tbl(curr, debug=False):
    print 'Updating reserve_volumes table ...'
    create_reserve_volumes_tbl(curr, debug)
    update_commodity_reserves(curr, debug)
    calculate_reserve_totals(curr, debug)


def update_asset_data_reserve_volumes(curr, debug=False):
    update_reserve_volumes_tbl(curr, debug)
    print 'Entering data from reserve_volumes table ...'
    for reserve_type in ['Contingent', '3p', '2p', '1p']:
        #sql_update = 'UPDATE asset_data AS ad, reserve_volumes AS r SET ad.recov_volume=r.boe_reserves, ad.recov_vol_type="{0}" WHERE ad.asset_id=r.asset_id AND r.reserve_type="{0}" '.format(reserve_type)
        sql_update = \
            """
            UPDATE asset_data AS ad,
               (SELECT DISTINCT asset_id, reserve_type, SUM(boe_reserves) AS total_boe_reserves FROM reserve_volumes GROUP BY asset_id, reserve_type) AS r
               SET ad.recov_volume=r.total_boe_reserves, ad.recov_vol_type='{0}' WHERE ad.asset_id=r.asset_id AND r.reserve_type='{0}'
            """.format(reserve_type)
        if debug: print sql_update
        curr.execute(sql_update)
        curr.execute('COMMIT')
        #_ = raw_input('continue?')
    calculate_reserve_pcts(curr, debug)
    #_ = raw_input('continue?')
    #for reserve_type in ['Prospective', 'Oil in place', 'Gas in place']:
    #    sql_update = 'UPDATE asset_data AS ad, in_place_reserves AS r SET ad.in_place_volume=r.boe_total, ad.in_place_vol_type="{0}" WHERE ad.asset_id=r.asset_id AND r.reserve_type="{0}" '.format(reserve_type)
    #    if debug: print sql_update
    #    curr.execute(sql_update)
    #    curr.execute('COMMIT')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_last_econ_data_key(curr):
    sql_select = 'SELECT MAX(SUBSTRING(session_key, -21, 15)) FROM econ_data'
    curr.execute(sql_select)
    last_econ_data_key = curr.fetchone()[0]
    return last_econ_data_key


def update_asset_data_recov_reserves(curr):
    print 'Entering recoverable reserves from econ_data table ...'
    sql_update  = 'UPDATE asset_data AS a, econ_data AS e SET a.recov_reserves=e.total_boe '
    sql_update += 'WHERE e.total_boe > 0 AND e.session_key LIKE CONCAT("%",(SELECT run_id FROM global_variables WHERE id=1),"%") '
    # sql_update += 'WHERE e.total_boe > 0 AND e.session_key LIKE "%20241209_230549%" '
    sql_update += 'AND a.asset_id = e.asset_id'
    print sql_update
    curr.execute(sql_update)
    curr.execute('COMMIT')


def update_asset_data_recov_factor(curr):
    print 'Entering recovery factor values for assets with in_place_reserves ...'
    sql_update = 'UPDATE asset_data SET recov_factor=ROUND(recov_reserves/in_place_volume, 5) WHERE NOT recov_reserves IS NULL AND in_place_volume > 0 '
    curr.execute(sql_update)
    curr.execute('COMMIT')


def update_asset_data_reserves(curr, debug=False):
    update_asset_data_in_place_reserves(curr, debug=debug)
    update_asset_data_reserve_volumes(curr, debug=debug)
    update_asset_data_recov_reserves(curr)
    update_asset_data_recov_factor(curr)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def convert_to_boe(curr, prod_value, commodity, unit, debug=False):
    boe_value = float(prod_value)
    if unit.lower() not in ['boe', 'barrels']:
        if debug:
            print '{} - {} - {}'.format(commodity, prod_value, unit)
        if commodity.strip().lower() == 'ngl':
            comm_name = 'ngls'
        else:
            comm_name = commodity.strip().lower()
        sql_where = "commodity='{}' AND unit='{}' AND base_unit='Boe'".format(comm_name, unit.strip())
        conv_factor = get_data('factor', 'unit_equals', server='mysql', database='globaldata', cursor=curr, single_value=True, datatype='float', sql_where=sql_where, debug=debug)
        boe_value = float(prod_value) * float(conv_factor)
    return boe_value

def update_boe_production(curr, debug=False):
    PROD_COLS = {
        'crude oil'  : 'oil_prod',
        'natural gas': 'gas_prod',
        'condensate' : 'cond_prod',
        'ngl'        : 'ngls_prod',
        'lng'        : 'lng_prod'
    }

    run_id = get_run_id()
    sql_insert = \
    """
    INSERT INTO boe_prod_data (asset_id, prod_year)
      (SELECT DISTINCT asset_id, period FROM production WHERE data_source='Engine' AND sources != 'EST: Forecast Engine' AND casetype='Base Case' AND production > 0 ORDER BY asset_id, period)
    """
    curr.execute(sql_insert)
    commit(curr)

    sql_update1 = "UPDATE boe_prod_data SET run_id='{}' WHERE run_id IS NULL".format(run_id)
    curr.execute(sql_update1)
    commit(curr)

    sql_update2 = "UPDATE boe_prod_data SET {}={} WHERE asset_id={} AND prod_year={} AND run_id='{}'"

    sql_where = "data_source='Engine' AND sources != 'EST: Forecast Engine' AND casetype='Base Case' AND production > 0 ORDER BY asset_id, commodity, period"
    prod_data = get_data('DISTINCT asset_id, period, commodity, production, unit', 'production', cursor=curr, datatype='plural', sql_where=sql_where)
    prod_data_count = len(prod_data)
    prod_data_num = 1
    for asset_id, prod_year, commodity, prod_value, prod_unit in prod_data:
        print '{}/{}: {} - {} - {}'.format(prod_data_num, prod_data_count, asset_id, prod_year, commodity)
        prod_col = PROD_COLS[commodity.lower()]
        boe_prod = convert_to_boe(curr, prod_value, commodity, prod_unit, debug=debug)
        curr.execute(sql_update2.format(prod_col, boe_prod, asset_id, prod_year, run_id))
        commit(curr)
        prod_data_num += 1


def update_asset_data_production(curr, debug=False):
    run_id = get_run_id()
    PROD_DATA_COLS = {
        'oil' : 'crude',
        'gas' : 'ng',
        'cond': 'condensate',
        'ngls': 'ngl',
        'lng' : 'lng'
    }

    curr.execute('DELETE FROM boe_prod_data WHERE run_id="{}"'.format(run_id))
    commit(curr)

    print 'Updating boe production ...'
    update_boe_production(curr=curr, debug=debug)

    sql_update_init_year = \
    """
    UPDATE asset_data AS a, (SELECT DISTINCT asset_id, MIN(prod_year) AS init_{0}_year FROM boe_prod_data WHERE {1}_prod > 0 AND run_id='{2}' GROUP BY asset_id) AS b 
      SET a.init_{0}_year=b.init_{0}_year WHERE a.asset_id=b.asset_id
    """

    sql_update_peak_prod = \
    """
    UPDATE asset_data AS a, (SELECT DISTINCT asset_id, MAX({1}_prod) AS peak_{0} FROM boe_prod_data WHERE {1}_prod > 0 AND run_id='{2}' GROUP BY asset_id) AS b 
      SET a.peak_{0}=b.peak_{0} WHERE a.asset_id=b.asset_id
    """

    sql_update_init_prod = \
    """
    UPDATE asset_data AS a, (SELECT DISTINCT asset_id, prod_year, {1}_prod FROM boe_prod_data WHERE {1}_prod > 0 AND run_id='{2}') AS b 
      SET a.init_{0}=b.{1}_prod WHERE a.asset_id=b.asset_id AND a.init_{0}_year=b.prod_year
    """

    sql_update_peak_year = \
    """
    UPDATE asset_data AS a, (SELECT DISTINCT asset_id, {1}_prod, MIN(prod_year) AS peak_year FROM boe_prod_data WHERE {1}_prod > 0 AND run_id='{2}' GROUP BY asset_id, {1}_prod) AS b 
      SET a.peak_{0}_year=b.peak_year WHERE a.asset_id=b.asset_id AND a.peak_{0}=b.{1}_prod
    """

    for comm_col in PROD_DATA_COLS.keys():
        data_col = PROD_DATA_COLS[comm_col]
        print 'Updating init {} years ...'.format(data_col)
        curr.execute(sql_update_init_year.format(data_col, comm_col, run_id))
        commit(curr)

        print 'Updating init {} prod ...'.format(data_col)
        curr.execute(sql_update_init_prod.format(data_col, comm_col, run_id))
        commit(curr)

        print 'Updating peak {} prod ...'.format(data_col)
        curr.execute(sql_update_peak_prod.format(data_col, comm_col, run_id))
        commit(curr)

        print 'Updating peak {} years ...'.format(data_col)
        curr.execute(sql_update_peak_year.format(data_col, comm_col, run_id))
        commit(curr)



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_max_points(score_type, param):
    param_max = 0
    score_dict = eval(score_type.upper()+'_SCORES')
    if param in PERCENTAGE_SCORES:
        if param in ['pipeline', 'gas_processing', 'oil_storage', 'gas_storage']:
            param_max = 75
        else:
            param_max = max(score_dict[param]['points'])
    elif param in OPTION_SCORES:
        param_max = max([score_dict[param][param_option]['points'] for param_option in score_dict[param].keys()])
    else:
        param_max = score_dict[param]['points']
    return param_max

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_max_scores(curr, debug=False):
    analogue_score_calc()
    for score_type in ['prod', 'cost']:
        print 'Entering max %s scores from analogue_scores table ...' % score_type
        sql_update = 'UPDATE asset_data AS d, analogue_scores AS s SET d.max_%s_score = s.max_score WHERE s.score_type = "%s" AND d.asset_id=s.asset_id' % (score_type, score_type)
        curr.execute(sql_update)
    curr.execute('COMMIT')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_asset_data_tbl(option_list=[], update_oprtrs=False, infra_fdate=None, debug=False):
    conn = start_database()
    curr = conn.cursor()
    if 'all' in option_list: #Added lines from 714- 723 to remove CO2_factor column drop issues in asset_data table while running Discovered Fields on 05-01-2025
        drop_CO2_factor = "Alter table asset_data drop column CO2_factor" #Droping CO2_factor column from asset_data at start of updating it while running discovered fields
        dummy = "Alter table asset_data drop column dummy"
        try:
           curr.execute(drop_CO2_factor)
           curr.execute('COMMIT')
           print("Dropped CO2_factor column from asset_data table.....")
        except :
            print("No CO2_factor column exists in asset_data table...")
            pass
        try:
           curr.execute(dummy)
           curr.execute('COMMIT')
           print("Dropped dummy column from asset_data table.....")
        except :
            print("No dummy column exists in asset_data table...")
            pass
    if 'all' in option_list:
        options = ['clear_tbl','assets','operators','infrastructure','param_track','error_log','reserves','max_scores', 'production']
        # options = ['production']
    else:
        options = option_list

    if 'clear_tbl' in options:
        clear_asset_data_tbl(curr)
    if 'assets' in options:
        update_asset_data_assets(curr, debug=debug)
    if 'operators' in options:
        update_asset_data_operators(curr, update=update_oprtrs, debug=debug)
    if 'infrastructure' in options:
        update_asset_data_infrastructure(curr, import_date=infra_fdate, debug=debug)
    if 'param_track' in options:
        update_asset_data_param_track(curr, debug=debug)
    if 'error_log' in options:
        update_asset_data_error_log(curr, debug=debug)
    if 'reserves' in options:
        update_asset_data_reserves(curr, debug=debug)
    if 'max_scores' in options:
        update_max_scores(curr, debug=debug)
    if 'production' in options:
        update_asset_data_production(curr, debug=debug)
    curr.close()
    conn.close()

    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    option_list = ['param_track']
    update_asset_data_tbl(option_list=option_list, debug=False)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
