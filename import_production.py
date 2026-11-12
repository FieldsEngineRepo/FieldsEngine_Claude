from globaldata import *

INPUT_FILE  = DATA_DIR + 'production_20180411.xlsx'

SQL_INSERT  = 'INSERT INTO production (asset_id, asset_name, country, constituent, region, commodity, period, production, unit, casetype, asset_relationship, sources, data_source, add_by, add_date) '
SQL_INSERT += 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "Parent", %s, %s, "Titan II", %s) '

SQL_DELETE  = 'DELETE FROM production WHERE asset_id=%s AND commodity=%s AND period=%s AND casetype=%s '

def import_production_data():
    conn = get_connection()
    curr = conn.cursor()
    wb = openpyxl.load_workbook(INPUT_FILE)
    ws = wb['data']
    add_date = get_add_date()
    row_num = 2
    data_found = True
    print add_date
    while data_found:
        print row_num
        asset_id    = ws['A'+str(row_num)].value
        asset_name  = ws['B'+str(row_num)].value
        country     = ws['C'+str(row_num)].value
        constituent = ws['D'+str(row_num)].value
        region      = ws['E'+str(row_num)].value
        commodity   = ws['F'+str(row_num)].value
        period      = ws['G'+str(row_num)].value
        production  = ws['H'+str(row_num)].value
        unit        = ws['I'+str(row_num)].value
        casetype    = ws['J'+str(row_num)].value
        sources     = ws['K'+str(row_num)].value
        data_source = ws['L'+str(row_num)].value
        if asset_id and asset_name:
            curr.execute(SQL_DELETE, (asset_id, commodity, period, casetype))
            curr.execute('COMMIT')
            curr.execute(SQL_INSERT, (asset_id, asset_name, country, constituent, region, commodity, period, production, unit, casetype, sources, data_source, add_date))
            curr.execute('COMMIT')
        else:
            data_found = False
        row_num += 1
    curr.close()
    conn.close()
    wb.save(INPUT_FILE)

if __name__=='__main__':
    import_production_data()