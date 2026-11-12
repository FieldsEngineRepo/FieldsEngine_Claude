from globaldata import *
import xlwings as xw

GOAL        = 0
INIT_GUESS  = 10
INIT_INCR   = 15
INCR_MIN    = 0.1
ZERO_range  = 0.1
ITER_MAX    = 100
OUT_DEFAULT = 999999999

CALC_BASE = True
CALC_HIGH = False
CALC_LOW  = False
DEBUG     = True


def check_guess(guess, in_row, in_col, out_row, out_col, assetInputs,  assetSensitivity, excelApp):
    outcome = OUT_DEFAULT
    assetInputs.range((in_row, in_col)).raw_value = guess
    excelApp.calculate()
    outcome = assetSensitivity.range((out_row, out_col)).raw_value
    try:
        ret_val = float(outcome)
    except:
        ret_val = OUT_DEFAULT
    return ret_val


def get_outcome_sign(outcome):
    sign = 1
    if abs(outcome - GOAL) < ZERO_range:
        sign = 0
    elif outcome < GOAL:
        sign = -1
    return sign


def check_plus_minus(guess, in_row, in_col, out_row, out_col, assetInputs, assetSensitivity, excelApp):
    check_val = False
    guess_plus  = check_guess(guess + INCR_MIN, in_row, in_col, out_row, out_col, assetInputs, assetSensitivity, excelApp)
    guess_minus = check_guess(guess - INCR_MIN, in_row, in_col, out_row, out_col, assetInputs, assetSensitivity, excelApp)
    if get_outcome_sign(guess_plus) == -get_outcome_sign(guess_minus):
        check_val = True
    return check_val


def goal_seek(in_row, in_col, out_row, out_col, assetInputs, assetSensitivity, excelApp):
    if DEBUG:
        print 'inside goal_seek'
    goal_reached = False
    breakeven_val = OUT_DEFAULT
    exit_code = 0
    return_code = 0
    iter_count = 1
    while not goal_reached:
        if iter_count == 1:
            last_outcome = check_guess(INIT_GUESS, in_row, in_col, out_row, out_col, assetInputs, assetSensitivity, excelApp)
            outcome = check_guess(INIT_GUESS+INIT_INCR, in_row, in_col, out_row, out_col, assetInputs, assetSensitivity, excelApp)
            last_guess = INIT_GUESS
            last_increment = INIT_INCR
            try:
                increment = float(last_increment * outcome)/float(last_outcome - outcome)
            except:
                iter_count = ITER_MAX
            guess = last_guess + increment
        outcome = check_guess(guess, in_row, in_col, out_row, out_col, assetInputs, assetSensitivity, excelApp)
        sign = get_outcome_sign(outcome)
        if DEBUG:
            print ''
            print 'iteration #:', iter_count
            print 'last_increment:', last_increment
            print 'last_guess:', last_guess
            print 'last_outcome:', last_outcome
            print 'increment:', increment
            print 'guess:', guess
            print 'outcome:', outcome
            print 'sign:', sign
        elif check_plus_minus(guess, in_row, in_col, out_row, out_col, assetInputs, assetSensitivity, excelApp):
            exit_code = 'exit 2'
            breakeven_val = guess
            goal_reached = True
        if sign == 0:
            exit_code = 'exit 1'
            breakeven_val = guess
            goal_reached = True
        elif iter_count >= ITER_MAX:
            exit_code = 'exit 3'
            breakeven_val = OUT_DEFAULT
            goal_reached = True
        else:
            last_guess = guess
            last_increment = increment
            try:
                increment = float(last_increment * outcome) / float(last_outcome - outcome)
            except:
                iter_count = ITER_MAX
            last_outcome = outcome
            guess = last_guess + increment
            iter_count += 1
    if DEBUG:
        print 'exit_code:', exit_code
    return breakeven_val


def copyAllValues(dataWorksheet, inCell, outCol, outRowStart, outRowEnd=134):
    formula_array = (("=%s" % inCell),)*(int(outRowEnd +1) - int(outRowStart))
    range_start = outCol + str(outRowStart)
    range_end = outCol + str(outRowEnd)
    formula_range = '%s:%s' % (range_start, range_end)
    dataWorksheet.range(formula_range).formula = formula_array


def fiscalWrite(fiscalInputs, commodityType, fiscal_discount_row, discount_row, NPVtype, colNames):
    if NPVtype == "R":
        inRow = str(discount_row)
    else:
        inRow = "24"
    if commodityType == "OIL":
        inCol = "H"
    else:
        inCol = "I"

    for i in range(8):
        community_unit = str(fiscalInputs.range((5, i + 2)).raw_value).strip()
        if (commodityType == "OIL" and community_unit[-3:] == "bbl") or (commodityType != "OIL" and len(community_unit) > 0):
            dataCell = '%s%s' % (colNames[i], fiscal_discount_row)
            fiscalInputs.range((fiscal_discount_row, i + 2)).formula = ("='Asset Inputs'!$%s$%s" % (inCol, inRow))
            copyAllValues(fiscalInputs, dataCell, colNames[i], int(fiscal_discount_row + 1), 206)


def get_asset_data(assetInputs, fiscalInputs):
    oilData = assetInputs.range("H24:H134")
    condensateData = assetInputs.range("J24:J134")
    gasData = assetInputs.range("I24:I134")
    LNGData = assetInputs.range("L24:L134")
    fiscalData = fiscalInputs.range("B6:I206")
    return oilData, condensateData, gasData, LNGData, fiscalData


def output_values(assetSummary,baseRemainBEOil,baseRemainBEgas,baseDevBEOil,baseDevBEgas,highRemainBEOil,highRemainBEgas,highDevBEOil,highDevBEgas,lowRemainBEOil,lowRemainBEgas,lowDevBEOil,lowDevBEgas):
    assetSummary.range((83, 4)).raw_value = round(baseRemainBEOil, 3)
    assetSummary.range((83, 2)).raw_value = round(baseDevBEOil, 3)
    assetSummary.range((84, 4)).raw_value = round(highRemainBEOil, 3)
    assetSummary.range((84, 2)).raw_value = round(highDevBEOil, 3)
    assetSummary.range((85, 4)).raw_value = round(lowRemainBEOil, 3)
    assetSummary.range((85, 2)).raw_value = round(lowDevBEOil, 3)
    assetSummary.range((83, 5)).raw_value = round(baseRemainBEgas, 3)
    assetSummary.range((83, 3)).raw_value = round(baseDevBEgas, 3)
    assetSummary.range((84, 5)).raw_value = round(highRemainBEgas, 3)
    assetSummary.range((84, 3)).raw_value = round(highDevBEgas, 3)
    assetSummary.range((85, 5)).raw_value = round(lowRemainBEgas, 3)
    assetSummary.range((85, 3)).raw_value = round(lowDevBEgas, 3)


def store_values(breakeven_output):
    conn = get_connection()
    curr = conn.cursor()
    for output_data in breakeven_output:
        param_vals = output_data
        sql_insert = 'INSERT INTO breakeven_output (asset_id,base_rem_oil,base_rem_gas,base_dev_oil,base_dev_gas,high_rem_oil,high_rem_gas,high_dev_oil,high_dev_gas,low_rem_oil,low_rem_gas,low_dev_oil,low_dev_gas,run_id) '
        sql_insert += 'VALUES (%s)' % (','.join(['%s']*14))
        curr.execute(sql_insert, param_vals)
    curr.execute('COMMIT')
    curr.close()
    conn.close()


def run_breakevens(asset_file, run_id, xlApp):
    colNames = 'BCDEFGHI'
    xlWb = xlApp.books.open(asset_file)

    assetInputs      = xlWb.sheets['Asset Inputs']
    assetSensitivity = xlWb.sheets['Asset Sensitivity']
    assetSummary     = xlWb.sheets['Asset Summary']
    fiscalInputs     = xlWb.sheets['Fiscal Inputs']

    baseRemainBEOil, baseRemainBEgas, baseDevBEOil, baseDevBEgas = (0.0,)*4
    highRemainBEOil, highRemainBEgas, highDevBEOil, highDevBEgas = (0.0,)*4
    lowRemainBEOil,  lowRemainBEgas,  lowDevBEOil,  lowDevBEgas  = (0.0,)*4

    discountYear = get_discount_year()

    assetInputs.range((10, 5)).raw_value = discountYear

    oilData, condensateData, gasData, LNGData, fiscalData = get_asset_data(assetInputs, fiscalInputs)

    asset_id            = int(assetInputs.range((1, 2)).raw_value)
    dev_start_year      = int(assetInputs.range((8, 2)).raw_value)
    prod_start_year     = int(assetInputs.range((10, 2)).raw_value)
    fiscal_start_year   = int(fiscalInputs.range((6, 1)).raw_value)
    
    discount_row        = max(24, 24 + (discountYear - dev_start_year))
    fiscal_row          = int(prod_start_year - fiscal_start_year) + 6
    fiscal_discount_row = int(discountYear - fiscal_start_year) + 6

    try:
        resource_type       = assetInputs.range((14, 2)).raw_value.upper()
    except:
        resource_type = ''

    if resource_type in ["Conventional Oil".upper(), "Unconventional Oil".upper(), "Heavy Oil".upper(),"Oil Sands".upper()]:
        commodity_type = "OIL"

        assetInputs.range((24, 8)).raw_value = 1
        assetInputs.range((25, 8)).raw_value = "=$H$24"

        copyAllValues(assetInputs, "H25", "H", 26)
        copyAllValues(assetInputs, "H25", "J", 24)

        fiscalWrite(fiscalInputs, "OIL", fiscal_row, 0, "N", colNames)
        # ----------------------------------------------------------------------------------
        print 'Calculating development oil breakevens ...'
        if CALC_BASE:
            try:
                baseDevBEOil = goal_seek(24, 8, 49, 2, assetInputs, assetSensitivity, xlApp)
            except:
                baseDevBEOil = OUT_DEFAULT
            print 'baseDevBEOil:', baseDevBEOil
        # ----------------------------------------------------------------------------------
        if CALC_HIGH:
            try:
                highDevBEOil = goal_seek(24, 8, 50, 2, assetInputs, assetSensitivity, xlApp)
            except:
                highDevBEOil = OUT_DEFAULT
            print 'highDevBEOil:', highDevBEOil
        # ----------------------------------------------------------------------------------
        if CALC_LOW:
            try:
                lowDevBEOil  = goal_seek(24, 8, 51, 2, assetInputs, assetSensitivity, xlApp)
            except:
                lowDevBEOil = OUT_DEFAULT
            print 'lowDevBEOil:', lowDevBEOil
        # ----------------------------------------------------------------------------------
        assetInputs.range("H24:H134").raw_value = oilData.raw_value
        assetInputs.range("J24:J134").raw_value = condensateData.raw_value
        fiscalInputs.range("B6:I206").raw_value = fiscalData.raw_value
        # ----------------------------------------------------------------------------------
        assetInputs.range((discount_row + 1, 8)).formula = "=$H$%s" % discount_row

        dataCell = "$H$%s" % (discount_row + 1)
        copyAllValues(assetInputs, dataCell, "H", int(discount_row + 2))
        copyAllValues(assetInputs, dataCell, "J", int(discount_row))

        fiscalWrite(fiscalInputs, "OIL", fiscal_discount_row, str(discount_row), "R", colNames)
        # ----------------------------------------------------------------------------------
        print 'Calculating remaining oil breakevens ...'
        if CALC_BASE:
            try:
                baseRemainBEOil = goal_seek(discount_row, 8, 49, 3, assetInputs, assetSensitivity, xlApp)
            except:
                baseRemainBEOil = OUT_DEFAULT
            print 'baseRemainBEOil:', baseRemainBEOil
        # ----------------------------------------------------------------------------------
        if CALC_HIGH:
            try:
                highRemainBEOil = goal_seek(discount_row, 8, 50, 3, assetInputs, assetSensitivity, xlApp)
            except:
                highRemainBEOil = OUT_DEFAULT
            print 'highRemainBEOil:', highRemainBEOil
        # ----------------------------------------------------------------------------------
        if CALC_LOW:
            try:
                lowRemainBEOil  = goal_seek(discount_row, 8, 51, 3, assetInputs, assetSensitivity, xlApp)
            except:
                lowRemainBEOil = OUT_DEFAULT
            print 'lowRemainBEOil:', lowRemainBEOil
        # ----------------------------------------------------------------------------------
        assetInputs.range("H24:H134").raw_value = oilData.raw_value
        assetInputs.range("J24:J134").raw_value = condensateData.raw_value
        fiscalInputs.range("B6:I206").raw_value = fiscalData.raw_value
    elif resource_type:
        commodity_type = "GAS"

        assetInputs.range((25, 9)).formula = "=$I$24"

        copyAllValues(assetInputs, "I25", "I", 26)
        #copyAllValues(assetInputs, "I25", "J", 24)
        copyAllValues(assetInputs, "I25", "L", 24)

        fiscalWrite(fiscalInputs, "GAS", fiscal_row, 0, "N", colNames)
        # ----------------------------------------------------------------------------------
        print 'Calculating development gas breakevens ...'
        if CALC_BASE:
            try:
                baseDevBEgas = goal_seek(24, 9, 49, 2, assetInputs, assetSensitivity, xlApp)
            except:
                baseDevBEgas = OUT_DEFAULT
            print 'baseDevBEgas:', baseDevBEgas
        # ----------------------------------------------------------------------------------
        if CALC_HIGH:
            try:
                highDevBEgas = goal_seek(24, 9, 50, 2, assetInputs, assetSensitivity, xlApp)
            except:
                highDevBEgas = OUT_DEFAULT
            print 'highDevBEgas:', highDevBEgas
        # ----------------------------------------------------------------------------------
        if CALC_LOW:
            try:
                lowDevBEgas  = goal_seek(24, 9, 51, 2, assetInputs, assetSensitivity, xlApp)
            except:
                lowDevBEgas = OUT_DEFAULT
            print 'lowDevBEgas:', lowDevBEgas
        # ----------------------------------------------------------------------------------
        assetInputs.range("I24:I134").raw_value = gasData.raw_value
        #assetInputs.range("J24:J134").raw_value = condensateData.raw_value
        assetInputs.range("L24:L134").raw_value = LNGData.raw_value
        fiscalInputs.range("B6:I206").raw_value = fiscalData.raw_value
        # ----------------------------------------------------------------------------------
        assetInputs.range((discount_row + 1, 9)).formula = "=$I$%s" % discount_row

        dataCell = "I%s" % (discount_row + 1)

        copyAllValues(assetInputs, dataCell, "I", int(discount_row + 2))
        #copyAllValues(assetInputs, dataCell, "J", int(discount_row))
        copyAllValues(assetInputs, dataCell, "L", int(discount_row))

        fiscalWrite(fiscalInputs, "GAS", fiscal_discount_row, str(discount_row), "R", colNames)
        # ----------------------------------------------------------------------------------
        print 'Calculating remaining gas breakevens ...'
        if CALC_BASE:
            try:
                baseRemainBEgas = goal_seek(discount_row, 9, 49, 3, assetInputs, assetSensitivity, xlApp)
            except:
                baseRemainBEgas = OUT_DEFAULT
            print 'baseRemainBEgas:', baseRemainBEgas
        # ----------------------------------------------------------------------------------
        if CALC_HIGH:
            try:
                highRemainBEgas = goal_seek(discount_row, 9, 50, 3, assetInputs, assetSensitivity, xlApp)
            except:
                highRemainBEgas = OUT_DEFAULT
            print 'highRemainBEgas:', highRemainBEgas
        # ----------------------------------------------------------------------------------
        if CALC_LOW:
            try:
                lowRemainBEgas  = goal_seek(discount_row, 9, 51, 3, assetInputs, assetSensitivity, xlApp)
            except:
                lowRemainBEgas = OUT_DEFAULT
            print 'lowRemainBEgas:', lowRemainBEgas
        # ----------------------------------------------------------------------------------
        assetInputs.range("I24:I134").raw_value = gasData.raw_value
        #assetInputs.range("J24:J134").raw_value = condensateData.raw_value
        assetInputs.range("L24:L134").raw_value = LNGData.raw_value
        fiscalInputs.range("B6:I206").raw_value = fiscalData.raw_value
    else:
        pass

    breakeven_out  = (baseRemainBEOil,baseRemainBEgas,baseDevBEOil,baseDevBEgas,highRemainBEOil,highRemainBEgas)
    breakeven_out += (highDevBEOil,highDevBEgas,lowRemainBEOil,lowRemainBEgas,lowDevBEOil,lowDevBEgas)
    output_values(assetSummary,*breakeven_out)
    xlWb.save()
    xlWb.close()

    output = (asset_id,baseRemainBEOil,baseRemainBEgas,baseDevBEOil,baseDevBEgas,highRemainBEOil,highRemainBEgas,highDevBEOil,highDevBEgas,lowRemainBEOil,lowRemainBEgas,lowDevBEOil,lowDevBEgas,run_id)
    return output


def breakeven_main(region='', asset_list=[], excelApp=None):
    #BE_REGIONS = 'D:\\GlobalData\\Macros\\BreakevenMacros\\Regions\\'
    start_time = get_datetime()
    run_id = get_run_id()

    print 'Start time: %s' % start_time

    if excelApp:
        xlApp = excelApp
    else:
        xlApp = xw.App(visible=False)
        xlApp.display_alerts = False

    if asset_list:
        asset_models = asset_list
    else:
        asset_models = [model for model in os.listdir(BE_REGIONS + region) if model[0] != '~' and model[-4:] == 'xlsx']

    model_count = len(asset_models)
    asset_num = 0
    breakeven_output = []
    for asset_model in asset_models:
        asset_num += 1
        print '\n%s/%s: %s' % (asset_num, model_count, asset_model)
        if asset_list:
            asset_file = asset_model
        else:
            asset_file = BE_REGIONS + region + '\\' + asset_model
        breakeven_output.append(run_breakevens(asset_file, run_id, xlApp))

    store_values(breakeven_output)
    if not excelApp:
        xlApp.quit()
        del xlApp
    end_time = get_datetime()
    print 'End time: %s' % end_time

if __name__=='__main__':
    breakeven_main(region="Unconventional")


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
