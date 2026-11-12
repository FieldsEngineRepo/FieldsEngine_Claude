from globaldata import *

def update_model_rules():
    conn = get_connection(database='miningengineextract')
    curr = conn.cursor()
    col_names = ['mineName', 'mineCountry', 'state', 'mineRegion', 'mineStage', 'mineType', 'mineMethod', 'commodity', 'production_units', 'operators', 'param_table', 'param_range']
    sql_update = 'UPDATE mining_model_rules SET %s=NULL WHERE LENGTH(%s) < 1 AND NOT %s IS NULL'
    for col_name in col_names:
        sql_update_str = sql_update % ((col_name,)*3)
        curr.execute(sql_update_str)
        curr.execute('COMMIT')
    col_names = ['NewMineId', 'Mineid', 'production_total', 'production_peak']
    sql_update = 'UPDATE mining_model_rules SET %s=0 WHERE LENGTH(%s) < 1 OR %s IS NULL'
    for col_name in col_names:
        sql_update_str = sql_update % ((col_name,)*3)
        curr.execute(sql_update_str)
        curr.execute('COMMIT')
    curr.close()
    conn.close()

if __name__=='__main__':
    update_model_rules()

