from globaldata import *

#SELECT COLUMN_NAME FROM globaldata.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='globaldata' AND TABLE_NAME='assets';


def get_uncon_data(curr, asset_id):
    uncon_data = ()
    discount_year = get_discount_year()
    sql_select = 'SELECT rigs FROM uncon_production WHERE period={} AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    rig_count = float(curr.fetchone()[0])

    sql_select = 'SELECT MAX(period), production_count FROM wells WHERE datatype LIKE "Wells Drilling & Completion%" AND asset_id={}'.format(asset_id)
    curr.execute(sql_select)
    drill_comp_days = float(curr.fetchone()[0])

    sql_select = 'SELECT well_life, rig_mobilization_days FROM well_params WHERE asset_id={}'.format(asset_id)
    curr.execute(sql_select)
    well_life, rig_mobile_days = float(curr.fetchone())
    drill_comp_days += rig_mobile_days

    sql_select = 'SELECT MAX(period) FROM uncon_production WHERE rigs > 0 AND asset_id={}'.format(asset_id)
    curr.execute(sql_select)
    last_rig_year = int(curr.fetchone()[0])

    sql_select = 'SELECT SUM(type_wells_added) FROM uncon_production WHERE period >= {} AND rigs > 0 AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    new_wells_rem = float(curr.fetchone()[0])

    sql_select = 'SELECT type_wells_added FROM uncon_production WHERE period={} AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    new_wells = float(curr.fetchone()[0])

    uncon_data = (rig_count, last_rig_year, well_life, new_wells, new_wells_rem, drill_comp_days)
    return uncon_data

def update_uncon_data(curr, run_id):
    sql_select = 'SELECT DISTINCT asset_id FROM econ_data WHERE run_id="{}" AND fiscal_model LIKE "%Resource Play%"'.format(run_id)



def update_econ_data():
    conn = get_connection()
    curr = conn.cursor()
    if 0:
        sql_update = 'UPDATE econ_data SET {0}=NULL WHERE ({0}="NULL" OR LENGTH({0}) < 1)'
        and_str = 'AND NOT DATA_TYPE IN ("double", "int", "float", "tinyint") '
        col_names = get_columns('econ_data', and_str=and_str)
        for col_name in col_names:
            sql_command = sql_update.format(col_name)
            print sql_command
            curr.execute(sql_command)
        commit(curr)

        sql_update = 'UPDATE econ_data SET {0}=0 WHERE ({0} IS NULL OR {0} IN (-4293652562, -2146826281)) '
        and_str = 'AND DATA_TYPE IN ("double", "int", "float") '
        col_names = get_columns('econ_data', no_id=True, and_str=and_str)
        for col_name in col_names:
            sql_command = sql_update.format(col_name)
            print sql_command
            curr.execute(sql_command)
        commit(curr)
    elif 1:
        sql_select = 'SELECT asset_name FROM econ_data WHERE fiscal_model LIKE "%Resource Play%"'
        curr.execute(sql_select)
        uncon_asset_names = [data[0] for data in curr.fetchall()]
        for asset_name in uncon_asset_names:
            if '(' in asset_name:
                position = asset_name.split('(')[0].strip()
                sql_update = 'UPDATE econ_data SET position="%s" WHERE asset_name="%s"'
                curr.execute(sql_update % (position, asset_name))
                commit(curr)
    curr.close()
    conn.close()

if __name__=='__main__':
    update_econ_data()