from globaldata import *


def update_abandonment():
    conn = get_connection()
    curr = conn.cursor()
    sql_update = 'UPDATE uk_abandon_data SET equity_date=(SELECT MAX(equity_date) FROM equity WHERE asset_id={0}) WHERE asset_id={0}'
    sql_insert = 'INSERT INTO uk_abandonment_data (asset_id, company, operator, parent_company, equity_pct) (SELECT DISTINCT a.asset_id, a.entity_name, a.operator, a.top_parent_company, a.equity_pct FROM equity AS a, uk_abandon_data AS b WHERE a.asset_id=b.asset_id AND a.equity_date=b.equity_date)'
    asset_ids = get_data('asset_id', 'uk_abandon_data', datatype='int')
    asset_count = len(asset_ids)
    for asset_id in asset_ids:
        print asset_id
        curr.execute(sql_update.format(asset_id))
        commit(curr)
    curr.execute(sql_insert)
    commit(curr)
    curr.close()
    conn.close()



if __name__=='__main__':
    update_abandonment()