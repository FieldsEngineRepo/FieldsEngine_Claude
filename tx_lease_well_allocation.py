import globaldata as gd

PROCESS_CODE    = 1

PROD_MONTH_COLS = {
    '01': ('oil_jan_bbl', 'csgd_jan_mcf'),
    '02': ('oil_feb_bbl', 'csgd_feb_mcf'),
    '03': ('oil_mar_bbl', 'csgd_mar_mcf'),
    '04': ('oil_apr_bbl', 'csgd_apr_mcf'),
    '05': ('oil_may_bbl', 'csgd_may_mcf'),
    '06': ('oil_jun_bbl', 'csgd_jun_mcf'),
    '07': ('oil_jul_bbl', 'csgd_jul_mcf'),
    '08': ('oil_aug_bbl', 'csgd_aug_mcf'),
    '09': ('oil_sep_bbl', 'csgd_sep_mcf'),
    '10': ('oil_oct_bbl', 'csgd_oct_mcf'),
    '11': ('oil_nov_bbl', 'csgd_nov_mcf'),
    '12': ('oil_dec_bbl', 'csgd_dec_mcf')
}

MONTH_NUMS      = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
PROD_DATES      = ['{}{}'.format(year_num, month_num) for year_num in range(1900, 2200) for month_num in MONTH_NUMS]

DISTRICT_DATA = {
    '1' : '01',
    '2' : '02',
    '3' : '03',
    '4' : '04',
    '5' : '05',
    '6' : '06',
    '6E': '07',
    '7B': '08',
    '7C': '09',
    '8' : '10',
    '8A': '11',
    '8B': '12',
    '9' : '13',
    '10': '14'
}


PROD_PCT_COLS = [
    'lease_id',
    'tx_well_id',
    'prod_year',
    'jan_prod_pct',
    'feb_prod_pct',
    'mar_prod_pct',
    'apr_prod_pct',
    'may_prod_pct',
    'jun_prod_pct',
    'jul_prod_pct',
    'aug_prod_pct',
    'sep_prod_pct',
    'oct_prod_pct',
    'nov_prod_pct',
    'dec_prod_pct'
]

prod_col_str            = \
'''
oil_total_bbl, gas_total_mcf, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, gas_jan_mcf, gas_feb_mcf, gas_mar_mcf, gas_apr_mcf, gas_may_mcf, gas_jun_mcf, gas_jul_mcf, gas_aug_mcf, gas_sep_mcf, gas_oct_mcf, gas_nov_mcf, gas_dec_mcf
'''

MONTH_NAMES           = {
	'01': 'jan',
	'02': 'feb',
	'03': 'mar',
	'04': 'apr',
	'05': 'may',
	'06': 'jun',
	'07': 'jul',
	'08': 'aug',
	'09': 'sep',
	'10': 'oct',
	'11': 'nov',
	'12': 'dec'
}

COMM_UNITS            = {
    "oil"       : "bbl",
    "gas"       : "mcf"
}

MONTHS = [
    'jan',
    'feb',
    'mar',
    'apr',
    'may',
    'jun',
    'jul',
    'aug',
    'sep',
    'oct',
    'nov',
    'dec'
]

LEASE_UPDATE_DATA = {
    'jan': ('dec', 'feb', 'prod_year - 1', 'prod_year'),
    'feb': ('jan', 'mar', 'prod_year', 'prod_year'),
    'mar': ('feb', 'apr', 'prod_year', 'prod_year'),
    'apr': ('mar', 'may', 'prod_year', 'prod_year'),
    'may': ('apr', 'jun', 'prod_year', 'prod_year'),
    'jun': ('may', 'jul', 'prod_year', 'prod_year'),
    'jul': ('jun', 'aug', 'prod_year', 'prod_year'),
    'aug': ('jul', 'sep', 'prod_year', 'prod_year'),
    'sep': ('aug', 'oct', 'prod_year', 'prod_year'),
    'oct': ('sep', 'nov', 'prod_year', 'prod_year'),
    'nov': ('oct', 'dec', 'prod_year', 'prod_year'),
    'dec': ('nov', 'jan', 'prod_year', 'prod_year + 1')
}


LEASE_UPDATE_DATA = {
    'jan': ('dec', 'feb'),
    'feb': ('jan', 'mar'),
    'mar': ('feb', 'apr'),
    'apr': ('mar', 'may'),
    'may': ('apr', 'jun'),
    'jun': ('may', 'jul'),
    'jul': ('jun', 'aug'),
    'aug': ('jul', 'sep'),
    'sep': ('aug', 'oct'),
    'oct': ('sep', 'nov'),
    'nov': ('oct', 'dec'),
    'dec': ('nov', 'jan')
}

def update_pct_gaps(curr, debug=False):
    start_time = gd.get_datetime()
    sql_update = \
    '''
    UPDATE tx_well_prod_pct SET {}_prod_pct={} WHERE lease_id='{}' AND tx_well_id='{}' AND prod_year={}
    '''
    sql_update_2 = \
    '''
    UPDATE tx_well_prod_pct 
      SET {0}_prod_pct=b.{1}_prod_pct
      FROM tx_well_prod_pct a, tx_well_prod_pct b, tx_lease_prod_pct c
      WHERE c.process_code=1 AND c.{0}_prod_pct=2 
      AND a.lease_id=b.lease_id a.lease_id=c.lease_id 
      AND a.prod_year=b.prod_year AND a.prod_year=c.prod_year AND a.prod_year=b.prod_year
      AND a.tx_well_id=b.tx_well_id
    '''
    sql_update_3 = \
    '''
    UPDATE tx_well_prod_pct
      SET {0}_prod_pct=1.0/a.lease_well_count
      FROM tx_well_prod_pct a, (SELECT DISTINCT lease_id, prod_year FROM tx_lease_prod_pct WHERE {0}_prod_pct=2 AND process_code=1) b
      WHERE a.lease_id=b.lease_id
      AND a.prod_year=b.prod_year
    '''
    sql_lease_update = \
    '''
    UPDATE tx_lease_prod_pct SET {0}_prod_pct=2, process_code=1 FROM tx_lease_prod_pct a, tx_production b 
      WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND a.{0}_prod_pct=0 AND (b.oil_{0}_bbl+b.csgd_{0}_mcf) > 0
    '''
    sql_where_1 = "lease_id='{}' AND prod_year='{}'"
    sql_where_2 = "lease_id='{}' AND prod_year={} AND {}_prod_pct > 1 AND tx_well_id='{}'"
    for month_name in MONTHS:
        print '\nUpdating tx_lease_prod_pct for {}...'.format(month_name)
        #if debug: print sql_lease_update.format(month_name)
        #curr.execute(sql_lease_update.format(month_name))
        #gd.commit(curr)
        #next_month = LEASE_UPDATE_DATA[month_name][1]
        curr.execute(sql_update_3.format(month_name))
        gd.commit(curr)


    #    print '\nUpdating well pct data...'
    #    lease_pct_data = gd.get_data('lease_id, prod_year', 'dbo.tx_lease_prod_pct', server='sql_server', database='US_WellS_Texas', cursor=curr, datatype='plural', sql_where='process_code=1 and {}_prod_pct=2'.format(month_name))
    #    lease_pct_data_count = len(lease_pct_data)
    #    lease_pct_data_num = 1
    #    for lease_id, prod_year in lease_pct_data:
    #        current_time = gd.get_datetime()
    #        elapsed_time = gd.elapsed_time(start_time, current_time)
    #        print '({}) {}/{} -- {} -- {}'.format(elapsed_time, lease_pct_data_num, lease_pct_data_count, lease_id, prod_year)
    #        prev_month     = LEASE_UPDATE_DATA[month_name][0]
    #        prev_prod_year = LEASE_UPDATE_DATA[month_name][2]
    #        sql_where      = "lease_id='{}' AND prod_year={} AND {}_prod_pct > 0".format(lease_id, prev_prod_year, prev_month)
    #        well_pct_ids   = gd.get_data('tx_well_id', 'dbo.tx_well_prod_pct', server='sql_server', database='US_Wells_Texas', cursor=curr, sql_where=sql_where)
    #        if well_pct_ids:
    #            well_pct_id_count = len(well_pct_ids)
    #            well_pct_id_num = 1
    #            for tx_well_id in well_pct_ids:
    #                current_time = gd.get_datetime()
    #                elapsed_time = gd.elapsed_time(start_time, current_time)
    #                print '({}) {}/{} -- {}/{} -- {} -- {} -- {}'.format(elapsed_time, lease_pct_data_num, lease_pct_data_count, well_pct_id_num, well_pct_id_count, lease_id, prod_year, tx_well_id)
    #                sql_where     = "lease_id='{}' AND prod_year={} AND tx_well_id='{}'".format(lease_id, prev_prod_year, tx_well_id)
    #                well_prod_pct = gd.get_data('{}_prod_pct'.format(prev_month), 'dbo.tx_well_prod_pct', server='sql_server', database='US_Wells_Texas', cursor=curr, datatype='float', sql_where=sql_where, single_value=True)
    #                if debug: print sql_update.format(month_name, well_prod_pct, lease_id, tx_well_id, prod_year)
    #                curr.execute(sql_update.format(month_name, well_prod_pct, lease_id, tx_well_id, prod_year))
    #                gd.commit(curr)
    #                well_pct_id_num += 1
    #        else:
    #            next_month     = LEASE_UPDATE_DATA[month_name][1]
    #            next_prod_year = LEASE_UPDATE_DATA[month_name][3]
    #            sql_where      = "lease_id='{}' AND prod_year={} AND {}_prod_pct > 0".format(lease_id, next_prod_year, next_month)
    #            well_pct_ids   = gd.get_data('tx_well_id', 'dbo.tx_well_prod_pct', server='sql_server', database='US_Wells_Texas', cursor=curr, sql_where=sql_where)
    #            if well_pct_ids:
    #                well_pct_id_count = len(well_pct_ids)
    #                well_pct_id_num = 1
    #                for tx_well_id in well_pct_ids:
    #                    current_time = gd.get_datetime()
    #                    elapsed_time = gd.elapsed_time(start_time, current_time)
    #                    print '({}) {}/{} -- {}/{} -- {} -- {} -- {}'.format(elapsed_time, lease_pct_data_num, lease_pct_data_count, well_pct_id_num, well_pct_id_count, lease_id, prod_year, tx_well_id)
    #                    sql_where     = "lease_id='{}' AND prod_year={} AND tx_well_id='{}'".format(lease_id, next_prod_year, tx_well_id)
    #                    well_prod_pct = gd.get_data('{}_prod_pct'.format(next_month), 'dbo.tx_well_prod_pct', server='sql_server', database='US_Wells_Texas', cursor=curr, datatype='float', sql_where=sql_where, single_value=True)
    #                    if debug: print sql_update.format(month_name, well_prod_pct, lease_id, tx_well_id, prod_year)
    #                    curr.execute(sql_update.format(month_name, well_prod_pct, lease_id, tx_well_id, prod_year))
    #                    gd.commit(curr)
    #                    well_pct_id_num += 1
    #            else:
    #                sql_where        = "lease_id='{}' AND prod_year={}".format(lease_id, prod_year)
    #                well_pct_ids     = gd.get_data('tx_well_id', 'dbo.tx_well_prod_pct', server='sql_server', database='US_Wells_Texas', cursor=curr, sql_where=sql_where)
    #                lease_well_count = len(well_pct_ids)
    #                well_prod_pct    = float(1.0/float(lease_well_count))
    #                well_pct_id_count = len(well_pct_ids)
    #                well_pct_id_num = 1
    #                for tx_well_id in well_pct_ids:
    #                    current_time = gd.get_datetime()
    #                    elapsed_time = gd.elapsed_time(start_time, current_time)
    #                    print '({}) {}/{} -- {}/{} -- {} -- {} -- {}'.format(elapsed_time, lease_pct_data_num, lease_pct_data_count, well_pct_id_num, well_pct_id_count, lease_id, prod_year, tx_well_id)
    #                    if debug: print sql_update_2.format(month_name, well_prod_pct, lease_id, prod_year)
    #                    curr.execute(sql_update_2.format(month_name, well_prod_pct, lease_id, prod_year))
    #                    gd.commit(curr)
    #                    well_pct_id_num += 1
    #        lease_pct_data_num += 1


def update_prev_prod(curr, debug=False):
    sql_update = \
    """
    UPDATE tx_lease_prod_schedule
      SET prev_lease_oil_prod=ISNULL(b.oil_prod_vol,0)
      FROM tx_lease_prod_schedule AS a, 
           (SELECT oil_prod_vol FROM tx_oil_production_data WHERE lease_id='{0}' AND prod_date='{1}') AS b 
      WHERE a.lease_id='{0}' AND a.prod_date='{2}'
    """
    sql_update_1 = \
    """
    UPDATE tx_lease_prod_schedule
      SET prev_prod_date='{1}'
      FROM tx_lease_prod_schedule
      WHERE lease_id='{0}' AND prod_date='{2}'
    """
    lease_prod_data = gd.get_data('lease_id, prod_date', 'dbo.tx_lease_prod_schedule', database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural', sql_where="NOT prod_date=lease_date_min AND process_code=2")
    lease_prod_data_count = len(lease_prod_data)
    lease_prod_data_num   = 1
    for lease_id, curr_prod_date in lease_prod_data:
        print '{}/{}: {} - {}'.format(lease_prod_data_num, lease_prod_data_count, lease_id, curr_prod_date)
        curr_prod_date_indx = PROD_DATES.index(curr_prod_date)
        prev_prod_date_indx = curr_prod_date_indx - 1
        prev_prod_date      = PROD_DATES[prev_prod_date_indx]
        if debug: print sql_update_1.format(lease_id, prev_prod_date, curr_prod_date)
        curr.execute(sql_update_1.format(lease_id, prev_prod_date, curr_prod_date))
        gd.commit(curr)
        lease_prod_data_num += 1


def calc_lease_period_prod(curr, debug=False):
    sql_update = \
    """
    UPDATE tx_oil_prod_schedule_2 AS a,
      (SELECT SUM(oil_prod_vol) AS total_oil_lease_prod FROM tx_production_data WHERE lease_id='{0}' AND prod_date >= '{1}' AND prod_date <= '{2}') AS b 
      SET a.lease_oil_prod=b.total_oil_lease_prod 
      WHERE a.lease_id='{0}' AND a.well_start_date='{1}' AND well_end_date='{2}'
    """
    sql_update2 = \
    """
    UPDATE tx_oil_prod_schedule_2
      SET lease_oil_prod=b.total_oil_lease_prod 
      FROM tx_oil_prod_schedule_2 AS a,
      (SELECT SUM(oil_prod_vol) AS total_oil_lease_prod FROM tx_production_data WHERE lease_id='{0}' AND prod_date >= '{1}' AND prod_date <= '{2}') AS b 
      WHERE a.lease_id='{0}' AND a.well_start_date='{1}' AND well_end_date='{2}'
    """
    sql_update3 = \
    """
    UPDATE tx_oil_prod_schedule_2
      SET lease_oil_prod=b.total_oil_lease_prod 
      FROM tx_oil_prod_schedule_2 AS a,
      (SELECT SUM(oil_prod_vol) AS total_oil_lease_prod FROM tx_oil_production_data WHERE lease_id='{0}' AND prod_date >= '{1}' AND prod_date <= '{2}') AS b 
      WHERE a.lease_id='{0}' AND a.well_start_date='{1}' AND well_end_date='{2}'
    """
    well_period_data = gd.get_data('lease_id, well_start_date, well_end_date', 'dbo.tx_oil_prod_schedule_2', database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural', sql_where="ISNULL(lease_oil_prod,0)=0 AND process_code=0")
    well_period_data_count = len(well_period_data)
    well_period_data_num = 1
    for lease_id, first_prod_date, last_prod_date in well_period_data:
        print '{}/{}: {} - {} - {}'.format(well_period_data_num, well_period_data_count, lease_id, first_prod_date, last_prod_date)
        curr.execute(sql_update3.format(lease_id, first_prod_date, last_prod_date))
        gd.commit(curr)
        well_period_data_num += 1


def get_prod_dates(start_date, end_date):
    start_date_indx = PROD_DATES.index(start_date)
    end_date_indx   = PROD_DATES.index(end_date) + 1
    prod_dates = sorted(PROD_DATES[start_date_indx: end_date_indx])
    return prod_dates


def update_prod_pct_table(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
    sql_insert = "INSERT INTO tx_well_prod_pct (lease_id, tx_well_id, prod_year) VALUES ('{}', '{}', {})"
    well_period_data = gd.get_data('lease_id, tx_well_id, start_year, end_year', 'dbo.tx_well_prod_dates', database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural', sql_where='process_code=1')
    well_period_count = len(well_period_data)
    well_period_num = 1
    for lease_id, tx_well_id, start_year, end_year in well_period_data:
        print '{}/{}: {}'.format(well_period_num, well_period_count, tx_well_id)
        for prod_year in range(start_year, end_year+1):
            if debug: print sql_insert.format(lease_id, tx_well_id, prod_year)
            curr.execute(sql_insert.format(lease_id, tx_well_id, prod_year))
            gd.commit(curr)
        well_period_num += 1
    curr.close()
    conn.close()


def lease_prod_allocation(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
    prod_pct_col_str = ', '.join(PROD_PCT_COLS)
    prod_pct_var_str = ', '.join((["'{}'"]*2) +["{}"]*15)

    if PROCESS_CODE in [1,5]:
        sql_update = \
    '''
    UPDATE tx_well_prod_pct
      SET jan_prod_pct={},feb_prod_pct={},mar_prod_pct={},apr_prod_pct={},may_prod_pct={},jun_prod_pct={},jul_prod_pct={},aug_prod_pct={},sep_prod_pct={},oct_prod_pct={},nov_prod_pct={},dec_prod_pct={} 
      WHERE lease_id='{}' AND tx_well_id='{}' AND prod_year={}
    '''
    else:
        sql_update = \
    '''
    UPDATE tx_well_prod_pct_{} 
      SET jan_prod_pct={},feb_prod_pct={},mar_prod_pct={},apr_prod_pct={},may_prod_pct={},jun_prod_pct={},jul_prod_pct={},aug_prod_pct={},sep_prod_pct={},oct_prod_pct={},nov_prod_pct={},dec_prod_pct={} 
      WHERE lease_id='{}' AND tx_well_id='{}' AND prod_year={}
    '''

    sql_where  = "process_code={}".format(PROCESS_CODE)
    lease_prod_data  = gd.get_data("lease_id, lease_date_min, lease_date_max", "tx_lease_prod_schedule", database="US_Wells_Texas", server='sql_server', cursor=curr, datatype="plural", sql_where=sql_where)
    lease_prod_count = len(lease_prod_data)
    lease_prod_num   = 1
    print lease_prod_count
    for lease_id, lease_date_min, lease_date_max in lease_prod_data:
        print '({}) -- {}/{}: {} - {} - {}'.format(gd.get_datetime(),lease_prod_num, lease_prod_count, lease_id, lease_date_min, lease_date_max)
        print ''
        all_prod_dates = get_prod_dates(lease_date_min, lease_date_max)
        all_prod_years = sorted(list(set([int(prod_date[:4]) for prod_date in all_prod_dates])))
        sql_where      = "lease_id='{}' AND lease_date_min='{}' AND lease_date_max='{}' AND process_code={}".format(lease_id, lease_date_min, lease_date_max, PROCESS_CODE)
        schedule_dates = gd.get_data('prod_date', 'tx_lease_prod_schedule', cursor=curr, database='US_Wells_Texas', server='sql_server', sql_where=sql_where)
        well_prod_pcts = {prod_year: {} for prod_year in all_prod_years}
        wells_online  = []
        wells_offline = []
        prev_year = min([int(prod_date[:4]) for prod_date in all_prod_dates])
        for prod_date in all_prod_dates:
            prod_year = int(prod_date[:4])
            prod_month = prod_date[4:]
            prev_month = MONTH_NUMS[MONTH_NUMS.index(prod_month)-1]
            if prev_year != prod_year:
                for well_id in wells_online:
                    well_prod_pcts[prod_year][well_id] = {month_num: 0.0 for month_num in MONTH_NUMS}
            if prod_date in schedule_dates:
                col_names = "schedule_id, prev_lease_oil_prod, curr_lease_oil_prod, oil_prod_vol_change"
                sql_where = "lease_id='{}' AND lease_date_min='{}' AND lease_date_max='{}' AND prod_date='{}' AND process_code={}".format(lease_id, lease_date_min, lease_date_max, prod_date, PROCESS_CODE)
                well_sched_data = gd.get_data(col_names, "tx_lease_prod_schedule", database='US_Wells_Texas', server='sql_server', cursor=curr, datatype="plural", sql_where=sql_where)
                for schedule_id, prev_lease_oil_prod, curr_lease_oil_prod, oil_prod_vol_change in well_sched_data:
                    begin_well_ids = gd.get_data("tx_well_id", "tx_oil_prod_schedule_2", database='US_Wells_Texas', server='sql_server', cursor=curr, sql_where="prod_start_id={} AND process_code={}".format(schedule_id, PROCESS_CODE))
                    end_well_ids   = gd.get_data("tx_well_id", "tx_oil_prod_schedule_2", database='US_Wells_Texas', server='sql_server', cursor=curr, sql_where="prod_end_id={} AND process_code={}".format(schedule_id, PROCESS_CODE))
                    if debug:
                        print '({}) begin_well_ids: {}'.format(prod_date, begin_well_ids)
                        print '({}) end_well_ids  : {}'.format(prod_date, end_well_ids)
                        print ''
                    for well_id in begin_well_ids:
                        well_prod_pcts[prod_year][well_id] = {month_num: 0.0 for month_num in MONTH_NUMS}
                    # If prod_date is the beginning of lease production, then divide production evenly between producing wells
                    # *** Need to incorporate allowable percentages and well production volumes on different leases to determine more accurate production percentages for each well ***
                    new_well_count = len(begin_well_ids)
                    if new_well_count:
                        if prod_date == lease_date_min:
                            for well_id in begin_well_ids:
                                well_prod_pcts[prod_year][well_id][prod_month] = 1.0/float(new_well_count)
                        elif oil_prod_vol_change <= 0:
                            for well_id in wells_online:
                                prev_prod_pct = float(well_prod_pcts[prod_year][well_id][prev_month])
                                well_prod_pcts[prod_year][well_id][prod_month] = float(0.98 * prev_prod_pct)
                            for well_id in begin_well_ids:
                                well_prod_pcts[prod_year][well_id][prod_month] = 0.02/float(new_well_count)
                        elif oil_prod_vol_change > 0:
                            prod_inc_pct = float(prev_lease_oil_prod)/float(curr_lease_oil_prod)
                            if prod_inc_pct > 0.02:
                                for well_id in wells_online:
                                    prev_prod_pct = float(well_prod_pcts[prod_year][well_id][prev_month])
                                    well_prod_pcts[prod_year][well_id][prod_month] = prev_prod_pct * float(prod_inc_pct - 0.02)
                                for well_id in begin_well_ids:
                                    well_prod_pcts[prod_year][well_id][prod_month] = (1 - (prod_inc_pct - 0.02))/float(new_well_count)
                            else:
                                for well_id in wells_online:
                                    prev_prod_pct = float(well_prod_pcts[prod_year][well_id][prev_month])
                                    well_prod_pcts[prod_year][well_id][prod_month] = prev_prod_pct * float(1-prod_inc_pct)
                                for well_id in begin_well_ids:
                                    well_prod_pcts[prod_year][well_id][prod_month] = float(prod_inc_pct)/float(new_well_count)
                    else:
                        for well_id in wells_online:
                            well_prod_pcts[prod_year][well_id][prod_month] = float(well_prod_pcts[prod_year][well_id][prev_month])
                    if len(wells_online+begin_well_ids):
                        total_prod_pct = float(sum([well_prod_pcts[prod_year][well_id][prod_month] for well_id in (wells_online+begin_well_ids)]))
                        pct_corr_factor = float(1 - total_prod_pct)/float(len(wells_online+begin_well_ids))
                        for well_id in (wells_online+begin_well_ids):
                            well_prod_pcts[prod_year][well_id][prod_month] = max(0,pct_corr_factor+well_prod_pcts[prod_year][well_id][prod_month])
                    wells_offline += end_well_ids
                    wells_online  += begin_well_ids
                    wells_online  = [well_id for well_id in wells_online if well_id not in wells_offline]
            else:
                producing_wells = [wellid for wellid in well_prod_pcts[prod_year].keys() if wellid in wells_online]
                if debug:
                    print ''
                    print '({}) producing_wells: {}'.format(prod_date, producing_wells)
                for well_id in producing_wells:
                    well_prod_pcts[prod_year][well_id][prod_month] = well_prod_pcts[prod_year][well_id][prev_month]
                    if debug: print '{} -- {} -- {} -- {}'.format(well_id, prod_year, prod_month, well_prod_pcts[prod_year][well_id][prev_month])
                total_prod_pct = sum([well_prod_pcts[prod_year][well_id][prod_month] for well_id in producing_wells])
                if total_prod_pct < 1:
                    prod_pct_diff = 1 - total_prod_pct
                    for well_id in producing_wells:
                        well_prod_pcts[prod_year][well_id][prod_month] = max(0,well_prod_pcts[prod_year][well_id][prod_month]+(float(prod_pct_diff)/float(len(producing_wells))))

            # Ensure the sum of all well production percentages = 1 for the production date
            #try:
            #    assert sum([well_prod_pcts[prod_year][wellid][prod_month] for wellid in well_prod_pcts[prod_year].keys()]) in [0, 1]
            #except:
            #    print well_prod_pcts[prod_year], sum([well_prod_pcts[prod_year][wellid][prod_month] for wellid in well_prod_pcts[prod_year].keys()])
            prev_year = prod_year
        if debug: print 'well_prod_pcts: {}'.format(well_prod_pcts)
        prod_year_count = len(well_prod_pcts.keys())
        prod_year_num = 1
        for lease_prod_year in sorted(well_prod_pcts.keys()):
            print '{}/{}: {}'.format(prod_year_num, prod_year_count, lease_prod_year)
            well_id_count = len(well_prod_pcts[lease_prod_year].keys())
            well_id_num = 1
            for well_id in well_prod_pcts[lease_prod_year].keys():
                well_pct_data = well_prod_pcts[lease_prod_year][well_id]
                if debug: print '{} -- {} -- {}'.format(well_id, lease_prod_year, well_prod_pcts[lease_prod_year][well_id])
                if PROCESS_CODE in [1,5]:
                    param_vals = tuple([well_pct_data[prod_month] for prod_month in well_pct_data.keys()]) + (lease_id, well_id, lease_prod_year)
                else:
                    param_vals = (PROCESS_CODE,)
                    param_vals += tuple([well_pct_data[prod_month] for prod_month in well_pct_data.keys()]) + (lease_id, well_id, lease_prod_year)
                if debug: print sql_update.format(*param_vals)
                curr.execute(sql_update.format(*param_vals))
                gd.commit(curr)
                well_id_num += 1
            prod_year_num += 1
        lease_prod_num += 1
    curr.close()
    conn.close()


def update_well_production_table(curr, debug=False):
    sql_update = \
    """
    INSERT INTO tx_well_production (lease_id, tx_well_id, prod_year, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, csgd_jan_mcf, csgd_feb_mcf, csgd_mar_mcf, csgd_apr_mcf, csgd_may_mcf, csgd_jun_mcf, csgd_jul_mcf, csgd_aug_mcf, csgd_sep_mcf, csgd_oct_mcf, csgd_nov_mcf, csgd_dec_mcf)
    (SELECT DISTINCT a.lease_id, a.tx_well_id, a.prod_year, a.jan_prod_pct*b.oil_jan_bbl AS well_oil_jan_bbl, a.feb_prod_pct*b.oil_feb_bbl AS well_oil_feb_bbl, a.mar_prod_pct*b.oil_mar_bbl AS well_oil_mar_bbl, a.apr_prod_pct*b.oil_apr_bbl AS well_oil_apr_bbl, a.may_prod_pct*b.oil_may_bbl AS well_oil_may_bbl, a.jun_prod_pct*b.oil_jun_bbl AS well_oil_jun_bbl, a.jul_prod_pct*b.oil_jul_bbl AS well_oil_jul_bbl, a.aug_prod_pct*b.oil_aug_bbl AS well_oil_aug_bbl, 
     a.sep_prod_pct*b.oil_sep_bbl AS well_oil_sep_bbl, a.oct_prod_pct*b.oil_oct_bbl AS well_oil_oct_bbl, a.nov_prod_pct*b.oil_nov_bbl AS well_oil_nov_bbl, a.dec_prod_pct*b.oil_dec_bbl AS well_oil_dec_bbl, a.jan_prod_pct*b.csgd_jan_mcf AS well_csgd_jan_mcf, a.feb_prod_pct*b.csgd_feb_mcf AS well_csgd_feb_mcf, a.mar_prod_pct*b.csgd_mar_mcf AS well_csgd_mar_mcf, a.apr_prod_pct*b.csgd_apr_mcf AS well_csgd_apr_mcf, a.may_prod_pct*b.csgd_may_mcf AS well_csgd_may_mcf, 
     a.jun_prod_pct*b.csgd_jun_mcf AS well_csgd_jun_mcf, a.jul_prod_pct*b.csgd_jul_mcf AS well_csgd_jul_mcf, a.aug_prod_pct*b.csgd_aug_mcf AS well_csgd_aug_mcf, a.sep_prod_pct*b.csgd_sep_mcf AS well_csgd_sep_mcf, a.oct_prod_pct*b.csgd_oct_mcf AS well_csgd_oct_mcf, a.nov_prod_pct*b.csgd_nov_mcf AS well_csgd_nov_mcf, a.dec_prod_pct*b.csgd_dec_mcf AS well_csgd_dec_mcf
     FROM tx_well_prod_pct AS a, tx_well_production AS b
     WHERE a.lease_id=b.lease_id)
    
    """


def tx_lease_to_well_prod(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
    month_names = [
        'jan',
        'feb',
        'mar',
        'apr',
        'may',
        'jun',
        'jul',
        'aug',
        'sep',
        'oct',
        'nov',
        'dec'
    ]
    sql_update = \
    '''
    UPDATE tx_well_allow_pct
      SET oil_{0}_bbl=b.well_allow_pct, csgd_{0}_mcf=b.well_allow_pct
      FROM tx_well_allow_pct AS a, tx_oil_field_schedule_lite_2 AS b 
      WHERE b.prod_month='{0}' AND a.prod_year={1} AND b.prod_year={1} AND a.tx_well_id='{2}' AND b.tx_well_id='{2}' AND a.lease_id='{3}' AND b.lease_id='{3}' 
    '''
    well_data = gd.get_data('tx_well_id, lease_id, prod_year', 'tx_well_allow_pct', database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural', sql_where='NOT tx_well_id IS NULL AND process_code={}'.format(PROCESS_CODE))
    well_data_count = len(well_data)
    well_data_num = 1
    print well_data_count
    for tx_well_id, lease_id, prod_year in well_data:
        well_prod_months = gd.get_data('prod_month', 'tx_oil_field_schedule_lite_2', database='US_Wells_Texas', server='sql_server', cursor=curr, sql_where="tx_well_id='{}' AND lease_id='{}' AND prod_year={} AND well_allow_pct > 0".format(tx_well_id, lease_id, prod_year), debug=debug)
        print '{}/{} {} well_prod_months -- {}% complete'.format(well_data_num,well_data_count, len(well_prod_months), 100*round(float(well_data_num)/float(well_data_count),3))
        if well_prod_months:
            for prod_month in well_prod_months:
                if debug: print sql_update.format(prod_month, prod_year, tx_well_id, lease_id)
                curr.execute(sql_update.format(prod_month, prod_year, tx_well_id, lease_id))
                gd.commit(curr)
            #sql_update_2 = \
            #'''
            #UPDATE tx_oil_production AS a,
            #   (SELECT SUM(oil_jan_bbl) AS total_oil_jan_bbl,
            #           SUM(oil_feb_bbl) AS total_oil_feb_bbl,
            #           SUM(oil_mar_bbl) AS total_oil_mar_bbl,
            #           SUM(oil_apr_bbl) AS total_oil_apr_bbl,
            #           SUM(oil_may_bbl) AS total_oil_may_bbl,
            #           SUM(oil_jun_bbl) AS total_oil_jun_bbl,
            #           SUM(oil_jul_bbl) AS total_oil_jul_bbl,
            #           SUM(oil_aug_bbl) AS total_oil_aug_bbl,
            #           SUM(oil_sep_bbl) AS total_oil_sep_bbl,
            #           SUM(oil_oct_bbl) AS total_oil_oct_bbl,
            #           SUM(oil_nov_bbl) AS total_oil_nov_bbl,
            #           SUM(oil_dec_bbl) AS total_oil_dec_bbl,
            #           SUM(csgd_jan_mcf) AS total_csgd_jan_mcf,
            #           SUM(csgd_feb_mcf) AS total_csgd_feb_mcf,
            #           SUM(csgd_mar_mcf) AS total_csgd_mar_mcf,
            #           SUM(csgd_apr_mcf) AS total_csgd_apr_mcf,
            #           SUM(csgd_may_mcf) AS total_csgd_may_mcf,
            #           SUM(csgd_jun_mcf) AS total_csgd_jun_mcf,
            #           SUM(csgd_jul_mcf) AS total_csgd_jul_mcf,
            #           SUM(csgd_aug_mcf) AS total_csgd_aug_mcf,
            #           SUM(csgd_sep_mcf) AS total_csgd_sep_mcf,
            #           SUM(csgd_oct_mcf) AS total_csgd_oct_mcf,
            #           SUM(csgd_nov_mcf) AS total_csgd_nov_mcf,
            #           SUM(csgd_dec_mcf) AS total_csgd_dec_mcf
            #     FROM tx_production WHERE lease_id='{1}' AND prod_year={2} AND tx_well_id IS NULL) AS b
            #SET a.oil_jan_bbl=(a.oil_jan_bbl*ISNULL(b.total_oil_jan_bbl,0)),
            #    a.oil_feb_bbl=(a.oil_feb_bbl*ISNULL(b.total_oil_feb_bbl,0)),
            #    a.oil_mar_bbl=(a.oil_mar_bbl*ISNULL(b.total_oil_mar_bbl,0)),
            #    a.oil_apr_bbl=(a.oil_apr_bbl*ISNULL(b.total_oil_apr_bbl,0)),
            #    a.oil_may_bbl=(a.oil_may_bbl*ISNULL(b.total_oil_may_bbl,0)),
            #    a.oil_jun_bbl=(a.oil_jun_bbl*ISNULL(b.total_oil_jun_bbl,0)),
            #    a.oil_jul_bbl=(a.oil_jul_bbl*ISNULL(b.total_oil_jul_bbl,0)),
            #    a.oil_aug_bbl=(a.oil_aug_bbl*ISNULL(b.total_oil_aug_bbl,0)),
            #    a.oil_sep_bbl=(a.oil_sep_bbl*ISNULL(b.total_oil_sep_bbl,0)),
            #    a.oil_oct_bbl=(a.oil_oct_bbl*ISNULL(b.total_oil_oct_bbl,0)),
            #    a.oil_nov_bbl=(a.oil_nov_bbl*ISNULL(b.total_oil_nov_bbl,0)),
            #    a.oil_dec_bbl=(a.oil_dec_bbl*ISNULL(b.total_oil_dec_bbl,0)),
            #    a.csgd_jan_mcf=(a.csgd_jan_mcf*ISNULL(b.total_csgd_jan_mcf,0)),
            #    a.csgd_feb_mcf=(a.csgd_feb_mcf*ISNULL(b.total_csgd_feb_mcf,0)),
            #    a.csgd_mar_mcf=(a.csgd_mar_mcf*ISNULL(b.total_csgd_mar_mcf,0)),
            #    a.csgd_apr_mcf=(a.csgd_apr_mcf*ISNULL(b.total_csgd_apr_mcf,0)),
            #    a.csgd_may_mcf=(a.csgd_may_mcf*ISNULL(b.total_csgd_may_mcf,0)),
            #    a.csgd_jun_mcf=(a.csgd_jun_mcf*ISNULL(b.total_csgd_jun_mcf,0)),
            #    a.csgd_jul_mcf=(a.csgd_jul_mcf*ISNULL(b.total_csgd_jul_mcf,0)),
            #    a.csgd_aug_mcf=(a.csgd_aug_mcf*ISNULL(b.total_csgd_aug_mcf,0)),
            #    a.csgd_sep_mcf=(a.csgd_sep_mcf*ISNULL(b.total_csgd_sep_mcf,0)),
            #    a.csgd_oct_mcf=(a.csgd_oct_mcf*ISNULL(b.total_csgd_oct_mcf,0)),
            #    a.csgd_nov_mcf=(a.csgd_nov_mcf*ISNULL(b.total_csgd_nov_mcf,0)),
            #    a.csgd_dec_mcf=(a.csgd_dec_mcf*ISNULL(b.total_csgd_dec_mcf,0))
            #WHERE a.tx_well_id='{0}' AND a.lease_id='{1}' AND a.prod_year={2}
            #'''
            #if debug: print sql_update_2.format(tx_well_id, lease_id, prod_year)
            #curr.execute(sql_update_2.format(tx_well_id, lease_id, prod_year))
            #gd.commit(curr)
        well_data_num += 1
    curr.close()
    conn.close()


def update_data_gaps(curr, debug=False):
    sql_update      = 'UPDATE tx_oil_field_schedule_lite_2 SET oil_allow_bbl={2}, well_portion_bbl={2} WHERE tx_well_id="{0}" AND sched_date="{1}"'
    sql_insert      = 'INSERT INTO tx_oil_field_schedule_lite_2 (tx_well_id, sched_date, oil_allow_bbl, well_portion_bbl, lease_allow_bbl, lease_prod_bbl, well_allow_pct, process_code) VALUES ("{0}", "{1}", {2}, {2}, 0, 0, 0, 3)'
    all_sched_dates = get_prod_dates('201301', '201912')
    tx_well_ids     = gd.get_data('tx_well_id', 'dbo.tx_oil_field_schedule_lite_2', cursor=curr, database='US_Wells_Texas', server='sql_server', datatype='plural', sql_where='well_allow_pct > 0')
    well_prod_data = {tx_well_id: sorted([(well_data[1], well_data[2]) for well_data in all_well_data if well_data[0] == tx_well_id]) for tx_well_id in well_ids}
    well_count = len(tx_well_ids)
    well_num   = 1
    for tx_well_id in tx_well_ids:
        well_sched_data   = gd.get_data('sched_date, ISNULL(well_portion_bbl,0)', 'dbo.tx_oil_field_schedule_lite_2', cursor=curr,database='US_Wells_Texas', server='sql_server', datatype='plural', sql_where='tx_well_id="{}"'.format(tx_well_id))
        well_sched_dates  = sorted(list(set([well_data[0] for well_data in well_sched_data])))
        well_portion_data = {well_data[0]: well_data[1] for well_data in well_sched_data}
        well_prod_dates   = [well_sched_date for well_sched_date in well_sched_dates if well_portion_data[well_sched_date] > 0]
        sched_start_indx  = all_sched_dates.index(well_sched_dates[0])
        sched_end_indx    = all_sched_dates.index(well_sched_dates[-1])
        last_well_portion = 0
        curr_well_portion = 0
        next_well_portion = 0
        curr_sched_indx = 0
        next_sched_indx = 1
        next_sched_date = well_sched_dates[1]
        for sched_date in all_sched_dates[sched_start_indx:sched_end_indx+2]:
            print '{}/{}: {} -- {}'.format(well_num, well_count, tx_well_id, sched_date)
            if sched_date in well_sched_dates:
                if sched_date in well_prod_dates:
                    last_well_portion = well_portion_data[sched_date]
                    last_sched_indx   = well_prod_dates.index(sched_date)
                    next_sched_indx   = last_sched_indx + 1
                    next_sched_date   = well_prod_dates[next_sched_indx]
                    try:
                        next_well_portion = well_portion_data[next_sched_date]
                    except:
                        next_well_portion = 0
                    curr_well_portion = round((float(last_well_portion)+float(next_well_portion))/2,3)
                else:
                    if debug: print sql_update.format(tx_well_id, sched_date, curr_well_portion)
                    curr.execute(sql_update.format(tx_well_id, sched_date, curr_well_portion))
                    gd.commit(curr)
            else:
                if debug: print sql_insert.format(tx_well_id, sched_date, curr_well_portion)
                curr.execute(sql_insert.format(tx_well_id, sched_date, curr_well_portion))
                gd.commit(curr)
        well_num += 1

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_tx_lease_details(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells')
    curr = conn.cursor()
    sql_update  = "UPDATE tblUSWell_Texas_Details SET Lease_No='{}', Field_No={}, District_No='{}', Oil_Gas_Code='{}' WHERE WellID={}"
    lease_data  = gd.get_data('WellID, API_Number', 'dbo.tblUSWell_Texas_Details', server='sql_server', database='US_Wells_Texas', datatype='plural', cursor=curr, sql_where="SUBSTRING(API_Number,1,1) IN ('O','G')")
    lease_count = len(lease_data)
    lease_num   = 1
    for well_id, api_num in lease_data:
        print '{}/{}: {} -- {}'.format(lease_num, lease_count, well_id, api_num)
        lease_info   = api_num.split('-')
        oil_gas_code = lease_info[0]
        district_no  = ('0'*(2-len(lease_info[1]))) + lease_info[1]
        lease_no     = ('0'*(6-len(lease_info[2]))) + lease_info[2]
        field_no     = int(lease_info[3])
        if debug: print sql_update.format(lease_no, field_no, district_no, oil_gas_code, well_id)
        curr.execute(sql_update.format(lease_no, field_no, district_no, oil_gas_code, well_id))
        gd.commit(curr)
        lease_num += 1
    curr.close()
    conn.close()


def update_tx_well_details(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells')
    curr = conn.cursor()
    sql_update  = "UPDATE tblUSWell_Texas_Details SET Lease_No='{}', District_No='{}', Oil_Gas_Code='{}', Well_No='{}' WHERE WellID={}"
    lease_data  = gd.get_data('WellID, Reported_API_Number', 'dbo.tblUSWell_Texas_Details', server='sql_server', database='US_Wells_Texas', datatype='plural', cursor=curr, sql_where="SUBSTRING(API_Number,1,2)='42' AND NOT Lease_Number IS NULL AND TX_Well_ID IS NULL")
    lease_count = len(lease_data)
    lease_num   = 1
    for well_id, api_num in lease_data:
        print '(1) {}/{}: {} -- {}'.format(lease_num, lease_count, well_id, api_num)
        lease_info   = api_num.split('-')
        oil_gas_code = lease_info[0][0]
        lease_no     = ('0' * (6 - len(lease_info[0][2:]))) + lease_info[0][2:]
        district_no  = DISTRICT_DATA[lease_info[1]]
        well_no      = ''.join(lease_info[3:])
        if debug: print sql_update.format(lease_no, district_no, oil_gas_code, well_no, well_id)
        curr.execute(sql_update.format(lease_no, district_no, oil_gas_code, well_no, well_id))
        gd.commit(curr)
        lease_num += 1

    sql_update  = "UPDATE tblUSWell_Texas_Details SET District_No='{}', Well_No='{}' WHERE WellID={}"
    lease_data  = gd.get_data('WellID, Reported_API_Number', 'dbo.tblUSWell_Texas_Details', server='sql_server', database='US_Wells_Texas', datatype='plural', cursor=curr, sql_where="SUBSTRING(API_Number,1,2)='42' AND Lease_Number IS NULL AND TX_Well_ID IS NULL")
    lease_count = len(lease_data)
    lease_num   = 1
    for well_id, api_num in lease_data:
        print '(2) {}/{}: {} -- {}'.format(lease_num, lease_count, well_id, api_num)
        lease_info   = api_num.split('-')
        district_no  = DISTRICT_DATA[lease_info[1]]
        well_no      = ''.join(lease_info[3:])
        if debug: print sql_update.format(district_no, well_no, well_id)
        curr.execute(sql_update.format(district_no, well_no, well_id))
        gd.commit(curr)
        lease_num += 1
    curr.close()
    conn.close()


def update_tx_lease_id_details(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells')
    curr = conn.cursor()
    sql_update = "UPDATE tblUSWell_Texas_Details SET Well_No='{}' WHERE WellID={}"
    lease_data = gd.get_data('WellID, Well_Name, Lease_Name', 'dbo.tblUSWell_Texas_Details', server='sql_server', database='US_Wells_Texas', datatype='plural', cursor=curr, sql_where="SUBSTRING(API_Number,1,1) IN ('O','G') AND Well_No IS NULL AND WellID > 9773432")
    lease_count = len(lease_data)
    lease_num = 1
    for well_id, well_name, lease_name in lease_data:
        print '{}/{}: {} -- {} -- {}'.format(lease_num, lease_count, well_id, well_name, lease_name)
        try:
            lease_name_len = len(lease_name)
        except:
            lease_name_len = 0
        try:
            well_no = well_name[lease_name_len:].strip()
        except:
            well_no = ''
        if debug: print sql_update.format(well_no, well_id), '\n'
        curr.execute(sql_update.format(gd.encode_str(well_no), well_id))
        gd.commit(curr)
        lease_num += 1
    curr.close()
    conn.close()


def find_curve_fit(curr=None, prod_periods=None, prod_values=None, well_life=25, yrs_before_term=3, decline_rate_type='avg', arps_params=None, prod_comm='', well_api='', debug=False):
    Qi          = prod_values[0]
    xdata       = np.arange(len(prod_periods))
    ydata       = np.array(prod_values)
    init_params = None

    if debug:
        print prod_comm, 'prod_periods: {}'.format(prod_periods)
        print prod_comm, 'prod_values : {}'.format(prod_values)

    def decline_curve(x, b, Di):
        return float(Qi) / (1.0 + (b*Di*x))**(1.0/float(b))

    def terminal_decline(x, Qt, Dt):
        Qx = Qt*(1-Dt)**(x+1)
        return Qx

    if debug and 0:
        print prod_comm, "xdata:", xdata
        print prod_comm, "ydata:", ydata

    if len(prod_periods) >= (yrs_before_term*12):
        term_decline_col = PROD_COMM_COLS[prod_comm][2]
        term_decline = gd.get_data(term_decline_col, 'dbo.tblUSWell_Parameters', sql_where="API_Number='{}'".format(well_api), server='sql_server', database='US_Wells', datatype='float', single_value=True, cursor=curr, debug=debug)
        monthly_decline = 1 - (1.0-term_decline)**float(1.0/12.0)
        if debug: print prod_comm, 'term_decline: {} --- monthly_decline: {}'.format(term_decline, monthly_decline)
        recent_prod_len  = min(6,len(prod_values))
        recent_prod_vals = [prod_val for prod_val in prod_values[-recent_prod_len:] if prod_val > 0]
        recent_prod_avg  = float(sum(recent_prod_vals))/float(max(1,len(recent_prod_vals)))
        Qt = max(prod_values[-1],recent_prod_avg)
        total_prod_months = (well_life*12)
        xdata = np.arange(well_life*12)
        ydata = terminal_decline(xdata, Qt, monthly_decline)
        forecast_vals = ydata.tolist()
        forecast_vals = [round(float(prod_val),2) for prod_val in forecast_vals if prod_val >= 1]
        if debug: print prod_comm, 'forecast_vals: {}'.format(forecast_vals)
    elif len(prod_periods) <= 2:
        if arps_params and sum([arps_params[prod_comm][param_name] for param_name in ["Qi", "Di", "b"]]) > 0:
            b  = arps_params[prod_comm]['b']
            Di = arps_params[prod_comm]['Di']
        else:
            b = DEFAULT_b_VALUE
            Di = DFAULT_Di_VALUE
        b  = min(max(0.1, b), 3)
        Di = min(max(0.05, Di), 0.9)
        xdata = np.arange(well_life*12)
        ydata = decline_curve(xdata, b, Di)
        forecast_vals = ydata.tolist()
        forecast_vals = [round(float(prod_val), 2) for prod_val in forecast_vals if prod_val >= 1]
    else:
        if arps_params and sum([arps_params[prod_comm][param_name] for param_name in ["Qi", "Di", "b"]]) > 0:
            b  = arps_params[prod_comm]['b']
            Di = arps_params[prod_comm]['Di']
            b = min(max(0.1, b), 3)
            Di = min(max(0.05, Di), 0.9)
        else:
            popt, pcov = scipy.optimize.curve_fit(decline_curve, xdata, ydata, maxfev=10000, p0=init_params)
            b, Di = popt
            b = min(max(0.1, b), 3)
            Di = min(max(0.05, Di), 0.9)
        if prod_comm in ['OIL', 'GAS']:
            sql_update = "UPDATE US_Wells.dbo.tblUSWell_Parameters SET Decline_Param_{0}_Qi={1}, Decline_Param_{0}_Di={2}, Decline_Param_{0}_b={3} WHERE API_Number='{4}'".format(prod_comm, Qi, Di, b, well_api)
            if debug: print prod_comm, sql_update
            curr.execute(sql_update)
            gd.commit(curr)
        xdata = np.arange(well_life * 12)
        ydata = decline_curve(xdata, b, Di)
        prod_vals = ydata.tolist()
        last_srcd_indx = len(prod_periods) - 1

        if debug:
            print prod_comm, 'prod_vals ({})   : {}'.format(len(prod_vals), prod_vals)
            print prod_comm, 'prod_periods ({}): {}'.format(len(prod_periods), prod_periods)
            print prod_comm, 'prod_values ({}) : {}'.format(len(prod_values), prod_values)
            print prod_comm, 'last_srcd_indx   : {}'.format(last_srcd_indx)

        #recent_prod_len  = min(6,len(prod_values))
        #recent_prod_vals = [prod_val for prod_val in prod_values[-recent_prod_len:] if prod_val > 0]
        #recent_prod_avg  = float(sum(recent_prod_vals))/float(max(1,len(recent_prod_vals)))
        #forecast_vals    = [round(float(prod_val),2) for prod_val in prod_vals if prod_val < max(recent_prod_avg,prod_values[-1])]
        forecast_vals    = [round(float(prod_val),2) for prod_val in prod_vals if prod_val < prod_values[-1]]
    all_prod_vals = prod_values + forecast_vals
    prod_months   = get_prod_dates(prod_periods[-1], len(forecast_vals)+1)[1:]
    prod_months   = prod_periods + prod_months
    prod_forecast = dict(zip(prod_months, all_prod_vals))
    if debug:
        print prod_comm, 'len(prod_values)    : {}'.format(len(prod_values))
        print prod_comm, 'len(forecast_values): {}'.format(len(forecast_vals))
        print prod_comm, 'len(all_prod_vals)  : {}'.format(len(all_prod_vals))
        print prod_comm, 'len(prod_periods)   : {}'.format(len(prod_periods))
        print prod_comm, 'len(prod_months)    : {}'.format(len(prod_months))

        print prod_comm, 'all_prod_vals       : {}'.format(all_prod_vals)
        print prod_comm, 'prod_months         : {}'.format(prod_months)
        print prod_comm, 'prod_forecast       : {}'.format(prod_forecast)
        print '\n'
    return prod_forecast


def update_well_no_data(debug=False):
    conn = gd.get_connection(database='us_wells')
    curr = conn.cursor()
    sql_update_1  = "UPDATE tx_oil_well_prod_data SET well_no='{}' WHERE id={}"
    sql_update_2  = "UPDATE tx_oil_well_prod_data SET well_no='{}', process_code=2 WHERE id={}"

    lease_data  = gd.get_data('id, api_number, lease_name', 'tx_oil_well_prod_data', database='US_Wells_Texas', server='sql_server', datatype='plural', cursor=curr, sql_where='process_code=1')
    lease_count = len(lease_data)
    lease_num   = 1
    for id, api_num, lease_name in lease_data:
        print '{}/{}: {} -- {} -- {}'.format(lease_num, lease_count, id, api_num, lease_name)
        lease_info = lease_name.split()
        well_no = lease_info[-1]
        if ('1' in well_no or '2' in well_no or '3' in well_no or '4' in well_no or '5' in well_no or '6' in well_no or '7' in well_no or '8' in well_no or '9' in well_no or '0' in well_no) and len(well_no) <= 10:
            if api_num:
                api_well_nos = gd.get_data('well_no', 'tx_ref_well_id', database='US_Wells_Texas', server='sql_server', cursor=curr, sql_where='api_number="{}"'.format(api_num))
                if well_no in api_well_nos:
                    if debug: print sql_update_1.format(well_no, id),'\n'
                    curr.execute(sql_update_1.format(well_no, id))
                    gd.commit(curr)
                else:
                    if debug: print sql_update_2.format(well_no, id),'\n'
                    curr.execute(sql_update_2.format(well_no, id))
                    gd.commit(curr)
            else:
                if debug: print sql_update_2.format(well_no, id),'\n'
                curr.execute(sql_update_2.format(well_no, id))
                gd.commit(curr)
        else:
            print '\n'
        lease_num += 1
    curr.close()
    conn.close()


def get_well_prod_id(curr, add_indx):
    curr.execute('SELECT ISNULL(MAX(id),1) FROM US_Wells_Texas.dbo.tx_hist_well_prod')
    max_prod_id = int(curr.fetchone()[0])
    well_prod_id = max_prod_id + add_indx
    return well_prod_id


def store_comm_prod_data(curr, tx_well_id, comm_prod_data, debug=False):
    sql_insert     = "INSERT INTO US_Wells_Texas.dbo.tx_hist_well_prod (id, tx_well_id, state_id, prod_year, {}, sources) VALUES ({}, '{}', '42', {}, {}, 'Historical')"
    sql_update     = "UPDATE US_Wells_Texas.dbo.tx_hist_well_prod SET {} WHERE tx_well_id='{}' AND prod_year={}"
    zero_str       = ', '.join(["0"]*26)
    oil_prod_years = []
    gas_prod_years = []
    well_prod_id   = get_well_prod_id(curr, 1)
    if comm_prod_data["oil"].keys():
        oil_prod_years = [int(prod_date[:4]) for prod_date in comm_prod_data["oil"].keys()]
    if comm_prod_data["gas"].keys():
        gas_prod_years = [int(prod_date[:4]) for prod_date in comm_prod_data["gas"].keys()]
    prod_years     = sorted(list(set(oil_prod_years + gas_prod_years)))
    if debug or 1: print '{}: prod_years: {}'.format(tx_well_id, prod_years)
    for prod_year in prod_years:
        annual_prod = 0
        try:
            annual_prod = sum([sum([comm_prod_data[prod_comm][prod_date] for prod_date in comm_prod_data[prod_comm].keys() if int(prod_date[:4])==prod_year]) for prod_comm in ["oil", "gas"]])
        except:
            pass
        if annual_prod > 0:
            if debug: print sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str)
            #try:
            curr.execute(sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str))
            gd.commit(curr)
            #except:
            #    try:
            #        well_prod_id = get_well_prod_id(curr, 2)
            #        curr.execute(sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str))
            #        gd.commit(curr)
            #    except:
            #        well_prod_id = get_well_prod_id(curr, 3)
            #        curr.execute(sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str))
            #        gd.commit(curr)
            well_prod_id += 1
            for comm in comm_prod_data.keys():
                comm_str_list = []
                comm_unit = COMM_UNITS[comm.lower()]
                prod_dates = [prod_date for prod_date in comm_prod_data[comm].keys() if int(prod_date[:4]) == prod_year]
                #print 'prod_dates: {}'.format(prod_dates)
                if prod_dates:
                    for prod_date in prod_dates:
                        month_name      = MONTH_NAMES[prod_date[4:]]
                        month_comm_prod = float(comm_prod_data[comm][prod_date])
                        comm_str_list.append('{}_{}_{}={}'.format(comm, month_name, comm_unit, month_comm_prod))
                    comm_str = ', '.join(comm_str_list)
                    if debug: print sql_update.format(comm_str, tx_well_id, prod_year)
                    curr.execute(sql_update.format(comm_str, tx_well_id, prod_year))
                    gd.commit(curr)


def insert_missing_prod_years(curr, tx_well_id, debug=False):
    comm_prod        = {'oil': 0, 'gas': 0}
    sql_insert       = "INSERT INTO US_Wells_Texas.dbo.tx_hist_well_prod (id, tx_well_id, state_id, prod_year, {}, sources) VALUES ({}, '{}', '42', {}, {}, 'Estimated')"
    sql_update       = "UPDATE US_Wells_Texas.dbo.tx_hist_well_prod SET {} WHERE tx_well_id='{}' AND prod_year={}"
    zero_str         = ', '.join(["0"]*26)
    well_prod_id     = get_well_prod_id(curr, 1)

    sql_where        = "tx_well_id='{}' AND (oil_prod_vol+gas_prod_vol) > 0 ORDER BY prod_date ASC".format(tx_well_id)
    first_prod_vals  = gd.get_data('TOP 1 oil_prod_vol, gas_prod_vol, prod_date', 'US_Wells_Texas.dbo.tx_oil_well_prod_data_lite', server='sql_server', database='US_Wells_Texas', cursor=curr, datatype='plural', sql_where=sql_where, single_value=True)
    comm_prod['oil'] = float(first_prod_vals[0])
    comm_prod['gas'] = float(first_prod_vals[1])

    prod_year_limits = gd.get_data('SUBSTRING(first_production_date,1,4), SUBSTRING(last_production_date,1,4)', 'US_Wells_Texas.dbo.tx_oil_prod_schedule', server='sql_server', database='US_Wells_Texas', datatype='plural', cursor=curr, sql_where="tx_well_id='{}'".format(tx_well_id), single_value=True)
    prod_start_year  = int(prod_year_limits[0])
    prod_end_year    = int(prod_year_limits[1])
    well_prod_years  = range(prod_start_year, prod_end_year+1)
    hist_prod_years  = gd.get_data('prod_year', 'US_Wells_Texas.dbo.tx_hist_well_prod', server='sql_server', database='US_Wells_Texas', datatype='int', cursor=curr, sql_where="tx_well_id='{}'".format(tx_well_id))
    if well_prod_years and hist_prod_years:
        prod_years       = sorted([prod_year for prod_year in well_prod_years if prod_year not in hist_prod_years and prod_year < min(hist_prod_years)])
        for prod_year in prod_years:
            if debug: print sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str)
            curr.execute(sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str))
            gd.commit(curr)
            well_prod_id += 1
            for comm in ['oil', 'gas']:
                comm_str_list = []
                comm_unit = COMM_UNITS[comm]
                for month_name in MONTH_NAMES.values():
                    month_comm_prod = comm_prod[comm]
                    comm_str_list.append('{}_{}_{}={}'.format(comm, month_name, comm_unit, month_comm_prod))
                    comm_str = ', '.join(comm_str_list)
                    if debug: print sql_update.format(comm_str, tx_well_id, prod_year)
                    curr.execute(sql_update.format(comm_str, tx_well_id, prod_year))
                    gd.commit(curr)


def get_hist_prod_data(curr, tx_well_id, debug=False):
    hist_prod_data = {'oil': {}, 'gas': {}}
    well_prod_data = gd.get_data('prod_date, oil_prod_vol, gas_prod_vol', 'US_Wells_Texas.dbo.tx_oil_well_prod_data_lite', server='sql_server', database='US_Wells_Texas', cursor=curr, datatype='plural', sql_where="tx_well_id='{}' AND prod_year=2019".format(tx_well_id))
    for prod_date, oil_prod_vol, gas_prod_vol in well_prod_data:
        prod_date = gd.decode_str(prod_date)
        hist_prod_data['oil'][prod_date] = oil_prod_vol
        hist_prod_data['gas'][prod_date] = gas_prod_vol
    return hist_prod_data


def get_comm_prod_data(curr, tx_well_id, debug=False):
    hist_prod_data = get_hist_prod_data(curr, tx_well_id, debug=debug)
    comm_prod_data = {}
    for comm in hist_prod_data.keys():
        comm_prod_data[comm] = {}
        comm_prod    = hist_prod_data[comm]
        prod_dates   = sorted([prod_dt for prod_dt in comm_prod.keys() if comm_prod[prod_dt] > 0])
        if prod_dates:
            start_date   = prod_dates[0]
            end_date     = prod_dates[-1]
            prod_periods = get_prod_dates(start_date, end_date)
            prod_years   = []
            prod_values  = []
            curr_indx    = 0
            last_indx    = 0
            curr_prod    = 0
            last_prod    = 0
            if debug: print '{}: prod_dates  : {}'.format(tx_well_id, prod_dates)
            if debug: print '{}: prod_periods: {}'.format(tx_well_id, prod_periods)
            for prod_date in prod_dates:
                prod_years.append(int(prod_date[:4]))
                last_indx = curr_indx
                curr_indx = prod_periods.index(prod_date)
                last_prod = curr_prod
                curr_prod = comm_prod[prod_date]
                if curr_indx - last_indx < 2:
                    prod_values.append(curr_prod)
                else:
                    add_points = gd.get_lin_vals((last_indx,last_prod),(curr_indx,curr_prod),(curr_indx-last_indx)+1)[0][1:]
                    prod_values += add_points
            comm_prod_data[comm] = dict(zip(prod_periods, prod_values))
    return comm_prod_data


def generate_hist_well_prod(debug=False):
    sql_where   = "process_code=5"
    tx_well_ids = gd.get_data('tx_well_id', 'dbo.tx_oil_well_prod_data_lite', server='sql_server', database='US_Wells_Texas', sql_where=sql_where,  debug=debug)
    tx_well_id_count = len(tx_well_ids)
    tx_well_id_num   = 1
    for tx_well_id in tx_well_ids:
        conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
        curr = conn.cursor()
        print '{}/{}: {}'.format(tx_well_id_num, tx_well_id_count, tx_well_id)
        curr.execute("SET IDENTITY_INSERT US_Wells_Texas.dbo.tx_hist_well_prod ON")
        comm_prod_data = get_comm_prod_data(curr, tx_well_id, debug=debug)
        store_comm_prod_data(curr, tx_well_id, comm_prod_data, debug=debug)
        curr.close()
        conn.close()
        tx_well_id_num += 1


def generate_missing_hist_well_prod(debug=False):
    sql_where   = "tx_well_id IN (SELECT DISTINCT tx_well_id FROM tx_oil_prod_schedule WHERE process_code=1)"
    tx_well_ids = gd.get_data('tx_well_id', 'dbo.tx_hist_well_prod', server='sql_server', database='US_Wells_Texas', sql_where=sql_where,  debug=debug)
    tx_well_id_count = len(tx_well_ids)
    tx_well_id_num   = 1
    for tx_well_id in tx_well_ids:
        conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
        curr = conn.cursor()
        print '{}/{}: {}'.format(tx_well_id_num, tx_well_id_count, tx_well_id)
        curr.execute("SET IDENTITY_INSERT US_Wells_Texas.dbo.tx_hist_well_prod ON")
        insert_missing_prod_years(curr, tx_well_id, debug=debug)
        curr.close()
        conn.close()
        tx_well_id_num += 1


def update_hist_oil_prod(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
    sql_update_1 = \
    '''
    UPDATE tx_hist_well_prod
      SET api_number=b.api_number, well_no=b.well_no, lease_id=b.lease_id, lease_no=b.lease_no, county_no=b.county_no, district_no=b.district_no, oil_gas_code=b.oil_gas_code
      FROM tx_hist_well_prod a, tx_ref_well_id b
      WHERE a.tx_well_id=b.tx_well_id
    '''

    sql_update_2 = \
    '''
    UPDATE tx_hist_well_prod
      SET lease_prod_id=b.lease_prod_id
      FROM tx_hist_well_prod a, tx_oil_well_prod_data_lite b
      WHERE a.tx_well_id=b.tx_well_id
    '''

    sql_insert = \
    '''
    INSERT INTO tx_hist_oil_prod (well_id, lease_well_id, tx_well_id, api_number, well_no, oil_gas_code, lease_prod_id, lease_id, lease_no, district_no, county_no, state_id, prod_year, oil_total_bbl, gas_total_mcf, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, gas_jan_mcf, gas_feb_mcf, gas_mar_mcf, gas_apr_mcf, gas_may_mcf, gas_jun_mcf, gas_jul_mcf, gas_aug_mcf, gas_sep_mcf, gas_oct_mcf, gas_nov_mcf, gas_dec_mcf, sources)
      (SELECT DISTINCT well_id, lease_well_id, tx_well_id, api_number, well_no, oil_gas_code, lease_prod_id, lease_id, lease_no, district_no, county_no, state_id, prod_year, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sources FROM tx_hist_well_prod)
    '''

    sql_update_main = \
    '''
    UPDATE tx_hist_oil_prod
      SET  oil_jan_bbl=ROUND(c.oil_jan_bbl*IIF(d.oil_jan_total=0,0,(b.oil_jan_bbl/d.oil_jan_total)),3),
           oil_feb_bbl=ROUND(c.oil_feb_bbl*IIF(d.oil_feb_total=0,0,(b.oil_feb_bbl/d.oil_feb_total)),3),
           oil_mar_bbl=ROUND(c.oil_mar_bbl*IIF(d.oil_mar_total=0,0,(b.oil_mar_bbl/d.oil_mar_total)),3),
           oil_apr_bbl=ROUND(c.oil_apr_bbl*IIF(d.oil_apr_total=0,0,(b.oil_apr_bbl/d.oil_apr_total)),3),
           oil_may_bbl=ROUND(c.oil_may_bbl*IIF(d.oil_may_total=0,0,(b.oil_may_bbl/d.oil_may_total)),3),
           oil_jun_bbl=ROUND(c.oil_jun_bbl*IIF(d.oil_jun_total=0,0,(b.oil_jun_bbl/d.oil_jun_total)),3),
           oil_jul_bbl=ROUND(c.oil_jul_bbl*IIF(d.oil_jul_total=0,0,(b.oil_jul_bbl/d.oil_jul_total)),3),
           oil_aug_bbl=ROUND(c.oil_aug_bbl*IIF(d.oil_aug_total=0,0,(b.oil_aug_bbl/d.oil_aug_total)),3),
           oil_sep_bbl=ROUND(c.oil_sep_bbl*IIF(d.oil_sep_total=0,0,(b.oil_sep_bbl/d.oil_sep_total)),3),
           oil_oct_bbl=ROUND(c.oil_oct_bbl*IIF(d.oil_oct_total=0,0,(b.oil_oct_bbl/d.oil_oct_total)),3),
           oil_nov_bbl=ROUND(c.oil_nov_bbl*IIF(d.oil_nov_total=0,0,(b.oil_nov_bbl/d.oil_nov_total)),3),
           oil_dec_bbl=ROUND(c.oil_dec_bbl*IIF(d.oil_dec_total=0,0,(b.oil_dec_bbl/d.oil_dec_total)),3),
    	  gas_jan_mcf=ROUND(c.csgd_jan_mcf*IIF(d.gas_jan_total=0,0,(b.gas_jan_mcf/d.gas_jan_total)),3),
    	  gas_feb_mcf=ROUND(c.csgd_feb_mcf*IIF(d.gas_feb_total=0,0,(b.gas_feb_mcf/d.gas_feb_total)),3),
    	  gas_mar_mcf=ROUND(c.csgd_mar_mcf*IIF(d.gas_mar_total=0,0,(b.gas_mar_mcf/d.gas_mar_total)),3),
    	  gas_apr_mcf=ROUND(c.csgd_apr_mcf*IIF(d.gas_apr_total=0,0,(b.gas_apr_mcf/d.gas_apr_total)),3),
    	  gas_may_mcf=ROUND(c.csgd_may_mcf*IIF(d.gas_may_total=0,0,(b.gas_may_mcf/d.gas_may_total)),3),
    	  gas_jun_mcf=ROUND(c.csgd_jun_mcf*IIF(d.gas_jun_total=0,0,(b.gas_jun_mcf/d.gas_jun_total)),3),
    	  gas_jul_mcf=ROUND(c.csgd_jul_mcf*IIF(d.gas_jul_total=0,0,(b.gas_jul_mcf/d.gas_jul_total)),3),
    	  gas_aug_mcf=ROUND(c.csgd_aug_mcf*IIF(d.gas_aug_total=0,0,(b.gas_aug_mcf/d.gas_aug_total)),3),
    	  gas_sep_mcf=ROUND(c.csgd_sep_mcf*IIF(d.gas_sep_total=0,0,(b.gas_sep_mcf/d.gas_sep_total)),3),
    	  gas_oct_mcf=ROUND(c.csgd_oct_mcf*IIF(d.gas_oct_total=0,0,(b.gas_oct_mcf/d.gas_oct_total)),3),
    	  gas_nov_mcf=ROUND(c.csgd_nov_mcf*IIF(d.gas_nov_total=0,0,(b.gas_nov_mcf/d.gas_nov_total)),3),
    	  gas_dec_mcf=ROUND(c.csgd_dec_mcf*IIF(d.gas_dec_total=0,0,(b.gas_dec_mcf/d.gas_dec_total)),3)
      FROM tx_hist_oil_prod a,
           tx_hist_well_prod b,
           tx_production c,
           (SELECT DISTINCT lease_prod_id,prod_year,SUM(oil_jan_bbl) AS oil_jan_total,SUM(oil_feb_bbl) AS oil_feb_total,SUM(oil_mar_bbl) AS oil_mar_total,SUM(oil_apr_bbl) AS oil_apr_total,SUM(oil_may_bbl) AS oil_may_total,SUM(oil_jun_bbl) AS oil_jun_total,SUM(oil_jul_bbl) AS oil_jul_total,SUM(oil_aug_bbl) AS oil_aug_total,SUM(oil_sep_bbl) AS oil_sep_total,SUM(oil_oct_bbl) AS oil_oct_total,SUM(oil_nov_bbl) AS oil_nov_total,SUM(oil_dec_bbl) AS oil_dec_total,SUM(gas_jan_mcf) AS gas_jan_total,SUM(gas_feb_mcf) AS gas_feb_total,SUM(gas_mar_mcf) AS gas_mar_total,SUM(gas_apr_mcf) AS gas_apr_total,SUM(gas_may_mcf) AS gas_may_total,SUM(gas_jun_mcf) AS gas_jun_total,SUM(gas_jul_mcf) AS gas_jul_total,SUM(gas_aug_mcf) AS gas_aug_total,SUM(gas_sep_mcf) AS gas_sep_total,SUM(gas_oct_mcf) AS gas_oct_total,SUM(gas_nov_mcf) AS gas_nov_total,SUM(gas_dec_mcf) AS gas_dec_total 
            FROM tx_hist_well_prod GROUP BY lease_prod_id, prod_year) d
      WHERE a.lease_id=b.lease_id AND a.lease_id=c.lease_id AND a.lease_id=d.lease_id AND a.prod_year=b.prod_year AND a.prod_year=c.prod_year AND a.prod_year=d.prod_year
    '''
    # --------------------------------------------
    #if debug: print sql_update_1
    #curr.execute(sql_update_1)
    #gd.commit(curr)
    #print 'tx_hist_oil_prod update 1 complete'

    #if debug: print sql_update_2
    #curr.execute(sql_update_2)
    #gd.commit(curr)
    #print 'tx_hist_oil_prod update 2 complete'

    if debug: print sql_insert
    curr.execute(sql_insert)
    gd.commit(curr)
    print 'tx_hist_oil_prod update 3 complete'

    if debug: print sql_update_main
    curr.execute(sql_update_main)
    gd.commit(curr)
    print 'tx_hist_oil_prod update 4 complete'

    curr.close()
    conn.close()


def main(update=False,
         allocate=False,
         calc=False,
         fill_gaps=False,
         update_lease_details=False,
         update_well_details=False,
         update_lease_id_details=False,
         gen_hist_prod=False,
         update_well_no=False,
         insert_missing_years=False,
         update_hist_oil=False,
         update_pct_table=False,
         update_missing_pct=False,
         debug=False):
    conn = gd.get_connection(database='US_Wells_Texas', server='sql_server')
    curr = conn.cursor()
    if update:
        update_prev_prod(curr, debug=debug)
    if allocate:
        lease_prod_allocation(debug=debug)
    if calc:
        calc_lease_period_prod(curr, debug=debug)
    if fill_gaps:
        update_data_gaps(curr, debug=debug)
    if update_lease_details:
        update_tx_lease_details(debug=debug)
    if update_well_details:
        update_tx_well_details(debug=debug)
    if update_lease_id_details:
        update_tx_lease_id_details(debug=debug)
    if update_well_no:
        update_well_no_data(debug=debug)
    if gen_hist_prod:
        generate_hist_well_prod(debug=debug)
    if insert_missing_years:
        generate_missing_hist_well_prod(debug=debug)
    if update_hist_oil:
        update_hist_oil_prod(debug=debug)
    if update_pct_table:
        update_prod_pct_table(debug=debug)
    if update_missing_pct:
        update_pct_gaps(curr, debug=debug)
    curr.close()
    conn.close()

if __name__=='__main__':
    main(update_missing_pct=True, debug=False)
    #tx_lease_to_well_prod()
    # Start: 8:55pm 2020-03-21
    # End:





