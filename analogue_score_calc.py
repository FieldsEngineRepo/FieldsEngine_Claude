from discovered_analogues import *


def get_max_points(score_type, param):
    param_max = 0
    score_dict = eval(score_type.upper()+'_SCORES')
    if param in PERCENTAGE_SCORES:
        if param in ['pipeline', 'gas_processing', 'oil_storage', 'gas_storage']:
            param_max = 75
        else:
            param_max = max(score_dict[param]['points'])
    elif param in OPTION_SCORES:
        param_max = max([score_dict[param][param_option]['points'] for param_option in score_dict[param].keys()])
    else:
        param_max = score_dict[param]['points']
    return param_max

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def calc_max_asset_scores(curr, sql_insert, score_types=[], in_place=False):
    for score_type in score_types:
        print 'score_type:', score_type
        for asset_data in get_asset_data(curr, score_type, in_place):
            if score_type == 'prod':
                api_gravity, terrain, ablock, basin, country, region, status, resource_type, formation, form_rock_type, trap_type, asset_id = asset_data
                facility_type, pipeline, gas_processing, oil_storage, gas_storage = (None, None, None, None, None)
            elif score_type == 'cost':
                api_gravity, terrain, ablock, basin, country, region, status, resource_type, facility_type, pipeline, gas_processing, oil_storage, gas_storage, asset_id = asset_data
                formation, form_rock_type, trap_type = (None, None, None)
            max_scores = ()
            #print asset_id
            for param_name in [param for param in PARAMS['all'] if param != 'reserve_volume']:
                if eval(param_name) in [None, 'NULL']:
                    max_scores += (0,)
                else:
                    max_scores += (get_max_points(score_type, param_name),)
            max_scores += (300,)
            max_score = sum(max_scores)
            param_vals = (asset_id, score_type, max_score) + max_scores
            #print sql_insert,sql_insert.count('%s'),param_vals,len(param_vals)
            curr.execute(sql_insert, param_vals)
        curr.execute('COMMIT')


def calc_max_field_scores(curr, sql_insert, score_types=[], in_place=False):
    discovered_fields = get_discovered_fields(with_reserves=False)
    for field in discovered_fields:
        for score_type in score_types:
            asset_data = get_field_data(curr, field, score_type, in_place)
            #print 'asset_data (calc_max_field_scores):', asset_data
            if score_type == 'prod':
                api_gravity, terrain, ablock, basin, country, region, status, resource_type, formation, form_rock_type, trap_type = asset_data
                facility_type, pipeline, gas_processing, oil_storage, gas_storage = (None, None, None, None, None)
            elif score_type == 'cost':
                api_gravity, terrain, ablock, basin, country, region, status, resource_type, facility_type, pipeline, gas_processing, oil_storage, gas_storage = asset_data
                formation, form_rock_type, trap_type = (None, None, None)
            max_scores = ()
            #print field
            for param_name in [param for param in PARAMS['all'] if param != 'reserve_volume']:
                if eval(param_name) in [None, 'NULL']:
                    max_scores += (0,)
                else:
                    max_scores += (get_max_points(score_type, param_name),)
            max_scores += (300,)
            max_score = sum(max_scores)
            param_vals = (field, score_type, max_score) + max_scores
            curr.execute(sql_insert, param_vals)
        curr.execute('COMMIT')

def analogue_score_calc():
    conn = get_connection()
    curr = conn.cursor()
    score_types = ['prod', 'cost']

    in_place = False

    field_list = ['asset_id', 'score_type', 'max_score'] + PARAMS['all']

    field_name_str = ','.join(field_list)
    field_var_str = ','.join(['%s']*len(field_list))
    curr.execute('TRUNCATE analogue_scores')
    curr.execute('COMMIT')
    sql_insert = 'INSERT INTO analogue_scores (%s) VALUES (%s)' % (field_name_str, field_var_str)

    calc_max_asset_scores(curr, sql_insert, score_types, in_place)
    calc_max_field_scores(curr, sql_insert, score_types, in_place)

    curr.close()
    conn.close()


if __name__=='__main__':
    analogue_score_calc()
