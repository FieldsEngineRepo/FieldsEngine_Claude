import globaldata as gd
from openpyxl import *
import win32com
from win32com.client import Dispatch


def convert_nulls(curr, session_keys=[], run_id=''):
    sql_updates = [
        "UPDATE error_log SET commodity='' WHERE commodity IS NULL AND session_key{}",
        "UPDATE error_log SET facility_type='' WHERE facility_type IS NULL AND session_key{}",
        "UPDATE error_log SET period=0 WHERE period IS NULL AND session_key{}",
        "UPDATE error_log SET production=0.0 WHERE production IS NULL AND session_key{}",
        "UPDATE error_log SET unit='' WHERE unit IS NULL AND session_key{}",
        "UPDATE error_log SET data_x=0.0 WHERE data_x IS NULL AND session_key{}",
        "UPDATE error_log SET data_y=0.0 WHERE data_y IS NULL AND session_key{}",
        "UPDATE error_log SET data_z=0.0 WHERE data_z IS NULL AND session_key{}"
    ]
    for sql_update in sql_updates:
        if run_id:
            sql_run_update = sql_update.format(" LIKE '%{}%'".format(run_id))
            print sql_run_update
            curr.execute(sql_run_update)
        elif session_keys:
            for session_key in session_keys:
                sql_session_update = sql_update.format("='{}'".format(session_key))
                print sql_session_update
                curr.execute(sql_session_update)
    gd.commit(curr)


def create_error_file(curr, session_key, log_type='main'):
    print session_key
    sql_statement  = 'SELECT asset_id, asset_name, country, constituent, region, status, commodity, facility_type, period, production, unit, comment, session_key, errortype, data_x, data_y, data_z '

    if log_type == 'full':
        sql_statement += 'FROM error_log WHERE (comment LIKE "MODELLED%" OR comment LIKE "NOT MODELLED%") AND session_key="{}" '.format(session_key)
        logfile_name = "{}error_logs\\ERROR_LOG_{}.xlsx".format(gd.DATA_DIR, session_key)
    else:
        sql_statement += 'FROM error_log WHERE (comment LIKE "MODELLED%" OR comment LIKE "NOT MODELLED%") AND session_key="{}" AND count_error=1'.format(session_key)
        logfile_name = "{}ERROR_LOG_{}.xlsx".format(gd.DATA_DIR, session_key)

    if 0:
        print sql_statement

    if curr.execute(sql_statement):
        error_file = Workbook()
        error_sheet = error_file.active
        error_sheet.title = 'Sheet'
        cols = 'ABCDEFGHIJKLMNOP'

        error_data = curr.fetchall()

        for i in range(len(error_data)):
            row_num = str(i + 1)
            error_sheet['A' + str(row_num)] = error_data[i][0]
            error_sheet['B' + str(row_num)] = error_data[i][1]
            error_sheet['C' + str(row_num)] = error_data[i][2]
            error_sheet['D' + str(row_num)] = error_data[i][3]
            error_sheet['E' + str(row_num)] = error_data[i][4]
            error_sheet['F' + str(row_num)] = error_data[i][5]
            error_sheet['G' + str(row_num)] = error_data[i][13]
            error_sheet['H' + str(row_num)] = error_data[i][7]
            error_sheet['I' + str(row_num)] = error_data[i][8]
            error_sheet['J' + str(row_num)] = error_data[i][9]
            error_sheet['K' + str(row_num)] = error_data[i][10]
            error_sheet['L' + str(row_num)] = error_data[i][11]
            error_sheet['M' + str(row_num)] = error_data[i][12]
            error_sheet['N' + str(row_num)] = error_data[i][14]
            error_sheet['O' + str(row_num)] = error_data[i][15]
            error_sheet['P' + str(row_num)] = error_data[i][16]

        error_file.save(logfile_name)

        del error_sheet
        del error_file

def run_error_report(report_type='main'):
    macro_name = 'Module3.ErrorLogReportMain'
    if report_type != 'main':
        macro_name = 'Module3.ErrorLogReportTotal'
    xlApp = win32com.client.Dispatch("Excel.Application")
    macro_filename = gd.MACRO_DIR+'ReportsMacro.xlsm'
    wb = xlApp.Workbooks.Open(Filename=macro_filename)
    xlApp.Application.Run("ReportsMacro.xlsm!" + macro_name)
    wb.SaveAs(macro_filename)
    xlApp.Application.Quit()
    del xlApp

def main(session_keys=[], run_ids=[], convert=False, reports=False):
    conn = gd.get_connection()
    curr = conn.cursor()

    if convert:
        for run_id in run_ids:
            convert_nulls(curr, session_keys, run_id)

    for session_key in session_keys:
        for log_type in ['main', 'full']:
            create_error_file(curr, session_key, log_type)

    if reports:
        for run_id in run_ids:
            print 'Updating run_id ...'
            curr.execute('UPDATE global_variables SET run_id="{}" WHERE id=1'.format(run_id))
            gd.commit(curr)
            for report_type in ['main', 'full']:
                print 'Running {} error report for {} engine run ...'.format(report_type, run_id)
                run_error_report(report_type)
    curr.close()
    conn.close()

if __name__ == '__main__':
    session_keys = [
        'auto_Titan II_20190109_155630_00712',
        'auto_Titan II_20190109_155630_06315',
        'auto_Titan II_20190109_155630_12377',
        'auto_Titan II_20190109_155630_24584',
        'auto_Titan II_20190109_155630_31718',
        'auto_Titan II_20190109_155630_32178',
        'auto_Titan II_20190109_155630_49521',
        'auto_Titan II_20190109_155630_53593',
        'auto_Titan II_20190109_155630_80077',
        'auto_Titan II_20190109_155630_83266',
        'auto_Titan II_20190109_155630_91652',
        'auto_Titan II_20190109_155630_99582',
        'auto_Titan II_20190116_190310_24313',
        'auto_Titan II_20190116_190310_67178',
        'auto_Titan II_20190116_190310_37621',
        'auto_Titan II_20190116_190310_49757',
        'auto_Titan II_20190116_190310_41144',
        'auto_Titan II_20190116_190310_71824',
        'auto_Titan II_20190116_190310_79358',
        'auto_Titan II_20190116_190310_73929',
        'auto_Titan II_20190116_190310_78496',
        'auto_Titan II_20190116_190310_97781',
        'auto_Titan II_20190116_190310_86559',
        'auto_Titan II_20190116_190310_32641'
    ]
    main(convert=False, session_keys=[], run_ids=['20190116_190310', '20190109_155630'], reports=True)

