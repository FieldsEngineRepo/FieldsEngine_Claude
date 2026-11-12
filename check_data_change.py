from globaldata import *
import pandas as pd

run_id_1 = '20180418_205149'
run_id_2 = '20180424_131345'

def get_changed_assets(run_id_1, run_id_2, dataframe=False):
    sql_select = \
    '''
    SELECT * FROM econ_data 
    WHERE asset_id IN 
    (SELECT c.asset_id FROM (SELECT a.asset_id, 
                                   (a.npv_rem-b.npv_rem) AS npv_rem_diff, 
                                   (a.npv_dev-b.npv_dev) AS npv_dev_diff, 
                                   (a.capex_boe_full-b.capex_boe_full) AS capex_boe_full_diff, 
                                   (a.opex_boe_full-b.opex_boe_full) AS opex_boe_full_diff, 
                                   (a.fiscal_full-b.fiscal_full) AS fiscal_full_diff
                             FROM econ_data AS a, econ_data AS b
                             WHERE a.run_id='{0}' AND b.run_id='{1}'
                             AND b.asset_id IN (SELECT DISTINCT asset_id FROM econ_data WHERE run_id='{0}')
                             AND a.asset_id IN (SELECT DISTINCT asset_id FROM econ_data WHERE run_id='{1}') 
                             ORDER BY a.asset_id) AS c
    WHERE c.npv_rem_diff=0 AND c.npv_dev_diff=0 AND c.capex_boe_full_diff=0 AND c.opex_boe_full_diff=0 AND c.fiscal_full_diff=0)
    AND run_id IN ('{0}', '{1}')
    '''
    sql_select = sql_select.format(run_id_1, run_id_2)

    conn = get_connection()
    if dataframe:
        sql_df = pd.read_sql(sql_select, con=conn)
        print sql_df
    else:
        curr = conn.cursor()
        curr.execute(sql_select)
        econ_data = curr.fetchall()
        curr.close()

    conn.close()

if __name__=='__main__':
    get_changed_assets('20180418_205149', '20180425_201952', dataframe=True)