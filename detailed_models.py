from globaldata import *


DET_MOD_DIR = DATA_DIR + 'detailed_models\\detailed_original\\'

def update_detailed_models_table(curr):
    curr.execute('TRUNCATE detailed_models')
    sql_insert = 'INSERT INTO detailed_models (asset_id, model_name) VALUES (%s, "%s")'
    for model_name in [model for model in os.listdir(DET_MOD_DIR) if model[:8] == 'DETAILED']:
        asset_id = int(model_name.split('_')[1])
        curr.execute(sql_insert % (asset_id, model_name))
        curr.execute('COMMIT')
    curr.execute('SELECT DISTINCT asset_id FROM detailed_models ORDER BY asset_id')
    asset_ids = [int(data[0]) for data in curr.fetchall()]
    return asset_ids

def enter_detailed_model_data(curr, asset_list=None):
    sql_insert  = 'INSERT INTO detailed_model_data  '
    sql_insert += '(asset_id,period,water,e_and_a,tangible_capex,intangible_capex,abandonment,other_expend,fixed_opex,variable_opex,payments,receipts,notes) '
    sql_insert += 'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    sql_select = 'SELECT asset_id, model_name FROM detailed_models '
    if asset_list:
        var_str = ', '.join(['%s']*len(asset_list))
        sql_where = 'WHERE asset_id IN (%s) ' % var_str
        sql_where = sql_where % tuple(asset_list)
        sql_select += sql_where
    sql_select += 'ORDER BY asset_id'

    print sql_select
    curr.execute(sql_select)

    cols = 'GMNOPQRSTUV'
    for asset_id, model_name in curr.fetchall():
        print asset_id, 'model name:', model_name
        wb = openpyxl.load_workbook(DET_MOD_DIR + model_name, data_only=True)
        ws = wb.get_sheet_by_name("Asset Inputs")
        period = int(ws['B8'].value)
        print '%s start year: %s' % (asset_id, period)
        for row in range(24,135):
            init_vals = (asset_id, period)
            print asset_id, period, row
            row_vals = ()
            for col in cols:
                data_val = ws[col + str(row)].value
                row_vals += (data_val,)
            row_vals = init_vals + row_vals
            curr.execute(sql_insert, row_vals)
            curr.execute('COMMIT')
            period += 1
        wb.save(DET_MOD_DIR + model_name)

def remove_null_rows(curr, asset_list=None):
    if asset_list:
        asset_ids = asset_list
    else:
        curr.execute('SELECT DISTINCT asset_id FROM detailed_model_data ORDER BY asset_id')
        asset_ids = [data_val[0] for data_val in curr.fetchall()]
    for asset_id in asset_ids:
        print asset_id
        sql_select  = 'SELECT id,e_and_a,tangible_capex,intangible_capex,abandonment,other_expend,fixed_opex,variable_opex,payments,receipts,notes '
        sql_select += 'FROM detailed_model_data WHERE asset_id=%s ORDER BY id'
        curr.execute(sql_select % asset_id)
        row_data = curr.fetchall()
        row_vals = [r[1:] for r in row_data]
        row_ids = [r[0] for r in row_data]
        last_data_row = 0
        for i in range(len(row_ids)):
            row = row_vals[i]
            if row == (None,)*10:
                pass
            else:
                last_data_row = row_ids[i]
        curr.execute('DELETE FROM detailed_model_data WHERE asset_id=%s AND id > %s' % (asset_id, last_data_row))
        curr.execute('COMMIT')

def process_detailed_models(update_tbl=False, asset_list=None, enter_data=False, remove_null=False):
    conn = get_connection()
    curr = conn.cursor()
    asset_ids = []
    if update_tbl:
        asset_ids = update_detailed_models_table(curr)
    if asset_list:
        asset_ids = asset_list
    if enter_data:
        enter_detailed_model_data(curr, asset_list=asset_ids)
    if remove_null:
        remove_null_rows(curr, asset_list=asset_ids)

    curr.close()
    conn.close()


if __name__=='__main__':
    process_detailed_models(update_tbl=True, enter_data=True, remove_null=True)
