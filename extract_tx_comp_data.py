import globaldata as gd
import os
from zipfile import ZipFile
import ftputil
from distutils.dir_util import copy_tree
import shutil
from csv_sql_import import main as csv_import_main

TX_COMP_DIR     = gd.DATA_DIR + 'tx_data\\tx_completion_data\\'
TX_ZIP_OUT_DIR  = gd.DATA_DIR + 'tx_data\\tx_completion_data\\comp_data\\'
TX_ZIP_IN_DIR   = gd.DATA_DIR + 'tx_data\\tx_completion_data\\Texas Completion Data\\'
COMP_ZIP_DIR    = gd.DATA_DIR + 'tx_data\\tx_completion_zipfiles\\'
COMP_OUT_DIR    = gd.DATA_DIR + 'tx_data\\tx_completion_data\\tx_completion_files\\'
EWA_FILE_DIR    = gd.DATA_DIR + 'tx_data\\tx_ewa_files\\'
EWA_DATA_DIR    = gd.DATA_DIR + 'tx_data\\tx_ewa_data\\'

EWA_HEADER_NAMES = [
    'DISTRICT_CODE',
    'COUNTY_CODE',
    'API_NUMBER',
    'COUNTY_NAME',
    'OIL_GAS_CODE',
    'LEASE_NAME',
    'FIELD_NUMBER',
    'FIELD_NAME',
    'LEASE_NUMBER',
    'WELL_NO_DISPLAY',
    'OIL_UNIT_NUMBER',
    'OPERATOR_NAME',
    'OPERATOR_NUMBER',
    'WB_WATER_LAND_CODE',
    'MULTI_COMP_FLAG',
    'API_DEPTH',
    'WB_SHUT_IN_DEPTH',
    'WB_14B2_FLAG',
    'WELL_TYPE_NAME',
    'WL_SHUT_IN_DATE',
    'PLUG_DATE',
    'PLUG_LEASE_NAME',
    'PLUG_OPERATOR_NAME',
    'RECENT_PERMIT',
    'RECENT_PERMIT_LEASE_NAME',
    'RECENT_PERMIT_OPERATOR_NO',
    'ON_SCHEDULE',
    'OG_WELLBORE_EWA_ID',
    'W2_G1_FILED_DATE',
    'W2_G1_DATE',
    'COMPLETION_DATE',
    'W3_FILE_DATE',
    'CREATED_BY',
    'CREATED_DT',
    'MODIFIED_BY',
    'MODIFIED_DT',
    'WELL_NO',
    'P5_RENEWAL_MONTH',
    'P5_RENEWAL_YEAR',
    'P5_ORG_STATUS',
    'CURR_INACT_YRS',
    'CURR_INACT_MOS',
    'WL_14_B2_EXT_STATUS',
    'WL_14_B2_MECH_INTEG',
    'WL_14_B2_PLG_ORD_SF',
    'WL_14_B2_POLLUTION',
    'WL_14_B2_FLDOPS_HOLD',
    'WL_14_B2_H15_PROB',
    'WL_14_B2_H15_DELQ',
    'WL_14_B2_OPER_DELQ',
    'WL_14_B2_DIST_SFP',
    'WL_14_B2_DIST_SF_CLNUP',
    'WL_14_B2_DIST_ST_PLG',
    'WL_14_B2_GOOD_FAITH',
    'WL_14_B2_WELL_OTHER',
    'SURF_EQP_VIOL',
    'W3X_VIOL',
    'H15_STATUS_CODE',
    'ORIG_COMPLETION_DT'
]

COMP_REC_CODE    = {
    'PACKET'                        : 'dbo.texas_comp_Packet_Data',
    'PACKET_WORKOVER'               : 'dbo.texas_comp_Reclass_Data',
    'G-1'                           : 'dbo.texas_comp_G1_Data',
    'G-1 Measurement Data'          : 'dbo.texas_comp_Gas_Measurement_Data',
    'G-1 Field Data'                : 'dbo.texas_comp_G1_Field_Data',
    'G-1 Amount And Material Data'  : 'dbo.texas_comp_Material_Used_Data',
    'G-1 Multiple Completion Data'  : 'dbo.texas_comp_Multiple_Completion_Data',
    'G-1 Multi-Completion Data'     : 'dbo.texas_comp_Multiple_Completion_Data',
    'G-1 Liner Data'                : 'dbo.texas_comp_Liner_Data',
    'G-1 Casing Data'               : 'dbo.texas_comp_Casing_Data',
    'G-1 Production Interval Data'  : 'dbo.texas_comp_Production_Interval_Data',
    'G-1 Tubing Data'               : 'dbo.texas_comp_Tubing_Data',
    'G-1 Formation Data'            : 'dbo.texas_comp_Formation_Data',
    'W-2'                           : 'dbo.texas_comp_W2_Data',
    'W-2 Amount And Material Data'  : 'dbo.texas_comp_Material_Used_Data',
    'W-2 Multiple Completion Data'  : 'dbo.texas_comp_Multiple_Completion_Data',
    'W-2 Multi-Completion Data'     : 'dbo.texas_comp_Multiple_Completion_Data',
    'W-2 Liner Data'                : 'dbo.texas_comp_Liner_Data',
    'W-2 Casing Data'               : 'dbo.texas_comp_Casing_Data',
    'W-2 Production Interval Data'  : 'dbo.texas_comp_Production_Interval_Data',
    'W-2 Tubing Data'               : 'dbo.texas_comp_Tubing_Data',
    'W-2 Formation Data'            : 'dbo.texas_comp_Formation_Data',
    'P-4'                           : 'dbo.texas_comp_P4_Data',
    'P-4 Gas Gatherer Data'         : 'dbo.texas_comp_P4_Gas_Gatherer_Data',
    'P-4 Oil Gatherer Data'         : 'dbo.texas_comp_P4_Oil_Gatherer_Data',
    'L-1'                           : 'dbo.texas_comp_L1_Data',
    'P-15'                          : 'dbo.texas_comp_P15_Data',
    'G-5'                           : 'dbo.texas_comp_G5_Data',
    'G-10'                          : 'dbo.texas_comp_G10_Data',
    'W-12'                          : 'dbo.texas_comp_W12_Data'
}

COMP_COL_COUNT = {
    'dbo.texas_comp_casing_data'               : 19,
    'dbo.texas_comp_formation_data'            : 12,
    'dbo.texas_comp_g10_data'                  : 21,
    'dbo.texas_comp_g1_data'                   : 90,
    'dbo.texas_comp_g1_field_data'             : 10,
    'dbo.texas_comp_g5_data'                   : 40,
    'dbo.texas_comp_gas_measurement_data'      : 16,
    'dbo.texas_comp_l1_data'                   : 19,
    'dbo.texas_comp_liner_data'                : 16,
    'dbo.texas_comp_material_used_data'        : 10,
    'dbo.texas_comp_multiple_completion_data'  : 10,
    'dbo.texas_comp_p15_data'                  : 8,
    'dbo.texas_comp_p4_data'                   : 14,
    'dbo.texas_comp_p4_gas_gatherer_data'      : 14,
    'dbo.texas_comp_p4_oil_gatherer_data'      : 10,
    'dbo.texas_comp_packet_data'               : 62,
    'dbo.texas_comp_production_interval_data'  : 11,
    'dbo.texas_comp_reclass_data'              : 12,
    'dbo.texas_comp_tubing_data'               : 10,
    'dbo.texas_comp_w12_data'                  : 15,
    'dbo.texas_comp_w2_data'                   : 84
}

TX_COMP_COLS = {
	'dbo.texas_comp_casing_data': [
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
	'dbo.texas_comp_formation_data': [
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
	'dbo.texas_comp_g10_data': [
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
	'dbo.texas_comp_g1_data': [
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
	'dbo.texas_comp_g1_field_data': [
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
	'dbo.texas_comp_g5_data': [
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
	'dbo.texas_comp_gas_measurement_data': [
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
	'dbo.texas_comp_l1_data': [
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
	'dbo.texas_comp_liner_data': [
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
	'dbo.texas_comp_material_used_data': [
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
	'dbo.texas_comp_multiple_completion_data': [
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
	'dbo.texas_comp_p15_data': [
		'[p_15]',
		'[tracking_no]',
		'[packet_id]',
		'[p15_id]',
		'[operator_certification]',
		'[form_certification]',
		'[plat_acres]',
		'[process_code]'
	],
	'dbo.texas_comp_p4_data': [
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
	'dbo.texas_comp_p4_gas_gatherer_data': [
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
	'dbo.texas_comp_p4_oil_gatherer_data': [
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
	'dbo.texas_comp_packet_data': [
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
	'dbo.texas_comp_production_interval_data': [
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
	'dbo.texas_comp_reclass_data': [
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
	'dbo.texas_comp_tubing_data': [
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
	'dbo.texas_comp_w12_data': [
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
	'dbo.texas_comp_w2_data': [
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


def change_seperators(file_dir=EWA_FILE_DIR, out_dir=EWA_DATA_DIR):
    for tx_file in os.listdir(file_dir):
        outfile_name = tx_file[:-4]+'.txt'
        outfile = ''
        with open(file_dir+tx_file) as tx_data:
            row_num = 1
            datarows = tx_data.readlines()
            row_count = len(datarows)
            for datarow in datarows:
                print '{}/{}'.format(row_num, row_count)
                datarow = datarow.replace('|', '@')
                datarow = datarow.replace('","', '"|"')
                outfile += datarow
                if row_num % 10000 == 0:
                    with open(out_dir + outfile_name, 'a') as outfile_txt:
                        outfile_txt.write(outfile)
                    outfile = ''
                row_num += 1

def ftp_download(ftp_data_dir='CMPL_Data', ftp_file_dir=COMP_OUT_DIR):
    with ftputil.FTPHost('ftp.rrc.texas.gov', 'subdata', 'WGn4t7SM') as ftp_host:
        ftp_host.chdir(ftp_data_dir)
        data_dirs = ftp_host.listdir(ftp_host.curdir)
        for data_dir in data_dirs[1:]:
            print data_dir
            ftp_host.chdir(data_dir)
            filenames = ftp_host.listdir(ftp_host.curdir)
            for filename in filenames:
                print '\t', filename
                if ftp_host.path.isfile(filename):
                    ftp_host.download(filename, ftp_file_dir+data_dir+filename[-4:])
            ftp_host.chdir('..')

def move_zipfiles(infile_dir, outfile_dir):
    for comp_year_dir in os.listdir(infile_dir):
        print comp_year_dir
        for comp_mon_dir in os.listdir('{}{}\\'.format(infile_dir, comp_year_dir)):
            print comp_year_dir, comp_mon_dir
            for comp_mon2_dir in os.listdir('{}{}\\{}\\'.format(infile_dir, comp_year_dir, comp_mon_dir)):
                print comp_year_dir, comp_mon_dir, comp_mon2_dir
                for comp_day_dir in [comp_dir for comp_dir in os.listdir('{}{}\\{}\\{}\\'.format(infile_dir, comp_year_dir, comp_mon_dir, comp_mon2_dir)) if comp_dir != 'Desktop.ini']:
                    print comp_year_dir, comp_mon_dir, comp_mon2_dir, comp_day_dir
                    for comp_file in os.listdir('{}{}\\{}\\{}\\{}\\'.format(infile_dir, comp_year_dir, comp_mon_dir, comp_mon2_dir, comp_day_dir)):
                        print comp_year_dir, comp_mon_dir, comp_day_dir, comp_file
                        if comp_file[-3:] == 'zip':
                            shutil.move('{}{}\\{}\\{}\\{}\\{}'.format(infile_dir, comp_year_dir, comp_mon_dir, comp_mon2_dir, comp_day_dir, comp_file), '{}{}'.format(outfile_dir,comp_file))

def unzip_files(zipfile_dir, unzip_dir):
    for zipfile in os.listdir(zipfile_dir):
        with ZipFile(zipfile_dir+zipfile) as zf:
            zf.extractall(unzip_dir+zipfile[:-4])

def parse_comp_data(debug=False):
    sql_insert_temp = 'INSERT INTO {} ({}) VALUES ({})'
    conn = gd.get_connection(database='US_Wells_Texas', server='sql_server')
    curr = conn.cursor()
    for record_code in COMP_REC_CODE.keys():
        data_table = COMP_REC_CODE[record_code]
        comp_data = gd.get_data('comp_record', 'dbo.texas_comp_data_records', sql_where="record_code='{}' AND process_code=0".format(record_code), database='US_Wells_Texas', server='sql_server', datatype='str')
        print record_code, comp_data
        data_count = len(comp_data)
        row_num = 1
        for comp_datarow in comp_data:
            comp_data_col_count = comp_datarow.count('{')
            comp_col_count = COMP_COL_COUNT[data_table.lower()]
            comp_col_str   = ','.join(TX_COMP_COLS[data_table.lower()])
            if comp_data_col_count != (comp_col_count-2):
                comp_datarow += ('{'*((comp_col_count-2)-comp_data_col_count))
            comp_data_vals = comp_datarow.split('{')
            var_str =','.join(['?']*(len(comp_data_vals)+1))
            param_vals = ()
            print '\n', '{}/{}'.format(row_num,data_count), data_table, len(comp_data_vals)
            for data_val in comp_data_vals:
                if not data_val:
                    param_vals += (None,)
                else:
                    param_vals += (data_val.replace(',',''),)
            param_vals += (0,)
            print len(param_vals), var_str.count('%')
            sql_insert = sql_insert_temp.format(data_table, comp_col_str, var_str)
            try:
                if debug:
                    try:
                        print sql_insert % param_vals
                    except:
                        print sql_insert, param_vals
                curr.execute(sql_insert, param_vals)
                gd.commit(curr)
            except:
                if debug:
                    try:
                        print sql_insert % param_vals
                    except:
                        print sql_insert, param_vals
            row_num += 1

    curr.close()
    conn.close()

def store_data_records(comp_dir=COMP_OUT_DIR, debug=False):
    sql_insert = "INSERT INTO dbo.texas_comp_data_records (tracking_no, header_data, record_code, comp_record, process_code, source_file) VALUES (?, ?, ?, ?, 0, ?)"
    sql_update = "UPDATE dbo.texas_comp_data_records SET comp_record=CONCAT(comp_record,' ',?) WHERE id=? AND process_code=0"
    conn = gd.get_connection(database='US_Wells_Texas', server='sql_server')
    curr = conn.cursor()
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
                                dataline = gd.encode_str(dataline.replace('\n',' '))
                                record_code = None
                                if len(dataline) > 1:
                                    data_vals = dataline.split('{')
                                    if data_vals[0] in COMP_REC_CODE.keys():
                                        record_code = data_vals[0]
                                        comp_rec = (tracking_number, header_data[:250], record_code, dataline[:-1], packet_dir + packet_filename)
                                        if debug: print sql_insert % comp_rec
                                        curr.execute(sql_insert, comp_rec)
                                        gd.commit(curr)
                                    elif str(tracking_number) != str(data_vals[0])[:6]:
                                        try:
                                            max_id = gd.get_data('MAX(id)', 'dbo.texas_comp_data_records', database='US_Wells_Texas', server='sql_server', datatype='int')[0]
                                        except:
											max_id = 1
                                        if debug: print sql_update % (dataline[:-1], max_id)
                                        curr.execute(sql_update, (dataline[:-1], max_id))
                                        gd.commit(curr)
                                    else:
                                        comp_rec = (tracking_number, header_data[:250], record_code, dataline[:-1], packet_dir + packet_filename)
                                        if debug: print sql_insert % comp_rec
                                        curr.execute(sql_insert, comp_rec)
                                        gd.commit(curr)
    curr.close()
    conn.close()

def main(download_comp=False, download_ewa=False, unzip_data=False, process_ewa=False, move_files=False, store_records=False, parse_data=False, debug=False):
    if download_comp:
        ftp_download(ftp_data_dir='CMPL_Data', ftp_file_dir=COMP_OUT_DIR)
    if download_ewa:
        ftp_download(ftp_data_dir='OG_Wellbore_EWA', ftp_file_dir=EWA_FILE_DIR)
    if unzip_data:
        unzip_files(zipfile_dir=COMP_ZIP_DIR, unzip_dir=COMP_OUT_DIR)
    if process_ewa:
        change_seperators(file_dir=EWA_FILE_DIR, out_dir=EWA_DATA_DIR)
        csv_import_main(all_files=True, table_name='tx_wellbore_data', database='us_wells', data_dir=EWA_DATA_DIR, header_names=EWA_HEADER_NAMES, delimiter='|', file_ext='txt')
    if move_files:
        move_zipfiles(TX_ZIP_OUT_DIR, COMP_ZIP_DIR)
    if store_records:
        store_data_records(debug=debug)
    if parse_data:
        parse_comp_data(debug=debug)


if __name__=='__main__':
    #move_zipfiles(TX_ZIP_OUT_DIR, COMP_ZIP_DIR)
    main(download_comp=False, download_ewa=False, process_ewa=False, unzip_data=False, move_files=False, store_records=True, parse_data=True, debug=False)