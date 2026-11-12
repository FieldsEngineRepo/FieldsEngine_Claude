from globaldata import *
import xlwings as xw


def extract_data(region, BE_REGION_DIR=BE_REGIONS):
    start_time = get_datetime()
    xlApp = xw.App(visible=False)
    conn = get_connection()
    curr = conn.cursor()
    run_id = get_run_id(curr)
    run_id = '%'+run_id+'%'
    asset_models = [model for model in os.listdir(BE_REGION_DIR + region) if model[:8] == 'MODELLED' and not ('~$' + model) in os.listdir(BE_REGION_DIR + region)]
    total_asset_count = len(asset_models)
    asset_num = 1
    for asset_model in asset_models:
        sql_insert = 'INSERT INTO abandonment_data (asset_id, country, prod_year, abandonment) VALUES ({}, "{}", {}, {})'
        wb = xlApp.books.open(r'%s/%s/%s' % (BE_REGION_DIR, region, asset_model))
        wb.app.calculation = 'semiautomatic'
        asset_inputs = wb.sheets['Asset Inputs']
        asset_id = int(asset_inputs.range('B1').value)
        start_year = int(asset_inputs.range('B8').value)
        end_year = start_year + 111
        country = asset_inputs.range('B5').value
        country = country.strip().lower()
        print '%s/%s asset_id: %s' % (asset_num, total_asset_count, asset_id)
        asset_num +=1
        row_num = 24
        for data_year in range(start_year, end_year):
            abandonment = 0.0
            try:
                abandonment = round(float(asset_inputs.range('P{}'.format(row_num)).value), 3)
            except:
                print asset_id, data_year
                pass
            curr.execute(sql_insert.format(asset_id, country, data_year, abandonment))
            commit(curr)
            row_num += 1
        wb.close()
    curr.close()
    conn.close()
    xlApp.quit()
    end_time = get_datetime()
    total_time = elapsed_time(start_time, end_time)
    print ''
    print 'Total Time: %s' % total_time
    print ''

def main(region):
    extract_data(region)


if __name__=='__main__':
    try:
        region = sys.argv[1]
    except:
        region = 'Central America'
    main(region)