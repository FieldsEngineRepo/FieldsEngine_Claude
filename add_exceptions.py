from globaldata import *
import xlwings as xw
'''
SELECT asset_id, 
       IFNULL(asset_name,""),
       IFNULL(country,""),
       IFNULL(constituent,""),
       IFNULL(region,""),
       IFNULL(status,""),
       IFNULL(commodity,""), 
       IFNULL(facility_type,""),
       period,
       production,
       IFNULL(unit,""),
       IFNULL(comment,""),
       IFNULL(session_key,""),
       IFNULL(errortype,"") 
FROM error_log 
WHERE (comment LIKE "MODELLED%" OR comment LIKE "NOT MODELLED%") AND session_key="Jason_20180716_124346_87371"

'''

def import_exceptions(exception_data_sheet='error_exception_list.xlsx'):
    xlApp = xw.App(visible=False)
    xlApp.display_alerts = False
    conn = get_connection()
    curr = conn.cursor()
    wb = xlApp.books.open(DATA_DIR + exception_data_sheet)
    data_sheet = wb.sheets['Data']

    sql_insert = 'INSERT INTO error_log_exception (asset_id, comment, errorType) VALUES ({}, "{}", "{}")'

    data_cols = {
        'asset_id'  : 'A',
        'commodity' : 'B',
        'period'    : 'C',
        'error_type': 'D'
    }
    error_comments = {
        'ERROR TYPE 12': 'MODELLED - DATA REVIEW - NO SOURCED PRODUCTION FOR ASSET ID {} IN YEAR {} FOR COMMODITY {}',
        'ERROR TYPE 21': 'MODELLED - DATA REVIEW - HISTORICAL PRODUCTION IS HARDCODED FOR ASSET ID {} IN YEAR {} FOR COMMODITY {}'
    }

    row_num = 2
    while data_sheet.range('A{}'.format(row_num)).raw_value:
        asset_id   = int(data_sheet.range('{}{}'.format(data_cols['asset_id'],row_num)).raw_value)
        commodity  = data_sheet.range('{}{}'.format(data_cols['commodity'], row_num)).raw_value
        period     = int(data_sheet.range('{}{}'.format(data_cols['period'], row_num)).raw_value)
        error_type = data_sheet.range('{}{}'.format(data_cols['error_type'], row_num)).raw_value
        comment = error_comments[error_type].format(asset_id, period, commodity)
        print sql_insert.format(asset_id, comment, error_type)
        curr.execute(sql_insert.format(asset_id, comment, error_type))
        commit(curr)
        row_num += 1

    wb.close()
    curr.close()
    conn.close()
    xlApp.quit()
    del xlApp

def rerun_error_report():
    run_id = get_run_id()
    # Rename original error report
    os.rename('{}Global Run Error Log {}.xlsx'.format(REPORTS_DIR, run_id), '{}Global Run Error Log {}_1.xlsx'.format(REPORTS_DIR, run_id))

    # Rerun error report with exceptions added
    os.system(RPT_TASK_DIR + 'ErrorLogReportMacro.bat')

    # Rename new error report to allow original to retain name
    os.rename('{}Global Run Error Log {}.xlsx'.format(REPORTS_DIR, run_id), '{}Global Run Error Log {}_2.xlsx'.format(REPORTS_DIR, run_id))

    # Save copy of original error report to offical error report filename
    shutil.copy2('{}Global Run Error Log {}_1.xlsx'.format(REPORTS_DIR, run_id), '{}Global Run Error Log {}.xlsx'.format(REPORTS_DIR, run_id))

def main():
    import_exceptions(exception_data_sheet='error_exception_list.xlsx')
    rerun_error_report()

if __name__ == '__main__':
    main()