import globaldata as gd


ASSUMPTION_PARAMS = {
    'Vertical'  : {
        'Completion cost breakdown': 'Vert_Completion_Cost_pct',
        'Drilling cost breakdown'  : 'Vert_Drilling_Cost_pct',
        'Drilling cost premium'    : 'Vert_Drilling_Cost_Premium_pct',
        'Facilities cost breakdown': 'Vert_Facilities_Cost_pct',
        'Well Cost'                : 'Vert_Well_Cost_usd_ft'
    },

    'Horizontal': {
        'Drilling cost breakdown'  : 'Horiz_Drilling_Cost_pct',
        'Well Cost'                : 'Horiz_Well_Cost_usd_ft'
    }
}

WELL_ASSUM_DATA   = [
    ('Vertical', ['Well Cost',
                  'Facilities cost breakdown',
                  'Drilling cost premium',
                  'Completion cost breakdown',
                  'Drilling cost breakdown']),

    ('Horizontal', ['Well Cost',
                    'Drilling cost breakdown'])
]

def get_well_assumption(curr, operator, resource_play, state_name, well_direction, param_list=[], debug=False):
    resource_play_str = "''"
    operator_str = "''"

    param_values = []

    if operator:
        operator_str = operator

    if resource_play:
        if ';' in resource_play:
            resource_plays = ["'{}'".format(play.strip()) for play in resource_play.split(';')]
            resource_play_str = ', '.join(resource_plays)
        else:
            resource_play_str = "'{}'".format(resource_play)

    for param_name in param_list:
        if debug: print '(get_well_assumption()) -- param_list: {}'.format(param_list)
        param_choice = 0
        sql_where = "Well_Direction='{}' AND (Operator='{}' OR Operator IS NULL) AND (Resource_Play IN ({}) OR Resource_Play IS NULL) AND (State_Name='{}' OR State_Name IS NULL) AND Param_Name='{}' AND ISNULL(Param_Value,0) > 0 "
        if param_name.lower() == 'well cost' and well_direction.lower() == 'vertical':
            sql_where += "AND ISNULL(Well_Cost_usd_ft,0) > 0 "
        sql_where += "ORDER BY Well_Direction DESC, State_Name DESC, Resource_Play DESC, Operator DESC"
        param_data = gd.get_data \
            ('TOP 1 Param_Value, Well_Cost_usd_ft, Well_Direction, State_Name, Resource_Play, Operator', 'tblUSWell_Assumptions', database='US_Wells', server='sql_server', cursor=curr, datatype='plural', single_value=True, sql_where=sql_where.format(well_direction, operator_str, resource_play_str, state_name, param_name), debug=debug)
        if debug: print '(get_well_assumption()) -- param_data: {}'.format(param_data)
        if param_data is not None:
            param_value, well_cost_usd_ft = param_data[:2]
            if param_name.lower == 'well cost':
                if (well_direction.lower() == 'horizontal') and param_value:
                    param_choice = param_value
                elif (well_direction.lower() == 'vertical') and well_cost_usd_ft:
                    param_choice = well_cost_usd_ft
            elif param_value:
                param_choice = param_value
        param_values.append(param_choice)
        if debug: print '(get_well_assumption()) -- param_name: {} -- param_choice: {} -- param_values: {}'.format \
            (param_name, param_choice, param_values)

    if debug: print '(get_well_assumption()) -- ret_val: {}'.format(param_values)
    return param_values


def update_well_cost_data(curr, debug=False):
    sql_update_tbl = \
    """
    UPDATE US_Wells.dbo.tblUSWell_Parameters SET Measured_Depth_ft=ROUND(True_Vertical_Depth_ft,2)
      WHERE ISNULL(Measured_Depth_ft,0)=0 AND ISNULL(True_Vertical_Depth_Ft,0) > 0
      AND Well_Direction='Vertical' AND Forecast_Well IN (4,6);
    
    TRUNCATE TABLE US_Wells.dbo.tblUSWell_Well_Cost_Data;
    
    INSERT INTO US_Wells.dbo.tblUSWell_Well_Cost_Data (Operator, Resource_Play, State_Name)
      (SELECT DISTINCT Operator, Resource_Play, State_Name
       FROM US_Wells.dbo.tblUSWell_Parameters
       WHERE Forecast_Well IN (4,6) AND State_Name IS NOT NULL);
    """
    #sql_update_tbl = \
    #    """
    #    TRUNCATE TABLE US_Wells.dbo.tblUSWell_Well_Cost_Data;
    #
    #    INSERT INTO US_Wells.dbo.tblUSWell_Well_Cost_Data (Operator, Resource_Play, State_Name)
    #      (SELECT DISTINCT Operator, Resource_Play, State_Name
    #       FROM US_Wells.dbo.tblUSWell_Parameters
    #       WHERE State_Name IS NOT NULL);
    #    """
    sql_update = \
    """
    UPDATE US_Wells.dbo.tblUSWell_Well_Cost_Data 
      SET {} 
      WHERE ISNULL(Operator,'')=ISNULL({},'') AND ISNULL(Resource_Play,'')=ISNULL({},'') AND State_Name='{}'
    """

    sql_update_avg_md = \
    """
    UPDATE US_Wells.dbo.tblUSWell_Well_Cost_Data 
      SET Avg_Measured_Depth_ft={} 
      WHERE ISNULL(Operator,'')=ISNULL({},'') AND ISNULL(Resource_Play,'')=ISNULL({},'') AND State_Name='{}'
    """

    curr.execute(sql_update_tbl)
    gd.commit(curr)
    params = 'operator, resource_play, state_name'
    sql_where = "Forecast_Well IN (4,6) AND State_Name IS NOT NULL"
    #sql_where = "State_Name IS NOT NULL"
    well_cost_data = gd.get_data(params, 'tblUSWell_Parameters', cursor=curr, database='US_Wells', server='sql_server', datatype='plural', sql_where=sql_where)
    well_cost_data_count = len(well_cost_data)
    well_cost_data_num = 1
    for operator, resource_play, state_name in well_cost_data:
        state_name = state_name.strip()
        print '{}/{}: {} -- {} -- {}'.format(well_cost_data_num, well_cost_data_count, operator, resource_play, state_name)

        if operator:
            operator_str = "'{}'".format(operator)
        else:
            operator_str = 'NULL'

        if resource_play:
            resource_play_str = "'{}'".format(resource_play)
        else:
            resource_play_str = 'NULL'

        for well_direction, param_list in WELL_ASSUM_DATA:
            param_values = get_well_assumption(curr, operator, resource_play, state_name, well_direction, param_list, debug=debug)
            assert len(param_values) == len(param_list)

            param_str = ','.join(["%s={}" % ASSUMPTION_PARAMS[well_direction][param_name] for param_name in param_list])

            if debug: print sql_update.format(param_str.format(*param_values), operator_str, resource_play_str, state_name)

            curr.execute(sql_update.format(param_str.format(*param_values), operator_str, resource_play_str, state_name))
            gd.commit(curr)

        sql_where = "Well_Direction='Horizontal' AND ISNULL(Measured_Depth_ft,0) > 1000"
        avg_measured_depth = gd.get_data('AVG(Measured_Depth_ft)', 'tblUSWell_Parameters', cursor=curr, single_value=True, datatype='float', sql_where=sql_where, debug=debug)

        if debug: print sql_update_avg_md.format(avg_measured_depth, operator_str, resource_play_str, state_name)

        curr.execute(sql_update_avg_md.format(avg_measured_depth, operator_str, resource_play_str, state_name))
        gd.commit(curr)

        well_cost_data_num += 1


def calc_vertical_well_cost(curr, debug=False):
    print 'Calculating Vertical Well Costs 1 ...'
    sql_update_1 = \
    """
    TRUNCATE TABLE US_Wells.dbo.tblUSWell_Vertical_Well_Cost;

    INSERT INTO US_Wells.dbo.tblUSWell_Vertical_Well_Cost (WellID, API_Number, Operator, Resource_Play, State_Name, True_Vertical_Depth_ft, Measured_Depth_ft, Forecast_Well)
      (SELECT DISTINCT WellID, API_Number, Operator, Resource_Play, State_Name, True_Vertical_Depth_ft, Measured_Depth_ft, Forecast_Well 
       FROM US_Wells.dbo.tblUSWell_Parameters 
       WHERE Forecast_Well IN (4,6) AND State_Name IS NOT NULL);
    """
    curr.execute(sql_update_1)
    gd.commit(curr)

    print 'Calculating Vertical Well Costs 2 ...'
    sql_update_2 = \
    """
    UPDATE US_Wells.dbo.tblUSWell_Vertical_Well_Cost 
      SET Drilling_Cost_pct=b.Vert_Drilling_Cost_pct,
          Completion_Cost_pct=b.Vert_Completion_Cost_pct,
          Facilities_Cost_pct=b.Vert_Facilities_Cost_pct,
          Vert_Drill_Cost_Prem_pct_Assum=b.Vert_Drilling_Cost_Premium_pct,
          Vert_Well_Cost_usd_ft_Assum=b.Vert_Well_Cost_usd_ft,
          Horiz_Well_Cost_Assum=b.Horiz_Well_Cost_usd_ft,
          Horiz_Drill_Cost_pct_Assum=b.Horiz_Drilling_Cost_pct,
          Avg_Measured_Depth_ft=b.Avg_Measured_Depth_ft
      FROM US_Wells.dbo.tblUSWell_Vertical_Well_Cost a, 
           US_Wells.dbo.tblUSWell_Well_Cost_Data b 
      WHERE ISNULL(a.Operator,'')=ISNULL(b.Operator,'') AND ISNULL(a.Resource_Play,'')=ISNULL(b.Resource_Play,'') AND a.State_Name=b.State_Name;
    """
    curr.execute(sql_update_2)
    gd.commit(curr)

    print 'Calculating Vertical Well Costs 3 ...'
    sql_update_3 = \
    """
    UPDATE US_Wells.dbo.tblUSWell_Vertical_Well_Cost SET Horiz_Drill_Cost_Calc = ROUND(Horiz_Well_Cost_Assum * Horiz_Drill_Cost_pct_Assum, 6);
    """
    curr.execute(sql_update_3)
    gd.commit(curr)

    print 'Calculating Vertical Well Costs 4 ...'
    sql_update_4 = \
    """
    UPDATE US_Wells.dbo.tblUSWell_Vertical_Well_Cost SET Vert_Drill_Cost_mm_usd_Calc  = ROUND((True_Vertical_Depth_ft/Avg_Measured_Depth_ft)*Horiz_Drill_Cost_Calc*(1 + Vert_Drill_Cost_Prem_pct_Assum), 3);
    """
    curr.execute(sql_update_4)
    gd.commit(curr)

    print 'Calculating Vertical Well Costs 5 ...'
    sql_update_5 = \
    """
    UPDATE US_Wells.dbo.tblUSWell_Vertical_Well_Cost SET Vert_Well_Cost_mm_usd_Calc=ROUND(Vert_Drill_Cost_mm_usd_Calc/Drilling_Cost_pct,3);
    """
    curr.execute(sql_update_5)
    gd.commit(curr)

    print 'Calculating Vertical Well Costs 6 ...'
    sql_update_6 = \
    """
    UPDATE US_Wells.dbo.tblUSWell_Vertical_Well_Cost SET Vert_Well_Cost_usd_ft_Calc = ROUND((Vert_Well_Cost_mm_usd_Calc*1000000)/Measured_Depth_ft, 3);
    """
    curr.execute(sql_update_6)
    gd.commit(curr)

    print 'Calculating Vertical Well Costs 7 ...'
    sql_update_7 = \
    """
    UPDATE tblUSWell_Parameters SET Well_Cost_usd_ft=b.Vert_Well_Cost_usd_ft_Calc
      FROM tblUSWell_Parameters a, tblUSWell_Vertical_Well_Cost b
      WHERE a.WellID=b.WellID AND a.API_Number=b.API_Number;
    """
    curr.execute(sql_update_7)
    gd.commit(curr)

def update_vertical_well_costs(update_cost_data=False, calc_well_costs=False, debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells')
    curr = conn.cursor()

    total_start = gd.get_datetime()
    print 'start processing:', total_start

    if update_cost_data:
        update_start = gd.get_datetime()
        print '\n\tstart update:', update_start

        update_well_cost_data(curr, debug=debug)

        update_end = gd.get_datetime()
        print '\tend update:', update_end
        print '\ttotal update time:', gd.elapsed_time(update_start, update_end)

    if calc_well_costs:
        calc_start = gd.get_datetime()
        print '\n\tstart calc:', calc_start

        calc_vertical_well_cost(curr, debug=debug)

        calc_end = gd.get_datetime()
        print '\tend calc:', calc_end
        print '\ttotal calc time:', gd.elapsed_time(calc_start, calc_end)

    total_end = gd.get_datetime()
    print '\nend processing:', total_end

    print 'total processing time:', gd.elapsed_time(total_start, total_end)

    curr.close()
    conn.close()


if __name__=='__main__':
    update_vertical_well_costs(update_cost_data=True, calc_well_costs=True, debug=False)

