from globaldata import *

# get_arps_variables = ('EXP', [np.exp(lnqi)[{}], exp_di[{}]]'.format(np.exp(lnqi), exp_di), self.r2)     # Exponentioal Decline Variables
# get_arps_variables = ("HYP", [qi[{}], b[{}], di[{}]]'.format(*self.parameters, self.r2)                 # Hyperbolic Decline Variables

def decline_curve(x, b, Di):
    return float(Qi) / (1.0 + (b * Di * x)) ** (1.0 / float(b))


def prod_decline(x, b, Di, max_loops, TimeVar, Dt):
    if x.all() > max_loops:
        Qx = 0
    elif x.all()  > TimeVar:
        Qx = prod_decline(x - 1, b, Di, max_loops, TimeVar, Dt) * (1 - Dt)
    else:
        Qx = decline_curve(x, b, Di)
    return Qx


b  = min(max(float(round(abs(results[1][1]), 8)), 0.05), 0.99)
Di = abs(float(round(results[1][-1], 8)))

xdata = np.arange(max_loops)
ydata = prod_decline(xdata, b, Di, well_life, years_before_terminal, monthly_decline)
prod_vals = ydata.tolist()
last_srcd_indx = len(prod_periods) - 1

if debug:
    print 'prod_vals ({})  : {}'.format(len(prod_vals), prod_vals)
    print 'prod_values ({}): {}'.format(len(prod_values), prod_values)
    print 'last_srcd_indx  : {}'.format(last_srcd_indx)

curve_diff = max(prod_vals[last_srcd_indx] - prod_values[-1], 0)
forecast_vals = [max(prod_val - curve_diff, 0) for prod_val in prod_vals if (prod_val - curve_diff) < prod_values[-1]]

all_prod_vals = prod_values + forecast_vals
prod_months = get_prod_dates(prod_periods[0], len(all_prod_vals))

prod_forecast = dict(zip(prod_months, all_prod_vals))