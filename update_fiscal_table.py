from globaldata import *

def update_fiscal_table():
    conn = get_connection()
    curr = conn.cursor()

    curr.execute('SELECT fiscalModelDir FROM global_variables WHERE id=1')
    fiscal_dir = curr.fetchone()[0]
    fiscal_models = [fiscal_model for fiscal_model in os.listdir(fiscal_dir) if fiscal_model[-4:] == 'xlsx']

    curr.execute('SELECT DISTINCT file_name FROM fiscal')
    fiscal_file_names = [data[0] for data in curr.fetchall()]
    for fiscal_file_name in fiscal_file_names:
        available = 0
        if fiscal_file_name in fiscal_models:
            available = 1
        sql_update = 'UPDATE fiscal SET available=%s WHERE file_name="%s"' % (available, fiscal_file_name)
        curr.execute(sql_update)
        curr.execute('COMMIT')
    curr.close()
    conn.close()

def update_model_names():
    conn = get_connection()
    curr = conn.cursor()
    sql_update = 'UPDATE fiscal SET file_name="{}" WHERE file_name="{}"'
    fiscal_model_names = get_params('file_name','fiscal')
    for old_fiscal_name in fiscal_model_names:
        new_fiscal_name = old_fiscal_name.replace('[SV]', 'Conventional')
        curr.execute(sql_update.format(new_fiscal_name, old_fiscal_name))
        print '{} --> {}'.format(old_fiscal_name, new_fiscal_name)
        commit(curr)
    curr.close()
    conn.close()

if __name__=='__main__':
    #update_fiscal_table()
    update_model_names()
