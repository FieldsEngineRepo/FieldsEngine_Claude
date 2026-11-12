import globaldata as gd
import xlwings as xw
import os

KEY_ASSET_TRACKER_DIR           = gd.DATA_DIR + 'key_asset_tracker\\'
KEY_ASSET_TRACKER_FILENAME      = 'Key Asset Tracker {}.xlsx'
KEY_ASSET_TRACKER_TEMP_FILENAME = 'Key Asset Tracker Template.xlsx'


KEY_ASSET_COLS = {
    'A' : ('asset_id', ''),
    'B' : ('field_name', ''),
    'C' : ('country', ''),
    'D' : ('region', ''),
    'E' : ('project_name', ''),
    'F' : ('project_type', ''),
    'G' : ('field_status', ''),
    'H' : ('project_stage', ''),
    'I' : ('operator', ''),
    'J' : ('reported_last_update', ''),
    'K' : ('reported_is_aligned', ''),
    'L' : ('reported_aligned_date', ''),
    'M' : ('reported_analyst_reviewed', ''),
    'N' : ('reported_reviewed_date', ''),
    'O' : ('reported_is_approved', ''),
    'P' : ('last_engine_run', ''),
    'Q' : ('engine_irr_dev_pct', 'irr_dev'),
    'R' : ('reported_irr_pct', ''),
    'S' : ('engine_capex_boe', 'capex_boe_full'),
    'T' : ('engine_opex_boe', 'opex_boe_full_model'),
    'U' : ('engine_be_oil_dev', 'be_oil_dev'),
    'V' : ('engine_be_oil_rem', 'be_oil_rem'),
    'W' : ('reported_be_oil', ''),
    'X' : ('engine_be_gas_dev', 'be_gas_dev'),
    'Y' : ('engine_be_gas_rem', 'be_gas_rem'),
    'Z' : ('reported_be_gas', ''),
    'AA': ('engine_recov_rem_boe', 'total_recov_rem'),
    'AB': ('engine_recov_tot_boe', 'total_recov'),
    'AC': ('engine_liquids_rem_boe', 'liquid_recov_rem'),
    'AD': ('engine_gas_rem_bcf', 'natgas_recov_rem'),
    'AE': ('engine_ngls_rem_bbl', 'ngls_recov_rem'),
    'AF': ('engine_liquids_tot_boe', 'liquid_recov_tot'),
    'AG': ('engine_gas_tot_bcf', 'natgas_recov_tot'),
    'AH': ('engine_ngls_tot_bbl', 'ngls_recov_tot'),
    'AI': ('reported_recov_tot_boe', ''),
    'AJ': ('reported_liquids_tot_mmbbl', ''),
    'AK': ('reported_gas_tot_bcf', ''),
    'AL': ('reported_reserves_type', ''),
    'AM': ('engine_dev_npv_usd', 'npv_dev'),
    'AN': ('reported_npv_usd_mil', ''),
    'AO': ('engine_full_capex_usd', 'capex_full'),
    'AP': ('reported_full_capex_usd_mil', ''),
    'AQ': ('engine_prod_start_year', 'first_production'),
    'AR': ('reported_prod_start_year', ''),
    'AS': ('reported_facility_type', ''),
    'AT': ('reported_est_avg_peak_prod', ''),
    'AU': ('reported_peak_capacity_unit', ''),
    'AV': ('engine_prod_peak_year', 'peak_year'),
    'AW': ('reported_prod_peak_year', ''),
    'AX': ('reported_number_of_wells', ''),
    'AY': ('reported_update_comments', ''),
    'AZ': ('reported_sources', ''),
    'BA': ('reported_sources_type', ''),
    'BB': ('reported_check_date', ''),
    'BC': ('engine_total_error_count', 'total_error_count'),
    'BD': ('engine_error_type_count', 'error_type_count'),
    'BE': ('engine_run_id', 'run_id'),
    'BF': ('engine_data_source', 'data_source')
}

def archive_data(curr, debug=False):
    curr.execute('TRUNCATE TABLE key_asset_data_archive')
    gd.commit(curr)
    curr.execute('INSERT INTO key_asset_data_archive (SELECT * FROM key_asset_data)')
    gd.commit(curr)
    curr.execute('TRUNCATE TABLE key_asset_data')
    gd.commit(curr)


def extract_reported_data(curr, debug=False):
    xlApp = xw.App(visible=False)
    xlApp.display_alerts = False
    for key_asset_tracker_filename in os.listdir(KEY_ASSET_TRACKER_DIR):
        wb = xlApp.books.open(r'%s/%s' % (KEY_ASSET_TRACKER_DIR, key_asset_tracker_filename))
        wb.app.calculation = 'semiautomatic'
        wb.app.screen_updating = False
        key_asset_sheet = wb.sheets['Key Asset Tracker']
        sql_insert = 'INSERT INTO key_asset_data ({}) VALUES ({})'
        row_num = 5
        while key_asset_sheet.range('A{}'.format(row_num)).raw_value and len(str(key_asset_sheet.range('A{}'.format(row_num)).raw_value)) > 1:
            print row_num, int(key_asset_sheet.range('A{}'.format(row_num)).raw_value)
            data_vals = ()
            data_cols = []
            data_vars = []
            for col_indx in range(len(KEY_ASSET_COLS.keys())):
                col = gd.XL_COLS[col_indx]
                data_cell = '{}{}'.format(col, row_num)
                data_col = KEY_ASSET_COLS[col][0]
                if col_indx < 10 or data_col.startswith('reported'):
                    try:
                        col_data_val = key_asset_sheet.range(data_cell).raw_value
                        if col_data_val is not None:
                            data_vals += ("""{}""".format(col_data_val),)
                        else:
                            data_vals += ('',)
                    except:
                        data_vals += ('',)
                    data_cols.append(data_col)
                    data_vars.append('%s')
            data_col_str = ', '.join(data_cols)
            data_var_str = ', '.join(data_vars)
            try:
                if debug: print sql_insert.format(data_col_str, data_var_str) % data_vals
                curr.execute(sql_insert.format(data_col_str, data_var_str), data_vals)
                gd.commit(curr)
            except:
                if debug: print sql_insert.format(data_col_str, data_var_str) % data_vals
            row_num += 1
        wb.close()
    xlApp.quit()
    del xlApp

def update_add_date(curr, current_date, debug=False):
    curr.execute('UPDATE key_asset_data SET last_engine_run="{}" WHERE last_engine_run IS NULL'.format(current_date))
    gd.commit(curr)


def update_key_asset_data(curr, current_date, debug=False):
    sql_update = \
    '''
    UPDATE key_asset_data AS a, econ_data AS b, (SELECT asset_id AS assetid, MAX(run_id) AS max_run_id FROM econ_data WHERE NOT total_boe IS NULL GROUP BY asset_id) AS c 
    SET {} WHERE a.asset_id=b.asset_id AND b.asset_id=c.assetid AND b.run_id=c.max_run_id'''
    param_updates = []
    param_update_str = ''
    for key_asset_col, econ_data_col  in [col_vals for col_vals in KEY_ASSET_COLS.values() if len(col_vals[1]) > 0]:
        param_updates.append('a.{}=b.{}'.format(key_asset_col, econ_data_col))
    param_update_str = ', '.join(param_updates)
    if debug: print sql_update.format(param_update_str)
    curr.execute(sql_update.format(param_update_str))
    gd.commit(curr)
    update_add_date(curr, current_date)


def update_asset_tracker_file(curr, current_date, debug=False):
    run_id = gd.get_run_id()
    xlApp = xw.App(visible=False)
    xlApp.display_alerts = False

    wb = xlApp.books.open(r'%s/%s' % (gd.TEMPLATE_DIR, KEY_ASSET_TRACKER_TEMP_FILENAME))
    wb.app.screen_updating = False
    wb.save(r'%s/%s' % (gd.REPORTS_DIR, KEY_ASSET_TRACKER_FILENAME.format(run_id)))
    wb.close()

    wb = xlApp.books.open(r'%s/%s' % (gd.REPORTS_DIR, KEY_ASSET_TRACKER_FILENAME.format(run_id)))
    wb.app.calculation = 'semiautomatic'
    key_asset_sheet = wb.sheets['Key Asset Tracker']
    data_col_str = ', '.join([KEY_ASSET_COLS[gd.XL_COLS[col_indx]][0] for col_indx in range(len(KEY_ASSET_COLS.keys()))])
    sql_select = 'SELECT {} FROM key_asset_data WHERE last_engine_run="{}" ORDER BY asset_id, project_name'.format(data_col_str,current_date)
    curr.execute(sql_select)
    key_asset_data = curr.fetchall()
    row_num = 5
    for datarow in key_asset_data:
        print row_num, datarow[0]
        for col_indx in range(len(datarow)):
            col_val = datarow[col_indx]
            col = gd.XL_COLS[col_indx]
            cell = '{}{}'.format(col, row_num)
            if col_val and len(str(col_val)) > 0:
                try:
                    key_asset_sheet.range(cell).raw_value = str(col_val)
                except:
                    key_asset_sheet.range(cell).raw_value = ''
        row_num += 1
    wb.save(r'%s/%s' % (gd.REPORTS_DIR, KEY_ASSET_TRACKER_FILENAME.format(run_id)))
    wb.close()
    xlApp.quit()
    del xlApp


def key_assets_main(archive=False, extract=False, update_table=False, update_file=False, debug=False):
    current_date = gd.get_date()
    conn = gd.get_connection()
    curr = conn.cursor()
    if archive:
        archive_data(curr, debug=debug)
    if extract:
        extract_reported_data(curr, debug=debug)
    if update_table:
        update_key_asset_data(curr, current_date, debug=debug)
    if update_file:
        update_asset_tracker_file(curr, current_date, debug=debug)
    curr.close()
    conn.close()

if __name__ == '__main__':
    key_assets_main(archive=True, extract=True, update_table=True, update_file=True)
