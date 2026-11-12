from globaldata import *
import pandas as pd
from decline_obj import DeclineObj
import numpy as np
import matplotlib.pyplot as plt

well_comm_list = ['crude', 'ng', 'condensate', 'ngls']

def get_well_life(asset_id):
    if asset_id:
        well_life = int(get_param('well_life', 'well_params', asset_id))
    else:
        conn = get_connection()
        curr = conn.cursor()
        curr.execute('SELECT AVG(well_life) FROM well_params')
        well_life = float(curr.fetchone()[0])
        curr.close()
        conn.close()
    return well_life

def get_typewell_data(asset_id=None, out_unit=None, month_limit=60, prod_file=None, debugMode=False):
    comm_names = {'crude oil': 'crude', 'natural gas': 'ng', 'condensate': 'condensate', 'ngl': 'ngls'}
    typewell_data = {comm: {} for comm in well_comm_list}
    if debugMode:
        print 'prod_file:', prod_file
        print 'asset_id:', asset_id
    if prod_file:
        raw_data = pd.read_csv(prod_file, index_col=0)
        prod_data = raw_data.fillna(0).iloc[:month_limit,:]
        typewell_data = prod_data.to_dict()
    elif asset_id:
        conn = get_connection()
        curr = conn.cursor()
        sql_select = 'SELECT period, commodity, production_count, unit FROM wells WHERE datatype="Production" AND asset_id=%s ORDER BY commodity, period'
        if debugMode:
            print sql_select % asset_id
        if curr.execute(sql_select % asset_id):
            for period, commodity, production_count, unit in curr.fetchall():
                comm_name = comm_names[commodity.lower()]
                conv_factor = 1.0
                if out_unit and (unit.lower() != out_unit.lower()):
                    conv_factor = get_conversion_factor(commodity=commodity, from_unit=unit, to_unit=out_unit, time_unit='month', cur=curr)
                if debugMode:
                    print 'period:', period
                    print 'commodity:', commodity
                    print 'production_count:', production_count
                    print 'unit:', unit
                    print 'conv_factor:', conv_factor
                    print 'float(production_count) * conv_factor:', float(production_count) * conv_factor
                typewell_data[comm_name][int(period)] = float(production_count) * conv_factor
        curr.close()
        conn.close()
    return typewell_data


def forecast_well_production(typewell_data, asset_id=None, well_life=0, debugMode=False):
    if not well_life:
        well_life = get_well_life(asset_id)
    days_in_year = 365.24
    max_decline_pct = 0.9999
    WELL_FC = {comm: {} for comm in well_comm_list}
    well_prod_data = {comm: {} for comm in well_comm_list}
    well_mon_len = max([len(typewell_data[comm].keys()) for comm in well_comm_list])
    if well_mon_len > 0 and (well_mon_len % 12 == 0):
        sourced_wells_prod = int(well_mon_len / 12)
    if debugMode:
        print "     typewell_data['crude']:", typewell_data['crude']
        print ''
        print "        typewell_data['ng']:", typewell_data['ng']
        print ''
        print "typewell_data['condensate']:", typewell_data['condensate']
        print ''
        print "      typewell_data['ngls']:", typewell_data['ngls']
        print ''
    for comm_name in well_comm_list:
        x_new = []
        y_new = []
        for month in [int(mnth) for mnth in typewell_data[comm_name].keys()]:
            if float(typewell_data[comm_name][month]) > 0:
                y_new.append(typewell_data[comm_name][month])
                x_new.append(month)
        if debugMode:
            print ''
            print 'x_new:', x_new
            print 'y_new:', y_new
            print 'len(x_new):', len(x_new)
            print 'len(y_new):', len(y_new)
            print "---- ** EVALUATING " + comm_name
        if y_new:
            well_prod_data[comm_name] = {i+1: y_new[i] for i in range(len(y_new))}
            peak_num = max(y_new)
            peak_index = y_new.index(peak_num)
            peak_month = x_new[peak_index]
            if debugMode:
                print ''
                print "-----------------------USING----------" + comm_name
                print 'well_prod_data[%s]:' % comm_name, well_prod_data[comm_name]
                print "length of " + comm_name
                print 'len(y_new):', len(y_new)
                print 'y_new:', y_new
                print "Peak Number"
                print 'peak_num:', peak_num
                print '-=-' * 50
            z_new = []
            for iii in range(len(y_new)):
                z_new.append(iii + 1)
            y_prime = y_new[peak_index:]
            x_prime = x_new[peak_index:]
            z_prime = z_new[peak_index:]
            if debugMode:
                print ''
                print 'peak_index:', peak_index
                print "Y - prime"
                print 'y_new:', y_new
                print 'y_prime:', y_prime
                print 'z_new:', z_new
                print 'z_prime:', z_prime
                print "Peak year --> " + str(peak_month) + " ----> Peak production: " + str(peak_num)
                print '-=-' * 50
            arps_output = DeclineObj(np.array(z_prime), np.array(y_prime))
            # --------------------------------------------------------------------
            results = arps_output()
            curve_type = results[0]
            if debugMode:
                print ''
                print "TOTAL RESULTS ARRAY"
                print 'results:', results
                print 'curve_type:', curve_type + " CURVE TYPE <--------------------------"

            Qi = y_prime[-1]
            
            if debugMode:
                print ''
                print "Qi in ****************"
                print 'Qi:', Qi
    
            b = round(results[1][1], 5)
            Di = round(results[1][-1], 5)
            if Di < 0:
                Di = -1 * Di

            if b < .05:
                b = .05
            elif b > .99:
                b = .9
            else:
                pass
            # ----------------------------------------
            p = max_decline_pct
            if p < .001:
                p = .01
            elif p > .999:
                p = .9
            else:
                pass
            if days_in_year > 0:
                Dlim = np.log(1 - p) / (days_in_year)
            else:
                Dlim = 0
            timeVar = abs(round(((((Di / Dlim) - 1) / b) / Di), 0))
            Qi = y_new[-1]
            #Qi = y_prime[0]
            if debugMode:
                print ''
                print 'comm_name:', comm_name
                print 'Qi:', Qi
                print 'b:', b
                print 'p:', p
                print 'Di:', Di
                print 'Dlim:', Dlim
                print 'timeVar:', timeVar
            fc = []
            auc = []
            ij = 1
            tVar = 0
            k = 0
            firstTime = 1
            modifiedFormula = 0
            currYear = 1
            qx_orig = []
            area = 0
            prod = []
            period = []
            firstQx = Qi
            fc = []
            start_month = int(sourced_wells_prod * 12)
            end_month = int(well_life * 12) + 1
            if debugMode:
                print '--- Well Forecast ---'
            for month in range(start_month, end_month):
                if debugMode:
                    print ''
                    print 'month %s out of %s' % (month, end_month)
                if firstTime:
                    power_var = round(-tVar * Dlim, 0)
                    if power_var > 100:
                        mErrorType = "ERROR TYPE 38"
                        power_var = 100
                    if tVar >= timeVar:
                        Qx = Qexp * (math.e ** (power_var))
                        area = 0
                        if debugMode:
                            print ''
                            print '7: tVar:', tVar
                            print '7: timeVar:', timeVar
                            print '7: Qexp:', Qexp
                            print '7: power_var:', power_var
                            print '7: Qx = Qexp*(math.e**(power_var))'
                            print '7: Qx', Qx
                    else:
                        if (1 + b * Di * tVar) < 0:
                            mErrorType = "ERROR TYPE 35"
                            exp_base = abs(1 + b * Di * tVar)
                            Qx = (Qi / ((exp_base) ** (1 / b)))
                            if debugMode:
                                print ''
                                print '8: tVar:', tVar
                                print '8: timeVar:', timeVar
                                print '8: Qi:', Qi
                                print '8: exp_base:', exp_base
                                print '8: b:', b
                                print '8: Qx = (Qi/((exp_base)**(1/b)))'
                                print '8: Qx', Qx
                        else:
                            Qx = (Qi / ((1 + b * Di * tVar) ** (1 / b)))
                            if debugMode:
                                print ''
                                print '9: Qx = (Qi/((1+b*Di*tVar)**(1/b)))'
                                print '9: Qx', Qx
                        area = 0
                    if debugMode:
                        print "Initial Qx: " + str(Qx)
                    firstTime = 0
                    firstQx = Qx
                else:
                    power_var = round(-tVar * Dlim, 0)
                    if power_var > 100:
                        mErrorType = "ERROR TYPE 37"
                        power_var = 100
                    if tVar >= timeVar:
                        Qexp = (Qi / ((1 + b * Di * timeVar) ** (1 / b))) * (1 / (math.e ** power_var))
                        Qx = Qexp * (math.e ** (power_var))
                        area = 0
                        if debugMode:
                            print ''
                            print '10: tVar:', tVar
                            print '10: timeVar:', timeVar
                            print '10: Qexp:', Qexp
                            print '10: power_var:', power_var
                            print '10: Qx = Qexp*(math.e**(power_var))'
                            print '10: Qx', Qx
                    else:
                        Qx = (Qi / ((1 + b * Di * tVar) ** (1 / b)))
                        if ((1 - b) * Di) * (1 - (1 + b * Di * tVar) ** (1 - (1 / b))) == 0:

                            mErrorType = "ERROR TYPE 36"
                            if debugMode:
                                print 'mErrorType:', mErrorType
                            area = 0
                        else:
                            area = Qi / ((1 - b) * Di) * (1 - (1 + b * Di * tVar) ** (1 - (1 / b)))
                        if debugMode:
                            print ''
                            print '11: Qi:', Qi
                            print '11: b:', b
                            print '11: Di:', Di
                            print '11: tVar:', tVar
                            print '11: timeVar:', timeVar
                            print '11: Qx = (Qi/((1+b*Di*tVar)**(1/b)))'
                            print '11: Qx', Qx
                if debugMode:
                    print ''
                    print 'Qx:', Qx
                    print '-=-' * 20
                if Qx != firstQx:
                    WELL_FC[comm_name][month] = Qx
                k += 1
                tVar += 1
                if Qx < 1:
                    if debugMode:
                        print ''
                        print 'if Qx < 1:'
                        print 'Qx:', Qx
            if debugMode:
                print ''
                print "X0X-" * 30
                print 'comm_name:', comm_name
                print 'WELL_FC[%s]:' % comm_name, WELL_FC[comm_name]
    for comm_name in well_comm_list:
        if debugMode:
            print ''
            print 'WELL_FC[%s]:' % comm_name, WELL_FC[comm_name]
        for month in WELL_FC[comm_name].keys():
            well_prod_data[comm_name][month] = WELL_FC[comm_name][month]
    return well_prod_data

def display_production_output(well_prod_data, subplot_size):
    line_types = ['b--', 'r--', 'y--', 'c--']
    subplot_width, subplot_height = subplot_size
    subplot_num = 0
    fig = plt.figure(figsize=(10, 16.18))
    axes = {axis_num: None for axis_num in range(len(well_comm_list))}
    for i in range(len(well_comm_list)):
        comm = well_comm_list[i]
        prod_months = len(well_prod_data[comm])
        if prod_months > 0:
            print comm, well_prod_data[comm]
            x_coord = 0.05
            y_coord = (subplot_height + 0.02)*(subplot_num) + 0.05
            y_max = max(well_prod_data[comm].values())
            axis = fig.add_axes([x_coord, y_coord , subplot_width, subplot_height], xticklabels=['%s' % month for month in range(0,prod_months,3)], ylim=(0, (y_max+10)))
            axis.xaxis.set_major_locator(plt.MaxNLocator(prod_months/4))
            axis.plot(sorted(well_prod_data[comm].values(), reverse=True), line_types[i])
            subplot_num += 1
    plt.show()

def main(prod_file=None, asset_id=None, well_life=0, save_output=False, display_output=False, debugMode=False):
    typewell_data = get_typewell_data(asset_id=asset_id, out_unit='boe', prod_file=prod_file, debugMode=debugMode)
    well_prod_data = forecast_well_production(typewell_data=typewell_data, asset_id=asset_id, well_life=well_life, debugMode=debugMode)
    if debugMode:
        for comm in well_comm_list:
            print ''
            print 'len(well_prod_data[%s]):' % comm, len(well_prod_data[comm])
            print '     well_prod_data[%s]:' % comm, well_prod_data[comm]
    if display_output:
        display_production_output(well_prod_data, (0.9, 0.25))

    if save_output:
        output_file = DATA_DIR + 'typewell_forecast_%s.csv'
        if asset_id:
            output_file = output_file % asset_id
        else:
            session_key = create_session_key(with_username=False)
            output_file = output_file % session_key
        well_data = pd.DataFrame.from_dict(well_prod_data)
        well_data = well_data[well_comm_list]
        well_data.to_csv(output_file, encoding='utf-8')



if __name__=='__main__':
    #input_prod_file = DATA_DIR + 'typewell_prod_input.csv'
    input_prod_file = None
    asset_id = 851671
    main(prod_file=input_prod_file, well_life=18, asset_id=asset_id,  display_output=True, save_output=True, debugMode=True)
