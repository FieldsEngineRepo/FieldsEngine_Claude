from globaldata import *

conn = get_connection()
curr = conn.cursor()
sql_select = 'SELECT DISTINCT asset_id FROM assets WHERE country=%s'
country = 'United States'
if curr.execute(sql_select, (country,)):
    asset_ids = [data[0] for data in curr.fetchall()]
    print 'asset_ids:', asset_ids
else:
    print 'no assets found'
curr.close()
conn.close()