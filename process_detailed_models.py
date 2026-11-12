from globaldata import *
from win32com.client import Dispatch
import data_export as de
import shutil


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

def generate_model_list():
    detailed_model_ids = get_data('asset_id', 'detailed_model_data', datatype='int')
    model_data_source_ids = get_data('asset_id', 'assets', datatype='int', sql_where='data_source="Model"')
    uncon_model_ids = get_data('asset_id', 'model_rules', sql_where='param_name="FISCAL" AND param_value LIKE "%Resource%"', datatype='int')
    detailed_model_ids = [asset_id for asset_id in detailed_model_ids if (asset_id not in uncon_model_ids and asset_id in model_data_source_ids)]
    with open(TEST_DIR + 'DT_1.csv', 'w') as csvfile:
        fieldnames = ['ASSET_ID', 'COUNTRY', 'CONSTITUENT', 'REGION', 'STATUS', 'TERRAIN', 'RESOURCE', 'FACILITY', 'BASIN', 'OPERATOR']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        for asid in detailed_model_ids:
            writer.writerow({'ASSET_ID': asid})
    shutil.copy2(TEST_DIR + 'DT_1.csv', MODEL_TASK_DIR+'DT_1.csv')

def create_detailed_models():
    move_files(DET_MD_NEW_DIR, DET_MD_PRC_DIR)
    move_files(DET_MD_NBE_DIR, DET_MD_PBE_DIR)
    os.system('%py2% %engine_drive%:\\python_code\\cmd_main.py create_model -detm-')#--commented on July 30-2024.uncomment after debug
    os.system('%py2% %engine_drive%:\\python_code\\cmd_main.py update_econ_data -aob')#--commented on July 30-2024.uncomment after debug

def exec_breakeven_macro():
    # os.system('%py2% %engine_drive%:\\python_code\\cmd_main.py update_econ_data -aob')
    copy_files(DET_MD_NEW_DIR, DET_MD_NBE_DIR, in_ext='xlsx', out_ext='xlsx')
    xlApp = Dispatch("Excel.Application")
    wb = xlApp.Workbooks.Open(Filename=BREAKEVEN_DIR + "Breakeven_Detailed.xlsm")
    xlApp.Application.Run("Breakeven_Detailed.xlsm!Module1.ProcessFolderBreakevens")
    wb.SaveAs(BREAKEVEN_DIR + "Breakeven_Detailed.xlsm")
    xlApp.Application.Quit()
    del xlApp

def extract_detailed_model_data(clear_int_tables=False):
    print 'Extract analytics parameters from detailed models ...'
    os.system('%py2% %engine_drive%:\\python_code\\cmd_main.py extract_detailed_econ_data')

    print 'Extracting data from detailed models ...'
    table_names = [
        'AssetSenRemainingNPV',
        'CashFlowData',
        'CommodityPriceSourceData',
        'DataPoints',
        'FEATData',
        'FEATData_Extn',
        'ProductionData',
        'WellInputInfo',
        'WellDataInfo',
        'WellInputproductionInfo'
    ]
    de.data_export(regions=['detailed'], region_dir=DET_MD_NEW_DIR, clear=clear_int_tables)

    conn = get_connection(server='sql_server', database='OGEngineDataExtract')
    curr = conn.cursor()
    sql_update = "UPDATE OGEngineDataExtract.Engine.tblEngine{} SET DetailedModel='Model'"
    for db_table in table_names:
        curr.execute(sql_update.format(db_table))
        commit(curr)
    curr.close()
    conn.close()

def export_detailed_model_data(clear_ext_tables=False):
    print 'Exporting detailed model data ...'
    de.update_servers('oilgas', export_tables=True, import_tables=True, truncate=clear_ext_tables)


def main(run_full_process=False, import_data=False, update_data=False, update_prices=False, list_models=False, create_models=False, run_breakeven=False, extract_data=False, export_data=False, clear_int_tables=False, clear_ext_tables=False, external_server=True):
    in_conn = get_connection()
    in_curr = in_conn.cursor()
    out_conn = get_connection(server='sql_server', database='OGEngineDataExtract', external=external_server)
    out_curr = out_conn.cursor()

    if import_data or run_full_process:
        print 'Importing detailed model data ...'
        detailed_model_data = import_detailed_model_data(out_curr)
        if update_data or run_full_process:
            print 'Updating detailed_model_data table ...'
            update_detailed_model_data(in_curr, detailed_model_data)
    if update_prices or run_full_process:
        print 'Updating detalied model price codes ...'
        update_pricing(in_curr, out_curr)

    if list_models or run_full_process:
        print 'Generating list of detailed models ...'
        generate_model_list()

    if create_models or run_full_process:
        print 'Creating detailed models ...'
        create_detailed_models()

    if run_breakeven or run_full_process:
        print 'Running breakeven macro on detailed models ...'
        exec_breakeven_macro()

    if extract_data or run_full_process:
        print 'Extracting detailed model data ...'
        extract_detailed_model_data(clear_int_tables)

    if export_data or run_full_process:
        print 'Exporting detailed model data ...'
        export_detailed_model_data(clear_ext_tables)


    out_curr.close()
    out_conn.close()
    in_curr.close()
    in_conn.close()

if __name__=='__main__':
    main(
        run_full_process = True,
        import_data      = True,
        update_data      = True,
        update_prices    = True,
        list_models      = True,
        create_models    = True,
        run_breakeven    = True,
        extract_data     = True,
        export_data      = True,
        clear_int_tables = True,
        clear_ext_tables = True,
        external_server  = True
    )
