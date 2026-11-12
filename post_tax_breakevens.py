# Default values and constants used in post-tax breakeven process

GOAL        = 0
INIT_GUESS  = 10
INIT_INCR   = 15
INCR_MIN    = 0.1
ZERO_range  = 0.1
ITER_MAX    = 100
OUT_DEFAULT = 999999999


COMM_PRICE_DEFAULTS = {
    "Natural Gas": 2.64,
    "NGLs"       : 24.71,
    "Condensate" : 44.78,
    "Crude Oil"  : 55.94
}

cost_inputs = {
    "completion_cost_pct"       : 0.0,
    "drilling_cost_pct"         : 0.0,
    "facilities_cost_pct"       : 0.0,
    "lateral_length_ft"         : 0.0,
    "well_cost_usd_ft"          : 0.0,
    "cost_capex_abandonment_usd": 0.0,
    "cost_capex_maintenance_usd": 0.0,
    "cost_opex_loe_usd_boe"     : 0.0,
    "loe_primary_usd_boe"       : 0.0,
    "cost_opex_water_usd_boe"   : 0.0,
    "cost_opex_gpt_usd_boe"     : 0.0,
    "gpt_primary_usd_boe"       : 0.0,
    "cost_opex_ngl_usd_boe"     : 0.0,
    "cost_opex_fixed_usd"       : 0.0,
    "royalty_rate_pct"          : 0.0,
    "capex_tangible_split_pct"  : 0.0
}

annual_prod_data = {
    "OIL"       : {prod_year: 0 for prod_year in prod_years},
    "GAS"       : {prod_year: 0 for prod_year in prod_years},
    "CONDENSATE": {prod_year: 0 for prod_year in prod_years},
    "NGL"       : {prod_year: 0 for prod_year in prod_years},
    "WATER"     : {prod_year: 0 for prod_year in prod_years}
}


# Functions used to generate input for Post-tax Breakeven Process ---------------------------------------------------------------------------------------------------------------------------------------------------

def get_production_data(curr, well_api, sql_where='', order_by='ORDER BY [Period]', hist_prod=False, all_prod=False, data_comms=[], debug=False):
    sql_and = ''
    sql_order = ''
    sql_sources = ''
    peak_comm_date = '{}01'.format(CURRENT_YEAR)
    production_data = {prod_comm: {} for prod_comm in PROD_COMMS}

    if all_prod:
        sql_sources = "Sources IN ('Historical', 'EST: Forecast Engine')"
    elif hist_prod:
        sql_sources = "Sources='Historical'"

    if sql_where:
        sql_and = 'AND {}'.format(sql_where)
    if data_comms:
        production_data = {prod_comm: {} for prod_comm in data_comms}
    if order_by:
        sql_order = order_by
    for prod_comm in production_data.keys():
        curr.execute(comm_sql[prod_comm].format(well_api, sql_sources, sql_and, sql_order))
        prod_data = curr.fetchall()
        for datarow in prod_data:
            for i in range(1, len(datarow)):
                prod_year = datarow[0]
                prod_month = month_nums[i]
                prod_date = '{}{}'.format(prod_year, prod_month)
                if datarow[i]:
                    production_data[prod_comm][prod_date] = float(datarow[i])
                else:
                    production_data[prod_comm][prod_date] = 0
    if debug:
        for prod_comm in PROD_COMMS:
            print well_api, ['{}: {}'.format(prod_date, production_data[prod_comm][prod_date]) for prod_date in sorted(production_data[prod_comm].keys())]
    return production_data


def calculate_annual_production(well_forecast_data, debug=False):
    conv_factor = {
        "OIL"       : 1.0,
        "GAS"       : 1.0/6.0,
        "CONDENSATE": 1.0,
        "NGL"       : 1.0,
        "WATER"     : 1.0
    }
    prod_years = sorted(list(set([int(prod_date[:4]) for prod_date in well_forecast_data[well_forecast_data.keys()[0]].keys()])))
    annual_prod_data = {prod_comm: {prod_year: 0 for prod_year in prod_years} for prod_comm in PROD_COMMS}
    annual_prod_data["TOTAL"] = {prod_year: 0 for prod_year in prod_years}
    for prod_comm in PROD_COMMS:
        for prod_year in prod_years:
            prod_value = sum([well_forecast_data[prod_comm][prod_date] for prod_date in well_forecast_data[prod_comm].keys() if int(prod_date[:4])==prod_year])
            annual_prod_data[prod_comm][prod_year] += prod_value
            if prod_comm != "WATER":
                annual_prod_data["TOTAL"][prod_year] += (conv_factor[prod_comm] * prod_value)
    return annual_prod_data


def get_eur_totals(annual_prod_data, debug=False):
    eur_params = {
        "OIL"        : "eur_oil",
        "GAS"        : "eur_gas",
        "CONDENSATE" : "eur_condensate",
        "NGL"        : "eur_ngls",
        "TOTAL"      : "eur_total"
        }
    eur_totals = {
        "eur_oil"       : 0,
        "eur_gas"       : 0,
        "eur_condensate": 0,
        "eur_ngls"      : 0,
        "eur_total"     : 0
    }
    for prod_comm in ["OIL", "CONDENSATE", "NGL", "GAS", "TOTAL"]:
        for prod_year in annual_prod_data[prod_comm].keys():
            eur_totals[eur_params[prod_comm]] += annual_prod_data[prod_comm][prod_year]
    return eur_totals


def get_cost_inputs(well_api, debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells', external=False)
    curr = conn.cursor()
    cost_inputs = {
        "completion_cost_pct"       : 0.0,
        "drilling_cost_pct"         : 0.0,
        "facilities_cost_pct"       : 0.0,
        "lateral_length_ft"         : 0.0,
        "well_cost_usd_ft"          : 0.0,
        "cost_capex_abandonment_usd": 0.0,
        "cost_capex_maintenance_usd": 0.0,
        "cost_opex_loe_usd_boe"     : 0.0,
        "loe_primary_usd_boe"       : 0.0,
        "cost_opex_water_usd_boe"   : 0.0,
        "cost_opex_gpt_usd_boe"     : 0.0,
        "gpt_primary_usd_boe"       : 0.0,
        "cost_opex_ngl_usd_boe"     : 0.0,
        "cost_opex_fixed_usd"       : 0.0,
        "royalty_rate_pct"          : 0.0,
        "capex_tangible_split_pct"  : 0.0
    }

    cost_params = sorted(cost_inputs.keys())
    param_str = ",".join(['ISNULL({},0)'.format(cost_param) for cost_param in cost_params])
    sql_select = "SELECT TOP 1 {} FROM US_Wells.dbo.tblUSWell_Parameters WHERE API_Number LIKE '%{}%'".format(param_str, well_api)
    curr.execute(sql_select)
    typewell_params = curr.fetchone()
    if well_api and typewell_params:
        for i in range(len(cost_params)):
            cost_param = cost_params[i]
            cost_inputs[cost_param] = typewell_params[i]
            if debug: print well_api,'\t',cost_param,'-',typewell_params[i]
        if debug: print '\n'
    curr.close()
    conn.close()
    return cost_inputs


def get_main_comm(well_econ_data, debug=False):
    main_comm = 'GAS'
    total_oil_prod  = well_econ_data["well_eur_oil_bbl"]
    total_cond_prod = well_econ_data["well_eur_condensate_bbl"]
    total_prod      = well_econ_data['well_eur_total_boe']
    if float(total_oil_prod + total_cond_prod) > (float(total_prod ) /2.0):
        main_comm = 'OIL'
    return main_comm


# Used to calculate well economics and determine economic limit and used to test different prices during the goal seek process of post-tax breakeven function -------------------------------------------------------

def calc_well_economics(well_api, annual_prod_data, eur_totals, cost_inputs, commodity_prices={}, econ_forecast_end=None, calc_econ_limit=False, debug=False):
    drilling_cost = 0
    completion_cost = 0
    facility_cost = 0

    ngls_proc_fee = 0
    water_disp_fee = 0
    fixed_opex_rate = 0
    abandonment = 0
    royalty_rate = 0
    total_prod = 0
    pre_tax_NPV = 0
    post_tax_NPV = 0

    total_oil_revenue = 0
    total_gas_revenue = 0
    total_cond_revenue = 0
    total_ngls_revenue = 0
    total_gross_revenue = 0
    total_net_revenue = 0
    total_capex_tangible = 0
    total_capex_intangible = 0
    total_capex = 0
    total_variable_opex = 0
    total_fixed_opex = 0
    total_opex = 0
    total_abandonment = 0
    total_production_tax = 0
    total_depreciation = 0
    total_net_income = 0
    total_state_tax = 0
    total_federal_tax = 0
    total_pre_tax_cf = 0
    total_post_tax_cf = 0
    total_disc_pre_tax_cf = 0
    total_disc_post_tax_cf = 0
    pre_tax_cash_flows = []
    post_tax_cash_flows = []

    # Determine the years to include in economic forecast
    prod_years = sorted(annual_prod_data["TOTAL"].keys())
    development_year = prod_years[0] - 1
    prod_years = [development_year] + prod_years
    if econ_forecast_end:
        last_econ_year = econ_forecast_end
    else:
        last_econ_year = max(prod_years)
    prod_years = [prod_year for prod_year in prod_years if prod_year <= last_econ_year]

    well_econ_data = {
        "prod_years"                  : prod_years,
        "param_data"                  : {
            "drilling_cost"  : 0,
            "completion_cost": 0,
            "facility_cost"  : 0,
            "ngls_proc_fee"  : 0,
            "water_disp_fee" : 0,
            "fixed_opex_rate": 0,
            "abandonment"    : 0,
            "oil_price"      : 0,
            "gas_price"      : 0,
            "cond_price"     : 0,
            "ngls_price"     : 0,
            "royalty_rate"   : 0
        },

        "oil_prod"                    : {prod_year: 0 for prod_year in prod_years},
        "gas_prod"                    : {prod_year: 0 for prod_year in prod_years},
        "cond_prod"                   : {prod_year: 0 for prod_year in prod_years},
        "ngls_prod"                   : {prod_year: 0 for prod_year in prod_years},
        "water_prod"                  : {prod_year: 0 for prod_year in prod_years},
        "total_prod"                  : {prod_year: 0 for prod_year in prod_years},
        "oil_revenue"                 : {prod_year: 0 for prod_year in prod_years},
        "gas_revenue"                 : {prod_year: 0 for prod_year in prod_years},
        "cond_revenue"                : {prod_year: 0 for prod_year in prod_years},
        "ngls_revenue"                : {prod_year: 0 for prod_year in prod_years},
        "gross_revenue"               : {prod_year: 0 for prod_year in prod_years},
        "net_revenue"                 : {prod_year: 0 for prod_year in prod_years},
        "prod_tax_value"              : {prod_year: 0 for prod_year in prod_years},
        "depreciation"                : {prod_year: 0 for prod_year in prod_years},
        "capex"                       : {prod_year: 0 for prod_year in prod_years},
        "capex_tangible"              : {prod_year: 0 for prod_year in prod_years},
        "capex_intangible"            : {prod_year: 0 for prod_year in prod_years},
        "abandonment"                 : {prod_year: 0 for prod_year in prod_years},
        "opex"                        : {prod_year: 0 for prod_year in prod_years},
        "variable_opex"               : {prod_year: 0 for prod_year in prod_years},
        "fixed_opex"                  : {prod_year: 0 for prod_year in prod_years},
        "net_income"                  : {prod_year: 0 for prod_year in prod_years},
        "state_tax_rate"              : {prod_year: 0 for prod_year in prod_years},
        "state_tax_value"             : {prod_year: 0 for prod_year in prod_years},
        "federal_tax_value"           : {prod_year: 0 for prod_year in prod_years},
        "pre_tax_cf"                  : {prod_year: 0 for prod_year in prod_years},
        "disc_pre_tax_cf"             : {prod_year: 0 for prod_year in prod_years},
        "post_tax_cf"                 : {prod_year: 0 for prod_year in prod_years},
        "disc_post_tax_cf"            : {prod_year: 0 for prod_year in prod_years},
        "fiscal_take"                 : {prod_year: 0 for prod_year in prod_years},

        "last_econ_year"              : last_econ_year,
        "well_api"                    : well_api,
        "state_id"                    : int(well_api[:2]),
        "total_oil_revenue"           : 0,
        "total_gas_revenue"           : 0,
        "total_cond_revenue"          : 0,
        "total_ngls_revenue"          : 0,
        "total_gross_revenue"         : 0,
        "total_net_revenue"           : 0,
        "total_capex_tangible"        : 0,
        "total_capex_intangible"      : 0,
        "total_capex"                 : 0,
        "total_variable_opex"         : 0,
        "total_fixed_opex"            : 0,
        "total_abandonment"           : 0,
        "total_production_tax"        : 0,
        "total_depreciation"          : 0,
        "total_net_income"            : 0,
        "total_state_tax"             : 0,
        "total_federal_tax"           : 0,
        "total_disc_pre_tax_cf"       : 0,
        "total_disc_post_tax_cf"      : 0,

        "royalty_rate_pct"            : 0,
        "pre_tax_cashflow_total_usd"  : 0,
        "post_tax_cashflow_total_usd" : 0,
        "pre_tax_BE_oil_usd_bbl"      : 0,
        "pre_tax_BE_gas_usd_mcf"      : 0,
        "post_tax_BE_oil_usd_bbl"     : 0,
        "post_tax_BE_gas_usd_mcf"     : 0,
        "well_eur_oil_bbl"            : 0,
        "well_eur_gas_mmcf"           : 0,
        "well_eur_condensate_bbl"     : 0,
        "well_eur_ngls_bbl"           : 0,
        "well_eur_total_boe"          : 0,
        "pre_tax_npv_usd"             : 0,
        "pre_tax_irr_pct"             : 0,
        "post_tax_npv_usd"            : 0,
        "post_tax_irr_pct"            : 0,
        "total_opex_mm_usd"           : 0,
        "total_well_cost_mm_usd"      : 0,
        "cost_capex_drilling_mm_usd"  : 0,
        "cost_capex_completion_mm_usd": 0,
        "cost_capex_facilities_mm_usd": 0
    }

    if commodity_prices:
        oil_price = commodity_prices["Crude Oil"]
        gas_price = commodity_prices["Natural Gas"]
        cond_price = commodity_prices["Condensate"]
        ngls_price = commodity_prices["NGLs"]
    else:
        oil_price = get_commodity_price("Crude Oil")
        gas_price = get_commodity_price("Natural Gas")
        cond_price = get_commodity_price("Condensate")
        ngls_price = get_commodity_price("NGLs")

    well_econ_data["param_data"]["oil_price"] = oil_price
    well_econ_data["param_data"]["gas_price"] = gas_price
    well_econ_data["param_data"]["cond_price"] = cond_price
    well_econ_data["param_data"]["ngls_price"] = ngls_price

    well_econ_data["well_eur_oil_bbl"] = eur_totals["eur_oil"]
    well_econ_data["well_eur_gas_mmcf"] = eur_totals["eur_gas"]
    well_econ_data["well_eur_condensate_bbl"] = eur_totals["eur_condensate"]
    well_econ_data["well_eur_ngls_bbl"] = eur_totals["eur_ngls"]
    well_econ_data["well_eur_total_boe"] = eur_totals["eur_total"]

    royalty_rate = get_royalty_rate(well_econ_data['state_id'])
    well_econ_data["param_data"]["royalty_rate"] = royalty_rate
    well_econ_data["royalty_rate_pct"] = royalty_rate

    total_well_cost = cost_inputs["well_cost_usd_ft"] * cost_inputs["lateral_length_ft"]

    if cost_inputs["drilling_cost_pct"] is not None:
        drilling_cost = total_well_cost * cost_inputs["drilling_cost_pct"]
        well_econ_data["param_data"]["drilling_cost"] = drilling_cost

    if cost_inputs["completion_cost_pct"] is not None:
        completion_cost = total_well_cost * cost_inputs["completion_cost_pct"]
        well_econ_data["param_data"]["completion_cost"] = completion_cost

    if cost_inputs["facilities_cost_pct"] is not None:
        facility_cost = total_well_cost * cost_inputs["facilities_cost_pct"]
        well_econ_data["param_data"]["facility_cost"] = facility_cost

    if cost_inputs["cost_opex_ngl_usd_boe"] is not None:
        ngls_proc_fee = cost_inputs["cost_opex_ngl_usd_boe"]
        well_econ_data["param_data"]["ngls_proc_fee"] = ngls_proc_fee

    if cost_inputs["cost_opex_water_usd_boe"] is not None:
        water_disp_fee = cost_inputs["cost_opex_water_usd_boe"]
        well_econ_data["param_data"]["water_disp_fee"] = water_disp_fee

    if cost_inputs["cost_opex_fixed_usd"] is not None:
        fixed_opex_rate = cost_inputs["cost_opex_fixed_usd"]
        well_econ_data["param_data"]["fixed_opex_rate"] = fixed_opex_rate

    if cost_inputs["cost_capex_abandonment_usd"] is not None:
        abandonment = cost_inputs["cost_capex_abandonment_usd"]
        well_econ_data["param_data"]["abandonment"] = abandonment

    if debug and 0:
        print "oil_price         : ", oil_price
        print "gas_price         : ", gas_price
        print "cond_price        : ", cond_price
        print "ngls_price        : ", ngls_price
        print "drilling_cost     : ", drilling_cost
        print "completion_cost   : ", completion_cost
        print "facility_cost     : ", facility_cost
        print "ngls_proc_fee     : ", ngls_proc_fee
        print "water_disp_fee    : ", water_disp_fee
        print "fixed_opex_rate   : ", fixed_opex_rate

    # Calculate total prod using all annual commodity production
    # Calculate gross revenue using all commodity production and commodity prices
    # Calculate capex, opex, pre-tax cash flow, pre-tax NPV, pre-tax IRR
    # Store as annual numbers in well_econ table and query table for sum of each column to output into well economics
    forecast_econ = True
    econ_year = 0
    for prod_year in prod_years:
        prod_year_num = prod_year - development_year
        if prod_year_num:
            oil_prod   = annual_prod_data["OIL"][prod_year]
            gas_prod   = annual_prod_data["GAS"][prod_year]
            cond_prod  = annual_prod_data["CONDENSATE"][prod_year]
            ngls_prod  = annual_prod_data["NGL"][prod_year]
            water_prod = annual_prod_data["WATER"][prod_year]
            total_prod = annual_prod_data["TOTAL"][prod_year]
        else:
            oil_prod   = 0
            gas_prod   = 0
            cond_prod  = 0
            ngls_prod  = 0
            water_prod = 0
            total_prod = 0

        if (total_prod or not prod_year_num) and forecast_econ:
            oil_revenue       = (oil_prod * oil_price)
            gas_revenue       = (gas_prod * gas_price)
            cond_revenue      = (cond_prod * cond_price)
            ngls_revenue      = (ngls_prod * ngls_price)
            gross_revenue     = round(float((oil_prod * oil_price) + (gas_prod * gas_price) + (cond_prod * cond_price) + (ngls_prod * ngls_price)), 2)
            net_revenue       = round(float(gross_revenue * (1 - royalty_rate)), 2)
            prod_tax_value    = get_production_tax(prod_year_num, well_api, oil_prod, gas_prod, cond_prod, ngls_prod, oil_price, gas_price, cond_price, ngls_price, cost_inputs)
            depreciation      = get_depreciation(prod_year_num, total_well_cost, cost_inputs)

            capex_tangible    = get_capex_tangible(prod_year_num, total_well_cost, cost_inputs)
            capex_intangible  = get_capex_intangible(prod_year_num, total_well_cost, cost_inputs)
            capex             = round(float(capex_tangible + capex_intangible), 2)

            variable_opex     = get_variable_opex(prod_year_num, total_prod, ngls_prod, water_prod, cost_inputs)
            fixed_opex        = get_fixed_opex(prod_year_num, cost_inputs)
            opex              = round(float(variable_opex + fixed_opex), 2)

            net_income        = round(float(net_revenue - (prod_tax_value + capex_intangible + opex + depreciation)), 2)
            state_tax_rate    = get_state_tax_rate(prod_year, well_api)
            state_tax_value   = round(float(net_income * state_tax_rate), 2)
            federal_tax_value = round(float((net_income - state_tax_value) * FEDERAL_TAX_RATE), 2)
            post_tax_cf       = round(float(net_revenue - (capex_intangible + opex + abandonment + prod_tax_value + state_tax_value + federal_tax_value)), 2)
            pre_tax_cf        = round(float(gross_revenue - capex - opex), 2)
            disc_pre_tax_cf   = round(float(pre_tax_cf / float(1.1 ** (prod_year_num - 1))), 2)
            disc_post_tax_cf  = round(float(post_tax_cf / float(1.1 ** (prod_year_num - 1))), 2)

            # Determine economic limit by stopping economic forecast when pre-tax cash flow is negative
            if pre_tax_cf > 0 or prod_year < (CURRENT_YEAR + 2) or not calc_econ_limit:
                econ_year = prod_year
                pre_tax_cash_flows.append(pre_tax_cf)
                post_tax_cash_flows.append(post_tax_cf)
                pre_tax_NPV            += disc_pre_tax_cf
                post_tax_NPV           += disc_post_tax_cf
                total_oil_revenue      += oil_revenue
                total_gas_revenue      += gas_revenue
                total_cond_revenue     += cond_revenue
                total_ngls_revenue     += ngls_revenue
                total_gross_revenue    += gross_revenue
                total_net_revenue      += net_revenue
                total_capex_tangible   += capex_tangible
                total_capex_intangible += capex_intangible
                total_capex            += capex
                total_variable_opex    += variable_opex
                total_fixed_opex       += fixed_opex
                total_opex             += opex
                total_abandonment      += abandonment
                total_production_tax   += prod_tax_value
                total_depreciation     += depreciation
                total_net_income       += net_income
                total_state_tax        += state_tax_value
                total_federal_tax      += federal_tax_value
                total_pre_tax_cf       += pre_tax_cf
                total_post_tax_cf      += post_tax_cf
                total_disc_pre_tax_cf  += disc_pre_tax_cf
                total_disc_post_tax_cf += disc_post_tax_cf

                well_econ_data["oil_prod"         ][prod_year] = oil_prod
                well_econ_data["gas_prod"         ][prod_year] = gas_prod
                well_econ_data["cond_prod"        ][prod_year] = cond_prod
                well_econ_data["ngls_prod"        ][prod_year] = ngls_prod
                well_econ_data["water_prod"       ][prod_year] = water_prod
                well_econ_data["total_prod"       ][prod_year] = total_prod
                well_econ_data["oil_revenue"      ][prod_year] = oil_price  * oil_prod
                well_econ_data["gas_revenue"      ][prod_year] = gas_price  * gas_prod
                well_econ_data["cond_revenue"     ][prod_year] = cond_price * cond_prod
                well_econ_data["ngls_revenue"     ][prod_year] = ngls_price * ngls_prod
                well_econ_data["gross_revenue"    ][prod_year] = gross_revenue
                well_econ_data["net_revenue"      ][prod_year] = net_revenue
                well_econ_data["prod_tax_value"   ][prod_year] = prod_tax_value
                well_econ_data["depreciation"     ][prod_year] = depreciation
                well_econ_data["capex"            ][prod_year] = capex
                well_econ_data["capex_tangible"   ][prod_year] = capex_tangible
                well_econ_data["capex_intangible" ][prod_year] = capex_intangible
                well_econ_data["abandonment"      ][prod_year] = 0
                well_econ_data["opex"             ][prod_year] = opex
                well_econ_data["variable_opex"    ][prod_year] = variable_opex
                well_econ_data["fixed_opex"       ][prod_year] = fixed_opex
                well_econ_data["net_income"       ][prod_year] = net_income
                well_econ_data["state_tax_rate"   ][prod_year] = state_tax_rate
                well_econ_data["state_tax_value"  ][prod_year] = state_tax_value
                well_econ_data["federal_tax_value"][prod_year] = federal_tax_value
                well_econ_data["post_tax_cf"      ][prod_year] = post_tax_cf
                well_econ_data["pre_tax_cf"       ][prod_year] = pre_tax_cf
                well_econ_data["disc_pre_tax_cf"  ][prod_year] = disc_pre_tax_cf
                well_econ_data["disc_post_tax_cf" ][prod_year] = disc_post_tax_cf
            else:
                forecast_econ = False
                last_econ_year = econ_year

    econ_year += 1
    prod_year_num = econ_year - development_year
    oil_revenue = 0
    gas_revenue = 0
    cond_revenue = 0
    ngls_revenue = 0
    gross_revenue = 0
    net_revenue = 0

    abandonment = get_abandonment(prod_year_num, cost_inputs)
    capex = abandonment
    variable_opex = 0
    fixed_opex = get_fixed_opex(prod_year_num, cost_inputs)
    opex = fixed_opex
    pre_tax_cf = round(float(gross_revenue - capex - opex), 2)
    pre_tax_cash_flows.append(pre_tax_cf)

    prod_tax_value = 0
    capex_intangible = 0
    capex_tangible = 0
    depreciation = 0
    state_tax_rate = get_state_tax_rate(econ_year, well_api)
    net_income = -fixed_opex
    state_tax_value = round(float(net_income * state_tax_rate), 2)
    federal_tax_value = round(float((net_income - state_tax_value) * FEDERAL_TAX_RATE), 2)
    post_tax_cf = round(float(net_revenue - (capex_intangible + opex + abandonment + prod_tax_value + state_tax_value + federal_tax_value)), 2)
    post_tax_cash_flows.append(post_tax_cf)

    pre_tax_irr_val = np.irr(np.array(pre_tax_cash_flows))
    if np.isnan(pre_tax_irr_val):
        pre_tax_IRR = 0
    else:
        pre_tax_IRR = round(float(pre_tax_irr_val), 2)

    post_tax_irr_val = np.irr(np.array(post_tax_cash_flows))
    if np.isnan(post_tax_irr_val):
        post_tax_IRR = 0
    else:
        post_tax_IRR = round(float(post_tax_irr_val), 2)

    disc_pre_tax_cf = round(float(pre_tax_cf / float(1.1 ** (econ_year - 1))), 2)
    disc_post_tax_cf = round(float(post_tax_cf / float(1.1 ** (econ_year - 1))), 2)

    pre_tax_NPV            += disc_pre_tax_cf
    post_tax_NPV           += disc_post_tax_cf
    total_oil_revenue      += oil_revenue
    total_gas_revenue      += gas_revenue
    total_cond_revenue     += cond_revenue
    total_ngls_revenue     += ngls_revenue
    total_gross_revenue    += gross_revenue
    total_net_revenue      += net_revenue
    total_capex_tangible   += capex_tangible
    total_capex_intangible += capex_intangible
    total_capex            += capex
    total_variable_opex    += variable_opex
    total_fixed_opex       += fixed_opex
    total_opex             += opex
    total_abandonment      += abandonment
    total_production_tax   += prod_tax_value
    total_depreciation     += depreciation
    total_net_income       += net_income
    total_state_tax        += state_tax_value
    total_federal_tax      += federal_tax_value
    total_pre_tax_cf       += pre_tax_cf
    total_post_tax_cf      += post_tax_cf
    total_disc_pre_tax_cf  += disc_pre_tax_cf
    total_disc_post_tax_cf += disc_post_tax_cf

    well_econ_data["oil_prod"         ][econ_year] = 0
    well_econ_data["gas_prod"         ][econ_year] = 0
    well_econ_data["cond_prod"        ][econ_year] = 0
    well_econ_data["ngls_prod"        ][econ_year] = 0
    well_econ_data["water_prod"       ][econ_year] = 0
    well_econ_data["total_prod"       ][econ_year] = 0
    well_econ_data["oil_revenue"      ][econ_year] = 0
    well_econ_data["gas_revenue"      ][econ_year] = 0
    well_econ_data["cond_revenue"     ][econ_year] = 0
    well_econ_data["ngls_revenue"     ][econ_year] = 0
    well_econ_data["gross_revenue"    ][econ_year] = 0
    well_econ_data["net_revenue"      ][econ_year] = 0
    well_econ_data["prod_tax_value"   ][econ_year] = 0
    well_econ_data["depreciation"     ][econ_year] = 0
    well_econ_data["capex_tangible"   ][econ_year] = 0
    well_econ_data["capex_intangible" ][econ_year] = 0
    well_econ_data["abandonment"      ][econ_year] = abandonment
    well_econ_data["capex"            ][econ_year] = capex
    well_econ_data["variable_opex"    ][econ_year] = 0
    well_econ_data["fixed_opex"       ][econ_year] = fixed_opex
    well_econ_data["opex"             ][econ_year] = opex
    well_econ_data["net_income"       ][econ_year] = net_income
    well_econ_data["state_tax_rate"   ][econ_year] = state_tax_rate
    well_econ_data["state_tax_value"  ][econ_year] = state_tax_value
    well_econ_data["federal_tax_value"][econ_year] = federal_tax_value
    well_econ_data["post_tax_cf"      ][econ_year] = post_tax_cf
    well_econ_data["pre_tax_cf"       ][econ_year] = pre_tax_cf
    well_econ_data["disc_pre_tax_cf"  ][econ_year] = disc_pre_tax_cf
    well_econ_data["disc_post_tax_cf" ][econ_year] = disc_post_tax_cf

    # Parameters not stored in database for each well
    well_econ_data["total_oil_revenue"	         ] = total_oil_revenue
    well_econ_data["total_gas_revenue"	         ] = total_gas_revenue
    well_econ_data["total_cond_revenue"	         ] = total_cond_revenue
    well_econ_data["total_ngls_revenue"	         ] = total_ngls_revenue
    well_econ_data["total_gross_revenue"         ] = total_gross_revenue
    well_econ_data["total_net_revenue"	         ] = total_net_revenue
    well_econ_data["total_capex_tangible"        ] = total_capex_tangible
    well_econ_data["total_capex_intangible"      ] = total_capex_intangible
    well_econ_data["total_capex"		         ] = total_capex
    well_econ_data["total_variable_opex"         ] = total_variable_opex
    well_econ_data["total_fixed_opex"	         ] = total_fixed_opex
    well_econ_data["total_abandonment"	         ] = total_abandonment
    well_econ_data["total_production_tax"        ] = total_production_tax
    well_econ_data["total_depreciation"	         ] = total_depreciation
    well_econ_data["total_net_income"	         ] = total_net_income
    well_econ_data["total_state_tax"	         ] = total_state_tax
    well_econ_data["total_federal_tax"	         ] = total_federal_tax
    well_econ_data["total_disc_pre_tax_cf"       ] = total_disc_pre_tax_cf
    well_econ_data["total_disc_post_tax_cf"      ] = total_disc_post_tax_cf
    well_econ_data["last_econ_year"              ] = last_econ_year
    well_econ_data["prod_years"                  ] = [prod_year for prod_year in prod_years if prod_year <= last_econ_year]

    # Parameters stored in tblUSWell_Parameters for each well
    well_econ_data["pre_tax_cashflow_total_usd"	 ] = total_pre_tax_cf
    well_econ_data["post_tax_cashflow_total_usd" ] = total_post_tax_cf
    well_econ_data["total_opex_mm_usd"			 ] = total_opex
    well_econ_data["post_tax_irr_pct"            ] = post_tax_IRR
    well_econ_data["post_tax_npv_usd"            ] = post_tax_NPV
    well_econ_data["pre_tax_irr_pct"             ] = pre_tax_IRR
    well_econ_data["pre_tax_npv_usd"             ] = pre_tax_NPV
    well_econ_data["total_well_cost_mm_usd"      ] = total_well_cost
    well_econ_data["cost_capex_drilling_mm_usd"  ] = drilling_cost
    well_econ_data["cost_capex_completion_mm_usd"] = completion_cost
    well_econ_data["cost_capex_facilities_mm_usd"] = facility_cost

    return well_econ_data


# Used as support functions for post-tax breakeven process ----------------------------------------------------------------------------------------------------------------------------------------------------------

def test_commodity_price(well_api, annual_prod_data, eur_totals, cost_inputs, commodity_prices, last_econ_year, debug=False):
    well_econ_data = calc_well_economics(well_api, annual_prod_data, eur_totals, cost_inputs, commodity_prices=commodity_prices, econ_forecast_end=last_econ_year, debug=debug)
    pre_tax_NPV = well_econ_data["pre_tax_npv_usd"]
    return pre_tax_NPV


def check_guess(guess, main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, last_econ_year, debug=False, check_plus_minus=False):
    outcome = OUT_DEFAULT
    comm_price_data = COMM_PRICE_DEFAULTS.copy()
    if main_comm == "OIL":
        comm_price_data["Crude Oil"]   = guess
        comm_price_data["Condensate"]  = guess
    else:
        comm_price_data["Natural Gas"] = guess
    outcome = test_commodity_price(well_api, annual_prod_data, eur_totals, cost_inputs, commodity_prices=comm_price_data, last_econ_year=last_econ_year, debug=debug)
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


def check_plus_minus(guess, main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, last_econ_year, debug=False):
    check_val = False
    guess_plus  = check_guess(guess + INCR_MIN, main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, last_econ_year=last_econ_year, debug=debug, check_plus_minus=True)
    guess_minus = check_guess(guess - INCR_MIN, main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, last_econ_year=last_econ_year, debug=debug, check_plus_minus=True)
    if get_outcome_sign(guess_plus) == -get_outcome_sign(guess_minus):
        check_val = True
    return check_val


def goal_seek(main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, debug=False):
    goal_reached = False
    breakeven_val = OUT_DEFAULT
    last_outcome = 0
    iter_count = 1
    while not goal_reached:
        if iter_count == 1:
            last_outcome = check_guess(INIT_GUESS, main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, last_econ_year=last_econ_year, debug=debug)
            outcome = check_guess(INIT_GUESS+INIT_INCR, main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, last_econ_year=last_econ_year, debug=debug)
            last_guess = INIT_GUESS
            last_increment = INIT_INCR
            try:
                increment = float(last_increment * outcome)/float(last_outcome - outcome)
            except:
                iter_count = ITER_MAX
            guess = last_guess + increment
        outcome = check_guess(guess, main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, last_econ_year=last_econ_year, debug=debug)
        sign = get_outcome_sign(outcome)
        if check_plus_minus(guess, main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, last_econ_year=last_econ_year, debug=debug):
            breakeven_val = guess
            goal_reached = True
        if sign == 0:
            breakeven_val = guess
            goal_reached = True
        elif iter_count >= ITER_MAX:
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
    return breakeven_val


# Main function to calculate post-tax breakeven values ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def calc_post_tax_breakeven(last_econ_year, main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, debug=False):
    post_tax_be = {"OIL": 0.0, "GAS": 0.0}
    post_tax_be[main_comm] = goal_seek(main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, last_econ_year=last_econ_year, debug=debug)
    post_tax_BE_oil_usd_bbl = round(float(post_tax_be["OIL"]),2)
    post_tax_BE_gas_usd_mcf = round(float(post_tax_be["GAS"]),2)
    return post_tax_BE_oil_usd_bbl, post_tax_BE_gas_usd_mcf


# Main function to execute entire post-tax breakeven process from gathering inputs to calculating the output values --------------------------------------------------------------------------------------------------

def main(well_api, debug=False):
    conn = get_connection(server='sql_server', database='US_Wells', external=False)
    curr = conn.cursor()

    forecast_data = get_production_data(curr=curr, well_api=well_api, all_prod=True, debug=debug)
    annual_prod_data = calculate_annual_production(forecast_data, debug=debug)
    eur_totals = get_eur_totals(annual_prod_data, debug=debug)
    cost_inputs = get_cost_inputs(well_api, debug=debug)
    well_econ_data = calc_well_economics(well_api, annual_prod_data, eur_totals, cost_inputs, commodity_prices=commodity_prices, econ_forecast_end=econ_forecast_end, calc_econ_limit=calc_econ_limit, debug=debug)
    main_comm = get_main_comm(well_econ_data, debug=debug)
    post_tax_BE_oil_usd_bbl, post_tax_BE_gas_usd_mcf = calc_post_tax_breakeven(last_econ_year, main_comm, well_api, annual_prod_data, eur_totals, cost_inputs, debug=debug)

    curr.close()
    conn.close()
    return post_tax_BE_oil_usd_bbl, post_tax_BE_gas_usd_mcf


if __name__ == '__main__':
    # List for wells for a state, collection of states, pool of wells, etc.
    well_list = []
    for well_api in well_list:
        post_tax_oil_breakeven_usd_bbl, post_tax_gas_breakeven_usd_mcf = main(well_api, debug=True)