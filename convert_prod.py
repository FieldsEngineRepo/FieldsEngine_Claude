from globaldata import *

conn = get_connection()
curr = conn.cursor()

comm_data = {
    'Crude Oil'  : {'conv': 'Crude Oil',   'unit': 'Boe'},
    'Natural Gas': {'conv': 'Natural Gas', 'unit': 'Boe'},
    'Condensate' : {'conv': 'Crude Oil',   'unit': 'Boe'},
    'NGLs'       : {'conv': 'Crude Oil',   'unit': 'Boe'},
    'NGL'        : {'conv': 'Crude Oil',   'unit': 'Boe'},
    'LNG'        : {'conv': 'Natural Gas', 'unit': 'Boe'}
}
prod_data = execute(params=['asset_id', 'period', 'commodity', 'production', 'unit'], table='prod_lite')

for data in prod_data:
    print data.asset_id, data.period, data.commodity, data.production, data.unit
    conv_comm = comm_data[data.commodity]['conv']
    conv_unit = comm_data[data.commodity]['unit']
    conv_factor = get_param(param='factor', table='unit_equals', sql_where='commodity="{}" and unit="{}" and base_unit="{}"'.format(conv_comm, data.unit, conv_unit), debug=True)
    print conv_factor
    conv_prod = float(data.production) * float(conv_factor)
    curr.execute('UPDATE prod_lite SET conv_prod={}, conv_unit="{}" WHERE asset_id={} AND period={} AND commodity="{}"'.format(conv_prod, conv_unit, data.asset_id, data.period, data.commodity))
    commit(curr)

curr.close()
conn.close()