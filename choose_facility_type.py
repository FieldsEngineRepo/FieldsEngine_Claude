from globaldata import *

UPDATED_FIELDS = []

def choose_facility_type(cursor, field_id):
    sql_select = '''SELECT c.facilitytype AS facility_type, SUM(c.analoguescore) AS total_analogue_score
    FROM (SELECT a.analogue_id, a.analogue_score AS analoguescore, b.facility_type AS facilitytype FROM globaldata.field_analogues AS a, globaldata.assets AS b WHERE a.analogue_id=b.asset_id AND a.asset_id={}) AS c
    WHERE NOT c.facilitytype='NULL' GROUP BY c.facilitytype ORDER BY total_analogue_score DESC LIMIT 1'''.format(field_id)
    if cursor.execute(sql_select):
        analogue_facility, analogue_facility_score = cursor.fetchall()[0]
        cursor.execute('UPDATE asset_data SET facility_type="{}" WHERE asset_id={}'.format(analogue_facility, field_id))
        print 'UPDATE asset_data SET facility_type="{}" WHERE asset_id={}'.format(analogue_facility, field_id)
        commit(cursor)
        UPDATED_FIELDS.append(field_id)

def update_facility_type():
    conn = get_connection()
    curr = conn.cursor()
    where_clause = 'asset_id IN (SELECT DISTINCT asset_id FROM field_analogues ORDER BY asset_id) AND (facility_type IS NULL OR facility_type="NULL")'
    disc_field_ids = get_data('asset_id', 'asset_data', sql_where=where_clause, datatype='int')
    for disc_field_id in disc_field_ids:
        print disc_field_id
        choose_facility_type(cursor=curr, field_id=disc_field_id)
    curr.close()
    conn.close()


if __name__=='__main__':
    update_facility_type()
    print UPDATED_FIELDS