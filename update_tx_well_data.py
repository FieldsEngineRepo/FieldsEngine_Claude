import os
import shutil
import urllib
import urllib2
from time import sleep
from zipfile import ZipFile

import pandas as pd
from sqlalchemy import create_engine
from win32com.client import Dispatch

import globaldata as gd

TX_DATA_DIR = gd.DATA_DIR + "tx_data\\"
TX_PROD_DIR = TX_DATA_DIR + "tx_production\\"
TX_PROD_OUT_DIR = TX_PROD_DIR + "output\\"
TX_PROD_ARCHIVE = TX_PROD_DIR + "archive\\"
TX_PROD_FILES_DIR = TX_PROD_DIR + "prod_files\\"
TX_API_DIR = TX_DATA_DIR + "tx_api_dbf\\"
TX_API_OUT_DIR = TX_API_DIR + "output\\"
TX_API_ARCHIVE = TX_API_DIR + "archive\\"
TX_WB_DIR = TX_DATA_DIR + "tx_wellbore_data\\"
TX_WB_ARCHIVE = TX_WB_DIR + "archive\\"
OIL_SCHED_DIR = TX_DATA_DIR + "tx_schedule_data\\process\\"
TX_COMP_DIR = TX_DATA_DIR + 'tx_completion_data\\'
TX_ZIP_OUT_DIR = TX_COMP_DIR + 'comp_data\\'
COMP_ZIP_DIR = TX_COMP_DIR + 'tx_completion_zipfiles\\'
COMP_OUT_DIR = TX_COMP_DIR + 'tx_completion_files\\'

INPUT_FILE = "OG_COUNTY_LEASE_CYCLE_DATA_TABLE_{}.dsv"
OUTPUT_FILE = "OG_COUNTY_LEASE_CYCLE_DATA_TABLE_{}.csv".format(gd.get_date())

WELLBORE_FILE = "OG_WELLBORE_EWA_Report.csv"
WB_HEADERS = '"DISTRICT_CODE","COUNTY_CODE","API_NUMBER","COUNTY_NAME","OIL_GAS_CODE","LEASE_NAME","FIELD_NUMBER","FIELD_NAME","LEASE_NUMBER","WELL_NO_DISPLAY","OIL_UNIT_NUMBER","OPERATOR_NAME","OPERATOR_NUMBER","WB_WATER_LAND_CODE","MULTI_COMP_FLAG","API_DEPTH","WB_SHUT_IN_DEPTH","WB_14B2_FLAG","WELL_TYPE_NAME","WL_SHUT_IN_DATE","PLUG_DATE","PLUG_LEASE_NAME","PLUG_OPERATOR_NAME","RECENT_PERMIT","RECENT_PERMIT_LEASE_NAME","RECENT_PERMIT_OPERATOR_NO","ON_SCHEDULE","OG_WELLBORE_EWA_ID","W2_G1_FILED_DATE","W2_G1_DATE","COMPLETION_DATE","W3_FILE_DATE","CREATED_BY","CREATED_DT","MODIFIED_BY","MODIFIED_DT","WELL_NO","P5_RENEWAL_MONTH","P5_RENEWAL_YEAR","P5_ORG_STATUS","CURR_INACT_YRS","CURR_INACT_MOS","WL_14_B2_EXT_STATUS","WL_14_B2_MECH_INTEG","WL_14_B2_PLG_ORD_SF","WL_14_B2_POLLUTION","WL_14_B2_FLDOPS_HOLD","WL_14_B2_H15_PROB","WL_14_B2_H15_DELQ","WL_14_B2_OPER_DELQ","WL_14_B2_DIST_SFP","WL_14_B2_DIST_SF_CLNUP","WL_14_B2_DIST_ST_PLG","WL_14_B2_GOOD_FAITH","WL_14_B2_WELL_OTHER","SURF_EQP_VIOL","W3X_VIOL","H15_STATUS_CODE","ORIG_COMPLETION_DT"\n"'

TX_PROD_ZIP = "PDQ_DSV.zip"
TX_PROD_FILE = "OG_COUNTY_LEASE_CYCLE_DATA_TABLE.dsv"
TX_PROD_URL = "ftp://ftpe.rrc.texas.gov/shpdqdmp/PDQ_DSV.zip"
API_DBF_URL = "ftp://ftpe.rrc.texas.gov/shpapidb/api/{}"
API_DBF_FILES = [
	'api001.dbf',
	'api003.dbf',
	'api005.dbf',
	'api007.dbf',
	'api009.dbf',
	'api011.dbf',
	'api013.dbf',
	'api015.dbf',
	'api017.dbf',
	'api019.dbf',
	'api021.dbf',
	'api023.dbf',
	'api025.dbf',
	'api027.dbf',
	'api029.dbf',
	'api031.dbf',
	'api033.dbf',
	'api035.dbf',
	'api037.dbf',
	'api039.dbf',
	'api041.dbf',
	'api043.dbf',
	'api045.dbf',
	'api047.dbf',
	'api049.dbf',
	'api051.dbf',
	'api053.dbf',
	'api055.dbf',
	'api057.dbf',
	'api059.dbf',
	'api061.dbf',
	'api063.dbf',
	'api065.dbf',
	'api067.dbf',
	'api069.dbf',
	'api071.dbf',
	'api073.dbf',
	'api075.dbf',
	'api077.dbf',
	'api079.dbf',
	'api081.dbf',
	'api083.dbf',
	'api085.dbf',
	'api087.dbf',
	'api089.dbf',
	'api091.dbf',
	'api093.dbf',
	'api095.dbf',
	'api097.dbf',
	'api099.dbf',
	'api101.dbf',
	'api103.dbf',
	'api105.dbf',
	'api107.dbf',
	'api109.dbf',
	'api111.dbf',
	'api113.dbf',
	'api115.dbf',
	'api117.dbf',
	'api119.dbf',
	'api121.dbf',
	'api123.dbf',
	'api125.dbf',
	'api127.dbf',
	'api129.dbf',
	'api131.dbf',
	'api133.dbf',
	'api135.dbf',
	'api137.dbf',
	'api139.dbf',
	'api141.dbf',
	'api143.dbf',
	'api145.dbf',
	'api147.dbf',
	'api149.dbf',
	'api151.dbf',
	'api153.dbf',
	'api155.dbf',
	'api157.dbf',
	'api159.dbf',
	'api161.dbf',
	'api163.dbf',
	'api165.dbf',
	'api167.dbf',
	'api169.dbf',
	'api171.dbf',
	'api173.dbf',
	'api175.dbf',
	'api177.dbf',
	'api179.dbf',
	'api181.dbf',
	'api183.dbf',
	'api185.dbf',
	'api187.dbf',
	'api189.dbf',
	'api191.dbf',
	'api193.dbf',
	'api195.dbf',
	'api197.dbf',
	'api199.dbf',
	'api201.dbf',
	'api203.dbf',
	'api205.dbf',
	'api207.dbf',
	'api209.dbf',
	'api211.dbf',
	'api213.dbf',
	'api215.dbf',
	'api217.dbf',
	'api219.dbf',
	'api221.dbf',
	'api223.dbf',
	'api225.dbf',
	'api227.dbf',
	'api229.dbf',
	'api231.dbf',
	'api233.dbf',
	'api235.dbf',
	'api237.dbf',
	'api239.dbf',
	'api241.dbf',
	'api243.dbf',
	'api245.dbf',
	'api247.dbf',
	'api249.dbf',
	'api251.dbf',
	'api253.dbf',
	'api255.dbf',
	'api257.dbf',
	'api259.dbf',
	'api261.dbf',
	'api263.dbf',
	'api265.dbf',
	'api267.dbf',
	'api269.dbf',
	'api271.dbf',
	'api273.dbf',
	'api275.dbf',
	'api277.dbf',
	'api279.dbf',
	'api281.dbf',
	'api283.dbf',
	'api285.dbf',
	'api287.dbf',
	'api289.dbf',
	'api291.dbf',
	'api293.dbf',
	'api295.dbf',
	'api297.dbf',
	'api299.dbf',
	'api301.dbf',
	'api303.dbf',
	'api305.dbf',
	'api307.dbf',
	'api309.dbf',
	'api311.dbf',
	'api313.dbf',
	'api315.dbf',
	'api317.dbf',
	'api319.dbf',
	'api321.dbf',
	'api323.dbf',
	'api325.dbf',
	'api327.dbf',
	'api329.dbf',
	'api331.dbf',
	'api333.dbf',
	'api335.dbf',
	'api337.dbf',
	'api339.dbf',
	'api341.dbf',
	'api343.dbf',
	'api345.dbf',
	'api347.dbf',
	'api349.dbf',
	'api351.dbf',
	'api353.dbf',
	'api355.dbf',
	'api357.dbf',
	'api359.dbf',
	'api361.dbf',
	'api363.dbf',
	'api365.dbf',
	'api367.dbf',
	'api369.dbf',
	'api371.dbf',
	'api373.dbf',
	'api375.dbf',
	'api377.dbf',
	'api379.dbf',
	'api381.dbf',
	'api383.dbf',
	'api385.dbf',
	'api387.dbf',
	'api389.dbf',
	'api391.dbf',
	'api393.dbf',
	'api395.dbf',
	'api397.dbf',
	'api399.dbf',
	'api401.dbf',
	'api403.dbf',
	'api405.dbf',
	'api407.dbf',
	'api409.dbf',
	'api411.dbf',
	'api413.dbf',
	'api415.dbf',
	'api417.dbf',
	'api419.dbf',
	'api421.dbf',
	'api423.dbf',
	'api425.dbf',
	'api427.dbf',
	'api429.dbf',
	'api431.dbf',
	'api433.dbf',
	'api435.dbf',
	'api437.dbf',
	'api439.dbf',
	'api441.dbf',
	'api443.dbf',
	'api445.dbf',
	'api447.dbf',
	'api449.dbf',
	'api451.dbf',
	'api453.dbf',
	'api455.dbf',
	'api457.dbf',
	'api459.dbf',
	'api461.dbf',
	'api463.dbf',
	'api465.dbf',
	'api467.dbf',
	'api469.dbf',
	'api471.dbf',
	'api473.dbf',
	'api475.dbf',
	'api477.dbf',
	'api479.dbf',
	'api481.dbf',
	'api483.dbf',
	'api485.dbf',
	'api487.dbf',
	'api489.dbf',
	'api491.dbf',
	'api493.dbf',
	'api495.dbf',
	'api497.dbf',
	'api499.dbf',
	'api501.dbf',
	'api503.dbf',
	'api505.dbf',
	'api507.dbf'
]

SQL_SERVER = "HAL-2017"
PROCESS_CODE = 1

MONTH_NOS = {
	'JAN': '01',
	'FEB': '02',
	'MAR': '03',
	'APR': '04',
	'MAY': '05',
	'JUN': '06',
	'JUL': '07',
	'AUG': '08',
	'SEP': '09',
	'OCT': '10',
	'NOV': '11',
	'DEC': '12'
}
MONTH_NUMS = {
	'JANUARY'  : '01',
	'FEBRUARY' : '02',
	'MARCH'    : '03',
	'APRIL'    : '04',
	'MAY'      : '05',
	'JUNE'     : '06',
	'JULY'     : '07',
	'AUGUST'   : '08',
	'SEPTEMBER': '09',
	'OCTOBER'  : '10',
	'NOVEMBER' : '11',
	'DECEMBER' : '12'
}
MONTH_NAMES = {
	'01': 'jan',
	'02': 'feb',
	'03': 'mar',
	'04': 'apr',
	'05': 'may',
	'06': 'jun',
	'07': 'jul',
	'08': 'aug',
	'09': 'sep',
	'10': 'oct',
	'11': 'nov',
	'12': 'dec'
}
MONTHS = [
	'jan',
	'feb',
	'mar',
	'apr',
	'may',
	'jun',
	'jul',
	'aug',
	'sep',
	'oct',
	'nov',
	'dec'
]
MONTH_NUM_LIST = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
PROD_DATES = ['{}{}'.format(year_num, month_num) for year_num in range(1900, 2200) for month_num in MONTH_NUM_LIST]

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

PROD_PCT_COLS = [
	'lease_id',
	'tx_well_id',
	'prod_year',
	'jan_prod_pct',
	'feb_prod_pct',
	'mar_prod_pct',
	'apr_prod_pct',
	'may_prod_pct',
	'jun_prod_pct',
	'jul_prod_pct',
	'aug_prod_pct',
	'sep_prod_pct',
	'oct_prod_pct',
	'nov_prod_pct',
	'dec_prod_pct'
]

WELLBORE_NUMS = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(wellbore_num) for wellbore_num in
                                                                                range(10, 100)]
WELLBORE_NUMS = sorted(WELLBORE_NUMS)

'''
- Download zipfile of production data to DATA_DIR from url:
	ftp://ftpe.rrc.texas.gov/shpdqdmp/PDQ_DSV.zip
- Unzip file and move OG_COUNTY_LEASE_CYCLE_DATA_TABLE.dsv to TX_PROD_DIR
- Split file into multiple 100MB files and move to :\\GlobalData\\Data\\tx_data\\tx_production\\
- Remove the following characters from dsv file:
	, . ' "
- Replace each } with a , and save as csv file
- Create table using:
	CREATE TABLE tx_og_county_lease_cycle_update
	(
		OIL_GAS_CODE				VARCHAR(1)   DEFAULT NULL,
		DISTRICT_NO					VARCHAR(2)   DEFAULT NULL,
		LEASE_NO					VARCHAR(6)   DEFAULT NULL,
		CYCLE_YEAR					INT          DEFAULT NULL,
		CYCLE_MONTH					VARCHAR(2)   DEFAULT NULL,
		COUNTY_NO					VARCHAR(3)   DEFAULT NULL,
		OPERATOR_NO					BIGINT       DEFAULT NULL,
		FIELD_NO					BIGINT       DEFAULT NULL,
		CYCLE_YEAR_MONTH			VARCHAR(6)   DEFAULT NULL,
		FIELD_TYPE					VARCHAR(10)  DEFAULT NULL,
		GAS_WELL_NO					VARCHAR(10)  DEFAULT NULL,
		PROD_REPORT_FILED_FLAG		VARCHAR(2)   DEFAULT NULL,
		CNTY_LSE_OIL_PROD_VOL		FLOAT        DEFAULT NULL,
		CNTY_LSE_OIL_ALLOW			FLOAT        DEFAULT NULL,
		CNTY_LSE_OIL_ENDING_BAL		FLOAT        DEFAULT NULL,
		CNTY_LSE_GAS_PROD_VOL		FLOAT        DEFAULT NULL,
		CNTY_LSE_GAS_ALLOW			FLOAT        DEFAULT NULL,
		CNTY_LSE_GAS_LIFT_INJ_VOL	FLOAT        DEFAULT NULL,
		CNTY_LSE_COND_PROD_VOL		FLOAT        DEFAULT NULL,
		CNTY_LSE_COND_LIMIT			FLOAT        DEFAULT NULL,
		CNTY_LSE_COND_ENDING_BAL	FLOAT        DEFAULT NULL,
		CNTY_LSE_CSGD_PROD_VOL		FLOAT        DEFAULT NULL,
		CNTY_LSE_CSGD_LIMIT			FLOAT        DEFAULT NULL,
		CNTY_LSE_CSGD_GAS_LIFT		FLOAT        DEFAULT NULL,
		CNTY_LSE_OIL_TOT_DISP		FLOAT        DEFAULT NULL,
		CNTY_LSE_GAS_TOT_DISP		FLOAT        DEFAULT NULL,
		CNTY_LSE_COND_TOT_DISP		FLOAT        DEFAULT NULL,
		CNTY_LSE_CSGD_TOT_DISP		FLOAT        DEFAULT NULL,
		DISTRICT_NAME				VARCHAR(150) DEFAULT NULL,
		LEASE_NAME					VARCHAR(150) DEFAULT NULL,
		OPERATOR_NAME				VARCHAR(150) DEFAULT NULL,
		FIELD_NAME					VARCHAR(150) DEFAULT NULL,
		COUNTY_NAME					VARCHAR(150) DEFAULT NULL
	)
	GO

	CREATE INDEX county_no_indx
	  ON tx_og_county_lease_cycle_update (county_no)
	GO

	CREATE INDEX district_no_indx
	  ON tx_og_county_lease_cycle_update (district_no)
	GO

	CREATE INDEX field_no_indx
	  ON tx_og_county_lease_cycle_update (field_no)
	GO

	CREATE INDEX lease_no_indx
	  ON tx_og_county_lease_cycle_update (lease_no)
	GO

	CREATE INDEX lease_well_district_indx
	  ON tx_og_county_lease_cycle_update (lease_no, gas_well_no, district_no)
	GO

	CREATE INDEX lease_well_district_og_code_county_field_indx
	  ON tx_og_county_lease_cycle_update (lease_no, gas_well_no, district_no, oil_gas_code, county_no, field_no)
	GO

	CREATE INDEX lease_well_district_og_code_county_field_operator_indx
	  ON tx_og_county_lease_cycle_update (lease_no, gas_well_no, district_no, oil_gas_code, county_no, field_no, operator_no)
	GO

	CREATE INDEX lease_well_district_og_code_county_field_operator_prod_date_indx
	  ON tx_og_county_lease_cycle_update (lease_no, gas_well_no, district_no, oil_gas_code, county_no, field_no, operator_no, cycle_year_month)
	GO

	CREATE INDEX lease_well_district_og_code_county_indx
	  ON tx_og_county_lease_cycle_update (lease_no, gas_well_no, district_no, oil_gas_code, county_no)
	GO

	CREATE INDEX lease_well_district_og_code_indx
	  ON tx_og_county_lease_cycle_update (lease_no, gas_well_no, district_no, oil_gas_code)
	GO

	CREATE INDEX oil_gas_code_indx
	  ON tx_og_county_lease_cycle_update (oil_gas_code)
	GO

	CREATE INDEX operator_no_indx
	  ON tx_og_county_lease_cycle_update (operator_no)
	GO

	CREATE INDEX prod_date_indx
	  ON tx_og_county_lease_cycle_update (cycle_year_month)
	GO

	CREATE INDEX prod_month_indx
	  ON tx_og_county_lease_cycle_update (cycle_month)
	GO

	CREATE INDEX prod_year_indx
	  ON tx_og_county_lease_cycle_update (cycle_year)
	GO

	CREATE INDEX well_no_indx
	  ON tx_og_county_lease_cycle_update (gas_well_no)
	GO
- Load csv file to SQL Server table US_Wells_Texas.dbo.tx_og_county_lease_cycle_update


'''


# --------------------------------------------------------------------------------------------------------------------------------------------

def move_files(src_dir, dst_dir, file_extn='xlsx', outfile_code=''):
	for asset_model in [filename for filename in os.listdir(src_dir) if filename.endswith(file_extn)]:
		print src_dir + asset_model
		shutil.move(src_dir + asset_model, dst_dir + asset_model)


def copy_files(src_dir, dst_dir, in_ext='', out_ext='', out_format='{}.{}', fname_indx=None, fname_incr=False):
	if fname_indx == None:
		fname_indx = -(len(in_ext) + 1)
	input_files = [filename for filename in os.listdir(src_dir) if filename.endswith(in_ext)]
	input_file_num = 0
	input_file_count = len(input_files)
	for input_file in input_files:
		input_filename = input_file[:fname_indx]
		if fname_incr:
			output_file = out_format.format(input_filename, input_file_num, out_ext)
		else:
			output_file = out_format.format(input_filename, out_ext)
		print '({}/{}): {} ---> {}'.format(input_file_num, input_file_count, src_dir + input_file,
		                                   dst_dir + output_file)
		shutil.copy2(src_dir + input_file, dst_dir + output_file)
		input_file_num += 1


def unzip_file(zipfile_dir, unzip_dir):
	with ZipFile(zipfile_dir) as zf:
		zf.extractall(unzip_dir)


def download_zipfile(url, output_dir, output_file, unzip=False, delete_zip=False):
	out_filename = output_dir + output_file + '.zip'
	zipfile = urllib.urlretrieve(url, out_filename)
	if unzip:
		unzip_file(out_filename, output_dir + output_file)
		if delete_zip:
			os.remove(out_filename)


def download_file(url, output_dir, output_file):
	out_filename = output_dir + output_file
	urllib.urlretrieve(url, out_filename)


def import_csv_to_sql(data_dir, table_name, truncate=False):
	if truncate:
		conn = gd.get_connection(server='sql_server', database='US_Wells_Texas', us_wells=True)
		curr = conn.cursor()
		curr.execute('TRUNCATE TABLE {}'.format(table_name))
		gd.commit(curr)
		curr.close()
		conn.close()
	data_files = [datafile for datafile in os.listdir(data_dir) if datafile[-4:] == '.csv']
	for data_file in data_files:
		print '\nProcessing {} to {}...'.format(data_file, table_name)
		total_rows = 0
		dframes = []
		df = pd.read_csv(data_dir + data_file, delimiter=',', low_memory=False)
		dframes.append(df)
		prod_data = pd.concat(dframes)
		print prod_data.shape[0], 'rows in table'
		params = urllib.quote_plus(
			"Driver={SQL Server}; Server=(local); Database=US_Wells_Texas; Trusted_Connection=True; unicode_results=True;")
		engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
		prod_data.to_sql(name=table_name, con=engine, if_exists="append", chunksize=10000, index=False)
		print '{} complete'.format(data_file)


# Production Data --------------------------------------------------------------------------------------------

def retrieve_prod_file():
	download_file(url=TX_PROD_URL, output_dir=TX_DATA_DIR, output_file=TX_PROD_ZIP)
	unzip_file(zipfile_dir=TX_DATA_DIR + TX_PROD_ZIP, unzip_dir=TX_PROD_FILES_DIR)
	shutil.move(TX_PROD_FILES_DIR + TX_PROD_FILE, TX_PROD_DIR + TX_PROD_FILE)


def configure_prod_file(input_dir=TX_PROD_FILES_DIR, output_dir=TX_PROD_OUT_DIR, output_filename=OUTPUT_FILE):
	for prod_file in [in_file for in_file in os.listdir(input_dir) if in_file[-3:] == 'dsv']:
		output_txt = ''
		print '\n', '{} Processing input file at {}{} ...'.format(gd.get_datetime(), input_dir, prod_file)
		with open(input_dir + prod_file) as input_prod_file:
			output_txt = input_prod_file.read()
			output_txt = output_txt.replace(',', '')
			output_txt = output_txt.replace('.', '')
			output_txt = output_txt.replace('"', '')
			output_txt = output_txt.replace("'", "")
			output_txt = output_txt.replace('}', ',')
		print '{} Saving output file at {}{} ...'.format(prod_file, output_dir, output_filename)
		with open(output_dir + output_filename, 'a') as output_prod_file:
			output_prod_file.write(output_txt)


def clear_production_tables():
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	sql_update = \
	"""
	TRUNCATE TABLE tx_production;
	TRUNCATE TABLE tx_production_data;
	TRUNCATE TABLE tx_well_production;
	TRUNCATE TABLE tx_oil_production_data;
	"""
	curr.execute(sql_update)
	gd.commit(curr)
	curr.close()
	conn.close()


def update_production_data():
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()

	sql_update_tx_prod_data = \
	"""
	TRUNCATE TABLE tx_production_data;
	
	INSERT INTO tx_production_data (oil_gas_code, district_no, lease_no, prod_year, prod_month, county_no, operator_no, field_no, prod_date, field_type, well_no, oil_prod_vol, gas_prod_vol, gas_lift_inj_vol, cond_prod_vol, csgd_prod_vol)
	  (SELECT DISTINCT OIL_GAS_CODE, DISTRICT_NO, LEASE_NO, CYCLE_YEAR, CYCLE_MONTH, COUNTY_NO, OPERATOR_NO, FIELD_NO, CYCLE_YEAR_MONTH, FIELD_TYPE, GAS_WELL_NO, CNTY_LSE_OIL_PROD_VOL, CNTY_LSE_GAS_PROD_VOL, CNTY_LSE_GAS_LIFT_INJ_VOL, CNTY_LSE_COND_PROD_VOL, CNTY_LSE_CSGD_PROD_VOL
	   FROM tx_og_county_lease_cycle_update);
	
	UPDATE tx_production_data SET well_no=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(well_no,'\\',''),'-',''),'_',''),'\t',''),'{',''),' ',''),'''',''),'"','') WHERE NOT well_no IS NULL;
	
	UPDATE tx_production_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_production_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_production_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_production_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_production_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_production_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_production_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_production_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_production_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_production_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	
	UPDATE tx_production_data SET well_no=NULL WHERE LEN(well_no)=0;
	
	UPDATE tx_production_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)=1;
	UPDATE tx_production_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)=2;
	UPDATE tx_production_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)=3;
	UPDATE tx_production_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)=4;
	UPDATE tx_production_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)=5;
	
	UPDATE tx_production_data SET district_no=CONCAT('0',district_no) WHERE LEN(district_no)=1;
	
	UPDATE tx_production_data SET county_no=CONCAT('0',county_no) WHERE LEN(county_no)=1;
	UPDATE tx_production_data SET county_no=CONCAT('0',county_no) WHERE LEN(county_no)=2;
	
	UPDATE tx_production_data SET lease_id=CONCAT(oil_gas_code,district_no,county_no,lease_no) WHERE lease_id IS NULL;
	"""
	sql_update_tx_well_prod = \
		"""
	TRUNCATE TABLE tx_well_production;
	
	INSERT INTO tx_well_production (LEASE_ID, PROD_YEAR, LEASE_NO, DISTRICT_NO, COUNTY_NO, OIL_GAS_CODE, FIELD_NO, OPERATOR_NO, WELL_NO)
	  (SELECT DISTINCT LEASE_ID, PROD_YEAR, LEASE_NO, DISTRICT_NO, COUNTY_NO, OIL_GAS_CODE, FIELD_NO, OPERATOR_NO, WELL_NO
	   FROM tx_production_data);
	
	UPDATE tx_well_production
	  SET GAS_JAN_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_JAN_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_JAN_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_JAN_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=1;
	
	UPDATE tx_well_production
	  SET GAS_FEB_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_FEB_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_FEB_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_FEB_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=2;
	
	UPDATE tx_well_production
	  SET GAS_MAR_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_MAR_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_MAR_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_MAR_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=3;
	
	UPDATE tx_well_production
	  SET GAS_APR_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_APR_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_APR_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_APR_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=4;
	
	UPDATE tx_well_production
	  SET GAS_MAY_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_MAY_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_MAY_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_MAY_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=5;
	
	UPDATE tx_well_production
	  SET GAS_JUN_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_JUN_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_JUN_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_JUN_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=6;
	
	UPDATE tx_well_production
	  SET GAS_JUL_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_JUL_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_JUL_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_JUL_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=7;
	
	UPDATE tx_well_production
	  SET GAS_AUG_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_AUG_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_AUG_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_AUG_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=8;
	
	UPDATE tx_well_production
	  SET GAS_SEP_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_SEP_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_SEP_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_SEP_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=9;
	
	UPDATE tx_well_production
	  SET GAS_OCT_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_OCT_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_OCT_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_OCT_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=10;
	
	UPDATE tx_well_production
	  SET GAS_NOV_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_NOV_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_NOV_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_NOV_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=11;
	
	UPDATE tx_well_production
	  SET GAS_DEC_MCF=ISNULL(b.gas_prod_vol,0),
		  OIL_DEC_BBL=ISNULL(b.oil_prod_vol,0),
		  CSGD_DEC_MCF=ISNULL(b.csgd_prod_vol,0),
		  COND_DEC_BBL=ISNULL(b.cond_prod_vol,0)
	  FROM tx_well_production a, tx_production_data b
	  WHERE a.PROD_YEAR=b.prod_year AND a.LEASE_NO=b.lease_no AND a.DISTRICT_NO=b.district_no AND a.COUNTY_NO=b.county_no AND a.OIL_GAS_CODE=b.oil_gas_code AND a.FIELD_NO=b.field_no AND a.OPERATOR_NO=b.operator_no AND ISNULL(a.WELL_NO,'')=ISNULL(b.well_no,'') AND b.prod_month=12;
	
	UPDATE tx_well_production
	  SET Gas_Jan_mcf=ISNULL(Gas_Jan_mcf,0),
		  Gas_Feb_mcf=ISNULL(Gas_Feb_mcf,0),
		  Gas_Mar_mcf=ISNULL(Gas_Mar_mcf,0),
		  Gas_Apr_mcf=ISNULL(Gas_Apr_mcf,0),
		  Gas_May_mcf=ISNULL(Gas_May_mcf,0),
		  Gas_Jun_mcf=ISNULL(Gas_Jun_mcf,0),
		  Gas_Jul_mcf=ISNULL(Gas_Jul_mcf,0),
		  Gas_Aug_mcf=ISNULL(Gas_Aug_mcf,0),
		  Gas_Sep_mcf=ISNULL(Gas_Sep_mcf,0),
		  Gas_Oct_mcf=ISNULL(Gas_Oct_mcf,0),
		  Gas_Nov_mcf=ISNULL(Gas_Nov_mcf,0),
		  Gas_Dec_mcf=ISNULL(Gas_Dec_mcf,0),
		  Oil_Jan_bbl=ISNULL(Oil_Jan_bbl,0),
		  Oil_Feb_bbl=ISNULL(Oil_Feb_bbl,0),
		  Oil_Mar_bbl=ISNULL(Oil_Mar_bbl,0),
		  Oil_Apr_bbl=ISNULL(Oil_Apr_bbl,0),
		  Oil_May_bbl=ISNULL(Oil_May_bbl,0),
		  Oil_Jun_bbl=ISNULL(Oil_Jun_bbl,0),
		  Oil_Jul_bbl=ISNULL(Oil_Jul_bbl,0),
		  Oil_Aug_bbl=ISNULL(Oil_Aug_bbl,0),
		  Oil_Sep_bbl=ISNULL(Oil_Sep_bbl,0),
		  Oil_Oct_bbl=ISNULL(Oil_Oct_bbl,0),
		  Oil_Nov_bbl=ISNULL(Oil_Nov_bbl,0),
		  Oil_Dec_bbl=ISNULL(Oil_Dec_bbl,0),
		  Cond_Jan_bbl=ISNULL(Cond_Jan_bbl,0),
		  Cond_Feb_bbl=ISNULL(Cond_Feb_bbl,0),
		  Cond_Mar_bbl=ISNULL(Cond_Mar_bbl,0),
		  Cond_Apr_bbl=ISNULL(Cond_Apr_bbl,0),
		  Cond_May_bbl=ISNULL(Cond_May_bbl,0),
		  Cond_Jun_bbl=ISNULL(Cond_Jun_bbl,0),
		  Cond_Jul_bbl=ISNULL(Cond_Jul_bbl,0),
		  Cond_Aug_bbl=ISNULL(Cond_Aug_bbl,0),
		  Cond_Sep_bbl=ISNULL(Cond_Sep_bbl,0),
		  Cond_Oct_bbl=ISNULL(Cond_Oct_bbl,0),
		  Cond_Nov_bbl=ISNULL(Cond_Nov_bbl,0),
		  Cond_Dec_bbl=ISNULL(Cond_Dec_bbl,0),
		  CSGD_Jan_mcf=ISNULL(CSGD_Jan_mcf,0),
		  CSGD_Feb_mcf=ISNULL(CSGD_Feb_mcf,0),
		  CSGD_Mar_mcf=ISNULL(CSGD_Mar_mcf,0),
		  CSGD_Apr_mcf=ISNULL(CSGD_Apr_mcf,0),
		  CSGD_May_mcf=ISNULL(CSGD_May_mcf,0),
		  CSGD_Jun_mcf=ISNULL(CSGD_Jun_mcf,0),
		  CSGD_Jul_mcf=ISNULL(CSGD_Jul_mcf,0),
		  CSGD_Aug_mcf=ISNULL(CSGD_Aug_mcf,0),
		  CSGD_Sep_mcf=ISNULL(CSGD_Sep_mcf,0),
		  CSGD_Oct_mcf=ISNULL(CSGD_Oct_mcf,0),
		  CSGD_Nov_mcf=ISNULL(CSGD_Nov_mcf,0),
		  CSGD_Dec_mcf=ISNULL(CSGD_Dec_mcf,0);
	
	UPDATE tx_well_production
	  SET Gas_TOTAL_mcf=ROUND((ISNULL(Gas_Jan_mcf,0) + ISNULL(Gas_Feb_mcf,0) + ISNULL(Gas_Mar_mcf,0) + ISNULL(Gas_Apr_mcf,0) + ISNULL(Gas_May_mcf,0) + ISNULL(Gas_Jun_mcf,0) + ISNULL(Gas_Jul_mcf,0) + ISNULL(Gas_Aug_mcf,0) + ISNULL(Gas_Sep_mcf,0) + ISNULL(Gas_Oct_mcf,0) + ISNULL(Gas_Nov_mcf,0) + ISNULL(Gas_Dec_mcf,0)),2),
		  Oil_TOTAL_bbl=ROUND((ISNULL(Oil_Jan_bbl,0) + ISNULL(Oil_Feb_bbl,0) + ISNULL(Oil_Mar_bbl,0) + ISNULL(Oil_Apr_bbl,0) + ISNULL(Oil_May_bbl,0) + ISNULL(Oil_Jun_bbl,0) + ISNULL(Oil_Jul_bbl,0) + ISNULL(Oil_Aug_bbl,0) + ISNULL(Oil_Sep_bbl,0) + ISNULL(Oil_Oct_bbl,0) + ISNULL(Oil_Nov_bbl,0) + ISNULL(Oil_Dec_bbl,0)),2),
		  CSGD_TOTAL_MCF=ROUND((ISNULL(CSGD_Jan_MCF,0) + ISNULL(CSGD_Feb_MCF,0) + ISNULL(CSGD_Mar_MCF,0) + ISNULL(CSGD_Apr_MCF,0) + ISNULL(CSGD_May_MCF,0) + ISNULL(CSGD_Jun_MCF,0) + ISNULL(CSGD_Jul_MCF,0) + ISNULL(CSGD_Aug_MCF,0) + ISNULL(CSGD_Sep_MCF,0) + ISNULL(CSGD_Oct_MCF,0) + ISNULL(CSGD_Nov_MCF,0) + ISNULL(CSGD_Dec_MCF,0)),2),
		  COND_TOTAL_bbl=ROUND((ISNULL(COND_Jan_bbl,0) + ISNULL(COND_Feb_bbl,0) + ISNULL(COND_Mar_bbl,0) + ISNULL(COND_Apr_bbl,0) + ISNULL(COND_May_bbl,0) + ISNULL(COND_Jun_bbl,0) + ISNULL(COND_Jul_bbl,0) + ISNULL(COND_Aug_bbl,0) + ISNULL(COND_Sep_bbl,0) + ISNULL(COND_Oct_bbl,0) + ISNULL(COND_Nov_bbl,0) + ISNULL(COND_Dec_bbl,0)),2);
	
	UPDATE tx_well_production
	  SET well_no=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(well_no,'\\',' '),'-',' '),'_',' '),'\t',' '),'{',''),'''',''),'"',''),'#',''),'/',' '),'.',''),',',' '),'  ',' '),'  ',' ')
	  WHERE well_no IS NOT NULL;
	
	UPDATE tx_well_production
	  SET well_no=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(well_no,'\\',''),'-',''),'_',''),'\t',''),'{',''),' ',''),'''',''),'"','')
	  WHERE well_no IS NOT NULL;
	
	UPDATE tx_well_production SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_production SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_production SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_production SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_production SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_production SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_production SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_production SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_production SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_production SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	
	UPDATE tx_well_production SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)<6;
	UPDATE tx_well_production SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)<6;
	UPDATE tx_well_production SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)<6;
	UPDATE tx_well_production SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)<6;
	UPDATE tx_well_production SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)<6;
	UPDATE tx_well_production SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no)<6;
	
	UPDATE tx_well_production SET county_no=CONCAT('0',county_no) WHERE LEN(county_no)<3;
	UPDATE tx_well_production SET county_no=CONCAT('0',county_no) WHERE LEN(county_no)<3;
	UPDATE tx_well_production SET county_no=CONCAT('0',county_no) WHERE LEN(county_no)<3;
	
	UPDATE tx_well_production SET district_no=CONCAT('0',district_no) WHERE LEN(district_no)<2;
	"""
	sql_update_tx_prod = \
		"""
	TRUNCATE TABLE tx_production;
	TRUNCATE TABLE tx_og_county_lease_cycle_update;
	
	INSERT INTO tx_production (lease_id, prod_year, gas_total_mcf, oil_total_bbl, cond_total_bbl, csgd_total_mcf, gas_jan_mcf, gas_feb_mcf, gas_mar_mcf, gas_apr_mcf, gas_may_mcf, gas_jun_mcf, gas_jul_mcf, gas_aug_mcf, gas_sep_mcf, gas_oct_mcf, gas_nov_mcf, gas_dec_mcf, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, cond_jan_bbl, cond_feb_bbl, cond_mar_bbl, cond_apr_bbl, cond_may_bbl, cond_jun_bbl, cond_jul_bbl, cond_aug_bbl, cond_sep_bbl, cond_oct_bbl, cond_nov_bbl, cond_dec_bbl, csgd_jan_mcf, csgd_feb_mcf, csgd_mar_mcf, csgd_apr_mcf, csgd_may_mcf, csgd_jun_mcf, csgd_jul_mcf, csgd_aug_mcf, csgd_sep_mcf, csgd_oct_mcf, csgd_nov_mcf, csgd_dec_mcf, process_code)
	  (SELECT DISTINCT lease_id, prod_year,
			  SUM(gas_total_mcf) AS gas_total_mcf_sum,
			  SUM(oil_total_bbl) AS oil_total_bbl_sum,
			  SUM(cond_total_bbl) AS cond_total_bbl_sum,
			  SUM(csgd_total_mcf) AS csgd_total_mcf_sum,
			  SUM(gas_jan_mcf) AS gas_jan_mcf_sum,
			  SUM(gas_feb_mcf) AS gas_feb_mcf_sum,
			  SUM(gas_mar_mcf) AS gas_mar_mcf_sum,
			  SUM(gas_apr_mcf) AS gas_apr_mcf_sum,
			  SUM(gas_may_mcf) AS gas_may_mcf_sum,
			  SUM(gas_jun_mcf) AS gas_jun_mcf_sum,
			  SUM(gas_jul_mcf) AS gas_jul_mcf_sum,
			  SUM(gas_aug_mcf) AS gas_aug_mcf_sum,
			  SUM(gas_sep_mcf) AS gas_sep_mcf_sum,
			  SUM(gas_oct_mcf) AS gas_oct_mcf_sum,
			  SUM(gas_nov_mcf) AS gas_nov_mcf_sum,
			  SUM(gas_dec_mcf) AS gas_dec_mcf_sum,
			  SUM(oil_jan_bbl) AS oil_jan_bbl_sum,
			  SUM(oil_feb_bbl) AS oil_feb_bbl_sum,
			  SUM(oil_mar_bbl) AS oil_mar_bbl_sum,
			  SUM(oil_apr_bbl) AS oil_apr_bbl_sum,
			  SUM(oil_may_bbl) AS oil_may_bbl_sum,
			  SUM(oil_jun_bbl) AS oil_jun_bbl_sum,
			  SUM(oil_jul_bbl) AS oil_jul_bbl_sum,
			  SUM(oil_aug_bbl) AS oil_aug_bbl_sum,
			  SUM(oil_sep_bbl) AS oil_sep_bbl_sum,
			  SUM(oil_oct_bbl) AS oil_oct_bbl_sum,
			  SUM(oil_nov_bbl) AS oil_nov_bbl_sum,
			  SUM(oil_dec_bbl) AS oil_dec_bbl_sum,
			  SUM(cond_jan_bbl) AS cond_jan_bbl_sum,
			  SUM(cond_feb_bbl) AS cond_feb_bbl_sum,
			  SUM(cond_mar_bbl) AS cond_mar_bbl_sum,
			  SUM(cond_apr_bbl) AS cond_apr_bbl_sum,
			  SUM(cond_may_bbl) AS cond_may_bbl_sum,
			  SUM(cond_jun_bbl) AS cond_jun_bbl_sum,
			  SUM(cond_jul_bbl) AS cond_jul_bbl_sum,
			  SUM(cond_aug_bbl) AS cond_aug_bbl_sum,
			  SUM(cond_sep_bbl) AS cond_sep_bbl_sum,
			  SUM(cond_oct_bbl) AS cond_oct_bbl_sum,
			  SUM(cond_nov_bbl) AS cond_nov_bbl_sum,
			  SUM(cond_dec_bbl) AS cond_dec_bbl_sum,
			  SUM(csgd_jan_mcf) AS csgd_jan_mcf_sum,
			  SUM(csgd_feb_mcf) AS csgd_feb_mcf_sum,
			  SUM(csgd_mar_mcf) AS csgd_mar_mcf_sum,
			  SUM(csgd_apr_mcf) AS csgd_apr_mcf_sum,
			  SUM(csgd_may_mcf) AS csgd_may_mcf_sum,
			  SUM(csgd_jun_mcf) AS csgd_jun_mcf_sum,
			  SUM(csgd_jul_mcf) AS csgd_jul_mcf_sum,
			  SUM(csgd_aug_mcf) AS csgd_aug_mcf_sum,
			  SUM(csgd_sep_mcf) AS csgd_sep_mcf_sum,
			  SUM(csgd_oct_mcf) AS csgd_oct_mcf_sum,
			  SUM(csgd_nov_mcf) AS csgd_nov_mcf_sum,
			  SUM(csgd_dec_mcf) AS csgd_dec_mcf_sum,
			  0
	  FROM tx_well_production
	  GROUP BY lease_id, prod_year);
	
	
	UPDATE tx_production SET oil_gas_code=SUBSTRING(lease_id,1,1), district_no=SUBSTRING(lease_id,2,2), county_no=SUBSTRING(lease_id,4,3), lease_no=SUBSTRING(lease_id,7,6) WHERE LEN(lease_id)=12;
	
	UPDATE tx_production SET well_no=b.well_no
	  FROM tx_production a, tx_well_production b
	  WHERE a.oil_gas_code='G' AND a.lease_id=b.lease_id AND a.prod_year=b.prod_year;
	
	UPDATE tx_production SET tx_well_id=b.tx_well_id
	  FROM tx_production a, tx_ref_well_id b
	  WHERE a.oil_gas_code='G' AND a.well_no=b.well_no AND a.lease_id=b.lease_id AND a.tx_well_id IS NULL;
	
	UPDATE tx_production SET tx_well_id=b.tx_well_id
	  FROM tx_production a, tx_ref_well_id b
	  WHERE a.oil_gas_code='G' AND a.oil_gas_code=b.oil_gas_code AND a.well_no=b.well_no AND a.lease_no=b.lease_no AND a.tx_well_id IS NULL;
	
	UPDATE tx_production SET tx_well_id=b.tx_well_id
	  FROM tx_production a, tx_ref_well_id b
	  WHERE a.oil_gas_code='G' AND a.lease_id=b.lease_id AND a.tx_well_id IS NULL;
	
	UPDATE tx_production SET process_code=0;
	
	UPDATE tx_production SET process_code=1
	  FROM tx_production a, (SELECT DISTINCT lease_id FROM tx_ref_well_id) b
	  WHERE a.lease_id=b.lease_id AND a.lease_id IS NOT NULL AND LEN(b.lease_id)=12;
	
	UPDATE tx_production SET process_code=2
	  FROM tx_production a, (SELECT DISTINCT lease_no, oil_gas_code, county_no FROM tx_ref_well_id) b
	  WHERE a.lease_no=b.lease_no AND a.lease_id IS NOT NULL AND a.oil_gas_code=b.oil_gas_code AND a.county_no=b.county_no AND a.process_code!=1;
	
	UPDATE tx_production SET process_code=3
	  FROM tx_production a, (SELECT DISTINCT lease_no, oil_gas_code FROM tx_ref_well_id) b
	  WHERE a.lease_no=b.lease_no AND a.lease_id IS NOT NULL AND a.oil_gas_code=b.oil_gas_code AND NOT a.process_code IN (1,2);
	  
	UPDATE tx_production SET process_code=4 WHERE process_code=0 AND (gas_total_mcf+oil_total_bbl+cond_total_bbl+csgd_total_mcf)=0; 
	  
	DELETE FROM US_Wells_Texas.dbo.tx_production WHERE US_Wells_Texas.dbo.tx_production.lease_id='O08429003863';

	UPDATE tx_production SET orig_lease_id=lease_id WHERE process_code=0;
	
	UPDATE tx_production SET lease_id=b.lease_id
	  FROM tx_production a, tx_ref_well_id b
	  WHERE a.lease_no=b.lease_no AND a.oil_gas_code=b.oil_gas_code AND a.district_no=b.district_no AND a.process_code=0;
	
	UPDATE tx_production SET lease_id=b.lease_id
	  FROM tx_production a, tx_ref_well_id b
	  WHERE a.tx_well_id=b.tx_well_id AND a.tx_well_id IS NOT NULL AND a.process_code=0;
	
	UPDATE tx_production SET lease_id=b.lease_id
	FROM tx_production a, tx_ref_well_id b, tx_production_data c
	WHERE a.well_no=b.well_no AND a.well_no=c.well_no AND a.oil_gas_code=b.oil_gas_code AND a.county_no=b.county_no AND a.district_no=b.district_no AND a.lease_id=c.lease_id  AND b.operator_no=c.operator_no AND c.field_no=b.field_no AND a.process_code=0;

	UPDATE tx_production SET lease_id=b.lease_id
		FROM tx_production a, tx_ref_well_id b, tx_production_data c
		WHERE a.well_no=b.well_no AND a.well_no=c.well_no AND a.oil_gas_code=b.oil_gas_code AND a.county_no=b.county_no AND a.district_no=b.district_no AND a.lease_id=c.lease_id AND c.field_no=b.field_no AND a.process_code=0;

	UPDATE tx_production SET lease_id=b.lease_id
		FROM tx_production a, tx_ref_well_id b, tx_production_data c
		WHERE a.oil_gas_code=b.oil_gas_code AND a.county_no=b.county_no AND a.district_no=b.district_no AND a.lease_id=c.lease_id  AND b.operator_no=c.operator_no AND c.field_no=b.field_no AND a.process_code=0;

	UPDATE tx_production SET lease_id=b.lease_id
		FROM tx_production a, tx_ref_well_id b, tx_production_data c
		WHERE a.oil_gas_code=b.oil_gas_code AND a.county_no=b.county_no AND a.district_no=b.district_no AND a.lease_id=c.lease_id AND c.field_no=b.field_no AND a.process_code=0;
	
	UPDATE tx_production SET lease_id=b.lease_id
		FROM tx_production a, tx_ref_well_id b, tx_production_data c
		WHERE a.oil_gas_code=b.oil_gas_code AND a.district_no=b.district_no AND a.lease_id=c.lease_id AND c.field_no=b.field_no AND a.process_code=0;
	
	UPDATE tx_production SET tx_well_id=b.tx_well_id
		FROM tx_production a, tx_ref_well_id b
		WHERE a.oil_gas_code='G' AND a.lease_id=b.lease_id AND a.tx_well_id IS NULL;
	
	UPDATE tx_production SET process_code=1
		FROM tx_production a, (SELECT DISTINCT lease_id FROM tx_ref_well_id) b
		WHERE a.lease_id=b.lease_id AND a.lease_id IS NOT NULL AND LEN(b.lease_id)=12 AND a.process_code=0;
	
	
	TRUNCATE TABLE tx_well_production;
	TRUNCATE TABLE tx_og_county_lease_cycle_update;
	"""

	print gd.get_datetime(), 'Updating tx_production_data ...'
	curr.execute(sql_update_tx_prod_data)
	gd.commit(curr)

	print gd.get_datetime(), 'Updating tx_well_production ...'
	curr.execute(sql_update_tx_well_prod)
	gd.commit(curr)

	print gd.get_datetime(), 'Updating tx_production ...'
	curr.execute(sql_update_tx_prod)
	gd.commit(curr)

	curr.close()
	conn.close()


def process_production_data(retrieve=False, configure=False, clear=False, update=False):
	# 4 - 5 hours total
	print '{}'.format(gd.get_datetime())
	# 20 - 30 minutes
	if retrieve:
		print 'Retrieving Production files ...'
		retrieve_prod_file()
	# 5 - 10 minutes
	if configure:
		print 'Configuring Lease Production file ...'
		configure_prod_file()
	#  - minutes
	if clear:
		print "Clearing Production Tables ..."
		clear_production_tables()
	# 45 minutes to load csv to database
	# 3 - 5 minutes
	if update:
		print "Updating Production Tables ..."
		update_production_data()
	print '{}'.format(gd.get_datetime())


# Well API Data -----------------------------------------------------------------------------------------------
def archive_api_files():
	move_files(TX_API_DIR, TX_API_ARCHIVE, file_extn='dbf')
	move_files(TX_API_OUT_DIR, TX_API_ARCHIVE + "output\\", file_extn='csv')


def retrieve_api_files():
	for api_file in API_DBF_FILES:
		sleep(1)
		print 'Downloading well data file: {} ...'.format(api_file)
		ftpfile = urllib2.urlopen(API_DBF_URL.format(api_file))
		with open(TX_API_DIR + api_file, "wb") as localfile:
			shutil.copyfileobj(ftpfile, localfile)


def run_dbf_csv_macro():
	xlApp = Dispatch("Excel.Application")
	wb = xlApp.Workbooks.Open(Filename=TX_DATA_DIR + "dbf_to_csv_macro.xlsm")
	xlApp.Application.Run("dbf_to_csv_macro.xlsm!Module1.ConvertDBFfiles")
	wb.SaveAs(TX_DATA_DIR + "dbf_to_csv_macro.xlsm")
	xlApp.Application.Quit()
	del xlApp


def update_well_api_data():
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	sql_update = \
	"""
	TRUNCATE TABLE tx_well_data_master;
	
	INSERT INTO tx_well_data_master (abstract, api_number, block, completion_date, field_name, lease_name, lease_no, oil_gas_code, on_sched, operator, permit_no, plug_date, current_api, section, survery, total_depth, well_no, quadnum, object_id1, drill_permit_no)
	  (SELECT DISTINCT ABSTRACT, APINUM, BLOCK, COMPLETION, FIELD_NAME, LEASE_NAME, GAS_RRCID, OIL_GAS_CO, ON_OFF_SCH, OPERATOR, PERMIT_NUM, PLUG_DATE, REFER_TO_A, SECTION, SURVEY, TOTAL_DEPT, WELLID, QUADNUM, OBJECTID_1, PERMIT_NUM FROM tx_well_data_update);
	
	UPDATE tx_well_data_master SET well_no=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(well_no,'\\',''),'-',''),'_',''),'\t',''),'{',''),' ',''),'''',''),'"','') WHERE NOT well_no IS NULL;
	UPDATE tx_well_data_master SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_data_master SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_data_master SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_data_master SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_data_master SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_data_master SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_data_master SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_data_master SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_data_master SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_well_data_master SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	
	UPDATE tx_well_data_master SET lease_name=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(lease_name,'''',''),'#',''),'(',''),')',''),'-',''),'"',''),'.',''),',','');
	UPDATE tx_well_data_master SET lease_name_str=REPLACE(lease_name,' ','');
	
	UPDATE tx_well_data_master SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_well_data_master SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_well_data_master SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_well_data_master SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_well_data_master SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_well_data_master SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_well_data_master SET lease_no=NULL WHERE lease_no='000000';
	
	UPDATE tx_well_data_master SET district_no=CONCAT('0', district_no) WHERE LEN(district_no) < 2;
	UPDATE tx_well_data_master SET district_no=CONCAT('0', district_no) WHERE LEN(district_no) < 2;

	UPDATE tx_well_data_master SET district_no='14' WHERE district_no='10';
	UPDATE tx_well_data_master SET district_no='10' WHERE district_no='08';
	UPDATE tx_well_data_master SET district_no='08' WHERE district_no='7B';
	UPDATE tx_well_data_master SET district_no='13' WHERE district_no='09';
	UPDATE tx_well_data_master SET district_no='09' WHERE district_no='7C';
	UPDATE tx_well_data_master SET district_no='07' WHERE district_no='6E';
	UPDATE tx_well_data_master SET district_no='11' WHERE district_no='8A';
	UPDATE tx_well_data_master SET district_no='12' WHERE district_no='8B';
	
	UPDATE tx_well_data_master SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_well_data_master SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_well_data_master SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_well_data_master SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_well_data_master SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_well_data_master SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_well_data_master SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_well_data_master SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	
	UPDATE tx_well_data_master SET api_number=CONCAT('42',api_number);
	UPDATE tx_well_data_master SET county_no=SUBSTRING(api_number,3,3);
	
	UPDATE tx_well_data_master SET completion_date=NULL WHERE completion_date=0;
	UPDATE tx_well_data_master SET completion_date=NULL WHERE LEN(completion_date)=0;
	UPDATE tx_well_data_master SET completion_date=SUBSTRING(completion_date,1,6) WHERE completion_date IS NOT NULL;
	UPDATE tx_well_data_master SET completion_date=CONCAT(SUBSTRING(completion_date,1,4),'12') WHERE SUBSTRING(completion_date,5,2)='00' AND completion_date IS NOT NULL;
	UPDATE tx_well_data_master SET completion_date=NULL WHERE LEN(completion_date) < 6;
	UPDATE tx_well_data_master SET completion_date=CONCAT(SUBSTRING(completion_date,1,4),'01') WHERE SUBSTRING(completion_date,5,2) NOT IN ('01','02','03','04','05','06','07','08','09','10','11','12');
	
	
	UPDATE tx_well_data_master SET plug_date=NULL WHERE plug_date=0;
	UPDATE tx_well_data_master SET plug_date=NULL WHERE LEN(plug_date)=0;
	UPDATE tx_well_data_master SET plug_date=SUBSTRING(plug_date,1,6) WHERE plug_date IS NOT NULL;
	UPDATE tx_well_data_master SET plug_date=CONCAT(SUBSTRING(plug_date,1,4),'12') WHERE SUBSTRING(plug_date,5,2)='00' AND plug_date IS NOT NULL;
	
	UPDATE tx_well_data_master SET drill_permit_no=CONCAT('0',drill_permit_no) WHERE LEN(ISNULL(drill_permit_no,'')) < 6;
	UPDATE tx_well_data_master SET drill_permit_no=CONCAT('0',drill_permit_no) WHERE LEN(ISNULL(drill_permit_no,'')) < 6;
	UPDATE tx_well_data_master SET drill_permit_no=CONCAT('0',drill_permit_no) WHERE LEN(ISNULL(drill_permit_no,'')) < 6;
	UPDATE tx_well_data_master SET drill_permit_no=CONCAT('0',drill_permit_no) WHERE LEN(ISNULL(drill_permit_no,'')) < 6;
	UPDATE tx_well_data_master SET drill_permit_no=CONCAT('0',drill_permit_no) WHERE LEN(ISNULL(drill_permit_no,'')) < 6;
	UPDATE tx_well_data_master SET drill_permit_no=CONCAT('0',drill_permit_no) WHERE LEN(ISNULL(drill_permit_no,'')) < 6;
	"""
	curr.execute(sql_update)
	gd.commit(curr)
	curr.close()
	conn.close()


def process_well_api_data(archive=False, retrieve=False, macro=False, import_csv=False, update=False):
	if archive:
		archive_api_files()
	if retrieve:
		print "Retreiving api dbf files from source ..."
		retrieve_api_files()
	if macro:
		print "Converting api dbf files to csv format ..."
		run_dbf_csv_macro()
	if import_csv:
		print "Importing api dbf files to US_Wells_Texas.dbo.tx_well_data_update ..."
		import_csv_to_sql(data_dir=TX_API_OUT_DIR, table_name='tx_well_data_update', truncate=True)
	if update:
		print "Updating well api data ..."
		update_well_api_data()


# Wellbore Data -----------------------------------------------------------------------------------------------

def configure_wellbore_file():
	print 'Processing wellbore file at {}{} ...'.format(TX_WB_DIR, WELLBORE_FILE)
	output_txt = ''
	output_filename = WELLBORE_FILE[:-4] + '_{}.csv'.format(gd.get_date())

	with open(TX_WB_DIR + WELLBORE_FILE) as wellbore_file:
		output_txt = wellbore_file.read()
		output_txt = output_txt.replace('","', '@')
		output_txt = output_txt.replace('"\n"', '\n')
		output_txt = output_txt.replace('.', '')
		output_txt = output_txt.replace('"', '')
		output_txt = output_txt.replace("'", "")
		output_txt = output_txt.replace(',', '')
		output_txt = output_txt.replace('\n', '"\n"')
		output_txt = output_txt.replace('@', '","')
		output_txt = WB_HEADERS + output_txt + '"'
		end_of_file_indx = output_txt.index('\n""\n')
		output_txt = output_txt[:end_of_file_indx]
	print 'Saving output file at {}{} ...'.format(TX_WB_DIR, output_filename)
	with open(TX_WB_DIR + output_filename, 'w') as output_prod_file:
		output_prod_file.write(output_txt)

	print 'Moving {} from {} to {} ...'.format(WELLBORE_FILE, TX_WB_DIR, TX_WB_ARCHIVE)
	shutil.move(TX_WB_DIR + WELLBORE_FILE, TX_WB_ARCHIVE + WELLBORE_FILE)


def update_wellbore_data():
	conn = gd.get_connection(server='sql_server', database='US_Wells_Texas', us_wells=True)
	curr = conn.cursor()
	print 'Updating tx_wellbore_date_lite table ...'
	sql_update = \
	"""
	UPDATE tx_wellbore_data_update SET API_NUMBER=CONCAT('42',API_NUMBER) WHERE LEN(API_NUMBER)=8;
	UPDATE tx_wellbore_data_update SET LEASE_NUMBER=CONCAT('0',LEASE_NUMBER) WHERE LEN(LEASE_NUMBER)=5;
	UPDATE tx_wellbore_data_update SET API_DEPTH=REPLACE(API_DEPTH,'	','');
	UPDATE tx_wellbore_data_update SET WB_SHUT_IN_DEPTH=REPLACE(WB_SHUT_IN_DEPTH,'	','');
	UPDATE tx_wellbore_data_update SET OPERATOR_NUMBER=REPLACE(OPERATOR_NUMBER,'	','');
	UPDATE tx_wellbore_data_update 
	  SET WELL_NO=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
	                      WELL_NO,'\\',''),'-',''),'_',''),'\t',''),'{',''),' ',''),'''',''),'"','');
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	
	UPDATE tx_wellbore_data_update SET DISTRICT_CODE='14' WHERE DISTRICT_CODE='10';
	UPDATE tx_wellbore_data_update SET DISTRICT_CODE='10' WHERE DISTRICT_CODE='08';
	UPDATE tx_wellbore_data_update SET DISTRICT_CODE='08' WHERE DISTRICT_CODE='7B';
	UPDATE tx_wellbore_data_update SET DISTRICT_CODE='13' WHERE DISTRICT_CODE='09';
	UPDATE tx_wellbore_data_update SET DISTRICT_CODE='09' WHERE DISTRICT_CODE='7C';
	UPDATE tx_wellbore_data_update SET DISTRICT_CODE='07' WHERE DISTRICT_CODE='6E';
	UPDATE tx_wellbore_data_update SET DISTRICT_CODE='11' WHERE DISTRICT_CODE='8A';
	UPDATE tx_wellbore_data_update SET DISTRICT_CODE='12' WHERE DISTRICT_CODE='8B';
	UPDATE tx_wellbore_data_update 
	  SET WELL_NO=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
	                      WELL_NO,'\\',''),'-',''),'_',''),'\t',''),'{',''),' ',''),'''',''),'"','') 
	  WHERE NOT WELL_NO IS NULL;
	UPDATE tx_wellbore_data_update SET WELL_NO=SUBSTRING(WELL_NO,2,LEN(WELL_NO)-1) WHERE SUBSTRING(WELL_NO,1,1)='0';
	UPDATE tx_wellbore_data_update SET WELL_NO=SUBSTRING(WELL_NO,2,LEN(WELL_NO)-1) WHERE SUBSTRING(WELL_NO,1,1)='0';
	UPDATE tx_wellbore_data_update SET WELL_NO=SUBSTRING(WELL_NO,2,LEN(WELL_NO)-1) WHERE SUBSTRING(WELL_NO,1,1)='0';
	UPDATE tx_wellbore_data_update SET WELL_NO=SUBSTRING(WELL_NO,2,LEN(WELL_NO)-1) WHERE SUBSTRING(WELL_NO,1,1)='0';
	UPDATE tx_wellbore_data_update SET WELL_NO=SUBSTRING(WELL_NO,2,LEN(WELL_NO)-1) WHERE SUBSTRING(WELL_NO,1,1)='0';
	UPDATE tx_wellbore_data_update SET WELL_NO=SUBSTRING(WELL_NO,2,LEN(WELL_NO)-1) WHERE SUBSTRING(WELL_NO,1,1)='0';
	UPDATE tx_wellbore_data_update SET WELL_NO=SUBSTRING(WELL_NO,2,LEN(WELL_NO)-1) WHERE SUBSTRING(WELL_NO,1,1)='0';
	UPDATE tx_wellbore_data_update SET WELL_NO=SUBSTRING(WELL_NO,2,LEN(WELL_NO)-1) WHERE SUBSTRING(WELL_NO,1,1)='0';
	UPDATE tx_wellbore_data_update SET WELL_NO=SUBSTRING(WELL_NO,2,LEN(WELL_NO)-1) WHERE SUBSTRING(WELL_NO,1,1)='0';
	UPDATE tx_wellbore_data_update SET WELL_NO=SUBSTRING(WELL_NO,2,LEN(WELL_NO)-1) WHERE SUBSTRING(WELL_NO,1,1)='0';
	UPDATE tx_wellbore_data_update 
	  SET LEASE_NAME=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
	                         LEASE_NAME,'''',''),'#',''),'(',''),')',''),'-',''),'"',''),'.',''),',','');
	UPDATE tx_wellbore_data_update SET LEASE_NUMBER=CONCAT('0',LEASE_NUMBER) WHERE LEN(LEASE_NUMBER) < 6;
	UPDATE tx_wellbore_data_update SET LEASE_NUMBER=CONCAT('0',LEASE_NUMBER) WHERE LEN(LEASE_NUMBER) < 6;
	UPDATE tx_wellbore_data_update SET LEASE_NUMBER=CONCAT('0',LEASE_NUMBER) WHERE LEN(LEASE_NUMBER) < 6;
	UPDATE tx_wellbore_data_update SET LEASE_NUMBER=CONCAT('0',LEASE_NUMBER) WHERE LEN(LEASE_NUMBER) < 6;
	UPDATE tx_wellbore_data_update SET LEASE_NUMBER=CONCAT('0',LEASE_NUMBER) WHERE LEN(LEASE_NUMBER) < 6;
	UPDATE tx_wellbore_data_update SET LEASE_NUMBER=CONCAT('0',LEASE_NUMBER) WHERE LEN(LEASE_NUMBER) < 6;
	UPDATE tx_wellbore_data_update SET LEASE_NUMBER=NULL WHERE LEASE_NUMBER='000000';
	UPDATE tx_wellbore_data_update SET API_NUMBER=CONCAT('0', API_NUMBER) WHERE LEN(API_NUMBER) < 8;
	UPDATE tx_wellbore_data_update SET API_NUMBER=CONCAT('0', API_NUMBER) WHERE LEN(API_NUMBER) < 8;
	UPDATE tx_wellbore_data_update SET API_NUMBER=CONCAT('0', API_NUMBER) WHERE LEN(API_NUMBER) < 8;
	UPDATE tx_wellbore_data_update SET API_NUMBER=CONCAT('0', API_NUMBER) WHERE LEN(API_NUMBER) < 8;
	UPDATE tx_wellbore_data_update SET API_NUMBER=CONCAT('0', API_NUMBER) WHERE LEN(API_NUMBER) < 8;
	UPDATE tx_wellbore_data_update SET API_NUMBER=CONCAT('0', API_NUMBER) WHERE LEN(API_NUMBER) < 8;
	UPDATE tx_wellbore_data_update SET API_NUMBER=CONCAT('0', API_NUMBER) WHERE LEN(API_NUMBER) < 8;
	UPDATE tx_wellbore_data_update SET API_NUMBER=CONCAT('0', API_NUMBER) WHERE LEN(API_NUMBER) < 8;
	UPDATE tx_wellbore_data_update SET API_NUMBER=CONCAT('42',API_NUMBER) WHERE LEN(API_NUMBER)=8;
	UPDATE tx_wellbore_data_update SET COUNTY_CODE=SUBSTRING(API_NUMBER,3,3) WHERE LEN(API_NUMBER)=10;
	UPDATE tx_wellbore_data_update SET PLUG_DATE=NULL WHERE LEN(PLUG_DATE)<2;
	UPDATE tx_wellbore_data_update SET PLUG_DATE=SUBSTRING(PLUG_DATE,1,6) WHERE LEN(PLUG_DATE)=8;
	
	UPDATE tx_wellbore_data_update 
	  SET FIELD_NAME=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
	                         FIELD_NAME,'''',''),'#',''),'(',''),')',''),'-',''),'"',''),'.',''),',',''),'  ',' ');
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	UPDATE tx_wellbore_data_update SET RECENT_PERMIT=CONCAT('0',RECENT_PERMIT) WHERE LEN(ISNULL(RECENT_PERMIT,'')) < 6;
	
	TRUNCATE TABLE tx_wellbore_data_lite;
	INSERT INTO tx_wellbore_data_lite (API_NUMBER, OIL_GAS_CODE, DISTRICT_NO, COUNTY_CODE, OPERATOR_NO, FIELD_NO,     
	                                   LEASE_NO, OIL_UNIT_NO, WELL_NO, COUNTY, OPERATOR, FIELD_NAME, LEASE_NAME, 
	                                   WELL_NO_DISPLAY, API_DEPTH, WB_SHUT_IN_DEPTH,  WELL_TYPE_NAME, ON_SCHEDULE, 
	                                   ORIG_COMPLETION_DT, COMPLETION_DATE,  WL_SHUT_IN_DATE, PLUG_DATE, PLUG_LEASE_NAME,
	                                   PLUG_OPERATOR_NAME, RECENT_PERMIT, RECENT_PERMIT_LEASE_NAME, 
	                                   RECENT_PERMIT_OPERATOR_NO, WB_14B2_FLAG, DISTRICT_CODE, H15_STATUS_CODE, 
	                                   WB_WATER_LAND_CODE, MULTI_COMP_FLAG) 
	                  (SELECT DISTINCT API_NUMBER, OIL_GAS_CODE, DISTRICT_CODE, COUNTY_CODE, OPERATOR_NUMBER, FIELD_NUMBER, 
		                  LEASE_NUMBER, OIL_UNIT_NUMBER, WELL_NO, COUNTY_NAME, OPERATOR_NAME, FIELD_NAME, LEASE_NAME, WELL_NO_DISPLAY, 
		                  CONVERT(INT,API_DEPTH), CONVERT(INT,WB_SHUT_IN_DEPTH), WELL_TYPE_NAME, ON_SCHEDULE, ORIG_COMPLETION_DT, 
		                  CONVERT(VARCHAR,COMPLETION_DATE), WL_SHUT_IN_DATE, PLUG_DATE, PLUG_LEASE_NAME, PLUG_OPERATOR_NAME, 
		                  RECENT_PERMIT, RECENT_PERMIT_LEASE_NAME, RECENT_PERMIT_OPERATOR_NO, WB_14B2_FLAG, DISTRICT_CODE, 
		                  H15_STATUS_CODE, WB_WATER_LAND_CODE, MULTI_COMP_FLAG  
	                  FROM tx_wellbore_data_update);
	UPDATE tx_wellbore_data_lite SET lease_id=NULL;
	UPDATE tx_wellbore_data_lite SET lease_id=CONCAT(oil_gas_code, district_no, county_code, lease_no) 
	  WHERE LEN(oil_gas_code)=1 AND LEN(district_no)=2 AND LEN(county_code)=3 AND LEN(lease_no)=6;
	UPDATE tx_wellbore_data_lite SET COMPLETION_DATE=NULL WHERE LEN(COMPLETION_DATE)<2;
	UPDATE tx_wellbore_data_lite SET COMPLETION_DATE=SUBSTRING(COMPLETION_DATE,1,6) WHERE LEN(COMPLETION_DATE)=8;
	"""
	curr.execute(sql_update)
	gd.commit(curr)
	curr.close()
	conn.close()

"""
	UPDATE tx_wellbore_data_lite SET lease_id=NULL;
	UPDATE tx_wellbore_data_lite SET district_no='14' WHERE district_no='10';
	UPDATE tx_wellbore_data_lite SET district_no='10' WHERE district_no='08';
	UPDATE tx_wellbore_data_lite SET district_no='08' WHERE district_no='7B';
	UPDATE tx_wellbore_data_lite SET district_no='13' WHERE district_no='09';
	UPDATE tx_wellbore_data_lite SET district_no='09' WHERE district_no='7C';
	UPDATE tx_wellbore_data_lite SET district_no='07' WHERE district_no='6E';
	UPDATE tx_wellbore_data_lite SET district_no='11' WHERE district_no='8A';
	UPDATE tx_wellbore_data_lite SET district_no='12' WHERE district_no='8B';
	UPDATE tx_wellbore_data_lite SET well_no=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(well_no,'\\',''),'-',''),'_',''),'\t',''),'{',''),' ',''),'''',''),'"','') WHERE NOT well_no IS NULL;
	UPDATE tx_wellbore_data_lite SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_wellbore_data_lite SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_wellbore_data_lite SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_wellbore_data_lite SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_wellbore_data_lite SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_wellbore_data_lite SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_wellbore_data_lite SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_wellbore_data_lite SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_wellbore_data_lite SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_wellbore_data_lite SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0';
	UPDATE tx_wellbore_data_lite SET lease_name=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(lease_name,'''',''),'#',''),'(',''),')',''),'-',''),'"',''),'.',''),',','');
	UPDATE tx_wellbore_data_lite SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_wellbore_data_lite SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_wellbore_data_lite SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_wellbore_data_lite SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_wellbore_data_lite SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_wellbore_data_lite SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6;
	UPDATE tx_wellbore_data_lite SET lease_no=NULL WHERE lease_no='000000';
	UPDATE tx_wellbore_data_lite SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_wellbore_data_lite SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_wellbore_data_lite SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_wellbore_data_lite SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_wellbore_data_lite SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_wellbore_data_lite SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_wellbore_data_lite SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_wellbore_data_lite SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8;
	UPDATE tx_wellbore_data_lite SET api_number=CONCAT('42',api_number) WHERE LEN(api_number)=8;
	UPDATE tx_wellbore_data_lite SET county_code=SUBSTRING(api_number,3,3) WHERE LEN(api_number)=10;
	UPDATE tx_wellbore_data_lite SET lease_id=CONCAT(oil_gas_code, district_no, county_code, lease_no) WHERE LEN(oil_gas_code)=1 AND LEN(district_no)=2 AND LEN(county_code)=3 AND LEN(lease_no)=6;
	UPDATE tx_wellbore_data_lite SET PLUG_DATE=NULL WHERE LEN(PLUG_DATE)<2;
	UPDATE tx_wellbore_data_lite SET PLUG_DATE=SUBSTRING(PLUG_DATE,1,6) WHERE LEN(PLUG_DATE)=8;
	UPDATE tx_wellbore_data_lite SET COMPLETION_DATE=NULL WHERE LEN(COMPLETION_DATE)<2;
	UPDATE tx_wellbore_data_lite SET COMPLETION_DATE=SUBSTRING(COMPLETION_DATE,1,6) WHERE LEN(COMPLETION_DATE)=8;
	UPDATE tx_wellbore_data_lite SET field_name=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(field_name,'''',''),'#',''),'(',''),')',''),'-',''),'"',''),'.',''),',',''),'  ',' ');
	UPDATE tx_wellbore_data_lite SET recent_permit=CONCAT('0',recent_permit) WHERE LEN(ISNULL(recent_permit,'')) < 6;
	UPDATE tx_wellbore_data_lite SET recent_permit=CONCAT('0',recent_permit) WHERE LEN(ISNULL(recent_permit,'')) < 6;
	UPDATE tx_wellbore_data_lite SET recent_permit=CONCAT('0',recent_permit) WHERE LEN(ISNULL(recent_permit,'')) < 6;
	UPDATE tx_wellbore_data_lite SET recent_permit=CONCAT('0',recent_permit) WHERE LEN(ISNULL(recent_permit,'')) < 6;
	UPDATE tx_wellbore_data_lite SET recent_permit=CONCAT('0',recent_permit) WHERE LEN(ISNULL(recent_permit,'')) < 6;
	UPDATE tx_wellbore_data_lite SET recent_permit=CONCAT('0',recent_permit) WHERE LEN(ISNULL(recent_permit,'')) < 6;
"""

def process_wellbore_data(configure=False, import_csv=False, update=False):
	if configure:
		configure_wellbore_file()
	if import_csv:
		import_csv_to_sql(data_dir=TX_WB_DIR, table_name='tx_wellbore_data_update', truncate=True)
	if update:
		update_wellbore_data()


# Permit Data --------------------------------------------------------------------------------------------------

def update_permit_data():
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	max_id = gd.get_data('MAX(id)', 'dbo.tx_permit_data', server='sql_server', database='US_Wells_Texas', cursor=curr,
	                     single_value=True, datatype='int')
	print max_id
	sql_update = \
	"""
	UPDATE tx_permit_data SET process_code=0;
	
	TRUNCATE TABLE tx_permit_data_update_;
	
	INSERT INTO tx_permit_data_update_ (Status_Date, Status_No, API_Number, Operator_Data, Lease_Name, Well_No, District_No, County, Well_Direction, Filing_Purpose, Amend, Total_Depth, Current_Queue)
	  (SELECT DISTINCT Status_Date, Status_No, API_Number, Operator_Data, Lease_Name, Well_No, District_No, County, Well_Direction, Filing_Purpose, Amend, Total_Depth, Current_Queue
	   FROM tx_permit_data_update);
	
	INSERT INTO tx_permit_data (id, status_date, drill_permit_no, api_number, operator_data, lease_name, well_no, district_no, county, well_direction, filing_purpose, amend, total_depth, current_queue, process_code)
	  (SELECT DISTINCT (update_id+{}), Status_Date, Status_No, API_Number, Operator_Data, Lease_Name, Well_No, District_No, County, Well_Direction, Filing_Purpose, Amend, Total_Depth, Current_Queue, 9
	   FROM tx_permit_data_update_);
	
	UPDATE tx_permit_data
	  SET submitted_date=CONCAT(SUBSTRING(status_date,17,4),SUBSTRING(status_date,11,2)),
		  approved_date=CONCAT(SUBSTRING(status_date,37,4),SUBSTRING(status_date,31,2))
	  WHERE status_date LIKE 'Submitted%Approved%' AND LEN(ISNULL(submitted_date,''))=0;
	
	UPDATE tx_permit_data SET well_no=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(well_no,'\\',''),'-',''),'_',''),'\t',''),' ',''),'''',''),'"','') WHERE NOT well_no IS NULL AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET lease_name=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(lease_name,'''',''),'#',''),'(',''),')',''),'-',''),'"',''),'.',''),',','') WHERE LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET lease_name_str=REPLACE(lease_name,' ','') WHERE LEN(ISNULL(county_no,''))=0 AND process_code=9;
	
	UPDATE tx_permit_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET lease_no=CONCAT('0',lease_no) WHERE LEN(lease_no) < 6 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	
	UPDATE tx_permit_data SET lease_no=NULL WHERE lease_no='000000' AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET api_number=CONCAT('0',api_number) WHERE LEN(api_number) < 8 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	
	UPDATE tx_permit_data SET api_number=CONCAT('42',api_number) WHERE LEN(ISNULL(county_no,''))=0 AND process_code=9;
	UPDATE tx_permit_data SET district_no=CONCAT('0',district_no) WHERE LEN(district_no) < 2 AND LEN(ISNULL(county_no,''))=0 AND process_code=9;
	
	UPDATE tx_permit_data SET county_no=SUBSTRING(api_number,3,3) WHERE LEN(ISNULL(county_no,''))=0 AND process_code=9;
	
	UPDATE tx_permit_data SET district_no='14' WHERE district_no='10' AND process_code=9;
	UPDATE tx_permit_data SET district_no='10' WHERE district_no='08' AND process_code=9;
	UPDATE tx_permit_data SET district_no='08' WHERE district_no='7B' AND process_code=9;
	UPDATE tx_permit_data SET district_no='13' WHERE district_no='09' AND process_code=9;
	UPDATE tx_permit_data SET district_no='09' WHERE district_no='7C' AND process_code=9;
	UPDATE tx_permit_data SET district_no='07' WHERE district_no='6E' AND process_code=9;
	UPDATE tx_permit_data SET district_no='11' WHERE district_no='8A' AND process_code=9;
	UPDATE tx_permit_data SET district_no='12' WHERE district_no='8B' AND process_code=9;
	
	UPDATE tx_permit_data SET lease_id=CONCAT(oil_gas_code, district_no, county_no, lease_no) WHERE LEN(oil_gas_code)=1 AND LEN(district_no)=2 AND LEN(county_no)=3 AND LEN(lease_no)=6 AND lease_id IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_well_data_master b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.district_no=b.district_no AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_well_data_master b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_well_data_master b
	  WHERE a.drill_permit_no=b.drill_permit_no AND a.api_number=b.api_number AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_wellbore_data_lite b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.district_no=b.district_code AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_wellbore_data_lite b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_wellbore_data_lite b
	  WHERE a.drill_permit_no=b.recent_permit AND a.api_number=b.api_number AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_wellbore_data_lite b
	  WHERE a.drill_permit_no=b.recent_permit AND a.api_number=b.api_number AND a.lease_no IS NULL AND b.lease_no IS NOT NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_wellbore_data_lite b
	  WHERE a.well_no=b.well_no AND a.api_number=b.api_number AND a.lease_no IS NULL AND b.lease_no IS NOT NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data
	  SET lease_no=b.lease_no
	  FROM tx_permit_data AS a, tx_well_data_master AS b
	  WHERE a.drill_permit_no=b.permit_no AND a.lease_name_str=b.lease_name_str AND a.api_number=b.api_number AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data
	  SET lease_no=b.lease_no
	  FROM tx_permit_data AS a, tx_well_data_master AS b
	  WHERE a.lease_name_str=b.lease_name_str AND a.api_number=b.api_number AND a.lease_no IS NULL AND NOT b.lease_no IS NULL;
	
	UPDATE tx_permit_data
	  SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data AS a, tx_well_data_master AS b
	  WHERE a.well_no=b.well_no AND a.drill_permit_no=b.permit_no AND a.api_number=b.api_number AND a.lease_no IS NULL AND NOT b.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=NULL WHERE lease_no='000000';
	
	"""
	curr.execute(sql_update.format(max_id))
	gd.commit(curr)
	curr.close()
	conn.close()


def extract_operator_data(debug=False):
	sql_update = "UPDATE tx_permit_data SET operator='{}', operator_no={} WHERE id={}"
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	well_operator_data = gd.get_data('id, operator_data', 'tx_permit_data', database='US_Wells_Texas',
	                                 server='sql_server', cursor=curr, datatype='plural', sql_where='process_code=9')
	data_count = len(well_operator_data)
	data_num = 1
	for id, operator_data in well_operator_data:
		try:
			data_parts = operator_data.split(' (')
			operator = ' ('.join(data_parts[:-1])
			operator_no = data_parts[-1]
			operator = operator.replace('.', '').replace(',', '')
			operator_no = int(operator_no[:-1])
			print '{}/{}  operator name: {} --- operator no: {}'.format(data_num, data_count, operator, operator_no)
			if debug: print sql_update.format(operator, operator_no, id)
			curr.execute(sql_update.format(operator, operator_no, id))
			gd.commit(curr)
		except:
			print operator_data
		data_num += 1
	curr.close()
	conn.close()


def process_permit_data(extract=False, update=False):
	if update:
		print 'Updating tx_permit_data table ...'
		update_permit_data()
	if extract:
		print 'Extracting operator data from tx_permit_data ...'
		extract_operator_data()


# Oil Schedule Data ---------------------------------------------------------------------------------------------------------------------------

def extract_oil_field_schedule_data(debug=False):
	conn = gd.get_connection(server='sql_server', database='US_Wells_Texas', us_wells=True)
	curr = conn.cursor()

	curr.execute("UPDATE tx_oil_field_schedule SET process_code=1")
	gd.commit(curr)

	sched_count = len(os.listdir(OIL_SCHED_DIR))
	print sched_count
	sched_num = 1
	sql_insert = "INSERT INTO tx_oil_field_schedule (process_code, well_record, source_line, source_file, sched_date, district_no, field_name, field_no, operator, operator_no, lease_name, lease_no) VALUES (0, '{}', {}, '{}', '{}', '{}', '{}', {}, '{}', {}, '{}', '{}')"
	for oil_field_sched in os.listdir(OIL_SCHED_DIR):
		print oil_field_sched
		in_data_group = False
		last_district_line = 0
		last_header_line = 0
		last_operator_line = 0
		last_lease_line = 0
		last_well_line = 0
		full_sched_date = ''
		sched_date = ''
		district_no = ''
		field_name = ''
		field_no = 0
		operator = ''
		operator_no = 0
		lease_name = ''
		lease_no = ''
		exit = 0
		exit_data = []
		header_data = ()
		with open(OIL_SCHED_DIR + oil_field_sched) as sched_file:
			filelines = sched_file.readlines()
			line_count = len(filelines)
			if line_count == 1:
				filelines = filelines[0].split('\r')
				line_count = len(filelines)
				print line_count
			for line_num in range(line_count):
				fileline = filelines[line_num]
				if fileline.startswith('EXHIBIT A - OIL PRORATION SCHEDULE'):
					exit = 1
					last_district_line = line_num
					full_sched_date = fileline[53:71].strip()
					sched_date = full_sched_date[-4:] + MONTH_NOS[full_sched_date[:3]]
					district_no = fileline.split()[-1].strip()[-2:]
					header_data = (sched_date, district_no,)
				elif len(fileline.strip()) > 0 and (
						((last_district_line == (line_num - 3)) and len(filelines[line_num - 1].strip()) == 0) or (
						(line_num + 1 < line_count) and (
						((last_district_line == (line_num - 2)) and filelines[line_num + 1][75:].startswith('MVBAL')) or
						filelines[line_num + 1].startswith('* *') or filelines[line_num + 1].startswith(' * *')))):
					exit = 2
					field_name = fileline[:33].rstrip().replace('"', '').replace(',', '').replace("'", "")
					field_no = fileline[33:41]
					header_data += (field_name, field_no)
				elif fileline.startswith('  WELL   DEPTH  POTE') or fileline.startswith('  WELL    POTE'):
					exit = 3
					last_header_line = line_num
				elif last_header_line and (last_header_line == (line_num - 2)) and len(fileline.strip()) > 0:
					exit = 4
					last_operator_line = line_num
					in_data_group = True
					operator = fileline[:33].rstrip().replace('"', '').replace(',', '').replace("'", "")
					operator_no = fileline[33:39]
					header_data += (operator, operator_no)
				elif fileline.startswith('WELLS: ') or fileline.startswith('UNIT " " TOTALS') or fileline.startswith(
						' * * *') or fileline.startswith('* * *') or fileline.startswith(
					'DISC:') or fileline.startswith('WELL STATUS TEST') or fileline.startswith(
					'ACRES:') or fileline.startswith('ALLOC:'):
					exit = 5
					in_data_group = False
				elif in_data_group and len(fileline.strip()) > 0 and (fileline[0] not in ['-', ' ', '*', '|']):
					exit = 6
					last_operator_line = line_num
					operator = fileline[:33].rstrip().replace('"', '').replace(',', '').replace("'", "")
					operator_no = fileline[33:39]
					header_data = (sched_date, district_no, field_name, field_no, operator, operator_no)
				elif in_data_group and (
						last_operator_line and (last_operator_line == (line_num - 1))) and not fileline.startswith(
					'- - - - -') and (len(fileline.strip()) == 0):
					exit = 7
					last_lease_line = line_num
					lease_no = '0' + fileline[1:6]
					lease_name = fileline[8:45].rstrip().replace('"', '').replace(',', '').replace("'", "")
					header_data += (lease_name, lease_no)
				elif in_data_group and ((len(fileline.strip()) == 122) or (fileline[45:].startswith('(CONT)'))) and (
						fileline[1] != ' '):
					exit = 8
					last_lease_line = line_num
					lease_no = '0' + fileline[1:6]
					lease_name = fileline[8:45].rstrip().replace('"', '').replace(',', '').replace("'", "")
					header_data = (
						sched_date, district_no, field_name, field_no, operator, operator_no, lease_name, lease_no)
				elif in_data_group and (len(fileline.rstrip()) == 132) and not (
						fileline.startswith('- -') or fileline.startswith(' - -')):
					exit = 9
					well_record = fileline.rstrip().replace('"', ' ').replace(',', ' ').replace("'", " ")
					curr.execute(sql_insert.format(well_record, line_num, oil_field_sched, *header_data))
					gd.commit(curr)
				elif in_data_group and (len(fileline.strip()) == 0):
					exit = 10
					in_data_group = False
				elif in_data_group and fileline.startswith('- - - - -'):
					exit = 11
					in_data_group = False
				else:
					exit = 12
					pass
				if debug:
					print '{} >> ({}/{}) --- {}/{} --- {}: {} --> {}'.format(oil_field_sched, sched_num, sched_count,
					                                                         line_num, line_count, exit,
					                                                         fileline.strip(), header_data)
				else:
					print '{} >> ({}/{}) --- {}/{}'.format(oil_field_sched, sched_num, sched_count, line_num,
					                                       line_count)
			sched_num += 1
	curr.close()
	conn.close()


def update_oil_field_schedule_data():
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	sql_update = \
		"""
	UPDATE tx_oil_field_schedule SET county_no=SUBSTRING(well_record, 120, 3) WHERE process_code=0;
	UPDATE tx_oil_field_schedule SET api_number=CONCAT('42',SUBSTRING(well_record, 124, 3),SUBSTRING(well_record, 128, 5)) WHERE process_code=0;
	UPDATE tx_oil_field_schedule SET well_no=REPLACE(REPLACE(REPLACE(SUBSTRING(well_record, 1, 8),' ',''),'-',''),'*','') WHERE process_code=0;
	UPDATE tx_oil_field_schedule SET potential=REPLACE(SUBSTRING(well_record, 17, 5),' ','') WHERE NOT SUBSTRING(well_record, 17, 5) IN ('     ', 'L:   ') AND process_code=0;
	UPDATE tx_oil_field_schedule SET oil_allow_bbl=REPLACE(SUBSTRING(well_record, 91, 5),' ','') WHERE NOT SUBSTRING(well_record, 91, 5)='     ' AND process_code=0;
	UPDATE tx_oil_field_schedule SET oil_allow_bd=REPLACE(SUBSTRING(well_record, 59, 4),' ','')
	  WHERE NOT SUBSTRING(well_record, 59, 4) IN ('14B ','14B2','    ','DLQ ','GAS ','H15 ','INJE','LIQ ','NO P','OBSE','PRTL','RO  ','SERV','SHUT','SI M','STRG','WATR', 'K   ','L   ', 'L  3', 'M   ', 'P   ', 'Y   ', 'T   ', 'CSG ') AND process_code=0;
	UPDATE tx_oil_field_schedule SET csgd_allow_mcfd=REPLACE(SUBSTRING(well_record, 66, 7),' ','') WHERE NOT SUBSTRING(well_record, 72, 1)='E' AND NOT SUBSTRING(well_record, 66, 7) IN ('K      ','       ','G      ','H      ','J      ','L      ','M      ','P      ','R      ','T      ','Y      ',' NET   ', 'T   ', 'CSG ') AND process_code=0;
	UPDATE tx_oil_field_schedule SET gas_allow_mcf=REPLACE(SUBSTRING(well_record, 115, 4),' ','') WHERE NOT SUBSTRING(well_record, 115, 4) IN ('    ', 'AL G') AND process_code=0;
	UPDATE tx_oil_field_schedule SET acres=REPLACE(SUBSTRING(well_record, 22, 6),' ','') WHERE NOT SUBSTRING(well_record, 26, 2) IN (' P', '  ') AND process_code=0;
	UPDATE tx_oil_field_schedule SET gas_to_oil=REPLACE(SUBSTRING(well_record, 29, 5),' ','') WHERE NOT SUBSTRING(well_record, 29, 5) IN ('     ', 'O    ') AND process_code=0;
	UPDATE tx_oil_field_schedule SET oil_limit_code=SUBSTRING(well_record, 63, 1) WHERE process_code=0;
	UPDATE tx_oil_field_schedule SET api_depth=REPLACE(SUBSTRING(well_record, 9, 5),' ','')
	  WHERE NOT SUBSTRING(well_record, 9, 5) IN ('TALS-', '     ') AND NOT SUBSTRING(well_record, 9, 1) IN ('E','M','P','S') AND process_code=0;
	UPDATE tx_oil_field_schedule SET allow_code=SUBSTRING(well_record, 15, 1) WHERE process_code=0;
	UPDATE tx_oil_field_schedule SET prod_method=SUBSTRING(well_record, 97, 1) WHERE process_code=0;
	UPDATE tx_oil_field_schedule SET test_date=SUBSTRING(well_record, 108, 6) WHERE process_code=0;
	
	UPDATE tx_oil_field_schedule SET well_no=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(well_no,'\\',''),'-',''),'_',''),'\t',''),'{',''),' ',''),'''',''),'"','') WHERE process_code=0;

	UPDATE tx_oil_field_schedule SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
	UPDATE tx_oil_field_schedule SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
	UPDATE tx_oil_field_schedule SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
	UPDATE tx_oil_field_schedule SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
	UPDATE tx_oil_field_schedule SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
	UPDATE tx_oil_field_schedule SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
	UPDATE tx_oil_field_schedule SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
	UPDATE tx_oil_field_schedule SET well_no=SUBSTRING(well_no,2,LEN(well_no)-1) WHERE SUBSTRING(well_no,1,1)='0' AND process_code=0;
	
	UPDATE tx_oil_field_schedule SET district_no='14' WHERE district_no='10' AND process_code=0;
	UPDATE tx_oil_field_schedule SET district_no='10' WHERE district_no='08' AND process_code=0;
	UPDATE tx_oil_field_schedule SET district_no='08' WHERE district_no='7B' AND process_code=0;
	UPDATE tx_oil_field_schedule SET district_no='13' WHERE district_no='09' AND process_code=0;
	UPDATE tx_oil_field_schedule SET district_no='09' WHERE district_no='7C' AND process_code=0;
	UPDATE tx_oil_field_schedule SET district_no='07' WHERE district_no='6E' AND process_code=0;
	UPDATE tx_oil_field_schedule SET district_no='11' WHERE district_no='8A' AND process_code=0;
	UPDATE tx_oil_field_schedule SET district_no='12' WHERE district_no='8B' AND process_code=0;
	
	UPDATE tx_oil_field_schedule SET lease_id=CONCAT('O', district_no, county_no, lease_no) WHERE LEN(district_no)=2 AND LEN(county_no)=3 AND LEN(lease_no)=6 AND lease_id IS NULL;

	UPDATE tx_oil_field_schedule SET lease_allow_bbl=0 WHERE process_code=0;
	UPDATE tx_oil_field_schedule SET well_allow_pct=0 WHERE process_code=0;
	
	UPDATE tx_oil_field_schedule
	  SET lease_allow_bbl=b.lease_oil_allow
	  FROM tx_oil_field_schedule AS a,
	  (SELECT DISTINCT lease_id, sched_date, SUM(ISNULL(oil_allow_bbl,0)) AS lease_oil_allow FROM tx_oil_field_schedule GROUP BY lease_id, sched_date) AS b
	  WHERE a.lease_id=b.lease_id AND a.sched_date=b.sched_date AND a.process_code=0;
	
	UPDATE tx_oil_field_schedule SET well_allow_pct=ROUND(oil_allow_bbl/lease_allow_bbl,3) WHERE process_code=0 AND ISNULL(lease_allow_bbl,0)>0;
	DELETE FROM tx_oil_field_schedule WHERE well_no='LSETO' AND process_code=0;
	
	UPDATE tx_oil_field_schedule SET tx_well_id=b.tx_well_id
	  FROM tx_oil_field_schedule a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.tx_well_id IS NULL AND b.tx_well_id IS NOT NULL AND a.lease_no=b.lease_no AND b.oil_gas_code='O' AND a.process_code=0;
	
	UPDATE tx_oil_field_schedule SET lease_id=CONCAT('O',district_no,county_no,lease_no) WHERE process_code=0;
	UPDATE tx_oil_field_schedule SET potential=0 WHERE potential IS NULL AND process_code=0;
	UPDATE tx_oil_field_schedule SET oil_allow_bbl=0 WHERE oil_allow_bbl IS NULL AND process_code=0;
	UPDATE tx_oil_field_schedule SET oil_allow_bd=0 WHERE oil_allow_bd IS NULL AND process_code=0;
	UPDATE tx_oil_field_schedule SET csgd_allow_mcfd=0 WHERE csgd_allow_mcfd IS NULL AND process_code=0;
	
	UPDATE tx_oil_field_schedule
	  SET county_name=b.county
	  FROM tx_oil_field_schedule AS a, (SELECT DISTINCT county, county_no FROM tx_well_details) AS b
	  WHERE a.county_no=b.county_no AND a.process_code=0;
	
	UPDATE tx_oil_field_schedule SET prod_year=CONVERT(INT,SUBSTRING(sched_date,1,4)) WHERE prod_year IS NULL;
	
	UPDATE tx_oil_field_schedule SET prod_month='jan' WHERE SUBSTRING(sched_date,5,2)='01' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='feb' WHERE SUBSTRING(sched_date,5,2)='02' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='mar' WHERE SUBSTRING(sched_date,5,2)='03' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='apr' WHERE SUBSTRING(sched_date,5,2)='04' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='may' WHERE SUBSTRING(sched_date,5,2)='05' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='jun' WHERE SUBSTRING(sched_date,5,2)='06' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='jul' WHERE SUBSTRING(sched_date,5,2)='07' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='aug' WHERE SUBSTRING(sched_date,5,2)='08' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='sep' WHERE SUBSTRING(sched_date,5,2)='09' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='oct' WHERE SUBSTRING(sched_date,5,2)='10' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='nov' WHERE SUBSTRING(sched_date,5,2)='11' AND prod_month IS NULL;
	UPDATE tx_oil_field_schedule SET prod_month='dec' WHERE SUBSTRING(sched_date,5,2)='12' AND prod_month IS NULL;
	
	UPDATE tx_oil_field_schedule SET well_allow_pct=0 WHERE well_allow_pct IS NULL;
	UPDATE tx_oil_field_schedule SET lease_allow_bbl=0;
	UPDATE tx_oil_field_schedule SET well_allow_pct=0;
	
	UPDATE tx_oil_field_schedule
	  SET lease_allow_bbl=b.lease_oil_allow
	  FROM tx_oil_field_schedule AS a,
	  (SELECT DISTINCT lease_id, sched_date, SUM(ISNULL(oil_allow_bbl,0)) AS lease_oil_allow FROM tx_oil_field_schedule GROUP BY lease_id, sched_date) AS b
	  WHERE a.lease_id=b.lease_id AND a.sched_date=b.sched_date;
	
	UPDATE tx_oil_field_schedule SET well_allow_pct=ROUND(oil_allow_bbl/CONVERT(FLOAT,lease_allow_bbl),3) WHERE ISNULL(lease_allow_bbl,0)!=0;
	"""
	curr.execute(sql_update)
	gd.commit(curr)
	curr.close()
	conn.close()


def process_oil_field_schedule_data(extract=False, update=False):
	if extract:
		print 'Extracting data from oil field proration schedules ...'
		extract_oil_field_schedule_data(debug=False)
	if update:
		print 'Updating tx_oil_field_schedule table ...'
		update_oil_field_schedule_data()


# Oil Production Allocation --------------------------------------------------------------------------------------------------------------------

def get_prod_dates(start_date, end_date):
	start_date_indx = PROD_DATES.index(start_date)
	end_date_indx = PROD_DATES.index(end_date) + 1
	prod_dates = sorted(PROD_DATES[start_date_indx: end_date_indx])
	return prod_dates


def update_oil_production_data(curr, debug=False):
	sql_update = \
		"""
	TRUNCATE TABLE tx_oil_production_data;

	INSERT INTO tx_oil_production_data (lease_id, prod_date, oil_prod_vol, csgd_prod_vol, process_code)
	  (SELECT DISTINCT lease_id, prod_date, SUM(oil_prod_vol), SUM(csgd_prod_vol), 1 FROM tx_production_data WHERE oil_gas_code='O' GROUP BY lease_id, prod_date);

	DELETE FROM tx_oil_production_data WHERE (oil_prod_vol+csgd_prod_vol)=0;

	UPDATE tx_oil_production_data SET prod_year=CONVERT(INT,SUBSTRING(prod_date,1,4));
	"""
	curr.execute(sql_update)
	gd.commit(curr)


def update_oil_field_sched_lite(curr, debug=False):
	sql_update = \
		"""
	SET IDENTITY_INSERT tx_oil_field_schedule_lite_2 ON;
	INSERT INTO tx_oil_field_schedule_lite_2 (schedule_id,tx_well_id,sched_date,lease_id,prod_year,prod_month,oil_allow_bbl,lease_allow_bbl,well_allow_pct,process_code)
	  (SELECT DISTINCT schedule_id,tx_well_id,sched_date,lease_id,prod_year,prod_month,oil_allow_bbl,lease_allow_bbl,well_allow_pct,1
	   FROM tx_oil_field_schedule WHERE schedule_id > (SELECT MAX(schedule_id) FROM tx_oil_field_schedule_lite_2));
	SET IDENTITY_INSERT tx_oil_field_schedule_lite_2 OFF;

	UPDATE tx_oil_field_schedule_lite_2 
	  SET lease_prod_bbl=0 
	  WHERE lease_prod_bbl IS NULL;

	UPDATE tx_oil_field_schedule_lite_2
	  SET lease_prod_bbl=b.oil_prod_vol
	  FROM tx_oil_field_schedule_lite_2 AS a, tx_oil_production_data AS b
	  WHERE a.lease_id=b.lease_id AND a.sched_date=b.prod_date;

	UPDATE tx_oil_field_schedule_lite_2
	  SET well_portion_bbl=((b.potential*(365.0/12.0))+b.oil_allow_bbl)
	  FROM tx_oil_field_schedule_lite_2 AS a, tx_oil_field_schedule AS b
	  WHERE a.schedule_id=b.schedule_id;

	UPDATE tx_oil_field_schedule_lite_2 SET lease_allow_bbl=0 WHERE lease_allow_bbl IS NULL;

	UPDATE tx_oil_field_schedule_lite_2
	  SET lease_allow_bbl=b.total_lease_portion
	  FROM tx_oil_field_schedule_lite_2 AS a,
	  (SELECT DISTINCT lease_id, sched_date, SUM(well_portion_bbl) AS total_lease_portion FROM tx_oil_field_schedule_lite_2 GROUP BY lease_id, sched_date) AS b
	  WHERE a.lease_id=b.lease_id AND a.sched_date=b.sched_date;

	UPDATE tx_oil_field_schedule_lite_2 SET well_allow_pct=0 WHERE well_allow_pct IS NULL;

	UPDATE tx_oil_field_schedule_lite_2 SET well_allow_pct=ROUND(ISNULL(well_portion_bbl,0)/lease_allow_bbl,3) WHERE ISNULL(lease_allow_bbl,0) > 0;

	UPDATE tx_oil_field_schedule_lite_2 SET well_allow_pct=1 WHERE well_allow_pct > 1;

	UPDATE tx_oil_field_schedule_lite_2
	  SET oil_allow_bbl=ROUND(a.lease_prod_bbl/b.well_count,3), well_portion_bbl=ROUND(a.lease_prod_bbl/b.well_count,3), lease_allow_bbl=a.lease_prod_bbl, well_allow_pct=ROUND(1.0/b.well_count,3)
	  FROM tx_oil_field_schedule_lite_2 AS a,
		   (SELECT DISTINCT lease_id, sched_date, CONVERT(FLOAT,COUNT(DISTINCT schedule_id)) AS well_count FROM tx_oil_field_schedule_lite_2 GROUP BY lease_id, sched_date) AS b
	  WHERE ISNULL(b.well_count,0) > 0 AND a.lease_id=b.lease_id AND a.sched_date=b.sched_date AND a.lease_prod_bbl > 0 AND a.lease_allow_bbl=0;
	"""
	curr.execute(sql_update)
	gd.commit(curr)


# Remove function because reference is made to non-existent object, so probably never run
def update_data_gaps(curr, debug=False):
	sql_update = 'UPDATE tx_oil_field_schedule_lite_2 SET oil_allow_bbl={2}, well_portion_bbl={2} WHERE tx_well_id="{0}" AND sched_date="{1}"'
	sql_insert = 'INSERT INTO tx_oil_field_schedule_lite_2 (tx_well_id, sched_date, oil_allow_bbl, well_portion_bbl, lease_allow_bbl, lease_prod_bbl, well_allow_pct, process_code) VALUES ("{0}", "{1}", {2}, {2}, 0, 0, 0, 3)'
	all_sched_dates = get_prod_dates('201301', '202003')
	tx_well_ids = gd.get_data('tx_well_id', 'dbo.tx_oil_field_schedule_lite_2', cursor=curr, database='US_Wells_Texas',
	                          server='sql_server', datatype='plural', sql_where='well_allow_pct > 0')
	well_prod_data = {
		tx_well_id: sorted([(well_data[1], well_data[2]) for well_data in all_well_data if well_data[0] == tx_well_id])
		for tx_well_id in tx_well_ids}
	well_count = len(tx_well_ids)
	well_num = 1
	for tx_well_id in tx_well_ids:
		well_sched_data = gd.get_data('sched_date, ISNULL(well_portion_bbl,0)', 'dbo.tx_oil_field_schedule_lite_2',
		                              cursor=curr, database='US_Wells_Texas', server='sql_server', datatype='plural',
		                              sql_where='tx_well_id="{}"'.format(tx_well_id))
		well_sched_dates = sorted(list(set([well_data[0] for well_data in well_sched_data])))
		well_portion_data = {well_data[0]: well_data[1] for well_data in well_sched_data}
		well_prod_dates = [well_sched_date for well_sched_date in well_sched_dates if
		                   well_portion_data[well_sched_date] > 0]
		sched_start_indx = all_sched_dates.index(well_sched_dates[0])
		sched_end_indx = all_sched_dates.index(well_sched_dates[-1])
		last_well_portion = 0
		curr_well_portion = 0
		next_well_portion = 0
		curr_sched_indx = 0
		next_sched_indx = 1
		next_sched_date = well_sched_dates[1]
		for sched_date in all_sched_dates[sched_start_indx:sched_end_indx + 2]:
			print '{}/{}: {} -- {}'.format(well_num, well_count, tx_well_id, sched_date)
			if sched_date in well_sched_dates:
				if sched_date in well_prod_dates:
					last_well_portion = well_portion_data[sched_date]
					last_sched_indx = well_prod_dates.index(sched_date)
					next_sched_indx = last_sched_indx + 1
					next_sched_date = well_prod_dates[next_sched_indx]
					try:
						next_well_portion = well_portion_data[next_sched_date]
					except:
						next_well_portion = 0
					curr_well_portion = round((float(last_well_portion) + float(next_well_portion)) / 2, 3)
				else:
					if debug: print sql_update.format(tx_well_id, sched_date, curr_well_portion)
					curr.execute(sql_update.format(tx_well_id, sched_date, curr_well_portion))
					gd.commit(curr)
			else:
				if debug: print sql_insert.format(tx_well_id, sched_date, curr_well_portion)
				curr.execute(sql_insert.format(tx_well_id, sched_date, curr_well_portion))
				gd.commit(curr)
		well_num += 1


def update_lease_prod_sched_2(curr, debug=False):
	sql_update = \
		"""
	TRUNCATE TABLE tx_lease_prod_schedule_2;

	INSERT INTO tx_lease_prod_schedule_2 (lease_id, lease_start_date, lease_end_date)
	  (SELECT DISTINCT lease_id, MIN(prod_date) AS lease_start_date, MAX(prod_date) AS lease_end_date
		FROM tx_oil_production_data WHERE (ISNULL(oil_prod_vol,0) + ISNULL(csgd_prod_vol,0)) > 0
		GROUP BY lease_id);

	DELETE FROM tx_lease_prod_schedule_2 WHERE SUBSTRING(lease_id,1,1)='G';

	UPDATE tx_lease_prod_schedule_2 SET district_no=SUBSTRING(lease_id,2,2), county_no=SUBSTRING(lease_id,4,3), lease_no=SUBSTRING(lease_id,7,6) WHERE LEN(lease_id)=12;

	UPDATE tx_lease_prod_schedule_2 SET total_well_count=0;

	UPDATE tx_lease_prod_schedule_2 SET total_well_count=b.total_well_count
	  FROM tx_lease_prod_schedule_2 a,
		   (SELECT DISTINCT lease_id, COUNT(DISTINCT tx_well_id) AS total_well_count FROM tx_ref_well_id WHERE lease_id IS NOT NULL AND tx_well_id IS NOT NULL GROUP BY lease_id) b
	  WHERE a.lease_id=b.lease_id;

	UPDATE tx_lease_prod_schedule_2 SET lease_id=REPLACE(lease_id, ' ','');
	"""
	curr.execute(sql_update)
	gd.commit(curr)


def create_well_allow_pct(curr, debug=False):
	sql_update = \
		"""
	DROP TABLE IF EXISTS tx_well_allow_pct; 
	CREATE TABLE tx_well_allow_pct (
	  id               INT   IDENTITY,
	  lease_id         VARCHAR(20),
	  tx_well_id       VARCHAR(15),
	  prod_year        INT,
	  oil_total_bbl    FLOAT,
	  csgd_total_mcf   FLOAT,
	  oil_jan_bbl      FLOAT,
	  oil_feb_bbl      FLOAT,
	  oil_mar_bbl      FLOAT,
	  oil_apr_bbl      FLOAT,
	  oil_may_bbl      FLOAT,
	  oil_jun_bbl      FLOAT,
	  oil_jul_bbl      FLOAT,
	  oil_aug_bbl      FLOAT,
	  oil_sep_bbl      FLOAT,
	  oil_oct_bbl      FLOAT,
	  oil_nov_bbl      FLOAT,
	  oil_dec_bbl      FLOAT,
	  csgd_jan_mcf     FLOAT,
	  csgd_feb_mcf     FLOAT,
	  csgd_mar_mcf     FLOAT,
	  csgd_apr_mcf     FLOAT,
	  csgd_may_mcf     FLOAT,
	  csgd_jun_mcf     FLOAT,
	  csgd_jul_mcf     FLOAT,
	  csgd_aug_mcf     FLOAT,
	  csgd_sep_mcf     FLOAT,
	  csgd_oct_mcf     FLOAT,
	  csgd_nov_mcf     FLOAT,
	  csgd_dec_mcf     FLOAT,
	  process_code     INT,
	  lease_well_count INT   DEFAULT NULL,
	  oil_jan_bbl_test FLOAT DEFAULT NULL,
	  PRIMARY KEY (id));
	
	CREATE INDEX lease_id_indx ON tx_well_allow_pct (lease_id);
	
	CREATE INDEX prod_year_indx ON tx_well_allow_pct (prod_year);
	
	CREATE INDEX tx_well_id_prod_year_indx ON tx_well_allow_pct (tx_well_id, prod_year);
	
	CREATE INDEX tx_well_id_indx ON tx_well_allow_pct (tx_well_id);
	
	CREATE INDEX process_code_indx ON tx_well_allow_pct (process_code);

	INSERT INTO tx_well_allow_pct (lease_id, tx_well_id, prod_year, oil_total_bbl, csgd_total_mcf, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, csgd_jan_mcf, csgd_feb_mcf, csgd_mar_mcf, csgd_apr_mcf, csgd_may_mcf, csgd_jun_mcf, csgd_jul_mcf, csgd_aug_mcf, csgd_sep_mcf, csgd_oct_mcf, csgd_nov_mcf, csgd_dec_mcf, process_code)
	  (SELECT DISTINCT lease_id, tx_well_id, prod_year, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 FROM tx_oil_field_schedule_lite_2);
	"""
	curr.execute(sql_update)
	gd.commit(curr)


# Total Time: 27:04:47 -- 2403620 rows (2020-06-30)
def tx_lease_to_well_prod(curr, debug=False):
	month_names = [
		'jan',
		'feb',
		'mar',
		'apr',
		'may',
		'jun',
		'jul',
		'aug',
		'sep',
		'oct',
		'nov',
		'dec'
	]
	sql_update = \
		'''
	UPDATE tx_well_allow_pct
	  SET oil_{0}_bbl=b.well_allow_pct, csgd_{0}_mcf=b.well_allow_pct
	  FROM tx_well_allow_pct AS a, tx_oil_field_schedule_lite_2 AS b 
	  WHERE b.prod_month='{0}' AND a.prod_year={1} AND b.prod_year={1} AND a.tx_well_id='{2}' AND b.tx_well_id='{2}' AND a.lease_id='{3}' AND b.lease_id='{3}' 
	'''
	well_data = gd.get_data('tx_well_id, lease_id, prod_year', 'tx_well_allow_pct', database='US_Wells_Texas',
	                        server='sql_server', cursor=curr, datatype='plural',
	                        sql_where='NOT tx_well_id IS NULL AND process_code={}'.format(PROCESS_CODE))
	well_data_count = len(well_data)
	well_data_num = 1
	print well_data_count
	for tx_well_id, lease_id, prod_year in well_data:
		well_prod_months = gd.get_data('prod_month', 'tx_oil_field_schedule_lite_2', database='US_Wells_Texas',
		                               server='sql_server', cursor=curr,
		                               sql_where="tx_well_id='{}' AND lease_id='{}' AND prod_year={} AND well_allow_pct > 0".format(
			                               tx_well_id, lease_id, prod_year), debug=debug)
		print '{}/{} {} well_prod_months -- {}% complete'.format(well_data_num, well_data_count, len(well_prod_months),
		                                                         100 * round(
			                                                         float(well_data_num) / float(well_data_count), 3))
		if well_prod_months:
			for prod_month in well_prod_months:
				if debug: print sql_update.format(prod_month, prod_year, tx_well_id, lease_id)
				curr.execute(sql_update.format(prod_month, prod_year, tx_well_id, lease_id))
				gd.commit(curr)
		well_data_num += 1


def update_well_allow_pct(curr, debug=False):
	sql_update = \
		"""
	UPDATE tx_well_allow_pct SET oil_jan_bbl_test=oil_jan_bbl;
	UPDATE tx_well_allow_pct SET lease_well_count=0;
	
	UPDATE tx_well_allow_pct SET lease_well_count=b.lease_well_count
	  FROM tx_well_allow_pct a,
		   (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count FROM tx_well_allow_pct GROUP BY lease_id, prod_year) b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year;
   
	UPDATE tx_well_allow_pct
	  SET oil_jan_bbl=(b.oil_jan_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_jan_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_jan_bbl) AS total_oil_jan_bbl FROM tx_well_allow_pct WHERE oil_jan_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_jan_bbl > 0 AND a.total_oil_jan_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_jan_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_feb_bbl=(b.oil_feb_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_feb_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_feb_bbl) AS total_oil_feb_bbl FROM tx_well_allow_pct WHERE oil_feb_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_feb_bbl > 0 AND a.total_oil_feb_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_feb_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_mar_bbl=(b.oil_mar_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_mar_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_mar_bbl) AS total_oil_mar_bbl FROM tx_well_allow_pct WHERE oil_mar_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_mar_bbl > 0 AND a.total_oil_mar_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_mar_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_apr_bbl=(b.oil_apr_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_apr_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_apr_bbl) AS total_oil_apr_bbl FROM tx_well_allow_pct WHERE oil_apr_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_apr_bbl > 0 AND a.total_oil_apr_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_apr_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_may_bbl=(b.oil_may_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_may_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_may_bbl) AS total_oil_may_bbl FROM tx_well_allow_pct WHERE oil_may_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_may_bbl > 0 AND a.total_oil_may_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_may_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_jun_bbl=(b.oil_jun_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_jun_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_jun_bbl) AS total_oil_jun_bbl FROM tx_well_allow_pct WHERE oil_jun_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_jun_bbl > 0 AND a.total_oil_jun_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_jun_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_jul_bbl=(b.oil_jul_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_jul_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_jul_bbl) AS total_oil_jul_bbl FROM tx_well_allow_pct WHERE oil_jul_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_jul_bbl > 0 AND a.total_oil_jul_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_jul_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_aug_bbl=(b.oil_aug_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_aug_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_aug_bbl) AS total_oil_aug_bbl FROM tx_well_allow_pct WHERE oil_aug_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_aug_bbl > 0 AND a.total_oil_aug_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_aug_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_sep_bbl=(b.oil_sep_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_sep_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_sep_bbl) AS total_oil_sep_bbl FROM tx_well_allow_pct WHERE oil_sep_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_sep_bbl > 0 AND a.total_oil_sep_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_sep_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_oct_bbl=(b.oil_oct_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_oct_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_oct_bbl) AS total_oil_oct_bbl FROM tx_well_allow_pct WHERE oil_oct_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_oct_bbl > 0 AND a.total_oil_oct_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_oct_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_nov_bbl=(b.oil_nov_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_nov_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_nov_bbl) AS total_oil_nov_bbl FROM tx_well_allow_pct WHERE oil_nov_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_nov_bbl > 0 AND a.total_oil_nov_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_nov_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_dec_bbl=(b.oil_dec_bbl + (c.pct_diff/c.lease_well_count))
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_dec_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_dec_bbl) AS total_oil_dec_bbl FROM tx_well_allow_pct WHERE oil_dec_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_dec_bbl > 0 AND a.total_oil_dec_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_dec_bbl > 0;

	UPDATE tx_well_allow_pct
	  SET oil_jan_bbl=(1/c.lease_well_count)
	  FROM tx_well_allow_pct b,
		   (SELECT a.lease_id, a.prod_year, a.lease_well_count, (1-a.total_oil_jan_bbl) AS pct_diff
			  FROM (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count, SUM(oil_jan_bbl) AS total_oil_jan_bbl FROM tx_well_allow_pct WHERE oil_jan_bbl > 0 GROUP BY lease_id, prod_year) AS a
			  WHERE (a.total_oil_jan_bbl > 0 AND a.total_oil_jan_bbl!=1)) c
	  WHERE b.lease_id=c.lease_id AND b.prod_year=c.prod_year AND b.oil_jan_bbl > 0;
	"""
	curr.execute(sql_update)
	gd.commit(curr)


def update_oil_prod_sched_2(curr, debug=False):
	sql_update = \
		"""
	TRUNCATE TABLE tx_oil_prod_schedule_2;
	INSERT INTO tx_oil_prod_schedule_2 (api_number, tx_well_id, lease_id, lease_no, district_no, county_no, well_no, process_code)
		(SELECT DISTINCT api_number, tx_well_id, lease_id, lease_no, district_no, county_no, well_no, process_code FROM tx_ref_well_id WHERE oil_gas_code='O' AND tx_well_id IS NOT NULL AND lease_id IS NOT NULL);
	
	UPDATE tx_oil_prod_schedule_2 SET lease_start_date=b.lease_start_date, lease_end_date=b.lease_end_date
	  FROM tx_oil_prod_schedule_2 a, tx_lease_prod_schedule_2 b
	  WHERE a.lease_id=b.lease_id;

	UPDATE tx_oil_prod_schedule_2 SET lease_well_count=b.total_well_count
	  FROM tx_oil_prod_schedule_2 a, tx_lease_prod_schedule_2 b
	  WHERE a.lease_id=b.lease_id;

	UPDATE tx_oil_prod_schedule_2
	  SET well_status=b.engine_well_status
	  FROM tx_oil_prod_schedule_2 a, tx_well_details b
	  WHERE a.tx_well_id=b.tx_well_id;

	UPDATE tx_oil_prod_schedule_2 SET prev_well_start=well_start_date;

	UPDATE tx_oil_prod_schedule_2
	  SET well_id=b.well_id
	  FROM tx_oil_prod_schedule_2 a, tx_well_details b
	  WHERE a.tx_well_id=b.tx_well_id;

	UPDATE tx_oil_prod_schedule_2 SET well_start_date=NULL, well_end_date=NULL;

	UPDATE tx_oil_prod_schedule_2
	  SET well_start_date=b.spud_date
	  FROM tx_oil_prod_schedule_2 a, tx_well_details b
	  WHERE a.tx_well_id=b.tx_well_id AND b.spud_date IS NOT NULL;

	UPDATE tx_oil_prod_schedule_2
	  SET well_start_date=b.completion_date
	  FROM tx_oil_prod_schedule_2 a, tx_well_details b
	  WHERE a.tx_well_id=b.tx_well_id AND b.completion_date IS NOT NULL AND a.well_start_date IS NULL;

	UPDATE tx_oil_prod_schedule_2
	  SET well_end_date=b.plug_date
	  FROM tx_oil_prod_schedule_2 a, tx_well_details b
	  WHERE a.tx_well_id=b.tx_well_id AND b.plug_date IS NOT NULL;

	UPDATE tx_oil_prod_schedule_2
	  SET well_start_date=lease_start_date WHERE well_start_date IS NOT NULL AND well_start_date < lease_start_date;

	UPDATE tx_oil_prod_schedule_2
	  SET well_start_date=lease_start_date WHERE well_start_date IS NOT NULL AND well_start_date > lease_end_date;

	UPDATE tx_oil_prod_schedule_2
	  SET well_end_date=lease_end_date WHERE well_end_date IS NOT NULL AND well_end_date > lease_end_date;

	UPDATE tx_oil_prod_schedule_2
	  SET well_end_date=lease_end_date WHERE well_end_date IS NULL;

	UPDATE tx_oil_prod_schedule_2
	  SET well_start_date=lease_start_date WHERE well_start_date IS NULL;

	UPDATE tx_oil_prod_schedule_2
	  SET well_end_date=lease_end_date WHERE well_end_date < well_start_date;

	UPDATE tx_oil_prod_schedule_2 SET well_start_date=lease_start_date, well_end_date=lease_end_date WHERE lease_well_count=1;
	"""
	curr.execute(sql_update)
	gd.commit(curr)


def calc_lease_period_prod(curr, debug=False):
	sql_update = \
		"""
	UPDATE tx_oil_prod_schedule_2
	  SET lease_oil_prod=b.total_oil_lease_prod 
	  FROM tx_oil_prod_schedule_2 AS a,
	  (SELECT SUM(oil_prod_vol) AS total_oil_lease_prod FROM tx_oil_production_data WHERE lease_id='{0}' AND prod_date >= '{1}' AND prod_date <= '{2}') AS b 
	  WHERE a.lease_id='{0}' AND a.well_start_date='{1}' AND well_end_date='{2}'
	"""
	well_period_data = gd.get_data('lease_id, well_start_date, well_end_date', 'dbo.tx_oil_prod_schedule_2',
	                               database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural',
	                               sql_where="ISNULL(lease_oil_prod,0)=0")
	well_period_data_count = len(well_period_data)
	well_period_data_num = 1
	for lease_id, first_prod_date, last_prod_date in well_period_data:
		print '{}/{}: {} - {} - {}'.format(well_period_data_num, well_period_data_count, lease_id, first_prod_date,
		                                   last_prod_date)
		curr.execute(sql_update.format(lease_id, first_prod_date, last_prod_date))
		gd.commit(curr)
		well_period_data_num += 1


def create_lease_prod_sched(curr, debug=False):
	sql_update_1 = \
		"""
	UPDATE tx_production SET process_code=0;
	UPDATE tx_production SET process_code=1 FROM tx_production a, tx_well_allow_pct b WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (a.oil_total_bbl+a.csgd_total_mcf) > 0;
	UPDATE tx_production SET process_code=3 WHERE process_code=0 AND (oil_total_bbl+csgd_total_mcf) > 0;
	UPDATE tx_production SET process_code=2 WHERE process_code=3 AND lease_id IN (SELECT DISTINCT lease_id FROM tx_oil_production_data WHERE (oil_prod_vol+csgd_prod_vol)>0);

	UPDATE tx_oil_prod_schedule_2 SET process_code=0;
	UPDATE tx_oil_prod_schedule_2 SET process_code=2 WHERE lease_id IN (SELECT DISTINCT lease_id FROM tx_production WHERE process_code=2);

	UPDATE tx_lease_prod_schedule_2 SET process_code=0;
	UPDATE tx_lease_prod_schedule_2 SET process_code=1 WHERE total_well_count=0;
	UPDATE tx_lease_prod_schedule_2 SET process_code=2 WHERE lease_id IN (SELECT DISTINCT lease_id FROM tx_production WHERE process_code=2) AND process_code=0;
	UPDATE tx_lease_prod_schedule_2 SET process_code=3 WHERE lease_id IN (SELECT DISTINCT lease_id FROM tx_production WHERE process_code=2) AND process_code=1;

	DROP TABLE IF EXISTS tx_lease_prod_schedule;

	CREATE TABLE tx_lease_prod_schedule (
	  schedule_id          INT          IDENTITY,
	  lease_id             NVARCHAR(20) DEFAULT NULL,
	  lease_no             NVARCHAR(6)  DEFAULT NULL,
	  district_no          NVARCHAR(2)  DEFAULT NULL,
	  county_no            NVARCHAR(3)  DEFAULT NULL,
	  operator_no          INT          DEFAULT NULL,
	  field_no             INT          DEFAULT NULL,
	  prod_date            NVARCHAR(6)  DEFAULT NULL,
	  lease_date_min       NVARCHAR(6)  DEFAULT NULL,
	  lease_date_max       NVARCHAR(6)  DEFAULT NULL,
	  prev_lease_oil_prod  FLOAT        DEFAULT NULL,
	  curr_lease_oil_prod  FLOAT        DEFAULT NULL,
	  oil_prod_vol_change  FLOAT        DEFAULT NULL,
	  oil_prod_pct_change  FLOAT        DEFAULT NULL,
	  prev_wells_online    INT          DEFAULT NULL,
	  wells_brought_online INT          DEFAULT NULL,
	  prev_wells_offline   INT          DEFAULT NULL,
	  wells_taken_offline  INT          DEFAULT NULL,
	  total_wells_online   INT          DEFAULT NULL,
	  total_wells_offline  INT          DEFAULT NULL,
	  total_well_count     INT          DEFAULT NULL,
	  well_id_count        INT          DEFAULT NULL,
	  process_code         SMALLINT     DEFAULT NULL,
	  lease_prod_id        INT          DEFAULT NULL,
	  PRIMARY KEY (schedule_id));

	CREATE INDEX county_no_indx ON tx_lease_prod_schedule (county_no);

	CREATE INDEX district_no_indx ON tx_lease_prod_schedule (district_no);

	CREATE INDEX field_no_indx ON tx_lease_prod_schedule (field_no);

	CREATE INDEX lease_district_county_indx ON tx_lease_prod_schedule (lease_no, district_no, county_no);

	CREATE INDEX lease_district_county_operator_field_indx ON tx_lease_prod_schedule (lease_no, district_no, county_no, operator_no, field_no);

	CREATE INDEX lease_district_county_operator_indx ON tx_lease_prod_schedule (lease_no, district_no, county_no, operator_no);

	CREATE INDEX lease_district_indx ON tx_lease_prod_schedule (lease_no, district_no);

	CREATE INDEX lease_id_indx ON tx_lease_prod_schedule (lease_id);

	CREATE INDEX lease_id_operator_field_indx ON tx_lease_prod_schedule (lease_id, operator_no, field_no);

	CREATE INDEX lease_id_operator_indx ON tx_lease_prod_schedule (lease_id, operator_no);

	CREATE INDEX lease_id_prod_date_indx ON tx_lease_prod_schedule (lease_id, prod_date);

	CREATE INDEX lease_no_indx ON tx_lease_prod_schedule (lease_no);

	CREATE INDEX operator_no_indx ON tx_lease_prod_schedule (operator_no);

	CREATE INDEX process_code_indx ON tx_lease_prod_schedule (process_code);

	CREATE INDEX prod_date_indx ON tx_lease_prod_schedule (prod_date);

	CREATE INDEX lease_prod_id_indx ON tx_lease_prod_schedule (lease_prod_id);

	DROP TABLE IF EXISTS tx_lease_prod_schedule_temp;

	CREATE TABLE tx_lease_prod_schedule_temp (
	  schedule_id          INT          IDENTITY,
	  lease_id             NVARCHAR(20) DEFAULT NULL,
	  lease_no             NVARCHAR(6)  DEFAULT NULL,
	  district_no          NVARCHAR(2)  DEFAULT NULL,
	  county_no            NVARCHAR(3)  DEFAULT NULL,
	  operator_no          INT          DEFAULT NULL,
	  field_no             INT          DEFAULT NULL,
	  prod_date            NVARCHAR(6)  DEFAULT NULL,
	  lease_date_min       NVARCHAR(6)  DEFAULT NULL,
	  lease_date_max       NVARCHAR(6)  DEFAULT NULL,
	  prev_lease_oil_prod  FLOAT        DEFAULT NULL,
	  curr_lease_oil_prod  FLOAT        DEFAULT NULL,
	  oil_prod_vol_change  FLOAT        DEFAULT NULL,
	  oil_prod_pct_change  FLOAT        DEFAULT NULL,
	  prev_wells_online    INT          DEFAULT NULL,
	  wells_brought_online INT          DEFAULT NULL,
	  prev_wells_offline   INT          DEFAULT NULL,
	  wells_taken_offline  INT          DEFAULT NULL,
	  total_wells_online   INT          DEFAULT NULL,
	  total_wells_offline  INT          DEFAULT NULL,
	  total_well_count     INT          DEFAULT NULL,
	  well_id_count        INT          DEFAULT NULL,
	  process_code         SMALLINT     DEFAULT NULL,
	  lease_prod_id        INT          DEFAULT NULL,
	  PRIMARY KEY (schedule_id));

	CREATE INDEX county_no_indx ON tx_lease_prod_schedule_temp (county_no);

	CREATE INDEX district_no_indx ON tx_lease_prod_schedule_temp (district_no);

	CREATE INDEX field_no_indx ON tx_lease_prod_schedule_temp (field_no);

	CREATE INDEX lease_district_county_indx ON tx_lease_prod_schedule_temp (lease_no, district_no, county_no);

	CREATE INDEX lease_district_county_operator_field_indx ON tx_lease_prod_schedule_temp (lease_no, district_no, county_no, operator_no, field_no);

	CREATE INDEX lease_district_county_operator_indx ON tx_lease_prod_schedule_temp (lease_no, district_no, county_no, operator_no);

	CREATE INDEX lease_district_indx ON tx_lease_prod_schedule_temp (lease_no, district_no);

	CREATE INDEX lease_id_indx ON tx_lease_prod_schedule_temp (lease_id);

	CREATE INDEX lease_id_operator_field_indx ON tx_lease_prod_schedule_temp (lease_id, operator_no, field_no);

	CREATE INDEX lease_id_operator_indx ON tx_lease_prod_schedule_temp (lease_id, operator_no);

	CREATE INDEX lease_id_prod_date_indx ON tx_lease_prod_schedule_temp (lease_id, prod_date);

	CREATE INDEX lease_no_indx ON tx_lease_prod_schedule_temp (lease_no);

	CREATE INDEX operator_no_indx ON tx_lease_prod_schedule_temp (operator_no);

	CREATE INDEX process_code_indx ON tx_lease_prod_schedule_temp (process_code);

	CREATE INDEX prod_date_indx ON tx_lease_prod_schedule_temp (prod_date);

	CREATE INDEX lease_prod_id_indx ON tx_lease_prod_schedule_temp (lease_prod_id);


	INSERT INTO tx_lease_prod_schedule_temp (lease_id, prod_date, process_code)
	  (SELECT DISTINCT lease_id, well_start_date, 1 FROM tx_oil_prod_schedule_2 WHERE process_code=2);

	INSERT INTO tx_lease_prod_schedule_temp (lease_id, prod_date, process_code)
	  (SELECT DISTINCT lease_id, well_end_date, 1 FROM tx_oil_prod_schedule_2 WHERE process_code=2);

	UPDATE tx_lease_prod_schedule_temp SET lease_date_min=b.lease_start_date, lease_date_max=b.lease_end_date
	  FROM tx_lease_prod_schedule_temp a, tx_oil_prod_schedule_2 b
	  WHERE a.lease_id=b.lease_id AND b.process_code=2;

	INSERT INTO tx_lease_prod_schedule (lease_id, lease_date_min, lease_date_max, prod_date)
	  (SELECT DISTINCT lease_id, lease_date_min, lease_date_max, prod_date FROM tx_lease_prod_schedule_temp);

	UPDATE tx_lease_prod_schedule SET process_code=0;
	UPDATE tx_lease_prod_schedule SET process_code=2 FROM tx_lease_prod_schedule a, tx_oil_prod_schedule_2 b WHERE a.lease_id=b.lease_id AND b.process_code=2;

	UPDATE tx_lease_prod_schedule SET wells_brought_online=0 WHERE wells_brought_online IS NULL;
	UPDATE tx_lease_prod_schedule SET wells_taken_offline=0 WHERE wells_taken_offline IS NULL;
	UPDATE tx_lease_prod_schedule SET prev_wells_online=0 WHERE prod_date=lease_date_min;
	UPDATE tx_lease_prod_schedule SET total_wells_online=wells_brought_online WHERE prod_date=lease_date_min;
	UPDATE tx_lease_prod_schedule SET prev_lease_oil_prod=0 WHERE prod_date=lease_date_min;
	UPDATE tx_lease_prod_schedule SET prev_lease_oil_prod=0 WHERE prev_lease_oil_prod IS NULL;
	UPDATE tx_lease_prod_schedule SET curr_lease_oil_prod=0 WHERE curr_lease_oil_prod IS NULL;

	UPDATE tx_lease_prod_schedule
	  SET curr_lease_oil_prod=ISNULL(b.oil_prod_vol,0)
	  FROM tx_lease_prod_schedule AS a,
		   tx_oil_production_data AS b
	  WHERE a.lease_id=b.lease_id AND a.prod_date=b.prod_date;
	"""
	curr.execute(sql_update_1)
	gd.commit(curr)


def update_prev_prod(curr, debug=False):
	sql_update = \
		"""
	UPDATE tx_lease_prod_schedule
	  SET prev_lease_oil_prod=ISNULL(b.oil_prod_vol,0)
	  FROM tx_lease_prod_schedule AS a, 
		   (SELECT oil_prod_vol FROM tx_oil_production_data WHERE lease_id='{0}' AND prod_date='{1}') AS b 
	  WHERE a.lease_id='{0}' AND a.prod_date='{2}'
	"""
	lease_prod_data = gd.get_data('lease_id, prod_date', 'dbo.tx_lease_prod_schedule', database='US_Wells_Texas',
	                              server='sql_server', cursor=curr, datatype='plural',
	                              sql_where="NOT prod_date=lease_date_min AND process_code=2")
	lease_prod_data_count = len(lease_prod_data)
	lease_prod_data_num = 1
	for lease_id, curr_prod_date in lease_prod_data:
		print '{}/{}: {} - {}'.format(lease_prod_data_num, lease_prod_data_count, lease_id, curr_prod_date)
		curr_prod_date_indx = PROD_DATES.index(curr_prod_date)
		prev_prod_date_indx = curr_prod_date_indx - 1
		prev_prod_date = PROD_DATES[prev_prod_date_indx]
		if debug: print sql_update.format(lease_id, prev_prod_date, curr_prod_date)
		curr.execute(sql_update.format(lease_id, prev_prod_date, curr_prod_date))
		gd.commit(curr)
		lease_prod_data_num += 1


def update_lease_prod_sched(curr, debug=False):
	sql_update = \
		"""
	UPDATE tx_lease_prod_schedule
	  SET oil_prod_vol_change=(ISNULL(curr_lease_oil_prod,0) - ISNULL(prev_lease_oil_prod,0));

	UPDATE tx_lease_prod_schedule
	  SET oil_prod_pct_change=ROUND(ISNULL(curr_lease_oil_prod,0)/prev_lease_oil_prod, 3)
	  WHERE ISNULL(prev_lease_oil_prod,0) > 0;

	UPDATE tx_lease_prod_schedule SET total_well_count=b.total_well_count
	  FROM tx_lease_prod_schedule a, tx_lease_prod_schedule_2 b
	  WHERE a.lease_id=b.lease_id AND b.process_code=2;

	UPDATE tx_oil_prod_schedule_2
	  SET prod_start_id=b.schedule_id
	  FROM tx_oil_prod_schedule_2 AS a, tx_lease_prod_schedule AS b
	  WHERE a.lease_id=b.lease_id AND a.well_start_date=b.prod_date;

	UPDATE tx_oil_prod_schedule_2
	  SET prod_end_id=b.schedule_id
	  FROM tx_oil_prod_schedule_2 AS a, tx_lease_prod_schedule AS b
	  WHERE a.lease_id=b.lease_id AND a.well_end_date=b.prod_date;

	UPDATE tx_lease_prod_schedule
	  SET wells_brought_online=b.wells_brought_online
	  FROM tx_lease_prod_schedule AS a,
	  (SELECT prod_start_id, COUNT(DISTINCT tx_well_id) AS wells_brought_online FROM tx_oil_prod_schedule_2 WHERE ISNULL(prod_start_id,0) > 0 AND process_code!=99 GROUP BY prod_start_id) AS b
	  WHERE a.schedule_id=b.prod_start_id;

	UPDATE tx_lease_prod_schedule
	  SET wells_taken_offline=b.wells_taken_offline
	  FROM tx_lease_prod_schedule AS a,
	  (SELECT prod_end_id, COUNT(DISTINCT tx_well_id) AS wells_taken_offline FROM tx_oil_prod_schedule_2 WHERE ISNULL(prod_end_id,0) > 0 AND process_code!=99 GROUP BY prod_end_id) AS b
	  WHERE a.schedule_id=b.prod_end_id;

	UPDATE tx_lease_prod_schedule
	  SET curr_lease_oil_prod=ISNULL(b.oil_prod_vol,0)
	  FROM tx_lease_prod_schedule AS a,
		   tx_oil_production_data AS b
	  WHERE a.lease_id=b.lease_id AND a.prod_date=b.prod_date AND a.process_code=2;

	UPDATE tx_lease_prod_schedule
	  SET oil_prod_vol_change=(ISNULL(curr_lease_oil_prod,0) - ISNULL(prev_lease_oil_prod,0)) WHERE process_code=2;

	UPDATE tx_lease_prod_schedule
	  SET oil_prod_pct_change=ROUND(ISNULL(curr_lease_oil_prod,0)/prev_lease_oil_prod, 3)
	  WHERE ISNULL(prev_lease_oil_prod,0) > 0 AND process_code=2;


	UPDATE tx_oil_prod_schedule_2
	  SET prod_start_id=b.schedule_id
	  FROM tx_oil_prod_schedule_2 AS a, tx_lease_prod_schedule AS b
	  WHERE a.lease_id=b.lease_id AND a.well_start_date=b.prod_date AND a.process_code=2;

	UPDATE tx_oil_prod_schedule_2
	  SET prod_end_id=b.schedule_id
	  FROM tx_oil_prod_schedule_2 AS a, tx_lease_prod_schedule AS b
	  WHERE a.lease_id=b.lease_id AND a.well_end_date=b.prod_date  AND a.process_code=2;

	UPDATE tx_lease_prod_schedule
	  SET wells_brought_online=b.wells_brought_online
	  FROM tx_lease_prod_schedule AS a,
	  (SELECT prod_start_id, COUNT(DISTINCT tx_well_id) AS wells_brought_online FROM tx_oil_prod_schedule_2 WHERE ISNULL(prod_start_id,0) > 0 AND process_code=2 GROUP BY prod_start_id) AS b
	  WHERE a.schedule_id=b.prod_start_id AND a.process_code=2;

	UPDATE tx_lease_prod_schedule
	  SET wells_taken_offline=b.wells_taken_offline
	  FROM tx_lease_prod_schedule AS a,
	  (SELECT prod_end_id, COUNT(DISTINCT tx_well_id) AS wells_taken_offline FROM tx_oil_prod_schedule_2 WHERE ISNULL(prod_end_id,0) > 0 AND process_code=2 GROUP BY prod_end_id) AS b
	  WHERE a.schedule_id=b.prod_end_id AND a.process_code=2;

	"""
	curr.execute(sql_update)
	gd.commit(curr)


def update_oil_well_prod_dates(curr, debug=False):
	sql_update = \
		"""
	DROP TABLE IF EXISTS tx_well_prod_dates;

	CREATE TABLE tx_well_prod_dates (
	  id               INT          IDENTITY,
	  lease_id         NVARCHAR(30) DEFAULT NULL,
	  tx_well_id       VARCHAR(16)  DEFAULT NULL,
	  start_year       INT          DEFAULT NULL,
	  end_year         INT          DEFAULT NULL,
	  process_code     INT          DEFAULT NULL,
	  PRIMARY KEY (id));

	CREATE INDEX lease_id_indx ON tx_well_prod_dates (lease_id);

	CREATE INDEX tx_well_id_indx ON tx_well_prod_dates (tx_well_id);

	CREATE INDEX start_year_indx ON tx_well_prod_dates (start_year);

	CREATE INDEX end_year_indx ON tx_well_prod_dates (end_year);

	CREATE INDEX process_code_indx ON tx_well_prod_dates (process_code);

	INSERT INTO tx_well_prod_dates (lease_id, tx_well_id, start_year, end_year, process_code)
	  (SELECT DISTINCT lease_id, tx_well_id, CONVERT(INT,SUBSTRING(well_start_date,1,4)), CONVERT(INT,SUBSTRING(well_end_date,1,4)), 1 FROM tx_oil_prod_schedule_2 WHERE process_code=2);
	
	TRUNCATE TABLE tx_well_prod_pct;
	"""
	curr.execute(sql_update)
	gd.commit(curr)


def update_prod_pct_table(curr, debug=False):
	sql_insert = "INSERT INTO tx_well_prod_pct (lease_id, tx_well_id, prod_year) VALUES ('{}', '{}', {})"
	well_period_data = gd.get_data('lease_id, tx_well_id, start_year, end_year', 'dbo.tx_well_prod_dates',
	                               database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural',
	                               sql_where='process_code=1')
	well_period_count = len(well_period_data)
	well_period_num = 1
	for lease_id, tx_well_id, start_year, end_year in well_period_data:
		print '{}/{}: {}'.format(well_period_num, well_period_count, tx_well_id)
		for prod_year in range(start_year, end_year + 1):
			if debug: print sql_insert.format(lease_id, tx_well_id, prod_year)
			curr.execute(sql_insert.format(lease_id, tx_well_id, prod_year))
			gd.commit(curr)
		well_period_num += 1


def update_well_prod_pct_split(curr, debug=False):
	lease_id_count = gd.get_data('COUNT(DISTINCT lease_id)', 'dbo.tx_lease_prod_schedule',
	                             cursor=curr, datatype='int', single_value=True)/4
	sql_update = \
		"""
		UPDATE tx_well_prod_pct SET process_code=0;
		UPDATE tx_lease_prod_schedule SET process_code=0;
		
		UPDATE tx_well_prod_pct SET process_code=1 
		  WHERE lease_id IN (SELECT TOP {0} a.lease_id FROM (SELECT DISTINCT lease_id FROM tx_lease_prod_schedule WHERE process_code=0) AS a);
		
		UPDATE tx_lease_prod_schedule SET process_code=1 
		  WHERE lease_id IN (SELECT DISTINCT lease_id FROM tx_well_prod_pct WHERE process_code=1);
		
		UPDATE tx_well_prod_pct SET process_code=2 
		  WHERE lease_id IN (SELECT TOP {0} a.lease_id FROM (SELECT DISTINCT lease_id FROM tx_lease_prod_schedule WHERE process_code=0) AS a);
		
		UPDATE tx_lease_prod_schedule SET process_code=2 
		  WHERE lease_id IN (SELECT DISTINCT lease_id FROM tx_well_prod_pct WHERE process_code=2);
		
		UPDATE tx_well_prod_pct SET process_code=3 
		  WHERE lease_id IN (SELECT TOP {0} a.lease_id FROM (SELECT DISTINCT lease_id FROM tx_lease_prod_schedule WHERE process_code=0) AS a);
		
		UPDATE tx_lease_prod_schedule SET process_code=3 
		  WHERE lease_id IN (SELECT DISTINCT lease_id FROM tx_well_prod_pct WHERE process_code=3);
		
		UPDATE tx_well_prod_pct SET process_code=4 
		  WHERE lease_id IN (SELECT TOP {0} a.lease_id FROM (SELECT DISTINCT lease_id FROM tx_lease_prod_schedule WHERE process_code=0) AS a);
		
		UPDATE tx_lease_prod_schedule SET process_code=4 
		  WHERE lease_id IN (SELECT DISTINCT lease_id FROM tx_well_prod_pct WHERE process_code=4);
		"""
	curr.execute(sql_update.format(lease_id_count))
	gd.commit(curr)

	sql_update_1 = \
		"""
	DROP TABLE IF EXISTS tx_well_prod_pct_1;
	CREATE TABLE tx_well_prod_pct_1 (
	  id           INT          IDENTITY,
	  lease_id     NVARCHAR(20) DEFAULT NULL,
	  tx_well_id   NVARCHAR(20) DEFAULT NULL,
	  prod_year    INT          DEFAULT NULL,
	  jan_prod_pct FLOAT        DEFAULT NULL,
	  feb_prod_pct FLOAT        DEFAULT NULL,
	  mar_prod_pct FLOAT        DEFAULT NULL,
	  apr_prod_pct FLOAT        DEFAULT NULL,
	  may_prod_pct FLOAT        DEFAULT NULL,
	  jun_prod_pct FLOAT        DEFAULT NULL,
	  jul_prod_pct FLOAT        DEFAULT NULL,
	  aug_prod_pct FLOAT        DEFAULT NULL,
	  sep_prod_pct FLOAT        DEFAULT NULL,
	  oct_prod_pct FLOAT        DEFAULT NULL,
	  nov_prod_pct FLOAT        DEFAULT NULL,
	  dec_prod_pct FLOAT        DEFAULT NULL,
	  process_code TINYINT      DEFAULT NULL,
	  PRIMARY KEY (id));
	
	CREATE INDEX lease_id_indx ON tx_well_prod_pct_1 (lease_id);
	
	CREATE INDEX prod_year_indx ON tx_well_prod_pct_1 (prod_year);
	
	CREATE INDEX tx_wel_id_prod_year_indx ON tx_well_prod_pct_1 (tx_well_id, prod_year);
	
	CREATE INDEX tx_well_id_indx ON tx_well_prod_pct_1 (tx_well_id);
	
	SET IDENTITY_INSERT tx_well_prod_pct_1 ON;
	INSERT INTO tx_well_prod_pct_1 (id, lease_id, tx_well_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code)
	  (SELECT DISTINCT id, lease_id, tx_well_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code
	   FROM tx_well_prod_pct WHERE process_code=1);
	SET IDENTITY_INSERT tx_well_prod_pct_1 OFF;
	"""
	curr.execute(sql_update_1)
	gd.commit(curr)

	sql_update_2 = \
		"""
	DROP TABLE IF EXISTS tx_well_prod_pct_2;
	CREATE TABLE tx_well_prod_pct_2 (
	  id           INT          IDENTITY,
	  lease_id     NVARCHAR(20) DEFAULT NULL,
	  tx_well_id   NVARCHAR(20) DEFAULT NULL,
	  prod_year    INT          DEFAULT NULL,
	  jan_prod_pct FLOAT        DEFAULT NULL,
	  feb_prod_pct FLOAT        DEFAULT NULL,
	  mar_prod_pct FLOAT        DEFAULT NULL,
	  apr_prod_pct FLOAT        DEFAULT NULL,
	  may_prod_pct FLOAT        DEFAULT NULL,
	  jun_prod_pct FLOAT        DEFAULT NULL,
	  jul_prod_pct FLOAT        DEFAULT NULL,
	  aug_prod_pct FLOAT        DEFAULT NULL,
	  sep_prod_pct FLOAT        DEFAULT NULL,
	  oct_prod_pct FLOAT        DEFAULT NULL,
	  nov_prod_pct FLOAT        DEFAULT NULL,
	  dec_prod_pct FLOAT        DEFAULT NULL,
	  process_code TINYINT      DEFAULT NULL,
	  PRIMARY KEY (id));
	
	CREATE INDEX lease_id_indx ON tx_well_prod_pct_2 (lease_id);
	
	CREATE INDEX prod_year_indx ON tx_well_prod_pct_2 (prod_year);
	
	CREATE INDEX tx_wel_id_prod_year_indx ON tx_well_prod_pct_2 (tx_well_id, prod_year);
	
	CREATE INDEX tx_well_id_indx ON tx_well_prod_pct_2 (tx_well_id);
	
	SET IDENTITY_INSERT tx_well_prod_pct_2 ON;
	INSERT INTO tx_well_prod_pct_2 (id, lease_id, tx_well_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code)
	  (SELECT DISTINCT id, lease_id, tx_well_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code
	   FROM tx_well_prod_pct WHERE process_code=2);
	SET IDENTITY_INSERT tx_well_prod_pct_2 OFF;
	"""
	curr.execute(sql_update_2)
	gd.commit(curr)

	sql_update_3 = \
		"""
	DROP TABLE IF EXISTS tx_well_prod_pct_3;
	CREATE TABLE tx_well_prod_pct_3 (
	  id           INT          IDENTITY,
	  lease_id     NVARCHAR(20) DEFAULT NULL,
	  tx_well_id   NVARCHAR(20) DEFAULT NULL,
	  prod_year    INT          DEFAULT NULL,
	  jan_prod_pct FLOAT        DEFAULT NULL,
	  feb_prod_pct FLOAT        DEFAULT NULL,
	  mar_prod_pct FLOAT        DEFAULT NULL,
	  apr_prod_pct FLOAT        DEFAULT NULL,
	  may_prod_pct FLOAT        DEFAULT NULL,
	  jun_prod_pct FLOAT        DEFAULT NULL,
	  jul_prod_pct FLOAT        DEFAULT NULL,
	  aug_prod_pct FLOAT        DEFAULT NULL,
	  sep_prod_pct FLOAT        DEFAULT NULL,
	  oct_prod_pct FLOAT        DEFAULT NULL,
	  nov_prod_pct FLOAT        DEFAULT NULL,
	  dec_prod_pct FLOAT        DEFAULT NULL,
	  process_code TINYINT      DEFAULT NULL,
	  PRIMARY KEY (id));
	
	CREATE INDEX lease_id_indx ON tx_well_prod_pct_3 (lease_id);
	
	CREATE INDEX prod_year_indx ON tx_well_prod_pct_3 (prod_year);
	
	CREATE INDEX tx_wel_id_prod_year_indx ON tx_well_prod_pct_3 (tx_well_id, prod_year);
	
	CREATE INDEX tx_well_id_indx ON tx_well_prod_pct_3 (tx_well_id);
	
	SET IDENTITY_INSERT tx_well_prod_pct_3 ON;
	INSERT INTO tx_well_prod_pct_3 (id, lease_id, tx_well_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code)
	  (SELECT DISTINCT id, lease_id, tx_well_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code
	   FROM tx_well_prod_pct WHERE process_code=3);
	SET IDENTITY_INSERT tx_well_prod_pct_3 OFF;
	"""
	curr.execute(sql_update_3)
	gd.commit(curr)

	sql_update_4 = \
		"""
	DROP TABLE IF EXISTS tx_well_prod_pct_4;
	CREATE TABLE tx_well_prod_pct_4 (
	  id           INT          IDENTITY,
	  lease_id     NVARCHAR(20) DEFAULT NULL,
	  tx_well_id   NVARCHAR(20) DEFAULT NULL,
	  prod_year    INT          DEFAULT NULL,
	  jan_prod_pct FLOAT        DEFAULT NULL,
	  feb_prod_pct FLOAT        DEFAULT NULL,
	  mar_prod_pct FLOAT        DEFAULT NULL,
	  apr_prod_pct FLOAT        DEFAULT NULL,
	  may_prod_pct FLOAT        DEFAULT NULL,
	  jun_prod_pct FLOAT        DEFAULT NULL,
	  jul_prod_pct FLOAT        DEFAULT NULL,
	  aug_prod_pct FLOAT        DEFAULT NULL,
	  sep_prod_pct FLOAT        DEFAULT NULL,
	  oct_prod_pct FLOAT        DEFAULT NULL,
	  nov_prod_pct FLOAT        DEFAULT NULL,
	  dec_prod_pct FLOAT        DEFAULT NULL,
	  process_code TINYINT      DEFAULT NULL,
	  PRIMARY KEY (id));
	
	CREATE INDEX lease_id_indx ON tx_well_prod_pct_4 (lease_id);
	
	CREATE INDEX prod_year_indx ON tx_well_prod_pct_4 (prod_year);
	
	CREATE INDEX tx_wel_id_prod_year_indx ON tx_well_prod_pct_4 (tx_well_id, prod_year);
	
	CREATE INDEX tx_well_id_indx ON tx_well_prod_pct_4 (tx_well_id);
	
	SET IDENTITY_INSERT tx_well_prod_pct_4 ON;
	INSERT INTO tx_well_prod_pct_4 (id, lease_id, tx_well_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code)
	  (SELECT DISTINCT id, lease_id, tx_well_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code
	   FROM tx_well_prod_pct WHERE process_code=4);
	SET IDENTITY_INSERT tx_well_prod_pct_4 OFF;
	"""
	curr.execute(sql_update_4)
	gd.commit(curr)


def update_prod_pct_main(curr, debug=False):
	sql_update_main = \
		"""
	UPDATE tx_well_prod_pct SET process_code=1;

	UPDATE tx_well_prod_pct   SET jan_prod_pct=0,feb_prod_pct=0,mar_prod_pct=0,
	                              apr_prod_pct=0,may_prod_pct=0,jun_prod_pct=0,
								  jul_prod_pct=0,aug_prod_pct=0,sep_prod_pct=0,
								  oct_prod_pct=0,nov_prod_pct=0,dec_prod_pct=0 WHERE process_code=1;
	
	UPDATE tx_well_prod_pct_1 SET jan_prod_pct=0,feb_prod_pct=0,mar_prod_pct=0,
	                              apr_prod_pct=0,may_prod_pct=0,jun_prod_pct=0,
								  jul_prod_pct=0,aug_prod_pct=0,sep_prod_pct=0,
								  oct_prod_pct=0,nov_prod_pct=0,dec_prod_pct=0;
	
	UPDATE tx_well_prod_pct_2 SET jan_prod_pct=0,feb_prod_pct=0,mar_prod_pct=0,
	                              apr_prod_pct=0,may_prod_pct=0,jun_prod_pct=0,
								  jul_prod_pct=0,aug_prod_pct=0,sep_prod_pct=0,
								  oct_prod_pct=0,nov_prod_pct=0,dec_prod_pct=0;
	
	UPDATE tx_well_prod_pct_3 SET jan_prod_pct=0,feb_prod_pct=0,mar_prod_pct=0,
	                              apr_prod_pct=0,may_prod_pct=0,jun_prod_pct=0,
								  jul_prod_pct=0,aug_prod_pct=0,sep_prod_pct=0,
								  oct_prod_pct=0,nov_prod_pct=0,dec_prod_pct=0;
	
	UPDATE tx_well_prod_pct_4 SET jan_prod_pct=0,feb_prod_pct=0,mar_prod_pct=0,
	                              apr_prod_pct=0,may_prod_pct=0,jun_prod_pct=0,
								  jul_prod_pct=0,aug_prod_pct=0,sep_prod_pct=0,
								  oct_prod_pct=0,nov_prod_pct=0,dec_prod_pct=0;
	"""
	curr.execute(sql_update_main)
	gd.commit(curr)


def lease_prod_allocation(forecast_code, debug=False):
	# Run with forecast codes 1, 2, 3, 4 concurrently
	start_time = gd.get_datetime()
	print '({}) -- lease prod allocation start: {}'.format(forecast_code, start_time)
	conn = gd.get_connection(server='sql_server', database='US_Wells_Texas', us_wells=True)
	curr = conn.cursor()
	prod_pct_col_str = ', '.join(PROD_PCT_COLS)
	prod_pct_var_str = ', '.join((["'{}'"] * 2) + ["{}"] * 15)

	sql_update = \
		'''
	UPDATE tx_well_prod_pct_{} 
	  SET jan_prod_pct={},feb_prod_pct={},mar_prod_pct={},apr_prod_pct={},may_prod_pct={},jun_prod_pct={},jul_prod_pct={},aug_prod_pct={},sep_prod_pct={},oct_prod_pct={},nov_prod_pct={},dec_prod_pct={} 
	  WHERE lease_id='{}' AND tx_well_id='{}' AND prod_year={}
	'''

	sql_where = "process_code={}".format(forecast_code)
	lease_prod_data = gd.get_data("lease_id, lease_date_min, lease_date_max", "tx_lease_prod_schedule",
	                              database="US_Wells_Texas", server='sql_server', cursor=curr, datatype="plural",
	                              sql_where=sql_where)
	lease_prod_count = len(lease_prod_data)
	lease_prod_num = 1
	for lease_id, lease_date_min, lease_date_max in lease_prod_data:
		print '({}) -- {}/{}: {} - {} - {}'.format(forecast_code, lease_prod_num, lease_prod_count, lease_id,
		                                           lease_date_min, lease_date_max)
		print ''
		all_prod_dates = get_prod_dates(lease_date_min, lease_date_max)
		all_prod_years = sorted(list(set([int(prod_date[:4]) for prod_date in all_prod_dates])))
		sql_where = "lease_id='{}' AND lease_date_min='{}' AND lease_date_max='{}' AND process_code={}".format(lease_id,
		                                                                                                       lease_date_min,
		                                                                                                       lease_date_max,
		                                                                                                       forecast_code)
		schedule_dates = gd.get_data('prod_date', 'tx_lease_prod_schedule', cursor=curr, database='US_Wells_Texas',
		                             server='sql_server', sql_where=sql_where)
		well_prod_pcts = {prod_year: {} for prod_year in all_prod_years}
		wells_online = []
		wells_offline = []
		prev_year = min([int(prod_date[:4]) for prod_date in all_prod_dates])
		for prod_date in all_prod_dates:
			prod_year = int(prod_date[:4])
			prod_month = prod_date[4:]
			prev_month = MONTH_NUM_LIST[MONTH_NUM_LIST.index(prod_month) - 1]
			if prev_year != prod_year:
				for well_id in wells_online:
					well_prod_pcts[prod_year][well_id] = {month_num: 0.0 for month_num in MONTH_NUM_LIST}
			if prod_date in schedule_dates:
				col_names = "schedule_id, prev_lease_oil_prod, curr_lease_oil_prod, oil_prod_vol_change"
				sql_where = "lease_id='{}' AND lease_date_min='{}' AND lease_date_max='{}' AND prod_date='{}'\
				             AND process_code={}".format(lease_id, lease_date_min, lease_date_max, prod_date, forecast_code)
				well_sched_data = gd.get_data(col_names, "tx_lease_prod_schedule", database='US_Wells_Texas',
				                              server='sql_server', cursor=curr, datatype="plural", sql_where=sql_where)
				for schedule_id, prev_lease_oil_prod, curr_lease_oil_prod, oil_prod_vol_change in well_sched_data:
					begin_well_ids = gd.get_data("tx_well_id", "tx_oil_prod_schedule_2", database='US_Wells_Texas',
					                             server='sql_server', cursor=curr,
					                             sql_where="prod_start_id={}".format(schedule_id))
					end_well_ids = gd.get_data("tx_well_id", "tx_oil_prod_schedule_2", database='US_Wells_Texas',
					                           server='sql_server', cursor=curr,
					                           sql_where="prod_end_id={}".format(schedule_id))
					if debug:
						print '({}) begin_well_ids: {}'.format(prod_date, begin_well_ids)
						print '({}) end_well_ids  : {}'.format(prod_date, end_well_ids)
						print ''
					for well_id in begin_well_ids:
						well_prod_pcts[prod_year][well_id] = {month_num: 0.0 for month_num in MONTH_NUM_LIST}
					# If prod_date is the beginning of lease production, then divide production evenly between producing wells
					# *** Need to incorporate allowable percentages and well production volumes on different leases to determine more accurate production percentages for each well ***
					new_well_count = len(begin_well_ids)
					if new_well_count:
						if prod_date == lease_date_min:
							for well_id in begin_well_ids:
								well_prod_pcts[prod_year][well_id][prod_month] = 1.0 / float(new_well_count)
						elif oil_prod_vol_change <= 0:
							for well_id in wells_online:
								prev_prod_pct = float(well_prod_pcts[prod_year][well_id][prev_month])
								well_prod_pcts[prod_year][well_id][prod_month] = float(0.98 * prev_prod_pct)
							for well_id in begin_well_ids:
								well_prod_pcts[prod_year][well_id][prod_month] = 0.02 / float(new_well_count)
						elif oil_prod_vol_change > 0:
							prod_inc_pct = float(prev_lease_oil_prod) / float(curr_lease_oil_prod)
							if prod_inc_pct > 0.02:
								for well_id in wells_online:
									prev_prod_pct = float(well_prod_pcts[prod_year][well_id][prev_month])
									well_prod_pcts[prod_year][well_id][prod_month] = prev_prod_pct * float(
										prod_inc_pct - 0.02)
								for well_id in begin_well_ids:
									well_prod_pcts[prod_year][well_id][prod_month] = (1 - (
											prod_inc_pct - 0.02)) / float(new_well_count)
							else:
								for well_id in wells_online:
									prev_prod_pct = float(well_prod_pcts[prod_year][well_id][prev_month])
									well_prod_pcts[prod_year][well_id][prod_month] = prev_prod_pct * float(
										1 - prod_inc_pct)
								for well_id in begin_well_ids:
									well_prod_pcts[prod_year][well_id][prod_month] = float(prod_inc_pct) / float(
										new_well_count)
					else:
						for well_id in wells_online:
							well_prod_pcts[prod_year][well_id][prod_month] = float(
								well_prod_pcts[prod_year][well_id][prev_month])
					if len(wells_online + begin_well_ids):
						total_prod_pct = float(sum([well_prod_pcts[prod_year][well_id][prod_month] for well_id in
						                            (wells_online + begin_well_ids)]))
						pct_corr_factor = float(1 - total_prod_pct) / float(len(wells_online + begin_well_ids))
						for well_id in (wells_online + begin_well_ids):
							well_prod_pcts[prod_year][well_id][prod_month] = max(0, pct_corr_factor +
							                                                     well_prod_pcts[prod_year][well_id][
								                                                     prod_month])
					wells_offline += end_well_ids
					wells_online += begin_well_ids
					wells_online = [well_id for well_id in wells_online if well_id not in wells_offline]
			else:
				producing_wells = [wellid for wellid in well_prod_pcts[prod_year].keys() if wellid in wells_online]
				if debug:
					print ''
					print '({}) producing_wells: {}'.format(prod_date, producing_wells)
				for well_id in producing_wells:
					well_prod_pcts[prod_year][well_id][prod_month] = well_prod_pcts[prod_year][well_id][prev_month]
					if debug: print '{} -- {} -- {} -- {}'.format(well_id, prod_year, prod_month,
					                                              well_prod_pcts[prod_year][well_id][prev_month])
				total_prod_pct = sum([well_prod_pcts[prod_year][well_id][prod_month] for well_id in producing_wells])
				if total_prod_pct < 1:
					prod_pct_diff = 1 - total_prod_pct
					for well_id in producing_wells:
						well_prod_pcts[prod_year][well_id][prod_month] = max(0, well_prod_pcts[prod_year][well_id][
							prod_month] + (float(prod_pct_diff) / float(len(producing_wells))))
			# Ensure the sum of all well production percentages = 1 for the production date
			# try:
			#    assert sum([well_prod_pcts[prod_year][wellid][prod_month] for wellid in well_prod_pcts[prod_year].keys()]) in [0, 1]
			# except:
			#    print well_prod_pcts[prod_year], sum([well_prod_pcts[prod_year][wellid][prod_month] for wellid in well_prod_pcts[prod_year].keys()])
			prev_year = prod_year
		if debug: print 'well_prod_pcts: {}'.format(well_prod_pcts)
		prod_year_count = len(well_prod_pcts.keys())
		prod_year_num = 1
		for lease_prod_year in sorted(well_prod_pcts.keys()):
			print '{}/{}: {}'.format(prod_year_num, prod_year_count, lease_prod_year)
			well_id_count = len(well_prod_pcts[lease_prod_year].keys())
			well_id_num = 1
			for well_id in well_prod_pcts[lease_prod_year].keys():
				well_pct_data = well_prod_pcts[lease_prod_year][well_id]
				if debug: print '{} -- {} -- {}'.format(well_id, lease_prod_year,
				                                        well_prod_pcts[lease_prod_year][well_id])
				param_vals = (forecast_code,)
				param_vals += tuple([well_pct_data[prod_month] for prod_month in well_pct_data.keys()]) + (
					lease_id, well_id, lease_prod_year)
				if debug: print sql_update.format(*param_vals)
				curr.execute(sql_update.format(*param_vals))
				gd.commit(curr)
				well_id_num += 1
			prod_year_num += 1
		lease_prod_num += 1
	curr.close()
	conn.close()
	end_time = gd.get_datetime()
	print '({}) -- lease prod allocation end: {}'.format(forecast_code, end_time)
	print '({}) -- total allocation time: {}'.format(forecast_code, gd.elapsed_time(start_time, end_time))

# (1) -- total allocation time: 04:49:01
# (2) -- total allocation time: 04:41:10
# (3) -- total allocation time: 06:45:02
# (4) -- total allocation time: 05:32:10

def allocate_lease_oil_prod(curr, debug=False):
	forecast_code = gd.get_forecast_code()
	gd.incr_forecast_code()
	lease_prod_allocation(forecast_code, debug=debug)
	print 'Collecting data from tx_well_prod_pct_{} ...'.format(forecast_code)
	sql_update = \
		"""
	UPDATE tx_well_prod_pct
	  SET jan_prod_pct=b.jan_prod_pct,
		  feb_prod_pct=b.feb_prod_pct,
		  mar_prod_pct=b.mar_prod_pct,
		  apr_prod_pct=b.apr_prod_pct,
		  may_prod_pct=b.may_prod_pct,
		  jun_prod_pct=b.jun_prod_pct,
		  jul_prod_pct=b.jul_prod_pct,
		  aug_prod_pct=b.aug_prod_pct,
		  sep_prod_pct=b.sep_prod_pct,
		  oct_prod_pct=b.oct_prod_pct,
		  nov_prod_pct=b.nov_prod_pct,
		  dec_prod_pct=b.dec_prod_pct
	  FROM tx_well_prod_pct a,
		   tx_well_prod_pct_{} b
	  WHERE a.id=b.id;
	"""
	curr.execute(sql_update.format(forecast_code))
	gd.commit(curr)


def update_prod_pct_new(curr, debug=False):
	gd.reset_forecast_code()
	curr.execute('DROP TABLE IF EXISTS tx_well_prod_pct_new')
	gd.commit(curr)

	sql_update = \
	"""
	CREATE TABLE tx_well_prod_pct_new (
	  id               INT          IDENTITY,
	  lease_id         NVARCHAR(20) DEFAULT NULL,
	  tx_well_id       NVARCHAR(20) DEFAULT NULL,
	  prod_year        INT          DEFAULT NULL,
	  jan_prod_pct     FLOAT        DEFAULT NULL,
	  feb_prod_pct     FLOAT        DEFAULT NULL,
	  mar_prod_pct     FLOAT        DEFAULT NULL,
	  apr_prod_pct     FLOAT        DEFAULT NULL,
	  may_prod_pct     FLOAT        DEFAULT NULL,
	  jun_prod_pct     FLOAT        DEFAULT NULL,
	  jul_prod_pct     FLOAT        DEFAULT NULL,
	  aug_prod_pct     FLOAT        DEFAULT NULL,
	  sep_prod_pct     FLOAT        DEFAULT NULL,
	  oct_prod_pct     FLOAT        DEFAULT NULL,
	  nov_prod_pct     FLOAT        DEFAULT NULL,
	  dec_prod_pct     FLOAT        DEFAULT NULL,
	  process_code     TINYINT      DEFAULT NULL,
	  lease_well_count INT          DEFAULT NULL,
	  PRIMARY KEY (id));
	
	CREATE INDEX lease_id_indx ON tx_well_prod_pct_new (lease_id);
	CREATE INDEX prod_year_indx ON tx_well_prod_pct_new (prod_year);
	CREATE INDEX tx_well_id_prod_year_indx ON tx_well_prod_pct_new (tx_well_id, prod_year);
	CREATE INDEX tx_well_id_indx ON tx_well_prod_pct_new (tx_well_id);

	INSERT INTO tx_well_prod_pct_new (lease_id, tx_well_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code)
	  (SELECT DISTINCT lease_id, tx_well_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code
	   FROM tx_well_prod_pct);
	
	UPDATE tx_well_prod_pct_new SET lease_well_count=0;

	UPDATE tx_well_prod_pct_new SET lease_well_count=b.lease_well_count
	  FROM tx_well_prod_pct_new a,
		   (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count FROM tx_well_prod_pct_new GROUP BY lease_id, prod_year) b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year;
	
	UPDATE tx_well_prod_pct SET lease_well_count=b.lease_well_count
	  FROM tx_well_prod_pct a,
		   (SELECT DISTINCT lease_id, prod_year, COUNT(DISTINCT tx_well_id) AS lease_well_count FROM tx_well_prod_pct GROUP BY lease_id, prod_year) b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year;
	  
	UPDATE tx_well_prod_pct_new SET jan_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_jan_bbl,0)+ISNULL(csgd_jan_mcf,0)) > 0 AND a.lease_well_count=1 AND a.jan_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET feb_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_feb_bbl,0)+ISNULL(csgd_feb_mcf,0)) > 0 AND a.lease_well_count=1 AND a.feb_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET mar_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_mar_bbl,0)+ISNULL(csgd_mar_mcf,0)) > 0 AND a.lease_well_count=1 AND a.mar_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET apr_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_apr_bbl,0)+ISNULL(csgd_apr_mcf,0)) > 0 AND a.lease_well_count=1 AND a.apr_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET may_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_may_bbl,0)+ISNULL(csgd_may_mcf,0)) > 0 AND a.lease_well_count=1 AND a.may_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET jun_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_jun_bbl,0)+ISNULL(csgd_jun_mcf,0)) > 0 AND a.lease_well_count=1 AND a.jun_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET jul_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_jul_bbl,0)+ISNULL(csgd_jul_mcf,0)) > 0 AND a.lease_well_count=1 AND a.jul_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET aug_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_aug_bbl,0)+ISNULL(csgd_aug_mcf,0)) > 0 AND a.lease_well_count=1 AND a.aug_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET sep_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_sep_bbl,0)+ISNULL(csgd_sep_mcf,0)) > 0 AND a.lease_well_count=1 AND a.sep_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET oct_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_oct_bbl,0)+ISNULL(csgd_oct_mcf,0)) > 0 AND a.lease_well_count=1 AND a.oct_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET nov_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_nov_bbl,0)+ISNULL(csgd_nov_mcf,0)) > 0 AND a.lease_well_count=1 AND a.nov_prod_pct!=1;
	
	UPDATE tx_well_prod_pct_new SET dec_prod_pct=1
	  FROM tx_well_prod_pct_new a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND (ISNULL(b.oil_dec_bbl,0)+ISNULL(csgd_dec_mcf,0)) > 0 AND a.lease_well_count=1 AND a.dec_prod_pct!=1;
	"""
	curr.execute(sql_update)
	gd.commit(curr)


def create_final_pct_table(curr, debug=False):
	sql_update_1 = \
		"""
	TRUNCATE TABLE tx_well_prod_pct;
	TRUNCATE TABLE tx_well_prod_pct_1;
	TRUNCATE TABLE tx_well_prod_pct_2;
	
	INSERT INTO tx_well_prod_pct_2 (lease_id, tx_well_id, prod_year,jan_prod_pct,feb_prod_pct,mar_prod_pct,apr_prod_pct,may_prod_pct,jun_prod_pct,jul_prod_pct,aug_prod_pct,sep_prod_pct,oct_prod_pct,nov_prod_pct,dec_prod_pct,process_code)
	  (SELECT DISTINCT lease_id, tx_well_id, prod_year, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 FROM tx_well_prod_pct_new);
	
	INSERT INTO tx_well_prod_pct_2 (lease_id, tx_well_id, prod_year,jan_prod_pct,feb_prod_pct,mar_prod_pct,apr_prod_pct,may_prod_pct,jun_prod_pct,jul_prod_pct,aug_prod_pct,sep_prod_pct,oct_prod_pct,nov_prod_pct,dec_prod_pct,process_code)
	  (SELECT DISTINCT lease_id, tx_well_id, prod_year, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 FROM tx_well_allow_pct);
	
	INSERT INTO tx_well_prod_pct (lease_id, tx_well_id, prod_year,jan_prod_pct,feb_prod_pct,mar_prod_pct,apr_prod_pct,may_prod_pct,jun_prod_pct,jul_prod_pct,aug_prod_pct,sep_prod_pct,oct_prod_pct,nov_prod_pct,dec_prod_pct,process_code)
	  (SELECT DISTINCT lease_id, tx_well_id, prod_year, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 FROM tx_well_prod_pct_2);
	
	UPDATE tx_well_prod_pct 
	  SET process_code=0 
	  FROM tx_well_prod_pct a, tx_well_prod_pct_new b
	  WHERE a.lease_id=b.lease_id AND a.tx_well_id=b.tx_well_id AND a.prod_year=b.prod_year;
	
	UPDATE tx_well_prod_pct 
	  SET process_code=2 
	  FROM tx_well_prod_pct a, tx_well_allow_pct b
	  WHERE a.lease_id=b.lease_id AND a.tx_well_id=b.tx_well_id AND a.prod_year=b.prod_year AND a.process_code=0;
	
	UPDATE tx_well_prod_pct
	  SET jan_prod_pct=b.jan_prod_pct,
		  feb_prod_pct=b.feb_prod_pct,
		  mar_prod_pct=b.mar_prod_pct,
		  apr_prod_pct=b.apr_prod_pct,
		  may_prod_pct=b.may_prod_pct,
		  jun_prod_pct=b.jun_prod_pct,
		  jul_prod_pct=b.jul_prod_pct,
		  aug_prod_pct=b.aug_prod_pct,
		  sep_prod_pct=b.sep_prod_pct,
		  oct_prod_pct=b.oct_prod_pct,
		  nov_prod_pct=b.nov_prod_pct,
		  dec_prod_pct=b.dec_prod_pct
	  FROM tx_well_prod_pct a, tx_well_prod_pct_new b
	  WHERE a.lease_id=b.lease_id AND a.tx_well_id=b.tx_well_id AND a.prod_year=b.prod_year AND a.process_code=0;
	
	UPDATE tx_well_prod_pct
	  SET jan_prod_pct=b.oil_jan_bbl,
		  feb_prod_pct=b.oil_feb_bbl,
		  mar_prod_pct=b.oil_mar_bbl,
		  apr_prod_pct=b.oil_apr_bbl,
		  may_prod_pct=b.oil_may_bbl,
		  jun_prod_pct=b.oil_jun_bbl,
		  jul_prod_pct=b.oil_jul_bbl,
		  aug_prod_pct=b.oil_aug_bbl,
		  sep_prod_pct=b.oil_sep_bbl,
		  oct_prod_pct=b.oil_oct_bbl,
		  nov_prod_pct=b.oil_nov_bbl,
		  
		  dec_prod_pct=b.oil_dec_bbl
	  FROM tx_well_prod_pct a, tx_well_allow_pct b
	  WHERE a.lease_id=b.lease_id AND a.tx_well_id=b.tx_well_id AND a.prod_year=b.prod_year AND a.process_code=1;
	
	UPDATE tx_well_prod_pct
	  SET jan_prod_pct=(b.oil_jan_bbl+c.jan_prod_pct),
		  feb_prod_pct=(b.oil_feb_bbl+c.feb_prod_pct),
		  mar_prod_pct=(b.oil_mar_bbl+c.mar_prod_pct),
		  apr_prod_pct=(b.oil_apr_bbl+c.apr_prod_pct),
		  may_prod_pct=(b.oil_may_bbl+c.may_prod_pct),
		  jun_prod_pct=(b.oil_jun_bbl+c.jun_prod_pct),
		  jul_prod_pct=(b.oil_jul_bbl+c.jul_prod_pct),
		  aug_prod_pct=(b.oil_aug_bbl+c.aug_prod_pct),
		  sep_prod_pct=(b.oil_sep_bbl+c.sep_prod_pct),
		  oct_prod_pct=(b.oil_oct_bbl+c.oct_prod_pct),
		  nov_prod_pct=(b.oil_nov_bbl+c.nov_prod_pct),
		  dec_prod_pct=(b.oil_dec_bbl+c.dec_prod_pct)
	  FROM tx_well_prod_pct a, tx_well_allow_pct b, tx_well_prod_pct_new c
	  WHERE a.lease_id=b.lease_id
		AND a.tx_well_id=b.tx_well_id
		AND a.prod_year=b.prod_year
		AND a.lease_id=c.lease_id
		AND a.tx_well_id=c.tx_well_id
		AND a.prod_year=c.prod_year
		AND a.process_code=2;
	
	UPDATE tx_well_prod_pct
	  SET jan_prod_pct=IIF(b.total_jan_prod_pct=0, 0 ,a.jan_prod_pct/b.total_jan_prod_pct),
		  feb_prod_pct=IIF(b.total_feb_prod_pct=0, 0 ,a.feb_prod_pct/b.total_feb_prod_pct),
		  mar_prod_pct=IIF(b.total_mar_prod_pct=0, 0 ,a.mar_prod_pct/b.total_mar_prod_pct),
		  apr_prod_pct=IIF(b.total_apr_prod_pct=0, 0 ,a.apr_prod_pct/b.total_apr_prod_pct),
		  may_prod_pct=IIF(b.total_may_prod_pct=0, 0 ,a.may_prod_pct/b.total_may_prod_pct),
		  jun_prod_pct=IIF(b.total_jun_prod_pct=0, 0 ,a.jun_prod_pct/b.total_jun_prod_pct),
		  jul_prod_pct=IIF(b.total_jul_prod_pct=0, 0 ,a.jul_prod_pct/b.total_jul_prod_pct),
		  aug_prod_pct=IIF(b.total_aug_prod_pct=0, 0 ,a.aug_prod_pct/b.total_aug_prod_pct),
		  sep_prod_pct=IIF(b.total_sep_prod_pct=0, 0 ,a.sep_prod_pct/b.total_sep_prod_pct),
		  oct_prod_pct=IIF(b.total_oct_prod_pct=0, 0 ,a.oct_prod_pct/b.total_oct_prod_pct),
		  nov_prod_pct=IIF(b.total_nov_prod_pct=0, 0 ,a.nov_prod_pct/b.total_nov_prod_pct),
		  dec_prod_pct=IIF(b.total_dec_prod_pct=0, 0 ,a.dec_prod_pct/b.total_dec_prod_pct)
	  FROM tx_well_prod_pct a,
		   (SELECT DISTINCT lease_id, prod_year,
			 SUM(jan_prod_pct) AS total_jan_prod_pct,
			 SUM(feb_prod_pct) AS total_feb_prod_pct,
			 SUM(mar_prod_pct) AS total_mar_prod_pct,
			 SUM(apr_prod_pct) AS total_apr_prod_pct,
			 SUM(may_prod_pct) AS total_may_prod_pct,
			 SUM(jun_prod_pct) AS total_jun_prod_pct,
			 SUM(jul_prod_pct) AS total_jul_prod_pct,
			 SUM(aug_prod_pct) AS total_aug_prod_pct,
			 SUM(sep_prod_pct) AS total_sep_prod_pct,
			 SUM(oct_prod_pct) AS total_oct_prod_pct,
			 SUM(nov_prod_pct) AS total_nov_prod_pct,
			 SUM(dec_prod_pct) AS total_dec_prod_pct
			 FROM tx_well_prod_pct GROUP BY lease_id, prod_year) b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year;
	"""
	sql_update_2 = \
		"""
	UPDATE tx_well_prod_pct SET process_code=0
		WHERE (ISNULL(jan_prod_pct,0)+ISNULL(feb_prod_pct,0)+ISNULL(mar_prod_pct,0)+ISNULL(apr_prod_pct,0)+ISNULL(may_prod_pct,0)+ISNULL(jun_prod_pct,0)+ISNULL(jul_prod_pct,0)+ISNULL(aug_prod_pct,0)+ISNULL(sep_prod_pct,0)+ISNULL(oct_prod_pct,0)+ISNULL(nov_prod_pct,0)+ISNULL(dec_prod_pct,0)) > 0;

	UPDATE tx_lease_prod_schedule SET process_code=0 FROM tx_lease_prod_schedule a, tx_well_prod_pct b WHERE a.lease_id=b.lease_id AND b.process_code=0;
	UPDATE tx_oil_prod_schedule_2 SET process_code=0 FROM tx_oil_prod_schedule_2 a, tx_well_prod_pct b WHERE a.lease_id=b.lease_id AND b.process_code=0;
	"""

	curr.execute(sql_update_1)
	gd.commit(curr)


# curr.execute(sql_update_2)
# gd.commit(curr)


def update_lease_prod_pct(curr, debug=False):
	sql_update = \
		"""
	DROP TABLE IF EXISTS tx_lease_prod_pct;
	CREATE TABLE tx_lease_prod_pct (
	  id           INT          IDENTITY,
	  lease_id     NVARCHAR(20) DEFAULT NULL,
	  prod_year    INT          DEFAULT NULL,
	  jan_prod_pct FLOAT        DEFAULT NULL,
	  feb_prod_pct FLOAT        DEFAULT NULL,
	  mar_prod_pct FLOAT        DEFAULT NULL,
	  apr_prod_pct FLOAT        DEFAULT NULL,
	  may_prod_pct FLOAT        DEFAULT NULL,
	  jun_prod_pct FLOAT        DEFAULT NULL,
	  jul_prod_pct FLOAT        DEFAULT NULL,
	  aug_prod_pct FLOAT        DEFAULT NULL,
	  sep_prod_pct FLOAT        DEFAULT NULL,
	  oct_prod_pct FLOAT        DEFAULT NULL,
	  nov_prod_pct FLOAT        DEFAULT NULL,
	  dec_prod_pct FLOAT        DEFAULT NULL,
	  process_code TINYINT      DEFAULT NULL,
	  PRIMARY KEY (id));
	
	CREATE INDEX lease_id_indx ON tx_lease_prod_pct (lease_id);
	
	CREATE INDEX prod_year_indx ON tx_lease_prod_pct (prod_year);
	
	CREATE INDEX lease_id_prod_year_indx ON tx_lease_prod_pct (lease_id, prod_year);
	
	CREATE INDEX process_code_indx ON tx_lease_prod_pct (process_code);

	INSERT INTO tx_lease_prod_pct (lease_id, prod_year, jan_prod_pct, feb_prod_pct, mar_prod_pct, apr_prod_pct, may_prod_pct, jun_prod_pct, jul_prod_pct, aug_prod_pct, sep_prod_pct, oct_prod_pct, nov_prod_pct, dec_prod_pct, process_code)
	  (SELECT DISTINCT lease_id, prod_year,
		  ROUND(SUM(jan_prod_pct),2) AS total_jan_prod_pct,
		  ROUND(SUM(feb_prod_pct),2) AS total_feb_prod_pct,
		  ROUND(SUM(mar_prod_pct),2) AS total_mar_prod_pct,
		  ROUND(SUM(apr_prod_pct),2) AS total_apr_prod_pct,
		  ROUND(SUM(may_prod_pct),2) AS total_may_prod_pct,
		  ROUND(SUM(jun_prod_pct),2) AS total_jun_prod_pct,
		  ROUND(SUM(jul_prod_pct),2) AS total_jul_prod_pct,
		  ROUND(SUM(aug_prod_pct),2) AS total_aug_prod_pct,
		  ROUND(SUM(sep_prod_pct),2) AS total_sep_prod_pct,
		  ROUND(SUM(oct_prod_pct),2) AS total_oct_prod_pct,
		  ROUND(SUM(nov_prod_pct),2) AS total_nov_prod_pct,
		  ROUND(SUM(dec_prod_pct),2) AS total_dec_prod_pct,
		  0
		FROM tx_well_prod_pct
		GROUP BY lease_id, prod_year);
	"""
	curr.execute(sql_update)
	gd.commit(curr)


def update_pct_gaps(curr, debug=False):
	start_time = gd.get_datetime()
	sql_update_1 = \
		"""
	UPDATE tx_lease_prod_pct SET {0}_prod_pct=2 FROM tx_lease_prod_pct a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year AND a.{0}_prod_pct=0 AND (b.oil_{0}_bbl+b.csgd_{0}_mcf) > 0;
	"""
	sql_update_2 = \
		"""
	UPDATE tx_well_prod_pct
	  SET {0}_prod_pct=1.0/a.lease_well_count
	  FROM tx_well_prod_pct a, (SELECT DISTINCT lease_id, prod_year FROM tx_lease_prod_pct WHERE {0}_prod_pct=2) b
	  WHERE a.lease_id=b.lease_id
	  AND a.prod_year=b.prod_year
	"""
	for month_name in MONTHS:
		print '\nUpdating tx_lease_prod_pct for {}...'.format(month_name)
		curr.execute(sql_update_1.format(month_name))
		gd.commit(curr)

		curr.execute(sql_update_2.format(month_name))
		gd.commit(curr)


def update_hist_oil_production(curr, debug=False):
	sql_update = \
	"""
	DROP TABLE IF EXISTS tx_hist_oil_production;
	
	CREATE TABLE tx_hist_oil_production (
	  id            INT IDENTITY,
	  well_id       INT,
	  tx_well_id    VARCHAR(20),
	  lease_id      VARCHAR(20),
	  prod_year     INT,
	  oil_total_bbl FLOAT,
	  gas_total_mcf FLOAT,
	  oil_jan_bbl   FLOAT,
	  oil_feb_bbl   FLOAT,
	  oil_mar_bbl   FLOAT,
	  oil_apr_bbl   FLOAT,
	  oil_may_bbl   FLOAT,
	  oil_jun_bbl   FLOAT,
	  oil_jul_bbl   FLOAT,
	  oil_aug_bbl   FLOAT,
	  oil_sep_bbl   FLOAT,
	  oil_oct_bbl   FLOAT,
	  oil_nov_bbl   FLOAT,
	  oil_dec_bbl   FLOAT,
	  gas_jan_mcf   FLOAT,
	  gas_feb_mcf   FLOAT,
	  gas_mar_mcf   FLOAT,
	  gas_apr_mcf   FLOAT,
	  gas_may_mcf   FLOAT,
	  gas_jun_mcf   FLOAT,
	  gas_jul_mcf   FLOAT,
	  gas_aug_mcf   FLOAT,
	  gas_sep_mcf   FLOAT,
	  gas_oct_mcf   FLOAT,
	  gas_nov_mcf   FLOAT,
	  gas_dec_mcf   FLOAT,
	  sources       VARCHAR(20),
	  process_code  INT,
	  PRIMARY KEY (id));
	  
	CREATE INDEX well_id_prod_year_indx ON tx_hist_oil_production (well_id, prod_year);
	CREATE INDEX well_id_source_indx ON tx_hist_oil_production (well_id, process_code);
	CREATE INDEX well_id_indx ON tx_hist_oil_production (well_id);
	CREATE INDEX tx_well_id_prod_year_indx ON tx_hist_oil_production (tx_well_id, prod_year);
	CREATE INDEX tx_well_id_process_code_indx ON tx_hist_oil_production (tx_well_id, process_code);
	CREATE INDEX tx_well_id_indx ON tx_hist_oil_production (tx_well_id);
	CREATE INDEX lease_id_indx ON tx_hist_oil_production (lease_id);
	CREATE INDEX lease_id_prod_year_indx ON tx_hist_oil_production (lease_id, prod_year);
	CREATE INDEX lease_id_process_code_indx ON tx_hist_oil_production (lease_id, process_code);
	CREATE INDEX prod_year_indx ON tx_hist_oil_production (prod_year);
	CREATE INDEX process_code_indx ON tx_hist_oil_production (process_code);

	INSERT INTO tx_hist_oil_production (lease_id,tx_well_id,prod_year,oil_jan_bbl,oil_feb_bbl,oil_mar_bbl,oil_apr_bbl,oil_may_bbl,oil_jun_bbl,oil_jul_bbl,oil_aug_bbl,oil_sep_bbl,oil_oct_bbl,oil_nov_bbl,oil_dec_bbl,gas_jan_mcf,gas_feb_mcf,gas_mar_mcf,gas_apr_mcf,gas_may_mcf,gas_jun_mcf,gas_jul_mcf,gas_aug_mcf,gas_sep_mcf,gas_oct_mcf,gas_nov_mcf,gas_dec_mcf,process_code)
	  (SELECT DISTINCT lease_id,tx_well_id,prod_year,jan_prod_pct,feb_prod_pct,mar_prod_pct,apr_prod_pct,may_prod_pct,jun_prod_pct,jul_prod_pct,aug_prod_pct,sep_prod_pct,oct_prod_pct,nov_prod_pct,dec_prod_pct,jan_prod_pct,feb_prod_pct,mar_prod_pct,apr_prod_pct,may_prod_pct,jun_prod_pct,jul_prod_pct,aug_prod_pct,sep_prod_pct,oct_prod_pct,nov_prod_pct,dec_prod_pct,1
	    FROM tx_well_prod_pct);
	
	UPDATE tx_hist_oil_production
	  SET oil_jan_bbl=a.oil_jan_bbl*b.oil_jan_bbl,
	      oil_feb_bbl=a.oil_feb_bbl*b.oil_feb_bbl,
	      oil_mar_bbl=a.oil_mar_bbl*b.oil_mar_bbl,
	      oil_apr_bbl=a.oil_apr_bbl*b.oil_apr_bbl,
	      oil_may_bbl=a.oil_may_bbl*b.oil_may_bbl,
	      oil_jun_bbl=a.oil_jun_bbl*b.oil_jun_bbl,
	      oil_jul_bbl=a.oil_jul_bbl*b.oil_jul_bbl,
	      oil_aug_bbl=a.oil_aug_bbl*b.oil_aug_bbl,
	      oil_sep_bbl=a.oil_sep_bbl*b.oil_sep_bbl,
	      oil_oct_bbl=a.oil_oct_bbl*b.oil_oct_bbl,
	      oil_nov_bbl=a.oil_nov_bbl*b.oil_nov_bbl,
	      oil_dec_bbl=a.oil_dec_bbl*b.oil_dec_bbl,
	      gas_jan_mcf=a.gas_jan_mcf*b.csgd_jan_mcf,
	      gas_feb_mcf=a.gas_feb_mcf*b.csgd_feb_mcf,
	      gas_mar_mcf=a.gas_mar_mcf*b.csgd_mar_mcf,
	      gas_apr_mcf=a.gas_apr_mcf*b.csgd_apr_mcf,
	      gas_may_mcf=a.gas_may_mcf*b.csgd_may_mcf,
	      gas_jun_mcf=a.gas_jun_mcf*b.csgd_jun_mcf,
	      gas_jul_mcf=a.gas_jul_mcf*b.csgd_jul_mcf,
	      gas_aug_mcf=a.gas_aug_mcf*b.csgd_aug_mcf,
	      gas_sep_mcf=a.gas_sep_mcf*b.csgd_sep_mcf,
	      gas_oct_mcf=a.gas_oct_mcf*b.csgd_oct_mcf,
	      gas_nov_mcf=a.gas_nov_mcf*b.csgd_nov_mcf,
	      gas_dec_mcf=a.gas_dec_mcf*b.csgd_dec_mcf
	  FROM tx_hist_oil_production a, tx_production b
	  WHERE a.lease_id=b.lease_id AND a.prod_year=b.prod_year;
	
	UPDATE tx_hist_oil_production
	  SET oil_total_bbl=(ISNULL(oil_jan_bbl,0) + ISNULL(oil_feb_bbl,0) + ISNULL(oil_mar_bbl,0) + ISNULL(oil_apr_bbl,0) + ISNULL(oil_may_bbl,0) + ISNULL(oil_jun_bbl,0) + ISNULL(oil_jul_bbl,0) + ISNULL(oil_aug_bbl,0) + ISNULL(oil_sep_bbl,0) + ISNULL(oil_oct_bbl,0) + ISNULL(oil_nov_bbl,0) + ISNULL(oil_dec_bbl,0)),
	      gas_total_mcf=(ISNULL(gas_jan_mcf,0) + ISNULL(gas_feb_mcf,0) + ISNULL(gas_mar_mcf,0) + ISNULL(gas_apr_mcf,0) + ISNULL(gas_may_mcf,0) + ISNULL(gas_jun_mcf,0) + ISNULL(gas_jul_mcf,0) + ISNULL(gas_aug_mcf,0) + ISNULL(gas_sep_mcf,0) + ISNULL(gas_oct_mcf,0) + ISNULL(gas_nov_mcf,0) + ISNULL(gas_dec_mcf,0));

	"""
	curr.execute(sql_update)
	gd.commit(curr)


def tx_oil_allocation_update(update_oil_prod=False,
                             update_oil_field=False,
                             update_gaps=False,
                             update_lease_2=False,
                             create_allow=False,
                             lease_to_well=False,
                             update_allow=False,
                             update_oil_2=False,
                             calc_lease=False,
                             create_lease=False,
                             update_prev=False,
                             update_lease=False,
                             update_well_dates=False,
                             update_prod_pct=False,
                             split_well_pct=False,
                             update_pct_main=False,
                             allocate=False,
                             update_pct_new=False,
                             create_pct_final=False,
                             update_lease_pct=False,
                             update_prod_pct_gaps=False,
                             update_hist_prod=False,
                             debug=False):
	conn = gd.get_connection(server='sql_server', database='US_Wells_Texas', us_wells=True)
	curr = conn.cursor()
	if update_oil_prod:
		print '1: Updating US_Wells_Texas.dbo.tx_oil_production_data table ...'
		update_oil_production_data(curr, debug=debug)

	if update_oil_field:
		print '2: Updating US_Wells_Texas.dbo.tx_oil_field_schedule_lite_2 table ...'
		update_oil_field_sched_lite(curr, debug=debug)

	if update_gaps:
		print '3: Updating data gaps in US_Wells_Texas.dbo.tx_oil_field_schedule_lite_2 table ...'
		update_data_gaps(curr, debug=debug)

	if update_lease_2:
		print '4: Updating US_Wells_Texas.dbo.tx_lease_prod_schedule_2 table ...'
		update_lease_prod_sched_2(curr, debug=debug)

	if create_allow:
		print '5: ...'
		create_well_allow_pct(curr, debug=debug)

	if lease_to_well:
		print '6: ...'
		tx_lease_to_well_prod(curr, debug=debug)

	if update_allow:
		print '7: ...'
		update_well_allow_pct(curr, debug=debug)

	if update_oil_2:
		print '8: Updating US_Wells_Texas.dbo.tx_oil_prod_schedule_2 table ...'
		update_oil_prod_sched_2(curr, debug=debug)

	if calc_lease:
		print '9: Calculating lease_oil_prod ...'
		calc_lease_period_prod(curr, debug=debug)

	if create_lease:
		print '10: Creating US_Wells_Texas.dbo.tx_lease_prod_schedule table ...'
		create_lease_prod_sched(curr, debug=debug)

	if update_prev:
		print '10.5 Updating previous oil production in US_Wells_Texas.dbo.tx_lease_prod_schedule table ...'
		update_prev_prod(curr, debug=debug)

	if update_lease:
		print '11: Updating US_Wells_Texas.dbo.tx_lease_prod_schedule table ...'
		update_lease_prod_sched(curr, debug=debug)

	if update_well_dates:
		print '12: Updating US_Wells_Texas.dbo.tx_well_prod_dates table ...'
		update_oil_well_prod_dates(curr, debug=debug)

	if update_prod_pct:
		print '13: Updating US_Wells_Texas.dbo.tx_well_prod_pct table ...'
		update_prod_pct_table(curr, debug=debug)

	if split_well_pct:
		print '14: Splitting tx_well_prod_pct table ...'
		update_well_prod_pct_split(curr, debug=debug)

	if update_pct_main:
		print '15: Updating all tx_well_prod_pct tables ...'
		update_prod_pct_main(curr, debug=debug)

	if allocate:
		print '16: Allocating lease oil production to wells ({}) ...'.format(gd.get_forecast_code())
		allocate_lease_oil_prod(curr, debug=debug)

	if update_pct_new:
		print '17: ...'
		update_prod_pct_new(curr, debug=debug)

	if create_pct_final:
		print '18: ...'
		create_final_pct_table(curr, debug=debug)

	if update_lease_pct:
		print '19: Updating US_Wells_Texas.dbo.tx_lease_prod_pct table ...'
		update_lease_prod_pct(curr, debug=debug)

	if update_prod_pct_gaps:
		print '20: Updating data gaps in US_Wells_Texas.dbo.tx_well_prod_pct table ...'
		update_pct_gaps(curr, debug=debug)
	
	if update_hist_prod:
		print '22: Updating historical oil production table ...'
		update_hist_oil_production(curr, debug=debug)
		
	curr.close()
	conn.close()


# Completion Data -----------------------------------------------------------------------------------------------------------------------------

def unzip_files(zipfile_dir, unzip_dir):
	for zipfile in os.listdir(zipfile_dir):
		with ZipFile(zipfile_dir + zipfile) as zf:
			zf.extractall(unzip_dir + zipfile[:-4])


def store_data_records(comp_dir=COMP_OUT_DIR, debug=False):
	sql_insert = "INSERT INTO dbo.texas_comp_data_records (tracking_no, header_data, record_code, comp_record, process_code, source_file) VALUES ({}, '{}', '{}', '{}', 0, '{}')"
	sql_update = "UPDATE dbo.texas_comp_data_records SET comp_record=CONCAT(comp_record,' ','{}') WHERE id={} AND process_code=0"
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	sql_update_2 = \
		'''
	UPDATE US_Wells_Texas.dbo.texas_comp_data_records SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_casing_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_formation_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_g10_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_g1_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_g1_field_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_g5_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_gas_measurement_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_l1_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_liner_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_material_used_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_multiple_completion_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_p15_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_p4_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_p4_gas_gatherer_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_p4_oil_gatherer_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_packet_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_production_interval_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_reclass_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_tubing_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_w12_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.texas_comp_w2_data SET process_code=1;
	UPDATE US_Wells_Texas.dbo.tx_completion_data SET process_code=1;
	'''
	curr.execute(sql_update_2)
	gd.commit(curr)
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
								dataline = gd.encode_str(dataline)
								dataline = dataline.replace(',', '')
								dataline = dataline.replace("'", "")
								dataline = dataline.replace('\n', ' ')
								dataline = dataline.replace('\\', ' ')
								if debug: print 'dataline: {}'.format(dataline)
								record_code = None
								if len(dataline) > 1:
									data_vals = dataline.split('{')
									if data_vals[0] in COMP_REC_CODE.keys():
										record_code = data_vals[0]
										comp_rec = (
											tracking_number, header_data[:250].replace('\n', ' '), record_code,
											dataline,
											packet_dir + packet_filename)
										if debug:
											print 1, sql_insert
											for rec in comp_rec:
												print rec
										if debug:
											print 1, dataline, sql_insert.format(*comp_rec)
										curr.execute(sql_insert.format(*comp_rec))
										gd.commit(curr)
									elif str(tracking_number) != str(data_vals[0])[:6]:
										try:
											max_id = gd.get_data('MAX(id)', 'dbo.texas_comp_data_records',
											                     database='US_Wells_Texas', server='sql_server',
											                     datatype='int')[0]
										except:
											max_id = 1
										if debug: print 2, dataline, sql_update.format(dataline[:-1], max_id)
										curr.execute(sql_update.format(dataline[:-1], max_id))
										gd.commit(curr)
									else:
										comp_rec = (tracking_number, header_data[:250], record_code, dataline[:-1],
										            packet_dir + packet_filename)
										if debug: print 3, dataline, sql_insert.format(*comp_rec)
										curr.execute(sql_insert.format(*comp_rec))
										gd.commit(curr)
	curr.close()
	conn.close()


def parse_comp_data(debug=False):
	sql_insert_temp = 'INSERT INTO {} ({}) VALUES ({})'
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	sql_update_2 = \
		"""
	UPDATE texas_comp_data_records SET record_code=REPLACE(REPLACE(REPLACE(record_code,',',''),'"',''),'''','');
	"""
	curr.execute(sql_update_2)
	gd.commit(curr)
	for record_code in COMP_REC_CODE.keys():
		data_table = COMP_REC_CODE[record_code]
		comp_data = gd.get_data('comp_record', 'dbo.texas_comp_data_records',
		                        sql_where="record_code='{}' AND process_code=0".format(record_code),
		                        database='US_Wells_Texas', server='sql_server', datatype='str')
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
				if debug:
					try:
						print 11, sql_insert % param_vals
					except:
						print 12, sql_insert, param_vals
				curr.execute(sql_insert, param_vals)
				gd.commit(curr)
			except:
				if debug:
					try:
						print 21, sql_insert.format(*param_vals)
					except:
						print 22, sql_insert, param_vals
				print 'error'
			row_num += 1

	curr.close()
	conn.close()


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
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	if unzip_data:
		print 'Extracting completion data from compressed files ...'
		unzip_files(zipfile_dir=COMP_ZIP_DIR, unzip_dir=COMP_OUT_DIR)
	if store_records:
		print 'Storing completion data records in US_Wells_Texas.dbo.texas_comp_data_records ...'
		store_data_records(debug=debug)
	if parse_data:
		print 'Parsing completion data records into completion data tables ...'
		parse_comp_data(debug=debug)
	if update_tables:
		print 'Updating completion data tables ...'
		update_completion_tables(curr=curr)
	curr.close()
	conn.close()


# Well Details --------------------------------------------------------------------------------------------------------------------------------

# Update tx_well_id in tx_permit_data, tx_wellbore_data_lite, tx_completion_data, tx_well_data_master, tx_oil_field_schedule
# Identify wells without tx_well_ids in those tables and add to tx_ref_well_id with desginated process_code
# Use all tables to fill in data missing in tx_ref_well_id
# Generate tx_well_id in tx_ref_well_id for new wells
# Update tx_well_id in tx_permit_data, tx_wellbore_data_lite, tx_completion_data, tx_well_data_master, tx_oil_field_schedule
# Update tx_well_details with new wells
# Use all tables to fill in data missing in tx_well_details

def update_well_data_tables():
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	print 'Updating well data tables ...'
	sql_update = \
		"""
	UPDATE tx_well_data_master SET process_code=0;
	
	UPDATE tx_well_data_master SET process_code=1
	  FROM tx_well_data_master a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.oil_gas_code=b.oil_gas_code AND a.lease_no=b.lease_no AND a.county_no=b.county_no;
	
	UPDATE tx_well_data_master SET process_code=2 WHERE process_code=0 AND lease_no IS NOT NULL;
	
	UPDATE tx_well_data_master SET district_no=b.district_code
	  FROM tx_well_data_master a, tx_wellbore_data_lite b
	  WHERE a.api_number=b.api_number AND a.county_no=b.county_code AND a.lease_no=b.lease_no AND a.oil_gas_code=b.oil_gas_code AND a.well_no=b.well_no;
	
	UPDATE tx_well_data_master SET district_no=b.district_code
	  FROM tx_well_data_master a, tx_wellbore_data_lite b
	  WHERE a.api_number=b.api_number AND a.county_no=b.county_code AND a.well_no=b.well_no AND a.district_no IS NULL;
	
	UPDATE tx_well_data_master SET district_no=b.district_no
	  FROM tx_well_data_master a, tx_production b
	  WHERE a.lease_no=b.lease_no AND a.county_no=b.county_no AND a.well_no=b.well_no AND a.district_no IS NULL;
	
	UPDATE tx_well_data_master SET tx_well_id=b.tx_well_id
	  FROM tx_well_data_master a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.oil_gas_code=b.oil_gas_code AND a.well_no=b.well_no AND a.lease_no=b.lease_no;
	
	
	
	UPDATE tx_wellbore_data_lite SET tx_well_id=b.tx_well_id
	  FROM tx_wellbore_data_lite a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.well_no=b.well_no AND a.oil_gas_code=b.oil_gas_code AND a.tx_well_id IS NULL;
	
	
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_well_data_master b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.district_no=b.district_no AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_well_data_master b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_well_data_master b
	  WHERE a.drill_permit_no=b.drill_permit_no AND a.api_number=b.api_number AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_number, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_wellbore_data_update b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.district_no=b.district_code AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_number, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_wellbore_data_update b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_wellbore_data_lite b
	  WHERE a.drill_permit_no=b.recent_permit AND a.api_number=b.api_number AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_wellbore_data_lite b
	  WHERE a.drill_permit_no=b.recent_permit AND a.api_number=b.api_number AND a.lease_no IS NULL AND b.lease_no IS NOT NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_wellbore_data_lite b
	  WHERE a.well_no=b.well_no AND a.api_number=b.api_number AND a.lease_no IS NULL AND b.lease_no IS NOT NULL;
	
	UPDATE tx_permit_data SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data
	  SET lease_no=b.lease_no
	  FROM tx_permit_data AS a, tx_well_data_master AS b
	  WHERE a.drill_permit_no=b.permit_no AND a.lease_name_str=b.lease_name_str AND a.api_number=b.api_number AND a.lease_no IS NULL;
	
	UPDATE tx_permit_data
	  SET lease_no=b.lease_no
	  FROM tx_permit_data AS a, tx_well_data_master AS b
	  WHERE a.lease_name_str=b.lease_name_str AND a.api_number=b.api_number AND a.lease_no IS NULL AND NOT b.lease_no IS NULL;
	
	UPDATE tx_permit_data
	  SET lease_no=b.lease_no, oil_gas_code=b.oil_gas_code
	  FROM tx_permit_data AS a, tx_well_data_master AS b
	  WHERE a.well_no=b.well_no AND a.drill_permit_no=b.permit_no AND a.api_number=b.api_number AND a.lease_no IS NULL AND NOT b.lease_no IS NULL;
	
	UPDATE tx_permit_data SET lease_no=NULL WHERE lease_no='000000';
	
	UPDATE tx_permit_data
	  SET tx_well_id=b.tx_well_id
	  FROM tx_permit_data AS a, tx_ref_well_id AS b
	  WHERE a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.well_no=b.well_no AND a.tx_well_id IS NULL;
	
	UPDATE tx_permit_data
	  SET lease_no=b.lease_no, tx_well_id=b.tx_well_id
	  FROM tx_permit_data AS a, tx_completion_data AS b
	  WHERE a.drill_permit_no=b.dp_no AND a.api_number=b.api_no AND a.lease_no IS NULL AND a.well_no=b.well_no AND b.lease_no IS NOT NULL AND a.tx_well_id IS NULL;
	
	
	
	UPDATE tx_oil_field_schedule
	  SET tx_well_id=b.tx_well_id
	  FROM tx_oil_field_schedule a, tx_ref_well_id b
	  WHERE a.lease_no=b.lease_no AND a.api_number=b.api_number AND a.well_no=b.well_no AND a.district_no=b.district_no AND b.oil_gas_code='O' AND a.field_no=b.field_no AND a.operator_no=b.operator_no AND a.process_code=0;
	
	UPDATE tx_oil_field_schedule
	  SET tx_well_id=b.tx_well_id
	  FROM tx_oil_field_schedule a, tx_ref_well_id b
	  WHERE a.lease_no=b.lease_no AND a.api_number=b.api_number AND a.well_no=b.well_no  AND a.district_no=b.district_no AND b.oil_gas_code='O' AND a.field_no=b.field_no AND a.tx_well_id IS NULL AND a.process_code=0;
	
	UPDATE tx_oil_field_schedule
	  SET tx_well_id=b.tx_well_id
	  FROM tx_oil_field_schedule a, tx_ref_well_id b
	  WHERE a.lease_no=b.lease_no AND a.api_number=b.api_number AND a.well_no=b.well_no  AND a.district_no=b.district_no AND b.oil_gas_code='O' AND a.tx_well_id IS NULL AND a.process_code=0;
	
	UPDATE tx_oil_field_schedule
	  SET tx_well_id=b.tx_well_id
	  FROM tx_oil_field_schedule a, tx_ref_well_id b
	  WHERE a.lease_no=b.lease_no AND a.well_no=b.well_no  AND a.district_no=b.district_no AND b.oil_gas_code='O' AND a.tx_well_id IS NULL AND a.process_code=0;
	
	UPDATE tx_oil_field_schedule
	  SET tx_well_id=c.tx_well_id
	  FROM tx_oil_field_schedule a,
		  (SELECT DISTINCT api_number, district_no, field_no, COUNT(*) AS well_count FROM tx_well_details GROUP BY api_number, district_no, field_no) b,
		   tx_ref_well_id c
	  WHERE a.api_number=b.api_number AND a.api_number=c.api_number AND a.district_no=b.district_no AND a.district_no=c.district_no AND a.field_no=b.field_no AND a.field_no=c.field_no AND b.well_count=1 AND a.tx_well_id IS NULL AND c.oil_gas_code='O' AND a.process_code=0;
	
	UPDATE tx_oil_field_schedule
	  SET tx_well_id=b.tx_well_id
	  FROM tx_oil_field_schedule a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.tx_well_id IS NULL AND b.tx_well_id IS NOT NULL AND a.lease_no=b.lease_no AND b.oil_gas_code='O';
	
	
	
	UPDATE tx_well_production
	  SET tx_well_id=b.tx_well_id, api_number=b.api_number
	  FROM tx_well_production a, tx_ref_well_id b
	  WHERE a.lease_prod_id=b.lease_prod_id AND ISNULL(a.lease_prod_id,0) > 0 AND a.oil_gas_code='G' AND LEN(b.tx_well_id)=14 AND LEN(b.api_number)=10 AND a.tx_well_id IS NULL AND a.api_number IS NULL;
	
	UPDATE tx_production
	  SET tx_well_id=b.tx_well_id, api_number=b.api_number
	  FROM tx_production a, tx_ref_well_id b
	  WHERE a.lease_id=b.lease_id AND a.oil_gas_code='G';
	
	UPDATE tx_production
	  SET tx_well_id=b.tx_well_id
	  FROM tx_production a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.lease_id=b.lease_id AND a.oil_gas_code='G' AND a.tx_well_id IS NULL;
	
	UPDATE tx_production
	  SET tx_well_id=b.tx_well_id
	  FROM tx_production a, tx_ref_well_id b
	  WHERE a.oil_gas_code='G' AND a.lease_id=b.lease_id AND a.well_no=b.well_no AND a.tx_well_id IS NULL;
	
	UPDATE tx_production
	  SET tx_well_id=b.tx_well_id
	  FROM tx_production a, tx_ref_well_id b
	  WHERE a.oil_gas_code='G' AND a.lease_id=b.lease_id AND a.tx_well_id IS NULL;
	
	
	UPDATE tx_ref_well_id
	  SET district_no=b.district_no, lease_id=b.lease_id
	  FROM tx_ref_well_id a, tx_wellbore_data_lite b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.lease_no=b.lease_no AND a.lease_id IS NULL AND a.oil_gas_code=b.oil_gas_code AND b.lease_id IS NOT NULL;
	"""
	curr.execute(sql_update)
	gd.commit(curr)

	print 'Updating new_well_data table ...'
	sql_update_new_well_data = \
		"""
	UPDATE tx_wellbore_data_lite SET process_code=0;
	UPDATE tx_well_data_master SET process_code=0;
	UPDATE tx_permit_data SET process_code=0;
	UPDATE tx_completion_data SET process_code=0;
	UPDATE tx_oil_field_schedule SET process_code=0;
	
	UPDATE tx_wellbore_data_lite SET process_code=1 WHERE tx_well_id IS NULL;
	UPDATE tx_well_data_master SET process_code=1 WHERE tx_well_id IS NULL;
	UPDATE tx_permit_data SET process_code=1 WHERE tx_well_id IS NULL;
	UPDATE tx_completion_data SET process_code=1 WHERE tx_well_id IS NULL;
	UPDATE tx_oil_field_schedule SET process_code=1 WHERE tx_well_id IS NULL;
	
	UPDATE tx_wellbore_data_lite SET process_code=2 WHERE process_code=1 AND lease_id IS NOT NULL;
	UPDATE tx_well_data_master SET process_code=2 WHERE process_code=1 AND lease_id IS NOT NULL;
	UPDATE tx_permit_data SET process_code=2 WHERE process_code=1 AND lease_id IS NOT NULL;
	UPDATE tx_completion_data SET process_code=2 WHERE process_code=1 AND lease_id IS NOT NULL;
	UPDATE tx_oil_field_schedule SET process_code=2 WHERE process_code=1 AND lease_id IS NOT NULL;
	
	INSERT INTO tx_new_well_data (lease_no, well_no, district_no, oil_gas_code, county_no, api_number, lease_id, process_code)
	  (SELECT DISTINCT lease_no, well_no, district_no, oil_gas_code, county_code, api_number, lease_id, process_code FROM tx_wellbore_data_lite WHERE process_code=2);
	
	INSERT INTO tx_new_well_data (lease_no, well_no, district_no, oil_gas_code, county_no, api_number, lease_id, process_code)
	  (SELECT DISTINCT lease_no, well_no, district_no, oil_gas_code, county_no, api_number, lease_id, process_code FROM tx_well_data_master WHERE process_code=2);
	
	INSERT INTO tx_new_well_data (lease_no, well_no, district_no, oil_gas_code, county_no, api_number, lease_id, process_code)
	  (SELECT DISTINCT lease_no, well_no, district_no, oil_gas_code, county_no, api_number, lease_id, process_code FROM tx_permit_data WHERE process_code=2);
	
	INSERT INTO tx_new_well_data (lease_no, well_no, district_no, oil_gas_code, county_no, api_number, lease_id, process_code)
	  (SELECT DISTINCT lease_no, well_no, district, oil_gas_type_code, county, api_no, lease_id, process_code FROM tx_completion_data WHERE process_code=2);
	
	INSERT INTO tx_new_well_data (lease_no, well_no, district_no, oil_gas_code, county_no, api_number, lease_id, process_code)
	  (SELECT DISTINCT lease_no, well_no, district_no, 'O', county_no, api_number, lease_id, process_code FROM tx_oil_field_schedule WHERE process_code=2);
	
	UPDATE tx_ref_well_id SET process_code=1;
	
	INSERT INTO tx_ref_well_id (api_number, lease_no, well_no, oil_gas_code, district_no, county_no, lease_id, process_code)
	  (SELECT DISTINCT api_number, lease_no, well_no, oil_gas_code, district_no, county_no, lease_id, process_code FROM tx_new_well_data);
	
	UPDATE tx_ref_well_id SET wellbore_no='98' WHERE process_code=2;
	"""
	curr.execute(sql_update_new_well_data)
	gd.commit(curr)
	curr.close()
	conn.close()


def update_tx_ref_well_id():
	print 'Updating tx_ref_well_id ...'
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	tx_well_data = gd.get_data('api_number, id, oil_gas_code', 'dbo.tx_ref_well_id', database='US_Wells_Texas',
	                           server='sql_server', sql_where="wellbore_no='98' AND oil_gas_code IS NOT NULL",
	                           datatype='plural', cursor=curr)
	sql_update = "UPDATE dbo.tx_ref_well_id SET wellbore_no='{}' WHERE api_number='{}' AND id={} AND oil_gas_code='{}'"
	well_data_count = len(tx_well_data)
	well_data_num = 1
	for api_number, well_id, oil_gas_code in tx_well_data:
		print '{}/{}: {} - {} - {}'.format(well_data_num, well_data_count, api_number, well_id, oil_gas_code)
		sql_where = "wellbore_no!='98' AND api_number='{}' AND oil_gas_code='{}'"
		try:
			max_wellbore_no = gd.get_data('MAX(wellbore_no)', 'dbo.tx_ref_well_id', database='US_Wells_Texas',
			                              server='sql_server', sql_where=sql_where.format(api_number, oil_gas_code),
			                              single_value=True)
			max_wellbore_indx = WELLBORE_NUMS.index(max_wellbore_no)
		except:
			max_wellbore_indx = -1
		wellbore_no = WELLBORE_NUMS[max_wellbore_indx + 1]
		curr.execute(sql_update.format(wellbore_no, api_number, well_id, oil_gas_code))
		gd.commit(curr)
		well_data_num += 1
	curr.execute(
		"UPDATE dbo.tx_ref_well_id SET tx_well_id=CONCAT(api_number,'00',wellbore_no) WHERE oil_gas_code='O' AND tx_well_id IS NULL AND LEN(wellbore_no)=2")
	gd.commit(curr)
	curr.execute(
		"UPDATE dbo.tx_ref_well_id SET tx_well_id=CONCAT(api_number,'01',wellbore_no) WHERE oil_gas_code='G' AND tx_well_id IS NULL AND LEN(wellbore_no)=2")
	gd.commit(curr)
	curr.close()
	conn.close()


def update_well_details():
	print 'Updating tx_well_details ...'
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()
	max_id = gd.get_data('MAX(id)', 'dbo.tx_well_details', cursor=curr, server='sql_server', database='US_Wells_Texas',
	                     single_value=True, datatype='int')
	sql_update_well_details = \
		"""
	UPDATE tx_ref_well_id SET tx_well_id=REPLACE(tx_well_id, ' ', '');
	UPDATE tx_ref_well_id SET api_number=REPLACE(api_number, ' ', '');
	
	UPDATE tx_well_data_master SET tx_well_id=b.tx_well_id
	  FROM tx_well_data_master a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.oil_gas_code=b.oil_gas_code AND a.well_no=b.well_no AND a.lease_no=b.lease_no;
	
	UPDATE tx_oil_field_schedule
	  SET tx_well_id=b.tx_well_id
	  FROM tx_oil_field_schedule a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.lease_id=b.lease_id AND a.well_no=b.well_no AND a.tx_well_id IS NULL;
	
	UPDATE tx_well_details
	  SET tx_well_id=b.tx_well_id
	  FROM tx_well_details a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.lease_id=b.lease_id AND a.well_no=b.well_no AND a.tx_well_id IS NULL;
	
	UPDATE tx_permit_data
	  SET tx_well_id=b.tx_well_id
	  FROM tx_permit_data AS a, tx_ref_well_id AS b
	  WHERE a.api_number=b.api_number AND a.lease_id=b.lease_id AND a.well_no=b.well_no AND a.tx_well_id IS NULL;
	
	UPDATE tx_completion_data
	  SET tx_well_id=b.tx_well_id
	  FROM tx_completion_data AS a, tx_ref_well_id AS b
	  WHERE a.api_no=b.api_number AND a.lease_id=b.lease_id AND a.well_no=b.well_no AND a.tx_well_id IS NULL;
	
	UPDATE tx_wellbore_data_lite SET tx_well_id=b.tx_well_id
	  FROM tx_wellbore_data_lite a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.well_no=b.well_no AND a.oil_gas_code=b.oil_gas_code AND a.tx_well_id IS NULL;
	
	UPDATE tx_ref_well_id SET process_code=0;
	
	UPDATE tx_ref_well_id SET process_code=1
	  FROM tx_ref_well_id a, tx_well_details b
	  WHERE a.tx_well_id=b.tx_well_id;
	
	
	INSERT INTO tx_well_details (id, lease_no, well_no, district_no, commodity, county_no, api_number, lease_id, tx_well_id)
	 (SELECT DISTINCT (id+{}), lease_no, well_no, district_no, oil_gas_code, county_no, api_number, lease_id, tx_well_id
	  FROM tx_ref_well_id WHERE process_code=0 AND tx_well_id IS NOT NULL);

	UPDATE tx_well_details SET well_id=(90000000+id) WHERE ISNULL(well_id,0)=0;
	
	UPDATE tx_well_details SET process_code=0;
	UPDATE tx_well_details SET process_code=1 WHERE well_id > 90000000;
	
	UPDATE tx_well_details
	  SET lease_id=b.lease_id
	  FROM tx_well_details a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.well_no=b.well_no AND a.lease_no=b.lease_no AND a.lease_id IS NULL;
	
	UPDATE tx_well_details
	  SET tx_well_id=b.tx_well_id
	  FROM tx_well_details a, tx_ref_well_id b
	  WHERE a.tx_well_id IS NULL AND b.tx_well_id IS NOT NULL AND a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.well_no=b.well_no AND a.commodity=b.oil_gas_code;
	
	UPDATE tx_well_details
	  SET tx_well_id=b.tx_well_id
	  FROM tx_well_details a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.lease_id=b.lease_id AND a.well_no=b.well_no AND a.tx_well_id IS NULL;
	
	UPDATE tx_well_details SET completion_date=b.completion_date, plug_date=b.plug_date, operator=b.operator, total_depth=b.total_depth
	  FROM tx_well_details a, tx_well_data_master b
	  WHERE a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.commodity=b.oil_gas_code AND a.process_code=1;
	
	UPDATE tx_well_details SET field_no=b.field_no, operator_no=b.operator_no, shut_in_date=b.wl_shut_in_date, well_status=b.well_type_name
	  FROM tx_well_details a, tx_wellbore_data_lite b
	  WHERE a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.commodity=b.oil_gas_code AND a.well_no=b.well_no AND a.process_code=1;
	
	UPDATE tx_well_details
	  SET tx_well_id=b.tx_well_id
	  FROM tx_well_details a, tx_ref_well_id b
	  WHERE a.tx_well_id IS NULL AND b.tx_well_id IS NOT NULL AND a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.well_no=b.well_no AND a.commodity=b.oil_gas_code;
	
	
	UPDATE tx_well_details SET lease_name=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(lease_name,'''',''),'#',''),'(',''),')',''),'-',''),'"',''),'.',''),',','');
	
	UPDATE tx_well_details
	  SET shut_in_date=b.SHUT_IN_DATE
	  FROM tx_well_details a,
		   (SELECT api_number, lease_id, well_no, oil_gas_code, MAX(WL_SHUT_IN_DATE) AS shut_in_date FROM tx_wellbore_data_lite GROUP BY api_number, lease_id, well_no, oil_gas_code) b
	  WHERE LEN(b.SHUT_IN_DATE) > 1 AND a.api_number=b.api_number AND a.lease_id=b.lease_id AND a.well_no=b.well_no AND a.commodity=b.oil_gas_code AND a.process_code=1;
	
	UPDATE tx_well_details
	  SET plug_date=b.PLUG_DATE
	  FROM tx_well_details a, tx_wellbore_data_lite b
	  WHERE LEN(b.PLUG_DATE) > 1 AND a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.commodity=b.oil_gas_code AND a.process_code=1;
	
	UPDATE tx_well_details SET plug_date=NULL;
	
	UPDATE tx_well_details SET completion_date=NULL;
	
	UPDATE tx_well_details
	  SET completion_date=b.COMPLETION_DATE
	  FROM tx_well_details a, tx_wellbore_data_lite b
	  WHERE a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.well_no=b.well_no AND a.commodity=b.oil_gas_code AND LEN(b.COMPLETION_DATE)=6 AND a.process_code=1;
	
	UPDATE tx_well_details SET lateral_length=0 WHERE lateral_length < 0;
	UPDATE tx_well_details SET lateral_length=20000 WHERE lateral_length > 20000;
	
	UPDATE tx_well_details
	  SET well_direction=b.well_direction, total_depth=b.total_depth
	  FROM tx_well_details AS a, tx_permit_data AS b
	  WHERE a.tx_well_id=b.tx_well_id;
	
	UPDATE tx_well_details
	  SET well_direction=b.well_direction, total_depth=b.total_depth
	  FROM tx_well_details AS a, tx_permit_data AS b
	  WHERE a.tx_well_id=b.tx_well_id AND a.well_direction IS NULL;
	
	
	UPDATE tx_well_details
	  SET total_depth=b.total_depth
	  FROM tx_well_details AS a, tx_well_data_master AS b
	  WHERE a.well_no=b.well_no AND a.district_no=b.district_no AND a.county_no=b.county_no AND a.api_number=b.api_number AND a.lease_no=b.lease_no;
	
	UPDATE tx_well_details
	  SET total_depth=b.total_depth
	  FROM tx_well_details AS a, tx_well_data_master AS b
	  WHERE a.well_no=b.well_no AND a.district_no=b.district_no AND a.county_no=b.county_no AND a.api_number=b.api_number AND ISNULL(a.total_depth,0)=0;
	
	UPDATE tx_well_details
	  SET api_depth=b.api_depth
	  FROM tx_well_details AS a, tx_wellbore_data_lite AS b
	  WHERE a.tx_well_id=b.tx_well_id AND ISNULL(a.api_depth,0)=0;
	
	UPDATE tx_well_details
	  SET county_no=SUBSTRING(api_number,3,3)
	  WHERE county_no IS NULL AND LEN(api_number)=10;
	
	UPDATE tx_well_details
	  SET api_number=REPLACE(api_number,' ','');
	
	UPDATE tx_well_details
	  SET true_vertical_depth=api_depth
	  WHERE NOT ISNULL(api_depth,0)=0;
	
	UPDATE tx_well_details
	  SET true_vertical_depth=total_depth
	  WHERE NOT total_depth IS NULL AND true_vertical_depth IS NULL;
	
	UPDATE tx_well_details
	  SET Well_Direction='Horizontal'
	  WHERE Well_Direction='Horizontal Sidetrack';
	
	UPDATE tx_well_details
	  SET Well_Direction='Vertical'
	  WHERE Well_Direction='Vertical Sidetrack';
	
	UPDATE tx_well_details
	  SET Well_Direction='Directional'
	  WHERE Well_Direction='Directional Sidetrack';
	
	UPDATE tx_well_details
	  SET Well_Direction='Horizontal'
	  WHERE well_no LIKE '%H' AND NOT Well_direction IN ('Horizontal', 'Vertical', 'Directional') AND NOT well_direction IS NULL;
	
	UPDATE tx_well_details
	  SET Well_Direction='Horizontal'
	  WHERE lateral_length > 1000 AND NOT Well_direction IN ('Horizontal', 'Vertical', 'Directional') AND NOT well_direction IS NULL;
	
	UPDATE tx_well_details
	  SET Well_Direction='Vertical'
	  WHERE lateral_length <= 1000 AND NOT Well_direction IN ('Horizontal', 'Vertical', 'Directional') AND NOT well_direction IS NULL;
	
	UPDATE tx_well_details
	  SET Well_Direction='Horizontal'
	  WHERE Well_Direction LIKE '%Horizontal%' AND NOT Well_direction IN ('Horizontal', 'Vertical', 'Directional') AND NOT well_direction IS NULL;
	
	UPDATE tx_well_details
	  SET Well_Direction='Vertical'
	  WHERE Well_Direction LIKE '%Vertical%' AND NOT Well_direction IN ('Horizontal', 'Vertical', 'Directional') AND NOT well_direction IS NULL;
	
	UPDATE tx_well_details
	  SET state_well_direction=REPLACE(state_well_direction,',',':');
	
	UPDATE tx_well_details
	  SET state_well_direction=well_direction
	  WHERE NOT well_direction IS NULL;
	
	UPDATE tx_well_details
	  SET well_direction='Vertical'
	  WHERE well_direction IS NULL AND ISNULL(lateral_length,0) > 0 AND lateral_length <= 1000;
	
	UPDATE tx_well_details
	  SET well_direction='Horizontal'
	  WHERE well_direction IS NULL AND ISNULL(lateral_length,0) > 1000;
	
	UPDATE tx_well_details
	  SET Resource_Play=NULL WHERE LEN(Resource_Play)=0;
	
	UPDATE tx_well_details SET well_status='PRODUCING' FROM tx_well_details a, tx_completion_data b
	  WHERE a.tx_well_id=b.tx_well_id AND b.well_type=1; 
	
	UPDATE tx_well_details SET well_status='SHUT IN' FROM tx_well_details a, tx_completion_data b
	  WHERE a.tx_well_id=b.tx_well_id AND b.well_type=2; 
	
	UPDATE tx_well_details SET well_status='INJECTION' FROM tx_well_details a, tx_completion_data b
	  WHERE a.tx_well_id=b.tx_well_id AND b.well_type=3; 
	
	UPDATE tx_well_details
	  SET measured_depth=b.measured_depth
	  FROM tx_well_details AS a, tx_completion_data AS b
	  WHERE a.tx_well_id=b.tx_well_id AND NOT b.measured_depth IS NULL AND a.measured_depth IS NULL;
	
	UPDATE tx_well_details
	  SET true_vertical_depth=b.vertical_depth
	  FROM tx_well_details AS a, tx_completion_data AS b
	  WHERE a.tx_well_id=b.tx_well_id AND NOT b.vertical_depth IS NULL AND a.true_vertical_depth IS NULL;
	
	UPDATE tx_well_details
	  SET spud_date=b.spud_dt
	  FROM tx_well_details AS a, tx_completion_data AS b
	  WHERE a.tx_well_id=b.tx_well_id AND LEN(b.spud_dt)=6;
	
	UPDATE tx_well_details
	  SET completion_date=b.completion_date
	  FROM tx_well_details AS a, tx_well_data_master AS b
	  WHERE a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.commodity=b.oil_gas_code AND a.completion_date IS NULL AND b.completion_date IS NOT NULL;
	
	UPDATE tx_well_details
	  SET plug_date=b.plug_date
	  FROM tx_well_details AS a, tx_well_data_master AS b
	  WHERE a.api_number=b.api_number AND a.lease_no=b.lease_no AND a.commodity=b.oil_gas_code AND a.plug_date IS NULL AND b.plug_date IS NOT NULL;
	
	UPDATE tx_well_details
	  SET spud_date=b.spud_dt
	  FROM tx_well_details AS a, tx_completion_data AS b
	  WHERE a.tx_well_id=b.tx_well_id AND LEN(b.spud_dt) > 5 AND a.spud_date IS NULL;
	
	UPDATE tx_well_details SET spud_date=CONCAT(SUBSTRING(spud_date,7,4),SUBSTRING(spud_date,4,2)) WHERE LEN(spud_date)=10 AND spud_date LIKE '%/%/%';
	UPDATE tx_well_details SET completion_date=REPLACE(completion_date,' ','');
	UPDATE tx_well_details SET completion_date=CONCAT(SUBSTRING(completion_date,1,4),SUBSTRING(completion_date,6,2)) WHERE LEN(completion_date)=10 AND completion_date LIKE '%-%-%';
	UPDATE tx_well_details SET plug_date=SUBSTRING(plug_date,1,6) WHERE LEN(plug_date) > 6;
	UPDATE tx_well_details SET plug_date=CONCAT(SUBSTRING(plug_date,1,4),'12') WHERE LEN(plug_date)=6 AND SUBSTRING(plug_date,5,2)='00';
	UPDATE tx_well_details SET completion_date=CONCAT(SUBSTRING(completion_date,1,4),'01') WHERE LEN(completion_date)=6 AND SUBSTRING(completion_date,5,2)='00';
	
	UPDATE tx_well_details SET completion_date=SUBSTRING(completion_date,1,6) WHERE LEN(completion_date) > 6;
	
	UPDATE tx_well_details SET process_code=0;
	UPDATE tx_well_details SET process_code=1 WHERE tx_well_id IN (SELECT DISTINCT tx_well_id FROM tx_oil_prod_schedule_2);
	
	UPDATE tx_well_details SET spud_date=NULL WHERE LEN(spud_date)<6;
	UPDATE tx_well_details SET completion_date=NULL WHERE LEN(completion_date)<6;
	UPDATE tx_well_details SET plug_date=NULL WHERE LEN(plug_date)<6;
	UPDATE tx_well_details SET shut_in_date=NULL WHERE LEN(shut_in_date)<6;
	UPDATE tx_well_details SET first_production_date=NULL WHERE LEN(first_production_date)=0;
	UPDATE tx_well_details SET last_production_date=NULL WHERE LEN(last_production_date)=0;
	UPDATE tx_well_details SET lease_name=NULL WHERE LEN(lease_name)=0;
	
	UPDATE tx_well_details SET spud_date=NULL WHERE LEN(spud_date)=0;
	UPDATE tx_well_details SET formation=NULL WHERE LEN(formation)=0;
	UPDATE tx_well_details SET basin=NULL WHERE LEN(basin)=0;
	UPDATE tx_well_details SET well_status=NULL WHERE LEN(well_status)=0;
	UPDATE tx_well_details SET engine_well_status=NULL WHERE LEN(engine_well_status)=0;
	UPDATE tx_well_details SET well_direction=NULL WHERE LEN(well_direction)=0;
	UPDATE tx_well_details SET state_well_direction=NULL WHERE LEN(state_well_direction)=0;
	
	
	UPDATE tx_well_details SET basin=b.Basin FROM tx_well_details a, US_Wells.dbo.tblUSWell_Details b WHERE a.tx_well_id=b.API_14;
	UPDATE tx_well_details SET well_id=b.WellID FROM tx_well_details a, US_Wells.dbo.tblUSWell_Details b WHERE a.tx_well_id=b.API_14;

	UPDATE tx_well_details SET resource_play=b.shale FROM tx_well_details a, US_Wells.dbo.tblUSWell_Details b WHERE a.tx_well_id=b.API_14 AND LEN(b.Shale) >0;
	UPDATE tx_well_details SET operator=b.ParentOperator FROM tx_well_details a, US_Wells.dbo.tblUSWell_Details b WHERE a.tx_well_id=b.API_14 AND LEN(b.ParentOperator) >0;
	
	UPDATE tx_well_details SET lease_start_date=b.lease_min, lease_end_date=b.lease_max
	  FROM tx_well_details a,
		(SELECT DISTINCT lease_id, MIN(prod_date) AS lease_min, MAX(prod_date) AS lease_max FROM tx_production_data
		 WHERE (ISNULL(oil_prod_vol,0)+ISNULL(gas_prod_vol,0)+ISNULL(cond_prod_vol,0)+ISNULL(csgd_prod_vol,0)) > 0 GROUP BY lease_id) b
	  WHERE a.lease_id=b.lease_id;
	
	UPDATE tx_well_details SET first_production_date=NULL;
	UPDATE tx_well_details SET last_production_date=NULL;
	UPDATE tx_well_details SET first_production_date=lease_start_date WHERE lease_start_date IS NOT NULL;
	UPDATE tx_well_details SET last_production_date=lease_end_date WHERE lease_end_date IS NOT NULL;
	
	UPDATE tx_well_details SET lease_id=b.lease_id FROM tx_well_details a, tx_production b WHERE a.tx_well_id=b.tx_well_id AND a.lease_id IS NULL AND a.tx_well_id IS NOT NULL;
	UPDATE tx_well_details SET district_no=SUBSTRING(lease_id,2,2) WHERE district_no IS NULL AND lease_id IS NOT NULL;
	
	UPDATE tx_well_details
	  SET tx_well_id=b.tx_well_id
	  FROM tx_well_details a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.lease_id=b.lease_id AND a.well_no=b.well_no AND b.process_code=1;
	
	UPDATE tx_well_details
	  SET tx_well_id=b.tx_well_id
	  FROM tx_well_details a, tx_ref_well_id b
	  WHERE a.api_number=b.api_number AND a.lease_id=b.lease_id AND a.well_no=b.well_no;
	"""
	# print sql_update_well_details.format(max_id)
	curr.execute(sql_update_well_details.format(max_id))
	gd.commit(curr)

	curr.close()
	conn.close()


def process_well_details_data(well_data=False, tx_well_id=False, well_details=False):
	if well_data:
		update_well_data_tables()
	if tx_well_id:
		update_tx_ref_well_id()
	if well_details:
		update_well_details()


def update_engine_gas_production(debug=False):
	print 'Updating US_Wells.dbo.tblUSWell_Production with Texas Gas Production data ...'
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()

	sql_update = \
		"""
	INSERT INTO US_Wells.dbo.tblUSWell_Production (API_Number,[Period],oil_jan_bbl,oil_feb_bbl,oil_mar_bbl,oil_apr_bbl,oil_may_bbl,oil_jun_bbl,oil_jul_bbl,oil_aug_bbl,oil_sep_bbl,oil_oct_bbl,oil_nov_bbl,oil_dec_bbl,gas_jan_mcf,gas_feb_mcf,gas_mar_mcf,gas_apr_mcf,gas_may_mcf,gas_jun_mcf,gas_jul_mcf,gas_aug_mcf,gas_sep_mcf,gas_oct_mcf,gas_nov_mcf,gas_dec_mcf,condensate_jan_bbl,condensate_feb_bbl,condensate_mar_bbl,condensate_apr_bbl,condensate_may_bbl,condensate_jun_bbl,condensate_jul_bbl,condensate_aug_bbl,condensate_sep_bbl,condensate_oct_bbl,condensate_nov_bbl,condensate_dec_bbl,[Source],PkgId,API_14)
	  (SELECT DISTINCT tx_well_id,prod_year,oil_jan_bbl,oil_feb_bbl,oil_mar_bbl,oil_apr_bbl,oil_may_bbl,oil_jun_bbl,oil_jul_bbl,oil_aug_bbl,oil_sep_bbl,oil_oct_bbl,oil_nov_bbl,oil_dec_bbl,(gas_jan_mcf + csgd_jan_mcf),(gas_feb_mcf + csgd_feb_mcf),(gas_mar_mcf + csgd_mar_mcf),(gas_apr_mcf + csgd_apr_mcf),(gas_may_mcf + csgd_may_mcf),(gas_jun_mcf + csgd_jun_mcf),(gas_jul_mcf + csgd_jul_mcf),(gas_aug_mcf + csgd_aug_mcf),(gas_sep_mcf + csgd_sep_mcf),(gas_oct_mcf + csgd_oct_mcf),(gas_nov_mcf + csgd_nov_mcf),(gas_dec_mcf + csgd_dec_mcf),cond_jan_bbl,cond_feb_bbl,cond_mar_bbl,cond_apr_bbl,cond_may_bbl,cond_jun_bbl,cond_jul_bbl,cond_aug_bbl,cond_sep_bbl,cond_oct_bbl,cond_nov_bbl,cond_dec_bbl,'Historical',1000001,tx_well_id
	   FROM tx_production WHERE oil_gas_code='G' AND process_code!=9);
	
	UPDATE US_Wells.dbo.tblUSWell_Production
	  SET Gas_Total_mcf=ROUND(ISNULL(Gas_Jan_mcf,0) + ISNULL(Gas_Feb_mcf,0) + ISNULL(Gas_Mar_mcf,0) + ISNULL(Gas_Apr_mcf,0) + ISNULL(Gas_May_mcf,0) + ISNULL(Gas_Jun_mcf,0) + ISNULL(Gas_Jul_mcf,0) + ISNULL(Gas_Aug_mcf,0) + ISNULL(Gas_Sep_mcf,0) + ISNULL(Gas_Oct_mcf,0) + ISNULL(Gas_Nov_mcf,0) + ISNULL(Gas_Dec_mcf,0),2),
		  Oil_Total_bbl=ROUND(ISNULL(Oil_Jan_bbl,0) + ISNULL(Oil_Feb_bbl,0) + ISNULL(Oil_Mar_bbl,0) + ISNULL(Oil_Apr_bbl,0) + ISNULL(Oil_May_bbl,0) + ISNULL(Oil_Jun_bbl,0) + ISNULL(Oil_Jul_bbl,0) + ISNULL(Oil_Aug_bbl,0) + ISNULL(Oil_Sep_bbl,0) + ISNULL(Oil_Oct_bbl,0) + ISNULL(Oil_Nov_bbl,0) + ISNULL(Oil_Dec_bbl,0),2),
		  Water_Total_bbl=ROUND(ISNULL(Water_Jan_bbl,0) + ISNULL(Water_Feb_bbl,0) + ISNULL(Water_Mar_bbl,0) + ISNULL(Water_Apr_bbl,0) + ISNULL(Water_May_bbl,0) + ISNULL(Water_Jun_bbl,0) + ISNULL(Water_Jul_bbl,0) + ISNULL(Water_Aug_bbl,0) + ISNULL(Water_Sep_bbl,0) + ISNULL(Water_Oct_bbl,0) + ISNULL(Water_Nov_bbl,0),0) + ISNULL(Water_Dec_bbl,2),
		  NGL_Total_bbl=ROUND(ISNULL(NGL_Jan_bbl,0) + ISNULL(NGL_Feb_bbl,0) + ISNULL(NGL_Mar_bbl,0) + ISNULL(NGL_Apr_bbl,0) + ISNULL(NGL_May_bbl,0) + ISNULL(NGL_Jun_bbl,0) + ISNULL(NGL_Jul_bbl,0) + ISNULL(NGL_Aug_bbl,0) + ISNULL(NGL_Sep_bbl,0) + ISNULL(NGL_Oct_bbl,0) + ISNULL(NGL_Nov_bbl,0) + ISNULL(NGL_Dec_bbl,0),2),
		  Condensate_Total_bbl=ROUND(ISNULL(Condensate_Jan_bbl,0) + ISNULL(Condensate_Feb_bbl,0) + ISNULL(Condensate_Mar_bbl,0) + ISNULL(Condensate_Apr_bbl,0) + ISNULL(Condensate_May_bbl,0) + ISNULL(Condensate_Jun_bbl,0) + ISNULL(Condensate_Jul_bbl,0) + ISNULL(Condensate_Aug_bbl,0) + ISNULL(Condensate_Sep_bbl,0) + ISNULL(Condensate_Oct_bbl,0) + ISNULL(Condensate_Nov_bbl,0) + ISNULL(Condensate_Dec_bbl,0),2);
	
	UPDATE US_Wells.dbo.tblUSWell_Production SET WellID=b.well_id
	  FROM US_Wells.dbo.tblUSWell_Production a, US_Wells_Texas.dbo.tx_well_details b
	  WHERE a.API_Number=b.tx_well_id AND a.WellID IS NULL AND a.PkgId=1000001;
	
	INSERT INTO US_Wells.dbo.tblUSWell_Production_Forecast (WellID, API_Number, StateID, [Period], Gas_Total_mcf, Gas_Jan_mcf, Gas_Feb_mcf, Gas_Mar_mcf, Gas_Apr_mcf, Gas_May_mcf, Gas_Jun_mcf, Gas_Jul_mcf, Gas_Aug_mcf, Gas_Sep_mcf, Gas_Oct_mcf, Gas_Nov_mcf, Gas_Dec_mcf, Oil_Total_bbl, Oil_Jan_bbl, Oil_Feb_bbl, Oil_Mar_bbl, Oil_Apr_bbl, Oil_May_bbl, Oil_Jun_bbl, Oil_Jul_bbl, Oil_Aug_bbl, Oil_Sep_bbl, Oil_Oct_bbl, Oil_Nov_bbl, Oil_Dec_bbl, Condensate_Total_bbl, Condensate_Jan_bbl, Condensate_Feb_bbl, Condensate_Mar_bbl, Condensate_Apr_bbl, Condensate_May_bbl, Condensate_Jun_bbl, Condensate_Jul_bbl, Condensate_Aug_bbl, Condensate_Sep_bbl, Condensate_Oct_bbl, Condensate_Nov_bbl, Condensate_Dec_bbl, NGL_Total_bbl, NGL_Jan_bbl, NGL_Feb_bbl, NGL_Mar_bbl, NGL_Apr_bbl, NGL_May_bbl, NGL_Jun_bbl, NGL_Jul_bbl, NGL_Aug_bbl, NGL_Sep_bbl, NGL_Oct_bbl, NGL_Nov_bbl, NGL_Dec_bbl, Water_Total_bbl, Water_Jan_bbl, Water_Feb_bbl, Water_Mar_bbl, Water_Apr_bbl, Water_May_bbl, Water_Jun_bbl, Water_Jul_bbl, Water_Aug_bbl, Water_Sep_bbl, Water_Oct_bbl, Water_Nov_bbl, Water_Dec_bbl, Reported_API_Number, Sources)
	  (SELECT DISTINCT ISNULL(WellID,0), ISNULL(API_14,'00000000000000'), SUBSTRING(API_14,1,2), [Period], Gas_Total_mcf, Gas_Jan_mcf, Gas_Feb_mcf, Gas_Mar_mcf, Gas_Apr_mcf, Gas_May_mcf, Gas_Jun_mcf, Gas_Jul_mcf, Gas_Aug_mcf, Gas_Sep_mcf, Gas_Oct_mcf, Gas_Nov_mcf, Gas_Dec_mcf, Oil_Total_bbl, Oil_Jan_bbl, Oil_Feb_bbl, Oil_Mar_bbl, Oil_Apr_bbl, Oil_May_bbl, Oil_Jun_bbl, Oil_Jul_bbl, Oil_Aug_bbl, Oil_Sep_bbl, Oil_Oct_bbl, Oil_Nov_bbl, Oil_Dec_bbl, Condensate_Total_bbl, Condensate_Jan_bbl, Condensate_Feb_bbl, Condensate_Mar_bbl, Condensate_Apr_bbl, Condensate_May_bbl, Condensate_Jun_bbl, Condensate_Jul_bbl, Condensate_Aug_bbl, Condensate_Sep_bbl, Condensate_Oct_bbl, Condensate_Nov_bbl, Condensate_Dec_bbl, NGL_Total_bbl, NGL_Jan_bbl, NGL_Feb_bbl, NGL_Mar_bbl, NGL_Apr_bbl, NGL_May_bbl, NGL_Jun_bbl, NGL_Jul_bbl, NGL_Aug_bbl, NGL_Sep_bbl, NGL_Oct_bbl, NGL_Nov_bbl, NGL_Dec_bbl, Water_Total_bbl, Water_Jan_bbl, Water_Feb_bbl, Water_Mar_bbl, Water_Apr_bbl, Water_May_bbl, Water_Jun_bbl, Water_Jul_bbl, Water_Aug_bbl, Water_Sep_bbl, Water_Oct_bbl, Water_Nov_bbl, Water_Dec_bbl, API_Number, [Source]
	   FROM US_Wells.dbo.tblUSWell_Production WHERE PkgId=1000001);
	
	UPDATE US_Wells.dbo.tblUSWell_Production_Forecast
	  SET Gas_Total_mcf=ISNULL(Gas_Total_mcf,0),
		  Oil_Total_bbl=ISNULL(Oil_Total_bbl,0),
		  Condensate_Total_bbl=ISNULL(Condensate_Total_bbl,0),
		  NGL_Total_bbl=ISNULL(NGL_Total_bbl,0),
		  Water_Total_bbl=ISNULL(Water_Total_bbl,0),
		  Gas_Jan_mcf=ISNULL(Gas_Jan_mcf,0),
		  Gas_Feb_mcf=ISNULL(Gas_Feb_mcf,0),
		  Gas_Mar_mcf=ISNULL(Gas_Mar_mcf,0),
		  Gas_Apr_mcf=ISNULL(Gas_Apr_mcf,0),
		  Gas_May_mcf=ISNULL(Gas_May_mcf,0),
		  Gas_Jun_mcf=ISNULL(Gas_Jun_mcf,0),
		  Gas_Jul_mcf=ISNULL(Gas_Jul_mcf,0),
		  Gas_Aug_mcf=ISNULL(Gas_Aug_mcf,0),
		  Gas_Sep_mcf=ISNULL(Gas_Sep_mcf,0),
		  Gas_Oct_mcf=ISNULL(Gas_Oct_mcf,0),
		  Gas_Nov_mcf=ISNULL(Gas_Nov_mcf,0),
		  Gas_Dec_mcf=ISNULL(Gas_Dec_mcf,0),
		  Oil_Jan_bbl=ISNULL(Oil_Jan_bbl,0),
		  Oil_Feb_bbl=ISNULL(Oil_Feb_bbl,0),
		  Oil_Mar_bbl=ISNULL(Oil_Mar_bbl,0),
		  Oil_Apr_bbl=ISNULL(Oil_Apr_bbl,0),
		  Oil_May_bbl=ISNULL(Oil_May_bbl,0),
		  Oil_Jun_bbl=ISNULL(Oil_Jun_bbl,0),
		  Oil_Jul_bbl=ISNULL(Oil_Jul_bbl,0),
		  Oil_Aug_bbl=ISNULL(Oil_Aug_bbl,0),
		  Oil_Sep_bbl=ISNULL(Oil_Sep_bbl,0),
		  Oil_Oct_bbl=ISNULL(Oil_Oct_bbl,0),
		  Oil_Nov_bbl=ISNULL(Oil_Nov_bbl,0),
		  Oil_Dec_bbl=ISNULL(Oil_Dec_bbl,0),
		  Condensate_Jan_bbl=ISNULL(Condensate_Jan_bbl,0),
		  Condensate_Feb_bbl=ISNULL(Condensate_Feb_bbl,0),
		  Condensate_Mar_bbl=ISNULL(Condensate_Mar_bbl,0),
		  Condensate_Apr_bbl=ISNULL(Condensate_Apr_bbl,0),
		  Condensate_May_bbl=ISNULL(Condensate_May_bbl,0),
		  Condensate_Jun_bbl=ISNULL(Condensate_Jun_bbl,0),
		  Condensate_Jul_bbl=ISNULL(Condensate_Jul_bbl,0),
		  Condensate_Aug_bbl=ISNULL(Condensate_Aug_bbl,0),
		  Condensate_Sep_bbl=ISNULL(Condensate_Sep_bbl,0),
		  Condensate_Oct_bbl=ISNULL(Condensate_Oct_bbl,0),
		  Condensate_Nov_bbl=ISNULL(Condensate_Nov_bbl,0),
		  Condensate_Dec_bbl=ISNULL(Condensate_Dec_bbl,0),
		  NGL_Jan_bbl=ISNULL(NGL_Jan_bbl,0),
		  NGL_Feb_bbl=ISNULL(NGL_Feb_bbl,0),
		  NGL_Mar_bbl=ISNULL(NGL_Mar_bbl,0),
		  NGL_Apr_bbl=ISNULL(NGL_Apr_bbl,0),
		  NGL_May_bbl=ISNULL(NGL_May_bbl,0),
		  NGL_Jun_bbl=ISNULL(NGL_Jun_bbl,0),
		  NGL_Jul_bbl=ISNULL(NGL_Jul_bbl,0),
		  NGL_Aug_bbl=ISNULL(NGL_Aug_bbl,0),
		  NGL_Sep_bbl=ISNULL(NGL_Sep_bbl,0),
		  NGL_Oct_bbl=ISNULL(NGL_Oct_bbl,0),
		  NGL_Nov_bbl=ISNULL(NGL_Nov_bbl,0),
		  NGL_Dec_bbl=ISNULL(NGL_Dec_bbl,0),
		  Water_Jan_bbl=ISNULL(Water_Jan_bbl,0),
		  Water_Feb_bbl=ISNULL(Water_Feb_bbl,0),
		  Water_Mar_bbl=ISNULL(Water_Mar_bbl,0),
		  Water_Apr_bbl=ISNULL(Water_Apr_bbl,0),
		  Water_May_bbl=ISNULL(Water_May_bbl,0),
		  Water_Jun_bbl=ISNULL(Water_Jun_bbl,0),
		  Water_Jul_bbl=ISNULL(Water_Jul_bbl,0),
		  Water_Aug_bbl=ISNULL(Water_Aug_bbl,0),
		  Water_Sep_bbl=ISNULL(Water_Sep_bbl,0),
		  Water_Oct_bbl=ISNULL(Water_Oct_bbl,0),
		  Water_Nov_bbl=ISNULL(Water_Nov_bbl,0),
		  Water_Dec_bbl=ISNULL(Water_Dec_bbl,0)
	  WHERE StateID='42';
	
	UPDATE US_Wells.dbo.tblUSWell_Production_Forecast
	  SET Gas_TOTAL_mcf=ROUND(ISNULL(Gas_Jan_mcf,0) + ISNULL(Gas_Feb_mcf,0) + ISNULL(Gas_Mar_mcf,0) + ISNULL(Gas_Apr_mcf,0) + ISNULL(Gas_May_mcf,0) + ISNULL(Gas_Jun_mcf,0) + ISNULL(Gas_Jul_mcf,0) + ISNULL(Gas_Aug_mcf,0) + ISNULL(Gas_Sep_mcf,0) + ISNULL(Gas_Oct_mcf,0) + ISNULL(Gas_Nov_mcf,0) + ISNULL(Gas_Dec_mcf,0),2),
		  Oil_TOTAL_bbl=ROUND(ISNULL(Oil_Jan_bbl,0) + ISNULL(Oil_Feb_bbl,0) + ISNULL(Oil_Mar_bbl,0) + ISNULL(Oil_Apr_bbl,0) + ISNULL(Oil_May_bbl,0) + ISNULL(Oil_Jun_bbl,0) + ISNULL(Oil_Jul_bbl,0) + ISNULL(Oil_Aug_bbl,0) + ISNULL(Oil_Sep_bbl,0) + ISNULL(Oil_Oct_bbl,0) + ISNULL(Oil_Nov_bbl,0) + ISNULL(Oil_Dec_bbl,0),2),
		  Water_TOTAL_bbl=ROUND(ISNULL(Water_Jan_bbl,0) + ISNULL(Water_Feb_bbl,0) + ISNULL(Water_Mar_bbl,0) + ISNULL(Water_Apr_bbl,0) + ISNULL(Water_May_bbl,0) + ISNULL(Water_Jun_bbl,0) + ISNULL(Water_Jul_bbl,0) + ISNULL(Water_Aug_bbl,0) + ISNULL(Water_Sep_bbl,0) + ISNULL(Water_Oct_bbl,0) + ISNULL(Water_Nov_bbl,0),0) + ISNULL(Water_Dec_bbl,2),
		  NGL_TOTAL_bbl=ROUND(ISNULL(NGL_Jan_bbl,0) + ISNULL(NGL_Feb_bbl,0) + ISNULL(NGL_Mar_bbl,0) + ISNULL(NGL_Apr_bbl,0) + ISNULL(NGL_May_bbl,0) + ISNULL(NGL_Jun_bbl,0) + ISNULL(NGL_Jul_bbl,0) + ISNULL(NGL_Aug_bbl,0) + ISNULL(NGL_Sep_bbl,0) + ISNULL(NGL_Oct_bbl,0) + ISNULL(NGL_Nov_bbl,0) + ISNULL(NGL_Dec_bbl,0),2),
		  Condensate_TOTAL_bbl=ROUND(ISNULL(Condensate_Jan_bbl,0) + ISNULL(Condensate_Feb_bbl,0) + ISNULL(Condensate_Mar_bbl,0) + ISNULL(Condensate_Apr_bbl,0) + ISNULL(Condensate_May_bbl,0) + ISNULL(Condensate_Jun_bbl,0) + ISNULL(Condensate_Jul_bbl,0) + ISNULL(Condensate_Aug_bbl,0) + ISNULL(Condensate_Sep_bbl,0) + ISNULL(Condensate_Oct_bbl,0) + ISNULL(Condensate_Nov_bbl,0) + ISNULL(Condensate_Dec_bbl,0),2)
	  WHERE StateID='42';

	UPDATE tx_well_details SET well_id=b.WellID FROM tx_well_details a, US_Wells.dbo.tblUSWell_Details b WHERE a.tx_well_id=b.API_14;
	
	UPDATE US_Wells.dbo.tblUSWell_Parameters SET WellID=b.well_id
	  FROM US_Wells.dbo.tblUSWell_Parameters a, US_Wells_Texas.dbo.tx_well_details b
	  WHERE a.API_Number=b.tx_well_id;
	  
	UPDATE tx_well_details SET process_code=0;
	
	UPDATE tx_well_details SET process_code=1
	  FROM tx_well_details a, US_Wells.dbo.tblUSWell_Parameters b
	  WHERE a.tx_well_id=b.API_Number;
	
	UPDATE tx_well_details SET process_code=2
	  FROM tx_well_details a, US_Wells.dbo.tblUSWell_Production b
	  WHERE a.tx_well_id=b.API_Number AND a.process_code=0;
	
	INSERT INTO US_Wells.dbo.tblUSWell_Parameters (WellID,API_Number,StateID,State_Name,Well_Direction,Operator,Commodity,Resource_Play,First_Production_Date,True_Vertical_Depth_ft,Lateral_Length_ft,Well_Status,State_Well_Direction,Forecast_Well)
	 (SELECT DISTINCT well_id,TX_Well_ID,'42','Texas',Well_Direction,Operator,Commodity,Resource_Play,First_Production_Date,True_Vertical_Depth,Lateral_Length,Well_Status,Well_Direction,9
	  FROM tx_well_details WHERE process_code=2);
	
	UPDATE US_Wells.dbo.tblUSWell_Parameters SET commodity='GAS' WHERE commodity='G';
	UPDATE US_Wells.dbo.tblUSWell_Parameters SET commodity='OIL' WHERE commodity='O';
	
	UPDATE US_Wells.dbo.tblUSWell_Parameters SET County_Code=SUBSTRING(API_Number,3,3),Oil_Decline_Rate_Type='avg',Gas_Decline_Rate_Type='avg',Cond_Decline_Rate_Type='avg',NGL_Decline_Rate_Type='avg',Capex_Tangible_Split_pct=0.67 WHERE Forecast_Well=9;
	UPDATE US_Wells.dbo.tblUSWell_Parameters SET Resource_Play=NULL WHERE LEN(Resource_Play)=0;
	
	UPDATE US_Wells.dbo.tblUSWell_Parameters SET Forecast_Well=0
	  FROM US_Wells.dbo.tblUSWell_Parameters a, US_Wells.dbo.tblUSWell_Production b
	  WHERE a.API_Number=b.API_Number AND a.State_Name='Texas' AND a.commodity='GAS';
	"""

	if debug: print sql_update

	curr.execute(sql_update)
	gd.commit(curr)

	curr.close()
	conn.close()


def update_engine_oil_production(debug=False):
	print 'Updating US_Wells.dbo.tblUSWell_Production with Allocated Texas Oil Production data ...'
	conn = gd.get_connection(database='US_Wells_Texas', server='sql_server', us_wells=True)
	curr = conn.cursor()

	sql_update = \
		"""
	UPDATE tx_well_details 
	  SET well_id=b.WellID 
	  FROM tx_well_details a, US_Wells.dbo.tblUSWell_Details b 
	  WHERE a.tx_well_id=b.API_14;
	  
	UPDATE tx_well_details SET well_id=(90000000+id) WHERE ISNULL(well_id,0)=0;
	
	UPDATE US_Wells.dbo.tblUSWell_Parameters 
	  SET WellID=b.well_id 
	  FROM US_Wells.dbo.tblUSWell_Parameters a, tx_well_details b 
	  WHERE a.API_Number=b.tx_well_id 
	  AND ISNULL(b.well_id,0)!=0;
	
	UPDATE tx_hist_oil_production 
	  SET well_id=b.well_id 
	  FROM tx_hist_oil_production a, tx_well_details b 
	  WHERE a.tx_well_id=b.tx_well_id 
	  AND ISNULL(a.well_id,0)=0 
	  AND ISNULL(b.well_id,0)!=0;
	
	 UPDATE tx_hist_oil_production 
	  SET well_id=b.WellID 
	  FROM tx_hist_oil_production a, US_Wells.dbo.tblUSWell_Parameters b 
	  WHERE a.tx_well_id=b.API_Number 
	  AND ISNULL(b.WellID,0)!=0;
	
	DELETE FROM tx_hist_oil_production WHERE (ISNULL(oil_total_bbl,0)+ISNULL(gas_total_mcf,0))=0;

	DELETE FROM US_Wells.dbo.tblUSWell_Production WHERE PkgId=1000002;

	INSERT INTO US_Wells.dbo.tblUSWell_Production (API_Number,[Period],oil_jan_bbl,oil_feb_bbl,oil_mar_bbl,oil_apr_bbl,oil_may_bbl,oil_jun_bbl,oil_jul_bbl,oil_aug_bbl,oil_sep_bbl,oil_oct_bbl,oil_nov_bbl,oil_dec_bbl,gas_jan_mcf,gas_feb_mcf,gas_mar_mcf,gas_apr_mcf,gas_may_mcf,gas_jun_mcf,gas_jul_mcf,gas_aug_mcf,gas_sep_mcf,gas_oct_mcf,gas_nov_mcf,gas_dec_mcf,[Source],PkgId,API_14)
	  (SELECT DISTINCT tx_well_id,prod_year,oil_jan_bbl,oil_feb_bbl,oil_mar_bbl,oil_apr_bbl,oil_may_bbl,oil_jun_bbl,oil_jul_bbl,oil_aug_bbl,oil_sep_bbl,oil_oct_bbl,oil_nov_bbl,oil_dec_bbl,gas_jan_mcf,gas_feb_mcf,gas_mar_mcf,gas_apr_mcf,gas_may_mcf,gas_jun_mcf,gas_jul_mcf,gas_aug_mcf,gas_sep_mcf,gas_oct_mcf,gas_nov_mcf,gas_dec_mcf,'Historical',1000002,tx_well_id
	   FROM tx_hist_oil_production);

	UPDATE US_Wells.dbo.tblUSWell_Production
	  SET Gas_Total_mcf=ROUND(ISNULL(Gas_Jan_mcf,0) + ISNULL(Gas_Feb_mcf,0) + ISNULL(Gas_Mar_mcf,0) + ISNULL(Gas_Apr_mcf,0) + ISNULL(Gas_May_mcf,0) + ISNULL(Gas_Jun_mcf,0) + ISNULL(Gas_Jul_mcf,0) + ISNULL(Gas_Aug_mcf,0) + ISNULL(Gas_Sep_mcf,0) + ISNULL(Gas_Oct_mcf,0) + ISNULL(Gas_Nov_mcf,0) + ISNULL(Gas_Dec_mcf,0),2),
		  Oil_Total_bbl=ROUND(ISNULL(Oil_Jan_bbl,0) + ISNULL(Oil_Feb_bbl,0) + ISNULL(Oil_Mar_bbl,0) + ISNULL(Oil_Apr_bbl,0) + ISNULL(Oil_May_bbl,0) + ISNULL(Oil_Jun_bbl,0) + ISNULL(Oil_Jul_bbl,0) + ISNULL(Oil_Aug_bbl,0) + ISNULL(Oil_Sep_bbl,0) + ISNULL(Oil_Oct_bbl,0) + ISNULL(Oil_Nov_bbl,0) + ISNULL(Oil_Dec_bbl,0),2),
		  Water_Total_bbl=ROUND(ISNULL(Water_Jan_bbl,0) + ISNULL(Water_Feb_bbl,0) + ISNULL(Water_Mar_bbl,0) + ISNULL(Water_Apr_bbl,0) + ISNULL(Water_May_bbl,0) + ISNULL(Water_Jun_bbl,0) + ISNULL(Water_Jul_bbl,0) + ISNULL(Water_Aug_bbl,0) + ISNULL(Water_Sep_bbl,0) + ISNULL(Water_Oct_bbl,0) + ISNULL(Water_Nov_bbl,0),0) + ISNULL(Water_Dec_bbl,2),
		  NGL_Total_bbl=ROUND(ISNULL(NGL_Jan_bbl,0) + ISNULL(NGL_Feb_bbl,0) + ISNULL(NGL_Mar_bbl,0) + ISNULL(NGL_Apr_bbl,0) + ISNULL(NGL_May_bbl,0) + ISNULL(NGL_Jun_bbl,0) + ISNULL(NGL_Jul_bbl,0) + ISNULL(NGL_Aug_bbl,0) + ISNULL(NGL_Sep_bbl,0) + ISNULL(NGL_Oct_bbl,0) + ISNULL(NGL_Nov_bbl,0) + ISNULL(NGL_Dec_bbl,0),2),
		  Condensate_Total_bbl=ROUND(ISNULL(Condensate_Jan_bbl,0) + ISNULL(Condensate_Feb_bbl,0) + ISNULL(Condensate_Mar_bbl,0) + ISNULL(Condensate_Apr_bbl,0) + ISNULL(Condensate_May_bbl,0) + ISNULL(Condensate_Jun_bbl,0) + ISNULL(Condensate_Jul_bbl,0) + ISNULL(Condensate_Aug_bbl,0) + ISNULL(Condensate_Sep_bbl,0) + ISNULL(Condensate_Oct_bbl,0) + ISNULL(Condensate_Nov_bbl,0) + ISNULL(Condensate_Dec_bbl,0),2);

	UPDATE US_Wells.dbo.tblUSWell_Production SET WellID=b.well_id
	  FROM US_Wells.dbo.tblUSWell_Production a, US_Wells_Texas.dbo.tx_well_details b
	  WHERE a.API_Number=b.tx_well_id AND ISNULL(a.WellID,0)=0 AND a.PkgId=1000002;

	INSERT INTO US_Wells.dbo.tblUSWell_Production_Forecast (WellID, API_Number, StateID, [Period], Gas_Total_mcf, Gas_Jan_mcf, Gas_Feb_mcf, Gas_Mar_mcf, Gas_Apr_mcf, Gas_May_mcf, Gas_Jun_mcf, Gas_Jul_mcf, Gas_Aug_mcf, Gas_Sep_mcf, Gas_Oct_mcf, Gas_Nov_mcf, Gas_Dec_mcf, Oil_Total_bbl, Oil_Jan_bbl, Oil_Feb_bbl, Oil_Mar_bbl, Oil_Apr_bbl, Oil_May_bbl, Oil_Jun_bbl, Oil_Jul_bbl, Oil_Aug_bbl, Oil_Sep_bbl, Oil_Oct_bbl, Oil_Nov_bbl, Oil_Dec_bbl, Condensate_Total_bbl, Condensate_Jan_bbl, Condensate_Feb_bbl, Condensate_Mar_bbl, Condensate_Apr_bbl, Condensate_May_bbl, Condensate_Jun_bbl, Condensate_Jul_bbl, Condensate_Aug_bbl, Condensate_Sep_bbl, Condensate_Oct_bbl, Condensate_Nov_bbl, Condensate_Dec_bbl, NGL_Total_bbl, NGL_Jan_bbl, NGL_Feb_bbl, NGL_Mar_bbl, NGL_Apr_bbl, NGL_May_bbl, NGL_Jun_bbl, NGL_Jul_bbl, NGL_Aug_bbl, NGL_Sep_bbl, NGL_Oct_bbl, NGL_Nov_bbl, NGL_Dec_bbl, Water_Total_bbl, Water_Jan_bbl, Water_Feb_bbl, Water_Mar_bbl, Water_Apr_bbl, Water_May_bbl, Water_Jun_bbl, Water_Jul_bbl, Water_Aug_bbl, Water_Sep_bbl, Water_Oct_bbl, Water_Nov_bbl, Water_Dec_bbl, Reported_API_Number, Sources)
	  (SELECT DISTINCT ISNULL(WellID,0), ISNULL(API_14,'00000000000000'), '42', [Period], Gas_Total_mcf, Gas_Jan_mcf, Gas_Feb_mcf, Gas_Mar_mcf, Gas_Apr_mcf, Gas_May_mcf, Gas_Jun_mcf, Gas_Jul_mcf, Gas_Aug_mcf, Gas_Sep_mcf, Gas_Oct_mcf, Gas_Nov_mcf, Gas_Dec_mcf, Oil_Total_bbl, Oil_Jan_bbl, Oil_Feb_bbl, Oil_Mar_bbl, Oil_Apr_bbl, Oil_May_bbl, Oil_Jun_bbl, Oil_Jul_bbl, Oil_Aug_bbl, Oil_Sep_bbl, Oil_Oct_bbl, Oil_Nov_bbl, Oil_Dec_bbl, Condensate_Total_bbl, Condensate_Jan_bbl, Condensate_Feb_bbl, Condensate_Mar_bbl, Condensate_Apr_bbl, Condensate_May_bbl, Condensate_Jun_bbl, Condensate_Jul_bbl, Condensate_Aug_bbl, Condensate_Sep_bbl, Condensate_Oct_bbl, Condensate_Nov_bbl, Condensate_Dec_bbl, NGL_Total_bbl, NGL_Jan_bbl, NGL_Feb_bbl, NGL_Mar_bbl, NGL_Apr_bbl, NGL_May_bbl, NGL_Jun_bbl, NGL_Jul_bbl, NGL_Aug_bbl, NGL_Sep_bbl, NGL_Oct_bbl, NGL_Nov_bbl, NGL_Dec_bbl, Water_Total_bbl, Water_Jan_bbl, Water_Feb_bbl, Water_Mar_bbl, Water_Apr_bbl, Water_May_bbl, Water_Jun_bbl, Water_Jul_bbl, Water_Aug_bbl, Water_Sep_bbl, Water_Oct_bbl, Water_Nov_bbl, Water_Dec_bbl, API_Number, [Source]
	   FROM US_Wells.dbo.tblUSWell_Production WHERE PkgId=1000002);

	UPDATE US_Wells.dbo.tblUSWell_Production_Forecast
	  SET Gas_Total_mcf=ISNULL(Gas_Total_mcf,0),
		  Oil_Total_bbl=ISNULL(Oil_Total_bbl,0),
		  Condensate_Total_bbl=ISNULL(Condensate_Total_bbl,0),
		  NGL_Total_bbl=ISNULL(NGL_Total_bbl,0),
		  Water_Total_bbl=ISNULL(Water_Total_bbl,0),
		  Gas_Jan_mcf=ISNULL(Gas_Jan_mcf,0),
		  Gas_Feb_mcf=ISNULL(Gas_Feb_mcf,0),
		  Gas_Mar_mcf=ISNULL(Gas_Mar_mcf,0),
		  Gas_Apr_mcf=ISNULL(Gas_Apr_mcf,0),
		  Gas_May_mcf=ISNULL(Gas_May_mcf,0),
		  Gas_Jun_mcf=ISNULL(Gas_Jun_mcf,0),
		  Gas_Jul_mcf=ISNULL(Gas_Jul_mcf,0),
		  Gas_Aug_mcf=ISNULL(Gas_Aug_mcf,0),
		  Gas_Sep_mcf=ISNULL(Gas_Sep_mcf,0),
		  Gas_Oct_mcf=ISNULL(Gas_Oct_mcf,0),
		  Gas_Nov_mcf=ISNULL(Gas_Nov_mcf,0),
		  Gas_Dec_mcf=ISNULL(Gas_Dec_mcf,0),
		  Oil_Jan_bbl=ISNULL(Oil_Jan_bbl,0),
		  Oil_Feb_bbl=ISNULL(Oil_Feb_bbl,0),
		  Oil_Mar_bbl=ISNULL(Oil_Mar_bbl,0),
		  Oil_Apr_bbl=ISNULL(Oil_Apr_bbl,0),
		  Oil_May_bbl=ISNULL(Oil_May_bbl,0),
		  Oil_Jun_bbl=ISNULL(Oil_Jun_bbl,0),
		  Oil_Jul_bbl=ISNULL(Oil_Jul_bbl,0),
		  Oil_Aug_bbl=ISNULL(Oil_Aug_bbl,0),
		  Oil_Sep_bbl=ISNULL(Oil_Sep_bbl,0),
		  Oil_Oct_bbl=ISNULL(Oil_Oct_bbl,0),
		  Oil_Nov_bbl=ISNULL(Oil_Nov_bbl,0),
		  Oil_Dec_bbl=ISNULL(Oil_Dec_bbl,0),
		  Condensate_Jan_bbl=ISNULL(Condensate_Jan_bbl,0),
		  Condensate_Feb_bbl=ISNULL(Condensate_Feb_bbl,0),
		  Condensate_Mar_bbl=ISNULL(Condensate_Mar_bbl,0),
		  Condensate_Apr_bbl=ISNULL(Condensate_Apr_bbl,0),
		  Condensate_May_bbl=ISNULL(Condensate_May_bbl,0),
		  Condensate_Jun_bbl=ISNULL(Condensate_Jun_bbl,0),
		  Condensate_Jul_bbl=ISNULL(Condensate_Jul_bbl,0),
		  Condensate_Aug_bbl=ISNULL(Condensate_Aug_bbl,0),
		  Condensate_Sep_bbl=ISNULL(Condensate_Sep_bbl,0),
		  Condensate_Oct_bbl=ISNULL(Condensate_Oct_bbl,0),
		  Condensate_Nov_bbl=ISNULL(Condensate_Nov_bbl,0),
		  Condensate_Dec_bbl=ISNULL(Condensate_Dec_bbl,0),
		  NGL_Jan_bbl=ISNULL(NGL_Jan_bbl,0),
		  NGL_Feb_bbl=ISNULL(NGL_Feb_bbl,0),
		  NGL_Mar_bbl=ISNULL(NGL_Mar_bbl,0),
		  NGL_Apr_bbl=ISNULL(NGL_Apr_bbl,0),
		  NGL_May_bbl=ISNULL(NGL_May_bbl,0),
		  NGL_Jun_bbl=ISNULL(NGL_Jun_bbl,0),
		  NGL_Jul_bbl=ISNULL(NGL_Jul_bbl,0),
		  NGL_Aug_bbl=ISNULL(NGL_Aug_bbl,0),
		  NGL_Sep_bbl=ISNULL(NGL_Sep_bbl,0),
		  NGL_Oct_bbl=ISNULL(NGL_Oct_bbl,0),
		  NGL_Nov_bbl=ISNULL(NGL_Nov_bbl,0),
		  NGL_Dec_bbl=ISNULL(NGL_Dec_bbl,0),
		  Water_Jan_bbl=ISNULL(Water_Jan_bbl,0),
		  Water_Feb_bbl=ISNULL(Water_Feb_bbl,0),
		  Water_Mar_bbl=ISNULL(Water_Mar_bbl,0),
		  Water_Apr_bbl=ISNULL(Water_Apr_bbl,0),
		  Water_May_bbl=ISNULL(Water_May_bbl,0),
		  Water_Jun_bbl=ISNULL(Water_Jun_bbl,0),
		  Water_Jul_bbl=ISNULL(Water_Jul_bbl,0),
		  Water_Aug_bbl=ISNULL(Water_Aug_bbl,0),
		  Water_Sep_bbl=ISNULL(Water_Sep_bbl,0),
		  Water_Oct_bbl=ISNULL(Water_Oct_bbl,0),
		  Water_Nov_bbl=ISNULL(Water_Nov_bbl,0),
		  Water_Dec_bbl=ISNULL(Water_Dec_bbl,0)
	  WHERE StateID='42';

	UPDATE US_Wells.dbo.tblUSWell_Production_Forecast
	  SET Gas_TOTAL_mcf=ROUND(ISNULL(Gas_Jan_mcf,0) + ISNULL(Gas_Feb_mcf,0) + ISNULL(Gas_Mar_mcf,0) + ISNULL(Gas_Apr_mcf,0) + ISNULL(Gas_May_mcf,0) + ISNULL(Gas_Jun_mcf,0) + ISNULL(Gas_Jul_mcf,0) + ISNULL(Gas_Aug_mcf,0) + ISNULL(Gas_Sep_mcf,0) + ISNULL(Gas_Oct_mcf,0) + ISNULL(Gas_Nov_mcf,0) + ISNULL(Gas_Dec_mcf,0),2),
		  Oil_TOTAL_bbl=ROUND(ISNULL(Oil_Jan_bbl,0) + ISNULL(Oil_Feb_bbl,0) + ISNULL(Oil_Mar_bbl,0) + ISNULL(Oil_Apr_bbl,0) + ISNULL(Oil_May_bbl,0) + ISNULL(Oil_Jun_bbl,0) + ISNULL(Oil_Jul_bbl,0) + ISNULL(Oil_Aug_bbl,0) + ISNULL(Oil_Sep_bbl,0) + ISNULL(Oil_Oct_bbl,0) + ISNULL(Oil_Nov_bbl,0) + ISNULL(Oil_Dec_bbl,0),2),
		  Water_TOTAL_bbl=ROUND(ISNULL(Water_Jan_bbl,0) + ISNULL(Water_Feb_bbl,0) + ISNULL(Water_Mar_bbl,0) + ISNULL(Water_Apr_bbl,0) + ISNULL(Water_May_bbl,0) + ISNULL(Water_Jun_bbl,0) + ISNULL(Water_Jul_bbl,0) + ISNULL(Water_Aug_bbl,0) + ISNULL(Water_Sep_bbl,0) + ISNULL(Water_Oct_bbl,0) + ISNULL(Water_Nov_bbl,0),0) + ISNULL(Water_Dec_bbl,2),
		  NGL_TOTAL_bbl=ROUND(ISNULL(NGL_Jan_bbl,0) + ISNULL(NGL_Feb_bbl,0) + ISNULL(NGL_Mar_bbl,0) + ISNULL(NGL_Apr_bbl,0) + ISNULL(NGL_May_bbl,0) + ISNULL(NGL_Jun_bbl,0) + ISNULL(NGL_Jul_bbl,0) + ISNULL(NGL_Aug_bbl,0) + ISNULL(NGL_Sep_bbl,0) + ISNULL(NGL_Oct_bbl,0) + ISNULL(NGL_Nov_bbl,0) + ISNULL(NGL_Dec_bbl,0),2),
		  Condensate_TOTAL_bbl=ROUND(ISNULL(Condensate_Jan_bbl,0) + ISNULL(Condensate_Feb_bbl,0) + ISNULL(Condensate_Mar_bbl,0) + ISNULL(Condensate_Apr_bbl,0) + ISNULL(Condensate_May_bbl,0) + ISNULL(Condensate_Jun_bbl,0) + ISNULL(Condensate_Jul_bbl,0) + ISNULL(Condensate_Aug_bbl,0) + ISNULL(Condensate_Sep_bbl,0) + ISNULL(Condensate_Oct_bbl,0) + ISNULL(Condensate_Nov_bbl,0) + ISNULL(Condensate_Dec_bbl,0),2)
	  WHERE StateID='42';

	UPDATE US_Wells.dbo.tblUSWell_Parameters 
	  SET WellID=b.well_id
	  FROM US_Wells.dbo.tblUSWell_Parameters a, US_Wells_Texas.dbo.tx_well_details b
	  WHERE a.API_Number=b.tx_well_id 
	  AND ISNULL(b.well_id,0)!=0;

	UPDATE tx_well_details SET process_code=0;

	UPDATE tx_well_details SET process_code=1
	  FROM tx_well_details a, US_Wells.dbo.tblUSWell_Parameters b
	  WHERE a.tx_well_id=b.API_Number;

	UPDATE tx_well_details SET process_code=2
	  FROM tx_well_details a, US_Wells.dbo.tblUSWell_Production b
	  WHERE a.tx_well_id=b.API_Number AND a.process_code=0;

	INSERT INTO US_Wells.dbo.tblUSWell_Parameters (WellID,API_Number,StateID,State_Name,Well_Direction,Operator,Commodity,Resource_Play,First_Production_Date,True_Vertical_Depth_ft,Lateral_Length_ft,Well_Status,State_Well_Direction,Forecast_Well)
	 (SELECT DISTINCT well_id,TX_Well_ID,'42','Texas',Well_Direction,Operator,Commodity,Resource_Play,First_Production_Date,True_Vertical_Depth,Lateral_Length,Well_Status,Well_Direction,9
	  FROM tx_well_details WHERE process_code=2);

	UPDATE US_Wells.dbo.tblUSWell_Parameters SET commodity='GAS' WHERE commodity='G';
	UPDATE US_Wells.dbo.tblUSWell_Parameters SET commodity='OIL' WHERE commodity='O';

	UPDATE US_Wells.dbo.tblUSWell_Parameters SET County_Code=SUBSTRING(API_Number,3,3),Oil_Decline_Rate_Type='avg',Gas_Decline_Rate_Type='avg',Cond_Decline_Rate_Type='avg',NGL_Decline_Rate_Type='avg',Capex_Tangible_Split_pct=0.67 WHERE Forecast_Well=9;
	UPDATE US_Wells.dbo.tblUSWell_Parameters SET Resource_Play=NULL WHERE LEN(Resource_Play)=0;

	UPDATE US_Wells.dbo.tblUSWell_Parameters SET Forecast_Well=30
	  FROM US_Wells.dbo.tblUSWell_Parameters a, US_Wells.dbo.tblUSWell_Production b
	  WHERE a.API_Number=b.API_Number AND a.State_Name='Texas' AND a.commodity='OIL' AND a.Forecast_Well!=9;
	
	UPDATE US_Wells.dbo.tblUSWell_Parameters SET Forecast_Well=39
	  FROM US_Wells.dbo.tblUSWell_Parameters a, US_Wells.dbo.tblUSWell_Production b
	  WHERE a.API_Number=b.API_Number AND a.State_Name='Texas' AND a.commodity='OIL' AND a.Forecast_Well=9;
	"""
	if debug: print sql_update

	curr.execute(sql_update)
	gd.commit(curr)

	curr.close()
	conn.close()

# -----------------------------------------------------------------------------------------------------------------------------


def main(prod=False, get_prod=False, conf_prod=False, clear_prod=False, update_prod=False,
         api_dbf=False, api_archive=False, get_api_data=False, api_macro=False, import_api=False, update_api=False,
         schedule=False, sched_extract=False, sched_update=False,
         wellbore=False, conf_wb=False, import_wb=False, update_wb=False,
         completion=False, unzip_comp=False, store_comp=False, parse_comp=False, update_comp=False,
         permit=False, permit_extract=False, permit_update=False,
         details=False, details_data=False, details_id=False, details_update=False,
         engine_gas_prod=False, engine_oil_prod=False,
         debug=False):
	if prod:
		print 'start prod:', gd.get_datetime()
		process_production_data(retrieve=get_prod, configure=conf_prod, clear=clear_prod, update=update_prod)
		print 'end prod:', gd.get_datetime()
	if api_dbf:
		# 45 minutes
		print 'start api:', gd.get_datetime()
		process_well_api_data(archive=api_archive, retrieve=get_api_data, macro=api_macro, import_csv=import_api,
		                      update=update_api)
		print 'end api:', gd.get_datetime()
	if wellbore:
		# 40 minutes
		print 'start wellbore:', gd.get_datetime()
		process_wellbore_data(configure=conf_wb, import_csv=import_wb, update=update_wb)
		print 'end wellbore:', gd.get_datetime()
	if schedule:
		# 8 minutes
		print 'start sched:', gd.get_datetime()
		process_oil_field_schedule_data(extract=sched_extract, update=sched_update)
		print 'end sched:', gd.get_datetime()
	if completion:
		# 3 minutes
		print 'start comp:', gd.get_datetime()
		process_completion_data(unzip_data=unzip_comp, store_records=store_comp, parse_data=parse_comp,
		                        update_tables=update_comp, debug=debug)
		print 'end comp:', gd.get_datetime()
	if permit:
		# 2 minutes
		print 'start permit:', gd.get_datetime()
		process_permit_data(extract=permit_extract, update=permit_update)
		print 'end permit:', gd.get_datetime()
	if details:
		# 5 hours
		print 'start details:', gd.get_datetime()
		process_well_details_data(well_data=details_data, tx_well_id=details_id, well_details=details_update)
		print 'end details:', gd.get_datetime()
	if engine_gas_prod:
		print 'start gas engine prod:', gd.get_datetime()
		update_engine_gas_production(debug=debug)
		print 'end gas engine prod:', gd.get_datetime()
	if engine_oil_prod:
		print 'start oil engine prod:', gd.get_datetime()
		update_engine_oil_production(debug=debug)
		print 'end oil engine prod:', gd.get_datetime()


if __name__ == '__main__':
	MAIN_UPDATE = True
	OIL_ALLOCATION = False
	if MAIN_UPDATE:
		main(debug=False,
			 api_dbf=False, api_archive=False, get_api_data=True, api_macro=True, import_api=True, update_api=True,
			 prod=False, get_prod=False, conf_prod=False, clear_prod=False, update_prod=True,
			 completion=True, unzip_comp=True, store_comp=True, parse_comp=True, update_comp=True,
			 wellbore=False, conf_wb=True, import_wb=True, update_wb=True,
			 schedule=False, sched_extract=True, sched_update=True,
			 permit=False, permit_update=True, permit_extract=True,
			 details=False, details_data=True, details_id=True, details_update=True,
			 engine_gas_prod=False,
			 engine_oil_prod=False)
	if OIL_ALLOCATION:
		start_time = gd.get_datetime()
		tx_oil_allocation_update(update_oil_prod=False,
								 update_oil_field=False, update_lease_2=False,  # update_gaps=False,
								 create_allow=False, lease_to_well=False, update_allow=False,
								 update_oil_2=False,
								 calc_lease=False, create_lease=False, update_prev=False, update_lease=False,
								 update_well_dates=False,
								 update_prod_pct=False, split_well_pct=False, update_pct_main=False,
								 allocate=False,
								 update_pct_new=False, create_pct_final=False, update_lease_pct=False,
								 update_prod_pct_gaps=False,
								 update_hist_prod=True,
								 debug=False)
		end_time = gd.get_datetime()
		print 'Total time: {}'.format(gd.elapsed_time(start_time, end_time))
