from data_export import *

NEW_PANORAMA = True

def save_output(output_file, output):
    if output_file:
        with open(output_file, 'w') as outfile:
            outfile.write(output)

def num_convert(input_number):
    output_number = input_number
    output_unit = ''
    if abs(input_number) > 1000000:
        output_number = float(input_number)/1000000.0
        output_unit = 'mil'
        if output_number > 1000:
            output_number = float(output_number)/1000.0
            output_unit = 'bil'
    output_number = round(output_number, 1)
    if output_number > 1000:
        output_number = str("{:,}".format(output_number))
    else:
        output_number = str(output_number)
    return output_number, output_unit

def num_end(number):
    end = ''
    number = str(number)
    if len(number) > 1 and number[-2] == '1':
        end = 'th'
    elif number[-1] == '1':
        end = 'st'
    elif number[-1] == '2':
        end = 'nd'
    elif number[-1] == '3':
        end = 'rd'
    else:
        end = 'th'
    return end

def sent_form(form_num,p0=None,p1=None,p2=None,p3=None,p4=None,p5=None,p6=None,p7=None,p8=None,p9=None,p10=None,p11=None,p12=None,p13=None,p14=None,p15=None,p16=None,p17=None,p18=None,p19=None,p20=None):
    sent_parts = [p for p in [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20] if p is not None]
    sent = ''
    if form_num == 1:
        if len(sent_parts) == 2:
            sent = p0 + p1 + '.'
        elif len(sent_parts) == 3:
            sent = p0 + p1 + ' and ' + p2 + '.'
        elif len(sent_parts) > 3:
            sent_parts[0] = sent_parts[0][:-1]      # remove space before comma
            sent = ', '.join(sent_parts[:-1]) + ', and ' + sent_parts[-1]
    return sent

def get_rank(curr, asset_id, run_id, param, rank_order, terrain=None, resource_type=None, operator=None, group_type=None, group=None):
    sql_select = 'asset_id, ' + param
    sql_where = ' AND NOT (asset_name is NULL OR asset_name LIKE "Other %" OR asset_name LIKE "Others %") '
    if group and group_type:
        sql_where += 'AND %s="%s" ' % (group_type, group)
    if terrain:
        sql_where += 'AND terrain="%s" ' % terrain
    if resource_type:
        sql_where += 'AND resource_type="%s" ' % resource_type
    if operator:
        sql_where += 'AND operator="%s" ' % operator

    sql_order = ' ORDER BY ' + param + ' ' + rank_order
    #sql_query = 'SELECT ' + sql_select + ' FROM econ_data WHERE run_id="' + run_id + '" ' + sql_where + sql_order
    sql_query = 'SELECT {} FROM econ_data WHERE run_id="{}" {} {}'.format(sql_select, run_id, sql_where, sql_order)
    curr.execute(sql_query)
    econ_data = curr.fetchall()
    rank = [ast_id for ast_id, param in econ_data].index(asset_id) + 1
    total = len(econ_data)
    return rank, total, group

def rank_phrase(rank_x, tot_x, grp_x=None, terrain=None, resource_type=None, model_type='conventional', position=None):
    if 0:
        print 'rank_x:{}, tot_x:{}, grp_x:{}, terrain:{}, resource_type:{}, model_type:{}\n'.format(rank_x, tot_x, grp_x, terrain, resource_type, model_type)
    part_a  = '%s out of %s'
    part_b  = 'in the %s %s%%'
    part_c1 = ' for %s fields'
    part_c2 = ' for %s plays'
    part_d1 = ' in %s'
    part_d2 = ' in the %s'
    part_d3 = ' for all positions in the %s formation'
    part_e  = ' %s'

    part_c = part_c1
    if model_type == 'unconventional':
        part_c = part_c2


    if rank_x <= 200:
        params_a = (str("{:,}".format(rank_x)) + num_end(rank_x), str("{:,}".format(tot_x)))
        px = part_a
        params_x = params_a
    else:
        if rank_x >= (tot_x/2):
            loc_x = 'bottom'
            pct_x = int((1 - (float(rank_x)/float(tot_x))) * 100)
        else:
            loc_x = 'top'
            pct_x = int((float(rank_x)/float(tot_x)) * 100)
        params_b = (str(loc_x), str(pct_x))
        px = part_b
        params_x = params_b

    if terrain and resource_type:
        px += part_c
        field_type = '%s %s' % (terrain.lower(), resource_type.lower())
        params_x += (field_type,)
    elif terrain:
        px += part_c
        params_x += (terrain.lower(),)
    if grp_x:
        if grp_x != 'globally':
            if position:
                part_d = part_d3
            elif grp_x.lower() in ['middle east','congo republic','czech republic','democratic republic of the congo','falkand islands',
                                 'netherlands','philippines','united arab emirates','united kingdom','united states']:
                part_d = part_d2
            else:
                part_d = part_d1
            px += part_d
        else:
            px += part_e
        params_x += (grp_x,)
    return px, params_x

def rank_sent(asset_name, full_sent, terrain, resource_type, model_type, position, rank_1, tot_1, grp_1, rank_2, tot_2, grp_2, rank_3, tot_3, grp_3):
    if 0:
        print 'asset_name:{}, full_sent:{}, terrain:{}, resource_type:{}, model_type:{}, rank_1:{}, tot_1:{}, grp_1:{}, rank_2:{}, tot_2:{}, grp_2:{}, rank_3:{}, tot_3:{}, grp_3:{}'.format(asset_name, full_sent, terrain, resource_type, model_type, rank_1, tot_1, grp_1, rank_2, tot_2, grp_2, rank_3, tot_3, grp_3)
    sent_parts = []
    param_parts = []
    params_0 = ()
    p0 = ''
    if full_sent:
        if model_type == 'unconventional':
            mod = random.choice(['ranks', 'situates', 'places'])
        else:
            mod = random.choice(['ranks', 'situates', 'positions'])
        p0 = '  This ' + mod + ' %s '
        params_0 = (asset_name,)

    rank_data = zip((rank_1, rank_2, rank_3), (tot_1, tot_2, tot_3), (grp_1, grp_2, grp_3))

    with_desc = True
    group_num = 0
    for rank_x, tot_x, grp_x in rank_data:
        group_num += 1
        if with_desc:
            trrn = terrain
            res_type = resource_type
        else:
            trrn = None
            res_type = None
        if model_type == 'unconventional' and group_num == 2:
            positn = position
        else:
            positn = None
        px, params_x = rank_phrase(rank_x, tot_x, grp_x, trrn, res_type, model_type=model_type, position=positn)
        sent_parts.append(px)
        param_parts.append(params_x)
        with_desc = False
    p1, p2, p3 = sent_parts
    sent = sent_form(1, p0, p1, p2, p3)

    params_1, params_2, params_3 = param_parts
    params = params_0 + params_1 + params_2 + params_3
    return sent % params

def rank_clause(asset_name, asset_id, run_id, param, rank_order, terrain, resource_type, country, region, curr, full_sent, model_type, position=None):
    if model_type == 'unconventional':
        grp_combos = [('country', country), ('position', position), ('region', region)]
    else:
        grp_combos = [('country', country), ('region', region), ('', 'globally.')]
    rank_x = map(lambda (grp_type, grp): get_rank(curr, asset_id, run_id, param, rank_order, terrain, resource_type, group_type=grp_type, group=grp), grp_combos)
    ranks = rank_x[0] + rank_x[1] + rank_x[2]
    return rank_sent(asset_name, full_sent, terrain, resource_type, model_type, position, *ranks)

def operator_sent(asset_name, asset_id, operator, curr, run_id, param, debug=False, model_type='conventional'):
    out_sent = ''
    if operator:
        part_a = '  Within %s\'s %sportfolio, %s is positioned '
        x, params_x  = rank_phrase(*get_rank(curr, asset_id, run_id, param, PARAM_DATA[param]['rank_order'], operator=operator, model_type=model_type))
        part_b = (x % params_x) + ' for ' + PARAM_DATA[param]['param_name'] +'.'
        mod = random.choice(['', 'company '])
        params = (operator, mod, asset_name)
        part_a = part_a % params
        sent = part_a + part_b
        if debug:
            print 'part_a:', part_a
            print 'part_b:', part_b
            print '   mod:', mod
            print 'params:', params
        out_sent = sent
    return out_sent

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_uncon_rank(curr, asset_id, position, param_name, rank_order, run_id):
    param_rank = 0
    param_total = 1
    sql_select = 'SELECT asset_id FROM econ_data WHERE run_id="{1}" AND position="{3}" AND fiscal_model LIKE "%Resource%" '
    sql_select += 'AND NOT (asset_name is NULL OR asset_name LIKE "Other %" OR asset_name LIKE "Others %") ORDER BY {0} {2} '
    curr.execute(sql_select.format(param_name, run_id, rank_order, position))
    ranked_uncon_assets = [data[0] for data in curr.fetchall()]
    param_rank = ranked_uncon_assets.index(asset_id) + 1
    param_total = len(ranked_uncon_assets)
    if 0:
        print '{}({}): {}/{}'.format(asset_id, param_name, param_rank, param_total)
    return param_rank, param_total

def uncon_section_(curr, asset_id, run_id, constituent, country, region, formation, position, terrain, resource_type, operator, rig_count, last_rig_year, capex_well_boe, opex_well_boe, well_life, new_wells, new_wells_rem, drill_comp_days, ip30_rate, eur_total, post_tax_irr, be_oil_post_tax, be_gas_post_tax):
    out_sent = ''
    discount_year = get_discount_year()
    if operator and position and terrain and constituent and country:
        out_sent1 = '''{0}'s {1} position is located {2} {3} in {4}.  '''
        out_sent += out_sent1.format(operator, position, terrain.lower(), constituent, country)

    if operator and position and constituent and rig_count and new_wells and drill_comp_days:
        out_sent2 = '''With respect to this position in {2}, {3} rigs are expected to be available in {4}, netting {5} wells with a drilling and completion time of {6} days.  '''
        out_sent += out_sent2.format(operator, position, constituent, rig_count, int(discount_year), int(new_wells), drill_comp_days)

    if new_wells_rem and last_rig_year:
        out_sent3 = '''The position is estimated to have a total of {0} new wells to be drilled up to {1}.  '''
        out_sent += out_sent3.format(int(new_wells_rem), int(last_rig_year))

    if operator and position and new_wells_rem:
        out_sent4 = '''This forecasts {0} as having {1} activity when compared with other operators in the {2} formation.  '''
        activity_rank, activity_total = get_uncon_rank(curr, asset_id, position, 'new_wells_rem', 'DESC', run_id)
        if activity_rank < (activity_total/3):
            activity_level = 'high'
        elif activity_rank > 2*(activity_total/3):
            activity_level = 'low'
        else:
            activity_level = 'medium'
        out_sent += out_sent4.format(operator, activity_level, position)

    if capex_well_boe and opex_well_boe and operator and position:
        out_sent5 = '''Per well capital and operating expenditure per boe equals US${0} ranking {1}'s {2} position {3}/{4} in the {2}.  '''
        capex_opex_boe_well_cost = capex_well_boe + opex_well_boe

        well_cost_rank, well_cost_total = get_uncon_rank(curr, asset_id, position, '(capex_well_boe + opex_well_boe)', 'ASC', run_id)
        out_sent += out_sent5.format(format_num(capex_opex_boe_well_cost,2,True,True), operator, position, well_cost_rank, well_cost_total)

    if ip30_rate and eur_total:
        out_sent6 = '''The type well for this position has a total IP30 rate of {0} boed with an EUR of {1} boe.  '''
        out_sent += out_sent6.format(format_num(ip30_rate,2,True), format_num(eur_total, 2, True))

    if position and ip30_rate and eur_total:
        out_sent7 = '''This ranks the productivity of the well {0}/{1} and the recovery {2}/{3} across all companies in the {4}.  '''
        productivity_rank, productivity_total = get_uncon_rank(curr, asset_id, position, 'ip30_rate', 'DESC', run_id)
        recovery_rank, recovery_total = get_uncon_rank(curr, asset_id, position, 'eur_total', 'DESC', run_id)
        out_sent += out_sent7.format(productivity_rank, productivity_total, recovery_rank, recovery_total, position)

    if well_life and post_tax_irr and resource_type and ((0 < be_oil_post_tax < 250) or (0 < be_gas_post_tax < 50)) and position:
        if be_oil_post_tax > 0:
            post_tax_be_unit = 'bbl'
            post_tax_be = be_oil_post_tax
            commodity = 'oil'
            be_param_name = 'be_oil_post_tax'
        else:
            post_tax_be_unit = 'mcf'
            post_tax_be = be_gas_post_tax
            commodity = 'gas'
            be_param_name = 'be_gas_post_tax'

        out_sent8 = '''With a well life spanning {0} years, post-tax IRR is {1}% and a post-tax break-even {2} price of US$ {3}/{4} ranking {5}/{6} in well economics for operators in the {7}.  '''
        irr_rank, irr_total = get_uncon_rank(curr, asset_id, position, 'post_tax_irr', 'DESC', run_id)
        out_sent += out_sent8.format(int(well_life), post_tax_irr, commodity, format_num(post_tax_be, 2, True, True), post_tax_be_unit, irr_rank, irr_total, position)
    return out_sent


def uncon_section(curr, asset_name, asset_id, run_id, constituent, country, region, formation, position, terrain, resource_type, operator, rig_count, prev_rig_count, last_rig_year,
                  capex_well_boe, opex_well_boe, well_life, new_wells, new_wells_rem, drill_comp_days, ip30_rate, eur_total, pre_tax_irr, be_oil_pre_tax, be_gas_pre_tax, capex_well,
                  opex_well, well_boe, remain_res, rem_liquid_recov, rem_natgas_recov, working_interest, boed_prod):
    out_sent = ''
    discount_year = get_discount_year()
    if asset_name and resource_type and terrain and position and operator:
        out_sent1 = "{0} is an {1} {2} position in {3} shale play operated by {4}.  "
        out_sent += out_sent1.format(asset_name, resource_type.lower(), terrain.lower(), position, operator)

    if position and discount_year:
        out_sent2 = "The company is forecasted to average {0} boed for their {1} asset in {2}.  "
        out_sent += out_sent2.format(str("{:,}".format(round(boed_prod,2))), position, int(discount_year))

    if prev_rig_count and discount_year and rig_count:
        out_sent3 = "The company ran {0} {4} in {1} and plans to operate {2} {5} in the area for {3}.  "
        rig_str1 = 'rig'
        rig_str2 = 'rig'

        if int(prev_rig_count) != 1:
            rig_str1 += 's'
        if int(rig_count) != 1:
            rig_str2 += 's'

        out_sent += out_sent3.format(float(prev_rig_count), discount_year - 1, rig_count, discount_year, rig_str1,
                                     rig_str2)

    if new_wells and operator and position and constituent:
        out_sent4a = "{0} expects first production from {1} new net wells throughout the year. "
        out_sent4b = "The average type wells for the operator in {0} {1} has initial production rate of {2} boed and an estimated ultimate recovery of {3} boe.  "
        out_sent += out_sent4a.format(operator, int(new_wells))
        sql_where = "operator='{}' AND position='{}' AND constituent='{}'".format(operator, position, constituent)
        avg_prod_rate, avg_eur = get_data('AVG(ip30_rate) AS avg_prod_rate, AVG(eur_total) AS avg_eur', 'econ_data', cursor=curr, datatype='plural', single_value=True, sql_where=sql_where)
        out_sent += out_sent4b.format(position, constituent, str("{:,}".format(round(avg_prod_rate,1))), str("{:,}".format(round(avg_eur,1))))

    if capex_well and opex_well and well_boe and working_interest:
        out_sent5 = "Average well cost are estimated at of US${0} mil with average production cost of US${1}/boe, and an average working interest of {2}%.  "
        out_sent += out_sent5.format(str("{:,}".format(round(float((capex_well + opex_well)/1000000.0),1))), str("{:,.2f}".format(round(float((capex_well + opex_well))/float(well_boe),2))), round(float(working_interest)*100,1))

    if ((0 < be_oil_pre_tax < 250) or (0 < be_gas_pre_tax < 50)) and pre_tax_irr:
        out_sent6 = "This type well has a pre-tax break-even price of US${0}/{1} and a pre-tax IRR of {2}%.  "
        if be_oil_pre_tax > 0:
            pre_tax_be_unit = 'bbl'
            pre_tax_be = be_oil_pre_tax
        else:
            pre_tax_be_unit = 'mcf'
            pre_tax_be = be_gas_pre_tax
        out_sent += out_sent6.format(str("{:,.2f}".format(round(pre_tax_be,2))), pre_tax_be_unit, round(float(pre_tax_irr)*100,2))

    if resource_type and remain_res and rem_liquid_recov >= 0 and rem_natgas_recov >= 0:
        part_a = 'This position has remaining reserves of {} mmboe'.format(str("{:,}".format(round(float(remain_res/1000000.0), 1))))
        part_b = ', comprised of {} mmbbl of liquid reserves and {} bcf of natural gas reserves'
        if 0 not in [rem_liquid_recov, rem_natgas_recov]:
            out_sent += (part_a + part_b.format(str("{:,}".format(round(float(rem_liquid_recov/1000000.0), 1))), str("{:,}".format(round(float(rem_natgas_recov), 1)))))
        else:
            out_sent += part_a
        out_sent += '.  '

    if position :
        npv_rem = get_data('npv_rem', 'econ_data', cursor=curr, datatype='float', single_value=True, sql_where="run_id='{}' AND asset_id={}".format(run_id, asset_id))
        npv_rem = str("{:,}".format(round(float(npv_rem/1000000.0), 2)))
        npv_rank, npv_total = get_uncon_rank(curr, asset_id, position, 'npv_rem', 'DESC', run_id)
        out_sent8 = "The remaining NPV for the overall position is US${0} mil, ranking this project {1} out of {2} for {3} positions in the United States.  "
        out_sent += out_sent8.format(npv_rem, npv_rank, str("{:,}".format(int(npv_total))), position)

    return out_sent

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def reserve_sent_1(asset_name, terrain, country_name, parent, basin, status):
    out_sent = ''
    if terrain and country_name and parent:
        if basin == 'Gulf of Mexico Basin':
            country_name += ' Gulf of Mexico'
        if status.lower() == 'abandoned':
            part_a = '%s, located in %s %s, was operated by %s.  '
        else:
            part_a = '%s, located in %s %s, is operated by %s.  '
        if parent[-1] == '.':
            parent = parent[:-1]
        params = (asset_name, country_name, terrain.lower(),  parent)
        sent = part_a
        out_sent += (sent % params)
    return out_sent

def reserve_sent_2(curr, asset_name, status, terrain, facility_type, country, country_name, run_id):
    out_sent = ''
    if facility_type and facility_type != 'NULL':
        if facility_type in ['FLNG', 'FPSO', 'FPU', 'FSO']:
            facility = facility_type
        else:
            facility = facility_type.lower()
        sent = "%s %s using a %s, which is %s in %s.  "
        mod_a1 = 'This field'
        mod_a2 = asset_name
        mod_a = random.choice([mod_a1, mod_a2])
        if status.lower() in ['producing', 'abandoned']:
            mod_b = 'was developed'
        elif status.lower() in ['planned', 'announced']:
            mod_b = 'will be developed'
        sql_select  = 'SELECT facility_type, COUNT(*) AS facility_count FROM econ_data WHERE country="%s" AND terrain="%s" '
        sql_select += 'AND NOT (facility_type IS NULL OR facility_type="NULL") AND run_id="%s" GROUP BY facility_type'
        curr.execute(sql_select % (country, terrain, run_id))
        facility_counts = curr.fetchall()
        most_common_count = max([facility_count for (facility_type, facility_count) in facility_counts])
        country_total = sum([facility_count for (facility_, facility_count) in facility_counts])

        sql_select  = 'SELECT COUNT(DISTINCT asset_id) FROM econ_data WHERE country="%s" '
        sql_select += 'AND terrain="%s" AND facility_type="%s" AND run_id="%s" '
        curr.execute(sql_select % (country, terrain, facility, run_id))
        facility_type_in_country = curr.fetchone()[0]
        facility_pct = (float(facility_type_in_country) / float(country_total))
        if facility_pct < 0.05:
            mod_c = 'atypical'
        elif facility_pct == 1:
            mod_c = 'the only of its kind'
        elif most_common_count == facility_type_in_country:
            mod_c = 'the most common'
        else:
            mod_c = 'typical'
        mod_d1 = random.choice(['the', 'this']) + ' country'
        mod_d2 = country_name
        mod_d = random.choice([mod_d1, mod_d2])

        out_sent = sent % (mod_a, mod_b, facility, mod_c, mod_d)
    return out_sent

def reserve_sent_3(asset_name, status, total_res, remain_res, first_production, peak_year, peak_prod, peak_prod_unit, cutoff_year):
    out_sent = ''
    if status.lower() == 'producing':
        sent = 'Regarding its production stage, %s %s, having recovered %s%% of its total reserves.  '
        if remain_res and total_res and (remain_res > 0) and (total_res > 0) and (total_res > remain_res):
            recover_res_pct = (1 - (float(remain_res)/float(total_res)))
            if recover_res_pct >= 0.8:
                mod_a = 'is mature'
            elif recover_res_pct < 0.5:
                mod_a = 'is yet to reach midway through field life'
            else:
                mod_a = 'is midway through field life'
            out_sent = sent % (asset_name, mod_a, round(recover_res_pct*100,1))
    elif status.lower() in ['planned', 'announced']:
        sent = 'With a projected field life of %s years, %s is %s to come online in %s, peaking at %s %s by %s.  '
        if first_production and peak_year and peak_prod and peak_prod_unit and cutoff_year:
            projected_field_life = int(cutoff_year) - int(first_production)
            mod = random.choice(['expected', 'anticipated'])
            out_sent = sent % (projected_field_life, asset_name, mod, first_production, peak_prod, peak_prod_unit, peak_year)
    return out_sent

def reserve_sent_4(asset_name, status, resource_type, total_res, tot_liquid_recov, tot_natgas_recov, remain_res, rem_liquid_recov, rem_natgas_recov, model_type):
    out_sent = ''
    recov_reserve_name = 'total_recov_rem'
    if status.lower() == 'producing':
        if resource_type and remain_res and rem_liquid_recov >= 0 and rem_natgas_recov >= 0:
            part_a = 'This field has remaining reserves of %s mmboe'
            if model_type == 'unconventional':
                part_a = 'This position has remaining reserves of %s mmboe'
            part_b = ', comprised of %s mmbbl of liquid reserves and %s bcf of natural gas reserves'
            params = (str("{:,}".format(round(float(remain_res/1000000.0), 2))),)
            if 0 not in [rem_liquid_recov, rem_natgas_recov]:
                sent = sent_form(1, part_a, part_b)
                params += (str("{:,}".format(round(float(rem_liquid_recov/1000000.0), 2))), str("{:,}".format(round(float(rem_natgas_recov), 2))))
            else:
                sent = sent_form(1, part_a, '')
            out_sent += sent % params
        else:
            out_sent += '.'
    elif status.lower() in ['planned', 'announced']:
        if resource_type and total_res and tot_liquid_recov >= 0 and tot_natgas_recov >= 0:
            part_a = 'This field has total recoverable reserves of %s mmboe'
            part_b = ', comprised of %s mmbbl of liquid reserves and %s bcf of natural gas reserves'
            params = (str("{:,}".format(round(float(total_res/1000000.0), 2))),)
            if 0 not in [tot_liquid_recov, tot_natgas_recov]:
                sent = sent_form(1, part_a, part_b)
                params += (str("{:,}".format(round(float(tot_liquid_recov/1000000.0), 2))), str("{:,}".format(round(float(tot_natgas_recov), 2))))
            else:
                sent = sent_form(1, part_a, '')
            out_sent += sent % params
        else:
            out_sent += '.'
        recov_reserve_name = 'total_recov'
    return out_sent, recov_reserve_name

def reserve_sent_5(total_res, status, cutoff_year):
    out_sent = ''
    recov_reserve_name = ''
    if total_res and cutoff_year and status.lower() == 'abandoned':
        sent = 'Field production was terminated in %s, having recovered reserves of %s mmboe. '
        params = (int(cutoff_year), str("{:,}".format(round(float(total_res/1000000.0), 2))))
        out_sent = sent % params
        recov_reserve_name = 'total_recov'
    return out_sent, recov_reserve_name

def reserve_sent_6(asset_name, asset_id, run_id, terrain, resource_type, recov_reserve_name, country, region, curr, model_type, position):
    out_sent = ''
    curr.execute('SELECT DISTINCT asset_id FROM econ_data WHERE NOT %s IS NULL AND run_id="%s"' % (recov_reserve_name, run_id))
    total_recov_assets = [int(data[0]) for data in curr.fetchall()]
    if int(asset_id) in total_recov_assets:
        out_sent = rank_clause(asset_name, asset_id, run_id, recov_reserve_name, 'DESC', terrain, resource_type, country, region, curr, True, model_type=model_type, position=position)
    return out_sent

def reserves_section(output, asset_name, asset_id, run_id, region, status, terrain, country, country_name, operator, parent, basin, resource_type, total_res, tot_liquid_res, tot_natgas_res,
                     remain_res, rem_liquid_recov, rem_natgas_recov, curr, facility_type, first_production, peak_year, peak_prod, peak_prod_unit, cutoff_year, model_type, position):
    reserves_output = ''
    if model_type == 'conventional':
        out_sent_1 = reserve_sent_1(asset_name, terrain, country_name, parent, basin, status)
        reserves_output += out_sent_1

        out_sent_2 = reserve_sent_2(curr, asset_name, status, terrain, facility_type, country, country_name, run_id)
        reserves_output += out_sent_2

    out_sent_3 = reserve_sent_3(asset_name, status, total_res, remain_res, first_production, peak_year, peak_prod, peak_prod_unit, cutoff_year)
    reserves_output += out_sent_3

    out_sent_4, recov_reserve_name = reserve_sent_4(asset_name, status, resource_type, total_res, tot_liquid_res, tot_natgas_res, remain_res, rem_liquid_recov, rem_natgas_recov, model_type)
    reserves_output += out_sent_4

    if status.lower() == 'abandoned':
        out_sent_5, recov_reserve_name = reserve_sent_5(total_res, status, cutoff_year)
        reserves_output += out_sent_5

    out_sent_6 = reserve_sent_6(asset_name, asset_id, run_id, terrain, resource_type, recov_reserve_name, country, region, curr, model_type, position)
    reserves_output += out_sent_6

    if reserves_output:
        output += '\n' + reserves_output
    return output

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def economic_sent_1(curr, asset_id, run_id, terrain, resource_type, country, region, asset_name, remain_npv, npv_dev, irr_dev, status, model_type, position):
    if model_type == 'conventional':
        resource_type = None
    out_sent = ''
    if (not (remain_npv is None or irr_dev is None) and status.lower() != 'abandoned') or (not (npv_dev is None or irr_dev is None) and status.lower() == 'abandoned'):
        if status.lower() != 'abandoned':
            npv_val = remain_npv
            npv_name = 'remaining'
            npv_col = 'npv_rem'
        else:
            npv_val = npv_dev
            npv_name = 'development'
            npv_col = 'npv_dev'
        if float(npv_val) < 0:
            npv_val = -float(npv_val)
            part_a = 'The %s NPV for %s is -US$%s %s with a development IRR of %s%%, %s'
        else:
            part_a = 'The %s NPV for %s is US$%s %s with a development IRR of %s%%, %s'
        npv, npv_unit = num_convert(npv_val)
        mod = random.choice(['ranking', 'positioning', 'situating']) + ' this project '
        part_a = part_a % (npv_name, asset_name, npv, npv_unit, str("{:,}".format(round(irr_dev*100, 1))), mod)
        if 0:
            print 'asset_name, asset_id, run_id, npv_col, rank_order, terrain, resource_type, country, region, curr, False, model_type', (asset_name, asset_id, run_id, npv_col, 'DESC', terrain, resource_type, country, region, curr, False, model_type)
        part_b = rank_clause(asset_name, asset_id, run_id, npv_col, 'DESC', terrain, resource_type, country, region, curr, False, model_type=model_type, position=position)
        out_sent = part_a + part_b
    return out_sent

def economic_sent_2(curr, asset_name, status, capex_full, capex_rem, capex_boe_rem, opex_boe_rem, capex_opex_boe_rem, capex_boe_full, opex_boe_full):
    out_sent = ''
    if not (asset_name is None or capex_full is None or capex_boe_rem is None or opex_boe_rem is None):
        if status.lower() == 'producing':
            total_capex, capex_unit = num_convert(capex_rem)
            part_a = '  The total remaining capex for %s is US$%s %s, with a combined remaining '
            part_b1 = 'capital and operating expenditure per boe'
            part_b2 = 'capex per boe and opex per boe'
            part_b = random.choice([part_b1, part_b2])
            part_c = ' of US$%s.'
            params = (asset_name, total_capex, capex_unit, str("{:,}".format(round(capex_opex_boe_rem,2))))
            sent = part_a + part_b + part_c
            out_sent = sent % params
        elif status.lower() in ['planned', 'announced']:
            total_capex, capex_unit = num_convert(capex_full)
            part_a = '  The total capex for %s is US$%s %s, with a combined remaining '
            part_b1 = 'capital and operating expenditure per boe'
            part_b2 = 'capex per boe and opex per boe'
            part_b = random.choice([part_b1, part_b2])
            part_c = ' of US$%s.'
            params = (asset_name, total_capex, capex_unit, str("{:,}".format(round(capex_opex_boe_rem,2))))
            sent = part_a + part_b + part_c
            out_sent = sent % params
        elif status.lower() == 'abandoned' and not (capex_boe_full is None or opex_boe_full is None):
            total_capex, capex_unit = num_convert(capex_full)
            part_a = '  The total capex for %s is US$%s %s, with a combined full-cycle '
            part_b1 = 'capital and operating expenditure per boe'
            part_b2 = 'capex per boe and opex per boe'
            part_b = random.choice([part_b1, part_b2])
            part_c = ' of US$%s.'
            capex_opex_boe_full = float(capex_boe_full) + float(opex_boe_full)
            params = (asset_name, total_capex, capex_unit, str("{:,}".format(round(capex_opex_boe_full,2))))
            sent = part_a + part_b + part_c
            out_sent = sent % params
    return out_sent

def economic_sent_3(curr, asset_id, run_id, terrain, resource_type, country, region, asset_name,status,model_type,position):
    if model_type == 'conventional':
        resource_type = None
    if status.lower() == 'abandoned':
        part_a = '  In terms of the combined full-cycle metrics, %s is positioned '
        param_name = '(capex_boe_full + opex_boe_full)'
    else:
        part_a = '  In terms of the combined remaining capex and opex per boe, %s is positioned '
        param_name = 'capex_opex_boe_rem'
    part_b = rank_clause(asset_name, asset_id, run_id, param_name, 'ASC', terrain, resource_type, country, region, curr, False, model_type=model_type,position=position)
    params = (asset_name,)
    part_a = part_a % params
    sent = part_a + part_b
    return sent

def economics_section(output, curr, asset_id, run_id, terrain, resource_type, country, country_name, region, status, asset_name, capex_full, capex_rem, capex_boe_rem, opex_boe_rem, capex_opex_boe_rem, capex_boe_full, opex_boe_full, npv_rem, npv_dev, irr_dev, operator, model_type, position):
    economics_output = ''

    out_sent_1 = economic_sent_1(curr, asset_id, run_id, terrain, resource_type, country, region, asset_name, npv_rem, npv_dev, irr_dev, status, model_type, position)
    economics_output += out_sent_1

    out_sent_2 = economic_sent_2(curr, asset_name, status, capex_full, capex_rem, capex_boe_rem, opex_boe_rem, capex_opex_boe_rem, capex_boe_full, opex_boe_full)
    if out_sent_2:
        economics_output += out_sent_2

        out_sent_3 = economic_sent_3(curr, asset_id, run_id, terrain, resource_type, country, region, asset_name, status, model_type, position)
        economics_output += out_sent_3

    if economics_output:
        output += '\n' + economics_output
    return output

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def current_comm_price(curr, price_name, debug=False):
    commodity_price = get_data('`{}`'.format(get_discount_year()), 'prices_data', datatype='float', single_value=True, cursor=curr, sql_where="price_name like '%{}%'".format(price_name.strip()), debug=debug)
    #Here sql_where argument in above function is modfied from "price_name = '{}'" to price_name like '%{}.strip()%' on 29_01_2025
    if debug: print 'commodity_price: {}'.format(commodity_price)
    return commodity_price

def breakeven_sent_1(asset_name, fiscal, crude_bm, ng_bm, condensate_bm, lng_bm, ngls_bm):
    out_sent = ''
    if crude_bm or ng_bm or condensate_bm or lng_bm or ngls_bm:
        part_a = '%s was valued using '
        part_b = ' under the %s fiscal regime.' % fiscal
        bm_parts = []
        benchmarks = [(bm,com) for bm,com in [(crude_bm,'crude oil'), (ng_bm,'natural gas'), (condensate_bm,'condensate'), (lng_bm,'LNG'), (ngls_bm,'NGL')] if (bm is not None and bm != '')]

        params = (asset_name,)
        for benchmark, commodity in benchmarks:
            bm_parts.append('the %s price benchmark for %s')
            params += (benchmark.strip(), commodity)
        sent = sent_form(1, part_a, *bm_parts)
        try:
            ret_sent = sent % params
            ret_sent = ret_sent[:-1] + part_b
        except:
            ret_sent = ''
        out_sent = ret_sent

    return out_sent

def breakeven_sent_2(asset_name, status, be_gas_rem, be_oil_rem, be_gas_dev, be_oil_dev, curr, crude_bm, ng_bm, condensate_bm, lng_bm, debug=False):
    out_sent = ''

    if status.lower() == 'producing' and not (be_gas_rem == 999999999 or be_oil_rem == 999999999) \
            and not (be_gas_rem < 0 or be_oil_rem < 0) and not (be_gas_rem > 50 or be_oil_rem > 250)\
            and (((crude_bm or condensate_bm) and (be_oil_rem > 0)) or ((ng_bm and lng_bm) and (be_gas_rem > 0))):

            sent = '  Given the current %s price is US$%s/%s and the fields\'s remaining break-even of US$%s/%s, this project is %s.'
            if (crude_bm or condensate_bm) and (be_oil_rem > 0):
                if crude_bm:
                    commodity = 'crude oil'
                    commodity_bm = crude_bm
                else:
                    commodity = 'liquids'
                    commodity_bm = condensate_bm
                commodity_unit = 'bbl'
                breakeven_price = round(be_oil_rem,2)
            elif (ng_bm and lng_bm) and (be_gas_rem > 0):
                if ng_bm:
                    commodity = 'natural gas'
                    commodity_bm = ng_bm
                else:
                    commodity = 'gas'
                    commodity_bm = lng_bm
                commodity_unit = 'mcf'
                breakeven_price = round(be_gas_rem,2)

            commodity_price = current_comm_price(curr, commodity_bm, debug=debug)

            if commodity_price - breakeven_price < 0:
                project_val = 'unprofitable'
            else:
                project_val = 'profitable'

            params = (commodity, commodity_price, commodity_unit, breakeven_price, commodity_unit, project_val)
            out_sent = sent % params

    elif status.lower() in ['planned', 'announced'] and not (be_gas_dev == 999999999 or be_oil_dev == 999999999) \
            and not (be_gas_dev < 0 or be_oil_dev < 0) and not (be_gas_dev > 50 or be_oil_dev > 250) \
            and (((crude_bm or condensate_bm) and (be_oil_dev > 0)) or ((ng_bm or lng_bm) and (be_gas_dev > 0))):
            breakeven_price = 0
            sent = '  %s the current %s price of US$%s/%s, the development break-even is US$%s/%s, making this project %s.'
            if (crude_bm or condensate_bm) and (be_oil_dev > 0):
                if crude_bm:
                    commodity = 'crude oil'
                    commodity_bm = crude_bm
                else:
                    commodity = 'liquids'
                    commodity_bm = condensate_bm
                commodity_unit = 'bbl'
                breakeven_price = round(be_oil_dev,2)
            elif (ng_bm or lng_bm) and (be_gas_dev > 0):
                if ng_bm:
                    commodity = 'natural gas'
                    commodity_bm = ng_bm
                else:
                    commodity = 'gas'
                    commodity_bm = lng_bm
                commodity_unit = 'mcf'
                breakeven_price = round(be_gas_dev,2)
            mod = random.choice(['With', 'Considering'])
            commodity_price = current_comm_price(curr, commodity_bm, debug=debug)

            if commodity_price - breakeven_price < 0:
                project_val = 'economically unfavorable'
            else:
                project_val = 'economically favorable'

            params = (mod, commodity, commodity_price, commodity_unit, breakeven_price, commodity_unit, project_val)
            out_sent = sent % params
    return out_sent

def breakeven_sent_3(be_gas_rem, be_oil_rem, be_gas_dev, be_oil_dev, asset_name, asset_id, run_id, terrain, resource_type, country, region, curr, status, model_type, position):
    out_sent = ''
    be_name = ''
    if model_type == 'conventional':
        resource_type = None
    if status.lower() != 'abandoned':
        if (0 < be_gas_rem < 50) or (0 < be_oil_rem < 250):

            part_a = '  %s the remaining break-even price, %s ranks '
            if be_oil_rem == 0:
                be_name = 'be_gas_rem'
            else:
                be_name = 'be_oil_rem'

            part_b = rank_clause(asset_name, asset_id, run_id, be_name, 'DESC', terrain, resource_type, country, region, curr, False, model_type=model_type, position=position)
            mod = random.choice(['Regarding', 'With respect to'])
            part_a = part_a % (mod, asset_name)
            out_sent = part_a + part_b

    elif status.lower() == 'abandoned':
        if (0 < be_gas_dev < 50) or (0 < be_oil_dev < 250):
            part_a = '  The development break-even was US$%s/%s, ranking %s '
            if be_oil_dev == 0:
                be_name = 'be_gas_dev'
                be_val = round(be_gas_dev,2)
                commodity_unit = 'mcf'
            else:
                be_name = 'be_oil_dev'
                be_val = round(be_oil_dev,2)
                commodity_unit = 'bbl'
            part_b = rank_clause(asset_name, asset_id, run_id, be_name, 'DESC', terrain, resource_type, country, region, curr, False, model_type=model_type,position=position)
            part_a = part_a % (be_val, commodity_unit, asset_name)
            out_sent = part_a + part_b

    return out_sent

def breakevens_section(output, asset_name, asset_id, run_id, terrain, resource_type, country, country_name, region, status, fiscal, be_rem_gas, be_rem_oil, be_gas_dev, be_oil_dev, crude_bm, ng_bm, condensate_bm, lng_bm, ngls_bm, curr, operator, debug, model_type, position):
    breakevens_output = ''
    out_sent_1 = breakeven_sent_1(asset_name, fiscal, crude_bm, ng_bm, condensate_bm, lng_bm, ngls_bm)
    breakevens_output += out_sent_1

    out_sent_2 = breakeven_sent_2(asset_name, status, be_rem_gas, be_rem_oil, be_gas_dev, be_oil_dev, curr, crude_bm, ng_bm, condensate_bm, lng_bm)
    breakevens_output += out_sent_2

    out_sent_3 = breakeven_sent_3(be_rem_gas, be_rem_oil, be_gas_dev, be_oil_dev, asset_name, asset_id, run_id, terrain, resource_type, country, region, curr, status, model_type, position)
    if out_sent_3:
        breakevens_output += out_sent_3

    if breakevens_output:
        output += '\n' + breakevens_output
    return output

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def asset_sent(curr, asset_name, status, formation, country, country_name):
    out_sent = ''
    if formation and formation != 'NULL' and country:
        mod_a1 = 'produces'
        mod_a2 = ''
        formations = []
        if ';' in formation:
            formations = formation.split(';')
        else:
            formations.append(formation)
        formation_count = len(formations)
        formation_limit = min(20, formation_count)
        formation_names = formations[:formation_limit]
        if formation_count > 1:
            mod_a2 = 's'
            formation_list = sent_form(1,'',*formation_names)[:-1]
        else:
            formation_list = formation

        if status.lower() in ['planned', 'announced']:
            mod_a1 = 'will produce'
        elif status.lower() == 'abandoned':
            mod_a1 = 'produced'

        part_a = '%s %s from the %s formation%s, ' % (asset_name, mod_a1, formation_list,  mod_a2)
        # ---------------------------------------------------------------------------------------
        common_formations = []
        for asset_formation in formations:
            sql_select = "SELECT COUNT(DISTINCT asset_id) FROM econ_data WHERE country='%s' AND NOT (formation IS NULL OR formation='NULL')" % country
            curr.execute(sql_select)
            country_total = curr.fetchone()[0]

            sql_select = 'SELECT COUNT(DISTINCT asset_id) FROM econ_data WHERE country="%s" AND formation LIKE "%%%s%%"'% (country, asset_formation)
            curr.execute(sql_select)
            formation_in_country = curr.fetchone()[0]

            if (float(formation_in_country)/float(country_total)) > 0.6:
                common_formations.append(asset_formation)

        if not common_formations:
            part_b = 'which few fields produce from '
        else:
            if len(common_formations) == formation_count:
                part_b = 'which many fields produce from '

            elif len(common_formations) > 1:
                common_formation_limit = min(len(common_formations), 20)
                common_formation_names = common_formations[:common_formation_limit]
                common_formation_list = sent_form(1,'', *common_formation_names)[:-1]
                part_b = 'where many fields produce from %s ' % common_formation_list
            else:
                common_formation_list = common_formations[0]
                part_b = 'where many fields produce from %s ' % common_formation_list

        # ---------------------------------------------------------------------------------------
        mod_c1 = random.choice(['the', 'this']) + ' country'
        mod_c2 = country_name
        mod_c = random.choice([mod_c1, mod_c2])

        part_c = 'in %s.  ' % mod_c

        out_sent = part_a + part_b + part_c
    return out_sent

def asset_section(output, curr, asset_name, status, formation, country, country_name, model_type):

    asset_output = ''

    asset_output = asset_sent(curr, asset_name, status, formation, country, country_name)

    if asset_output:
        output += '\n' + asset_output
    return output

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_irr_rank(curr, asset_id, status, resource_type, irr_dev, run_id, debug=False):
    param_rank = 0
    param_total = 1
    sql_select = 'SELECT asset_id FROM econ_data WHERE run_id="{0}" AND resource_type="{1}" AND status="{2}" '
    sql_select += 'AND NOT (asset_name is NULL OR asset_name LIKE "Other %" OR asset_name LIKE "Others %") ORDER BY irr_dev DESC '
    curr.execute(sql_select.format(run_id, resource_type, status))
    ranked_uncon_assets = [data[0] for data in curr.fetchall()]
    param_rank = ranked_uncon_assets.index(asset_id) + 1
    param_total = len(ranked_uncon_assets)
    if debug:
        print '{}: {}/{}'.format(asset_id, param_rank, param_total)
    irr_rank_pct = round(1 - (float(param_rank)/float(param_total)),2)
    return irr_rank_pct

def get_reserves_rank(curr, asset_id, status, resource_type, run_id, debug=False):
    param_rank = 0
    param_total = 1
    sql_select = 'SELECT asset_id FROM econ_data WHERE run_id="{0}" AND resource_type="{1}" AND status="{2}" '
    sql_select += 'AND NOT (asset_name is NULL OR asset_name LIKE "Other %" OR asset_name LIKE "Others %") ORDER BY total_recov DESC '
    curr.execute(sql_select.format(run_id, resource_type, status))
    ranked_uncon_assets = [data[0] for data in curr.fetchall()]
    param_rank = ranked_uncon_assets.index(asset_id) + 1
    param_total = len(ranked_uncon_assets)
    if debug:
        print '{}: {}/{}'.format(asset_id, param_rank, param_total)
    reserve_rank_pct = round(1 - (float(param_rank) / float(param_total)), 3)
    return reserve_rank_pct

def get_opex_terrain_rank(curr, asset_id, status, terrain, region, run_id, debug=False):
    param_rank = 0
    param_total = 1
    sql_select = 'SELECT asset_id FROM econ_data WHERE run_id="{0}" AND terrain="{1}" AND region="{2}" AND status="{3}" '
    sql_select += 'AND NOT (asset_name is NULL OR asset_name LIKE "Other %" OR asset_name LIKE "Others %") ORDER BY opex_boe_full ASC '
    curr.execute(sql_select.format(run_id, terrain, region, status))
    ranked_uncon_assets = [data[0] for data in curr.fetchall()]
    param_rank = ranked_uncon_assets.index(asset_id) + 1
    param_total = len(ranked_uncon_assets)
    if debug:
        print '{}: {}/{}'.format(asset_id, param_rank, param_total)
    terrain_rank_pct = round(1 - (float(param_rank) / float(param_total)), 3)
    return terrain_rank_pct

def get_opex_global_rank(curr, asset_id, status, terrain, run_id, debug=False):
    param_rank = 0
    param_total = 1
    sql_select = 'SELECT asset_id FROM econ_data WHERE run_id="{0}" AND terrain="{1}" AND `status`="{2}" '
    sql_select += 'AND NOT (asset_name is NULL OR asset_name LIKE "Other %" OR asset_name LIKE "Others %") ORDER BY opex_boe_full ASC '
    curr.execute(sql_select.format(run_id, terrain, status))
    ranked_uncon_assets = [data[0] for data in curr.fetchall()]
    param_rank = ranked_uncon_assets.index(asset_id) + 1
    param_total = len(ranked_uncon_assets)
    if debug:
        print '{}: {}/{}'.format(asset_id, param_rank, param_total)
    global_rank_pct = round(1 - (float(param_rank)/float(param_total)),3)
    return global_rank_pct

def get_capex_opex_boe_rank(curr, asset_id, status, resource_type, region, run_id, debug=False):
    param_rank = 0
    param_total = 1
    sql_select = 'SELECT asset_id FROM econ_data WHERE run_id="{0}" AND resource_type="{1}" AND Region="{2}" AND `status`="{3}" '
    sql_select += 'AND NOT (asset_name is NULL OR asset_name LIKE "Other %" OR asset_name LIKE "Others %") ORDER BY (capex_boe_full + opex_boe_full) ASC '
    curr.execute(sql_select.format(run_id, resource_type, region, status))
    ranked_assets = [data[0] for data in curr.fetchall()]
    param_rank = ranked_assets.index(asset_id) + 1
    param_total = len(ranked_assets)
    if debug:
        print '{}: {}/{}'.format(asset_id, param_rank, param_total)
    regional_rank_pct = round(1 - (float(param_rank)/float(param_total)),3)
    return regional_rank_pct


def FIELD_SIZE(total_res):
    field_size = ''
    if total_res > 500000000:
        field_size = 'giant'
    elif total_res > 200000000:
        field_size = 'large'
    elif total_res > 50000000:
        field_size = 'mid-sized'
    else:
        field_size = 'small'
    return field_size


PART_1 = {
    'PRODUCING': ' producing', 
    'ANNOUNCED': '',            
    'PLANNED'  : ''
}

PART_2 = {
    'PRODUCING': 'field',      
    'ANNOUNCED': 'development', 
    'PLANNED'  : 'development'
}

PART_3 = {
    'CRUDE OIL'  : 'bd', 
    'NATURAL GAS': 'mmcfd',     
    'CONDENSATE' : 'bd', 
    'NGL'        : 'bd', 
    'LNG'        : 'mmcfd'
}

def PART_4(remain_res, total_res):
    part_4          = ''
    recover_res_pct = 0
    if remain_res and total_res and (remain_res > 0) and (total_res > 0) and (total_res > remain_res):
        recover_res_pct = (1 - (float(remain_res)/float(total_res)))
        if recover_res_pct >= 0.8:
            part_4 = 'is mature'
        elif recover_res_pct < 0.5:
            part_4 = 'is yet to reach midway through field life'
        else:
            part_4 = 'is midway through field life'
        recover_res_pct = round(recover_res_pct*100,2)
    return part_4, recover_res_pct

def PART_5(rank_pct):
    part_5 = ''
    if rank_pct >= 0.67:
        part_5 = 'top'
    elif rank_pct >= 0.33:
        part_5 = 'middle'
    else:
        part_5 = 'bottom'
    return part_5

def PART_6(commodity_price, breakeven_price):
    if commodity_price - breakeven_price < 0:
        project_val = 'economically unfavorable'
    else:
        project_val = 'economically favorable'
    return project_val

def PART_7(irr_rank_pct):
    part_7 = ''
    if irr_rank_pct >= 0.75:
        part_7 = 'top'
    elif irr_rank_pct >= 0.5:
        part_7 = 'second'
    elif irr_rank_pct >= 0.25:
        part_7 = 'third'
    else:
        part_7 = 'bottom'
    return part_7

def PART_8(commodity_price, breakeven_price):
    if commodity_price - breakeven_price < 0:
        project_val = 'unprofitable'
    else:
        project_val = 'profitable'
    return project_val

def PART_9(opex_boe_full, avg_op_costs):
    part_9 = ''
    if opex_boe_full < 0.85*avg_op_costs:
        part_9 = 'low'
    elif opex_boe_full > 1.15*avg_op_costs:
        part_9 = 'high'
    else:
        part_9 = 'similar'
    return part_9

def PART_10(rank_pct):
    part_10 = ''
    if rank_pct >= 0.67:
        part_10 = 'above'
    elif rank_pct >= 0.33:
        part_10 = 'close to'
    else:
        part_10 = 'below'
    return part_10

def PART_11(peak_year):
    part_11 = 'and is expected to reach'
    current_year = get_discount_year()
    if peak_year < current_year:
        part_11 = 'with'
    return part_11

def PART_12(region):
    part_12 = region
    if region.lower() in ['middle east', 'former soviet union']:
        part_12 = 'the {}'.format(region)
    return part_12

def sentence_1(asset_name, total_res, status, resource_type, terrain, country, operator):
    field_size = FIELD_SIZE(total_res)
    part_1     = PART_1[status.upper()]
    part_2     = PART_2[status.upper()]

    field_params = (asset_name, field_size, part_1, resource_type, part_2, terrain, country, operator)

    out_sent = "{} is a {}{} {} {} located in {} {} and is operated by {}."

    return out_sent.format(*field_params)

def sentence_2(sent_type, peak_prod_unit, remain_res, total_res, project_stage, project_name, project_active_year, stage_change_quarter, first_prod, peak_production, peak_year, asset_name, fid, pilot_test=0, debug=False):
    part_4, recover_res_pct = PART_4(remain_res, total_res)
    part_11 = PART_11(peak_year)
    peak_prod = str("{:,}".format(round(peak_production,1)))

    OUT_SENT = {
        'a1': ["The project entered {} stage in {} and is anticipated to come online in {}, peaking at {} {} by {}.",
              (project_stage, stage_change_quarter, project_active_year, peak_prod, peak_prod_unit, peak_year)],

        'a2': ["The project is currently in the construction stage and is anticipated to come online in {}, peaking at {} {} by {}.",
               (project_active_year, peak_prod, peak_prod_unit, peak_year)],
        
        'a3': ["The project is anticipated to come online in {}, peaking at {} {} by {}.",
               (first_prod, peak_prod, peak_prod_unit, peak_year)],
        
        'b': ["The field {}, having recovered {}% of its total reserves, {} peak production in {}.",
              (part_4, recover_res_pct, part_11, peak_year)],

        'c': ["An expansion project, {}, is currently in the {} stage, targeting start-up in {}.",
              (project_name, project_stage, project_active_year)],

        'd': ["The project's final investment decision (FID) is targeted for {} and is anticipated to come online in {}, peaking at {} {} by {}.",
              (fid, project_active_year, peak_prod, peak_prod_unit, peak_year)],

        'e': ["The project entered its {} stage in {}.  ",
              (project_stage, stage_change_quarter)],

        'f': ["The {} field is undergoing pilot testing and is expected to realize peak capacity of {} {} in {}.",
              (asset_name, peak_prod, peak_prod_unit, peak_year)],
       
        'g': ["The project's final investment decision (FID) was finalized in {} and is anticipated to come online in {}, peaking at {} {} by {}.",
              (fid, project_active_year, peak_prod, peak_prod_unit, peak_year)],
    }

    out_sent, field_params = OUT_SENT[sent_type]
    return out_sent.format(*field_params)

def sentence_3(epc_contractor):
    out_sent = "EPC work has been contracted to {}."
    if ';' in epc_contractor:
        params = [1] + [contractor.strip() for contractor in epc_contractor.split(';')]
        epc_contractor_str = sent_form(*params)
    else:
        epc_contractor_str = epc_contractor
    if epc_contractor_str[-1] == '.':
        epc_contractor_str = epc_contractor_str[:-1]
    return out_sent.format(epc_contractor_str)

def sentence_4(remain_res, rem_lqd_recov, rem_ng_recov):
    out_sent = "The field is expected to recover {} mmboe, comprised of {} mmbbl of liquid reserves and {} bcf of natural gas reserves."

    field_params = (str("{:,}".format(round(float(remain_res/1000000.0), 1))), str("{:,}".format(round(float(rem_lqd_recov/1000000.0), 1))),  str("{:,}".format(round(float(rem_ng_recov), 1))))
    return out_sent.format(*field_params)

def sentence_5(status, resource_type, curr, asset_id, run_id, debug=False):
    out_sent = "This ranks the field reserves within the {} {}% of existing {} {} fields globally."

    reserve_rank_pct = get_reserves_rank(curr, asset_id, status, resource_type, run_id, debug=debug)

    part_5 = PART_5(reserve_rank_pct)

    if part_5 == 'top':
        rank_pct = round((1 - reserve_rank_pct)*100,2)
    else:
        rank_pct = round((reserve_rank_pct)*100,2)

    field_params = (part_5, rank_pct, status, resource_type)
    return out_sent.format(*field_params)

def sentence_6(sent_type, curr, be_gas_rem, be_oil_rem, be_gas_dev, be_oil_dev, crude_bm, ng_bm, condensate_bm, lng_bm, peak_comm, status, resource_type, irr_dev, asset_id, run_id, debug=False):
    irr_rank_pct = get_irr_rank(curr, asset_id, status, resource_type, irr_dev, run_id, debug=debug)
    discount_year = get_discount_year()
    benchmark_name = ''
    be_rem_unit    = ''
    be_dev_value   = 0
    be_rem_value   = 0
    #ng
    # crude
    # ngls
    # condensate
    # lng
    if debug:
        print crude_bm, condensate_bm, ng_bm, lng_bm, peak_comm
    if (crude_bm or condensate_bm) and (0 < be_oil_rem < 250) and (0 < be_oil_rem < 250):
        if crude_bm and peak_comm.lower() != 'condensate':
            commodity = 'crude oil'
            benchmark_name = crude_bm
        else:
            commodity = 'liquids'
            benchmark_name = condensate_bm
        be_rem_unit = 'bbl'
        be_rem_value = round(be_oil_rem, 2)
        be_dev_value = round(be_oil_dev, 2)
        if debug: print 1, benchmark_name
    elif (ng_bm or lng_bm) and (0 < be_gas_rem < 50) and (0 < be_gas_dev < 50):
        if ng_bm and peak_comm.lower() != 'lng':
            commodity = 'natural gas'
            benchmark_name = ng_bm

        else:
            commodity = 'gas'
            benchmark_name = lng_bm

        be_rem_unit = 'mcf'
        be_rem_value = round(be_gas_rem, 2)
        be_dev_value = round(be_gas_dev, 2)
        if debug: print 2, benchmark_name
    be_dev_unit     = be_rem_unit
    benchmark_unit  = be_rem_unit
    commodity_price = current_comm_price(curr, benchmark_name, debug=debug)
    if debug: print 'commodity_price: {} -- be_dev_value: {}'.format(commodity_price, be_dev_value)
    part_6 = PART_6(commodity_price, be_dev_value)
    part_7 = PART_7(irr_rank_pct)
    part_8 = PART_8(commodity_price, be_rem_value)
    OUT_SENT = {
        'a': ["The estimated development break-even price of US${}/{}, compared to a {} {} price of US${}/{} suggests this project appears {} and the project's rate of return is in the {} quartile for {} {} projects.",
              (str("{:,.2f}".format(round(be_dev_value,2))), be_dev_unit, benchmark_name, discount_year, str("{:,.2f}".format(round(commodity_price,2))), benchmark_unit, part_6, part_7, status, resource_type)],
        'b': ["Given a {} {} price of US${}/{} and the field's estimated remaining break-even of US${}/{}, this project is {}.",
              (discount_year, benchmark_name, str("{:,.2f}".format(round(commodity_price,2))), benchmark_unit, str("{:,.2f}".format(round(be_rem_value,2))), be_rem_unit, part_8)]
    }
    out_sent, field_params = OUT_SENT[sent_type]
    return out_sent.format(*field_params)

def sentence_7(curr, curr_opex_boe, resource_type, region, status, run_id):
    avg_op_costs = get_data('ROUND(AVG(curr_opex_boe),2)', 'econ_data', cursor=curr, single_value=True, datatype='float', sql_where='region="{}" AND status="{}" AND resource_type="{}" AND run_id="{}"'.format(region, status, resource_type, run_id))

    #out_sent = "The field's operating costs, of around ${} per boe, are {} compared to the regional average for {} fields."
    out_sent = "The field's operating costs are {} compared to the regional average for {} fields."

    part_9 = PART_9(curr_opex_boe, avg_op_costs)

    field_params = (part_9, status, resource_type)
    return out_sent.format(*field_params)

def sentence_8(curr, terrain, region, asset_id, status, run_id, debug=False):
    terrain_rank_pct = get_opex_terrain_rank(curr, asset_id, status, terrain, region, run_id, debug=debug)
    global_rank_pct  = get_opex_global_rank(curr, asset_id, status, terrain, run_id, debug=debug)

    out_sent = "On a value per boe basis, the field is positioned in the {} {}% of {} fields in {}, and the {} {}% of {} fields globally."

    part_5a = PART_5(terrain_rank_pct)
    part_5b = PART_5(global_rank_pct)

    region_str = PART_12(region)

    if part_5a == 'top':
        rank_5a_pct = round((1 - terrain_rank_pct)*100,2)
    else:
        rank_5a_pct = round((terrain_rank_pct)*100,2)

    if part_5b == 'top':
        rank_5b_pct = round((1 - global_rank_pct)*100,2)
    else:
        rank_5b_pct = round((global_rank_pct)*100,2)

    field_params = (part_5a, rank_5a_pct , terrain, region_str, part_5b, rank_5b_pct, status)
    return out_sent.format(*field_params)

def sentence_9(curr, project_cost, capex_boe_full, opex_boe_full, resource_type, region, asset_id, status, run_id, debug=False):
    capex_opex_rank_pct = get_capex_opex_boe_rank(curr, asset_id, status, resource_type, region, run_id, debug=debug)

    if project_cost:
        part_a = "The project cost is expected to be US${} mil, and its ".format(str("{:,}".format(round(project_cost,1))))
    else:
        part_a = "Its "

    part_b = "lifetime combined capital and operating expenditure per boe place it {} the average for new {} developments in {}."
    out_sent = part_a + part_b

    part_10 = PART_10(capex_opex_rank_pct)

    region_str = PART_12(region)

    field_params = (part_10, status, region_str)
    return out_sent.format(*field_params)

def announced_planned_panorama(asset_id, run_id, asset_name, total_res, status, resource_type, terrain, country, operator, peak_prod_unit, remain_res, project_stage, project_name, project_active_year, stage_change_quarter, first_prod, peak_comm, peak_prod, peak_year,
                               epc_contractor, rem_lqd_recov, rem_ng_recov, curr, be_gas_rem, be_oil_rem, be_gas_dev, be_oil_dev, crude_bm, ng_bm, condensate_bm, lng_bm, irr_dev, project_cost, pilot_test, capex_boe_full, opex_boe_full, region, fid, debug=False):
    output = ''
    if asset_name and total_res and status and resource_type and terrain and country and operator:
        output += sentence_1(asset_name, total_res, status.lower(), resource_type.lower(), terrain.lower(), country, operator) + '  '
    
    if peak_prod_unit and peak_prod and peak_year:
        if pilot_test:
            if project_stage and stage_change_quarter:
                output += sentence_2('e', peak_prod_unit, remain_res, total_res, project_stage.lower(), project_name, project_active_year, stage_change_quarter, first_prod, peak_prod, peak_year, asset_name, fid, pilot_test, debug)
            output += sentence_2('f', peak_prod_unit, remain_res, total_res, project_stage, project_name, project_active_year, stage_change_quarter, first_prod, peak_prod, peak_year, asset_name, fid, pilot_test, debug) + '  '
        elif fid and project_active_year:
            discount_year = get_discount_year(cursor=curr)
            fid_year = int(fid[-4:])
            if fid_year < discount_year:
                output += sentence_2('g', peak_prod_unit, remain_res, total_res, project_stage, project_name, project_active_year, stage_change_quarter, first_prod, peak_prod, peak_year, asset_name, fid, pilot_test, debug) + '  '
            else:
                output += sentence_2('d', peak_prod_unit, remain_res, total_res, project_stage, project_name, project_active_year, stage_change_quarter, first_prod, peak_prod, peak_year, asset_name, fid, pilot_test, debug) + '  '
        elif project_stage and stage_change_quarter and project_active_year:
            output += sentence_2('a1', peak_prod_unit, remain_res, total_res, project_stage.lower(), project_name, project_active_year, stage_change_quarter, first_prod, peak_prod, peak_year, asset_name, fid, pilot_test, debug) + '  '
        elif project_active_year:
            output += sentence_2('a2', peak_prod_unit, remain_res, total_res, project_stage, project_name, project_active_year, stage_change_quarter, first_prod, peak_prod, peak_year, asset_name, fid, pilot_test, debug) + '  '
        elif first_prod:
            output += sentence_2('a3', peak_prod_unit, remain_res, total_res, project_stage, project_name, project_active_year, stage_change_quarter, first_prod, peak_prod, peak_year, asset_name, fid, pilot_test, debug) + '  '

    if epc_contractor:
        output += sentence_3(epc_contractor) + '  '
    
    if remain_res and rem_lqd_recov and rem_ng_recov:
        output += sentence_4(remain_res, rem_lqd_recov, rem_ng_recov) + '  '
    
    if status and resource_type:
        output += sentence_5(status.lower(), resource_type.lower(), curr, asset_id, run_id, debug=debug) + '  '

    if capex_boe_full and opex_boe_full and region and resource_type:
        output += sentence_9(curr, project_cost, capex_boe_full, opex_boe_full, resource_type.lower(), region, asset_id, status.lower(), run_id, debug=debug) + '  '

    if curr and (((crude_bm or condensate_bm) and (0 < be_oil_rem < 250) and (0 < be_oil_rem < 250)) or ((ng_bm or lng_bm) and (0 < be_gas_rem < 50) and (0 < be_gas_dev < 50))) and status and resource_type and irr_dev:
        output += sentence_6('a', curr, be_gas_rem, be_oil_rem, be_gas_dev, be_oil_dev, crude_bm, ng_bm, condensate_bm, lng_bm, peak_comm, status.lower(), resource_type.lower(), irr_dev, asset_id, run_id, debug=debug) + '  '
    return output


def producing_panorama(asset_id, run_id, asset_name, tot_res, status, resource_type, terrain, country, operator, peak_prod_unit, rem_res, project_stage, project_name, project_active_year, stage_change_quarter, first_prod, peak_comm,
                       peak_prod, peak_year, epc_contractor, opex_boe_full, curr, region, be_gas_rem, be_oil_rem, be_gas_dev, be_oil_dev, crude_bm, ng_bm, condensate_bm, lng_bm, irr_dev, curr_opex_boe, fid, debug=False):
    output = ''
    
    if asset_name and tot_res and status and resource_type and terrain and country and operator:
        output += sentence_1(asset_name, tot_res, status.lower(), resource_type.lower(), terrain.lower(), country, operator) + '  '
    
    if rem_res and tot_res and peak_year:
        output += sentence_2('b', peak_prod_unit, rem_res, tot_res, project_stage, project_name, project_active_year, stage_change_quarter, first_prod, peak_prod, peak_year, asset_name, fid, debug=debug) + '  '

    if project_stage and project_name and project_active_year:
        output += sentence_2('c', peak_prod_unit, rem_res, tot_res, project_stage.lower(), project_name, project_active_year, stage_change_quarter, first_prod, peak_prod, peak_year, asset_name, fid, debug=debug) + '  '
    
    if epc_contractor:
        output += sentence_3(epc_contractor) + '  '
    
    if opex_boe_full and resource_type and region:
        output += sentence_7(curr, curr_opex_boe, resource_type.lower(), region, status.lower(), run_id) + '  '

    if curr and (((crude_bm or condensate_bm) and (0 < be_oil_rem < 250) and (0 < be_oil_rem < 250)) or ((ng_bm or lng_bm) and (0 < be_gas_rem < 50) and (0 < be_gas_dev < 50))) and status and resource_type and irr_dev:
        output += sentence_6('b', curr, be_gas_rem, be_oil_rem, be_gas_dev, be_oil_dev, crude_bm, ng_bm, condensate_bm, lng_bm, peak_comm, status.lower(), resource_type.lower(), irr_dev, asset_id, run_id, debug=debug) + '  '
    
    if terrain and region:
        output += sentence_8(curr, terrain.lower(), region, asset_id, status.lower(), run_id, debug=debug) + '  '
    return output


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def generate_news_deals_contracts_section(output_file=None):
    ndc_file = DATA_DIR + 'NewsDealsContracts.xlsx'
    ndc_wb = openpyxl.load_workbook(ndc_file)

    ndc_data = {'News': {'title': 'C', 'summary': 'D'},
                'Deals': {'title': 'F', 'summary': 'H'},
                'Contracts': {'title': 'G', 'summary': 'C'}}
    if output_file:
        with open(output_file, 'w') as outfile:
            output = '-' * 70 + '\n'
            for ws_name in ndc_data.keys():
                output += get_news_deals_contracts_data(ws_name, ndc_data, ndc_wb) + '-' * 70 + '\n'
            print output
            outfile.write(output.encode('utf-8'))
    ndc_wb.save(ndc_file)

def get_news_deals_contracts_data(ws_name, ndc_data, ndc_wb):
    news_deals_contracts = ws_name + ':\n'
    try:
        ws = ndc_wb[ws_name]
    except:
        ws = ndc_wb.get_sheet_by_name(ws_name)
    max_row = 6
    if ws.max_row < max_row:
        max_row = ws.max_row
    for row in range(2, max_row + 1):
        title = ws[ndc_data[ws_name]['title'] + str(row)].value
        summary = ws[ndc_data[ws_name]['summary'] + str(row)].value
        date = ws['B' + str(row)].value
        if '<P/>' in summary:
            summary = summary.replace('<P/>', '\r\t')
        news_deals_contracts += str(date).split()[0] + '\r\n'
        news_deals_contracts += title + '\r\n'
        news_deals_contracts += summary + '\r\n'
    return news_deals_contracts

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_peak_year(curr, run_id, asset_list=None, debug=False):
    prod_comms = {
        'ng'        : ('Natural Gas', 'Natural Gas'),
        'crude'     : ('Crude Oil', 'Crude Oil'),
        'lng'       : ('LNG', 'LNG'),
        'condensate': ('Condensate', 'Condensate'),
        'ngls'      : ('NGL', 'NGLs')
    }
    sql_update_1 = \
    '''
    UPDATE econ_data AS a, param_track AS b
      SET a.peak_comm=b.peak_commodity
      WHERE a.asset_id=b.asset_id AND a.session_key=b.session_key AND a.run_id='{}';
    '''
    curr.execute(sql_update_1.format(run_id))
    commit(curr)
    
    sql_where = \
        '''
        run_id="{}" AND NOT `status` IN ("Discovered", "Stalled", "Suspended") AND NOT asset_name IS NULL AND NOT operator IS NULL AND NOT parent_company IS NULL AND NOT (asset_name LIKE "Other %" OR asset_name LIKE "Others %")
        '''
    
    if asset_list is None:
        assets = get_data('asset_id', 'econ_data', datatype='int', cursor=curr, sql_where=sql_where.format(run_id))
    else:
        assets = asset_list
    
    asset_num = 1
    asset_count = len(assets)
    for asset_id in assets:
        print '{}/{} peak year update: {}'.format(asset_num, asset_count, asset_id)
        sql_where = 'asset_id={} AND run_id="{}"'.format(asset_id, run_id)
        peak_comm, peak_prod, peak_prod_unit = get_data('peak_comm, peak_prod, peak_prod_unit', 'econ_data', datatype='plural', cursor=curr, single_value=True, sql_where=sql_where)
        prod_comm, conv_comm = prod_comms[peak_comm]
        prod_factor = get_data('factor * 1.0', 'unit_equals', datatype='float', single_value=True, cursor=curr, sql_where='unit="{}" AND commodity="{}" AND base_unit="Boe"'.format(peak_prod_unit, conv_comm))
        try:
            conv_prod = round(float(peak_prod)*prod_factor, 2)
        except:
            print("Check ", asset_id)
            conv_prod = 0.00

        sql_update = \
            '''
            UPDATE econ_data AS a,
              (SELECT MIN(b.period) AS first_peak_year FROM (SELECT DISTINCT period, production, unit FROM production WHERE casetype='Base Case' AND asset_id={0} AND commodity="{1}") AS b,
                (SELECT DISTINCT factor, unit FROM unit_equals WHERE commodity="{2}" AND base_unit="Boe") AS c
                 WHERE ROUND(b.production*c.factor,2)={3} AND c.unit=b.unit) AS d
              SET a.first_peak_year=d.first_peak_year
              WHERE a.asset_id={0} AND a.run_id="{4}"
            '''
        if debug: print sql_update.format(asset_id, prod_comm, conv_comm, conv_prod, run_id)
        try:
            curr.execute(sql_update.format(asset_id, prod_comm, conv_comm, conv_prod, run_id))
            commit(curr)
        except:
            curr.execute(sql_update.format(asset_id, prod_comm, conv_comm, conv_prod, run_id))
            commit(curr)
        asset_num += 1
    curr.execute('UPDATE econ_data SET first_peak_year=peak_year WHERE first_peak_year IS NULL AND peak_year IS NOT NULL')
    commit(curr)


def get_econ_data(curr, run_id, run_asset_id=None, run_country=None, run_region=None, asset_list=None, update_econ_data=False, debug=False):
    sql_update_1a = \
    '''
    UPDATE projects_extract SET stage_change_quarter=CONCAT('Q1 ',SUBSTRING(stage_change_quarter,1,4)) 
      WHERE LENGTH(stage_change_quarter)=10 AND SUBSTRING(stage_change_quarter,6,2) IN ('01', '02', '03');
    '''
    sql_update_1b = \
    '''
    UPDATE projects_extract SET stage_change_quarter=CONCAT('Q2 ',SUBSTRING(stage_change_quarter,1,4)) 
      WHERE LENGTH(stage_change_quarter)=10 AND SUBSTRING(stage_change_quarter,6,2) IN ('04', '05', '06');
    '''
    sql_update_1c = \
    '''
    UPDATE projects_extract SET stage_change_quarter=CONCAT('Q3 ',SUBSTRING(stage_change_quarter,1,4)) 
      WHERE LENGTH(stage_change_quarter)=10 AND SUBSTRING(stage_change_quarter,6,2) IN ('07', '08', '09');
    '''
    sql_update_1d = \
    '''
    UPDATE projects_extract SET stage_change_quarter=CONCAT('Q4 ',SUBSTRING(stage_change_quarter,1,4)) 
      WHERE LENGTH(stage_change_quarter)=10 AND SUBSTRING(stage_change_quarter,6,2) IN ('10', '11', '12');
    '''

    sql_update_2a = \
    '''
    UPDATE projects_extract SET fid=CONCAT('Q1 ',SUBSTRING(fid,1,4)) 
      WHERE LENGTH(fid)=10 AND SUBSTRING(fid,6,2) IN ('01', '02', '03');    
    '''
    sql_update_2b = \
    '''
    UPDATE projects_extract SET fid=CONCAT('Q2 ',SUBSTRING(fid,1,4)) 
      WHERE LENGTH(fid)=10 AND SUBSTRING(fid,6,2) IN ('04', '05', '06');    
    '''
    sql_update_2c = \
    '''
    UPDATE projects_extract SET fid=CONCAT('Q3 ',SUBSTRING(fid,1,4)) 
      WHERE LENGTH(fid)=10 AND SUBSTRING(fid,6,2) IN ('07', '08', '09');    
    '''
    sql_update_2d = \
    '''
    UPDATE projects_extract SET fid=CONCAT('Q4 ',SUBSTRING(fid,1,4)) 
      WHERE LENGTH(fid)=10 AND SUBSTRING(fid,6,2) IN ('10', '11', '12');    
    '''

    sql_update_2e = \
    '''
    UPDATE projects_extract SET project_active_year=NULL WHERE project_active_year='NULL';
    '''

    sql_update_2f = \
    '''
    UPDATE projects_extract SET project_cost=NULL WHERE project_cost='NULL';
    '''

    sql_update_2g = \
    '''
    UPDATE projects_extract SET epc_contractor=NULL WHERE epc_contractor='NULL';
    '''

    sql_update_2h = \
    '''
    UPDATE projects_extract SET stage_change_quarter=NULL WHERE stage_change_quarter='NULL';
    '''

    sql_update_2i = \
    '''
    UPDATE projects_extract SET fid=NULL WHERE fid='NULL';
    '''

    sql_update_2 = \
    '''
    UPDATE econ_data AS a, projects_extract AS b
      SET a.project_name=b.project_name, a.project_active_year=b.project_active_year, a.project_stage=b.project_stage, a.stage_change_quarter=b.stage_change_quarter, a.epc_contractor=b.epc_contractor, a.fid=b.fid
      WHERE a.asset_id=b.asset_id AND a.run_id="{}"
    '''

    sql_update_3 = \
    """
    UPDATE econ_data SET pilot_test=0 WHERE run_id='{}';
    """

    sql_update_4 = \
    """
    UPDATE econ_data SET pilot_test=1 
      WHERE `status` IN ('Planned', 'Announced')
      AND first_production <= (SELECT discount_year FROM global_variables WHERE id=1) 
      AND run_id='{}';
    """

    sql_update_5 = \
    """
    UPDATE econ_data AS a, projects_extract AS b SET a.project_cost_mm_usd=b.project_cost WHERE a.asset_id=b.asset_id AND a.run_id='{}' AND b.project_cost IS NOT NULL;
    """
    
    sql_update_6 = \
    """
    UPDATE econ_data SET stage_change_quarter=NULL WHERE stage_change_quarter='NULL' AND run_id=(SELECT DISTINCT run_id FROM global_variables WHERE id=1);
    """
    
    sql_update_7 = \
    """
    UPDATE econ_data SET project_active_year=NULL WHERE project_active_year='NULL' AND run_id=(SELECT DISTINCT run_id FROM global_variables WHERE id=1);
    """
    
    sql_update_8 = \
    """
    UPDATE econ_data SET epc_contractor=NULL WHERE epc_contractor='NULL' AND run_id=(SELECT DISTINCT run_id FROM global_variables WHERE id=1);
    """
    
    sql_update_9 = \
    """
    UPDATE econ_data SET fid=NULL WHERE fid='NULL' AND run_id=(SELECT DISTINCT run_id FROM global_variables WHERE id=1);
    """
    
    if update_econ_data:
        curr.execute(sql_update_1a)
        commit(curr)

        curr.execute(sql_update_1b)
        commit(curr)

        curr.execute(sql_update_1c)
        commit(curr)

        curr.execute(sql_update_1d)
        commit(curr)

        curr.execute(sql_update_2a)
        commit(curr)

        curr.execute(sql_update_2b)
        commit(curr)

        curr.execute(sql_update_2c)
        commit(curr)

        curr.execute(sql_update_2d)
        commit(curr)

        curr.execute(sql_update_2e)
        commit(curr)

        curr.execute(sql_update_2f)
        commit(curr)

        curr.execute(sql_update_2g)
        commit(curr)

        curr.execute(sql_update_2h)
        commit(curr)

        curr.execute(sql_update_2i)
        commit(curr)

        curr.execute(sql_update_2.format(run_id))
        commit(curr)

        curr.execute(sql_update_3.format(run_id))
        commit(curr)

        curr.execute(sql_update_4.format(run_id))
        commit(curr)

        curr.execute(sql_update_5.format(run_id))
        commit(curr)
        
        curr.execute(sql_update_6)
        commit(curr)
        
        curr.execute(sql_update_7)
        commit(curr)
        
        curr.execute(sql_update_8)
        commit(curr)
        
        curr.execute(sql_update_9)
        commit(curr)
        
    sql_query  = 'SELECT asset_id, asset_name, terrain, constituent, country, region, formation, facility_type, status, operator, parent_company, basin, fiscal_model, first_production, peak_comm, first_peak_year, peak_prod,   '
    sql_query += 'peak_prod_unit, cutoff_year, resource_type, total_recov, liquid_recov_tot, natgas_recov_tot, total_recov_rem, liquid_recov_rem, natgas_recov_rem, npv_rem, npv_dev, irr_dev, capex_full, capex_rem, '
    sql_query += 'capex_boe_rem, opex_boe_rem, capex_opex_boe_rem, capex_boe_full, opex_boe_full, crude_bm, ng_bm, condensate_bm, lng_bm, ngls_bm, be_gas_rem, be_oil_rem, be_gas_dev, be_oil_dev, '
    sql_query += 'position, eur_total, pre_tax_irr, post_tax_irr, be_oil_post_tax, be_gas_post_tax, capex_well_boe, opex_well_boe, capex_well, opex_well, well_boe, working_interest, ip30_rate, rig_count, prev_rig_count, last_rig_year, well_life, new_wells, new_wells_rem,  '
    sql_query += 'drill_comp_days, project_stage, project_name, project_active_year, stage_change_quarter, epc_contractor, project_cost_mm_usd, pilot_test, curr_opex_boe, boed_prod, fid '
    sql_query += 'FROM econ_data WHERE run_id="{}" AND NOT `status` IN ("Discovered", "Stalled", "Suspended") AND NOT asset_name IS NULL AND NOT operator IS NULL '.format(run_id)
    sql_query += 'AND NOT parent_company IS NULL AND NOT (asset_name LIKE "Other %" OR asset_name LIKE "Others %") '

    if run_asset_id:
        sql_query += 'AND asset_id=%s ' % run_asset_id
    if run_country:
        sql_query += 'AND country="%s" ' % run_country
    if run_region:
        sql_query += ' AND region="%s" ' % run_region
    if asset_list:
        asset_str = ','.join([str(asset_id) for asset_id in asset_list])
        sql_query += 'AND asset_id IN (%s) ' % asset_str
    sql_query += 'ORDER BY asset_id '
    if debug: print sql_query
    curr.execute(sql_query)
    econ_data = curr.fetchall()
    return econ_data

def get_uncon_data(curr, asset_id, run_id):
    uncon_data = ()
    discount_year = get_discount_year()
    only_full_groupby ="SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));"
    curr.execute(only_full_groupby)
    sql_select = 'SELECT MAX(period), (IFNULL(production_count,100)/100) FROM wells WHERE datatype="Working Interest" AND asset_id={}'.format(asset_id)
    curr.execute(sql_select)
    working_interest = float(curr.fetchone()[1])

    sql_select = 'SELECT IFNULL(rigs,0) FROM uncon_data WHERE period={} AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    result = curr.fetchone()
    rig_count = round(float(result[0])*working_interest,1)
    try:
        sql_select = 'SELECT IFNULL(rigs,0) FROM uncon_data WHERE period={} AND asset_id={}'.format(discount_year-1, asset_id)
        curr.execute(sql_select)
        result = curr.fetchone()
        prev_rig_count = round(float(result[0])*working_interest,1)
    except:
        prev_rig_count = 0

    sql_select = 'SELECT IFNULL(MAX(period),{}), IFNULL(production_count,0) FROM wells WHERE datatype LIKE "Wells Drilling & Completion%" AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    drill_comp_days = float(curr.fetchone()[1])

    sql_select = 'SELECT IFNULL(well_life,0), IFNULL(rig_mobilization_days,0) FROM param_track WHERE asset_id={} AND session_key LIKE "%{}%"'.format(
        asset_id, run_id)
    curr.execute(sql_select)
    well_life, rig_mobile_days = curr.fetchone()
    drill_comp_days += rig_mobile_days

    sql_select = 'SELECT IFNULL(MAX(period),{}) FROM uncon_data WHERE rigs > 0 AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    last_rig_year = int(curr.fetchone()[0])

    sql_select = 'SELECT IFNULL(SUM(type_wells_added),0) FROM uncon_data WHERE period >= {} AND rigs > 0 AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    new_wells_rem = round(float(curr.fetchone()[0])*working_interest,0)

    sql_select = 'SELECT IFNULL(type_wells_added,0) FROM uncon_data WHERE period={} AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    new_wells = round(float(curr.fetchone()[0])*working_interest,0)

    ip30_rate = get_data('(IFNULL(ip30_oil_bd,0) + IFNULL(ip30_cond_bd,0) + IFNULL(ip30_NGLs_bd,0) + ((1000*IFNULL(ip30_gas_mmcfd,0))/6.0))', 'econ_data', cursor=curr, single_value=True, datatype='float', sql_where="asset_id={} AND run_id='{}'".format(asset_id, run_id))
    uncon_data = (rig_count, prev_rig_count, last_rig_year, well_life, new_wells, new_wells_rem, drill_comp_days, ip30_rate)
    return uncon_data


#Old code
# def update_uncon_data(curr, run_id):
#     print("Updating parameters(rig count , operators etc., ) for Unconventional assets in econ_data table")
#     curr.execute('UPDATE econ_data SET position=NULL')
#     commit(curr)
#     sql_select = 'SELECT asset_name FROM econ_data WHERE fiscal_model LIKE "%Resource%"'
#     curr.execute(sql_select)
#     uncon_asset_names = [data[0] for data in curr.fetchall()]
#     for asset_name in uncon_asset_names:
#         if '(' in asset_name:
#             position = asset_name.split('(')[0].strip()
#             sql_update = 'UPDATE econ_data SET position="{}" WHERE asset_name="{}" AND fiscal_model LIKE "%Resource%"'
#             curr.execute(sql_update.format(position, asset_name))
#             commit(curr)
#     sql_select = 'SELECT DISTINCT asset_id FROM econ_data WHERE run_id="{}" AND fiscal_model LIKE "%Resource%"'.format(run_id)
#     curr.execute(sql_select)
#     uncon_assets = [int(data[0]) for data in curr.fetchall()]
#     sql_update = 'UPDATE econ_data SET rig_count=%s, prev_rig_count=%s, last_rig_year=%s, well_life=%s, new_wells=%s, new_wells_rem=%s, drill_comp_days=%s, ip30_rate=%s WHERE asset_id=%s AND run_id=%s'
#     sql_update_2 = "UPDATE econ_data SET position='{}' WHERE asset_id={}"
#     for asset_id in uncon_assets:
#         rig_count, prev_rig_count, last_rig_year, well_life, new_wells, new_wells_rem, drill_comp_days, ip30_rate = get_uncon_data(curr, asset_id, run_id)
#         param_vals = (rig_count, prev_rig_count, last_rig_year, round(float(well_life),1), new_wells, new_wells_rem, round(float(drill_comp_days),1), ip30_rate, asset_id, run_id)
#         curr.execute(sql_update,param_vals)
#         commit(curr)
#         asset_name = get_data('asset_name', 'assets', cursor=curr, single_value=True, sql_where='asset_id={}'.format(asset_id))
#         position = asset_name
#         if ' (' in asset_name:
#             position = asset_name[:asset_name.index(' (')]
#         if ' unconventional' in position.lower():
#             position = position[:position.lower().index(' unconventional')]
#         curr.execute(sql_update_2.format(position, asset_id))
#         commit(curr)
#New code updated on 07-11-2025 by Sunil
def update_uncon_data(curr, run_id):
    try:
        curr.execute("use globaldata")
    except Exception as e:
        pass
    try:
        curr.execute("alter table econ_data drop index idx_econ_runid")
        conn.commit()
    except Exception as e:
        pass
    try:
        curr.execute("alter table econ_data drop index  idx_econ_assetname")
        conn.commit()
    except Exception as e:
        pass
    try:
        curr.execute("alter table econ_data drop index  idx_econ_assetid")
        conn.commit()
    except Exception as e:
        pass
    try:

        curr.execute('CREATE INDEX idx_econ_runid ON econ_data(run_id(20))')
        conn.commit()
    except Exception as e:
        pass
    try:
        curr.execute('CREATE INDEX idx_econ_assetname ON econ_data(asset_name(120))')
        conn.commit()
    except Exception as e:
        pass
    try:
        curr.execute('CREATE INDEX idx_econ_assetid ON econ_data(asset_id)')
        conn.commit()
    except Exception as e:
        pass

    print("Updating parameters (rig count, operators etc.) for Unconventional assets in econ_data table")

    # 1. Clear position values
    curr.execute('UPDATE econ_data SET position=NULL')
    # conn.commit()
    commit(curr)

    # 2. Bulk update for asset_name containing '('
    sql_select = 'SELECT asset_name FROM econ_data WHERE fiscal_model LIKE "%Resource%"'
    curr.execute(sql_select)
    uncon_asset_names = [data[0] for data in curr.fetchall()]

    position_updates = []
    for asset_name in uncon_asset_names:
        if '(' in asset_name:
            position = asset_name.split('(')[0].strip()
            position_updates.append((position, asset_name))

    if position_updates:
        curr.executemany(
            'UPDATE econ_data SET position=%s WHERE asset_name=%s AND fiscal_model LIKE "%%Resource%%"',
            position_updates
        )
        commit(curr)

    # 3. Get all unconventional assets
    sql_select = (
        'SELECT DISTINCT asset_id FROM econ_data '
        'WHERE run_id=%s AND fiscal_model LIKE "%%Resource%%"'
    )
    curr.execute(sql_select, (run_id,))
    uncon_assets = [int(data[0]) for data in curr.fetchall()]

    # 4. Prepare batch update data for rig/well parameters
    update_params = []
    position_updates2 = []

    for asset_id in uncon_assets:
        rig_count, prev_rig_count, last_rig_year, well_life, new_wells, new_wells_rem, drill_comp_days, ip30_rate = get_uncon_data(
            curr, asset_id, run_id)
        update_params.append((
            rig_count, prev_rig_count, last_rig_year,
            round(float(well_life), 1), new_wells, new_wells_rem,
            round(float(drill_comp_days), 1), ip30_rate,
            asset_id, run_id
        ))

        asset_name = get_data('asset_name', 'assets', cursor=curr, single_value=True,
                              sql_where='asset_id={}'.format(asset_id))
        position = asset_name
        if ' (' in asset_name:
            position = asset_name[:asset_name.index(' (')]
        if ' unconventional' in position.lower():
            position = position[:position.lower().index(' unconventional')]
        position_updates2.append((position, asset_id))

    # 5. Batch execute both updates
    sql_update = (
        'UPDATE econ_data SET rig_count=%s, prev_rig_count=%s, last_rig_year=%s, '
        'well_life=%s, new_wells=%s, new_wells_rem=%s, drill_comp_days=%s, '
        'ip30_rate=%s WHERE asset_id=%s AND run_id=%s'
    )

    curr.executemany(sql_update, update_params)
    commit(curr)

    curr.executemany('UPDATE econ_data SET position=%s WHERE asset_id=%s', position_updates2)
    commit(curr)

# def generate_output(curr, run_id, server, run_asset_id, run_country, run_region, asset_list,  export, clear_tbl, new_panorama, update_econ_data=False, update_first_peak=False, update_all_peak=False, debug=False):
#     total_output = ''
#     sql_where = 'run_id="{}" AND NOT `status` IN ("Discovered", "Stalled") AND NOT asset_name IS NULL AND NOT operator IS NULL AND NOT parent_company IS NULL AND NOT (asset_name LIKE "Other %" OR asset_name LIKE "Others %") '.format(run_id)
#     all_assets   = []
#     panorama_ids = []
#     if 1:
#         # sqlserv_conn = get_connection(server='sql_server', database='OGEngineDataExtract')
#         sqlserv_conn = get_connection(server='sql_server', database='OG_Effuah') #Comment this line and Uncomment above line after this run/Debug
#         sqlserv_curr = sqlserv_conn.cursor()
#         if clear_tbl and server == 'sql_server':  #Uncomment after Debug
#             sqlserv_curr.execute('TRUNCATE TABLE dbo.tblAutomatedPanorama')
#             sqlserv_curr.execute('COMMIT')
#         sqlserv_curr.execute('SELECT DISTINCT AssetID FROM dbo.tblAutomatedPanorama')
#         panorama_ids = [int(data[0]) for data in sqlserv_curr.fetchall()]
#     if run_asset_id and not int(run_asset_id) in panorama_ids:
#         all_assets = [int(run_asset_id)]
#     elif run_country:
#         sql_where += 'AND country="{}"'.format(run_country)
#         all_assets = [int(asset) for asset in get_assets(table='econ_data', sql_where=sql_where) if not asset in panorama_ids]
#     elif run_region:
#         sql_where += 'AND region="{}"'.format(run_region)
#         all_assets = [int(asset) for asset in get_assets(table='econ_data', sql_where=sql_where) if not asset in panorama_ids]
#     elif asset_list:
#         all_assets = [int(asset) for asset in asset_list if not asset in panorama_ids]
#     if debug: print 'all_assets: {}'.format(all_assets)
#     if update_first_peak: #Uncomment after debug
#         if update_all_peak:
#             assets = None
#         else:
#             assets = all_assets
#         update_peak_year(curr, run_id=run_id, asset_list=assets,  debug=debug)
#     print 'all_assets: {}'.format(all_assets)
#     # all_assets = ['921185','921186']
#     batch_data = []  # Temporary storage for batch updates
#     batch_size = 100  # Number of records to process in each batch
#     counter = 0
#     processed_count = 0
#     for assetid in all_assets:
#         # print('{}--econ_asset_id'.format(asset_id))
#         econ_data = get_econ_data(curr=curr, run_id=run_id, run_asset_id=assetid, update_econ_data=update_econ_data, debug=debug)
#         if debug:
#             print 'econ_data: {}'.format(econ_data)
#         # print 'econ_data: {}'.format(econ_data)
#         for asset_data in econ_data:
#             counter += 1
#             output = ''
#             asset_id,asset_name,terrain,constituent,country,region,formation,facility_type,status,operator,parent,basin,fiscal,first_prod,peak_comm,peak_year,peak_prod,peak_prod_unit,cutoff_year,resource_type,tot_res,tot_lqd_recov,tot_ng_recov,rem_res, \
#             rem_lqd_recov,rem_ng_recov,npv_rem,npv_dev,irr_dev,capex_full,capex_rem,capex_boe_rem,opex_boe_rem,capex_opex_boe_rem,capex_boe_full,opex_boe_full,crude_bm,ng_bm,cond_bm,lng_bm,ngls_bm,be_rem_gas,\
#             be_rem_oil,be_gas_dev,be_oil_dev,position,eur_total,pre_tax_irr,post_tax_irr,be_oil_post_tax,be_gas_post_tax,capex_well_boe,opex_well_boe,capex_well,opex_well,well_boe,working_interest,ip30_rate,rig_count,prev_rig_count,last_rig_year,well_life,new_wells,new_wells_rem,drill_comp_days, \
#             project_stage, project_name, project_active_year, stage_change_quarter, epc_contractor, project_cost, pilot_test, curr_opex_boe, boed_prod, fid = asset_data
#             print('{}-->econ_asset_id'.format(asset_id))
#             fiscal = fiscal[:-5]
#             print(fiscal) #Comment after Debug
#             if int(asset_id) in panorama_ids and server=='sql_server':
#                 pass
#             else:
#                 print ''
#                 # print 'asset_id: %s' % asset_id
#                 if debug:
#                     print 'asset_name: %s' % asset_name
#                 country_name = ''
#                 model_type = 'conventional'
#                 if country.lower() in ['congo republic', 'czech republic', 'democratic republic of the congo', 'falkand islands',
#                                        'netherlands', 'philippines', 'united arab emirates', 'united kingdom', 'united states']:
#                     country_name = 'the %s' % country
#                 else:
#                     country_name = country
#
#                 # Generate Unconventional Section
#                 if 'resource' in fiscal.lower():
#                     model_type = 'unconventional'
#
#                     uncon_asset_name = "{}'s {} position - {}".format(operator, position, asset_name)
#                     if new_panorama:
#                         output = uncon_section(curr, uncon_asset_name, asset_id, run_id, constituent, country, region, formation, position, terrain, resource_type, operator, rig_count, prev_rig_count, last_rig_year, capex_well_boe, opex_well_boe, well_life, new_wells, new_wells_rem, drill_comp_days, ip30_rate, eur_total, pre_tax_irr, be_rem_oil, be_rem_gas, capex_well, opex_well, well_boe, rem_res, rem_lqd_recov, rem_ng_recov, working_interest, boed_prod)
#                     else:
#                         output = uncon_section_(curr, asset_id, run_id, constituent, country, region, formation, position, terrain, resource_type, operator, rig_count, last_rig_year, capex_well_boe, opex_well_boe, well_life, new_wells, new_wells_rem, drill_comp_days, ip30_rate, eur_total, post_tax_irr, be_oil_post_tax, be_gas_post_tax)
#                 elif status.upper() in ['PLANNED', 'PRODUCING', 'ANNOUNCED'] and new_panorama:
#                     if status.upper() in ['PLANNED', 'ANNOUNCED']:
#                         output += announced_planned_panorama(asset_id, run_id, asset_name, tot_res, status, resource_type, terrain, country, operator, peak_prod_unit, rem_res, project_stage, project_name,
#                                                              project_active_year, stage_change_quarter, first_prod, peak_comm, peak_prod, peak_year, epc_contractor, rem_lqd_recov, rem_ng_recov, curr, be_rem_gas, be_rem_oil, be_gas_dev,
#                                                              be_oil_dev, crude_bm, ng_bm, cond_bm, lng_bm, irr_dev, project_cost, pilot_test, capex_boe_full, opex_boe_full, region, fid=fid, debug=debug)
#                     else:
#                         output += producing_panorama(asset_id, run_id, asset_name, tot_res, status, resource_type, terrain, country, operator, peak_prod_unit, rem_res, project_stage, project_name, project_active_year,
#                                                      stage_change_quarter, first_prod, peak_comm, peak_prod, peak_year, epc_contractor, opex_boe_full, curr, region, be_rem_gas, be_rem_oil, be_gas_dev, be_oil_dev, crude_bm, ng_bm, cond_bm,
#                                                      lng_bm, irr_dev, curr_opex_boe, fid=fid, debug=debug)
#                 else:
#                     # Generate Reserves Section
#                     output = reserves_section(output,asset_name,asset_id,run_id,region,status,terrain,country,country_name,operator,parent,basin,resource_type,tot_res,tot_lqd_recov,tot_ng_recov,
#                                               rem_res,rem_lqd_recov,rem_ng_recov,curr,facility_type,first_prod,peak_year,peak_prod, peak_prod_unit,cutoff_year,model_type,position)
#
#                     # Generate Economics Section
#                     output = economics_section(output,curr,asset_id,run_id,terrain,resource_type,country,country_name,region,status,asset_name,capex_full,capex_rem,capex_boe_rem,opex_boe_rem,capex_opex_boe_rem,
#                                                capex_boe_full,opex_boe_full,npv_rem,npv_dev,irr_dev,operator,model_type,position)
#
#                     # Generate Breakevens Section
#                     output = breakevens_section(output,asset_name,asset_id,run_id,terrain,resource_type,country,country_name,region,status,fiscal,be_rem_gas,be_rem_oil,be_gas_dev,be_oil_dev,crude_bm,ng_bm,
#                                                 cond_bm,lng_bm,ngls_bm,curr,operator,debug, model_type,position)
#
#                     # Generate Asset Section
#                     if model_type == 'conventional':
#                         output = asset_section(output,curr,asset_name,status,formation,country,country_name, model_type)
#
#                 if 0:
#                     print output
#                 # if server == 'sql_server':
#                 #     extracted_on = get_add_date()
#                 #     try:
#                 #         sqlserv_curr.execute('INSERT INTO dbo.tblAutomatedPanorama (AssetID, AssetName, ProjectOutlook, CreatedOn) VALUES (?, ?, ?, ?)', (asset_id, asset_name, output, extracted_on))
#                 #         sqlserv_curr.execute('COMMIT')
#                 #     except:
#                 #         pass
#                 # elif server == 'mysql' and export:
#                 #     curr.execute('INSERT INTO panorama_output (asset_id, asset_name, automated_panorama, run_id) VALUES (%s, %s, %s, %s)', (asset_id, asset_name, output, run_id))
#                 #     curr.execute('COMMIT')
#                 extracted_on = get_add_date()
#
#                 batch_data.append((asset_id, asset_name, output, extracted_on))
#                 # print(batch_data)
#                 # print counter
#                 if counter % batch_size == 0:
#                     print(counter)
#
#                     if server == 'sql_server':
#                         # extracted_on = get_add_date()
#                         try:
#                             sqlserv_curr.executemany(
#                                 'INSERT INTO dbo.tblAutomatedPanorama (AssetID, AssetName, ProjectOutlook, CreatedOn) VALUES (?, ?, ?, ?)',
#                                 batch_data)
#                             sqlserv_curr.execute('COMMIT')
#                             processed_count += counter
#                             print '{} assets were inserted into panoramas table'.format(processed_count)
#                             batch_data = []
#                         except Exception as e:
#                             print('Error updating database: {}'.format(e))
#                             pass
#                     # elif server == 'mysql' and export:
#                     #     curr.executemany('INSERT INTO panorama_output (asset_id, asset_name, automated_panorama, run_id) VALUES (%s, %s, %s, %s)', batch_data)
#                     #     curr.execute('COMMIT')
#                 elif counter > len(all_assets) - processed_count:
#                     try:
#                         sqlserv_curr.executemany(
#                             'INSERT INTO dbo.tblAutomatedPanorama (AssetID, AssetName, ProjectOutlook, CreatedOn) VALUES (?, ?, ?, ?)',
#                             batch_data)
#                         sqlserv_curr.execute('COMMIT')
#                         batch_data = []
#                     except Exception as e:
#                         print('Error updating database: {}'.format(e))
#                         pass
#         if server == 'sql_server' and export:
#             update_servers(dataset='panorama',export_tables=True,import_tables=True)
#     if 1:
#         sqlserv_curr.close()
#         sqlserv_conn.close()
#     return total_output
def generate_output(curr, run_id, server, run_asset_id, run_country, run_region,
                    asset_list, export, clear_tbl, new_panorama, update_econ_data=False,
                    update_first_peak=False, update_all_peak=False, debug=False):

    total_output = ''
    sql_where = (
        'run_id="{}" AND NOT `status` IN ("Discovered", "Stalled") '
        'AND NOT asset_name IS NULL AND NOT operator IS NULL '
        'AND NOT parent_company IS NULL '
        'AND NOT (asset_name LIKE "Other %%" OR asset_name LIKE "Others %%" )'
    ).format(run_id)

    all_assets = []
    panorama_ids = []
    batch_data = []
    batch_size = 100
    counter = 0
    processed_count = 0

    try:
        # ---------------------------------------------------------
        # CONNECT TO SQL SERVER
        # ---------------------------------------------------------
        sqlserv_conn = get_connection(server='sql_server', database='OGEngineDataExtract')
        # sqlserv_conn = get_connection(server='sql_server', database='OG_Effuah') #Change to previous database after Testing
        sqlserv_curr = sqlserv_conn.cursor()

        # logging.info("Connected to SQL Server.")
        if clear_tbl and server == 'sql_server':
            sqlserv_curr.execute('TRUNCATE TABLE dbo.tblAutomatedPanorama')
            sqlserv_curr.execute('COMMIT')
            print ("Cleared dbo.tblAutomatedPanorama table.")

        # Fetch existing Panorama IDs to skip already processed assets
        sqlserv_curr.execute('SELECT DISTINCT AssetID FROM dbo.tblAutomatedPanorama')
        panorama_ids = [int(row[0]) for row in sqlserv_curr.fetchall()]
        # logging.info("Fetched %s existing panorama IDs.", len(panorama_ids))

        # ---------------------------------------------------------
        # DETERMINE WHICH ASSETS TO PROCESS
        # ---------------------------------------------------------
        if run_asset_id and not int(run_asset_id) in panorama_ids:
            all_assets = [int(run_asset_id)]
        elif run_country:
            sql_where += ' AND country="{}"'.format(run_country)
            all_assets = [
                int(asset) for asset in get_assets(table='econ_data', sql_where=sql_where)
                if asset not in panorama_ids
            ]
        elif run_region:
            sql_where += ' AND region="{}"'.format(run_region)
            all_assets = [
                int(asset) for asset in get_assets(table='econ_data', sql_where=sql_where)
                if asset not in panorama_ids
            ]
        elif asset_list:
            all_assets = [
                int(asset) for asset in asset_list if asset not in panorama_ids
            ]

        print 'Total assets to process: {}'.format(len(all_assets))
        # logging.info("Total assets to process: %s", len(all_assets))

        # ---------------------------------------------------------
        # OPTIONAL PEAK YEAR UPDATES
        # ---------------------------------------------------------
        if update_first_peak:
            assets = None if update_all_peak else all_assets
            update_peak_year(curr, run_id=run_id, asset_list=assets, debug=debug)
            print ("Peak year updated for assets.")

        # ---------------------------------------------------------
        # MAIN ASSET PROCESSING LOOP
        # ---------------------------------------------------------
        for asset_id in all_assets:
            # try:
            econ_data = get_econ_data(
                curr=curr,
                run_id=run_id,
                run_asset_id=asset_id,
                update_econ_data=update_econ_data,
                debug=debug
            )

            if not econ_data:
                print ("No econ data found for asset %s", asset_id)
                continue

            for asset_data in econ_data:
                counter += 1
                output = ''
                (
                    asset_id, asset_name, terrain, constituent, country, region,
                    formation, facility_type, status, operator, parent, basin,
                    fiscal, first_prod, peak_comm, peak_year, peak_prod,
                    peak_prod_unit, cutoff_year, resource_type, tot_res,
                    tot_lqd_recov, tot_ng_recov, rem_res, rem_lqd_recov,
                    rem_ng_recov, npv_rem, npv_dev, irr_dev, capex_full,
                    capex_rem, capex_boe_rem, opex_boe_rem, capex_opex_boe_rem,
                    capex_boe_full, opex_boe_full, crude_bm, ng_bm, cond_bm,
                    lng_bm, ngls_bm, be_rem_gas, be_rem_oil, be_gas_dev,
                    be_oil_dev, position, eur_total, pre_tax_irr, post_tax_irr,
                    be_oil_post_tax, be_gas_post_tax, capex_well_boe,
                    opex_well_boe, capex_well, opex_well, well_boe,
                    working_interest, ip30_rate, rig_count, prev_rig_count,
                    last_rig_year, well_life, new_wells, new_wells_rem,
                    drill_comp_days, project_stage, project_name,
                    project_active_year, stage_change_quarter, epc_contractor,
                    project_cost, pilot_test, curr_opex_boe, boed_prod, fid
                ) = asset_data

                if not fiscal:
                    continue
                fiscal = fiscal[:-5]

                # skip if already processed
                if int(asset_id) in panorama_ids and server == 'sql_server':
                    continue

                country_name = (
                    'the %s' % country
                    if country.lower() in [
                        'congo republic', 'czech republic', 'democratic republic of the congo',
                        'falkand islands', 'netherlands', 'philippines',
                        'united arab emirates', 'united kingdom', 'united states'
                    ]
                    else country
                )

                model_type = 'conventional'
                # ---------------------------------------------------------
                # Unconventional Assets
                # ---------------------------------------------------------
                if 'resource' in fiscal.lower():
                    model_type = 'unconventional'
                    uncon_asset_name = "{}'s {} position - {}".format(operator, position, asset_name)
                    if new_panorama:
                        output = uncon_section(
                            curr, uncon_asset_name, asset_id, run_id, constituent, country,
                            region, formation, position, terrain, resource_type, operator,
                            rig_count, prev_rig_count, last_rig_year, capex_well_boe,
                            opex_well_boe, well_life, new_wells, new_wells_rem,
                            drill_comp_days, ip30_rate, eur_total, pre_tax_irr, be_rem_oil,
                            be_rem_gas, capex_well, opex_well, well_boe, rem_res,
                            rem_lqd_recov, rem_ng_recov, working_interest, boed_prod
                        )
                    else:
                        output = uncon_section_(
                            curr, asset_id, run_id, constituent, country, region,
                            formation, position, terrain, resource_type, operator,
                            rig_count, last_rig_year, capex_well_boe, opex_well_boe,
                            well_life, new_wells, new_wells_rem, drill_comp_days,
                            ip30_rate, eur_total, post_tax_irr, be_oil_post_tax,
                            be_gas_post_tax
                        )

                # ---------------------------------------------------------
                # Panorama (Planned / Producing / Announced)
                # ---------------------------------------------------------
                elif status.upper() in ['PLANNED', 'PRODUCING', 'ANNOUNCED'] and new_panorama:
                    if status.upper() in ['PLANNED', 'ANNOUNCED']:
                        output += announced_planned_panorama(
                            asset_id, run_id, asset_name, tot_res, status, resource_type,
                            terrain, country, operator, peak_prod_unit, rem_res,
                            project_stage, project_name, project_active_year,
                            stage_change_quarter, first_prod, peak_comm, peak_prod,
                            peak_year, epc_contractor, rem_lqd_recov, rem_ng_recov,
                            curr, be_rem_gas, be_rem_oil, be_gas_dev, be_oil_dev,
                            crude_bm, ng_bm, cond_bm, lng_bm, irr_dev, project_cost,
                            pilot_test, capex_boe_full, opex_boe_full, region,
                            fid=fid, debug=debug
                        )
                    else:
                        output += producing_panorama(
                            asset_id, run_id, asset_name, tot_res, status, resource_type,
                            terrain, country, operator, peak_prod_unit, rem_res,
                            project_stage, project_name, project_active_year,
                            stage_change_quarter, first_prod, peak_comm, peak_prod,
                            peak_year, epc_contractor, opex_boe_full, curr, region,
                            be_rem_gas, be_rem_oil, be_gas_dev, be_oil_dev, crude_bm,
                            ng_bm, cond_bm, lng_bm, irr_dev, curr_opex_boe,
                            fid=fid, debug=debug
                        )

                # ---------------------------------------------------------
                # Conventional Assets
                # ---------------------------------------------------------
                else:
                    output = reserves_section(
                        output, asset_name, asset_id, run_id, region, status, terrain,
                        country, country_name, operator, parent, basin, resource_type,
                        tot_res, tot_lqd_recov, tot_ng_recov, rem_res, rem_lqd_recov,
                        rem_ng_recov, curr, facility_type, first_prod, peak_year,
                        peak_prod, peak_prod_unit, cutoff_year, model_type, position
                    )

                    output = economics_section(
                        output, curr, asset_id, run_id, terrain, resource_type, country,
                        country_name, region, status, asset_name, capex_full, capex_rem,
                        capex_boe_rem, opex_boe_rem, capex_opex_boe_rem, capex_boe_full,
                        opex_boe_full, npv_rem, npv_dev, irr_dev, operator, model_type,
                        position
                    )

                    output = breakevens_section(
                        output, asset_name, asset_id, run_id, terrain, resource_type,
                        country, country_name, region, status, fiscal, be_rem_gas,
                        be_rem_oil, be_gas_dev, be_oil_dev, crude_bm, ng_bm, cond_bm,
                        lng_bm, ngls_bm, curr, operator, debug, model_type, position
                    )

                    if model_type == 'conventional':
                        output = asset_section(
                            output, curr, asset_name, status, formation, country,
                            country_name, model_type
                        )

                # now = datetime.now()
                # extracted_on=now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                batch_data.append((asset_id, asset_name, output))

                # ---------------------------------------------------------
                # BATCH INSERTION
                # ---------------------------------------------------------
                if len(batch_data) >= batch_size:
                    # cleaned_batch_data = []
                    #
                    # for row in batch_data:
                    #     row_list = list(row)
                    #     # Check if the 4th item (index 3) is a datetime object
                    #     if isinstance(row_list[3], datetime):
                    #         dt_obj = row_list[3]
                    #         # Format time manually to maintain strict SQL-supported 3-digit milliseconds
                    #         base_time = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
                    #         ms_val = int(dt_obj.microsecond / 1000)
                    #         row_list[3] = "%s.%03d" % (base_time, ms_val)
                    #
                    #     cleaned_batch_data.append(tuple(row_list))
                    # batch_data=cleaned_batch_data
                    # try:
                    # sqlserv_curr.executemany(
                    #     'INSERT INTO dbo.tblAutomatedPanorama (AssetID, AssetName, ProjectOutlook, CreatedOn) VALUES (?, ?, ?, ?)',
                    #     batch_data
                    # )
                    #removed Date issue which is having accuracy upto milliseconds by implementing sql native getdate()
                    sqlserv_curr.executemany(
                        'INSERT INTO dbo.tblAutomatedPanorama (AssetID, AssetName, ProjectOutlook, CreatedOn) VALUES (?, ?, ?, GETDATE())',
                        batch_data
                    )
                    sqlserv_curr.execute('COMMIT')
                    processed_count += len(batch_data)
                    print '{} panoramas inserted...'.format(processed_count)
                    # logging.info("%s panoramas inserted.", processed_count)
                    batch_data = []
                    # except Exception as e:
                    #     print "Batch insert error: %s", str(e)
                    #     # traceback.print_exc()
                    #     batch_data = []

            # except Exception as e:
            #     print ("Error processing asset %s: %s", asset_id, str(e))
                # traceback.print_exc()

        # ---------------------------------------------------------
        # FINAL BATCH INSERT (if any)
        # ---------------------------------------------------------
        if batch_data:
            try:
                sqlserv_curr.executemany(
                    'INSERT INTO dbo.tblAutomatedPanorama (AssetID, AssetName, ProjectOutlook, CreatedOn) VALUES (?, ?, ?, ?)',
                    batch_data
                )
                sqlserv_curr.execute('COMMIT')
                processed_count += len(batch_data)
                print 'Final batch inserted: {} assets'.format(len(batch_data))
                # logging.info('Final batch inserted: %s assets.', len(batch_data))
            except Exception as e:
                print "Final batch insert failed: %s", str(e)
                # traceback.print_exc()

        if server == 'sql_server' and export:
            update_servers(dataset='panorama', export_tables=True, import_tables=True)
            # logging.info("Server data synchronized.")

    # except Exception as e:
    #     print "Critical error in generate_output: %s", str(e)
        # traceback.print_exc()
    finally:
        try:
            sqlserv_curr.close()
            sqlserv_conn.close()
        except:
            pass
        # logging.info("SQL Server connection closed.")

    print "Processing completed. Total processed: %s", processed_count
    return total_output
def generate_rank_sections(output_file=None, run_asset_id=None, run_country=None, run_region=None, asset_list=None, run_id='', server='mysql', export=False,
                           clear_tbl=False, uncon=True, new_panorama=NEW_PANORAMA, update_econ_data=True,  update_first_peak=True, update_all_peak=True, debug=False):
    total_output = ''
    conn = get_connection()
    curr = conn.cursor()

    # Get id from last engine run
    if run_id:
        run_id = run_id
    else:
        run_id = get_run_id(curr)
        # run_id = '20241021_164427' #comment after debug

    # Update uncon data stored in econ_data table
    if uncon: #uncomment If condition after Debug
        update_uncon_data(curr, run_id) #uncomment If condition after Debug

    # Get economic data and store in variable
    if run_asset_id or run_country or run_region or asset_list:
        econ_data = get_econ_data(curr, run_id, run_asset_id, run_country, run_region, asset_list)

        # Generate comparison sections with rankings

        #total_output = generate_output(econ_data, curr, run_id, server, export, clear_tbl, debug)
        total_output = generate_output(curr, run_id, server, run_asset_id, run_country, run_region, asset_list,  export, clear_tbl, new_panorama=new_panorama,
                                       update_econ_data=update_econ_data, update_first_peak=update_first_peak, update_all_peak=update_all_peak, debug=debug)

        # If output file is provided then save output to file
        #save_output(output_file, total_output)

    curr.close()
    conn.close()
    return total_output



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__=='__main__':
    #run_id = '20180418_205149'
    #uncon_assets = get_assets('econ_data', 'run_id="{}" AND fiscal_model LIKE "%Resource Play%"'.format(run_id))
    #generate_rank_sections(run_id=run_id, asset_list=[], run_asset_id=851345, uncon=True)
    asset_list = [
        128736,
        133573,
        133757,
        134036,
        134275,
        134482,
        134579,
        134775,
        135306,
        135380,
        135453,
        135735,
        135740,
        135836,
        135890,
        136141,
        136143,
        136150,
        136302,
        136453,
        136456,
        136497,
        136526,
        206594,
        206629,
        207516,
        208318,
        208510,
        208706,
        208709,
        208844,
        216488,
        225620,
        237713,
        249439,
        249454,
        252419,
        254182,
        254332,
        254783,
        256359,
        257273,
        257277,
        257281,
        257292,
        257857,
        257859,
        257859,
        258042,
        258850,
        261269,
        261518,
        270751,
        270751,
        270758,
        270758,
        271206,
        271207,
        276115,
        318890,
        319234,
        319407,
        319410,
        319410,
        320689,
        322242,
        322258,
        325912,
        362119,
        366001,
        368460,
        376812,
        381101,
        381104,
        382000,
        382243,
        386944,
        389037,
        393764,
        398228,
        398588,
        408604,
        410410,
        414585,
        465627,
        465677,
        501927,
        523059,
        523128,
        523129,
        526648,
        530017,
        533577,
        533595,
        534962,
        562859,
        568894,
        573034,
        578342,
        578350,
        624008,
        624731,
        624922,
        625183,
        625227,
        625349,
        625424,
        625955,
        629225,
        630913,
        630986,
        630986,
        642228,
        642383,
        642392,
        642667,
        642901,
        642994,
        643242,
        649871,
        681132,
        681407,
        720893,
        728719,
        729113,
        729204,
        729726,
        729783,
        733255,
        734667,
        734818,
        734856,
        734861,
        734933,
        736791,
        737335,
        737759,
        738398,
        738784,
        739048,
        741139,
        741140,
        741284,
        741514,
        741899,
        742235,
        746674,
        747987,
        778963,
        779247,
        779360,
        779369,
        819370,
        844794,
        844847,
        844917,
        845734,
        845735,
        845792,
        845933,
        846664,
        847327,
        848548,
        848548,
        851186,
        851188,
        858141,
        863946,
        864531,
        866914,
        867336,
        867536,
        867932,
        878958,
        879673,
        879844,
        880569,
        880820,
        896341,
        897102,
        907222,
        907421,
        907650,
        909754,
        909895,
        911185,
        911203,
        911531,
        911773,
        913255,
        917853,
        917969,
        917991,
        918839,
        918870,
        919017,
        920771,
        921349,
        921518,
        922482,
        922548,
        925166,
        926368,
        940713,
        940734,
        959686,
        961145,
        999339,
        999361,
        1010674,
        1010688,
        1010908,
        1010974,
        1012662,
        1012802,
        1016255,
        1016258,
        1016260,
        1026034,
        1026739,
        1026742,
        1027161,
        1027436,
        1027862,
        1032166,
        1032362,
        1032841,
        1033253,
        1033555,
        1034193,
        1034988,
        1037084,
        1037307,
        1037371,
        1038091,
        1038877,
        1039606,
        1039753,
        1230678,
        1279531,
        1279817,
        1479808,
        1499651,
        1503984,
        1503985,
        1504407,
        1508552,
        1512073,
        1521765,
        1543610,
        1557345,
        1562214,
        1605455,
        1605456,
        1610758,
        1622747,
        1622751,
        1624399,
        1629594,
        1633283,
        1633284,
        1643934,
        1652648
    ]
    # run_id = "20201015_100139"
    print generate_rank_sections(run_id=run_id, server='sql_server', asset_list=asset_list, clear_tbl=False, debug=False, uncon=False, export=False, update_econ_data=False, update_first_peak=True, update_all_peak=True)
    #print generate_rank_sections(run_id='20200624_180145', server='sql_server', run_region='Middle East', debug=False, uncon=False, export=False, update_econ_data=True, clear_tbl=True)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
