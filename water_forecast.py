WATER_PCT_SLOPE_DEFAULT = 0.0012
WATER_CUT_DEFAUT        = 0
MAX_WATER_CUT_PCT       = 0.95


def get_total_prod(well_forecast_data, period, debug=False):
    comms = ["OIL", "GAS", "CONDENSATE", "NGL"]
    total_prod = 0
    for comm in comms:
        comm_prod = well_forecast_data[comm][period]
        if comm == "GAS":
            comm_prod = float(comm_prod)/6.0
        total_prod += comm_prod
    return total_prod

def get_init_water_cut(well_forecast_data, last_sourced_prod, debug=False):
    try:
        # If available, use last sourced water cut =: water production/(water production + hydrocarbon production)
        last_sourced_water_prod = float(well_forecast_data['WATER'][last_sourced_prod])
        # Calculate total production of forecast data in boe
        last_sourced_total_prod = float(get_total_prod(well_forecast_data, last_sourced_prod, debug=debug))
        if float(last_sourced_water_prod + last_sourced_total_prod) > 0:
            init_water_cut = last_sourced_water_prod/float(last_sourced_water_prod + last_sourced_total_prod)
        else:
            init_water_cut = WATER_CUT_DEFAULT
    # Use water cut default of 0 if no historical water production exists
    except:
        init_water_cut = WATER_CUT_DEFAULT
    return init_water_cut


def get_water_cut(period, init_water_cut, water_pct_slope=None, debug=False):
    # water_cut = m*x + b -- linear increasing value
    # Use initial water cut as starting point (b == y-intercept) where x = 0
    # Use default water % slope (m) to represent the increasing water cut throughout well life
    if water_pct_slope is None:
        water_pct_slope = WATER_PCT_SLOPE_DEFAULT
    water_cut = min(MAX_WATER_CUT_PCT, (water_pct_slope * period) + init_water_cut)
    return water_cut





def forecast_water_prod(well_forecast_data, last_sourced_prod, debug=False):
    # Identify forecast dates and determine initial water cut
    forecast_periods = [prod_period for prod_period in well_forecast_data['WATER'].keys() if prod_period >= last_sourced_prod]
    init_water_cut = get_init_water_cut(well_forecast_data, last_sourced_prod, debug=debug)
    if init_water_cut:
        for period in range(len(forecast_periods)):
            prod_date = forecast_periods[period]
            period_total_prod = float(get_total_prod(well_forecast_data, prod_date, debug=debug))
            water_cut = float(get_water_cut(period, init_water_cut, debug=debug))
            # Calculate water production after water cut and total hydrocarbon production are calculated
            water_prod = period_total_prod * float(water_cut / float(1 - water_cut))
            well_forecast_data['WATER'][prod_date] = water_prod
    return well_forecast_data


























