from globaldata import *
import xlwings as xw


def extract_data(region, BE_REGION_DIR=BE_REGIONS, debug=False):
    # if region[:8] == 'scenario':
    #     BE_REGION_DIR = SCENARIO_DIR
    # elif region[:] == 'test':
    #     BE_REGION_DIR = TEST_RGNS_DIR
    # start_time = get_datetime()
    # xlApp = xw.App(visible=False)
    # conn = get_connection()
    # curr = conn.cursor()
    # run_id = get_run_id(curr)
    # all_asset_files = os.listdir(BE_REGION_DIR + region)
    # for asset_file in all_asset_files:
    #     if asset_file[:2] == '~$':
    #         os.remove(asset_file)
    # asset_models = [model for model in all_asset_files if model[:8] in ['MODELLED', 'DETAILED']]
    # if debug: print 'asset_models: {} --- all_asset_files: {}'.format(asset_models, all_asset_files)
    # total_asset_count = len(asset_models)
    # asset_num = 1
    # for asset_model in asset_models:
    #     sql_update = 'UPDATE econ_data SET %s WHERE asset_id=%s AND run_id="%s"'
    #     sun_path=r'%s%s\%s' % (BE_REGION_DIR, region, asset_model)
    #     sun_path.replace("\\\\","\\")
    #     wb = xlApp.books.open(sun_path)
    #     wb.app.calculation = 'semiautomatic'
    #     asset_inputs  = wb.sheets['Asset Inputs']
    #     asset_summary = wb.sheets['Asset Summary']
    #     calculations  = wb.sheets['Calculations']
    #     if region.lower() == 'unconventional':
    #         well_inputs = wb.sheets['Type Well Inputs']
    #         dev_inputs  = wb.sheets['Development Inputs']
    #     asset_id = int(asset_inputs.range('B1').value)
    #     discount_year = int(asset_inputs.range('E10').value)
    #     license_start = int(asset_inputs.range('B8').value)
    #     discount_row  = (discount_year - license_start) + 24
    #     curr_calc_row = (discount_year - license_start) + 8
    #     print '%s/%s asset_id: %s' % (asset_num, total_asset_count, asset_id)
    #     asset_num +=1
    #     ECON_DATA = {
    #                'total_boe': {'ws': asset_inputs,  'cell': 'E4',  'val': 0},
    #                  'npv_rem': {'ws': asset_inputs,  'cell': 'J4',  'val': 0},
    #                  'npv_dev': {'ws': asset_summary, 'cell': 'C21', 'val': 0},
    #                 'irr_full': {'ws': asset_summary, 'cell': 'B22', 'val': 0},
    #                  'irr_dev': {'ws': asset_summary, 'cell': 'C22', 'val': 0},
    #              'fiscal_full': {'ws': asset_summary, 'cell': 'B70', 'val': 0},
    #               'fiscal_rem': {'ws': asset_summary, 'cell': 'C70', 'val': 0},
    #              'fiscal_take': {'ws': asset_summary, 'cell': 'B69', 'val': 0},
    #             'abandon_rem' : {'ws': asset_summary, 'cell': 'C50', 'val': 0},
    #             'abandon_full': {'ws': asset_summary, 'cell': 'B50', 'val': 0},
    #            'capex_boe_rem': {'ws': asset_summary, 'cell': 'C51', 'val': 0},
    #           'capex_boe_full': {'ws': asset_summary, 'cell': 'B51', 'val': 0},
    #      'opex_boe_full_model': {'ws': asset_summary, 'cell': 'B52', 'val': 0},
    #             'opex_boe_rem': {'ws': asset_summary, 'cell': 'C52', 'val': 0},
    #                'capex_rem': {'ws': asset_summary, 'cell': 'C59', 'val': 0},
    #               'capex_full': {'ws': asset_summary, 'cell': 'B59', 'val': 0},
    #                'opex_rem' : {'ws': asset_summary, 'cell': 'C60', 'val': 0},
    #                'opex_full': {'ws': asset_summary, 'cell': 'B60', 'val': 0},
    #         'natgas_recov_rem': {'ws': asset_summary, 'cell': 'E22', 'val': 0},
    #         'liquid_recov_rem': {'ws': asset_summary, 'cell': 'E21', 'val': 0},
    #           'ngls_recov_rem': {'ws': asset_summary, 'cell': 'E23', 'val': 0},
    #          'total_recov_rem': {'ws': asset_summary, 'cell': 'E20', 'val': 0},
    #         'liquid_recov_tot': {'ws': asset_summary, 'cell': 'E17', 'val': 0},
    #         'natgas_recov_tot': {'ws': asset_summary, 'cell': 'E18', 'val': 0},
    #           'ngls_recov_tot': {'ws': asset_summary, 'cell': 'E19', 'val': 0},
    #              'total_recov': {'ws': asset_summary, 'cell': 'E16', 'val': 0},
    #               'be_gas_rem': {'ws': asset_summary, 'cell': 'E83', 'val': 0},
    #               'be_oil_rem': {'ws': asset_summary, 'cell': 'D83', 'val': 0},
    #               'be_gas_dev': {'ws': asset_summary, 'cell': 'C83', 'val': 0},
    #               'be_oil_dev': {'ws': asset_summary, 'cell': 'B83', 'val': 0}
    #
    #     }
    #     if region.lower() == 'unconventional':
    #         ECON_DATA['eur_total']        = {'ws': well_inputs, 'cell': 'G43',  'val': 0}
    #         ECON_DATA['post_tax_irr']     = {'ws': well_inputs, 'cell': 'G48',  'val': 0}
    #         ECON_DATA['pre_tax_irr']      = {'ws': well_inputs, 'cell': 'G45',  'val': 0}
    #         ECON_DATA['be_oil_post_tax']  = {'ws': well_inputs, 'cell': 'G66',  'val': 0}
    #         ECON_DATA['be_gas_post_tax']  = {'ws': well_inputs, 'cell': 'G67',  'val': 0}
    #         ECON_DATA['capex_well']       = {'ws': dev_inputs,  'cell': 'I126', 'val': 0}
    #         ECON_DATA['opex_well']        = {'ws': dev_inputs,  'cell': 'J126', 'val': 0}
    #         ECON_DATA['ip30_oil_bd']      = {'ws': well_inputs, 'cell': 'G84',  'val': 0}
    #         ECON_DATA['ip30_gas_mmcfd']   = {'ws': well_inputs, 'cell': 'H84',  'val': 0}
    #         ECON_DATA['ip30_cond_bd']     = {'ws': well_inputs, 'cell': 'I84',  'val': 0}
    #         ECON_DATA['ip30_NGLs_bd']     = {'ws': well_inputs, 'cell': 'J84',  'val': 0}
    #         ECON_DATA['working_interest'] = {'ws': well_inputs, 'cell': 'G27',  'val': 0}
    #
    #     curr_opex_boe = 0
    #     curr_prod = 0
    #     try:
    #         curr_prod = float(calculations.range('H{}'.format(curr_calc_row)).value)
    #         curr_opex = float(calculations.range('AB{}'.format(curr_calc_row)).value)
    #         if curr_prod:
    #             curr_opex_boe = round(float(curr_opex)/float(curr_prod), 3)
    #     except:
    #         pass
    #
    #     econ_params = sorted(ECON_DATA.keys())
    #
    #     for econ_param in econ_params:
    #         param_ws = ECON_DATA[econ_param]['ws']
    #         param_cell = ECON_DATA[econ_param]['cell']
    #         if debug: print 'econ_param: {} -- param_cell: {}'.format(econ_param, param_cell)
    #         try:
    #             ECON_DATA[econ_param]['val'] = round(float(param_ws.range(param_cell).value), 3)
    #         except:
    #             pass
    #
    #     param_vals = tuple([ECON_DATA[econ_param]['val'] for econ_param in econ_params])
    #
    #     try:
    #         capex_opex_boe_rem = ECON_DATA['capex_boe_rem']['val'] + ECON_DATA['opex_boe_rem']['val']
    #     except:
    #         capex_opex_boe_rem = None
    #
    #     try:
    #         npv_rem_per_boe = round(ECON_DATA['npv_rem']['val']/ECON_DATA['total_recov_rem']['val'], 3)
    #     except:
    #         npv_rem_per_boe = None
    #
    #     try:
    #         npv_dev_per_boe = round(ECON_DATA['npv_dev']['val']/ECON_DATA['total_recov']['val'], 3)
    #     except:
    #         npv_dev_per_boe = None
    #
    #     try:
    #         boed_prod = round(float(calculations.range('H{}'.format(curr_calc_row)).value)/365.242,2)
    #     except:
    #         boed_prod = 0
    #     param_vals += (capex_opex_boe_rem, npv_rem_per_boe, npv_dev_per_boe, boed_prod, curr_opex_boe)
    #     econ_params += ['capex_opex_boe_rem', 'npv_rem_per_boe', 'npv_dev_per_boe', 'boed_prod', 'curr_opex_boe']
    #     if debug: print 'param_vals: {} -- econ_params: {}'.format(param_vals, econ_params)
    #
    #     if region.lower() == 'unconventional':
    #         try:
    #             ip30_rate = float(ECON_DATA['ip30_oil_bd']['val'])+(float(ECON_DATA['ip30_gas_mmcfd']['val'])*1000.0/6.0)+float(ECON_DATA['ip30_cond_bd']['val'])+float(ECON_DATA['ip30_NGLs_bd']['val'])
    #         except:
    #             ip30_rate = 0.0
    #
    #         try:
    #             capex_well_boe = round(float(ECON_DATA['capex_well']['val']) / float(ECON_DATA['eur_total']['val']), 2)
    #         except:
    #             capex_well_boe = None
    #
    #         try:
    #             opex_well_boe = round(float(ECON_DATA['opex_well']['val']) / float(ECON_DATA['eur_total']['val']), 2)
    #         except:
    #             opex_well_boe = None
    #
    #         try:
    #             well_boe = 0
    #             for col in 'BDEG':
    #                 well_boe += float(dev_inputs.range('{}126'.format(col)).value)
    #             for col in 'CF':
    #                 well_boe += (float(dev_inputs.range('{}126'.format(col)).value * (1000.0/6.0)))
    #         except:
    #             well_boe = None
    #         param_vals += (ip30_rate, capex_well_boe, opex_well_boe, well_boe)
    #         econ_params += ['ip30_rate', 'capex_well_boe', 'opex_well_boe', 'well_boe']
    #
    #     param_str = ','.join([econ_param + '=%s' for econ_param in econ_params])
    #     sql_update = sql_update % (param_str, asset_id, run_id)
    #     if debug: print sql_update % param_vals
    #     curr.execute(sql_update, param_vals)
    #     curr.execute('COMMIT')
    #     wb.close()
    # curr.close()
    # conn.close()
    # xlApp.quit()
    # end_time = get_datetime()
    # total_time = elapsed_time(start_time, end_time)
    # print ''
    # print 'Total Time: %s' % total_time
    # print ''
    # Region directory selection
    if region.startswith('scenario'):
        BE_REGION_DIR = SCENARIO_DIR
    elif region == 'test':
        BE_REGION_DIR = TEST_RGNS_DIR

    start_time = get_datetime()
    xlApp = xw.App(visible=False)
    conn = get_connection()
    curr = conn.cursor()
    run_id = get_run_id(curr)

    region_path = os.path.join(BE_REGION_DIR, region)
    all_asset_files = os.listdir(region_path)

    for f in all_asset_files:
        if f.startswith('~$'):
            try:
                os.remove(os.path.join(region_path, f))
            except:
                pass

    asset_models = [m for m in all_asset_files if m[:8] in ['MODELLED', 'DETAILED']]
    total_assets = len(asset_models)
    asset_num = 1

    sql_rows = []
    sql_param_list = None
    sql_update = None

    for asset_file in asset_models:
        asset_path = os.path.join(region_path, asset_file)
        try:
            wb = xlApp.books.open(asset_path)
        except:
            print('Skipping file (unable to open): %s' % asset_file)
            continue

        wb.app.calculation = 'semiautomatic'
        try:
            asset_inputs = wb.sheets['Asset Inputs']
            asset_summary = wb.sheets['Asset Summary']
            calculations = wb.sheets['Calculations']
        except:
            wb.close()
            continue

        if region.lower() == 'unconventional':
            try:
                well_inputs = wb.sheets['Type Well Inputs']
                dev_inputs = wb.sheets['Development Inputs']
            except:
                wb.close()
                continue

        try:
            asset_id = int(asset_inputs.range('B1').value)
        except:
            wb.close()
            continue

        print('%s/%s asset_id: %s' % (asset_num, total_assets, asset_id))
        asset_num += 1

        ECON_DATA = {
            'total_boe': ('Asset Inputs', 'E4'),
            'npv_rem': ('Asset Inputs', 'J4'),
            'npv_dev': ('Asset Summary', 'C21'),
            'irr_full': ('Asset Summary', 'B22'),
            'irr_dev': ('Asset Summary', 'C22'),
            'fiscal_full': ('Asset Summary', 'B70'),
            'fiscal_rem': ('Asset Summary', 'C70'),
            'fiscal_take': ('Asset Summary', 'B69'),
            'abandon_rem': ('Asset Summary', 'C50'),
            'abandon_full': ('Asset Summary', 'B50'),
            'capex_boe_rem': ('Asset Summary', 'C51'),
            'capex_boe_full': ('Asset Summary', 'B51'),
            'opex_boe_full_model': ('Asset Summary', 'B52'),
            'opex_boe_rem': ('Asset Summary', 'C52'),
            'capex_rem': ('Asset Summary', 'C59'),
            'capex_full': ('Asset Summary', 'B59'),
            'opex_rem': ('Asset Summary', 'C60'),
            'opex_full': ('Asset Summary', 'B60'),
            'natgas_recov_rem': ('Asset Summary', 'E22'),
            'liquid_recov_rem': ('Asset Summary', 'E21'),
            'ngls_recov_rem': ('Asset Summary', 'E23'),
            'total_recov_rem': ('Asset Summary', 'E20'),
            'liquid_recov_tot': ('Asset Summary', 'E17'),
            'natgas_recov_tot': ('Asset Summary', 'E18'),
            'ngls_recov_tot': ('Asset Summary', 'E19'),
            'total_recov': ('Asset Summary', 'E16'),
            'be_gas_rem': ('Asset Summary', 'E83'),
            'be_oil_rem': ('Asset Summary', 'D83'),
            'be_gas_dev': ('Asset Summary', 'C83'),
            'be_oil_dev': ('Asset Summary', 'B83')
        }

        if region.lower() == 'unconventional':
            extra = {
                'eur_total': ('Type Well Inputs', 'G43'),
                'post_tax_irr': ('Type Well Inputs', 'G48'),
                'pre_tax_irr': ('Type Well Inputs', 'G45'),
                'be_oil_post_tax': ('Type Well Inputs', 'G66'),
                'be_gas_post_tax': ('Type Well Inputs', 'G67'),
                'capex_well': ('Development Inputs', 'I126'),
                'opex_well': ('Development Inputs', 'J126'),
                'ip30_oil_bd': ('Type Well Inputs', 'G84'),
                'ip30_gas_mmcfd': ('Type Well Inputs', 'H84'),
                'ip30_cond_bd': ('Type Well Inputs', 'I84'),
                'ip30_NGLs_bd': ('Type Well Inputs', 'J84'),
                'working_interest': ('Type Well Inputs', 'G27')
            }
            ECON_DATA.update(extra)

        results = {}
        for key, (ws_name, cell) in ECON_DATA.items():
            try:
                ws = wb.sheets[ws_name]
                val = ws.range(cell).value
                results[key] = round(float(val), 3)
            except:
                results[key] = None

        curr_calc_row = None
        try:
            discount_year = int(asset_inputs.range('E10').value)
            license_start = int(asset_inputs.range('B8').value)
            curr_calc_row = (discount_year - license_start) + 8
        except:
            curr_calc_row = None

        curr_opex_boe = None
        if curr_calc_row:
            try:
                prod = float(calculations.range('H%s' % curr_calc_row).value)
                opex = float(calculations.range('AB%s' % curr_calc_row).value)
                if prod:
                    curr_opex_boe = round(opex / prod, 3)
            except:
                pass

        try:
            capex_opex_boe_rem = results['capex_boe_rem'] + results['opex_boe_rem']
        except:
            capex_opex_boe_rem = None

        try:
            npv_rem_per_boe = round(results['npv_rem'] / results['total_recov_rem'], 3)
        except:
            npv_rem_per_boe = None

        try:
            npv_dev_per_boe = round(results['npv_dev'] / results['total_recov'], 3)
        except:
            npv_dev_per_boe = None

        try:
            boed_prod = round(float(calculations.range('H%s' % curr_calc_row).value) / 365.242, 2)
        except:
            boed_prod = None

        results.update({
            'capex_opex_boe_rem': capex_opex_boe_rem,
            'npv_rem_per_boe': npv_rem_per_boe,
            'npv_dev_per_boe': npv_dev_per_boe,
            'boed_prod': boed_prod,
            'curr_opex_boe': curr_opex_boe
        })

        if region.lower() == 'unconventional':
            try:
                ip30_rate = (
                        results['ip30_oil_bd'] +
                        (results['ip30_gas_mmcfd'] * 1000.0 / 6.0) +
                        results['ip30_cond_bd'] +
                        results['ip30_NGLs_bd']
                )
            except:
                ip30_rate = None

            try:
                capex_well_boe = round(results['capex_well'] / results['eur_total'], 2)
            except:
                capex_well_boe = None

            try:
                opex_well_boe = round(results['opex_well'] / results['eur_total'], 2)
            except:
                opex_well_boe = None

            try:
                well_boe = 0
                for col in 'BDEG':
                    well_boe += float(dev_inputs.range('%s126' % col).value)
                for col in 'CF':
                    well_boe += float(dev_inputs.range('%s126' % col).value) * (1000.0 / 6.0)
            except:
                well_boe = None

            results.update({
                'ip30_rate': ip30_rate,
                'capex_well_boe': capex_well_boe,
                'opex_well_boe': opex_well_boe,
                'well_boe': well_boe
            })

        params = sorted(results.keys())
        param_vals = tuple(results[k] for k in params)

        if not sql_update:
            param_str = ",".join(["%s=%%s" % k for k in params])
            sql_update = "UPDATE econ_data SET %s WHERE asset_id=%%s AND run_id='%s'" % (param_str, run_id)
            sql_param_list = params[:]

        sql_rows.append(param_vals + (asset_id,))
        wb.close()

    if sql_update and sql_rows:
        curr.executemany(sql_update, sql_rows)
        curr.execute("COMMIT")

    curr.close()
    conn.close()
    xlApp.quit()

    end_time = get_datetime()
    print('Total Time: %s' % elapsed_time(start_time, end_time))


def main(region, debug=False):
    extract_data(region, debug=debug)


if __name__=='__main__':
    region = 'South America'
    try:
        region = sys.argv[1]
        #debug  = False
    except:
        pass
    main(region)