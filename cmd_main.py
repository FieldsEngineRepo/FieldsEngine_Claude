# import win32com.client
from Tkinter import *
from tqdm import tqdm
from globaldata import *
from param_detail import splitFiscalModels
from standard_menu_titan_V25 import NewMenuDemo
import warnings
import datetime
warnings.filterwarnings('ignore')
# Silence the specific cryptography deprecation warning
warnings.filterwarnings("ignore", category=UserWarning, module="cryptography")

try:
    #
    import data_export as de
except:
    #
    pass

try:
    #
    from automated_panorama import generate_rank_sections
except:
    #
    pass

try:
    from discovered_analogues import calc_field_analogues
    from discovered_analogues import get_discovered_fields
except:
    #
    pass

try:
    #
    from analyst_kpi import main as kpi_main
except:
    #
    pass

try:
    #
    from update_asset_data import update_asset_data_tbl
except:
    #
    pass

try:
    #
    from process_deals import process_deals_assets
except:
    #
    pass

try:
    #
    from process_detailed_models import main as detailed_models_main
except:
    #
    pass

try:
    #
    from calc_breakevens import *
except:
    #
    pass
from extract_econ_data import extract_data as extract_econ
try:
    #
    from extract_econ_data import extract_data as extract_econ
except:
    #
    pass

try:
    #
    from analytics_param_report import main as analytics_report
except:
    #
    pass

try:
    #
    from process_mining import *
except:
    #
    pass

try:
    #
    from add_exceptions import main as add_exceptions_main
except:
    #
    pass

try:
    #
    from process_econ_limits import econ_limit_main
except:
    #
    pass

try:
    #
    from csv_sql_import import main as import_csv_main
except:
    try:
        from well_data import main as import_csv_main
    except:
        #
        print 'csv_sql_import not found'
        pass

try:
    #
    from update_key_asset_data import key_assets_main
except:
    #
    pass

try:
    #
    from extract_supply_curve_data import extract_production_data
except:
    #
    pass

try:
    #
    from well_forecast import main as well_forecast_main
except:
    #
    pass

try:
    #
    from extract_supply_curve_data import main as extract_supply_data_main
except:
    #
    pass

try:
    #
    from well_data_engine import main as well_data_main
except:
    #
    pass

try:
    #
    from update_tx_well_data import main as tx_main
except:
    #
    pass

try:
    #
    from update_tx_well_data import tx_oil_allocation_update as tx_oil_allocate
except:
    #
    pass

try:
    #
    from undiscovered_resources import calc_undiscovered_reserves as calc_undisc_data
except:
    #
    pass

try:
    #
    from server_import import server_data_import
except:
    #
    pass


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def commandLineMain(argumentList, command, curr):
    if command.upper() == 'DATA_IMPORT':
        print 'import'
        dataImport(curr)
        sys.exit(0)
    
    elif command.upper() in ['PARAM_IMPORT', 'PARAM_EXPORT']:
        paramImportExport(curr)
        sys.exit(0)

    elif command.upper() == 'LOG':
        if argumentList[1][1] == 'e':
            updateLog(curr, argumentList[1][1], argumentList[2])
        else:
            updateLog(curr, argumentList[1][1], argumentList[2], argumentList[3])
        sys.exit(0)

    elif command.upper() == 'TEMP_LOG':
        if argumentList[1] == 'create_model':
            if COMPUTER == 'TITAN III':
                temp_log(curr, 'CreateModel', CHECK_T3_MODEL_SET, '4_CreateModelComplete', True)
            else:
                temp_log(curr, 'CreateModel', CHECK_MODEL_SET, '4_CreateModelComplete', True)
        elif argumentList[1] == 'econ_error':
            temp_log(curr, 'EconError', CHECK_ECON_ERROR_SET, '7b_EconErrorDataComplete')
        elif argumentList[1] == 'create_model_test':
            temp_log(curr, 'CreateModel', CHECK_TEST_SET, 'CreateModelTestComplete')
        sys.exit(0)

    elif command.upper() == 'CREATE_MODEL':
        createModel()
        #sys.exit(0)

    elif command.upper() == 'CHECK_BREAKEVEN':
        brkeven_outfile = BREAKEVEN_DIR + 'Breakeven_' + argumentList[2]
        check_process(curr=curr,
              region_name=argumentList[1],
              region_code=argumentList[2],
              process_name='Breakeven',
              outfile_name=brkeven_outfile,
              file_ext='.xlsm',
              task_dir=BE_TASK_DIR,
              check_set=CHECK_REGION_SET,
              complete_task='6_BreakevenComplete',
              engine_model_dir=REGIONS_DIR,
              macro_model_dir=BE_REGIONS)
        sys.exit(0)

    elif command.upper() == 'CHECK_DEALS_PROCESS':
        check_deals_process(curr)
        sys.exit(0)

    elif command.upper() == 'MACRO':
        print 'argumentList:', argumentList
        run_macro(argumentList[1],argumentList[2],argumentList[3])
        sys.exit(0)

    elif command.upper() == 'REPORT':
        report_macro()
        sys.exit(0)
        
    elif command.upper() == 'BREAKEVEN':
        breakeven_macro()
        sys.exit(0)

    elif command.upper() == 'CHECK_IMPORT':
        check_all_import_data(curr)
        sys.exit(0)

    elif command.upper() == 'COPY_MODELS':
        try:
            copy_models(argumentList[1], argumentList[2])
        except:
            copy_models(argumentList[1])
        sys.exit(0)

    elif command.upper() == 'ASSET_TEST':
        asset_test()
        run_macro(TEST_DIR, "find_changes.xlsm", "Module1.FindChanges")
        sys.exit(0)

    elif command.upper() == 'DATE_CONVERT':
        old_date = argumentList[1]
        new_date = argumentList[2]
        convert_dates(old_date, new_date)
        sys.exit(0)

    elif command.upper() == 'CHANGE_DRIVE':
        try:
            change_drive(argumentList[1], argumentList[2])
        except:
            change_drive(argumentList[1])
        sys.exit(0)

    elif command.upper() == 'CLEAR_REGION_FOLDERS':
        clear_region_folders()
        sys.exit(0)

    elif command.upper() == 'ENGINE_RUN_PREP':
        clear_region_folders()
        clear_temp_folder()
        archive_files()
        sys.exit(0)

    elif command.upper() == 'PROCESS_DEALS':
        import_deals  = True #After Debug change it to True
        create_models = True #After Debug change it to True
        calc_prices   = False
        export_deals  = False
        report        = True
        external      = False
        process_deals_assets(import_deals_data=import_deals, create_models=create_models, calc_implied_prices=calc_prices, export_deals_data=export_deals, generate_report=report, external=external)
        # updateLog(curr, 'e', 'ImpliedPrices')
        run_task('13_EndRun', ENGN_TASK_DIR + '13_EndRun.bat')
        sys.exit(0)

    elif command.upper() == 'SPLIT_FISCAL':
        update      = True
        split_NA    = False
        split_EU    = False
        split_FS    = False
        split_SA    = False
        disc_fields = False
        T3 = False

        if COMPUTER == 'TITAN III':
            T3 = True

        if argumentList[1] == 'update_db':
            update = True
        if 'NA' in argumentList[2]:
            split_NA = True
        if 'EU' in argumentList[2]:
            split_EU = True
        if 'FS' in argumentList[2]:
            split_FS = True
        if 'SA' in argumentList[2]:
            split_SA = True
        if 'DF' in argumentList[2]:
            disc_fields = True

        splitFiscalModels(update_database=update, split_NA=split_NA, split_EU=split_EU, split_FS=split_FS, split_SA=split_SA, T3=T3, disc_fields=disc_fields)
        sys.exit(0)

    elif command.upper() == 'UPDATE_ECON_DATA':
        operators  = False
        asset_data = False
        xl_macro   = False
        benchmarks = False
        uncon_data = False
        regions    = None
        update_choices = [choice for choice in argumentList[1][1:6]]
        if 'o' in update_choices:
            operators = True
        if 'a' in update_choices:
            asset_data = True
        if 'x' in update_choices:
            xl_macro = True
        if 'b' in update_choices:
            benchmarks = True
        if 'u' in update_choices:
            uncon_data = True
        if '*' in update_choices:
            regn_indx = argumentList[1].index('*')
            regions = [argumentList[1][regn_indx+1:]]
        update_econ_data(curr, operators, asset_data, xl_macro, benchmarks, uncon_data, regions)
        sys.exit(0)

    elif command.upper() == 'BE_CONFIG':
        if argumentList[1] == 'full_be':
            setting = 'full be'
        elif argumentList[1] == 'base_be':
            setting = 'base be'
        elif argumentList[1] == 'engine':
            setting = 'engine'
        elif argumentList[1] == 'econ_report':
            setting = 'econ report'
        elif argumentList[1] == 'full_econ':
            setting = 'full econ'
        elif argumentList[1] == 'uncon':
            setting = 'uncon'
        elif argumentList[1] == 'disc_fields':
            setting = 'disc fields'
        breakeven_config(setting)
        sys.exit(0)

    elif command.upper() == 'DISC_FIELDS':
        if argumentList[1] == 'model':
            setting = 'full be'

    elif command.upper() in ['DATA_EXTRACT', 'DATA_EXPORT']:
        regions      = []
        region_dir   = BE_REGIONS #uncomment it after debug
        # region_dir = REGIONS_DIR #Comment it after Debug
        discovered   = False
        undiscovered = False
        clear        = False
        external     = False
        ext_override = True
        tables       = EXT_TABLES

        # regns-AF,AS,CR,CA,EU,FS,ME,NA,N1,N2,OC,SA,UN
        regns = argumentList[1].split('-')[1].split(',')

        if 'AF' in regns:
            regions.append('Africa')
        if 'AS' in regns:
            regions.append('Asia')
        if 'CR' in regns:
            regions.append('Caribbean')
        if 'CA' in regns:
            regions.append('Central America')
        if 'EU' in regns:
            regions.append('Europe')
        if 'E1' in regns:
            regions.append('Europe_1')
        if 'E2' in regns:
            regions.append('Europe_2')
        if 'E3' in regns:
            regions.append('Europe_3')
        if 'FS' in regns:
            regions.append('Former Soviet Union')
        if 'F1' in regns:
            regions.append('Former_Soviet_Union_1')
        if 'F2' in regns:
            regions.append('Former_Soviet_Union_2')
        if 'F3' in regns:
            regions.append('Former_Soviet_Union_3')
        if 'F4' in regns:
            regions.append('Former_Soviet_Union_4')
        if 'ME' in regns:
            regions.append('Middle East')
        if 'NA' in regns:
            regions.append('North America')
        if 'N1' in regns:
            regions.append('North_America_1')
        if 'N2' in regns:
            regions.append('North_America_2')
        if 'N3' in regns:
            regions.append('North_America_3')
        if 'N4' in regns:
            regions.append('North_America_4')
        if 'N5' in regns:
            regions.append('North_America_5')
        if 'N6' in regns:
            regions.append('North_America_6')
        if 'OC' in regns:
            regions.append('Oceania')
        if 'SA' in regns:
            regions.append('South America')
        if 'S1' in regns:
            regions.append('South_America_1')
        if 'S2' in regns:
            regions.append('South_America_2')
        if 'S3' in regns:
            regions.append('South_America_3')
        if 'UN' in regns:
            regions.append('Unconventional')
        if 'U1' in regns:
            regions.append('Unconventional_1')
        if 'U2' in regns:
            regions.append('Unconventional_2')
        if 'U3' in regns:
            regions.append('Unconventional_3')
        if 'U4' in regns:
            regions.append('Unconventional_4')
        if 'U5' in regns:
            regions.append('Unconventional_5')
        if 'U6' in regns:
            regions.append('Unconventional_6')

        print argumentList[2]

        if 'p' in argumentList[2]:
            tables = ['tblEngineProductionData', 'tblEngineCashFlowData']
        if 'c' in argumentList[2]:
            clear = True
        if 'e' in argumentList[2]:
            external = True
        if 'd' in argumentList[2]:
            # region_dir = DF_REGIONS
            region_dir = "E:\\GlobalData\\Macros\\BreakevenMacros\\Regions\\Discovered\\"
            discovered = True
        if 'u' in argumentList[2]:
            undiscovered = True
            print 'Extracting data from only undiscovered models ...'
        if ext_override:
            external = False
        is_test_data = get_param(param='export_to_test_db', table='global_variables', data_type='bool')
        # de.data_export(tables=tables, regions=regions, region_dir=region_dir, discovered=discovered, undiscovered=undiscovered, clear=clear, ext=external, test_data=is_test_data, debug=False)
        de.data_export(tables=tables, regions=regions, region_dir=region_dir, discovered=discovered, clear=clear, ext=external, test_data=is_test_data, debug=False)
        sys.exit(0)

    elif command.upper() == 'SCENARIO_EXTRACT':
        scenario_num = argumentList[1].split(':')[0]
        region_num   = argumentList[1].split(':')[1]
        scenario_regions = ['scenario_{}\\region_{}'.format(scenario_num, region_num)]
        is_test_data = get_param(param='export_to_test_db', table='global_variables', data_type='bool')
        de.data_export(regions=scenario_regions, region_dir=SCENARIO_DIR, clear=True, test_data=is_test_data)

    elif command.upper() in ['CHECK_EXPORT', 'CHECK_EXTRACT']:
        extract_complete = de.check_process('extract')
        if extract_complete:
            updateLog(curr, 'e', 'DataExtract')
            #send_update_email(send_to=['jason.skophammer@gmail.com'], message='DataExtract Process complete')
            export_engine_data = get_data(param='export_engine_data', table='global_variables', datatype='int', sql_where='id=1')[0]
            if export_engine_data:
                clear_engine_data = get_data(param='clear_engine_data', table='global_variables', datatype='int', sql_where='id=1')[0]
                if clear_engine_data:
                    run_task('11_EngineExportClearData', ENGN_TASK_DIR + '11_EngineExportClearData.bat')
                else:
                    run_task('11_EngineExportKeepData', ENGN_TASK_DIR + '11_EngineExportKeepData.bat')
        sys.exit(0)
        
    elif command.upper() == 'CHECK_UNDISC_MODEL':
        process_complete = de.check_process('UnDiscFieldModel')
        if process_complete:
            updateLog(curr, 'e', 'UnDiscFieldModel')
            calc_undisc_data(step_9=True)
        sys.exit(0)

    elif command.upper() == 'CHECK_SUPPLY_MACRO':
        process_complete = False
        process_name = 'SupplyCurveMacro_' + argumentList[1]
        updateLog(curr, 'e', process_name)
        process_complete = de.check_process('SupplyCurveMacro')
        if process_complete:
            updateLog(curr, 'e', 'SupplyCurveMacro')
            os.system('%engine_drive%:\\GlobalData\\Tasks\\EngineTasks\\UpdateAllEconUndisc')
        
        sys.exit(0)

    elif command.upper() == 'CHECK_UNDISC_ECON_DATA':
        region = argumentList[1]
        process_name = 'UndiscEconData_%s' % region
        updateLog(curr, 'e', process_name)
        process_complete = de.check_process('undisc_econ_data')
        if process_complete:
            updateLog(curr, 'e', 'UndiscEconData')
            os.system('%engine_drive%:\\GlobalData\\Tasks\\EngineTasks\\ExtractAllUndisc')
        sys.exit(0)

    elif command.upper() == 'CHECK_UNDISC_EXTRACT':
        extract_complete = de.check_process('undisc_extract')
        if extract_complete:
            updateLog(curr, 'e', 'DataExtractUndisc')
            os.system('%engine_drive%:\\GlobalData\\Tasks\\EngineTasks\\Process_Supply_Curve_Data')
        sys.exit(0)
        
    elif command.upper() == 'CHECK_ECON_DATA':
        region = argumentList[1]
        process_name = 'EconData_%s' % region
        updateLog(curr, 'e', process_name)
        process_complete = de.check_process('econ_data')
        # if process_complete:
        #     updateLog(curr, 'e', 'EconData')
        #     send_update_email(send_to=['sunil.lanke@globaldata.com'], message='EconData Process complete')
        #     run_task('8_GenerateReports', ENGN_TASK_DIR + '8_GenerateReports.bat')
        sys.exit(0)

    elif command.upper() == 'GENERATE_PANORAMAS':
        regions = []
        clear_tbl = False

        regns = argumentList[1].split('-')[1].split(',')
        args  = argumentList[2].split('-')[1].split(',')

        if 'AF' in regns:
            regions.append('Africa')
        if 'AS' in regns:
            regions.append('Asia')
        if 'CR' in regns:
            regions.append('Caribbean')
        if 'CA' in regns:
            regions.append('Central America')
        if 'EU' in regns:
            regions.append('Europe')
        if 'FS' in regns:
            regions.append('Former Soviet Union')
        if 'ME' in regns:
            regions.append('Middle East')
        if 'NA' in regns:
            regions.append('North America')
        if 'OC' in regns:
            regions.append('Oceania')
        if 'SA' in regns:
            regions.append('South America')

        if 'clear_tbl' in args:
            clear_tbl = True #Change to True after Debug
            generate_rank_sections(server='sql_server', run_id='99999999_999999', asset_list=['000000'], clear_tbl=clear_tbl)

        for region in regions:
            generate_rank_sections(server='sql_server', run_region=region, export=False)

        sys.exit(0)

    elif command.upper() == 'GENERATE_ALL_PANORAMAS':
        run_id = get_run_id()
        sql_where = 'run_id="{}" AND NOT `status` IN ("Discovered", "Stalled", "Suspended") AND total_boe IS NOT NULL AND NOT asset_name IS NULL AND NOT operator IS NULL AND NOT parent_company IS NULL AND NOT (asset_name LIKE "Other %" OR asset_name LIKE "Others %") '.format(run_id)

        assets = get_assets(table='econ_data', sql_where=sql_where)
        assets = sorted(list(set(assets)))
        for asset in assets:
            print asset
        print "{} assets selected for Panorama generation ...".format(len(assets))
        generate_rank_sections(server='sql_server', asset_list=assets, run_id=run_id, clear_tbl=True, export=False) #After debug set clear_tbl to "True"
        # updateLog(curr, 'e', 'AutomatedPanorama')
        # updateLog(curr, 's', 'Panorama_Export', 'Automated Panorama Export Process')
        # is_test_data = get_param(param='export_to_test_db', table='global_variables', data_type='bool')
        # de.update_servers(dataset='panorama', export_tables=True, import_tables=True, test_data=is_test_data)
        # updateLog(curr, 'e', 'Panorama_Export')
        #send_update_email(send_to=['jason.skophammer@gmail.com'], message='AutomatedPanorama Process complete')
        # run_task('10_ExtractAllData', ENGN_TASK_DIR + '10_ExtractAllData.bat') #Uncomment after debug
        sys.exit(0)

    elif command.upper() == 'GENERATE_TEST_PANORAMAS':
        run_id = get_run_id()
        sql_where = 'run_id="{}" AND NOT `status` IN ("Discovered", "Stalled", "Suspended") AND total_boe IS NOT NULL AND NOT asset_name IS NULL AND NOT operator IS NULL AND NOT parent_company IS NULL AND NOT (asset_name LIKE "Other %" OR asset_name LIKE "Others %") '.format(run_id)
        assets = get_assets(table='econ_data', sql_where=sql_where)
        assets = sorted(list(set(assets)))
        for asset in assets:
            print asset
        generate_rank_sections(server='sql_server', asset_list=assets, run_id=run_id, clear_tbl=True, export=False)

        conn = get_connection(server='sql_server', database='OGEngineDataExtract')
        # conn = get_connection(server='sql_server', database='OG_Effuah') #Changed to original DB after testing
        curr_1 = conn.cursor()
        sql_update = \
        """
        UPDATE [OGEngineDataExtract].[dbo].[tblAutomatedPanorama] 
          SET ProjectOutlook=SUBSTRING(ProjectOutlook,2,LEN(ProjectOutlook)-1) WHERE SUBSTRING(ProjectOutlook,1,1)='
        ';
        """
        curr_1.execute(sql_update)
        commit(curr_1)
        curr_1.close()
        conn.close()

        sys.exit(0)

    elif command.upper() == 'PROCESS_DISC_FIELDS':
        #clear_data=False, field_id=None, field_list=None, calc_scores=False, enter_prod=False, conf_score=False, in_place=False, debug=False
        regions     = []
        field_list  = []

        clear_data = False
        calc_scores = False
        enter_prod = False
        conf_score = False
        calc_conf = False
        curve_score = False
        gen_lists = False
        with_analog = True
        use_regions = True
        with_reserves = False

        # 20200909 change to false after disc field run
        not_modelled = False

        # regns-AF,AS,CR,CA,EU,FS,ME,NA,OC,SA -clear,calc,prod,conf
        regns = argumentList[1].split('-')[1].split(',')
        args = argumentList[2].split('-')[1].split(',')

        if 'AF' in regns:
            regions.append('Africa')
        if 'AS' in regns:
            regions.append('Asia')
        if 'CR' in regns:
            regions.append('Caribbean')
        if 'CA' in regns:
            regions.append('Central America')
        if 'EU' in regns:
            regions.append('Europe')
        if 'FS' in regns:
            regions.append('Former Soviet Union')
        if 'ME' in regns:
            regions.append('Middle East')
        if 'NA' in regns:
            regions.append('North America')
        if 'OC' in regns:
            regions.append('Oceania')
        if 'SA' in regns:
            regions.append('South America')

        if 'no_analog' in args:
            with_analog = False
        if 'clear' in args:
            clear_data  = True
        if 'calc' in args:
            calc_scores = True
        if 'prod' in args:
            enter_prod  = True
            with_reserves = True
        if 'conf1' in args:
            conf_score  = True
            calc_conf   = True
            with_reserves = True
        if 'conf2' in args:
            conf_score  = True
            curve_score = True
            with_reserves = True
        if 'gen_lists' in args:
            gen_lists = True
            with_reserves = True

        disc_field_count = len(get_discovered_fields(with_analogues=with_analog, not_modelled=not_modelled, with_reserves=with_reserves))
        disc_field_group = int(disc_field_count / 16)
        field_start = ''
        field_end = ''

        if 'R1' in regns:
            use_regions = False
            field_start = 0*disc_field_group
            field_end = 1*disc_field_group
        elif 'R2' in regns:
            use_regions = False
            field_start = 1*disc_field_group
            field_end = 2*disc_field_group
        elif 'R3' in regns:
            use_regions = False
            field_start = 2*disc_field_group
            field_end = 3*disc_field_group
        elif 'R4' in regns:
            use_regions = False
            field_start = 3*disc_field_group
            field_end = 4*disc_field_group
        elif 'R5' in regns:
            use_regions = False
            field_start = 4*disc_field_group
            field_end = 5*disc_field_group
        elif 'R6' in regns:
            use_regions = False
            field_start = 5*disc_field_group
            field_end = 6*disc_field_group
        elif 'R7' in regns:
            use_regions = False
            field_start = 6*disc_field_group
            field_end = 7*disc_field_group
        elif 'R8' in regns:
            use_regions = False
            field_start = 7*disc_field_group
            field_end = 8*disc_field_group
        elif 'R9' in regns:
            use_regions = False
            field_start = 8*disc_field_group
            field_end = 9*disc_field_group
        elif 'R10' in regns:
            use_regions = False
            field_start = 9*disc_field_group
            field_end = 10*disc_field_group
        elif 'R11' in regns:
            use_regions = False
            field_start = 10*disc_field_group
            field_end = 11*disc_field_group
        elif 'R12' in regns:
            use_regions = False
            field_start = 11*disc_field_group
            field_end = 12*disc_field_group
        elif 'R13' in regns:
            use_regions = False
            field_start = 12*disc_field_group
            field_end = 13*disc_field_group
        elif 'R14' in regns:
            use_regions = False
            field_start = 13*disc_field_group
            field_end = 14*disc_field_group
        elif 'R15' in regns:
            use_regions = False
            field_start = 14*disc_field_group
            field_end = 15*disc_field_group
        elif 'R16' in regns:
            use_regions = False
            field_start = 15*disc_field_group
            field_end = None

        if use_regions:
            for region in regions:
                disc_fields = get_discovered_fields(with_analogues=with_analog, not_modelled=not_modelled,
                                                    region=region, with_reserves=with_reserves)
                field_list += disc_fields
            field_list = sorted(list(set(field_list)))
        else:
            field_list = get_discovered_fields(with_analogues=with_analog, not_modelled=not_modelled, with_reserves=with_reserves)[
                         field_start:field_end]

        print 'Processing %s dicovered fields ...' % len(field_list)

        calc_field_analogues(field_list=field_list,
                             clear_data=clear_data,
                             calc_scores=calc_scores,
                             enter_prod=enter_prod,
                             conf_score=conf_score,
                             calc_conf=calc_conf,
                             curve_score=curve_score,
                             gen_lists=gen_lists)
        sys.exit(0)

    elif command.upper() == 'CLEAR_DISC_FIELD_PROD':
        curr.execute('SET sql_safe_updates=0')
        curr.execute('DELETE FROM production WHERE add_by="Analogue"')
        curr.execute('COMMIT')

    elif command.upper() == 'CHECK_DISC_FIELDS':
        stages = ['Calc', 'Prod', 'Conf1', 'Conf2', 'Model', 'Macro1', 'Macro2', 'Macro3', 'Econ', 'Extract', 'Export']
        process_stage = argumentList[1].split('-')[1]
        stage_num = stages.index(process_stage) + 1
        process_name = 'DiscField' + process_stage
        if 'Macro' in process_stage:
            region_code = argumentList[2].split('-')[1]
            region_name = REGIONS[region_code]
            disc_field_outfile = DISC_FIELD_DIR + 'DiscField_' + region_code
            df_macro_task_dir = DF_MACROS_DIR  + process_name + '\\'
            process_complete = check_process(curr=curr,
                                             region_name=region_name,
                                             region_code=region_code,
                                             process_name=process_name,
                                             outfile_name=disc_field_outfile,
                                             file_ext='.xlsm',
                                             task_dir=df_macro_task_dir,
                                             engine_model_dir=DF_REGION_DIR,
                                             macro_model_dir=DF_REGIONS)
            # pass
        elif 'Econ' in process_stage:
            pass
        else:
            process_complete = de.check_process(process_name)
        if 'Macro' in process_stage:
            pass
        else:
            next_process_task = DF_TASKS + str(stage_num + 1) + '_RunDiscField' + stages[stage_num] + '.bat'
        if process_complete:
            # updateLog(curr, 'e', process_name)
            if process_stage == 'Model':
                copy_models(DF_REGIONS, model_dir=DF_REGION_DIR)
            if process_stage == 'Econ':
                sql_update = \
                    '''
					UPDATE econ_data AS a,
                    (SELECT DISTINCT asset_id, MAX(run_id) AS max_run_id FROM econ_data WHERE total_recov IS NOT NULL GROUP BY asset_id) AS b
                    SET a.run_id=(SELECT run_id FROM global_variables WHERE id=1)
                    WHERE a.run_id=b.max_run_id AND a.asset_id=b.asset_id AND b.max_run_id!=(SELECT run_id FROM global_variables WHERE id=1);
					'''
                curr.execute(sql_update)
                curr.execute('COMMIT')
            os.system(next_process_task)
        sys.exit(0)

    elif command.upper() == 'CHECK_PANORAMA':
        process_complete = False
        process_name = 'AutomatedPanorama_' + argumentList[1]
        updateLog(curr, 'e', process_name)
        process_complete = de.check_process('AutomatedPanorama')
        if process_complete:
            updateLog(curr, 'e', 'AutomatedPanorama')
            updateLog(curr, 's', 'Panorama_Export', 'Automated Panorama Export Process')
            is_test_data = get_param(param='export_to_test_db', table='global_variables', data_type='bool')
            de.update_servers(dataset='panorama', export_tables=True, import_tables=True, test_data=is_test_data)
            updateLog(curr, 'e', 'Panorama_Export')
            #send_update_email(send_to=['jason.skophammer@gmail.com'], message='AutomatedPanorama Process complete')
            run_task('10_ExtractAllData', ENGN_TASK_DIR+'10_ExtractAllData.bat')
        sys.exit(0)

    elif command.upper() == 'DISC_FIELD_EXPORT':
        is_test_data = get_param(param='export_to_test_db', table='global_variables', data_type='bool')
        print 'is_test_data: {}'.format(is_test_data)
        # de.update_servers(dataset='discovered', export_tables=True, import_tables=True, truncate=False, test_data=is_test_data)
        os.system('START %engine_drive%:\\GlobalData\\Tasks\\EngineTasks\\Calc_Undiscovered_Reserves_Data')
        sys.exit(0)

    elif command.upper() == 'ENGINE_DATA_EXPORT':
        truncate = True
        if len(argumentList) > 1 and argumentList[1] == 'keep_data':
            truncate = False
        is_test_data = get_param(param='export_to_test_db', table='global_variables', data_type='bool')
        #send_update_email(send_to=['jason.skophammer@gmail.com'], message='EngineDataExport Process complete')
        de.update_servers(dataset='oilgas', export_tables=True, import_tables=True, truncate=truncate, test_data=is_test_data)
        updateLog(curr, 'e', 'EngineDataExport')
        #send_engine_email()
        #send_update_email(send_to=['jason.skophammer@gmail.com'], message='EngineDataExport Process complete')
        updateLog(curr, 's', 'EconomicLimits', 'Economic Limits Report Process')
        run_task('Process_Econ_limit_Models', ENGN_TASK_DIR+'Process_Econ_Limit_Models.bat')
        sys.exit(0)

    elif command.upper() == 'ANALYST_KPI':
        kpi_main()
        sys.exit(0)

    elif command.upper() == 'UPDATE_ASSET_DATA':
        option_list = ['clear_tbl', 'assets']
        if argumentList[1:]:
            option_list = argumentList[1:]
        print 'options:', option_list
        update_asset_data_tbl(option_list, debug=False)
        sys.exit(0)

    elif command.upper() == 'CALC_BREAKEVENS':
        region = argumentList[1]
        xlApp = xw.App(visible=False)
        xlApp.display_alerts = False
        breakeven_main(region=region, excelApp=xlApp)
        xlApp.quit()
        del xlApp
        sys.exit(0)

    elif command.upper() == 'EXTRACT_ECON_DATA':
        region = argumentList[1]
        extract_econ(region)
        sys.exit(0)

    elif command.upper() == 'EXTRACT_DISC_ECON_DATA':
        region = argumentList[1]
        extract_econ(region, BE_REGION_DIR=DF_BE_DIR)
        sys.exit(0)
    
    elif command.upper() == 'EXTRACT_UNDISC_ECON_DATA':
        region = argumentList[1]
        extract_econ(region, undiscovered=True)
        sys.exit(0)
    
    elif command.upper() == 'EXTRACT_DETAILED_ECON_DATA':
        extract_econ(region='detailed', BE_REGION_DIR=DET_MD_NEW_DIR)#region_dir
        sys.exit(0)

    elif command.upper() == 'CALC_MIN_ECON':
        region = argumentList[1]
        xlApp = xw.App(visible=False)
        xlApp.display_alerts = False
        min_econ_main(region=region, excelApp=xlApp)
        xlApp.quit()
        del xlApp
        sys.exit(0)

    elif command.upper() == 'UPDATE_FISCAL':
        update_fiscal_table()
        sys.exit(0)

    elif command.upper() in ['RUNID', 'RUN_ID']:
        try:
            run_id = argumentList[1]
        except:
            run_id = None
        update_run_id(curr, run_id)
        sys.exit(0)

    elif command.upper() == 'SET_NULL':
        table = argumentList[1]
        set_to_null(table)
        set_to_zero(table)
        sys.exit(0)

    elif command.upper() == 'ANALYTICS_REPORT':
        analytics_report()
        sys.exit(0)

    elif command.upper() == 'PROCESS_MINING':
        options = argumentList[1]
        export_data  = False
        archive      = False
        copy_tables  = False
        process_data = False
        gen_reports  = False

        if 'e' in options:
            export_data =True
        if 'a' in options:
            archive = True
        if 'c' in options:
            copy_tables = True
        if 'p' in options:
            process_data = True
        if 'r' in options:
            gen_reports = True

        process_mining_main(archive=archive, copy_tables=copy_tables, process_data=process_data, export_data=export_data, gen_reports=gen_reports)
        sys.exit(0)

    elif command.upper() == 'PROCESS_DETAILED_MODELS':
        detailed_models_main(run_full_process=True, external_server=True)

    elif command.upper() == 'ADD_EXCEPTIONS':
        add_exceptions_main()
        sys.exit(0)

    elif command.upper() == 'CLEAR_SERVER_CHECK':
        data_process = argumentList[1]
        database     = argumentList[2]
        test_data = False
        clear_internal_data = False
        if database.upper() == 'T':
            test_data = True
        else:
            if data_process.upper() == 'ENGINE':
                clear_internal_data = get_param(param='clear_internal_data', table='global_variables', data_type='bool')
            elif data_process.upper() == 'DISC_FIELDS':
                clear_internal_data = get_param(param='clear_internal_data_df', table='global_variables', data_type='bool')
            elif data_process.upper() == 'DETAILED':
                clear_internal_data = get_param(param='clear_internal_data_dt', table='global_variables', data_type='bool')
            else:
                clear_internal_data = False
        if clear_internal_data:
            clear_server_data(data_process, test_data)
        sys.exit(0)

    elif command.upper() == 'ECON_LIMITS':
        econ_limit_main()
        # updateLog(curr, 'e', 'EconomicLimits')
        run_task('12_ImpliedPrices', ENGN_TASK_DIR + '12_ImpliedPrices.bat')
        sys.exit(0)

    # elif command.upper() == 'SEND_EMAIL':
    #     # subject, message = argumentList[1].split(',')[:2]
    #     subject = 'Engine run start'
    #     message = subject
    #     print 'subject: {} -- message: {}'.format(subject, message)
    #     send_update_email(send_to=['sunil.lanke@globaldata.com'], subject='{}'.format(subject), message='{}'.format(message), attach_files=[])
    #     send_engine_email()
    #     sys.exit(0)
    #     pass

    elif command.upper() == 'UPDATE_DISC_FIELD_FACILITY_TYPE':
        debug=False
        update_facility_type(debug=debug)
        sys.exit(0)

    elif command.upper() == 'UPDATE_PRICES_DATA':
        truncate_table(table='prices_data')
        truncate_table(table='prices_data_temp')
        update_prices_data_file()
        import_csv_main(all_files=True, table_name='prices_data_temp', data_dir=CSV_IMPORT_DIR)
        update_prices_data()
        sys.exit(0)

    elif command.upper() == 'UPDATE_KEY_ASSET_DATA':
        key_assets_main(archive=True, extract=True, update_table=True, update_file=True, debug=False)
        sys.exit(0)

    elif command.upper() == 'EXTRACT_SUPPLY_PROD':
        run_id = get_run_id()
        region = argumentList[1]
        extract_production_data(curr, region, run_id)

    elif command.upper() == 'FORECAST_WELLS':
        update_config   = argumentList[1]
        forecast_config = argumentList[2]
        state_list      = argumentList[3]

        update_args     = update_config.split('-')[1].split()
        forecast_args   = forecast_config.split('-')[1].split()
        states          = state_list.split('-')[1].split(',')

        update_params      = False
        update_assumptions = False
        calc_prod          = False
        calc_econ          = False

        if 'p' in update_args:
            update_params = True
        if 'a' in update_args:
            update_assumptions = True

        if 'p' in forecast_args:
            calc_prod = True
        if 'e' in forecast_args:
            calc_econ = True

        state_list_str = ','.join(["'{}'".format(state_code) for state_code in states])
        state_names = get_data('STATE_NAME', 'us_ref_state', server='sql_server', database='US_Wells', sql_where="STATE_CODE IN ({})".format(state_list_str), us_wells=True)

        for state in state_names:
            sql_where = "((Forecast_Well=1) AND (State_Name='{}'))".format(state)
            well_id_list = get_data('API_Number, WellID', 'dbo.tblUSWell_Parameters', sql_where=sql_where, server='sql_server', database='US_Wells', datatype='plural', debug=False, us_wells=True)
            well_forecast_main(well_list=well_id_list, update_params=update_params, update_assumptions=update_assumptions, calc_prod=calc_prod, calc_econ=calc_econ, dec_month_min=0, store_data=True, null_well_type=True, debug=False)

    elif command.upper() == 'PROCESS_SUPPLY_DATA':
        run_id=get_run_id()
        extract_supply_data_main(run_id=run_id, copy_data=True, extract=True, update=True, update_prod=True, undisc=True, export_data=True)
        updateLog(curr, 'e', 'ProcessSupplyData')
        sys.exit(0)

    elif command.upper() == 'CHECK_SUPPLY_MACRO':
        process_complete = False
        process_name = 'SupplyCurveMacro_' + argumentList[1]
        updateLog(curr, 'e', process_name)
        process_complete = de.check_process('SupplyCurveMacro')
        if process_complete:
            updateLog(curr, 'e', 'SupplyCurveMacro')
            os.system('%engine_drive%:\\GlobalData\\Tasks\\EngineTasks\\UpdateAllEconUndisc')
        sys.exit(0)
    
    # elif command.upper() == 'CHECK_SUPPLY_MACRO':
    #     process_complete = False
    #     process_name = 'SupplyCurveMacro_' + argumentList[1]
    #     updateLog(curr, 'e', process_name)
    #     process_complete = de.check_process('SupplyCurveMacro')
    #     if process_complete:
    #         updateLog(curr, 'e', 'SupplyCurveMacro')
    #         os.system(ENGN_TASK_DIR + 'Process_Supply_Curve_Data.bat')
    #     sys.exit(0)
    
    elif command.upper() == 'WELL_DATA_ENGINE':
        engine_phase = argumentList[1]
        texas_data = bool(int(argumentList[2]))
        if engine_phase == '1_1':
            # Import well data
            if not texas_data:
                well_data_main(import_details=True,
                               import_prod=True)
        elif engine_phase == '2_1':
            # Update engine tables
            engine_list = get_engine_list()
            if engine_list == 'tx':
                
                well_data_main(update_well_id_api=True,
                               update_params=True,
                               update_params_insert=True,
                               update_params_data=True,
                               update_params_last_prod=True,
                               all_tx=texas_data,
                               debug=False)
            else:
                well_data_main(update_well_id_api=True,
                               update_prod=True,
                               update_prod_insert=True,
                               update_prod_data=True,
                               update_forecast=True,
                               update_forecast_insert=True,
                               update_forecast_data=True,
                               update_params=True,
                               update_params_insert=True,
                               update_params_data=True,
                               update_params_last_prod=True,
                               all_tx=texas_data,
                               debug=False)
        elif engine_phase in ['3_1', '3_2', '3_3', '3_4', '3_5']:
            if engine_phase == '3_1':
                reset_session_count()
            # Update well parameters (Run as 5 concurrent sessions)
            well_data_main(pre_engine_params=True,
                           choose_assum=True,
                           est_len_params=True,
                           est_len_params_lat_len=True,
                           est_len_params_tvd=True,
                           split_well_list=True)
            process_complete = check_well_engine_session()
            if process_complete:
                run_task('3_6_WellEngineTask_UpdateCost', WELL_TASK_DIR + '3_6_WellEngineTask_UpdateCost.bat')
        elif engine_phase == '3_6':
            # Update well costs
            well_data_main(update_well_costs=True,
                           well_cost_update=True,
                           well_cost_calc=True)
        elif engine_phase in ['4_1', '4_2', '4_3', '4_4', '4_5']:
            if engine_phase == '4_1':
                reset_session_count()
            # Forecast well data
            #(Run as 5 concurrent sessions)
            well_data_main(forecast_prod=True,
                          forecast_econ=False,
                          split_well_list=True)
            _ = raw_input('are all production forecasts complete?')
            well_data_main(forecast_prod=False,
                           forecast_econ=True,
                           split_well_list=True)
            process_complete = check_well_engine_session()
            if process_complete:
                run_task('5_1_WellEngineTask_UpdateCost', WELL_TASK_DIR + '5_1_WellEngineTask_UpdateCost.bat')
        elif engine_phase == '5_1':
            # Post-process data
            well_data_main(post_engine_params=True,
                           copy_engine_params=True,
                           remove_outliers=True,
                           update_last_prod_data=True,
                           update_error_log=True)
        elif engine_phase == '6_1':
            # Export forecast data
            well_data_main(export_params=True,
                           export_econ=True,
                           export_prod=True,
                           export_error_log=True)
        sys.exit(0)

    elif command.upper() == 'TX_DATA_PROCESS':
        pass
    
    elif command.upper() == "SET_ENGINE_LIST":
        engine_list = argumentList[1]
        set_engine_list(str(engine_list))
        sys.exit(0)
    
    elif command.upper() == "CALC_UNDISC_DATA":
        calc_undisc_data(step_0=True, step_1=True, step_2=True, step_3=True, step_4=True, step_5=True, step_6=True, step_7=True, step_8=True)
    
    elif command.upper() == "UPDATE_EXPEND_DATA":
        server_data_import(current_day=True, update_expend=True)
        sys.exit(0)
    else:
        print "Error: Invalid Command"
        sys.exit(1)

def initVariables(mainProgram, options):
    if command.upper() == "DATA_IMPORT":
        mainProgram.assetId = StringVar()
        mainProgram.assetId.set("")

        mainProgram.chkAll = IntVar()
        mainProgram.chkAll.set(0)

        mainProgram.chkOption = ["Production", "Equity", "Reserves", "Assets", "Wells", "Expenditure"]
        mainProgram.chkOption0 = IntVar()
        mainProgram.chkOption1 = IntVar()
        mainProgram.chkOption2 = IntVar()
        mainProgram.chkOption3 = IntVar()
        mainProgram.chkOption4 = IntVar()
        mainProgram.chkOption5 = IntVar()

        mainProgram.chkOption0.set(0)
        mainProgram.chkOption1.set(0)
        mainProgram.chkOption2.set(0)
        mainProgram.chkOption3.set(0)
        mainProgram.chkOption4.set(0)
        mainProgram.chkOption5.set(0)

        mainProgram.totOptions = len(mainProgram.chkOption)
        mainProgram.importSource = StringVar()
        mainProgram.importSource.set("file")

        mainProgram.varMessage = StringVar()
        mainProgram.msgOption0 = StringVar()
        mainProgram.msgOption1 = StringVar()
        mainProgram.msgOption2 = StringVar()
        mainProgram.msgOption3 = StringVar()
        mainProgram.msgOption4 = StringVar()
        mainProgram.msgOption5 = StringVar()

        mainProgram.mProgComment = StringVar()

        mainProgram.varMessage.set("")
        mainProgram.msgOption0.set("")
        mainProgram.msgOption1.set("")
        mainProgram.msgOption2.set("")
        mainProgram.msgOption3.set("")
        mainProgram.msgOption4.set("")
        mainProgram.msgOption5.set("")

        mainProgram.mProgComment.set("")

        if 'A' in options:
            mainProgram.chkAll.set(1)
        if 'p' in options:
            mainProgram.chkOption0.set(1)
        if 'e' in options:
            mainProgram.chkOption1.set(1)
        if 'r' in options:
            mainProgram.chkOption2.set(1)
        if 'a' in options:
            mainProgram.chkOption3.set(1)
        if 'x' in options:
            mainProgram.chkOption5.set(1)
        if 's' in options:
            mainProgram.importSource.set("server")

    elif command.upper() in ["PARAM_IMPORT", "PARAM_EXPORT"]:
        param_dict = dict(abandonment="ABANDONMENT", capex_per_boe="CAPEX PER BOE",
                          capex_tangible_pct="CAPEX TANGIBLE PCT",
                          field_life_threshold_boed="FIELD LIFE THRESHOLD BOED", fiscal="FISCAL",
                          fixed_opex="FIXED OPEX", pricing="PRICING", variable_opex_per_b="VARIABLE OPEX PER B",
                          variable_opex_per_mmcf="VARIABLE OPEX PER MMCF", capex_redevelopment="CAPEX REDEVELOPMENT",
                          abandonment_alloc="ABANDONMENT ALLOC", capex_alloc="CAPEX ALLOC",
                          capex_alloc_redevelopment="CAPEX ALLOC REDEVELOPMENT", prices="PRICES",
                          price_values="PRICES VALUES", unit_conversion="UNIT CONVERSION", inflation="INFLATION",
                          auxilary_param="AUXILARY PARAM", sensitivity="SENSITIVITY",
                          minimum_daily_production="MINIMUM DAILY PRODUCTION", economic_limit="ECONOMIC LIMIT",
                          opex_capacity="OPEX CAPACITY", capex_capcity="CAPEX CAPACITY", all="ALL")

        mainProgram.lblDirName = StringVar()
        mainProgram.mExportDir = StringVar()
        mainProgram.varType_function = StringVar()
        mainProgram.mFileLabel = StringVar()
        mainProgram.varParam_titles = StringVar()

        mainProgram.lblDirName = mainProgram.mDataDir.get()
        mainProgram.mExportDir.set(mainProgram.mDataDir.get())
        mainProgram.varType_function.set(command[6:])
        mainProgram.varParam_titles.set(param_dict[options])

        mainProgram.param_titles = ["ABANDONMENT", "CAPEX PER BOE", "CAPEX TANGIBLE PCT", "FIELD LIFE THRESHOLD BOED",
                                    "FISCAL", "FIXED OPEX", "PRICING", "VARIABLE OPEX PER B", "VARIABLE OPEX PER MMCF",
                                    "CAPEX REDEVELOPMENT", "ABANDONMENT ALLOC", "CAPEX ALLOC",
                                    "CAPEX ALLOC REDEVELOPMENT", "PRICES", "PRICES VALUES", "UNIT CONVERSION",
                                    "INFLATION", "AUXILARY PARAM", "SENSITIVITY", "MINIMUM DAILY PRODUCTION",
                                    "ECONOMIC LIMIT", "OPEX CAPACITY", "CAPEX CAPACITY", "ALL"]

        mainProgram.param_names = ["ABANDONMENT", "CAPEX_PER_BOE", "CAPEX_TANGIBLE_PCT",
                                   "FIELD_LIFE_ANNUAL_PROD_THRESH_BOED", "FISCAL", "FIXED_OPEX", "PRICING",
                                   "VARIABLE_OPEX_PER_B", "VARIABLE_OPEX_PER_MMCF", "CAPEX_REDEVELOPMENT",
                                   "ABANDONMENT_ALLOC", "CAPEX_ALLOC", "CAPEX_REDEV_ALLOC", "PRICES", "PRICES_VALUES",
                                   "UNIT_CONVERSION", "INFLATION", "AUXILARY_PARAM", "SENSITIVITY",
                                   "MINIMUM_DAILY_PRODUCTION", "ECONOMIC_LIMIT", "OPEX_CAPACITY", "CAPEX_CAPACITY", "ALL"]

        mainProgram.table_name = ["MODEL_RULES", "MODEL_RULES", "MODEL_RULES", "MODEL_RULES", "MODEL_RULES",
                                  "MODEL_RULES", "MODEL_RULES", "MODEL_RULES", "MODEL_RULES", "MODEL_RULES",
                                  "ABANDONMENT_ALLOC", "CAPEX_ALLOC", "CAPEX_REDEV_ALLOC", "PRICES", "PRICES_VALUES",
                                  "UNIT_CONVERSION", "INFLATION", "AUXILARY_PARAM", "MODEL_RULES", "MODEL_RULES",
                                  "ECONOMIC_LIMIT", "MODEL_RULES", "MODEL_RULES", "ALL"]

        mainProgram.param_type = ["P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "T", "T", "T", "T", "T", "T", "T",
                                  "T", "P", "P", "T", "T", "T", "A"]

        mainProgram.generalMsg = StringVar()
        mainProgram.generalMsg.set("")
        mainProgram.mFileLabel.set("File")

    elif command.upper() == 'CREATE_MODEL':

        mainProgram.debug.set(1)

        mainProgram.roundTo = IntVar()
        mainProgram.roundTo.set(4)

        mainProgram.generalMsg = StringVar()
        mainProgram.generalMsg.set("")
        
        mainProgram.assetId = StringVar()
        mainProgram.assetId.set("")

        mainProgram.assetCountryName = StringVar()
        mainProgram.assetCountryName.set("")

        mainProgram.constituentName = StringVar()
        mainProgram.constituentName.set("")

        mainProgram.regionName = StringVar()
        mainProgram.regionName.set("")

        mainProgram.statusName = StringVar()
        mainProgram.statusName.set("")

        mainProgram.terrainName = StringVar()
        mainProgram.terrainName.set("")

        mainProgram.resourceName = StringVar()
        mainProgram.resourceName.set("")

        mainProgram.facilityTypeName = StringVar()
        mainProgram.facilityTypeName.set("")

        mainProgram.basinName = StringVar()
        mainProgram.basinName.set("")

        mainProgram.operatorName = StringVar()
        mainProgram.operatorName.set("")
        
        mainProgram.chkAll = IntVar()
        mainProgram.chkAll.set(0)
        
        mainProgram.chkDebugMode = IntVar()
        mainProgram.chkDebugMode.set(0)
        
        mainProgram.chkDeleteExistingFiles = IntVar()
        mainProgram.chkDeleteExistingFiles.set(0)
        
        mainProgram.chkDeleteForecastData = IntVar()
        mainProgram.chkDeleteForecastData.set(0)        
        
        mainProgram.chkTestNewModule = IntVar()
        mainProgram.chkTestNewModule.set(0)
        
        mainProgram.chkBEModule = IntVar()
        mainProgram.chkBEModule.set(0)
        
        mainProgram.chkFEATModule = IntVar()
        mainProgram.chkFEATModule.set(0)

        mainProgram.chkExternalAssetFile = IntVar()
        mainProgram.chkExternalAssetFile.set(0)

        mainProgram.chkStatusAnnounced.set(1)
        mainProgram.chkStatusAbandoned.set(1)
        mainProgram.chkStatusPlanned.set(1)
        mainProgram.chkStatusProducing.set(1)
        mainProgram.chkStatusStalled.set(1)
        mainProgram.chkStatusSuspended.set(1)

        mainProgram.chkAfrica = IntVar()
        mainProgram.chkAsia = IntVar()
        mainProgram.chkCaribbean = IntVar()
        mainProgram.chkCentralAmerica = IntVar()
        mainProgram.chkEurope = IntVar()
        mainProgram.chkMiddleEast = IntVar()
        mainProgram.chkNorthAmerica = IntVar()
        mainProgram.chkOceania = IntVar()
        mainProgram.chkSouthAmerica = IntVar()
        mainProgram.chkFormerSovietUnion = IntVar()

        mainProgram.chkAfrica.set(0)
        mainProgram.chkAsia.set(0)
        mainProgram.chkCaribbean.set(0)
        mainProgram.chkCentralAmerica.set(0)
        mainProgram.chkEurope.set(0)
        mainProgram.chkMiddleEast.set(0)
        mainProgram.chkNorthAmerica.set(0)
        mainProgram.chkOceania.set(0)
        mainProgram.chkSouthAmerica.set(0)
        mainProgram.chkFormerSovietUnion.set(0)

        mainProgram.run_check = IntVar()
        mainProgram.run_check.set(1)

        mainProgram.msgAll = StringVar()
        mainProgram.msgAfrica = StringVar()
        mainProgram.msgAsia = StringVar()
        mainProgram.msgCaribbean = StringVar()
        mainProgram.msgCentralAmerica = StringVar()
        mainProgram.msgEurope = StringVar()
        mainProgram.msgMiddleEast = StringVar()
        mainProgram.msgNorthAmerica = StringVar()
        mainProgram.msgOceania = StringVar()
        mainProgram.msgSouthAmerica = StringVar()
        mainProgram.msgFormerSovietUnion = StringVar()

        mainProgram.msgAll.set('')
        mainProgram.msgAfrica.set('')
        mainProgram.msgAsia.set('')
        mainProgram.msgCaribbean.set('')
        mainProgram.msgCentralAmerica.set('')
        mainProgram.msgEurope.set('')
        mainProgram.msgMiddleEast.set('')
        mainProgram.msgNorthAmerica.set('')
        mainProgram.msgOceania.set('')
        mainProgram.msgSouthAmerica.set('')
        mainProgram.msgFormerSovietUnion.set('')
        mainProgram.mRegionFolder.set('')

        mainProgram.code_profile = False
        mainProgram.profile_param_detail = False
        mainProgram.output_files = True
        mainProgram.full_forecast = False
        mainProgram.north_america_split = True
        mainProgram.save_breakeven_models = True
        mainProgram.calc_deals = False
        mainProgram.model_all = False
        mainProgram.write_inflation_values = False
        mainProgram.model_non_engine = False
        mainProgram.external_server = False
        mainProgram.update_operators = False
        mainProgram.model_discovered_fields = False
        mainProgram.is_engine_run = True
        for i in range(1,len(argumentList)):
            option = argumentList[i][:6]
            print "option",i,":",option
            if option in 'engine':
                mainProgram.is_engine_run = True
            if option == '-dbug-':
                mainProgram.debug.set(int(argumentList[i][6:]) + 1)
            if option == "-delt-":
                delete_options = list(argumentList[i][6:])
                if 'e' in delete_options:
                    mainProgram.chkDeleteExistingFiles.set(1)
                if 'f' in delete_options:
                    mainProgram.chkDeleteForecastData.set(1)
            if option == "-asid-":
                mainProgram.assetId.set(argumentList[i][6:])
                if not ',' in argumentList[i][6:]:
                    asset_region = get_param(param='region', table='assets', sql_where='asset_id={}'.format(argumentList[i][6:]))
                    mainProgram.mRegionFolder.set(asset_region)
            if option == "-ctry-":
                mainProgram.assetCountryName.set(argumentList[i][6:])
                print "country:", argumentList[i][6:]
                country_region = get_param(param='DISTINCT region', table='assets', sql_where='country="{}"'.format(argumentList[i][6:]))
                mainProgram.mRegionFolder.set(country_region)
            if option == "-regn-":
                regions = argumentList[i][6:].split(',')
                print "regions:", argumentList[i][6:].split(',')
                if 'africa' in regions:
                    mainProgram.chkAfrica.set(1)
                    mainProgram.mRegionFolder.set('Africa')
                if 'asia' in regions:
                    mainProgram.chkAsia.set(1)
                    mainProgram.mRegionFolder.set('Asia')
                if 'caribbean' in regions:
                    mainProgram.chkCaribbean.set(1)
                    mainProgram.mRegionFolder.set('Caribbean')
                if 'central_america' in regions:
                    mainProgram.chkCentralAmerica.set(1)
                    mainProgram.mRegionFolder.set('Central America')

                if 'europe' in regions:
                    mainProgram.chkEurope.set(1)
                    mainProgram.mRegionFolder.set('Europe')
                if 'europe_1' in regions:
                    mainProgram.getAssetFile(EU_1)
                    #mainProgram.mRegionFolder.set('Europe_1')
                    mainProgram.mRegionFolder.set('Europe')
                if 'europe_2' in regions:
                    mainProgram.getAssetFile(EU_2)
                    #mainProgram.mRegionFolder.set('Europe_2')
                    mainProgram.mRegionFolder.set('Europe')
                if 'europe_3' in regions:
                    mainProgram.getAssetFile(EU_3)
                    #mainProgram.mRegionFolder.set('Europe_3')
                    mainProgram.mRegionFolder.set('Europe')

                if 'middle_east' in regions:
                    mainProgram.chkMiddleEast.set(1)
                    mainProgram.mRegionFolder.set('Middle East')
                if 'oceania' in regions:
                    mainProgram.chkOceania.set(1)
                    mainProgram.mRegionFolder.set('Oceania')

                if 'south_america' in regions:
                    mainProgram.chkSouthAmerica.set(1)
                    mainProgram.mRegionFolder.set('South America')
                if 'south_america_1' in regions:
                    mainProgram.getAssetFile(SA_1)
                    #mainProgram.mRegionFolder.set('South_America_1')
                    mainProgram.mRegionFolder.set('South America')
                if 'south_america_2' in regions:
                    mainProgram.getAssetFile(SA_2)
                    #mainProgram.mRegionFolder.set('South_America_2')
                    mainProgram.mRegionFolder.set('South America')
                if 'south_america_3' in regions:
                    mainProgram.getAssetFile(SA_3)
                    #mainProgram.mRegionFolder.set('South_America_3')
                    mainProgram.mRegionFolder.set('South America')

                if 'former_soviet_union' in regions:
                    mainProgram.chkFormerSovietUnion.set(1)
                    mainProgram.mRegionFolder.set('Former Soviet Union')
                if 'former_soviet_union_1' in regions:
                    mainProgram.getAssetFile(FS_1)
                    #mainProgram.mRegionFolder.set('Former_Soviet_Union_1')
                    mainProgram.mRegionFolder.set('Former Soviet Union')
                if 'former_soviet_union_2' in regions:
                    mainProgram.getAssetFile(FS_2)
                    #mainProgram.mRegionFolder.set('Former_Soviet_Union_2')
                    mainProgram.mRegionFolder.set('Former Soviet Union')
                if 'former_soviet_union_3' in regions:
                    mainProgram.getAssetFile(FS_3)
                    #mainProgram.mRegionFolder.set('Former_Soviet_Union_3')
                    mainProgram.mRegionFolder.set('Former Soviet Union')
                if 'former_soviet_union_4' in regions:
                    mainProgram.getAssetFile(FS_4)
                    #mainProgram.mRegionFolder.set('Former_Soviet_Union_4')
                    mainProgram.mRegionFolder.set('Former Soviet Union')

                if 'north_america' in regions:
                    mainProgram.chkNorthAmerica.set(1)
                    mainProgram.mRegionFolder.set('North America')
                if 'north_america_1' in regions:
                    mainProgram.getAssetFile(NA_1)
                    mainProgram.mRegionFolder.set('North_America_1')
                if 'north_america_2' in regions:
                    mainProgram.getAssetFile(NA_2)
                    mainProgram.mRegionFolder.set('North_America_2')
                if 'north_america_3' in regions:
                    mainProgram.getAssetFile(NA_3)
                    #mainProgram.mRegionFolder.set('North_America_3')
                    mainProgram.mRegionFolder.set('North_America_1')
                if 'north_america_4' in regions:
                    mainProgram.getAssetFile(NA_4)
                    #mainProgram.mRegionFolder.set('North_America_4')
                    mainProgram.mRegionFolder.set('North_America_2')
                if 'north_america_5' in regions:
                    mainProgram.getAssetFile(NA_5)
                    #mainProgram.mRegionFolder.set('North_America_5')
                    mainProgram.mRegionFolder.set('North_America_2')
                if 'north_america_6' in regions:
                    mainProgram.getAssetFile(NA_6)
                    #mainProgram.mRegionFolder.set('North_America_6')
                    mainProgram.mRegionFolder.set('North_America_2')

                if 'unconventional' in regions:
                    mainProgram.getAssetFile(UN_1)
                    mainProgram.mRegionFolder.set('Unconventional')
                uncon_files = [
                    UN_1,
                    UN_2,
                    UN_3,
                    UN_4,
                    UN_5,
                    UN_6,
                    UN_7,
                    UN_8,
                    UN_9
                ]
                for i in range(1,10):
                    if 'uncon{}'.format(i) in regions or 'unconventional_{}'.format(i) in regions:
                        print 'i-1: {} -- uncon_files[{}]: {}'.format(i-1, i-1, uncon_files[i-1])
                        mainProgram.getAssetFile(uncon_files[i-1])
                        mainProgram.mRegionFolder.set('Unconventional')
                test_files = [
                    TEST_1,
                    TEST_2,
                    TEST_3,
                    TEST_4,
                    TEST_5,
                    TEST_6,
                    TEST_7,
                    TEST_8,
                    TEST_9,
                    TEST_10,
                    TEST_11,
                    TEST_12,
                    TEST_13,
                    TEST_14,
                    TEST_15,
                    TEST_16,
                    TEST_17,
                    TEST_18,
                    TEST_19,
                    TEST_20

                ]
                for i in range(1,21):
                    if 'test{}'.format(i) in regions:
                        mainProgram.getAssetFile(test_files[i - 1])
                        if not os.path.exists(REGIONS_DIR + 'Test_{}\\'.format(i)):
                            os.mkdir(REGIONS_DIR + 'Test_{}\\'.format(i))
                        mainProgram.mRegionFolder.set('Test_{}'.format(i))
                if 'disc_africa' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_AF)
                if 'disc_asia' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_AS)
                if 'disc_caribbean' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_CR)
                if 'disc_central_america' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_CA)
                if 'disc_europe' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_EU)
                if 'disc_former_soviet_union' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_FS)
                if 'disc_middle_east' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_ME)
                if 'disc_north_america' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_NA)
                if 'disc_oceania' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_OC)
                if 'disc_south_america' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_SA)
                if 'disc_rest_of_world_1' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_RW_1)
                if 'disc_rest_of_world_2' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_RW_2)
                if 'disc_rest_of_world_3' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_RW_3)
                if 'disc_F1' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_FS_1)
                if 'disc_F2' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_FS_2)
                if 'disc_F3' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_FS_3)
                if 'disc_F4' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_FS_4)
                if 'disc_E1' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_EU_1)
                if 'disc_E2' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_EU_2)
                if 'disc_E3' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_EU_3)
                if 'disc_N1' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_NA_1)
                if 'disc_N2' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_NA_2)
                if 'disc_N3' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_NA_3)
                if 'disc_N4' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_NA_4)
                if 'disc_N5' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_NA_5)
                if 'disc_N6' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_NA_6)
                if 'disc_S1' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_SA_1)
                if 'disc_S2' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_SA_2)
                if 'disc_S3' in regions:
                    mainProgram.model_discovered_fields = True
                    mainProgram.getAssetFile(DF_SA_3)
            if option == "-stat-":
                statuses = list(argumentList[i][6:])
                print "status: ", list(argumentList[i][6:])
                if 'b' in statuses:
                    mainProgram.chkStatusAbandoned.set(1)
                if 'n' in statuses:
                    mainProgram.chkStatusAnnounced.set(1)
                if 'l' in statuses:
                    mainProgram.chkStatusPlanned.set(1)
                if 'r' in statuses:
                    mainProgram.chkStatusProducing.set(1)
                    mainProgram.chkStatusStalled.set(1)
                    mainProgram.chkStatusSuspended.set(1)
                if 's' in statuses:
                    mainProgram.chkStatusStalled.set(1)
            if option == "-cnst":
                mainProgram.constituentName.set(argumentList[i][6:])
            if option == "-trrn-":
                mainProgram.terrainName.set(argumentList[i][6:])
            if option == "-rsrc-":
                mainProgram.resourceName.set(argumentList[i][6:])
            if option == "-fcty-":
                mainProgram.facilityTypeName.set(argumentList[i][6:])
            if option == "-basn-":
                mainProgram.basinName.set(argumentList[i][6:])
            if option == "-optr-":
                mainProgram.operatorName.set(argumentList[i][6:])
            if option == "-rnid-":
                mainProgram.run_check.set(argumentList[i][6:])
            if option == "-file-":
                mainProgram.getAssetFile(argumentList[i][6:])
            if option == "-deal-":
                mainProgram.calc_deals = True
                mainProgram.write_inflation_values = True
                mainProgram.mRegionFolder.set('Deals\\incomplete')
            if option == "-detm-":
                mainProgram.detailed_models = True
                mainProgram.getAssetFile(DT_1)
            if option == "-eclm-":
                mainProgram.econ_limit = False
                mainProgram.econ_limit_rerun = True
                mainProgram.getAssetFile(EL_1)
                mainProgram.mRegionFolder.set(ECN_LMT_EN_DIR)
            if option == "-arps-":
                mainProgram.getAssetFile(ARPS_TEST)
            if option == "-scnr-":
                mainProgram.save_breakeven_models = True
                scenario_settings = argumentList[i][6:].split('|')
                scenario_num = int(scenario_settings[0])
                region_count = int(scenario_settings[1])
                mainProgram.assetId.set(scenario_settings[2])
                mainProgram.mRegionFolder.set('Scenarios\\scenario_{}\\engine'.format(scenario_num))
                '''
                if not os.path.exists(REGIONS_DIR + 'Scenarios\\'):
                    os.mkdir(REGIONS_DIR + 'Scenarios\\')

                if not os.path.exists(REGIONS_DIR + 'Scenarios\\scenario_{}\\'.format(scenario_num)):
                    os.mkdir(REGIONS_DIR + 'Scenarios\\scenario_{}\\'.format(scenario_num))

                if not os.path.exists(REGIONS_DIR + 'Scenarios\\scenario_{}\\engine\\'.format(scenario_num)):
                    os.mkdir(REGIONS_DIR + 'Scenarios\\scenario_{}\\engine\\'.format(scenario_num))

                for region_num in range(1, region_count+1):
                    if not os.path.exists(REGIONS_DIR + 'Scenarios\\scenario_{}\\region_{}\\'.format(scenario_num, region_num)):
                        os.mkdir(REGIONS_DIR + 'Scenarios\\scenario_{}\\region_{}\\'.format(scenario_num, region_num))
                    shutil.copy2(REGIONS_DIR + 'Scenarios\\Breakeven_Scenario_.xlsm', REGIONS_DIR + 'Scenarios\\scenario_{}\\Breakeven_Scenario_{}.xlsm'.format(scenario_num, region_num))
                    breakeven_config('engine', scenario_num, region_num)
                '''
            if option == '-disc-':
                mainProgram.model_discovered_fields = True
                mainProgram.output_files = False



# Functions run during discovered field data processing ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def choose_facility_type(cursor, field_id):
    facility_type = 'NULL'
    sql_select = '''SELECT c.facilitytype AS facility_type, SUM(c.analoguescore) AS total_analogue_score
    FROM (SELECT a.analogue_id, a.analogue_score AS analoguescore, b.facility_type AS facilitytype FROM globaldata.field_analogues AS a, globaldata.assets AS b WHERE a.analogue_id=b.asset_id AND a.asset_id={}) AS c
    WHERE NOT c.facilitytype='NULL' GROUP BY c.facilitytype ORDER BY total_analogue_score DESC LIMIT 1'''.format(field_id)
    if cursor.execute(sql_select):
        analogue_facility, analogue_facility_score = cursor.fetchall()[0]
        cursor.execute('UPDATE asset_data SET facility_type="{}" WHERE asset_id={}'.format(analogue_facility, field_id))
        commit(cursor)
        facility_type = analogue_facility
    return facility_type

def update_facility_type(debug=False):
    conn = get_connection()
    curr = conn.cursor()
    where_clause = 'asset_id IN (SELECT DISTINCT asset_id FROM field_analogues ORDER BY asset_id) AND (facility_type IS NULL OR facility_type="NULL")'
    disc_field_ids = get_data('asset_id', 'asset_data', sql_where=where_clause, datatype='int')
    if debug: print 'disc_field_ids: {}'.format(disc_field_ids)
    count=0
    print('Assets to be updated : {}'.format(len(disc_field_ids)))
    for disc_field_id in sorted(list(set(disc_field_ids))):
        changed_val = choose_facility_type(cursor=curr, field_id=disc_field_id)
        if debug: print '{}: {}'.format(disc_field_id, changed_val)
        count+=1
        print(('Updated {} assets facility type').format(count))
    curr.close()
    conn.close()

# Function run before engine data processing ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_prices_data_file():
    output_filename = 'prices_data_{}.csv'.format(get_date())
    prices_filename = os.listdir(CSV_IMPORT_DIR)[0]
    output_lines = ''
    with open(CSV_IMPORT_DIR + prices_filename) as prices_file:
        for prices_file_line in prices_file.readlines():
            if '(%)' in prices_file_line:
                output_lines += (prices_file_line.replace(' (%)', '_pct'))
            else:
                output_lines += prices_file_line
    shutil.move(CSV_IMPORT_DIR + prices_filename, DATA_DIR + prices_filename)
    with open(CSV_IMPORT_DIR + output_filename, 'w') as output_file:
        output_file.write(output_lines)

def update_prices_data():
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("TRUNCATE TABLE prices_data")
    commit(curr)
    sql_insert = """INSERT INTO prices_data (`prices_id`, `price_code`, `price_name`, `price_link_type`, `price_link_code`, `price_link_factor`, `1900`, `1901`, `1902`, `1903`, `1904`, `1905`, `1906`, `1907`, `1908`, `1909`, `1910`, `1911`, `1912`, `1913`, `1914`, `1915`, `1916`, `1917`, `1918`, `1919`, `1920`, `1921`, `1922`, `1923`, `1924`, `1925`, `1926`, `1927`, `1928`, `1929`, `1930`, `1931`, `1932`, `1933`, `1934`, `1935`, `1936`, `1937`, `1938`, `1939`, `1940`, `1941`, `1942`, `1943`, `1944`, `1945`, `1946`, `1947`, `1948`, `1949`, `1950`, `1951`, `1952`, `1953`, `1954`, `1955`, `1956`, `1957`, `1958`, `1959`, `1960`, `1961`, `1962`, `1963`, `1964`, `1965`, `1966`, `1967`, `1968`, `1969`, `1970`, `1971`, `1972`, `1973`, `1974`, `1975`, `1976`, `1977`, `1978`, `1979`, `1980`, `1981`, `1982`, `1983`, `1984`, `1985`, `1986`, `1987`, `1988`, `1989`, `1990`, `1991`, `1992`, `1993`, `1994`, `1995`, `1996`, `1997`, `1998`, `1999`, `2000`, `2001`, `2002`, `2003`, `2004`, `2005`, `2006`, `2007`, `2008`, `2009`, `2010`, `2011`, `2012`, `2013`, `2014`, `2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`, `2025`, `2026`, `2027`, `2028`, `2029`, `2030`, `2031`, `2032`, `2033`, `2034`, `2035`, `2036`, `2037`, `2038`, `2039`, `2040`, `2041`, `2042`, `2043`, `2044`, `2045`, `2046`, `2047`, `2048`, `2049`, `2050`, `2051`, `2052`, `2053`, `2054`, `2055`, `2056`, `2057`, `2058`, `2059`, `2060`, `2061`, `2062`, `2063`, `2064`, `2065`, `2066`, `2067`, `2068`, `2069`, `2070`, `2071`, `2072`, `2073`, `2074`, `2075`, `2076`, `2077`, `2078`, `2079`, `2080`, `2081`, `2082`, `2083`, `2084`, `2085`, `2086`, `2087`, `2088`, `2089`, `2090`, `2091`, `2092`, `2093`, `2094`, `2095`, `2096`, `2097`, `2098`, `2099`, `2100`) (SELECT `SNo`, `Short Name`, `Long Name`, `Type`, `Link`, `Factor_pct`, `1900`, `1901`, `1902`, `1903`, `1904`, `1905`, `1906`, `1907`, `1908`, `1909`, `1910`, `1911`, `1912`, `1913`, `1914`, `1915`, `1916`, `1917`, `1918`, `1919`, `1920`, `1921`, `1922`, `1923`, `1924`, `1925`, `1926`, `1927`, `1928`, `1929`, `1930`, `1931`, `1932`, `1933`, `1934`, `1935`, `1936`, `1937`, `1938`, `1939`, `1940`, `1941`, `1942`, `1943`, `1944`, `1945`, `1946`, `1947`, `1948`, `1949`, `1950`, `1951`, `1952`, `1953`, `1954`, `1955`, `1956`, `1957`, `1958`, `1959`, `1960`, `1961`, `1962`, `1963`, `1964`, `1965`, `1966`, `1967`, `1968`, `1969`, `1970`, `1971`, `1972`, `1973`, `1974`, `1975`, `1976`, `1977`, `1978`, `1979`, `1980`, `1981`, `1982`, `1983`, `1984`, `1985`, `1986`, `1987`, `1988`, `1989`, `1990`, `1991`, `1992`, `1993`, `1994`, `1995`, `1996`, `1997`, `1998`, `1999`, `2000`, `2001`, `2002`, `2003`, `2004`, `2005`, `2006`, `2007`, `2008`, `2009`, `2010`, `2011`, `2012`, `2013`, `2014`, `2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`, `2025`, `2026`, `2027`, `2028`, `2029`, `2030`, `2031`, `2032`, `2033`, `2034`, `2035`, `2036`, `2037`, `2038`, `2039`, `2040`, `2041`, `2042`, `2043`, `2044`, `2045`, `2046`, `2047`, `2048`, `2049`, `2050`, `2051`, `2052`, `2053`, `2054`, `2055`, `2056`, `2057`, `2058`, `2059`, `2060`, `2061`, `2062`, `2063`, `2064`, `2065`, `2066`, `2067`, `2068`, `2069`, `2070`, `2071`, `2072`, `2073`, `2074`, `2075`, `2076`, `2077`, `2078`, `2079`, `2080`, `2081`, `2082`, `2083`, `2084`, `2085`, `2086`, `2087`, `2088`, `2089`, `2090`, `2091`, `2092`, `2093`, `2094`, `2095`, `2096`, `2097`, `2098`, `2099`, `2100` FROM prices_data_temp)"""
    curr.execute(sql_insert)
    commit(curr)
    curr.execute("TRUNCATE TABLE prices_data_temp")
    commit(curr)
    curr.execute("UPDATE prices_data SET `2101`=`2100`, `2102`=`2100`, `2103`=`2100`, `2104`=`2100`, `2105`=`2100`, `2106`=`2100`, `2107`=`2100`, `2108`=`2100`, `2109`=`2100`, `2110`=`2100`, `2111`=`2100`, `2112`=`2100`, `2113`=`2100`, `2114`=`2100`, `2115`=`2100`, `2116`=`2100`, `2117`=`2100`, `2118`=`2100`, `2119`=`2100`, `2120`=`2100`, `2121`=`2100`, `2122`=`2100`, `2123`=`2100`, `2124`=`2100`, `2125`=`2100`, `2126`=`2100`, `2127`=`2100`, `2128`=`2100`, `2129`=`2100`, `2130`=`2100`, `2131`=`2100`, `2132`=`2100`")
    commit(curr)
    curr.execute("UPDATE prices_data SET is_crude_oil_price=0, is_natural_gas_price=0, is_condensate_price=0, is_ngls_price=0, is_lng_price=0")
    commit(curr)
    curr.execute("UPDATE prices_data AS a, prices AS b SET a.is_crude_oil_price=1   WHERE b.commodity='Crude Oil' AND a.price_code=b.price_code")
    commit(curr)
    curr.execute("UPDATE prices_data AS a, prices AS b SET a.is_natural_gas_price=1 WHERE b.commodity='Natural Gas' AND a.price_code=b.price_code")
    commit(curr)
    curr.execute("UPDATE prices_data AS a, prices AS b SET a.is_condensate_price=1  WHERE b.commodity='Condensate' AND a.price_code=b.price_code")
    commit(curr)
    curr.execute("UPDATE prices_data AS a, prices AS b SET a.is_ngls_price=1        WHERE b.commodity='NGLs' AND a.price_code=b.price_code")
    commit(curr)
    curr.execute("UPDATE prices_data AS a, prices AS b SET a.is_lng_price=1         WHERE b.commodity='LNG' AND a.price_code=b.price_code")
    commit(curr)
    curr.execute("UPDATE prices_data SET unit='usd/bbl' WHERE (is_crude_oil_price=1 OR is_ngls_price=1 OR is_condensate_price=1) AND unit IS NULL")
    commit(curr)
    curr.execute("UPDATE prices_data SET unit='usd/bbl', is_crude_oil_price=1 WHERE (price_name LIKE '%crude%' OR price_name LIKE '%oil%') AND unit IS NULL")
    commit(curr)
    curr.execute("UPDATE prices_data SET unit='usd/bbl', is_ngls_price=1 WHERE price_name LIKE '%ngl%' AND unit IS NULL")
    commit(curr)
    curr.execute("UPDATE prices_data SET unit='usd/bbl', is_condensate_price=1 WHERE price_name LIKE '%condensate%' AND unit IS NULL")
    commit(curr)
    curr.execute("UPDATE prices_data SET unit='usd/mcf' WHERE (is_natural_gas_price=1 OR is_lng_price=1) AND unit IS NULL")
    commit(curr)
    curr.execute("UPDATE prices_data SET unit='usd/mcf', is_natural_gas_price=1 WHERE price_name LIKE '%gas%' AND unit IS NULL")
    commit(curr)
    curr.execute("UPDATE prices_data SET unit='usd/mcf', is_lng_price=1 WHERE price_name LIKE '%lng%' AND unit IS NULL")
    commit(curr)

    curr.close()
    conn.close()

def update_fiscal_table():
    conn = get_connection()
    curr = conn.cursor()

    curr.execute('SELECT fiscalModelDir FROM global_variables WHERE id=1')
    fiscal_dir = curr.fetchone()[0]
    fiscal_models = [fiscal_model for fiscal_model in os.listdir(fiscal_dir) if fiscal_model[-4:] == 'xlsx']

    curr.execute('SELECT DISTINCT file_name FROM fiscal')
    fiscal_file_names = [data[0] for data in curr.fetchall()]
    for fiscal_file_name in fiscal_file_names:
        available = 0
        if fiscal_file_name in fiscal_models:
            available = 1
        sql_update = 'UPDATE fiscal SET available=%s WHERE file_name="%s"' % (available, fiscal_file_name)
        curr.execute(sql_update)
        curr.execute('COMMIT')
    curr.close()
    conn.close()

def clear_server_data(data_process, test_data=False):
    database = 'OGEngineDataExtract'
    if test_data:
        database = 'OG_Effuah'

    tables = OILGAS_TABLE_DATA.keys()
    if data_process.upper() == 'DISC_FIELDS':
        tables = DISCOVERED_TABLE_DATA.keys()

    conn = get_connection(server='sql_server', database=database)
    curr = conn.cursor()

    for table_name in tables:
        print 'Clearing data from {}'.format(table_name)
        curr.execute('TRUNCATE TABLE Engine.{}'.format(table_name))
        curr.execute('COMMIT')

    curr.close()
    conn.close()

# Functions used with processing deals ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_deals_process(curr):
    processed   = [model for model in os.listdir(DEALS_DIR + 'Completed\\') if model[0] != "~" and model[-4:] == 'xlsx']
    unprocessed = [model for model in os.listdir(DEALS_DIR) if model[0] != "~" and model[-4:] == 'xlsx']
    if unprocessed:
        os.system(CMD_TASK_DIR + 'calc_implied_prices.bat')
        pass
    elif processed:
        for model in processed:
            shutil.move(DEALS_DIR + 'Completed\\' + model, DEALS_DIR + model)
        updateLog(curr, 'e', 'ImpliedPrices')
        run_task('13_EndRun', ENGN_TASK_DIR+'13_EndRun.bat')
        # os.system('START %engine_drive%:\\GlobalData\\Tasks\\EngineTasks\\Process_Detailed_Models')


# Functions used in econ_data update -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_breakeven_data(curr, be_file=None):
    curr.execute('SELECT run_id FROM global_variables WHERE id=1')
    run_id = curr.fetchone()[0]
    be_file = [report for report in os.listdir(REPORTS_DIR) if report == 'Breakeven Review ' + run_id + '.xlsx'][0]
    be_report = openpyxl.load_workbook(be_file)
    try:
        be_data = be_report['RAW DATA']
    except:
        be_data = be_report.get_sheet_by_name('RAW DATA')

    for row in range(2, be_data.max_row + 1):
        print row
        be_oil_rem = be_data['J' + str(row)].value
        be_gas_rem = be_data['K' + str(row)].value
        be_oil_dev = be_data['L' + str(row)].value
        be_gas_dev = be_data['M' + str(row)].value
        asset_id   = be_data['A' + str(row)].value

        if not (isinstance(be_oil_rem, long) or isinstance(be_oil_rem, float)):
            be_oil_rem = 0
        if not (isinstance(be_gas_rem, long) or isinstance(be_gas_rem, float)):
            be_gas_rem = 0
        if not (isinstance(be_oil_dev, long) or isinstance(be_oil_dev, float)):
            be_oil_dev = 0
        if not (isinstance(be_gas_dev, long) or isinstance(be_gas_dev, float)):
            be_gas_dev = 0

        sql_update = 'UPDATE econ_data SET be_oil_rem=%s, be_gas_rem=%s, be_oil_dev=%s, be_gas_dev=%s '
        sql_update += 'WHERE session_key LIKE "%%Titan_' + run_id + '%%" AND asset_id=%s'

        params = (be_oil_rem, be_gas_rem, be_oil_dev, be_gas_dev, asset_id)
        print sql_update % params

        curr.execute(sql_update, params)
        curr.execute('COMMIT;')
        be_report.save(be_file)

def get_uncon_data(curr, asset_id, run_id):
    uncon_data = ()
    discount_year = get_discount_year()
    sql_select = 'SELECT MAX(period), (IFNULL(production_count,100)/100) FROM wells WHERE datatype="Working Interest" AND asset_id={}'.format(asset_id)
    curr.execute(sql_select)
    working_interest = float(curr.fetchone()[1])

    sql_select = 'SELECT IFNULL(rigs,0) FROM uncon_production WHERE period={} AND asset_id={}'.format(discount_year, asset_id)
    print sql_select
    curr.execute(sql_select)
    result = curr.fetchone()
    print result
    rig_count = round(float(result[0])*working_interest,1)

    sql_select = 'SELECT IFNULL(MAX(period),{}), IFNULL(production_count,0) FROM wells WHERE datatype LIKE "Wells Drilling & Completion%" AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    drill_comp_days = float(curr.fetchone()[1])

    sql_select = 'SELECT IFNULL(well_life,0), IFNULL(rig_mobilization_days,0) FROM param_track WHERE asset_id={} AND session_key LIKE "%{}%"'.format(asset_id,run_id)
    curr.execute(sql_select)
    well_life, rig_mobile_days = curr.fetchone()
    drill_comp_days += rig_mobile_days

    sql_select = 'SELECT IFNULL(MAX(period),{}) FROM uncon_production WHERE rigs > 0 AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    last_rig_year = int(curr.fetchone()[0])

    sql_select = 'SELECT IFNULL(SUM(type_wells_added),0) FROM uncon_production WHERE period >= {} AND rigs > 0 AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    new_wells_rem = round(float(curr.fetchone()[0])*working_interest,0)

    sql_select = 'SELECT IFNULL(type_wells_added,0) FROM uncon_production WHERE period={} AND asset_id={}'.format(discount_year, asset_id)
    curr.execute(sql_select)
    new_wells = round(float(curr.fetchone()[0])*working_interest,0)

    uncon_data = (rig_count, last_rig_year, well_life, new_wells, new_wells_rem, drill_comp_days)
    return uncon_data

def update_uncon_data(curr):
    print 'Updating uncon data ...'
    run_id = get_run_id(curr)
    curr.execute('UPDATE econ_data SET position=NULL')
    commit(curr)
    sql_select = 'SELECT asset_name FROM econ_data WHERE fiscal_model LIKE "%Resource%"'
    curr.execute(sql_select)
    uncon_asset_names = [data[0] for data in curr.fetchall()]
    for asset_name in uncon_asset_names:
        if '(' in asset_name:
            position = asset_name.split('(')[0].strip()
            sql_update = 'UPDATE econ_data SET position="{}" WHERE asset_name="{}" AND fiscal_model LIKE "%Resource%"'
            curr.execute(sql_update.format(position, asset_name))
            commit(curr)
    sql_select = 'SELECT DISTINCT asset_id FROM econ_data WHERE run_id="{}" AND fiscal_model LIKE "%Resource%"'.format(run_id)
    curr.execute(sql_select)
    uncon_assets = [int(data[0]) for data in curr.fetchall()]
    sql_update  = 'UPDATE econ_data SET rig_count=%s, last_rig_year=%s, well_life=%s, new_wells=%s, new_wells_rem=%s, drill_comp_days=%s '
    sql_update += 'WHERE asset_id=%s AND run_id=%s '
    for asset_id in uncon_assets:
        rig_count, last_rig_year, well_life, new_wells, new_wells_rem, drill_comp_days = get_uncon_data(curr, asset_id, run_id)
        param_vals = (rig_count, last_rig_year, round(float(well_life),1), new_wells, new_wells_rem, round(float(drill_comp_days),1), asset_id, run_id)
        curr.execute(sql_update,param_vals)
        commit(curr)
    print 'Uncon data update complete\n'

def update_operators(curr):
    print 'Updating operators ...'
    curr.execute('USE globaldata')
    curr.execute('TRUNCATE TABLE operators')
    # sql_update = 'INSERT INTO operators (asset_id, operator) SELECT eq_max.ast_id, eq.operator FROM equity AS eq,   '
    # sql_update += '(SELECT asset_id as ast_id, MAX(equity_date) AS max_date FROM equity GROUP BY asset_id) AS eq_max '
    # sql_update += 'WHERE eq.asset_id = eq_max.ast_id AND eq.equity_date = eq_max.max_date GROUP BY eq_max.ast_id    ;'
    #Updated above query to correct the syntax ( done on 16th Sep 2025 )
    # sql_update = ' INSERT INTO operators (asset_id, operator) SELECT eq.asset_id, eq.operator FROM equity AS eq '
    # sql_update += 'JOIN ( SELECT asset_id, MAX(equity_date) AS max_date FROM equity GROUP BY asset_id) AS eq_max '
    # sql_update += 'ON eq.asset_id = eq_max.asset_id AND eq.equity_date = eq_max.max_date;'
    # Updated above query to correct the syntax ( done on 09th Feb 2026 )
    sql_update ='''INSERT INTO operators (asset_id, operator) 
                      SELECT asset_id, operator
                    FROM (
                        SELECT asset_id, operator,
                               ROW_NUMBER() OVER (PARTITION BY asset_id ORDER BY equity_date DESC) as rn
                        FROM equity
                    ) as ranked_equity
                    WHERE rn = 1;'''
    curr.execute(sql_update)
    curr.execute('COMMIT')
    print 'Operator update complete\n'

def update_parent_company(curr):
    print 'Updating parent company data ...'
    run_id = get_run_id(curr)
    #_______________________________________________New Code ( implemented on 30-10-2025 by Sunil and Manognya ____________________________
    try:
        curr.execute("ALTER TABLE equity DROP INDEX idx_equity_asset_date;")
        conn.commit()
    except:
        pass
    try:
        curr.execute("ALTER TABLE equity DROP INDEX idx_equity_asset_pct;")
        conn.commit()
    except:
        pass
    try:
        curr.execute("ALTER TABLE econ_data drop index idx_econ_data_asset_run;")
        conn.commit()
    except:
        pass
    try:
        curr.execute('CREATE INDEX idx_equity_asset_date ON equity (asset_id, equity_date);')
        conn.commit()
    except:
        pass
    try:
        curr.execute('CREATE INDEX idx_equity_asset_pct ON equity (asset_id, equity_pct);')
        conn.commit()
    except:
        pass
    try:
        curr.execute('CREATE INDEX idx_econ_data_asset_run ON econ_data (asset_id, run_id(50));')
        conn.commit()
    except:
        pass

    sql_update = """
    WITH ranked_equity AS (
        SELECT 
            e.asset_id,
            e.top_parent_company,
            e.equity_date,
            e.equity_pct,
            ROW_NUMBER() OVER (
                PARTITION BY e.asset_id 
                ORDER BY e.equity_date DESC, e.equity_pct DESC
            ) AS rn,
            COUNT(*) OVER (
                PARTITION BY e.asset_id, e.equity_date, e.equity_pct
            ) AS dup_count
        FROM equity e
    ),
    latest_equity AS (
        SELECT 
            r.asset_id,
            CASE 
                WHEN r.dup_count > 1 THEN o.operator
                ELSE r.top_parent_company
            END AS parent_company
        FROM ranked_equity r
        LEFT JOIN operators o 
            ON r.asset_id = o.asset_id
        WHERE r.rn = 1
    )
    UPDATE econ_data AS ed
    JOIN latest_equity AS le
        ON ed.asset_id = le.asset_id
    SET ed.parent_company = le.parent_company
    WHERE ed.run_id = %s;
    """

    curr.execute(sql_update, (run_id,))
    conn.commit()
    print 'Parent Company Update Completed..'
    #__________________________________________Old Code_______________________________________________________________________________________
    # sql_select = \
    # '''
    # SELECT top_parent_company FROM equity
    # WHERE asset_id={0} AND
	#       equity_pct=(SELECT MAX(equity_pct) FROM equity
    #                   WHERE equity_date=(SELECT MAX(equity_date) FROM equity WHERE asset_id={0}) AND
    #                         asset_id={0}) AND
    #       equity_date=(SELECT MAX(equity_date) FROM equity WHERE asset_id={0});
    # '''
    # sql_update = 'UPDATE econ_data SET parent_company=%s WHERE asset_id=%s AND run_id=%s'
    # for asset_id in asset_ids:
    #     parent_company = ''
    #     curr.execute(sql_select.format(asset_id))
    #     top_parent_companies = curr.fetchall()
    #     if len(top_parent_companies) == 1:
    #         parent_company = top_parent_companies[0]
    #     else:
    #         parent_company = get_param('operator', 'operators', sql_where='asset_id={}'.format(asset_id))
    #     curr.execute(sql_update, (parent_company, asset_id, run_id))
    #     commit(curr)
    #______________________________________________________________________________________________________________________________________
def update_asset_data(curr):
    run_id = get_run_id(curr)
    #___________________________________New Code (implemented on @30-10-2025_______________________________
    print 'Updating asset data ...'
    print("\nStarting econ_data update in batches...\n")

    # Drop & recreate staging table
    try:
        curr.execute("DROP TABLE IF EXISTS latest_param_track_stage;")
        conn.commit()
    except:
        pass

    # Create staging table
    curr.execute("""
    CREATE TABLE latest_param_track_stage AS
    SELECT
        a.asset_id,
        a.fiscal_regime_chosen,
        a.peak_commodity,
        a.peak_year,
        a.peak_prod,
        a.peak_prod_unit,
        a.cutoff_year,
        a.first_production,
        a.condensate_benchmark,
        a.crude_benchmark,
        a.ng_benchmark,
        a.lng_benchmark,
        a.ngls_benchmark,
        a.session_key
    FROM param_track a
    JOIN (
        SELECT
            asset_id,
            MAX(SUBSTR(session_key, LENGTH(session_key) - 20, 15)) AS run_id
        FROM param_track
        GROUP BY asset_id
    ) b
      ON a.asset_id = b.asset_id
     AND a.session_key LIKE CONCAT('%', b.run_id, '%');
    """)
    conn.commit()
    curr.execute("delete from latest_param_track_stage where session_key not like CONCAT('%%', %s, '%%');", (run_id,))
    conn.commit()
    print("Created latest_param_track_stage table.")
    curr.execute("CREATE INDEX idx_assetid_stage ON latest_param_track_stage(asset_id);")
    conn.commit()

    print("Using run_id: %s\n" % run_id)

    # Determine batching range
    curr.execute("SELECT MIN(asset_id), MAX(asset_id) FROM econ_data WHERE run_id = %s", (run_id,))
    result = curr.fetchone()
    if not result or result[0] is None:
        print("No matching econ_data rows found for run_id.")
        conn.close()
        raise SystemExit

    min_id, max_id = result
    batch_size = 5000
    current_start = min_id

    # Update query for MySQL
    update_query = """
    UPDATE econ_data E
    JOIN operators O ON E.asset_id = O.asset_id
    JOIN assets A ON E.asset_id = A.asset_id
    JOIN latest_param_track_stage P ON E.asset_id = P.asset_id
    SET
        E.asset_name       = A.asset_name,
        E.country          = A.country,
        E.constituent      = A.constituent,
        E.formation        = A.formation,
        E.region           = A.region,
        E.status           = A.status,
        E.resource_type    = A.resource_type,
        E.operator         = O.operator,
        E.terrain          = A.terrain,
        E.facility_type    = A.facility_type,
        E.basin            = A.basin,
        E.first_production = P.first_production,
        E.peak_comm        = P.peak_commodity,
        E.peak_year        = P.peak_year,
        E.peak_prod        = P.peak_prod,
        E.peak_prod_unit   = P.peak_prod_unit,
        E.cutoff_year      = P.cutoff_year,
        E.parent_company   = O.operator,
        E.crude_bm         = P.crude_benchmark,
        E.ng_bm            = P.ng_benchmark,
        E.lng_bm           = P.lng_benchmark,
        E.ngls_bm          = P.ngls_benchmark,
        E.condensate_bm    = P.condensate_benchmark,
        E.fiscal_model     = P.fiscal_regime_chosen,
        E.data_source      = A.data_source
    WHERE E.run_id = %s

      AND E.asset_id BETWEEN %s AND %s;
    """
    #
    print("Running batched updates...\n")

    while current_start <= max_id:
        batch_end = min(current_start + batch_size - 1, max_id)
        start_time = time.time()
        curr.execute(update_query, (run_id, current_start, batch_end))
        conn.commit()
        current_start = batch_end + 1

    # print("\nAll batches processed. Total rows updated: %d" % total_updated)
    # print("\nUpdate completed.\n")
    #---------------------------------------------------------Old Code-----------------------------------------------------------------------
    #Old Update Query
    # sql_update  = 'UPDATE econ_data AS E, operators AS O, assets AS A, '
    # sql_update += '(SELECT a.asset_id, a.fiscal_regime_chosen, a.peak_commodity, a.peak_year, a.peak_prod, a.peak_prod_unit, a.cutoff_year,  a.first_production,  a.condensate_benchmark, a.crude_benchmark, a.ng_benchmark, a.lng_benchmark, a.ngls_benchmark, a.session_key '
    # sql_update += 'FROM param_track AS a, (SELECT asset_id AS assetid, MAX(SUBSTR(session_key,LENGTH(session_key)-20,15)) AS run_id FROM param_track GROUP BY asset_id) AS b WHERE a.asset_id=b.assetid AND a.session_key LIKE CONCAT("%",b.run_id,"%")) AS P '
    # sql_update += 'SET E.asset_name=A.asset_name, E.country=A.country, E.constituent=A.constituent, E.formation=A.formation, E.region=A.region, E.status=A.status, E.resource_type=A.resource_type, E.operator=O.operator, E.terrain=A.terrain, E.facility_type=A.facility_type, '
    # sql_update += 'E.basin=A.basin, E.first_production=P.first_production, E.peak_comm=P.peak_commodity, E.peak_year=P.peak_year, E.peak_prod=P.peak_prod, E.peak_prod_unit=P.peak_prod_unit, E.cutoff_year=P.cutoff_year, E.parent_company=O.operator, '
    # sql_update += 'E.crude_bm=P.crude_benchmark, E.ng_bm=P.ng_benchmark, E.lng_bm=P.lng_benchmark, E.ngls_bm=P.ngls_benchmark, E.condensate_bm=P.condensate_benchmark, E.fiscal_model=P.fiscal_regime_chosen, E.data_source=A.data_source '
    # sql_update += 'WHERE E.asset_id=O.asset_id AND E.asset_id=A.asset_id AND E.asset_id=P.asset_id '
    # #sql_update += 'AND P.session_key LIKE CONCAT("%", E.run_id, "%") '
    # sql_update += 'AND E.run_id=(SELECT run_id FROM global_variables WHERE id=1)'
    # curr.execute(sql_update)
    # curr.execute('COMMIT')
    #____________________________________________________________________________________________________________________________________
    curr.execute('UPDATE econ_data SET formation="Bourgan 'B';Dictioconous;Nahr Umr;Yamama" WHERE asset_id=129943')
    curr.execute('COMMIT')
    curr.execute("UPDATE econ_data SET operator=NULL WHERE operator=''")
    curr.execute('COMMIT')
    curr.execute("UPDATE econ_data SET operator='Ukrgazvydobuvannya' WHERE operator='Ukrgazvydobuvannya""'")
    curr.execute('COMMIT')
    sql_update_2 = \
    '''
    UPDATE econ_data AS a, projects_extract AS b
      SET a.project_name=b.project_name, a.project_active_year=b.project_active_year, a.project_stage=b.project_stage, a.stage_change_quarter=b.stage_change_quarter, a.epc_contractor=b.epc_contractor, a.fid=b.fid
      WHERE a.asset_id=b.asset_id AND a.run_id="{}"
    '''
    curr.execute(sql_update_2.format(run_id))
    curr.execute('COMMIT')

    update_parent_company(curr)
    print 'Asset data update complete'

def update_benchmarks(curr):
    print 'Updating benchmarks ...'
    benchmarks = ("crude_bm", "ng_bm", "condensate_bm", "lng_bm", "ngls_bm")
    for benchmark in benchmarks:
        print 'Updating ' + benchmark + ' ...'
        sql_update = 'CALL updateBM(%s)'
        curr.execute(sql_update, (benchmark,))
        print benchmark + ' update complete'
    print '\tBenchmark update complete\n'

def update_reserve_volume(curr):
    sql_query = ''
    """
    SELECT eq_max.ast_id, eq.operator FROM equity AS eq,
	(SELECT asset_id as ast_id, MAX(equity_date) AS max_date FROM equity GROUP BY asset_id) AS eq_max
	WHERE eq.asset_id = eq_max.ast_id AND eq.equity_date = eq_max.max_date GROUP BY eq_max.ast_id;
    """
    return None

def update_econ_data(curr, operators=True, asset_data=True, xl_macro=True, benchmarks=True, uncon=True, regions=None):
    print 'Updating econ data ...\n'
    if operators: update_operators(curr)
    if asset_data: update_asset_data(curr)
    if xl_macro: breakeven_process('full econ', regions)
    if benchmarks: update_benchmarks(curr)
    if uncon: update_uncon_data(curr)
    curr.execute('COMMIT')
    
    print 'Econ data update complete'


# Function used with engine tasks ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_session_key(curr, mode, session_code):
    session_key = ""
    if mode == 'start':
        randnum = randint(1000, 9999)
        if session_code in ['Run', 'DataImport', 'CreateModel', 'Breakeven', 'GenerateReports', 'EconError']:
            time_string = get_datetime()
            time_string = '_'.join(''.join(''.join(time_string.split('-')).split(':')).split(' '))
            session_key = time_string + '_' + str(randnum)
        else:
            session_key = get_run_id(curr) + '_' + str(randnum)
    if mode == 'end':
        session_key_file = open(TEMP_LOG_DIR + session_code + '_session_key.txt')
        session_key = session_key_file.readline()
        session_key_file.close()
        if session_code != 'Run':
            os.remove(TEMP_LOG_DIR + session_code + '_session_key.txt')
    return session_key

def temp_log(curr, process_name, check_set, complete_task, copy=False):
    time = get_datetime()
    task_name = argumentList[2]
    try:
        logfile = open(TEMP_LOG_DIR + process_name + '_log.txt', 'a')
    except:
        logfile = open(TEMP_LOG_DIR + process_name + '_log.txt', 'w')
    logfile.write(task_name + ": " + str(time)[:19] + "\n")
    logfile.close()
    check_log(curr, process_name, check_set, complete_task, copy)

def check_log(curr, process_name, check_set, complete_task, copy=False):
    # Create set of completed task names
    logfile = open(TEMP_LOG_DIR + process_name + '_log.txt')
    lines = [line for line in logfile.readlines() if line != '\n']
    task_names = {line.split(':')[0] for line in lines}
    logfile.close()
    # Check set of completed task names against standard set
    if task_names == check_set:
        try:
            updateLog(curr, 'e', process_name)        # Breakeven
        except:
            pass
        # Run complete-task to trigger next task in scheduler and remove process log file
        run_task(complete_task, ENGN_TASK_DIR + complete_task + '.bat')      # C:\GlobalData\Tasks\6_BreakevenComplete.bat
        os.remove(TEMP_LOG_DIR + process_name + '_log.txt')
        # Copy models to breakeven directory after CreateModel process
        if copy:
            copy_models(BE_REGIONS)
        sys.exit(0)
    else:
        sys.exit(1)

def update_run_id(curr, run_id=None):
    session_key = '%s_%s' % ('Run', get_session_key(curr, 'start', 'Run'))
    if run_id:
        session_key = session_key[:4]+run_id+session_key[19:]
    else:
        run_id = session_key[4:19]
    sql_update = "UPDATE global_variables SET run_id='%s' WHERE id=1 " % run_id
    print sql_update
    curr.execute(sql_update)
    commit(curr)
    session_key_file = open(TEMP_LOG_DIR + 'Run_session_key.txt', 'w')
    session_key_file.write(session_key)
    session_key_file.close()

def updateLog(curr, mode_option='e', session_code='log', process_message=''):
    # Get current time and open connection with database
    process_time = get_datetime()
    # If start of process then get session key, create entry for process in database and save session key file in temp folder
    if mode_option.lower() == 's':
        session_key = session_code + '_' + get_session_key(curr, 'start', session_code)
        # save run ID in global_variables table
        if session_code == 'Run':
            SQLstr = "UPDATE global_variables SET run_id='" + session_key[4:19] + "' WHERE id=1;"
            curr.execute(SQLstr)
        process_key = session_key[:-5]
        curr.execute("DELETE FROM command_line_log WHERE session_key LIKE '%s%%'" % process_key)
        curr.execute('COMMIT')
        SQLstr = "INSERT INTO command_line_log (session_key, start_time, message) VALUES ('" + session_key + "', '" + process_time + "', '" + process_message + "')"
        session_key_file = open(TEMP_LOG_DIR + session_code + '_session_key.txt', 'w')
        session_key_file.write(session_key)
        session_key_file.close()
    elif mode_option.lower() == 'e':
        session_key = get_session_key(curr, 'end', session_code)
        curr.execute("SELECT start_time FROM command_line_log WHERE session_key='"+session_key+"'")
        start_time = str(curr.fetchone()[0])
        #print "Start_time:", start_time
        end_time = process_time
        end_time = str(end_time)
        exit_status = os.system('ECHO %ERRORLEVEL%')
        SQLstr = "UPDATE command_line_log SET end_time='" + process_time + "', exit_status=" + str(exit_status) + \
                 ", total_time='" + elapsed_time(start_time, end_time) + "' WHERE session_key='" + session_key + "'"
    else:
        print 'Invalid options provided'
        sys.exit(1)
    curr.execute(SQLstr)
    curr.execute('COMMIT')

def copy_models(regions_dir, region_folder=None, model_dir=REGIONS_DIR):
    if region_folder:
        regions_list = [region_folder]
    else:
        regions_list = os.listdir(model_dir)
    if not os.path.exists(regions_dir):
        os.mkdir(regions_dir)
    for region in regions_list:
        if not os.path.exists(regions_dir + region + "\\"):
            os.mkdir(regions_dir + region + "\\")
        if os.listdir(regions_dir + region + "\\"):
            for model in [mod for mod in os.listdir(regions_dir + region + "\\") if mod[0] != "~" and mod[:8] == "MODELLED"]:
                os.remove(regions_dir + region + "\\" + model)
        for model in [mod for mod in os.listdir(model_dir + region + "\\") if mod[0] != "~" and mod[:8] == "MODELLED"]:
            model_fpath = region + "\\" + model
            shutil.copy2(model_dir + model_fpath, regions_dir + model_fpath)

def check_process(curr, region_name=None, region_code=None, process_name=None, outfile_name=None, file_ext=None, task_dir=None, check_set=None, complete_task=None, copy=False, engine_model_dir=REGIONS_DIR, macro_model_dir=BE_REGIONS):
    '''
    region_name     --> "Former Soviet Union"
    region_code     --> Former_Soviet_Union
    process_name    --> 'Breakeven'
    outfile_name    --> BREAKEVEN_DIR + 'Breakeven_' + region_code --> C:\GlobalData\Macros\BreakevenMacros\Breakeven_Former_Soviet_Union
    file_ext        --> .xlsm
    task_dir        --> C:\GlobalData\Tasks\BreakevenTasks\
    check_set       --> {'Africa', 'Asia', 'Caribbean', 'Central_America', 'Europe', 'Former_Soviet_Union', 'Middle_East', 'North_America_1', 'North_America_2','Oceania', 'South_America', 'Unconventional'}
    complete_task   --> '6_BreakevenComplete'
    '''
    process_complete = False
    if 'DiscFieldMacro' in process_name and region_code == 'Central_America':
        # updateLog(curr, 'e', process_name + '_' + region_code)
        process_complete = de.check_process(process_name)
    else:
        sleep(10)
        processed = []
        be_log = ''
        region_dir = macro_model_dir + region_name + '\\'
        be_log += 'region_dir: %s\n' % region_dir

        # Determine total number of models by counting models in region folder
        model_count = len([model for model in os.listdir(engine_model_dir + region_name + '\\') if model[0] != "~" and model[:8] == 'MODELLED'])
        be_log += 'model_count: %s\n' % model_count

        # Count number of models in breakeven region folder
        models = [model for model in os.listdir(region_dir) if model[:8] == 'MODELLED' and '~$'+model not in os.listdir(region_dir)]
        model_times = [(model, last_mod_time(region_dir + model)) for model in models]
        be_log += 'model times: %s\n' % ','.join([str(model_time) for model_time in model_times])

        # Count number of models in breakeven region folder that have already completed breakeven process
        completed = [model for model in models if last_mod_time(region_dir + model) >= last_mod_time(region_dir + models[0]) and model[0] != "~" and ("~$" + model not in models)]
        be_log += 'models[0]: %s\n' % models[0]
        be_log += 'last_mod_time(region_dir + models[0]): %s\n' % last_mod_time(region_dir + models[0])
        be_log += 'completed: %s\n' % '\n'.join(['%s: %s' % (last_mod_time(region_dir + model), model) for model in completed])

        # If a temp folder exists and contains models then add number of models in temp folder to completed count to get processed count
        if os.path.exists(region_dir + 'Temp\\') and [mod for mod in os.listdir(region_dir + 'Temp\\') if mod[0] != "~" and mod[:8] == "MODELLED"]:
            processed = [model for model in os.listdir(region_dir + 'Temp\\') if model[:8] == 'MODELLED']
            processed += completed
        else:
            processed = completed

        # If processed count is less than total number of models move completed to temp folder and run breakeven process on rest
        if (model_count - len(processed) > 1)  and model_count > 0:
            print process_name + " Incomplete"
            if not os.path.exists(region_dir + 'Temp\\'):
                os.mkdir(region_dir + 'Temp\\')
            if completed:
                for model in completed:
                    try:
                        shutil.move(region_dir + model, region_dir + 'Temp\\' + model)
                        print model
                        be_log += '%s moved\n' % model
                    except:
                        print "Cannot move " + model + " to temp folder"
                        be_log += '%s not moved\n' % model

                # Save copy of breakeven macro to preserve breakeven output for completed models
                new_macro_name = outfile_name + '_' + str(randint(1000, 9999)) + file_ext
                shutil.copy2(outfile_name + file_ext, new_macro_name)
                be_log += 'new_macro_name: %s\n' % new_macro_name
                triggered_task = task_dir + process_name + '_' + region_code
                be_log += 'triggered_task: %s\n' % triggered_task
                with open(TASK_DIR + 'tasklog\\' + new_macro_name.split('\\')[-1][:-5] + '.txt', 'w') as f:
                    f.write(be_log)
                os.system(triggered_task)      # C:\GlobalData\Tasks\BreakevenTasks\Breakeven_Africa
            else:
                sys.exit(1)
        else:
            # If a temp folder exists and contains models then move the models back to the breakeven region folder and delete the temp folder
            if os.path.exists(region_dir + 'Temp\\') and [mod for mod in os.listdir(region_dir + 'Temp\\') if mod[0] != "~" and mod[:8] == "MODELLED"]:
                for model in [mod for mod in os.listdir(region_dir + 'Temp\\') if mod[0] != "~" and mod[:8] == "MODELLED"]:
                    try:
                        shutil.move(region_dir + 'Temp\\' + model, region_dir + model)
                    except:
                        print "Cannot move " + model + " from temp folder"
                os.rmdir(region_dir + 'Temp\\')
            print process_name + ' ' + region_code + ' Complete'

            # Update command_line_log to complete breakeven entry for given region
            updateLog(curr, 'e', process_name + '_' + region_code)        # Breakeven_Africa
            if 'DiscFieldMacro' in process_name:
                process_complete = de.check_process(process_name)
            else:
                # Add breakeven task name to log file and check if all tasks have been completed
                temp_log(curr, process_name, check_set, complete_task, copy)
                sys.exit(0)
    return process_complete

# Functions used in engine prep -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def clear_region_folders():
    region_dirs = [REGIONS_DIR, BE_REGIONS, DF_REGION_DIR, DF_REGIONS]  #--Uncomment after Debug
    # region_dirs = [REGIONS_DIR,DF_REGION_DIR, DF_REGIONS] #-- Comment after Debug
    for region_dir in region_dirs:
        print 'Clearing files from %s ...' % region_dir
        for region in os.listdir(region_dir):
            if os.listdir(region_dir + region + "\\"):
                for model in [mod for mod in os.listdir(region_dir + region + "\\") if mod[-5:] == '.xlsx' and mod[0] != '~']:
                    os.remove(region_dir + region + "\\" + model)

def clear_temp_folder(keepRunID=False):
    print 'Clearing temp files ...'
    for tempfile in os.listdir(TEMP_LOG_DIR):
        if keepRunID and tempfile[:3] == "Run":
            continue
        else:
            os.remove(TEMP_LOG_DIR + tempfile)

def archive_files(reports=True, data=True, output=True, run_date=None):
    if reports:
        print 'Archiving reports ...'
        for reportfile in [fname for fname in os.listdir(REPORTS_DIR) if fname[-4:-1] == 'xls']:
            if not os.path.exists(REPORTS_DIR + "Archive\\"):
                os.mkdir(REPORTS_DIR + "Archive\\")
            shutil.move(REPORTS_DIR + reportfile, REPORTS_DIR + "Archive\\" + reportfile)
    if output:
        print 'Archiving output files ...'
        for outputfile in [fname for fname in os.listdir(ENGINE_DIR + "Output\\") if fname[-3:] == 'txt' or fname[-4:-1] == 'xls']:
            if not os.path.exists(ENGINE_DIR + "Output\\" + "Archive\\"):
                os.mkdir(ENGINE_DIR + "Output\\" + "Archive\\")
            shutil.move(ENGINE_DIR + "Output\\" + outputfile, ENGINE_DIR + "Output\\" + "Archive\\" + outputfile)

def breakeven_config(setting, scenario_num='', region_num=''):
    print 'Configuring breakeven macros ...'
    config = {
     'Calculate Breakevens': {        'cell': 'E10',
                                   'full be': True,
                                   'base be': True,
                                    'engine': True,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': True,
                               'disc fields': True},

      'Calculate Base Case': {        'cell': 'E11',
                                   'full be': True,
                                   'base be': True,
                                    'engine': True,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': True,
                               'disc fields': True},

      'Calculate High Case': {        'cell': 'E12',
                                   'full be': True,
                                   'base be': False,
                                    'engine': True,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': True,
                               'disc fields': False},

       'Calculate Low Case': {        'cell': 'E13',
                                   'full be': True,
                                   'base be': False,
                                    'engine': True,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': True,
                               'disc fields': False},

         'Update Econ Data': {        'cell': 'E15',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': True,
                                 'full econ': True,
                                     'uncon': True,
                               'disc fields': True},

          'Update All Econ': {        'cell': 'E16',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': True,
                                     'uncon': False,
                               'disc fields': False},

    'Connected to Database': {        'cell': 'E18',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': True,
                                 'full econ': True,
                                     'uncon': False,
                               'disc fields': True},

           'Unconventional': {        'cell': 'E19',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': True,
                               'disc fields': False},

          'New Uncon Model': {'cell'       : 'F19',
                               'full be'    : False,
                               'base be'    : False,
                               'engine'     : False,
                               'econ report': False,
                               'full econ'  : False,
                               'uncon'      : True,
                               'disc fields': False},

       'Calculate Min Econ': {       'cell': 'E21',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': False,
                               'disc fields': True},

        'Calculate Max Dev': {       'cell': 'E22',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': False,
                               'disc fields': True},

        'Update Asset Data': {       'cell': 'E23',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': False,
                               'disc fields': True},

          'Remove Formulas': {        'cell': 'E24',
                                   'full be': True,
                                   'base be': True,
                                    'engine': True,
                               'econ report': True,
                                 'full econ': True,
                                     'uncon': True,
                               'disc fields': True},

            'Set comms = 0': {            'cell': 'E25',
                                   'full be': False,
                                   'base be': False,
                                    'engine': False,
                               'econ report': False,
                                 'full econ': False,
                                     'uncon': False,
                               'disc fields': True},

             'Scenario Num': {        'cell': 'C2',
                                   'full be': scenario_num,
                                   'base be': scenario_num,
                                    'engine': scenario_num,
                               'econ report': scenario_num,
                                 'full econ': scenario_num,
                                     'uncon': scenario_num,
                               'disc fields': scenario_num},

               'Region Num': {        'cell': 'C4',
                                   'full be': region_num,
                                   'base be': region_num,
                                    'engine': region_num,
                               'econ report': region_num,
                                 'full econ': region_num,
                                     'uncon': region_num,
                               'disc fields': region_num}
    }

    macro_dir = BREAKEVEN_DIR
    if setting == 'full econ':
        macro_dir = ECON_MACRO_DIR
    elif setting == 'disc fields':
        macro_dir = DISC_FIELD_DIR
    elif scenario_num:
        macro_dir = SCENARIO_DIR+'scenario_{}\\'.format(scenario_num)
    for macro_filename in [file for file in os.listdir(macro_dir) if file[-4:] == 'xlsm' and file[:9] in ['Breakeven', 'EconData_', 'DiscField']]:
        wb = openpyxl.load_workbook(macro_dir + macro_filename, read_only=False, keep_vba=True)
        try:
            ws = wb['Sheet1']
        except:
            ws = wb.get_sheet_by_name('Sheet1')
        for option in config.keys():
            if option.lower() in ['unconventional', 'new uncon model'] and macro_filename.lower()[:24] == 'breakeven_unconventional':
                ws[config[option]['cell']].value = str(config[option]['uncon']).upper()
            else:
                ws[config[option]['cell']].value = str(config[option][setting]).upper()
        wb.save(macro_dir + macro_filename)


# Functions used by task_scheduler.py ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def list_days(days_of_week):
    day_list = ""
    day_names = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    for i in range(7):
        if days_of_week[i]:
            day_list += day_names + ","
    if day_list:
        day_list = day_list[:-1]
    return day_list

def generateXML(task_name, trigger_task, batch_file):
    xml_query = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2017-01-23T23:35:04.0859557</Date>
    <Author>%s</Author>
    <URI>\%s</URI>
  </RegistrationInfo>
  <Triggers>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="Microsoft-Windows-TaskScheduler/Operational"&gt;&lt;Select Path="Microsoft-Windows-TaskScheduler/Operational"&gt;*[EventData[@Name='TaskSuccessEvent']
      [Data[@Name='TaskName']='\%s']]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
    </EventTrigger>
  </Triggers>
    <Principals>
    <Principal id="Author">
      <UserId>%s</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>%s</Command>
    </Exec>
  </Actions>
</Task>""" % (AUTHOR, task_name, trigger_task, USER_ID, batch_file)
    with open(XML_TASK_DIR + task_name + '.xml', 'w') as f:
        f.write(xml_query)

def create_triggered_task(task_name, trigger_task, batch_file):
    generateXML(task_name, trigger_task, batch_file)
    xml_path = XML_TASK_DIR + task_name + '.xml'
    task_command = 'schtasks /Create /F /XML "' + xml_path + '" /TN ' + task_name
    os.system(task_command)

def create_scheduled_task(task_name, schedule, start_time, task_run, month=None, day=None, recurring=None, days_of_week=None):
    task_command = 'schtasks /Create /F /SC ' + schedule + ' /TN ' + task_name + ' /TR "' + task_run + '" /ST ' + start_time
    if schedule == 'Weekly':
        day_list = list_days(days_of_week)
        task_command += ' /D ' + day_list
    print task_command
    os.system(task_command)

def run_task(task_name, batch_file=''):
    try:
        os.system('schtasks /RUN /TN ' + task_name)
    except:
        create_scheduled_task(task_name, 'ONCE', '00:01', batch_file)
        os.system('schtasks /RUN /TN ' + task_name)

def delete_task(task_name):
    os.system('schtasks /DELETE /F /TN ' + task_name)

def delete_all_tasks(task_list):
    for task in task_list:
        delete_task(task)


# Functions for running excel macros ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def run_macro(macro_dir, macro_file, macro_name):
    xlApp = win32com.client.Dispatch("Excel.Application")
    wb = xlApp.Workbooks.Open(Filename=macro_dir + macro_file)
    xlApp.Application.Run(macro_file + "!" + macro_name)
    wb.SaveAs(macro_dir + macro_file)
    xlApp.Application.Quit()
    del xlApp

def breakeven_macro(region=None):
    if region:
        region_name = region
    else:
        region_name = argumentList[1]
    macro_dir = BREAKEVEN_DIR
    macro_file = "Breakeven_" + region_name + ".xlsm"
    macro_name = "Module1.ProcessFolderBreakevens"
    run_macro(macro_dir, macro_file, macro_name)

def report_macro():
    macro_dir = MACRO_DIR
    macro_file = "ReportsMacro.xlsm"
    macro_name = argumentList[1]
    run_macro(macro_dir, macro_file, macro_name)

def run_breakevens(regions=None):
    if regions:
        region_list = regions
    else:
        region_list = CHECK_REGION_SET
    for region in region_list: breakeven_macro(region)

def breakeven_process(setting, regions=None):
    breakeven_config(setting)
    run_breakevens(regions)


# Functions imported from engine code ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def dataImport(curr):
    region = ""
    options = list(argumentList[1][1:])
    
    mainProgram = NewMenuDemo(autorun=1)
    initVariables(mainProgram, options)
    try:
        region = argumentList[2][1:]
        if argumentList[2][0] == '!':
            mainProgram.importProduction(mainProgram.curr, region, mainProgram.mDataDir.get(), "", split=True, clear_db=True)
        else:
            mainProgram.importProduction(mainProgram.curr, region, mainProgram.mDataDir.get(), "", split=True)
    except:
        updateLog(curr, 's', 'DataImport', 'Data Import Process')
        mainProgram.importAll()
        updateLog(curr, 'e', 'DataImport')

def createModel(debug=True):
    options = argumentList[1][1:]
    mainProgram = NewMenuDemo(autorun=1)
    initVariables(mainProgram, options)
    mainProgram.BatchAssetCurve2()


# Functions used with specific commands -------------------------------------------------------------------------------------------------------------------------------------------------------------------

def change_drive(new_drive_letter, task_folder=TASK_DIR+'TitanTasks\\'):
    for batch_file in [bfile for bfile in os.listdir(task_folder) if bfile[0] != '~' and bfile[-4:] in ['.cmd', '.bat']]:
        with open(task_folder + batch_file, 'r+') as f:
            new_text = ""
            lines = f.readlines()
            for line in lines:
                if line[:10] == 'SET drive=':
                    line = line[:10] + new_drive_letter + '\n'
                print line
                new_text += line
            f.seek(0)
            f.write(new_text)
            f.truncate()

def convert_dates(old_date, new_date):
    print 'Converting dates ...'
    for datafile in [dfile for dfile in os.listdir(DATA_DIR) if dfile[:3] == 'GD_']:
        new_filename = ""
        print datafile
        date_indx = datafile.find(old_date)
        if date_indx != -1:
            new_filename += datafile[:date_indx] + new_date + datafile[date_indx+8:]
            print "new_filename:", new_filename
            os.rename(DATA_DIR+datafile, DATA_DIR+new_filename)

def asset_test():
    region_dir = TEST_DIR + "models\\"
    for asset_id, region in KEY_ASSETS:
        print asset_id, region
        asset_file_list = [a_file for a_file in os.listdir(region_dir + region + "\\") if
                           str(asset_id) in a_file]
        if asset_file_list:
            asset_file = asset_file_list[0]
            print "asset_file:", asset_file
            shutil.copy2(region_dir + region + "\\" + asset_file, KEY_ASSET_DIR + asset_file)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    conn = get_connection()
    curr = conn.cursor()
    curr.execute('USE globaldata')

    argumentList = sys.argv[1:]
    # argumentList = ['update_asset_data', 'all']
    # argumentList = ['data_import', '-ps']
    # argumentList = ['data_import', '-sx']
    # argumentList = ['generate_all_panoramas']
    # argumentList = ['split_fiscal', 'update_db', 'NA,EU,FS,SA']
    # argumentList = ['log', '-s' ,'CreateModel_Central_America', 'Create Model Central America']
    # argumentList = ['log', '-s', 'Breakeven_Unconventional', 'Breakeven Unconventional']
    # argumentList = ['run_id']
    # argumentList = ['update_econ_data', '-ab']
    # argumentList = ['create_model', '-stat-nlrb', '-delt-e','-regn-central_america']
    # argumentList = ['process_deals']
    # argumentList = ['update_asset_data', 'all']
    # argumentList = ['process_disc_fields', '-' ,'-clear']
    # argumentList = ['process_disc_fields', '-EU', '-no_analog,calc']
    # argumentList = ['create_model' ,'-regn-disc_asia']
    # argumentList = ['update_asset_data', 'all']
    # argumentList = ['log', '-s', 'CreateModel_Central_America', 'Create Model Central America']
    # argumentList=['create_model', '-stat-nlrb', '-delt-e', '-regn-central_america']
    # argumentList = ['update_econ_data', '-ab']
    # argumentList = ['create_model', '-asid-322260']
    # argumentList = ['generate_all_panoramas']
    # argumentList = ['split_fiscal', 'update_db', 'NA,EU,FS,SA']
    # argumentList = ['create_model', '-deal-', '-asid-737439']
    # argumentList =['check_disc_fields', '-Macro1', '-Asia']
    # argumentList = ['UPDATE_PRICES_DATA']
    command = argumentList[0]
    commandLineMain(argumentList, command, curr)
    curr.close()
    conn.close()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

