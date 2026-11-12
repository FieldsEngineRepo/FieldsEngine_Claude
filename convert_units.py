from globaldata import *

conn = get_connection()
curr = conn.cursor()
from_boe = {
    'Crude Oil'  : {'unit':'bd',    'factor': float(1.0/365.242)},
    'Natural Gas': {'unit':'mmcfd', 'factor': float(1.0/60873.7)},
    'Condensate' : {'unit':'bd',    'factor': float(1.0/365.242)},
    'LNG'        : {'unit':'mmcfd', 'factor': float(1.0/60873.7)},
    'NGL'        : {'unit':'bd',    'factor': float(1.0/365.242)}
}

asset_ids = get_assets(table='assets', sql_where='status="Producing" AND region IN ("North America", "Caribbean", "Central America")')
asset_count = len(asset_ids)
asset_num = 1
for asset_id in asset_ids:
    print '{}/{}: {}'.format(asset_num, asset_count, asset_id)
    asset_select = 'SELECT asset_name, country, constituent, region, status, terrain, basin, resource_type, facility_type FROM asset_data WHERE asset_id={}'.format(asset_id)
    curr.execute(asset_select)
    asset_name, country, constituent, region, status, terrain, basin, resource_type, facility_type = curr.fetchone()
    sql_select = 'SELECT commodity, period, production, unit FROM production WHERE asset_id={} AND casetype="Base Case" AND period < 2018 AND commodity IN ("Crude Oil","Natural Gas","Condensate","LNG","NGL") ORDER BY commodity, period'.format(asset_id)
    curr.execute(sql_select)
    for commodity, period, production, unit in curr.fetchall():
        conv_factor = get_conversion_factor(commodity, unit, 'Boe', time_unit='year', cur=curr)
        converted_prod = (float(production) * conv_factor) * from_boe[commodity]['factor']
        converted_unit = from_boe[commodity]['unit']
        sql_insert = 'INSERT INTO production_converted (asset_id, asset_name, country, constituent, region, status, terrain, basin, resource_type, facility_type, commodity, period, production, unit) '
        sql_insert += 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        param_vals = (asset_id, asset_name, country, constituent, region, status, terrain, basin, resource_type, facility_type, commodity, period, converted_prod, converted_unit)
        curr.execute(sql_insert, param_vals)
    commit(curr)
    asset_num += 1

curr.close()
conn.close()