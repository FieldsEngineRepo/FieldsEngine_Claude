from globaldata import *

def import_company_data(curr):
    sql_insert = 'INSERT INTO parent_companies (company_name, parent_company) VALUES (%s, %s) '
    curr.execute('TRUNCATE parent_companies')
    filename = 'E:\\Documents\\parent_companies_20180315.xlsx'
    wb = openpyxl.load_workbook(filename)
    ws = wb['data']
    row_num = 2
    data_found = True
    while data_found:
        print row_num
        company_name   = ws['A'+str(row_num)].value
        parent_company = ws['B'+str(row_num)].value
        if company_name and parent_company:
            curr.execute(sql_insert, (company_name, parent_company))
            curr.execute('COMMIT')
        else:
            data_found = False
        row_num += 1


def update_econ_data(curr):
    curr.execute('SELECT company_name, parent_company FROM parent_companies ORDER BY company_name')
    companies = {data[0].lower(): data[1] for data in curr.fetchall()}
    sql_select = 'SELECT asset_id, operator, session_key FROM econ_data WHERE session_key LIKE "%20180%" AND (NOT operator IS NULL OR LENGTH(operator) > 0) ORDER BY asset_id, session_key'
    curr.execute(sql_select)
    for asset_id, operator, session_key in curr.fetchall():
        sql_update = 'UPDATE econ_data SET parent_company=%s WHERE operator=%s AND asset_id=%s AND session_key=%s'
        company_name = operator.lower()
        if company_name in companies.keys():
            print '%s: %s %s' % (asset_id, operator, session_key)
            parent_company = companies[company_name]
            curr.execute(sql_update, (parent_company, operator, asset_id, session_key))
            curr.execute('COMMIT')





def main():
    conn = get_connection()
    curr = conn.cursor()
    #import_company_data(curr)
    update_econ_data(curr)
    curr.close()
    conn.close()

if __name__=='__main__':
    main()