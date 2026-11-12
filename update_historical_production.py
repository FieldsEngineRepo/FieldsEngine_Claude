import globaldata as gd

MONTH_NAMES = {
     1: 'Jan',
     2: 'Feb',
     3: 'Mar',
     4: 'Apr',
     5: 'May',
     6: 'Jun',
     7: 'Jul',
     8: 'Aug',
     9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}


def main(insert=False, update=False, debug=False):
    sql_inserts= \
    """
    INSERT INTO tblUSWell_Production_Historical (WellID, API_Number, ProductionDate, Production_Year, Production_Month, Oil_bbl, Gas_mcf, Condensate_bbl, NGL_bbl, Water_bbl, Source, CreatedBy, CreatedOn, ModifiedOn, Pkgid)
      (SELECT DISTINCT WellID, API_Number, ProductionDate, Production_Year, Production_Month, Oil_bbl, Gas_mcf, Condensate_bbl, NGL_bbl, Water_bbl, Source, CreatedBy, CreatedOn, ModifiedOn, Pkgid
       FROM tblUSWell_Production_Historical_Update);

    TRUNCATE TABLE tblUSWell_Production_Historical_Update;
    
    INSERT INTO tblUSWell_Production (WellID, API_Number, [Period], WellProdID) (SELECT DISTINCT WellID, API_Number, Production_Year, WellProdID FROM tblUSWell_Production_Historical);
    """
    sql_update = \
    '''
    UPDATE tblUSWell_Production 
      SET Gas_{0}_MCF=ISNULL(b.Gas_mcf,0),
          Oil_{0}_BBL=ISNULL(b.Oil_bbl,0),
          NGL_{0}_BBL=ISNULL(b.NGL_bbl,0),
          Condensate_{0}_BBL=ISNULL(b.Condensate_bbl,0),
          Water_{0}_BBL=ISNULL(b.Water_bbl,0)
      FROM tblUSWell_Production a, tblUSWell_Production_Historical b
      WHERE a.WellProdID=b.WellProdID AND a.API_Number=b.API_Number AND b.Production_Month={1};
    '''
    sql_update_id_data = \
    '''
    UPDATE tblUSWell_Production 
      SET PkgId=b.Max_PkgId,
          WellProductionID=b.Max_HistoricID,
          Source='Historical',
          CreatedBy='Engine',
          CreatedOn='{}'
      FROM tblUSWell_Production a,
           (SELECT DISTINCT WellID, Production_Year, MAX(PkgId) AS Max_PkgId, MAX(WellProductionHistoricID) AS Max_HistoricID FROM tblUSWell_Production_Historical GROUP BY WellID, Production_Year) b 
      WHERE a.WellID=b.WellID AND a.[Period]=b.Production_Year;
    '''
    sql_update_api = \
    '''
    UPDATE tblUSWell_Production 
      SET API_14=b.API_14
      FROM tblUSWell_Production a, tblUSWell_Details b 
      WHERE a.WellID=b.WellID AND a.API_14 IS NULL;
    '''
    sql_update_prod_totals = \
    '''
    UPDATE US_Wells.dbo.tblUSWell_Production
      SET Gas_TOTAL_mcf=ROUND(ISNULL(Gas_Jan_mcf,0) + ISNULL(Gas_Feb_mcf,0) + ISNULL(Gas_Mar_mcf,0) + ISNULL(Gas_Apr_mcf,0) + ISNULL(Gas_May_mcf,0) + ISNULL(Gas_Jun_mcf,0) + ISNULL(Gas_Jul_mcf,0) + ISNULL(Gas_Aug_mcf,0) + ISNULL(Gas_Sep_mcf,0) + ISNULL(Gas_Oct_mcf,0) + ISNULL(Gas_Nov_mcf,0) + ISNULL(Gas_Dec_mcf,0),2),
	      Oil_TOTAL_bbl=ROUND(ISNULL(Oil_Jan_bbl,0) + ISNULL(Oil_Feb_bbl,0) + ISNULL(Oil_Mar_bbl,0) + ISNULL(Oil_Apr_bbl,0) + ISNULL(Oil_May_bbl,0) + ISNULL(Oil_Jun_bbl,0) + ISNULL(Oil_Jul_bbl,0) + ISNULL(Oil_Aug_bbl,0) + ISNULL(Oil_Sep_bbl,0) + ISNULL(Oil_Oct_bbl,0) + ISNULL(Oil_Nov_bbl,0) + ISNULL(Oil_Dec_bbl,0),2),
		  Water_TOTAL_bbl=ROUND(ISNULL(Water_Jan_bbl,0) + ISNULL(Water_Feb_bbl,0) + ISNULL(Water_Mar_bbl,0) + ISNULL(Water_Apr_bbl,0) + ISNULL(Water_May_bbl,0) + ISNULL(Water_Jun_bbl,0) + ISNULL(Water_Jul_bbl,0) + ISNULL(Water_Aug_bbl,0) + ISNULL(Water_Sep_bbl,0) + ISNULL(Water_Oct_bbl,0) + ISNULL(Water_Nov_bbl,0),0) + ISNULL(Water_Dec_bbl,2),
          NGL_TOTAL_bbl=ROUND(ISNULL(NGL_Jan_bbl,0) + ISNULL(NGL_Feb_bbl,0) + ISNULL(NGL_Mar_bbl,0) + ISNULL(NGL_Apr_bbl,0) + ISNULL(NGL_May_bbl,0) + ISNULL(NGL_Jun_bbl,0) + ISNULL(NGL_Jul_bbl,0) + ISNULL(NGL_Aug_bbl,0) + ISNULL(NGL_Sep_bbl,0) + ISNULL(NGL_Oct_bbl,0) + ISNULL(NGL_Nov_bbl,0) + ISNULL(NGL_Dec_bbl,0),2),
          Condensate_TOTAL_bbl=ROUND(ISNULL(Condensate_Jan_bbl,0) + ISNULL(Condensate_Feb_bbl,0) + ISNULL(Condensate_Mar_bbl,0) + ISNULL(Condensate_Apr_bbl,0) + ISNULL(Condensate_May_bbl,0) + ISNULL(Condensate_Jun_bbl,0) + ISNULL(Condensate_Jul_bbl,0) + ISNULL(Condensate_Aug_bbl,0) + ISNULL(Condensate_Sep_bbl,0) + ISNULL(Condensate_Oct_bbl,0) + ISNULL(Condensate_Nov_bbl,0) + ISNULL(Condensate_Dec_bbl,0),2)
    '''
    conn = gd.get_connection(server='sql_server', database='US_Wells')
    curr = conn.cursor()
    if insert:
        print '{} Inserting Production Data ...'.format(gd.get_datetime())
        if debug:
            print sql_inserts
        curr.execute(sql_inserts)
        gd.commit(curr)
        print '{} Production Data Insert Complete'.format(gd.get_datetime())
    if update:
        for prod_month in sorted(MONTH_NAMES.keys()):
            print '{} Updating Production Data for {} ...'.format(gd.get_datetime(), MONTH_NAMES[prod_month])
            if debug:
                print sql_update.format(MONTH_NAMES[prod_month], prod_month)
            curr.execute(sql_update.format(MONTH_NAMES[prod_month], prod_month))
            gd.commit(curr)
            print '{} Production Data Update for {}'.format(gd.get_datetime(), MONTH_NAMES[prod_month])
        #-------------------------------------------------------------------------------------------------------------------
        update_time = gd.get_datetime()
        print '{} Updating Production ID Data ...'.format(update_time)
        if debug:
            print sql_update_id_data.format(update_time)
        curr.execute(sql_update_id_data.format(update_time))
        gd.commit(curr)
        print '{} Production ID Data Update Complete'.format(gd.get_datetime())
        #-------------------------------------------------------------------------------------------------------------------
        print '{} Updating API 14 Data ...'.format(gd.get_datetime())
        if debug:
            print sql_update_api
        curr.execute(sql_update_api)
        gd.commit(curr)
        print '{} API 14 Data Update Complete'.format(gd.get_datetime())
        #-------------------------------------------------------------------------------------------------------------------
        print '{} Updating Production Totals ...'.format(gd.get_datetime())
        if debug:
            print sql_update_prod_totals
        curr.execute(sql_update_prod_totals)
        gd.commit(curr)
        print '{} Production Totals Update Complete'.format(gd.get_datetime())
    curr.close()
    conn.close()


if __name__=='__main__':
    main(insert=False, update=True, debug=False)

