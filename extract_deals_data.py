from globaldata import *
import xlwings as xw


def extract_data():
    start_time = get_datetime()
    xlApp = xw.App(visible=False)
    conn = get_connection()
    curr = conn.cursor()
    run_id = get_run_id(curr)

    for asset_model in [model for model in os.listdir(DATA_DIR + 'implied_price_models\\') if model[:8] == 'MODELLED' and not ('~$' + model) in os.listdir(DATA_DIR + 'implied_price_models\\')]:
        sql_update = 'UPDATE deals SET {} WHERE asset_id={} AND deal_id={} AND run_id="{}"'
        wb = xlApp.books.open(r'%s:/GlobalData/Data/implied_price_models/%s' % (PROGRAM_DRIVE, asset_model))
        asset_inputs = wb.sheets['Asset Inputs']
        asset_summary = wb.sheets['Asset Summary']
        asset_id = int(asset_inputs.range('B1').value)
        deal_id = int(asset_model[asset_model.rindex('_')+1:][:-5])
        print 'asset_id:', asset_id
        DEALS_DATA = {
            'npv_remain' : {'ws': asset_summary, 'cell': 'B76', 'val': 0},
            'implied_npv': {'ws': asset_summary, 'cell': 'B77', 'val': 0},
            'implied_oil': {'ws': asset_summary, 'cell': 'B78', 'val': 0},
            'implied_gas': {'ws': asset_summary, 'cell': 'B79', 'val': 0},
            'value_diff' : {'ws': asset_summary, 'cell': 'B80', 'val': 0}
        }
        deal_params = sorted(DEALS_DATA.keys())
        for deal_param in deal_params:
            param_ws   = DEALS_DATA[deal_param]['ws']
            param_cell = DEALS_DATA[deal_param]['cell']
            try:
                DEALS_DATA[deal_param]['val'] = round(float(param_ws.range(param_cell).value), 3)
            except:
                pass
        param_vals = tuple([DEALS_DATA[deal_param]['val'] for deal_param in deal_params])
        param_str = ','.join([deal_param + '=%s' for deal_param in deal_params])
        sql_update = sql_update.format(param_str, asset_id, deal_id, run_id)
        curr.execute(sql_update, param_vals)
        curr.execute('COMMIT')
        wb.close()
    curr.close()
    conn.close()
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