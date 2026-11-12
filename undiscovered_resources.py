import os
import shutil

import numpy as np
from scipy.optimize import *

import globaldata as gd
from discovered_analogues import main as analogue_main
from update_asset_data import update_asset_data_tbl as update_asset_data_table

TOP_BASINS = [
    'West Siberian Basin',
    'Widyan-North Arabian Gulf Basin',
    'Arabian Basin',
    'Zagros Fold and Thrust Belt',
    'Mesopotamian Foredeep Basin',
    'Rub al-Khali Basin',
    'Northern North Sea Basin',
    'Persian Gulf Basin',
    'Gulf of Mexico Basin',
    'Permian Basin',
    'Southeastern Basin',
    'Lower Congo Basin',
    'Santos Basin'
]

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_reserve_start(curr, runid=''):
    run_id = gd.get_run_id()
    if runid: run_id = runid
    sql_update = \
     '''
    UPDATE econ_data AS c, 
       (SELECT a.asset_id AS ast_id, IF(a.discovery_date='NULL', b.first_production, CONVERT(SUBSTR(a.discovery_date,1,4),SIGNED)) AS res_start FROM assets a, (SELECT asset_id, first_production FROM econ_data WHERE run_id='{0}') b WHERE a.asset_id=b.asset_id) AS d
    SET c.reserve_start=d.res_start WHERE c.asset_id=d.ast_id AND c.run_id='{0}'
    '''
    curr.execute(sql_update.format(run_id))
    gd.commit(curr)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def find_curve_fit(x_values=None, y_values=None, start_year=1900, opt_config='', max_reserve_limit=0, debug=False):
    if debug: print y_values

    min_res = y_values[-1]
    max_res = 2 * y_values[-1]

    if max_reserve_limit:
        max_res = max(max_reserve_limit, max_res)

    a, b, c = [min_res * 1.1, 7, 0.075]
    bounds  = ((min_res, 1, 0.0001), (max_res, 100, .99))

    init_len = len(y_values)
    xdata_init = np.zeros(1)
    ydata_init = np.zeros(1)
    xdata_init = np.arange(init_len)
    ydata_init = np.array(y_values)
    xdata = xdata_init
    ydata = ydata_init

    def og_creaming_curve(x, a, b, c):
        return a * np.exp(-b * np.exp(-c * x))

    try:
        init_params = np.array([a, b, c])
        opt_round = 1
        if opt_config:
            config_str = opt_config
        else:
            config_str = 'abcx'
        print '{}: a: {} - b: {} - c: {}'.format(0, a, b, c)
        round_config = ''
        for var_opt in config_str:
            round_config += var_opt
            if var_opt == 'a':
                init_params = np.array([a])
                if debug: print 'a: (bounds[0][0], bounds[1][0]): {}'.format((bounds[0][0], bounds[1][0]))
                popt, pcov = curve_fit((lambda _x, _a: og_creaming_curve(_x, _a, b, c)), xdata, ydata, maxfev=10000, p0=init_params, bounds=(bounds[0][0], bounds[1][0]))
                a = popt[0]
            elif var_opt == 'b':
                init_params = np.array([b])
                popt, pcov = curve_fit((lambda _x, _b: og_creaming_curve(_x, a, _b, c)), xdata, ydata, maxfev=10000, p0=init_params, bounds=(bounds[0][1], bounds[1][1]))
                b = popt[0]
            elif var_opt == 'c':
                init_params = np.array([c])
                popt, pcov = curve_fit((lambda _x, _c: og_creaming_curve(_x, a, b, _c)), xdata, ydata, maxfev=10000, p0=init_params, bounds=(bounds[0][2], bounds[1][2]))
                c = popt[0]
            else:
                init_params = np.array([a, b, c])
                if debug: print 'init_params: {} --- bounds[0], bounds[1]: {}, {}'.format(init_params, bounds[0], bounds[1])
                popt, pcov = curve_fit(og_creaming_curve, xdata, ydata, maxfev=10000000, p0=init_params, bounds=bounds)
                a, b, c = popt
            if debug: print '{} ({}): a: {} - b: {} - c: {}'.format(opt_round, round_config, a, b, c)
            opt_round += 1
        a_out, b_out, c_out = (a, b, c)
        xdata_out = np.arange(len(range(start_year, 2065)))
        ydata_out = og_creaming_curve(xdata_out, a, b, c)
        curve_params = (a, b, c)
        fit_curve = dict(zip(xdata_out, ydata_out.tolist()))
    except:
        print 'Optimal parameters not found: Number of calls to function has reached maxfev = 800'
        curve_params = (0, 0, 0)
        fit_curve = {}

    return curve_params, fit_curve

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def abandoned_field_check(curr, basin, debug=False):
    has_abandoned_fields = False
    abandoned_field_count = gd.get_data('COUNT(*)', 'assets', sql_where='basin="{}" AND status="Abandoned"'.format(basin), datatype='int', single_value=True, cursor=curr, debug=debug)
    if abandoned_field_count:
        has_abandoned_fields = True
    return has_abandoned_fields


def remaining_reserves_check(curr, basin, debug=False):
    low_remaining_reserves = False
    remaining_reserve_pct = gd.get_data('remaining_reserve_pct', 'basin_data', sql_where='basin_name="{}"'.format(basin), single_value=True, cursor=curr, datatype='float', debug=debug)
    if 0 < remaining_reserve_pct < 0.5:
        low_remaining_reserves = True
    return low_remaining_reserves


def update_analog_basins(curr, debug=False):
    curr.execute('UPDATE reserves_forecast AS a, basin_data AS b SET a.basin_id=b.basin_id WHERE a.basin=b.basin_name')
    gd.commit(curr)

    curr.execute('UPDATE basin_data AS a, reserves_forecast AS b SET a.a_value=b.a_value, a.b_value=b.b_value, a.c_value=b.c_value WHERE a.basin_name=b.basin AND b.hist_reserves_mmboe IS NULL AND a.is_mature_basin=1')
    gd.commit(curr)

    sql_select = \
    '''
    SELECT a.basin_name, (b.avg_field_reserves-a.avg_field_reserves) AS field_reserves_diff FROM basin_data AS a,
    (SELECT primary_terrain, avg_field_reserves FROM basin_data WHERE basin_name="{0}") AS b
    WHERE a.primary_terrain=b.primary_terrain AND ((b.avg_field_reserves-a.avg_field_reserves) > 0)
    AND a.basin_name IN (SELECT DISTINCT basin FROM reserves_forecast WHERE (a_value > 0) AND (b_value > 0) AND (c_value > 0))
    AND NOT a.basin_name IN ("{0}", "NULL") AND a.is_mature_basin=1
    ORDER BY field_reserves_diff ASC LIMIT 5
    '''
    avg_val_sql_update = \
    '''
    UPDATE basin_data AS a,
    (SELECT ROUND(AVG(a_value),3) AS max_reserves
     FROM basin_data WHERE (basin_name=(SELECT analogue_basin_1 FROM basin_data WHERE basin_name="{0}")
        OR basin_name=(SELECT analogue_basin_2 FROM basin_data WHERE basin_name="{0}")
        OR basin_name=(SELECT analogue_basin_3 FROM basin_data WHERE basin_name="{0}")
        OR basin_name=(SELECT analogue_basin_4 FROM basin_data WHERE basin_name="{0}")
        OR basin_name=(SELECT analogue_basin_5 FROM basin_data WHERE basin_name="{0}"))) AS b
     SET a.max_reserves=b.max_reserves WHERE a.basin_name="{0}"
    '''
    immature_basins = gd.get_data('basin_name', 'basin_data', sql_where='is_mature_basin=0 AND NOT avg_field_reserves IS NULL', cursor=curr, debug=debug)
    print 'immature_basins: {}'.format(immature_basins)
    for basin in immature_basins:
        curr.execute(sql_select.format(basin))
        analog_basin_data = curr.fetchall()
        analog_num = 1
        for analog_basin, reserves_diff in analog_basin_data:
            if debug: print 'UPDATE basin_data SET analogue_basin_{}="{}" WHERE basin_name="{}"'.format(analog_num, analog_basin, basin)
            curr.execute('UPDATE basin_data SET analogue_basin_{}="{}" WHERE basin_name="{}"'.format(analog_num, analog_basin, basin))
            gd.commit(curr)
            analog_num += 1
        if debug: print avg_val_sql_update.format(basin)
        curr.execute(avg_val_sql_update.format(basin))
        gd.commit(curr)

    curr.execute('DELETE FROM basin_data WHERE (NOT field_count > 0) OR (field_count IS NULL) OR (total_recov IS NULL)')
    gd.commit(curr)


def update_basin_data(curr, with_disc=False, debug=False):
    curr.execute('TRUNCATE TABLE basin_data')
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------------------------------
    if debug: print 'INSERT INTO basin_data (basin_name) (SELECT DISTINCT basin FROM assets WHERE NOT basin IS NULL ORDER BY basin)'
    curr.execute('INSERT INTO basin_data (basin_name) (SELECT DISTINCT basin FROM assets WHERE NOT basin IS NULL ORDER BY basin)')
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------------------------------
    if debug: print 'UPDATE basin_data SET basin_id=(id+100)'
    curr.execute('UPDATE basin_data SET basin_id=(id+100)')
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------------------------------
    if debug: print 'UPDATE basin_data SET remaining_reserve_pct=0'
    curr.execute('UPDATE basin_data SET remaining_reserve_pct=0')
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------------------------------
    if debug: print 'UPDATE basin_data SET onshore_pct=0, offshore_pct=0'
    curr.execute('UPDATE basin_data SET onshore_pct=0, offshore_pct=0')
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------------------------------
    if with_disc:
        onshore_pct_sql_update = \
        """
        UPDATE basin_data AS f,
        (SELECT c.basin, IF(d.terrain='Onshore',d.terrain,'Offshore') AS primary_terrain, ROUND(d.total_terrain_reserves/c.total_basin_reserves,3) AS total_terrain_pct FROM
          (SELECT a.basin, SUM(a.total_terrain_recov) AS total_basin_reserves
            FROM (SELECT DISTINCT basin, terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL GROUP BY basin, terrain) AS a
            GROUP BY a.basin) AS c,
          (SELECT b.basin, IF(b.primary_terrain='Onshore',b.primary_terrain,'Offshore') AS terrain, SUM(b.total_terrain_recov) AS total_terrain_reserves
            FROM (SELECT DISTINCT basin, IF(terrain='Onshore',terrain,'Offshore') AS primary_terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL GROUP BY basin, terrain) AS b
            GROUP BY b.basin, terrain) AS d
          WHERE c.basin=d.basin
          GROUP BY c.basin, primary_terrain) AS e
        SET f.onshore_pct=e.total_terrain_pct WHERE f.basin_name=e.basin AND e.primary_terrain='Onshore'
        """
    else:
        onshore_pct_sql_update = \
        """
        UPDATE basin_data AS f,
        (SELECT c.basin, IF(d.terrain='Onshore',d.terrain,'Offshore') AS primary_terrain, ROUND(d.total_terrain_reserves/c.total_basin_reserves,3) AS total_terrain_pct FROM
          (SELECT a.basin, SUM(a.total_terrain_recov) AS total_basin_reserves
            FROM (SELECT DISTINCT basin, terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL AND NOT status="Discovered" GROUP BY basin, terrain) AS a
            GROUP BY a.basin) AS c,
          (SELECT b.basin, IF(b.primary_terrain='Onshore',b.primary_terrain,'Offshore') AS terrain, SUM(b.total_terrain_recov) AS total_terrain_reserves
            FROM (SELECT DISTINCT basin, IF(terrain='Onshore',terrain,'Offshore') AS primary_terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL AND NOT status="Discovered" GROUP BY basin, terrain) AS b
            GROUP BY b.basin, terrain) AS d
          WHERE c.basin=d.basin
          GROUP BY c.basin, primary_terrain) AS e
        SET f.onshore_pct=e.total_terrain_pct WHERE f.basin_name=e.basin AND e.primary_terrain='Onshore'
        """
    if debug: print onshore_pct_sql_update
    curr.execute(onshore_pct_sql_update)
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------------------------------
    if with_disc:
        offshore_pct_sql_update = \
        """
        UPDATE basin_data AS f,
        (SELECT c.basin, IF(d.terrain='Onshore',d.terrain,'Offshore') AS primary_terrain, ROUND(d.total_terrain_reserves/c.total_basin_reserves,3) AS total_terrain_pct FROM
          (SELECT a.basin, SUM(a.total_terrain_recov) AS total_basin_reserves
            FROM (SELECT DISTINCT basin, terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL GROUP BY basin, terrain) AS a
            GROUP BY a.basin) AS c,
          (SELECT b.basin, IF(b.primary_terrain='Onshore',b.primary_terrain,'Offshore') AS terrain, SUM(b.total_terrain_recov) AS total_terrain_reserves
            FROM (SELECT DISTINCT basin, IF(terrain='Onshore',terrain,'Offshore') AS primary_terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL GROUP BY basin, terrain) AS b
            GROUP BY b.basin, terrain) AS d
          WHERE c.basin=d.basin
          GROUP BY c.basin, primary_terrain) AS e
        SET f.offshore_pct=e.total_terrain_pct WHERE f.basin_name=e.basin AND e.primary_terrain='Offshore'
        """
    else:
        offshore_pct_sql_update = \
        """
        UPDATE basin_data AS f,
        (SELECT c.basin, IF(d.terrain='Onshore',d.terrain,'Offshore') AS primary_terrain, ROUND(d.total_terrain_reserves/c.total_basin_reserves,3) AS total_terrain_pct FROM
          (SELECT a.basin, SUM(a.total_terrain_recov) AS total_basin_reserves
            FROM (SELECT DISTINCT basin, terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL AND NOT status="Discovered" GROUP BY basin, terrain) AS a
            GROUP BY a.basin) AS c,
          (SELECT b.basin, IF(b.primary_terrain='Onshore',b.primary_terrain,'Offshore') AS terrain, SUM(b.total_terrain_recov) AS total_terrain_reserves
            FROM (SELECT DISTINCT basin, IF(terrain='Onshore',terrain,'Offshore') AS primary_terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL AND NOT status="Discovered" GROUP BY basin, terrain) AS b
            GROUP BY b.basin, terrain) AS d
          WHERE c.basin=d.basin
          GROUP BY c.basin, primary_terrain) AS e
        SET f.offshore_pct=e.total_terrain_pct WHERE f.basin_name=e.basin AND e.primary_terrain='Offshore'
        """
    if debug: print offshore_pct_sql_update
    curr.execute(offshore_pct_sql_update)
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------------------------------
    if with_disc:
        terrain_sql_update = \
        """
        UPDATE basin_data AS f,
        (SELECT c.basin, IF(d.terrain='Onshore',d.terrain,'Offshore') AS primary_terrain, ROUND(d.total_terrain_reserves/c.total_basin_reserves,3) AS total_terrain_pct FROM
          (SELECT a.basin, SUM(a.total_terrain_recov) AS total_basin_reserves
            FROM (SELECT DISTINCT basin, terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL GROUP BY basin, terrain) AS a
            GROUP BY a.basin) AS c,
          (SELECT b.basin, IF(b.primary_terrain='Onshore',b.primary_terrain,'Offshore') AS terrain, SUM(b.total_terrain_recov) AS total_terrain_reserves
            FROM (SELECT DISTINCT basin, IF(terrain='Onshore',terrain,'Offshore') AS primary_terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL GROUP BY basin, terrain) AS b
            GROUP BY b.basin, terrain) AS d
          WHERE c.basin=d.basin
          GROUP BY c.basin, primary_terrain) AS e
        SET f.primary_terrain=e.primary_terrain
        WHERE f.basin_name=e.basin AND e.total_terrain_pct > 0.5
        """
    else:
        terrain_sql_update = \
        """
        UPDATE basin_data AS f,
        (SELECT c.basin, IF(d.terrain='Onshore',d.terrain,'Offshore') AS primary_terrain, ROUND(d.total_terrain_reserves/c.total_basin_reserves,3) AS total_terrain_pct FROM
          (SELECT a.basin, SUM(a.total_terrain_recov) AS total_basin_reserves
            FROM (SELECT DISTINCT basin, terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL AND NOT status="Discovered" GROUP BY basin, terrain) AS a
            GROUP BY a.basin) AS c,
          (SELECT b.basin, IF(b.primary_terrain='Onshore',b.primary_terrain,'Offshore') AS terrain, SUM(b.total_terrain_recov) AS total_terrain_reserves
            FROM (SELECT DISTINCT basin, IF(terrain='Onshore',terrain,'Offshore') AS primary_terrain, SUM(total_recov) AS total_terrain_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT total_recov IS NULL AND NOT status="Discovered" GROUP BY basin, terrain) AS b
            GROUP BY b.basin, terrain) AS d
          WHERE c.basin=d.basin
          GROUP BY c.basin, primary_terrain) AS e
        SET f.primary_terrain=e.primary_terrain
        WHERE f.basin_name=e.basin AND e.total_terrain_pct > 0.5
        """
    if debug: print terrain_sql_update
    curr.execute(terrain_sql_update)
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------------------------------
    if with_disc:
        reserves_sql_update = \
        """
        UPDATE basin_data AS a,
        (SELECT basin, ROUND(SUM(total_recov_rem),2) AS basin_total_recov_rem, ROUND(SUM(total_recov),2) AS basin_total_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) GROUP BY basin) AS b
          SET a.total_recov_rem=b.basin_total_recov_rem, a.total_recov=b.basin_total_recov, a.remaining_reserve_pct=ROUND(b.basin_total_recov_rem/b.basin_total_recov, 3)
          WHERE a.basin_name=b.basin
        """
    else:
        reserves_sql_update = \
        """
        UPDATE basin_data AS a,
        (SELECT basin, ROUND(SUM(total_recov_rem),2) AS basin_total_recov_rem, ROUND(SUM(total_recov),2) AS basin_total_recov FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT status="Discovered" GROUP BY basin) AS b
          SET a.total_recov_rem=b.basin_total_recov_rem, a.total_recov=b.basin_total_recov, a.remaining_reserve_pct=ROUND(b.basin_total_recov_rem/b.basin_total_recov, 3)
          WHERE a.basin_name=b.basin
        """
    if debug: print reserves_sql_update
    curr.execute(reserves_sql_update)
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------------------------------
    if with_disc:
        field_count_sql_update = \
        """
        UPDATE basin_data AS a,
        (SELECT basin, COUNT(DISTINCT asset_id) AS field_count FROM assets
        WHERE IF(assoc_asset_id='NULL', asset_id, assoc_asset_id) IN (SELECT DISTINCT asset_id FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1))
        GROUP BY basin) AS b
        SET a.field_count=b.field_count WHERE a.basin_name=b.basin
        """
    else:
        field_count_sql_update = \
        """
        UPDATE basin_data AS a,
        (SELECT basin, COUNT(DISTINCT asset_id) AS field_count FROM assets
        WHERE IF(assoc_asset_id='NULL', asset_id, assoc_asset_id) IN (SELECT DISTINCT asset_id FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1) AND NOT status="Discovered")
        GROUP BY basin) AS b
        SET a.field_count=b.field_count WHERE a.basin_name=b.basin
        """
    if debug: print field_count_sql_update
    curr.execute(field_count_sql_update)
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------------------------------
    print 'Updating basin field data ...'
    update_basin_field_data(curr, with_disc=with_disc, debug=debug)
    
    print 'Updating Child Fields ...'
    update_child_fields(curr, debug=debug)
    #
    print 'Updating Median Field Sizes ...'
    update_avg_field_reserves(curr, debug=debug)
    #
    print 'Identifying Mature Basins ...'
    identify_mature_basins(curr, debug=debug)


def update_basin_field_data(curr, with_disc=False, debug=False):
    curr.execute('TRUNCATE TABLE basin_field_data')
    gd.commit(curr)
    curr.execute('''UPDATE econ_data AS a,
                    (SELECT DISTINCT asset_id, MAX(run_id) AS max_run_id FROM econ_data WHERE total_recov IS NOT NULL GROUP BY asset_id) AS b
                    SET a.run_id=(SELECT run_id FROM global_variables WHERE id=1)
                    WHERE a.run_id=b.max_run_id AND a.asset_id=b.asset_id AND b.max_run_id!=(SELECT run_id FROM global_variables WHERE id=1);''')
    gd.commit(curr)
    
    # -----------------------------------------------------------------------------------------------------
    if with_disc:
        sql_insert = 'INSERT INTO basin_field_data (asset_id, parent_asset_id, asset_relation, basin, reserve_type) (SELECT DISTINCT asset_id, IF(asset_relation="Child",IF(assoc_asset_id="NULL",asset_id,assoc_asset_id),asset_id), asset_relation, basin, "Recoverable" FROM assets ORDER BY asset_id)'
    else:
        sql_insert = 'INSERT INTO basin_field_data (asset_id, parent_asset_id, asset_relation, basin, reserve_type) (SELECT DISTINCT asset_id, IF(asset_relation="Child",IF(assoc_asset_id="NULL",asset_id,assoc_asset_id),asset_id), asset_relation, basin, "Recoverable" FROM assets WHERE NOT `status`="Discovered" ORDER BY asset_id)'

    if debug: print sql_insert
    curr.execute(sql_insert)
    gd.commit(curr)

    # -----------------------------------------------------------------------------------------------------------------------------
    sql_update_1 = \
    '''
    UPDATE basin_field_data AS a,
      (SELECT parent_asset_id, COUNT(DISTINCT asset_id) AS field_count FROM basin_field_data GROUP BY parent_asset_id) AS b
      SET a.child_field_count=b.field_count WHERE a.asset_id=b.parent_asset_id AND a.asset_relation='Parent'
    '''
    if debug: print sql_update_1
    curr.execute(sql_update_1)
    gd.commit(curr)

    # -----------------------------------------------------------------------------------------------------------------------------
    if debug: print 'UPDATE basin_field_data SET reserve_start=NULL, total_recov_mmboe=NULL'
    curr.execute('UPDATE basin_field_data SET reserve_start=NULL, total_recov_mmboe=NULL')
    gd.commit(curr)

    # -----------------------------------------------------------------------------------------------------------------------------
    sql_update_2 = \
    '''
    UPDATE basin_field_data AS a, econ_data AS b
      SET a.reserve_start=b.reserve_start, a.total_recov_mmboe=ROUND(b.total_recov/1000000,2)
      WHERE a.asset_id=b.asset_id AND a.asset_relation='Parent'
      AND b.run_id=(SELECT run_id FROM global_variables WHERE id=1);
    '''
    if debug: print sql_update_2
    curr.execute(sql_update_2)
    gd.commit(curr)

    # -----------------------------------------------------------------------------------------------------------------------------
    sql_update_3 = \
    '''
    UPDATE basin_field_data AS a,
      (SELECT asset_id, ROUND(reserve_volume/1000000,2) AS total_reserves FROM reserves 
      WHERE NOT asset_id IN (SELECT DISTINCT asset_id FROM econ_data WHERE run_id=(SELECT run_id FROM global_variables WHERE id=1))
      AND reserve_type='Recoverable' AND casetype='Base Case' AND commodity='Crude Oil & Natural Gas' ) AS b
      SET a.total_recov_mmboe=b.total_reserves WHERE a.asset_id=b.asset_id AND a.asset_relation='Parent' AND a.total_recov_mmboe IS NULL;
    '''
    if debug: print sql_update_3
    curr.execute(sql_update_3)
    gd.commit(curr)

    # -----------------------------------------------------------------------------------------------------------------------------
    sql_update_4 = \
    '''
    UPDATE basin_field_data AS a, assets AS b
      SET a.reserve_start=CONVERT(SUBSTR(b.discovery_date,1,4),SIGNED) WHERE a.asset_relation='Child' AND NOT b.discovery_date='NULL' AND a.asset_id=b.asset_id
    '''
    if debug: print sql_update_4
    curr.execute(sql_update_4)
    gd.commit(curr)

    # -----------------------------------------------------------------------------------------------------------------------------
    sql_update_5 = \
    '''
    UPDATE basin_field_data AS a, assets AS b
      SET a.reserve_start=CONVERT(SUBSTR(b.discovery_date,1,4),SIGNED) WHERE a.asset_relation='Parent' AND a.reserve_start IS NULL AND NOT b.discovery_date='NULL' AND a.asset_id=b.asset_id
    '''
    if debug: print sql_update_5
    curr.execute(sql_update_5)
    gd.commit(curr)

    # -----------------------------------------------------------------------------------------------------------------------------
    sql_update_6 = \
    '''
    UPDATE basin_field_data AS a,
      (SELECT asset_id, reserve_start FROM basin_field_data WHERE asset_relation='Parent') AS b
      SET a.reserve_start=b.reserve_start WHERE a.reserve_start IS NULL AND a.asset_relation='Child' AND a.parent_asset_id=b.asset_id
    '''
    if debug: print sql_update_6
    curr.execute(sql_update_6)
    gd.commit(curr)


def update_child_fields(curr, debug=False):
    parent_field_data = gd.get_data('asset_id, total_recov_mmboe', 'basin_field_data', sql_where='asset_relation="Parent" AND child_field_count > 1 AND NOT total_recov_mmboe IS NULL', cursor=curr, datatype='plural')
    sql_update = 'UPDATE basin_field_data SET total_recov_mmboe={} WHERE parent_asset_id={} AND asset_id={}'
    for parent_field, total_reserves in parent_field_data:
        child_fields = gd.get_data('asset_id', 'basin_field_data', sql_where='parent_asset_id={}'.format(parent_field), datatype='int')
        child_count = len(child_fields)
        child_reserve_portion = round(float(total_reserves)/float(child_count),3)
        for child_field in child_fields:
            if debug: print sql_update.format(child_reserve_portion, parent_field, child_field)
            curr.execute(sql_update.format(child_reserve_portion, parent_field, child_field))
            gd.commit(curr)


def update_avg_field_reserves(curr, debug=False):
    basin_list = gd.get_data('basin_name', 'basin_data', sql_where='NOT total_recov IS NULL AND field_count > 0')
    for basin in basin_list:
        print 'Determining median field size for {}'.format(basin)
        median_field_size = 0
        field_sizes = gd.get_data('(total_recov_mmboe*1000000)', 'basin_field_data', sql_where='basin="{}" AND NOT total_recov_mmboe IS NULL'.format(basin), cursor=curr, datatype='float', distinct=False)
        if debug: print 'field_sizes: {}'.format(field_sizes)
        if len(field_sizes):
            median_field_size = gd.get_median(field_sizes)
        if debug: print 'UPDATE basin_data SET avg_field_reserves={} WHERE basin_name="{}"'.format(median_field_size, basin)
        curr.execute('UPDATE basin_data SET avg_field_reserves={} WHERE basin_name="{}"'.format(median_field_size, basin))
        gd.commit(curr)


def identify_mature_basins(curr, debug=False):
    sql_update_1 = \
        '''
        UPDATE basin_data SET remaining_reserve_pct=IFNULL(remaining_reserve_pct,0);
        '''
    curr.execute(sql_update_1)
    gd.commit(curr)
    sql_update_2 = \
        '''
        UPDATE basin_data SET is_mature_basin=IFNULL(is_mature_basin,0);
    	'''
    curr.execute(sql_update_2)
    gd.commit(curr)
    
    sql_update = 'UPDATE basin_data SET is_mature_basin={}, low_remaining_reserves={}, has_abandoned_fields={} WHERE basin_name="{}"'
    basin_list = gd.get_data('basin_name', 'basin_data', cursor=curr, sql_where='1=1', debug=True)
    for basin in basin_list:
        low_remaining_reserves = False
        has_abandoned_fields = False
        is_mature_basin = False
        low_remaining_reserves = remaining_reserves_check(curr, basin, debug=debug)
        has_abandoned_fields   = abandoned_field_check(curr, basin, debug=debug)
        if low_remaining_reserves and has_abandoned_fields:
            is_mature_basin = True
        if debug: print sql_update.format(int(is_mature_basin), int(low_remaining_reserves), int(has_abandoned_fields), basin)
        curr.execute(sql_update.format(int(is_mature_basin), int(low_remaining_reserves), int(has_abandoned_fields), basin))
        gd.commit(curr)


def update_country_reserves_forecast(curr, debug=False):
    curr.execute('TRUNCATE TABLE country_reserves_forecast')
    gd.commit(curr)
    sql_insert = 'INSERT INTO country_reserves_forecast (basin, country, terrain, resource_type, period, proj_reserves_boe) VALUES ("{}", "{}", "{}", "{}", {}, {})'
    country_data = gd.get_data('basin, country, terrain, resource_type, reserve_pct', 'basin_country_data', cursor=curr, datatype='plural', sql_where='reserve_pct > 0 AND (NOT basin="NULL")')
    for basin, country, terrain, resource_type, reserve_pct in country_data:
        country_reserves_data = gd.get_data('period, country_reserves_boe', 'reserves_forecast', cursor=curr, sql_where='NOT country_reserves_boe IS NULL AND basin="{}"'.format(basin), datatype='plural', debug=debug)
        if debug: print 'basin: {} -- country: {} -- terrain: {} -- resource_type: {} -- reserve_pct: {} -- len(country_reserves_data): {}'.format(basin, country, terrain, resource_type, reserve_pct, len(country_reserves_data))
        for period, country_reserves_boe in country_reserves_data:
            proj_reserves_boe = round(float(country_reserves_boe)*float(reserve_pct), 6)
            print 'basin: {} -- country: {} -- terrain: {} -- resource_type: {} -- period: {} -- proj_reserves_boe: {}'.format(basin, country, terrain, resource_type, period, proj_reserves_boe)
            if debug: print sql_insert.format(basin, country, terrain, resource_type, period, proj_reserves_boe)
            curr.execute(sql_insert.format(basin, country, terrain, resource_type, period, proj_reserves_boe))
            gd.commit(curr)


def update_assets_table(curr, debug=False):
    sql_insert = \
        '''
		INSERT INTO assets (asset_id,       asset_name, country, constituent, region,      status, terrain, basin, resource_type, prod_phase, recover_factor, assoc_asset_id, assoc_asset_name, assoc_region, assoc_country, assoc_area, trap_type, api_gravity, sulfer, lic_no, county, calorific, hsulfer,   gor, ablock, ablock_region, ablock_country, ablock_constituent, asset_relation,   irr, payback_years, capex,  opex, reserve_status,   npv, bc_npv, lc_npv, hc_npv, facility_type, formation, water_depth, discovery_date, license_num, license_effective, license_expire, porosity, permeability, measured_depth, carbon_dioxide, form_rock_type, data_source, fiscal_regime,           last_update, add_by,             add_date, edit_by,            edit_date)
		VALUES             (      {},"undiscovered-{}",    "{}",      "NULL",   "{}","Discovered",    "{}",  "{}",          "{}",     "NULL",         "NULL",         "NULL",           "NULL",       "NULL",        "NULL",     "NULL",    "NULL",      "NULL", "NULL", "NULL", "NULL",    "NULL",  "NULL","NULL", "NULL",        "NULL",         "NULL",             "NULL",       "Parent","NULL",        "NULL","NULL","NULL",         "NULL","NULL", "NULL", "NULL", "NULL",        "NULL",    "NULL",      "NULL",         "NULL",      "NULL",            "NULL",         "NULL",   "NULL",       "NULL",         "NULL",         "NULL",         "NULL",    "Engine",        "NULL", "2019-08-19 00:00:00","Titan","2019-08-19 18:17:00", "Titan","2019-08-19 18:17:00")
		'''
    basin_asset_data = gd.get_data('asset_id, id, country, region, terrain, basin, resource_type', 'basin_country_data',
                                   datatype='plural', cursor=curr)
    for asset_id, basin_country_id, country, region, terrain, basin, resource_type in basin_asset_data:
        if debug: print sql_insert.format(asset_id, basin_country_id, country, region, terrain, basin, resource_type)
        curr.execute(sql_insert.format(asset_id, basin_country_id, country, region, terrain, basin, resource_type))
        gd.commit(curr)
    sql_update_1 = \
        """
		INSERT INTO asset_data (asset_id, asset_name, country, constituent, region, `status`, terrain, basin, ablock, formation, form_rock_type, trap_type, facility_type, discovery_date, hsulfer, sulfer, calorific, api_gravity, carbon_dioxide, resource_type)
		  (SELECT DISTINCT asset_id, asset_name, country, constituent, region, `status`, terrain, basin, ablock, formation, form_rock_type, trap_type, facility_type, discovery_date, hsulfer, sulfer, calorific, api_gravity, carbon_dioxide, resource_type
		   FROM assets WHERE asset_id>=9000001);
		"""
    sql_update_2 = "UPDATE asset_data SET avg_recov_factor=1.0, prod_adjust_count=0, asset_relation='Parent', data_source='Engine' WHERE asset_id >= 9000001;"
    sql_update_3 = "UPDATE asset_data AS a, basin_country_data AS b SET a.reserve_volume=b.avg_field_reserves WHERE a.asset_id=b.asset_id AND a.asset_id >= 9000001;"
    
    sql_update_4 = \
        '''
        UPDATE asset_data AS a, (SELECT DISTINCT basin, country, region, terrain, resource_type, operator FROM asset_data WHERE operator IS NOT NULL) AS b
          SET a.operator=b.operator WHERE a.basin=b.basin AND a.country=b.country AND a.region=b.region AND a.terrain=b.terrain AND a.resource_type=b.resource_type AND a.operator IS NULL;
        '''
    sql_update_5 = \
        '''
		UPDATE asset_data AS a, (SELECT DISTINCT basin, country, region, terrain, operator FROM asset_data WHERE operator IS NOT NULL) AS b
		  SET a.operator=b.operator WHERE a.basin=b.basin AND a.country=b.country AND a.region=b.region AND a.terrain=b.terrain AND a.operator IS NULL;
		'''
    sql_update_6 = \
        '''
        UPDATE asset_data AS a, (SELECT DISTINCT basin, country, region, operator FROM asset_data WHERE operator IS NOT NULL) AS b
          SET a.operator=b.operator WHERE a.basin=b.basin AND a.country=b.country AND a.region=b.region AND a.operator IS NULL;
		'''
    sql_update_7 = \
        '''
        UPDATE asset_data AS a, (SELECT DISTINCT country, operator FROM asset_data WHERE operator IS NOT NULL) AS b
         SET a.operator=b.operator WHERE a.country=b.country AND a.operator IS NULL;
		'''
    sql_update_8 = \
        '''
	    INSERT INTO operators (asset_id, operator) (SELECT DISTINCT asset_id, operator FROM asset_data WHERE asset_id>=9000001);
		'''
		
    print sql_update_1
    curr.execute(sql_update_1)
    gd.commit(curr)
    print sql_update_2
    curr.execute(sql_update_2)
    gd.commit(curr)
    print sql_update_3
    curr.execute(sql_update_3)
    gd.commit(curr)
    print sql_update_4
    curr.execute(sql_update_4)
    gd.commit(curr)
    print sql_update_5
    curr.execute(sql_update_5)
    gd.commit(curr)
    print sql_update_6
    curr.execute(sql_update_6)
    gd.commit(curr)
    print sql_update_7
    curr.execute(sql_update_7)
    gd.commit(curr)
    print sql_update_8
    curr.execute(sql_update_8)
    
    gd.commit(curr)
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_basin_data(curr, basins=[], config_str='', runid='', mature_basins=False, with_disc=False, debug=False):
    run_id = gd.get_run_id()
    if runid: run_id = runid
    if mature_basins:
        sql_update_ = \
            '''
			INSERT INTO reserves_forecast (basin, period, reserve_type, hist_reserves_mmboe, run_id)
			 (SELECT b.basin, a.prod_year, "Recoverable", ROUND(SUM(b.total_recov_mmboe),2), "{}"
				FROM (SELECT id-(SELECT MIN(id) FROM econ_data) AS prod_year FROM econ_data WHERE (id-(SELECT MIN(id) FROM econ_data)) BETWEEN 2000 AND 2020 ORDER BY prod_year) AS a,
					  basin_field_data AS b
				WHERE b.total_recov_mmboe > 0
				AND b.basin='Arkoma Basin'
				AND b.reserve_start <= a.prod_year
				GROUP BY a.prod_year);
			'''
        curr.execute(sql_update_.format(runid))
        gd.commit(curr)
    
    discount_year = gd.get_discount_year()
    sql_where = 'run_id="{}" AND '
    if basins:
        basin_names = ','.join('"{}"'.format(basin) for basin in basins)
        sql_where += 'basin IN ({}) AND '.format(basin_names)
    if not with_disc:
        sql_where += 'NOT `status`="Discovered" AND '
    sql_where += 'LENGTH(basin) > 0 AND reserve_start <= {} GROUP BY basin'
    basin_reserve_years = gd.get_data('MIN(reserve_start), basin', 'econ_data',
                                      sql_where=sql_where.format(run_id, discount_year), datatype='plural', debug=debug)
    if debug: print 'basin_reserve_years: {}'.format(basin_reserve_years)
    sql_insert_zero_val = 'INSERT INTO reserves_forecast (basin, period, reserve_type, hist_reserves_mmboe, run_id) VALUES ("{}", {}, "Recoverable", 0, "{}")'
    sql_insert = \
        '''
		INSERT INTO reserves_forecast (basin, period, reserve_type, hist_reserves_mmboe, run_id)
		  (SELECT b.basin, a.prod_year, "Recoverable", ROUND(SUM(b.total_recov_mmboe),2), %s FROM
		  (SELECT id-(SELECT MIN(id) FROM econ_data) AS prod_year FROM econ_data WHERE (id-(SELECT MIN(id) FROM econ_data)) BETWEEN %s AND %s ORDER BY prod_year) AS a,
		  basin_field_data AS b
		  WHERE b.total_recov_mmboe > 0 AND b.basin=%s AND b.reserve_start <= a.prod_year GROUP BY a.prod_year ORDER BY a.prod_year)
		'''
    sql_update = 'UPDATE reserves_forecast SET proj_reserves_mmboe=%s, a_value=%s, b_value=%s, c_value=%s WHERE basin=%s AND period=%s AND run_id=%s'
    for first_disc, basin in basin_reserve_years:
        if first_disc < discount_year:
            if debug: print sql_insert_zero_val.format(basin, first_disc-1, run_id)
            curr.execute(sql_insert_zero_val.format(basin, first_disc-1, run_id))
            gd.commit(curr)
            if debug: print sql_insert % (run_id, first_disc, discount_year, basin)
            curr.execute(sql_insert, (run_id, first_disc, discount_year, basin))
            gd.commit(curr)
            basin_data = gd.get_data('hist_reserves_mmboe', 'reserves_forecast', sql_where='basin="{}" AND period < {} ORDER BY period'.format(basin, discount_year), datatype='float', distinct=False, debug=debug)
            y_values = [float(reserve_val) for reserve_val in basin_data]
            x_values = range(1, len(y_values) + 1)
            print basin
            if not mature_basins:
                max_reserves = gd.get_data('max_reserves', 'basin_data', sql_where='basin_name="{}"'.format(basin), single_value=True, cursor=curr, datatype='float', debug=debug)
                if max_reserves < (2 * y_values[-1]):
                    max_reserves = 2 * y_values[-1]
                    if debug:
                        print 'UPDATE basin_data SET max_reserves={} WHERE basin_name="{}"'.format(max_reserves, basin)
                    curr.execute('UPDATE basin_data SET max_reserves={} WHERE basin_name="{}"'.format(max_reserves, basin))
                    gd.commit(curr)
                params, fit_curve = find_curve_fit(x_values=x_values, y_values=y_values, start_year=(first_disc-1), max_reserve_limit=max_reserves, opt_config=config_str, debug=debug)
            else:
                params, fit_curve = find_curve_fit(x_values=x_values, y_values=y_values, start_year=(first_disc-1), opt_config=config_str, debug=debug)
            param_vals = [round(float(param_val),4) for param_val in params]
            print basin, param_vals, '\n'
            a_value, b_value, c_value = param_vals
            for year_num in sorted(fit_curve.keys()):
                if ((first_disc-1)+int(year_num)) <= discount_year:
                    if debug: print sql_update % (round(float(fit_curve[year_num]),2), a_value, b_value, c_value, basin, (first_disc-1) + int(year_num), run_id)
                    curr.execute(sql_update, (round(float(fit_curve[year_num]),2), a_value, b_value, c_value, basin, (first_disc-1) + int(year_num), run_id))
                else:
                    sql_insert_ = 'INSERT INTO reserves_forecast (basin, period, reserve_type, proj_reserves_mmboe, a_value, b_value, c_value, run_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
                    if debug: print sql_insert_ % (basin, (first_disc-1)+int(year_num), "Recoverable", round(float(fit_curve[year_num]),2), a_value, b_value, c_value, run_id)
                    curr.execute(sql_insert_, (basin, (first_disc-1)+int(year_num), "Recoverable", round(float(fit_curve[year_num]),2), a_value, b_value, c_value, run_id))
                gd.commit(curr)
    if debug: print 'UPDATE reserves_forecast AS a, basin_data AS b SET a.basin_id=b.basin_id WHERE a.basin=b.basin_name'
    curr.execute('UPDATE reserves_forecast AS a, basin_data AS b SET a.basin_id=b.basin_id WHERE a.basin=b.basin_name')
    gd.commit(curr)
    if debug: print 'UPDATE basin_data AS a, reserves_forecast AS b SET a.a_value=b.a_value, a.b_value=b.b_value, a.c_value=b.c_value WHERE a.basin_name=b.basin AND b.hist_reserves_mmboe IS NULL'
    curr.execute('UPDATE basin_data AS a, reserves_forecast AS b SET a.a_value=b.a_value, a.b_value=b.b_value, a.c_value=b.c_value WHERE a.basin_name=b.basin AND b.hist_reserves_mmboe IS NULL')
    gd.commit(curr)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_post_macro_data(curr, debug=False):
    curr.execute("UPDATE supply_breakeven_data SET pre_fid=0")
    gd.commit(curr)
    curr.execute("UPDATE supply_breakeven_data SET pre_fid=1 WHERE asset_status IN ('Discovered', 'Announced', 'Stalled')")
    gd.commit(curr)
    curr.execute("UPDATE supply_breakeven_data SET 2020_phase=1")
    gd.commit(curr)
    curr.execute("UPDATE supply_breakeven_data SET lower_48='FALSE'")
    gd.commit(curr)
    curr.execute("UPDATE supply_breakeven_data SET lower_48='TRUE' WHERE country='United States' AND (NOT constituent IN ('Alaska', 'Central Planning Area', 'Western Planning Area'))")
    gd.commit(curr)
    curr.execute("UPDATE supply_breakeven_data SET fob_lng='TRUE' WHERE lng_bm IN ('EALNG', 'ALGLNGEXP', 'SANDSLNG', 'MALLNG', 'INDONLNG', 'NORLNG', 'LNGRUS', 'QATLNG', 'AUSLNG')")
    gd.commit(curr)
    curr.execute("")
    gd.commit(curr)
    curr.execute("")
    gd.commit(curr)
    curr.execute("")
    gd.commit(curr)
    curr.execute("")
    gd.commit(curr)
    curr.execute("")
    gd.commit(curr)
    curr.execute("")
    gd.commit(curr)
    curr.execute("")
    gd.commit(curr)
    curr.execute("")
    gd.commit(curr)
    curr.execute("")
    gd.commit(curr)


def calc_analogue_data():
    print 'Calculating analogue data ...'
    
    #update_asset_data_table(option_list=['all'], debug=False)
    conn = gd.get_connection()
    curr = conn.cursor()
    if 0:
        sql_update_1 = \
            '''
            UPDATE reserve_volumes AS a, (SELECT DISTINCT asset_id, reserve_type, SUM(boe_reserves) AS type_reserves FROM reserve_volumes GROUP BY asset_id, reserve_type) AS b
              SET a.reserve_pct=ROUND(b.type_reserves/a.boe_total,4)
              WHERE a.asset_id=b.asset_id AND a.reserve_type=b.reserve_type AND a.asset_id > 9000000;
            '''
        sql_update_2 = \
            '''
            UPDATE asset_data SET crude_reserve_pct=0, ng_reserve_pct=0, condensate_reserve_pct=0, ngl_reserve_pct=0, lng_reserve_pct=0 WHERE IFNULL(in_place_volume,0) = 0 AND IFNULL(recov_volume,0) > 0 AND asset_id > 9000000;
            '''
        sql_update_7 = \
        '''
            UPDATE asset_data AS a, reserve_volumes AS b
              SET a.crude_reserve_pct=b.reserve_pct
              WHERE a.asset_id=b.asset_id AND b.commodity='Crude Oil' AND a.recov_vol_type=b.reserve_type AND a.asset_id > 9000000;
        '''
        sql_update_3 = \
            '''
            UPDATE asset_data AS a, reserve_volumes AS b
              SET a.ng_reserve_pct=b.reserve_pct
              WHERE a.asset_id=b.asset_id AND b.commodity='Natural Gas' AND a.recov_vol_type=b.reserve_type AND a.asset_id > 9000000;
            '''
        sql_update_4 = \
            '''
            UPDATE asset_data AS a, reserve_volumes AS b
              SET a.condensate_reserve_pct=b.reserve_pct
              WHERE a.asset_id=b.asset_id AND b.commodity='Condensate' AND a.recov_vol_type=b.reserve_type AND a.asset_id > 9000000;
            '''
        sql_update_5 = \
            '''
            UPDATE asset_data AS a, reserve_volumes AS b
              SET a.ngl_reserve_pct=b.reserve_pct
              WHERE a.asset_id=b.asset_id AND b.commodity='NGL' AND a.recov_vol_type=b.reserve_type AND a.asset_id > 9000000;
            '''
        sql_update_6 = \
            '''
            UPDATE asset_data AS a, reserve_volumes AS b
              SET a.lng_reserve_pct=b.reserve_pct
              WHERE a.asset_id=b.asset_id AND b.commodity='LNG' AND a.recov_vol_type=b.reserve_type AND a.asset_id > 9000000;
            '''
        curr.execute(sql_update_1)
        gd.commit(curr)
        curr.execute(sql_update_2)
        gd.commit(curr)
        curr.execute(sql_update_3)
        gd.commit(curr)
        curr.execute(sql_update_4)
        gd.commit(curr)
        curr.execute(sql_update_5)
        gd.commit(curr)
        curr.execute(sql_update_6)
        gd.commit(curr)
        curr.execute(sql_update_7)
        gd.commit(curr)
        
        curr.close()
        conn.close()
    
    analogue_main(undiscovered=True, undisc_calc=True, undisc_prod=True)

def update_avg_country_reserves(curr, debug=False):
    sql_update = 'UPDATE basin_country_data SET avg_field_reserves={} WHERE basin="{}" AND terrain="{}" AND resource_type="{}"'
    basin_country_data = gd.get_data('basin, terrain, resource_type', 'basin_country_data', cursor=curr, datatype='plural', sql_where='IFNULL(total_reserves_boe,0)>0')
    for basin, terrain, resource_type in basin_country_data:
        avg_field_reserves = 0
        sql_where = 'IFNULL(total_recov_mmboe,0) > 0 AND basin="{}" AND terrain="{}" AND resource_type="{}"'.format(basin, terrain, resource_type)
        basin_field_data = gd.get_data('total_recov_mmboe*1000000', 'basin_field_data', cursor=curr, sql_where=sql_where, datatype='float', distinct=False)
        if len(basin_field_data) > 0:
            avg_field_reserves = gd.get_median(basin_field_data)
        if debug: print sql_update.format(avg_field_reserves, basin, terrain, resource_type)
        curr.execute(sql_update.format(avg_field_reserves, basin, terrain, resource_type))
        gd.commit(curr)

def update_econ_data(regions=['North_America'], debug=False):
    for region in regions:
        os.system(gd.DATA_TASK_DIR + 'EconData_{}_.bat'.format(region.replace(' ', '_')))

def pre_modeling_update(debug=False):
    # Ensure econ_data extraction has already been run before executeing the following updates
    print 'Pre-modeling update ...'
    conn = gd.get_connection()
    curr = conn.cursor()
    
    sql_update_1 = \
        '''
    UPDATE basin_field_data AS a, econ_data AS b
      SET a.reserve_start=b.reserve_start, a.total_recov_mmboe=ROUND(b.total_recov/1000000,2)
      WHERE a.asset_id=b.asset_id AND a.asset_relation='Parent'
      AND b.run_id=(SELECT run_id FROM global_variables WHERE id=1);
        '''
    sql_update_2 = \
        '''
    UPDATE basin_field_data AS a, assets AS b
      SET a.country=b.country, a.region=b.region, a.asset_status=b.`status`, a.terrain=b.terrain, a.resource_type=b.resource_type, a.formation=b.formation
      WHERE a.asset_id=b.asset_id;
        '''
    sql_update_3 = \
        '''
    UPDATE basin_field_data SET formation=NULL WHERE formation='NULL';
        '''
    sql_update_4 = \
        '''
    UPDATE basin_field_data SET child_field_count=0 WHERE child_field_count IS NULL;
        '''
    sql_update_5 = \
        '''
    UPDATE basin_data AS a,
       (SELECT DISTINCT basin, COUNT(DISTINCT country) AS country_count FROM basin_country_data GROUP BY basin) AS b
        SET a.country_count=b.country_count WHERE a.basin_name=b.basin;
        '''
    sql_update_6 = \
        '''
        UPDATE basin_country_data SET avg_field_reserves=0;
        '''
    sql_update_7 = \
    '''
    UPDATE asset_data AS a, basin_country_data AS b SET a.reserve_volume=b.avg_field_reserves WHERE a.asset_id=b.asset_id AND a.asset_id >= 9000001
    '''
    curr.execute(sql_update_1)
    gd.commit(curr)
    curr.execute(sql_update_2)
    gd.commit(curr)
    curr.execute(sql_update_3)
    gd.commit(curr)
    curr.execute(sql_update_4)
    gd.commit(curr)
    curr.execute(sql_update_5)
    gd.commit(curr)
    curr.execute(sql_update_6)
    gd.commit(curr)
    update_avg_country_reserves(curr, debug=debug)

    curr.execute('''UPDATE basin_country_data SET total_reserves_mmboe=0;''')
    gd.commit(curr)

    curr.execute('''UPDATE basin_country_data SET total_reserves_boe=0;''')
    gd.commit(curr)

    curr.execute('''UPDATE basin_country_data AS a,
    	            (SELECT DISTINCT country, terrain, resource_type, basin, ROUND(SUM(total_recov_mmboe), 6) AS total_reserves_mmboe FROM basin_field_data GROUP BY country, terrain, resource_type, basin) AS b
                    SET a.total_reserves_mmboe=b.total_reserves_mmboe
                    WHERE a.country=b.country AND a.terrain=b.terrain AND a.resource_type=b.resource_type AND a.basin=b.basin;''')
    gd.commit(curr)

    curr.execute('''UPDATE basin_country_data SET total_reserves_mmboe=0 WHERE total_reserves_mmboe IS NULL;''')
    gd.commit(curr)

    curr.execute('''UPDATE basin_country_data SET total_reserves_boe=ROUND(total_reserves_mmboe*1000000,5);''')
    gd.commit(curr)

    curr.execute('''UPDATE basin_country_data SET reserve_pct=0;''')
    gd.commit(curr)

    curr.execute('''UPDATE basin_country_data AS a,
                    (SELECT DISTINCT basin, SUM(total_reserves_boe) AS basin_reserves FROM basin_country_data GROUP BY basin) AS b
                     SET a.reserve_pct=ROUND(a.total_reserves_boe/b.basin_reserves,7)
                     WHERE a.basin=b.basin AND b.basin_reserves > 0;''')
    gd.commit(curr)

    curr.execute('''UPDATE basin_country_data SET avg_field_reserves=0 WHERE total_reserves_boe=0;''')
    gd.commit(curr)

    curr.execute('''UPDATE country_reserves_forecast AS a,
                    reserves_forecast AS b,
                    basin_country_data AS c
                    SET proj_reserves_boe=ROUND(b.proj_reserves_mmboe*1000000*c.reserve_pct,2)
                    WHERE a.basin=b.basin AND c.basin=b.basin AND a.asset_id=c.asset_id AND a.period=b.period;''')
    gd.commit(curr)

    curr.execute('''UPDATE country_reserves_forecast AS a, country_reserves_forecast AS b,
    	            (SELECT DISTINCT asset_id, MIN(period) AS prod_start_year FROM country_reserves_forecast GROUP BY asset_id) AS c
                     SET a.proj_reserves_boe=IF((a.proj_reserves_boe-b.proj_reserves_boe)>=0, a.proj_reserves_boe-b.proj_reserves_boe,0) WHERE a.asset_id=b.asset_id AND a.asset_id=c.asset_id AND a.period!=c.prod_start_year AND a.period=b.period+1;''')
    gd.commit(curr)

    curr.execute('''UPDATE country_reserves_forecast AS a,
                    reserves_forecast AS b,
                    reserves_forecast AS c,
                    basin_country_data AS d,
                    (SELECT DISTINCT asset_id, MIN(period) AS prod_start_year FROM country_reserves_forecast GROUP BY asset_id) AS e
                     SET a.proj_reserves_boe=ROUND(IF((b.proj_reserves_mmboe-c.proj_reserves_mmboe)>=0,b.proj_reserves_mmboe-c.proj_reserves_mmboe,0)*1000000*d.reserve_pct,2)
                     WHERE a.basin=b.basin AND a.basin=c.basin AND a.basin=d.basin AND a.asset_id=e.asset_id AND a.asset_id=d.asset_id AND a.period=b.period
                     AND b.period=c.period+1 AND b.period=e.prod_start_year;''')
    gd.commit(curr)

    curr.execute(sql_update_7)
    gd.commit(curr)
    curr.close()
    conn.close()

def create_undisc_models():
    os.system('%engine_drive%:\\GlobalData\\Tasks\\DiscoveredFieldTasks\\5_RunDiscFieldModel2.bat')

def run_supply_curve_macro():
    for region in gd.REGION_NAMES:
        print 'Moving {} files to breakeven hold folder ...'.format(region)
        for model in os.listdir(gd.BE_REGIONS + '{}\\'.format(region)):
            if os.path.isfile(gd.BE_REGIONS + '{}\\{}'.format(region, model)):
                shutil.move(gd.BE_REGIONS + '{}\\{}'.format(region, model),
                            gd.BREAKEVEN_DIR + 'BreakevenHold\\{}\\{}'.format(region, model))
        print 'Moving {} files to breakeven hold folder ...'.format(region)
        if region not in ['North_America_1', 'North_America_2', 'Unconventional']:
            for model in os.listdir(gd.REGIONS_DIR + 'Discovered\\{}\\'.format(region)):
                if os.path.isfile(gd.REGIONS_DIR + 'Discovered\\{}\\{}'.format(region, model)) and int(
                        model.split('_')[1]) >= 9000000:
                    shutil.move(gd.REGIONS_DIR + 'Discovered\\{}\\{}'.format(region, model),
                                gd.BE_REGIONS + '{}\\{}'.format(region, model))
    os.system("%engine_drive%:\\GlobalData\\Tasks\\EngineTasks\\Disc_Supply_Curve_Breakevens.bat")

def calc_supply_curve_data():
    os.system("%engine_drive%:\\GlobalData\\Tasks\\EngineTasks\\Process_Supply_Curve_Data.bat")


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main(basins=[], config_str='', update_basin_data_table=False, update_analogs=False, update_reserves=False,
         clear_data=False, forecast_basins=False, mature_basins=False, with_disc=False, country_reserves=False,
         update_assets=False, debug=False):
    conn = gd.get_connection()
    curr = conn.cursor()
    
    if update_basin_data_table:
        update_basin_data(curr, with_disc=with_disc, debug=debug)
    
    if update_analogs:
        update_analog_basins(curr, debug=debug)
    
    if update_reserves:
        print 'Updating reserve_start in econ_data table ...'
        update_reserve_start(curr)
    
    if clear_data:
        print 'Clearing data in reserves_forecast table ...'
        curr.execute('TRUNCATE TABLE reserves_forecast')
        gd.commit(curr)
    
    if forecast_basins:
        print 'Forecasting basin reserves ...'
        get_basin_data(curr, basins=basins, config_str=config_str, mature_basins=mature_basins, with_disc=with_disc,
                       debug=debug)
    if country_reserves:
        print 'Forecasting country reserves ...'
        update_country_reserves_forecast(curr, debug=debug)
    
    if update_assets:
        print 'Updating asset data table ...'
        update_assets_table(curr, debug=debug)
    
    curr.close()
    conn.close()


def calc_undiscovered_reserves(step_0=False, step_1=False, step_2=False, step_3=False, step_4=False, step_5=False,
                               step_6=False, step_7=False, step_8=False, step_9=False, step_10=False, debug=False):
    if step_0:
        update_asset_data_table(option_list=['param_track', 'reserves'], debug=False)
    
    if step_1:
        main(update_basin_data_table=True, with_disc=True, debug=debug)
    
    if step_2:
        mature_basins = gd.get_data('basin_name', 'basin_data', sql_where='is_mature_basin=1 AND field_count >= 1')
        main(basins=mature_basins, update_reserves=True, config_str='abcx', clear_data=True, forecast_basins=True,
             mature_basins=True, with_disc=True, debug=debug)
    
    if step_3:
        main(update_analogs=True, debug=debug)
    
    if step_4:
        basin_list = gd.get_data('basin_name', 'basin_data',
                                 sql_where='is_mature_basin=0 AND (NOT max_reserves IS NULL) AND total_recov_rem > 0 AND field_count >= 1')
        main(basins=basin_list, update_reserves=True, config_str='abcx', clear_data=False, forecast_basins=True,
             mature_basins=False, with_disc=True, debug=debug)
    
    if step_5:
        main(country_reserves=False, update_assets=True, debug=debug)
    
    if step_6:
        pre_modeling_update(debug=debug)
    
    if step_7:
        calc_analogue_data()
    
    if step_8:
        create_undisc_models()
    
    if step_9:
        run_supply_curve_macro()
    
    if step_10:
        calc_supply_curve_data()


if __name__ == '__main__':
    calc_undiscovered_reserves(step_0=False, step_1=True, step_2=True, step_3=True, step_4=True, step_5=True, step_6=True, step_7=True, step_8=True, step_9=False, step_10=False, debug=False)
    # calc_undiscovered_reserves(step_9=True, step_10=False, debug=False)
    # calc_undiscovered_reserves(step_9=False, step_10=True, debug=False)
    # ain(update_basin_data_table=True, with_disc=True, basins=['Mumbai Offshore Basin'], debug=True)
    #main(basins=['Mumbai Offshore Basin'], update_reserves=True, config_str='abcx', clear_data=True, forecast_basins=True, mature_basins=True, with_disc=True, debug=True)