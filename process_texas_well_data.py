from globaldata import *
import globaldata as gd
import urllib2
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium import webdriver
import os
import random
import shutil
from zipfile import ZipFile
import ftputil
from distutils.dir_util import copy_tree
from csv_sql_import import main as csv_import_main
import globaldata as gd
import codecs
import io
import ftputil
import urllib2, shutil
from time import sleep
import os
from globaldata import get_data

INPUT_FILE_DIR  = 'D:\\GlobalData\\Data\\web_scrape\\TX_web_data\\field_schedules\\'
OUTPUT_FILE_DIR = gd.DATA_DIR + 'web_scrape\\TX_Web_Data\\schedule_txts\\'
OIL_SCHED_DIR   = 'C:\\Texas_Well_Data\\tx_schedule_data\\process\\'

MONTH_NOS  = {
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
OUTPUT_DIR = 'D:\\GlobalData\\Data\\tx_data\\csv_files\\'
TX_FILE_DIR = gd.DATA_DIR + 'well_data\\'
HEX_FILE_DIR = TX_FILE_DIR + 'tx_gas_data_hex\\'
HEX_IN_FILE = 'tx_gas_data_{}.txt'
HEX_OUT_FILE = 'tx_gas_data_{}_converted.txt'
INPUT_FILE = HEX_FILE_DIR + 'tx_gas_data_{}_converted.txt'
HEADER_FILE = gd.DATA_DIR + 'tx_{}_header_data.txt'
OUPUT_FILE = TX_FILE_DIR + 'tx_gas_well_data_1_processed.txt'
IMPORT_CSV_DIR  = 'D:\\GlobalData\\Data\\import_csv\\'
EXPORT_CSV_DIR  = 'D:\\GlobalData\\Data\\export_csv\\'
RERUN_CSV_DIR   = 'D:\\GlobalData\\Data\\tx_permit_rerun\\'
TX_COMP_DIR     = gd.DATA_DIR + 'tx_data\\tx_completion_data\\'
TX_ZIP_OUT_DIR  = gd.DATA_DIR + 'tx_data\\tx_completion_data\\comp_data\\'
TX_ZIP_IN_DIR   = gd.DATA_DIR + 'tx_data\\tx_completion_data\\Texas Completion Data\\'
COMP_ZIP_DIR    = gd.DATA_DIR + 'tx_data\\tx_completion_zipfiles\\'
COMP_OUT_DIR    = gd.DATA_DIR + 'tx_data\\tx_completion_files\\'
EWA_FILE_DIR    = gd.DATA_DIR + 'tx_data\\tx_ewa_files\\'
EWA_DATA_DIR    = gd.DATA_DIR + 'tx_data\\tx_ewa_data\\'

PROCESS_CODE    = 1

PROD_MONTH_COLS = {
    '01': ('oil_jan_bbl', 'csgd_jan_mcf'),
    '02': ('oil_feb_bbl', 'csgd_feb_mcf'),
    '03': ('oil_mar_bbl', 'csgd_mar_mcf'),
    '04': ('oil_apr_bbl', 'csgd_apr_mcf'),
    '05': ('oil_may_bbl', 'csgd_may_mcf'),
    '06': ('oil_jun_bbl', 'csgd_jun_mcf'),
    '07': ('oil_jul_bbl', 'csgd_jul_mcf'),
    '08': ('oil_aug_bbl', 'csgd_aug_mcf'),
    '09': ('oil_sep_bbl', 'csgd_sep_mcf'),
    '10': ('oil_oct_bbl', 'csgd_oct_mcf'),
    '11': ('oil_nov_bbl', 'csgd_nov_mcf'),
    '12': ('oil_dec_bbl', 'csgd_dec_mcf')
}

MONTH_NUMS      = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
PROD_DATES      = ['{}{}'.format(year_num, month_num) for year_num in range(1900, 2200) for month_num in MONTH_NUMS]

DISTRICT_DATA = {
    '1' : '01',
    '2' : '02',
    '3' : '03',
    '4' : '04',
    '5' : '05',
    '6' : '06',
    '6E': '07',
    '7B': '08',
    '7C': '09',
    '8' : '10',
    '8A': '11',
    '8B': '12',
    '9' : '13',
    '10': '14'
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

prod_col_str            = \
'''
oil_total_bbl, gas_total_mcf, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, gas_jan_mcf, gas_feb_mcf, gas_mar_mcf, gas_apr_mcf, gas_may_mcf, gas_jun_mcf, gas_jul_mcf, gas_aug_mcf, gas_sep_mcf, gas_oct_mcf, gas_nov_mcf, gas_dec_mcf
'''

MONTH_NAMES           = {
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

COMM_UNITS            = {
    "oil"       : "bbl",
    "gas"       : "mcf"
}


wellbore_nums = ['00','01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(wellbore_num) for wellbore_num in range(10,100)]
wellbore_nums = sorted(wellbore_nums)

WEBDRIVE_CONFIG = {
    'tx_prod': {
        'url'  : 'http://webapps2.rrc.texas.gov/EWA/wellboreQueryAction.do',
        'click': [
            ('xpath', "//select[@name='searchArgs.wellTypeArg']/option[text()='{}']", 0),
            ('xpath', "//select[@name='searchArgs.districtCodeArg']/option[text()='{}']", 0),
            ('xpath', "//input[@type='submit' and @value='Submit']", 2),
            ('xpath', "//select[@name='pager.pageSize']/option[text()='View All']", 2),
            ('xpath', "//input[@type='button' and @value='Download']", 1)
        ]
    }
}

TX_DATA = {
    'counties' : [
        'ATASCOSA',
        'AUSTIN',
        'BAILEY',
        'BANDERA',
        'BASTROP',
        'BAYLOR',
        'BEE',
        'BELL',
        'BEXAR',
        'BLANCO',
        'BORDEN',
        'BOSQUE',
        'BOWIE',
        'BRAZORIA',
        'BRAZOS',
        'BREWSTER',
        'BRISCOE',
        'BROOKS',
        'BROWN',
        'BURLESON',
        'BURNET',
        'CALDWELL',
        'CALHOUN',
        'CALLAHAN',
        'CAMERON',
        'CAMP',
        'CARSON',
        'CASS',
        'CASTRO',
        'CHAMBERS',
        'CHEROKEE',
        'CHILDRESS',
        'CLAY',
        'COCHRAN',
        'COKE',
        'COLEMAN',
        'COLLIN',
        'COLLINGSWORTH',
        'COLORADO',
        'COMAL',
        'COMANCHE',
        'CONCHO',
        'COOKE',
        'CORYELL',
        'COTTLE',
        'CRANE',
        'CROCKETT',
        'CROSBY',
        'CULBERSON',
        'DALLAM',
        'DALLAS',
        'DAWSON',
        'DEAF SMITH',
        'DELTA',
        'DENTON',
        'DE WITT',
        'DICKENS',
        'DIMMIT',
        'DONLEY',
        'DUVAL',
        'EASTLAND',
        'ECTOR',
        'EDWARDS',
        'ELLIS',
        'EL PASO',
        'ERATH',
        'FALLS',
        'FANNIN',
        'FAYETTE',
        'FISHER',
        'FLOYD',
        'FOARD',
        'FORT BEND',
        'FRANKLIN',
        'FREESTONE',
        'FRIO',
        'GAINES',
        'GALVESTON',
        'GARZA',
        'GILLESPIE',
        'GLASSCOCK',
        'GOLIAD',
        'GONZALES',
        'GRAY',
        'GRAYSON',
        'GREGG',
        'GRIMES',
        'GUADALUPE',
        'HALE',
        'HALL',
        'HAMILTON',
        'HANSFORD',
        'HARDEMAN',
        'HARDIN',
        'HARRIS',
        'HARRISON',
        'HARTLEY',
        'HASKELL',
        'HAYS',
        'HEMPHILL',
        'HENDERSON',
        'HIDALGO',
        'HILL',
        'HOCKLEY',
        'HOOD',
        'HOPKINS',
        'HOUSTON',
        'HOWARD',
        'HUDSPETH',
        'HUNT',
        'HUTCHINSON',
        'IRION',
        'JACK',
        'JACKSON',
        'JASPER',
        'JEFF DAVIS',
        'JEFFERSON',
        'JIM HOGG',
        'JIM WELLS',
        'JOHNSON',
        'JONES',
        'KARNES',
        'KAUFMAN',
        'KENDALL',
        'KENEDY',
        'KENT',
        'KERR',
        'KIMBLE',
        'KING',
        'KINNEY',
        'KLEBERG',
        'KNOX',
        'LAMAR',
        'LAMB',
        'LAMPASAS',
        'LA SALLE',
        'LAVACA',
        'LEE',
        'LEON',
        'LIBERTY',
        'LIMESTONE',
        'LIPSCOMB',
        'LIVE OAK',
        'LLANO',
        'LOVING',
        'LUBBOCK',
        'LYNN',
        'MCCULLOCH',
        'MCLENNAN',
        'MCMULLEN',
        'MADISON',
        'MARION',
        'MARTIN',
        'MASON',
        'MATAGORDA',
        'MAVERICK',
        'MEDINA',
        'MENARD',
        'MIDLAND',
        'MILAM',
        'MILLS',
        'MITCHELL',
        'MONTAGUE',
        'MONTGOMERY',
        'MOORE',
        'MORRIS',
        'MOTLEY',
        'NACOGDOCHES',
        'NAVARRO',
        'NEWTON',
        'NOLAN',
        'NUECES',
        'OCHILTREE',
        'OLDHAM',
        'ORANGE',
        'PALO PINTO',
        'PANOLA',
        'PARKER',
        'PARMER',
        'PECOS',
        'POLK',
        'POTTER',
        'PRESIDIO',
        'RAINS',
        'RANDALL',
        'REAGAN',
        'REAL',
        'RED RIVER',
        'REEVES',
        'REFUGIO',
        'ROBERTS',
        'ROBERTSON',
        'ROCKWALL',
        'RUNNELS',
        'RUSK',
        'SABINE',
        'SAN AUGUSTINE',
        'SAN JACINTO',
        'SAN PATRICIO',
        'SAN SABA',
        'SCHLEICHER',
        'SCURRY',
        'SHACKELFORD',
        'SHELBY',
        'SHERMAN',
        'SMITH',
        'SOMERVELL',
        'STARR',
        'STEPHENS',
        'STERLING',
        'STONEWALL',
        'SUTTON',
        'SWISHER',
        'TARRANT',
        'TAYLOR',
        'TERRELL',
        'TERRY',
        'THROCKMORTON',
        'TITUS',
        'TOM GREEN',
        'TRAVIS',
        'TRINITY',
        'TYLER',
        'UPSHUR',
        'UPTON',
        'UVALDE',
        'VAL VERDE',
        'VAN ZANDT',
        'VICTORIA',
        'WALKER',
        'WALLER',
        'WARD',
        'WASHINGTON',
        'WEBB',
        'WHARTON',
        'WHEELER',
        'WICHITA',
        'WILBARGER',
        'WILLACY',
        'WILLIAMSON',
        'WILSON',
        'WINKLER',
        'WISE',
        'WOOD',
        'YOAKUM',
        'YOUNG',
        'ZAPATA',
        'ZAVALA',
        'S PADRE IS-SB',
        'N PADRE IS-SB',
        'MUSTANG IS-SB',
        'MATGRDA IS-SB',
        'BRAZOS-SB',
        'GALVESTON-SB',
        'HIGH IS-SB',
        'S PADRE IS-LB',
        'N PADRE IS-LB',
        'MUSTANG IS-LB',
        'MATGRDA IS-LB',
        'BRAZOS-LB',
        'BRAZOS-S',
        'GALVESTON-LB',
        'GALVESTON-S',
        'HIGH IS-LB',
        'HIGH IS-S',
        'HIGH IS-E',
        '"HIGH IS-E,S"',
        'MUSTANG IS-E',
        'N PADRE IS-E',
        'S PADRE IS-E',
        'SABINE PASS'
    ],
    'districts': [
        '01',
        '02',
        '03',
        '04',
        '05',
        '06',
        '6E',
        '7B',
        '7C',
        '08',
        '8A',
        '09',
        '10'
    ],
    'typewells': [
        'ABANDONED',
        'BRINE MINING',
        'DOMESTIC USE WELL',
        'GAS STRG-INJECTION',
        'GAS STRG-SALT FORMATION',
        'GEOTHERMAL WELL',
        'GAS STRG-WITHDRAWAL',
        'HISTORY',
        'INJECTION',
        'LPG STORAGE',
        'LEASE-USE-WELL',
        'NO PRODUCTION',
        'OBSERVATION',
        'OTHER TYPE SERVICE',
        'PROD FACTOR WELL',
        'PRODUCING',
        'PARTIAL PLUG',
        'SWR-10-WELL',
        'SEALED',
        'SHUT IN',
        'SHUT IN-MULTI-COMPL',
        'TEMP ABANDONED',
        'TRAINING',
        'WATER SUPPLY',
        'NOT ELIGIBLE FOR ALLOWABLE'
    ]
}

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

FILE_NUMS = [
    '001',
    '002',
    '003',
    '004',
    '005',
    '006',
    '007',
    '008',
    '009',
    '010',
    '011',
    '012',
    '013',
    '014',
    '015',
    '016',
    '017',
    '018',
    '019',
    '020',
    '021',
    '022',
    '023',
    '024',
    '025',
    '026',
    '027',
    '028',
    '029',
    '030',
    '031',
    '032',
    '033',
    '034',
    '035',
    '036',
    '037',
    '038',
    '039',
    '040',
    '041',
    '042',
    '043',
    '044',
    '045',
    '046',
    '047',
    '048',
    '049',
    '050',
    '051',
    '052',
    '053',
    '054',
    '055',
    '056',
    '057',
    '058',
    '059',
    '060',
    '061',
    '062',
    '063',
    '064',
    '065',
    '066',
    '067',
    '068',
    '069',
    '070',
    '071',
    '072',
    '073',
    '074',
    '075',
    '076',
    '077',
    '078',
    '079',
    '080',
    '081',
    '082',
    '083',
    '084',
    '085',
    '086',
    '087',
    '088',
    '089',
    '090',
    '091',
    '092',
    '093',
    '094',
    '095',
    '096',
    '097',
    '098',
    '099',
    '100',
    '101',
    '102',
    '103',
    '104',
    '105',
    '106',
    '107',
    '108',
    '109',
    '110',
    '111',
    '112',
    '113',
    '114',
    '115',
    '116',
    '117',
    '118',
    '119',
    '120',
    '121',
    '122',
    '123',
    '124',
    '125',
    '126',
    '127',
    '128',
    '129',
    '130',
    '131',
    '132',
    '133',
    '134',
    '135',
    '136',
    '137',
    '138',
    '139',
    '140',
    '141',
    '142',
    '143',
    '144',
    '145',
    '146',
    '147',
    '148',
    '149',
    '150',
    '151',
    '152',
    '153',
    '154',
    '155',
    '156',
    '157',
    '158',
    '159',
    '160',
    '161',
    '162'
]

tx_table_data = {
    'tx_gas_altf'  : [
        (2, 'record_key', 0),
        (1, 'transfer_code', 0),
        (9, 'transfer_amount', 0),
        (19, 'data_filler_4', 0)
    ],
    'tx_gas_c1'    : [
        (2, 'record_key', 0),
        (6, 'gc1_key', 0),
        (1, 'gc1_number_of_eff_cycles', 0),
        (4, 'gc1_test_year', 0),
        (2, 'gc1_test_month', 0),
        (2, 'gc1_test_day', 0),
        (1, 'gc1_type_test_flag', 0),
        (32,'gc1_other_remark', 0),
        (9, 'gc1_subst_capability', 0),
        (9, 'data_filler_10', 0),
        (1, 'gc1_engineer_flag', 0),
        (32, 'gc1_certifier_name', 0),
        (9, 'data_filler_12', 0)
    ],
    'tx_gas_frmds' : [
        (2, 'record_key', 0),
        (20, 'forms_description', 0),
        (6, 'data_filler_3', 0)
    ],
    'tx_gas_frmlk' : [
        (2, 'record_key', 0),
        (4, 'form_lack_code', 0),
        (6, 'data_filler_3', 0)
    ],
    'tx_gas_g1'    : [
        (2, 'record_key', 0),
        (8, 'g1_key', 0),
        (4, 'g1_test_year', 0),
        (2, 'g1_test_month', 0),
        (2, 'g1_test_day', 0),
        (9, 'g1_potential', 0),
        (5, 'g1_slope', 3),
        (5, 'g1_siwh', 0),
        (5, 'g1_bhp', 0),
        (5, 'g1_gas_gravity', 3),
        (3, 'g1_cond_gravity', 1),
        (5, 'g1_gor', 0),
        (9, 'g1_test_gas', 0),
        (1, 'g1_admin_add_flag', 0),
        (6, 'data_filler_15', 0)
    ],
    'tx_gas_g10'   : [
        (2, 'record_key', 0),
        (4, 'g10_cycle_key', 0),
        (2, 'g10_day_key', 0),
        (4, 'g10_eff_year', 0),
        (2, 'g10_eff_month', 0),
        (2, 'g10_eff_day', 0),
        (4, 'g10_test_year', 0),
        (2, 'g10_test_month', 0),
        (2, 'g10_test_day', 0),
        (1, 'g10_type_test_flag', 0),
        (9, 'g10_deliverability', 0),
        (7, 'g10_daily_cond', 1),
        (7, 'g10_daily_water', 0),
        (5, 'g10_gas_gravity', 3),
        (3, 'g10_cond_gravity', 1),
        (5, 'g10_ratio', 0),
        (7, 'g10_siwh', 0),
        (5, 'g10_flow_press', 0),
        (9, 'g10_potential', 0),
        (5, 'g10_bhp', 0),
        (1, 'g10_cd_shutin', 0),
        (7, 'g10_whp_shutin_well', 0),
        (5, 'g10_rock_press', 0),
        (9, 'g10_cal_del_pote', 0),
        (4, 'g10_issue_year', 0),
        (2, 'g10_issue_month', 0),
        (2, 'g10_issue_day', 0),
        (4, 'g10_shutin_year', 0),
        (2, 'g10_shutin_month', 0),
        (1, 'g10_annual_cmgl_tst_flag', 0),
        (1, 'g10_survey_counted_flag', 0),
        (1, 'g10_filed_edi_flag', 0),
        (1, 'g10_2yr_survey_counted_flag', 0),
        (4, 'g10_whp_test_year', 0),
        (2, 'g10_whp_test_month', 0),
        (2, 'g10_whp_test_day', 0),
        (2, 'data_filler_37', 0)
    ],
    'tx_gas_prval' : [
        (2, 'record_key', 0),
        (4, 'allow_eff_year_prev', 0),
        (2, 'allow_eff_month_prev', 0),
        (2, 'allow_eff_day_prev', 0),
        (4, 'allow_iss_year_prev', 0),
        (2, 'allow_iss_month_prev', 0),
        (2, 'allow_iss_day_prev', 0),
        (9, 'allow_cycle_amt_prev', 0),
        (9, 'allow_daily_amt_prev', 0),
        (2, 'allow_code_prev', 0),
        (9, 'top_schedule_allow_prev', 0),
        (8, 'word_allow_prev', 0),
        (9, 'spec_allow_daily_prev', 0),
        (1, 'special_allow_code_prev', 0),
        (9, 'liquid_allow_prev', 0),
        (1, 'liquid_allow_code_prev', 0),
        (9, '49b_daily_rate_prev', 0),
        (5, 'data_filler_18', 0),
        (2, 'perm_exc_cycs_prev', 0),
        (7, 'data_filler_20', 0),
        (1, 'data_filler_21', 0),
        (9, 'cal_del_pote_prev', 0),
        (1, 'cal_del_pote_chng_flag', 0),
        (9, 'deliv_prev', 0),
        (1, 'deliv_chng_flag', 0),
        (5, 'bhp_prev', 0),
        (1, 'bhp_chng_flag', 0),
        (7, 'siwh_prev', 0),
        (1, 'siwh_chng_flag', 0),
        (5, 'rock_press_prev', 0),
        (1, 'rock_press_chng_flag', 0),
        (11, 'acres_prev', 4),
        (1, 'acres_chng_flag', 0),
        (7, 'acre_feet_prev', 1),
        (1, 'acre_feet_chng_flag', 0),
        (2, 'well_type_prev', 0),
        (33, 'allow_remarks_prev', 0),
        (1, '14b2_code_prev', 0),
        (4, 'deliv_ltr_eff_yr_prev', 0),
        (2, 'deliv_ltr_eff_mo_prev', 0),
        (2, 'deliv_ltr_eff_da_prev', 0),
        (4, 'test_year_prev', 0),
        (2, 'test_month_prev', 0),
        (2, 'test_day_prev', 0),
        (9, 'lease_percent_reserves_prev', 4),
        (36, 'data_filler_43', 0)
    ],
    'tx_gas_pvg10' : [
        (2, 'record_key', 0),
        (4, 'g10_cycle_key_prev', 0),
        (2, 'g10_day_key_prev', 0),
        (4, 'g10_eff_year_prev', 0),
        (2, 'g10_eff_month_prev', 0),
        (2, 'g10_eff_day_prev', 0),
        (4, 'g10_test_year_prev', 0),
        (2, 'g10_test_month_prev', 0),
        (2, 'g10_test_day_prev', 0),
        (1, 'g10_type_test_flag_prev', 0),
        (9, 'g10_deliverability_prev', 0),
        (7, 'g10_daily_cond_prev', 1),
        (7, 'g10_daily_water_prev', 0),
        (5, 'g10_gas_gravity_prev', 3),
        (3, 'g10_cond_gravity_prev', 1),
        (5, 'g10_ratio_prev', 0),
        (7, 'g10_siwh_prev', 0),
        (5, 'g10_flow_press_prev', 0),
        (9, 'g10_potential_prev', 0),
        (5, 'g10_bhp_prev', 0),
        (1, 'g10_cd_shutin_prev', 0),
        (7, 'g10_whp_shutin_well_prev', 0),
        (5, 'g10_rock_press_prev', 0),
        (9, 'g10_cal_del_pote_prev', 0),
        (4, 'g10_issue_year_prev', 0),
        (2, 'g10_issue_month_prev', 0),
        (2, 'g10_issue_day_prev', 0),
        (4, 'g10_shutin_year_prev', 0),
        (2, 'g10_shutin_month_prev', 0),
        (1, 'g10_ann_cmgl_tst_flag_prev', 0),
        (1, 'g10_survey_cnted_flag_prev', 0),
        (1, 'g10_filing_edi_prev_flag', 0),
        (1, 'g10_2yr_srvy_cnted_flag_prv', 0),
        (4, 'g10_whp_test_year_prev', 0),
        (2, 'g10_whp_test_month_prev', 0),
        (2, 'g10_whp_test_day_prev', 0),
        (2, 'data_filler_37', 0)
    ],
    'tx_gas_remark': [
        (2, 'record_key', 0),
        (3, 'remark_key', 0),
        (4, 'remark_year', 0),
        (2, 'remark_mon', 0),
        (2, 'remark_day', 0),
        (66, 'remark_text', 0),
        (1, 'well_print_on_ledger_flag', 0),
        (13, 'data_filler_8', 0)
    ],
    'tx_gas_root'  : [
        (2, 'record_key', 0),
        (8, 'root_key', 0),
        (1, 'on_off_sched_indicator', 0),
        (1, 'gas_or_oil', 0),
        (2, 'numeric_district', 0),
        (6, 'rrc_id', 0),
        (6, 'well_number', 0),
        (2, 'remove_from_sched_reasn', 0),
        (4, 'remove_from_sched_year', 0),
        (2, 'remove_from_sched_month', 0),
        (2, 'remove_from_sched_day', 0),
        (1, 'prob_prevent_allow_flag', 0),
        (1, 'bay_or_estuary', 0),
        (4, 'last_utilized_year', 0),
        (2, 'last_utilized_month', 0),
        (2, 'last_utilized_day', 0),
        (1, 'except_to_svy_test_flag', 0),
        (8, 'reclassed_well_pointer', 0),
        (2, 'survey_eff_century', 0),
        (2, 'survey_eff_year', 0),
        (2, 'survey_eff_month', 0),
        (25, 'data_filler_22', 0),
        (1, 'subject_to_14b2_flag', 0),
        (1, 'uic_violation_flag', 0),
        (1, 'legal_violation_flag', 0),
        (1, 'ext_for_state_plug_flag', 0),
        (1, 'cert_hb_1975_flag', 0),
        (2, 'cert_effective_cc', 0),
        (2, 'cert_effective_yy', 0),
        (2, 'cert_effective_mm', 0),
        (2, 'certification_ltr_cc', 0),
        (2, 'certification_ltr_yy', 0),
        (2, 'certification_ltr_mm', 0),
        (2, 'certification_ltr_dd', 0),
        (4, 'shut_in_ccyy', 0),
        (2, 'shut_in_mm', 0),
        (1, 'pend_removal_14b2_flag', 0),
        (116, 'data_filler_38', 0)
    ],
    'tx_gas_rptcy' : [
        (2, 'record_key', 0),
        (6, 'report_cycle_date', 0),
        (4, 'allow_effect_year', 0),
        (2, 'allow_effect_mon', 0),
        (2, 'allow_effect_day', 0),
        (4, 'allow_issue_year', 0),
        (2, 'allow_issue_mon', 0),
        (2, 'allow_issue_day', 0),
        (2, 'type_wells', 0),
        (9, 'allowable_cycle_amt', 0),
        (9, 'allowable_daily_amt', 0),
        (2, 'allowable_code', 0),
        (8, 'word_allowable', 0),
        (2, 'assigned_allow_code', 0),
        (9, 'assigned_allow', 0),
        (2, 'adjusted_allow_code', 0),
        (9, 'adjusted_allow_amt', 0),
        (9, 'administrative_allow', 0),
        (9, 'special_allow_daily_amt', 0),
        (1, 'special_allow_code', 0),
        (9, 'liquid_allow_amt', 0),
        (1, 'liquid_allow_code', 0),
        (9, '49b_daily_rate_amt', 0),
        (1, 'past_prod_changed_flag', 0),
        (1, 'high_daily_chngd_flag', 0),
        (1, 'is_a_pf_well_flag', 0),
        (1, 'k2_special_allow_flag', 0),
        (1, 'h15_violation_flag', 0),
        (2, 'perm_exc_cycs', 0),
        (11, 'acres', 4),
        (7, 'acre_feet', 1),
        (9, 'cal_del_pote', 0),
        (5, 'bhp', 0),
        (7, 'siwh', 0),
        (5, 'rock_press', 0),
        (4, 'deliv_letter_effect_yr', 0),
        (2, 'deliv_letter_effect_mo', 0),
        (2, 'deliv_letter_effect_da', 0),
        (9, 'deliverability', 0),
        (9, 'top_schedule_allowable', 0),
        (1, 'exc_to_g10_test_flag', 0),
        (33, 'allowable_remarks', 0),
        (1, 'auto_special_flag', 0),
        (1, 'no_supplement_flag', 0),
        (2, 'highest_daily_avg_cc', 0),
        (2, 'highest_daily_avg_year', 0),
        (2, 'highest_daily_avg_month', 0),
        (9, 'highest_daily_average', 0),
        (4, '12_month_peak_year', 0),
        (2, '12_month_peak_month', 0),
        (9, '12_month_peak', 0),
        (1, 'g10_bhp_except_flag', 0),
        (1, 'g10_sip_except_flag', 0),
        (1, 'dpt_code_except_flag', 0),
        (1, '14b2_code', 0),
        (4, '14b2_year', 0),
        (2, '14b2_month', 0),
        (3, 'bh_temperature', 0),
        (1, 'panhandle_comp_code', 0),
        (8, 'field_deliverability_share', 2),
        (1, 'admin_allow_flag', 0),
        (4, 'test_year', 0),
        (2, 'test_month', 0),
        (2, 'test_day', 0),
        (1, 'tmp_monthly_flag', 0),
        (1, 'recommenced_well_flag', 0),
        (1, 'permanent_gas_well_flag', 0),
        (7, 'data_filler_71', 0)
    ],
    'tx_gas_sb126' : [
        (2, 'record_key', 0),
        (1, 'sb126_cert_flag', 0),
        (2, 'sb126_cert_effect_cc', 0),
        (2, 'sb126_cert_effect_yy', 0),
        (2, 'sb126_cert_effect_mm', 0),
        (2, 'sb126_cert_ltr_cc', 0),
        (2, 'sb126_cert_ltr_yy', 0),
        (2, 'sb126_cert_ltr_mm', 0),
        (2, 'sb126_cert_ltr_dd', 0),
        (2, 'sb126_turnaround_ltr_cc', 0),
        (2, 'sb126_turnaround_ltr_yy', 0),
        (2, 'sb126_turnaround_ltr_mm', 0),
        (2, 'sb126_turnaround_ltr_dd', 0),
        (2, 'data_filler_14', 0)
    ],
    'tx_gas_seal'  : [
        (2, 'record_key', 0),
        (2, 'sealed_effective_century', 0),
        (2, 'sealed_effective_year', 0),
        (2, 'sealed_effective_month', 0),
        (2, 'sealed_reason', 0),
        (4, 'sealed_issue_year', 0),
        (2, 'sealed_issue_month', 0),
        (2, 'sealed_issue_day', 0),
        (2, 'sealed_issued_by', 0),
        (4, 'seal_removed_year', 0),
        (2, 'seal_removed_month', 0),
        (2, 'seal_removed_day', 0),
        (9, 'data_filler_13', 0)
    ],
    'tx_gas_uic'   : [
        (2, 'record_key', 0),
        (9, 'uic_control_number', 0),
        (1, 'h_10_required_flag', 0),
        (2, 'uic_status_century', 0),
        (2, 'uic_status_year', 0),
        (2, 'uic_status_month', 0),
        (2, 'uic_status_day', 0),
        (1, 'prev_h_10_status', 0),
        (1, 'roll_segment_flag', 0),
        (30, 'data_filler_6', 0)
    ],
    'tx_oil_altf'  : [
        (2, 'record_key', 0),
        (1, 'transfer_from_to', 0),
        (4, 'max_can_recv', 0),
        (4, 'total_actual_transfer', 0),
        (1, 'actual_transfer_type', 0),
        (6, 'data_filler_7', 0)
    ],
    'tx_oil_etds'  : [
        (2, 'record_key', 0),
        (8, 'e_tx_designated_wl_key', 0),
        (12, 'data_filler_3', 0)
    ],
    'tx_oil_etex'  : [
        (2, 'record_key', 0),
        (2, 'eswa_bonus_amt', 0),
        (2, 'tswa_bonus_amt', 0),
        (1, 'well_is_clat_flag', 0),
        (1, 'well_is_designated_flag', 0),
        (1, 'well_is_key_well_flag', 0),
        (50, 'well_clat_remarks', 0),
        (1, 'water_oil_ratio_exc_flg', 0),
        (1, 'water_well_shut_down', 0),
        (4, 'clat_removal_year', 0),
        (2, 'clat_removal_month', 0),
        (2, 'clat_removal_day', 0),
        (3, 'clat_plugged_out_amt', 0),
        (1, 'clat_plugged_out_code', 0),
        (4, 'data_filler_15', 0)
    ],
    'tx_oil_frmds' : [
        (2, 'record_key', 0),
        (20, 'forms_description', 0),
        (206, 'data_filler_3', 0)
    ],
    'tx_oil_frmlk' : [
        (2, 'record_key', 0),
        (4, 'form_lacking', 0),
        (222, 'data_filler_3', 0)
    ],
    'tx_oil_phbal' : [
        (2, 'record_key', 0),
        (1, 'well_lost_compl_2_8_flag', 0),
        (4, 'lost_compl_2_8_year', 0),
        (2, 'lost_compl_2_8_month', 0),
        (2, 'lost_compl_2_8_day', 0),
        (41, 'data_filler_6', 0)
    ],
    'tx_oil_phprod': [
        (2, 'record_key', 0),
        (9, 'casinghead_gas_amount', 0),
        (9, 'casinghead_gas_percent', 5),
        (50, 'data_filler_4', 0)
    ],
    'tx_oil_prval' : [
        (2, 'record_key', 0),
        (4, 'prev_effective_year', 0),
        (2, 'prev_effective_month', 0),
        (2, 'prev_effective_day', 0),
        (4, 'prev_issue_year', 0),
        (2, 'prev_issue_month', 0),
        (2, 'prev_issue_day', 0),
        (7, 'prev_work_potential', 1),
        (1, 'data_filler_9', 0),
        (5, 'prev_allow_amount', 0),
        (7, 'prev_gas_limit', 0),
        (5, 'prev_gas_oil_ratio', 0),
        (30, 'prev_remarks', 0),
        (2, 'allowable_codes_prv', 0),
        (1, 'allow_limited_cd_prv', 0),
        (2, 'type_wells_prv', 0),
        (7, 'well_monthly_allow_prv', 0),
        (9, 'csh_monthly_limit_prv', 0),
        (1, '14b2_code_prv', 0),
        (1, 'etex_pro_marg_prv', 0),
        (2, 'etex_oil_trns_prv', 0),
        (2, 'etex_gas_trns_prv', 0),
        (1, 'allocation_prv_flag', 0),
        (1, 'data_filler_23', 0)
    ],
    'tx_oil_pvtyp' : [
        (2, 'record_key', 0),
        (2, 'prev_well_type', 0),
        (224, 'data_filler_3', 0)
    ],
    'tx_oil_pvw10' : [
        (2, 'record_key', 0),
        (4, 'w10_cycle_key_prev', 0),
        (2, 'w10_day_key_prev', 0),
        (4, 'w10_eff_year_prev', 0),
        (2, 'w10_eff_month_prev', 0),
        (2, 'w10_eff_day_prev', 0),
        (1, 'w10_type_status_flag_prev', 0),
        (1, 'w10_producing_method_prev', 0),
        (20, 'w10_prd_meth_other_rpt_prev', 0),
        (4, 'w10_test_year_prev', 0),
        (2, 'w10_test_month_prev', 0),
        (2, 'w10_test_day_prev', 0),
        (7, 'w10_daily_oil_prev', 1),
        (5, 'w10_daily_water_prev', 0),
        (7, 'w10_daily_gas_prev', 0),
        (5, 'w10_gas_oil_ratio_prev', 0),
        (7, 'w10_siwh_pressure_prev', 0),
        (4, 'w10_siwh_year_prev', 0),
        (2, 'w10_siwh_month_prev', 0),
        (6, 'data_filler_20', 0),
        (2, 'w10_type_well_flag_prev', 0),
        (6, 'data_filler_22', 0),
        (4, 'w10_issue_year_prev', 0),
        (2, 'w10_issue_month_prev', 0),
        (2, 'w10_issue_day_prev', 0),
        (1, 'w10_filing_edi_prev_flag', 0),
        (9, 'data_filler_25', 0)
    ],
    'tx_oil_remark': [
        (2, 'record_key', 0),
        (3, 'remark_key', 0),
        (4, 'remark_year', 0),
        (2, 'remark_mon', 0),
        (2, 'remark_day', 0),
        (66, 'remark_text', 0),
        (1, 'well_print_on_ledger_flag', 0),
        (13, 'data_filler_8', 0)
    ],
    'tx_oil_root'  : [
        (2, 'record_key', 0),
        (8, 'root_key', 0),
        (1, 'on_off_sched_indicator', 0),
        (1, 'oil_or_gas', 0),
        (2, 'numeric_district', 0),
        (5, 'lease_number', 0),
        (1, 'unit_number', 0),
        (6, 'well_number', 0),
        (2, 'remove_from_sched_reasn', 0),
        (4, 'remove_from_sched_year', 0),
        (2, 'remove_from_sched_month', 0),
        (2, 'remove_from_sched_day', 0),
        (8, 'reclassed_well_pointer', 0),
        (1, 'prob_prevent_allow_flag', 0),
        (1, 'data_filler_15', 0),
        (5, 'reservoir', 0),
        (1, 'bay_or_estuary', 0),
        (4, 'data_filler_18', 0),
        (1, 'w10_exc_to_svy_flag', 0),
        (3, 'onshore_co_code', 0),
        (9, 'original_potential', 3),
        (3, 'data_filler_22', 0),
        (1, 'unit_no', 0),
        (5, 'unit_value', 3),
        (2, 'survey_eff_century', 0),
        (2, 'survey_eff_year', 0),
        (2, 'survey_eff_month', 0),
        (8, 'new_wb_connect_date', 0),
        (1, 'subject_to_14b2_flag', 0),
        (1, 'uic_violation_flag', 0),
        (1, 'legal_violation_flag', 0),
        (1, 'ext_for_state_plug_flag', 0),
        (1, 'cert_hb_1975_flag', 0),
        (2, 'cert_effective_cc', 0),
        (2, 'cert_effective_yy', 0),
        (2, 'cert_effective_mm', 0),
        (2, 'certification_ltr_cc', 0),
        (2, 'certification_ltr_yy', 0),
        (2, 'certification_ltr_mm', 0),
        (2, 'certification_ltr_dd', 0),
        (4, 'shut_in_ccyy', 0),
        (2, 'shut_in_mm', 0),
        (1, 'pend_removal_14b2_flag', 0),
        (116, 'data_filler_44', 0)
    ],
    'tx_oil_rptcy' : [
        (2, 'record_key', 0),
        (6, 'report_cycle_date', 0),
        (7, 'acres', 2),
        (5, 'acre_feet', 0),
        (5, 'net_acre_feet', 0),
        (5, 'bhp', 0),
        (7, 'working_potential', 1),
        (1, 'tolerance_acres_flag', 0),
        (4, 'effective_year', 0),
        (2, 'effective_month', 0),
        (2, 'effective_day', 0),
        (4, 'issue_year', 0),
        (2, 'issue_month', 0),
        (2, 'issue_day', 0),
        (5, 'allowable_amount', 0),
        (7, 'limit', 0),
        (5, 'oil_ratio', 0),
        (30, 'report_cycle_remark', 0),
        (7, 'original_oil_in_place', 0),
        (2, 'allowable_codes_rpt', 0),
        (1, 'allow_limited_cd_rpt', 0),
        (2, 'type_wells_rpt', 0),
        (3, 'sand_thickness', 0),
        (1, 'co_reg_depth_code', 0),
        (1, 'net_gor_code', 0),
        (5, 'net_gor', 0),
        (1, 'special_allow_code', 0),
        (5, 'special_allow_amt', 0),
        (1, '14b2_code', 0),
        (4, '14b2_year', 0),
        (2, '14b2_month', 0),
        (5, 'water_production', 0),
        (5, 'frozen_potential', 0),
        (1, 'producing_method_rpt', 0),
        (20, 'other_prod_method_rpt', 0),
        (7, 'well_monthly_allowable', 0),
        (5, 'lowest_perforation', 0),
        (1, 'data_filler_38', 0),
        (1, 'w10_exc_to_test_flag', 0),
        (4, 'test_year', 0),
        (2, 'test_month', 0),
        (2, 'test_day', 0),
        (1, 'retest_flag', 0),
        (5, '12_hour_potential', 0),
        (1, 'bonus_code', 0),
        (3, 'bonus_amount', 0),
        (1, 'eb_flag', 0),
        (1, 'allow_pote_gor_chg_flag', 0),
        (9, 'csh_monthly_limit', 0),
        (1, 'eb_change_month_flag', 0),
        (7, 'well_top', 0),
        (1, 'panhandle_comp_code', 0),
        (1, 'panhandle_sub_code', 0),
        (1, 'h15_violation_flag', 0),
        (1, 'allocation_flag', 0),
        (6, 'data_filler_56', 0)
    ],
    'tx_oil_sb126' : [
        (2, 'record_key', 0),
        (1, 'sb126_cert_flag', 0),
        (2, 'sb126_cert_effect_cc', 0),
        (2, 'sb126_cert_effect_yy', 0),
        (2, 'sb126_cert_effect_mm', 0),
        (2, 'sb126_cert_ltr_cc', 0),
        (2, 'sb126_cert_ltr_yy', 0),
        (2, 'sb126_cert_ltr_mm', 0),
        (2, 'sb126_cert_ltr_dd', 0),
        (2, 'sb126_turnaround_ltr_cc', 0),
        (2, 'sb126_turnaround_ltr_yy', 0),
        (2, 'sb126_turnaround_ltr_mm', 0),
        (2, 'sb126_turnaround_ltr_dd', 0),
        (2, 'data_filler_14', 0)
    ],
    'tx_oil_seal'  : [
        (2, 'record_key', 0),
        (2, 'sealed_effective_century', 0),
        (2, 'sealed_effective_year', 0),
        (2, 'sealed_effective_month', 0),
        (2, 'sealed_reason', 0),
        (4, 'sealed_issue_year', 0),
        (2, 'sealed_issue_month', 0),
        (2, 'sealed_issue_day', 0),
        (2, 'sealed_issued_by', 0),
        (4, 'seal_removed_year', 0),
        (2, 'seal_removed_month', 0),
        (2, 'seal_removed_day', 0),
        (9, 'data_filler_13', 0)
    ],
    'tx_oil_tfwl'  : [
        (2, 'record_key', 0),
        (8, 'well_transferred', 0),
        (1, 'transfer_type', 0),
        (4, 'oil_transfer', 0),
        (4, 'gas_transfer', 0),
        (13, 'data_filler_6', 0)
    ],
    'tx_oil_uic'   : [
        (2, 'record_key', 0),
        (9, 'uic_control_number', 0),
        (1, 'h_10_required_flag', 0),
        (2, 'uic_status_century', 0),
        (2, 'uic_status_year', 0),
        (2, 'uic_status_month', 0),
        (2, 'uic_status_day', 0),
        (1, 'prev_h_10_status', 0),
        (1, 'roll_segment_flag', 0),
        (30, 'data_filler_6', 0)
    ],
    'tx_oil_w10'   : [
        (2, 'record_key', 0),
        (4, 'w10_cycle_key', 0),
        (2, 'w10_day_key', 0),
        (4, 'w10_eff_year', 0),
        (2, 'w10_eff_month', 0),
        (2, 'w10_eff_day', 0),
        (1, 'w10_type_status_flag', 0),
        (1, 'w10_producing_method', 0),
        (20, 'w10_prod_meth_other_rpt', 0),
        (4, 'w10_test_year', 0),
        (2, 'w10_test_month', 0),
        (2, 'w10_test_day', 0),
        (7, 'w10_daily_oil', 1),
        (5, 'w10_daily_water', 0),
        (7, 'w10_daily_gas', 0),
        (5, 'w10_gas_oil_ratio', 0),
        (7, 'w10_siwh_pressure', 0),
        (4, 'w10_siwh_year', 0),
        (2, 'w10_siwh_month', 0),
        (6, 'data_filler_20', 0),
        (2, 'w10_type_well_flag', 0),
        (6, 'data_filler_22', 0),
        (4, 'w10_issue_year', 0),
        (2, 'w10_issue_month', 0),
        (2, 'w10_issue_day', 0),
        (1, 'w10_survey_counted_flag', 0),
        (1, 'w10_filed_edi_flag', 0),
        (1, 'w10_allocation_flag', 0),
        (1, 'w10_2yr_survey_counted_flag', 0),
        (6, 'data_filler_28', 0)
    ]
}

tx_wb_table_data = {
	'tx_wb_root': [
		(2,'record_key',0),
		(3,'api_cnty',0),
		(5,'api_unique',0),
		(2,'nxt_avail_suffix',0),
		(2,'nxt_avail_hole_chge_nbr',0),
		(2,'field_district',0),
		(3,'res_cnty_code',0),
		(1,'orig_compl_cc',0),
		(2,'orig_compl_cent',0),
		(2,'orig_compl_yy',0),
		(2,'orig_compl_mm',0),
		(2,'orig_compl_dd',0),
		(5,'total_depth',0),
		(5,'valid_fluid_level',0),
		(2,'cert_revoked_cc',0),
		(2,'cert_revoked_yy',0),
		(2,'cert_revoked_mm',0),
		(2,'cert_revoked_dd',0),
		(2,'certification_denial_cc',0),
		(2,'certification_denial_yy',0),
		(2,'certification_denial_mm',0),
		(2,'certification_denial_dd',0),
		(1,'denial_reason_flag',0),
		(1,'error_api_assign_code',0),
		(8,'refer_correct_api_nbr',0),
		(8,'dummy_api_number',0),
		(8,'date_dummy_replaced',0),
		(6,'newest_drl_pmt_nbr',0),
		(1,'cancel_expire_code',0),
		(1,'filler_1',0),
		(1,'except_13_a',0),
		(1,'fresh_water_flag',0),
		(1,'plug_flag',0),
		(8,'previous_api_nbr',0),
		(1,'completion_data_ind',0),
		(1,'hist_date_source_flag',0),
		(1,'filler_2',0),
		(2,'ex14b2_count',0),
		(1,'designation_hb_1975_flag',0),
		(2,'designation_effec_cc',0),
		(2,'designation_effec_yy',0),
		(2,'designation_effec_mm',0),
		(2,'designation_revised_cc',0),
		(2,'designation_revised_yy',0),
		(2,'designation_revised_mm',0),
		(2,'designation_letter_cc',0),
		(2,'designation_letter_yy',0),
		(2,'designation_letter_mm',0),
		(2,'designation_letter_dd',0),
		(2,'certification_effec_cc',0),
		(2,'certification_effec_yy',0),
		(2,'certification_effec_mm',0),
		(1,'water_land_code',0),
		(6,'total_bonded_depth',0),
		(7,'override_est_plug_cost',0),
		(4,'shut_in_year',0),
		(2,'shut_in_month',0),
		(6,'override_bonded_depth',0),
		(1,'subj_to_14b2_flag',0),
		(1,'pend_removal_14b2_flag',0),
		(1,'orphan_well_hold_flag',0),
		(1,'w3x_well_flag',0),
		(6,'filler_3',0),
		(80,'data_filler_end',0)
	],
	'tx_wb_compl': [
		(2,'record_key',0),
		(1,'oil_gas_code',0),
		(13,'oil_gas_key',0),
		(2,'gas_dist',0),
		(6,'gas_well_no',0),
		(1,'multi_well_rec_nbr',0),
		(2,'api_suffix',0),
		(18,'filler_4',0),
		(1,'active_inactive_code',0),
		(40,'filler_5',0),
		(1,'dwn_hole_commingle_code',0),
		(34,'filler_6',0),
		(1,'created_from_pi_flag',0),
		(7,'rule_37_nbr',0),
		(5,'filler_7',0),
		(5,'filler_8',0),
		(10,'filler_9',0),
		(4,'filler_10',0),
		(2,'filler_11',0),
		(1,'p_15',0),
		(1,'p_12',0),
		(8,'plug_date_pointer',0),
		(6,'filler_12',0),
		(76,'data_filler_end',0)
	],
	'tx_wb_date': [
		(2,'record_key',0),
		(8,'file_key',0),
		(8,'file_date',0),
		(8,'filler_13',0),
		(1,'except_rule_11',0),
		(1,'cement_affidavit',0),
		(1,'g_5',0),
		(1,'w_12',0),
		(1,'dir_survey',0),
		(8,'w2_g1_date',0),
		(2,'compl_century',0),
		(2,'compl_year',0),
		(2,'compl_month',0),
		(2,'compl_day',0),
		(8,'drl_compl_date',0),
		(5,'plugb_depth1',0),
		(5,'plugb_depth2',0),
		(6,'water_injection_nbr',0),
		(5,'salt_wtr_nbr',0),
		(8,'filler_14',0),
		(1,'remarks_ind',0),
		(4,'elevation',0),
		(2,'elevation_code',0),
		(8,'log_file_rba',0),
		(10,'docket_nbr',0),
		(1,'psa_well_flag',0),
		(1,'allocation_well_flag',0),
		(6,'filler_15',0),
		(130,'data_filler_end',0)
	],
	'tx_wb_rmks': [
		(2,'record_key',0),
		(3,'rmk_lne_cnt',0),
		(1,'rmk_type_code',0),
		(70,'remarks',0),
		(171,'data_filler_end',0)
	],
	'tx_wb_tube': [
		(2,'record_key',0),
		(3,'segment_counter',0),
		(2,'tubing_inches',0),
		(2,'fr_numerator',0),
		(2,'fr_denominator',0),
		(5,'depth_set',0),
		(5,'packer_set',0),
		(10,'filler_16',0),
		(16,'filler_17',0),
		(200,'data_filler_end',0)
	],
	'tx_wb_case': [
		(2,'record_key',0),
		(3,'casing_count',0),
		(2,'cas_inch',0),
		(2,'cas_frac_num',0),
		(2,'cas_frac_denom',0),
		(8,'cas_wt_table',0),
		(5,'casing_depth_set',0),
		(5,'mlti_stg_tool_dpth',0),
		(5,'amount_of_cement',0),
		(1,'cement_measurement',0),
		(2,'hole_inch',0),
		(2,'hole_frac_num',0),
		(2,'hole_frac_denom',0),
		(1,'filler_18',0),
		(7,'top_of_cement_casing',0),
		(5,'amount_casing_left',0),
		(50,'filler_19',0),
		(143,'data_filler_end',0)
	],
	'tx_wb_perf': [
		(2,'record_key',0),
		(3,'perf_count',0),
		(5,'from_perf',0),
		(5,'to_perf',0),
		(2,'open_hole_code',0),
		(10,'filler_20',0),
		(220,'data_filler_end',0)
	],
	'tx_wb_line': [
		(2,'record_key',0),
		(3,'line_count',0),
		(2,'lin_inch',0),
		(2,'lin_frac_num',0),
		(2,'lin_frac_denom',0),
		(5,'sacks_of_cement',0),
		(5,'top_of_liner',0),
		(5,'bottom_of_liner',0),
		(20,'filler_21',0),
		(201,'data_filler_end',0)
	],
	'tx_wb_form': [
		(2,'record_key',0),
		(3,'formation_cntr',0),
		(32,'formation_name',0),
		(5,'formation_depth',0),
		(5,'filler_22',0),
		(200,'data_filler_end',0)
	],
	'tx_wb_sqeze': [
		(2,'record_key',0),
		(3,'squeeze_cntr',0),
		(5,'squeeze_upper_depth',0),
		(5,'squeeze_lower_depth',0),
		(50,'squeeze_kind_amount',0),
		(7,'filler_23',0),
		(175,'data_filler_end',0)
	],
	'tx_wb_fresh': [
		(2,'record_key',0),
		(3,'fresh_water_cntr',0),
		(8,'twdb_date',0),
		(1,'surface_casing_deter_code',0),
		(4,'uqwp_from',0),
		(4,'uqwp_to',0),
		(10,'filler_24',0),
		(215,'data_filler_end',0)
	],
	'tx_wb_oldloc': [
		(2,'record_key',0),
		(32,'lease_name',0),
		(52,'sec_blk_survey_loc',0),
		(4,'well_loc_miles',0),
		(6,'well_loc_direction',0),
		(13,'well_loc_nearest_town',0),
		(28,'filler_25',0),
		(28,'dist_from_survey_lines',0),
		(28,'dist_direct_near_well',0),
		(28,'filler_26',0),
		(26,'data_filler_end',0)
	],
	'tx_wb_newloc': [
		(2,'record_key',0),
		(3,'loc_county',0),
		(6,'abstract',0),
		(55,'survey',0),
		(10,'block_number',0),
		(8,'section',0),
		(4,'alt_section',0),
		(6,'alt_abstract',0),
		(6,'feet_from_sur_sect_1',0),
		(13,'direc_from_sur_sect_1',0),
		(6,'feet_from_sur_sect_2',0),
		(13,'direc_from_sur_sect_2',0),
		(10,'wgs84_latitude',7),
		(10,'wgs84_longitude',7),
		(5,'filler_27',0),
		(2,'plane_zone',0),
		(10,'plane_coordinate_east',2),
		(10,'plane_coordinate_north',2),
		(1,'verification_flag',0),
		(1,'filler_28',0),
		(66,'data_filler_end',0)
	],
	'tx_wb_plug': [
		(2,'record_key',0),
		(8,'date_w3_filed',0),
		(8,'date_well_bore_plugged',0),
		(5,'plug_total_depth',0),
		(32,'plug_cement_comp',0),
		(1,'plug_mud_filled',0),
		(12,'plug_mud_applied',0),
		(3,'plug_mud_weight',0),
		(4,'filler_29',0),
		(8,'plug_dril_perm_date',0),
		(6,'plug_dril_perm_no',0),
		(8,'plug_dril_comp_date',0),
		(1,'plug_log_attached',0),
		(32,'plug_log_released_to',0),
		(1,'plug_type_log',0),
		(5,'plug_fresh_water_depth',0),
		(40,'plug_uwqp',0),
		(1,'plug_material_left',0),
		(1,'plug_oil_gas_code',0),
		(13,'plug_oil_gas_key',0),
		(2,'plug_gas_dist',0),
		(6,'plug_gas_well_no',0),
		(1,'plug_type_well',0),
		(1,'plug_multi_compl_flag',0),
		(1,'plug_cem_aff',0),
		(1,'plug_13a',0),
		(8,'plug_log_released_date',0),
		(8,'plug_log_file_rba',0),
		(7,'state_funded_plug_number',0),
		(21,'filler_30',0)
	],
	'tx_wb_plrmks': [
		(2,'record_key',0),
		(3,'plug_rmk_lne_cnt',0),
		(1,'plug_rmk_type_code',0),
		(70,'plug_remarks',0),
		(171,'data_filler_end',0)
	],
	'tx_wb_plrec': [
		(2,'record_key',0),
		(3,'plug_number',0),
		(5,'nbr_of_cement_sacks',0),
		(5,'meas_top_of_plug',0),
		(5,'bottom_tube_pipe_depth',0),
		(5,'plug_calc_top',0),
		(6,'plug_type_cement',0),
		(19,'filler_31',0),
		(197,'data_filler_end',0)
	],
	'tx_wb_plcase': [
		(2,'record_key',0),
		(6,'plg_cas_counter',0),
		(2,'plug_cas_inch',0),
		(2,'plug_cas_frac_num',0),
		(2,'plug_cas_frac_denom',0),
		(3,'plug_wgt_whole',0),
		(1,'plug_wgt_tenths',0),
		(5,'plug_amt_put',0),
		(5,'plug_amt_left',0),
		(2,'plug_hole_inch',0),
		(2,'plug_hole_frac_num',0),
		(2,'plug_hole_frac_denom',0),
		(20,'filler_32',0),
		(193,'data_filler_end',0)
	],
	'tx_wb_plperf': [
		(2,'record_key',0),
		(3,'plug_perf_counter',0),
		(5,'plug_from_perf',0),
		(5,'plug_to_perf',0),
		(1,'plug_open_hole_indicator',0),
		(19,'filler_33',0),
		(212,'data_filler_end',0)
	],
	'tx_wb_plname': [
		(2,'record_key',0),
		(8,'plug_field_no',0),
		(32,'plug_field_name',0),
		(6,'plug_oper_no',0),
		(32,'plug_oper_name',0),
		(32,'plug_lease_name',0),
		(135,'data_filler_end',0)
	],
	'tx_wb_drill': [
		(2,'record_key',0),
		(6,'permit_number',0),
		(14,'filler_34',0),
		(225,'data_filler_end',0),
	],
	'tx_wb_wellid': [
		(2,'record_key',0),
		(1,'oil_gas_code',0),
		(13,'oil_gas_key',0),
		(11,'filler_35',0),
		(220,'data_filler_end',0)
	],
	'tx_wb_14b2': [
		(2,'record_key',0),
		(1,'oil_gas_code',0),
		(13,'oil_gas_key',0),
		(6,'application_number',0),
		(2,'gas_district',0),
		(1,'ext_status_flag',0),
		(1,'ext_cancelled_reason',0),
		(2,'ext_approved_cent',0),
		(2,'ext_approved_year',0),
		(2,'ext_approved_month',0),
		(2,'ext_approved_day',0),
		(2,'ext_exp_cent',0),
		(2,'ext_exp_year',0),
		(2,'ext_exp_month',0),
		(2,'ext_exp_day',0),
		(2,'ext_denied_cent',0),
		(2,'ext_denied_year',0),
		(2,'ext_denied_month',0),
		(2,'ext_denied_day',0),
		(2,'ext_hist_cent',0),
		(2,'ext_hist_year',0),
		(2,'ext_hist_month',0),
		(2,'ext_hist_day',0),
		(1,'mech_integ_viol_flag',0),
		(1,'plug_order_sf_hold_flag',0),
		(1,'pollution_viol_flag',0),
		(1,'field_ops_hold_flag',0),
		(1,'h15_problem_flag',0),
		(1,'h15_not_filed_flag',0),
		(1,'oper_delq_flag',0),
		(1,'district_hold_sfp_flag',0),
		(1,'dist_sf_clean_up_flag',0),
		(1,'dist_state_plug_flag',0),
		(1,'good_faith_viol_flag',0),
		(1,'well_other_viol_flag',0),
		(1,'w3c_surf_eqp_viol_flag',0),
		(1,'w3x_viol_flag',0),
		(7,'filler_36',0),
		(1,'hb2259_w3x_pub_ent',0),
		(1,'hb2259_w3x_10pct',0),
		(1,'hb2259_w3x_bonding',0),
		(1,'hb2259_w3x_h13_eor',0),
		(1,'hb2259_w3x_aop',0),
		(1,'hb2259_w3x_mit',0),
		(1,'hb2259_w3x_escrow',0),
		(8,'w3x_filing_key',0),
		(8,'w3x_aop_received_date',0),
		(8,'w3x_aop_fee_rcvd_date',0),
		(8,'w3x_h15_fee_rcvd_date',0),
		(5,'w3x_escrow_fund_whole',0),
		(2,'w3x_escrow_fund_decimal',0),
		(1,'60_day_letter_sent_flag',0),
		(1,'w1x_36_needs_bond_flag',0),
		(1,'w1x_36_type_coverage',0),
		(9,'w1x_36_amt_filed',0),
		(5,'w1x_36_surety',0),
		(2,'w1x_36_exp_cent',0),
		(2,'w1x_36_exp_year',0),
		(2,'w1x_36_exp_mon',0),
		(2,'w1x_36_exp_day',0),
		(20,'w1x_36_bond_number',0),
		(32,'filler_37',0),
		(45,'data_filler_end',0)
	],
	'tx_wb_h15': [
		(2,'record_key',0),
		(8,'h15_date_key',0),
		(1,'h15_status',0),
		(6,'h15_operator',0),
		(4,'next_test_ccyy',0),
		(2,'next_test_mm',0),
		(2,'h15_district',0),
		(8,'h15_field',0),
		(1,'h15_hist_wellbore_flag',0),
		(2,'h15_hist_well_cc',0),
		(2,'h15_hist_well_yy',0),
		(2,'h15_hist_well_mm',0),
		(2,'h15_hist_well_dd',0),
		(1,'h15_w1x_well',0),
		(1,'h15_oil_gas_code',0),
		(5,'h15_lease_nbr',0),
		(6,'h15_well_nbr',0),
		(6,'h15_gasid_nbr',0),
		(2,'h15_test_cc',0),
		(2,'h15_test_yy',0),
		(2,'h15_test_mm',0),
		(2,'h15_test_dd',0),
		(6,'h15_base_usable_water',0),
		(1,'h15_type_test_flag',0),
		(6,'h15_top_of_fluid',0),
		(1,'h15_fluid_test_flag',0),
		(1,'h15_mech_integ_test_flag',0),
		(1,'h15_mech_test_reason_flag',0),
		(2,'h15_alternate_test_period',0),
		(20,'h15_other_mit_test_type',0),
		(2,'h15_status_cc',0),
		(2,'h15_status_yy',0),
		(2,'h15_status_mm',0),
		(2,'h15_status_dd',0),
		(1,'h15_no_date_well_flag',0),
		(1,'h15_record_from_edi_flag',0),
		(2,'h15_keyed_cc',0),
		(2,'h15_keyed_yy',0),
		(2,'h15_keyed_mm',0),
		(2,'h15_keyed_dd',0),
		(2,'h15_changed_cc',0),
		(2,'h15_changed_yy',0),
		(2,'h15_changed_mm',0),
		(2,'h15_changed_dd',0),
		(1,'h15_previous_status',0),
		(1,'h15_uic_test_flag',0),
		(1,'h15_2yrs_approved_flag',0),
		(1,'h15_mail_hold_flag',0),
		(1,'h15_10yr_inactive_flag',0),
		(1,'h15_w3x_well_flag',0),
		(13,'filler_38',0),
		(95,'data_filler_end',0)
	],
	'tx_wb_h15rmk': [
		(2,'record_key',0),
		(3,'h15_remark_key',0),
		(70,'h15_remark_text',0),
		(7,'filler_39',0),
		(165,'data_filler_end',0)
	],
	'tx_wb_sb126': [
		(2,'record_key',0),
		(1,'sb126_designation_flag',0),
		(2,'sb126_desig_effec_cc',0),
		(2,'sb126_desig_effec_yy',0),
		(2,'sb126_desig_effec_mm',0),
		(2,'sb126_desig_revised_cc',0),
		(2,'sb126_desig_revised_yy',0),
		(2,'sb126_desig_revised_mm',0),
		(2,'sb126_desig_letter_cc',0),
		(2,'sb126_desig_letter_yy',0),
		(2,'sb126_desig_letter_mm',0),
		(2,'sb126_desig_letter_dd',0),
		(2,'sb126_cert_effec_cc',0),
		(2,'sb126_cert_effec_yy',0),
		(2,'sb126_cert_effec_mm',0),
		(2,'sb126_cert_revoked_cc',0),
		(2,'sb126_cert_revoked_yy',0),
		(2,'sb126_cert_revoked_mm',0),
		(2,'sb126_cert_revoked_dd',0),
		(2,'sb126_cert_denial_cc',0),
		(2,'sb126_cert_denial_yy',0),
		(2,'sb126_cert_denial_mm',0),
		(2,'sb126_cert_denial_dd',0),
		(1,'sb126_denial_reason_flag',0),
		(16,'filler_40',0),
		(185,'data_filler_end',0)
	],
	'tx_wb_dastat': [
		(2,'record_key',0),
		(7,'stat_num',0),
		(2,'uniq_num',0),
		(1,'deleted_flag',0),
		(10,'filler_41',0),
		(225,'data_filler_end',0)
	],
	'tx_wb_w3c': [
		(2,'record_key',0),
		(1,'w3c_1yr_flag',0),
		(8,'w3c_1yr_filed_date',0),
		(6,'w3c_1yr_filing_oper',0),
		(1,'w3c_5yr_flag',0),
		(8,'w3c_5yr_filed_date',0),
		(6,'w3c_5yr_filing_oper',0),
		(1,'w3c_10yr_flag',0),
		(8,'w3c_10yr_filed_date',0),
		(6,'w3c_10yr_filing_oper',0),
		(8,'w3c_14b2_removal_date',0),
		(1,'w3c_extension_flag',0),
		(4,'w3c_extension_year',0),
		(2,'w3c_extension_month',0),
		(2,'w3c_extension_day',0),
		(1,'w3c_5yr_flag_previous',0),
		(1,'w3c_10yr_flag_previous',0),
		(36,'filler_42',0),
		(145,'data_filler_end',0)
	],
	'tx_wb_14b2rm': [
		(2,'record_key',0),
		(3,'14b2_rmk_lne_cnt',0),
		(8,'14b2_rmk_date',0),
		(8,'14b2_rmk_userid',0),
		(66,'14b2_remarks',0),
		(15,'filler_43',0),
		(145,'data_filler_end',0)
	]
}

tx_oil = {
    '01': (2, 8, 1, 1, 2, 5, 1, 6, 2, 4, 2, 2, 8, 1, 1, 5, 1, 4, 1, 3, 5, 3, 1, 3, 2, 2, 2, 8, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 4, 2, 1, 116),
    '02': [
        (2, False, 'rrc_tape_rec_id'),
        (6, False, 'report_cycle_date'),
        (7, True, 'acres'),
        (5, True, 'acre_feet'),
        (5, True, 'net_acre_feet'),
        (5, True, 'bhp'),
        (7, True, 'working_potential'),
        (1, False, 'tolerance_acres'),
        (4, False, 'effective_year'),
        (2, False, 'effective_month'),
        (2, False, 'effective_day'),
        (4, False, 'issue_year'),
        (2, False, 'issue_month'),
        (2, False, 'issue_day'),
        (5, True, 'allowable_amount'),
        (7, True, 'gas_limit'),
        (5, True, 'gas_oil_ratio'),
        (30, False, 'report_cycle_remark'),
        (7, True, 'original_oil_in_place'),
        (2, False, 'allowable_code'),
        (1, False, 'allow_limit_cd'),
        (2, False, 'type_wells'),
        (3, False, 'sand_thickness'),
        (1, False, 'co_reg_depth_code'),
        (1, False, 'net_gor_code'),
        (5, True, 'net_gor'),
        (1, False, 'special_allow_code'),
        (5, True, 'special_allow_amount'),
        (1, False, '14B2_code'),
        (4, False, '14B2_year'),
        (2, False, '14B2_month'),
        (5, True, 'water_production'),
        (5, True, 'frozen_potential'),
        (1, False, 'producing_method'),
        (20, False, 'other_prod_method'),
        (7, True, 'well_monthly_allowable'),
        (5, True, 'lowest_perforation'),
        (1, False, 'filler'),
        (1, False, 'w10_exc_to_test_flag'),
        (4, False, 'test_year'),
        (2, False, 'test_month'),
        (2, False, 'test_day'),
        (1, False, 'retest_flag'),
        (5, True, '12_hour_potential'),
        (1, False, 'bonus_code'),
        (3, False, 'bonus_amount'),
        (1, False, 'eb_flag'),
        (1, False, 'allow_pote_gor_chg_flag'),
        (9, True, 'cash_monthly_limit'),
        (1, False, 'eb_change_month_flag'),
        (7, True, 'top_allowable_amount'),
        (1, False, 'panhandle_comp_code'),
        (1, False, 'panhandle_sub_code'),
        (1, False, 'h15_violation_flag'),
        (1, False, 'oil_allocation_flag'),
        (6, False, 'filler_2')
    ],
    '03': (2, 226),
    '04': (2, 226),
    '05': (2, 226),
    '06': (2, 226),
    '07': (2, 226),
    '08': (2, 226),
    '09': (2, 226),
    '10': (2, 226),
    '11': (2, 226),
    '12': (2, 226),
    '13': (2, 226),
    '14': (2, 226),
    '15': (2, 226),
    '16': (2, 226),
    '26': (2, 226),
    '28': (2, 226)
}

comp_3_conv = {
    '00': 'f0f0',
    '01': 'f0f1',
    '02': 'f0f2',
    '03': 'f0f3',
    '04': 'f0f4',
    '05': 'f0f5',
    '06': 'f0f6',
    '07': 'f0f7',
    '08': 'f0f8',
    '09': 'f0f9',
    '10': 'f1f0',
    '11': 'f1f1',
    '12': 'f1f2',
    '13': 'f1f3',
    '14': 'f1f4',
    '15': 'f1f5',
    '16': 'f1f6',
    '17': 'f1f7',
    '18': 'f1f8',
    '19': 'f1f9',
    '20': 'f2f0',
    '21': 'f2f1',
    '22': 'f2f2',
    '23': 'f2f3',
    '24': 'f2f4',
    '25': 'f2f5',
    '26': 'f2f6',
    '27': 'f2f7',
    '28': 'f2f8',
    '29': 'f2f9',
    '30': 'f3f0',
    '31': 'f3f1',
    '32': 'f3f2',
    '33': 'f3f3',
    '34': 'f3f4',
    '35': 'f3f5',
    '36': 'f3f6',
    '37': 'f3f7',
    '38': 'f3f8',
    '39': 'f3f9',
    '40': 'f4f0',
    '41': 'f4f1',
    '0a': 'f0',
    '0b': 'f0',
    '0c': 'f0',
    '0d': 'f0',
    '0e': 'f0',
    '0f': 'f0',
    'ff': '40',
    'a0': 'f0',
    'b0': 'f0',
    'c0': 'f0',
    'd0': 'f0',
    'e0': 'f0',
    '42': 'f4f2',
    '43': 'f4f3',
    '44': 'f4f4',
    '45': 'f4f5',
    '46': 'f4f6',
    '47': 'f4f7',
    '48': 'f4f8',
    '49': 'f4f9',
    '50': 'f5f0',
    '51': 'f5f1',
    '52': 'f5f2',
    '53': 'f5f3',
    '54': 'f5f4',
    '55': 'f5f5',
    '56': 'f5f6',
    '57': 'f5f7',
    '58': 'f5f8',
    '59': 'f5f9',
    '60': 'f6f0',
    '61': 'f6f1',
    '62': 'f6f2',
    '63': 'f6f3',
    '64': 'f6f4',
    '65': 'f6f5',
    '66': 'f6f6',
    '67': 'f6f7',
    '68': 'f6f8',
    '69': 'f6f9',
    '70': 'f7f0',
    '71': 'f7f1',
    '72': 'f7f2',
    '73': 'f7f3',
    '74': 'f7f4',
    '75': 'f7f5',
    '76': 'f7f6',
    '77': 'f7f7',
    '78': 'f7f8',
    '79': 'f7f9',
    '80': 'f8f0',
    '81': 'f8f1',
    '82': 'f8f2',
    '83': 'f8f3',
    '84': 'f8f4',
    '85': 'f8f5',
    '86': 'f8f6',
    '87': 'f8f7',
    '88': 'f8f8',
    '89': 'f8f9',
    '90': 'f9f0',
    '91': 'f9f1',
    '92': 'f9f2',
    '93': 'f9f3',
    '94': 'f9f4',
    '95': 'f9f5',
    '96': 'f9f6',
    '97': 'f9f7',
    '98': 'f9f8',
    '99': 'f9f9',
    '1a': 'f1',
    '1b': 'f1',
    '1c': 'f1',
    '1d': 'f1',
    '1e': 'f1',
    '1f': 'f1',
    '2a': 'f2',
    '2b': 'f2',
    '2c': 'f2',
    '2d': 'f2',
    '2e': 'f2',
    '2f': 'f2',
    '3a': 'f3',
    '3b': 'f3',
    '3c': 'f3',
    '3d': 'f3',
    '3e': 'f3',
    '3f': 'f3',
    '4a': 'f4',
    '4b': 'f4',
    '4c': 'f4',
    '4d': 'f4',
    '4e': 'f4',
    '4f': 'f4',
    '5a': 'f5',
    '5b': 'f5',
    '5c': 'f5',
    '5d': 'f5',
    '5e': 'f5',
    '5f': 'f5',
    '6a': 'f6',
    '6b': 'f6',
    '6c': 'f6',
    '6d': 'f6',
    '6e': 'f6',
    '6f': 'f6',
    '7a': 'f7',
    '7b': 'f7',
    '7c': 'f7',
    '7d': 'f7',
    '7e': 'f7',
    '7f': 'f7',
    '8a': 'f8',
    '8b': 'f8',
    '8c': 'f8',
    '8d': 'f8',
    '8e': 'f8',
    '8f': 'f8',
    '9a': 'f9',
    '9b': 'f9',
    '9c': 'f9',
    '9d': 'f9',
    '9e': 'f9',
    '9f': 'f9',
    'a1': 'a1',
    'a2': 'a2',
    'a3': 'a3',
    'a4': 'a4',
    'a5': 'a5',
    'a6': 'a6',
    'a7': 'a7',
    'a8': 'a8',
    'a9': 'a9',
    'aa': 'aa',
    'ab': 'ab',
    'ac': 'ac',
    'ad': 'ad',
    'ae': 'ae',
    'af': 'af',
    'b1': 'b1',
    'b2': 'b2',
    'b3': 'b3',
    'b4': 'b4',
    'b5': 'b5',
    'b6': 'b6',
    'b7': 'b7',
    'b8': 'b8',
    'b9': 'b9',
    'ba': 'ba',
    'bb': 'bb',
    'bc': 'bc',
    'bd': 'bd',
    'be': 'be',
    'bf': 'bf',
    'c1': 'c1',
    'c2': 'c2',
    'c3': 'c3',
    'c4': 'c4',
    'c5': 'c5',
    'c6': 'c6',
    'c7': 'c7',
    'c8': 'c8',
    'c9': 'c9',
    'ca': 'ca',
    'cb': 'cb',
    'cc': 'cc',
    'cd': 'cd',
    'ce': 'ce',
    'cf': 'cf',
    'd1': 'd1',
    'd2': 'd2',
    'd3': 'd3',
    'd4': 'd4',
    'd5': 'd5',
    'd6': 'd6',
    'd7': 'd7',
    'd8': 'd8',
    'd9': 'd9',
    'da': 'da',
    'db': 'db',
    'dc': 'dc',
    'dd': 'dd',
    'de': 'de',
    'df': 'df',
    'e1': 'e1',
    'e2': 'e2',
    'e3': 'e3',
    'e4': 'e4',
    'e5': 'e5',
    'e6': 'e6',
    'e7': 'e7',
    'e8': 'e8',
    'e9': 'e9',
    'ea': 'ea',
    'eb': 'eb',
    'ec': 'ec',
    'ed': 'ed',
    'ee': 'ee',
    'ef': 'ef',
    'f1': 'f1',
    'f2': 'f2',
    'f3': 'f3',
    'f4': 'f4',
    'f5': 'f5',
    'f6': 'f6',
    'f7': 'f7',
    'f8': 'f8',
    'f9': 'f9',
    'fa': 'fa',
    'fb': 'fb',
    'fc': 'fc',
    'fd': 'fd',
    'fe': 'fe',
    'f0': 'f0'
}

comp_3_conv2 = {
    '00': 'f0f0',
    '01': 'f0f1',
    '02': 'f0f2',
    '03': 'f0f3',
    '04': 'f0f4',
    '05': 'f0f5',
    '06': 'f0f6',
    '07': 'f0f7',
    '08': 'f0f8',
    '09': 'f0f9',
    '10': 'f1f0',
    '11': 'f1f1',
    '12': 'f1f2',
    '13': 'f1f3',
    '14': 'f1f4',
    '15': 'f1f5',
    '16': 'f1f6',
    '17': 'f1f7',
    '18': 'f1f8',
    '19': 'f1f9',
    '20': 'f2f0',
    '21': 'f2f1',
    '22': 'f2f2',
    '23': 'f2f3',
    '24': 'f2f4',
    '25': 'f2f5',
    '26': 'f2f6',
    '27': 'f2f7',
    '28': 'f2f8',
    '29': 'f2f9',
    '30': 'f3f0',
    '31': 'f3f1',
    '32': 'f3f2',
    '33': 'f3f3',
    '34': 'f3f4',
    '35': 'f3f5',
    '36': 'f3f6',
    '37': 'f3f7',
    '38': 'f3f8',
    '39': 'f3f9',
    '40': 'f4f0',
    '41': 'f4f1',
    '0a': 'f040',
    '0b': 'f040',
    '0c': 'f040',
    '0d': 'f040',
    '0e': 'f040',
    '0f': 'f040',
    'ff': '4040',
    'a0': 'f040',
    'b0': 'f040',
    'c0': 'f040',
    'd0': 'f040',
    'e0': 'f040',
    '42': 'f4f2',
    '43': 'f4f3',
    '44': 'f4f4',
    '45': 'f4f5',
    '46': 'f4f6',
    '47': 'f4f7',
    '48': 'f4f8',
    '49': 'f4f9',
    '50': 'f5f0',
    '51': 'f5f1',
    '52': 'f5f2',
    '53': 'f5f3',
    '54': 'f5f4',
    '55': 'f5f5',
    '56': 'f5f6',
    '57': 'f5f7',
    '58': 'f5f8',
    '59': 'f5f9',
    '60': 'f6f0',
    '61': 'f6f1',
    '62': 'f6f2',
    '63': 'f6f3',
    '64': 'f6f4',
    '65': 'f6f5',
    '66': 'f6f6',
    '67': 'f6f7',
    '68': 'f6f8',
    '69': 'f6f9',
    '70': 'f7f0',
    '71': 'f7f1',
    '72': 'f7f2',
    '73': 'f7f3',
    '74': 'f7f4',
    '75': 'f7f5',
    '76': 'f7f6',
    '77': 'f7f7',
    '78': 'f7f8',
    '79': 'f7f9',
    '80': 'f8f0',
    '81': 'f8f1',
    '82': 'f8f2',
    '83': 'f8f3',
    '84': 'f8f4',
    '85': 'f8f5',
    '86': 'f8f6',
    '87': 'f8f7',
    '88': 'f8f8',
    '89': 'f8f9',
    '90': 'f9f0',
    '91': 'f9f1',
    '92': 'f9f2',
    '93': 'f9f3',
    '94': 'f9f4',
    '95': 'f9f5',
    '96': 'f9f6',
    '97': 'f9f7',
    '98': 'f9f8',
    '99': 'f9f9',
    '1a': 'f140',
    '1b': 'f140',
    '1c': 'f140',
    '1d': 'f140',
    '1e': 'f140',
    '1f': 'f140',
    '2a': 'f240',
    '2b': 'f240',
    '2c': 'f240',
    '2d': 'f240',
    '2e': 'f240',
    '2f': 'f240',
    '3a': 'f340',
    '3b': 'f340',
    '3c': 'f340',
    '3d': 'f340',
    '3e': 'f340',
    '3f': 'f340',
    '4a': 'f440',
    '4b': 'f440',
    '4c': 'f440',
    '4d': 'f440',
    '4e': 'f440',
    '4f': 'f440',
    '5a': 'f540',
    '5b': 'f540',
    '5c': 'f540',
    '5d': 'f540',
    '5e': 'f540',
    '5f': 'f540',
    '6a': 'f640',
    '6b': 'f640',
    '6c': 'f640',
    '6d': 'f640',
    '6e': 'f640',
    '6f': 'f640',
    '7a': 'f740',
    '7b': 'f740',
    '7c': 'f740',
    '7d': 'f740',
    '7e': 'f740',
    '7f': 'f740',
    '8a': 'f840',
    '8b': 'f840',
    '8c': 'f840',
    '8d': 'f840',
    '8e': 'f840',
    '8f': 'f840',
    '9a': 'f940',
    '9b': 'f940',
    '9c': 'f940',
    '9d': 'f940',
    '9e': 'f940',
    '9f': 'f940',
    'a1': 'a140',
    'a2': 'a240',
    'a3': 'a340',
    'a4': 'a440',
    'a5': 'a540',
    'a6': 'a640',
    'a7': 'a740',
    'a8': 'a840',
    'a9': 'a940',
    'aa': 'aa40',
    'ab': 'ab40',
    'ac': 'ac40',
    'ad': 'ad40',
    'ae': 'ae40',
    'af': 'af40',
    'b1': 'b140',
    'b2': 'b240',
    'b3': 'b340',
    'b4': 'b440',
    'b5': 'b540',
    'b6': 'b640',
    'b7': 'b740',
    'b8': 'b840',
    'b9': 'b940',
    'ba': 'ba40',
    'bb': 'bb40',
    'bc': 'bc40',
    'bd': 'bd40',
    'be': 'be40',
    'bf': 'bf40',
    'c1': 'c140',
    'c2': 'c240',
    'c3': 'c340',
    'c4': 'c440',
    'c5': 'c540',
    'c6': 'c640',
    'c7': 'c740',
    'c8': 'c840',
    'c9': 'c940',
    'ca': 'ca40',
    'cb': 'cb40',
    'cc': 'cc40',
    'cd': 'cd40',
    'ce': 'ce40',
    'cf': 'cf40',
    'd1': 'd140',
    'd2': 'd240',
    'd3': 'd340',
    'd4': 'd440',
    'd5': 'd540',
    'd6': 'd640',
    'd7': 'd740',
    'd8': 'd840',
    'd9': 'd940',
    'da': 'da40',
    'db': 'db40',
    'dc': 'dc40',
    'dd': 'dd40',
    'de': 'de40',
    'df': 'df40',
    'e1': 'e140',
    'e2': 'e240',
    'e3': 'e340',
    'e4': 'e440',
    'e5': 'e540',
    'e6': 'e640',
    'e7': 'e740',
    'e8': 'e840',
    'e9': 'e940',
    'ea': 'ea40',
    'eb': 'eb40',
    'ec': 'ec40',
    'ed': 'ed40',
    'ee': 'ee40',
    'ef': 'ef40',
    'f1': 'f140',
    'f2': 'f240',
    'f3': 'f340',
    'f4': 'f440',
    'f5': 'f540',
    'f6': 'f640',
    'f7': 'f740',
    'f8': 'f840',
    'f9': 'f940',
    'fa': 'fa40',
    'fb': 'fb40',
    'fc': 'fc40',
    'fd': 'fd40',
    'fe': 'fe40',
    'f0': 'f040'
}

comp_3_conv_ = {
    '00': '3030',
    '01': '3031',
    '02': '3032',
    '03': '3033',
    '04': '3034',
    '05': '3035',
    '06': '3036',
    '07': '3037',
    '08': '3038',
    '09': '3039',
    '10': '3130',
    '11': '3131',
    '12': '3132',
    '13': '3133',
    '14': '3134',
    '15': '3135',
    '16': '3136',
    '17': '3137',
    '18': '3138',
    '19': '3139',
    '20': '3230',
    '21': '3231',
    '22': '3232',
    '23': '3233',
    '24': '3234',
    '25': '3235',
    '26': '3236',
    '27': '3237',
    '28': '3238',
    '29': '3239',
    '30': '3330',
    '31': '3331',
    '32': '3332',
    '33': '3333',
    '34': '3334',
    '35': '3335',
    '36': '3336',
    '37': '3337',
    '38': '3338',
    '39': '3339',
    '40': '3430',
    '41': '3431',
    '0a': '30',
    '0b': '30',
    '0c': '30',
    '0d': '30',
    '0e': '30',
    '0f': '30',
    'ff': '40',
    'a0': '30',
    'b0': '30',
    'c0': '30',
    'd0': '30',
    'e0': '30',
    '42': '3432',
    '43': '3433',
    '44': '3434',
    '45': '3435',
    '46': '3436',
    '47': '3437',
    '48': '3438',
    '49': '3439',
    '50': '3530',
    '51': '3531',
    '52': '3532',
    '53': '3533',
    '54': '3534',
    '55': '3535',
    '56': '3536',
    '57': '3537',
    '58': '3538',
    '59': '3539',
    '60': '3630',
    '61': '3631',
    '62': '3632',
    '63': '3633',
    '64': '3634',
    '65': '3635',
    '66': '3636',
    '67': '3637',
    '68': '3638',
    '69': '3639',
    '70': '3730',
    '71': '3731',
    '72': '3732',
    '73': '3733',
    '74': '3734',
    '75': '3735',
    '76': '3736',
    '77': '3737',
    '78': '3738',
    '79': '3739',
    '80': '3830',
    '81': '3831',
    '82': '3832',
    '83': '3833',
    '84': '3834',
    '85': '3835',
    '86': '3836',
    '87': '3837',
    '88': '3838',
    '89': '3839',
    '90': '3930',
    '91': '3931',
    '92': '3932',
    '93': '3933',
    '94': '3934',
    '95': '3935',
    '96': '3936',
    '97': '3937',
    '98': '3938',
    '99': '3939',
    '1a': '31',
    '1b': '31',
    '1c': '31',
    '1d': '31',
    '1e': '31',
    '1f': '31',
    '2a': '32',
    '2b': '32',
    '2c': '32',
    '2d': '32',
    '2e': '32',
    '2f': '32',
    '3a': '33',
    '3b': '33',
    '3c': '33',
    '3d': '33',
    '3e': '33',
    '3f': '33',
    '4a': '34',
    '4b': '34',
    '4c': '34',
    '4d': '34',
    '4e': '34',
    '4f': '34',
    '5a': '35',
    '5b': '35',
    '5c': '35',
    '5d': '35',
    '5e': '35',
    '5f': '35',
    '6a': '36',
    '6b': '36',
    '6c': '36',
    '6d': '36',
    '6e': '36',
    '6f': '36',
    '7a': '37',
    '7b': '37',
    '7c': '37',
    '7d': '37',
    '7e': '37',
    '7f': '37',
    '8a': '38',
    '8b': '38',
    '8c': '38',
    '8d': '38',
    '8e': '38',
    '8f': '38',
    '9a': '39',
    '9b': '39',
    '9c': '39',
    '9d': '39',
    '9e': '39',
    '9f': '39',
    'a1': 'a1',
    'a2': 'a2',
    'a3': 'a3',
    'a4': 'a4',
    'a5': 'a5',
    'a6': 'a6',
    'a7': 'a7',
    'a8': 'a8',
    'a9': 'a9',
    'aa': 'aa',
    'ab': 'ab',
    'ac': 'ac',
    'ad': 'ad',
    'ae': 'ae',
    'af': 'af',
    'b1': 'b1',
    'b2': 'b2',
    'b3': 'b3',
    'b4': 'b4',
    'b5': 'b5',
    'b6': 'b6',
    'b7': 'b7',
    'b8': 'b8',
    'b9': 'b9',
    'ba': 'ba',
    'bb': 'bb',
    'bc': 'bc',
    'bd': 'bd',
    'be': 'be',
    'bf': 'bf',
    'c1': 'c1',
    'c2': 'c2',
    'c3': 'c3',
    'c4': 'c4',
    'c5': 'c5',
    'c6': 'c6',
    'c7': 'c7',
    'c8': 'c8',
    'c9': 'c9',
    'ca': 'ca',
    'cb': 'cb',
    'cc': 'cc',
    'cd': 'cd',
    'ce': 'ce',
    'cf': 'cf',
    'd1': 'd1',
    'd2': 'd2',
    'd3': 'd3',
    'd4': 'd4',
    'd5': 'd5',
    'd6': 'd6',
    'd7': 'd7',
    'd8': 'd8',
    'd9': 'd9',
    'da': 'da',
    'db': 'db',
    'dc': 'dc',
    'dd': 'dd',
    'de': 'de',
    'df': 'df',
    'e1': 'e1',
    'e2': 'e2',
    'e3': 'e3',
    'e4': 'e4',
    'e5': 'e5',
    'e6': 'e6',
    'e7': 'e7',
    'e8': 'e8',
    'e9': 'e9',
    'ea': 'ea',
    'eb': 'eb',
    'ec': 'ec',
    'ed': 'ed',
    'ee': 'ee',
    'ef': 'ef',
    'f1': 'f1',
    'f2': 'f2',
    'f3': 'f3',
    'f4': 'f4',
    'f5': 'f5',
    'f6': 'f6',
    'f7': 'f7',
    'f8': 'f8',
    'f9': 'f9',
    'fa': 'fa',
    'fb': 'fb',
    'fc': 'fc',
    'fd': 'fd',
    'fe': 'fe',
    'f0': 'f0'
}

comp_3_nums = {
    'cc': 3036,
    'cd': 3037,
    'ce': 3038,
    'cf': 3039,
    'da': 3430,
    'db': 3431,
    'e2': 3432,
    'e4': 3433,
    'e0': 3434,
    'e1': 3435,
    'e3': 3436,
    'e5': 3437,
    'e7': 3438,
    'f1': 3439,
    '26': 3530,
    'e9': 3531,
    'ea': 3532,
    'eb': 3533,
    'e8': 3534,
    'ed': 3535,
    'ee': 3536,
    'ef': 3537,
    'ec': 3538,
    'df': 3539,
    '2d': 3630,
    '2f': 3631,
    'c2': 3632,
    'c4': 3633,
    'c0': 3634,
    'c1': 3635,
    'c3': 3636,
    'c5': 3637,
    'c7': 3638,
    'd1': 3639,
    'f8': 3730,
    'c9': 3731,
    'ca': 3732,
    'cb': 3733,
    'c8': 3734,
    'cd': 3735,
    'ce': 3736,
    'cf': 3737,
    'cc': 3738,
    '60': 3739,
    'd8': 3830,
    '61': 3831,
    '62': 3832,
    '63': 3833,
    '64': 3834,
    '65': 3835,
    '66': 3836,
    '67': 3837,
    '68': 3838,
    '69': 3839,
    'b0': 3930,
    '6a': 3931,
    '6b': 3932,
    '6c': 3933,
    '6d': 3934,
    '6e': 3935,
    '6f': 3936,
    '70': 3937,
    '71': 3938,
    '72': 3939,
    '41': 3130,
    '42': 3131,
    '43': 3132,
    '44': 3133,
    '45': 3134,
    '46': 3135,
    '47': 3136,
    '48': 3137,
    '49': 3138,
    '4a': 3139,
    '4b': 3230,
    '4c': 3231,
    '4d': 3232,
    '4e': 3233,
    '4f': 3234,
    '50': 3235,
    '51': 3236,
    '52': 3237,
    '53': 3238,
    '54': 3239,
    '55': 3330,
    '56': 3331,
    '57': 3332,
    '58': 3333,
    '59': 3334,
    '5a': 3335

}

tx_oil_well_info_cols = [
    'well_root_no',
    'district_no',
    'lease_no',
    'well_no',
    'rrc_tape_rec_id',
    'report_cycle_date',
    'acres',
    'acre_feet',
    'net_acre_feet',
    'bhp',
    'working_potential',
    'tolerance_acres',
    'effective_year',
    'effective_month',
    'effective_day',
    'issue_year',
    'issue_month',
    'issue_day',
    'allowable_amount',
    'gas_limit',
    'gas_oil_ratio',
    'report_cycle_remark',
    'original_oil_in_place',
    'allowable_code',
    'allow_limit_cd',
    'type_wells',
    'sand_thickness',
    'co_reg_depth_code',
    'net_gor_code',
    'net_gor',
    'special_allow_code',
    'special_allow_amount',
    '14B2_code',
    '14B2_year',
    '14B2_month',
    'water_production',
    'frozen_potential',
    'producing_method',
    'other_prod_method',
    'well_monthly_allowable',
    'lowest_perforation',
    'filler',
    'w10_exc_to_test_flag',
    'test_year',
    'test_month',
    'test_day',
    'retest_flag',
    '12_hour_potential',
    'bonus_code',
    'bonus_amount',
    'eb_flag',
    'allow_pote_gor_chg_flag',
    'cash_monthly_limit',
    'eb_change_month_flag',
    'top_allowable_amount',
    'panhandle_comp_code',
    'panhandle_sub_code',
    'h15_violation_flag',
    'oil_allocation_flag'
]

wb_hex_data = {
    '09': [42],
    '10': [10, 15]
}

comp_3_data = {
    'oil': {
        'f0f1': [20, 61, 62, 63, 64, 65, 70, 71, 72],
        'f0f2': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 83, 84, 85, 86, 94, 97, 98, 99, 101, 102, 103, 111, 112, 113, 114, 115, 116, 138, 139, 140, 141, 142, 143, 144, 145, 156, 157, 158, 162, 165, 166, 167, 168, 169, 171, 172, 173, 174],
        'f0f3': [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 69, 70, 71, 72, 73, 74, 75, 76, 77],
        'f1f0': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'f1f3': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],
        'f1f4': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]
    },
    'gas': {
        'f2f4': [4, 5, 6, 7, 8],
        'f2f5': [
            19, 20, 21, 22, 23,
            24, 25, 26, 27, 28,
            31, 32, 33, 34, 35,
            44, 45, 46, 47, 48,
            50, 51, 52, 53, 54,
            56, 57, 58, 59, 60,
            61, 62, 63, 64, 65,
            68, 69, 70, 71,
            73, 74, 75, 76, 77,
            79, 80, 81, 82, 83,
            85, 86, 87,
            89, 90, 91, 92,
            94, 95, 96,
            98, 99, 100, 101, 102, 103,
            105, 106, 107, 108,
            162, 163, 164, 165, 166
        ],
        'f2f0': [
            51, 52, 53, 54, 55,
            56, 57, 58, 59, 60
        ],
        '3230': [
            52, 53, 54, 55, 56,
            57, 58, 59, 60, 61
        ],
        'f2f1': [
            27, 28, 29, 30, 31,
            32, 33, 34, 35, 36,
            49, 50, 51, 52, 53,
            56, 57, 58, 59, 60,
            61, 62, 63, 64, 65,
            66, 67, 68, 69, 70,
            72, 73, 74, 75, 76,
            78, 79, 80, 81, 82,
            90, 91, 92, 93, 94, 95,
            96, 97, 98, 99,
            100, 101, 102, 103, 104,
            105, 106, 107,
            108, 109, 110, 111,
            112, 113, 114,
            123, 124, 125, 126, 127,
            128, 129, 130, 131, 132,
            175, 176, 177, 178, 179,
            186, 187, 188, 189, 190#,
            #204, 205, 206, 207, 208,
            #209,
            #222, 223, 224, 225, 226
        ],
        'f1f9': [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74],
        'f1f8': [
            26, 27, 28, 29, 30,
            31, 32, 33, 34,
            35, 36, 37, 38,
            39, 40, 41,
            42, 43,
            44, 45, 46,
            47, 48, 49, 50,
            51, 52, 53,
            54, 55, 56, 57, 58,
            59, 60, 61,
            63, 64, 65, 66,
            67, 68, 69,
            70, 71, 72, 73, 74
        ],
        'f1f7': [
            19, 20, 21, 22, 23,
            24, 25, 26,
            27, 28, 29,
            30, 31, 32,
            33, 34, 35,
            36, 37,
            38, 39, 40,
            41, 42, 43, 44, 45
        ]
    }
}

rec_comp_3_data = {
    'oil': {
        '03': [
            (19, 5),
            (24, 3),
            (27, 4),
            (31, 3),
            (69, 4),
            (73, 5),
        ],
        '14': [
            (47, 4),
            (51, 3),
            (54, 4),
            (58, 3),
            (61, 4)
        ],
        '02': [
            (9, 4),
            (13, 3),
            (16, 3),
            (19, 3),
            (22, 4),
            (43, 3),
            (46, 4),
            (50, 3),
            (83, 4),
            (97, 3),
            (101, 3),
            (111, 3),
            (114, 3),
            (138, 4),
            (142, 4),
            (156, 3),
            (165, 5),
            (171, 4)
        ],
        '13': [
            (47, 4),
            (51, 3),
            (54, 4),
            (58, 3),
            (61, 4)
        ],
        '10': [
            (3, 5),
            (8, 5)
        ],
        '01': [
            (61, 5)
        ]
    },
    'gas': {
        '17': [
            (19, 5),
            (24, 3),
            (27, 3),
            (30, 3),
            (33, 3),
            (36, 2),
            (38, 3),
            (41, 5)
        ],
        '18': [
            (26, 5),
            (31, 4),
            (35, 4),
            (39, 3),
            (42, 2),
            (44, 3),
            (47, 4),
            (51, 3),
            (54, 5),
            (59, 3),
            (63, 4),
            (67, 3),
            (70, 5)
        ],
        '19': [
            (26, 5),
            (31, 4),
            (35, 4),
            (39, 3),
            (42, 2),
            (44, 3),
            (47, 4),
            (51, 3),
            (54, 5),
            (59, 3),
            (63, 4),
            (67, 3),
            (70, 5)
        ],
        '20': [(51, 1)],
        '21': [
            (27, 5),
            (32, 5),
            (49, 5),
            (56, 5),
            (61, 5),
            (66, 5),
            (72, 5),
            (78, 5),
            (90, 6),
            (96, 4),
            (100, 5),
            (105, 3),
            (108, 4),
            (112, 3),
            (123, 5),
            (128, 5),
            (175, 5),
            (186, 3)
        ],
        '24': [(4, 5)],
        '25': [
            (19, 5),
            (24, 5),
            (31, 5),
            (44, 5),
            (50, 5),
            (56, 10),
            (68, 4),
            (73, 5),
            (79, 5),
            (85, 3),
            (89, 4),
            (94, 3),
            (98, 6),
            (105, 4),
            (162, 5)
        ]
    }
}

tx_record_tables = {
    'oil': {
        '01': 'tx_oil_root',
        '02': 'tx_oil_rptcy',
        '03': 'tx_oil_prval',
        '04': 'tx_oil_frmlk',
        '05': 'tx_oil_frmds',
        '06': 'tx_oil_etex',
        '07': 'tx_oil_etds',
        '08': 'tx_oil_altf',
        '09': 'tx_oil_tfwl',
        '10': 'tx_oil_phprod',
        '11': 'tx_oil_pvtyp',
        '12': 'tx_oil_phbal',
        '13': 'tx_oil_w10',
        '14': 'tx_oil_pvw10',
        '15': 'tx_oil_remark',
        '16': 'tx_oil_seal',
        '26': 'tx_oil_uic',
        '28': 'tx_oil_sb126'
    },
    'gas': {
        '01': 'tx_gas_root',
        '15': 'tx_gas_remark',
        '16': 'tx_gas_seal',
        '17': 'tx_gas_g1',
        '18': 'tx_gas_g10',
        '19': 'tx_gas_pvg10',
        '20': 'tx_gas_c1',
        '21': 'tx_gas_rptcy',
        '22': 'tx_gas_frmlk',
        '23': 'tx_gas_frmds',
        '24': 'tx_gas_altf',
        '25': 'tx_gas_prval',
        '27': 'tx_gas_uic',
        '28': 'tx_gas_sb126'
    }
}

tx_wb_record_tables = {
    '01': 'tx_wb_root',
    '02': 'tx_wb_compl',
    '03': 'tx_wb_date',
    '04': 'tx_wb_rmks',
    '05': 'tx_wb_tube',
    '06': 'tx_wb_case',
    '07': 'tx_wb_perf',
    '08': 'tx_wb_line',
    '09': 'tx_wb_form',
    '10': 'tx_wb_sqeze',
    '11': 'tx_wb_fresh',
    '12': 'tx_wb_oldloc',
    '13': 'tx_wb_newloc',
    '14': 'tx_wb_plug',
    '15': 'tx_wb_plrmks',
    '16': 'tx_wb_plrec',
    '17': 'tx_wb_plcase',
    '18': 'tx_wb_plperf',
    '19': 'tx_wb_plname',
    '20': 'tx_wb_drill',
    '21': 'tx_wb_wellid',
    '22': 'tx_wb_14b2',
    '23': 'tx_wb_h15',
    '24': 'tx_wb_h15rmk',
    '25': 'tx_wb_sb126',
    '26': 'tx_wb_dastat',
    '27': 'tx_wb_w3c',
    '28': 'tx_wb_14b2rm'
}

tx_oil_gas_key_data = {
    '02': [
        '03',
        '04',
        '05',
        '06',
        '07',
        '08',
        '09',
        '10',
        '11'
    ],
    '14': [
        '15',
        '16',
        '17',
        '18',
        '19'
    ],
    '22': [
        '28'
    ],
    '21': [
    ]
}

tx_oil_gas_key_tables = [
    '02',
    '03'
    '07',
    '09',
    '14',
    '18',
    '21',
    '22'
]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def download_tx_sched_files():
    schedule_urls = [
        #"/media/21853/oildist1.txt",
        #"/media/21987/oildist1.txt",
        #"/media/22052/oildist1.txt",
        #"/media/21802/oildist1.txt",
        #"/media/21766/oildist1.txt",
        #"/media/21827/oildist1.txt",
        #"/media/21904/oildist1.txt",
        #"/media/22160/oildist1.txt",
        #"/media/22113/oildist1.txt",
        #"/media/21861/oildist10.txt",
        #"/media/21998/oildist10.txt",
        #"/media/22062/oildist10.txt",
        #"/media/21810/oildist10.txt",
        #"/media/21773/oildist10.txt",
        #"/media/21833/oildist10.txt",
        #"/media/21909/oildist10.txt",
        #"/media/22169/oildist10.txt",
        #"/media/22144/oildist10.txt",
        #"/media/22117/oildist10.txt",
        #"/media/21851/oildist2.txt",
        #"/media/21986/oildist2.txt",
        #"/media/22053/oildist2.txt",
        #"/media/21800/oildist2.txt",
        #"/media/21765/oildist2.txt",
        #"/media/21825/oildist2.txt",
        #"/media/21902/oildist2.txt",
        #"/media/22161/oildist2.txt",
        #"/media/22137/oildist2.txt",
        #"/media/22110/oildist2.txt",
        #"/media/21857/oildist3.txt",
        #"/media/21992/oildist3.txt",
        #"/media/22055/oildist3.txt",
        #"/media/21807/oildist3.txt",
        #"/media/21769/oildist3.txt",
        #"/media/21829/oildist3.txt",
        #"/media/21903/oildist3.txt",
        #"/media/22162/oildist3.txt",
        #"/media/22140/oildist3.txt",
        #"/media/22115/oildist3.txt",
        #"/media/21856/oildist4.txt",
        #"/media/21991/oildist4.txt",
        #"/media/22059/oildist4.txt",
        #"/media/21806/oildist4.txt",
        #"/media/21767/oildist4.txt",
        #"/media/21830/oildist4.txt",
        #"/media/21906/oildist4.txt",
        #"/media/22164/oildist4.txt",
        #"/media/22138/oildist4.txt",
        #"/media/22112/oildist4.txt",
        #"/media/21990/oildist5.txt",
        #"/media/22054/oildist5.txt",
        #"/media/21803/oildist5.txt",
        #"/media/21828/oildist5.txt",
        #"/media/21828/oildist5.txt",
        #"/media/21905/oildist5.txt",
        #"/media/22163/oildist5.txt",
        #"/media/22136/oildist5.txt",
        #"/media/22111/oildist5.txt",
        #"/media/21855/oildist6.txt",
        #"/media/21994/oildist6.txt",
        #"/media/22057/oildist6.txt",
        #"/media/21805/oildist6.txt",
        #"/media/21768/oildist6.txt",
        #"/media/21831/oildist6.txt",
        #"/media/21908/oildist6.txt",
        #"/media/22165/oildist6.txt",
        #"/media/22139/oildist6.txt",
        #"/media/22114/oildist6.txt",
        #"/media/21858/oildist6e.txt",
        #"/media/21993/oildist6e.txt",
        #"/media/22056/oildist6e.txt",
        #"/media/21804/oildist6e.txt",
        #"/media/21770/oildist6e.txt",
        #"/media/30285/oildist6e.txt",
        #"/media/21832/oildist6e.txt",
        #"/media/21907/oildist6e.txt",
        #"/media/22166/oildist6e.txt",
        #"/media/22141/oildist6e.txt",
        #"/media/22116/oildist6e.txt",
        #"/media/21859/oildist7b.txt",
        #"/media/21997/oildist7b.txt",
        #"/media/22060/oildist7b.txt",
        #"/media/21808/oildist7b.txt",
        #"/media/21771/oildist7b.txt",
        #"/media/30286/oildist7b.txt",
        #"/media/21838/oildist7b.txt",
        #"/media/21912/oildist7b.txt",
        #"/media/22168/oildist7b.txt",
        #"/media/22142/oildist7b.txt",
        #"/media/22119/oildist7b.txt",
        #"/media/21860/oildist7c.txt",
        #"/media/21995/oildist7c.txt",
        #"/media/22058/oildist7c.txt",
        #"/media/21809/oildist7c.txt",
        #"/media/21772/oildist7c.txt",
        #"/media/21834/oildist7c.txt",
        #"/media/21911/oildist7c.txt",
        #"/media/22167/oildist7c.txt",
        #"/media/22143/oildist7c.txt",
        #"/media/22118/oildist7c.txt",
        #"/media/21863/oildist8.txt",
        #"/media/21813/oildist8.txt",
        #"/media/21776/oildist8.txt",
        #"/media/21837/oildist8.txt",
        #"/media/21914/oildist8.txt",
        #"/media/22172/oildist8.txt",
        #"/media/22146/oildist8.txt",
        #"/media/22122/oildist8.txt",
        #"/media/21862/oildist8a.txt",
        #"/media/21999/oildist8a.txt",
        #"/media/22064/oildist8a.txt",
        #"/media/21811/oildist8a.txt",
        #"/media/21775/oildist8a.txt",
        #"/media/21835/oildist8a.txt",
        #"/media/21913/oildist8a.txt",
        #"/media/22170/oildist8a.txt",
        #"/media/22147/oildist8a.txt",
        #"/media/22120/oildist8a.txt",
        #"/media/23266/oildist8-aug13.txt",
        #"/media/21864/oildist9.txt",
        #"/media/22000/oildist9.txt",
        #"/media/22063/oildist9.txt",
        #"/media/21812/oildist9.txt",
        #"/media/21774/oildist9.txt",
        #"/media/21836/oildist9.txt",
        #"/media/21910/oildist9.txt",
        #"/media/22171/oildist9.txt",
        #"/media/22145/oildist9.txt",
        #"/media/22121/oildist9.txt",
        #"/media/23485/oildistrict8-dec2013.txt",
        #"/media/30296/oilsch1.pdf",
        #"/media/27595/oilsch1.txt",
        #"/media/39142/oilsch1.txt",
        #"/media/44715/oilsch1.txt",
        #"/media/51351/oilsch1.txt",
        #"/media/22222/oilsch1.txt",
        #"/media/29677/oilsch1.txt",
        #"/media/41132/oilsch1.txt",
        #"/media/46777/oilsch1.txt",
        #"/media/53115/oilsch1.txt",
        #"/media/25416/oilsch1.txt",
        #"/media/31387/oilsch1.txt",
        #"/media/42935/oilsch1.txt",
        #"/media/48861/oilsch1.txt",
        #"/media/48928/oilsch1.txt",
        #"/media/26846/oilsch1.txt",
        #"/media/38106/oilsch1.txt",
        #"/media/43790/oilsch1.txt",
        #"/media/50135/oilsch1.txt",
        #"/media/26214/oilsch1.txt",
        #"/media/37615/oilsch1.txt",
        #"/media/43340/oilsch1.txt",
        #"/media/49688/oilsch1.txt",
        #"/media/21534/oilsch1.txt",
        #"/media/29266/oilsch1.txt",
        #"/media/40630/oilsch1.txt",
        #"/media/46327/oilsch1.txt",
        #"/media/52803/oilsch1.txt",
        #"/media/19769/oilsch1.txt",
        #"/media/28697/oilsch1.txt",
        #"/media/40277/oilsch1.txt",
        #"/media/45864/oilsch1.txt",
        #"/media/52114/oilsch1.txt",
        #"/media/27127/oilsch1.txt",
        #"/media/38661/oilsch1.txt",
        #"/media/44269/oilsch1.txt",
        #"/media/50679/oilsch1.txt",
        #"/media/21879/oilsch1.txt",
        #"/media/28409/oilsch1.txt",
        #"/media/39649/oilsch1.txt",
        #"/media/45224/oilsch1.txt",
        #"/media/51638/oilsch1.txt",
        #"/media/24800/oilsch1.txt",
        #"/media/30963/oilsch1.txt",
        #"/media/42481/oilsch1.txt",
        #"/media/48866/oilsch1.txt",
        #"/media/24171/oilsch1.txt",
        #"/media/30454/oilsch1.txt",
        #"/media/42114/oilsch1.txt",
        #"/media/47911/oilsch1.txt",
        #"/media/54473/oilsch1.txt",
        #"/media/23162/oilsch1.txt",
        #"/media/29886/oilsch1.txt",
        #"/media/41731/oilsch1.txt",
        #"/media/47506/oilsch1.txt",
        #"/media/53896/oilsch1.txt",
        #"/media/27599/oilsch10.txt",
        #"/media/39147/oilsch10.txt",
        #"/media/44697/oilsch10.txt",
        #"/media/51354/oilsch10.txt",
        #"/media/22230/oilsch10.txt",
        #"/media/29686/oilsch10.txt",
        #"/media/41135/oilsch10.txt",
        #"/media/46783/oilsch10.txt",
        #"/media/53125/oilsch10.txt",
        #"/media/25422/oilsch10.txt",
        #"/media/31396/oilsch10.txt",
        #"/media/42940/oilsch10.txt",
        #"/media/48923/oilsch10.txt",
        #"/media/26855/oilsch10.txt",
        #"/media/38109/oilsch10.txt",
        #"/media/43791/oilsch10.txt",
        #"/media/50137/oilsch10.txt",
        #"/media/26223/oilsch10.txt",
        #"/media/37619/oilsch10.txt",
        #"/media/43344/oilsch10.txt",
        #"/media/49672/oilsch10.txt",
        #"/media/21539/oilsch10.txt",
        #"/media/29273/oilsch10.txt",
        #"/media/40637/oilsch10.txt",
        #"/media/46311/oilsch10.txt",
        #"/media/52786/oilsch10.txt",
        #"/media/19752/oilsch10.txt",
        #"/media/28702/oilsch10.txt",
        #"/media/40197/oilsch10.txt",
        #"/media/45850/oilsch10.txt",
        #"/media/52126/oilsch10.txt",
        #"/media/27136/oilsch10.txt",
        #"/media/38664/oilsch10.txt",
        #"/media/44276/oilsch10.txt",
        #"/media/50677/oilsch10.txt",
        #"/media/21886/oilsch10.txt",
        #"/media/28411/oilsch10.txt",
        #"/media/39662/oilsch10.txt",
        #"/media/45207/oilsch10.txt",
        #"/media/51639/oilsch10.txt",
        #"/media/24806/oilsch10.txt",
        #"/media/30972/oilsch10.txt",
        #"/media/42488/oilsch10.txt",
        #"/media/48863/oilsch10.txt",
        #"/media/24180/oilsch10.txt",
        #"/media/30459/oilsch10.txt",
        #"/media/42123/oilsch10.txt",
        #"/media/47918/oilsch10.txt",
        #"/media/54490/oilsch10.txt",
        #"/media/23169/oilsch10.txt",
        #"/media/29888/oilsch10.txt",
        #"/media/41716/oilsch10.txt",
        #"/media/47504/oilsch10.txt",
        #"/media/53892/oilsch10.txt",
        #"/media/26094/oilsch12.txt",
        #"/media/30294/oilsch2.pdf",
        #"/media/27594/oilsch2.txt",
        #"/media/39138/oilsch2.txt",
        #"/media/44714/oilsch2.txt",
        #"/media/51352/oilsch2.txt",
        #"/media/22221/oilsch2.txt",
        #"/media/29678/oilsch2.txt",
        #"/media/41127/oilsch2.txt",
        #"/media/46773/oilsch2.txt",
        #"/media/53117/oilsch2.txt",
        #"/media/25414/oilsch2.txt",
        #"/media/31386/oilsch2.txt",
        #"/media/42932/oilsch2.txt",
        #"/media/48930/oilsch2.txt",
        #"/media/26847/oilsch2.txt",
        #"/media/38103/oilsch2.txt",
        #"/media/43785/oilsch2.txt",
        #"/media/50132/oilsch2.txt",
        #"/media/26219/oilsch2.txt",
        #"/media/37612/oilsch2.txt",
        #"/media/43338/oilsch2.txt",
        #"/media/49686/oilsch2.txt",
        #"/media/21531/oilsch2.txt",
        #"/media/29267/oilsch2.txt",
        #"/media/40628/oilsch2.txt",
        #"/media/46308/oilsch2.txt",
        #"/media/52799/oilsch2.txt",
        #"/media/19765/oilsch2.txt",
        #"/media/28696/oilsch2.txt",
        #"/media/40276/oilsch2.txt",
        #"/media/45843/oilsch2.txt",
        #"/media/52113/oilsch2.txt",
        #"/media/27132/oilsch2.txt",
        #"/media/38659/oilsch2.txt",
        #"/media/44268/oilsch2.txt",
        #"/media/50675/oilsch2.txt",
        #"/media/21877/oilsch2.txt",
        #"/media/28408/oilsch2.txt",
        #"/media/39651/oilsch2.txt",
        #"/media/45223/oilsch2.txt",
        #"/media/51630/oilsch2.txt",
        #"/media/24796/oilsch2.txt",
        #"/media/30962/oilsch2.txt",
        #"/media/42478/oilsch2.txt",
        #"/media/48867/oilsch2.txt",
        #"/media/24172/oilsch2.txt",
        #"/media/30450/oilsch2.txt",
        #"/media/42115/oilsch2.txt",
        #"/media/47910/oilsch2.txt",
        #"/media/54471/oilsch2.txt",
        #"/media/23161/oilsch2.txt",
        #"/media/29880/oilsch2.txt",
        #"/media/41734/oilsch2.txt",
        #"/media/47497/oilsch2.txt",
        #"/media/53898/oilsch2.txt",
        #"/media/27591/oilsch3.txt",
        #"/media/39140/oilsch3.txt",
        #"/media/44696/oilsch3.txt",
        #"/media/51357/oilsch3.txt",
        #"/media/22225/oilsch3.txt",
        #"/media/29683/oilsch3.txt",
        #"/media/41130/oilsch3.txt",
        #"/media/46778/oilsch3.txt",
        #"/media/53122/oilsch3.txt",
        #"/media/25418/oilsch3.txt",
        #"/media/31389/oilsch3.txt",
        #"/media/42934/oilsch3.txt",
        #"/media/48931/oilsch3.txt",
        #"/media/26849/oilsch3.txt",
        #"/media/38105/oilsch3.txt",
        #"/media/43786/oilsch3.txt",
        #"/media/50130/oilsch3.txt",
        #"/media/26218/oilsch3.txt",
        #"/media/37610/oilsch3.txt",
        #"/media/43342/oilsch3.txt",
        #"/media/49690/oilsch3.txt",
        #"/media/21537/oilsch3.txt",
        #"/media/29269/oilsch3.txt",
        #"/media/40631/oilsch3.txt",
        #"/media/46310/oilsch3.txt",
        #"/media/52801/oilsch3.txt",
        #"/media/19768/oilsch3.txt",
        #"/media/28699/oilsch3.txt",
        #"/media/40188/oilsch3.txt",
        #"/media/45848/oilsch3.txt",
        #"/media/52121/oilsch3.txt",
        #"/media/27131/oilsch3.txt",
        #"/media/38662/oilsch3.txt",
        #"/media/44266/oilsch3.txt",
        #"/media/50678/oilsch3.txt",
        #"/media/21881/oilsch3.txt",
        #"/media/28402/oilsch3.txt",
        #"/media/39653/oilsch3.txt",
        #"/media/45205/oilsch3.txt",
        #"/media/51633/oilsch3.txt",
        #"/media/24799/oilsch3.txt",
        #"/media/30969/oilsch3.txt",
        #"/media/42486/oilsch3.txt",
        #"/media/48872/oilsch3.txt",
        #"/media/24173/oilsch3.txt",
        #"/media/30453/oilsch3.txt",
        #"/media/42119/oilsch3.txt",
        #"/media/47913/oilsch3.txt",
        #"/media/54474/oilsch3.txt",
        #"/media/23165/oilsch3.txt",
        #"/media/29884/oilsch3.txt",
        #"/media/41733/oilsch3.txt",
        #"/media/47499/oilsch3.txt",
        #"/media/53894/oilsch3.txt",
        #"/media/27590/oilsch4.txt",
        #"/media/39141/oilsch4.txt",
        #"/media/44694/oilsch4.txt",
        #"/media/51350/oilsch4.txt",
        #"/media/22224/oilsch4.txt",
        #"/media/29680/oilsch4.txt",
        #"/media/41129/oilsch4.txt",
        #"/media/46776/oilsch4.txt",
        #"/media/53119/oilsch4.txt",
        #"/media/25415/oilsch4.txt",
        #"/media/31394/oilsch4.txt",
        #"/media/42930/oilsch4.txt",
        #"/media/48932/oilsch4.txt",
        #"/media/26850/oilsch4.txt",
        #"/media/38104/oilsch4.txt",
        #"/media/43789/oilsch4.txt",
        #"/media/50339/oilsch4.txt",
        #"/media/26216/oilsch4.txt",
        #"/media/37611/oilsch4.txt",
        #"/media/43339/oilsch4.txt",
        #"/media/49689/oilsch4.txt",
        #"/media/21536/oilsch4.txt",
        #"/media/29270/oilsch4.txt",
        #"/media/40626/oilsch4.txt",
        #"/media/46306/oilsch4.txt",
        #"/media/52800/oilsch4.txt",
        #"/media/19766/oilsch4.txt",
        #"/media/28698/oilsch4.txt",
        #"/media/40192/oilsch4.txt",
        #"/media/45844/oilsch4.txt",
        #"/media/52118/oilsch4.txt",
        #"/media/27133/oilsch4.txt",
        #"/media/38660/oilsch4.txt",
        #"/media/44271/oilsch4.txt",
        #"/media/50674/oilsch4.txt",
        #"/media/21880/oilsch4.txt",
        #"/media/28401/oilsch4.txt",
        #"/media/39655/oilsch4.txt",
        #"/media/45203/oilsch4.txt",
        #"/media/51632/oilsch4.txt",
        #"/media/24798/oilsch4.txt",
        #"/media/30966/oilsch4.txt",
        #"/media/42480/oilsch4.txt",
        #"/media/48871/oilsch4.txt",
        #"/media/24174/oilsch4.txt",
        #"/media/30451/oilsch4.txt",
        #"/media/42116/oilsch4.txt",
        #"/media/47908/oilsch4.txt",
        #"/media/54491/oilsch4.txt",
        #"/media/23163/oilsch4.txt",
        #"/media/29883/oilsch4.txt",
        #"/media/41732/oilsch4.txt",
        #"/media/47502/oilsch4.txt",
        #"/media/53890/oilsch4.txt",
        #"/media/21854/oilsch5.txt",
        #"/media/27592/oilsch5.txt",
        #"/media/39143/oilsch5.txt",
        #"/media/44693/oilsch5.txt",
        #"/media/51348/oilsch5.txt",
        #"/media/22223/oilsch5.txt",
        #"/media/29679/oilsch5.txt",
        #"/media/41128/oilsch5.txt",
        #"/media/46774/oilsch5.txt",
        #"/media/53114/oilsch5.txt",
        #"/media/25413/oilsch5.txt",
        #"/media/31388/oilsch5.txt",
        #"/media/42928/oilsch5.txt",
        #"/media/48920/oilsch5.txt",
        #"/media/26848/oilsch5.txt",
        #"/media/38102/oilsch5.txt",
        #"/media/43784/oilsch5.txt",
        #"/media/50131/oilsch5.txt",
        #"/media/21764/oilsch5.txt",
        #"/media/26215/oilsch5.txt",
        #"/media/37613/oilsch5.txt",
        #"/media/43336/oilsch5.txt",
        #"/media/49667/oilsch5.txt",
        #"/media/21532/oilsch5.txt",
        #"/media/29278/oilsch5.txt",
        #"/media/40625/oilsch5.txt",
        #"/media/40625/oilsch5.txt",
        #"/media/46304/oilsch5.txt",
        #"/media/52796/oilsch5.txt",
        #"/media/19744/oilsch5.txt",
        #"/media/28693/oilsch5.txt",
        #"/media/40278/oilsch5.txt",
        #"/media/45840/oilsch5.txt",
        #"/media/52116/oilsch5.txt",
        #"/media/27128/oilsch5.txt",
        #"/media/38657/oilsch5.txt",
        #"/media/44267/oilsch5.txt",
        #"/media/50672/oilsch5.txt",
        #"/media/21878/oilsch5.txt",
        #"/media/28406/oilsch5.txt",
        #"/media/39654/oilsch5.txt",
        #"/media/45201/oilsch5.txt",
        #"/media/51629/oilsch5.txt",
        #"/media/24801/oilsch5.txt",
        #"/media/30965/oilsch5.txt",
        #"/media/42476/oilsch5.txt",
        #"/media/48870/oilsch5.txt",
        #"/media/24175/oilsch5.txt",
        #"/media/30452/oilsch5.txt",
        #"/media/42113/oilsch5.txt",
        #"/media/47906/oilsch5.txt",
        #"/media/54472/oilsch5.txt",
        #"/media/23164/oilsch5.txt",
        #"/media/29879/oilsch5.txt",
        #"/media/41710/oilsch5.txt",
        #"/media/47498/oilsch5.txt",
        #"/media/53893/oilsch5.txt",
        #"/media/27593/oilsch6.txt",
        #"/media/39144/oilsch6.txt",
        #"/media/44691/oilsch6.txt",
        #"/media/51349/oilsch6.txt",
        #"/media/22226/oilsch6.txt",
        #"/media/29681/oilsch6.txt",
        #"/media/41131/oilsch6.txt",
        #"/media/46775/oilsch6.txt",
        #"/media/53116/oilsch6.txt",
        #"/media/25417/oilsch6.txt",
        #"/media/31390/oilsch6.txt",
        #"/media/42933/oilsch6.txt",
        #"/media/48922/oilsch6.txt",
        #"/media/26851/oilsch6.txt",
        #"/media/38107/oilsch6.txt",
        #"/media/43787/oilsch6.txt",
        #"/media/50134/oilsch6.txt",
        #"/media/26217/oilsch6.txt",
        #"/media/37616/oilsch6.txt",
        #"/media/43341/oilsch6.txt",
        #"/media/49666/oilsch6.txt",
        #"/media/21535/oilsch6.txt",
        #"/media/29279/oilsch6.txt",
        #"/media/40627/oilsch6.txt",
        #"/media/46307/oilsch6.txt",
        #"/media/52797/oilsch6.txt",
        #"/media/19767/oilsch6.txt",
        #"/media/28694/oilsch6.txt",
        #"/media/40279/oilsch6.txt",
        #"/media/45845/oilsch6.txt",
        #"/media/52117/oilsch6.txt",
        #"/media/27130/oilsch6.txt",
        #"/media/38658/oilsch6.txt",
        #"/media/44270/oilsch6.txt",
        #"/media/50673/oilsch6.txt",
        #"/media/21882/oilsch6.txt",
        #"/media/28407/oilsch6.txt",
        #"/media/39664/oilsch6.txt",
        #"/media/45202/oilsch6.txt",
        #"/media/51631/oilsch6.txt",
        #"/media/24803/oilsch6.txt",
        #"/media/30967/oilsch6.txt",
        #"/media/42477/oilsch6.txt",
        #"/media/48874/oilsch6.txt",
        #"/media/24177/oilsch6.txt",
        #"/media/30449/oilsch6.txt",
        #"/media/42117/oilsch6.txt",
        #"/media/47907/oilsch6.txt",
        #"/media/54475/oilsch6.txt",
        #"/media/23166/oilsch6.txt",
        #"/media/29882/oilsch6.txt",
        #"/media/41713/oilsch6.txt",
        #"/media/47501/oilsch6.txt",
        #"/media/53889/oilsch6.txt",
        #"/media/27596/oilsch6e.txt",
        #"/media/39145/oilsch6e.txt",
        #"/media/44692/oilsch6e.txt",
        #"/media/51353/oilsch6e.txt",
        #"/media/22227/oilsch6e.txt",
        #"/media/29682/oilsch6e.txt",
        #"/media/41133/oilsch6e.txt",
        #"/media/46779/oilsch6e.txt",
        #"/media/53124/oilsch6e.txt",
        #"/media/25419/oilsch6e.txt",
        #"/media/31391/oilsch6e.txt",
        #"/media/42931/oilsch6e.txt",
        #"/media/48921/oilsch6e.txt",
        #"/media/26852/oilsch6e.txt",
        #"/media/38108/oilsch6e.txt",
        #"/media/43788/oilsch6e.txt",
        #"/media/50133/oilsch6e.txt",
        #"/media/26220/oilsch6e.txt",
        #"/media/37614/oilsch6e.txt",
        #"/media/43343/oilsch6e.txt",
        #"/media/49668/oilsch6e.txt",
        #"/media/21533/oilsch6e.txt",
        #"/media/29268/oilsch6e.txt",
        #"/media/40629/oilsch6e.txt",
        #"/media/46305/oilsch6e.txt",
        #"/media/52795/oilsch6e.txt",
        #"/media/19781/oilsch6e.txt",
        #"/media/28695/oilsch6e.txt",
        #"/media/40181/oilsch6e.txt",
        #"/media/45841/oilsch6e.txt",
        #"/media/52115/oilsch6e.txt",
        #"/media/27129/oilsch6e.txt",
        #"/media/38663/oilsch6e.txt",
        #"/media/44272/oilsch6e.txt",
        #"/media/50676/oilsch6e.txt",
        #"/media/21883/oilsch6e.txt",
        #"/media/28405/oilsch6e.txt",
        #"/media/39656/oilsch6e.txt",
        #"/media/45200/oilsch6e.txt",
        #"/media/51640/oilsch6e.txt",
        #"/media/24802/oilsch6e.txt",
        #"/media/30968/oilsch6e.txt",
        #"/media/42479/oilsch6e.txt",
        #"/media/48862/oilsch6e.txt",
        #"/media/24176/oilsch6e.txt",
        #"/media/30455/oilsch6e.txt",
        #"/media/42118/oilsch6e.txt",
        #"/media/47909/oilsch6e.txt",
        #"/media/54488/oilsch6e.txt",
        #"/media/23167/oilsch6e.txt",
        #"/media/29881/oilsch6e.txt",
        #"/media/41711/oilsch6e.txt",
        #"/media/47500/oilsch6e.txt",
        #"/media/53895/oilsch6e.txt",
        #"/media/27597/oilsch7b.txt",
        #"/media/39146/oilsch7b.txt",
        #"/media/44698/oilsch7b.txt",
        #"/media/51359/oilsch7b.txt",
        #"/media/22228/oilsch7b.txt",
        #"/media/29685/oilsch7b.txt",
        #"/media/41136/oilsch7b.txt",
        #"/media/46780/oilsch7b.txt",
        #"/media/53120/oilsch7b.txt",
        #"/media/25420/oilsch7b.txt",
        #"/media/31392/oilsch7b.txt",
        #"/media/42937/oilsch7b.txt",
        #"/media/48924/oilsch7b.txt",
        #"/media/26853/oilsch7b.txt",
        #"/media/38110/oilsch7b.txt",
        #"/media/43792/oilsch7b.txt",
        #"/media/50136/oilsch7b.txt",
        #"/media/26221/oilsch7b.txt",
        #"/media/37618/oilsch7b.txt",
        #"/media/43345/oilsch7b.txt",
        #"/media/49670/oilsch7b.txt",
        #"/media/21540/oilsch7b.txt",
        #"/media/29275/oilsch7b.txt",
        #"/media/40632/oilsch7b.txt",
        #"/media/46309/oilsch7b.txt",
        #"/media/52779/oilsch7b.txt",
        #"/media/19771/oilsch7b.txt",
        #"/media/28700/oilsch7b.txt",
        #"/media/40190/oilsch7b.txt",
        #"/media/45842/oilsch7b.txt",
        #"/media/52123/oilsch7b.txt",
        #"/media/27134/oilsch7b.txt",
        #"/media/38665/oilsch7b.txt",
        #"/media/44273/oilsch7b.txt",
        #"/media/50688/oilsch7b.txt",
        #"/media/21884/oilsch7b.txt",
        #"/media/28404/oilsch7b.txt",
        #"/media/39657/oilsch7b.txt",
        #"/media/45206/oilsch7b.txt",
        #"/media/51636/oilsch7b.txt",
        #"/media/24809/oilsch7b.txt",
        #"/media/30970/oilsch7b.txt",
        #"/media/42482/oilsch7b.txt",
        #"/media/48864/oilsch7b.txt",
        #"/media/24178/oilsch7b.txt",
        #"/media/30457/oilsch7b.txt",
        #"/media/42121/oilsch7b.txt",
        #"/media/47912/oilsch7b.txt",
        #"/media/54476/oilsch7b.txt",
        #"/media/23170/oilsch7b.txt",
        #"/media/29885/oilsch7b.txt",
        #"/media/41712/oilsch7b.txt",
        #"/media/47509/oilsch7b.txt",
        #"/media/53905/oilsch7b.txt",
        #"/media/27598/oilsch7c.txt",
        #"/media/39149/oilsch7c.txt",
        #"/media/44695/oilsch7c.txt",
        #"/media/51355/oilsch7c.txt",
        #"/media/22229/oilsch7c.txt",
        #"/media/29684/oilsch7c.txt",
        #"/media/41134/oilsch7c.txt",
        #"/media/41134/oilsch7c.txt",
        #"/media/46781/oilsch7c.txt",
        #"/media/53128/oilsch7c.txt",
        #"/media/25421/oilsch7c.txt",
        #"/media/31393/oilsch7c.txt",
        #"/media/42936/oilsch7c.txt",
        #"/media/48925/oilsch7c.txt",
        #"/media/26854/oilsch7c.txt",
        #"/media/38112/oilsch7c.txt",
        #"/media/43793/oilsch7c.txt",
        #"/media/50138/oilsch7c.txt",
        #"/media/26224/oilsch7c.txt",
        #"/media/37617/oilsch7c.txt",
        #"/media/43346/oilsch7c.txt",
        #"/media/21538/oilsch7c.txt",
        #"/media/29271/oilsch7c.txt",
        #"/media/40633/oilsch7c.txt",
        #"/media/40633/oilsch7c.txt",
        #"/media/46314/oilsch7c.txt",
        #"/media/52785/oilsch7c.txt",
        #"/media/19770/oilsch7c.txt",
        #"/media/28701/oilsch7c.txt",
        #"/media/40194/oilsch7c.txt",
        #"/media/45847/oilsch7c.txt",
        #"/media/52119/oilsch7c.txt",
        #"/media/27135/oilsch7c.txt",
        #"/media/38666/oilsch7c.txt",
        #"/media/44275/oilsch7c.txt",
        #"/media/50681/oilsch7c.txt",
        #"/media/21885/oilsch7c.txt",
        #"/media/28400/oilsch7c.txt",
        #"/media/39658/oilsch7c.txt",
        #"/media/45204/oilsch7c.txt",
        #"/media/51635/oilsch7c.txt",
        #"/media/24804/oilsch7c.txt",
        #"/media/30971/oilsch7c.txt",
        #"/media/42483/oilsch7c.txt",
        #"/media/48865/oilsch7c.txt",
        #"/media/24179/oilsch7c.txt",
        #"/media/30456/oilsch7c.txt",
        #"/media/42120/oilsch7c.txt",
        #"/media/47914/oilsch7c.txt",
        #"/media/54487/oilsch7c.txt",
        #"/media/23168/oilsch7c.txt",
        #"/media/29887/oilsch7c.txt",
        #"/media/41714/oilsch7c.txt",
        #"/media/47507/oilsch7c.txt",
        #"/media/53908/oilsch7c.txt",
        #"/media/49778/oilsch7c-2.txt",
        #"/media/27601/oilsch8.txt",
        #"/media/39150/oilsch8.txt",
        #"/media/44705/oilsch8.txt",
        #"/media/51360/oilsch8.txt",
        #"/media/22233/oilsch8.txt",
        #"/media/29689/oilsch8.txt",
        #"/media/41149/oilsch8.txt",
        #"/media/46797/oilsch8.txt",
        #"/media/53138/oilsch8.txt",
        #"/media/25425/oilsch8.txt",
        #"/media/31398/oilsch8.txt",
        #"/media/42939/oilsch8.txt",
        #"/media/48929/oilsch8.txt",
        #"/media/26858/oilsch8.txt",
        #"/media/38114/oilsch8.txt",
        #"/media/43800/oilsch8.txt",
        #"/media/50145/oilsch8.txt",
        #"/media/26225/oilsch8.txt",
        #"/media/37622/oilsch8.txt",
        #"/media/43349/oilsch8.txt",
        #"/media/49677/oilsch8.txt",
        #"/media/21543/oilsch8.txt",
        #"/media/29274/oilsch8.txt",
        #"/media/40635/oilsch8.txt",
        #"/media/46328/oilsch8.txt",
        #"/media/52802/oilsch8.txt",
        #"/media/19778/oilsch8.txt",
        #"/media/28705/oilsch8.txt",
        #"/media/40203/oilsch8.txt",
        #"/media/45846/oilsch8.txt",
        #"/media/52133/oilsch8.txt",
        #"/media/27139/oilsch8.txt",
        #"/media/38669/oilsch8.txt",
        #"/media/44289/oilsch8.txt",
        #"/media/50696/oilsch8.txt",
        #"/media/21889/oilsch8.txt",
        #"/media/28403/oilsch8.txt",
        #"/media/39661/oilsch8.txt",
        #"/media/45220/oilsch8.txt",
        #"/media/51648/oilsch8.txt",
        #"/media/24808/oilsch8.txt",
        #"/media/30975/oilsch8.txt",
        #"/media/42485/oilsch8.txt",
        #"/media/48873/oilsch8.txt",
        #"/media/24183/oilsch8.txt",
        #"/media/30460/oilsch8.txt",
        #"/media/42129/oilsch8.txt",
        #"/media/47915/oilsch8.txt",
        #"/media/54493/oilsch8.txt",
        #"/media/23173/oilsch8.txt",
        #"/media/29891/oilsch8.txt",
        #"/media/41727/oilsch8.txt",
        #"/media/47521/oilsch8.txt",
        #"/media/53913/oilsch8.txt",
        #"/media/27602/oilsch8a.txt",
        #"/media/39148/oilsch8a.txt",
        #"/media/44700/oilsch8a.txt",
        #"/media/51356/oilsch8a.txt",
        #"/media/22231/oilsch8a.txt",
        #"/media/29687/oilsch8a.txt",
        #"/media/41148/oilsch8a.txt",
        #"/media/46790/oilsch8a.txt",
        #"/media/53132/oilsch8a.txt",
        #"/media/25423/oilsch8a.txt",
        #"/media/31395/oilsch8a.txt",
        #"/media/42938/oilsch8a.txt",
        #"/media/48927/oilsch8a.txt",
        #"/media/26856/oilsch8a.txt",
        #"/media/38111/oilsch8a.txt",
        #"/media/43794/oilsch8a.txt",
        #"/media/50140/oilsch8a.txt",
        #"/media/26222/oilsch8a.txt",
        #"/media/37621/oilsch8a.txt",
        #"/media/43355/oilsch8a.txt",
        #"/media/49669/oilsch8a.txt",
        #"/media/21541/oilsch8a.txt",
        #"/media/29272/oilsch8a.txt",
        #"/media/40634/oilsch8a.txt",
        #"/media/46315/oilsch8a.txt",
        #"/media/52789/oilsch8a.txt",
        #"/media/19773/oilsch8a.txt",
        #"/media/28704/oilsch8a.txt",
        #"/media/40201/oilsch8a.txt",
        #"/media/45853/oilsch8a.txt",
        #"/media/52127/oilsch8a.txt",
        #"/media/27138/oilsch8a.txt",
        #"/media/38667/oilsch8a.txt",
        #"/media/44285/oilsch8a.txt",
        #"/media/50680/oilsch8a.txt",
        #"/media/21887/oilsch8a.txt",
        #"/media/28410/oilsch8a.txt",
        #"/media/39659/oilsch8a.txt",
        #"/media/45209/oilsch8a.txt",
        #"/media/51641/oilsch8a.txt",
        #"/media/24805/oilsch8a.txt",
        #"/media/30973/oilsch8a.txt",
        #"/media/42484/oilsch8a.txt",
        #"/media/48869/oilsch8a.txt",
        "/media/24181/oilsch8a.txt",
        "/media/30458/oilsch8a.txt",
        "/media/42122/oilsch8a.txt",
        "/media/47916/oilsch8a.txt",
        "/media/54489/oilsch8a.txt",
        "/media/23171/oilsch8a.txt",
        "/media/29889/oilsch8a.txt",
        "/media/41715/oilsch8a.txt",
        "/media/47503/oilsch8a.txt",
        "/media/47503/oilsch8a.txt",
        "/media/53899/oilsch8a.txt",
        "/media/27600/oilsch9.txt",
        "/media/39151/oilsch9.txt",
        "/media/44701/oilsch9.txt",
        "/media/51358/oilsch9.txt",
        "/media/22232/oilsch9.txt",
        "/media/29688/oilsch9.txt",
        "/media/41138/oilsch9.txt",
        "/media/46785/oilsch9.txt",
        "/media/53123/oilsch9.txt",
        "/media/25424/oilsch9.txt",
        "/media/31397/oilsch9.txt",
        "/media/30974/oilsch9.txt",
        "/media/42941/oilsch9.txt",
        "/media/48926/oilsch9.txt",
        "/media/26857/oilsch9.txt",
        "/media/38113/oilsch9.txt",
        "/media/43796/oilsch9.txt",
        "/media/50142/oilsch9.txt",
        "/media/26226/oilsch9.txt",
        "/media/37620/oilsch9.txt",
        "/media/43347/oilsch9.txt",
        "/media/49671/oilsch9.txt",
        "/media/21542/oilsch9.txt",
        "/media/29276/oilsch9.txt",
        "/media/40638/oilsch9.txt",
        "/media/46317/oilsch9.txt",
        "/media/52780/oilsch9.txt",
        "/media/19775/oilsch9.txt",
        "/media/28703/oilsch9.txt",
        "/media/40200/oilsch9.txt",
        "/media/45856/oilsch9.txt",
        "/media/52128/oilsch9.txt",
        "/media/27137/oilsch9.txt",
        "/media/38668/oilsch9.txt",
        "/media/44278/oilsch9.txt",
        "/media/50684/oilsch9.txt",
        "/media/21888/oilsch9.txt",
        "/media/28412/oilsch9.txt",
        "/media/39660/oilsch9.txt",
        "/media/45210/oilsch9.txt",
        "/media/51637/oilsch9.txt",
        "/media/24807/oilsch9.txt",
        "/media/30974/oilsch9.txt",
        "/media/30974/oilsch9.txt",
        "/media/42487/oilsch9.txt",
        "/media/48868/oilsch9.txt",
        "/media/24182/oilsch9.txt",
        "/media/30461/oilsch9.txt",
        "/media/42124/oilsch9.txt",
        "/media/47921/oilsch9.txt",
        "/media/54477/oilsch9.txt",
        "/media/23172/oilsch9.txt",
        "/media/29890/oilsch9.txt",
        "/media/41717/oilsch9.txt",
        "/media/47519/oilsch9.txt",
        "/media/53891/oilsch9.txt"
    ]
    url = "https://www.rrc.state.tx.us"
    for schedule_url in schedule_urls:
        filename = schedule_url[7:-4].replace('/','-') + '.txt'
        out_filename = 'D:\\GlobalData\\Data\\tx_data\\tx_schedule_data\\process\\'+filename
        print url + schedule_url, out_filename
        with open(out_filename,'w') as outfile:
            output = ''
            try:
                for line in urllib2.urlopen(url + schedule_url):
                    output += line[:-1]
            except:
                try:
                    output = ''
                    for line in urllib2.urlopen(url + schedule_url):
                        output += line[:-1]
                except:
                    pass
            outfile.write(output)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_tx_historical_prod():
    sql_delete = \
    '''
    DELETE FROM tblUSWell_Texas_Historical_Production WHERE [Period]={0} AND TX_Well_ID IN (SELECT DISTINCT tx_well_id FROM tx_hist_well_prod_2 WHERE prod_year={0})
    '''
    sql_insert = \
    '''
    INSERT INTO tblUSWell_Texas_Historical_Production (WellID, tx_well_id, api_number, well_no, oil_gas_code, lease_prod_id, lease_id, lease_no, district_no, county_no, field_no, operator_no, StateID, [Period], oil_total_bbl, gas_total_mcf, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, gas_jan_mcf, gas_feb_mcf, gas_mar_mcf, gas_apr_mcf, gas_may_mcf, gas_jun_mcf, gas_jul_mcf, gas_aug_mcf, gas_sep_mcf, gas_oct_mcf, gas_nov_mcf, gas_dec_mcf)
      (SELECT DISTINCT well_id, tx_well_id, api_number, well_no, oil_gas_code, lease_prod_id, lease_id, lease_no, district_no, county_no, field_no, operator_no, state_id, prod_year, oil_total_bbl, gas_total_mcf, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, gas_jan_mcf, gas_feb_mcf, gas_mar_mcf, gas_apr_mcf, gas_may_mcf, gas_jun_mcf, gas_jul_mcf, gas_aug_mcf, gas_sep_mcf, gas_oct_mcf, gas_nov_mcf, gas_dec_mcf
       FROM tx_hist_well_prod_2 WHERE prod_year={0})
    '''
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
    prod_years = sorted(gd.get_data('prod_year', 'dbo.tx_hist_well_prod_2', server='sql_server', database='US_Wells_Texas', cursor=curr, datatype='int'))
    for prod_year in prod_years:
        print prod_year
        curr.execute(sql_delete.format(prod_year))
        gd.commit(curr)
        curr.execute(sql_insert.format(prod_year))
        gd.commit(curr)
    curr.close()
    conn.close()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def webpage_click(driver, click_config, period_option_num=None):
    for find_method, element_ref, sleep_time in click_config['click']:
        if find_method == 'id':
            print element_ref
            click_var = driver.find_element_by_id(element_ref)
            click_var.click()
        elif find_method == 'xpath':
            print element_ref
            try:
                click_var = driver.find_element_by_xpath(element_ref).click()
                sleep(sleep_time)
            except:
                print '{} skipped'.format(element_ref)
                pass

def webdrive_main(webdrive_config, headless=False):
    try:
        period_option_num = sys.argv[1]
    except:
        period_option_num = 15

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    webpage_url = webdrive_config['url']
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(webpage_url)
    webpage_click(driver, webdrive_config, period_option_num=None)
    driver.quit()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_html_data(url, html_data):
    '''
    Ex:
        url = 'http://www.drillingedge.com/alabama/wells?page=2'
        html_data = {
            'prod_year': {
                'xpath': '//*[@id="ASPxFormLayout2_ASPxGridView1_DXFREditorcol3_I"]/@value',
                'value': None
            }
        }
    '''
    response = urllib2.urlopen(url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    for param in html_data.keys():
        param_xpath = html_data[param]['xpath']
        try:
            html_val = tree.xpath(param_xpath)
            print '{}: {}'.format(x_path, html_val)

        except:
            html_val = response.read()
            print response.info()
        html_data[param]['value'] = html_val
    return html_data

def get_html(url, well_ids=[], state='', sleep_time=0, start_indx=0, end_indx=0):
    if well_ids:
        well_id_list = well_ids
    else:
        well_id_list = get_data('well_api', '{}_well_data'.format(state), debug=True)
    session = requests.Session()
    if end_indx:
        well_list = well_id_list[:end_indx]
    else:
        well_list = well_id_list
    if start_indx:
        well_list = well_list[start_indx:]
    for well_id in well_list:
        print url.format(well_id, well_id)
        if sleep_time:
            print 'sleep for {} seconds'.format(sleep_time)
            sleep(sleep_time)
        r1 = requests.get(url.format(well_id))
        with open(WELL_DATA_DIR + 'web_scrape\\{}_Web_Data\\{}-{}-{}_well_data.html'.format(state.upper(), well_id[:2], well_id[2:5], well_id[5:]), 'w') as web_text:
            web_text.write(decode_str(r1.text))

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

def extract_tx_comp_data(download_comp=False, download_ewa=False, unzip_data=False, process_ewa=False, move_files=False, store_records=False, parse_data=False, debug=False):
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

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def TX_webdrive():
    for typewell in TX_DATA['typewells']:
        tx_config = WEBDRIVE_CONFIG.copy()
        tx_config['tx_prod']['click'][0] = ('xpath', "//select[@name='searchArgs.wellTypeArg']/option[text()='{}']".format(typewell), 0)
        for district in TX_DATA['districts']:
            tx_config['tx_prod']['click'][1] = ('xpath', "//select[@name='searchArgs.districtCodeArg']/option[text()='{}']".format(district), 0)
            webdrive_main(webdrive_config=tx_config['tx_prod'], headless=False)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_TX_html(url, well_ids=[], state='', sleep_time=0, start_indx=0, end_indx=0, debug=False):
    session = requests.Session()
    if end_indx:
        well_list = well_ids[:end_indx]
    else:
        well_list = well_ids
    if start_indx:
        well_list = well_list[start_indx:]
    well_count = len(well_list)
    well_num = 1
    for api_number in well_list:
        print '{}/{}: {}'.format(well_num, well_count, url.format(api_number))
        if sleep_time:
            print 'sleep for {} seconds'.format(sleep_time)
            sleep(sleep_time)
        r1 = requests.get(url.format(api_number))
        with open(DATA_DIR + 'web_scrape\\TX_Web_Data\\field_schedules\\{}_field_sched.html'.format(api_number), 'w') as web_text:
            if debug: print r1.text
            web_text.write(decode_str(r1.text))
        well_num += 1
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------


def remove_title_lines():
    for permit_filename in os.listdir(IMPORT_CSV_DIR):
        print permit_filename
        with open(IMPORT_CSV_DIR + permit_filename) as permit_file:
            output = ''
            filelines = permit_file.readlines()
            for i in range(len(filelines)):
                if i > 3:
                    output += filelines[i]
            outfile_name = '{}{}_{}.csv'.format(EXPORT_CSV_DIR,permit_filename[:-4],random.randint(1000000,9999999))
            with open(outfile_name,'w') as permit_outfile:
                permit_outfile.write(output)

#County: MCMULLEN, Well Type: Oil Well,
#https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17&search=%7B"item"%3A%5B%7B"key"%3A"api_ft"%2C"value"%3A"00101692"%7D%5D%7D

def extract_search_data():
    for in_filename in os.listdir(RERUN_CSV_DIR):
        if in_filename[-3:] == 'csv':
            out_filename = in_filename
        else:
            out_filename = '{}_{}.csv'.format(in_filename.split('.csv')[0],random.randint(1000000,9999999))
        print '{}{} ---> {}{}'.format(RERUN_CSV_DIR, in_filename, IMPORT_CSV_DIR, out_filename)

        shutil.copy2(RERUN_CSV_DIR+in_filename, IMPORT_CSV_DIR+out_filename)
    for permit_filename in os.listdir(IMPORT_CSV_DIR):
        with open(IMPORT_CSV_DIR + permit_filename) as permit_file:
            #print permit_filename
            output = []
            filelines = permit_file.readlines()
            search_line = filelines[2]
            search_parts = search_line.split(',')
            for search_part in search_parts[:2]:
                #print search_part
                search_data = search_part.split(': ')[1]
                output.append(search_data)
            print "('{}','{}')".format(*output)

def extract_operator_data(debug=False):
    sql_update = 'UPDATE tx_permit_data SET operator="{}", operator_no={} WHERE id={}'
    conn = gd.get_connection(database='us_wells')
    curr = conn.cursor()
    well_operator_data = gd.get_data('id, operator_data', 'tx_permit_data', database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural', sql_where='operator_no IS NULL')
    data_count = len(well_operator_data)
    data_num = 1
    for id, operator_data in well_operator_data:
        try:
            data_parts = operator_data.split(' (')
            operator = ' ('.join(data_parts[:-1])
            operator_no = data_parts[-1]
            operator = operator.replace('.','').replace(',','')
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
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_oil_gas_key_id(curr, index_table, wb_table, debug=False):
    sql_update = "UPDATE {} AS a, {} AS b SET a.oil_gas_key=b.oil_gas_key, a.oil_gas_code=b.oil_gas_code, a.lease_no=b.lease_no, a.well_no=b.well_no, a.district_no=b.district_no WHERE a.file_source_line={} AND b.file_source_line={}"
    target_src_lines = gd.get_data('file_source_line', '{}'.format(wb_table), database='us_wells', cursor=curr, datatype='int')
    src_line_count   = len(target_src_lines)
    src_line_num     = 1
    if debug: print 'source_lines: {}'.format(target_src_lines)
    for source_line in target_src_lines:
        print '({}) - {}/{}: {}'.format(wb_table, src_line_num, src_line_count, source_line)
        max_source_line = gd.get_data('file_source_line AS max_source_line', '{}'.format(index_table), database='us_wells', cursor=curr, single_value=True, datatype='int', sql_where='file_source_line < {} ORDER BY file_source_line DESC LIMIT 1'.format(int(source_line)))
        if debug: print sql_update.format(wb_table, index_table, source_line, max_source_line)
        curr.execute(sql_update.format(wb_table, index_table, source_line, max_source_line))
        gd.commit(curr)
        src_line_num += 1


def update_wb_oil_gas_key_data(debug=False):
    conn = gd.get_connection(database='us_wells')
    curr = conn.cursor()
    for index_rec_key in tx_oil_gas_key_data.keys():
        index_table = tx_wb_record_tables[index_rec_key]
        for wb_table in [tx_wb_record_tables[rec_key] for rec_key in tx_oil_gas_key_data[index_rec_key] if rec_key in tx_oil_gas_key_tables]:
            update_oil_gas_key_id(curr, index_table, wb_table, debug=debug)
    curr.close()
    conn.close()


def get_comp_3_cols(data_comm='oil'):
    comp_3_data_ = {}
    for rec_key in rec_comp_3_data[data_comm].keys():
        rec_comp_3_cols = []
        for start_indx, data_len in rec_comp_3_data[data_comm][rec_key]:
            rec_comp_3_cols += range(start_indx, start_indx + data_len)
        hex_rec_key = 'f{}f{}'.format(rec_key[0], rec_key[1])
        comp_3_data_[hex_rec_key] = rec_comp_3_cols
    return comp_3_data_


def convert_file(input_dir, input_file):
    with io.open(input_dir + input_file, 'r', encoding="cp037") as ebc_file:
        for fileline in ebc_file:
            print 0, fileline
            repr(codecs.encode(fileline, 'latin-1'))


def convert_ebc_file(input_dir, output_dir, input_file, output_file, data_comm='oil', debug=False):
    output_text = ''
    input_filename = input_file[:-4]
    data_comm = input_file[3:6].lower()
    column_hex = {col: [] for col in range(1, 229)}
    with open(input_dir + input_file, 'r') as ebc_file:
        fileline_num = 1
        output_doc_num = 1
        fileline = ' ' * 228
        if '162' in input_file:
            fileline_max = 50525
        else:
            fileline_max = 51200
        while fileline_num < fileline_max:
            if fileline_num % 500 == 0:
                print '{} -- {}% processed ({}/{}) '.format(input_file, round(100 * (float(fileline_num) / float(fileline_max)), 1), fileline_num, fileline_max)
            fileline = ebc_file.read(228)
            linedata = repr(codecs.encode(fileline, "hex"))[1:]
            output_line = ''
            for col in range(1, 229):
                start_indx = (col - 1) * 2
                end_indx = (col) * 2
                hex_val = linedata[start_indx:end_indx]
                if col > 2:
                    record_key = output_line[:4]
                    if record_key in comp_3_data[data_comm].keys() and col in comp_3_data[data_comm][record_key]:
                        hex_val = comp_3_conv[hex_val]
                    elif record_key == 'f2f1':
                        if 203 < col < 210:
                            hex_val = comp_3_conv2[hex_val]
                        elif col > 221:
                            hex_val = 'f0'
                output_line += hex_val
                if debug:
                    column_hex[col].append(hex_val)
            try:
                output_line = codecs.decode(output_line, 'hex')
                output_line = output_line.decode('cp500').encode('latin-1')
                output_text += (output_line + '\n')
            except:
                with open(output_dir + '{}_'.format(fileline_num) + output_file, 'w') as outfile:
                    outfile.write(output_text)
            fileline_num += 1
    if debug:
        for col in range(1, 229):
            print 'col {}: {}'.format(col, column_hex[col])
    with open(output_dir + output_file, 'w') as outfile:
        outfile.write(output_text)


def parse_datalines(output_data, input_file):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    col_str = ', '.join(tx_oil_well_info_cols)
    var_str = ', '.join(['%s'] * len(tx_oil_well_info_cols))
    print len(tx_oil_well_info_cols), var_str.count('%s'), len(tx_oil['02'])
    sql_insert = 'INSERT INTO tx_oil_well_input ({}) VALUES ({})'.format(col_str, var_str)
    sql_record = 'INSERT INTO tx_record_data (well_root_no, district_no, lease_no, well_no, file_source, file_line_num, record_key, data_comm, record_text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    well_count = len(output_data.keys())
    well_num = 1
    for well_root_id in output_data.keys():
        well_root_no = well_root_id[2:10]
        district_no = well_root_id[12:14]
        lease_no = well_root_id[14:19]
        well_no = well_root_id[20:26]
        well_info = output_data[well_root_id]
        print 'well({}): {}/{}'.format(well_root_id[:26], well_num, well_count)
        for record_key in well_info.keys():
            well_records = well_info[record_key]
            well_rec_count = len(well_records)
            well_rec_num = 1
            for well_record, dataline_num in well_records:
                last_indx = 0
                record_data = (well_root_no, district_no, lease_no, well_no)
                if record_key == '02':
                    for i in range(len(tx_oil[record_key][:-1])):
                        segment_len = tx_oil[record_key][i][0]
                        is_comp_3 = tx_oil[record_key][i][1]
                        curr_indx = last_indx + segment_len
                        segment_rec = gd.decode_str(well_record[last_indx:curr_indx], encoding='latin-1')
                        if is_comp_3 and 0:
                            test_rec = codecs.decode(segment_rec, 'cp500').encode('cp500')
                            hex_rec = codecs.encode(test_rec, 'hex')
                            new_hex = ''
                            for col in range(len(test_rec)):
                                hex_char = hex_rec[col * 2:(col + 1) * 2].lower()
                                if hex_char in comp_3_nums.keys():
                                    hex_char = str(comp_3_nums[hex_char])
                                new_hex += hex_char
                            new_hex = codecs.decode(new_hex, 'hex').encode('latin-1')
                            segment_rec = str(int(new_hex))
                        record_data += (segment_rec,)
                        last_indx = curr_indx
                    try:
                        curr.execute(sql_insert, record_data)
                        gd.commit(curr)
                    except:
                        rec_data = ()
                        for rec in record_data:
                            try:
                                test_rec = codecs.encode(rec, 'latin-1')
                            except:
                                test_rec = codecs.decode(rec, 'cp500').encode('cp500')
                                hex_rec = codecs.encode(test_rec, 'hex')
                                new_hex = ''
                                for col in range(len(test_rec)):
                                    hex_char = hex_rec[col * 2:(col + 1) * 2]
                                    if hex_char in comp_3_nums.keys():
                                        hex_char = str(comp_3_nums[hex_char])
                                    new_hex += hex_char
                                new_hex = codecs.decode(new_hex, 'hex').encode('latin-1')
                                rec = int(new_hex)
                            rec_data += (rec,)
                        curr.execute(sql_insert, rec_data)
                        gd.commit(curr)
                else:
                    data_comm = input_file[3:6].upper()
                    record_data += (input_file, dataline_num, record_key, data_comm, well_record)
                    try:
                        curr.execute(sql_record, record_data)
                        gd.commit(curr)
                    except:
                        print 'SQL error: {} - {} - {} - {} - {} - {} - {} - {}'.format(well_root_no, district_no, lease_no, well_no, input_file, dataline_num, record_key, data_comm)
                well_rec_num += 1
        well_num += 1
    curr.close()
    conn.close()


def store_record_data(output_data, input_file):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    sql_record = 'INSERT INTO tx_{}_record_data (well_root_no, district_no, lease_no, well_no, file_source, file_line_num, record_key, data_comm, record_text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    well_count = len(output_data.keys())
    well_num = 1
    for well_root_id in output_data.keys():
        well_root_no = well_root_id[2:10]
        district_no = well_root_id[12:14]
        lease_no = well_root_id[14:20]
        well_no = well_root_id[20:26]
        well_info = output_data[well_root_id]
        print 'well({}): {}/{}'.format(well_root_id[:26], well_num, well_count)
        #for record_key in [rec_key for rec_key in well_info.keys() if rec_key not in ['01', '15']]:
        for record_key in ['21']:
            well_records = well_info[record_key]
            well_rec_count = len(well_records)
            well_rec_num = 1
            for well_record, dataline_num in well_records:
                last_indx = 0
                data_comm = input_file[3:6].upper()
                if record_key == '20' and 0:
                    try:
                        well_record = well_record.decode('utf-8')
                    except:
                        well_record = well_record.encode('utf-8')
                    test_rec = codecs.decode(well_record, 'cp500').encode('cp500')
                    rec_data = codecs.encode(test_rec, 'hex')
                    print '*' * 100
                    rec_output = ''
                    rec_print = ''
                    for col in range(1, 229):
                        start_indx = (col - 1) * 2
                        end_indx = (col) * 2
                        hex_val = rec_data[start_indx:end_indx]
                        print 1, hex_val
                        hex_rec_key = '3230'
                        if col in comp_3_data[data_comm.lower()][hex_rec_key]:
                            hex_val = comp_3_conv_[hex_val]
                            print 2, hex_val
                        rec_output += hex_val
                        rec_print += hex_val + ' '
                    print 'rec_print: {}'.format(rec_print)
                    print 'rec_output: {}'.format(rec_output)
                    rec_output = codecs.decode(rec_output, 'hex')
                    # rec_output = rec_output.decode('cp500').encode('latin-1')
                    rec_output = rec_output.encode('latin-1')
                    well_record = rec_output
                record_data = (well_root_no, district_no, lease_no, well_no, input_file, dataline_num, record_key, data_comm, well_record)
                try:
                    curr.execute(sql_record.format(data_comm), record_data)
                    gd.commit(curr)
                except:
                    try:
                        record_data = (well_root_no, district_no, lease_no, well_no, input_file, dataline_num, record_key, data_comm, (well_record[:-1].strip()).encode('utf-8'))
                        print '1 SQL error: {}-{}-{}-{}-{}-{}-{}-{}'.format(well_root_no, district_no, lease_no, well_no, input_file, dataline_num, record_key, data_comm)
                        print '1 {}'.format((sql_record.format(data_comm) % record_data).encode('utf-8'))
                    except:
                        print '2 SQL error: {}-{}-{}-{}-{}-{}-{}-{}'.format(well_root_no, district_no, lease_no, well_no, input_file, dataline_num, record_key, data_comm)
                        print '2 {}'.format((sql_record.format(data_comm) % record_data).decode('utf-8'))
                    curr.execute(sql_record.format(data_comm), record_data)
                    gd.commit(curr)
                well_rec_num += 1
        well_num += 1
    curr.close()
    conn.close()


def process_tx_oil_data(input_dir, input_file):
    output_data = {'': {record_key: [] for record_key in tx_oil.keys()}}
    with io.open(input_dir + input_file, encoding='latin-1') as tx_file:
        datalines = tx_file.readlines()
        root_segment = ''
        dataline_count = len(datalines)
        dataline_num = 1
        for dataline in datalines:
            print 'processing line: {}/{}'.format(dataline_num, dataline_count)
            record_key = dataline[:2]
            if record_key == '01':
                root_segment = dataline[:112]
                output_data[root_segment] = {rec_key: [] for rec_key in tx_oil.keys()}
            output_data[root_segment][record_key].append((dataline, dataline_num))
            dataline_num += 1
    parse_datalines(output_data, input_file)


def process_tx_data(input_dir, infile_temp, file_nums, data_comm):
    root_segment = ''
    for file_num in file_nums:
        input_file = infile_temp.format(file_num)
        output_data = {root_segment: {record_key: [] for record_key in tx_record_tables[data_comm].keys()}}
        with io.open(input_dir + input_file, encoding='latin-1') as tx_file:
            datalines = tx_file.readlines()
            dataline_count = len(datalines)
            dataline_num = 1
            last_dataline = ''
            for dataline in datalines:
                print 'processing line: {}/{}'.format(dataline_num, dataline_count)
                record_key = dataline[:2]
                if record_key == '01':
                    root_segment = dataline[:112]
                    output_data[root_segment] = {rec_key: [] for rec_key in tx_record_tables[data_comm].keys()}
                try:
                    output_data[root_segment][record_key].append((dataline, dataline_num))
                except:
                    output_data[root_segment][last_dataline[:2]][-1][0] += dataline
                last_dataline = dataline
                dataline_num += 1
        store_record_data(output_data, input_file)


def store_wb_record_data(output_data, input_file, root_segments):
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
    sql_record = 'INSERT INTO tx_wellbore_record_data (record_key, wellbore_api_root, county_no, unique_api, district_no, total_depth, file_source, file_source_line, data_table, root_segment, record_text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    well_count = len(output_data.keys())
    well_num = 1
    for well_root_id in root_segments:
        root_segment      = well_root_id
        record_key        = well_root_id[:2]
        wellbore_api_root = well_root_id[2:10]
        county_no         = well_root_id[2:5]
        unique_api        = well_root_id[5:10]
        district_no       = well_root_id[14:16]
        total_depth       = well_root_id[28:33]
        file_source       = input_file
        well_info         = output_data[well_root_id]
        print 'well({}): {}/{}'.format(wellbore_api_root, well_num, well_count)
        for record_key in ['23']:
            well_records = well_info[record_key]
            well_rec_count = len(well_records)
            well_rec_num = 1
            for well_record, file_source_line in well_records:
                well_rec_len = len(well_record)
                try:
                    record_data = (record_key, wellbore_api_root, county_no, unique_api, district_no, total_depth, file_source, file_source_line, tx_wb_record_tables[record_key], root_segment, well_record)
                    print  '{}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}'.format(*record_data)
                    curr.execute(sql_record, record_data)
                    gd.commit(curr)
                except:
                    well_record = '*'*20
                    record_data = (record_key, wellbore_api_root, county_no, unique_api, district_no, total_depth, file_source, file_source_line, tx_wb_record_tables[record_key], root_segment, well_record)
                    print  '{}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}'.format(*record_data)
                    curr.execute(sql_record, record_data)
                    gd.commit(curr)
                well_rec_num += 1
        well_num += 1
    curr.close()
    conn.close()


def process_tx_wb_data(input_dir='D:\\Documents\\', infile_temp='dbf900_{}.txt', file_nums=['01']):
    root_segment = ''
    root_segments = []
    for file_num in file_nums:
        input_file = infile_temp.format(file_num)
        output_data = {root_segment: {record_key: [] for record_key in tx_wb_record_tables.keys()}}
        with open(input_dir + input_file) as tx_file:
            datalines = tx_file.readlines()
            dataline_count = len(datalines)
            dataline_num = 1
            last_dataline = ''
            for dataline in datalines:
                print 'processing line: {}/{}'.format(dataline_num, dataline_count)
                record_key = dataline[:2]
                if record_key == '01':
                    root_segment = dataline[:162]
                    root_segments.append(root_segment)
                    output_data[root_segment] = {rec_key: [] for rec_key in tx_wb_record_tables.keys()}
                try:
                    output_data[root_segment][record_key].append((dataline, dataline_num))
                except:
                    output_data[root_segment][last_dataline[:2]][-1][0] += dataline
                last_dataline = dataline
                dataline_num += 1
        store_wb_record_data(output_data, input_file, root_segments)


def extract_read_data(data_comm):
    record_keys = {
        'oil': [
            'WLROOT',
            'WLORPTCY',
            'WLOPRVAL',
            'WLOFRMLK',
            'WLOFRMDS',
            'WLOETEX',
            'WLOETDS',
            'WLOALTF',
            'WLOTFWL',
            'WLPHPROD',
            'WLOPVTYP',
            'WLPHBAL',
            'WLOW10',
            'WLOPVW10',
            'WLREMARK',
            'WLSEAL',
            'WLOUIC',
            'WLSB126'
        ],
        'gas': [
            'WLROOT',
            'WLREMARK',
            'WLSEAL',
            'WLGG1',
            'WLGG10',
            'WLGPVG10',
            'WLGC1',
            'WLGRPTCY',
            'WLGFRMLK',
            'WLGFRMDS',
            'WLGALTF',
            'WLGPRVAL',
            'WLGUIC',
            'WLSB126'
        ]
    }
    tape_data = {
        'oil': {rec_key: {} for rec_key in record_keys['oil']},
        'gas': {rec_key: {} for rec_key in record_keys['gas']}
    }
    with open(HEADER_FILE.format(data_comm)) as tx_file:
        datalines = tx_file.readlines()
        record_key = ''
        in_record_key_sec = 0
        in_record_col_sec = 1
        for dataline in datalines:
            if '*' * 65 in dataline:
                in_record_key_sec = (1 - in_record_key_sec)
                in_record_col_sec = (1 - in_record_col_sec)
            if 'SEGMENT_NAME:' in dataline:
                line_parts = dataline.split()
                record_key = [line_part.strip()[13:] for line_part in line_parts if 'SEGMENT_NAME:' in line_part][0]
                in_record_key_sec = 1
                in_record_col_sec = 0
            if in_record_col_sec:
                try:
                    line_parts = dataline.split()
                    if line_parts and line_parts[0] in ['02', '03', '05', '10'] and ' PIC-' in dataline and dataline[-2:] != '.\n':
                        record_segment = line_parts[1]
                        tape_data[data_comm][record_key][record_segment] = {'data_type': '', 'default_val': '', 'start_indx': 0}
                        for line_part in line_parts:
                            if 'PIC-' in line_part:
                                tape_data[data_comm][record_key][record_segment]['data_type'] = line_part.strip()
                            elif 'VALUE' in line_part:
                                tape_data[data_comm][record_key][record_segment]['default_val'] = line_part.strip()
                            elif line_part == line_parts[-1] and line_part.isdigit():
                                tape_data[data_comm][record_key][record_segment]['start_indx'] = int(line_part.strip())
                except:
                    pass

    for record_key in tape_data[data_comm].keys():
        for rec_segment in tape_data[data_comm][record_key].keys():
            rec_data = tape_data[data_comm][record_key][rec_segment]
            print '{},{},{},{},{},{}'.format(record_key, data_comm.upper(), rec_segment, rec_data['data_type'], rec_data['default_val'], rec_data['start_indx'])


def create_tx_data_tables(tx_data_table=None, data_comm='oil'):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    sql_drop = 'DROP TABLE IF EXISTS {}'
    sql_create = \
        '''
        CREATE TABLE `{0}` (
          `id` INT(11) NOT NULL AUTO_INCREMENT,
          `well_root_no` VARCHAR(8) DEFAULT NULL,
          `api_number` VARCHAR(20) DEFAULT NULL,
          `lease_no` VARCHAR(6) DEFAULT NULL,
          `well_no` VARCHAR(6) DEFAULT NULL,
          `district_no` VARCHAR(2) DEFAULT NULL,
          `oil_gas_code` CHAR(1) DEFAULT NULL,
          {1}`root_segment` VARCHAR(350) DEFAUL NULL,
          `record_text` VARCHAR(350) DEFAULT NULL,
          PRIMARY KEY (`id`),
          INDEX well_root_indx (`well_root_no`),
          INDEX well_api_indx (`api_number`),
          INDEX lease_indx (`lease_no`),
          INDEX well_no_indx (`lease_no`, `well_no`),
          INDEX district_indx (`district_no`),
          INDEX record_key_indx (`record_key`)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin-1'''
    if tx_data_table:
        tx_data_tables = [tx_data_table]
    else:
        tx_data_tables = gd.get_data(param='data_table', table='tx_header_data', database='well_data', sql_where='data_comm="{}"'.format(data_comm))
    print tx_data_tables

    for data_table in [table for table in tx_data_tables if table != 'tx_oil_rptcy']:
        col_create = ''
        tbl_schema_data = gd.get_data('column_name, sql_data_type', table='tx_header_data', sql_where='data_table="{}" ORDER BY header_position'.format(data_table), datatype='plural', database='well_data')
        for col_name, data_type in tbl_schema_data:
            col_create += '`{}` {} DEFAULT NULL,\n  '.format(col_name, data_type)
        try:
            curr.execute(sql_drop.format(data_table))
            gd.commit(curr)
            curr.execute(sql_create.format(data_table, col_create))
            gd.commit(curr)
        except:
            print sql_create.format(data_table, col_create)
    curr.close()
    conn.close()


def create_tx_wb_data_tables(tx_data_table=None):
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
    sql_drop = 'DROP TABLE IF EXISTS {}'
    sql_create = \
        '''
CREATE TABLE us_wells.`{0}` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `wellbore_api_root` VARCHAR(8) DEFAULT NULL,
  `well_root_no` VARCHAR(8) DEFAULT NULL,
  `api_number` VARCHAR(20) DEFAULT NULL,
  `lease_no` VARCHAR(6) DEFAULT NULL,
  `well_no` VARCHAR(6) DEFAULT NULL,
  `district_no` VARCHAR(2) DEFAULT NULL,
  {1}`root_segment` VARCHAR(350) DEFAULT NULL,
  `record_text` VARCHAR(350) DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX well_root_indx (`well_root_no`),
  INDEX wellbore_api_indx (`wellbore_api_root`),
  INDEX well_api_indx (`api_number`),
  INDEX lease_indx (`lease_no`),
  INDEX well_no_indx (`lease_no`, `well_no`),
  INDEX district_indx (`district_no`),
  INDEX record_key_indx (`record_key`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8'''
    if tx_data_table:
        tx_data_tables = [tx_data_table]
    else:
        tx_data_tables = gd.get_data(param='data_table', table='tx_wellbore_header_data', database='us_wells', sql_where='NOT data_table="tx_wb_root"')

    print tx_data_tables

    for data_table in tx_data_tables:
        col_create = ''
        tbl_schema_data = gd.get_data('column_name, sql_data_type', table='tx_wellbore_header_data', sql_where='data_table="{}" ORDER BY header_position'.format(data_table), datatype='plural', database='us_wells')
        for col_name, data_type in tbl_schema_data:
            col_create += '`{}` {} DEFAULT NULL,\n  '.format(col_name, data_type)
        #try:
        curr.execute(sql_drop.format(data_table))
        gd.commit(curr)
        curr.execute(sql_create.format(data_table, col_create))
        gd.commit(curr)
        #except:
        #    print sql_create.format(data_table, col_create)
    curr.close()
    conn.close()


def insert_decimal():
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    tx_data_tables = gd.get_data(param='data_table', table='tx_header_data', database='well_data', sql_where='sql_data_type LIKE "DECIMAL%"')
    for data_table in tx_data_tables:
        sql_update = "UPDATE {0} SET {1}=CONCAT(SUBSTR({1},1,LENGTH({1})-{2}), '.', SUBSTR({1}, (LENGTH({1})-{2})+1, {2}))"
        dec_col_data = gd.get_data('column_name, sql_data_type', 'tx_header_data', database='well_data', sql_where='sql_data_type LIKE "DECIMAL%"')
        for col_name, data_type in dec_col_data:
            decimal_vals = int(data_type[-2])
            curr.execute(sql_update.format(data_table, col_name, decimal_vals))
            gd.commit(curr)
    curr.close()
    conn.close()


def add_indexing_cols(update=False, debug=False):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    sql_alter = \
        '''
        ALTER TABLE {}
          ADD COLUMN well_root_no VARCHAR(8) DEFAULT NULL AFTER id,
          ADD COLUMN lease_no VARCHAR(5) DEFAULT NULL AFTER well_root_no,
          ADD COLUMN well_no VARCHAR(6) DEFAULT NULL AFTER lease_no,
          ADD COLUMN district_no VARCHAR(2) DEFAULT NULL AFTER well_no
          ADD COLUMN record_text VARCHAR(250) DEFAULT NULL;'''
    sql_update = 'UPDATE {} SET well_root_no=SUBSTR(well_root_id,3,8), lease_no=SUBSTR(well_root_id,15,5), well_no=SUBSTR(well_root_id,21,6), district_no=SUBSTR(well_root_id,13,2)'
    tx_data_tables = gd.get_data('data_table', 'tx_header_data', database='well_data')
    for data_table in tx_data_tables:
        if debug:
            print sql_alter.format(data_table)
            if update: print sql_update.format(data_table)
        curr.execute(sql_alter.format(data_table))
        gd.commit(curr)
        if update:
            curr.execute(sql_update.format(data_table))
            gd.commit(curr)
    curr.close()
    conn.close()


def insert_record_data(debug=False, data_comm='oil', tx_rec_key=None, exclude=[]):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    sql_insert = 'INSERT INTO {} (well_root_no, well_api, lease_no, well_no, district_no, record_text) (SELECT DISTINCT well_root_no, well_api, lease_no, well_no, district_no, record_text FROM tx_{}_record_data WHERE record_key="{}")'
    if tx_rec_key:
        data_table = tx_record_tables[data_comm][tx_rec_key]
        if debug:
            print sql_insert.format(data_table, data_comm, tx_rec_key)
        curr.execute(sql_insert.format(data_table, data_comm, tx_rec_key))
        gd.commit(curr)
    else:
        tx_record_keys = gd.get_data('record_key', 'tx_{}_record_data'.format(data_comm), database='well_data', sql_where='data_comm="{}"'.format(data_comm))
        for rec_key in [rkey for rkey in tx_record_keys if rkey not in exclude]:
            data_table = tx_record_tables[data_comm][rec_key]
            if debug:
                print sql_insert.format(data_table, data_comm, rec_key)
            curr.execute(sql_insert.format(data_table, data_comm, rec_key))
            gd.commit(curr)
    curr.close()
    conn.close()


def insert_wb_record_data(debug=False, tx_rec_key=None, exclude=[]):
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
    sql_insert = 'INSERT INTO {} (wellbore_api_root, api_number, root_segment, record_text, file_source_line) (SELECT DISTINCT wellbore_api_root, unique_api, root_segment, record_text, file_source_line FROM tx_wellbore_record_data WHERE record_key="{}")'
    if tx_rec_key:
        data_table = tx_wb_record_tables[tx_rec_key]
        if debug:
            print sql_insert.format(data_table, tx_rec_key)
        curr.execute(sql_insert.format(data_table, tx_rec_key))
        gd.commit(curr)
    else:
        tx_record_keys = gd.get_data('record_key', 'tx_wellbore_record_data', database='us_wells')
        for rec_key in [rkey for rkey in tx_record_keys if rkey not in exclude]:
            data_table = tx_wb_record_tables[rec_key]
            print sql_insert.format(data_table, rec_key)
            curr.execute(sql_insert.format(data_table, rec_key))
            gd.commit(curr)
    curr.close()
    conn.close()


def parse_wb_record_data(exclude=[], start_index=1, column_start=0):
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
    sql_alter = 'ALTER TABLE {} CHANGE {} {} VARCHAR({}) DEFAULT NULL'
    sql_update = 'UPDATE {} SET {}=SUBSTR(record_text,{},{})'
    sql_update_dec = 'UPDATE {} SET {}=CONCAT(SUBSTR(record_text,{},{}),".",SUBSTR(record_text,{},{}))'
    record_keys = gd.get_data('record_key', 'tx_wellbore_record_data', database='us_wells')
    start_indx = start_index
    col_start  = column_start
    for rec_key in [rkey for rkey in record_keys if rkey not in exclude]:
        record_table = tx_wb_record_tables[rec_key]
        table_data = tx_wb_table_data[record_table]
        current_index = start_indx
        for data_len, col_name, dec_plcs in table_data[col_start:-1]:
            if dec_plcs:
                data_sub_len = data_len - dec_plcs
                print sql_update_dec.format(record_table, col_name, current_index, data_sub_len, current_index + data_sub_len, dec_plcs)
                try:
                    curr.execute(sql_update_dec.format(record_table, col_name, current_index, data_sub_len, current_index + data_sub_len, dec_plcs))
                    gd.commit(curr)
                except:
                    curr.execute(sql_alter.format(record_table, col_name, col_name, data_len+1))
                    gd.commit(curr)
                    curr.execute(sql_update_dec.format(record_table, col_name, current_index, data_sub_len, current_index + data_sub_len, dec_plcs))
                    gd.commit(curr)
            else:
                print sql_update.format(record_table, col_name, current_index, data_len)
                try:
                    curr.execute(sql_update.format(record_table, col_name, current_index, data_len))
                    gd.commit(curr)
                except:
                    curr.execute(sql_alter.format(record_table, col_name, col_name, data_len+1))
                    gd.commit(curr)
                    curr.execute(sql_update.format(record_table, col_name, current_index, data_len))
                    gd.commit(curr)

            current_index += data_len
        start_indx = 1
        col_start  = 0
    curr.close()
    conn.close()


def parse_record_data(exclude=[], data_comm='oil', start_index=1, column_start=0):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    sql_update = 'UPDATE {} SET {}=SUBSTR(record_text,{},{})'
    sql_update_dec = 'UPDATE {} SET {}=CONCAT(SUBSTR(record_text,{},{}),".",SUBSTR(record_text,{},{}))'
    record_keys = gd.get_data('record_key', 'tx_{}_record_data'.format(data_comm), database='well_data', sql_where='data_comm="{}"'.format(data_comm))
    for rec_key in [rkey for rkey in record_keys if rkey not in exclude]:
        record_table = tx_record_tables[data_comm][rec_key]
        table_data = tx_table_data[record_table]
        current_index = start_index
        for data_len, col_name, dec_plcs in table_data[column_start:-1]:
            if dec_plcs:
                data_sub_len = data_len - dec_plcs
                print sql_update_dec.format(record_table, col_name, current_index, data_sub_len, current_index + data_sub_len, dec_plcs)
                curr.execute(sql_update_dec.format(record_table, col_name, current_index, data_sub_len, current_index + data_sub_len, dec_plcs))
            else:
                print sql_update.format(record_table, col_name, current_index, data_len)
                curr.execute(sql_update.format(record_table, col_name, current_index, data_len))
            gd.commit(curr)
            current_index += data_len
    curr.close()
    conn.close()


def tx_lease_to_well_prod():
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
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
    UPDATE tx_oil_well_production AS a, tx_oil_data AS c 
      SET a.oil_{0}_bbl=c.well_allowable_pct, a.csgd_{0}_mcf=c.well_allowable_pct
      WHERE c.prod_month='{0}' AND a.prod_year=c.prod_year AND a.tx_well_id=c.tx_well_id
    '''
    for prod_month in month_names:
        print sql_update.format(prod_month)
        curr.execute(sql_update.format(prod_month))
        gd.commit(curr)
    sql_update = \
    '''
    UPDATE tx_oil_well_production AS a, tx_well_production AS b, tx_oil_data AS c 
      SET a.oil_{0}_bbl=(c.well_allowable_pct * b.oil_{0}_bbl), a.csgd_{0}_mcf=(c.well_allowable_pct * b.csgd_{0}_mcf) 
      WHERE c.prod_month='{0}' AND a.prod_year=c.prod_year AND a.prod_year=b.prod_year AND a.lease_id=b.lease_id AND a.tx_well_id=c.tx_well_id
    '''
    curr.close()
    conn.close()


def process_tx_files(input_dir=HEX_FILE_DIR, output_dir=HEX_FILE_DIR, input_file=HEX_IN_FILE, output_file=HEX_OUT_FILE, data_comm='oil', record_key=None, process_wb_data=False, parse_exclude=[], column_start=0, start_index=1, insert_exclude=[], create_tbls=False, table_type='wb', tbl_name='', extract_headers=False, comp_3_cols=False, convert=False, file_nums=[], store=False, insert=False, parse=False, debug=False):
    if create_tbls:
        if table_type == 'og':
            create_tx_data_tables(tx_data_table=tbl_name, data_comm=data_comm)
        elif table_type == 'wb':
            create_tx_wb_data_tables()
    if extract_headers:
        extract_read_data(data_comm)
    if comp_3_cols:
        get_comp_3_cols(data_comm)
    if convert:
        for file_num in file_nums:
            convert_ebc_file(input_dir, output_dir, input_file.format(file_num), output_file.format(file_num), data_comm=data_comm)
    if store:
        process_tx_data(input_dir, infile_temp=HEX_OUT_FILE, file_nums=file_nums, data_comm=data_comm)
    if insert:
        if table_type == 'og':
            insert_record_data(debug=debug, data_comm=data_comm, tx_rec_key=record_key, exclude=insert_exclude)
        elif table_type == 'wb':
            insert_wb_record_data(debug=debug, tx_rec_key=record_key, exclude=insert_exclude)
    if parse:
        if table_type == 'og':
            parse_record_data(data_comm=data_comm, exclude=parse_exclude, start_index=start_index, column_start=column_start)
        elif table_type == 'wb':
            parse_wb_record_data(exclude=parse_exclude, start_index=start_index, column_start=column_start)

    if process_wb_data:
        process_tx_wb_data()


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_completion_data():
    with ftputil.FTPHost('ftp.rrc.texas.gov', 'subdata', 'WGn4t7SM') as ftp_host:
        ftp_host.chdir('CMPL_Data')
        cmpl_dirs = ftp_host.listdir(ftp_host.curdir)
        for cmpl_dir in cmpl_dirs:
            print cmpl_dir
            ftp_host.chdir(cmpl_dir)
            zipfiles = ftp_host.listdir(ftp_host.curdir)
            for zipfile in zipfiles:
                print '\t', zipfile
                if ftp_host.path.isfile(zipfile):
                    ftp_host.download(zipfile, OUTPUT_DIR+zipfile)
            ftp_host.chdir('..')


def get_well_data():
    url = 'ftp://ftpe.rrc.texas.gov/shpapidb/api/api{}.dbf'
    county_nos = get_data('county_no', 'dbo.tx_ref_well_id', database='US_Wells_Texas', server='sql_server')
    print sorted(county_nos)
    for county_no in sorted(county_nos):
        sleep(1)
        print 'Downloading well data file for county no: {} ...'.format(county_no)
        ftpfile = urllib2.urlopen(url.format(county_no))
        localfile = open(OUTPUT_DIR+'api{}.dbf'.format(county_no), "wb")
        shutil.copyfileobj(ftpfile, localfile)


def rename_api_dbf_files():
    for api_dbf_filename in os.listdir(OUTPUT_DIR):
        os.rename(OUTPUT_DIR+api_dbf_filename, OUTPUT_DIR+'')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_prev_prod(curr, debug=False):
    sql_update = \
        """
        UPDATE tx_lease_prod_schedule AS a, 
               (SELECT oil_prod_vol FROM tx_production WHERE lease_id='{0}' AND prod_date='{1}' AND tx_well_id IS NULL) AS b 
          SET a.prev_lease_oil_prod=b.oil_prod_vol
          WHERE a.lease_id='{0}' AND a.prod_date='{2}' AND a.prev_lease_oil_prod IS NULL
        """
    lease_prod_data = gd.get_data('lease_id, prod_date', 'dbo.tx_lease_prod_schedule', database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural', sql_where="NOT prod_date=lease_date_min")
    lease_prod_data_count = len(lease_prod_data)
    lease_prod_data_num = 1
    for lease_id, curr_prod_date in lease_prod_data:
        print '{}/{}: {} - {}'.format(lease_prod_data_num, lease_prod_data_count, lease_id, curr_prod_date)
        curr_prod_date_indx = PROD_DATES.index(curr_prod_date)
        prev_prod_date_indx = curr_prod_date_indx - 1
        prev_prod_date = PROD_DATES[prev_prod_date_indx]
        curr.execute(sql_update.format(lease_id, prev_prod_date, curr_prod_date))
        gd.commit(curr)
        lease_prod_data_num += 1


def calc_lease_period_prod(curr, debug=False):
    sql_update = \
        """
        UPDATE tx_oil_prod_schedule AS a,
          (SELECT SUM(oil_prod_vol) AS total_oil_lease_prod FROM tx_production_data WHERE lease_id='{0}' AND prod_date >= '{1}' AND prod_date <= '{2}') AS b 
          SET a.lease_oil_prod=b.total_oil_lease_prod 
          WHERE a.lease_id='{0}' AND a.first_production_date='{1}' AND last_production_date='{2}'
        """
    sql_update2 = \
        """
        UPDATE tx_oil_prod_schedule AS a,
          (SELECT SUM(oil_prod_vol) AS total_oil_lease_prod FROM tx_production_data WHERE lease_id='{0}' AND prod_date >= '{1}' AND prod_date <= '{2}') AS b 
          SET a.lease_oil_prod=b.total_oil_lease_prod 
          WHERE a.lease_id='{0}' AND a.first_production_date='{1}' AND last_production_date='{2}'
        """
    well_period_data = gd.get_data('lease_id, first_production_date, last_production_date', 'dbo.tx_oil_prod_schedule', database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural', sql_where="process_code={} AND IFNULL(lease_oil_prod,0)=0".format(PROCESS_CODE))
    well_period_data_count = len(well_period_data)
    well_period_data_num = 1
    for lease_id, first_prod_date, last_prod_date in well_period_data:
        print '{}/{}: {} - {} - {} - {}'.format(well_period_data_num, well_period_data_count, lease_id, first_prod_date, last_prod_date)
        curr.execute(sql_update2.format(lease_id, first_prod_date, last_prod_date))
        gd.commit(curr)
        well_period_data_num += 1


def get_prod_dates(start_date, end_date):
    start_date_indx = PROD_DATES.index(start_date)
    end_date_indx = PROD_DATES.index(end_date) + 1
    prod_dates = sorted(PROD_DATES[start_date_indx: end_date_indx])
    return prod_dates


def lease_prod_allocation(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
    prod_pct_col_str = ', '.join(PROD_PCT_COLS)
    prod_pct_var_str = ', '.join((["'{}'"] * 2) + ["{}"] * 15)
    sql_insert = "INSERT INTO tx_well_prod_pct ({}) VALUES ({})".format(prod_pct_col_str, prod_pct_var_str)
    sql_where = "process_code={}".format(PROCESS_CODE)
    lease_prod_data = gd.get_data("lease_id, lease_date_min, lease_date_max", "tx_lease_prod_schedule", database="US_Wells_Texas", server='sql_server', cursor=curr, datatype="plural", sql_where=sql_where)
    lease_prod_count = len(lease_prod_data)
    lease_prod_num = 1
    for lease_id, lease_date_min, lease_date_max in lease_prod_data:
        print '({}) -- {}/{}: {} - {} - {}'.format(gd.get_datetime(), lease_prod_num, lease_prod_count, lease_id, lease_date_min, lease_date_max)
        all_prod_dates = get_prod_dates(lease_date_min, lease_date_max)
        all_prod_years = sorted(list(set([int(prod_date[:4]) for prod_date in all_prod_dates])))
        sql_where = "lease_id='{}' AND lease_date_min='{}' AND lease_date_max='{}' AND process_code={}".format(lease_id, lease_date_min, lease_date_max, PROCESS_CODE)
        schedule_dates = gd.get_data('prod_date', 'tx_lease_prod_schedule', cursor=curr, database='US_Wells_Texas', server='sql_server', sql_where=sql_where)
        well_prod_pcts = {prod_year: {} for prod_year in all_prod_years}
        wells_online = []
        wells_offline = []
        prev_year = min([int(prod_date[:4]) for prod_date in all_prod_dates])
        for prod_date in all_prod_dates:
            prod_year = int(prod_date[:4])
            prod_month = prod_date[4:]
            prev_month = MONTH_NUMS[MONTH_NUMS.index(prod_month) - 1]
            if prev_year != prod_year:
                for well_id in wells_online:
                    well_prod_pcts[prod_year][well_id] = {month_num: 0.0 for month_num in MONTH_NUMS}
            if prod_date in schedule_dates:
                col_names = "schedule_id, prev_lease_oil_prod, curr_lease_oil_prod, oil_prod_vol_change"
                sql_where = "lease_id='{}' AND lease_date_min='{}' AND lease_date_max='{}' AND prod_date='{}' AND process_code={}".format(lease_id, lease_date_min, lease_date_max, prod_date, PROCESS_CODE)
                well_sched_data = gd.get_data(col_names, "tx_lease_prod_schedule", database='US_Wells_Texas', server='sql_server', cursor=curr, datatype="plural", sql_where=sql_where)
                for schedule_id, prev_lease_oil_prod, curr_lease_oil_prod, oil_prod_vol_change in well_sched_data:
                    begin_well_ids = gd.get_data("tx_well_id", "tx_oil_prod_schedule", database='US_Wells_Texas', server='sql_server', cursor=curr, sql_where="prod_start_id={} AND process_code={}".format(schedule_id, PROCESS_CODE))
                    end_well_ids = gd.get_data("tx_well_id", "tx_oil_prod_schedule", database='US_Wells_Texas', server='sql_server', cursor=curr, sql_where="prod_end_id={} AND process_code={}".format(schedule_id, PROCESS_CODE))
                    for well_id in begin_well_ids:
                        well_prod_pcts[prod_year][well_id] = {month_num: 0.0 for month_num in MONTH_NUMS}
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
                                    well_prod_pcts[prod_year][well_id][prod_month] = prev_prod_pct * float(prod_inc_pct - 0.02)
                                for well_id in begin_well_ids:
                                    well_prod_pcts[prod_year][well_id][prod_month] = (1 - (prod_inc_pct - 0.02)) / float(new_well_count)
                            else:
                                for well_id in wells_online:
                                    prev_prod_pct = float(well_prod_pcts[prod_year][well_id][prev_month])
                                    well_prod_pcts[prod_year][well_id][prod_month] = prev_prod_pct * float(1 - prod_inc_pct)
                                for well_id in begin_well_ids:
                                    well_prod_pcts[prod_year][well_id][prod_month] = float(prod_inc_pct) / float(new_well_count)
                    else:
                        for well_id in wells_online:
                            well_prod_pcts[prod_year][well_id][prod_month] = float(well_prod_pcts[prod_year][well_id][prev_month])
                    if len(wells_online + begin_well_ids):
                        total_prod_pct = float(sum([well_prod_pcts[prod_year][well_id][prod_month] for well_id in (wells_online + begin_well_ids)]))
                        pct_corr_factor = float(1 - total_prod_pct) / float(len(wells_online + begin_well_ids))
                        for well_id in (wells_online + begin_well_ids):
                            well_prod_pcts[prod_year][well_id][prod_month] = max(0, pct_corr_factor + well_prod_pcts[prod_year][well_id][prod_month])
                    wells_offline += end_well_ids
                    wells_online += begin_well_ids
                    wells_online = [well_id for well_id in wells_online if well_id not in wells_offline]
            else:
                producing_wells = [wellid for wellid in well_prod_pcts[prod_year].keys() if wellid in wells_online]
                for well_id in producing_wells:
                    well_prod_pcts[prod_year][well_id][prod_month] = well_prod_pcts[prod_year][well_id][prev_month]
                total_prod_pct = sum([well_prod_pcts[prod_year][well_id][prod_month] for well_id in producing_wells])
                if total_prod_pct < 1:
                    prod_pct_diff = 1 - total_prod_pct
                    for well_id in producing_wells:
                        well_prod_pcts[prod_year][well_id][prod_month] = max(0, well_prod_pcts[prod_year][well_id][prod_month] + (float(prod_pct_diff) / float(len(producing_wells))))

            # Ensure the sum of all well production percentages = 1 for the production date
            # try:
            #    assert sum([well_prod_pcts[prod_year][wellid][prod_month] for wellid in well_prod_pcts[prod_year].keys()]) in [0, 1]
            # except:
            #    print well_prod_pcts[prod_year], sum([well_prod_pcts[prod_year][wellid][prod_month] for wellid in well_prod_pcts[prod_year].keys()])
            prev_year = prod_year
        prod_year_count = len(well_prod_pcts.keys())
        prod_year_num = 1
        for lease_prod_year in sorted(well_prod_pcts.keys()):

            print '{}/{}: {}'.format(prod_year_num, prod_year_count, lease_prod_year)
            well_id_count = len(well_prod_pcts[lease_prod_year].keys())
            well_id_num = 1
            for well_id in well_prod_pcts[lease_prod_year].keys():
                well_pct_data = well_prod_pcts[lease_prod_year][well_id]
                curr.execute(sql_insert.format(lease_id, well_id, lease_prod_year, *[well_pct_data[prod_month] for prod_month in well_pct_data.keys()]))
                gd.commit(curr)
                well_id_num += 1
            prod_year_num += 1
        lease_prod_num += 1
    curr.close()
    conn.close()


def update_well_production_table(curr, debug=False):
    sql_update = \
        """
        INSERT INTO tx_well_production (lease_id, tx_well_id, prod_year, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, csgd_jan_mcf, csgd_feb_mcf, csgd_mar_mcf, csgd_apr_mcf, csgd_may_mcf, csgd_jun_mcf, csgd_jul_mcf, csgd_aug_mcf, csgd_sep_mcf, csgd_oct_mcf, csgd_nov_mcf, csgd_dec_mcf)
        (SELECT DISTINCT a.lease_id, a.tx_well_id, a.prod_year, a.jan_prod_pct*b.oil_jan_bbl AS well_oil_jan_bbl, a.feb_prod_pct*b.oil_feb_bbl AS well_oil_feb_bbl, a.mar_prod_pct*b.oil_mar_bbl AS well_oil_mar_bbl, a.apr_prod_pct*b.oil_apr_bbl AS well_oil_apr_bbl, a.may_prod_pct*b.oil_may_bbl AS well_oil_may_bbl, a.jun_prod_pct*b.oil_jun_bbl AS well_oil_jun_bbl, a.jul_prod_pct*b.oil_jul_bbl AS well_oil_jul_bbl, a.aug_prod_pct*b.oil_aug_bbl AS well_oil_aug_bbl, 
         a.sep_prod_pct*b.oil_sep_bbl AS well_oil_sep_bbl, a.oct_prod_pct*b.oil_oct_bbl AS well_oil_oct_bbl, a.nov_prod_pct*b.oil_nov_bbl AS well_oil_nov_bbl, a.dec_prod_pct*b.oil_dec_bbl AS well_oil_dec_bbl, a.jan_prod_pct*b.csgd_jan_mcf AS well_csgd_jan_mcf, a.feb_prod_pct*b.csgd_feb_mcf AS well_csgd_feb_mcf, a.mar_prod_pct*b.csgd_mar_mcf AS well_csgd_mar_mcf, a.apr_prod_pct*b.csgd_apr_mcf AS well_csgd_apr_mcf, a.may_prod_pct*b.csgd_may_mcf AS well_csgd_may_mcf, 
         a.jun_prod_pct*b.csgd_jun_mcf AS well_csgd_jun_mcf, a.jul_prod_pct*b.csgd_jul_mcf AS well_csgd_jul_mcf, a.aug_prod_pct*b.csgd_aug_mcf AS well_csgd_aug_mcf, a.sep_prod_pct*b.csgd_sep_mcf AS well_csgd_sep_mcf, a.oct_prod_pct*b.csgd_oct_mcf AS well_csgd_oct_mcf, a.nov_prod_pct*b.csgd_nov_mcf AS well_csgd_nov_mcf, a.dec_prod_pct*b.csgd_dec_mcf AS well_csgd_dec_mcf
         FROM tx_well_prod_pct AS a, tx_well_production AS b
         WHERE a.lease_id=b.lease_id)
    
        """


def tx_lease_to_well_prod(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
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
        UPDATE tx_oil_production AS a, tx_oil_field_schedule_lite AS b 
          SET a.oil_{0}_bbl=b.well_allow_pct, a.csgd_{0}_mcf=b.well_allow_pct
          WHERE b.prod_month='{0}' AND a.prod_year={1} AND b.prod_year={1} AND a.tx_well_id='{2}' AND b.tx_well_id='{2}' AND a.lease_id='{3}' AND b.lease_id='{3}' 
        '''
    well_data = gd.get_data('tx_well_id, lease_id, prod_year', 'tx_oil_production', database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural', sql_where='NOT tx_well_id IS NULL AND process_code=0')
    well_data_count = len(well_data)
    well_data_num = 1
    print well_data_count
    for tx_well_id, lease_id, prod_year in well_data:
        well_prod_months = gd.get_data('prod_month', 'tx_oil_field_schedule_lite', database='US_Wells_Texas', server='sql_server', cursor=curr, sql_where="tx_well_id='{}' AND lease_id='{}' AND prod_year={} AND well_allow_pct > 0".format(tx_well_id, lease_id, prod_year), debug=debug)
        print '{}/{} {} well_prod_months -- {}% complete'.format(well_data_num, well_data_count, len(well_prod_months), 100 * round(float(well_data_num) / float(well_data_count), 3))
        if well_prod_months:
            for prod_month in well_prod_months:
                if debug: print sql_update.format(prod_month, prod_year, tx_well_id, lease_id)
                curr.execute(sql_update.format(prod_month, prod_year, tx_well_id, lease_id))
                gd.commit(curr)
            sql_update_2 = \
                '''
                UPDATE tx_oil_production AS a, 
                   (SELECT SUM(oil_jan_bbl) AS total_oil_jan_bbl, 
                           SUM(oil_feb_bbl) AS total_oil_feb_bbl,
                           SUM(oil_mar_bbl) AS total_oil_mar_bbl,
                           SUM(oil_apr_bbl) AS total_oil_apr_bbl,
                           SUM(oil_may_bbl) AS total_oil_may_bbl,
                           SUM(oil_jun_bbl) AS total_oil_jun_bbl,
                           SUM(oil_jul_bbl) AS total_oil_jul_bbl,
                           SUM(oil_aug_bbl) AS total_oil_aug_bbl,
                           SUM(oil_sep_bbl) AS total_oil_sep_bbl,
                           SUM(oil_oct_bbl) AS total_oil_oct_bbl,
                           SUM(oil_nov_bbl) AS total_oil_nov_bbl,
                           SUM(oil_dec_bbl) AS total_oil_dec_bbl,
                           SUM(csgd_jan_mcf) AS total_csgd_jan_mcf,
                           SUM(csgd_feb_mcf) AS total_csgd_feb_mcf,
                           SUM(csgd_mar_mcf) AS total_csgd_mar_mcf,
                           SUM(csgd_apr_mcf) AS total_csgd_apr_mcf,
                           SUM(csgd_may_mcf) AS total_csgd_may_mcf,
                           SUM(csgd_jun_mcf) AS total_csgd_jun_mcf,
                           SUM(csgd_jul_mcf) AS total_csgd_jul_mcf,
                           SUM(csgd_aug_mcf) AS total_csgd_aug_mcf,
                           SUM(csgd_sep_mcf) AS total_csgd_sep_mcf,
                           SUM(csgd_oct_mcf) AS total_csgd_oct_mcf,
                           SUM(csgd_nov_mcf) AS total_csgd_nov_mcf,
                           SUM(csgd_dec_mcf) AS total_csgd_dec_mcf
                     FROM tx_production WHERE lease_id='{1}' AND prod_year={2} AND tx_well_id IS NULL) AS b  
                SET a.oil_jan_bbl=(a.oil_jan_bbl*IFNULL(b.total_oil_jan_bbl,0)),
                    a.oil_feb_bbl=(a.oil_feb_bbl*IFNULL(b.total_oil_feb_bbl,0)),
                    a.oil_mar_bbl=(a.oil_mar_bbl*IFNULL(b.total_oil_mar_bbl,0)),
                    a.oil_apr_bbl=(a.oil_apr_bbl*IFNULL(b.total_oil_apr_bbl,0)),
                    a.oil_may_bbl=(a.oil_may_bbl*IFNULL(b.total_oil_may_bbl,0)),
                    a.oil_jun_bbl=(a.oil_jun_bbl*IFNULL(b.total_oil_jun_bbl,0)),
                    a.oil_jul_bbl=(a.oil_jul_bbl*IFNULL(b.total_oil_jul_bbl,0)),
                    a.oil_aug_bbl=(a.oil_aug_bbl*IFNULL(b.total_oil_aug_bbl,0)),
                    a.oil_sep_bbl=(a.oil_sep_bbl*IFNULL(b.total_oil_sep_bbl,0)),
                    a.oil_oct_bbl=(a.oil_oct_bbl*IFNULL(b.total_oil_oct_bbl,0)),
                    a.oil_nov_bbl=(a.oil_nov_bbl*IFNULL(b.total_oil_nov_bbl,0)),
                    a.oil_dec_bbl=(a.oil_dec_bbl*IFNULL(b.total_oil_dec_bbl,0)),
                    a.csgd_jan_mcf=(a.csgd_jan_mcf*IFNULL(b.total_csgd_jan_mcf,0)),
                    a.csgd_feb_mcf=(a.csgd_feb_mcf*IFNULL(b.total_csgd_feb_mcf,0)),
                    a.csgd_mar_mcf=(a.csgd_mar_mcf*IFNULL(b.total_csgd_mar_mcf,0)),
                    a.csgd_apr_mcf=(a.csgd_apr_mcf*IFNULL(b.total_csgd_apr_mcf,0)),
                    a.csgd_may_mcf=(a.csgd_may_mcf*IFNULL(b.total_csgd_may_mcf,0)),
                    a.csgd_jun_mcf=(a.csgd_jun_mcf*IFNULL(b.total_csgd_jun_mcf,0)),
                    a.csgd_jul_mcf=(a.csgd_jul_mcf*IFNULL(b.total_csgd_jul_mcf,0)),
                    a.csgd_aug_mcf=(a.csgd_aug_mcf*IFNULL(b.total_csgd_aug_mcf,0)),
                    a.csgd_sep_mcf=(a.csgd_sep_mcf*IFNULL(b.total_csgd_sep_mcf,0)),
                    a.csgd_oct_mcf=(a.csgd_oct_mcf*IFNULL(b.total_csgd_oct_mcf,0)),
                    a.csgd_nov_mcf=(a.csgd_nov_mcf*IFNULL(b.total_csgd_nov_mcf,0)),
                    a.csgd_dec_mcf=(a.csgd_dec_mcf*IFNULL(b.total_csgd_dec_mcf,0))
                WHERE a.tx_well_id='{0}' AND a.lease_id='{1}' AND a.prod_year={2} 
                '''
            if debug: print sql_update_2.format(tx_well_id, lease_id, prod_year)
            curr.execute(sql_update_2.format(tx_well_id, lease_id, prod_year))
            gd.commit(curr)
        well_data_num += 1
    curr.close()
    conn.close()


def update_data_gaps(curr, debug=False):
    sql_update = 'UPDATE tx_oil_field_schedule_lite SET oil_allow_bbl={2}, well_portion_bbl={2} WHERE tx_well_id="{0}" AND sched_date="{1}"'
    sql_insert = 'INSERT INTO tx_oil_field_schedule_lite (tx_well_id, sched_date, oil_allow_bbl, well_portion_bbl, lease_allow_bbl, lease_prod_bbl, well_allow_pct, process_code) VALUES ("{0}", "{1}", {2}, {2}, 0, 0, 0, 3)'
    all_sched_dates = get_prod_dates('201301', '201703')
    tx_well_ids = gd.get_data('tx_well_id', 'tx_oil_field_schedule_lite', cursor=curr, database='us_wells', datatype='plural', sql_where='sched_date > "201301" AND sched_date < "201703" AND well_allow_pct > 0')
    well_prod_data = {tx_well_id: sorted([(well_data[1], well_data[2]) for well_data in all_well_data if well_data[0] == tx_well_id]) for tx_well_id in well_ids}
    well_count = len(tx_well_ids)
    well_num = 1
    for tx_well_id in tx_well_ids:
        well_sched_data = gd.get_data('sched_date, IFNULL(well_portion_bbl,0)', 'tx_oil_field_schedule_lite', cursor=curr, database='us_wells', datatype='plural', sql_where='tx_well_id="{}" AND sched_date > "201301" AND sched_date < "201703"'.format(tx_well_id))
        well_sched_dates = sorted(list(set([well_data[0] for well_data in well_sched_data])))
        well_portion_data = {well_data[0]: well_data[1] for well_data in well_sched_data}
        well_prod_dates = [well_sched_date for well_sched_date in well_sched_dates if well_portion_data[well_sched_date] > 0]
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


def update_tx_lease_details(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells')
    curr = conn.cursor()
    sql_update = "UPDATE tblUSWell_Texas_Details SET Lease_No='{}', Field_No={}, District_No='{}', Oil_Gas_Code='{}' WHERE WellID={}"
    lease_data = gd.get_data('WellID, API_Number', 'dbo.tblUSWell_Texas_Details', server='sql_server', database='US_Wells_Texas', datatype='plural', cursor=curr, sql_where="SUBSTRING(API_Number,1,1) IN ('O','G')")
    lease_count = len(lease_data)
    lease_num = 1
    for well_id, api_num in lease_data:
        print '{}/{}: {} -- {}'.format(lease_num, lease_count, well_id, api_num)
        lease_info = api_num.split('-')
        oil_gas_code = lease_info[0]
        district_no = ('0' * (2 - len(lease_info[1]))) + lease_info[1]
        lease_no = ('0' * (6 - len(lease_info[2]))) + lease_info[2]
        field_no = int(lease_info[3])
        if debug: print sql_update.format(lease_no, field_no, district_no, oil_gas_code, well_id)
        curr.execute(sql_update.format(lease_no, field_no, district_no, oil_gas_code, well_id))
        gd.commit(curr)
        lease_num += 1
    curr.close()
    conn.close()


def update_tx_well_details(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells')
    curr = conn.cursor()
    sql_update = "UPDATE tblUSWell_Texas_Details SET Lease_No='{}', District_No='{}', Oil_Gas_Code='{}', Well_No='{}' WHERE WellID={}"
    lease_data = gd.get_data('WellID, Reported_API_Number', 'dbo.tblUSWell_Texas_Details', server='sql_server', database='US_Wells_Texas', datatype='plural', cursor=curr, sql_where="SUBSTRING(API_Number,1,2)='42' AND NOT Lease_Number IS NULL AND TX_Well_ID IS NULL")
    lease_count = len(lease_data)
    lease_num = 1
    for well_id, api_num in lease_data:
        print '(1) {}/{}: {} -- {}'.format(lease_num, lease_count, well_id, api_num)
        lease_info = api_num.split('-')
        oil_gas_code = lease_info[0][0]
        lease_no = ('0' * (6 - len(lease_info[0][2:]))) + lease_info[0][2:]
        district_no = DISTRICT_DATA[lease_info[1]]
        well_no = ''.join(lease_info[3:])
        if debug: print sql_update.format(lease_no, district_no, oil_gas_code, well_no, well_id)
        curr.execute(sql_update.format(lease_no, district_no, oil_gas_code, well_no, well_id))
        gd.commit(curr)
        lease_num += 1

    sql_update = "UPDATE tblUSWell_Texas_Details SET District_No='{}', Well_No='{}' WHERE WellID={}"
    lease_data = gd.get_data('WellID, Reported_API_Number', 'dbo.tblUSWell_Texas_Details', server='sql_server', database='US_Wells_Texas', datatype='plural', cursor=curr, sql_where="SUBSTRING(API_Number,1,2)='42' AND Lease_Number IS NULL AND TX_Well_ID IS NULL")
    lease_count = len(lease_data)
    lease_num = 1
    for well_id, api_num in lease_data:
        print '(2) {}/{}: {} -- {}'.format(lease_num, lease_count, well_id, api_num)
        lease_info = api_num.split('-')
        district_no = DISTRICT_DATA[lease_info[1]]
        well_no = ''.join(lease_info[3:])
        if debug: print sql_update.format(district_no, well_no, well_id)
        curr.execute(sql_update.format(district_no, well_no, well_id))
        gd.commit(curr)
        lease_num += 1
    curr.close()
    conn.close()


def update_tx_lease_id_details(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells')
    curr = conn.cursor()
    sql_update = "UPDATE tblUSWell_Texas_Details SET Well_No='{}' WHERE WellID={}"
    lease_data = gd.get_data('WellID, Well_Name, Lease_Name', 'dbo.tblUSWell_Texas_Details', server='sql_server', database='US_Wells_Texas', datatype='plural', cursor=curr, sql_where="SUBSTRING(API_Number,1,1) IN ('O','G') AND Well_No IS NULL AND WellID > 9773432")
    lease_count = len(lease_data)
    lease_num = 1
    for well_id, well_name, lease_name in lease_data:
        print '{}/{}: {} -- {} -- {}'.format(lease_num, lease_count, well_id, well_name, lease_name)
        try:
            lease_name_len = len(lease_name)
        except:
            lease_name_len = 0
        try:
            well_no = well_name[lease_name_len:].strip()
        except:
            well_no = ''
        if debug: print sql_update.format(well_no, well_id), '\n'
        curr.execute(sql_update.format(gd.encode_str(well_no), well_id))
        gd.commit(curr)
        lease_num += 1
    curr.close()
    conn.close()


def find_curve_fit(curr=None, prod_periods=None, prod_values=None, well_life=25, yrs_before_term=3, decline_rate_type='avg', arps_params=None, prod_comm='', well_api='', debug=False):
    Qi = prod_values[0]
    xdata = np.arange(len(prod_periods))
    ydata = np.array(prod_values)
    init_params = None

    if debug:
        print prod_comm, 'prod_periods: {}'.format(prod_periods)
        print prod_comm, 'prod_values : {}'.format(prod_values)

    def decline_curve(x, b, Di):
        return float(Qi) / (1.0 + (b * Di * x)) ** (1.0 / float(b))

    def terminal_decline(x, Qt, Dt):
        Qx = Qt * (1 - Dt) ** (x + 1)
        return Qx

    if debug and 0:
        print prod_comm, "xdata:", xdata
        print prod_comm, "ydata:", ydata

    if len(prod_periods) >= (yrs_before_term * 12):
        term_decline_col = PROD_COMM_COLS[prod_comm][2]
        term_decline = gd.get_data(term_decline_col, 'dbo.tblUSWell_Parameters', sql_where="API_Number='{}'".format(well_api), server='sql_server', database='US_Wells', datatype='float', single_value=True, cursor=curr, debug=debug)
        monthly_decline = 1 - (1.0 - term_decline) ** float(1.0 / 12.0)
        if debug: print prod_comm, 'term_decline: {} --- monthly_decline: {}'.format(term_decline, monthly_decline)
        recent_prod_len = min(6, len(prod_values))
        recent_prod_vals = [prod_val for prod_val in prod_values[-recent_prod_len:] if prod_val > 0]
        recent_prod_avg = float(sum(recent_prod_vals)) / float(max(1, len(recent_prod_vals)))
        Qt = max(prod_values[-1], recent_prod_avg)
        total_prod_months = (well_life * 12)
        xdata = np.arange(well_life * 12)
        ydata = terminal_decline(xdata, Qt, monthly_decline)
        forecast_vals = ydata.tolist()
        forecast_vals = [round(float(prod_val), 2) for prod_val in forecast_vals if prod_val >= 1]
        if debug: print prod_comm, 'forecast_vals: {}'.format(forecast_vals)
    elif len(prod_periods) <= 2:
        if arps_params and sum([arps_params[prod_comm][param_name] for param_name in ["Qi", "Di", "b"]]) > 0:
            b = arps_params[prod_comm]['b']
            Di = arps_params[prod_comm]['Di']
        else:
            b = DEFAULT_b_VALUE
            Di = DFAULT_Di_VALUE
        b = min(max(0.1, b), 3)
        Di = min(max(0.05, Di), 0.9)
        xdata = np.arange(well_life * 12)
        ydata = decline_curve(xdata, b, Di)
        forecast_vals = ydata.tolist()
        forecast_vals = [round(float(prod_val), 2) for prod_val in forecast_vals if prod_val >= 1]
    else:
        if arps_params and sum([arps_params[prod_comm][param_name] for param_name in ["Qi", "Di", "b"]]) > 0:
            b = arps_params[prod_comm]['b']
            Di = arps_params[prod_comm]['Di']
            b = min(max(0.1, b), 3)
            Di = min(max(0.05, Di), 0.9)
        else:
            popt, pcov = scipy.optimize.curve_fit(decline_curve, xdata, ydata, maxfev=10000, p0=init_params)
            b, Di = popt
            b = min(max(0.1, b), 3)
            Di = min(max(0.05, Di), 0.9)
        if prod_comm in ['OIL', 'GAS']:
            sql_update = "UPDATE US_Wells.dbo.tblUSWell_Parameters SET Decline_Param_{0}_Qi={1}, Decline_Param_{0}_Di={2}, Decline_Param_{0}_b={3} WHERE API_Number='{4}'".format(prod_comm, Qi, Di, b, well_api)
            if debug: print prod_comm, sql_update
            curr.execute(sql_update)
            gd.commit(curr)
        xdata = np.arange(well_life * 12)
        ydata = decline_curve(xdata, b, Di)
        prod_vals = ydata.tolist()
        last_srcd_indx = len(prod_periods) - 1

        if debug:
            print prod_comm, 'prod_vals ({})   : {}'.format(len(prod_vals), prod_vals)
            print prod_comm, 'prod_periods ({}): {}'.format(len(prod_periods), prod_periods)
            print prod_comm, 'prod_values ({}) : {}'.format(len(prod_values), prod_values)
            print prod_comm, 'last_srcd_indx   : {}'.format(last_srcd_indx)

        # recent_prod_len  = min(6,len(prod_values))
        # recent_prod_vals = [prod_val for prod_val in prod_values[-recent_prod_len:] if prod_val > 0]
        # recent_prod_avg  = float(sum(recent_prod_vals))/float(max(1,len(recent_prod_vals)))
        # forecast_vals    = [round(float(prod_val),2) for prod_val in prod_vals if prod_val < max(recent_prod_avg,prod_values[-1])]
        forecast_vals = [round(float(prod_val), 2) for prod_val in prod_vals if prod_val < prod_values[-1]]
    all_prod_vals = prod_values + forecast_vals
    prod_months = get_prod_dates(prod_periods[-1], len(forecast_vals) + 1)[1:]
    prod_months = prod_periods + prod_months
    prod_forecast = dict(zip(prod_months, all_prod_vals))
    if debug:
        print prod_comm, 'len(prod_values)    : {}'.format(len(prod_values))
        print prod_comm, 'len(forecast_values): {}'.format(len(forecast_vals))
        print prod_comm, 'len(all_prod_vals)  : {}'.format(len(all_prod_vals))
        print prod_comm, 'len(prod_periods)   : {}'.format(len(prod_periods))
        print prod_comm, 'len(prod_months)    : {}'.format(len(prod_months))

        print prod_comm, 'all_prod_vals       : {}'.format(all_prod_vals)
        print prod_comm, 'prod_months         : {}'.format(prod_months)
        print prod_comm, 'prod_forecast       : {}'.format(prod_forecast)
        print '\n'
    return prod_forecast


def update_well_no_data(debug=False):
    conn = gd.get_connection(database='us_wells')
    curr = conn.cursor()
    sql_update_1 = "UPDATE tx_oil_well_prod_data SET well_no='{}' WHERE id={}"
    sql_update_2 = "UPDATE tx_oil_well_prod_data SET well_no='{}', process_code=2 WHERE id={}"

    lease_data = gd.get_data('id, api_number, lease_name', 'tx_oil_well_prod_data', database='US_Wells_Texas', server='sql_server', datatype='plural', cursor=curr, sql_where='process_code=1')
    lease_count = len(lease_data)
    lease_num = 1
    for id, api_num, lease_name in lease_data:
        print '{}/{}: {} -- {} -- {}'.format(lease_num, lease_count, id, api_num, lease_name)
        lease_info = lease_name.split()
        well_no = lease_info[-1]
        if ('1' in well_no or '2' in well_no or '3' in well_no or '4' in well_no or '5' in well_no or '6' in well_no or '7' in well_no or '8' in well_no or '9' in well_no or '0' in well_no) and len(well_no) <= 10:
            if api_num:
                api_well_nos = gd.get_data('well_no', 'tx_ref_well_id', database='US_Wells_Texas', server='sql_server', cursor=curr, sql_where='api_number="{}"'.format(api_num))
                if well_no in api_well_nos:
                    if debug: print sql_update_1.format(well_no, id), '\n'
                    curr.execute(sql_update_1.format(well_no, id))
                    gd.commit(curr)
                else:
                    if debug: print sql_update_2.format(well_no, id), '\n'
                    curr.execute(sql_update_2.format(well_no, id))
                    gd.commit(curr)
            else:
                if debug: print sql_update_2.format(well_no, id), '\n'
                curr.execute(sql_update_2.format(well_no, id))
                gd.commit(curr)
        else:
            print '\n'
        lease_num += 1
    curr.close()
    conn.close()


def get_well_prod_id(curr, add_indx):
    curr.execute('SELECT ISNULL(MAX(id),1) FROM US_Wells_Texas.dbo.tx_hist_well_prod')
    max_prod_id = int(curr.fetchone()[0])
    well_prod_id = max_prod_id + add_indx
    return well_prod_id


def store_comm_prod_data(curr, tx_well_id, comm_prod_data, debug=False):
    sql_insert = "INSERT INTO US_Wells_Texas.dbo.tx_hist_well_prod (id, tx_well_id, state_id, prod_year, {}, sources) VALUES ({}, '{}', '42', {}, {}, 'Historical')"
    sql_update = "UPDATE US_Wells_Texas.dbo.tx_hist_well_prod SET {} WHERE tx_well_id='{}' AND prod_year={}"
    zero_str = ', '.join(["0"] * 26)
    oil_prod_years = []
    gas_prod_years = []
    well_prod_id = get_well_prod_id(curr, 1)
    if comm_prod_data["oil"].keys():
        oil_prod_years = [int(prod_date[:4]) for prod_date in comm_prod_data["oil"].keys()]
    if comm_prod_data["gas"].keys():
        gas_prod_years = [int(prod_date[:4]) for prod_date in comm_prod_data["gas"].keys()]
    prod_years = sorted(list(set(oil_prod_years + gas_prod_years)))
    if debug or 1: print '{}: prod_years: {}'.format(tx_well_id, prod_years)
    for prod_year in prod_years:
        annual_prod = 0
        try:
            annual_prod = sum([sum([comm_prod_data[prod_comm][prod_date] for prod_date in comm_prod_data[prod_comm].keys() if int(prod_date[:4]) == prod_year]) for prod_comm in ["oil", "gas"]])
        except:
            pass
        if annual_prod > 0:
            if debug: print sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str)
            # try:
            curr.execute(sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str))
            gd.commit(curr)
            # except:
            #    try:
            #        well_prod_id = get_well_prod_id(curr, 2)
            #        curr.execute(sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str))
            #        gd.commit(curr)
            #    except:
            #        well_prod_id = get_well_prod_id(curr, 3)
            #        curr.execute(sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str))
            #        gd.commit(curr)
            well_prod_id += 1
            for comm in comm_prod_data.keys():
                comm_str_list = []
                comm_unit = COMM_UNITS[comm.lower()]
                prod_dates = [prod_date for prod_date in comm_prod_data[comm].keys() if int(prod_date[:4]) == prod_year]
                # print 'prod_dates: {}'.format(prod_dates)
                if prod_dates:
                    for prod_date in prod_dates:
                        month_name = MONTH_NAMES[prod_date[4:]]
                        month_comm_prod = float(comm_prod_data[comm][prod_date])
                        comm_str_list.append('{}_{}_{}={}'.format(comm, month_name, comm_unit, month_comm_prod))
                    comm_str = ', '.join(comm_str_list)
                    if debug: print sql_update.format(comm_str, tx_well_id, prod_year)
                    curr.execute(sql_update.format(comm_str, tx_well_id, prod_year))
                    gd.commit(curr)


def insert_missing_prod_years(curr, tx_well_id, debug=False):
    comm_prod = {'oil': 0, 'gas': 0}
    sql_insert = "INSERT INTO US_Wells_Texas.dbo.tx_hist_well_prod (id, tx_well_id, state_id, prod_year, {}, sources) VALUES ({}, '{}', '42', {}, {}, 'Estimated')"
    sql_update = "UPDATE US_Wells_Texas.dbo.tx_hist_well_prod SET {} WHERE tx_well_id='{}' AND prod_year={}"
    zero_str = ', '.join(["0"] * 26)
    well_prod_id = get_well_prod_id(curr, 1)

    sql_where = "tx_well_id='{}' AND (oil_prod_vol+gas_prod_vol) > 0 ORDER BY prod_date ASC".format(tx_well_id)
    first_prod_vals = gd.get_data('TOP 1 oil_prod_vol, gas_prod_vol, prod_date', 'US_Wells_Texas.dbo.tx_oil_well_prod_data_lite', server='sql_server', database='US_Wells_Texas', cursor=curr, datatype='plural', sql_where=sql_where, single_value=True)
    comm_prod['oil'] = float(first_prod_vals[0])
    comm_prod['gas'] = float(first_prod_vals[1])

    prod_year_limits = gd.get_data('SUBSTRING(first_production_date,1,4), SUBSTRING(last_production_date,1,4)', 'US_Wells_Texas.dbo.tx_oil_prod_schedule', server='sql_server', database='US_Wells_Texas', datatype='plural', cursor=curr, sql_where="tx_well_id='{}'".format(tx_well_id), single_value=True)
    prod_start_year = int(prod_year_limits[0])
    prod_end_year = int(prod_year_limits[1])
    well_prod_years = range(prod_start_year, prod_end_year + 1)
    hist_prod_years = gd.get_data('prod_year', 'US_Wells_Texas.dbo.tx_hist_well_prod', server='sql_server', database='US_Wells_Texas', datatype='int', cursor=curr, sql_where="tx_well_id='{}'".format(tx_well_id))
    if well_prod_years and hist_prod_years:
        prod_years = sorted([prod_year for prod_year in well_prod_years if prod_year not in hist_prod_years and prod_year < min(hist_prod_years)])
        for prod_year in prod_years:
            if debug: print sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str)
            curr.execute(sql_insert.format(prod_col_str, well_prod_id, tx_well_id, prod_year, zero_str))
            gd.commit(curr)
            well_prod_id += 1
            for comm in ['oil', 'gas']:
                comm_str_list = []
                comm_unit = COMM_UNITS[comm]
                for month_name in MONTH_NAMES.values():
                    month_comm_prod = comm_prod[comm]
                    comm_str_list.append('{}_{}_{}={}'.format(comm, month_name, comm_unit, month_comm_prod))
                    comm_str = ', '.join(comm_str_list)
                    if debug: print sql_update.format(comm_str, tx_well_id, prod_year)
                    curr.execute(sql_update.format(comm_str, tx_well_id, prod_year))
                    gd.commit(curr)


def get_hist_prod_data(curr, tx_well_id, debug=False):
    hist_prod_data = {'oil': {}, 'gas': {}}
    well_prod_data = gd.get_data('prod_date, oil_prod_vol, gas_prod_vol', 'US_Wells_Texas.dbo.tx_oil_well_prod_data_lite', server='sql_server', database='US_Wells_Texas', cursor=curr, datatype='plural', sql_where="tx_well_id='{}' AND prod_year=2019".format(tx_well_id))
    for prod_date, oil_prod_vol, gas_prod_vol in well_prod_data:
        prod_date = gd.decode_str(prod_date)
        hist_prod_data['oil'][prod_date] = oil_prod_vol
        hist_prod_data['gas'][prod_date] = gas_prod_vol
    return hist_prod_data


def get_comm_prod_data(curr, tx_well_id, debug=False):
    hist_prod_data = get_hist_prod_data(curr, tx_well_id, debug=debug)
    comm_prod_data = {}
    for comm in hist_prod_data.keys():
        comm_prod_data[comm] = {}
        comm_prod = hist_prod_data[comm]
        prod_dates = sorted([prod_dt for prod_dt in comm_prod.keys() if comm_prod[prod_dt] > 0])
        if prod_dates:
            start_date = prod_dates[0]
            end_date = prod_dates[-1]
            prod_periods = get_prod_dates(start_date, end_date)
            prod_years = []
            prod_values = []
            curr_indx = 0
            last_indx = 0
            curr_prod = 0
            last_prod = 0
            if debug: print '{}: prod_dates  : {}'.format(tx_well_id, prod_dates)
            if debug: print '{}: prod_periods: {}'.format(tx_well_id, prod_periods)
            for prod_date in prod_dates:
                prod_years.append(int(prod_date[:4]))
                last_indx = curr_indx
                curr_indx = prod_periods.index(prod_date)
                last_prod = curr_prod
                curr_prod = comm_prod[prod_date]
                if curr_indx - last_indx < 2:
                    prod_values.append(curr_prod)
                else:
                    add_points = gd.get_lin_vals((last_indx, last_prod), (curr_indx, curr_prod), (curr_indx - last_indx) + 1)[0][1:]
                    prod_values += add_points
            comm_prod_data[comm] = dict(zip(prod_periods, prod_values))
    return comm_prod_data


def generate_hist_well_prod(debug=False):
    sql_where = "process_code=5"
    tx_well_ids = gd.get_data('tx_well_id', 'dbo.tx_oil_well_prod_data_lite', server='sql_server', database='US_Wells_Texas', sql_where=sql_where, debug=debug)
    tx_well_id_count = len(tx_well_ids)
    tx_well_id_num = 1
    for tx_well_id in tx_well_ids:
        conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
        curr = conn.cursor()
        print '{}/{}: {}'.format(tx_well_id_num, tx_well_id_count, tx_well_id)
        curr.execute("SET IDENTITY_INSERT US_Wells_Texas.dbo.tx_hist_well_prod ON")
        comm_prod_data = get_comm_prod_data(curr, tx_well_id, debug=debug)
        store_comm_prod_data(curr, tx_well_id, comm_prod_data, debug=debug)
        curr.close()
        conn.close()
        tx_well_id_num += 1


def generate_missing_hist_well_prod(debug=False):
    sql_where = "tx_well_id IN (SELECT DISTINCT tx_well_id FROM tx_oil_prod_schedule WHERE process_code=1)"
    tx_well_ids = gd.get_data('tx_well_id', 'dbo.tx_hist_well_prod', server='sql_server', database='US_Wells_Texas', sql_where=sql_where, debug=debug)
    tx_well_id_count = len(tx_well_ids)
    tx_well_id_num = 1
    for tx_well_id in tx_well_ids:
        conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
        curr = conn.cursor()
        print '{}/{}: {}'.format(tx_well_id_num, tx_well_id_count, tx_well_id)
        curr.execute("SET IDENTITY_INSERT US_Wells_Texas.dbo.tx_hist_well_prod ON")
        insert_missing_prod_years(curr, tx_well_id, debug=debug)
        curr.close()
        conn.close()
        tx_well_id_num += 1


def update_hist_oil_prod(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
    sql_update_1 = \
        '''
        UPDATE tx_hist_well_prod
          SET api_number=b.api_number, well_no=b.well_no, lease_id=b.lease_id, lease_no=b.lease_no, county_no=b.county_no, field_no=b.field_no, district_no=b.district_no, oil_gas_code=b.oil_gas_code
          FROM tx_hist_well_prod a, tx_ref_well_id b
          WHERE a.tx_well_id=b.tx_well_id
        '''

    sql_update_2 = \
        '''
        UPDATE tx_hist_well_prod
          SET lease_prod_id=b.lease_prod_id
          FROM tx_hist_well_prod a, tx_oil_well_prod_data_lite b
          WHERE a.tx_well_id=b.tx_well_id
        '''

    sql_insert = \
        '''
        INSERT INTO tx_hist_oil_prod (well_id, lease_well_id, tx_well_id, api_number, well_no, oil_gas_code, lease_prod_id, lease_id, lease_no, district_no, county_no, state_id, prod_year, oil_total_bbl, gas_total_mcf, oil_jan_bbl, oil_feb_bbl, oil_mar_bbl, oil_apr_bbl, oil_may_bbl, oil_jun_bbl, oil_jul_bbl, oil_aug_bbl, oil_sep_bbl, oil_oct_bbl, oil_nov_bbl, oil_dec_bbl, gas_jan_mcf, gas_feb_mcf, gas_mar_mcf, gas_apr_mcf, gas_may_mcf, gas_jun_mcf, gas_jul_mcf, gas_aug_mcf, gas_sep_mcf, gas_oct_mcf, gas_nov_mcf, gas_dec_mcf, sources)
          (SELECT DISTINCT well_id, lease_well_id, tx_well_id, api_number, well_no, oil_gas_code, lease_prod_id, lease_id, lease_no, district_no, county_no, state_id, prod_year, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sources FROM tx_hist_well_prod)
        '''

    sql_update_main = \
        '''
        UPDATE tx_hist_oil_prod
          SET  oil_jan_bbl=ROUND(c.oil_jan_bbl*IIF(d.oil_jan_total=0,0,(b.oil_jan_bbl/d.oil_jan_total)),3),
               oil_feb_bbl=ROUND(c.oil_feb_bbl*IIF(d.oil_feb_total=0,0,(b.oil_feb_bbl/d.oil_feb_total)),3),
               oil_mar_bbl=ROUND(c.oil_mar_bbl*IIF(d.oil_mar_total=0,0,(b.oil_mar_bbl/d.oil_mar_total)),3),
               oil_apr_bbl=ROUND(c.oil_apr_bbl*IIF(d.oil_apr_total=0,0,(b.oil_apr_bbl/d.oil_apr_total)),3),
               oil_may_bbl=ROUND(c.oil_may_bbl*IIF(d.oil_may_total=0,0,(b.oil_may_bbl/d.oil_may_total)),3),
               oil_jun_bbl=ROUND(c.oil_jun_bbl*IIF(d.oil_jun_total=0,0,(b.oil_jun_bbl/d.oil_jun_total)),3),
               oil_jul_bbl=ROUND(c.oil_jul_bbl*IIF(d.oil_jul_total=0,0,(b.oil_jul_bbl/d.oil_jul_total)),3),
               oil_aug_bbl=ROUND(c.oil_aug_bbl*IIF(d.oil_aug_total=0,0,(b.oil_aug_bbl/d.oil_aug_total)),3),
               oil_sep_bbl=ROUND(c.oil_sep_bbl*IIF(d.oil_sep_total=0,0,(b.oil_sep_bbl/d.oil_sep_total)),3),
               oil_oct_bbl=ROUND(c.oil_oct_bbl*IIF(d.oil_oct_total=0,0,(b.oil_oct_bbl/d.oil_oct_total)),3),
               oil_nov_bbl=ROUND(c.oil_nov_bbl*IIF(d.oil_nov_total=0,0,(b.oil_nov_bbl/d.oil_nov_total)),3),
               oil_dec_bbl=ROUND(c.oil_dec_bbl*IIF(d.oil_dec_total=0,0,(b.oil_dec_bbl/d.oil_dec_total)),3),
              gas_jan_mcf=ROUND(c.csgd_jan_mcf*IIF(d.gas_jan_total=0,0,(b.gas_jan_mcf/d.gas_jan_total)),3),
              gas_feb_mcf=ROUND(c.csgd_feb_mcf*IIF(d.gas_feb_total=0,0,(b.gas_feb_mcf/d.gas_feb_total)),3),
              gas_mar_mcf=ROUND(c.csgd_mar_mcf*IIF(d.gas_mar_total=0,0,(b.gas_mar_mcf/d.gas_mar_total)),3),
              gas_apr_mcf=ROUND(c.csgd_apr_mcf*IIF(d.gas_apr_total=0,0,(b.gas_apr_mcf/d.gas_apr_total)),3),
              gas_may_mcf=ROUND(c.csgd_may_mcf*IIF(d.gas_may_total=0,0,(b.gas_may_mcf/d.gas_may_total)),3),
              gas_jun_mcf=ROUND(c.csgd_jun_mcf*IIF(d.gas_jun_total=0,0,(b.gas_jun_mcf/d.gas_jun_total)),3),
              gas_jul_mcf=ROUND(c.csgd_jul_mcf*IIF(d.gas_jul_total=0,0,(b.gas_jul_mcf/d.gas_jul_total)),3),
              gas_aug_mcf=ROUND(c.csgd_aug_mcf*IIF(d.gas_aug_total=0,0,(b.gas_aug_mcf/d.gas_aug_total)),3),
              gas_sep_mcf=ROUND(c.csgd_sep_mcf*IIF(d.gas_sep_total=0,0,(b.gas_sep_mcf/d.gas_sep_total)),3),
              gas_oct_mcf=ROUND(c.csgd_oct_mcf*IIF(d.gas_oct_total=0,0,(b.gas_oct_mcf/d.gas_oct_total)),3),
              gas_nov_mcf=ROUND(c.csgd_nov_mcf*IIF(d.gas_nov_total=0,0,(b.gas_nov_mcf/d.gas_nov_total)),3),
              gas_dec_mcf=ROUND(c.csgd_dec_mcf*IIF(d.gas_dec_total=0,0,(b.gas_dec_mcf/d.gas_dec_total)),3)
          FROM tx_hist_oil_prod a,
               tx_hist_well_prod b,
               tx_well_production c,
               (SELECT DISTINCT lease_prod_id,prod_year,SUM(oil_jan_bbl) AS oil_jan_total,SUM(oil_feb_bbl) AS oil_feb_total,SUM(oil_mar_bbl) AS oil_mar_total,SUM(oil_apr_bbl) AS oil_apr_total,SUM(oil_may_bbl) AS oil_may_total,SUM(oil_jun_bbl) AS oil_jun_total,SUM(oil_jul_bbl) AS oil_jul_total,SUM(oil_aug_bbl) AS oil_aug_total,SUM(oil_sep_bbl) AS oil_sep_total,SUM(oil_oct_bbl) AS oil_oct_total,SUM(oil_nov_bbl) AS oil_nov_total,SUM(oil_dec_bbl) AS oil_dec_total,SUM(gas_jan_mcf) AS gas_jan_total,SUM(gas_feb_mcf) AS gas_feb_total,SUM(gas_mar_mcf) AS gas_mar_total,SUM(gas_apr_mcf) AS gas_apr_total,SUM(gas_may_mcf) AS gas_may_total,SUM(gas_jun_mcf) AS gas_jun_total,SUM(gas_jul_mcf) AS gas_jul_total,SUM(gas_aug_mcf) AS gas_aug_total,SUM(gas_sep_mcf) AS gas_sep_total,SUM(gas_oct_mcf) AS gas_oct_total,SUM(gas_nov_mcf) AS gas_nov_total,SUM(gas_dec_mcf) AS gas_dec_total FROM tx_hist_well_prod GROUP BY lease_prod_id, prod_year) d
          WHERE a.lease_prod_id=b.lease_prod_id AND a.lease_prod_id=c.lease_prod_id AND a.lease_prod_id=d.lease_prod_id AND a.prod_year=b.prod_year AND a.prod_year=c.prod_year AND a.prod_year=d.prod_year
        '''
    # --------------------------------------------
    # if debug: print sql_update_1
    # curr.execute(sql_update_1)
    # gd.commit(curr)
    # print 'tx_hist_oil_prod update 1 complete'

    # if debug: print sql_update_2
    # curr.execute(sql_update_2)
    # gd.commit(curr)
    # print 'tx_hist_oil_prod update 2 complete'

    if debug: print sql_insert
    curr.execute(sql_insert)
    gd.commit(curr)
    print 'tx_hist_oil_prod update 3 complete'

    if debug: print sql_update_main
    curr.execute(sql_update_main)
    gd.commit(curr)
    print 'tx_hist_oil_prod update 4 complete'

    curr.close()
    conn.close()


def tx_lease_well_allocation(update=False, allocate=False, calc=False, fill_gaps=False, update_lease_details=False, update_well_details=False, update_lease_id_details=False, gen_hist_prod=False, update_well_no=False, insert_missing_years=False, update_hist_oil=False, debug=False):
    conn = gd.get_connection(database='US_Wells_Texas', server='sql_server')
    curr = conn.cursor()
    if update:
        update_prev_prod(curr, debug=debug)
    if allocate:
        lease_prod_allocation(debug=debug)
    if calc:
        calc_lease_period_prod(curr, debug=debug)
    if fill_gaps:
        update_data_gaps(curr, debug=debug)
    if update_lease_details:
        update_tx_lease_details(debug=debug)
    if update_well_details:
        update_tx_well_details(debug=debug)
    if update_lease_id_details:
        update_tx_lease_id_details(debug=debug)
    if update_well_no:
        update_well_no_data(debug=debug)
    if gen_hist_prod:
        generate_hist_well_prod(debug=debug)
    if insert_missing_years:
        generate_missing_hist_well_prod(debug=debug)
    if update_hist_oil:
        update_hist_oil_prod(debug=debug)
    curr.close()
    conn.close()


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def extract_schedule_urls():
    for in_fname in os.listdir(INPUT_FILE_DIR):
        with open(INPUT_FILE_DIR + in_fname) as in_file:
            filelines = in_file.readlines()
            for fileline in filelines:
                if fileline.startswith('<td><a href='):
                    print in_fname, fileline[12:]


def parse_oil_field_schedules(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
    sched_count = len(os.listdir(OIL_SCHED_DIR))
    sched_num   = 1
    sql_insert = "INSERT INTO tx_oil_field_schedule (process_code, well_record, source_line, source_file, sched_date, district_no, field_name, field_no, operator, operator_no, lease_name, lease_no) VALUES (0, '{}', {}, '{}', '{}', '{}', '{}', {}, '{}', {}, '{}', '{}')"
    for oil_field_sched in os.listdir(OIL_SCHED_DIR):
        in_data_group    = False
        last_district_line = 0
        last_header_line   = 0
        last_operator_line = 0
        last_lease_line    = 0
        last_well_line     = 0
        full_sched_date    = ''
        sched_date         = ''
        district_no        = ''
        field_name         = ''
        field_no           = 0
        operator           = ''
        operator_no        = 0
        lease_name         = ''
        lease_no           = ''
        exit               = 0
        exit_data          = []
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
                elif len(fileline.strip()) > 0 and (((last_district_line == (line_num - 3)) and len(filelines[line_num-1].strip()) == 0) or ((line_num+1 < line_count) and (((last_district_line == (line_num - 2)) and filelines[line_num+1][75:].startswith('MVBAL')) or filelines[line_num+1].startswith('* *') or filelines[line_num+1].startswith(' * *')))):
                    exit = 2
                    field_name = fileline[:33].rstrip().replace('"', '').replace(',', '').replace("'","")
                    field_no = fileline[33:41]
                    header_data += (field_name, field_no)
                elif fileline.startswith('  WELL   DEPTH  POTE') or fileline.startswith('  WELL    POTE'):
                    exit = 3
                    last_header_line = line_num
                elif last_header_line and (last_header_line == (line_num - 2)) and len(fileline.strip()) > 0:
                    exit = 4
                    last_operator_line = line_num
                    in_data_group = True
                    operator    = fileline[:33].rstrip().replace('"', '').replace(',', '').replace("'","")
                    operator_no = fileline[33:39]
                    header_data += (operator, operator_no)
                elif fileline.startswith('WELLS: ') or fileline.startswith('UNIT " " TOTALS') or fileline.startswith(' * * *') or fileline.startswith('* * *') or fileline.startswith('DISC:') or fileline.startswith('WELL STATUS TEST') or fileline.startswith('ACRES:')  or fileline.startswith('ALLOC:'):
                    exit = 5
                    in_data_group = False
                elif in_data_group and len(fileline.strip()) > 0 and (fileline[0] not in ['-', ' ', '*', '|']):
                    exit = 6
                    last_operator_line = line_num
                    operator    = fileline[:33].rstrip().replace('"', '').replace(',', '').replace("'","")
                    operator_no = fileline[33:39]
                    header_data = (sched_date, district_no, field_name, field_no, operator, operator_no)
                elif in_data_group and (last_operator_line and (last_operator_line == (line_num - 1))) and not fileline.startswith('- - - - -') and (len(fileline.strip()) == 0):
                    exit = 7
                    last_lease_line = line_num
                    lease_no   = '0'+fileline[1:6]
                    lease_name = fileline[8:45].rstrip().replace('"', '').replace(',', '').replace("'","")
                    header_data += (lease_name, lease_no)
                elif in_data_group and ((len(fileline.strip()) == 122) or (fileline[45:].startswith('(CONT)'))) and (fileline[1] != ' '):
                    exit = 8
                    last_lease_line = line_num
                    lease_no   = '0'+fileline[1:6]
                    lease_name = fileline[8:45].rstrip().replace('"', '').replace(',', '').replace("'","")
                    header_data = (sched_date, district_no, field_name, field_no, operator, operator_no, lease_name, lease_no)
                elif in_data_group and (len(fileline.rstrip()) == 132) and not (fileline.startswith('- -') or fileline.startswith(' - -')):
                    exit = 9
                    well_record = fileline.rstrip().replace('"', ' ').replace(',', ' ').replace("'"," ")
                    curr.execute(sql_insert.format(well_record,line_num,oil_field_sched,*header_data))
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
                    print '{} >> ({}/{}) --- {}/{} --- {}: {} --> {}'.format(oil_field_sched, sched_num, sched_count, line_num, line_count, exit, fileline.strip(), header_data)
                else:
                    print '{} >> ({}/{}) --- {}/{}'.format(oil_field_sched, sched_num, sched_count, line_num, line_count)
            sched_num += 1
    curr.close()
    conn.close()


def parse_oil_operator_schedules(debug=False):
    conn = gd.get_connection(database='us_wells')
    curr = conn.cursor()
    sched_count = len(os.listdir(OIL_SCHED_DIR))
    sched_num   = 1
    sql_insert = 'INSERT INTO tx_oil_operator_schedule (process_code, well_record, source_line, source_file, sched_date, operator, district_no, field_name, lease_name, lease_no) VALUES (0, "{}", {}, "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
    for oil_operator_sched in os.listdir(OIL_SCHED_DIR):
        in_data_group      = False
        in_oil_data_group  = False
        in_gas_data_group  = False
        in_operator_group  = False
        well_record        = ''
        full_sched_date    = ''
        sched_date         = ''
        district_no        = ''
        field_name         = ''
        operator           = ''
        lease_name         = ''
        lease_no           = ''
        exit               = 0
        exit_data          = []
        header_data        = ()
        with open(OIL_SCHED_DIR + oil_operator_sched) as sched_file:
            filelines = sched_file.readlines()
            line_count = len(filelines)
            if line_count == 1:
                filelines = filelines[0].split('\r')
                line_count = len(filelines)
                print line_count
            for line_num in range(line_count):
                fileline = filelines[line_num]
                if fileline.startswith('         OIL AND GAS PRORATION SCHEDULE LISTED BY OPERATOR'):
                    exit               = 1
                    full_sched_date    = fileline[64:].strip().split()
                    sched_date         = full_sched_date[1] + MONTH_NUMS[full_sched_date[0].upper()]
                    in_operator_group  = True
                    in_data_group      = False
                    in_oil_data_group  = False
                    in_gas_data_group  = False
                    district_no        = ''
                    field_name         = ''
                    operator           = ''
                    lease_name         = ''
                    lease_no           = ''
                    header_data        = (sched_date,)
                elif in_operator_group and fileline.upper()[55:].startswith('STATUS DATE'):
                    exit               = 2
                    operator = fileline[8:55].upper().strip().replace('"', '').replace(',', '').replace("'","")
                    in_operator_group  = False
                    in_data_group      = True
                    header_data        = (sched_date, operator)
                elif in_data_group and not in_operator_group and fileline.upper().startswith('OIL-WELLS'):
                    exit               = 3
                    in_oil_data_group  = True
                    in_gas_data_group  = False
                elif in_data_group and not in_operator_group and fileline.upper().startswith('GAS-WELLS'):
                    exit               = 4
                    in_gas_data_group  = True
                    in_oil_data_group  = False
                elif in_data_group and not in_operator_group and len(fileline.strip()) == 0:
                    exit               = 5
                    in_gas_data_group  = False
                    in_oil_data_group  = False
                elif in_oil_data_group and not in_operator_group and fileline.upper()[:4] in ['01  ','02  ','03  ','04  ','05  ','06  ','6E  ','7B  ','7C  ','08  ','8A  ','8B  ','09  ','10  ']:
                    exit               = 6
                    district_no        = fileline.upper()[:2]
                    field_name         = fileline.upper()[4:].rstrip().replace('"', '').replace(',', '').replace("'","")
                    header_data        = (sched_date, operator, district_no, field_name)
                elif in_oil_data_group and not in_operator_group and len(fileline.strip()) > 0 and (fileline[:7] == '       ') and (fileline[24] in ['0','1','2','3','4','5','6','7','8','9']):
                    exit               = 7
                    line_len           = len(fileline)
                    lease_name         = fileline[7:24].strip().replace('"', ' ').replace(',', ' ').replace("'"," ")
                    lease_no           = '0' + fileline[24:29]
                    well_record        = gd.encode_str(fileline.replace('"', ' ').replace(',', ' ').replace("'"," "))
                    well_rec_len       = len(well_record)
                    well_record        = (' '*(line_len-well_rec_len)) + well_record
                    header_data        = (sched_date, operator, district_no, field_name, lease_name, lease_no)
                    curr.execute(sql_insert.format(well_record,line_num,oil_operator_sched,*header_data))
                    gd.commit(curr)
                elif in_oil_data_group and not in_operator_group and len(fileline.strip()) > 0 and (fileline[:38] == (' '*38)) and not fileline[42:].upper().startswith('LEASE TOTALS'):
                    exit               = 8
                    line_len           = len(fileline)
                    well_record        = gd.encode_str(fileline.replace('"', ' ').replace(',', ' ').replace("'"," "))
                    well_rec_len       = len(well_record)
                    well_record        = (' '*(line_len-well_rec_len)) + well_record
                    curr.execute(sql_insert.format(well_record,line_num,oil_operator_sched,*header_data))
                    gd.commit(curr)
                else:
                    exit               = 9

                if debug:
                    print '{} >> ({}/{}) --- {}/{} --- {}: {} --> {}'.format(oil_operator_sched, sched_num, sched_count, line_num, line_count, exit, fileline.strip(), header_data)
                else:
                    print '{} >> ({}/{}) --- {}/{}'.format(oil_operator_sched, sched_num, sched_count, line_num, line_count)
            sched_num += 1
    curr.close()
    conn.close()


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_tx_well_id():
    conn = get_connection(database='US_Wells_Texas', server='sql_server')
    curr = conn.cursor()
    tx_well_data = get_data('api_number, lease_id, well_no, oil_gas_code', 'dbo.tx_ref_well_id', database='US_Wells_Texas', server='sql_server', sql_where="wellbore_no='98'", datatype='plural', cursor=curr)
    sql_update = "UPDATE dbo.tx_ref_well_id SET wellbore_no='{}' WHERE api_number='{}' AND lease_id='{}' AND well_no='{}' AND oil_gas_code='{}'"
    well_data_count = len(tx_well_data)
    well_data_num = 1
    for api_number, lease_id, well_no, oil_gas_code in tx_well_data:
        print '{}/{}: {} - {} - {} - {}'.format(well_data_num, well_data_count, api_number, lease_id, well_no, oil_gas_code)
        sql_where = "wellbore_no!='98' AND api_number='{}' AND oil_gas_code='{}'"
        try:
            max_wellbore_no = get_data('MAX(wellbore_no)', 'dbo.tx_ref_well_id', database='US_Wells_Texas', server='sql_server', sql_where=sql_where.format(api_number, oil_gas_code), single_value=True)
            max_wellbore_indx = wellbore_nums.index(max_wellbore_no)
        except:
            max_wellbore_indx = -1
        wellbore_no = wellbore_nums[max_wellbore_indx + 1]
        curr.execute(sql_update.format(wellbore_no, api_number, lease_id, well_no, oil_gas_code))
        commit(curr)
        well_data_num += 1
    curr.execute("UPDATE dbo.tx_ref_well_id SET tx_well_id=CONCAT(api_number,'00',wellbore_no) WHERE oil_gas_code='O' AND tx_well_id IS NULL AND LEN(wellbore_no)=2")
    commit(curr)
    curr.execute("UPDATE dbo.tx_ref_well_id SET tx_well_id=CONCAT(api_number,'01',wellbore_no) WHERE oil_gas_code='G' AND tx_well_id IS NULL AND LEN(wellbore_no)=2")
    commit(curr)
    curr.close()
    conn.close()

if __name__=='__main__':
    main()