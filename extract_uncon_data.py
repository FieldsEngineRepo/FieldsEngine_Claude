from globaldata import *
import xlwings as xw

MODEL_DIR = DATA_DIR + 'unconventional_new\\'
EXCEL_LIB = 'xlwings'

def extract_data():
    start_time = get_datetime()
    if EXCEL_LIB == 'xlwings':
        xlApp = xw.App(visible=False)
    conn = get_connection()
    curr = conn.cursor()

    for asset_model in [model for model in os.listdir(MODEL_DIR) if model[:8] == 'MODELLED' and not ('~$' + model) in os.listdir(MODEL_DIR)]:
        sql_insert     = 'INSERT INTO uncon_data_extract (asset_id, period, hist_wells_total, hist_capex_per_well, hist_capex_total) VALUES ({}, {}, {})'

        if EXCEL_LIB == 'xlwings':
            wb             = xlApp.books.open(MODEL_DIR + ('%s' % asset_model))
            wb.app.calculation = 'semiautomatic'
            asset_inputs   = wb.sheets['Asset Inputs']
            well_cash_flow = wb.sheets['Well Cash Flow']
            asset_id       = int(asset_inputs.range('B1').value)
            discount_year  = int(asset_inputs.range('E10').value)
        elif EXCEL_LIB == 'openpyxl':
            wb = openpyxl.load_workbook(MODEL_DIR + ('%s' % asset_model), data_only=True)
            asset_inputs   = wb.get_sheet_by_name('Asset Inputs')
            well_cash_flow = wb.get_sheet_by_name('Well Cash Flow')
            asset_id       = int(asset_inputs['B1'].value)
            discount_year  = int(asset_inputs['E10'].value)

        print 'asset_id:', asset_id
        UNCON_DATA = {
            'hist_wells_total'    : {'ws': well_cash_flow, 'col': 'Q', 'val': 0},
            'hist_capex_per_well' : {'ws': well_cash_flow, 'col': 'R', 'val': 0},
            'hist_capex_total'    : {'ws': well_cash_flow, 'col': 'S', 'val': 0}
        }
        row_num = 9
        if EXCEL_LIB == 'xlwings':
            period = int(well_cash_flow.range('P' + str(row_num)).raw_value)
        elif EXCEL_LIB == 'openpyxl':
            period = int(well_cash_flow['P' + str(row_num)].value)
        while period < discount_year:
            uncon_params = sorted(UNCON_DATA.keys())
            for uncon_param in uncon_params:
                param_ws   = UNCON_DATA[uncon_param]['ws']
                param_cell  = UNCON_DATA[uncon_param]['col'] + str(row_num)
                try:
                    if EXCEL_LIB == 'xlwings':
                        UNCON_DATA[uncon_param]['val'] = round(float(param_ws.range(param_cell).raw_value), 3)
                        print UNCON_DATA[uncon_param]['val']
                    elif EXCEL_LIB == 'openpyxl':
                        UNCON_DATA[uncon_param]['val'] = round(float(param_ws[param_cell].value), 3)
                except:
                    pass
            param_vals = tuple([UNCON_DATA[uncon_param]['val'] for uncon_param in uncon_params])
            param_str = ','.join(uncon_params)
            sql_insert = sql_insert.format(period, asset_id, param_str)
            print sql_insert % param_vals
            curr.execute(sql_insert, param_vals)
            commit(curr)
            row_num += 1
            if EXCEL_LIB == 'xlwings':
                period = int(well_cash_flow.range('P' + str(row_num)).value)
            elif EXCEL_LIB == 'openpyxl':
                period = int(well_cash_flow['P' + str(row_num)].value)
        if EXCEL_LIB == 'xlwings':
            wb.close()
        elif EXCEL_LIB == 'openpyxl':
            wb.save(MODEL_DIR + ('%s' % asset_model))
    curr.close()
    conn.close()
    if EXCEL_LIB == 'xlwings':
        xlApp.quit()
    end_time = get_datetime()
    total_time = elapsed_time(start_time, end_time)
    print ''
    print 'Total Time: %s' % total_time
    print ''

def main():
    extract_data()


if __name__=='__main__':
    main()