from globaldata import *
# import xlwings as xw

DATE = get_date()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def build_param_dict(param_dict):
    params = param_dict
    params['tblEngineFEATData']                 = {param: {} for param in TABLE_COLS['tblEngineFEATData']}
    params['tblEngineFEATData_Extn']            = {param: {} for param in TABLE_COLS['tblEngineFEATData_Extn']}
    params['tblEngineProductionData']           = {param: {} for param in TABLE_COLS['tblEngineProductionData']}
    params['tblEngineAnalogueFields']           = {param: {} for param in TABLE_COLS['tblEngineAnalogueFields']}
    params['tblEngineCashFlowData']             = {param: {} for param in TABLE_COLS['tblEngineCashFlowData']}
    params['tblEngineAssetSenRemainingNPV']     = {param: {} for param in TABLE_COLS['tblEngineAssetSenRemainingNPV']}
    params['tblEngineWellInputProductionInfo']  = {param: {} for param in TABLE_COLS['tblEngineWellInputProductionInfo']}
    params['tblEngineWellDataInfo']             = {param: {} for param in TABLE_COLS['tblEngineWellDataInfo']}
    params['tblEngineCommodityPriceSourceData'] = {param: '' for param in TABLE_COLS['tblEngineCommodityPriceSourceData']}
    params['tblEngineWellInputInfo']            = {param: [] for param in TABLE_COLS['tblEngineWellInputInfo']}
    params['tblEngineDataPoints']               = {param: {'Base Case': '', 'High Case': '', 'Low Case': ''} for param in TABLE_COLS['tblEngineDataPoints']}
    return params

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_asset_inputs_values(wb, param_dict, asset_id, debug=False):
    params = param_dict
    ws_name = 'Asset Inputs'
    try:
        ws = wb[ws_name]
    except:
        ws = wb.get_sheet_by_name(ws_name)
    for param in COL_REFS[ws_name].keys():
        ext_table = COL_REFS[ws_name][param]['tbl']
        ref = COL_REFS[ws_name][param]['ref']
        default_val = COL_REFS[ws_name][param]['null']
        if param in ['AssetStatus', 'ProductionStartYear']:
            case_rows = 111
            if int(asset_id) == 776055:
                case_rows = 150
            if int(asset_id) == 130187:
                case_rows = 130
            if int(asset_id) == 129343:
                case_rows = 135
            year_start = int(ws['B8'].value)
            for year in range(year_start, year_start + case_rows):
                params[ext_table][param][year] = {'Base Case': '', 'High Case': '', 'Low Case': ''}
            for case_type in CASE_TYPES[1]:
                for year in range(year_start, year_start+case_rows):
                    if param == 'AssetStatus':
                        try:
                            params[ext_table][param][year][case_type] = str(ws[ref].value)
                        except:
                            params[ext_table][param][year][case_type] = default_val

                    elif param == 'ProductionStartYear':
                        try:
                            params[ext_table][param][year][case_type] = int(ws[ref].value)
                        except:
                            params[ext_table][param][year][case_type] = default_val
        else:
            try:
                params[ext_table][param] = str(ws[ref].value)
            except:
                params[ext_table][param] = default_val
    return params


def get_asset_summary_values(wb, param_dict, asset_id, asset_status, discovered=False, debug=False):
    params = param_dict
    main_params = ['[Full-cycle break-even oil price ($/bbl)]', '[Full-cycle break-even gas price ($/mcf)]',
                   '[Remaining break-even oil price ($/bbl)]', '[Remaining break-even gas price ($/mcf)]']
    ws_name = 'Asset Summary'
    try:
        ws = wb[ws_name]
    except:
        ws = wb.get_sheet_by_name(ws_name)
    for i in range(len(CASE_TYPES[2])):
        row_num = 83 + i
        case_type = CASE_TYPES[2][i]
        for param in main_params:
            ext_table = COL_REFS[ws_name][param]['tbl']
            ref = COL_REFS[ws_name][param]['ref']
            default_val = COL_REFS[ws_name][param]['null']
            try:
                params[ext_table][param][case_type] = '%.2f' % float(ws[ref + str(row_num)].value)
            except:
                params[ext_table][param][case_type] = default_val
    disc_params = [
        'MinimumEconomicFieldsSize',
        'MaximumEconomicDeveopmentCost',
        'ConfidenceScore',
        'ProductionAnalogRank',
        'CostAnalogRank',
        'NearbyInfrastructureRank',
        'ReservesDataAvailability',
        'HydrocarbonQualityDataAvailability'
        #'FacilityTypeMatchRank',
        ]
    for param in disc_params:
        ext_table = COL_REFS[ws_name][param]['tbl']
        ref_cell  = COL_REFS[ws_name][param]['ref']
        default_val = COL_REFS[ws_name][param]['null']

        if asset_status.upper() == 'DISCOVERED' and discovered:
            try:
                params[ext_table][param]['Base Case'] = '%.2f' % float(ws[ref_cell].value)
            except:
                params[ext_table][param]['Base Case'] = default_val
        else:
            params[ext_table][param]['Base Case'] = default_val

        params[ext_table][param]['High Case'] = default_val
        params[ext_table][param]['Low Case'] = default_val
    if asset_status.upper() == 'DISCOVERED' and discovered:
        analogue_params = ['ProductionAnaloguesFieldID', 'CostAnaloguesFieldID']
        for param in analogue_params:
            ext_table = COL_REFS[ws_name][param]['tbl']
            ref_col   = COL_REFS[ws_name][param]['ref']
            default_val = COL_REFS[ws_name][param]['null']
            params[ext_table][param] = []
            row_num = 89
            for i in range(20):
                params[ext_table][param].append(ws[ref_col + str(row_num)].value)
                row_num += 1
    return params


def get_asset_sensitivity_values(wb, param_dict, asset_id, debug=False):
    params = param_dict
    ws_name = 'Asset Sensitivity'
    try:
        ws = wb[ws_name]
        # ws = wb.sheets[ws_name]  # comment it later
    except:
        ws = wb.get_sheet_by_name(ws_name)
    # except KeyError:
    #     print("Worksheet {} not found.".format(ws_name))

    for i in range(len(CASE_TYPES[1])):
        row_num = 49 + i
        case_type = CASE_TYPES[1][i]
        default_val = '0.0'
        try:
            params['tblEngineDataPoints']['NPVUS$MM'         ][case_type] = '%.2f' % (float(ws['B' + str(row_num)].value)/1000000.0)
        except:
            params['tblEngineDataPoints']['NPVUS$MM'][case_type] = default_val
        try:
            params['tblEngineDataPoints']['RemainingNPVUS$MM'][case_type] = '%.2f' % (float(ws['C' + str(row_num)].value)/1000000.0)
        except:
            params['tblEngineDataPoints']['RemainingNPVUS$MM'][case_type] = default_val

        for param in ['[IRR (%)]', '[Payback (years)]']:
            ext_table = COL_REFS[ws_name][param]['tbl']
            ref = COL_REFS[ws_name][param]['ref']
            default_val = COL_REFS[ws_name][param]['null']
            if param == '[IRR (%)]':
                try:
                    if case_type == 'Base Case':
                        row_num = 33
                        ref = 'B'
                        params[ext_table][param][case_type] = '%.2f' % float(ws[ref + str(row_num)].value*100)

                    else:
                        params[ext_table][param][case_type] = '%.2f' % float(ws[ref + str(row_num)].value * 100)
                except:
                    params[ext_table][param][case_type] = default_val
            else:
                if case_type == 'Base Case':
                    row_num = 49
                    ref = 'E'
                    try:
                        params[ext_table][param][case_type] = '%.2f' % float(ws[ref + str(row_num)].value)
                    except:
                        params[ext_table][param][case_type] = default_val
                else:
                    try:
                        params[ext_table][param][case_type] = '%.2f' % float(ws[ref + str(row_num)].value)
                    except:
                        params[ext_table][param][case_type] = default_val

    for param in ['[-20]', '[-10]', '[0]', '[10]', '[20]']:
        ext_table = COL_REFS[ws_name][param]['tbl']
        default_val = COL_REFS[ws_name][param]['null']
        for datatype in COL_REFS[ws_name][param]['ref'].keys():
            ref_cell = COL_REFS[ws_name][param]['ref'][datatype]
            try:
                params[ext_table][param][datatype] = '%.2f' % float(ws[ref_cell].value)
            except:
                params[ext_table][param][datatype] = default_val

    return params


def get_calculations_values(wb, param_dict, asset_id, debug=False):
    params = param_dict
    ws_name = 'Calculations'
    case_rows = 111
    if int(asset_id) == 776055:
        case_rows = 150
    if int(asset_id) == 130187:
        case_rows = 130
    if int(asset_id) == 129343:
        case_rows = 135
    try:
        ws = wb[ws_name]
    except:
        ws = wb.get_sheet_by_name(ws_name)
    year_start = int(ws['A' + str(8)].value)
    for ext_table in ['tblEngineFEATData', 'tblEngineFEATData_Extn', 'tblEngineProductionData']:
        for param in TABLE_COLS[ext_table]:
            if param not in ['AssetStatus', 'ProductionStartYear']:
                for i in range(case_rows):
                    year = year_start + i
                    params[ext_table][param][year] = {'Base Case': '', 'High Case': '', 'Low Case': ''}
    for i in range(len(CASE_TYPES[1])):
        ext_table = 'tblEngineDataPoints'
        row_num = 7 + (i * (case_rows + 2))
        case_type = CASE_TYPES[1][i]
        default_val = '0.0'
        try:
            params[ext_table]['[CapitalExpenditurePerboe (US$/boe)]'][case_type] = '%.2f' % (float(ws['Y' + str(row_num)].value)/float(ws['H' + str(row_num)].value))
        except:
            params[ext_table]['[CapitalExpenditurePerboe (US$/boe)]'][case_type] = default_val
        # --------------------------------------------------------------------------------------------------------
        try:
            params[ext_table]['[OperatingExpenditurePerboe (US$/boe)]'][case_type] = '%.2f' % (float(ws['AB' + str(row_num)].value)/float(ws['H' + str(row_num)].value))
        except:
            params[ext_table]['[OperatingExpenditurePerboe (US$/boe)]'][case_type] = default_val
        # --------------------------------------------------------------------------------------------------------
        ext_table = 'tblEngineProductionData'
        for j in range(case_rows):
            default_val = '0.0'
            year = year_start + j
            row_num += 1
            try:
                params[ext_table]['[Total Pre Tax Cash Flow US$]'    ][year][case_type] = '%.2f' % float(((ws['S'+str(row_num)].value+ws['AD'+str(row_num)].value)-(ws['Y'+str(row_num)].value+ws['AB'+str(row_num)].value)))
            except:
                params[ext_table]['[Total Pre Tax Cash Flow US$]'    ][year][case_type] = default_val
            # --------------------------------------------------------------------------------------------------------
            try:
                params[ext_table]['[Total Capital Expenditure US$]'  ][year][case_type] = '%.2f' % float(ws['Y'  + str(row_num)].value)
            except:
                params[ext_table]['[Total Capital Expenditure US$]'][year][case_type] = default_val
            # --------------------------------------------------------------------------------------------------------
            try:
                params[ext_table]['[Total Operating Expenditure US$]'][year][case_type] = '%.2f' % float(ws['AB' + str(row_num)].value)
            except:
                params[ext_table]['[Total Operating Expenditure US$]'][year][case_type] = default_val
            # --------------------------------------------------------------------------------------------------------
            try:
                params[ext_table]['[State Net Cash Flow (US$)]'      ][year][case_type] = '%.2f' % float(ws['AE' + str(row_num)].value)
            except:
                params[ext_table]['[State Net Cash Flow (US$)]'][year][case_type] = default_val
            # --------------------------------------------------------------------------------------------------------
            try:
                params[ext_table]['[Total Post Tax Cash Flow US$]'   ][year][case_type] = '%.2f' % float(ws['AG' + str(row_num)].value)
            except:
                params[ext_table]['[Total Post Tax Cash Flow US$]'][year][case_type] = default_val
            # --------------------------------------------------------------------------------------------------------
            for param in COL_REFS[ws_name].keys():
                ext_table = COL_REFS[ws_name][param]['tbl']
                ref = COL_REFS[ws_name][param]['ref']
                default_val = COL_REFS[ws_name][param]['null']
                if param in ['[Entitlement Crude Oil]', '[Entitlement Natural Gas]', '[Entitlement Condensate]', '[Entitlement NGLs]', '[Entitlement LNG]']:
                    try:
                        params[ext_table][param][year][case_type] = '%.2f' % float(ws[ref + str(row_num)].value*100)
                    except:
                        params[ext_table][param][year][case_type] = default_val

                else:
                    try:
                        params[ext_table][param][year][case_type] = '%.2f' % float(ws[ref + str(row_num)].value)
                    except:
                        params[ext_table][param][year][case_type] = default_val
    return params


def get_cash_flow_values(wb, param_dict, asset_id, debug=False):
    params = param_dict
    ws_name = 'Cash Flow'
    case_rows = 111
    if int(asset_id) == 776055:
        case_rows = 150
    if int(asset_id) == 130187:
        case_rows = 130
    if int(asset_id) == 129343:
        case_rows = 135
    try:
        ws = wb[ws_name]
    except:
        ws = wb.get_sheet_by_name(ws_name)
    year_start = int(ws['A' + str(7)].value)
    operator_data = {'total': 5}
    for param in TABLE_COLS['tblEngineCashFlowData']:
        for i in range(case_rows):
            year = year_start + i
            params['tblEngineCashFlowData'][param][year] = {operator: '' for operator in operator_data.keys()}
    for operator, operator_row in operator_data.items():
        row_num = operator_row + 2
        for j in range(case_rows):
            year = year_start + j
            for param in COL_REFS[ws_name].keys():
                ext_table = COL_REFS[ws_name][param]['tbl']
                ref = COL_REFS[ws_name][param]['ref']
                default_val = COL_REFS[ws_name][param]['null']
                try:
                    params[ext_table][param][year][operator] = '%.2f' % float(ws[ref + str(row_num)].value)
                except:
                    params[ext_table][param][year][operator] = default_val
            row_num += 1
    return params


def get_development_inputs_values(wb, param_dict, asset_id, debug=False):
    ws_name = 'Type Well Inputs'
    try:
        ws_1 = wb[ws_name]
    except:
        ws_1 = wb.get_sheet_by_name(ws_name)
    params = param_dict

    typewell_count = get_typewell_count(asset_id)

    for typewell in range(typewell_count):

        ext_table = 'tblEngineWellInputProductionInfo'
        typewell_col = WELL_INPUTS_COLS[WELL_NUMS[typewell]]
        if 0:
            print '{0}: typewell-{1} typewell_col-{2} ws_name="{3}" --> ws[{2}54].value = {4}'.format(asset_id, typewell, typewell_col, ws_name, ws_1['{}54'.format(typewell_col)].value)
        tangible_pct = float(ws_1['{}54'.format(typewell_col)].value)
        intangible_pct = float(1-tangible_pct)

        ws_name = 'Development Inputs'
        try:
            ws = wb[ws_name]
        except:
            ws = wb.get_sheet_by_name(ws_name)
        for year_num in range(61):
            row_num = year_num + 127

            params[ext_table]['[Capital Expenditure Intangible]'][year_num] = []
            params[ext_table]['[Capital Expenditure Tangible]'][year_num]   = []
            params[ext_table]['[Total (boe)]'][year_num] = []

            ref_col = FISCAL_WELL_COLS[typewell+1]['type_well_capex']
            ref_cell = '{}{}'.format(ref_col, row_num)

            try:
                params[ext_table]['[Capital Expenditure Intangible]'][year_num].append('%.2f' % (float(ws[ref_cell].value)*intangible_pct))
            except:
                default_val = COL_REFS[ws_name]['[Capital Expenditure Intangible]']['null']
                params[ext_table]['[Capital Expenditure Intangible]'][year_num].append(default_val)

            try:
                params[ext_table]['[Capital Expenditure Tangible]'][year_num].append('%.2f' % (float(ws[ref_cell].value)*tangible_pct))
            except:
                default_val = COL_REFS[ws_name]['[Capital Expenditure Tangible]']['null']
                params[ext_table]['[Capital Expenditure Tangible]'][year_num].append(default_val)

            try:
                type_well_cols = [('type_well_crude',1.0),('type_well_ng', (1000.0/6.0)),('type_well_condensate', 1.0),('type_well_ngls', 1.0),('type_well_lng', (1000.0/6.0))]
                total_boe = 0.0
                for param_name, conv_factor in type_well_cols:
                    ref_col = FISCAL_WELL_COLS[typewell + 1][param_name]
                    ref_cell = '{}{}'.format(ref_col, row_num)
                    total_boe += (float(ws[ref_cell].value) * float(conv_factor))
                params[ext_table]['[Total (boe)]'][year_num].append('%.2f' % total_boe)
            except:
                params[ext_table]['[Total (boe)]'][year_num].append('0.0')
            for param in TABLE_COLS[ext_table]:
                if param in COL_REFS[ws_name].keys():
                    params[ext_table][param][year_num] = []
                    ref_col = FISCAL_WELL_COLS[typewell+1][COL_REFS[ws_name][param]['ref']]
                    ref_cell = '{}{}'.format(ref_col, row_num)
                    default_val = COL_REFS[ws_name][param]['null']
                    if ws[ref_col + str(row_num)].value:
                        try:
                            params[ext_table][param][year_num].append('%.2f' % float(ws[ref_col + str(row_num)].value))
                        except:
                            params[ext_table][param][year_num].append(default_val)
                    else:
                        params[ext_table][param][year_num].append(default_val)
    return params


def get_type_well_inputs_values(wb, param_dict, asset_id, debug=False):
    params = param_dict
    ws_name = 'Type Well Inputs'
    try:
        ws = wb[ws_name]
    except:
        ws = wb.get_sheet_by_name(ws_name)
    pre_tax_resource = {
        'CRUDE OIL'  : 'Pre-Tax Break-Even Oil Price (US$/bbl)',
        'NATURAL GAS': 'Pre-Tax Break-Even Gas Price (US$/mcf)'
    }
    typewell_count = get_typewell_count(asset_id)
    for typewell in range(typewell_count):
        ext_table = 'tblEngineWellInputProductionInfo'
        typewell_col = WELL_INPUTS_COLS[WELL_NUMS[typewell]]
        col_num = XL_COLS.index(typewell_col)
        for month in range(1, 721):
            row_num = month + 83
            month_num = '{}{}'.format('0'*(3-len(str(month))), month)
            month_name = 'M{}'.format(month_num)
            for param in TABLE_COLS[ext_table]:
                params[ext_table][param][month_name] = []
                if param in COL_REFS[ws_name].keys():
                    ref_col = XL_COLS[col_num + COL_REFS[ws_name][param]['ref']]
                    ref_cell = '{}{}'.format(ref_col, row_num)
                    default_val = COL_REFS[ws_name][param]['null']
                    if ws[ref_cell].value:
                        try:
                            params[ext_table][param][month_name].append('%.2f' % (float(ws[ref_cell].value)*float(365.242/12.0)))
                        except:
                            params[ext_table][param][month_name].append(default_val)
                    else:
                        params[ext_table][param][month_name].append(default_val)
                else:
                    params[ext_table][param][month_name].append('0.0')

        ext_table = 'tblEngineWellInputInfo'
        primary_resource = ws['G20'].value
        resource_col_name = pre_tax_resource[primary_resource.upper()]
        for param in TABLE_COLS[ext_table]:
            if param in COL_REFS[ws_name].keys():
                default_val = COL_REFS[ws_name][param]['null']
                params[ext_table][param] = []

                if 'IP30-' in param:
                    ref_col = XL_COLS[col_num + COL_REFS[ws_name][param]['ref']]
                    ref_cell = '{}84'.format(ref_col)
                else:
                    ref_row = COL_REFS[ws_name][param]['ref']
                    ref_cell = '{}{}'.format(typewell_col, ref_row)

                if param in ['Working Interest (%)', 'Royalty Rate']:
                    try:
                        params[ext_table][param].append('%.2f' % float(ws[ref_cell].value*100))
                    except:
                        params[ext_table][param].append(default_val)
                elif param in ['Pre-Tax Break-Even Oil Price (US$/bbl)', 'Pre-Tax Break-Even Gas Price (US$/mcf)'] and param != resource_col_name:
                    params[ext_table][param].append(default_val)
                else:
                    if ws[ref_cell].value:
                        try:
                            params[ext_table][param].append('%.2f' % float(ws[ref_cell].value))
                        except:
                            params[ext_table][param].append(default_val)
                    else:
                        params[ext_table][param].append(default_val)
    return params


def get_well_data_values(wb, param_dict, asset_id, debug=False):
    params = param_dict
    ws_name = 'Well Data'
    try:
        ws = wb[ws_name]
    except:
        ws = wb.get_sheet_by_name(ws_name)
    typewell_count = get_typewell_count(asset_id)
    ext_table = 'tblEngineWellDataInfo'
    for typewell in range(typewell_count):
        row_num = 2
        year = ws['A' + str(row_num)].value
        while year:
            for param in TABLE_COLS[ext_table]:
                params[ext_table][param][year] = []
                ref_col = COL_REFS[ws_name][param]['ref']
                default_val = COL_REFS[ws_name][param]['null']
                try:
                    if param == '[DUC Wells Added]' and float(ws[ref_col + str(row_num)].value) < 0:
                        params[ext_table][param][year].append(default_val)
                    else:
                        params[ext_table][param][year].append('%.2f' % float(ws[ref_col + str(row_num)].value))
                except:
                    params[ext_table][param][year].append(default_val)
            row_num += 1
            year = ws['A' + str(row_num)].value
    return params

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_typewell_count(asset_id):
    typewell_count = 1
    typewell_ids = [asset_id]
    #typewell_ids = get_data('well_id', 'type_well_inputs', 'well_id LIKE "{}-%"'.format(asset_id))
    if typewell_ids:
        typewell_count = len(typewell_ids)
    return typewell_count


def get_drill_comp_data(asset_id):
    drilling_split = 0.0
    drilling_days = 0
    completion_days = 0
    drilling_cost = 0
    completion_cost = 0

    conn = get_connection()
    curr = conn.cursor()

    run_id = get_run_id(curr)
    sql_select_pct  = "SELECT drilling_split FROM param_track WHERE session_key LIKE '%{}%' AND asset_id={}".format(run_id, asset_id)
    sql_select_days = "SELECT production_count FROM wells WHERE datatype='Wells Drilling & Completion Days' AND asset_id={} ORDER BY period DESC LIMIT 1".format(asset_id)
    sql_select_cost = "SELECT production_count FROM wells WHERE datatype='Drilling & Completion well cost' AND asset_id={} ORDER BY period DESC LIMIT 1".format(asset_id)

    if curr.execute(sql_select_pct):
        drilling_split = float(curr.fetchone()[0])
    if curr.execute(sql_select_days):
        total_drill_comp_time = curr.fetchone()[0]
        drilling_days = round(float(total_drill_comp_time) * float(drilling_split),2)
        completion_days = round(total_drill_comp_time - drilling_days,2)
    if curr.execute(sql_select_cost):
        total_drill_comp_cost = curr.fetchone()[0] * 1000000
        drilling_cost = round(float(total_drill_comp_cost) * float(drilling_split),2)
        completion_cost = round(total_drill_comp_cost - drilling_cost,2)

    curr.close()
    conn.close()
    return drilling_days, completion_days, drilling_cost, completion_cost


def get_typewell_input_data(asset_id):
    param_data = {
        'Historical production decline'         : [],
        'Rig mobilization time (days)'          : [],
        'Well Life'                             : [],
        'Facilities ($)'                        : [],
        'Tangible cost percent split'           : [],
        'Annual maintenance capital expenditure': [],
        'Abandonment'                           : [],
        'Fixed Operating Expenditure'           : [],
        'Liquids transportation ($/bbl)'        : [],
        'Gas Transportation ($/mcf)'            : [],
        'Well Drilling time (days)'             : [],
        'Well Completion time (days)'           : [],
        'Drilling ($)'                          : [],
        'Completion ($)'                        : []
    }

    conn = get_connection()
    curr = conn.cursor()
    run_id = get_run_id(curr)
    typewell_count = get_typewell_count(asset_id)

    sql_select  = 'SELECT (1-decline_rate) AS well_decline_rate, rig_mobilization_days, ROUND(well_life,2), facility_cost,  ROUND(capex_tangible_pct, 2),  capex_maintenance, well_abandonment, fixed_opex_rate, '
    sql_select += 'ROUND(opex_liquids + opex_trans_liquids,2) AS total_opex_liquids, ROUND((opex_gas + opex_trans_gas)/1000,2) AS total_opex_gas FROM param_track WHERE session_key LIKE "%{}%" AND asset_id={}'
    for typewell in range(typewell_count):
        # typewell_id = '{}-{}'.format(asset_id, WELL_NUMS[typewell])
        typewell_id = asset_id
        curr.execute(sql_select.format(run_id, typewell_id))
        well_decline_rate, rig_mobilization_days, well_life, facility_cost, tangible_split_pct, capex_maintenance, abandonment, fixed_opex_rate, total_opex_liquids, total_opex_gas = curr.fetchone()
        drilling_days, completion_days, drilling_cost, completion_cost = get_drill_comp_data(typewell_id)

        param_data['Historical production decline'].append(str(well_decline_rate))
        param_data['Rig mobilization time (days)'].append(str(rig_mobilization_days))
        param_data['Well Life'].append(str(well_life))
        param_data['Facilities ($)'].append(str(facility_cost))
        param_data['Tangible cost percent split'].append(str(tangible_split_pct))
        param_data['Annual maintenance capital expenditure'].append(str(capex_maintenance))
        param_data['Abandonment'].append(str(abandonment))
        param_data['Fixed Operating Expenditure'].append(str(fixed_opex_rate))
        param_data['Liquids transportation ($/bbl)'].append(str(total_opex_liquids))
        param_data['Gas Transportation ($/mcf)'].append(str(total_opex_gas))
        param_data['Well Drilling time (days)'].append(str(drilling_days))
        param_data['Well Completion time (days)'].append(str(completion_days))
        param_data['Drilling ($)'].append(str(drilling_cost))
        param_data['Completion ($)'].append(str(completion_cost))

    curr.close()
    conn.close()
    return param_data


def get_asset_data(asset_id):
    in_conn = get_connection(server='mysql', database='globaldata', external=False)
    in_curr = in_conn.cursor()
    #in_curr.execute('SELECT asset_id, asset_name, country, region, status FROM asset_data WHERE asset_id=%s' % asset_id)
    in_curr.execute('SELECT asset_id, asset_name, country, region, status FROM assets WHERE asset_id=%s' % asset_id)
    asset_data = in_curr.fetchone()
    in_curr.close()
    in_conn.close()
    return asset_data[:4], asset_data[4]

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def truncate_table(database, schema, table, ext=True):
    print 'Clearing %s table ...' % table
    if ext:
        truncate_cmd = TRUNCATE_CMD % (database, database, schema, table)
    else:
        truncate_cmd = TRUNCATE_CMD_INT % (database, database, schema, table)
    os.system(truncate_cmd)
    print '%s table clear\n' % table


def export_to_txt(database, table_data, data_dir):
    for table in table_data.keys():
        schema = table_data[table]['schema']
        print 'Exporting {}.{}.{} table ...'.format(database, schema, table)

        export_cmd = EXPORT_CMD % (database, schema, table, 'out', data_dir, table, DATE)
        os.system(export_cmd)
        print '%s table export complete\n' % table



def remote_export_to_txt(server, database, schema, table, username, password, data_dir):
    export_cmd_temp = 'bcp %s.%s.%s %s %s%s_%s.txt -n -S %s -U %s -P %s'
    print 'Exporting {}.{}.{} table ...'.format(database, schema, table)
    export_cmd = export_cmd_temp % (database, schema, table, 'out', data_dir, table, DATE, server, username, password)
    print export_cmd
    os.system(export_cmd)
    print '%s table export complete\n' % table


def import_from_txt(truncate, ext, database, table_data, data_dir):
    for table in table_data.keys():
        schema = table_data[table]['schema']
        if truncate:
            truncate_table(database, schema, table, ext)
        print 'Importing {}.{}.{} table ...'.format(database, schema, table)
        if ext:
            import_cmd = IMPORT_CMD % (database, schema, table, 'in', data_dir, table, DATE)
        else:
            import_cmd = IMPORT_CMD_INT % (database, schema, table, 'in', data_dir, table, DATE, SERVER_NAME)
        print import_cmd
        os.system(import_cmd)
        print '%s table import complete\n' % table

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_export_data(region, asset_model, region_dir=BE_REGIONS, discovered=False, well_data=True, debug=False):
    model_path = region_dir + region + '\\' + asset_model
    asset_id = int(asset_model.split('_')[1])
    asset_data, asset_status = get_asset_data(asset_id)
    param_dict = build_param_dict(TABLE_PARAMS)
    wb = openpyxl.load_workbook(model_path, data_only=True)
    # wb = xw.Book(model_path, data_only=True) #Comment it later
    param_dict = get_asset_inputs_values(wb, param_dict, asset_id, debug)
    param_dict = get_asset_summary_values(wb, param_dict, asset_id, asset_status, discovered, debug)
    param_dict = get_asset_sensitivity_values(wb, param_dict, asset_id, debug)
    param_dict = get_calculations_values(wb, param_dict, asset_id, debug)
    param_dict = get_cash_flow_values(wb, param_dict, asset_id, debug)
    if region.upper() == 'UNCONVENTIONAL':
        param_dict = get_type_well_inputs_values(wb, param_dict, asset_id, debug=debug)
        param_dict = get_development_inputs_values(wb, param_dict, asset_id, debug=debug)
        if well_data:
            param_dict = get_well_data_values(wb, param_dict, asset_id, debug=debug)
    wb.save(model_path)
    return param_dict, asset_data, asset_id


def export_asset_data(out_curr, ext_table, param_dict, asset_data, asset_id=None, in_curr=None, run_id='', debug=False):
    if debug: print ext_table
    if asset_data:
        add_date = get_add_date(with_time=False)
        export_params = param_dict[ext_table]
        param_list = sorted(export_params.keys())
        column_count = len(param_list)
        col_str = ', '.join(param_list)
        if ext_table == 'tblEngineCommodityPriceSourceData':
            var_str = ', '.join(['?'] * (column_count + 5))
            param_values = tuple([export_params[param] for param in param_list])
            param_values += asset_data
            param_values += (add_date,)
            sql_update = 'INSERT INTO %s (%s, AssetID, AssetName, Country, Region, CreatedDate) VALUES (%s)' % ('Engine.' + ext_table, col_str, var_str)
            out_curr.execute(sql_update, param_values)
            out_curr.execute('COMMIT')
        elif ext_table == 'tblEngineDataPoints':
            var_str = ', '.join(['?'] * (column_count + 6))
            for i in range(len(CASE_TYPES[1])):
                case_type = CASE_TYPES[1][i]
                param_values = tuple([export_params[param][case_type] for param in param_list])
                param_values += asset_data
                param_values += (add_date,case_type)
                sql_update = 'INSERT INTO %s (%s, AssetID, AssetName, Country, Region, CreatedDate, CaseType) VALUES (%s)' % ('Engine.'+ext_table, col_str, var_str)
                out_curr.execute(sql_update, param_values)
            out_curr.execute('COMMIT')
        elif ext_table in ['tblEngineFEATData', 'tblEngineFEATData_Extn', 'tblEngineProductionData']:
            var_str = ', '.join(['?'] * (column_count + 7))
            for i in range(len(CASE_TYPES[1])):
                case_type = CASE_TYPES[1][i]
                x_param = param_list[0]
                for year in export_params[x_param].keys():
                    param_values = tuple([export_params[param][year][case_type] for param in param_list])
                    param_values += asset_data
                    param_values += (add_date,case_type,year)
                    sql_update = 'INSERT INTO %s (%s, AssetID, AssetName, Country, Region, CreatedDate, CaseType, Year) VALUES (%s)' % ('Engine.'+ext_table, col_str, var_str)
                    out_curr.execute(sql_update, param_values)
                    if (ext_table == 'tblEngineProductionData') and (case_type == 'Base Case'):
                        assetid = asset_data[0]
                        param_values = tuple([float(export_params[param][year][case_type]) for param in ['[Crude Oil]','[Natural Gas]','Condensate','LNG',]])
                        param_values += (year, assetid, run_id)
                        # in_curr.execute('INSERT INTO supply_production_data (oil_prod_bbl, gas_prod_mcf, cond_prod_bbl, lng_prod_mcf, prod_year, asset_id, run_id) VALUES ({},{},{},{},{},{},"{}")'.format(*param_values))
                        # commit(in_curr)
            out_curr.execute('COMMIT')
        elif ext_table == 'tblEngineCashFlowData':
            var_str = ', '.join(['?'] * (column_count + 7))
            x_param = param_list[0]
            x_year = export_params[x_param].keys()[0]
            for operator in export_params[x_param][x_year].keys():
                for year in export_params[x_param].keys():
                    param_values = tuple([export_params[param][year][operator] for param in param_list])
                    param_values += asset_data
                    param_values += (add_date,operator,year)
                    sql_update = 'INSERT INTO %s (%s, AssetID, AssetName, Country, Region, CreatedDate, CaseType, Year) VALUES (%s)' % ('Engine.'+ext_table, col_str, var_str)
                    out_curr.execute(sql_update, param_values)
                    assetid = asset_data[0]
                    param_vals = (float(export_params['[Capital expenditure]'][year][operator]),)
                    param_vals += (year, assetid, run_id)
                    # in_curr.execute('INSERT INTO supply_capex_data (total_capex, prod_year, asset_id, run_id) VALUES ({},{},{},"{}")'.format(*param_vals))
                    # commit(in_curr)
            out_curr.execute('COMMIT')
        elif ext_table == 'tblEngineAnalogueFields':
            asset_id = asset_data[0]
            var_str = ', '.join(['?'] * (column_count + 1))
            for param in param_list:
                for analogue_field in export_params[param]:
                    param_values = (asset_id, analogue_field, add_date)
                    sql_update = 'INSERT INTO %s (AssetID, %s, CreatedDate) VALUES (%s)' % ('Engine.'+ext_table, param, var_str)
                    out_curr.execute(sql_update, param_values)
            out_curr.execute('COMMIT')
        elif ext_table in ['tblEngineWellDataInfo', 'tblEngineWellInputProductionInfo']:
            typewell_count = get_typewell_count(asset_id)
            for typewell in range(typewell_count):
                #typewell_id = '{}-{}'.format(asset_id, WELL_NUMS[typewell])
                typewell_id = asset_id
                var_str = ', '.join(['?'] * (column_count + 6))
                x_param = param_list[0]
                for year in sorted(export_params[x_param].keys()):
                    #for param in param_list:
                    #    print '{}(ext_table) -- {}(year) {}(export_params[{}][year])'.format(ext_table, year, export_params[param][year], param)
                    param_values = tuple([export_params[param][year][typewell] for param in param_list])
                    param_values += (typewell_id,)
                    param_values += asset_data[1:]
                    param_values += (add_date, year)
                    sql_update = 'INSERT INTO %s (%s, AssetID, AssetName, Country, Region, CreatedDate, Year) VALUES (%s)' % ('Engine.'+ext_table, col_str, var_str)
                    out_curr.execute(sql_update, param_values)
            out_curr.execute('COMMIT')
        elif ext_table == 'tblEngineWellInputInfo':
            typewell_count = get_typewell_count(asset_id)
            for typewell in range(typewell_count):
                #typewell_id = '{}-{}'.format(asset_id, WELL_NUMS[typewell])
                typewell_id = asset_id
                if 0:
                    well_input_data = get_typewell_input_data(typewell_id)
                    for param_type, param_val in well_input_data.items():
                        export_params[param_type] = param_val
                for param_type, param_val in export_params.items():
                    param_values = (param_type, param_val[typewell], typewell_id)
                    param_values += asset_data[1:]
                    param_values += (add_date,)
                    var_str = ', '.join(['?'] * 7)
                    sql_update = 'INSERT INTO %s (Type, Value, AssetID, AssetName, Country, Region, CreatedDate) VALUES (%s)' % ('Engine.' + ext_table, var_str)
                    out_curr.execute(sql_update, param_values)
            out_curr.execute('COMMIT')
        elif ext_table == 'tblEngineAssetSenRemainingNPV':
            x_param = param_list[0]
            var_str = ', '.join(['?'] * (column_count + 6))
            for datatype in export_params[x_param].keys():
                param_values = tuple([export_params[param][datatype] for param in param_list])
                param_values += (unicode(str(datatype), errors='ignore'),)
                param_values += asset_data
                param_values += (add_date,)
                sql_update = 'INSERT INTO %s (%s, [Type], AssetID, AssetName, Country, Region, CreatedDate) VALUES (%s)' % ('Engine.' + ext_table, col_str, var_str)
                out_curr.execute(sql_update, param_values)
            out_curr.execute('COMMIT')


def check_export():
    export_complete = False
    run_id = get_run_id()
    in_conn = get_connection()
    in_curr = in_conn.cursor()
    in_curr.execute("SELECT COUNT(*) FROM command_line_log WHERE session_key LIKE 'DataExport_%%_%%%s%%' AND NOT end_time IS NULL" % run_id)
    regions_completed = in_curr.fetchone()[0]
    print '%s regions completed' % regions_completed
    if regions_completed == 6:
        export_complete = True
    in_curr.close()
    in_conn.close()
    return export_complete


def check_process(process):
    if COMPUTER == 'TITAN III':
        process_data = {
            'export'          : {'name'    : 'DataExport_%%_%%%s%%',
                                 'sessions': 6},

            'extract'         : {'name'    : 'DataExtract_%%_%%%s%%',
                                 'sessions': 6},

            'create_model'    : {'name'    : 'CreateModel_%%_%%%s%%',
                                 'sessions': 21},

            'breakeven'       : {'name'    : 'Breakeven_%%_%%%s%%',
                                 'sessions': 12},

            'econ_data'       : {'name'    : 'EconData_%%_%%%s%%',
                                 'sessions': 12},

            'DiscFieldCalc'   : {'name'    : 'DiscFieldCalc_%%_%%%s%%',
                                 'sessions': 16},

            'DiscFieldConf1'  : {'name'    : 'DiscFieldConf1_%%_%%%s%%',
                                 'sessions': 6},

            'DiscFieldConf2'  : {'name'    : 'DiscFieldConf2_%%_%%%s%%',
                                 'sessions': 6},

            'DiscFieldExtract': {'name'    : 'DiscFieldExtract_%%_%%%s%%',
                                 'sessions': 6},

            'DiscFieldMacro1' : {'name'    : 'DiscFieldMacro1_%%_%%%s%%',
                                 'sessions': 9},

            'DiscFieldMacro2' : {'name'    : 'DiscFieldMacro2_%%_%%%s%%',
                                 'sessions': 9},

            'DiscFieldMacro3' : {'name'    : 'DiscFieldMacro3_%%_%%%s%%',
                                 'sessions': 9},

            'DiscFieldModel'  : {'name'    : 'DiscFieldModel_%%_%%%s%%',
                                 'sessions': 20},

            'DiscFieldProd'   : {'name'    : 'DiscFieldProd_%%_%%%s%%',
                                 'sessions': 6},

            'AutomatedPanorama': {'name'   : 'AutomatedPanorama_%%_%%%s%%',
                                 'sessions': 10},

            'SupplyCurveMacro' : {'name'   : 'SupplyCurveMacro_%%_%%%s%%',
                                 'sessions': 12}
        }
    else:
        process_data = {
             'export': {    'name': 'DataExport_%%_%%%s%%',
                        'sessions': 6},

            'extract': {    'name': 'DataExtract_%%_%%%s%%',
                        'sessions': 6},

       'create_model': {    'name': 'CreateModel_%%_%%%s%%',
                        'sessions': 6},

          'breakeven': {    'name': 'Breakeven_%%_%%%s%%',
                        'sessions': 12},

          'econ_data': {    'name': 'EconData_%%_%%%s%%',
                        'sessions': 12},

      'DiscFieldCalc': {    'name': 'DiscFieldCalc_%%_%%%s%%',
                         'sessions': 6},

     'DiscFieldConf1': {   'name': 'DiscFieldConf1_%%_%%%s%%',
                         'sessions': 6},

     'DiscFieldConf2': {   'name': 'DiscFieldConf2_%%_%%%s%%',
                         'sessions': 6},

   'DiscFieldExtract': {    'name': 'DiscFieldExtract_%%_%%%s%%',
                         'sessions': 6},

    'DiscFieldMacro1': {    'name': 'DiscFieldMacro1_%%_%%%s%%',
                         'sessions': 9},

    'DiscFieldMacro2': {    'name': 'DiscFieldMacro2_%%_%%%s%%',
                         'sessions': 9},

    'DiscFieldMacro3': {    'name': 'DiscFieldMacro3_%%_%%%s%%',
                         'sessions': 9},

     'DiscFieldModel': {    'name': 'DiscFieldModel_%%_%%%s%%',
                         'sessions': 6},

      'DiscFieldProd': {    'name': 'DiscFieldProd_%%_%%%s%%',
                         'sessions': 6},

    'AutomatedPanorama': {'name': 'AutomatedPanorama_%%_%%%s%%',
                         'sessions': 10},

    'SupplyCurveMacro' : {'name'   : 'SupplyCurveMacro_%%_%%%s%%',
                          'sessions': 12}
                          }
    process_complete = False
    in_conn = get_connection()
    in_curr = in_conn.cursor()
    run_id = get_run_id(cursor=in_curr)
    session_name = process_data[process]['name'] % run_id
    in_curr.execute("SELECT COUNT(*) FROM command_line_log WHERE session_key LIKE '%s' AND NOT end_time IS NULL" % session_name)
    sessions_completed = in_curr.fetchone()[0]
    print '%s process: %s sessions completed' % (process, sessions_completed)
    if sessions_completed >= process_data[process]['sessions']:
        process_complete = True
    in_curr.close()
    in_conn.close()
    return process_complete


def export_uncon_param_data():
    pass

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def data_export(tables=EXT_TABLES, regions=REGION_NAMES, region_dir=BE_REGIONS, discovered=False, clear=False, ext=False, test_data=False, well_data=True, debug=True):
    #print tables
    ext_database = 'OGEngineDataExtract'
    # ext_database = 'OG_Effuah'
    if test_data:
        ext_database = 'OG_Effuah'
    out_conn = get_connection(server='sql_server', database=ext_database, external=ext, debug=debug)
    out_curr = out_conn.cursor()
    in_conn  = get_connection()
    in_curr  = in_conn.cursor()
    run_id   = get_run_id()
    ###### unocmmnet below lines later
    # clear =True
    if clear:
        for ext_table in tables:
            out_curr.execute('TRUNCATE TABLE %s' % 'Engine.' + ext_table)
            out_curr.execute('COMMIT')
    asset_ids = []  # to pick failed assets while handled by openpyxl
    assets_failed=[] # to pick failed assets while handled by openpyxl
    for region in regions:
        asset_models = [model for model in os.listdir(region_dir+ region) if model[0] != '~' and model[-4:] == 'xlsx']
        model_count = len(asset_models)
        asset_num = 0

        for asset_model in asset_models:
            asset_num += 1
            print '%s/%s: %s' % (asset_num, model_count, asset_model)
            try:
                # try:#comment later
                param_dict, asset_data, asset_id = get_export_data(region, asset_model, region_dir, discovered, well_data, debug=debug)
                # except:#comment later
                #     assets_failed.append(asset_model)#comment later
                for ext_table in tables:
                    if (ext_table not in ['tblEngineAnalogueFields','tblEngineWellInputInfo', 'tblEngineWellDataInfo', 'tblEngineWellInputProductionInfo']) or (ext_table == 'tblEngineAnalogueFields' and discovered) or (ext_table in ['tblEngineWellInputInfo', 'tblEngineWellDataInfo', 'tblEngineWellInputProductionInfo'] and 'UNCONVENTIONAL' in region.upper()):
                        export_asset_data(out_curr, ext_table, param_dict, asset_data, asset_id, in_curr, run_id, debug=debug)
            except:

                # # pass
                # asset_ids.append(asset_id)
                pass
                # param_dict, asset_data, asset_id = get_export_data(region, asset_model, region_dir, discovered,well_data, debug=debug)

    in_curr.close()
    in_conn.close()
    out_curr.close()
    out_conn.close()


def update_servers(dataset, export_tables=False, import_tables=False, truncate=True, test_data=False, ext=True):
    if test_data:
        if dataset in ['oilgas', 'oilgas_test']:
            data_config = OG_TEST_CONFIG
        elif dataset in ['discovered', 'discovered_test']:
            data_config = DF_TEST_CONFIG
        else:
            data_config = OG_TEST_CONFIG
    else:
        if dataset == 'oilgas':
            data_config = OILGAS_CONFIG
        elif dataset == 'mining':
            data_config = MINING_CONFIG
        elif dataset == 'panorama':
            data_config = PANORAMA_CONFIG
        elif dataset == 'discovered':
            data_config = DISCOVERED_CONFIG
        elif dataset == 'uncon':
            data_config = UNCON_CONFIG
        elif dataset == 'uncon_limit':
            data_config = OILGAS_LIMIT_CONFIG
        elif dataset == 'us_wells':
            data_config = WELLS_CONFIG
        elif dataset == 'production':
            data_config = PRODUCTION_CONFIG
        else:
            data_config = OILGAS_CONFIG
	if export_tables:
		export_to_txt(*data_config)
	if import_tables:
		import_from_txt(truncate, ext, *data_config)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
	# PROD_TABLE_DATA = {'tblEngineProductionData': {'schema': 'Engine'}}
	# data_export(regions=['Central America'], tables=EXT_LIMIT_TABLES, clear=False, ext=False, well_data=False, debug=True, test_data=False)
	#update_servers(dataset='panorama', export_tables=True, import_tables=True, truncate=False, test_data=False, ext=True)
    import_from_txt(truncate=False, ext=True, database='OGEngineDataExtract', table_data=OILGAS_TABLE_DATA_, data_dir=OILGAS_DB_DIR)
