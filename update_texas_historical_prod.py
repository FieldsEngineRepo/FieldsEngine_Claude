import globaldata as gd


def main():
    sql_delete = \
    '''
    DELETE FROM tblUSWell_Texas_Historical_Production WHERE [Period]={0} AND TX_Well_ID IN (SELECT DISTINCT tx_well_id FROM tx_hist_well_prod_2 WHERE prod_year={0})
    '''
    sql_insert = \
    '''
    INSERT INTO tblUSWell_Texas_Historical_Production (WellID, tx_well_id, api_number, well_no, oil_gas_code, lease_prod_id, lease_id, lease_no, district_no, county_no, field_no, operator_no, StateID, [Period], oil_total_bbl, gas_total_mcf, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, gas_jan_mcf, gas_feb_mcf, gas_mar_mcf, gas_apr_mcf, gas_may_mcf, gas_jun_mcf, gas_jul_mcf, gas_aug_mcf, gas_sep_mcf, gas_oct_mcf, gas_nov_mcf, gas_dec_mcf)
      (SELECT DISTINCT well_id, tx_well_id, api_number, well_no, oil_gas_code, lease_prod_id, lease_id, lease_no, district_no, county_no, field_no, operator_no, state_id, prod_year, oil_total_bbl, gas_total_mcf, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, gas_jan_mcf, gas_feb_mcf, gas_mar_mcf, gas_apr_mcf, gas_may_mcf, gas_jun_mcf, gas_jul_mcf, gas_aug_mcf, gas_sep_mcf, gas_oct_mcf, gas_nov_mcf, gas_dec_mcf
       FROM tx_hist_well_prod_2 WHERE prod_year={0})
    '''
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
    prod_years = sorted(gd.get_data('prod_year', 'dbo.tx_hist_well_prod_2', server='sql_server', database='US_Wells_Texas', cursor=curr, datatype='int'))
    for prod_year in prod_years:
        print prod_year
        curr.execute(sql_delete.format(prod_year))
        gd.commit(curr)
        curr.execute(sql_insert.format(prod_year))
        gd.commit(curr)
    curr.close()
    conn.close()


if __name__=='__main__':
    main()

