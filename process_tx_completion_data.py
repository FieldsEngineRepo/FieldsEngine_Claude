from zipfile import ZipFile
import os
import pymysql
import pypyodbc

'''
File Structure:

tx_data\\
	- tx_completion_data\\
		- tx_completion_files\\
		- tx_completion_zipfiles\\
'''

TX_DATA_DIR = "D:\\GlobalData\\Data\\tx_data\\"
TX_COMP_DIR = TX_DATA_DIR + 'tx_completion_data\\'
COMP_ZIP_DIR = TX_COMP_DIR + 'tx_completion_zipfiles\\'
COMP_OUT_DIR = TX_COMP_DIR + 'tx_completion_files\\'

COMP_REC_CODE = {
	'PACKET'                      : 'texas_comp_Packet_Data',
	'PACKET_WORKOVER'             : 'texas_comp_Reclass_Data',
	'G-1'                         : 'texas_comp_G1_Data',
	'G-1 Measurement Data'        : 'texas_comp_Gas_Measurement_Data',
	'G-1 Field Data'              : 'texas_comp_G1_Field_Data',
	'G-1 Amount And Material Data': 'texas_comp_Material_Used_Data',
	'G-1 Multiple Completion Data': 'texas_comp_Multiple_Completion_Data',
	'G-1 Multi-Completion Data'   : 'texas_comp_Multiple_Completion_Data',
	'G-1 Liner Data'              : 'texas_comp_Liner_Data',
	'G-1 Casing Data'             : 'texas_comp_Casing_Data',
	'G-1 Production Interval Data': 'texas_comp_Production_Interval_Data',
	'G-1 Tubing Data'             : 'texas_comp_Tubing_Data',
	'G-1 Formation Data'          : 'texas_comp_Formation_Data',
	'W-2'                         : 'texas_comp_W2_Data',
	'W-2 Amount And Material Data': 'texas_comp_Material_Used_Data',
	'W-2 Multiple Completion Data': 'texas_comp_Multiple_Completion_Data',
	'W-2 Multi-Completion Data'   : 'texas_comp_Multiple_Completion_Data',
	'W-2 Liner Data'              : 'texas_comp_Liner_Data',
	'W-2 Casing Data'             : 'texas_comp_Casing_Data',
	'W-2 Production Interval Data': 'texas_comp_Production_Interval_Data',
	'W-2 Tubing Data'             : 'texas_comp_Tubing_Data',
	'W-2 Formation Data'          : 'texas_comp_Formation_Data',
	'P-4'                         : 'texas_comp_P4_Data',
	'P-4 Gas Gatherer Data'       : 'texas_comp_P4_Gas_Gatherer_Data',
	'P-4 Oil Gatherer Data'       : 'texas_comp_P4_Oil_Gatherer_Data',
	'L-1'                         : 'texas_comp_L1_Data',
	'P-15'                        : 'texas_comp_P15_Data',
	'G-5'                         : 'texas_comp_G5_Data',
	'G-10'                        : 'texas_comp_G10_Data',
	'W-12'                        : 'texas_comp_W12_Data'
}

COMP_COL_COUNT = {
	'texas_comp_casing_data'             : 19,
	'texas_comp_formation_data'          : 12,
	'texas_comp_g10_data'                : 21,
	'texas_comp_g1_data'                 : 90,
	'texas_comp_g1_field_data'           : 10,
	'texas_comp_g5_data'                 : 40,
	'texas_comp_gas_measurement_data'    : 16,
	'texas_comp_l1_data'                 : 19,
	'texas_comp_liner_data'              : 16,
	'texas_comp_material_used_data'      : 10,
	'texas_comp_multiple_completion_data': 10,
	'texas_comp_p15_data'                : 8,
	'texas_comp_p4_data'                 : 14,
	'texas_comp_p4_gas_gatherer_data'    : 14,
	'texas_comp_p4_oil_gatherer_data'    : 10,
	'texas_comp_packet_data'             : 62,
	'texas_comp_production_interval_data': 11,
	'texas_comp_reclass_data'            : 12,
	'texas_comp_tubing_data'             : 10,
	'texas_comp_w12_data'                : 15,
	'texas_comp_w2_data'                 : 84
}

TX_COMP_COLS = {
	'texas_comp_casing_data'             : [
		'[casing_data]',
		'[tracking_no]',
		'[packet_id]',
		'[g1_id_w2_id]',
		'[row_no]',
		'[casing_size]',
		'[weight_lb_per_foot]',
		'[weight_lb_per_foot2]',
		'[depth_set]',
		'[multistage_tool_depth]',
		'[type_of_cement]',
		'[amount_of_cement]',
		'[hole_size]',
		'[top_of_cement]',
		'[slurry_volume]',
		'[casing_type_code]',
		'[multi_stage_shoe_depth]',
		'[top_cement_determine_code]',
		'[process_code]'
	],
	'texas_comp_formation_data'          : [
		'[formation_data]',
		'[tracking_no]',
		'[packet_id]',
		'[w2_id_g1_id]',
		'[row_no]',
		'[formation]',
		'[depth]',
		'[depth_tmd]',
		'[user_encountered]',
		'[user_remark]',
		'[user_isolated]',
		'[process_code]'
	],
	'texas_comp_g10_data'                : [
		'[g_10]',
		'[tracking_no]',
		'[packet_id]',
		'[g10_id]',
		'[reason_code]',
		'[due_dt]',
		'[effective_dt]',
		'[cond_produced]',
		'[cond_gravity]',
		'[water_produced]',
		'[xbhole_pressure]',
		'[form_certification]',
		'[date_tested]',
		'[tester_name]',
		'[tester_company]',
		'[gas_prod_during_test]',
		'[gravity_dry_gas]',
		'[siwh_pressure]',
		'[flowing_pressure]',
		'[tester_phone]',
		'[process_code]'
	],
	'texas_comp_g1_data'                 : [
		'[g_1]',
		'[tracking_no]',
		'[packet_id]',
		'[g1_id]',
		'[date_of_test]',
		'[test_gas_production]',
		'[is_dry_gas_well]',
		'[gravity_dry_gas]',
		'[gas_hydro_ratio]',
		'[avg_shutin_temp]',
		'[gravity_hydrocarbon]',
		'[gravity_of_mixture]',
		'[bottom_hole_temp]',
		'[bottom_hole_depth]',
		'[notice_of_intention]',
		'[number_of_producing_wells]',
		'[acres_in_lease]',
		'[work_commenced_dt]',
		'[work_completed_dt]',
		'[distance_to_nearest_well]',
		'[distance_to_bndry_a]',
		'[direction_to_bnday_a_code]',
		'[distance_to_bndry_b]',
		'[direction_to_bndry_b_code]',
		'[boundary_lease_name]',
		'[elevation]',
		'[elevation_code]',
		'[was_direct_survey_made]',
		'[top_of_pay]',
		'[measured_depth]',
		'[vertical_depth]',
		'[plug_back_depth]',
		'[casing_detr_field_rules]',
		'[casing_detr_recommend_dt]',
		'[casing_detr_rrc_dt]',
		'[drilling_contractor_nm]',
		'[is_multiple_completion]',
		'[did_preflow_48_hours]',
		'[pipeline_connection]',
		'[any_condensate]',
		'[remarks]',
		'[intervals_drilled_by_code]',
		'[section_one_remarks]',
		'[cementing_affidavit_attached]',
		'[amount_material_remarks]',
		'[form_certification]',
		'[tester_name]',
		'[tester_company]',
		'[intervals_drilled_by_other]',
		'[prod_intv_remark]',
		'[tester_phone]',
		'[op_is_tester]',
		'[gmm_orifice_meter]',
		'[gmm_flange_taps]',
		'[gmm_pos_choke]',
		'[gmm_pipe_taps]',
		'[gmm_orifice_vent]',
		'[gmm_pitot_tube]',
		'[gmm_critical_flow]',
		'[bottom_hole_press]',
		'[is_unperforated_cmpl]',
		'[plug_back_depth_tmd]',
		'[top_of_pay_tmd]',
		'[off_lease]',
		'[commingled]',
		'[interval_hydrogen_sulfide]',
		'[hydraulic_fracking_used]',
		'[has_fracking_disclosure]',
		'[tubing_rec_remarks]',
		'[surface_casing_rotation_time]',
		'[casing_detr_recommend_depth]',
		'[casing_detr_swr_13_depth]',
		'[is_actuation_valve_on_well]',
		'[prod_case_psig_bef_frack_treat]',
		'[hydraulic_fracking_max_psig]',
		'[casing_detr_swr_13_excep]',
		'[casing_detr_recommend_gau_gpd]',
		'[actuation_valve_on_well_psig]',
		'[gmm_mass_flow_meter]',
		'[gmm_other]',
		'[measurement_data_row_cnt]',
		'[amount_and_material_row_cnt]',
		'[field_data_row_cnt]',
		'[multi_cmpl_row_count]',
		'[casing_data_row_count]',
		'[liner_data_row_count]',
		'[tubing_data_row_count]',
		'[prod_intrvl_data_row_cnt]',
		'[formation_data_row_cnt]',
		'[process_code]'
	],
	'texas_comp_g1_field_data'           : [
		'[field_data]',
		'[tracking_no]',
		'[packet_id]',
		'[g1_id]',
		'[row_no]',
		'[time_of_run]',
		'[choke_size]',
		'[wellhead_press]',
		'[wellhead_flow_temp]',
		'[process_code]'
	],
	'texas_comp_g5_data'                 : [
		'[g_5]',
		'[tracking_no]',
		'[packet_id]',
		'[g5_id]',
		'[oil_cond_volume]',
		'[water_volume]',
		'[casing_pressure]',
		'[sep_op_pressure]',
		'[color_liquid_code]',
		'[gravity_sep_liquid]',
		'[gravity_stk_liquid]',
		'[liquid_sample_dt]',
		'[where_obtained_code]',
		'[initial_boiling_temp]',
		'[over_10p_temp]',
		'[over_20p_temp]',
		'[over_30p_temp]',
		'[over_40p_temp]',
		'[over_50p_temp]',
		'[over_60p_temp]',
		'[over_70p_temp]',
		'[over_80p_temp]',
		'[over_90p_temp]',
		'[over_95p_temp]',
		'[end_point_temp]',
		'[total_recovery]',
		'[residue]',
		'[loss]',
		'[date_of_test_dt]',
		'[gas_volume]',
		'[gas_hydro_ratio]',
		'[flowing_tubing_pressure]',
		'[choke_size]',
		'[si_wellhead_pressure]',
		'[specific_gravity]',
		'[pipeline_connection]',
		'[form_certification]',
		'[packet_purpose_of_filing]',
		'[pvt]',
		'[process_code]'
	],
	'texas_comp_gas_measurement_data'    : [
		'[measurement_data]',
		'[tracking_no]',
		'[packet_id]',
		'[g1_id]',
		'[row number]',
		'[line_size]',
		'[orifice_choke_size]',
		'[twentyfour_hour_coeff]',
		'[static_choke_press]',
		'[diff]',
		'[flow_temp]',
		'[temp_factor]',
		'[gravity_factor]',
		'[compress_factor]',
		'[volume]',
		'[process_code]'
	],
	'texas_comp_l1_data'                 : [
		'[l_1]',
		'[tracking_no]',
		'[packet_id]',
		'[l1_id]',
		'[electric_log_not_run]',
		'[electric_log_run]',
		'[confidentiality_requested]',
		'[confidentiality_already_granted]',
		'[log_on_file]',
		'[log_attached_to]',
		'[to_form_l1]',
		'[to_form_p7]',
		'[to_form_w4]',
		'[company_lease_name]',
		'[log_was_held_confidential]',
		'[lease_numbers]',
		'[well_numbers]',
		'[form_certification]',
		'[process_code]'
	],
	'texas_comp_liner_data'              : [
		'[liner_data]',
		'[tracking_no]',
		'[packet_id]',
		'[g1_id]',
		'[row_no]',
		'[size]',
		'[top]',
		'[bottom]',
		'[sacks_of_cement]',
		'[screen]',
		'[hole_size]',
		'[type_of_cement]',
		'[slurry_volume]',
		'[top_cement_determine_code]',
		'[top_of_cement]',
		'[process_code]'
	],
	'texas_comp_material_used_data'      : [
		'[material_data]',
		'[tracking_no]',
		'[packet_id]',
		'[comm_id]',
		'[row_no]',
		'[from]',
		'[to]',
		'[material_used]',
		'[amt_material_process_code]',
		'[process_code]'
	],
	'texas_comp_multiple_completion_data': [
		'[multi_completion_data]',
		'[tracking_no]',
		'[packet_id]',
		'[g1_id or w2_id]',
		'[row_no]',
		'[field_reservoir]',
		'[lease_no]',
		'[well_type]',
		'[well_no]',
		'[process_code]'
	],
	'texas_comp_p15_data'                : [
		'[p_15]',
		'[tracking_no]',
		'[packet_id]',
		'[p15_id]',
		'[operator_certification]',
		'[form_certification]',
		'[plat_acres]',
		'[process_code]'
	],
	'texas_comp_p4_data'                 : [
		'[p_4]',
		'[tracking_no]',
		'[packet_id]',
		'[p4_id]',
		'[classification]',
		'[filing_due_to_code]',
		'[operator_certification]',
		'[effective_dt]',
		'[temp_abandoned]',
		'[unperforated_not_completed]',
		'[service_well]',
		'[gas_gatherer_row_cnt]',
		'[oil_gatherer_row_cnt]',
		'[process_code]'
	],
	'texas_comp_p4_gas_gatherer_data'    : [
		'[gas_gatherer_data]',
		'[tracking_no]',
		'[packet_id]',
		'[p4_id]',
		'[row_no]',
		'[gatherer]',
		'[purchaser]',
		'[operator_name]',
		'[rrc_code]',
		'[percent_of_take]',
		'[full_well_stream]',
		'[operator_no]',
		'[product_code]',
		'[process_code]'
	],
	'texas_comp_p4_oil_gatherer_data'    : [
		'[oil_gatherer_data]',
		'[tracking_no]',
		'[packet_id]',
		'[p4_id]',
		'[row_no]',
		'[operator_name]',
		'[percent_of_take]',
		'[operator_no]',
		'[product_code]',
		'[process_code]'
	],
	'texas_comp_packet_data'             : [
		'[packet]',
		'[tracking_no]',
		'[packet_id]',
		'[submit_dt]',
		'[approved_dt]',
		'[operator_no]',
		'[api_no]',
		'[dp_no]',
		'[lease_no]',
		'[well_no]',
		'[well_type]',
		'[purpose_of_filing]',
		'[completion_type]',
		'[rule37_case_no]',
		'[wtr_injctn_prmt_dt]',
		'[wtr_injctn_prmt_no]',
		'[sltwtr_dspsl_prmt_dt]',
		'[sltwtr_dspsl_prmt_no]',
		'[other_permit_dscrptn]',
		'[other_permit_date]',
		'[other_permit_no]',
		'[cmpl_or_recmpl_date]',
		'[frmr_lease_name]',
		'[frmr_gas_id_or_oil_lse_no]',
		'[frmr_gas_id_or_oil_lease]',
		'[field_no]',
		'[lease_name]',
		'[district]',
		'[county]',
		'[field_name]',
		'[survey]',
		'[frmr_well_no]',
		'[cmpl_packet_type]',
		'[direction_nearest_town]',
		'[rule37_case_dt]',
		'[frmr_operator_name]',
		'[latitude]',
		'[longitude]',
		'[electric_log_run]',
		'[dp_dt]',
		'[wellbore_profile]',
		'[total_acres]',
		'[no_of_producing_wells]',
		'[nearest_well_dist]',
		'[latlong_code]',
		'[latlong_other]',
		'[oil_gas_type_code]',
		'[survey_block]',
		'[survey_section]',
		'[survey_abstract]',
		'[unit_no]',
		'[electric_log_other_desc]',
		'[filing_method_code]',
		'[horiz_wellbore_type_code]',
		'[spud_dt]',
		'[dist_direction_miles]',
		'[dist_direction_direction]',
		'[stacked_lat_status_no_parent]',
		'[field_horz_severance_depth_txt]',
		'[field_horz_severance_depth_low]',
		'[workover_row_count]',
		'[process_code]'
	],
	'texas_comp_production_interval_data': [
		'[production_interval_data]',
		'[tracking_no]',
		'[packet_id]',
		'[g1_id or w2_id]',
		'[row_no]',
		'[from]',
		'[to]',
		'[bottom_hole_label]',
		'[lateral_label]',
		'[open_hole]',
		'[process_code]'
	],
	'texas_comp_reclass_data'            : [
		'[packet_workover]',
		'[tracking_no]',
		'[packet_id]',
		'[row_no]',
		'[field_reservoir]',
		'[lease_no]',
		'[well_no]',
		'[well_type]',
		'[district]',
		'[field_no]',
		'[prior_service_code]',
		'[process_code]'
	],
	'texas_comp_tubing_data'             : [
		'[tubing_data]',
		'[tracking_no]',
		'[packet_id]',
		'[w2_id]',
		'[row_no]',
		'[tubing_size]',
		'[depth_set]',
		'[packer_set]',
		'[packer_type]',
		'[process_code]'
	],
	'texas_comp_w12_data'                : [
		'[w_12]',
		'[tracking_no]',
		'[packet_id]',
		'[w12_id]',
		'[shot_point_500ft]',
		'[shot_points_1000ft]',
		'[last_shot_point_1000ft]',
		'[bore_displacement_1]',
		'[bore_displacement_2]',
		'[nearest_lease_line]',
		'[was_well_deviated]',
		'[yes_remarks]',
		'[remarks]',
		'[form_certification]',
		'[process_code]'
	],
	'texas_comp_w2_data'                 : [
		'[w_2]',
		'[tracking_no]',
		'[packet_id]',
		'[w2_id]',
		'[date_of_test]',
		'[hours_tested]',
		'[prod_method]',
		'[pump_size]',
		'[pump_type]',
		'[choke_size]',
		'[prod_during_test_oil]',
		'[prod_gas]',
		'[prod_flow_tube_press]',
		'[prod_water]',
		'[calc_24hr_rate_oil]',
		'[calc_gas]',
		'[calc_casing_press]',
		'[calc_water]',
		'[calc_oil_gravity]',
		'[was_swab_used]',
		'[oil_prod_prior_test]',
		'[injection_ratio]',
		'[remarks_pg1]',
		'[notice_of_intention]',
		'[number_of_producing_wells]',
		'[acres_in_lease]',
		'[work_commenced_dt]',
		'[work_completed_dt]',
		'[distance_to_nearest_well]',
		'[distance_to_boundary_a]',
		'[direction_to_bndry_a_code]',
		'[distance_to_boundary_b]',
		'[direction_to_bndry_b_code]',
		'[boundary_lease_name]',
		'[elevation]',
		'[elevation_code]',
		'[was_direct_survey_made]',
		'[top_of_pay]',
		'[measured_depth]',
		'[vertical_depth]',
		'[plug_back_depth]',
		'[casing_detr_field_rules]',
		'[casing_detr_recommend_dt]',
		'[casing_detr_rrc_dt]',
		'[drilling_contractor_nm]',
		'[is_multiple_completion]',
		'[cementing_aff_attached]',
		'[remarks]',
		'[intervals_drilled_by_code]',
		'[amount_material_remarks]',
		'[form_certification_y_n]',
		'[intervals_drilled_by_other]',
		'[prod_intv_remark]',
		'[is_unperforated_cmpl]',
		'[plug_back_depth_tmd]',
		'[top_of_pay_tmd]',
		'[off_lease]',
		'[tester_name]',
		'[tester_company]',
		'[tester_phone]',
		'[op_is_tester]',
		'[commingled]',
		'[interval_hydrogen_sulfide]',
		'[hydraulic_fracking_used]',
		'[has_fracking_disclosure]',
		'[tubing_rec_remarks]',
		'[tubing_rec_swr13_exception]',
		'[surface_casing_rotation_time]',
		'[casing_detr_recommend_depth]',
		'[casing_detr_swr_13_depth]',
		'[is_actuation_valve_on_well]',
		'[prod_case_psig_bef_frack_treat]',
		'[hydraulic_fracking_max_psig]',
		'[casing_detr_swr_13_excep]',
		'[casing_detr_recommend_gau_g pd]',
		'[actuation_valve_on_well_psig]',
		'[amount_and_material_cnt]',
		'[multi_cmpl_row_count]',
		'[casing_data_row_cnt]',
		'[liner_data_row_cnt]',
		'[tubing_data_row_cnt]',
		'[prod_interval_data_row_cnt]',
		'[formation_data_row_cnt]',
		'[process_code]'
	]
}

# Utils ---------------------------------------------------------------------------------------------------------------------------------------

def get_connection(database='US_Wells', server_name='63.33.172.39', username='uswellsdata', password='uswellsdata', external=False):
	if external:
		conn_str = 'Driver={SQL Server}; Server=%s; Database=%s; uid=%s; pwd=%s' % (server_name, database, username, password)
	else:
		conn_str = 'Driver={SQL Server}; Server=(local); Database=%s; Trusted_Connection=True; unicode_results=True;' % database
	conn = pypyodbc.connect(conn_str)
	return conn


def encode_str(ascii_str):
    encoded = ''
    try:
        encoded = unicode(ascii_str.encode('utf-8').strip(), errors='ignore')
    except:
        pass
    return encoded


def commit(curr):
    curr.execute('COMMIT')


def get_data(param, table, cursor, datatype='str', sql_where='1=1', single_value=False, debug=False):
    param_values = []

    sql_select = 'SELECT DISTINCT {0} FROM {1} WHERE {2} '.format(param, table, sql_where)
    if debug:
        print 'sql_select: {}'.format(sql_select)
		
    if cursor.execute(sql_select):
        data_points = cursor.fetchall()
        if debug:
            print ','.join(['{}']*len(data_points)).format(*data_points)
			
        if datatype == 'int':
            param_values = [int(data[0]) for data in data_points]
			
        elif datatype == 'str':
            param_values = [str(data[0]) for data in data_points]
			
        elif datatype == 'float':
            param_values = [float(data[0]) for data in data_points]
			
        elif datatype == 'plural':
            param_values = list(data_points)
    else:
        param_values = []
		
    if single_value:
        if len(param_values):
            param_values = param_values[0]
        else:
            param_values = None

    return param_values


# Completion Data -----------------------------------------------------------------------------------------------------------------------------

def unzip_files(zipfile_dir, unzip_dir):
	for zipfile in os.listdir(zipfile_dir):
		with ZipFile(zipfile_dir + zipfile) as zf:
			zf.extractall(unzip_dir + zipfile[:-4])


def store_data_records(curr, comp_dir=COMP_OUT_DIR):
	sql_insert = "INSERT INTO texas_comp_data_records (tracking_no, header_data, record_code, comp_record, process_code, source_file) VALUES ({}, '{}', '{}', '{}', 0, '{}')"
	sql_update = "UPDATE texas_comp_data_records SET comp_record=CONCAT(comp_record,' ','{}') WHERE id={} AND process_code=0"
	sql_update_2 = \
		'''
		UPDATE texas_comp_data_records SET process_code=1;
		UPDATE texas_comp_casing_data SET process_code=1;
		UPDATE texas_comp_formation_data SET process_code=1;
		UPDATE texas_comp_g10_data SET process_code=1;
		UPDATE texas_comp_g1_data SET process_code=1;
		UPDATE texas_comp_g1_field_data SET process_code=1;
		UPDATE texas_comp_g5_data SET process_code=1;
		UPDATE texas_comp_gas_measurement_data SET process_code=1;
		UPDATE texas_comp_l1_data SET process_code=1;
		UPDATE texas_comp_liner_data SET process_code=1;
		UPDATE texas_comp_material_used_data SET process_code=1;
		UPDATE texas_comp_multiple_completion_data SET process_code=1;
		UPDATE texas_comp_p15_data SET process_code=1;
		UPDATE texas_comp_p4_data SET process_code=1;
		UPDATE texas_comp_p4_gas_gatherer_data SET process_code=1;
		UPDATE texas_comp_p4_oil_gatherer_data SET process_code=1;
		UPDATE texas_comp_packet_data SET process_code=1;
		UPDATE texas_comp_production_interval_data SET process_code=1;
		UPDATE texas_comp_reclass_data SET process_code=1;
		UPDATE texas_comp_tubing_data SET process_code=1;
		UPDATE texas_comp_w12_data SET process_code=1;
		UPDATE texas_comp_w2_data SET process_code=1;
		UPDATE tx_completion_data SET process_code=1;
		'''
	curr.execute(sql_update_2)
	commit(curr)
	for comp_date_dir in os.listdir(comp_dir):
		for district_no in os.listdir('{}{}\\'.format(comp_dir, comp_date_dir)):
			district_dir = '{}{}\\{}\\'.format(comp_dir, comp_date_dir, district_no)
			for foldername in os.listdir(district_dir):
				tracking_number = int(foldername[11:])
				packet_dir = district_dir + foldername + '\\'
				for packet_filename in os.listdir(packet_dir):
					print packet_filename
					with open(packet_dir + packet_filename) as packet_file:
						datalines = packet_file.readlines()
						if len(datalines):
							header_data = datalines[0]
							for dataline in datalines[1:]:
								dataline = encode_str(dataline)
								dataline = dataline.replace(',', '')
								dataline = dataline.replace("'", "")
								dataline = dataline.replace('\n', ' ')
								dataline = dataline.replace('\\', ' ')
								record_code = None
								if len(dataline) > 1:
									data_vals = dataline.split('{')
									if data_vals[0] in COMP_REC_CODE.keys():
										record_code = data_vals[0]
										comp_rec = (
											tracking_number, header_data[:250].replace('\n', ' '), record_code,
											dataline,
											packet_dir + packet_filename)
										curr.execute(sql_insert.format(*comp_rec))
										commit(curr)
									elif str(tracking_number) != str(data_vals[0])[:6]:
										try:
											max_id = get_data('MAX(id)', 'texas_comp_data_records', curr, datatype='int', single_value=True)
										except:
											max_id = 1
										
										curr.execute(sql_update.format(dataline[:-1], max_id))
										commit(curr)
									else:
										comp_rec = (
											tracking_number, header_data[:250], record_code,
											dataline[:-1], packet_dir + packet_filename)
										
										curr.execute(sql_insert.format(*comp_rec))
										commit(curr)


def parse_comp_data(curr):
	sql_insert_temp = 'INSERT INTO {} ({}) VALUES ({})'
	sql_update_2 = \
		"""
		UPDATE texas_comp_data_records SET record_code=REPLACE(REPLACE(REPLACE(record_code,',',''),'"',''),'''','');
		"""
	curr.execute(sql_update_2)
	commit(curr)
	for record_code in COMP_REC_CODE.keys():
		data_table = COMP_REC_CODE[record_code]
		sql_where = "record_code='{}' AND process_code=0".format(record_code)
		comp_data = get_data('comp_record', 'dbo.texas_comp_data_records', curr, sql_where=sql_where, datatype='str')
		print record_code
		data_count = len(comp_data)
		row_num = 1
		for comp_datarow in comp_data:
			comp_data_col_count = comp_datarow.count('{')
			comp_col_count = COMP_COL_COUNT[data_table.lower()]
			comp_col_str = ','.join(TX_COMP_COLS[data_table.lower()])
			if comp_data_col_count != (comp_col_count - 2):
				comp_datarow += ('{' * ((comp_col_count - 2) - comp_data_col_count))
			comp_data_vals = comp_datarow.split('{')
			var_str = ','.join(['?'] * (len(comp_data_vals) + 1))
			param_vals = ()
			print '\n', '{}/{}'.format(row_num, data_count), data_table, len(comp_data_vals)
			for data_val in comp_data_vals:
				if not data_val:
					param_vals += (None,)
				else:
					param_vals += (data_val.replace(',', ''),)
			param_vals += (0,)
			sql_insert = sql_insert_temp.format(data_table, comp_col_str, var_str)
			assert (len(param_vals) == sql_insert.count('?'))
			try:
				curr.execute(sql_insert, param_vals)
				commit(curr)
			except:
				print sql_insert.replace('?', '{}').format(*param_vals)
			row_num += 1


def update_completion_tables(curr):
	sql_update = \
		"""
		UPDATE texas_comp_packet_data SET api_no=CONCAT('4200', api_no) WHERE LEN(api_no)=6 AND process_code=0;
		UPDATE texas_comp_packet_data SET api_no=CONCAT('420', api_no) WHERE LEN(api_no)=7 AND process_code=0;
		UPDATE texas_comp_packet_data SET api_no=CONCAT('42', api_no) WHERE LEN(api_no)=8 AND process_code=0;
		UPDATE texas_comp_packet_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
		UPDATE texas_comp_packet_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
		UPDATE texas_comp_packet_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
		UPDATE texas_comp_packet_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
		UPDATE texas_comp_packet_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
		UPDATE texas_comp_packet_data SET well_no=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(well_no,'\\',''),'-',''),'_',''),'\t',''),'{',''),' ',''),'''',''),'"','') WHERE process_code=0;
		UPDATE texas_comp_packet_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND process_code=0;
		UPDATE texas_comp_packet_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND process_code=0;
		UPDATE texas_comp_packet_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND process_code=0;
		UPDATE texas_comp_packet_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND process_code=0;
		UPDATE texas_comp_packet_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND process_code=0;
		UPDATE texas_comp_packet_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND process_code=0;
		UPDATE texas_comp_packet_data SET district='14' WHERE district='10' AND process_code=0;
		UPDATE texas_comp_packet_data SET district='10' WHERE district='08' AND process_code=0;
		UPDATE texas_comp_packet_data SET district='08' WHERE district='7B' AND process_code=0;
		UPDATE texas_comp_packet_data SET district='13' WHERE district='09' AND process_code=0;
		UPDATE texas_comp_packet_data SET district='09' WHERE district='7C' AND process_code=0;
		UPDATE texas_comp_packet_data SET district='07' WHERE district='6E' AND process_code=0;
		UPDATE texas_comp_packet_data SET district='11' WHERE district='8A' AND process_code=0;
		UPDATE texas_comp_packet_data SET district='12' WHERE district='8B' AND process_code=0;
		UPDATE texas_comp_packet_data
		  SET tx_well_id=b.tx_well_id
		  FROM texas_comp_packet_data AS a, tx_ref_well_id AS b
		  WHERE a.api_no=b.api_number AND a.lease_no=b.lease_no AND a.well_no=b.well_no AND a.district=b.district_no AND a.tx_well_id IS NULL AND a.process_code=0;
		UPDATE texas_comp_packet_data
		  SET tx_well_id=b.tx_well_id, lease_no=b.lease_no
		  FROM texas_comp_packet_data AS a, tx_ref_well_id AS b
		  WHERE a.api_no=b.api_number AND a.well_no=b.well_no AND a.district=b.district_no AND a.county=b.county_no AND a.tx_well_id IS NULL AND a.operator_no=b.operator_no AND a.field_no=b.field_no AND a.process_code=0;
		UPDATE texas_comp_packet_data SET cmpl_or_recmpl_date=CONCAT(SUBSTRING(cmpl_or_recmpl_date,7,4),SUBSTRING(cmpl_or_recmpl_date,1,2)) WHERE NOT cmpl_or_recmpl_date IS NULL AND process_code=0;
		UPDATE texas_comp_w2_data
		  SET tx_well_id=b.tx_well_id
		  FROM texas_comp_w2_data AS a, texas_comp_packet_data AS b
		  WHERE NOT b.tx_well_id IS NULL AND a.packet_id=b.packet_id AND a.tracking_no=b.tracking_no AND a.process_code=0;
		UPDATE texas_comp_g1_data
		  SET tx_well_id=b.tx_well_id
		  FROM texas_comp_g1_data AS a, texas_comp_packet_data AS b
		  WHERE NOT b.tx_well_id IS NULL AND a.packet_id=b.packet_id AND a.tracking_no=b.tracking_no AND a.process_code=0;
		UPDATE texas_comp_w2_data SET date_of_test=CONCAT(SUBSTRING(date_of_test,7,4),SUBSTRING(date_of_test,1,2)) WHERE NOT date_of_test IS NULL AND process_code=0;
		INSERT INTO tx_completion_data (packet,tracking_no,packet_id,tx_well_id,api_no,dp_no,lease_no,well_no,oil_gas_type_code,operator_no,field_no,lease_name,district,county,field_name,well_type,wellbore_profile,latitude,longitude,total_acres,no_of_producing_wells,unit_no,horiz_wellbore_type_code,completion_type,cmpl_or_recmpl_date,dp_dt,spud_dt,submit_dt,approved_dt,cmpl_packet_type,purpose_of_filing,frmr_lease_name,frmr_gas_id_or_oil_lse_no,frmr_gas_id_or_oil_lease,frmr_well_no,process_code)
		  (SELECT DISTINCT packet,tracking_no,packet_id,tx_well_id,api_no,dp_no,lease_no,well_no,oil_gas_type_code,operator_no,field_no,lease_name,district,county,field_name,well_type,wellbore_profile,latitude,longitude,total_acres,no_of_producing_wells,unit_no,horiz_wellbore_type_code,completion_type,cmpl_or_recmpl_date,dp_dt,spud_dt,submit_dt,approved_dt,cmpl_packet_type,purpose_of_filing,frmr_lease_name,frmr_gas_id_or_oil_lse_no,frmr_gas_id_or_oil_lease,frmr_well_no,process_code
		   FROM texas_comp_packet_data WHERE process_code=0);
		UPDATE tx_completion_data
		  SET lease_no=b.lease_no
		  FROM tx_completion_data AS a, texas_comp_packet_data AS b
		  WHERE a.api_no=b.api_no AND a.operator_no=b.operator_no AND a.well_no=b.well_no AND a.district=b.district AND a.dp_no=b.dp_no AND a.tx_well_id IS NULL AND NOT b.lease_no IS NULL AND a.lease_no IS NULL AND a.process_code=0;
		UPDATE tx_completion_data
		  SET tx_well_id=b.tx_well_id
		  FROM tx_completion_data AS a, texas_comp_packet_data AS b
		  WHERE a.api_no=b.api_no AND a.operator_no=b.operator_no AND a.well_no=b.well_no AND a.district=b.district AND a.dp_no=b.dp_no AND a.tx_well_id IS NULL AND NOT b.tx_well_id IS NULL AND a.process_code=0;
		UPDATE tx_completion_data
		  SET tx_well_id=b.tx_well_id
		  FROM tx_completion_data AS a, tx_ref_well_id AS b
		  WHERE a.api_no=b.api_number AND a.lease_no=b.lease_no AND a.well_no=b.well_no AND a.district=b.district_no AND a.tx_well_id IS NULL AND a.process_code=0;
		UPDATE tx_completion_data
		  SET tx_well_id=b.tx_well_id, lease_no=b.lease_no
		  FROM tx_completion_data AS a, tx_ref_well_id AS b
		  WHERE a.api_no=b.api_number AND a.well_no=b.well_no AND a.district=b.district_no AND a.county=b.county_no AND a.tx_well_id IS NULL AND a.operator_no=b.operator_no AND a.field_no=b.field_no AND a.process_code=0;
		UPDATE tx_completion_data SET oil_gas_type_code='G' WHERE oil_gas_type_code='2';
		UPDATE tx_completion_data SET oil_gas_type_code='O' WHERE oil_gas_type_code='1';
		UPDATE tx_completion_data
		  SET measured_depth=b.measured_depth,vertical_depth=b.vertical_depth,top_of_pay=b.top_of_pay,prod_method=b.prod_method,hours_tested=b.hours_tested,prod_oil_bd=b.prod_during_test_oil,prod_gas_mcfd=b.prod_gas
		  FROM tx_completion_data AS a, texas_comp_w2_data AS b
		  WHERE a.tx_well_id=b.tx_well_id AND NOT a.tx_well_id IS NULL AND a.process_code=0;
		UPDATE tx_completion_data
		  SET measured_depth=b.measured_depth,vertical_depth=b.vertical_depth,top_of_pay=b.top_of_pay,bottom_hole_depth=b.bottom_hole_depth,prod_gas_mcfd=b.test_gas_production
		  FROM tx_completion_data AS a, texas_comp_g1_data AS b
		  WHERE a.tx_well_id=b.tx_well_id AND NOT a.tx_well_id IS NULL AND a.process_code=0;
		UPDATE tx_completion_data
		  SET measured_depth=b.measured_depth,vertical_depth=b.vertical_depth,top_of_pay=b.top_of_pay,prod_method=b.prod_method,hours_tested=b.hours_tested,prod_oil_bd=b.prod_during_test_oil,prod_gas_mcfd=b.prod_gas
		  FROM tx_completion_data AS a, texas_comp_w2_data AS b
		  WHERE a.packet_id=b.packet_id AND a.tracking_no=b.tracking_no AND a.tx_well_id IS NULL AND a.process_code=0;
		UPDATE tx_completion_data
		  SET measured_depth=b.measured_depth,vertical_depth=b.vertical_depth,top_of_pay=b.top_of_pay,bottom_hole_depth=b.bottom_hole_depth,prod_gas_mcfd=b.test_gas_production
		  FROM tx_completion_data AS a, texas_comp_g1_data AS b
		  WHERE a.packet_id=b.packet_id AND a.tracking_no=b.tracking_no AND a.tx_well_id IS NULL AND a.process_code=0;
		UPDATE tx_completion_data SET dp_dt=b.dp_dt, spud_dt=b.spud_dt, submit_dt=b.submit_dt, approved_dt=b.approved_dt
		  FROM tx_completion_data a, texas_comp_packet_data b
		  WHERE a.packet=b.packet AND a.tracking_no=b.tracking_no AND a.packet_id=b.packet_id;
		UPDATE tx_completion_data SET dp_dt=CONCAT(SUBSTRING(dp_dt,7,4),SUBSTRING(dp_dt,1,2)) WHERE dp_dt LIKE '%/%/%';
		UPDATE tx_completion_data SET spud_dt=CONCAT(SUBSTRING(spud_dt,7,4),SUBSTRING(spud_dt,1,2)) WHERE spud_dt LIKE '%/%/%';
		UPDATE tx_completion_data SET submit_dt=CONCAT(SUBSTRING(submit_dt,7,4),SUBSTRING(submit_dt,1,2)) WHERE submit_dt LIKE '%/%/%';
		UPDATE tx_completion_data SET approved_dt=CONCAT(SUBSTRING(approved_dt,7,4),SUBSTRING(approved_dt,1,2)) WHERE approved_dt LIKE '%/%/%';
		COMMIT;
		"""
	curr.execute(sql_update)


def process_completion_data(unzip_data=False, store_records=False, parse_data=False, update_tables=False, debug=False):
	# Replace with database name -- US_Wells_DataExtract
	conn = get_connection(database='US_Wells_Texas')
	curr = conn.cursor()
	
	if unzip_data:
		print 'Extracting completion data from compressed files ...'
		unzip_files(zipfile_dir=COMP_ZIP_DIR, unzip_dir=COMP_OUT_DIR)
	
	if store_records:
		print 'Storing completion data records in US_Wells_Texas.dbo.texas_comp_data_records ...'
		store_data_records(curr)
	
	if parse_data:
		print 'Parsing completion data records into completion data tables ...'
		parse_comp_data(curr)
	
	if update_tables:
		print 'Updating completion data tables ...'
		update_completion_tables(curr)
	
	curr.close()
	conn.close()


if __name__ == '__main__':
	process_completion_data(unzip_data=True, store_records=True, parse_data=True, update_tables=True, debug=False)
