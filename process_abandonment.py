from globaldata import *

def update_operator_equity():
    print 'Updating operator equity data ...'
    conn = get_connection()
    curr = conn.cursor()
    asset_data = get_data(param='asset_id, country', table='abandonment_data', datatype='plural')
    sql_select = \
    '''
    SELECT DISTINCT entity_name, operator, top_parent_company, equity_pct FROM equity 
    WHERE asset_id={0} AND 
          equity_date=(SELECT MAX(equity_date) FROM equity WHERE asset_id={0});
    '''
    sql_insert = 'INSERT INTO operator_abandonment (asset_id,country,company,operator,parent_company,equity_pct,`2018`,`2019`,`2020`,`2021`,`2022`,`2023`,`2024`,`2025`) VALUES ({}, "{}", "{}", "{}", "{}", {}, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)'
    sql_update = 'UPDATE operator_abandonment SET `{}`=ROUND({}*(equity_pct/100),2) WHERE asset_id={}'
    asset_count = 1
    asset_total = len(asset_data)
    for asset_id, country in asset_data:
        print '{}/{}: {}'.format(asset_count,asset_total,asset_id)
        total_equity = 0
        curr.execute(sql_select.format(asset_id))
        equity_data = curr.fetchall()
        for company, operator, top_parent, equity_pct in equity_data:
            curr.execute(sql_insert.format(asset_id, country, company, operator, top_parent, equity_pct))
            commit(curr)
        for prod_year in range(2018, 2026):
            abandonment = float(get_param(param='abandonment', table='abandonment_data', sql_where='asset_id={} AND prod_year={}'.format(asset_id, prod_year)))
            curr.execute(sql_update.format(prod_year, abandonment, asset_id))
            commit(curr)
        asset_count += 1

def update_operator_equity():
    print 'Updating operator equity data ...'
    conn = get_connection()
    curr = conn.cursor()
    asset_data = get_data(param='asset_id, country', table='abandonment_data', datatype='plural')
    sql_select = \
    '''
    SELECT DISTINCT entity_name, operator, top_parent_company, equity_pct FROM equity 
    WHERE asset_id={0} AND 
          equity_date=(SELECT MAX(equity_date) FROM equity WHERE asset_id={0});
    '''
    sql_insert = 'INSERT INTO operator_abandonment (asset_id,country,company,operator,parent_company,equity_pct,`2018`,`2019`,`2020`,`2021`,`2022`,`2023`,`2024`,`2025`) VALUES ({}, "{}", "{}", "{}", "{}", {}, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)'
    sql_update = 'UPDATE operator_abandonment SET `{}`=ROUND({}*(equity_pct/100),2) WHERE asset_id={}'
    asset_count = 1
    asset_total = len(asset_data)
    for asset_id, country in asset_data:
        print '{}/{}: {}'.format(asset_count,asset_total,asset_id)
        total_equity = 0
        curr.execute(sql_select.format(asset_id))
        equity_data = curr.fetchall()
        for company, operator, top_parent, equity_pct in equity_data:
            curr.execute(sql_insert.format(asset_id, country, company, operator, top_parent, equity_pct))
            commit(curr)
        for prod_year in range(2018, 2026):
            abandonment = float(get_param(param='abandonment', table='abandonment_data', sql_where='asset_id={} AND prod_year={}'.format(asset_id, prod_year)))
            curr.execute(sql_update.format(prod_year, abandonment, asset_id))
            commit(curr)
        asset_count += 1

if __name__=='__main__':
    update_operator_equity()