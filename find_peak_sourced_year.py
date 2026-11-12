from globaldata import *


def get_conv_factor(curr,commodity,unit):
    conv_factor = 1.0
    sql_select  = "SELECT factor FROM unit_equals WHERE commodity='{}' and unit='{}' and base_unit='Boe'"
    prod_comm = commodity.lower().strip()
    comm_unit = unit.lower().strip()
    if prod_comm == 'ngl': prod_comm = 'ngls'
    if curr.execute(sql_select.format(prod_comm,comm_unit)):
        conv_factor = float(curr.fetchone()[0])
    return conv_factor

def find_peak_year(curr, asset_id):
    prod_start, capex_end = get_data('prod_start_year, capex_end_year', 'asset_prod_data', cursor=curr, datatype='plural', single_value=True, sql_where='asset_id={}'.format(asset_id))
    peak_sourced_year     = prod_start
    peak_prod_val         = 0
    sql_where = 'period={} AND casetype="Base Case" AND sources!="EST: Forecast Engine" AND asset_id={} AND IFNULL(production,0) > 0'
    for prod_year in range(prod_start, capex_end+1):
        prod_year_val = 0
        prod_data = get_data('commodity, production, unit', 'production', cursor=curr, datatype='plural', sql_where=sql_where.format(prod_year, asset_id))
        if prod_data:
            for prod_comm, prod_value, prod_unit in prod_data:
                conv_factor = get_conv_factor(curr, prod_comm, prod_unit)
                prod_value *= conv_factor
                prod_year_val += prod_value
        if prod_year_val > peak_prod_val:
            peak_prod_val = prod_year_val
            peak_sourced_year = prod_year
    return peak_sourced_year


def update_peak_prod_year():
    conn = get_connection()
    curr = conn.cursor()
    sql_update = 'UPDATE asset_prod_data SET peak_prod_year={} WHERE asset_id={}'
    asset_ids = get_data('asset_id', 'asset_prod_data', cursor=curr, datatype='int')
    asset_count = len(asset_ids)
    asset_num = 1
    for asset_id in asset_ids:
        print '{}/{}: {}'.format(asset_num, asset_count, asset_id)
        peak_prod_year = find_peak_year(curr, asset_id)
        curr.execute(sql_update.format(peak_prod_year, asset_id))
        commit(curr)
        asset_num += 1
    curr.close()
    conn.close()



if __name__=='__main__':
    main()