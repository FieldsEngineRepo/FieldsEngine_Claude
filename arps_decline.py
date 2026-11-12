import globaldata as gd
import numpy as np
import scipy.optimize



def find_curve_fit(well_life=None, prod_periods=None, prod_values=None, curve_params={}, optimize=True, debug=False):
    conn = gd.get_connection()
    curr = conn.cursor()

    Qi             = 0
    xdata          = np.zeros(1)
    ydata          = np.zeros(1)
    init_params    = None
    years_before_terminal = 2
    monthly_decline  = 0.02

    if not well_life:
        well_life = 20

    if prod_values:
        Qi = prod_values[0]
        xdata = np.arange(len(prod_periods))
        ydata = np.array(prod_values)

    if curve_params:
        if debug:
            print "curve_params:", curve_params
        if curve_params["Qi"]:
            Qi = curve_params["Qi"]
        if curve_params["b"]:
            b  = curve_params["b"]
        if curve_params["Di"]:
            Di = curve_params["Di"]
        if curve_params["well_life"]:
            Dl = int(curve_params["well_life"])
            well_life = Dl
        if curve_params["years_before_terminal"]:
            DX = curve_params["years_before_terminal"]
        if curve_params["monthly_decline"]:
            Dt = curve_params["monthly_decline"]
        if curve_params["b"] and curve_params["Di"]:
            init_params = np.array([b, Di])
    else:
        curve_params = {
            'Qi'                   : Qi,
            'b'                    : None,
            'Di'                   : None,
            'well_life'            : well_life,
            'years_before_terminal': years_before_terminal,
            'monthly_decline'      : monthly_decline,
            'curve data'           : {}
        }
    curve_params["well_life"] = well_life

    def decline_curve(x, b, Di):
        return float(Qi) / (1.0 + (b*Di*x))**(1.0/float(b))

    #def prod_decline(x, b, Di, Dl, Dx, Dt):
    #    print 'x: {}'.format(x)
    #    if x.all()/12.0 > Dl:
    #        print x.all(), '--1'
    #        Qx = 0
    #    elif x.all()/12.0 > Dx:
    #        print x.all(), '--2'
    #        Qx = prod_decline(x-1, b, Di, Dl, Dx, Dt) * (1-Dt)
    #    else:
    #        print x.all(), '--3'
    #        Qx = decline_curve(x, b, Di)
    #    return Qx

    def prod_decline(x, b, Di, Dl, Dx, Dt):
        print '1-- x: {}, b: {}, Di: {}, Dl: {}, Dx: {}, Dt: {}'.format(x, b, Di, Dl, Dx, Dt)
        if b < .0001:
            b = .0001
        elif b > .99:
            b = .9
        print '2-- x: {}, b: {}, Di: {}, Dl: {}, Dx: {}, Dt: {}'.format(x, b, Di, Dl, Dx, Dt)

        if x.all() > Dl:
            print x.all(), '--1'
            Qx = 0
        elif x.all() > Dx:
            print x.all(), '--2'
            Qx = prod_decline(x-1, b, Di, Dl, Dx, Dt) * (1-Dt)
        else:
            print x.all(), '--3'
            Qx = decline_curve(x, b, Di)
        return Qx

    if debug:
        print "prod_periods :", xdata
        print "prod_values  :", ydata

    if optimize:
        popt, pcov = scipy.optimize.curve_fit(decline_curve, xdata, ydata, p0=init_params)
        b, Di = popt
        curve_params["b"]  = b
        curve_params["Di"] = Di
        curve_params["Qi"] = Qi

    prod_months = range(1, (well_life * 12) + 1)

    xdata = np.arange(len(prod_months))
    ydata = prod_decline(xdata, curve_params["b"], curve_params["Di"], curve_params["well_life"], curve_params["years_before_terminal"], curve_params["monthly_decline"])

    fit_curve = dict(zip(prod_months, ydata.tolist()))
    curve_params["curve data"] = fit_curve

    curr.close()
    conn.close()
    return curve_params

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def generate_type_curve(well_id='', decline_curve_params=None, prod_periods=[], prod_values=[], well_forecast=True, debug=False):
    conn = gd.get_connection()
    curr = conn.cursor()
    commodities = ["Crude Oil", "Natural Gas", "Condensate", "NGLs", "LNG", "Water"]



    if well_forecast and well_id:
        curve_data = {comm: {} for comm in commodities}
        forecast_data = {comm: {} for comm in commodities}
        well_life = int(gd.get_param('well_life', 'type_well_inputs', sql_where='well_id="{}"'.format(well_id)))
        typewell_data = gd.get_typewell_data(well_id)

        for comm in commodities:
            prod_periods = sorted(typewell_data[comm].keys())
            prod_values  = [typewell_data[comm][int(prod_period)] for prod_period in prod_periods]
            if sum(prod_values) > 0:
                output_data = find_curve_fit(well_life, prod_periods, prod_values, decline_curve_params, debug=True)
                forecast_data[comm] = output_data["curve data"]
                for param in ['b', 'Di', 'well_life', 'years_before_terminal', 'monthly_decline']:
                    curve_data[comm][param] = output_data[param]
    else:
        curve_data    = {}
        forecast_data = {}
        typewell_data = {prod_periods[i]: prod_values[i] for i in range(len(prod_values))}
        output_data   = find_curve_fit(100, prod_periods, prod_values, decline_curve_params, debug=True)
        forecast_data = output_data['curve data']
        for param in ['b', 'Di', 'well_life', 'years_before_terminal', 'monthly_decline']:
            curve_data[param] = output_data[param]

    curr.close()
    conn.close()
    return typewell_data, curve_data, forecast_data

if __name__ == '__main__':
    typewell_data, curve_data, forecast_data = generate_type_curve(well_forecast=False, prod_periods=[0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132], prod_values=[681690.0, 674360.0, 663773.2731182795, 650085.9827326997, 633497.5255110678, 614245.6995856975, 592601.0370117326, 568860.4891458324, 543340.6705704173, 516370.8755999182, 488286.0811495304, 459420.14116022614])
    print '   curve_data: {}'.format(curve_data)
    for prod_year in forecast_data.keys():
        if prod_year % 12 == 0:
            print '{}:\t\t{}'.format(prod_year/12, forecast_data[prod_year])
    #for comm in ["Crude Oil", "Natural Gas", "Condensate", "NGLs", "LNG", "Water"]:
    #    print 'typewell_data[{}]: {}'.format(comm, typewell_data[comm])
    #    print '   curve_data[{}]: {}'.format(comm, curve_data[comm])
    #    print 'forecast_data[{}]: {}'.format(comm, forecast_data[comm])
    #    print ''