from calc_breakevens import *


def store_econ_values(curr, econReserveMin, asset_id):
    sql_update = 'UPDATE asset_data SET min_econ_res_oil=%s, min_econ_res_gas=%s WHERE asset_id=%s'
    curr.execute(sql_update, (econReserveMin, econReserveMin, asset_id))
    curr.execute('COMMIT')


def get_asset_data(assetInputs, fiscalInputs):
    oilData = assetInputs.range("H24:H134")
    condensateData = assetInputs.range("J24:J134")
    gasData = assetInputs.range("I24:I134")
    LNGData = assetInputs.range("L24:L134")
    fiscalData = fiscalInputs.range("B6:I206")
    return oilData, condensateData, gasData, LNGData, fiscalData


def auto_fill(dataSheet, factorCell, formulaStart, outCol, outRowStart, outRowEnd):
    formula_array = tuple(['=%s%s*%s' % (outCol, i, factorCell) for i in range(formulaStart, formulaStart + (outRowEnd-outRowStart) + 1)])
    formula_range = '%s%s:%s%s' % (outCol, outRowStart, outCol, outRowEnd)
    dataSheet.range(formula_range).formula = formula_array


def minimum_econ_reserves(curr, asset_file, run_id, xlApp):
    colNames = 'BCDEFGHI'
    xlWb = xlApp.books.open(asset_file)

    assetInputs      = xlWb.sheets['Asset Inputs']
    assetSensitivity = xlWb.sheets['Asset Sensitivity']
    assetSummary     = xlWb.sheets['Asset Summary']

    goalSeekReset = 0
    econReserveMin = 0

    currYear = get_date()[:4]
    asset_id = assetInputs.range("B1").raw_value

    oilData        = assetInputs.range("B24:B134")
    condensateData = assetInputs.range("D24:D134")
    gasData        = assetInputs.range("C24:C134")
    LNGData        = assetInputs.range("F24:F134")

    assetInputs.range("B144:B254").raw_value = oilData.raw_value
    assetInputs.range("C144:C254").raw_value = gasData.raw_value
    assetInputs.range("D144:D254").raw_value = condensateData.raw_value
    assetInputs.range("F144:F254").raw_value = LNGData.raw_value

    assetInputs.range("K4").raw_value = 1

    for col in 'BCDF':
        auto_fill(assetInputs, '$K$4', 144, col, 24, 134)

    try:
        goal_seek(4, 11, 49, 2, assetInputs, assetSensitivity, xlApp)
        econReserveMin = assetInputs.range("E4").raw_value
    except:
        econReserveMin = 999999999

    print 'minimum economic reserves: ', econReserveMin

    assetInputs.range("B24:B134").raw_value = oilData.raw_value
    assetInputs.range("C24:C134").raw_value = gasData.raw_value
    assetInputs.range("D24:D134").raw_value = condensateData.raw_value
    assetInputs.range("F24:F134").raw_value = LNGData.raw_value

    assetSummary.range((82, 6)).raw_value = "Minimum Economic Field Size"
    assetSummary.range((83, 6)).raw_value = round(econReserveMin, 3)

    xlWb.save()
    xlWb.close()

    store_econ_values(curr, econReserveMin, asset_id)

    return asset_id


def min_econ_main(region='', asset_list=[], excelApp=None):
    start_time = get_datetime()

    conn = get_connection()
    curr = conn.cursor()

    run_id = get_run_id(curr)

    print 'Start time: %s' % start_time

    if excelApp:
        xlApp = excelApp
    else:
        xlApp = xw.App(visible=False)

    if asset_list:
        asset_models = asset_list
    else:
        asset_models = [model for model in os.listdir(DF_REGIONS + region) if model[0] != '~' and model[-4:] == 'xlsx']

    model_count = len(asset_models)
    asset_num = 0

    for asset_model in asset_models:
        asset_num += 1
        print '\n%s/%s: %s' % (asset_num, model_count, asset_model)

        if asset_list:
            asset_file = asset_model
        else:
            asset_file = DF_REGIONS + region + '\\' + asset_model

        minimum_econ_reserves(curr, asset_file, run_id, xlApp)

    if not excelApp:
        xlApp.quit()
        del xlApp

    curr.close()
    conn.close()

    end_time = get_datetime()
    print 'End time: %s' % end_time

if __name__=='__main__':
    min_econ_main(region="Caribbean")
