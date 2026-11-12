from globaldata import *


def import_detailed_model_data(out_curr):
    sql_select = \
    """
    SELECT AssetID,Year,[E&A (US$)],[Tangibles (US$)],[Intangibles (US$)],[Abandonment (US$)],[Fixed (US$)],[Variable (US$)],[Payments (US$)],[Receipts (US$)] FROM tblFEATDataInput WHERE NOT Year='NULL'
    """
    out_curr.execute(sql_select)
    detailed_model_data = out_curr.fetchall()
    processed_data = ()
    for data_row in detailed_model_data:
        processed_row = ()
        for data_point in data_row:
            if isinstance(data_point,str):
                data_point = unicode(data_point.strip(), errors='ignore')
            processed_row += (data_point,)
        processed_data += (processed_row,)
    return processed_data

def update_detailed_model_data(in_curr, detailed_model_data):
    truncate_table(table='detailed_model_data')

    sql_statement  = 'INSERT INTO detailed_model_data (asset_id, period, e_and_a, tangible_capex, intangible_capex, abandonment, fixed_opex, variable_opex, payments, receipts) '
    sql_statement += 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    for param_vals in detailed_model_data:
        in_curr.execute(sql_statement,param_vals)
    in_curr.execute('COMMIT')

def update_pricing(in_curr, out_curr):
    price_changes = [('Contracted Gas Price', 'Iran Domestic Gas', 'NaturalGas'),
                     ('Tittle Transfer Facility', 'Title Transfer Facility Gas', 'NaturalGas'),
                     ('OLMECA', 'Istmo Crude', 'CrudeOil'),
                     ('Kazakhstan Export Price', 'Turkmenistan Export Gas', 'NaturalGas'),
                     ('Dilbit Blend', 'Alberta BVM Hardisty Bitumen',  'CrudeOil'),
                     ('European Union Import Gas', 'Europa Landed LNG', 'LNG'),
                     ('Olmeca Crude', 'Istmo Crude', 'CrudeOil'),
                     ('Algeria LNG Export','Algeria NGL Export', 'NGLs')]

    for old_name, new_name, commodity in price_changes:
        sql_update = "UPDATE tblCommodityPriceSourceDataInput SET [{0}]='{1}' WHERE [{0}]='{2}'".format(commodity, new_name, old_name)
        #print sql_update
        out_curr.execute(sql_update)
        commit(out_curr)

    add_date = get_datetime()
    edit_date = add_date
    sql_select = 'SELECT AssetID, CrudeOil, NaturalGas, Condensate, NGLs, LNG FROM tblCommodityPriceSourceDataInput'
    out_curr.execute(sql_select)
    detailed_model_pricing = out_curr.fetchall()
    processed_data = ()
    for data_row in detailed_model_pricing:
        processed_row = ()
        for data_point in data_row:
            if isinstance(data_point,str):
                data_point = unicode(data_point.strip(), errors='ignore')
            processed_row += (data_point,)
        processed_data += (processed_row,)
    sql_price  = 'SELECT price_code FROM prices WHERE price_name="%s" AND commodity="%s"'
    sql_select = 'SELECT * FROM model_rules WHERE param_name="PRICING" AND commodity="%s" AND asset_id=%s'
    sql_update = 'UPDATE model_rules SET param_table="%s" WHERE param_name="PRICING" AND commodity="%s" AND asset_id=%s'
    sql_insert = 'INSERT INTO model_rules (asset_id, country, region, commodity, param_name, param_table, add_by, add_date, edit_by, edit_date) '
    sql_insert += 'VALUES (%s, "%s", "%s", "%s", "PRICING", "%s", "Detailed Model", "%s", "Detailed Model", "%s")'
    for asset_id, pricing_crude, pricing_ng, pricing_condensate, pricing_ngls, pricing_lng in processed_data:
        if pricing_crude is not None and pricing_crude != 'NULL':
            commodity = 'Crude Oil'
            in_curr.execute(sql_price % (pricing_crude, commodity))
            try:
                price_code = in_curr.fetchone()[0]
            except:
                print '%s:   \t %s\t\t %s' % (asset_id, commodity, pricing_crude)
                continue
            if in_curr.execute(sql_select % (commodity, asset_id)):
                in_curr.execute(sql_update % (price_code, commodity, asset_id))
                commit(in_curr)
            else:
                country = get_param(param='country', table='assets', asset_id=asset_id, cur=in_curr)
                region = get_param(param='region', table='assets', asset_id=asset_id, cur=in_curr)
                param_vals = (asset_id, country, region, commodity, price_code, add_date, edit_date)
                in_curr.execute(sql_insert % param_vals)
                commit(in_curr)
        if pricing_ng is not None and pricing_ng != 'NULL':
            commodity = 'Natural Gas'
            in_curr.execute(sql_price % (pricing_ng, commodity))
            try:
                price_code = in_curr.fetchone()[0]
            except:
                print '%s:   \t %s\t %s' % (asset_id, commodity, pricing_ng)
                continue
            if in_curr.execute(sql_select % (commodity, asset_id)):
                in_curr.execute(sql_update % (price_code, commodity, asset_id))
                commit(in_curr)
            else:
                country = get_param(param='country', table='assets', asset_id=asset_id, cur=in_curr)
                region = get_param(param='region', table='assets', asset_id=asset_id, cur=in_curr)
                param_vals = (asset_id, country, region, commodity, price_code, add_date, edit_date)
                in_curr.execute(sql_insert % param_vals)
                commit(in_curr)
        if pricing_condensate is not None and pricing_condensate != 'NULL':
            commodity = 'Condensate'
            in_curr.execute(sql_price % (pricing_condensate, commodity))
            try:
                price_code = in_curr.fetchone()[0]
            except:
                print '%s:   \t %s\t\t %s' % (asset_id, commodity, pricing_condensate)
                continue
            if in_curr.execute(sql_select % (commodity, asset_id)):
                in_curr.execute(sql_update % (price_code, commodity, asset_id))
                commit(in_curr)
            else:
                country = get_param(param='country', table='assets', asset_id=asset_id, cur=in_curr)
                region = get_param(param='region', table='assets', asset_id=asset_id, cur=in_curr)
                param_vals = (asset_id, country, region, commodity, price_code, add_date, edit_date)
                in_curr.execute(sql_insert % param_vals)
                commit(in_curr)
        if pricing_ngls is not None and pricing_ngls != 'NULL':
            commodity = 'NGLs'
            in_curr.execute(sql_price % (pricing_ngls, commodity))
            try:
                price_code = in_curr.fetchone()[0]
            except:
                print '%s:   \t %s\t\t\t %s' % (asset_id, commodity, pricing_ngls)
                continue
            if in_curr.execute(sql_select % (commodity, asset_id)):
                in_curr.execute(sql_update % (price_code, commodity, asset_id))
                commit(in_curr)
            else:
                country = get_param(param='country', table='assets', asset_id=asset_id, cur=in_curr)
                region = get_param(param='region', table='assets', asset_id=asset_id, cur=in_curr)
                param_vals = (asset_id, country, region, commodity, price_code, add_date, edit_date)
                in_curr.execute(sql_insert % param_vals)
                commit(in_curr)
        if pricing_lng is not None and pricing_lng != 'NULL':
            commodity = 'LNG'
            in_curr.execute(sql_price % (pricing_lng, commodity))
            try:
                price_code = in_curr.fetchone()[0]
            except:
                print '%s:   \t %s\t\t\t %s' % (asset_id, commodity, pricing_lng)
                continue
            if in_curr.execute(sql_select % (commodity, asset_id)):
                in_curr.execute(sql_update % (price_code, commodity, asset_id))
                commit(in_curr)
            else:
                country = get_param(param='country', table='assets', asset_id=asset_id, cur=in_curr)
                region = get_param(param='region', table='assets', asset_id=asset_id, cur=in_curr)
                param_vals = (asset_id, country, region, commodity, price_code, add_date, edit_date)
                in_curr.execute(sql_insert % param_vals)
                commit(in_curr)

    update_assumption_points('model_rules')

def main(import_data=False, update_data=False, update_prices=False, external_server=False):
    in_conn = get_connection()
    in_curr = in_conn.cursor()
    out_conn = get_connection(server='sql_server', database='OGEngineDataExtract', external=external_server)
    # out_conn = get_connection(server='sql_server', database='OG_Effuah', external=external_server) #Change to original DB after Testing
    out_curr = out_conn.cursor()

    if import_data:
        print 'Importing detailed model data ...'
        detailed_model_data = import_detailed_model_data(out_curr)
        if update_data:
            print 'Updating detailed_model_data table ...'
            update_detailed_model_data(in_curr, detailed_model_data)
    if update_prices:
        print 'Updating detalied model price codes ...'
        update_pricing(in_curr, out_curr)

    out_curr.close()
    out_conn.close()
    in_curr.close()
    in_conn.close()

if __name__=='__main__':
    main(import_data=True, update_data=True, update_prices=True, external_server=True)
