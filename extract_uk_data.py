from globaldata import *
import xlwings as xw

def extract_data(sub_folder):
    start_time = get_datetime()
    xlApp = xw.App(visible=False)
    xlApp.display_alerts = False
    conn = get_connection()
    curr = conn.cursor()
    run_id = get_run_id(curr)

    for asset_model in [model for model in os.listdir(DATA_DIR + sub_folder) if model[:8] in ['MODELLED','DETAILED'] and not ('~$' + model) in os.listdir(DATA_DIR + sub_folder)]:
        wb = xlApp.books.open(DATA_DIR + sub_folder + asset_model)
        asset_inputs  = wb.sheets['Asset Inputs']
        calculations  = wb.sheets['Calculations']

        asset_id   = int(asset_inputs.range('B1').value)
        start_year = int(asset_inputs.range('B8').value)
        end_year   = start_year + 111
        prod_years = range(start_year, end_year)
        print 'asset_id:', asset_id

        sql_select = 'SELECT asset_id, asset_name, country, constituent, region, terrain, `status`, resource_type, data_source FROM assets WHERE asset_id={}'.format(asset_id)
        curr.execute(sql_select)
        param_vals = curr.fetchone()

        case_types = ['base']
        case_start_row = {'base': 8}

        MODEL_DATA = {
            'total_met_payable'    : {  'ws': calculations,
                                       'col': 'DZ',
                                      'case': {case_type: {year: 0 for year in prod_years} for case_type in case_types}},
            'duty_payable'         : {  'ws': calculations,
                                       'col': 'EM',
                                      'case': {case_type: {year: 0 for year in prod_years} for case_type in case_types}},
            'corporate_tax_payable': {'ws'  : calculations,
                             'col' : 'EM',
                             'case': {case_type: {year: 0 for year in prod_years} for case_type in case_types}},
        }
        extract_params = sorted(MODEL_DATA.keys())
        var_str = ','.join(['%s'] * (len(param_vals) + 4))
        sql_insert = 'INSERT INTO uk_model_data (asset_id,asset_name,country,constituent,region,terrain,`status`,resource_type,data_source,period,taxable_income,abandonment,case_type) VALUES ({})'.format(var_str)
        for case_type in case_types:
            param_row = case_start_row[case_type]
            for period in prod_years:
                row_vals = param_vals[:]
                row_vals += (period,)
                for param in ['taxable_income', 'abandonment']:
                    param_ws   = MODEL_DATA[param]['ws']
                    param_col  = MODEL_DATA[param]['col']
                    param_cell = '{}{}'.format(param_col, param_row)
                    try:
                        MODEL_DATA[param]['case'][case_type][period] = round(float(param_ws.range(param_cell).raw_value), 3)
                        row_vals += (MODEL_DATA[param]['case'][case_type][period],)
                    except:
                        row_vals += (0,)
                row_vals += (case_type,)
                #print sql_insert
                #print row_vals
                curr.execute(sql_insert, row_vals)
                commit(curr)
                param_row += 1
        wb.close()
    curr.close()
    conn.close()
    xlApp.quit()
    del xlApp
    end_time = get_datetime()
    total_time = elapsed_time(start_time, end_time)
    print ''
    print 'Total Time: %s' % total_time
    print ''

def main(sub_folder):
    extract_data(sub_folder)


if __name__=='__main__':
    main(sub_folder = 'completed\\')