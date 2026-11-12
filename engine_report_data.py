from globaldata import *
import xlwings as xw

def create_report_tables(curr, table_data):
    for table_name, data_types in table_data.items():
        col_create = []
        for col_name, data_type in data_types:
            col_create.append(CREATE_COLUMN_TEMPLATE % (col_name, data_type))
        sql_col_create = ',\n'.join(col_create)
        sql_tbl_create = CREATE_TABLE_TEMPLATE % (table_name, sql_col_create)
        print sql_tbl_create
        curr.execute(sql_tbl_create)
        curr.execute('COMMIT')


def clear_report_tables(curr):
    for table in REPORT_TABLE_DATA.keys():
        curr.execute('TRUNCATE TABLE %s' % table)
        curr.execute('COMMIT')


def clear_kpi_quality(curr):
    curr.execute('TRUNCATE TABLE kpi_quality')
    curr.execute('COMMIT')


def get_asset_file_name(run_id):
    month_names = {'01': 'JAN',
                   '02': 'FEB',
                   '03': 'MAR',
                   '04': 'APR',
                   '05': 'MAY',
                   '06': 'JUN',
                   '07': 'JUL',
                   '08': 'AUG',
                   '09': 'SEP',
                   '10': 'OCT',
                   '11': 'NOV',
                   '12': 'DEC'}
    run_date = run_id.split('_')[0]
    run_year = run_date[:4]
    run_month = month_names[run_date[4:6]]
    run_day = run_date[6:8]
    report_name = 'GD_ASSETS_DAILY_'+run_day+run_month+run_year
    return report_name


def convert_assets_file(run_id, xlApp):
    asset_file_name = get_asset_file_name(run_id)
    xlwb = xw.Book()
    xlws = xlwb.sheets[0]
    xlws.name = asset_file_name
    row_num = 1
    with open(REPORTS_DIR + asset_file_name + '.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            row = [unicode(str(data), errors='ignore') for data in row]
            col_count = len(row)
            xlws.range((row_num,1), (row_num,col_count)).raw_value = tuple(row)
            row_num += 1
    print REPORTS_DIR + asset_file_name + '.xlsx'
    xlwb.save(REPORTS_DIR + asset_file_name + '.xlsx')
    xlwb.close()


def data_check(data_cell):
    is_data = False
    try:
        if data_cell is not None and (len(str(data_cell)) > 5 or str(int(data_cell)) == '0'):
            is_data = True
    except:
        pass
    return is_data


def extract_report_data(curr, xlApp, engine_run_id=None):
    """
    Extract data from engine-generated reports to store in database

    Parameters:
        engine_run_id: Run id associated with engine run that generated reports
    """
    # Use run_id from global_variables if engine_run_id is not provided as argument
    if engine_run_id:
        run_id = engine_run_id
    else:
        run_id = get_run_id()

    for data in REPORT_DATA:
        report_file = data['report_file'] % run_id
        worksheet   = data['worksheet']
        row_start   = data['row_start']
        col_data    = data['col_data']
        table_name  = data['table_name']

        # Open report and extract data from worksheet to database
        xlwb = xlApp.books.open(REPORTS_DIR + report_file)
        xlws = xlwb.sheets[worksheet]

        sql_insert = 'INSERT INTO %s (%s) VALUES (%s)'
        col_str = ','.join([data[0] for data in col_data]+['run_id'])
        var_str = ','.join(['%s']*(len(col_data)+1))
        sql_insert = sql_insert % (table_name, col_str, var_str)

        data_found = True
        row_num = row_start
        while data_found:
            if data_check(xlws.range('A'+str(row_num)).raw_value):
                print '%s: %s -- row %s' % (table_name, worksheet, row_num)
                data_cache = ()
                for col_name, data_col in col_data:
                    data_cell = data_col + str(row_num)
                    data_val = xlws.range(data_cell).raw_value
                    if data_val == '-':
                        data_val = 0.0
                    data_cache += (data_val,)
                data_cache += (run_id,)
                curr.execute(sql_insert, data_cache)
                curr.execute('COMMIT')
                row_num += 1
            else:
                data_found = False
        xlwb.save(REPORTS_DIR + report_file)
        xlwb.close()


def update_error_logs(curr):
    curr.execute('UPDATE engine_error_log AS e, assets AS a SET e.terrain=a.terrain WHERE e.asset_id=a.asset_id')
    curr.execute('COMMIT')


def extract_asset_data(curr, run_id, xlApp):
    convert_assets_file(run_id, xlApp)
    report_name = get_asset_file_name(run_id)
    report_file = report_name +'.xlsx'
    worksheet = report_name
    row_start = 2
    col_data = {('asset_id','A'), ('country', 'C'), ('constituent', 'D'), ('region', 'E'), ('terrain', 'G'), ('status', 'F'), ('asset_relation', 'AC'), ('data_source', 'AN')}
    table_name = 'eligible_assets'

    # Open report and extract data from worksheet to database
    xlwb = xlApp.books.open(REPORTS_DIR + report_file)
    xlws = xlwb.sheets[worksheet]

    sql_insert = 'INSERT INTO %s (%s) VALUES (%s)'
    col_str = ','.join([data[0] for data in col_data] + ['run_id'])
    var_str = ','.join(['%s'] * (len(col_data) + 1))
    sql_insert = sql_insert % (table_name, col_str, var_str)

    data_found = True
    row_num = row_start
    while data_found:
        if len(str(xlws.range('A' + str(row_num)).raw_value)) > 5 or str(xlws.range('A' + str(row_num)).raw_value) == '0':
            print '%s: %s -- row %s' % (table_name, worksheet, row_num)
            data_cache = ()
            for col_name, data_col in col_data:
                data_cell = data_col + str(row_num)
                data_val = xlws.range(data_cell).raw_value
                if data_val == '-':
                    data_val = 0.0
                data_cache += (data_val,)
            data_cache += (run_id,)
            curr.execute(sql_insert, data_cache)
            curr.execute('COMMIT')
            row_num += 1
        else:
            data_found = False
    xlwb.save(REPORTS_DIR + report_file)
    xlwb.close()
    sql_delete = "DELETE FROM eligible_assets WHERE (NOT status IN ('Announced', 'Planned', 'Producing') "
    sql_delete += "OR NOT asset_relation='Parent' OR NOT data_source='Engine') "
    curr.execute(sql_delete)
    curr.execute('COMMIT')


def update_deals_data(curr):
    curr.execute("TRUNCATE implied_price_outliers")
    curr.execute("COMMIT")
    sql_insert  = 'INSERT INTO implied_price_outliers (asset_id, asset_name, country, region, status, implied_oil_outlier, implied_gas_outlier, value_diff_outlier, run_id) '
    sql_insert += '(SELECT parent_id, parent_asset_name, parent_country, parent_region, parent_status, implied_oil_outliers, implied_gas_outliers, value_diff_outliers, run_id FROM deals '
    sql_insert += 'WHERE (implied_oil_outliers + implied_gas_outliers + value_diff_outliers) > 0)'
    curr.execute(sql_insert)
    curr.execute("COMMIT")
    sql_update = 'UPDATE implied_price_outliers AS i, assets AS a SET i.constituent=a.constituent, i.terrain=a.terrain WHERE i.asset_id=a.asset_id'
    curr.execute(sql_update)
    curr.execute("COMMIT")


def update_domain_data(curr):
    curr.execute('SELECT DISTINCT domain FROM analyst_domains ORDER BY domain')
    domains = [data[0] for data in curr.fetchall()]
    for domain in domains:
        country, constituent, terrain = domain.split('::')
        for report_table in REPORT_TABLE_DATA.keys():
            sql_update = 'UPDATE %s SET domain="%s" WHERE country="%s" '
            param_vals = (report_table, domain, country)
            if constituent:
                sql_update += 'AND constituent="%s" '
                param_vals += (constituent,)
            if terrain:
                sql_update += 'AND terrain="%s" '
                param_vals += (terrain,)
            sql_update = sql_update % param_vals
            print sql_update
            curr.execute(sql_update)
            curr.execute('COMMIT')


def enter_report_data(curr, run_id):
    curr.execute('SELECT DISTINCT domain, region, analyst FROM analyst_domains ORDER BY domain')
    for domain, region, analyst in curr.fetchall():
        sql_insert = 'INSERT INTO kpi_quality (domain, region, analyst, run_id) VALUES (%s, %s, %s, %s) '
        curr.execute(sql_insert, (domain, region, analyst, run_id))
        curr.execute('COMMIT')
        for kpi_col in KPI_TOTAL_SQL.keys():
            kpi_update = 'UPDATE kpi_quality SET %s=(%s) WHERE domain="%s" AND run_id="%s" '
            kpi_sql = KPI_TOTAL_SQL[kpi_col]['sql'] % (domain, run_id)
            kpi_update = kpi_update % (kpi_col, kpi_sql, domain, run_id)
            curr.execute(kpi_update)
            curr.execute('COMMIT')


def enter_category_scores(curr, run_id):
    for kpi_col in KPI_SCORE_SQL.keys():
        kpi_sql = KPI_SCORE_SQL[kpi_col]['sql'] % run_id
        print kpi_sql
        curr.execute(kpi_sql)
        curr.execute('COMMIT')


def add_assumption_counts(curr, xlws, run_date, date_str):
    analyst_str = "('Adrian Lara', 'Anna Belova', 'Gregory Bosunga', 'Jonathan Markham', 'Andrew Folse', 'Nicole Zhou', 'Svetlana Doh', 'David Bautista', 'Cao Chai', 'Stephen Ho', 'Daniel Rogers')"
    curr.execute('COMMIT')
    sql_select = '''
    SELECT analyst_add.analyst,
           (IFNULL(model_add_count,0) + IFNULL(capex_add_count,0) + IFNULL(redev_add_count,0) + IFNULL(abandonment_add_count,0)) AS add_count,
           (IFNULL(model_edit_count,0) + IFNULL(capex_edit_count,0) + IFNULL(redev_edit_count,0) + IFNULL(abandonment_edit_count,0)) AS edit_count
    FROM
        (SELECT e.edit_by AS analyst,
                IF(e.edit_by IN (SELECT DISTINCT edit_by FROM model_rules WHERE edit_date LIKE "%s"),
                  (SELECT COUNT(edit_by) FROM model_rules WHERE edit_date LIKE "%s" AND edit_by=e.edit_by AND NOT edit_date=add_date GROUP BY edit_by), 0) AS model_edit_count,
                IF(e.edit_by IN (SELECT DISTINCT edit_by FROM capex_alloc WHERE edit_date LIKE "%s"),
                  (SELECT COUNT(edit_by) FROM capex_alloc WHERE edit_date LIKE "%s" AND edit_by=e.edit_by AND NOT edit_date=add_date GROUP BY edit_by), 0) AS capex_edit_count,
                IF(e.edit_by IN (SELECT DISTINCT edit_by FROM capex_redev_alloc WHERE edit_date LIKE "%s"),
                  (SELECT COUNT(edit_by) FROM capex_redev_alloc WHERE edit_date LIKE "%s" AND edit_by=e.edit_by AND NOT edit_date=add_date GROUP BY edit_by), 0) AS redev_edit_count,
                IF(e.edit_by IN (SELECT DISTINCT edit_by FROM abandonment_alloc WHERE edit_date LIKE "%s"),
                  (SELECT COUNT(edit_by) FROM abandonment_alloc WHERE edit_date LIKE "%s" AND edit_by=e.edit_by AND NOT edit_date=add_date GROUP BY edit_by), 0) AS abandonment_edit_count
        FROM model_rules AS e WHERE e.edit_by IN %s GROUP BY e.edit_by) AS analyst_edit,
        (SELECT d.add_by AS analyst,
                IF(d.add_by IN (SELECT DISTINCT add_by FROM model_rules WHERE add_date LIKE "%s"),
                  (SELECT COUNT(add_by) FROM model_rules WHERE add_date LIKE "%s" AND add_by=d.add_by GROUP BY add_by), 0) AS model_add_count,
                IF(d.add_by IN (SELECT DISTINCT add_by FROM capex_alloc WHERE add_date LIKE "%s"),
                  (SELECT COUNT(add_by) FROM capex_alloc WHERE add_date LIKE "%s" AND add_by=d.add_by GROUP BY add_by), 0) AS capex_add_count,
                IF(d.add_by IN (SELECT DISTINCT add_by FROM capex_redev_alloc WHERE add_date LIKE "%s"),
                  (SELECT COUNT(add_by) FROM capex_redev_alloc WHERE add_date LIKE "%s" AND add_by=d.add_by GROUP BY add_by), 0) AS redev_add_count,
                IF(d.add_by IN (SELECT DISTINCT add_by FROM abandonment_alloc WHERE add_date LIKE "%s"),
                  (SELECT COUNT(add_by) FROM abandonment_alloc WHERE add_date LIKE "%s" AND add_by=d.add_by GROUP BY add_by), 0) AS abandonment_add_count
        FROM model_rules AS d WHERE d.add_by IN %s GROUP BY d.add_by) AS analyst_add
    WHERE analyst_add.analyst=analyst_edit.analyst;
    '''
    params = ((date_str,)*8) + (analyst_str,) + ((date_str,)*8) + (analyst_str,)
    curr.execute(sql_select % params)
    row_num = 5
    column_width = 0
    for analyst, edit_count, add_count in curr.fetchall():
        xlws.range('N' + str(row_num)).raw_value = analyst
        xlws.range('O' + str(row_num)).raw_value = add_count
        xlws.range('P' + str(row_num)).raw_value = edit_count
        row_num += 1
    return xlws


def generate_kpi_report(curr, run_id, report_period, xlApp):
    full_month_names = {'01': 'January',
                        '02': 'February',
                        '03': 'March',
                        '04': 'April',
                        '05': 'May',
                        '06': 'June',
                        '07': 'July',
                        '08': 'August',
                        '09': 'September',
                        '10': 'October',
                        '11': 'November',
                        '12': 'December'}
    run_date = run_id[:8]
    report_year = report_period[:4]
    report_month = report_period[4:]
    date_str = '%s-%s%%' % (report_year, report_month)
    
    xlwb = xlApp.books.open(DATA_DIR + 'analyst_kpi\\Upstream Analyst KPI Template.xlsx')
    xlws = xlwb.sheets['Engine Score']
    xlws = add_assumption_counts(curr, xlws, run_date, date_str)
    
    sql_select = 'SELECT domain, region, analyst, eligible_assets, modelled_assets, complexity_score, data_quality_score, econ_quality_score, '
    sql_select += 'dev_be_score, rem_be_score, implied_price_outliers, value_diff_outliers FROM kpi_quality WHERE run_id="%s"'
    curr.execute(sql_select % run_id)
    
    cols = 'ABCDEFGHIJKL'
    row_num = 5
    for datarow in curr.fetchall():
        assert(len(datarow) == len(cols))
        for i in range(len(datarow)):
            if datarow[i]:
                xlws.range(cols[i]+str(row_num)).raw_value = datarow[i]
            else:
                if datarow[3] == 0:
                    if i > 4:
                        xlws.range(cols[i] + str(row_num)).raw_value = ''
                    else:
                        xlws.range(cols[i] + str(row_num)).raw_value = 0.0
                else:
                    if i == 5:
                        xlws.range(cols[i] + str(row_num)).raw_value = 0.0
                    elif i in [10,11]:
                        xlws.range(cols[i] + str(row_num)).raw_value = 0
                    else:
                        xlws.range(cols[i] + str(row_num)).raw_value = 1.0
        row_num += 1
    xlws.range('F3').raw_value = '%s/%s/%s' % (run_date[4:6], run_date[6:], run_date[:4])
    xlws.range('M3').raw_value = '%s %s' % (full_month_names[report_month], report_year)
    xlwb.save(REPORTS_DIR + 'Upstream Analyst KPI %s.xlsx' % run_id)
    xlwb.close()


def main(run_id, create_tbls=False, clear_tbls=False, extract_data=False, update_tbls=False, enter_score_data=False, generate_kpi=False, report_period=None):
    conn = get_connection()
    curr = conn.cursor()

    xlApp = xw.App(visible=False)
    xlApp.display_alerts = False

    if create_tbls:
        create_report_tables(curr, REPORT_TABLE_DATA)
        create_report_tables(curr, QUALITY_TABLE_DATA)

    if clear_tbls:
        clear_report_tables(curr)
        clear_kpi_quality(curr)

    if extract_data:
        extract_report_data(curr, xlApp=xlApp, engine_run_id=run_id)
        extract_asset_data(curr, run_id, xlApp)

    if update_tbls:
        update_deals_data(curr)
        update_error_logs(curr)
        update_domain_data(curr)

    if enter_score_data:
        enter_report_data(curr, run_id)
        enter_category_scores(curr, run_id)

    if generate_kpi:
        generate_kpi_report(curr, run_id, report_period, xlApp)


    curr.close()
    conn.close()
    xlApp.quit()
    del xlApp


if __name__=='__main__':
    main(run_id='20181128_161551', clear_tbls=True, extract_data=True, update_tbls=True, enter_score_data=True, generate_kpi=True, report_period='201811')


