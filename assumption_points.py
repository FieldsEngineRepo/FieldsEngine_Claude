from globaldata import *


def update_assumption_points(table):
    conn = get_connection()
    curr = conn.cursor()
    set_to_null(table)
    print 'Updating assumption points ...'
    main_cols = PARAM_LISTS[table]['main']
    main_param_str = get_update_str(main_cols)

    scored_cols = PARAM_LISTS[table]['scored']

    sql_update = 'UPDATE {} SET points=%s WHERE {} '.format(table, main_param_str)

    all_cols = PARAM_LISTS[table]['scored'] + PARAM_LISTS[table]['main']
    param_str = get_param_str(all_cols)
    sql_select = 'SELECT %s FROM %s' % (param_str, table)
    curr.execute(sql_select)
    row_num = 1
    for datarow in curr.fetchall():
        sql_command = sql_update
        params = ()
        main_count = len(main_cols)
        param_vals = ()
        if main_count:
            param_vals = datarow[-main_count:]
        assumption_points = 0
        for i in range(len(scored_cols)):
            param_name = scored_cols[i]
            data_val = datarow[i]
            if data_val is None:
                sql_command += 'AND {} IS NULL '.format(param_name)
            else:
                sql_command += 'AND {}=%s '.format(param_name)
                param_vals += (data_val,)
                if data_val and data_val != 'None':
                    assumption_points += PARAM_POINTS[param_name]
                    if (param_name in ['production_peak', 'production_total']) and (table in ['capex_alloc', 'capex_redev_alloc', 'abandonment_alloc']):
                        assumption_points += 1920
        param_vals = (assumption_points,) + param_vals
        try:
            curr.execute(sql_command, param_vals)
            curr.execute('COMMIT')
        except:
            print sql_select
            print sql_command
            print param_vals
            print sql_command % param_vals
        row_num += 1
    set_to_zero(table)
    curr.close()
    conn.close()

def update_assumption_points(table):
    conn = get_connection()
    curr = conn.cursor()
    set_to_null(table)
    set_to_zero(table)
    main_cols = PARAM_LISTS[table]['main']
    main_param_str = get_update_str(main_cols)

    scored_cols = PARAM_LISTS[table]['scored']

    sql_update = 'UPDATE {} SET points=%s WHERE {} '.format(table, main_param_str)

    all_cols = PARAM_LISTS[table]['scored'] + PARAM_LISTS[table]['main']
    param_str = get_param_str(all_cols)
    sql_select = 'SELECT %s FROM %s' % (param_str, table)
    curr.execute(sql_select)
    row_num = 1
    for datarow in curr.fetchall():
        sql_command = sql_update
        params = ()
        main_count = len(main_cols)
        param_vals = ()
        if main_count:
            param_vals = datarow[-main_count:]
        assumption_points = 0
        for i in range(len(scored_cols)):
            param_name = scored_cols[i]
            data_val = datarow[i]
            if data_val is None:
                sql_command += 'AND {} IS NULL '.format(param_name)
            else:
                sql_command += 'AND {}=%s '.format(param_name)
                param_vals += (data_val,)
                if data_val and data_val != 'None':
                    assumption_points += PARAM_POINTS[param_name]
                    if (param_name in ['production_peak', 'production_total']) and (table in ['capex_alloc', 'capex_redev_alloc', 'abandonment_alloc']):
                        assumption_points += 1920
        param_vals = (assumption_points,) + param_vals
        try:
            curr.execute(sql_command, param_vals)
        except:
            print sql_select
            print sql_command
            print param_vals
            print sql_command % param_vals
        curr.execute('COMMIT')
        row_num += 1
    curr.close()
    conn.close()

if __name__=='__main__':
    for table in PARAM_LISTS.keys():
        update_assumption_points(table)
