from globaldata import *

debug = False
'''
'Historical production decline',
'Well Drilling time (days)',
'Well Completion time (days)',
'Rig mobilization time (days)',
'Well Life',
'Drilling ($)',
'Completion ($)',
'Facilities ($)',
'Tangible cost percent split',
'Annual maintenance capital expenditure',
'Abandonment',
'Fixed Operating Expenditure',
'Liquids transportation ($/bbl)',
'Gas Transportation ($/mcf)'
'''


def enter_type_well_data(curr):
    #truncate_table(curr,'type_well_inputs')
    print 'Entering type-well data ...'
    run_id = get_run_id(curr)
    sql_update = \
        """
        UPDATE type_well_inputs AS a, param_track AS b 
          SET a.well_id=CONCAT(b.asset_id,'-01'), 
              a.well_name=CONCAT('Type-Well ',b.asset_id,'-01'), 
              a.constituent=b.constituent, 
              a.well_decline_rate=b.decline_rate, 
              a.rig_mobilization_days=b.rig_mobilization_days, 
              a.opex_liquids=ROUND(b.opex_liquids,2), 
              a.opex_gas=ROUND(b.opex_gas,2), 
              a.opex_trans_liquids=ROUND(b.opex_trans_liquids,2), 
              a.opex_trans_gas=ROUND(b.opex_trans_gas,2), 
              a.abandonment=b.well_abandonment, 
              a.well_life=ROUND(b.well_life,2), 
              a.capex_maintenance=b.capex_maintenance, 
              a.facility_cost=b.facility_cost, 
              a.fixed_opex_rate=b.fixed_opex_rate, 
              a.tangible_split_pct=ROUND(b.capex_tangible_pct, 2) 
          WHERE a.asset_id=b.asset_id
          AND b.session_key LIKE '%{0}%' 
          AND b.asset_id IN (SELECT DISTINCT asset_id FROM econ_data WHERE run_id='{0}' AND fiscal_model LIKE '%Resource%')
        """
    print sql_update.format(run_id)
    curr.execute(sql_update.format(run_id))
    commit(curr)
    curr.execute('''UPDATE type_well_inputs AS t, well_params AS w SET t.drilling_pct=ROUND(w.drilling_split,2) WHERE t.well_id LIKE CONCAT(w.asset_id, '%')''')
    commit(curr)
    curr.execute('''UPDATE type_well_inputs AS t, param_track AS p SET t.drilling_pct=ROUND(p.drilling_split,2) WHERE t.drilling_pct IS NULL AND t.well_id LIKE CONCAT(p.asset_id, '%')''')
    commit(curr)

def set_default_values(curr):
    print 'Setting default values ...'
    discount_year = get_discount_year(curr)
    edit_date = get_datetime()
    sql_update  = 'UPDATE type_well_inputs SET drilling_days=0.0, completion_days=0.0, drilling_cost=0.0, completion_cost=0.0, working_interest=1.0, well_density=0.01, '
    sql_update += 'oil_phase_pct=1.0, gas_phase_pct=1.0, condensate_phase_pct=0.0, ngls_phase_pct=0.0, water_disp_fee=0.0, ngls_proc_fee=0.0, field_maintenance=0.0, '
    sql_update += 'acreage_pct=0.0, annual_well_improve=0.0, well_improve_start={0}, annual_well_degrade=0.0, well_degrade_start={0}, add_by="Titan", edit_by="Titan", edit_date="{1}"'
    curr.execute(sql_update.format(discount_year, edit_date))
    commit(curr)

def update_drill_comp_data(asset_id):
    drilling_split  = 0.0
    drilling_days   = 0
    completion_days = 0
    drilling_cost   = 0
    completion_cost = 0

    conn = get_connection()
    curr = conn.cursor()

    run_id = get_run_id(curr)
    sql_select_pct  = "SELECT drilling_split FROM param_track WHERE session_key LIKE '%{}%' AND asset_id={}".format(run_id, asset_id)
    sql_select_days = "SELECT production_count FROM wells WHERE datatype='Wells Drilling & Completion Days' AND asset_id={} ORDER BY period DESC LIMIT 1".format(asset_id)
    sql_select_cost = "SELECT production_count FROM wells WHERE datatype='Drilling & Completion well cost' AND asset_id={} ORDER BY period DESC LIMIT 1".format(asset_id)

    if curr.execute(sql_select_pct):
        drilling_split = float(curr.fetchone()[0])
    if curr.execute(sql_select_days):
        total_drill_comp_time = curr.fetchone()[0]
        drilling_days = float(total_drill_comp_time) * float(drilling_split)
        completion_days = total_drill_comp_time - drilling_days
    if curr.execute(sql_select_cost):
        total_drill_comp_cost = curr.fetchone()[0]
        drilling_cost = float(total_drill_comp_cost) * float(drilling_split)
        completion_cost = total_drill_comp_cost - drilling_cost

    curr.close()
    conn.close()
    return drilling_days, completion_days, drilling_cost, completion_cost



def update_drill_comp_days(curr):
    print 'Updating drilling and completion days ...'
    asset_ids = get_assets('wells', "datatype='Wells Drilling & Completion Days'")
    sql_select = "SELECT production_count FROM wells WHERE datatype='Wells Drilling & Completion Days' AND asset_id={} ORDER BY period DESC LIMIT 1"
    sql_update = "UPDATE type_well_inputs SET drilling_days=ROUND({0}*drilling_pct,2), completion_days=ROUND({0}*(1-drilling_pct),2) WHERE well_id='{1}-01'"
    for asset_id in asset_ids:
        curr.execute(sql_select.format(asset_id))
        drill_comp_days = float(curr.fetchone()[0])
        if debug:
            print asset_id, sql_update.format(drill_comp_days, asset_id)
        curr.execute(sql_update.format(drill_comp_days, asset_id))
        commit(curr)

def update_drill_comp_cost(curr):
    print 'Updating drilling and completion cost ...'
    asset_ids = get_assets('wells', "datatype='Drilling & Completion well cost'")
    sql_select = "SELECT production_count FROM wells WHERE datatype='Drilling & Completion well cost' AND asset_id={} ORDER BY period DESC LIMIT 1"
    sql_update = "UPDATE type_well_inputs SET drilling_cost=ROUND({0}*drilling_pct,2), completion_cost=ROUND({0}*(1-drilling_pct),2) WHERE well_id='{1}-01'"
    for asset_id in asset_ids:
        curr.execute(sql_select.format(asset_id))
        drill_comp_cost = float(curr.fetchone()[0])
        if debug:
            print asset_id, sql_update.format(drill_comp_cost, asset_id)
        curr.execute(sql_update.format(drill_comp_cost, asset_id))
        curr.execute('UPDATE type_well_inputs SET drilling_pct=0.0 WHERE well_id="{0}-01"'.format(asset_id))
        commit(curr)

def update_working_interest(curr):
    print 'Updating working interest ...'
    asset_ids = get_assets('wells', "datatype='Working Interest'")
    sql_select = "SELECT production_count FROM wells WHERE datatype='Working Interest' AND asset_id={} ORDER BY period DESC LIMIT 1"
    sql_update = "UPDATE type_well_inputs SET working_interest=ROUND({0}/100,2) WHERE well_id='{1}-01'"
    for asset_id in asset_ids:
        curr.execute(sql_select.format(asset_id))
        working_interest = float(curr.fetchone()[0])
        if debug:
            print asset_id, sql_update.format(working_interest, asset_id)
        curr.execute(sql_update.format(working_interest, asset_id))
        commit(curr)

def update_royalty_rates(curr):
    print 'Updating royalty rates ...'
    royalty_rates = {
        'Alabama'       : 0.25,
        'Arizona'       : 0.125,
        'Arkansas'      : 0.125,
        'California'    : 0.2,
        'Colorado'      : 0.2,
        'Florida'       : 0.2,
        'Idaho'         : 0.125,
        'Illinois'      : 0.125,
        'Indiana'       : 0.125,
        'Kansas'        : 0.125,
        'Kentucky'      : 0.125,
        'Louisiana'     : 0.219,
        'Michigan'      : 0.1667,
        'Mississippi'   : 0.1875,
        'Montana'       : 0.1667,
        'Nebraska'      : 0.125,
        'New Mexico'    : 0.2,
        'New York'      : 0.125,
        'North Carolina': 0.125,
        'North Dakota'  : 0.1875,
        'Ohio'          : 0.125,
        'Oklahoma'      : 0.1875,
        'Pennsylvania'  : 0.125,
        'South Carolina': 0.125,
        'South Dakota'  : 0.125,
        'Texas'         : 0.25,
        'Utah'          : 0.1667,
        'Washington'    : 0.125,
        'West Virginia' : 0.125,
        'Wyoming'       : 0.1667,
        'Neuquen'       : 0.12
    }
    run_id = get_run_id(curr)
    asset_ids = get_assets('well_data', 'session_key LIKE "%{}%"'.format(run_id))
    sql_update = "UPDATE type_well_inputs SET royalty_rate=ROUND({0},2) WHERE well_id='{1}-01'"
    for asset_id in asset_ids:
        constituent = get_param('constituent', 'assets', asset_id=asset_id, cur=curr)
        if constituent in royalty_rates.keys():
            royalty_rate = royalty_rates[constituent]
            if debug:
                print asset_id, sql_update.format(royalty_rate, asset_id)
            curr.execute(sql_update.format(royalty_rate, asset_id))
        commit(curr)

def update_well_profiles(curr):
    print 'Updating type-well production profiles ...'
    comm_names = {'1': 'crude', '2':'ng', '3':'condensate','4':'ngls', '5':'lng'}
    curr.execute('SELECT DISTINCT profile_id FROM type_well_production WHERE NOT well_id="000000-00" ORDER BY well_id')
    profile_ids = [data[0] for data in curr.fetchall()]
    sql_update = "UPDATE type_well_inputs SET {}_profile_id='{}' WHERE well_id='{}'"
    for profile_id in profile_ids:
        well_id = profile_id[:-2]
        comm_code = profile_id[-1]
        comm_name = comm_names[comm_code]
        if debug:
            print well_id, sql_update.format(comm_name, profile_id, well_id)
        curr.execute(sql_update.format(comm_name, profile_id, well_id))
        commit(curr)
    for comm_code, comm_name in comm_names.items():
        curr.execute("UPDATE type_well_inputs SET {0}_profile_id='000000-00-{1}' WHERE {0}_profile_id IS NULL".format(comm_name, comm_code))
        commit(curr)



def main():
    conn = get_connection()
    curr = conn.cursor()

    enter_type_well_data(curr)
    set_default_values(curr)
    update_drill_comp_days(curr)
    update_drill_comp_cost(curr)
    update_working_interest(curr)
    update_royalty_rates(curr)
    #update_well_profiles(curr)

    curr.close()
    conn.close()

if __name__=='__main__':
    main()