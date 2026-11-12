import requests
import json
import numpy as np
import scipy




def get_prod_dates(start_date, date_count):
    prod_dates = ['{}{}'.format(prod_year, prod_month) for prod_year in range(1900, 2200) for prod_month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']]
    start_date_indx = prod_dates.index(start_date)
    return prod_dates[start_date_indx: start_date_indx+date_count]


def get_prod_curve_data(curr, profile_id):
    prod_curve_data = {}
    curr.execute("SELECT DISTINCT commodity, unit FROM US_Wells.dbo.tbltype_well_production WHERE profile_id={}".format(profile_id))
    commodity_data = curr.fetchall()
    for commodity, unit in commodity_data:
        prod_curve_data[commodity] = {'unit': unit, 'production': ()}
        curr.execute("SELECT MonthNo, Production FROM US_Wells.dbo.tbltype_well_production WHERE profile_id={} AND commodity='{}' AND unit='{}' ORDER BY MonthNo".format(profile_id, commodity, unit))
        comm_data = curr.fetchall()
        prod_curve_data[commodity]['production'] = find_curve_fit(comm_data)
    return prod_curve_data


def find_curve_fit(prod_data, commodity=''):
    well_life = 30
    years_before_terminal = 20
    monthly_decline = 0.05
    prod_periods = [int(month_num) for (month_num, prod_val) in prod_data]
    prod_values  = [float(prod_val) for (month_num, prod_val) in prod_data]

    Qi = prod_values[0]
    xdata = np.arange(len(prod_periods))
    ydata = np.array(prod_values)

    def decline_curve(x, b, Di):
        return float(Qi) / (1.0 + ( b*Di*x) )**(1.0/float(b))

    def prod_decline(x, b, Di, Dl, Dx, Dt):
        if x.all( ) /12.0 > Dl:
            Qx = 0
        elif x.all( ) /12.0 > Dx:
            Qx = prod_decline( x -1, b, Di, Dl, Dx, Dt) * ( 1 -Dt)
        else:
            Qx = decline_curve(x, b, Di)
        return Qx

    popt, pcov = scipy.optimize.curve_fit(decline_curve, xdata, ydata, maxfev=10000, p0=init_params)
    b, Di = popt

    #xdata = np.arange(well_life * 12)
    #ydata = prod_decline(xdata, b, Di, well_life, years_before_terminal, monthly_decline)
    #prod_vals = ydata.tolist()
    #last_srcd_indx = len(prod_periods) - 1
    #curve_diff = max(prod_vals[last_srcd_indx] - prod_values[-1], 0)
    #forecast_vals = [max(prod_val - curve_diff, 0) for prod_val in prod_vals if (prod_val - curve_diff) < prod_values[-1]]
    #all_prod_vals = prod_values + forecast_vals
    #prod_months = get_prod_dates(prod_periods[0], len(all_prod_vals))
    #prod_forecast = zip(prod_months, all_prod_vals)
    curve_params = {'commodity': commodity, 'b': b, 'Di': Di}
    return curve_params