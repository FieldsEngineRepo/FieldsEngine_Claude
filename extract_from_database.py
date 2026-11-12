from globaldata import *
BE_FILE = DATA_DIR + 'be_20180513.xlsx'

def update_disc_field_values():
    out_conn = get_connection(server='sql_server', database='OGEngineDataExtract')
    out_curr = out_conn.cursor()
    in_conn = get_connection()
    in_curr = in_conn.cursor()

    wb = openpyxl.load_workbook(BE_FILE)
    ws = wb.get_sheet_by_name('data')
    for row_num in range(1, 7968):
        asset_id    = int(ws['A' + str(row_num)].value)
        be_fc_oil   = str(ws['B' + str(row_num)].value)
        be_fc_gas   = str(ws['C' + str(row_num)].value)
        be_rem_oil  = str(ws['D' + str(row_num)].value)
        be_rem_gas  = str(ws['E' + str(row_num)].value)
        sql_update  = "UPDATE Engine.tblEngineDataPoints SET [Full-cycle break-even oil price ($/bbl)]='{}', [Full-cycle break-even gas price ($/mcf)]='{}', "
        sql_update += "[Remaining break-even oil price ($/bbl)]='{}', [Remaining break-even gas price ($/mcf)]='{}' WHERE AssetID={} AND [CaseType]='Base Case'"
        out_curr.execute(sql_update.format(be_fc_oil, be_fc_gas, be_rem_oil, be_rem_gas, asset_id))
        out_curr.execute('COMMIT')
    wb.save(BE_FILE)

    sql_select = 'SELECT asset_id, min_econ_res_oil, max_dev_cost FROM asset_data WHERE asset_id IN (SELECT DISTINCT asset_id FROM field_analogues)'
    in_curr.execute(sql_select)
    disc_field_data = in_curr.fetchall()
    sql_update = "UPDATE Engine.tblEngineDataPoints SET MinimumEconomicFieldsSize='{}', MaximumEconomicDeveopmentCost='{}' WHERE AssetID={} AND [CaseType]='Base Case'"
    for asset_id, min_econ, max_dev in disc_field_data:
        out_curr.execute(sql_update.format(min_econ, max_dev, asset_id))
        out_curr.execute('COMMIT')

    out_curr.close()
    out_conn.close()
    in_curr.close()
    in_conn.close()

update_disc_field_values()
