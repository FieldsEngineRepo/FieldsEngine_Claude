import globaldata as gd
from win32com.client import Dispatch
import data_export as de
import shutil
import openpyxl
import os
import csv
import xlwings as xw


def get_econ_col_str(table, database='globaldata', quoted=False, no_id=False):
    col_names = gd.get_columns(table_name=table, database=database, no_id=no_id)
    if quoted:
        param_str = ','.join(["'{}'".format(col) for col in col_names])
    else:
        param_str = ','.join(["`{}`".format(col) for col in col_names])
    return param_str

def export_data(cursor, run_id):
    sql_export       = """SELECT {} UNION ALL SELECT {} FROM {} WHERE {} INTO OUTFILE '{}' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'"""
    quoted_param_str = get_econ_col_str(table='economic_limit', database='globaldata', quoted=True, no_id=True)
    param_str        = get_econ_col_str(table='economic_limit', database='globaldata', quoted=False, no_id=True)
    sql_where        = 'NOT econ_limit_code=0 AND run_id="{}"'.format(run_id)
    outfile          = gd.REPORTS_DIR+'Economic Limit Report {}.csv'.format(run_id)
    cursor.execute(sql_export.format(quoted_param_str, param_str, 'economic_limit', sql_where, outfile))

def create_econ_limit_list(run_id):
    econ_limit_ids = gd.get_data(param='asset_id', table='economic_limit', sql_where='econ_limit_code=1 AND run_id="{}"'.format(run_id), datatype='int')
    with open(gd.TEST_DIR + 'EL_1.csv', 'w') as csvfile:
        fieldnames = ['ASSET_ID', 'COUNTRY', 'CONSTITUENT', 'REGION', 'STATUS', 'TERRAIN', 'RESOURCE', 'FACILITY', 'BASIN', 'OPERATOR']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        for asid in econ_limit_ids:
            writer.writerow({'ASSET_ID': asid})
    shutil.copy2(gd.TEST_DIR + 'EL_1.csv', gd.MODEL_TASK_DIR+'EL_1.csv')

def rerun_econ_limit_models():
    gd.move_files(gd.ECN_LMT_EN_DIR, gd.ECN_LMT_PR_DIR)
    os.system('%py2% %engine_drive%:\\python_code\\cmd_main.py create_model -eclm-')

def extract_npv_data(curr, update_current, update_original, run_id):
    sql_update_orig = 'UPDATE economic_limit SET orig_remaining_NPV={} WHERE asset_id={} AND run_id="{}"'
    sql_update_curr = 'UPDATE economic_limit SET curr_remaining_NPV={} WHERE asset_id={} AND run_id="{}"'

    xlApp = xw.App(visible=False)
    xlApp.display_alerts = False

    if update_original:
        for asset_model in os.listdir(gd.ECN_LMT_EN_DIR):
            xlWb = xlApp.books.open(gd.ECN_LMT_EN_DIR + asset_model)
            asset_inputs = xlWb.sheets['Asset Inputs']
            xlApp.calculate()
            asset_id = asset_inputs['B1'].value
            npv_rem  = asset_inputs['J4'].value
            print asset_id, npv_rem
            curr.execute(sql_update_orig.format(npv_rem, asset_id, run_id))
            gd.commit(curr)
            xlWb.close()

    if update_current:
        economic_limit_ids = gd.get_data(param='asset_id', table='economic_limit', sql_where='econ_limit_code=1 AND run_id="{}"'.format(run_id), datatype='int')
        for region in os.listdir(gd.BE_REGIONS):
            region_dir = gd.BE_REGIONS + '{}\\'.format(region)
            for asset_model in [filename for filename in os.listdir(region_dir) if filename[-4:] == 'xlsx']:
                asset_id = int(asset_model.split('_')[1])
                if asset_id in economic_limit_ids:
                    xlWb = xlApp.books.open(region_dir + asset_model)
                    asset_inputs = xlWb.sheets['Asset Inputs']
                    xlApp.calculate()
                    npv_rem = asset_inputs['J4'].value
                    print asset_id, npv_rem
                    curr.execute(sql_update_curr.format(npv_rem, asset_id, run_id))
                    gd.commit(curr)
                    xlWb.close()
    xlApp.quit()
    del xlApp

def generate_econ_limit_report(curr, run_id):
    econ_limit_cols = gd.get_columns('economic_limit', no_id=True)
    col_str = ', '.join(econ_limit_cols)
    econ_limit_data = gd.get_data(col_str, 'economic_limit', sql_where='NOT econ_limit_code=0 AND run_id="{}" ORDER BY econ_limit_code, region, country, asset_id'.format(run_id), datatype='plural')
    econ_lmt_rpt_temp = gd.TEMPLATE_DIR + 'Economic Limit Report Template.xlsx'
    report_wb = openpyxl.load_workbook(econ_lmt_rpt_temp)
    data_ws = report_wb['Data']
    datarow_count = len(econ_limit_data)
    for i in range(datarow_count):
        print 'Writing datarow {}/{} ...'.format(i+1, datarow_count)
        row  = i + 2
        datarow = econ_limit_data[i]
        for j in range(len(datarow)):
            col = gd.XL_COLS[j]
            cell = '{}{}'.format(col, row)
            data_ws[cell].value = datarow[j]
    report_wb.save(gd.REPORTS_DIR + 'Economic Limit Report {}.xlsx'.format(run_id))
    report_wb.close()


def econ_limit_main(run_id='', create_list=False, rerun_models=False, extract_data=False, update_current=False, update_original=False, gen_report=False):
    conn = gd.get_connection()
    curr = conn.cursor()
    if not run_id:
        run_id = gd.get_run_id()
    if create_list:
        create_econ_limit_list(run_id)
    if rerun_models:
        rerun_econ_limit_models()
    if extract_data:
        extract_npv_data(curr, update_current, update_original, run_id)
    if gen_report:
        generate_econ_limit_report(curr, run_id)
    curr.close()
    conn.close()

if __name__=='__main__':
    run_id = gd.get_run_id()
    econ_limit_main(run_id=run_id, create_list=True, rerun_models=True, extract_data=True, update_current=True, update_original=True, gen_report=True)
