import globaldata as gd

gd.REGION_NAMES

conn = gd.get_connection()
curr = conn.cursor()
sql_where = "run_id=(SELECT DISTINCT run_id FROM global_variables WHERE id=1) AND `status` NOT IN ('Producing', 'Abandoned', 'Suspended')"
asset_list = gd.get_data('asset_id', 'econ_data', cursor=curr, datatype='int', sql_where=sql_where)
gd.move_files(gd.BE_REGIONS+'North America\\', gd.BE_REGIONS+'North_America_1\\', file_extn='xlsx', outfile_code='', asset_list=asset_list)
# Export analogue asset data