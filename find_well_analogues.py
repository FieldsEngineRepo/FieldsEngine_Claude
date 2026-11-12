import globaldata as gd
from math import cos, asin, sqrt


PROCESS_CODE    = 1
PROD_RATE_UNITS = {
    "OIL"       : "bd",
    "GAS"       : "mmcfd",
    "CONDENSATE": "bd",
    "NGL"       : "bd"
}


def distance(lat1, lon1, lat2, lon2):
    p = 0.01745329251994329508887757483
    a = 0.5 - (float(cos((lat2 - lat1) * p))/2.0) + (float(cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p)))/2.0)
    return 7926.382 * asin(sqrt(a))


def calc_length_est(curr, well_data, len_col, debug=False):
    if debug: print well_data
    analogue_wells = []
    operator       = well_data['operator']
    state_name     = well_data['state_name']
    county         = well_data['county']
    peak_prod_rate = well_data['peak_prod_rate']
    prod_start     = well_data['prod_start']
    prod_comm      = well_data['prod_comm']
    prod_rate_unit = PROD_RATE_UNITS[prod_comm]

    param_str      = "API_Number, Operator, State_Well_Direction, County_Code, Lateral_Length_ft, True_Vertical_Depth_ft, Peak_{}_Prod_Rate_{}, Production_Start_Year".format(prod_comm, prod_rate_unit)
    sql_where      = "State_Name='{}' AND (ISNULL(Peak_{}_Prod_Rate_{},0) BETWEEN {} AND {}) AND Commodity='{}' AND ISNULL({},0) > 0".format(state_name, prod_comm, prod_rate_unit, 0.5*float(peak_prod_rate), 1.5*float(peak_prod_rate), prod_comm, len_col)
    well_analogue_data = gd.get_data(param_str, 'dbo.tblUSWell_Parameters', cursor=curr, server='sql_server', database='US_Wells', datatype='plural', sql_where=sql_where)
    operator_analogues = [data for data in well_analogue_data if data[1] == operator]
    if operator_analogues:
        analogue_pool = operator_analogues
    else:
        analogue_pool = well_analogue_data
    i = 1
    while i <= 5 and not analogue_wells:
        prod_rate_analogues = [data for data in analogue_pool if (peak_prod_rate*(1-(0.1*i))) <= data[6] <= (peak_prod_rate*(1+(0.1*i)))]
        if prod_rate_analogues:
            prod_rate_analogues_a = [data for data in prod_rate_analogues if data[3] == county]
            if prod_rate_analogues_a:
                prod_rate_analogues_b = [data for data in prod_rate_analogues_a if (prod_start-2) <=  data[7] <= (prod_start+2)]
                if prod_rate_analogues_b:
                    analogue_wells = prod_rate_analogues_b
                else:
                    analogue_wells = prod_rate_analogues_a
            else:
                prod_rate_analogues_c = [data for data in prod_rate_analogues if (prod_start-2) <=  data[7] <= (prod_start+2)]
                if prod_rate_analogues_c:
                    analogue_wells = prod_rate_analogues_c
                else:
                    analogue_wells = prod_rate_analogues
        else:
            i += 1
    if debug: print analogue_pool
    calc_len = 0
    if analogue_pool:
        if len(analogue_pool) == 1:
            avg_ppr     = analogue_pool[0][6]
            if len_col == 'Lateral_Length_ft':
                avg_len = analogue_pool[0][4]
            else:
                avg_len = analogue_pool[0][5]
        else:
            avg_ppr     = gd.get_median([data[6] for data in analogue_pool])
            if len_col == 'Lateral_Length_ft':
                avg_len = gd.get_median([data[4] for data in analogue_pool])
            else:
                avg_len = gd.get_median([data[5] for data in analogue_pool])
        if avg_ppr > 0:
            calc_len = (float(peak_prod_rate)/float(avg_ppr))*float(avg_len)
    return calc_len


def est_length_params(curr, debug=False):
    sql_update = "UPDATE tblUSWell_Parameters SET {}={} WHERE API_Number='{}'"
    param_str = "API_Number, Operator, State_name, County_Code, Peak_Oil_Prod_Rate_bd, Peak_Gas_Prod_Rate_mmcfd, Production_Start_Year, Commodity"

    # Estimate Lateral Length values --------------------------------------------------------------------------------------------------------------------------------------
    sql_where = "State_Well_Direction='Horizontal' AND ISNULL(Lateral_Length_ft,0)=0 AND (Commodity='OIL' OR Commodity='GAS') AND Forecast_Well=3"
    well_param_data = gd.get_data(param_str, 'dbo.tblUSWell_Parameters', cursor=curr, server='sql_server', database='US_Wells', datatype='plural', sql_where=sql_where)
    data_count = len(well_param_data)
    datarow = 1
    for api_number, operator, state_name, county, peak_oil_rate, peak_gas_rate, prod_start, prod_comm in well_param_data:
        well_data = {}
        print ''
        print 'Lateral Length Est. -- {}/{}: {}'.format(datarow, data_count, api_number)
        if prod_comm == 'OIL':
            peak_prod_rate = peak_oil_rate
        else:
            peak_prod_rate = peak_gas_rate
        well_data['operator']       = operator
        well_data['state_name']     = state_name
        well_data['county']         = county
        well_data['peak_prod_rate'] = peak_prod_rate
        well_data['prod_start']     = prod_start
        well_data['prod_comm']      = prod_comm
        calc_lat_len = calc_length_est(curr, well_data, len_col='Lateral_Length_ft', debug=debug)
        if debug: print sql_update.format('Lateral_Length_ft', calc_lat_len, api_number)
        curr.execute(sql_update.format('Lateral_Length_ft', calc_lat_len, api_number))
        gd.commit(curr)
        datarow += 1

    # Estimate True Vertical Depth values ---------------------------------------------------------------------------------------------------------------------------------
    sql_where = "State_Well_Direction='Vertical' AND ISNULL(True_Vertical_Depth_ft,0)=0 AND (Commodity='OIL' OR Commodity='GAS') AND Forecast_Well=3"
    well_param_data = gd.get_data(param_str, 'dbo.tblUSWell_Parameters', cursor=curr, server='sql_server', database='US_Wells', datatype='plural', sql_where=sql_where)
    data_count = len(well_param_data)
    datarow = 1
    for api_number, operator, state_name, county, peak_oil_rate, peak_gas_rate, prod_start, prod_comm in well_param_data:
        well_data = {}
        print ''
        print 'True Vertical Depth Est. -- {}/{}: {}'.format(datarow, data_count, api_number)
        if prod_comm == 'OIL':
            peak_prod_rate = peak_oil_rate
        else:
            peak_prod_rate = peak_gas_rate
        well_data['operator']       = operator
        well_data['state_name']     = state_name
        well_data['county']         = county
        well_data['peak_prod_rate'] = peak_prod_rate
        well_data['prod_start']     = prod_start
        well_data['prod_comm']      = prod_comm
        calc_tvd = calc_length_est(curr, well_data, len_col='True_Vertical_Depth_ft', debug=debug)
        if debug: print sql_update.format('True_Vertical_Depth_ft', calc_tvd, api_number)
        curr.execute(sql_update.format('True_Vertical_Depth_ft', calc_tvd, api_number))
        gd.commit(curr)
        datarow += 1


def tx_lease_to_well_prod(debug=False):
    conn = gd.get_connection(server='mysql', database='us_wells')
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
    UPDATE tx_oil_well_production AS a, tx_oil_data AS b 
      SET a.oil_{0}_bbl=b.well_allowable_pct, a.csgd_{0}_mcf=b.well_allowable_pct
      WHERE b.prod_month='{0}' AND a.prod_year={1} AND b.prod_year={1} AND a.tx_well_id='{2}' AND b.tx_well_id='{2}'
    '''
    well_data = gd.get_data('tx_well_id, lease_id, prod_year', 'tx_oil_well_production', database='us_wells', cursor=curr, datatype='plural', sql_where="process_code={} AND prod_year=2018".format(PROCESS_CODE))
    well_data_count = len(well_data)
    well_data_num = 1
    for tx_well_id, lease_id, prod_year in well_data:
        well_prod_months = gd.get_data('prod_month', 'tx_oil_data', database='us_wells', cursor=curr, sql_where='tx_well_id="{}" AND prod_year={} AND well_allowable_pct > 0 AND prod_month="dec"'.format(tx_well_id, prod_year))
        print '{}/{} -- {}% complete'.format(well_data_num,well_data_count, 100*round(float(well_data_num)/float(well_data_count),3))
        if well_prod_months:
            for prod_month in well_prod_months:
                if debug: print sql_update.format(prod_month, prod_year, tx_well_id)
                curr.execute(sql_update.format(prod_month, prod_year, tx_well_id))
                gd.commit(curr)
            sql_update_2_ = \
            '''
                UPDATE tx_oil_well_production AS a, 
                   (SELECT SUM(oil_jan_bbl) AS total_oil_jan_bbl, 
                           SUM(oil_feb_bbl) AS total_oil_feb_bbl,
                           SUM(oil_mar_bbl) AS total_oil_mar_bbl,
                           SUM(oil_apr_bbl) AS total_oil_apr_bbl,
                           SUM(oil_may_bbl) AS total_oil_may_bbl,
                           SUM(oil_jun_bbl) AS total_oil_jun_bbl,
                           SUM(oil_jul_bbl) AS total_oil_jul_bbl,
                           SUM(oil_aug_bbl) AS total_oil_aug_bbl,
                           SUM(oil_sep_bbl) AS total_oil_sep_bbl,
                           SUM(oil_oct_bbl) AS total_oil_oct_bbl,
                           SUM(oil_nov_bbl) AS total_oil_nov_bbl,
                           SUM(oil_dec_bbl) AS total_oil_dec_bbl,
                           SUM(csgd_jan_mcf) AS total_csgd_jan_mcf,
                           SUM(csgd_feb_mcf) AS total_csgd_feb_mcf,
                           SUM(csgd_mar_mcf) AS total_csgd_mar_mcf,
                           SUM(csgd_apr_mcf) AS total_csgd_apr_mcf,
                           SUM(csgd_may_mcf) AS total_csgd_may_mcf,
                           SUM(csgd_jun_mcf) AS total_csgd_jun_mcf,
                           SUM(csgd_jul_mcf) AS total_csgd_jul_mcf,
                           SUM(csgd_aug_mcf) AS total_csgd_aug_mcf,
                           SUM(csgd_sep_mcf) AS total_csgd_sep_mcf,
                           SUM(csgd_oct_mcf) AS total_csgd_oct_mcf,
                           SUM(csgd_nov_mcf) AS total_csgd_nov_mcf,
                           SUM(csgd_dec_mcf) AS total_csgd_dec_mcf
                     FROM tx_well_production WHERE lease_id='{1}' AND prod_year={2} AND tx_well_id IS NULL) AS b  
                SET a.oil_jan_bbl=(a.oil_jan_bbl*IFNULL(b.total_oil_jan_bbl,0)),
                    a.oil_feb_bbl=(a.oil_feb_bbl*IFNULL(b.total_oil_feb_bbl,0)),
                    a.oil_mar_bbl=(a.oil_mar_bbl*IFNULL(b.total_oil_mar_bbl,0)),
                    a.oil_apr_bbl=(a.oil_apr_bbl*IFNULL(b.total_oil_apr_bbl,0)),
                    a.oil_may_bbl=(a.oil_may_bbl*IFNULL(b.total_oil_may_bbl,0)),
                    a.oil_jun_bbl=(a.oil_jun_bbl*IFNULL(b.total_oil_jun_bbl,0)),
                    a.oil_jul_bbl=(a.oil_jul_bbl*IFNULL(b.total_oil_jul_bbl,0)),
                    a.oil_aug_bbl=(a.oil_aug_bbl*IFNULL(b.total_oil_aug_bbl,0)),
                    a.oil_sep_bbl=(a.oil_sep_bbl*IFNULL(b.total_oil_sep_bbl,0)),
                    a.oil_oct_bbl=(a.oil_oct_bbl*IFNULL(b.total_oil_oct_bbl,0)),
                    a.oil_nov_bbl=(a.oil_nov_bbl*IFNULL(b.total_oil_nov_bbl,0)),
                    a.oil_dec_bbl=(a.oil_dec_bbl*IFNULL(b.total_oil_dec_bbl,0)),
                    a.csgd_jan_mcf=(a.csgd_jan_mcf*IFNULL(b.total_csgd_jan_mcf,0)),
                    a.csgd_feb_mcf=(a.csgd_feb_mcf*IFNULL(b.total_csgd_feb_mcf,0)),
                    a.csgd_mar_mcf=(a.csgd_mar_mcf*IFNULL(b.total_csgd_mar_mcf,0)),
                    a.csgd_apr_mcf=(a.csgd_apr_mcf*IFNULL(b.total_csgd_apr_mcf,0)),
                    a.csgd_may_mcf=(a.csgd_may_mcf*IFNULL(b.total_csgd_may_mcf,0)),
                    a.csgd_jun_mcf=(a.csgd_jun_mcf*IFNULL(b.total_csgd_jun_mcf,0)),
                    a.csgd_jul_mcf=(a.csgd_jul_mcf*IFNULL(b.total_csgd_jul_mcf,0)),
                    a.csgd_aug_mcf=(a.csgd_aug_mcf*IFNULL(b.total_csgd_aug_mcf,0)),
                    a.csgd_sep_mcf=(a.csgd_sep_mcf*IFNULL(b.total_csgd_sep_mcf,0)),
                    a.csgd_oct_mcf=(a.csgd_oct_mcf*IFNULL(b.total_csgd_oct_mcf,0)),
                    a.csgd_nov_mcf=(a.csgd_nov_mcf*IFNULL(b.total_csgd_nov_mcf,0)),
                    a.csgd_dec_mcf=(a.csgd_dec_mcf*IFNULL(b.total_csgd_dec_mcf,0))
                WHERE a.tx_well_id='{0}' AND a.lease_id='{1}' AND a.prod_year={2}
                '''
            sql_update_2 = \
            '''
                UPDATE tx_oil_well_production AS a, 
                   (SELECT SUM(oil_dec_bbl) AS total_oil_dec_bbl,
                           SUM(csgd_dec_mcf) AS total_csgd_dec_mcf
                     FROM tx_well_production WHERE lease_id='{1}' AND prod_year={2} AND tx_well_id IS NULL) AS b  
                SET a.oil_dec_bbl=(a.oil_dec_bbl*IFNULL(b.total_oil_dec_bbl,0)),
                    a.csgd_dec_mcf=(a.csgd_dec_mcf*IFNULL(b.total_csgd_dec_mcf,0))
                WHERE a.tx_well_id='{0}' AND a.lease_id='{1}' AND a.prod_year={2}
                '''
            if debug: print sql_update_2.format(tx_well_id, lease_id, prod_year)
            curr.execute(sql_update_2.format(tx_well_id, lease_id, prod_year))
            gd.commit(curr)
        well_data_num += 1
    curr.close()
    conn.close()


def fix_tx_oil_prod(debug=False):
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
    #sql_delete = 'DELETE FROM tx_oil_well_production WHERE lease_id="{}" AND prod_year={}'
    #sql_update = 'UPDATE tx_oil_data SET process_code={} WHERE lease_id="{}" AND prod_year={}'
    #sql_select = \
    #'''
    #SELECT DISTINCT c.lease_id, c.prod_year
    #  FROM (SELECT a.lease_id, a.prod_year, a.well_count AS oil_data_well_count, b.well_count AS oil_production_well_count
    #    FROM (SELECT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS well_count FROM tx_oil_data GROUP BY lease_id, prod_year) AS a,
    #         (SELECT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS well_count FROM tx_oil_well_production GROUP BY lease_id, prod_year) AS b
    #    WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year) AS c
    #  WHERE NOT c.oil_data_well_count=c.oil_production_well_count
    #'''
    sql_insert = \
    '''
    INSERT INTO tx_oil_well_production (lease_id, tx_well_id, api_number, lease_no, well_no, district_no, county_no, prod_year, lease_dist_api_wellno, process_code)
      (SELECT DISTINCT lease_id, tx_well_id, well_api, lease_no, well_no, district_no, SUBSTRING(well_api,3,3), prod_year, lease_dist_api_wellno, process_code FROM tx_oil_data
       WHERE process_code={}
       ORDER BY tx_well_id, prod_year)
    '''
    #curr.execute(sql_select)
    #datapoints = curr.fetchall()
    #lease_prod_data = list(datapoints)
    #data_count = len(lease_prod_data)
    #data_num = 1
    #for lease_id, prod_year in lease_prod_data:
    #    print '{}/{} -- {} {}'.format(data_num, data_count, lease_id, prod_year)
    #    curr.execute(sql_update.format(PROCESS_CODE, lease_id, prod_year))
    #    gd.commit(curr)
    #    curr.execute(sql_delete.format(lease_id, prod_year))
    #    gd.commit(curr)
    #    data_num += 1
    curr.execute(sql_insert.format(PROCESS_CODE))
    gd.commit(curr)
    curr.close()
    conn.close()


def update_texas_details(curr, debug=False):
    DISTRICT_MAP = {
         '1': '01',
         '2': '02',
         '3': '03',
         '4': '04',
         '5': '05',
         '6': '06',
        '6E': '07',
        '7B': '08',
        '7C': '09',
         '8': '10',
        '8A': '11',
        '8B': '12',
        '09': '13',
        '10': '14'
    }
    sql_update = "UPDATE tblUSWell_Texas_Details SET District_No='{}', Well_No='{}' WHERE Reported_API_Number='{}'"
    well_lease_ids = gd.get_data('Reported_API_Number', 'dbo.tblUSWell_Texas_Details', server='sql_server', database='US_Wells', cursor=curr, sql_where="Reported_API_Number LIKE 'OL%' OR Reported_API_Number LIKE 'GL%'")

    data_count = len(well_lease_ids)
    data_num = 1
    for well_lease_id in well_lease_ids:
        print '{}/{}'.format(data_num, data_count)
        try:
            dash_count = well_lease_id.count('-')
            district_name = well_lease_id.split('-')[1]
            well_no = well_lease_id.split('-')[dash_count]
            district_no = DISTRICT_MAP[district_name]
            if debug: print '{}'.format(sql_update.format(district_no, well_no, well_lease_id))
            curr.execute(sql_update.format(district_no, well_no, well_lease_id))
            gd.commit(curr)
        except:
            print well_lease_id
        data_num += 1

def main(lease_well=False, calc_len=False, fix_prod=False, update_details=False, debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells')
    curr = conn.cursor()
    if fix_prod:
        fix_tx_oil_prod(debug=debug)
    if lease_well:
        tx_lease_to_well_prod(debug=debug)
    if calc_len:
        est_length_params(curr, debug=debug)
    if update_details:
        update_texas_details(curr, debug=debug)
    curr.close()
    conn.close()

if __name__=='__main__':
    # start time 12:50am 09-24-2019
    main(fix_prod=False, lease_well=True, update_details=False)