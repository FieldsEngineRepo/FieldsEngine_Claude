class EconomicLimit():
    def __init__(self):
        pass
    def get_economic_limit(self):
        if start_year < 1900:
            inflt_end_year = start_year + 111
            inflt_start_year = max(1900, start_year)
            inflation_years = xrange(inflt_start_year, inflt_end_year)
            inflt_year_count = len(inflation_years)
        
            inflt_base = self.getInflationRange(mCur, inflt_start_year, inflt_end_year, mCountry)
            capx_inflt_base, opex_inflt_base = inflt_base[:inflt_year_count], inflt_base[inflt_year_count:]
        else:
            max_inflt_year = get_param('MAX(period)', 'inflation')
            inflt_end_year = min(start_year + 111, max_inflt_year)
            inflation_years = xrange(start_year, inflt_end_year + 1)
            inflt_year_count = len(inflation_years)
            inflt_base = self.getInflationRange(mCur, start_year, inflt_end_year, mCountry)
            capx_inflt_base, opex_inflt_base = inflt_base[:inflt_year_count], inflt_base[inflt_year_count:]
        
        inflation_data = {'opex' : {opex_inflt_base[i][0]: float(opex_inflt_base[i][1]) for i in range(inflt_year_count)},
                          'capex': {capx_inflt_base[i][0]: float(capx_inflt_base[i][1]) for i in range(inflt_year_count)}}
        
        if self.write_inflation_values:
            map((lambda row_num: self.enterBaseInflation(23, row_num, 'AA', ws2, capx_inflt_base)), xrange(23, len(capx_inflt_base) + 23))
            map((lambda row_num: self.enterBaseInflation(23, row_num, 'AB', ws2, opex_inflt_base)), xrange(23, len(opex_inflt_base) + 23))
        
        # ---------------------------------------------------------------------------------
        self.model_section = '20.00.00'

        if not (self.detailed_models and self.is_detailed_model(mCur, ast_id)) and mStatus != 'Abandoned' and not (do_L48 and self.unConventionalCheck(mCur,ast_id) and self.new_fiscal_model and 'Resource.xlsx' in fiscal_model):
            model_years = self.year
            last_model_year = model_years[-1]
            pre_tax_data = {prod_yr: {'crude_prod'        : 0,
                                      'crude_price'       : 0,
                                      'ng_prod'           : 0,
                                      'ng_price'          : 0,
                                      'condensate_prod'   : 0,
                                      'condensate_price'  : 0,
                                      'ngls_prod'         : 0,
                                      'ngls_price'        : 0,
                                      'lng_prod'          : 0,
                                      'lng_price'         : 0,
                                      'capex_cost'        : 0,
                                      'opex_cost'         : 0,
                                      'abandonment_cost'  : 0,
                                      'total_expenditure' : 0,
                                      'total_revenue'     : 0,
                                      'cash_flow'         : 0}}
            for ij in range(0, len(model_years)):
                prod_year = model_years[ij]
                first_capex_year = min([int(capex_year) for capex_year in col_data['n'].keys() if col_data['n'][capex_year] > 0])
                last_abandon_year = max([int(abandon_year) for abandon_year in col_data['p'].keys()])

                # COMMODITY PRICES
                if prod_year in col_data['h'].keys() and prod_year >= first_capex_year and prod_year <= last_abandon_year:
                    pre_tax_data[prod_year]['crude_price']      = round(float(col_data['h'][prod_year]), self.roundAll)
                    pre_tax_data[prod_year]['ng_price']         = round(float(col_data['i'][prod_year]), self.roundAll)
                    pre_tax_data[prod_year]['condensate_price'] = round(float(col_data['j'][prod_year]), self.roundAll)
                    pre_tax_data[prod_year]['ngls_price']       = round(float(col_data['k'][prod_year]), self.roundAll)
                    pre_tax_data[prod_year]['lng_price']        = round(float(col_data['l'][prod_year]), self.roundAll)

                # CAPEX COST
                try:
                    opex_inflation_value  = float(inflation_data['opex'][int(prod_year)])
                    capex_inflation_value = float(inflation_data['capex'][int(prod_year)])
                except:
                    opex_inflation_value  = 1.0
                    capex_inflation_value = 1.0

                capex_cost_value = (round(float(col_data['n'][prod_year]), self.roundAll) + round(float(col_data['o'][prod_year]), self.roundAll)) * capex_inflation_value
                if prod_year > self.capexCapacityYear.get() and prod_year >= last_peak_year:
                    capex_cost_value   *= self.capexCapacityFactor.get()

                pre_tax_data[prod_year]['capex_cost'] = float(capex_cost_value)

                year_len = len(model_years) - 10
                if (pre_prod_yrs - 1) < ij < year_len:
                    # COMMODITY PRODUCTION
                    pre_tax_data[prod_year]['crude_prod']       = round(float(col_data['b'][prod_year])/float(self.days_in_year), self.roundAll)
                    pre_tax_data[prod_year]['ng_prod']          = round(float(col_data['c'][prod_year])/float(self.days_in_year), self.roundAll)
                    pre_tax_data[prod_year]['condensate_prod']  = round(float(col_data['d'][prod_year])/float(self.days_in_year), self.roundAll)
                    pre_tax_data[prod_year]['ngls_prod']        = round(float(col_data['e'][prod_year])/float(self.days_in_year), self.roundAll)
                    pre_tax_data[prod_year]['lng_prod']         = round(float(col_data['f'][prod_year])/float(self.days_in_year), self.roundAll)

                    # ABANDONMENT COST
                    pre_tax_data[prod_year]['abandonment_cost'] = round(float(col_data['p'][prod_year]), self.roundAll) * capex_inflation

                    # OPEX COST
                    opex_reduction_factor = 1.0
                    reduced_prod_years = zero_prod_years + prod_dec_years
                    if prod_year in reduced_prod_years:
                        if prod_year in zero_prod_years:
                            opex_reduction_factor *= self.opex_reduction
                        elif prod_year in prod_dec_years:
                            opex_reduction_factor *= (1.5 * self.opex_reduction)
                    if prod_year in low_prod_years:
                        if prod_year in prod_inc_years:
                            opex_reduction_factor *= (1.5 * self.opex_reduction)
                        else:
                            opex_reduction_factor *= self.opex_reduction
                    fixed_opex_value = round(float(col_data['r'][prod_year]), self.roundAll) * float(opex_inflation_value) * float(opex_reduction_factor)

                    if prod_year >= self.opexCapacityYear.get():
                        if prod_year >= self.opexCapacityYear2.get():
                            fixed_opex_value *= float(self.opexCapacityFactor2.get())
                        else:
                            fixed_opex_value *= float(self.opexCapacityFactor.get())

                    colb = pre_tax_data[prod_year]['crude_prod']
                    colc = pre_tax_data[prod_year]['ng_prod']
                    cold = pre_tax_data[prod_year]['condensate_prod']
                    cole = pre_tax_data[prod_year]['ngls_prod']
                    colf = pre_tax_data[prod_year]['lng_prod']

                    variable_opex_value = round((((colb + cold + cole)*float(var_opex_b)) + ((colc + colf)*float(var_opex_mmcf))) * self.days_in_year, self.roundAll) * opex_inflation_value
                    pre_tax_data[prod_year]['opex_cost'] = fixed_opex_value + variable_opex_value

                if ij >= (len(model_years) - 10):
                    pre_tax_data[prod_year]['abandonment_cost'] = round(col_data['p'][prod_year], self.roundAll)

                #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                pre_tax_data[prod_year]['total_expenditure']    = pre_tax_data[prod_year]['capex_cost'] + pre_tax_data[prod_year]['opex_cost'] + pre_tax_data[prod_year]['abandonment_cost']
                for comm_name in ['crude', 'ng', 'condensate', 'ngls', 'lng']:
                    pre_tax_data[prod_year]['total_revenue'] += (pre_tax_data[prod_year]['{}_prod'.format(comm_name)] * pre_tax_data[prod_year]['{}_price'.format(comm_name)])
                pre_tax_data[prod_year]['cash_flow'] = pre_tax_data[prod_year]['total_revenue'] - pre_tax_data[prod_year]['total_expenditure']

            last_positive_year  = max([prod_yr for prod_yr in pre_tax_data.keys() if pre_tax_data[prod_yr]['cash_flow'] >= 0])
            negative_year_count = last_model_year - last_positive_year
            if self.debugMode:
                print 'pre_tax_data                : {}'.format(['{}: {}'.format(prod_yr, pre_tax_data[prod_yr]) for prod_yr in sorted(pre_tax_data.keys())])
                print 'last_positive_year          : {}'.format(last_positive_year)
                print 'cash_flow from last_positive: {}'.format(['{}: {}'.format(prod_yr, pre_tax_data[prod_yr]['cash_flow']) for prod_yr in pre_tax_data.keys() if prod_yr >= last_positive_year])
                print 'last_model_year             : {}'.format(last_model_year)
                print 'negative_year_count         : {}'.format(negative_year_count)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ECONOMIC LIMITS TEST ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def econ_limit_test(self):
        if self.econ_limit and not self.model_discovered_fields and not self.calc_deals and not (self.detailed_models and self.is_detailed_model(mCur, ast_id)) \
                and mStatus != 'Abandoned' and not (do_L48 and self.unConventionalCheck(mCur, ast_id) and self.new_fiscal_model and 'Resource.xlsx' in fiscal_model):
            cash_flow_years = self.year
            last_model_year = cash_flow_years[-1]
            pre_tax_data = {prod_yr: {'crude_prod'       : 0,
                                      'crude_price'      : 0,
                                      'ng_prod'          : 0,
                                      'ng_price'         : 0,
                                      'condensate_prod'  : 0,
                                      'condensate_price' : 0,
                                      'ngls_prod'        : 0,
                                      'ngls_price'       : 0,
                                      'lng_prod'         : 0,
                                      'lng_price'        : 0,
                                      'capex_cost'       : 0,
                                      'opex_cost'        : 0,
                                      'abandonment_cost' : 0,
                                      'total_expenditure': 0,
                                      'total_revenue'    : 0,
                                      'cash_flow'        : 0} for prod_yr in cash_flow_years}
            if self.debugMode:
                print '%s - %s:' % (self.AssetId, self.model_section), 'col_data[h].keys() : {}'.format(sorted(col_data['h'].keys()))
                print '%s - %s:' % (self.AssetId, self.model_section), 'pre_tax_data.keys(): {}'.format(pre_tax_data.keys())

            for ij in range(0, len(cash_flow_years)):
                prod_year = cash_flow_years[ij]
                first_capex_year = min([int(capex_year) for capex_year in col_data['n'].keys() if col_data['n'][capex_year] > 0])
                last_abandon_year = max([int(abandon_year) for abandon_year in col_data['p'].keys()])

                # COMMODITY PRICES
                if prod_year in col_data['h'].keys() and prod_year >= first_capex_year and prod_year <= last_abandon_year:
                    pre_tax_data[prod_year]['crude_price'] = round(float(col_data['h'][prod_year]), self.roundAll)
                    pre_tax_data[prod_year]['ng_price'] = round(float(col_data['i'][prod_year]), self.roundAll)
                    pre_tax_data[prod_year]['condensate_price'] = round(float(col_data['j'][prod_year]), self.roundAll)
                    pre_tax_data[prod_year]['ngls_price'] = round(float(col_data['k'][prod_year]), self.roundAll)
                    pre_tax_data[prod_year]['lng_price'] = round(float(col_data['l'][prod_year]), self.roundAll)

                # CAPEX COST
                try:
                    opex_inflation_value = float(inflation_data['opex'][int(prod_year)])
                    capex_inflation_value = float(inflation_data['capex'][int(prod_year)])
                except:
                    opex_inflation_value = 1.0
                    capex_inflation_value = 1.0

                capex_cost_value = (round(float(col_data['n'][prod_year]), self.roundAll) + round(float(col_data['o'][prod_year]), self.roundAll)) * capex_inflation_value
                if prod_year > self.capexCapacityYear.get() and prod_year >= last_peak_year:
                    capex_cost_value *= self.capexCapacityFactor.get()

                pre_tax_data[prod_year]['capex_cost'] = float(capex_cost_value)

                year_len = len(cash_flow_years) - 10
                if (pre_prod_yrs - 1) < ij < year_len:
                    # COMMODITY PRODUCTION
                    pre_tax_data[prod_year]['crude_prod'] = round(float(col_data['b'][prod_year]) / float(self.days_in_year), self.roundAll)
                    pre_tax_data[prod_year]['ng_prod'] = round(float(col_data['c'][prod_year]) / float(self.days_in_year), self.roundAll)
                    pre_tax_data[prod_year]['condensate_prod'] = round(float(col_data['d'][prod_year]) / float(self.days_in_year), self.roundAll)
                    pre_tax_data[prod_year]['ngls_prod'] = round(float(col_data['e'][prod_year]) / float(self.days_in_year), self.roundAll)
                    pre_tax_data[prod_year]['lng_prod'] = round(float(col_data['f'][prod_year]) / float(self.days_in_year), self.roundAll)

                    # ABANDONMENT COST
                    pre_tax_data[prod_year]['abandonment_cost'] = round(float(col_data['p'][prod_year]), self.roundAll) * capex_inflation_value

                    # OPEX COST
                    opex_reduction_factor = 1.0
                    reduced_prod_years = zero_prod_years + prod_dec_years
                    if prod_year in reduced_prod_years:
                        if prod_year in zero_prod_years:
                            opex_reduction_factor *= self.opex_reduction
                        elif prod_year in prod_dec_years:
                            opex_reduction_factor *= (1.5 * self.opex_reduction)
                    if prod_year in low_prod_years:
                        if prod_year in prod_inc_years:
                            opex_reduction_factor *= (1.5 * self.opex_reduction)
                        else:
                            opex_reduction_factor *= self.opex_reduction
                    fixed_opex_value = round(float(col_data['r'][prod_year]), self.roundAll) * float(opex_inflation_value) * float(opex_reduction_factor)

                    if prod_year >= self.opexCapacityYear.get():
                        if prod_year >= self.opexCapacityYear2.get():
                            fixed_opex_value *= float(self.opexCapacityFactor2.get())
                        else:
                            fixed_opex_value *= float(self.opexCapacityFactor.get())

                    colb = pre_tax_data[prod_year]['crude_prod']
                    colc = pre_tax_data[prod_year]['ng_prod']
                    cold = pre_tax_data[prod_year]['condensate_prod']
                    cole = pre_tax_data[prod_year]['ngls_prod']
                    colf = pre_tax_data[prod_year]['lng_prod']

                    variable_opex_value = round((((colb + cold + cole) * float(var_opex_b)) + ((colc + colf) * float(var_opex_mmcf))) * self.days_in_year, self.roundAll) * opex_inflation_value
                    pre_tax_data[prod_year]['opex_cost'] = fixed_opex_value + variable_opex_value

                if ij >= (len(cash_flow_years) - 10):
                    pre_tax_data[prod_year]['abandonment_cost'] = round(col_data['p'][prod_year], self.roundAll)

                # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                pre_tax_data[prod_year]['total_expenditure'] = pre_tax_data[prod_year]['capex_cost'] + pre_tax_data[prod_year]['opex_cost'] + pre_tax_data[prod_year]['abandonment_cost']
                for comm_name in ['crude', 'condensate', 'ngls']:
                    pre_tax_data[prod_year]['total_revenue'] += (pre_tax_data[prod_year]['{}_prod'.format(comm_name)] * self.days_in_year * pre_tax_data[prod_year]['{}_price'.format(comm_name)])
                for comm_name in ['ng', 'lng']:
                    pre_tax_data[prod_year]['total_revenue'] += (pre_tax_data[prod_year]['{}_prod'.format(comm_name)] * self.days_in_year * 1000 * pre_tax_data[prod_year]['{}_price'.format(comm_name)])
                pre_tax_data[prod_year]['cash_flow'] = pre_tax_data[prod_year]['total_revenue'] - pre_tax_data[prod_year]['total_expenditure']
            if self.debugMode:
                for prod_yr in sorted(pre_tax_data.keys()):
                    for pre_tax_val in sorted(pre_tax_data[prod_yr].keys()):
                        print '%s - %s:' % (self.AssetId, self.model_section), '[economic limit] {}: {} = {}'.format(prod_yr, pre_tax_val, pre_tax_data[prod_yr][pre_tax_val])
                    print '------------------------------------------------------------------------------------'

            positive_cash_flow_years = [prod_yr for prod_yr in pre_tax_data.keys() if pre_tax_data[prod_yr]['cash_flow'] > 0]

            if positive_cash_flow_years:
                last_positive_year = max(positive_cash_flow_years)
                last_crude_prod_bd = round(pre_tax_data[last_positive_year]['crude_prod'], 2)
                last_ng_prod_mmcfd = round(pre_tax_data[last_positive_year]['ng_prod'], 2)
                last_condensate_prod_bd = round(pre_tax_data[last_positive_year]['condensate_prod'], 2)
                last_ngls_prod_bd = round(pre_tax_data[last_positive_year]['ngls_prod'], 2)
                last_lng_prod_bd = round(pre_tax_data[last_positive_year]['lng_prod'], 2)
                econ_limit_code = 0
            else:
                last_positive_year = cash_flow_years[pre_prod_yrs - 1]
                last_crude_prod_bd = 0
                last_ng_prod_mmcfd = 0
                last_condensate_prod_bd = 0
                last_ngls_prod_bd = 0
                last_lng_prod_bd = 0
                econ_limit_code = -1
                mErrorType = "ERROR TYPE 26"
                mComment = "NO POSITIVE CASH FLOW YEARS FOR ASSET {}".format(ast_id)
                self.asset_error_data.append((ast_id, mAsset_name, mCountry, mConstituent, mRegion, mStatus, mTerrain, "", "", mComment, mSessionKey, mErrorType))

            first_negative_year = last_positive_year + 1
            negative_year_count = last_model_year - last_positive_year

            if self.debugMode:
                print '%s - %s:' % (self.AssetId, self.model_section), 'last_positive_year          : {}'.format(last_positive_year)
                print '%s - %s:' % (self.AssetId, self.model_section), 'cash_flow from last_positive: {}'.format(['{}: {}'.format(prod_yr, pre_tax_data[prod_yr]['cash_flow']) for prod_yr in sorted(pre_tax_data.keys()) if prod_yr >= last_positive_year])
                print '%s - %s:' % (self.AssetId, self.model_section), 'last_model_year             : {}'.format(last_model_year)
                print '%s - %s:' % (self.AssetId, self.model_section), 'negative_year_count         : {}'.format(negative_year_count)
                print '%s - %s:' % (self.AssetId, self.model_section), 'self.negative_year_lim      : {}'.format(self.negative_year_lim)

            asset_id = self.param_data['asset_id']
            asset_name = self.param_data['asset_name']
            country = self.param_data['country']
            constituent = self.param_data['constituent']
            region = self.param_data['region']
            terrain = self.param_data['terrain']
            asset_status = self.param_data['status']

            peak_prod_commodity = self.commodity_names[self.param_data['peak_commodity']]
            peak_prod_year = self.param_data['peak_year']
            peak_prod_value = round(self.param_data['peak_prod'], 2)
            peak_prod_unit = self.param_data['peak_prod_unit']

            orig_abandon_year = last_model_year - 10
            curr_abandon_year = orig_abandon_year

            run_id = get_run_id()
            if negative_year_count > self.negative_year_lim and econ_limit_code == 0:
                if last_positive_year > discount_year:
                    econ_limit_code = 1
                    curr_abandon_year = last_positive_year
                    new_last_model_year = last_model_year - (negative_year_count - 10)

                    if self.debugMode:
                        for col in 'bcdefghijklmnopqrs':
                            print '%s - %s:' % (self.AssetId, self.model_section), 'col_data[{}]: {}'.format(col, ['{}: {}'.format(abandon_year, col_data[col][abandon_year]) for abandon_year in sorted(col_data[col].keys())])
                    for abandon_year in sorted([abandon_yr for abandon_yr in col_data['p'].keys() if col_data['p'][abandon_yr] > 0]):
                        new_abandon_yr = abandon_year - (negative_year_count - 10)
                        abandonment_value = col_data['p'][abandon_year]
                        if new_abandon_yr in col_data['p'].keys():
                            col_data['p'][new_abandon_yr] = abandonment_value
                            col_data['p'][abandon_year] = 0
                            if self.debugMode:
                                print '%s - %s:' % (self.AssetId, self.model_section), 'economic limit reached: abandonment value {} was shifted from year {} to year {}'.format(abandonment_value, abandon_year, new_abandon_yr)
                    if self.debugMode:
                        print ''
                    for model_year in [model_yr for model_yr in self.year if model_yr > last_positive_year]:
                        if model_year <= new_last_model_year:
                            col_str = 'bcdefnors'
                            if self.debugMode:
                                print '%s - %s:' % (self.AssetId, self.model_section), 'economic limit reached: data in columns {} set to 0 for year {}'.format(list(col_str), model_year)
                            for col in col_str:
                                col_data[col][model_year] = 0
                        else:
                            col_str = 'bcdefhijklmnopqr'
                            if self.debugMode:
                                print '%s - %s:' % (self.AssetId, self.model_section), 'economic limit reached: data in columns {} removed from model for year {}'.format(list(col_str), model_year)
                            for col in col_str:
                                if self.debugMode:
                                    print '%s - %s:' % (self.AssetId, self.model_section), 'col: {}'.format(col)
                                if model_year in col_data[col].keys():
                                    del col_data[col][model_year]
                    new_last_model_year = last_model_year - (negative_year_count - 10)
                    first_model_year = self.year[0]
                    self.year = range(first_model_year, new_last_model_year + 1)
                else:
                    econ_limit_code = 2
            econ_limit_params = [
                'asset_id',
                'asset_name',
                'country',
                'constituent',
                'region',
                'terrain',
                'asset_status',
                'peak_prod_commodity',
                'peak_prod_year',
                'peak_prod_value',
                'peak_prod_unit',
                'last_crude_prod_bd',
                'last_ng_prod_mmcfd',
                'last_condensate_prod_bd',
                'last_ngls_prod_bd',
                'last_lng_prod_bd',
                'negative_year_count',
                'first_negative_year',
                'orig_abandon_year',
                'curr_abandon_year',
                'econ_limit_code',
                'run_id'
            ]
            econ_param_str = ', '.join(econ_limit_params)

            param_vals = (
                econ_param_str,
                asset_id,
                asset_name,
                country,
                constituent,
                region,
                terrain,
                asset_status,
                peak_prod_commodity,
                peak_prod_year,
                peak_prod_value,
                peak_prod_unit,
                last_crude_prod_bd,
                last_ng_prod_mmcfd,
                last_condensate_prod_bd,
                last_ngls_prod_bd,
                last_lng_prod_bd,
                negative_year_count,
                first_negative_year,
                orig_abandon_year,
                curr_abandon_year,
                econ_limit_code,
                run_id
            )

            sql_insert = 'INSERT INTO economic_limit ({}) VALUES ({},"{}","{}","{}","{}","{}","{}","{}",{},{},"{}",{},{},{},{},{},{},{},{},{},{},"{}")'.format(*param_vals)
            if self.debugMode:
                print ''
                print '%s - %s:' % (self.AssetId, self.model_section), 'Economic limit update: {}'.format(sql_insert)
            mCur.execute(sql_insert)
            commit(mCur)

# END ECONOMIC LIMITS TEST -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



