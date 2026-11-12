from globaldata import *

def update_uncon_capex(curr, ss_curr, last_fiscal_year, add_date):
    sql_select  = 'SELECT DISTINCT asset_id, asset_name, country, constituent, region FROM wells WHERE asset_id IN '
    sql_select += '(SELECT DISTINCT asset_id FROM uncon_data WHERE capex_tangible > 0 AND capex_intangible > 0 AND period=%s) ' % last_fiscal_year
    sql_select += 'AND NOT asset_id IN (SELECT DISTINCT asset_id FROM wells WHERE datatype="Capex (US$ mil)" AND period=%s) ' % last_fiscal_year
    curr.execute(sql_select)
    uncon_asset_data = curr.fetchall()
    sql_select = 'SELECT [Capital Expenditure] FROM Engine.tblEngineCashFlowData WHERE AssetID=? AND Year=?'
    sql_insert = 'INSERT INTO wells (asset_id,asset_name,country,constituent,commodity,region,datatype,period,production_count,unit,casetype,asset_relationship,sources,data_source,add_by,add_date) VALUES (%s) '
    var_str = '%s,"%s","%s","%s","NULL","%s","Capex (US$ mil)", %s, %s, "Mil", "Base Case", "Parent", "EST: Hardcode", "Engine", "Titan II", "%s"'
    sql_insert = sql_insert % var_str
    for asset_id, asset_name, country, constituent, region in uncon_asset_data:
        ss_curr.execute(sql_select, (str(asset_id), str(last_fiscal_year)))
        capex = round(float(ss_curr.fetchone()[0])/1000000.0,7)
        param_vals = (asset_id, asset_name, country, constituent, region, last_fiscal_year, capex, add_date)
        curr.execute(sql_insert % param_vals)
        curr.execute('COMMIT')


def update_uncon_opex(curr, ss_curr, last_fiscal_year, add_date):
    sql_select  = 'SELECT DISTINCT asset_id, asset_name, country, constituent, region FROM wells WHERE asset_id IN '
    sql_select += '(SELECT DISTINCT asset_id FROM uncon_data WHERE opex_fixed > 0 AND opex_variable > 0 AND period=%s) ' % last_fiscal_year
    sql_select += 'AND NOT asset_id IN (SELECT DISTINCT asset_id FROM wells WHERE datatype="Opex (US$ mil)" AND period=%s) ' % last_fiscal_year
    curr.execute(sql_select)
    uncon_asset_data = curr.fetchall()
    sql_select = 'SELECT [Operating Expenditure] FROM Engine.tblEngineCashFlowData WHERE AssetID=? AND Year=?'
    sql_insert = 'INSERT INTO wells (asset_id,asset_name,country,constituent,commodity,region,datatype,period,production_count,unit,casetype,asset_relationship,sources,data_source,add_by,add_date) VALUES (%s) '
    var_str = '%s,"%s","%s","%s","NULL","%s","Opex (US$ mil)", %s, %s, "Mil", "Base Case", "Parent", "EST: Hardcode", "Engine", "Titan II", "%s"'
    sql_insert = sql_insert % var_str
    for asset_id, asset_name, country, constituent, region in uncon_asset_data:
        ss_curr.execute(sql_select, (str(asset_id), str(last_fiscal_year)))
        opex = round(float(ss_curr.fetchone()[0])/1000000.0,7)
        param_vals = (asset_id, asset_name, country, constituent, region, last_fiscal_year, opex, add_date)
        curr.execute(sql_insert % param_vals)
        curr.execute('COMMIT')


def main():
    conn = get_connection()
    curr = conn.cursor()
    ss_conn = get_connection(server='sql_server', database='OGEngineDataExtract')
    ss_curr = ss_conn.cursor()
    discount_year = get_discount_year(curr)
    last_fiscal_year = discount_year - 1
    add_date = get_add_date()

    update_uncon_capex(curr, ss_curr, last_fiscal_year, add_date)
    update_uncon_opex(curr, ss_curr, last_fiscal_year, add_date)
    ss_curr.close()
    ss_conn.close()
    curr.close()
    conn.close()


def get_uncon_rank(curr, asset_id, param_name, rank_order, run_id):
    param_rank = 0
    param_total = 1
    sql_select = 'SELECT asset_id FROM econ_data WHERE run_id="{1}" AND fiscal_model LIKE "%Resource Play%" ORDER BY {0} {2}'.format(param_name, run_id, rank_order)
    curr.execute(sql_select)
    ranked_uncon_assets = [data[0] for data in curr.fetchall()]
    param_rank = ranked_uncon_assets.index(asset_id)+1
    param_total = len(ranked_uncon_assets)
    if 1:
        print '{}({}): {}/{}'.format(asset_id, param_name, param_rank, param_total)
    return param_rank, param_total

if __name__=='__main__':
    conn = get_connection()
    curr = conn.cursor()
    param_rank, param_total = get_uncon_rank(curr, 851671, 'new_wells_rem', 'DESC', '20180418_205149')
    curr.close()
    conn.close()