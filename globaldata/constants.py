import itertools
import os

import pymysql

try:
    # conn = pymysql.connect(user='root', passwd='OilAndGas321', host='localhost', db='globaldata') #host = 'localhost' originally
    conn = pymysql.connect(user="titan", passwd="}2Ek}dTd*Z)k_dCI_Pm%", host="10.8.114.14", db="globaldata")
    # ''
    curr = conn.cursor()
    curr.execute('USE globaldata')
    curr.execute("SELECT computer_name, discount_year FROM global_variables WHERE id=1")

    COMPUTER, DISCOUNT_YEAR = curr.fetchone()

    curr.close()
    conn.close()
except:
    COMPUTER      = 'OTHER'
    DISCOUNT_YEAR = 2025
    # 'TITAN': {       'AUTHOR': 'Titan-PC\Titan',
    #                 'USER_ID': 'Titan-PC\Titan',
    #           'PROGRAM_DRIVE': 'E:',
    #                'GD_DRIVE': 'E:',
    #                    'HOST': '10.5.0.101',
    #             'SERVER_NAME': 'TITAN-PC'},
CONFIG = {    
    'TITAN': {       'AUTHOR': 'Titan-PC\Titan',
                    'USER_ID': 'Titan-PC\Titan',
              'PROGRAM_DRIVE': 'D:\TitanJobs\Titan1\\',
                   'GD_DRIVE': 'D:\TitanJobs\Titan1\\',
                       'HOST': '10.8.114.12',
                'SERVER_NAME': 'UK-TITANRDS-01'},
  
  'HAL2017': {       'AUTHOR': 'HAL-2017\Jason', 
                    'USER_ID': 'HAL-2017\Jason', 
              'PROGRAM_DRIVE': 'D:',
                   'GD_DRIVE': 'D:',
                       'HOST': '10.5.0.100',
                'SERVER_NAME': 'HAL-2017'},
  
 'TITAN II': {       'AUTHOR': 'TITAN-II\Titan II',
                    'USER_ID': 'TITAN-II\Titan II',
              'PROGRAM_DRIVE': 'C:',
                   'GD_DRIVE': 'C:',
                       'HOST': '10.5.0.102',
                'SERVER_NAME': 'TITAN-II'},
  
'TITAN III': {       'AUTHOR': 'TITAN-III\Titan', 
                    'USER_ID': 'TITAN-III\Titan', 
              'PROGRAM_DRIVE': 'E:',
                   'GD_DRIVE': 'E:',
                       'HOST': '10.5.0.103',
                'SERVER_NAME': 'TITAN-III'},

'DIGITALSTORM-PC': { 'AUTHOR': 'DIGITALSTORM-PC\Jason',
                    'USER_ID': 'DIGITALSTORM-PC\Jason',
              'PROGRAM_DRIVE': 'D:',
                   'GD_DRIVE': 'D:',
                       'HOST': '10.5.0.100',
                 'SERVER_NAME': 'DIGITALSTORM-PC'} #,
    #
    # 'OTHER': {       'AUTHOR': '{}\{}'.format(os.environ['COMPUTERNAME'], os.environ['USERNAME']),
    #                 'USER_ID': '{}\{}'.format(os.environ['COMPUTERNAME'], os.environ['USERNAME']),
    #           'PROGRAM_DRIVE': os.environ['SYSTEMDRIVE'],
    #                'GD_DRIVE': os.environ['SYSTEMDRIVE'],
    #                    'HOST': 'localhost',
    #            'SERVER_NAME': ''}
}

AUTHOR         = CONFIG[COMPUTER]['AUTHOR']
USER_ID        = CONFIG[COMPUTER]['USER_ID']
PROGRAM_DRIVE  = CONFIG[COMPUTER]['PROGRAM_DRIVE']
GD_DRIVE       = CONFIG[COMPUTER]['GD_DRIVE']
HOST           = CONFIG[COMPUTER]['HOST']
SERVER_NAME    = CONFIG[COMPUTER]['SERVER_NAME']
# PROGRAM_DIR    = PROGRAM_DRIVE  + '\\python_code\\'
PROGRAM_DIR    = PROGRAM_DRIVE  + 'python_code\\'
# ENGINE_DIR     = GD_DRIVE       + '\\GlobalData\\'
ENGINE_DIR     = GD_DRIVE       + 'GlobalData\\'

WEB_DATA_DIR   = PROGRAM_DIR    + 'web_scrape\\production\\'
WELL_CODE_DIR  = PROGRAM_DIR    + 'well_data\\'

TASK_DIR       = ENGINE_DIR     + 'Tasks\\'
REGIONS_DIR    = ENGINE_DIR     + 'Regions\\'
DATA_DIR       = ENGINE_DIR     + 'Data\\'
MACRO_DIR      = ENGINE_DIR     + 'Macros\\'
OUTPUT_DIR     = ENGINE_DIR     + 'Output\\'
REPORTS_DIR    = ENGINE_DIR     + 'Reports\\'
TEST_DIR       = ENGINE_DIR     + 'Tests\\'

DATABASE_DIR   = DATA_DIR       + 'database\\'
MINING_DIR     = DATA_DIR       + 'mining\\'
MINING_DB_DIR  = DATA_DIR       + 'mining\\mining_db\\'
DET_MOD_DIR    = DATA_DIR       + 'detailed_models\\detailed_original\\'
CSV_IMPORT_DIR = DATA_DIR       + 'import_csv\\'
OILGAS_DIR     = DATA_DIR       + 'oilgas\\'
OILGAS_DB_DIR  = DATA_DIR       + 'oilgas\\oilgas_db\\'
DF_DATA_DIR    = DATA_DIR       + 'discovered_fields\\'
UNCON_DATA_DIR = DATA_DIR       + 'wells\\'
WELL_DATA_DIR  = UNCON_DATA_DIR

DET_MODELS_DIR = DATA_DIR       + 'detailed_models\\'
DET_MD_NEW_DIR = DET_MODELS_DIR + 'detailed_new\\'
DET_MD_PRC_DIR = DET_MODELS_DIR + 'detailed_processed\\'
DET_MD_PBE_DIR = DET_MD_PRC_DIR + 'detailed\\'
DET_MD_NBE_DIR = DET_MD_NEW_DIR + 'detailed\\'

ECN_LMT_DIR    = DATA_DIR       + 'economic_limit\\'
ECN_LMT_EN_DIR = ECN_LMT_DIR    + 'Engine_Models\\'
ECN_LMT_PR_DIR = ECN_LMT_DIR    + 'Processed_Models\\'

DEALS_DIR      = REGIONS_DIR    + 'Deals\\'
DF_REGION_DIR  = REGIONS_DIR    + 'Discovered\\'
SCENARIO_DIR   = REGIONS_DIR    + 'Scenarios\\'

KEY_ASSET_DIR  = TEST_DIR       + 'key_assets\\'

ECON_MACRO_DIR = MACRO_DIR      + 'EconDataMacros\\'
ECON_REGIONS   = ECON_MACRO_DIR + 'Regions\\'
BREAKEVEN_DIR  = MACRO_DIR      + 'BreakevenMacros\\'
BE_REGIONS     = BREAKEVEN_DIR  + 'Regions\\'
DISC_FIELD_DIR = MACRO_DIR      + 'DiscFieldMacros\\'
DF_REGIONS     = DISC_FIELD_DIR + 'Regions\\'
TEST_RGNS_DIR  = BREAKEVEN_DIR  + 'TestMacros\\Regions\\'

ECON_ERR_DIR   = REPORTS_DIR    + 'EconErrorReports\\'
TEMPLATE_DIR   = REPORTS_DIR    + 'templates\\'

TEMP_LOG_DIR   = TASK_DIR       + 'temp\\'
BE_TASK_DIR    = TASK_DIR       + 'BreakevenTasks\\'
MODEL_TASK_DIR = TASK_DIR       + 'CreateModelTasks\\'
XML_TASK_DIR   = TASK_DIR       + 'xml\\'
ECON_TASK_DIR  = TASK_DIR       + 'EconErrorTasks\\'
ENGN_TASK_DIR  = TASK_DIR       + 'EngineTasks\\'
ENGN_TASK_DIR_ = TASK_DIR       + 'EngineTasks_\\'
DATA_TASK_DIR  = TASK_DIR       + 'EconDataTasks\\'
EXTRT_TASK_DIR = TASK_DIR       + 'DataExtractTasks\\'
CMD_TASK_DIR   = TASK_DIR       + 'Commands\\'
RPT_TASK_DIR   = TASK_DIR       + 'ReportTasks\\'
WELL_TASK_DIR  = TASK_DIR       + 'WellEngineTasks\\'

DF_TASKS       = TASK_DIR       + 'DiscoveredFieldTasks\\'
DF_CALC_DIR    = DF_TASKS       + 'DiscFieldCalcTasks\\'
DF_CONFS_DIR   = DF_TASKS       + 'DiscFieldConfTasks\\'
DF_CONF1_DIR   = DF_CONFS_DIR   + 'DiscFieldConf1\\'
DF_CONF2_DIR   = DF_CONFS_DIR   + 'DiscFieldConf2\\'
DF_EXTRACT_DIR = DF_TASKS       + 'DiscFieldExtractTasks\\'
DF_MACROS_DIR  = DF_TASKS       + 'DiscFieldMacroTasks\\'
DF_MACRO1_DIR  = DF_MACROS_DIR  + 'DiscFieldMacro1\\'
DF_MACRO2_DIR  = DF_MACROS_DIR  + 'DiscFieldMacro2\\'
DF_MACRO3_DIR  = DF_MACROS_DIR  + 'DiscFieldMacro3\\'
DF_MODEL_DIR   = DF_TASKS       + 'DiscFieldModelTasks\\'
DF_PROD_DIR    = DF_TASKS       + 'DiscFieldProdTasks\\'
DF_BE_DIR      = BE_REGIONS     + 'Discovered\\'

NA_1           = MODEL_TASK_DIR + 'NA_1.csv'
NA_2           = MODEL_TASK_DIR + 'NA_2.csv'
NA_3           = MODEL_TASK_DIR + 'NA_3.csv'
NA_4           = MODEL_TASK_DIR + 'NA_4.csv'
NA_5           = MODEL_TASK_DIR + 'NA_5.csv'
NA_6           = MODEL_TASK_DIR + 'NA_6.csv'

EU_1           = MODEL_TASK_DIR + 'EU_1.csv'
EU_2           = MODEL_TASK_DIR + 'EU_2.csv'
EU_3           = MODEL_TASK_DIR + 'EU_3.csv'

FS_1           = MODEL_TASK_DIR + 'FS_1.csv'
FS_2           = MODEL_TASK_DIR + 'FS_2.csv'
FS_3           = MODEL_TASK_DIR + 'FS_3.csv'
FS_4           = MODEL_TASK_DIR + 'FS_4.csv'

SA_1           = MODEL_TASK_DIR + 'SA_1.csv'
SA_2           = MODEL_TASK_DIR + 'SA_2.csv'
SA_3           = MODEL_TASK_DIR + 'SA_3.csv'

UN_1           = MODEL_TASK_DIR + 'UN_1.csv'
UN_2           = MODEL_TASK_DIR + 'UN_2.csv'
UN_3           = MODEL_TASK_DIR + 'UN_3.csv'
UN_4           = MODEL_TASK_DIR + 'UN_4.csv'
UN_5           = MODEL_TASK_DIR + 'UN_5.csv'
UN_6           = MODEL_TASK_DIR + 'UN_6.csv'
UN_7           = MODEL_TASK_DIR + 'UN_7.csv'
UN_8           = MODEL_TASK_DIR + 'UN_8.csv'
UN_9           = MODEL_TASK_DIR + 'UN_9.csv'
DT_1           = MODEL_TASK_DIR + 'DT_1.csv'
EL_1           = MODEL_TASK_DIR + 'EL_1.csv'

TEST_1         = MODEL_TASK_DIR + 'TEST_1.csv'
TEST_2         = MODEL_TASK_DIR + 'TEST_2.csv'
TEST_3         = MODEL_TASK_DIR + 'TEST_3.csv'
TEST_4         = MODEL_TASK_DIR + 'TEST_4.csv'
TEST_5         = MODEL_TASK_DIR + 'TEST_5.csv'
TEST_6         = MODEL_TASK_DIR + 'TEST_6.csv'
TEST_7         = MODEL_TASK_DIR + 'TEST_7.csv'
TEST_8         = MODEL_TASK_DIR + 'TEST_8.csv'
TEST_9         = MODEL_TASK_DIR + 'TEST_9.csv'
TEST_10        = MODEL_TASK_DIR + 'TEST_10.csv'
TEST_11        = MODEL_TASK_DIR + 'TEST_11.csv'
TEST_12        = MODEL_TASK_DIR + 'TEST_12.csv'
TEST_13        = MODEL_TASK_DIR + 'TEST_13.csv'
TEST_14        = MODEL_TASK_DIR + 'TEST_14.csv'
TEST_15        = MODEL_TASK_DIR + 'TEST_15.csv'
TEST_16        = MODEL_TASK_DIR + 'TEST_16.csv'
TEST_17        = MODEL_TASK_DIR + 'TEST_17.csv'
TEST_18        = MODEL_TASK_DIR + 'TEST_18.csv'
TEST_19        = MODEL_TASK_DIR + 'TEST_19.csv'
TEST_20        = MODEL_TASK_DIR + 'TEST_20.csv'

AF             = MODEL_TASK_DIR + 'AF.csv'
AS             = MODEL_TASK_DIR + 'AS.csv'
CR             = MODEL_TASK_DIR + 'CR.csv'
CA             = MODEL_TASK_DIR + 'CA.csv'
EU             = MODEL_TASK_DIR + 'EU.csv'
FS             = MODEL_TASK_DIR + 'FS.csv'
ME             = MODEL_TASK_DIR + 'ME.csv'
NA             = MODEL_TASK_DIR + 'NA.csv'
OC             = MODEL_TASK_DIR + 'OC.csv'
SA             = MODEL_TASK_DIR + 'SA.csv'

RW_1           = MODEL_TASK_DIR + 'RW_1.csv'
RW_2           = MODEL_TASK_DIR + 'RW_2.csv'
RW_3           = MODEL_TASK_DIR + 'RW_3.csv'

DF_NA_1        = DF_MODEL_DIR   + 'DF_NA_1.csv'
DF_NA_2        = DF_MODEL_DIR   + 'DF_NA_2.csv'
DF_NA_3        = DF_MODEL_DIR   + 'DF_NA_3.csv'
DF_NA_4        = DF_MODEL_DIR   + 'DF_NA_4.csv'
DF_NA_5        = DF_MODEL_DIR   + 'DF_NA_5.csv'
DF_NA_6        = DF_MODEL_DIR   + 'DF_NA_6.csv'
DF_EU_1        = DF_MODEL_DIR   + 'DF_EU_1.csv'
DF_EU_2        = DF_MODEL_DIR   + 'DF_EU_2.csv'
DF_EU_3        = DF_MODEL_DIR   + 'DF_EU_3.csv'
DF_FS_1        = DF_MODEL_DIR   + 'DF_FS_1.csv'
DF_FS_2        = DF_MODEL_DIR   + 'DF_FS_2.csv'
DF_FS_3        = DF_MODEL_DIR   + 'DF_FS_3.csv'
DF_FS_4        = DF_MODEL_DIR   + 'DF_FS_4.csv'
DF_SA_1        = DF_MODEL_DIR   + 'DF_SA_1.csv'
DF_SA_2        = DF_MODEL_DIR   + 'DF_SA_2.csv'
DF_SA_3        = DF_MODEL_DIR   + 'DF_SA_3.csv'
DF_UN_1        = DF_MODEL_DIR   + 'DF_UN_1.csv'
DF_AF          = DF_MODEL_DIR   + 'DF_AF.csv'
DF_AS          = DF_MODEL_DIR   + 'DF_AS.csv'
DF_CR          = DF_MODEL_DIR   + 'DF_CR.csv'
DF_CA          = DF_MODEL_DIR   + 'DF_CA.csv'
DF_EU          = DF_MODEL_DIR   + 'DF_EU.csv'
DF_FS          = DF_MODEL_DIR   + 'DF_FS.csv'
DF_ME          = DF_MODEL_DIR   + 'DF_ME.csv'
DF_NA          = DF_MODEL_DIR   + 'DF_NA.csv'
DF_OC          = DF_MODEL_DIR   + 'DF_OC.csv'
DF_SA          = DF_MODEL_DIR   + 'DF_SA.csv'
DF_RW_1        = DF_MODEL_DIR   + 'DF_RW_1.csv'
DF_RW_2        = DF_MODEL_DIR   + 'DF_RW_2.csv'
DF_RW_3        = DF_MODEL_DIR   + 'DF_RW_3.csv'

ARPS_TEST      = TEST_DIR       + 'test_assets\\ARPS_TEST.csv'

COMPLEXTY_TMP  = TEMPLATE_DIR   + 'Complexity Score Template.xlsm'
PARAM_TRK_TMP  = TEMPLATE_DIR   + 'Engine Parameter Tracker Template.xlsx'
ERROR_LOG_TMP  = TEMPLATE_DIR   + 'Global Run Error Log Template.xlsx'
BREAKEVEN_TMP  = TEMPLATE_DIR   + 'Breakeven Review Template.xlsx'
ECON_ERR_TMP   = TEMPLATE_DIR   + 'Economics Global Run Error Log Template.xlsx'
MINING_ERR_TMP = TEMPLATE_DIR   + 'Mining Error Log Template.xlsx'
MINING_CPX_TMP = TEMPLATE_DIR   + 'Mining Complexity Template.xlsx'
IMPLIED_PR_TMP = TEMPLATE_DIR   + 'Upstream Deals Metric Template.xlsx'
ANALYTICS_TMP  = TEMPLATE_DIR   + 'Analytics Parameter Tracker Template.xlsx'


COMPLEXTY_RPT  = REPORTS_DIR    + 'Complexity Score Report %s.xlsm'
PARAM_TRK_RPT  = REPORTS_DIR    + 'Engine Parameter Tracker %s.xlsx'
ERROR_LOG_RPT  = REPORTS_DIR    + 'Global Run Error Log %s.xlsx'
BREAKEVEN_RPT  = REPORTS_DIR    + 'Breakeven Review %s.xlsx'
ECON_ERR_RPT   = REPORTS_DIR    + 'Economics Global Run Error Log %s.xlsx'
MINING_ERR_RPT = REPORTS_DIR    + 'Mining Error Log Report %s.xlsx'
MINING_CPX_RPT = REPORTS_DIR    + 'Mining Complexity Report %s.xlsx'
IMPLIED_PR_RPT = REPORTS_DIR    + 'Upstream Deals Metric Report %s.xlsx'
ANALYTICS_RPT  = REPORTS_DIR    + 'Analytics Parameter Tracker %s.xlsx'


CHECK_T3_REGION_SET  = {
    'Africa',
    'Asia',
    'Caribbean',
    'Central_America',
    'Europe_1',
    'Europe_2',
    'Europe_3',
    'Former_Soviet_Union_1',
    'Former_Soviet_Union_2',
    'Former_Soviet_Union_3',
    'Former_Soviet_Union_4',
    'Middle_East',
    'North_America_1',
    'North_America_2',
    'North_America_3',
    'North_America_4',
    'North_America_5',
    'North_America_6',
    'Oceania',
    'South_America_1',
    'South_America_2',
    'South_America_3',
    'Unconventional'
}

CHECK_REGION_SET     = {
    'Africa',
    'Asia',
    'Caribbean',
    'Central_America',
    'Europe',
    'Former_Soviet_Union',
    'Middle_East',
    'North_America_1',
    'North_America_2',
    'Oceania',
    'South_America',
    'Unconventional'
}

CHECK_MODEL_SET      = {
    'North_America_2',
    'Former_Soviet_Union',
    'South_America',
    'Europe',
    'Rest_of_World_1',
    'Rest_of_World_2',
    'Unconventional_1',
    'Unconventional_2'
}

CHECK_T3_MODEL_SET   = {
    'Africa',
    'Asia',
    'Europe_1',
    'Europe_2',
    'Europe_3',
    'Former_Soviet_Union_1',
    'Former_Soviet_Union_2',
    'Former_Soviet_Union_3',
    'Former_Soviet_Union_4',
    'North_America_1',
    'North_America_3',
    'North_America_4',
    'North_America_6',
    'Oceania',
    'South_America_1',
    'South_America_2',
    'South_America_3',
    'Rest_of_World_1',
    'Rest_of_World_3',
    'Unconventional_1',
    'Unconventional_2'
}

CHECK_TEST_SET       = {
    'Africa',
    'Asia',
    'Caribbean',
    'Central_America',
    'Europe',
    'Former_Soviet_Union',
    'Middle_East',
    'North_America_1',
    'North_America_2',
    'Oceania',
    'South_America'
}

REGION_NAMES = [
    'Africa',
    'Asia',
    'Caribbean',
    'Central America',
    'Europe',
    'Former Soviet Union',
    'Middle East',
    'North America',
    'North_America_1',
    'North_America_2',
    'Oceania',
    'South America',
    'Unconventional'
]



DISC_REGIONS         = {
    'Africa',
    'Asia',
    'Caribbean',
    'Central_America',
    'Europe',
    'Former_Soviet_Union',
    'Middle_East',
    'North_America',
    'Oceania',
    'South_America'
}

CHECK_ECON_ERROR_SET = CHECK_REGION_SET
MAIN_REGIONS         = DISC_REGIONS

REGIONS              = {
    'Africa'                : 'Africa',
    'Asia'                  : 'Asia',
    'Caribbean'             : 'Caribbean',
    'Central_America'       : 'Central America',
    'Europe'                : 'Europe',
    'Former_Soviet_Union'   : 'Former Soviet Union',
    'Middle_East'           : 'Middle East',
    'North_America'         : 'North America',
    'North_America_1'       : 'North_America_1',
    'North_America_2'       : 'North_America_2',
    'Oceania'               : 'Oceania',
    'Rest_of_World_1'       : 'Rest of World 1',
    'Rest_of_World_2'       : 'Rest of World 2',
    'South_America'         : 'South America',
    'Unconventional'        : 'Unconventional'
}

REGION_CODES         = {
    'Africa'                : 'AF',
    'Asia'                  : 'AS',
    'Caribbean'             : 'CR',
    'Central_America'       : 'CA',
    'Europe'                : 'EU',
    'Europe_1'              : 'E1',
    'Europe_2'              : 'E2',
    'Europe_3'              : 'E3',
    'Former_Soviet_Union'   : 'FS',
    'Former_Soviet_Union_1' : 'F1',
    'Former_Soviet_Union_2' : 'F2',
    'Former_Soviet_Union_3' : 'F3',
    'Former_Soviet_Union_4' : 'F4',
    'Middle_East'           : 'ME',
    'North_America'         : 'NA',
    'North_America_1'       : 'N1',
    'North_America_2'       : 'N2',
    'North_America_3'       : 'N3',
    'North_America_4'       : 'N4',
    'North_America_5'       : 'N5',
    'North_America_6'       : 'N6',
    'Oceania'               : 'OC',
    'South_America'         : 'SA',
    'South_America_1'       : 'S1',
    'South_America_2'       : 'S2',
    'South_America_3'       : 'S3',
    'Unconventional'        : 'UN',
    'Rest_of_World_1'       : [
        'UN',
        'N1',
        'ME'
    ]
    ,
    'Rest_of_World_2': [
        'AF',
        'AS',
        'CR',
        'CA',
        'OC'
    ]
}

RGN_CODES            = {
    'AF':'Africa',
    'AS':'Asia',
    'CR':'Caribbean',
    'CA':'Central_America',
    'EU':'Europe',
    'E1':'Europe_1',
    'E2':'Europe_2',
    'E3':'Europe_3',
    'FS':'Former_Soviet_Union',
    'F1':'Former_Soviet_Union_1',
    'F2':'Former_Soviet_Union_2',
    'F3':'Former_Soviet_Union_3',
    'F4':'Former_Soviet_Union_4',
    'ME':'Middle_East',
    'NA':'North_America',
    'N1':'North_America_1',
    'N2':'North_America_2',
    'N3':'North_America_3',
    'N4':'North_America_4',
    'N5':'North_America_5',
    'N6':'North_America_6',
    'OC':'Oceania',
    'SA':'South_America',
    'S1':'South_America_1',
    'S2':'South_America_2',
    'S3':'South_America_3',
    'UN':'Unconventional'
}

GLOBALDATA_PROGRAMS  = [
    'analogue_score_calc.py',
    'analytics_param_report.py',
    'assumption_points.py',
    'automated_panorama.py',
    'calc_breakevens.py',
    'calc_min_econ.py',
    'cmd_main.py',
    'create_light_models.py',
    'data_export.py',
    'decline_obj.py',
    'discovered_analogues.py',
    'econ_error_report.py',
    'engine_report_data.py',
    'extract_econ_data.py',
    'extract_deals_data.py',
    'extract_uncon_data.py',
    'globaldata/__init__.py',
    'globaldata/constants.py',
    'globaldata/config.py',
    'globaldata/utils.py',
    'implied_price_report.py',
    'import_detailed_models.py',
    'mining_complexity_report.py',
    'mining_error_report.py',
    'mining_functions.py',
    'mining_v5.py',
    'oilgas_field.py',
    'param_detail.py',
    'process_econ_limits.py',
    'process_deals.py',
    'process_detailed_models.py',
    'process_mining.py',
    'server_import.py',
    'server2.py',
    'sqlserver_import_db.py',
    'standard_menu_titan_V23.py',
    'standard_menu_titan_V24.py',
    'task_scheduler.py',
    'update_asset_data.py',
    'update_fiscal_table.py',
    'update_key_asset_data.py',
    'update_programs.py',
    'us_well_data.py',
    'well_data/category_tree_gui.py',
    'well_data/column_filter_gui.py',
    'well_data/csv_sql_import.py',
    'well_data/extract_completion_data.py',
    'well_data/globaldata_stylesheet.css',
    'well_data/tree_browser.py',
    'well_data/tree_browser_tool.pyw',
    'well_data/well_analytics.py',
    'well_data/well_data_charts.py',
    'well_data/well_data_tool.pyw',
    'well_data/well_data_gui.py',
    'well_data/well_data_launch.py',
    'well_data/well_utils.py',
    'well_data/web_scrape.py'
]

ERR_TBL_DATA         = {
      'error_log_exception': {'filename': 'error_log_exceptions_%s.csv',
                               'msg_col': 'comment',
                               'flg_col': 'errorType'},

    'econ_error_exceptions': {'filename': 'econ_error_exceptions_%s.csv',
                               'msg_col': 'error_message',
                               'flg_col': 'error_flag'}
}

PARAM_DATA           = {
            'irr_dev': {'rank_order': 'DESC',
                        'param_name': 'development IRR'},

      'capex_boe_rem': {'rank_order': 'ASC',
                        'param_name': 'remaining capex per boe'},

       'opex_boe_rem': {'rank_order': 'ASC',
                        'param_name': 'remaining opex per boe'},

    'total_recov_rem': {'rank_order': 'DESC',
                        'param_name': 'remaining reserves'},

        'total_recov': {'rank_order': 'DESC',
                        'param_name': 'recoverable reserves'},

            'npv_rem': {'rank_order': 'DESC',
                        'param_name': 'remaining NPV'},

         'be_gas_rem': {'rank_order': 'ASC',
                        'param_name': 'remaining break-even price'},

         'be_oil_rem': {'rank_order': 'ASC',
                        'param_name': 'remaining break-even price'},

         'capex_full': {'rank_order': 'DESC',
                        'param_name': 'total capex'},

          'commodity': {     'crude': 'crude oil',
                                'ng': 'natural gas',
                        'condensate': 'condensate',
                               'lng': 'LNG',
                              'ngls': 'NGL'}
}

SCHEMAS              = {
    'tblAutomatedPanorama'                      : 'dbo',
    'tblDiscoveredFieldsNearestInfra'           : 'dbo',
    'tblFielUnconventionalDataInput'            : 'dbo',
    'tblFieldBasicExtract'                      : 'dbo',
    'tblFieldEquityExtract'                     : 'dbo',
    'tblFieldProductionExtract_Africa'          : 'dbo',
    'tblFieldProductionExtract_Asia'            : 'dbo',
    'tblFieldProductionExtract_Caribbean'       : 'dbo',
    'tblFieldProductionExtract_CentralAmerica'  : 'dbo',
    'tblFieldProductionExtract_Europe'          : 'dbo',
    'tblFieldProductionExtract_FSU'             : 'dbo',
    'tblFieldProductionExtract_MiddleEast'      : 'dbo',
    'tblFieldProductionExtract_NorthAmerica'    : 'dbo',
    'tblFieldProductionExtract_Oceania'         : 'dbo',
    'tblFieldProductionExtract_SouthAmerica'    : 'dbo',
    'tblFieldReserveExtract'                    : 'dbo',
    'tblGEDiscoveryFieldsInput'                 : 'dbo',
    'tblImpliedOilPriceInput'                   : 'dbo',
    'tblImpliedOilPriceOutput'                  : 'dbo',
    'tblEngineCommodityPriceSourceData'         : 'Engine',
    'tblEngineDataPoints'                       : 'Engine',
    'tblEngineFEATData'                         : 'Engine',
    'tblEngineFEATData_Extn'                    : 'Engine',
    'tblEngineProductionData'                   : 'Engine',
    'tblEngineCashFlowData'                     : 'Engine',
    'tblEngineAssetSenRemainingNPV'             : 'Engine',
    'tblEngineAnalogueFields'                   : 'Engine',
    'tblEngineWellInputInfo'                    : 'Engine',
    'tblEngineWellDataInfo'                     : 'Engine',
    'tblEngineWellInputProductionInfo'          : 'Engine',
    'Mining_Assets_Daily'                       : 'dbo',
    'Mining_Assets_Forecast'                    : 'dbo',
    'Mining_Capacity_Daily'                     : 'dbo',
    'Mining_Capacity_Forecast'                  : 'dbo',
    'Mining_compounds'                          : 'dbo',
    'Mining_Equity_Daily'                       : 'dbo',
    'Mining_Error_Log'                          : 'dbo',
    'Mining_Error_Log_Exceptions'               : 'dbo',
    'Mining_Machinery_Daily'                    : 'dbo',
    'Mining_Metrics'                            : 'dbo',
    'Mining_Model_Rules'                        : 'dbo',
    'Mining_Model_RulesPending'                 : 'dbo',
    'Mining_Operator_Daily'                     : 'dbo',
    'Mining_ProcessingPlant_Daily'              : 'dbo',
    'Mining_Production_Daily'                   : 'dbo',
    'Mining_Production_Forecast'                : 'dbo',
    'Mining_Reserves_Daily'                     : 'dbo',
    'Mining_Reserves_Forecast'                  : 'dbo',
    'Mining_Resource_Daily'                     : 'dbo',
    'Mining_Resource_Forecast'                  : 'dbo'
}

PARAM_POINTS         = {
            'asset_id': 50000,
           'operators': 4000,
       'resource_type': 750,
       'facility_type': 600,
         'constituent': 500,
     'production_peak': 100,
    'production_total': 100,
             'terrain': 100,
             'country': 50,
              'region': 10,
              'status': 2,
               'basin': 2,
         'param_table': 0,
           'params_id': 0,
         'param_value': 0
}

PARAM_LISTS          = {
    'model_rules'      : {
        'scored': [
            'asset_id',
            'operators',
            'resource_type',
            'facility_type',
            'constituent',
            'production_peak',
            'production_total',
            'terrain',
            'country',
            'region',
            'status',
            'basin',
            'param_table',
            'params_id',
            'param_value'
        ],
        'main': ['param_name']},

    'capex_alloc'      : {'scored': ['asset_id',
                                   'operators',
                                   'resource_type',
                                   'facility_type',
                                   'constituent',
                                   'production_peak',
                                   'production_total',
                                   'terrain',
                                   'country',
                                   'region',
                                   'status',
                                   'basin'],
                        'main'  : []},

    'capex_redev_alloc': {'scored': ['asset_id',
                                     'operators',
                                     'resource_type',
                                     'facility_type',
                                     'constituent',
                                     'production_peak',
                                     'production_total',
                                     'terrain',
                                     'country',
                                     'region',
                                     'status',
                                     'basin'],
                            'main': []},

    'abandonment_alloc': {'scored': ['asset_id',
                                     'operators',
                                     'resource_type',
                                     'facility_type',
                                     'constituent',
                                     'production_peak',
                                     'production_total',
                                     'terrain',
                                     'country',
                                     'region',
                                     'status',
                                     'basin'],
                            'main': []},

    'auxilary_param': {'scored': ['status',
                                  'country',
                                  'constituent',
                                  'region',
                                  'resource_type',
                                  'terrain'],
                         'main': ['param_name',
                                  'field_name',
                                  'data_range',
                                  'factor']}
}

MODEL_RULES_DATA     = {
                     'PRICING': {     'p_num': 8,
                                     'id_num': 13,
                                 'param_type': 'MODEL_RULES',
                                  'points_id': 14},

                 'MODEL_RULES': {     'p_num': 6,
                                     'id_num': 14,
                                 'param_type': 'MODEL_RULES',
                                  'points_id': 15},

               'OPEX_CAPACITY': {     'p_num': 6,
                                     'id_num': 15,
                                 'param_type': 'CAPACITY',
                                  'points_id': 16},

              'CAPEX_CAPACITY': {     'p_num': 6,
                                     'id_num': 15,
                                 'param_type': 'CAPACITY',
                                  'points_id': 16},

    'MINIMUM_DAILY_PRODUCTION': {     'p_num': 6,
                                     'id_num': 13,
                                 'param_type': '',
                                  'points_id': 14},

           'ABANDONMENT_ALLOC': {     'p_num': 6,
                                     'id_num': 6,
                                 'param_type': '',
                                  'points_id': 14},

           'CAPEX_REDEV_ALLOC': {     'p_num': 6,
                                     'id_num': 6,
                                 'param_type': '',
                                  'points_id': 14},

                 'CAPEX_ALLOC': {     'p_num': 6,
                                     'id_num': 6,
                                 'param_type': '',
                                  'points_id': 14},

                      'FISCAL': {     'p_num': 6,
                                     'id_num': 14,
                                 'param_type': 'MODEL_RULES',
                                  'points_id': 15},

}

SYSTEM_FLAGS         = [
	'model_discovered_fields',
	'calc_deals',
	'model_abandoned_uncon',
	'update_capex_opex',
	'detailed_models',
	'model_all',
	'model_non_engine',
	'full_forecast',
	'econ_limit',
	'store_engine_prod_data',
    'use_adj_decline',
	'export_engine_data',
	'clear_engine_data',
	'export_disc_field_data',
	'clear_disc_field_data',
    'export_to_test_db',
    'clear_internal_data',
    'clear_internal_data_df',
    'clear_internal_data_dt',
    'use_arps_updates',
    'use_prices_data'
]

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
XL_COLS = list(ALPHA) + sorted([x + y for (x, y) in itertools.product(ALPHA, repeat=2)])
WELL_NUMS = [('0'*(2-len(str(i))))+str(i) for i in range(1, 13)]
WELL_INPUTS_COLS = {well_num: XL_COLS[(6*int(well_num))] for well_num in WELL_NUMS}
WELL_INPUTS_ROWS = {
    'primary_resource'        : 20,
	'well_decline_rate'		  : 21,
	'constituent'			  : 22,
	'well_density'      	  : 23,
	'drilling_days'			  : 24,
	'completion_days'		  : 25,
	'rig_mobilization_days'	  : 26,
	'working_interest'		  : 27,
	'royalty_rate'			  : 28,
	'well_life'				  : 29,
	'acreage_pct'			  : 30,
	'drilling_pct'			  : 31,
	'annual_well_improve'	  : 32,
	'well_improve_start'	  : 33,
	'annual_well_degrade'	  : 34,
	'well_degrade_start'	  : 35,
	'drilling_cost'			  : 51,
	'completion_cost'		  : 52,
	'facility_cost'			  : 53,
	'tangible_split_pct'	  : 54,
	'capex_maintenance'		  : 55,
	'work_recom'			  : 56,
	'years_before_work_recom' : 57,
	'abandonment'			  : 58,
	'fixed_opex_rate'		  : 59,
	'opex_liquids'			  : 61,
	'opex_gas'				  : 62,
	'water_disp_fee'		  : 63,
	'ngls_proc_fee'			  : 64,
	'field_maintenance'		  : 65,
    'net_remain_loc'          : 66  # Need to change once finalized (to 38?) for maximum remaining net wells
}

FISCAL_COLS = [
    'year_num',
    'type_well_crude',
    'type_well_ng',
    'type_well_condensate',
    'type_well_ngls',
    'type_well_lng',
    'type_well_water',
    'gross_revenue',
    'type_well_capex',
    'type_well_opex',
    'fiscal_take',
    'pre_tax_cash_flow',
    'disc_pre_tax_cash_flow',
    'post_tax_cash_flow',
    'disc_post_tax_cash_flow'
]

DEV_IN_COLS = [
    'prod_year',
    'total_producing_net_wells',
    'annual_net_wells_comp',
    'capex_per_comp_well',
    'total_capex_input',
    'total_capex_calc',
    'hist_opex',
    'hist_crude',
    'hist_ng',
    'hist_condensate',
    'hist_ngls',
    'hist_lng',
    'hist_water',
    'rig_count',
    'producing_hist_net_wells',
    'duc_wells_comp',
    'new_net_wells_comp',
    'producing_hist_net_wells',
    'total_net_wells',
    'abandoned_net_wells',
    'total_abandoned_net_wells'
]

DEV_IN_COL_COUNT = len(DEV_IN_COLS) + 1
DEV_INPUT_COLS   = {type_well_num: {DEV_IN_COLS[i]: XL_COLS[(DEV_IN_COL_COUNT * (type_well_num-1)) + i] for i in range(len(DEV_IN_COLS))} for type_well_num in range(1,13)}
FISCAL_WELL_COLS = {type_well_num: {FISCAL_COLS[i]: XL_COLS[(DEV_IN_COL_COUNT * (type_well_num-1)) + i] for i in range(len(FISCAL_COLS))} for type_well_num in range(1,13)}
XL_FORMULAS = {
	'Asset Inputs': {
		'production'      : {
			'cell'        : 'B139',
			'formula'     : '''=IF($A140>=$E$10,IF($A140>=($E$10+'Well Inputs'!$H$29+'Well Inputs'!$H$30),0,SUMIF('Well Cash Flow'!$P$7:$P$117,$E$10 - 1,'Well Cash Flow'!W$7:W$117)*((1-'Well Inputs'!$H$21)^($A140 - ($E$10-1))))+SUMIF('Well Calculations'!$A$9:$A$728,$A140,'Well Calculations'!I$9:I$728)/12,SUMIF('Well Cash Flow'!$P$7:$P$117,'Asset Inputs'!$A140,'Well Cash Flow'!W$7:W$117))''',
			'template'    : '''=IF($A{1}>=$E$10,IF($A{1}>=($E$10+'Well Inputs'!${0}$29+'Well Inputs'!${0}$30),0,SUMIF('Well Cash Flow'!${6}$7:${6}$117,$E$10-1,'Well Cash Flow'!{15}$7:{15}$117)*((1-'Well Inputs'!${0}$21)^($A{1} - ($E$10-1))))+SUMIF('Well Calculations'!$A$9:$A$728,$A{1},'Well Calculations'!{16}$9:{16}$728)/12,SUMIF('Well Cash Flow'!${6}$7:${6}$117,'Asset Inputs'!$A{1},'Well Cash Flow'!{15}$7:{15}$117))'''
		},
		'capex tangible'  : {
			'cell'        : 'N139',

			'formula'     : '''=IF(A139<($E$10+'Well Inputs'!$G$29+'Well Inputs'!$G$30),IF(SUMIF('Well Cash Flow'!$P$9:$P$119,$A139,'Well Cash Flow'!$S$9:$S$119)>0,SUMIF('Well Cash Flow'!$P$9:$P$119,$A139,'Well Cash Flow'!$S$9:$S$119),(((('Well Inputs'!$G$50+'Well Inputs'!$G$51)+IFERROR('Well Inputs'!$G$52/'Well Inputs'!$G$27,0))*SUMIF('Well Cash Flow'!$P$9:$P$119,$A139,'Well Cash Flow'!$AF$9:$AF$119))+('Well Inputs'!$G$55*SUMIF('Well Cash Flow'!$P$9:$P$119,$A139,'Well Cash Flow'!$AE$9:$AE$119))+((('Well Inputs'!$G$51*'Well Inputs'!$G$27)+'Well Inputs'!$G$52)*SUMIF('Well Cash Flow'!$P$9:$P$119,$A139,'Well Cash Flow'!$V$9:$V$119)))+(IFERROR(SUMIF('Well Cash Flow'!$P$9:$P$119,A139-'Well Inputs'!$G$57,'Well Cash Flow'!$AF$9:$AF$119),0)*'Well Inputs'!$G$56)),0)*'Well Inputs'!$G$54''',
			'template'    : '''=IF(A{1}<($E$10+'Well Inputs'!${0}$29+'Well Inputs'!${0}$30),IF(SUMIF('Well Cash Flow'!${6}$7:${6}$117,$A{1},'Well Cash Flow'!${7}$7:${7}$117)>0,SUMIF('Well Cash Flow'!${6}$7:${6}$117,$A{1},'Well Cash Flow'!${7}$7:${7}$117),((('Well Inputs'!${0}$50+'Well Inputs'!${0}$51+'Well Inputs'!${0}$52)*SUMIF('Well Cash Flow'!${6}$7:${6}$117,$A{1},'Well Cash Flow'!${8}$7:${8}$117))+('Well Inputs'!${0}$55*SUMIF('Well Cash Flow'!${6}$7:${6}$117,$A{1},'Well Cash Flow'!${18}$7:${18}$117))+((('Well Inputs'!${0}$51+'Well Inputs'!${0}$52)*'Well Inputs'!${0}$27)*SUMIF('Well Cash Flow'!${6}$7:${6}$117,$A{1},'Well Cash Flow'!${17}$7:${17}$117)))+(IFERROR(SUMIF('Well Cash Flow'!${6}$7:${6}$117,A{1}-'Well Inputs'!${0}$57,'Well Cash Flow'!${8}$7:${8}$117),0)*'Well Inputs'!${0}$56)),0)*'Well Inputs'!${0}$54'''
		},
		'capex intangible': {
			'cell'        : 'O139',
			'formula'     : '''=N140*IFERROR('Well Inputs'!$H$53/'Well Inputs'!$H$54,0)''',
			'template'    : '''=N{1}*IFERROR('Well Inputs'!${0}$53/'Well Inputs'!${0}$54,0)'''
		},
		'abandonment'     : {
			'cell'        : 'P139',
			'formula'     : '''=IF($A140<($E$10 + 'Well Inputs'!$H$29 + 'Well Inputs'!$H$30),SUMIF('Well Cash Flow'!$P$7:$P$117,A140,'Well Cash Flow'!$AJ$7:$AJ$117)*'Well Inputs'!$H$58,0)''',
			'template'    : '''=IF($A{1}<($E$10+'Well Inputs'!${0}$29+'Well Inputs'!${0}$30),SUMIF('Well Cash Flow'!${6}$7:${6}$117,A{1},'Well Cash Flow'!${10}$7:${10}$117)*'Well Inputs'!${0}$58,0)'''
		},
		'fixed opex'      : {
			'cell'        : 'R139',
			'formula'     : '''=IF($A140<($E$10 + 'Well Inputs'!$H$29 + 'Well Inputs'!$H$30),'Well Cash Flow'!AG7*'Well Inputs'!$H$59,0)''',
			'template'    : '''=IF($A{1}<($E$10+'Well Inputs'!${0}$29+'Well Inputs'!${0}$30),'Well Cash Flow'!{9}7*'Well Inputs'!${0}$59,0)'''
		},
		'variable opex'   : {
			'cell'        : 'S139',
			'formula'     : '''=IF($A140<($E$10+'Well Inputs'!$H$29+'Well Inputs'!$H$30),IF(A140<$B$10,0,IF(SUMIF('Well Cash Flow'!$P$7:$P$117,A140,'Well Cash Flow'!$T$7:$T$117)>0,SUMIF('Well Cash Flow'!$P$7:$P$117,A140,'Well Cash Flow'!$T$7:$T$117)-R140,((B140+D140+E140)*365.242*'Well Inputs'!$H$61 + (C140+F140)*365.242*1000*'Well Inputs'!$H$62 + G140*365.242*'Well Inputs'!$H$63+E140*365.242*'Well Inputs'!$H$64)+SUMIF('Well Cash Flow'!$P$7:$P$117,A140,'Well Cash Flow'!$AH$7:$AH$117)*'Well Inputs'!$H$65)),0)''',
			'template'    : '''=IF($A{1}<($E$10+'Well Inputs'!${0}$29+'Well Inputs'!${0}$30),IF(A{1}<$B$10,0,IF(SUMIF('Well Cash Flow'!${6}$7:${6}$117,A{1},'Well Cash Flow'!${14}$7:${14}$117)>0,SUMIF('Well Cash Flow'!${6}$7:${6}$117,A{1},'Well Cash Flow'!${14}$7:${14}$117)-R{1},((B{1}+D{1}+E{1})*365.242*'Well Inputs'!${0}$61 + (C{1}+F{1})*365.242*1000*'Well Inputs'!${0}$62 + G{1}*365.242*'Well Inputs'!${0}$63+E{1}*365.242*'Well Inputs'!${0}$64)+SUMIF('Well Cash Flow'!${6}$7:${6}$117,A{1},'Well Cash Flow'!${9}$7:${9}$117)*'Well Inputs'!${0}$65)),0)'''
		}
	}
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Constants primarily asociated with discovered_analogues.py

SCORE_LIMITS = {
     'prod_min': 0,
     'cost_min': 0,
    'error_max': 5,
    'field_min': 20,
    'field_max': 20
}

PARAMS = {
    'main': ['reserve_volume',
             'api_gravity',
             'terrain',
             'ablock',
             'basin',
             'country',
             'region',
             'status'],

    'prod': ['formation',
             'reserve_volume',
             'form_rock_type',
             'api_gravity',
             'terrain',
             'trap_type',
             'ablock',
             'basin',
             'country',
             'region',
             'status'],

    'cost': ['facility_type',
             'pipeline',
             'gas_processing',
             'oil_storage',
             'gas_storage',
             'reserve_volume',
             'terrain',
             'api_gravity',
             'ablock',
             'basin',
             'country',
             'region',
             'status'],

     'all': ['formation',
             'facility_type',
             'pipeline',
             'gas_processing',
             'oil_storage',
             'gas_storage',
             'form_rock_type',
             'api_gravity',
             'terrain',
             'trap_type',
             'ablock',
             'basin',
             'country',
             'region',
             'status',
             'reserve_volume'
             ]
}

COST_ONLY = list(set(PARAMS['cost']) - set(PARAMS['prod']))
PROD_ONLY = list(set(PARAMS['prod']) - set(PARAMS['cost']))

RESERVE_FACTOR = {
    '1p'          : 1,
    '2p'          : 1,
    'Gas in place': 1,
    'Oil in place': 1,
    '3p'          : float(5.0/6.0),
    'Contingent'  : float(2.0/3.0),
    'Prospective' : float(2.0/3.0)
}

PARAM_DICT = {
    'prod': [param for param in PARAMS['prod'] if param != 'reserve_volume'] + ['reserve_volume'] + COST_ONLY,
    'cost': [param for param in PARAMS['cost'] if param != 'reserve_volume'] + ['reserve_volume'] + PROD_ONLY
}

PROD_PARAM_LISTS = {
          'capex_alloc': ['cx_year_minus5',
                          'cx_year_minus4',
                          'cx_year_minus3',
                          'cx_year_minus2',
                          'cx_year_minus1',
                          'cx_year_0',
                          'cx_year_1',
                          'cx_year_2',
                          'cx_year_3',
                          'cx_year_4',
                          'cx_year_5',
                          'cx_year_6'],

    'abandonment_alloc': ['aa_year_minus5',
                          'aa_year_minus4',
                          'aa_year_minus3',
                          'aa_year_minus2',
                          'aa_year_minus1',
                          'aa_year_0',
                          'aa_year_1',
                          'aa_year_2',
                          'aa_year_3',
                          'aa_year_4',
                          'aa_year_5',
                          'aa_year_6'],

    'capex_redev_alloc': ['cx_rd_year_minus5',
                          'cx_rd_year_minus4',
                          'cx_rd_year_minus3',
                          'cx_rd_year_minus2',
                          'cx_rd_year_minus1',
                          'cx_rd_year_0',
                          'cx_rd_year_1',
                          'cx_rd_year_2',
                          'cx_rd_year_3',
                          'cx_rd_year_4',
                          'cx_rd_year_5',
                          'cx_rd_year_6'],

      'total_init_prod': ['init_Crude Oil',
                          'init_Natural Gas',
                          'init_Condensate',
                          'init_LNG',
                          'init_NGL'],

      'total_peak_prod': ['peak_Crude Oil',
                          'peak_Natural Gas',
                          'peak_Condensate',
                          'peak_LNG',
                          'peak_NGL']
}

PROD_SCORES  = {
             'formation': {'points': 300},
        'reserve_volume': {'points': [300, 200, 125],
                           'ranges': [0.1, 0.3, 0.5]},
        'form_rock_type': {'points': 200},
           'api_gravity': {'points': 120,
                            'range': 3},
               'terrain': {
                   ('match','match')       : {'points': 100},
                   ('shallow','deep')      : {'points': 40},
                   ('ultra-deep','deep')   : {'points': 40},
                   ('shallow','ultra-deep'): {'points': 6},
                },
                 'basin': {'points': 250},
             'trap_type': {'points': 75},
                'ablock': {'points': 50},
               'country': {'points': 150},
                'region': {'points': 100},
                'status': {
                    'Producing': {'points': 5},
                    'Planned'  : {'points': 4},
                    'Abandoned': {'points': 3},
                    'Announced': {'points': 1}
                }
}

COST_SCORES  = { 'facility_type': {'points': 0},
                      'pipeline': {'points': [300, 200, 125],
                                   'ranges': [0.1, 0.3, 0.5]},
                'gas_processing': {'points': [300, 200, 125],
                                   'ranges': [0.1, 0.3, 0.5]},
                   'oil_storage': {'points': [300, 200, 125],
                                   'ranges': [0.1, 0.3, 0.5]},
                   'gas_storage': {'points': [300, 200, 125],
                                   'ranges': [0.1, 0.3, 0.5]},
                'reserve_volume': {'points': [300, 200, 125],
                                   'ranges': [0.1, 0.3, 0.5]},
                       'terrain': {
                   ('match','match'): {'points': 100},
                  ('shallow','deep'): {'points': 40},
               ('ultra-deep','deep'): {'points': 40},
            ('shallow','ultra-deep'): {'points': 6}
                                  },
                   'api_gravity': {'points': 50,
                                    'range': 3},
                         'basin': {'points': 250},
                        'ablock': {'points': 50},
                       'country': {'points': 150},
                        'region': {'points': 100},
                        'status': {
                           'Planned': {'points': 5},
                         'Producing': {'points': 4},
                         'Announced': {'points': 3},
                         'Abandoned': {'points': 3}
                                  }}

PLUS_MINUS_SCORES = ['api_gravity']
PERCENTAGE_SCORES = ['reserve_volume',
                     'pipeline',
                     'gas_processing',
                     'oil_storage',
                     'gas_storage']
OPTION_SCORES     = ['terrain',
                     'status']

M_PARAMS = ['analogue_id',
            'analogue_type',
            'total_score',
            'api_gravity',
            'reserve_volume',
            'terrain',
            'ablock',
            'basin',
            'country',
            'region',
            'status']

P_PARAMS = ['formation',
            'form_rock_type',
            'trap_type']

C_PARAMS = ['facility_type',
            'pipeline',
            'gas_processing',
            'oil_storage',
            'gas_storage']

ALL_PARAMS = M_PARAMS + P_PARAMS + C_PARAMS

VINTAGE_FACTOR     = 0.25
NO_RESERVES_FACTOR = 0.10
RECOV_FACTOR_MAX   = 0.60
AUX_SCORE_MAX      = 1.0
CONF_SCORE_MAX     = 5.0

CONF_WEIGHTS = {
     'facility_type': ( 0.0/24.0),
    'infrastructure': ( 3.0/24.0),
          'reserves': ( 5.0/24.0),
            'sulfur': ( 0.5/24.0),
           'hsulfur': ( 0.5/24.0),
       'api_gravity': ( 0.5/24.0),
         'calorific': ( 0.5/24.0),
    'carbon_dioxide': ( 0.5/24.0),
     'prod_analogue': (6.25/24.0),
     'cost_analogue': (6.25/24.0)
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Constants associated with server_import.py

TABLE_CONFIG  = {
           'production': {'format_str': '%s,"%s","%s","%s","%s","%s",%s,%s,"%s","%s","%s","%s","%s","%s","%s","%s"',
                           'date_cols': [13],
                            'num_cols': [6, 7],
                          'ext_tables': ['tblFieldProductionExtract_Africa',
                                         'tblFieldProductionExtract_Asia',
                                         'tblFieldProductionExtract_Caribbean',
                                         'tblFieldProductionExtract_CentralAmerica',
                                         'tblFieldProductionExtract_Europe',
                                         'tblFieldProductionExtract_FSU',
                                         'tblFieldProductionExtract_MiddleEast',
                                         'tblFieldProductionExtract_NorthAmerica',
                                         'tblFieldProductionExtract_Oceania',
                                         'tblFieldProductionExtract_SouthAmerica'],
                        # 'ext_tables': ['tblFieldProductionExtract_Africa'],
                        #                  'tblFieldProductionExtract_MiddleEast'],
                                'cols': ['AssetID',
                                         'AssetName',
                                         'Country_Name',
                                         'Constituent Entity',
                                         'Region',
                                         'Commodity',
                                         'Period_Yr',
                                         'Production',
                                         'Unit',
                                         'CaseType',
                                         'AssetRelationship',
                                         'Sources',
                                         'DataSource',
                                         'Last Update']},

               'equity': {'format_str': '%s,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"',
                           'date_cols': [7, 9],
                            'num_cols': [],
                          'ext_tables': ['tblFieldEquityExtract'],
                                'cols': ['AssetID',
                                         'AssetName',
                                         'Country_Name',
                                         'Constituent Entity',
                                         'Region',
                                         'Equity',
                                         'Eq_Percentage',
                                         'Eq_Date',
                                         'Operator',
                                         'Last Update',
                                         'Top Parent Company',
                                         'Profit Share',
                                         'Cost Share']},

             'reserves': {'format_str': '%s,"%s","%s","%s","%s","%s","%s","%s","%s","%s",%s,"%s","%s","%s","%s","%s","%s","%s"',
                           'date_cols': [9, 15],
                            'num_cols': [10],
                          'ext_tables': ['tblFieldReserveExtract'],
                                'cols': ['AssetID',
                                         'AssetName',
                                         'Country_Name',
                                         'Constituent Entity',
                                         'Region',
                                         'Field Status',
                                         'ReserveStatus',
                                         'ReserveType',
                                         'Commodity',
                                         'ReservePublishedDate',
                                         'ReserveVolume',
                                         'Unit',
                                         'ReserveSource',
                                         'CaseType',
                                         'DataSource',
                                         'Last Update']},

               'assets': {'format_str': '%s,' + ('"%s",'*51) + '"%s","%s","%s"',
                           'date_cols': [52],
                            'num_cols': [],
                          'ext_tables': ['tblFieldBasicExtract'],
                                'cols': ['AssetID',
                                         'AssetName',
                                         'Country_Name',
                                         'Constituent Entity',
                                         'Region',
                                         'Status',
                                         'Field Terrain',
                                         'BasinName',
                                         'Resource Type',
                                         'ProductionPhase',
                                         'Recovery Factor',
                                         'AssociatedParentID',
                                         'AssociatedParentFieldName',
                                         'AssociatedParentFieldRegion',
                                         'AssociatedParentFieldCountry',
                                         'AssociatedParentFieldArea',
                                         'Primary Trap Type',
                                         'Gravity',
                                         'Sulphur',
                                         'LicenseNumber',
                                         'County',
                                         'Calorific Value',
                                         'Hydrogen Sulfide Content',
                                         'Gas Oil Ratio',
                                         'Associated Block',
                                         'Associated Block Region',
                                         'Associated Block Country',
                                         'Associated Block Constituent Entity',
                                         'AssetRelationship',
                                         'IRR(%)',
                                         'Payback(years)',
                                         'CapitalExpenditurePerboe(US$/boe)',
                                         'OperatingExpenditurePerboe(US$/boe)',
                                         'ReserveStatus',
                                         'NPV(US$MM)',
                                         'BaseCaseRemainingNPVUS$MM',
                                         'LowCaseRemainingNPVUS$MM',
                                         'HighCaseRemainingNPVUS$MM',
                                         'Facility Type',
                                         'Formation',
                                         'Max Water Depth (ft)',
                                         'DiscoveryDate',
                                         'FieldLicenseNumber',
                                         'LicenseEffectiveDate',
                                         'LicenseExpiryDate',
                                         'Porosity',
                                         'Permeability',
                                         'MeasuredDepth',
                                         'Carbon dioxide',
                                         'FormationRockType',
                                         'DataSource',
                                         'Fiscal Regime',
                                         'Last Update']},

       'sourced_expend': {'format_str': '%s,"%s","%s","%s","%s","%s",%s,%s,"%s","%s",%s,"%s"',
                           'date_cols': [],
                            'num_cols': [],
                          'ext_tables': ['tblGESourcedExpenditureDataExtract'],
                                'cols': ['AssetID',
                                         'AssetName',
                                         'Country_Name',
                                         'Constituent Entity',
                                         'Region',
                                         'ExpenditureType',
                                         'Year',
                                         'ExpenditurePeriod',
                                         'Currency',
                                         'Unit',
                                         'Value',
                                         'ExtractDate']},

    'currency_exchange': {'format_str': '%s,%s,"%s","%s",%s',
                           'date_cols': [],
                            'num_cols': [],
                          'ext_tables': ['tblGECurrency'],
                                'cols': ['CurrencyID',
                                         'Year',
                                         'From',
                                         'To',
                                         'ConversionFactor']},

     'projects_extract': {'format_str': '%s,"%s","%s","%s","%s","%s","%s","%s","%s",%s,"%s","%s","%s"',
                           'date_cols': [],
                            'num_cols': [],
                          'ext_tables': ['tblFieldProjectsExtract'],
                                'cols': ['FieldAssetID',
                                         'Project Name',
                                         'Project Segment',
                                         'Project country',
                                         'Project Region',
                                         'Project Type',
                                         'Project Stage',
                                         'Project Active Year',
                                         'Project Cost (US$ mil)',
                                         'Associated Project Asset ID',
                                         'EPC Contractor',
                                         'Stage Change Quarter',
                                         'FID']}
    }

TABLE_COLUMNS = {
         'tblFieldProductionExtract': ['AssetID',
                                       'AssetName',
                                       'Country_Name',
                                       'Constituent Entity',
                                       'Region',
                                       'Commodity',
                                       'Period_Yr',
                                       'Production',
                                       'Unit',
                                       'CaseType',
                                       'AssetRelationship',
                                       'Sources',
                                       'DataSource',
                                       'Last Update'],

             'tblFieldEquityExtract': ['AssetID',
                                       'AssetName',
                                       'Country_Name',
                                       'Constituent Entity',
                                       'Region',
                                       'Equity',
                                       'Eq_Percentage',
                                       'Eq_Date',
                                       'Operator',
                                       'Last Update',
                                       'Top Parent Company',
                                       'Profit Share',
                                       'Cost Share'],

            'tblFieldReserveExtract': ['AssetID',
                                       'AssetName',
                                       'Country_Name',
                                       'Constituent Entity',
                                       'Region',
                                       'Field Status',
                                       'ReserveStatus',
                                       'ReserveType',
                                       'Commodity',
                                       'ReservePublishedDate',
                                       'ReserveVolume',
                                       'Unit',
                                       'ReserveSource',
                                       'CaseType',
                                       'DataSource',
                                       'Last Update'],

              'tblFieldBasicExtract': ['AssetID',
                                       'AssetName',
                                       'Country_Name',
                                       'Constituent Entity',
                                       'Region',
                                       'Status',
                                       'Field Terrain',
                                       'BasinName',
                                       'Resource Type',
                                       'ProductionPhase',
                                       'Recovery Factor',
                                       'AssociatedParentID',
                                       'AssociatedParentFieldName',
                                       'AssociatedParentFieldRegion',
                                       'AssociatedParentFieldCountry',
                                       'AssociatedParentFieldArea',
                                       'Primary Trap Type',
                                       'Gravity',
                                       'Sulphur',
                                       'LicenseNumber',
                                       'County',
                                       'Calorific Value',
                                       'Hydrogen Sulfide Content',
                                       'Gas Oil Ratio',
                                       'Associated Block',
                                       'Associated Block Region',
                                       'Associated Block Country',
                                       'Associated Block Constituent Entity',
                                       'AssetRelationship',
                                       'IRR(%)',
                                       'Payback(years)',
                                       'CapitalExpenditurePerboe(US$/boe)',
                                       'OperatingExpenditurePerboe(US$/boe)',
                                       'ReserveStatus',
                                       'NPV(US$MM)',
                                       'BaseCaseRemainingNPVUS$MM',
                                       'LowCaseRemainingNPVUS$MM',
                                       'HighCaseRemainingNPVUS$MM',
                                       'Facility Type',
                                       'Formation',
                                       'Max Water Depth (ft)',
                                       'DiscoveryDate',
                                       'FieldLicenseNumber',
                                       'LicenseEffectiveDate',
                                       'LicenseExpiryDate',
                                       'Porosity',
                                       'Permeability',
                                       'MeasuredDepth',
                                       'Carbon dioxide',
                                       'FormationRockType',
                                       'DataSource',
                                       'Fiscal Regime',
                                       'Last Update'],

'tblGESourcedExpenditureDataExtract': ['AssetID',
                                       'AssetName',
                                       'Country_Name',
                                       'Constituent Entity',
                                       'Region',
                                       'ExpenditureType',
                                       'Year',
                                       'ExpenditurePeriod',
                                       'Currency',
                                       'Unit',
                                       'Value',
                                       'ExtractDate'],

                     'tblGECurrency': ['CurrencyID',
                                       'Year',
                                       'From',
                                       'To',
                                       'ConversionFactor'],

           'tblFieldProjectsExtract': ['FieldAssetID',
                                       'Project Name',
                                       'Project Segment',
                                       'Project country',
                                       'Project Region',
                                       'Project Type',
                                       'Project Stage',
                                       'Project Active Year',
                                       'Project Cost (US$ mil)',
                                       'Associated Project Asset ID',
                                       'EPC Contractor',
                                       'Stage Change Quarter',
                                       'FID']

    }

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Constants primarily associated with data_export.py

MAIN_COLS  = ['AssetID',
              'AssetName',
              'Country',
              'Region',
              'CreatedDate']

TABLE_COLS = {
    'tblEngineCommodityPriceSourceData' : [
        'CrudeOil',
        'NaturalGas',
        'Condensate',
        'NGLs',
        'LNG'
    ],

    'tblEngineDataPoints'               : [
        '[Payback (years)]',
        'NPVUS$MM',
        '[CapitalExpenditurePerboe (US$/boe)]',
        '[OperatingExpenditurePerboe (US$/boe)]',
        '[Remaining break-even oil price ($/bbl)]',
        '[IRR (%)]',
        'RemainingNPVUS$MM',
        '[Remaining break-even gas price ($/mcf)]',
        '[Full-cycle break-even oil price ($/bbl)]',
        '[Full-cycle break-even gas price ($/mcf)]',
        'MinimumEconomicFieldsSize',
        'MaximumEconomicDeveopmentCost',
        'ConfidenceScore',
        'ProductionAnalogRank',
        'CostAnalogRank',
        #'FacilityTypeMatchRank',
        'NearbyInfrastructureRank',
        'ReservesDataAvailability',
        'HydrocarbonQualityDataAvailability'
    ],

    'tblEngineFEATData'                 : [
        '[CrudeOil ($/bbl)]',
        '[NaturalGas ($/mcf)]',
        '[Condensate ($/bbl)]',
        '[NGLs ($/bbl)]',
        '[LNG ($/mcf)]',
        '[Crude oil (US$)]',
        '[Natural gas (US$)]',
        '[Condensate (US$)]',
        '[NGLs (US$)]',
        '[LNG (US$)]',
        '[Total (US$)]',
        '[E&A (US$)]',
        '[Tangibles (US$)]',
        '[Intangibles (US$)]',
        '[Abandonment (US$)]',
        '[Others (US$)]',
        '[Total Capital Expenditure (US$)]',
        '[Fixed (US$)]',
        '[Variable (US$)]',
        '[Total Operating Expenditure (US$)]',
        '[Payments (US$)]',
        '[Receipts (US$)]'
    ],

    'tblEngineFEATData_Extn'            : [
        '[Ring-fenced fiscal take (US$)]',
        '[Allowance 1 (US$)]',
        '[Allowance 2 (US$)]',
        '[Allowance 3 (US$)]',
        '[WTI ($/bbl)]',
        '[BRENT ($/bbl)]',
        '[URALS ($/bbl)]',
        '[HH ($/mcf)]',
        '[Bechmark 1]',
        '[Bechmark 2]',
        '[Bechmark 3]',
        '[Bechmark 4]',
        '[FX RATE (GTQ/USD)]'
    ],

    'tblEngineProductionData'           : [
        '[Crude Oil]',
        '[Natural Gas]',
        'Condensate',
        'NGL',
        'LNG',
        '[Total Capital Expenditure US$]',
        '[Total Operating Expenditure US$]',
        '[Total Pre Tax Cash Flow US$]',
        '[Total Post Tax Cash Flow US$]',
        '[State Net Cash Flow (US$)]',
        '[Entitlement Crude Oil]',
        '[Entitlement Natural Gas]',
        '[Entitlement Condensate]',
        '[Entitlement NGLs]',
        '[Entitlement LNG]',
        'AssetStatus',
        'ProductionStartYear'
    ],

    'tblEngineAnalogueFields'           : [
        'ProductionAnaloguesFieldID',
        'CostAnaloguesFieldID'
    ],

    'tblEngineWellInputInfo'            : [
        'Pre-tax well NPV10 ($)',
        'Post-tax well NPV10 ($)',
        'Pre-tax well IRR',
        'Post-tax well IRR',
        'Pre-Tax Break-Even Oil Price (US$/bbl)',
        'Pre-Tax Break-Even Gas Price (US$/mcf)',
        'Post-Tax Break-Even Oil Price (US$/bbl)',
        'Post-Tax Break-Even Gas Price (US$/mcf)',
        'Working Interest (%)',
        'Royalty Rate',
        'Well EUR-oil (bbl)',
        'Well EUR-gas (mmcf)',
        'Well EUR-condensate (bbl)',
        'Well EUR-NGLs (bbl)',
        'Well EUR-total (boe)',
        'IP30-oil (bd)',
        'IP30-gas (mmcfd)',
        'IP30-condensate (bd)',
        'IP30-NGLs (bd)',
        'Historical production decline',
        'Rig mobilization time (days)',
        'Well life (years)',
        'Facilities ($)',
        'Tangible cost percent split',
        'Annual maintainance capital expenditure ($)',
        'Abandonment ($)',
        'Fixed Operating Expenditure ($)',
        'Liquids transportation ($/bbl)',
        'Gas transportation ($/mcf)',
        'Well drilling time (days)',
        'Well completion time (days)',
        'Drilling ($)',
        'Completion ($)'
                                       ],

    'tblEngineWellDataInfo'             : [
        'Rigs',
        '[Historical Wells Added]',
        '[Type Wells Added]',
        '[DUC Wells Added]',
        '[Historical Wells Total]',
        '[Type Wells Total]',
        '[DUC Wells Total]',
        '[Historical Crude (boe)]',
        '[Type-well Crude (boe)]',
        '[DUC Crude (boe)]',
        '[Historical Natural Gas (boe)]',
        '[Type-well Natural Gas (boe)]',
        '[DUC Natural Gas (boe)]',
        '[Historical Condensate (boe)]',
        '[Type-well Condensate (boe)]',
        '[DUC Condensate (boe)]',
        '[Historical NGLs (boe)]',
        '[Type-well NGLs (boe)]',
        '[DUC NGLs (boe)]'
    ],

    'tblEngineWellInputProductionInfo'  : [
        '[Crude Oil (bbl)]',
        '[Natural Gas (mmcf)]',
        '[Condensate (bbl)]',
        '[NGLs (bbl)]',
        '[Total (boe)]',
        '[Capital Expenditure Tangible]',
        '[Capital Expenditure Intangible]',
        '[Total Operating Expenditure ($)]',
        '[Total Pre-tax Cash Flow ($)]',
        '[Fiscal Take ($)]',
        '[Total Post-tax Cash Flow ($)]'
    ],

    'tblEngineCashFlowData'             : [
        '[Gross revenue]',
        '[Royalties bonuses fees]',
        '[Capital expenditure]',
        '[Operating expenditure]',
        '[Depreciation and amortization]',
        '[State entitlement]',
        '[Total tax payable]',
        '[Other payments to state]',
        '[Pre-tax cash flow]',
        '[Post-tax cash flow]',
        '[Remaining NPV10]'
    ],

    'tblEngineAssetSenRemainingNPV'     : [
        '[-20]',
        '[-10]',
        '[0]',
        '[10]',
        '[20]'
    ]
}

EXT_TABLES = [
    'tblEngineDataPoints',
    'tblEngineFEATData',
    'tblEngineCommodityPriceSourceData',
    'tblEngineFEATData_Extn',
    'tblEngineProductionData',
    'tblEngineAnalogueFields',
    'tblEngineWellInputInfo',
    'tblEngineWellInputProductionInfo',
    'tblEngineCashFlowData',
    'tblEngineAssetSenRemainingNPV',
    'tblEngineWellDataInfo'
]
#
# EXT_TABLES = [
#     'tblEngineDataPoints']
# EXT_TABLES = [
#      'tblEngineFEATData',
#     'tblEngineCommodityPriceSourceData',
#     'tblEngineFEATData_Extn',
#     'tblEngineProductionData',
#     'tblEngineAnalogueFields',
#     'tblEngineWellInputInfo',
#     'tblEngineWellInputProductionInfo',
#     'tblEngineCashFlowData',
#     'tblEngineAssetSenRemainingNPV',
#     'tblEngineWellDataInfo']  ##Remove after debug and uncomment above list

EXT_LIMIT_TABLES = [
    'tblEngineDataPoints',
    'tblEngineFEATData',
    'tblEngineCommodityPriceSourceData',
    'tblEngineFEATData_Extn',
    'tblEngineProductionData',
    'tblEngineWellInputInfo',
    'tblEngineWellInputProductionInfo',
    'tblEngineCashFlowData',
    'tblEngineAssetSenRemainingNPV'
]

COL_REFS = {
    'Asset Inputs'      : {
        'CrudeOil'                                      : {'tbl': 'tblEngineCommodityPriceSourceData', 'ref': 'H20',                    'null': ''},
        'NaturalGas'                                    : {'tbl': 'tblEngineCommodityPriceSourceData', 'ref': 'I20',                    'null': ''},
        'Condensate'                                    : {'tbl': 'tblEngineCommodityPriceSourceData', 'ref': 'J20',                    'null': ''},
        'NGLs'                                          : {'tbl': 'tblEngineCommodityPriceSourceData', 'ref': 'K20',                    'null': ''},
        'LNG'                                           : {'tbl': 'tblEngineCommodityPriceSourceData', 'ref': 'L20',                    'null': ''},
        'AssetStatus'                                   : {'tbl': 'tblEngineProductionData',           'ref': 'AA23',                   'null': ''},
        'ProductionStartYear'                           : {'tbl': 'tblEngineProductionData',           'ref': 'B10',                    'null': 0}
    },

    'Asset Summary'     : {
        '[Full-cycle break-even oil price ($/bbl)]'     : {'tbl': 'tblEngineDataPoints',                'ref': 'B',                     'null': '0.0'},
        '[Full-cycle break-even gas price ($/mcf)]'     : {'tbl': 'tblEngineDataPoints',                'ref': 'C',                     'null': '0.0'},
        '[Remaining break-even oil price ($/bbl)]'      : {'tbl': 'tblEngineDataPoints',                'ref': 'D',                     'null': '0.0'},
        '[Remaining break-even gas price ($/mcf)]'      : {'tbl': 'tblEngineDataPoints',                'ref': 'E',                     'null': '0.0'},
        'MinimumEconomicFieldsSize'                     : {'tbl': 'tblEngineDataPoints',                'ref': 'F83',                   'null': None},
        'MaximumEconomicDeveopmentCost'                 : {'tbl': 'tblEngineDataPoints',                'ref': 'G83',                   'null': None},
        'ConfidenceScore'                               : {'tbl': 'tblEngineDataPoints',                'ref': 'H83',                   'null': None},
        'ProductionAnalogRank'                          : {'tbl': 'tblEngineDataPoints',                'ref': 'I83',                   'null': None},
        'CostAnalogRank'                                : {'tbl': 'tblEngineDataPoints',                'ref': 'J83',                   'null': None},
        #'FacilityTypeMatchRank'                         : {'tbl': 'tblEngineDataPoints',                'ref': 'K83',                   'null': None},
        'NearbyInfrastructureRank'                      : {'tbl': 'tblEngineDataPoints',                'ref': 'K83',                   'null': None},
        'ReservesDataAvailability'                      : {'tbl': 'tblEngineDataPoints',                'ref': 'L83',                   'null': None},
        'HydrocarbonQualityDataAvailability'            : {'tbl': 'tblEngineDataPoints',                'ref': 'M83',                   'null': None},
        'ProductionAnaloguesFieldID'                    : {'tbl': 'tblEngineAnalogueFields',            'ref': 'A',                     'null': None},
        'CostAnaloguesFieldID'                          : {'tbl': 'tblEngineAnalogueFields',            'ref': 'B',                     'null': None}
    },

    'Asset Sensitivity' : {
        '[IRR (%)]'         : {'tbl': 'tblEngineDataPoints', 'ref': 'D', 'null': '0.0'},
        '[Payback (years)]' : {'tbl': 'tblEngineDataPoints', 'ref': 'E', 'null': '0.0'},
        '[-20]'             : {'tbl': 'tblEngineAssetSenRemainingNPV', 'null': '0',
                               'ref': {'Price': 'C25',
                                   'Production': 'C26',
                                   'Capital expenditure': 'C27',
                                   'Operating expenditure': 'C28',
                                   'Royalties, bonuses and fees': 'C29',
                                   'State share of profit oil': 'C30',
                                   'Taxes': 'C31'}},
        '[-10]'             : {'tbl': 'tblEngineAssetSenRemainingNPV','null': '0',
                               'ref': {                      'Price': 'D25',
                                   'Production': 'D26',
                                   'Capital expenditure': 'D27',
                                   'Operating expenditure': 'D28',
                                   'Royalties, bonuses and fees': 'D29',
                                   'State share of profit oil': 'D30',
                                   'Taxes': 'D31'}},
        '[0]'               : {'tbl': 'tblEngineAssetSenRemainingNPV', 'null': '0',
                               'ref': {                    'Price': 'E25',
                                   'Production': 'E26',
                                   'Capital expenditure': 'E27',
                                   'Operating expenditure': 'E28',
                                   'Royalties, bonuses and fees': 'E29',
                                   'State share of profit oil': 'E30',
                                   'Taxes': 'E31'}},
        '[10]'              : {'tbl': 'tblEngineAssetSenRemainingNPV', 'null': '0',
                              'ref': {                    'Price': 'F25',
                                   'Production': 'F26',
                                   'Capital expenditure': 'F27',
                                   'Operating expenditure': 'F28',
                                   'Royalties, bonuses and fees': 'F29',
                                   'State share of profit oil': 'F30',
                                   'Taxes': 'F31'}},
        '[20]'              : {'tbl': 'tblEngineAssetSenRemainingNPV', 'null': '0',
                               'ref': {                    'Price': 'G25',
                                   'Production': 'G26',
                                   'Capital expenditure': 'G27',
                                   'Operating expenditure': 'G28',
                                   'Royalties, bonuses and fees': 'G29',
                                   'State share of profit oil': 'G30',
                                   'Taxes': 'G31'}}
    },

    'Calculations'      : {
        '[CrudeOil ($/bbl)]'                            : {'tbl': 'tblEngineFEATData',                  'ref': 'I',                     'null': '0.0'},
        '[NaturalGas ($/mcf)]'                          : {'tbl': 'tblEngineFEATData',                  'ref': 'J',                     'null': '0.0'},
        '[Condensate ($/bbl)]'                          : {'tbl': 'tblEngineFEATData',                  'ref': 'K',                     'null': '0.0'},
        '[NGLs ($/bbl)]'                                : {'tbl': 'tblEngineFEATData',                  'ref': 'L',                     'null': '0.0'},
        '[LNG ($/mcf)]'                                 : {'tbl': 'tblEngineFEATData',                  'ref': 'M',                     'null': '0.0'},
        '[Crude oil (US$)]'                             : {'tbl': 'tblEngineFEATData',                  'ref': 'N',                     'null': '0.0'},
        '[Natural gas (US$)]'                           : {'tbl': 'tblEngineFEATData',                  'ref': 'O',                     'null': '0.0'},
        '[Condensate (US$)]'                            : {'tbl': 'tblEngineFEATData',                  'ref': 'P',                     'null': '0.0'},
        '[NGLs (US$)]'                                  : {'tbl': 'tblEngineFEATData',                  'ref': 'Q',                     'null': '0.0'},
        '[LNG (US$)]'                                   : {'tbl': 'tblEngineFEATData',                  'ref': 'R',                     'null': '0.0'},
        '[Total (US$)]'                                 : {'tbl': 'tblEngineFEATData',                  'ref': 'S',                     'null': '0.0'},
        '[E&A (US$)]'                                   : {'tbl': 'tblEngineFEATData',                  'ref': 'T',                     'null': '0.0'},
        '[Tangibles (US$)]'                             : {'tbl': 'tblEngineFEATData',                  'ref': 'U',                     'null': '0.0'},
        '[Intangibles (US$)]'                           : {'tbl': 'tblEngineFEATData',                  'ref': 'V',                     'null': '0.0'},
        '[Abandonment (US$)]'                           : {'tbl': 'tblEngineFEATData',                  'ref': 'W',                     'null': '0.0'},
        '[Others (US$)]'                                : {'tbl': 'tblEngineFEATData',                  'ref': 'X',                     'null': '0.0'},
        '[Total Capital Expenditure (US$)]'             : {'tbl': 'tblEngineFEATData',                  'ref': 'Y',                     'null': '0.0'},
        '[Fixed (US$)]'                                 : {'tbl': 'tblEngineFEATData',                  'ref': 'Z',                     'null': '0.0'},
        '[Variable (US$)]'                              : {'tbl': 'tblEngineFEATData',                  'ref': 'AA',                    'null': '0.0'},
        '[Total Operating Expenditure (US$)]'           : {'tbl': 'tblEngineFEATData',                  'ref': 'AB',                    'null': '0.0'},
        '[Payments (US$)]'                              : {'tbl': 'tblEngineFEATData',                  'ref': 'AC',                    'null': '0.0'},
        '[Receipts (US$)]'                              : {'tbl': 'tblEngineFEATData',                  'ref': 'AD',                    'null': '0.0'},
        '[Crude Oil]'                                   : {'tbl': 'tblEngineProductionData',            'ref': 'B',                     'null': '0.0'},
        '[Natural Gas]'                                 : {'tbl': 'tblEngineProductionData',            'ref': 'C',                     'null': '0.0'},
        'Condensate'                                    : {'tbl': 'tblEngineProductionData',            'ref': 'D',                     'null': '0.0'},
        'NGL'                                           : {'tbl': 'tblEngineProductionData',            'ref': 'E',                     'null': '0.0'},
        'LNG'                                           : {'tbl': 'tblEngineProductionData',            'ref': 'F',                     'null': '0.0'},
        '[Entitlement Crude Oil]'                       : {'tbl': 'tblEngineProductionData',            'ref': 'AI',                    'null': '0.0'},
        '[Entitlement Natural Gas]'                     : {'tbl': 'tblEngineProductionData',            'ref': 'AJ',                    'null': '0.0'},
        '[Entitlement Condensate]'                      : {'tbl': 'tblEngineProductionData',            'ref': 'AK',                    'null': '0.0'},
        '[Entitlement NGLs]'                            : {'tbl': 'tblEngineProductionData',            'ref': 'AL',                    'null': '0.0'},
        '[Entitlement LNG]'                             : {'tbl': 'tblEngineProductionData',            'ref': 'AM',                    'null': '0.0'},
        '[Ring-fenced fiscal take (US$)]'               : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AN',                    'null': '0.0'},
        '[Allowance 1 (US$)]'                           : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AO',                    'null': '0.0'},
        '[Allowance 2 (US$)]'                           : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AP',                    'null': '0.0'},
        '[Allowance 3 (US$)]'                           : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AQ',                    'null': '0.0'},
        '[WTI ($/bbl)]'                                 : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AR',                    'null': '0.0'},
        '[BRENT ($/bbl)]'                               : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AS',                    'null': '0.0'},
        '[URALS ($/bbl)]'                               : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AT',                    'null': '0.0'},
        '[HH ($/mcf)]'                                  : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AU',                    'null': '0.0'},
        '[Bechmark 1]'                                  : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AV',                    'null': '0.0'},
        '[Bechmark 2]'                                  : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AW',                    'null': '0.0'},
        '[Bechmark 3]'                                  : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AX',                    'null': '0.0'},
        '[Bechmark 4]'                                  : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AY',                    'null': '0.0'},
        '[FX RATE (GTQ/USD)]'                           : {'tbl': 'tblEngineFEATData_Extn',             'ref': 'AZ',                    'null': '0.0'}
    },

    'Cash Flow'         : {
        '[Gross revenue]'                               : {'tbl': 'tblEngineCashFlowData',              'ref': 'B',                     'null': '0.0'},
        '[Royalties bonuses fees]'                      : {'tbl': 'tblEngineCashFlowData',              'ref': 'C',                     'null': '0.0'},
        '[Capital expenditure]'                         : {'tbl': 'tblEngineCashFlowData',              'ref': 'D',                     'null': '0.0'},
        '[Operating expenditure]'                       : {'tbl': 'tblEngineCashFlowData',              'ref': 'E',                     'null': '0.0'},
        '[Depreciation and amortization]'               : {'tbl': 'tblEngineCashFlowData',              'ref': 'F',                     'null': '0.0'},
        '[State entitlement]'                           : {'tbl': 'tblEngineCashFlowData',              'ref': 'G',                     'null': '0.0'},
        '[Total tax payable]'                           : {'tbl': 'tblEngineCashFlowData',              'ref': 'H',                     'null': '0.0'},
        '[Other payments to state]'                     : {'tbl': 'tblEngineCashFlowData',              'ref': 'I',                     'null': '0.0'},
        '[Pre-tax cash flow]'                           : {'tbl': 'tblEngineCashFlowData',              'ref': 'J',                     'null': '0.0'},
        '[Post-tax cash flow]'                          : {'tbl': 'tblEngineCashFlowData',              'ref': 'K',                     'null': '0.0'},
        '[Remaining NPV10]'                             : {'tbl': 'tblEngineCashFlowData',              'ref': 'L',                     'null': '0.0'}
        },

    'Type Well Inputs'  : {
        '[Crude Oil (bbl)]'                             : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 0,                       'null': '0.0'},
        '[Natural Gas (mmcf)]'                          : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 1,                       'null': '0.0'},
        '[Condensate (bbl)]'                            : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 2,                       'null': '0.0'},
        '[NGLs (bbl)]'                                  : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 3,                       'null': '0.0'},
        'Historical production decline'                 : {'tbl': 'tblEngineWellInputInfo',             'ref': '21',                    'null': '0.0'},
        'Well drilling time (days)'                     : {'tbl': 'tblEngineWellInputInfo',             'ref': '24',                    'null': '0.0'},
        'Well completion time (days)'                   : {'tbl': 'tblEngineWellInputInfo',             'ref': '25',                    'null': '0.0'},
        'Rig mobilization time (days)'                  : {'tbl': 'tblEngineWellInputInfo',             'ref': '26',                    'null': '0.0'},
        'Working Interest (%)'                          : {'tbl': 'tblEngineWellInputInfo',             'ref': '27',                    'null': '0.0'},
        'Royalty Rate'                                  : {'tbl': 'tblEngineWellInputInfo',             'ref': '28',                    'null': '0.0'},
        'Well life (years)'                             : {'tbl': 'tblEngineWellInputInfo',             'ref': '29',                    'null': '0.0'},
        'Well EUR-oil (bbl)'                            : {'tbl': 'tblEngineWellInputInfo',             'ref': '39',                    'null': '0.0'},
        'Well EUR-gas (mmcf)'                           : {'tbl': 'tblEngineWellInputInfo',             'ref': '40',                    'null': '0.0'},
        'Well EUR-condensate (bbl)'                     : {'tbl': 'tblEngineWellInputInfo',             'ref': '41',                    'null': '0.0'},
        'Well EUR-NGLs (bbl)'                           : {'tbl': 'tblEngineWellInputInfo',             'ref': '42',                    'null': '0.0'},
        'Well EUR-total (boe)'                          : {'tbl': 'tblEngineWellInputInfo',             'ref': '43',                    'null': '0.0'},
        'Pre-tax well NPV10 ($)'                        : {'tbl': 'tblEngineWellInputInfo',             'ref': '44',                    'null': '0.0'},
        'Post-tax well NPV10 ($)'                       : {'tbl': 'tblEngineWellInputInfo',             'ref': '47',                    'null': '0.0'},
        'Pre-tax well IRR'                              : {'tbl': 'tblEngineWellInputInfo',             'ref': '45',                    'null': '0.0'},
        'Post-tax well IRR'                             : {'tbl': 'tblEngineWellInputInfo',             'ref': '48',                    'null': '0.0'},
        'Drilling ($)'                                  : {'tbl': 'tblEngineWellInputInfo',             'ref': '51',                    'null': '0.0'},
        'Completion ($)'                                : {'tbl': 'tblEngineWellInputInfo',             'ref': '52',                    'null': '0.0'},
        'Facilities ($)'                                : {'tbl': 'tblEngineWellInputInfo',             'ref': '53',                    'null': '0.0'},
        'Tangible cost percent split'                   : {'tbl': 'tblEngineWellInputInfo',             'ref': '54',                    'null': '0.0'},
        'Annual maintainance capital expenditure ($)'   : {'tbl': 'tblEngineWellInputInfo',             'ref': '55',                    'null': '0.0'},
        'Abandonment ($)'                               : {'tbl': 'tblEngineWellInputInfo',             'ref': '58',                    'null': '0.0'},
        'Fixed Operating Expenditure ($)'               : {'tbl': 'tblEngineWellInputInfo',             'ref': '59',                    'null': '0.0'},
        'Liquids transportation ($/bbl)'                : {'tbl': 'tblEngineWellInputInfo',             'ref': '61',                    'null': '0.0'},
        'Gas transportation ($/mcf)'                    : {'tbl': 'tblEngineWellInputInfo',             'ref': '62',                    'null': '0.0'},
        'IP30-oil (bd)'                                 : {'tbl': 'tblEngineWellInputInfo',             'ref': 0,                       'null': '0.0'},
        'IP30-gas (mmcfd)'                              : {'tbl': 'tblEngineWellInputInfo',             'ref': 1,                       'null': '0.0'},
        'IP30-condensate (bd)'                          : {'tbl': 'tblEngineWellInputInfo',             'ref': 2,                       'null': '0.0'},
        'IP30-NGLs (bd)'                                : {'tbl': 'tblEngineWellInputInfo',             'ref': 3,                       'null': '0.0'},
        'Pre-Tax Break-Even Oil Price (US$/bbl)'        : {'tbl': 'tblEngineWellInputInfo',             'ref': '46',                    'null': None},
        'Pre-Tax Break-Even Gas Price (US$/mcf)'        : {'tbl': 'tblEngineWellInputInfo',             'ref': '46',                    'null': None},
        'Post-Tax Break-Even Oil Price (US$/bbl)'       : {'tbl': 'tblEngineWellInputInfo',             'ref': '66',                    'null': None},
        'Post-Tax Break-Even Gas Price (US$/mcf)'       : {'tbl': 'tblEngineWellInputInfo',             'ref': '67',                    'null': None}
    },

    'Development Inputs': {
        '[Crude Oil (bbl)]'                             : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 'type_well_crude',       'null': '0.0'},
        '[Natural Gas (mmcf)]'                          : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 'type_well_ng',          'null': '0.0'},
        '[Condensate (bbl)]'                            : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 'type_well_condensate',  'null': '0.0'},
        '[NGLs (bbl)]'                                  : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 'type_well_ngls',        'null': '0.0'},
        '[Total Operating Expenditure ($)]'             : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 'type_well_opex',        'null': '0.0'},
        '[Total Pre-tax Cash Flow ($)]'                 : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 'pre_tax_cash_flow',     'null': '0.0'},
        '[Fiscal Take ($)]'                             : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 'fiscal_take',           'null': '0.0'},
        '[Total Post-tax Cash Flow ($)]'                : {'tbl': 'tblEngineWellInputProductionInfo',   'ref': 'post_tax_cash_flow',    'null': '0.0'},

    },

    'Well Data'         : {
        '[Historical Wells Added]'                  : {'tbl': 'tblEngineWellDataInfo',              'ref': 'C',                    'null': '0.0'},
        '[Type Wells Added]'                        : {'tbl': 'tblEngineWellDataInfo',              'ref': 'D',                    'null': '0.0'},
        '[DUC Wells Added]'                         : {'tbl': 'tblEngineWellDataInfo',              'ref': 'E',                    'null': '0.0'},
        '[Historical Wells Total]'                  : {'tbl': 'tblEngineWellDataInfo',              'ref': 'F',                    'null': '0.0'},
        '[Type Wells Total]'                        : {'tbl': 'tblEngineWellDataInfo',              'ref': 'G',                    'null': '0.0'},
        '[DUC Wells Total]'                         : {'tbl': 'tblEngineWellDataInfo',              'ref': 'H',                    'null': '0.0'},
        '[Historical Crude (boe)]'                  : {'tbl': 'tblEngineWellDataInfo',              'ref': 'I',                    'null': '0.0'},
        '[Type-well Crude (boe)]'                   : {'tbl': 'tblEngineWellDataInfo',              'ref': 'J',                    'null': '0.0'},
        '[DUC Crude (boe)]'                         : {'tbl': 'tblEngineWellDataInfo',              'ref': 'K',                    'null': '0.0'},
        '[Historical Natural Gas (boe)]'            : {'tbl': 'tblEngineWellDataInfo',              'ref': 'L',                    'null': '0.0'},
        '[Type-well Natural Gas (boe)]'             : {'tbl': 'tblEngineWellDataInfo',              'ref': 'M',                    'null': '0.0'},
        '[DUC Natural Gas (boe)]'                   : {'tbl': 'tblEngineWellDataInfo',              'ref': 'N',                    'null': '0.0'},
        '[Historical Condensate (boe)]'             : {'tbl': 'tblEngineWellDataInfo',              'ref': 'O',                    'null': '0.0'},
        '[Type-well Condensate (boe)]'              : {'tbl': 'tblEngineWellDataInfo',              'ref': 'P',                    'null': '0.0'},
        '[DUC Condensate (boe)]'                    : {'tbl': 'tblEngineWellDataInfo',              'ref': 'Q',                    'null': '0.0'},
        '[Historical NGLs (boe)]'                   : {'tbl': 'tblEngineWellDataInfo',              'ref': 'R',                    'null': '0.0'},
        '[Type-well NGLs (boe)]'                    : {'tbl': 'tblEngineWellDataInfo',              'ref': 'S',                    'null': '0.0'},
        '[DUC NGLs (boe)]'                          : {'tbl': 'tblEngineWellDataInfo',              'ref': 'T',                    'null': '0.0'},
        'Rigs'                                      : {'tbl': 'tblEngineWellDataInfo',              'ref': 'B',                    'null': '0.0'}}
}

CASE_TYPES     = {1: ['Base Case', 'High Case', 'Low Case'],
                  2: ['Base Case', 'Low Case', 'High Case']}

CASE_TYPE_DICT = {'Base Case': '', 'High Case': '', 'Low Case': ''}

TABLE_PARAMS   = {table: {} for table in TABLE_COLS.keys()}

# OILGAS_DATABASE = 'OG_Effuah' #Remove post debugging and uncomment below line
OILGAS_DATABASE = 'OGEngineDataExtract'
# TEST_DATABASE   = 'OGEngineDataExtract_Effuah'
TEST_DATABASE   = 'OG_Effuah'

MINING_DATABASE = 'MiningEngineExtract'
WELLS_DATABASE  = 'US_Wells'

OILGAS_TABLE_DATA       = {'tblEngineCommodityPriceSourceData': {'schema': 'Engine'},
                                         'tblEngineDataPoints': {'schema': 'Engine'},
                                           'tblEngineFEATData': {'schema': 'Engine'},
                                      'tblEngineFEATData_Extn': {'schema': 'Engine'},
                                     'tblEngineProductionData': {'schema': 'Engine'},
                                       'tblEngineCashFlowData': {'schema': 'Engine'},
                               'tblEngineAssetSenRemainingNPV': {'schema': 'Engine'},
                                     'tblEngineAnalogueFields': {'schema': 'Engine'},
                                      'tblEngineWellInputInfo': {'schema': 'Engine'},
                                       'tblEngineWellDataInfo': {'schema': 'Engine'},
                            'tblEngineWellInputProductionInfo': {'schema': 'Engine'}}

OILGAS_TABLE_DATA_      = {'tblEngineCommodityPriceSourceData': {'schema': 'Engine'},
                                         'tblEngineDataPoints': {'schema': 'Engine'},
                                           'tblEngineFEATData': {'schema': 'Engine'},
                                      'tblEngineFEATData_Extn': {'schema': 'Engine'},
                                     'tblEngineProductionData': {'schema': 'Engine'},
                                       'tblEngineCashFlowData': {'schema': 'Engine'},
                               'tblEngineAssetSenRemainingNPV': {'schema': 'Engine'},
                                     'tblEngineAnalogueFields': {'schema': 'Engine'},
                                      'tblEngineWellInputInfo': {'schema': 'Engine'},
                                       'tblEngineWellDataInfo': {'schema': 'Engine'},
                            'tblEngineWellInputProductionInfo': {'schema': 'Engine'},
                                        'tblAutomatedPanorama': {'schema': 'dbo'}}

OILGAS_LIMIT_TABLE_DATA = {'tblEngineCommodityPriceSourceData': {'schema': 'Engine'},
                                         'tblEngineDataPoints': {'schema': 'Engine'},
                                           'tblEngineFEATData': {'schema': 'Engine'},
                                      'tblEngineFEATData_Extn': {'schema': 'Engine'},
                                     'tblEngineProductionData': {'schema': 'Engine'},
                                       'tblEngineCashFlowData': {'schema': 'Engine'},
                               'tblEngineAssetSenRemainingNPV': {'schema': 'Engine'},
                                      'tblEngineWellInputInfo': {'schema': 'Engine'},
                            'tblEngineWellInputProductionInfo': {'schema': 'Engine'}}

PRODUCTION_TABLE_DATA   = {'tblEngineProductionData': {'schema': 'Engine'},
                           'tblEngineFEATData'      : {'schema': 'Engine'}}

MINING_TABLE_DATA       = {           'Mining_Assets_Forecast': {'schema': 'dbo'},
                                    'Mining_Capacity_Forecast': {'schema': 'dbo'},
                                  'Mining_Production_Forecast': {'schema': 'dbo'},
                                    'Mining_Reserves_Forecast': {'schema': 'dbo'},
                                    'Mining_Resource_Forecast': {'schema': 'dbo'},
                                            'Mining_Error_Log': {'schema': 'dbo'}}

PANORAMA_TABLE_DATA     = {'tblAutomatedPanorama': {'schema': 'dbo'}}

DISCOVERED_TABLE_DATA   = {'tblEngineCommodityPriceSourceData': {'schema': 'Engine'},
                                         'tblEngineDataPoints': {'schema': 'Engine'},
                                           'tblEngineFEATData': {'schema': 'Engine'},
                                      'tblEngineFEATData_Extn': {'schema': 'Engine'},
                                     'tblEngineProductionData': {'schema': 'Engine'},
                                       'tblEngineCashFlowData': {'schema': 'Engine'},
                               'tblEngineAssetSenRemainingNPV': {'schema': 'Engine'},
                                     'tblEngineAnalogueFields': {'schema': 'Engine'}}

UNCON_TABLE_DATA        = {           'tblEngineWellInputInfo': {'schema': 'Engine'},
                                       'tblEngineWellDataInfo': {'schema': 'Engine'},
                            'tblEngineWellInputProductionInfo': {'schema': 'Engine'}}

US_WELLS_TABLE_DATA     = {
    1: {
        'us_ref_state'      : {'schema': 'dbo'}
    },
    2: {
        'us_ref_operator'   : {'schema': 'dbo'},
        'us_ref_formation'  : {'schema': 'dbo'},
        'us_ref_well'       : {'schema': 'dbo'},
        'us_ref_well_pad'   : {'schema': 'dbo'},
        'us_ref_well_pool'  : {'schema': 'dbo'},
        'us_ref_well_status': {'schema': 'dbo'},
        'us_ref_well_type'  : {'schema': 'dbo'}
    },
    3: {
        'us_well_details'   : {'schema': 'dbo'}
    },
    4: {
        'us_well_prod_data' : {'schema': 'dbo'}
    }
}

OILGAS_CONFIG       = (OILGAS_DATABASE, OILGAS_TABLE_DATA, OILGAS_DB_DIR)
OILGAS_LIMIT_CONFIG = (OILGAS_DATABASE, OILGAS_LIMIT_TABLE_DATA, OILGAS_DB_DIR)
OG_TEST_CONFIG      = (TEST_DATABASE, OILGAS_TABLE_DATA, OILGAS_DB_DIR)
DF_TEST_CONFIG      = (TEST_DATABASE, DISCOVERED_TABLE_DATA, DF_DATA_DIR)
MINING_CONFIG       = (MINING_DATABASE, MINING_TABLE_DATA, MINING_DB_DIR)
PANORAMA_CONFIG     = (OILGAS_DATABASE, PANORAMA_TABLE_DATA, OILGAS_DB_DIR)
DISCOVERED_CONFIG   = (OILGAS_DATABASE, DISCOVERED_TABLE_DATA, DF_DATA_DIR)
UNCON_CONFIG        = (OILGAS_DATABASE, UNCON_TABLE_DATA, UNCON_DATA_DIR)

WELLS_CONFIG        = (WELLS_DATABASE, US_WELLS_TABLE_DATA[4], OILGAS_DB_DIR)
PRODUCTION_CONFIG   = (OILGAS_DATABASE, PRODUCTION_TABLE_DATA, OILGAS_DB_DIR)
#database, schema, table, 'out', data_dir, table, DATE
#Driver={SQL Server}; Server=(local); Database=%s; Trusted_Connection=True; unicode_results=True;
EXPORT_CMD          = 'bcp %s.%s.%s %s %s%s_%s.txt -n -T'
IMPORT_CMD          = 'bcp %s.%s.%s %s %s%s_%s.txt -n -S 10.55.22.78 -U uswellsdata -P uswellsdata'
TRUNCATE_CMD        = 'sqlcmd -S 10.55.22.78 -U uswellsdata -P uswellsdata -d %s -Q "TRUNCATE TABLE %s.%s.%s"'

IMPORT_CMD_INT      = 'bcp %s.%s.%s %s %s%s_%s.txt -n -S %s -T'
TRUNCATE_CMD_INT    = 'sqlcmd -S {} -E -d %s -Q "TRUNCATE TABLE %s.%s.%s"'.format(SERVER_NAME)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE_TABLE_TEMPLATE = \
'''
CREATE TABLE %s (
id INT(11) AUTO_INCREMENT PRIMARY KEY,
%s
);
'''

CREATE_COLUMN_TEMPLATE = '%s %s DEFAULT NULL'

REPORT_TABLE_DATA = {
        'breakeven_outliers': [('asset_id','INT(11)'),
                               ('file_name', 'VARCHAR(200)'),
                               ('asset_name', 'LONGTEXT'),
                               ('country', 'VARCHAR(100)'),
                               ('constituent', 'VARCHAR(150)'),
                               ('region', 'VARCHAR(100)'),
                               ('domain', 'VARCHAR(350)'),
                               ('status', 'VARCHAR(45)'),
                               ('terrain', 'VARCHAR(100)'),
                               ('resource_type', 'VARCHAR(100)'),
                               ('reserves_outlier', 'VARCHAR(50)'),
                               ('be_rem_oil_base', 'DOUBLE'),
                               ('be_rem_gas_base', 'DOUBLE'),
                               ('be_dev_oil_base', 'DOUBLE'),
                               ('be_dev_gas_base', 'DOUBLE'),
                               ('be_rem_oil_high', 'DOUBLE'),
                               ('be_rem_gas_high', 'DOUBLE'),
                               ('be_dev_oil_high', 'DOUBLE'),
                               ('be_dev_gas_high', 'DOUBLE'),
                               ('be_rem_oil_low', 'DOUBLE'),
                               ('be_rem_gas_low', 'DOUBLE'),
                               ('be_dev_oil_low', 'DOUBLE'),
                               ('be_dev_gas_low', 'DOUBLE'),
                               ('rem_oil_outlier', 'INT(11)'),
                               ('rem_gas_outlier', 'INT(11)'),
                               ('dev_oil_outlier', 'INT(11)'),
                               ('dev_gas_outlier', 'INT(11)'),
                               ('run_id', 'VARCHAR(100)')],

         'parameter_tracker': [('asset_id','INT(11)'),
                               ('asset_name', 'LONGTEXT'),
                               ('country', 'VARCHAR(100)'),
                               ('constituent', 'VARCHAR(150)'),
                               ('region', 'VARCHAR(100)'),
                               ('domain', 'VARCHAR(350)'),
                               ('facility_type', 'VARCHAR(100)'),
                               ('terrain', 'VARCHAR(100)'),
                               ('basin', 'VARCHAR(100)'),
                               ('resource_type', 'VARCHAR(100)'),
                               ('status', 'VARCHAR(45)'),
                               ('fiscal_regime_chosen', 'VARCHAR(120)'),
                               ('run_id', 'VARCHAR(100)')],

           'eligible_assets': [('asset_id','INT(11)'),
                               ('country', 'VARCHAR(100)'),
                               ('constituent', 'VARCHAR(150)'),
                               ('region', 'VARCHAR(100)'),
                               ('domain', 'VARCHAR(350)'),
                               ('terrain', 'VARCHAR(100)'),
                               ('status', 'VARCHAR(45)'),
                               ('asset_relation', 'VARCHAR(100)'),
                               ('data_source', 'VARCHAR(45)'),
                               ('run_id', 'VARCHAR(100)')],

          'engine_error_log': [('asset_id','INT(11)'),
                               ('asset_name', 'LONGTEXT'),
                               ('country', 'VARCHAR(100)'),
                               ('constituent', 'VARCHAR(150)'),
                               ('region', 'VARCHAR(100)'),
                               ('domain', 'VARCHAR(350)'),
                               ('status', 'VARCHAR(45)'),
                               ('terrain', 'VARCHAR(100)'),
                               ('flag_number', 'VARCHAR(50)'),
                               ('flag', 'VARCHAR(255)'),
                               ('irr', 'DOUBLE'),
                               ('total_boe', 'DOUBLE'),
                               ('capex_boe', 'DOUBLE'),
                               ('opex_boe', 'DOUBLE'),
                               ('run_id', 'VARCHAR(100)')],

     'assumption_complexity': [('asset_id','INT(11)'),
                               ('status', 'VARCHAR(45)'),
                               ('country', 'VARCHAR(100)'),
                               ('constituent', 'VARCHAR(150)'),
                               ('region', 'VARCHAR(100)'),
                               ('domain', 'VARCHAR(350)'),
                               ('terrain', 'VARCHAR(100)'),
                               ('param_name', 'VARCHAR(100)'),
                               ('complexity_score', 'DOUBLE'),
                               ('run_id', 'VARCHAR(100)')],

    'implied_price_outliers': [('asset_id','INT(11)'),
                               ('asset_name', 'LONGTEXT'),
                               ('country', 'VARCHAR(100)'),
                               ('constituent', 'VARCHAR(150)'),
                               ('region', 'VARCHAR(100)'),
                               ('domain', 'VARCHAR(350)'),
                               ('status', 'VARCHAR(45)'),
                               ('terrain', 'VARCHAR(100)'),
                               ('implied_oil_outlier', 'INT(11)'),
                               ('implied_gas_outlier', 'INT(11)'),
                               ('value_diff_outlier', 'INT(11)'),
                               ('run_id', 'VARCHAR(100)')]
    }

QUALITY_TABLE_DATA = {
    'kpi_quality': [('domain', 'VARCHAR(350)'),
                    ('region', 'VARCHAR(100)'),
                    ('analyst', 'VARCHAR(100)'),
                    ('eligible_assets', 'INT(11)'),
                    ('modelled_assets', 'INT(11)'),
                    ('complexity_total', 'DOUBLE'),
                    ('complexity_score', 'DOUBLE'),
                    ('data_quality', 'INT(11)'),
                    ('data_quality_score', 'DOUBLE'),
                    ('econ_quality', 'INT(11)'),
                    ('econ_quality_score', 'DOUBLE'),
                    ('dev_be_outliers', 'INT(11)'),
                    ('dev_be_score', 'DOUBLE'),
                    ('rem_be_outliers', 'INT(11)'),
                    ('rem_be_score', 'DOUBLE'),
                    ('implied_price_outliers', 'INT(11)'),
                    ('value_diff_outliers', 'INT(11)'),
                    ('run_id', 'VARCHAR(100)')]
                    }

REPORT_DATA = [
    {'report_file': 'Breakeven Review %s.xlsx',
       'worksheet': 'BE OUTLIER LIST',
        'col_data': [('asset_id','A'),
                     ('file_name', 'B'),
                     ('asset_name', 'C'),
                     ('country', 'D'),
                     ('constituent', 'E'),
                     ('region', 'F'),
                     ('status', 'G'),
                     ('terrain', 'H'),
                     ('resource_type', 'I'),
                     ('reserves_outlier', 'J'),
                     ('be_rem_oil_base', 'K'),
                     ('be_rem_gas_base', 'L'),
                     ('be_dev_oil_base', 'M'),
                     ('be_dev_gas_base', 'N'),
                     ('be_rem_oil_high', 'O'),
                     ('be_rem_gas_high', 'P'),
                     ('be_dev_oil_high', 'Q'),
                     ('be_dev_gas_high', 'R'),
                     ('be_rem_oil_low', 'S'),
                     ('be_rem_gas_low', 'T'),
                     ('be_dev_oil_low', 'U'),
                     ('be_dev_gas_low', 'V'),
                     ('rem_oil_outlier', 'W'),
                     ('rem_gas_outlier', 'X'),
                     ('dev_oil_outlier', 'Y'),
                     ('dev_gas_outlier', 'Z')],
       'row_start': 2,
      'table_name': 'breakeven_outliers'},

    {'report_file': 'Engine Parameter Tracker %s.xlsx',
       'worksheet': 'Sheet',
        'col_data': [('asset_id','A'),
                     ('asset_name', 'B'),
                     ('country', 'C'),
                     ('constituent', 'D'),
                     ('region', 'E'),
                     ('facility_type', 'F'),
                     ('terrain', 'G'),
                     ('basin', 'H'),
                     ('resource_type', 'I'),
                     ('status', 'J'),
                     ('fiscal_regime_chosen', 'K')],
       'row_start': 2,
      'table_name': 'parameter_tracker'},

    {'report_file': 'Global Run Error Log %s.xlsx',
       'worksheet': 'Error Log',
        'col_data': [('asset_id','A'),
                     ('asset_name', 'B'),
                     ('country', 'C'),
                     ('constituent', 'D'),
                     ('region', 'E'),
                     ('status', 'F'),
                     ('flag_number', 'G'),
                     ('flag', 'H')],
       'row_start': 4,
      'table_name': 'engine_error_log'},

    {'report_file': 'Economics Global Run Error Log %s.xlsx',
       'worksheet': 'Economics Error Log',
        'col_data': [('asset_id','A'),
                     ('asset_name', 'B'),
                     ('country', 'C'),
                     ('constituent', 'D'),
                     ('region', 'E'),
                     ('status', 'F'),
                     ('flag_number', 'G'),
                     ('flag', 'H'),
                     ('irr', 'I'),
                     ('total_boe', 'J'),
                     ('capex_boe', 'K'),
                     ('opex_boe', 'L')],
       'row_start': 4,
      'table_name': 'engine_error_log'},

    {'report_file': 'Complexity Score Report %s.xlsm',
       'worksheet': 'Assumptions - model rules',
        'col_data': [('asset_id','A'),
                     ('status', 'B'),
                     ('country', 'C'),
                     ('constituent', 'D'),
                     ('region', 'E'),
                     ('terrain', 'H'),
                     ('param_name', 'O'),
                     ('complexity_score', 'W')],
       'row_start': 2,
      'table_name': 'assumption_complexity'},

    {'report_file': 'Complexity Score Report %s.xlsm',
       'worksheet': 'Allocation Tables',
        'col_data': [('asset_id','A'),
                     ('status', 'B'),
                     ('country', 'C'),
                     ('constituent', 'D'),
                     ('region', 'E'),
                     ('terrain', 'H'),
                     ('param_name', 'L'),
                     ('complexity_score', 'AA')],
       'row_start': 2,
      'table_name': 'assumption_complexity'}
    ]

dev_be_outliers_sql = 'SELECT COUNT(DISTINCT asset_id) FROM breakeven_outliers WHERE (dev_gas_outlier=1 OR dev_oil_outlier=1) AND domain="%s" AND run_id="%s" '

rem_be_outliers_sql = 'SELECT COUNT(DISTINCT asset_id) FROM breakeven_outliers WHERE (rem_gas_outlier=1 OR rem_oil_outlier=1) AND domain="%s" AND run_id="%s" '

data_quality_sql    = 'SELECT COUNT(DISTINCT asset_id) FROM engine_error_log WHERE NOT flag_number IN ("ERROR TYPE 14", "ERROR TYPE 15", "ERROR TYPE 16") AND domain="%s" AND run_id="%s" '

econ_quality_sql    = 'SELECT COUNT(DISTINCT asset_id) FROM engine_error_log WHERE flag_number IN ("ERROR TYPE 14", "ERROR TYPE 15", "ERROR TYPE 16") AND domain="%s" AND run_id="%s" '

modelled_assets_sql = 'SELECT COUNT(DISTINCT asset_id) FROM parameter_tracker WHERE status IN ("Announced", "Planned", "Producing") AND NOT fiscal_regime_chosen IS NULL AND domain="%s" AND run_id="%s" '

eligible_assets_sql = 'SELECT COUNT(DISTINCT asset_id) FROM eligible_assets WHERE domain="%s" AND run_id="%s" '

assumption_comp_sql = 'SELECT SUM(a.avg_score) FROM (SELECT AVG(complexity_score) AS avg_score FROM assumption_complexity WHERE domain="%s" AND run_id="%s" GROUP BY param_name) AS a '

implied_price_sql   = 'SELECT COUNT(DISTINCT asset_id) FROM implied_price_outliers WHERE (implied_oil_outlier=1 OR implied_gas_outlier=1) AND domain="%s" AND run_id="%s" '

value_diff_sql      = 'SELECT COUNT(DISTINCT asset_id) FROM implied_price_outliers WHERE value_diff_outlier=1 AND domain="%s" AND run_id="%s" '

KPI_TOTAL_SQL = {       'eligible_assets': {'sql': eligible_assets_sql},
                        'modelled_assets': {'sql': modelled_assets_sql},
                       'complexity_total': {'sql': assumption_comp_sql},
                           'data_quality': {'sql': data_quality_sql},
                           'econ_quality': {'sql': econ_quality_sql},
                        'dev_be_outliers': {'sql': dev_be_outliers_sql},
                        'rem_be_outliers': {'sql': rem_be_outliers_sql},
                 'implied_price_outliers': {'sql': implied_price_sql},
                    'value_diff_outliers': {'sql': value_diff_sql}}

comp_score_sql   = 'UPDATE kpi_quality SET complexity_score=(complexity_total/(5*16)) WHERE NOT complexity_total IS NULL AND run_id="%s" '
data_score_sql   = 'UPDATE kpi_quality SET data_quality_score=(1-(data_quality/eligible_assets)) WHERE data_quality > 0 AND run_id="%s" '
econ_score_sql   = 'UPDATE kpi_quality SET econ_quality_score=(1-(econ_quality/eligible_assets)) WHERE econ_quality > 0 AND run_id="%s" '
dev_be_score_sql = 'UPDATE kpi_quality SET dev_be_score=(1-(dev_be_outliers/eligible_assets)) WHERE dev_be_outliers > 0 AND run_id="%s" '
rem_be_score_sql = 'UPDATE kpi_quality SET rem_be_score=(1-(rem_be_outliers/eligible_assets)) WHERE rem_be_outliers > 0 AND run_id="%s" '


KPI_SCORE_SQL = {  'complexity_score': {'sql': comp_score_sql},
                 'data_quality_score': {'sql': data_score_sql},
                 'econ_quality_score': {'sql': econ_score_sql},
                       'dev_be_score': {'sql': dev_be_score_sql},
                       'rem_be_score': {'sql': rem_be_score_sql}}

