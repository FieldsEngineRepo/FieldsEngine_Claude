from time import sleep
from os import listdir
from os.path import isfile, join
from datetime import datetime,date,timedelta
from data_export import update_servers
from globaldata import *


class MiningForecast:
    def __init__(self, mine_list=[], processData=False, forecastData=False, debugAll=False, importTables=False, updateTables=False, updateServer=False):
        self.mine_list                            = mine_list
        self.processData                          = processData
        self.forecastData                         = forecastData
        self.debugAll                             = debugAll
        self.importTables                         = importTables
        self.updateTables                         = updateTables
        self.updateServer                         = updateServer
        # ==========================================================================================================================
        self.removeForecast                       = False
        self.lUpdateRemote                        = False
        self.lCopyDataLocal                       = False
        self.useLocalData                         = True
        self.updateOreGrade                       = False
        self.updateSaleable                       = False
        self.updateFactors                        = False
        self.debugMode                            = False
        self.debugSQL                             = False
        self.debugReserves                        = False
        self.include_T2E                          = True
        self.include_T3E                          = True
        self.ytp_flag                             = True
        # ==========================================================================================================================
        if self.forecastData:
            self.removeForecast                   = True
            self.processData                      = True
            self.lUpdateRemote                    = True
            self.lCopyDataLocal                   = True
            self.useLocalData                     = True
            self.importTables                     = True
            self.updateTables                     = True
            self.mine_list                        = []
        if self.updateTables:
            self.updateOreGrade                   = True
            self.updateSaleable                   = True
            self.updateFactors                    = True
        if self.debugAll:
            self.debugMode                        = True
            self.debugSQL                         = True
            self.debugReserves                    = True
        # ==========================================================================================================================
        self.minimumForecastMax                   = 8
        self.prodDecimals                         = 2
        self.discountYear                         = get_discount_year()
        self.years_to_project                     = 10
        self.pct_of_capacity                      = 0.90
        self.production_tolerance                 = 0.2
        self.last_year_fctr                       = 0.5
        self.ore_cap_to_rom                       = 0.96
        self.reserve_tot_resource                 = 0.80
        self.yearly_effeciency                    = 0.0025
        self.ye_lt5                               = 0.025
        self.ye_lt10                              = 0.0025
        self.ye_lt20                              = 0.00025
        self.yr_range                             = range(1940, 2200)
        self.sale_yield                           = 0.75
        self.resc_to_resv                         = 0.5
        self.meas_to_total                        = 0.5 / self.resc_to_resv
        self.ind_to_total                         = 0.4 / self.resc_to_resv
        self.inf_to_total                         = 0.3 / self.resc_to_resv
        # ==========================================================================================================================
        self.mOutputLogsDir                       = ENGINE_DIR + 'Projects\\Mining\\'
        self.mSession_key                         = create_session_key()
        self.runningTime                          = time.time()
        self.timeStarted                          = datetime.now()
        self.mProgComment                         = 'Mining Models Program Started at: %s\n' % (get_datetime())
        self.mining_section                       = '0.0.0'
        self.ts                                   = time.time()
        self.st                                   = datetime.fromtimestamp(self.ts).strftime('%Y-%m-%d %H:%M:%S')
        self.dt                                   = self.timeStarted.timetuple()
        self.conn                                 = get_connection(server='mysql', database='miningengineextract')
        self.curr                                 = self.conn.cursor()
        # ==========================================================================================================================
        self.mining_categories                    = ['Mine id',
                                                     'Start year',
                                                     'Mine life',
                                                     'Remaining life',
                                                     'Acreage',
                                                     'Reserve type',
                                                     'Reserve year',
                                                     'Reserves',
                                                     'Reserve unit',
                                                     'Capacity type',
                                                     'Capacity year',
                                                     'Capacity',
                                                     'Capacity unit',
                                                     'Production Type',
                                                     'Production Year',
                                                     'Production Value',
                                                     'Production unit',
                                                     'Resource Type',
                                                     'Commodity',
                                                     'Resource Year',
                                                     'Resource %',
                                                     'Resource unit',
                                                     'Production Source',
                                                     'Resource Source',
                                                     'Capacity Source',
                                                     'Reserves Source',
                                                     'Production Source']
        self.MINES                                = {category: [] for category in self.mining_categories}
        # ==========================================================================================================================
        self.mining_data                          = None
        self.mineStage                            = None
        self.startYear                            = None
        self.mineLife                             = None
        self.remainingLife                        = None
        self.acreage                              = None
        self.mineName                             = None
        self.mineCountry                          = None
        self.state                                = None
        self.mineRegion                           = None
        self.commodities                          = None
        self.mineType                             = None
        self.mineMethod                           = None
        self.projectType                          = None
        self.mineSubStage                         = None
        self.mineSubStageStatus                   = None
        self.constructionStartYear                = None
        self.mineEndYear                          = None
        self.mineDepth                            = None
        self.mineLocationSource                   = None
        self.remainingMineLifeYear                = None
        self.originalProductionStartYear          = None
        self.TotalMineLifeSource                  = None
        self.RemainingMineLifeSource              = None
        self.MineEndYearSource                    = None
        self.mineAcreageSource                    = None
        self.ActualProductionStartYearSource      = None
        self.mineStatus                           = None
        self.ActualProductionStartYear            = None
        self.totalMineLife                        = None
        self.remainingMineLife                    = None
        self.MineAcreageHectares                  = None
        # ==========================================================================================================================
        self.APSY                                 = True
        self.MEY                                  = True
        self.TML                                  = True
        self.RML                                  = True
        
        self.RMLY                                 = False
        self.firstType1                           = False
        self.firstType2                           = False
        self.firstType3                           = False
        self.pt_ran                               = False
        self.octr_ran                             = False
        self.rr_ran                               = False

        self.romProductionFound                   = False
        self.productionFound                      = False
        self.metalProductionFound                 = False
        self.oreProductionFound                   = False
        self.overburdenFound                      = False
        self.saleProductionFound                  = False
        self.resourcesFound                       = False
        self.totalResourcesFound                  = False
        self.measResourcesFound                   = False
        self.indResourcesFound                    = False
        self.infResourcesFound                    = False
        self.metalResourcesFound                  = False
        self.capacityFound                        = False
        self.romCapacityFound                     = False
        self.metalCapacityFound                   = False
        self.oreCapacityFound                     = False
        self.saleCapacityFound                    = False
        self.reservesFound                        = False
        self.totalReservesFound                   = False
        self.provReservesFound                    = False
        self.probReservesFound                    = False
        self.metalReservesFound                   = False

        self.generate_history                     = False
        self.generate_forecast                    = False
        self.generated_hist                       = False
        self.generated_FC                         = False
        self.updateQAsite                         = False
        self.thisWasModelled                      = False
        self.createdMetalProduction               = False
        # ==========================================================================================================================
        self.newProd                              = 0
        self.recovery_rate                        = 0
        self.mTotRecs                             = 0
        self.NewMineId                            = 0
        self.Mineid                               = 0
        self.modelled                             = 0
        self.not_modelled                         = 0
        self.recsProcessed                        = 0
        self.maxProduction                        = 0
        self.max_additional_production            = 0
        self.mTotalProduction                     = 0
        self.origCalcMaxProduction                = 0
        self.convertFactor                        = 0
        self.estimated_total_recoverable_reserves = 0
        self.lastYear                             = 0
        self.historical_years                     = 0
        self.forecast_years                       = 0
        self.lastProd                             = 0
        self.resources_to_reserves                = 0
        self.first_reserve_year                   = 0
        self.first_reserve_amt                    = 0
        self.first_capacity_year                  = 0
        self.first_capacity_amt                   = 0
        self.first_ore_cap                        = 0
        self.last_reserve_year                    = 0
        self.last_reserve_amt                     = 0
        self.last_capacity_year                   = 0
        self.last_capacity_amt                    = 0
        self.last_ore_year                        = 0
        self.last_ore_cap                         = 0
        # ==========================================================================================================================
        self.userName                             = ''
        self.newProdUnit                          = ''
        self.mCommodities                         = ''
        self.otherFilter                          = ''
        self.metal_comm                           = ''
        self.mOperators                           = ''
        self.key_commodity                        = ''
        self.extraWhere                           = ''
        self.extraVars                            = ''
        self.baseU                                = ''
        self.sqlExclude                           = ''
        self.lastProdUnit                         = ''
        self.lastProdType                         = ''
        self.first_reserve_type                   = ''
        self.first_reserve_unit                   = ''
        self.first_capacity_type                  = ''
        self.first_capacity_unit                  = ''
        self.last_reserve_type                    = ''
        self.last_reserve_unit                    = ''
        self.last_capacity_type                   = ''
        self.last_capacity_unit                   = ''
        self.last_ore_type                        = ''
        self.last_ore_unit                        = ''
        # ==========================================================================================================================
        self.all_commodities                      = {}
        self.modelled_commod                      = {}
        self.not_modelled_commod                  = {}
        self.mines                                = {}
        self.last_data                            = {}
        
        self.fldAssetsList                        = []
        self.fldAssetsListDT                      = []
        self.error_log                            = []
        self.commod_list                          = []
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def import_mining_tables(self):
        command = 'sqlcmd -S localhost -d MiningEngineextract -i %s'
        os.system('cd %s' % MINING_DB_DIR)
        for sql_file in [filename for filename in os.listdir(MINING_DB_DIR) if filename[-3:] == 'sql']:
            filename = sql_file[:-4]
            new_filename = filename.replace('.', '_')
            sql_filename = new_filename + '.sql'
            os.rename(MINING_DB_DIR + sql_file, MINING_DB_DIR + sql_filename)
            print '%s - %s:' % (self.NewMineId, self.mining_section),  command % (MINING_DB_DIR + sql_filename)
            os.system(command % (MINING_DB_DIR + sql_filename))
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def mining_units(self, fromUnit, toUnit):
        conv_factor = 0.0
        sql_select = 'SELECT unitFactor FROM mining_unit_conversion WHERE fromUnit="%s" AND toUnit="%s"' % (fromUnit, toUnit)
        self.curr.execute(sql_select)
        ret_val = self.curr.fetchone()
        if ret_val:
            conv_factor = float(ret_val[0])
        return conv_factor
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def check_exception_log(self, mComment, mErrorType):
        ret_val = False
        sql_statement = ""
        if len(mErrorType.strip()) > 0:
            sql_statement += "error_Type = '" + mErrorType + "' AND "
        if len(mComment.strip()) > 0:
            sql_statement += "comment = '" + mComment + "' AND "
        if len(sql_statement) > 0:
            sql_statement = "SELECT * FROM mining_error_log_exceptions WHERE " + sql_statement[:-4]
            self.curr.execute(sql_statement)
            r2 = self.curr.fetchall()
            for datarow in r2:
                ret_val = True
        return ret_val
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def save_error_log(self, mComment, eSymbol, ii):
        mPeriod = self.error_log[1][ii]
        mErrorType = self.error_log[4][ii]
        mParam = self.error_log[5][ii]
        mParam_value = self.error_log[6][ii]
        col_names = ['NewMineid','Mineid','mineName','mineCountry','state','mineRegion','mineStage','comment','Commodities','period','param_value','nparam_value','session_key','error_type','add_by','add_date']
        col_str = ','.join(col_names)
        var_str = buildMySQLin(len(col_names), "%s")
        if self.check_exception_log(mComment, mErrorType):
            pass
        else:
            ts = time.time()
            add_by   = getpass.getuser()
            add_date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            sql_insert = "INSERT INTO mining_error_log (%s) VALUES %s" % (col_str, var_str)
            param_vals = (int(self.NewMineId), self.Mineid, self.mineName, self.mineCountry, self.state, self.mineRegion, self.mineStage, mComment)
            param_vals += (self.key_commodity, mPeriod, mParam, float(mParam_value), self.mSession_key, mErrorType, add_by, add_date)
            self.curr.execute(sql_statement, param_vals)
            self.curr.execute('COMMIT')
        #
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_param_detail(self, param_name, commodity='', extraWhere='', extraVars=''):
        debug = False
        if commodity:
            mCommodity = commodity
        else:
            mCommodity = self.key_commodity
        param_type = ""
        if param_name == "FIRST_YEAR_FACTOR" or param_name == "LAST_YEAR_FACTOR":
            pass
        if debug:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "In PARAMDETAIL "
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'extraWhere:', extraWhere
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'extraVars:', extraVars
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'param_name:', param_name
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "+" * 25
        # ----------------------------------------------------------------------------------------------------
        ret_val = ""
        mPoints = 0
        lmineid = 0
        lRegion = 0
        lCommodity = 0
        param = []
        param_points = []  # <----------------- Score
        param_ans = []
        if param_name in ("YEARS_TO_PROJECT", "PRODUCTION_TOLERANCE", "LAST_YEAR_FACTOR", "ORE_CAPACITY_TO_ROM", "RECOVERY_RATE", "RESOURCES_TO_RESERVES", "CAPACITY_TO_PRODUCTION",
                          "BASE_UNIT", "FIRST_YEAR_FACTOR", "SALEABLE_PRODUCTION_YIELD_FACTOR", "METALLURGICAL_RECOVERY_FACTOR", "ORE_GRADE"):
            if debug:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  'param_name:', param_name + " ""+^" * 20
            p_num = 0  # <-------------- 
            param_type = "MODEL_RULES"
            sql_statement = \
'''SELECT rtrim(param_value) as pvalue,
    case when Param_range is null then ' ' else Param_range end as pRange,
    case when newMineId is null then ' ' else newMineId end as mineId,
    case when MineCountry is null then ' ' else MineCountry end as mCountry,
    case when MineRegion is null then ' ' else MineRegion end as mRegion,
    case when State is null then ' ' else State end as mState,
    case when MineStage is null then ' ' else MineStage end as mStage,
    case when MineType is null then ' ' else MineType end as mType,
    case when MineMethod is null then ' ' else MineMethod end as mMethod,
    case when Commodity is null then ' ' else Commodity end as mCommodity,
    case when Operators is null then ' ' else Operators end as mOperators,
    case when param_name is null then ' ' else param_name end as mparam_name
     from mining_model_rules WHERE UPPER(param_name) =  '''
            sql_statement += "'" + param_name + "' "
            if debug:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
                print '%s - %s:' % (self.NewMineId, self.mining_section),  'param_name:', param_name
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "$=" * 20
            self.curr.execute(sql_statement)
            # ----------------------------------------------------------------------------------------------------
        else:
            if debug:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "ALL OTHER PARAM NAMES"
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "IN SQL----"
                print '%s - %s:' % (self.NewMineId, self.mining_section),  'mStatus:', mStatus
            param_type = "MODEL_RULES"
            p_num = 6
            sql_statement = '''SELECT
    case when newMineId is null then ' ' else newMineId end as mineId,
    rtrim(param_value) as pvalue,
    case when Param_range is null then ' ' else Param_range end as pRange,
    case when MineRegion is null then ' ' else MineRegion end as mRegion,
    case when MineCountry is null then ' ' else MineCountry end as mCountry,
    case when State is null then ' ' else State end as mState,
    case when MineStage is null then ' ' else MineStage end as mStage,
    case when MineType is null then ' ' else MineType end as mType,
    case when MineMethod is null then ' ' else MineMethod end as mMethod,
    case when Commodity is null then ' ' else Commodity end as mCommodity,
    case when Operators is null then ' ' else Operators end as mOperators
     from mining_model_rules WHERE UPPER(param_name) = %s '''
            self.curr.execute(sql_statement + ";", (param_name,))
        # ----------------------------------------------------------------------------------------------------
        r2 = self.curr.fetchall()
        for datarow in r2:
            mPoints = 0
            goAhead = 1
            extraParse = " goAhead "
            # ----------------------------------------------- CHECK FOR EVERY LINE
            if param_name == "XFIRST_YEAR_FACTOR" or param_name == "XLAST_YEAR_FACTOR":
                # if debugMode:
                #    print '%s - %s:' % (self.NewMineId, self.mining_section),  "in FIRST_YEAR_FACTOR"
                # add code to parde the params_id field
                fldParse = datarow[1]
                if fldParse.count("=") > 0:
                    posDash = fldParse.index("=")
                    fldVar2 = fldParse[posDash + 1:]
                    extraParse = " float(" + str(extraWhere) + ") == float(" + fldVar2 + ") "
                elif fldParse.count(">") > 0:
                    #
                    posDash = fldParse.index(">")
                    fldVar2 = fldParse[posDash + 1:]
                    extraParse = " float(" + str(extraWhere) + ") > float(" + fldVar2 + ") "
                elif fldParse.count("<") > 0:
                    #
                    posDash = fldParse.index("<")
                    fldVar2 = fldParse[posDash + 1:]
                    extraParse = " float(" + str(extraWhere) + ") < float(" + fldVar2 + ") "
                elif fldParse.count("-") > 0:
                    #
                    posDash = fldParse.index("-")
                    fldVar1 = fldParse[:posDash]
                    fldVar2 = fldParse[posDash + 1:]
                    extraParse = "  float(" + str(extraWhere) + ") <= float(" + fldVar1 + ") and float(" + str(extraWhere) + ") > float(" + fldVar2 + ") "
                else:
                    extraParse = " goAhead "
                if eval(extraParse):
                    mPoints = 15000
                    goAhead = 1
                else:
                    goAhead = 0
            # --------------------------------------------------------------------------
            # MineId
            if datarow[2] is None or str(datarow[2]) == '0' or len(datarow[2].strip()) == 0:
                goAhead = 1
            else:
                if str(self.NewMineId) == str(datarow[2]) and eval(extraParse):
                    mPoints = 10000
                    if debug:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),  str(datarow[0]) + " <-->" + datarow[2] + " Points " + str(mPoints)
                    lAsset_id = 1
                    goAhead = 0
            # ----------------------------------------------------------------------
            # Mine Region
            if goAhead and len(datarow[4].strip()) > 0:
                if self.mineRegion.strip().upper() == datarow[4].strip().upper() and eval(extraParse):
                    lRegion = 1
                    mPoints += 10
                    if debug:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),  str(datarow[0]) + " <-->" + datarow[4] + " Region " + str(mPoints)
                else:
                    # no match, do not advance, erase all points
                    goAhead = 0
                    mPoints = 0
            else:
                # no points, but move ahead
                pass
            # ------------------------------------------------------------------------------------------
            # Mine Country
            if goAhead and len(datarow[3].strip()) > 0:
                if self.mineCountry.strip().upper() == datarow[3].strip().upper() and eval(extraParse):
                    lCountry = 1
                    mPoints += 50
                    if debug:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),  str(datarow[0]) + " - " + datarow[3] + " Country " + str(mPoints)
                else:
                    # no match, do not advance, erase all points
                    goAhead = 0
                    mPoints = 0
            else:
                # no points, but move ahead
                pass
            # ------------------------------------------------------------------------------------------
            # Mine State
            if goAhead and len(datarow[5].strip()) > 0:
                if self.state.strip().upper() == datarow[5].strip().upper() and eval(extraParse):
                    lState = 1
                    mPoints += 100
                    if debug:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),  str(datarow[0]) + " - " + datarow[5] + " State " + str(mPoints)
                else:
                    # no match, do not advance, erase all points
                    goAhead = 0
                    mPoints = 0
            else:
                # no points, but move ahead
                pass
                #
            # ------------------------------------------------------------------------------------------
            # Mine Stage
            if goAhead and len(datarow[6].strip()) > 0:
                if self.mineStatus.strip().upper() == datarow[6].strip().upper() and eval(extraParse):
                    lStage = 1
                    mPoints += 200
                    if debug:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),  str(datarow[6]) + " - " + datarow[6] + " Stage " + str(mPoints)
                else:
                    # no match, do not advance, erase all points
                    goAhead = 0
                    mPoints = 0
            else:
                # no points, but move ahead
                pass
                #
            # ------------------------------------------------------------------------------------------
            # Mine Type
            if goAhead and len(datarow[7].strip()) > 0:
                if debug:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  extraParse
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  param_name
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  "=" * 25
                if datarow[7] is None or eval(extraParse) is None or self.mineType is None:
                    goAhead = 0
                    mPoints = 0
                elif self.mineType.strip().upper() == datarow[7].strip().upper() and eval(extraParse):
                    lMineType = 1
                    mPoints += 600
                    if debug:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),  str(datarow[0]) + " - " + datarow[7] + " Mine Type " + str(mPoints)
                else:
                    # no match, do not advance, erase all points
                    goAhead = 0
                    mPoints = 0
            else:
                # no points, but move ahead
                pass
            # ------------------------------------------------------------------------------------------
            # Mine Method
            if goAhead and len(datarow[8].strip()) > 0:
                if self.mineMethod.strip().upper() == datarow[8].strip().upper() and eval(extraParse):
                    lMineMethod = 1
                    mPoints += 800
                    if debug:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),  str(datarow[0]) + " - " + datarow[8] + " Mine Method " + str(mPoints)
                else:
                    # no match, do not advance, erase all points
                    goAhead = 0
                    mPoints = 0
            else:
                # no points, but move ahead
                pass
            # ------------------------------------------------------------------------------------------
            # Mine Commodity
            if goAhead and len(datarow[9].strip()) > 0:
                if mCommodity.strip().upper() == datarow[9].strip().upper() and eval(extraParse):
                    lCommodity = 1
                    mPoints += 1000
                    if debug:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),  str(datarow[0]) + " - " + datarow[9] + " Mine Commodity " + str(mPoints)
                else:
                    # no match, do not advance, erase all points
                    goAhead = 0
                    mPoints = 0
            else:
                # no points, but move ahead
                pass
            # ------------------------------------------------------------------------------------------
            # Mine Operator
            if goAhead and len(datarow[10].strip()) > 0:
                if self.mOperators.strip().upper() == datarow[10].strip().upper() and eval(extraParse):
                    lOperator = 1
                    mPoints += 3000
                    if debug:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),  str(datarow[0]) + " - " + datarow[9] + " Mine operator " + str(mPoints)
                else:
                    # no match, do not advance, erase all points
                    goAhead = 0
                    mPoints = 0
            else:
                # no points, but move ahead
                pass
            #
            if goAhead and len(param_name.strip()) > 0:
                if param_name.strip().upper() == datarow[11].strip().upper() and eval(extraParse):
                    lStatus = 1
                    mPoints += 1
                    if debug:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),  str(datarow[0]) + " ***** " + datarow[11] + " BASE PARAMETER FOUND " + str(mPoints)
                else:
                    # no match, do not advance, erase all points
                    goAhead = 0
                    mPoints = 0
            else:
                # no points, but move ahead
                pass
            # ------------------------------------------------------------------------------------------
            if mPoints > 0:
                param_points.append(mPoints)
                param_ans.append(datarow[p_num])
                if debug:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  "POINTS ----> " + str(mPoints)
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  extraParse
            # check each criteria against the asset if there is a match add to the array
            mPoints = 0
        # ----------------------------------------------------------------------------------------------------
        if len(param_points) > 0:
            mPoints = max(param_points)
            fmIndex = param_points.index(mPoints)
            ret_val = param_ans[fmIndex]
            if debug:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  param_name + " (param_name) chosen(ret_val): " + str(ret_val)
                print '%s - %s:' % (self.NewMineId, self.mining_section),  'fmIndex:', fmIndex
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "Points -->" + str(mPoints)
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "------------------------------------------------------"
        return ret_val
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_asset_data(self, data_table, data_type):
        data_names = {
            'production': {     'type': 'productionType',
                           'commodity': 'productionByCommodity',
                               'value': 'productionValue',
                                'year': 'productionYear',
                                'unit': 'productionUnit'},

              'capacity': {     'type': 'capacityType',
                           'commodity': 'CommodityByCapacity',
                               'value': 'capacity',
                                'year': 'capacityYear',
                                'unit': 'capacityUnit'},

              'reserves': {     'type': 'reserveType',
                           'commodity': 'CommodityByReserve',
                               'value': 'reserve',
                                'year': 'reserveYear',
                                'unit': 'reserveUnit'},

              'resource': {     'type': 'resourceType',
                           'commodity': 'CommodityByResource',
                               'value': 'resource',
                                'year': 'resourceYear',
                                'unit': 'resourceUnit'}
        }
        data = data_names[data_table]
        params = (data['type'], data['commodity'], data['value'], data['year'], data['unit'], data_table, self.NewMineId, data['type'], data_type)

        sql_select = "SELECT NewMineId,%s,%s,%s,%s,%s,source FROM mining_%s_daily WHERE NewMineId=%s AND %s='%s' " % params
        sql_select += "AND NOT (UCASE(source) LIKE 'EST:%' OR UCASE(source) LIKE '%ESTIMATION%' OR source='') "

        if data_table in []:
            discount_year = get_discount_year(curr)
            sql_select += "AND %s < %s " % (data['year'], discount_year)

        sql_select += ""
        sql_select += "ORDER BY %s,%s,%s ASC " % (data['type'], data['commodity'], data['year'])
        self.curr.execute(sql_select)
        asset_data = self.curr.fetchall()

        if not asset_data:
            asset_data = ()

        return asset_data
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_param_avg(self, value_col, param_table, param_col, param, commodity_col, commodity, range_col='', range='', data_type_col='', data_type='', sql_where=''):
        param_avg = 0.0
        sql_select = 'SELECT %s FROM %s WHERE %s="%s" AND %s="%s" '
        params = (value_col, param_table, param_col, param, commodity_col, commodity)
        if range_col:
            sql_select += 'AND %s="%s" '
            params += (range_col, range)
        if sql_where:
            sql_select += sql_where
        if data_type_col:
            sql_select += 'AND %s="%s" '
            params += (data_type_col, data_type)
        sql_query = sql_select % params
        self.curr.execute(sql_query)
        param_vals = [float(data[0]) for data in self.curr.fetchall()]
        if len(param_vals) > 0:
            val_count = float(len(param_vals))
            param_avg = float(sum(param_vals)) / float(val_count)
        return param_avg
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_ore_country_avg(self, country, commodity):
        sql_extra = 'AND oreGrade < 100 '
        ore_grade = self.get_param_avg('oreGrade', 'mining_ore_grade', 'mineCountry', country, 'commodity', commodity, sql_where=sql_extra)
        return ore_grade
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_ore_region_avg(self, region, commodity):
        sql_extra = 'AND oreGrade < 100 '
        ore_grade = self.get_param_avg('oreGrade', 'mining_ore_grade', 'mineRegion', region, 'commodity', commodity, sql_where=sql_extra)
        return ore_grade
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_ore_global_avg(self, commodity):
        sql_extra = 'AND oreGrade < 100 '
        ore_grade = self.get_param_avg('oreGrade', 'mining_ore_grade', 'oreGradeUnit', '%', 'commodity', commodity, sql_where=sql_extra)
        return ore_grade
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_ore_grade_default(self):
        conn = get_connection(server='mysql', database='miningengineextract')
        curr = conn.cursor()
        curr.execute('SELECT globalAvg FROM mining_ore_averages GROUP BY commodity ORDER BY globalAvg')
        data_results = curr.fetchall()
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'data_results:', data_results
        global_avgs = [data[0] for data in data_results]
        global_avg_count = len(global_avgs)
        avg_mid_indx = int(global_avg_count / 2)
        ore_grade_default = global_avgs[avg_mid_indx]
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'global_avg_count:', global_avg_count
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'avg_mid_indx:', avg_mid_indx
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'global_avgs:', global_avgs
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'ore_grade_default:', ore_grade_default
        curr.close()
        conn.close()
        return ore_grade_default
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_saleable_factor(self, commodity):
        saleable_factor = self.sale_yield
        self.curr.execute('SELECT mineCountry, mineRegion, mineStage, mineType, mineMethod FROM mining_assets_daily WHERE NewMineId=%s' % self.NewMineId)
        self.mineCountry, self.mineRegion, self.mineStage, self.mineType, self.mineMethod = self.curr.fetchone()
        saleable_yield = self.get_param_detail('SALEABLE_PRODUCTION_YIELD_FACTOR', commodity)
        if saleable_yield:
            saleable_factor = float(saleable_yield)
        return saleable_factor
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_ore_capacity_to_rom(self, commodity):
        ore_capacity_to_rom = self.ore_cap_to_rom
        self.curr.execute('SELECT mineCountry, mineRegion, mineStage, mineType, mineMethod FROM mining_assets_daily WHERE NewMineId=%s' % self.NewMineId)
        self.mineCountry, self.mineRegion, self.mineStage, self.mineType, self.mineMethod = self.curr.fetchone()
        ore_cap = self.get_param_detail('ORE_CAPACITY_TO_ROM', commodity)
        if ore_cap:
            ore_capacity_to_rom = float(ore_cap)
        return ore_capacity_to_rom
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_recov_factor(self, commodity):
        self.curr.execute('SELECT mineCountry, mineRegion, mineStage, mineType, mineMethod FROM mining_assets_daily WHERE NewMineId=%s' % self.NewMineId)
        self.mineCountry, self.mineRegion, self.mineStage, self.mineType, self.mineMethod = self.curr.fetchone()
        recov_factor = self.get_param_detail('METALLURGICAL_RECOVERY_FACTOR', commodity)
        if recov_factor:
            recov_factor = float(recov_factor)
        else:
            recov_factor = 0.9
        return recov_factor
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_ore_grade(self, commodity):
        self.curr.execute('SELECT mineCountry, mineRegion, mineStage, mineType, mineMethod FROM mining_assets_daily WHERE NewMineId=%s' % self.NewMineId)
        self.mineCountry, self.mineRegion, self.mineStage, self.mineType, self.mineMethod = self.curr.fetchone()

        sql_select = 'SELECT DISTINCT NewMineId, productionByCommodity FROM mining_production_daily WHERE productionType="Ore Grade" '
        sql_select += 'AND NOT (UCASE(source) LIKE "EST:%" or UCASE(source) LIKE "%ESTIMATION%") '
        self.curr.execute(sql_select)
        ore_data = self.curr.fetchall()
        if (self.NewMineId, commodity) in ore_data:
            sql_select = 'SELECT productionValue, productionUnit FROM mining_production_daily WHERE productionType="Ore Grade" '
            sql_select += 'AND NewMineId=%s AND productionByCommodity="%s" ORDER BY productionYear DESC'

            self.curr.execute(sql_select % (self.NewMineId, commodity))
            prod_val, prod_unit = self.curr.fetchone()

            if prod_unit == '%':
                ore_grade = float(prod_val)
            else:
                conv_factor = self.mining_units(prod_unit, '%')
                prod_val = float(prod_val) * conv_factor
                ore_grade = prod_val
        else:
            ore_grade = ''

        if ore_grade:
            ore_grade = float(ore_grade) / 100.0
        else:
            self.curr.execute('SELECT DISTINCT NewMineId FROM mining_ore_grade WHERE commodity="%s" ' % commodity)
            ore_avg_data = [data[0] for data in self.curr.fetchall()]
            if self.NewMineId in ore_avg_data:
                self.curr.execute('SELECT oreGrade FROM mining_ore_grade WHERE NewMineId=%s AND commodity="%s" ' % (self.NewMineId, commodity))
                ore_grade = self.curr.fetchone()[0]
            else:
                ore_grade = ''
            if ore_grade:
                ore_grade = float(ore_grade) / 100.0
            else:
                self.curr.execute('SELECT DISTINCT mineCountry FROM mining_ore_averages WHERE commodity="%s" ' % commodity)
                ore_avg_data = [data[0] for data in self.curr.fetchall()]
                if self.mineCountry in ore_avg_data:
                    self.curr.execute('SELECT countryAvg FROM mining_ore_averages WHERE mineCountry="%s" AND commodity="%s" ' % (self.mineCountry, commodity))
                    ore_grade = self.curr.fetchone()[0]
                else:
                    ore_grade = ''
                if ore_grade:
                    ore_grade = float(ore_grade) / 100.0
                else:
                    self.curr.execute('SELECT DISTINCT mineRegion FROM mining_ore_averages WHERE commodity="%s" ' % commodity)
                    ore_avg_data = [data[0] for data in self.curr.fetchall()]
                    if self.mineRegion in ore_avg_data:
                        self.curr.execute('SELECT regionAvg FROM mining_ore_averages WHERE mineRegion="%s" AND commodity="%s" ' % (self.mineRegion, commodity))
                        ore_grade = self.curr.fetchone()[0]
                    else:
                        ore_grade = ''
                    if ore_grade:
                        ore_grade = float(ore_grade) / 100.0
                    else:
                        self.curr.execute('SELECT DISTINCT commodity FROM mining_ore_averages')
                        ore_avg_data = [data[0] for data in self.curr.fetchall()]
                        if commodity in ore_avg_data:
                            self.curr.execute('SELECT globalAvg FROM mining_ore_averages WHERE commodity="%s" ' % commodity)
                            ore_grade = self.curr.fetchone()[0]
                        else:
                            ore_grade = ''
                        if ore_grade:
                            ore_grade = float(ore_grade) / 100.0
                        else:
                            # Check mining_model_rules for ORE_GRADE
                            ore_grade = self.get_param_detail('ORE_GRADE', commodity)
                            if ore_grade:
                                ore_grade = float(ore_grade) / 100.0
                            else:
                                # Get average ore grade for commodity by country
                                sql_and = 'AND param_value < 100 '
                                ore_grade = self.get_param_avg('param_value', 'mining_model_rules', 'param_name', 'ORE_GRADE', 'commodity', commodity, range_col='mineCountry', range=self.mineCountry, sql_where=sql_and)
                                if ore_grade:
                                    ore_grade = float(ore_grade) / 100.0
                                else:
                                    # Get average ore grade for commodity by region
                                    sql_and = 'AND mineCountry IN (SELECT DISTINCT mineCountry FROM mining_assets_daily WHERE mineRegion="%s") ' % self.mineRegion
                                    sql_and += 'AND param_value < 100 '
                                    ore_grade = self.get_param_avg('param_value', 'mining_model_rules', 'param_name', 'ORE_GRADE', 'commodity', commodity, sql_where=sql_and)
                                    if ore_grade:
                                        ore_grade = float(ore_grade) / 100.0
                                    else:
                                        # Get average ore grade for commodity globally
                                        sql_and = 'AND param_value < 100 '
                                        ore_grade = self.get_param_avg('param_value', 'mining_model_rules', 'param_name', 'ORE_GRADE', 'commodity', commodity, sql_where=sql_and)
                                        ore_grade = float(ore_grade) / 100.0
        return ore_grade
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_metal_grade(self, data_table, commodity, year):
        data_names = {
            'reserves': {'year': 'reserveYear',
                         'value': 'reserve',
                         'unit': 'reserveUnit',
                         'type': 'reserveType',
                         'data type': 'Total Reserves - Metal Grade',
                         'commodity': 'CommodityByReserve'},
            'resource': {'year': 'resourceYear',
                         'value': 'resource',
                         'unit': 'resourceUnit',
                         'type': 'resourceType',
                         'data type': 'Total Resources Metal Grade',
                         'commodity': 'CommodityByResource'}
        }
        year_name  = data_names[data_table]['year']
        value_name = data_names[data_table]['value']
        unit_name  = data_names[data_table]['unit']
        type_name  = data_names[data_table]['type']
        data_type  = data_names[data_table]['data type']
        comm_name  = data_names[data_table]['commodity']

        sql_select = "SELECT %s, %s FROM mining_%s_daily WHERE %s=%s AND %s='%s' AND %s='%s' " % (value_name, unit_name, data_table, year_name, year, type_name, data_type, comm_name, commodity)
        sql_select += "AND NOT (UCASE(source) LIKE 'EST:%' OR UCASE(source) LIKE '%ESTIMATION%' OR source='') "
        self.curr.execute(sql_select)
        metal_ore_grade = self.curr.fetchone()
        if metal_ore_grade:
            metal_grade = float(metal_ore_grade[0]) / 100.0
        else:
            metal_grade = self.get_ore_grade(commodity)
        param_vals = (value_name, metal_grade, value_name, commodity, self.NewMineId, self.mSession_key)
        self.curr.execute('UPDATE mining_param_track SET %sOreGrade=%s, %sOreCommodity="%s" WHERE NewMineId=%s AND sessionKey="%s"' % param_vals)
        self.curr.execute('COMMIT')
        return metal_grade
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_metal_commodity(self, data_table):
        data_names = {
            'production': {     'type': 'productionType',
                           'commodity': 'productionByCommodity',
                                'year': 'productionYear',
                           'type name': 'Metal Production'},

              'capacity': {     'type': 'capacityType',
                           'commodity': 'commodityByCapacity',
                                'year': 'capacityYear',
                           'type name': 'Metal Capacity'},

              'reserves': {     'type': 'reserveType',
                           'commodity': 'CommodityByReserve',
                                'year': 'reserveYear',
                           'type name': 'Pure Metal Total Reserves'},

              'resource': {     'type': 'resourceType',
                           'commodity': 'CommodityByResource',
                                'year': 'resourceYear',
                           'type name': 'Total Pure Metal Resources'},
        }

        data_year = data_names[data_table]['year']
        data_type = data_names[data_table]['type']
        data_comm = data_names[data_table]['commodity']
        type_name = data_names[data_table]['type name']

        sql_select = "SELECT MAX(%s) FROM mining_%s_daily WHERE NewMineId=%s " % (data_year, data_table, self.NewMineId)
        sql_query = "AND %s='%s' " % (data_type, type_name)
        sql_query += "AND NOT (UCASE(source) LIKE 'EST:%' OR UCASE(source) LIKE '%ESTIMATION%' OR source='') "
        self.curr.execute(sql_select + sql_query)
        max_metal_year = self.curr.fetchone()[0]

        sql_select = "SELECT DISTINCT %s FROM mining_%s_daily WHERE NewMineId=%s " % (data_comm, data_table, self.NewMineId)
        sql_query += "AND %s=%s " % (data_year, max_metal_year)
        self.curr.execute(sql_select + sql_query)
        metal_comms = [data[0] for data in self.curr.fetchall()]
        metal_commodity = metal_comms[0]
        return metal_commodity
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_total_factor(self, data_table, data_type):
        total_factor = 0
        data_names = {
            'reserves': {'year': 'reserveYear',
                         'value': 'reserve',
                         'unit': 'reserveUnit',
                         'type': 'reserveType'},
            'resource': {'year': 'resourceYear',
                         'value': 'resource',
                         'unit': 'resourceUnit',
                         'type': 'resourceType'}
        }

        year_name = data_names[data_table]['year']
        value_name = data_names[data_table]['value']
        unit_name = data_names[data_table]['unit']
        type_name = data_names[data_table]['type']

        sql_select = "SELECT AVG(c.type_to_total) FROM (SELECT (a.%s/b.%s) AS type_to_total FROM mining_%s_daily AS a, mining_%s_daily AS b " % (
        value_name, value_name, data_table, data_table)
        sql_select += "WHERE a.%s='%s' AND b.%s ='total %ss' AND a.NewMineId = b.NewMineId AND a.%s=b.%s AND a.%s=b.%s " % (
        type_name, data_type, type_name, value_name, unit_name, unit_name, year_name, year_name)
        sql_select += "AND NOT (UCASE(a.source) LIKE 'EST:%' OR UCASE(a.source) LIKE '%ESTIMATION%' OR a.source='') AND NOT (UCASE(b.source) LIKE 'EST:%' OR UCASE(b.source) LIKE '%ESTIMATION%' OR b.source='') "
        sql_select += "AND a.%s <= b.%s) AS c " % (value_name, value_name)

        self.curr.execute(sql_select)
        total_factor = float(self.curr.fetchone()[0])
        return total_factor
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def metal_to_rom(self, last_data):
        rom_value = 0
        data_commodity = last_data['commodity']
        data_value = float(last_data['value'])
        data_unit = last_data['unit']
        if data_unit.upper() in ['MMT', 'MTPA']:
            conv_factor = 1.0
        else:
            conv_factor = float(self.mining_units(data_unit, 'MMT'))
            data_unit = 'MMT'
        data_value = float(data_value) * conv_factor
        recov_factor = float(self.get_recov_factor(data_commodity))
        ore_grade = float(self.get_ore_grade(data_commodity))
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'data_commodity:', data_commodity
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'data_value:', data_value
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'data_unit:', data_unit
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'recov_factor:', recov_factor
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'ore_grade:', ore_grade
        param_vals = ((ore_grade * 100), data_commodity, recov_factor, self.NewMineId, self.mSession_key)
        self.curr.execute('UPDATE mining_param_track SET oreGrade=%s, oreGradeCommodity=%s, recoveryFactor=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
        self.curr.execute('COMMIT')
        if ore_grade and recov_factor:
            rom_value = float(data_value) / float(ore_grade * recov_factor)
        return rom_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def saleable_to_rom(self, last_data):
        rom_value = 0
        data_commodity = last_data['commodity']
        data_value = float(last_data['value'])
        data_unit = last_data['unit']
        if data_unit.upper() in ['MMT', 'MTPA']:
            conv_factor = 1.0
        else:
            conv_factor = float(self.mining_units(data_unit, 'MMT'))
            data_unit = 'MMT'
            data_value = float(data_value) * conv_factor
        saleable_factor = float(self.get_saleable_factor(data_commodity))
        self.curr.execute('UPDATE mining_param_track SET saleableYieldFactor=%s WHERE NewMineId=%s AND sessionKey=%s',(saleable_factor, self.NewMineId, self.mSession_key))
        self.curr.execute('COMMIT')
        rom_value = float(data_value) / float(saleable_factor)
        return rom_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def ore_to_rom(self, last_data):
        rom_value = 0
        data_commodity = last_data['commodity']
        data_value = float(last_data['value'])
        data_unit = last_data['unit']
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'data_commodity:', data_commodity
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'data_value:', data_value
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'data_unit:', data_unit
        if data_unit.upper() in ['MMT', 'MTPA']:
            conv_factor = 1.0
        else:
            conv_factor = float(self.mining_units(data_unit, 'MMT'))
            data_unit = 'MMT'
            data_value = float(data_value) * conv_factor
        ore_capacity_to_rom = float(self.get_ore_capacity_to_rom(data_commodity))
        param_vals = (ore_capacity_to_rom, self.NewMineId, self.mSession_key)
        self.curr.execute('UPDATE mining_param_track SET oreCapacityToROM=%s WHERE NewMineId=%s AND sessionKey=%s',param_vals)
        self.curr.execute('COMMIT')
        rom_value = float(data_value) / float(ore_capacity_to_rom)
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'ore_capacity_to_rom:', ore_capacity_to_rom
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'rom_value (ore_to_rom):', rom_value
        return rom_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def probable_to_total(self, last_data):
        '''Use probable reserves to estimate total reserves'''
        total_value = 0
        data_commodity = last_data['commodity']
        data_value = float(last_data['value'])
        data_unit = last_data['unit']
        if data_unit.upper() in ['MMT', 'MTPA']:
            conv_factor = 1.0
        else:
            conv_factor = float(self.mining_units(data_unit, 'MMT'))
            data_unit = 'MMT'
            data_value = float(data_value) * conv_factor
        self.curr.execute('SELECT param_value FROM mining_model_rules WHERE param_name="PROBABLE_TO_TOTAL"')
        probable_factor = self.curr.fetchone()[0]
        if probable_factor:
            total_value = float(data_value) / float(probable_factor)
        self.curr.execute('UPDATE mining_param_track SET probableToTotal=%s WHERE NewMineId=%s AND sessionKey=%s',(probable_factor, self.NewMineId, self.mSession_key))
        self.curr.execute('COMMIT')
        return total_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def proved_to_total(self, last_data):
        '''Use proved reserves to estimate total reserves'''
        total_value = 0
        data_commodity = last_data['commodity']
        data_value = float(last_data['value'])
        data_unit = last_data['unit']
        if data_unit.upper() in ['MMT', 'MTPA']:
            conv_factor = 1.0
        else:
            conv_factor = float(self.mining_units(data_unit, 'MMT'))
            data_unit = 'MMT'
            data_value = float(data_value) * conv_factor
        self.curr.execute('SELECT param_value FROM mining_model_rules WHERE param_name="PROVED_TO_TOTAL"')
        proved_factor = self.curr.fetchone()[0]
        if proved_factor:
            total_value = float(data_value) / float(proved_factor)
        self.curr.execute('UPDATE mining_param_track SET provedToTotal=%s WHERE NewMineId=%s AND sessionKey=%s',(proved_factor, self.NewMineId, self.session_key))
        self.curr.execute('COMMIT')
        return total_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def metal_to_total(self, data_table, last_data):
        '''Use metal reserves or resources to estimate total reserves or resources'''
        total_value = 0
        data_commodity = last_data['commodity']
        data_value = float(last_data['value'])
        data_unit = last_data['unit']
        data_year = last_data['year']
        if data_unit.upper() in ['MMT', 'MTPA']:
            conv_factor = 1.0
        else:
            conv_factor = float(self.mining_units(data_unit, 'MMT'))
            data_unit = 'MMT'
            data_value = float(data_value) * conv_factor
        recov_factor = float(self.get_recov_factor(data_commodity))
        ore_grade = self.get_metal_grade(data_table, data_commodity, data_year)
        if ore_grade and recov_factor:
            total_value = float(data_value) / float(recov_factor * ore_grade)
        return total_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def measured_to_total(self, last_data):
        '''Use measured resources to estimate total resources'''
        total_value = 0
        data_commodity = last_data['commodity']
        data_value = float(last_data['value'])
        data_unit = last_data['unit']
        if data_unit.upper() in ['MMT', 'MTPA']:
            conv_factor = 1.0
        else:
            conv_factor = float(self.mining_units(data_unit, 'MMT'))
            data_unit = 'MMT'
            data_value = float(data_value) * conv_factor
        self.curr.execute('SELECT param_value FROM mining_model_rules WHERE param_name="MEASURED_TO_TOTAL"')
        measured_factor = self.curr.fetchone()[0]
        if measured_factor:
            total_value = float(data_value) / float(measured_factor)
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'measured_factor:', measured_factor
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'measured resources:', data_value
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'estimated total resources:', total_value
        self.curr.execute('UPDATE mining_param_track SET measuredToTotal=%s WHERE NewMineId=%s AND sessionKey=%s', (measured_factor, self.NewMineId, self.mSession_key))
        self.curr.execute('COMMIT')
        return total_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def indicated_to_total(self, last_data):
        '''Use indicated resources to estimate total resources'''
        total_value = 0
        data_commodity = last_data['commodity']
        data_value = float(last_data['value'])
        data_unit = last_data['unit']
        if data_unit.upper() in ['MMT', 'MTPA']:
            conv_factor = 1.0
        else:
            conv_factor = float(self.mining_units(data_unit, 'MMT'))
            data_unit = 'MMT'
            data_value = float(data_value) * conv_factor
        self.curr.execute('SELECT param_value FROM mining_model_rules WHERE param_name="INDICATED_TO_TOTAL"')
        indicated_factor = self.curr.fetchone()[0]
        if indicated_factor:
            total_value = float(data_value) / float(indicated_factor)
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'indicated_factor:', indicated_factor
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'indicated resources:', data_value
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'estimated total resources:', total_value
        self.curr.execute('UPDATE mining_param_track SET indicatedToTotal=%s WHERE NewMineId=%s AND sessionKey=%s',(indicated_factor, self.NewMineId, self.mSession_key))
        self.curr.execute('COMMIT')
        return total_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def inferred_to_total(self, last_data):
        '''Use inferred resources to estimate total resources'''
        total_value = 0
        data_commodity = last_data['commodity']
        data_value = float(last_data['value'])
        data_unit = last_data['unit']
        if data_unit.upper() in ['MMT', 'MTPA']:
            conv_factor = 1.0
        else:
            conv_factor = float(self.mining_units(data_unit, 'MMT'))
            data_unit = 'MMT'
            data_value = float(data_value) * conv_factor
        self.curr.execute('SELECT param_value FROM mining_model_rules WHERE param_name="INFERRED_TO_TOTAL"')
        inferred_factor = self.curr.fetchone()[0]
        if inferred_factor:
            total_value = float(data_value) / float(inferred_factor)
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'inferred_factor:', inferred_factor
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'inferred resources:', data_value
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'estimated total resources:', total_value
        self.curr.execute('UPDATE mining_param_track SET inferredToTotal=%s WHERE NewMineId=%s AND sessionKey=%s',(inferred_factor, self.NewMineId, self.mSession_key))
        self.curr.execute('COMMIT')
        return total_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def convert_to_total(self, data_table, data_type, last_data):
        '''Convert reserve and resource data to estimated total values'''
        total_value = 0

        if data_table == 'reserves':
            if data_type == 'probable':
                total_value = self.probable_to_total(last_data)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  'total_value (probable_to_total):', total_value

            elif data_type == 'proved':
                total_value = self.proved_to_total(last_data)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  'total_value (proved_to_total):', total_value

            elif data_type == 'metal':
                total_value = self.metal_to_total(data_table, last_data)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  'total_value (metal_to_total):', total_value

        elif data_table == 'resource':
            if data_type == 'measured':
                total_value = self.measured_to_total(last_data)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  'total_value (measured_to_total):', total_value

            elif data_type == 'indicated':
                total_value = self.indicated_to_total(last_data)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  'total_value (indicated_to_total):', total_value

            elif data_type == 'inferred':
                total_value = self.inferred_to_total(last_data)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  'total_value (inferred_to_total):', total_value

            elif data_type == 'metal':
                total_value = self.metal_to_total(data_table, last_data)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  'total_value (metal_to_total):', total_value

        return total_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def convert_to_rom(self, data_type, last_data):
        '''Convert production and capacity data to estimated ROM values'''
        rom_value = 0

        if data_type == 'metal':
            rom_value = self.metal_to_rom(last_data)
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  'rom_value (metal_to_rom):', rom_value

        elif data_type == 'sale':
            rom_value = self.saleable_to_rom(last_data)
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  'rom_value (saleable_to_rom):', rom_value

        elif data_type == 'ore':
            rom_value = self.ore_to_rom(last_data)
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  'rom_value (ore_to_rom):', rom_value

        return rom_value
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def update_forecast(self):
        # --------------------------------------------------------
        #
        #  Connection string to local data
        # --------------------------------------------------------
        
        userName = getpass.getuser()
        
        mysqlHost = 'localhost'
        mysqlUser = 'root'
        mysqlPassword = 'OilAndGas321'
        mysqlDB = 'MiningEngineExtract'
        connLocal = pymysql.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPassword, db=mysqlDB, charset='utf8',use_unicode=True)
        curr = connLocal.cursor()
        curr.execute("USE MiningEngineExtract")

        # --------------------------------------------------------
        #
        #  Connection string to SQL SERVER
        # --------------------------------------------------------
        print '%s - %s:' % (self.NewMineId, self.mining_section),  'Connecting to SQL server ...'

        # conn = pypyodbc.connect('Driver={SQL Server}; Server=115.112.83.122\energy,1450; Database=MiningEngineextract; uid=ogtest;pwd=Pass@3$58')
        conn = pypyodbc.connect('Driver={SQL Server}; Server=(local); Database=MiningEngineextract; Trusted_Connection=True; unicode_results=True;')
        mCur = conn.cursor()
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        #  MINING ASSET FORECAST
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        # Open the remote site table mining_asstes_daily
        # 1 - truncate the table
        # 2 - Count the number of records to be updated
        # 3 - Update from local to remote table
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # 1
        truncate_table(mCur, 'mining_assets_forecast')
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # 2
        mSQLWhereExtra = ""

        sql_statement = "SELECT count(*) from Mining_Assets_Forecast "

        curr.execute(sql_statement)
        r1 = curr.fetchall()
        for datarow in r1:
            mTotRecs = datarow[0]

        # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewMineid,Mineid,mineName,mineCountry,state,mineRegion,mineStage,commodities,mineType,mineMethod,projectType,mineSubStage,mineSubStageStatus,totalMineLife,mineEndYear,'
        mFields += 'mineAcreageHectares,mineDepth,prefeasibilityStartYear,prefeasibilityStartQuarter,feasibilityStartYear,feasibilityStartQuarter,constructionStartYear,constructionStartQuarter,'
        mFields += 'originalProductionStartYear,originalProductionStartQuarter,actualProductionStartYear,actualProductionStartQuarter,plannedProductionStartYear,plannedProductionStartQuarter,'
        mFields += 'mineLocationSource,remainingMineLife,remainingMineLifeYear,MineAcreageSource,ActualProductionStartYearSource,TotalMineLifeSource,RemainingMineLifeSource,'
        mFields += 'MineEndYearSource,estimated_total_recoverable_reserves'

        sql_statement = 'SELECT %s FROM Mining_Assets_Forecast ORDER BY Newmineid ' % mFields

        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
            print '%s - %s:' % (self.NewMineId, self.mining_section),  ''
        curr.execute(sql_statement)
        recsProcessed = 0
        asset_forecast_data = curr.fetchall()

        # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewMineID,MineID,MineName,MineCountry,State,MineRegion,MineStage,Commodities,MineType,MineMethod,ProjectType,MineSubStage,MineSubStageStatus,TotalMineLife,MineEndYear,'
        mFields += 'MineAcreageHectares,[MineDepth(Meters)],PrefeasibilityStartYear,PrefeasibilityStartQuarter,FeasibilityStartYear,FeasibilityStartQuarter,ConstructionStartYear,ConstructionStartQuarter,'
        mFields += 'OriginalProductionStartYear,OriginalProductionStartQuarter,ActualProductionStartYear,ActualProductionStartQuarter,PlannedProductionStartYear,PlannedProductionStartQuarter,'
        mFields += 'MineLocationSource,remainingMineLife,remainingMineLifeYear,MineAcreageSource,ActualProductionStartYearSource,TotalMineLifeSource,RemainingMineLifeSource,'
        mFields += 'MineEndYearSource,estimated_total_recoverable_reserves,DataExtractedOn'

        eSymbol = buildMySQLin(39, "?")

        '''
        sql_statement = 'INSERT INTO dbo.mining_assets_forecast (NewMineID,MineName,MineCountry,State,MineRegion,MineStage,Commodities,MineType,MineMethod,ProjectType,MineSubStage,MineSubStageStatus,' \
                        'TotalMineLife,MineEndYear,MineAcreageHectares,[MineDepth(Meters)],PrefeasibilityStartYear,PrefeasibilityStartQuarter,FeasibilityStartYear,FeasibilityStartQuarter,ConstructionStartYear,' \
                        'ConstructionStartQuarter,OriginalProductionStartYear,OriginalProductionStartQuarter,ActualProductionStartYear,ActualProductionStartQuarter,PlannedProductionStartYear,' \
                        'PlannedProductionStartQuarter,MineLocationSource,remainingMineLife,remainingMineLifeYear,MineAcreageSource,ActualProductionStartYearSource,TotalMineLifeSource,RemainingMineLifeSource,' \
                        'MineEndYearSource,estimated_total_recoverable_reserves,DataExtractedOn) VALUES ' + eSymbol
        '''
        sql_statement = 'INSERT INTO dbo.mining_assets_forecast (%s) VALUES %s' % (mFields, eSymbol)
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement

        DataExtractedOn = st
        for datarow in asset_forecast_data:
            MineId = 0
            param_values = datarow + (DataExtractedOn,)
            mCur.execute(sql_statement, param_values)
            mCur.execute('COMMIT')
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "Table: mining_assets_forecast - " + str(round(recsProcessed / mTotRecs, 2) * 100)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        #  ERROR LOG
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        truncate_table(mCur, 'mining_error_log')
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # 2
        mSQLWhereExtra = ""
        sql_statement = "SELECT count(*) from Mining_Error_log "
        curr.execute(sql_statement)
        r1 = curr.fetchall()
        for datarow in r1:
            mTotRecs = datarow[0]

        # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewMineid,Mineid,mineName,mineCountry,mineRegion,state,mineStage,Commodities,period,comment,session_key,error_type,nParam_value,Param_value'

        sql_statement = 'SELECT %s FROM Mining_Error_log ORDER BY Newmineid ' % mFields

        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
            print '%s - %s:' % (self.NewMineId, self.mining_section),  ""
        curr.execute(sql_statement)
        recsProcessed = 0
        error_log_data = curr.fetchall()

        # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewMineID,MineID,MineName,MineCountry,MineRegion,State,MineStage,Commodities,Period,Comment,Session_key,Error_type,nParam_value,Param_value'

        eSymbol = buildMySQLin(14, "?")

        sql_statement = 'INSERT INTO Mining_Error_log (%s) VALUES %s' % (mFields, eSymbol)
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement

        DataExtractedOn = st
        for datarow in error_log_data:
            MineId = 0
            mCur.execute(sql_statement, datarow)
            mCur.execute('COMMIT')
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "Table: mining_error_log - " + str(round(recsProcessed / mTotRecs, 2) * 100)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        #  MINING RESERVES FORECAST
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        # Open the remote site table mining_production_forecast
        # 1 - truncate the table
        # 2 - Count the number of records to be updated
        # 3 - Update from local to remote table
        # mCur = conn.cursor()
        # 1
        tableType = "Reserves"
        truncate_table(mCur, "mining_" + tableType + "_forecast")
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # 2
        mSQLWhereExtra = ""
        sql_statement = "SELECT count(*) from Mining_" + tableType + "_Forecast "
        curr.execute(sql_statement)
        r1 = curr.fetchall()
        for datarow in r1:
            mTotRecs = datarow[0]

        # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewmineId,Mineid,mineName,mineCountry,state,mineRegion,mineStage,ReserveType,CommodityByReserve,ReserveYear,Reserve,ReserveUnit,source,Session_key'

        sql_statement = 'SELECT %s FROM Mining_%s_Forecast ORDER BY Newmineid ' % (mFields, tableType)

        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
            print '%s - %s:' % (self.NewMineId, self.mining_section),  ""
        curr.execute(sql_statement)
        recsProcessed = 0
        reserves_forecast_data = curr.fetchall()

        # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewMineID,MineID,MineName,MineCountry,MineRegion,State,MineStage,ReserveType,CommodityByReserve,ReserveYear,Reserve,ReserveUnit,Source,Session_key,DataExtractedOn'

        eSymbol = buildMySQLin(15, "?")

        sql_statement = "INSERT INTO Mining_%s_Forecast (%s) VALUES %s" % (tableType, mFields, eSymbol)
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement

        DataExtractedOn = st
        for datarow in reserves_forecast_data:
            MineId = 0
            param_values = datarow + (DataExtractedOn,)
            mCur.execute(sql_statement, param_values)
            mCur.execute('COMMIT')
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "Table: mining_" + tableType + "_forecast - " + str(round(recsProcessed / mTotRecs, 2) * 100)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        #  MINING RESOURCE FORECAST
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        # Open the remote site table mining_production_forecast
        # 1 - truncate the table
        # 2 - Count the number of records to be updated
        # 3 - Update from local to remote table
        # mCur = conn.cursor()
        # 1
        tableType = "Resource"
        truncate_table(mCur, "mining_" + tableType + "_forecast")
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # 2
        mSQLWhereExtra = ""
        sql_statement = "SELECT count(*) from Mining_" + tableType + "_Forecast "
        curr.execute(sql_statement)
        r1 = curr.fetchall()
        for datarow in r1:
            mTotRecs = datarow[0]

        # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewmineId,Mineid,mineName,mineCountry,state,mineRegion,mineStage,ResourceType,CommodityByResource,ResourceYear,Resource,ResourceUnit,source,Session_key'

        sql_statement = 'SELECT %s FROM Mining_%s_Forecast ORDER BY Newmineid ' % (mFields, tableType)

        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
            print '%s - %s:' % (self.NewMineId, self.mining_section),  ""
        curr.execute(sql_statement)
        recsProcessed = 0
        resource_forecast_data = curr.fetchall()

        # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewMineID,MineID,MineName,MineCountry,State,MineRegion,MineStage,ResourceType,CommodityByResource,ResourceYear,Resource,ResourceUnit,Source,Session_key,DataExtractedOn'

        eSymbol = buildMySQLin(15, "?")

        sql_statement = "INSERT INTO Mining_%s_Forecast (%s) VALUES %s" % (tableType, mFields, eSymbol)
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement

        for datarow in resource_forecast_data:
            MineId = 0
            DataExtractedOn = st
            param_values = datarow + (DataExtractedOn,)
            mCur.execute(sql_statement, param_values)
            mCur.execute('COMMIT')
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "Table: mining_" + tableType + "_forecast - " + str(round(recsProcessed / mTotRecs, 2) * 100)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        #  MINING CAPACITY FORECAST
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        # Open the remote site table mining_production_forecast
        # 1 - truncate the table
        # 2 - Count the number of records to be updated
        # 3 - Update from local to remote table
        # mCur = conn.cursor()
        # 1
        tableType = "Capacity"
        truncate_table(mCur, "mining_" + tableType + "_forecast")
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # 2
        mSQLWhereExtra = ""
        sql_statement = "SELECT count(*) from Mining_" + tableType + "_Forecast "
        curr.execute(sql_statement)
        r1 = curr.fetchall()
        for datarow in r1:
            mTotRecs = datarow[0]

        # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewmineId,Mineid,mineName,mineCountry,state,mineRegion,mineStage,CapacityType,CommodityByCapacity,CapacityYear,Capacity,CapacityUnit,source,Session_key'

        sql_statement = 'SELECT %s FROM Mining_%s_Forecast ORDER BY Newmineid ' % (mFields, tableType)

        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
            print '%s - %s:' % (self.NewMineId, self.mining_section),  ""
        curr.execute(sql_statement)
        recsProcessed = 0
        capacity_forecast_data = curr.fetchall()

        # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewMineID,MineID,MineName,MineCountry,State,MineRegion,MineStage,CapacityType,CommodityByCapacity,CapacityYear,Capacity,CapacityUnit,Source,Session_key,DataExtractedOn'

        eSymbol = buildMySQLin(15, "?")

        sql_statement = 'INSERT INTO Mining_%s_Forecast (%s) VALUES %s' % (tableType, mFields, eSymbol)
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement

        DataExtractedOn = st
        for datarow in capacity_forecast_data:
            MineId = 0
            param_values = datarow + (DataExtractedOn,)
            mCur.execute(sql_statement, param_values)
            mCur.execute('COMMIT')
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "Table: mining_" + tableType + "_forecast - " + str(round(recsProcessed / mTotRecs, 2) * 100)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        #  MINING PRODUCTION FORECAST
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        # Open the remote site table mining_production_forecast
        # 1 - truncate the table
        # 2 - Count the number of records to be updated
        # 3 - Update from local to remote table
        # mCur = conn.cursor()
        # 1
        truncate_table(mCur, 'mining_production_forecast')
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # 2
        mSQLWhereExtra = ""
        sql_statement = "SELECT count(*) from Mining_Production_Forecast "
        curr.execute(sql_statement)
        r1 = curr.fetchall()
        for datarow in r1:
            mTotRecs = datarow[0]
        #
        # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewmineId,Mineid,mineName,mineCountry,state,mineRegion,mineStage,productionType,productionByCommodity,productionYear,productionValue,productionUnit,source,session_key'

        sql_statement = 'SELECT %s FROM Mining_Production_Forecast ORDER BY Newmineid ' % mFields

        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
            print '%s - %s:' % (self.NewMineId, self.mining_section),  ""
        curr.execute(sql_statement)
        recsProcessed = 0
        production_forecast_data = curr.fetchall()

        # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
        mFields = 'NewMineID,MineID,MineName,MineCountry,State,MineRegion,MineStage,ProductionType,ProductionByCommodity,ProductionYear,ProductionValue,ProductionUnit,Source,Session_key,DataExtractedOn'

        eSymbol = buildMySQLin(15, "?")

        sql_statement = 'INSERT INTO Mining_Production_Forecast (%s) VALUES %s' % (mFields, eSymbol)
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement

        DataExtractedOn = st
        for datarow in production_forecast_data:
            MineId = 0
            param_values = datarow + (DataExtractedOn,)
            mCur.execute(sql_statement, param_values)
            mCur.execute('COMMIT')
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  "Table: mining_production_forecast - %s%% " % str(round(recsProcessed / mTotRecs, 2) * 100)

        mCur.close()
        conn.close()
        curr.close()
        connLocal.close()
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def make_local_data(self):
        # --------------------------------------------------------
        #
        #  Connection string to local data
        # --------------------------------------------------------
        userName = getpass.getuser()
        mysqlHost = 'localhost'
        mysqlUser = 'root'
        mysqlPassword = 'OilAndGas321'
        mysqlDB = 'MiningEngineExtract'
        connLocal = pymysql.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPassword, db=mysqlDB, charset='utf8', use_unicode=True)
        currLocal = connLocal.cursor()
        currLocal.execute("USE MiningEngineExtract")
        # --------------------------------------------------------
        #  Connection string to SQL SERVER
        # --------------------------------------------------------
        conn = pypyodbc.connect('Driver={SQL Server}; Server=(local); Database=MiningEngineextract; Trusted_Connection=True; unicode_results=True;')
        mCur = conn.cursor()
        # ------------------------------------------------------------------------------------
        #
        #  MINING ASSET DAILY TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mining_assets_daily'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ''
        sql_statement = "SELECT COUNT(*) FROM dbo.Mining_Assets_Daily "
        mSQLOrderBy = "ORDER BY Newmineid "
        mSQLWhere = "WHERE mineStage='Operation' %s " % mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        # --------------------------------------------------------------------
        mFields = "NewMineId,mineStage,ActualProductionStartYear,totalMineLife,remainingMineLife,"
        mFields += "MineAcreageHectares,mineName,mineCountry,state,mineRegion,"
        mFields += "commodities,mineType,mineMethod,projectType,mineSubStage,"
        mFields += "mineSubStageStatus,constructionStartYear,mineEndYear,[mineDepth(Meters)],mineLocationSource,"
        mFields += "remainingMineLifeYear,originalProductionStartYear,TotalMineLifeSource,RemainingMineLifeSource,MineEndYearSource,"
        mFields += "mineAcreageSource,ActualProductionStartYearSource,MineID"
        sql_statement = "select " + mFields + " from dbo.Mining_Assets_Daily"
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = " WHERE mineStage = 'Operation' " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()

        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        for datarow in r2:
            NewMineId = datarow[0]
            mineStage = datarow[1]
            if datarow[2] is None:
                ActualProductionStartYear = 0
            else:
                ActualProductionStartYear = datarow[2]
            if datarow[3] is None:
                totalMineLife = 0
            else:
                totalMineLife = datarow[3]
            if datarow[4] is None:
                remainingMineLife = 0
            else:
                remainingMineLife = datarow[4]
            MineAcreageHectares = datarow[5]
            mineName = datarow[6]
            mineCountry = datarow[7]
            state = datarow[8]
            mineRegion = datarow[9]
            commodities = datarow[10]
            mineType = datarow[11]
            mineMethod = datarow[12]
            projectType = datarow[13]
            mineSubStage = datarow[14]
            mineSubStageStatus = datarow[15]
            if datarow[16] is None:
                constructionStartYear = 0
            else:
                constructionStartYear = datarow[16]
            mineEndYear = datarow[17]
            mineDepth = datarow[18]
            mineLocationSource = datarow[19]
            if datarow[20] is None:
                remainingMineLifeYear = 0
            else:
                remainingMineLifeYear = datarow[20]
            originalProductionStartYear = datarow[21]
            TotalMineLifeSource = datarow[22]
            RemainingMineLifeSource = datarow[23]
            MineEndYearSource = datarow[24]
            mineAcreageSource = datarow[25]
            ActualProductionStartYearSource = datarow[26]
            MineID = datarow[27]
            if ActualProductionStartYearSource == "EST: Forecast Engine":
                ActualProductionStartYear = 0
            if MineEndYearSource == "EST: Forecast Engine":
                MineEndYear = 0
            if RemainingMineLifeSource == "EST: Forecast Engine":
                RemainingMineLife = 0
            if TotalMineLifeSource == "EST: Forecast Engine":
                TotalMineLife = 0
            if mineAcreageSource == "EST: Forecast Engine":
                MineAcreageHectares = 0
            # --------------------------------------------------------------------
            sqlStatement = "INSERT INTO mining_assets_daily (" + \
                           "NewMineId,mineStage,ActualProductionStartYear,totalMineLife,remainingMineLife," + \
                           "MineAcreageHectares,mineName,mineCountry,state,mineRegion," + \
                           "commodities,mineType,mineMethod,projectType,mineSubStage," + \
                           "mineSubStageStatus,constructionStartYear,mineEndYear,mineDepth,mineLocationSource," + \
                           "remainingMineLifeYear,originalProductionStartYear,TotalMineLifeSource,RemainingMineLifeSource,MineEndYearSource," + \
                           "mineAcreageSource,ActualProductionStartYearSource,Mineid)" + \
                           "VALUES (" + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s ) "

            currLocal.execute(sqlStatement,(NewMineId, mineStage, ActualProductionStartYear, totalMineLife, remainingMineLife, MineAcreageHectares, mineName, mineCountry, state, mineRegion, commodities,
                                            mineType, mineMethod, projectType, mineSubStage, mineSubStageStatus, constructionStartYear, mineEndYear, mineDepth, mineLocationSource, remainingMineLifeYear,
                                            originalProductionStartYear, TotalMineLifeSource, RemainingMineLifeSource, MineEndYearSource, mineAcreageSource, ActualProductionStartYearSource, MineID))
            currLocal.execute("commit;")
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)
        # ------------------------------------------------------------------------------------
        #
        #  CAPACITY TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mining_capacity_daily'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ""
        sql_statement = "select count (*) from dbo.Mining_Capacity_Daily "
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = "  " + mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        # --------------------------------------------------------------------
        mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
        mFields += "mineStage,capacityType,commodityByCapacity,capacityYear,capacity,"
        mFields += "capacityUnit,source,MineID"
        sql_statement = "select " + mFields + " from Mining_Capacity_Daily"
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = " " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()
        #
        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        for datarow in r2:
            NewMineId = datarow[0]
            mineName = datarow[1]
            mineCountry = datarow[2]
            state = datarow[3]
            mineRegion = datarow[4]
            #
            mineStage = datarow[5]
            capacityType = datarow[6]
            commodityByCapacity = datarow[7]
            capacityYear = datarow[8]
            capacity = datarow[9]
            #
            capacityUnit = datarow[10]
            source = datarow[11]
            MineID = datarow[12]
            #
            sqlStatement = "INSERT INTO mining_Capacity_daily (" + \
                           "NewMineId,mineName,mineCountry,state,mineRegion," + \
                           "mineStage,capacityType,commodityByCapacity,capacityYear,capacity," + \
                           "capacityUnit,source,Mineid) " + \
                           "VALUES (" + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s )"
            currLocal.execute(sqlStatement, (NewMineId, mineName, mineCountry, state, mineRegion, \
                                             mineStage, capacityType, commodityByCapacity, capacityYear, capacity, \
                                             capacityUnit, source, MineID))
            currLocal.execute("commit;")
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)

        # ------------------------------------------------------------------------------------
        #
        #  EQUITY TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mining_equity_daily'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ""
        sql_statement = "select count (*) from dbo.Mining_Equity_Daily "
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = "  " + mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        # --------------------------------------------------------------------
        mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
        mFields += "mineStage,equityPartnerStatus,equityCompany,equityPartnerStake,equityPartnerBeginningYear,"
        mFields += "source,MineID"
        sql_statement = "select " + mFields + " from Mining_equity_daily"
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = " " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()
        #
        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        for datarow in r2:
            NewMineId = datarow[0]
            mineName = datarow[1]
            mineCountry = datarow[2]
            state = datarow[3]
            mineRegion = datarow[4]
            #
            mineStage = datarow[5]
            equityPartnerStatus = datarow[6]
            equityCompany = datarow[7]
            equityPartnerStake = datarow[8]
            equityPartnerBeginningYear = datarow[9]
            #
            source = datarow[10]
            MineID = datarow[11]
            #
            sqlStatement = "INSERT INTO mining_Equity_daily (" + \
                           "NewMineId,mineName,mineCountry,state,mineRegion," + \
                           "mineStage,equityPartnerStatus,equityCompany,equityPartnerStake,equityPartnerBeginningYear," + \
                           "source,MineID) " + \
                           "VALUES (" + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s )"
            currLocal.execute(sqlStatement, (NewMineId, mineName, mineCountry, state, mineRegion, \
                                             mineStage, equityPartnerStatus, equityCompany, equityPartnerStake,
                                             equityPartnerBeginningYear, \
                                             source, MineID))
            currLocal.execute("commit;")
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)
        # ------------------------------------------------------------------------------------
        #
        #  MODEL RULES TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mining_model_rules'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ""
        sql_statement = "select count (*) from dbo.Mining_Model_Rules "
        mSQLOrderBy = " order by param_name "
        mSQLWhere = "  " + mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        # --------------------------------------------------------------------
        mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
        mFields += "mineStage,mineType,mineMethod,commodity,production_total,"
        mFields += "production_peak,production_units,operators,param_name,param_value,"
        mFields += "param_table,param_range,MineID"
        sql_statement = "select " + mFields + " from Mining_Model_Rules"
        mSQLOrderBy = " order by param_name "
        mSQLWhere = " " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()
        #
        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        for datarow in r2:
            NewMineId = datarow[0]
            mineName = datarow[1]
            mineCountry = datarow[2]
            state = datarow[3]
            mineRegion = datarow[4]
            #
            mineStage = datarow[5]
            mineType = datarow[6]
            mineMethod = datarow[7]
            commodity = datarow[8]
            production_total = datarow[9]
            #
            production_peak = datarow[10]
            production_units = datarow[11]
            operators = datarow[12]
            param_name = datarow[13]
            param_value = datarow[14]
            #
            param_table = datarow[15]
            param_range = datarow[16]
            MineID = datarow[17]
            #
            sqlStatement = "INSERT INTO mining_Model_Rules (" + \
                           "NewMineId,mineName,mineCountry,state,mineRegion," + \
                           "mineStage,mineType,mineMethod,commodity,production_total," + \
                           "production_peak,production_units,operators,param_name,param_value," + \
                           "param_table,param_range,Mineid) " + \
                           "VALUES (" + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s)"
            currLocal.execute(sqlStatement, (NewMineId, mineName, mineCountry, state, mineRegion, \
                                             mineStage, mineType, mineMethod, commodity, production_total, \
                                             production_peak, production_units, operators, param_name, param_value, \
                                             param_table, param_range, MineID))
            currLocal.execute("commit;")
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)
        # ------------------------------------------------------------------------------------
        #
        #  MODEL RULES PENDING TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mining_model_rulespending'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ""
        sql_statement = "select count (*) from dbo.Mining_Model_RulesPending "
        mSQLOrderBy = " order by param_name "
        mSQLWhere = "  " + mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        # --------------------------------------------------------------------
        mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
        mFields += "mineStage,mineType,mineMethod,commodity,production_total,"
        mFields += "production_peak,production_units,operators,param_name,param_value,"
        mFields += "param_table,param_range,MineID"
        sql_statement = "select " + mFields + " from Mining_Model_RulesPending"
        mSQLOrderBy = " order by param_name "
        mSQLWhere = " " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()
        #
        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        for datarow in r2:
            NewMineId = datarow[0]
            mineName = datarow[1]
            mineCountry = datarow[2]
            state = datarow[3]
            mineRegion = datarow[4]
            #
            mineStage = datarow[5]
            mineType = datarow[6]
            mineMethod = datarow[7]
            commodity = datarow[8]
            production_total = datarow[9]
            #
            production_peak = datarow[10]
            production_units = datarow[11]
            operators = datarow[12]
            param_name = datarow[13]
            param_value = datarow[14]
            #
            param_table = datarow[15]
            param_range = datarow[16]
            MineID = datarow[17]
            #
            sqlStatement = "INSERT INTO mining_Model_RulesPending (" + \
                           "NewMineId,mineName,mineCountry,state,mineRegion," + \
                           "mineStage,mineType,mineMethod,commodity,production_total," + \
                           "production_peak,production_units,operators,param_name,param_value," + \
                           "param_table,param_range,MineID) " + \
                           "VALUES (" + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s)"
            currLocal.execute(sqlStatement, (NewMineId, mineName, mineCountry, state, mineRegion, \
                                             mineStage, mineType, mineMethod, commodity, production_total, \
                                             production_peak, production_units, operators, param_name, param_value, \
                                             param_table, param_range, MineID))
            currLocal.execute("commit;")
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)
        # ------------------------------------------------------------------------------------
        #
        #  CAPACITY DAILY TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mining_operator_daily'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ""
        sql_statement = "select count (*) from dbo.Mining_Operator_daily "
        mSQLOrderBy = " order by newmineid "
        mSQLWhere = "  " + mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        # --------------------------------------------------------------------
        mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
        mFields += "mineStage,operatorType,OperatorCompany,operatorBeginningYear,operatorSources,MineID"
        sql_statement = "select " + mFields + " from Mining_Operator_daily"
        mSQLOrderBy = " order by NewMineId "
        mSQLWhere = " " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()
        #
        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        for datarow in r2:
            NewMineId = datarow[0]
            mineName = datarow[1]
            mineCountry = datarow[2]
            state = datarow[3]
            mineRegion = datarow[4]
            #
            mineStage = datarow[5]
            operatorType = datarow[6]
            equityCompany = datarow[7]
            operatorBeginningYear = datarow[8]
            operatorSources = datarow[9]
            MineID = datarow[10]
            #
            sqlStatement = "INSERT INTO mining_Operator_daily (" + \
                           "NewMineId,mineName,mineCountry,state,mineRegion," + \
                           "mineStage,operatorType,equityCompany,operatorBeginningYear,operatorSources,Mineid) " + \
                           "VALUES (" + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," \
                           "%s )"
            currLocal.execute(sqlStatement, (NewMineId, mineName, mineCountry, state, mineRegion, \
                                             mineStage, operatorType, equityCompany, operatorBeginningYear,
                                             operatorSources, MineID))
            currLocal.execute("commit;")
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)
        # ------------------------------------------------------------------------------------
        #
        #  ORE QUALITY TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mine_ore_quality'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ""
        sql_statement = "select count (*) from dbo.Mine_Ore_Quality "
        mSQLOrderBy = " order by newmineid "
        mSQLWhere = "  " + mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        # --------------------------------------------------------------------
        mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
        mFields += "mineStage,elementName,grade,gradeUnits,source,MineID"
        sql_statement = "select " + mFields + " from Mine_ore_quality"
        mSQLOrderBy = " order by NewMineId "
        mSQLWhere = " " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()
        #
        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        for datarow in r2:
            NewMineId = datarow[0]
            mineName = datarow[1]
            mineCountry = datarow[2]
            state = datarow[3]
            mineRegion = datarow[4]
            #
            mineStage = datarow[5]
            elementName = datarow[6]
            grade = datarow[7]
            gradeUnits = datarow[8]
            source = datarow[9]
            MineID = datarow[10]
            #
            sqlStatement = "INSERT INTO Mine_Ore_Quality (" + \
                           "NewMineId,mineName,mineCountry,state,mineRegion," + \
                           "mineStage,elementName,grade,gradeUnits,source,MineID) " + \
                           "VALUES (" + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," \
                           "%s )"
            currLocal.execute(sqlStatement, (NewMineId, mineName, mineCountry, state, mineRegion, \
                                             mineStage, elementName, grade, gradeUnits, source, MineID))
            currLocal.execute("commit;")
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)
        # ------------------------------------------------------------------------------------
        #
        #  MINING PRODUCTION DAILY TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mining_production_daily'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ""
        sql_statement = "select count (*) from dbo.Mining_Production_Daily "
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = "  " + mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        # --------------------------------------------------------------------
        mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
        mFields += "mineStage,productionType,productionByCommodity,productionYear,productionValue,"
        mFields += "productionUnit,source,MineID"
        sql_statement = "select " + mFields + " from Mining_Production_Daily"
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = " " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()
        #
        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        for datarow in r2:
            NewMineId = datarow[0]
            mineName = datarow[1]
            mineCountry = datarow[2]
            state = datarow[3]
            mineRegion = datarow[4]
            #
            mineStage = datarow[5]
            productionType = datarow[6]
            productionByCommodity = datarow[7]
            productionYear = datarow[8]
            productionValue = datarow[9]
            #
            productionUnit = datarow[10]
            source = datarow[11]
            MineID = datarow[12]
            #
            sqlStatement = "INSERT INTO Mining_Production_Daily (" + \
                           "NewMineId,mineName,mineCountry,state,mineRegion," + \
                           "mineStage,productionType,productionByCommodity,productionYear,productionValue," + \
                           "productionUnit,source,Mineid) " + \
                           "VALUES (" + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s )"
            currLocal.execute(sqlStatement, (NewMineId, mineName, mineCountry, state, mineRegion, \
                                             mineStage, productionType, productionByCommodity, productionYear,
                                             productionValue, \
                                             productionUnit, source, MineID))
            currLocal.execute("commit;")
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)
        # ------------------------------------------------------------------------------------
        #
        #  MINING RESERVES DAILY TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mining_reserves_daily'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ""
        sql_statement = "select count (*) from dbo.Mining_Reserves_Daily "
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = "  " + mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        # --------------------------------------------------------------------
        mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
        mFields += "mineStage,reserveType,commodityByReserve,reserveYear,reserve,"
        mFields += "reserveUnit,source,MineID"
        sql_statement = "select " + mFields + " from Mining_Reserves_Daily"
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = " " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()
        #
        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        for datarow in r2:
            NewMineId = datarow[0]
            mineName = datarow[1]
            mineCountry = datarow[2]
            state = datarow[3]
            mineRegion = datarow[4]
            #
            mineStage = datarow[5]
            reserveType = datarow[6]
            if datarow[7] is not None:
                commodityByReserve = datarow[7].strip()[:50]
            else:
                commodityByReserve = ""
            reserveYear = datarow[8]
            reserve = datarow[9]
            #
            reserveUnit = datarow[10]
            source = datarow[11]
            MineID = datarow[12]
            #
            sqlStatement = "INSERT INTO Mining_Reserves_Daily (" + \
                           "NewMineId,mineName,mineCountry,state,mineRegion," + \
                           "mineStage,reserveType,commodityByReserve,reserveYear,reserve," + \
                           "reserveUnit,source,Mineid) " + \
                           "VALUES (" + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s )"
            currLocal.execute(sqlStatement, (NewMineId, mineName, mineCountry, state, mineRegion, \
                                             mineStage, reserveType, commodityByReserve, reserveYear, reserve, \
                                             reserveUnit, source, MineID))
            currLocal.execute("commit;")
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)
        # ------------------------------------------------------------------------------------
        #
        #  MINING RESOURCES DAILY TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mining_resource_daily'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ""
        sql_statement = "select count (*) from dbo.Mining_Resource_Daily "
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = "  " + mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        print '%s - %s:' % (self.NewMineId, self.mining_section),  r1
        print '%s - %s:' % (self.NewMineId, self.mining_section),  mTotRecs
        # --------------------------------------------------------------------
        mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
        mFields += "mineStage,resourceType,commodityByResource,resourceYear,resource,"
        mFields += "resourceUnit,source,MineID"
        sql_statement = "select " + mFields + " from Mining_Resource_Daily"
        mSQLOrderBy = " order by Newmineid "
        mSQLWhere = " " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()
        #
        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        for datarow in r2:
            NewMineId = datarow[0]
            mineName = datarow[1]
            mineCountry = datarow[2]
            state = datarow[3]
            mineRegion = datarow[4]
            #
            mineStage = datarow[5]
            resourceType = datarow[6]
            commodityByResource = datarow[7]
            resourceYear = datarow[8]
            resource = datarow[9]
            #
            resourceUnit = datarow[10]
            source = datarow[11]
            MineID = datarow[12]
            #
            sqlStatement = "INSERT INTO Mining_Resource_Daily (" + \
                           "NewMineId,mineName,mineCountry,state,mineRegion," + \
                           "mineStage,resourceType,commodityByResource,resourceYear,resource," + \
                           "resourceUnit,source,MineID) " + \
                           "VALUES (" + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s, %s, %s," + \
                           "%s, %s, %s )"
            currLocal.execute(sqlStatement, (NewMineId, mineName, mineCountry, state, mineRegion, \
                                             mineStage, resourceType, commodityByResource, resourceYear, resource, \
                                             resourceUnit, source, MineID))
            currLocal.execute("commit;")
            #                print '%s - %s:' % (self.NewMineId, self.mining_section),  "Table: mining_reserves_daily - " + str(round(recsProcessed / mTotRecs, 2) * 100)

            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)

        # ------------------------------------------------------------------------------------
        #
        #  MINING MACHINERY DAILY TABLE
        # --------------------------------------------------------------------------------------
        # wipe out the existing DB
        table_name = 'mining_machinery_daily'
        truncate_table(currLocal, table_name)
        mSQLWhereExtra = ""
        sql_statement = "SELECT COUNT(*) from dbo.Mining_Machinery_Daily "
        mSQLOrderBy = " ORDER BY Newmineid "
        mSQLWhere = "  " + mSQLWhereExtra
        sql_statement += mSQLWhere
        mCur.execute(sql_statement)
        r1 = mCur.fetchall()
        for datarow in r1:
            mTotRecs = float(datarow[0])
        print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement
        print '%s - %s:' % (self.NewMineId, self.mining_section),  r1
        print '%s - %s:' % (self.NewMineId, self.mining_section),  mTotRecs
        # --------------------------------------------------------------------
        mFields  = "NewMineId, MineID, MineName, MineCountry, State, MineRegion, mineStage, MachineryType, EquipmentType, "
        mFields += "Make, Model, SizeClass, EquipmentCost, NumberInstalled, EquipmentVintage, EquipmentVintageSource, "
        mFields += "EstimatedReplacementTiming, EstimatedAdditionsNumber, EstimatedAdditionsYear, ReportedYear, Source "
        sql_statement = "SELECT " + mFields + " from Mining_Machinery_Daily"
        mSQLOrderBy = " ORDER BY Newmineid "
        mSQLWhere = " " + mSQLWhereExtra
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur.execute(sql_statement)
        r2 = mCur.fetchall()
        #
        recsProcessed = 0.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  "*" * 25
            print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_statement

        sqlStatement = "INSERT INTO Mining_Machinery_Daily (NewMineId, MineID, MineName, MineCountry, State, MineRegion, mineStage, MachineryType, EquipmentType, "
        sqlStatement += "Make, Model, SizeClass, EquipmentCost, NumberInstalled, EquipmentVintage, EquipmentVintageSource, EstimatedReplacementTiming, "
        sqlStatement += "EstimatedAdditionsNumber, EstimatedAdditionsYear, ReportedYear, Source) "
        sqlStatement += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        for datarow in r2:
            currLocal.execute(sqlStatement, datarow)
            currLocal.execute("COMMIT")
            recsProcessed += 1
            if recsProcessed % 100 == 0:
                complete_pct = round(float(recsProcessed) / float(mTotRecs), 3) * 100.0
                print 'Importing %s - %s%% complete' % (table_name, complete_pct)
        mCur.close()
        conn.close()
        currLocal.close()
        connLocal.close()
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def update_total_factors(self):
        table_names = {
            'reserves': {'Probable Reserves': {'param_name': 'PROBABLE_TO_TOTAL'},
                         'Proved Reserves': {'param_name': 'PROVED_TO_TOTAL'}},

            'resource': {'Measured Resources': {'param_name': 'MEASURED_TO_TOTAL'},
                         'Indicated Resources': {'param_name': 'INDICATED_TO_TOTAL'},
                         'Inferred Resources': {'param_name': 'INFERRED_TO_TOTAL'}}
        }
        for data_table in table_names.keys():
            for data_type in table_names[data_table]:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  'Updating %s to total average ...' % data_type.lower()
                param_name = table_names[data_table][data_type]['param_name']
                param_value = self.get_total_factor(data_table, data_type)
                sql_insert = 'INSERT INTO mining_model_rules (NewMineId, MineId, production_total, production_peak, param_name, param_value) '
                sql_insert += 'VALUES (0, 0, 0, 0, "%s", %s)' % (param_name, param_value)
                self.curr.execute(sql_insert)
                self.curr.execute('COMMIT')
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def update_mining_ore_grade(self, clear_tbl=True, ore_data=True, comm_names=True, update_avgs=True, country_avg=True, region_avg=True, global_avg=True, ore_default=True):
        conn = get_connection(server='mysql', database='miningengineextract')
        curr = conn.cursor()
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
        if clear_tbl:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'Clearing mining_ore_table ...'
            curr.execute('TRUNCATE mining_ore_grade')
            curr.execute('COMMIT')
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
        if ore_data:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'Inserting data from mine_ore_quality table ...'
            curr.execute('SELECT NewMineId, mineCountry, mineRegion, elementName, grade, gradeUnits FROM mine_ore_quality')
            ore_quality_data = curr.fetchall()
            for mine_id, country, region, element, grade, gradeUnit in ore_quality_data:
                if '-' in grade:
                    continue
                grade = grade.replace(' ', '')
                grade = grade.replace(',', '')
                grade = grade.replace('..', '.')
                if grade[-1] == '%':
                    grade = grade[:-1]
                grade = float(grade.strip())
                if gradeUnit in ['gms/tonne', 'CPT']:
                    convFactor = float(self.mining_units(gradeUnit, '%'))
                    grade = float(grade) * float(convFactor)
                    gradeUnit = '%'
                params = (mine_id, country, region, element, grade, gradeUnit)
                curr.execute('INSERT INTO mining_ore_grade (NewMineId, mineCountry, mineRegion, elementName, oreGrade, oreGradeUnit) VALUES (%s, %s, %s, %s, %s, %s)',params)
                curr.execute('COMMIT')
            # --------------------------------------------------------------------------------------------------
            curr.execute('SELECT DISTINCT NewMineId, mineCountry, mineRegion, commodity FROM mining_ore_grade')
            ore_grade_data = curr.fetchall()
            curr.execute('SELECT NewMineId, mineCountry, mineRegion, productionByCommodity, productionValue, productionUnit FROM mining_production_daily WHERE productionType="Ore Grade" ')
            ore_prod_data = curr.fetchall()
            for mine_id, country, region, commodity, grade, gradeUnit in ore_prod_data:
                params = (mine_id, country, region, commodity, grade, gradeUnit)
                if not params in ore_grade_data:
                    if gradeUnit in ['gms/tonne', 'CPT']:
                        convFactor = float(self.mining_units(gradeUnit, '%'))
                        grade = float(grade) * float(convFactor)
                        gradeUnit = '%'
                    curr.execute('INSERT INTO mining_ore_grade (NewMineId, mineCountry, mineRegion, commodity, oreGrade, oreGradeUnit) VALUES (%s, %s, %s, %s, %s, %s)',params)
                    curr.execute('COMMIT')
            # --------------------------------------------------------------------------------------------------
            curr.execute('SELECT DISTINCT NewMineId, mineCountry, mineRegion, commodity FROM mining_ore_grade')
            ore_grade_data = curr.fetchall()
            curr.execute('SELECT NewMineId, mineCountry, mineRegion, CommodityByReserve, reserve, reserveUnit FROM mining_reserves_daily WHERE reserveType="Total Reserves - Metal Grade" ')
            ore_reserves_data = curr.fetchall()
            for mine_id, country, region, commodity, grade, gradeUnit in ore_reserves_data:
                params = (mine_id, country, region, commodity, grade, gradeUnit)
                if not params in ore_grade_data:
                    if grade:
                        if gradeUnit in ['gms/tonne', 'CPT']:
                            convFactor = float(self.mining_units(gradeUnit, '%'))
                            grade = float(grade) * float(convFactor)
                            gradeUnit = '%'
                        params = (mine_id, country, region, commodity, grade, gradeUnit)
                        curr.execute('INSERT INTO mining_ore_grade (NewMineId, mineCountry, mineRegion, commodity, oreGrade, oreGradeUnit) VALUES (%s, %s, %s, %s, %s, %s)', params)
                        curr.execute('COMMIT')
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
        if comm_names:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'Insert commodity name from mining_compounds table ...'
            curr.execute('UPDATE mining_ore_grade AS o, mining_compounds AS c SET o.commodity=c.commodity WHERE o.elementName=c.elementName')
            curr.execute('COMMIT')
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
        if update_avgs:
            curr.execute('TRUNCATE mining_ore_averages')
            curr.execute('COMMIT')
            curr.execute('INSERT INTO mining_ore_averages (mineCountry, mineRegion, commodity) (SELECT DISTINCT mineCountry, mineRegion, commodity FROM mining_ore_grade)')
            curr.execute('COMMIT')
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
        if country_avg:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'Updating average ore-grade for each commodity by country ...'
            curr.execute('SELECT DISTINCT mineCountry, commodity FROM mining_ore_grade')
            ore_country_data = curr.fetchall()
            for country, commodity in ore_country_data:
                ore_country_avg = self.get_ore_country_avg(country, commodity)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  'ore_country_avg:', ore_country_avg
                curr.execute('UPDATE mining_ore_averages SET countryAvg=%s WHERE commodity="%s" AND mineCountry="%s" ' % (ore_country_avg, commodity, country))
                curr.execute('COMMIT')
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
        if region_avg:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'Updating average ore-grade for each commodity by region ...'
            curr.execute('SELECT DISTINCT mineRegion, commodity FROM mining_ore_grade')
            ore_region_data = curr.fetchall()
            for region, commodity in ore_region_data:
                ore_region_avg = self.get_ore_region_avg(region, commodity)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  'ore_region_avg:', ore_region_avg
                curr.execute('UPDATE mining_ore_averages SET regionAvg=%s WHERE commodity="%s" AND mineRegion="%s" ' % (ore_region_avg, commodity, region))
                curr.execute('COMMIT')
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
        if global_avg:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'Updating global average ore-grade for each commodity ...'
            curr.execute('SELECT DISTINCT commodity FROM mining_ore_grade')
            ore_commodity_data = [data[0] for data in curr.fetchall()]
            for commodity in ore_commodity_data:
                ore_global_avg = self.get_ore_global_avg(commodity)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),  'ore_global_avg:', ore_global_avg
                curr.execute('UPDATE mining_ore_averages SET globalAvg=%s WHERE commodity="%s" ' % (ore_global_avg, commodity))
                curr.execute('COMMIT')
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
        if ore_default:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'Updating global average ore-grade for each commodity ...'
            commodities = []
            curr.execute('SELECT DISTINCT commodityByCapacity FROM mining_capacity_daily WHERE NOT commodityByCapacity IN (SELECT DISTINCT commodity FROM mining_ore_averages)')
            capacity_comms = [data[0] for data in curr.fetchall()]
            commodities += capacity_comms
            curr.execute('SELECT DISTINCT productionByCommodity FROM mining_production_daily WHERE NOT productionByCommodity IN (SELECT DISTINCT commodity FROM mining_ore_averages)')
            production_comms = [data[0] for data in curr.fetchall()]
            commodities += production_comms
            commodities = list(set(commodities))
            ore_grade_default = self.get_ore_grade_default()
            for commodity in commodities:
                curr.execute('INSERT INTO mining_ore_averages (commodity, globalAvg) VALUES ("%s", %s)' % (commodity, ore_grade_default))
                curr.execute('COMMIT')
        curr.close()
        conn.close()
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def update_saleable_to_rom(self):
        conn = start_database(database='miningengineextract')
        curr = conn.cursor()
        curr.execute('DELETE FROM mining_model_rules WHERE param_name="SALEABLE_PRODUCTION_YIELD_FACTOR"')
        curr.execute('COMMIT')
        sql_select = "SELECT a.productionByCommodity, a.productionValue/b.productionValue AS sale_to_rom FROM mining_production_daily AS a, mining_production_daily AS b "
        sql_select += "WHERE a.NewMineId=b.NewMineId AND a.productionType='Saleable Production' AND b.productionType='ROM Production' "
        sql_select += "AND a.productionYear=b.productionYear AND a.productionUnit=b.productionUnit "
        sql_select += "AND NOT (UCASE(a.source) LIKE 'EST:%' OR UCASE(a.source) LIKE '%ESTIMATION%' OR a.source='') "
        sql_select += "AND NOT (UCASE(b.source) LIKE 'EST:%' OR UCASE(b.source) LIKE '%ESTIMATION%' OR b.source='') "
        #
        curr.execute(sql_select)
        sale_prod_ratios = curr.fetchall()
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'sale_prod_ratios:', sale_prod_ratios
        # ----------------------------------------------------------------------------------------------------------------------------------------------------
        sql_select = "SELECT a.CommodityByCapacity, a.capacity/b.capacity AS sale_to_rom FROM mining_capacity_daily AS a, mining_capacity_daily AS b "
        sql_select += "WHERE a.NewMineId=b.NewMineId AND a.capacityType='Saleable Capacity' AND b.capacityType='ROM Capacity' "
        sql_select += "AND a.capacityYear=b.capacityYear AND a.capacityUnit=b.capacityUnit "
        sql_select += "AND NOT (UCASE(a.source) LIKE 'EST:%' OR UCASE(a.source) LIKE '%ESTIMATION%' OR a.source='') "
        sql_select += "AND NOT (UCASE(b.source) LIKE 'EST:%' OR UCASE(b.source) LIKE '%ESTIMATION%' OR b.source='') "
        #
        curr.execute(sql_select)
        sale_cap_ratios = curr.fetchall()
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'sale_cap_ratios:', sale_cap_ratios
        # ----------------------------------------------------------------------------------------------------------------------------------------------------
        commodities = list(set([data[0] for data in (sale_prod_ratios + sale_cap_ratios)]))
        saleable_ratios = {commodity: [sale_avg for (sale_comm, sale_avg) in (sale_prod_ratios + sale_cap_ratios) if sale_comm == commodity] for commodity in commodities}
        saleable_avgs = {commodity: sum(ratios) / float(len(ratios)) for (commodity, ratios) in saleable_ratios.items()}
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),  'saleable_avgs:', saleable_avgs
        for commodity, saleable_avg in saleable_avgs.items():
            sql_insert = 'INSERT INTO mining_model_rules (NewMineid, Mineid, commodity, production_total, production_peak, param_name, param_value) VALUES (0, 0, "%s", 0, 0, "SALEABLE_PRODUCTION_YIELD_FACTOR", %s)'
            sql_insert = sql_insert % (commodity.upper(), round(saleable_avg, 4))
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),  sql_insert
            curr.execute(sql_insert)
            curr.execute('COMMIT')
        curr.close()
        conn.close()
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # ========================================================================================================================================================================

    def get_mining_data(self):
        self.mining_section = 1.0
        print '%s:' % self.mining_section, self.mProgComment

        self.conn = get_connection(server='mysql', database='MiningEngineExtract')
        self.curr = self.conn.cursor()
        self.curr.execute('USE MiningEngineExtract')

        self.userName = getpass.getuser()
        # ------------------------------------------------------------------
        mSQLWhereExtra = ''
        if self.mine_list:
            mine_list_str = ','.join([str(mine_id) for mine_id in self.mine_list])
            mSQLWhereExtra += 'AND NewMineId IN (%s) ' % mine_list_str

        self.sqlExclude = 'AND NOT (UCASE(source) LIKE "EST:%" OR UCASE(source) LIKE "%ESTIMATION%" OR source="") '
    
        mFields = 'NewmineId, mineStage, ActualProductionStartYear, totalMineLife, remainingMineLife, '
        mFields += 'MineAcreageHectares, mineName, mineCountry, state, mineRegion, commodities, mineType, Mineid, '
    
        sql_statement = 'SELECT COUNT(1) FROM Mining_Assets_Daily '
    
        mSQLWhere = "WHERE mineStage = 'Operation' %s " % mSQLWhereExtra
    
        sql_statement += mSQLWhere
    
        self.mProgComment += '\n%s\n' % sql_statement
    
        self.curr.execute(sql_statement)
        self.mTotRecs = self.curr.fetchone()[0]
        self.mProgComment += '\n%s Records processsed\n' % self.mTotRecs
        self.otherFilter = " True "
        # --------------------------------------------------------------------
        forecastTables = ['Mining_Assets_Forecast', 'Mining_Production_Forecast', 'Mining_Capacity_Forecast', 'Mining_Resource_Forecast', 'Mining_Reserves_Forecast', 'Mining_Error_log', 'Mining_metrics']
        if self.removeForecast:
            for table in forecastTables:
                if self.debugMode:
                    print '%s:' % self.mining_section, 'Removing forecast data from %s ...' % table
                truncate_table(self.curr, table)
        # --------------------------------------------------------------------
        '''
        fldAssetsList2 = ['NewMineId', 'mineStage', 'ActualProductionStartYear', 'totalMineLife', 'remainingMineLife', 'MineAcreageHectares', 'mineName', 'mineCountry, state',
                          'mineRegion', 'commodities', 'mineType', 'mineMethod', 'projectType', 'mineSubStage', 'mineSubStageStatus', 'constructionStartYear', 'mineEndYear',
                          'mineDepth', 'mineLocationSource', 'remainingMineLifeYear', 'originalProductionStartYear', 'TotalMineLifeSource', 'RemainingMineLifeSource',
                          'MineEndYearSource', 'mineAcreageSource', 'ActualProductionStartYearSource', 'estimated_total_recoverable_reserves', 'Mineid']
    
        fldAssetsListDT2 = ['i','c','i','i','i','i','c','c','c','c','c','c','c','c','c','c','i','i','i','c','i','i','c','c','c','c','c','i','i']
    
        fldAssetData = {fldAssetsList2[i]: fldAssetsListDT2[i] for i in range(len(fldAssetsList2))}
        #
        '''
        fldAssets = 'NewMineId,mineStage,ActualProductionStartYear,totalMineLife,remainingMineLife,MineAcreageHectares,mineName,mineCountry,state,mineRegion,'
        fldAssets += 'commodities,mineType,mineMethod,projectType,mineSubStage,mineSubStageStatus,constructionStartYear,mineEndYear,mineDepth,mineLocationSource,'
        fldAssets += 'remainingMineLifeYear,originalProductionStartYear,TotalMineLifeSource,RemainingMineLifeSource,MineEndYearSource,mineAcreageSource,'
        fldAssets += 'ActualProductionStartYearSource,estimated_total_recoverable_reserves,Mineid,'
    
        fldAssetsDT = 'i,c,i,i,i,i,c,c,c,c,c,c,c,c,c,c,i,i,i,c,i,i,c,c,c,c,c,i,i,'
    
        # --------------------------------------------------------------------
        # Turn the line into a list
        commas = fldAssets.count(",")
        fldAssets2 = fldAssets
        fldAssetsDT2 = fldAssetsDT
        for i in range(commas):
            pos = fldAssets2.index(",")
            self.fldAssetsList.append(fldAssets2[:pos])
            fldAssets2 = fldAssets2[pos + 1:]
            #
            posDT = fldAssetsDT2.index(",")
            self.fldAssetsListDT.append(fldAssetsDT2[:posDT])
            fldAssetsDT2 = fldAssetsDT2[posDT + 1:]
        mFields = ""
        for i in range(len(self.fldAssetsList)):
            mFields += self.fldAssetsList[i] + ","
        # Remove last comma
        mFields = mFields[:-1]
        sql_statement = "SELECT %s FROM Mining_Assets_Daily " % (mFields,)
        mSQLWhere = "WHERE mineStage = 'Operation' %s" % mSQLWhereExtra
        mSQLOrderBy = "ORDER BY Newmineid "
        sql_statement += mSQLWhere + mSQLOrderBy
        if self.debugMode:
            print '%s:' % self.mining_section, "*" * 50
            print '%s:' % self.mining_section, sql_statement
        self.curr.execute(sql_statement)
        self.mining_data = self.curr.fetchall()
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def initialize_mining_variables(self, datarow):
        self.mining_section = '2.0.0'
        self.NewMineId = int(datarow[0])
    
        if datarow[28]:
            self.Mineid = int(datarow[28])
    
        print '%s - %s:' % (self.NewMineId, self.mining_section),    "=-=" * 50
        print '%s - %s:' % (self.NewMineId, self.mining_section),    'NewMineID:', self.NewMineId

        self.mines = {'Mine id': [],
                     'Start year': [],
                     'Mine life': [],
                     'Remaining life': [],
                     'Acreage': [],
                     'Reserve type': [],
                     'Reserve year': [],
                     'Reserves': [],
                     'Reserve unit': [],
                     'Capacity type': [],
                     'Capacity year': [],
                     'Capacity': [],
                     'Capacity unit': [],
                     'Production Type': [],
                     'Production Year': [],
                     'Production Value': [],
                     'Production unit': [],
                     'Resource Type': [],
                     'Commodity': [],
                     'Resource Year': [],
                     'Resource %': [],
                     'Resource unit': [],
                     'Production Source': [],
                     'Resource Source': [],
                     'Capacity Source': [],
                     'Reserves Source': [],
                     'Production Source': []
                     }
        self.error_log = [['Mine id'], ['Period'], ['Comment'], ['Session_key'], ['Error type'], ['Error Param'], ['Error Value']]
        #
        self.mining_section = 0
        self.years_to_project = 0
        self.maxProduction = 0
        self.max_additional_production = 20
        self.mTotalProduction = 0
        self.origCalcMaxProduction = 0
        self.metal_comm = ''
        self.thisWasModelled = True
        self.mCommodities = datarow[10]
        self.convertFactor = float(1)
        self.mOperators = ''
        self.generate_history = False
        self.generate_forecast = False
        self.generated_hist = False
        self.generated_FC = False
        self.recovery_rate = 0
        self.historical_years = 0
        self.forecast_years = 0
        self.lastProd = 0
        self.newProd = 0
        self.newProdUnit = ''
        self.lastProdUnit = ''
        self.lastProdType = ''
        self.APSY, self.MEY, self.TML, self.RML = (True,) * 4
        self.RMLY = False
        self.firstType1, self.firstType2, self.firstType3 = (False,)*3
        self.pt_ran, self.octr_ran, self.rr_ran = (False,)*3
        #
        self.last_data = {
            'capacity': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'ore_capacity': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'sale_capacity': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'metal_capacity': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
    
            'reserves': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'prob_reserves': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'prov_reserves': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'metal_reserves': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
    
            'resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'meas_resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'ind_resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'inf_resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'metal_resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
    
            'production': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'metal_production': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'ore_production': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'sale_production': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'overburden': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''}
        }
        #
        self.createdMetalProduction = False
        self.romProductionFound, self.productionFound, self.metalProductionFound, self.oreProductionFound, self.overburdenFound, self.saleProductionFound = (False,)*6
        self.resourcesFound, self.totalResourcesFound, self.measResourcesFound, self.indResourcesFound, self.infResourcesFound, self.metalResourcesFound = (False,)*6
        self.capacityFound, self.romCapacityFound, self.metalCapacityFound, self.oreCapacityFound, self.saleCapacityFound = (False,)*5
        self.reservesFound, self.totalReservesFound, self.provReservesFound, self.probReservesFound, self.metalReservesFound = (False,)*5
        #
        self.first_reserve_type, self.first_reserve_unit, self.first_capacity_type, self.first_capacity_unit = ("",)*4
        self.last_reserve_type, self.last_reserve_unit, self.last_capacity_type, self.last_capacity_unit, self.last_ore_type, self.last_ore_unit = ("",)*6
        self.first_reserve_year, self.first_reserve_amt, self.first_capacity_year, self.first_capacity_amt, self.first_ore_cap = (0,)*5
        self.last_reserve_year, self.last_reserve_amt, self.last_capacity_year, self.last_capacity_amt, self.last_ore_year, self.last_ore_cap = (0,)*6
        #
        self.mineStage, self.startYear, self.mineLife, self.remainingLife, self.acreage, self.mineName, self.mineCountry, self.state, self.mineRegion = datarow[1:10]
        self.commodities, self.mineType, self.mineMethod, self.projectType, self.mineSubStage, self.mineSubStageStatus, self.constructionStartYear = datarow[10:17]
        self.mineEndYear, self.mineDepth, self.mineLocationSource,self.remainingMineLifeYear, self.originalProductionStartYear, self.TotalMineLifeSource = datarow[17:23]
        self.RemainingMineLifeSource, self.MineEndYearSource, self.mineAcreageSource, self.ActualProductionStartYearSource = datarow[23:27]
        self.mineStatus, self.ActualProductionStartYear, self.totalMineLife, self.remainingMineLife, self.MineAcreageHectares = datarow[1: 6]

        self.estimated_total_recoverable_reserves = 0
        self.lastYear = 0

        if self.MineAcreageHectares:
            mComment = "MINE ACREAGE PROVIDED WITHOUT SOURCE"
            self.error_log[0].append(self.NewMineId)
            self.error_log[1].append(0)
            self.error_log[2].append(mComment)
            self.error_log[3].append(self.mSession_key)
            self.error_log[4].append("ERROR TYPE 31")
            self.error_log[5].append("")
            self.error_log[6].append(self.MineAcreageHectares)
        #
        if self.mineAcreageSource is None:
            self.mineAcreageSource = ""
    
        if "EST:" in self.mineAcreageSource or "ESTIMATI" in self.mineAcreageSource.upper():
            self.MineAcreageHectares = 0
            self.mineAcreageSource = ""
    
        param_vals = (self.NewMineId, self.Mineid, self.mineName, self.mineCountry, self.mineRegion, self.mSession_key)
        self.curr.execute('INSERT INTO mining_param_track (NewMineId, MineId, mineName, mineCountry, mineRegion, sessionKey) VALUES (%s, %s, %s, %s, %s, %s)', param_vals)
        self.curr.execute('COMMIT')
    
        self.mines['Mine id'].append(self.NewMineId)
        self.mines['Start year'].append(self.startYear)
        self.mines['Mine life'].append(self.mineLife)
        self.mines['Remaining life'].append(self.remainingLife)
        self.mines['Acreage'].append(self.acreage)
    
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "-" * 40
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "Session key: " + str(self.mSession_key)
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "ID: " + str(self.NewMineId), pws("- Start Year: " + str(self.startYear), 18), pws("- Mine Life: " + str(self.mineLife), 18, 'R'), \
                pws("- Remaining: " + str(self.remainingLife), 18, 'R'), pws("- Acreage: " + str(self.acreage), 18, 'R'), " - Commodities: " + self.mCommodities

        self.commod_list = []
        self.key_commodity = ''
        self.extraWhere = ''
        self.extraVars = ''
        self.baseU = ''
        self.resources_to_reserves = 0
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_equity_data(self):
        self.mining_section = '3.0.0'
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'Processing equity data ...'
        
        mCFields = 'newMineId, mineName, operatorType, '
        mCFields += 'equityCompany, '
        mCFields += 'operatorBeginningYear '
    
        sql_statement = 'SELECT %s FROM Mining_Operator_daily ' % (mCFields,)
        sql_statement += 'WHERE newmineId = %s ORDER BY operatorBeginningYear DESC ' % self.NewMineId
        self.curr.execute(sql_statement)
        equity_data = self.curr.fetchall()
        #
        oneFoundEquity = False
        for datarow in equity_data:
            self.mining_section = '3.1.0'
            if not oneFoundEquity:
                self.mining_section = '3.1.1'
                operatorType = datarow[2]
                if datarow[3] is None:
                    equityCompany = ""
                else:
                    equityCompany = datarow[3]
                self.mOperators = equityCompany
                operatorBeginningYear = datarow[4]
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    " ** OPERATOR ** " + self.mOperators
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                oneFoundEquity = True
        
        temp_commod = self.mCommodities
        num_commod = self.mCommodities.count(";")
        begin = 0
        for ii in range(num_commod):
            pos = temp_commod.index(";")
            self.commod_list.append(temp_commod[0:pos])
            temp_commod = temp_commod[pos + 1:]

        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'commod_list, len(commod_list):', self.commod_list, len(self.commod_list)
        if len(self.commod_list) == 1:
            key = self.commod_list[ii]
        else:
            key = "Multi Commodity"
        self.mining_section = '3.2.0'
        self.key_commodity = key
        if key in self.all_commodities:
            self.all_commodities[self.key_commodity] += 1
        else:
            self.all_commodities[self.key_commodity] = 1
            self.not_modelled_commod[self.key_commodity] = 0
            self.modelled_commod[self.key_commodity] = 0

        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'all_commodities:', self.all_commodities
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "$" * 30
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "BASE UNIT (equity)"
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'baseU:', self.baseU

        if self.baseU == "" or len(self.baseU.strip()) == 0:
            self.mining_section = '3.2.1'
            self.baseU = "MMT"
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_reserves_data(self):
        self.mining_section = '4.0.0'
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'Processing reserves data ...'
    
        reserves_data = ()
        total_reserves_data = ()
        prob_reserves_data = ()
        prov_reserves_data = ()
        metal_reserves_data = ()

        # *&* Check for metal reserves even if higher level reserves are found
        self.mining_section = '4.1.0'
        total_reserves_data = self.get_asset_data('reserves', 'Total Reserves')
        if total_reserves_data:
            reserves_data = total_reserves_data
            self.totalReservesFound = True
            self.reservesFound = True
        else:
            prob_reserves_data = self.get_asset_data('reserves', 'Probable Reserves')
            if prob_reserves_data:
                reserves_data = prob_reserves_data
                self.probReservesFound = True
                self.reservesFound = True
            else:
                prov_reserves_data = self.get_asset_data('reserves', 'Proved Reserves')
                if prob_reserves_data:
                    reserves_data = prob_reserves_data
                    self.provReservesFound = True
                    self.reservesFound = True
                else:
                    metal_reserves_data = self.get_asset_data('reserves', 'Pure Metal Total Reserves')
                    if metal_reserves_data:
                        #*&* Allow for list of metal commodities to be forecasted
                        self.metal_comm = self.get_metal_commodity('reserves')
                        reserves_data = [data for data in metal_reserves_data if data[2] == self.metal_comm]
                        self.metalReservesFound = True
                        self.reservesFound = True
    
        firstTime = True
        firstTotalReserves = True
    
        for datarow in reserves_data:
            self.mining_section = '4.2.0'
            self.reservesFound = True
            reserveType = datarow[1]
            reserveCommodity = datarow[2]
            reserves = datarow[3]
            reserveYear = datarow[4]
            reserveUnit = datarow[5]
            reserveSource = datarow[6]
    
            if self.baseU == reserveUnit:
                self.mining_section = '4.2.1'
                if self.debugMode or self.debugReserves:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "BASE U = reserveUnit"
                    pass
            elif self.baseU == "MMT" and reserveUnit == "MTPA":
                self.mining_section = '4.2.1'
                if self.debugMode or self.debugReserves:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "MMT = MTPA #########"
                    pass
            else:
                self.mining_section = '4.2.2'
                beforeUnit = reserveUnit
                convertFactor = self.mining_units(reserveUnit, self.baseU)
                reserveUnit = self.baseU
                reserves = float(reserves) * float(convertFactor)
                if self.debugMode or self.debugReserves:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "-=-" * 25
                    print
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'From reserve unit %s to base unit %s' % (beforeUnit, self.baseU)
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "1: Conversion Factor"
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'convertFactor:', convertFactor
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Converted reserves: %s' % reserves
            if self.convertFactor == 0:
                self.mining_section = '4.2.3'
                mComment = "CONVERSION FACTOR FROM " + reserveUnit + " TO " + self.baseU + " NOT FOUND "
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 12")
                self.error_log[5].append("")
                self.error_log[6].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
            else:
                self.convertFactor = float(self.convertFactor)

            self.mining_section = '4.3.0'
            if self.totalReservesFound:
                self.mining_section = '4.3.1'
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Total Reserves Found'
                self.last_data['reserves']['type'] = reserveType
                self.last_data['reserves']['commodity'] = reserveCommodity
                self.last_data['reserves']['year'] = reserveYear
                self.last_data['reserves']['value'] = reserves
                self.last_data['reserves']['unit'] = reserveUnit
    
            elif self.probReservesFound:
                self.mining_section = '4.3.2'
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Probable Reserves Found'

                self.last_data['prob_reserves']['type'] = reserveType
                self.last_data['prob_reserves']['commodity'] = reserveCommodity
                self.last_data['prob_reserves']['year'] = reserveYear
                self.last_data['prob_reserves']['value'] = reserves
                self.last_data['prob_reserves']['unit'] = reserveUnit
    
                reserves = self.convert_to_total('reserves', 'probable', self.last_data['prob_reserves'])
                reserveType = "Total Reserves"
                reserveSource = "EST: Engine Estimation"
    
            elif self.provReservesFound:
                self.mining_section = '4.3.3'
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Proved Reserves Found'
                self.last_data['prov_reserves']['type'] = reserveType
                self.last_data['prov_reserves']['commodity'] = reserveCommodity
                self.last_data['prov_reserves']['year'] = reserveYear
                self.last_data['prov_reserves']['value'] = reserves
                self.last_data['prov_reserves']['unit'] = reserveUnit
    
                reserves = self.convert_to_total('reserves', 'proved', self.last_data['prov_reserves'])
                reserveType = "Total Reserves"
                reserveSource = "EST: Engine Estimation"
    
            elif self.metalReservesFound:
                self.mining_section = '4.3.4'
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Metal Reserves Found'
                self.last_data['metal_reserves']['type'] = reserveType
                self.last_data['metal_reserves']['commodity'] = reserveCommodity
                self.last_data['metal_reserves']['year'] = reserveYear
                self.last_data['metal_reserves']['value'] = reserves
                self.last_data['metal_reserves']['unit'] = reserveUnit
    
                reserves = self.convert_to_total('reserves', 'metal', self.last_data['metal_reserves'])
                reserveType = "Total Reserves"
                reserveSource = "EST: Engine Estimation"

            self.mining_section = '4.4.0'

            self.mines['Reserve type'].append(reserveType)
            self.mines['Reserve year'].append(reserveYear)
            self.mines['Reserves'].append(reserves)
            self.mines['Reserve unit'].append(reserveUnit)
            self.mines['Reserves Source'].append(reserveSource)
    
            if self.debugReserves:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (reserveType, "mines['Reserve type']")
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (reserveYear, "mines['Reserve year']")
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (reserves, "mines['Reserves']")
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (reserveUnit, "mines['Reserve unit']")
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (reserveSource, "mines['Reserves Source']")
    
            if reserveType == 'Total Reserves':
                self.last_reserve_type = reserveType
                self.last_reserve_year = reserveYear
                self.last_reserve_amt = reserves
                self.last_reserve_unit = reserveUnit
                if firstTotalReserves:
                    self.first_reserve_type = reserveType
                    self.first_reserve_year = reserveYear
                    self.first_reserve_amt = reserves
                    self.first_reserve_unit = reserveUnit
                    firstTotalReserves = False
            self.mining_section = '4.5.0'
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "RESERVES (NewMineId,reserveType,reserveYear,reserves,reserveUnit)------>", self.NewMineId, reserveType, reserveYear, reserves, reserveUnit
            firstTime = False

        self.mining_section = '4.6.0'
        if self.totalReservesFound:
            last_resv = self.last_data['reserves']
            param_vals = (last_resv['type'], last_resv['commodity'], last_resv['year'], last_resv['value'], last_resv['unit'], self.NewMineId, self.mSession_key)
            sql_update = 'UPDATE mining_param_track SET lastReservesType=%s,lastReservesComm=%s,lastReservesYear=%s,lastReservesVal=%s,lastReservesUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
            self.curr.execute(sql_update, param_vals)
            self.curr.execute('COMMIT')
    
        elif self.probReservesFound:
            last_resv = self.last_data['prob_reserves']
            param_vals = (last_resv['type'], last_resv['commodity'], last_resv['year'], last_resv['value'], last_resv['unit'], self.NewMineId, self.mSession_key)
            sql_update = 'UPDATE mining_param_track SET lastReservesType=%s,lastReservesComm=%s,lastReservesYear=%s,lastReservesVal=%s,lastReservesUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
            self.curr.execute(sql_update, param_vals)
            self.curr.execute('COMMIT')
    
        elif self.provReservesFound:
            last_resv = self.last_data['prov_reserves']
            param_vals = (last_resv['type'], last_resv['commodity'], last_resv['year'], last_resv['value'], last_resv['unit'], self.NewMineId, self.mSession_key)
            sql_update = 'UPDATE mining_param_track SET lastReservesType=%s,lastReservesComm=%s,lastReservesYear=%s,lastReservesVal=%s,lastReservesUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
            self.curr.execute(sql_update, param_vals)
            self.curr.execute('COMMIT')
    
        elif self.metalReservesFound:
            last_resv = self.last_data['metal_reserves']
            param_vals = (last_resv['type'], last_resv['commodity'], last_resv['year'], last_resv['value'], last_resv['unit'], self.NewMineId, self.mSession_key)
            sql_update = 'UPDATE mining_param_track SET lastReservesType=%s,lastReservesComm=%s,lastReservesYear=%s,lastReservesVal=%s,lastReservesUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
            self.curr.execute(sql_update, param_vals)
            self.curr.execute('COMMIT')
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_capacity_data(self):
        self.mining_section = '5.0.0'
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'Processing capacity data ...'
        mCFields = "newmineId,capacityType,capacityYear,capacity,capacityUnit,source,commodityByCapacity"
        sql_statement = "SELECT " + mCFields + " FROM Mining_Capacity_daily "
        sql_statement += "WHERE capacityType IN ('ROM Capacity', 'Metal Capacity', 'Ore Processed Capacity', 'Saleable Capacity') "
        sql_statement += "AND newmineId = " + str(self.NewMineId) + " " + self.sqlExclude + " ORDER BY capacityYear ASC "
        self.curr.execute(sql_statement)
        capacity_data = self.curr.fetchall()
        #
        first_ore_cap_year = 0
        first_metal_cap_year = 0
        first_sale_cap_year = 0
        #
        firstTime = True
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
            print '%s - %s:' % (self.NewMineId, self.mining_section),    sql_statement
        first_rom_data = True
        first_ore_data = True
        first_sale_data = True
        first_metal_data = True
        printCapacity = False
        for datarow in capacity_data:
            capacityType, capacityYear, capacity, capacityUnit, capacitySource, capacityCommodity = datarow[1:]
            #
            if self.baseU == capacityUnit:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "BASE U = capacityUnit"
                    pass
            elif self.baseU == "MMT" and capacityUnit == "MTPA":
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "MMT = MTPA #########"
                    pass
            else:
                self.convertFactor = 1.0
                beforeUnit = capacityUnit
                self.convertFactor = self.mining_units(capacityUnit, self.baseU)
                capacityUnit = self.baseU
                capacity = float(capacity) * float(self.convertFactor)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "-=-" * 25
                    print
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'From capacity unit %s to base unit %s' % (beforeUnit, self.baseU)
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "2: Conversion Factor"
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'convertFactor:', self.convertFactor
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Converted capacity: %s' % capacity
    
            if self.convertFactor == 0:
                mComment = "CONVERSION FACTOR FROM " + capacityUnit + " TO " + self.baseU + " NOT FOUND "
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 12")
                self.error_log[5].append("")
                self.error_log[6].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
            else:
                self.convertFactor = float(self.convertFactor)
            #
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'capacityType:', capacityType
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'capacityYear:', capacityYear
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'capacity:', capacity
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'convertFactor:', self.convertFactor
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'capacityUnit:', capacityUnit
            #
            self.mines['Capacity type'].append(capacityType)
            self.mines['Capacity year'].append(capacityYear)
            self.mines['Capacity'].append(float(capacity))
            self.mines['Capacity unit'].append(capacityUnit)
            self.mines['Capacity Source'].append(capacitySource)
    
            if capacityType == 'ROM Capacity':
                self.last_capacity_type = capacityType
                self.last_capacity_year = capacityYear
                self.last_capacity_amt = capacity
                self.last_capacity_unit = capacityUnit
                self.last_data['capacity']['type'] = capacityType
                self.last_data['capacity']['year'] = capacityYear
                self.last_data['capacity']['value'] = capacity
                self.last_data['capacity']['unit'] = capacityUnit
                printCapacity = True
                self.capacityFound = True
                if first_rom_data:
                    self.first_capacity_year = capacityYear
                    first_rom_data = False
            elif capacityType == "Saleable Capacity":
                self.last_data['sale_capacity']['type'] = capacityType
                self.last_data['sale_capacity']['year'] = capacityYear
                self.last_data['sale_capacity']['value'] = capacity
                self.last_data['sale_capacity']['unit'] = capacityUnit
                printCapacity = True
                self.saleCapacityFound = True
                if first_sale_data:
                    first_sale_cap_year = capacityYear
                    first_sale_data = False
            elif capacityType == "Ore Processed Capacity":
                self.last_ore_type = capacityType
                self.last_ore_year = capacityYear
                self.last_ore_cap = capacity
                self.last_ore_unit = capacityUnit
                self.last_data['ore_capacity']['type'] = capacityType
                self.last_data['ore_capacity']['year'] = capacityYear
                self.last_data['ore_capacity']['value'] = capacity
                self.last_data['ore_capacity']['unit'] = capacityUnit
                printCapacity = True
                self.oreCapacityFound = True
                if first_ore_data:
                    first_ore_cap_year = capacityYear
                    first_ore_data = False
            elif capacityType == "Metal Capacity":
                if self.metal_comm:
                    if capacityCommodity == self.metal_comm:
                        self.last_data['metal_capacity']['type'] = capacityType
                        self.last_data['metal_capacity']['commodity'] = capacityCommodity
                        self.last_data['metal_capacity']['year'] = capacityYear
                        self.last_data['metal_capacity']['value'] = capacity
                        self.last_data['metal_capacity']['unit'] = capacityUnit
                        printCapacity = True
                        self.metalCapacityFound = True
                        if first_metal_data:
                            first_metal_cap_year = capacityYear
                            first_metal_data = False
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'last_data[metal_capacity]:', self.last_data['metal_capacity']
                else:
                    self.metal_comm = self.get_metal_commodity('capacity')
                    if capacityCommodity == self.metal_comm:
                        self.last_data['metal_capacity']['type'] = capacityType
                        self.last_data['metal_capacity']['commodity'] = capacityCommodity
                        self.last_data['metal_capacity']['year'] = capacityYear
                        self.last_data['metal_capacity']['value'] = capacity
                        self.last_data['metal_capacity']['unit'] = capacityUnit
                        printCapacity = True
                        self.metalCapacityFound = True
                        if first_metal_data:
                            first_metal_cap_year = capacityYear
                            first_metal_data = False
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'last_data[metal_capacity]:', self.last_data['metal_capacity']
    
        if self.capacityFound:
            last_cap = self.last_data['capacity']
            param_vals = (last_cap['type'], last_cap['commodity'], last_cap['year'], last_cap['value'], last_cap['unit'], self.NewMineId, self.mSession_key)
            self.curr.execute('UPDATE mining_param_track SET lastCapacityType=%s,lastCapacityComm=%s,lastCapacityYear=%s,lastCapacityVal=%s,lastCapacityUnit=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
    
        elif self.saleCapacityFound:
            last_cap = self.last_data['sale_capacity']
            param_vals = (last_cap['type'], last_cap['commodity'], last_cap['year'], last_cap['value'], last_cap['unit'], self.NewMineId, self.mSession_key)
            self.curr.execute('UPDATE mining_param_track SET lastCapacityType=%s,lastCapacityComm=%s,lastCapacityYear=%s,lastCapacityVal=%s,lastCapacityUnit=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
            rom_capacity = self.convert_to_rom('sale', self.last_data['sale_capacity'])
            self.last_capacity_type = 'ROM Capacity'
            self.last_capacity_year = self.last_data['sale_capacity']['year']
            self.last_capacity_amt = rom_capacity
            self.last_capacity_unit = 'MMT'
            self.last_data['capacity']['type'] = 'ROM Capacity'
            self.last_data['capacity']['year'] = self.last_data['sale_capacity']['year']
            self.last_data['capacity']['value'] = rom_capacity
            self.last_data['capacity']['unit'] = 'MMT'
            self.mines['Capacity type'].append('ROM Capacity')
            self.mines['Capacity year'].append(self.last_data['sale_capacity']['year'])
            self.mines['Capacity'].append(float(rom_capacity))
            self.mines['Capacity unit'].append('MMT')
            self.mines['Capacity Source'].append('EST: Engine Estimation')
            self.first_capacity_year = first_sale_cap_year
            self.capacityFound = True
    
        elif self.oreCapacityFound:
            last_cap = self.last_data['ore_capacity']
            param_vals = (last_cap['type'], last_cap['commodity'], last_cap['year'], last_cap['value'], last_cap['unit'], self.NewMineId, self.mSession_key)
            self.curr.execute('UPDATE mining_param_track SET lastCapacityType=%s,lastCapacityComm=%s,lastCapacityYear=%s,lastCapacityVal=%s,lastCapacityUnit=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
            rom_capacity = self.convert_to_rom('ore', self.last_data['ore_capacity'])
            self.last_capacity_type = 'ROM Capacity'
            self.last_capacity_year = self.last_data['ore_capacity']['year']
            self.last_capacity_amt = rom_capacity
            self.last_capacity_unit = 'MMT'
            self.last_data['capacity']['type'] = 'ROM Capacity'
            self.last_data['capacity']['year'] = self.last_data['ore_capacity']['year']
            self.last_data['capacity']['value'] = rom_capacity
            self.last_data['capacity']['unit'] = 'MMT'
            self.mines['Capacity type'].append('ROM Capacity')
            self.mines['Capacity year'].append(self.last_data['ore_capacity']['year'])
            self.mines['Capacity'].append(float(rom_capacity))
            self.mines['Capacity unit'].append('MMT')
            self.mines['Capacity Source'].append('EST: Engine Estimation')
            self.first_capacity_year = first_ore_cap_year
            self.capacityFound = True
    
        elif self.metalCapacityFound:
            last_cap = self.last_data['metal_capacity']
            param_vals = (last_cap['type'], last_cap['commodity'], last_cap['year'], last_cap['value'], last_cap['unit'], self.NewMineId, self.mSession_key)
            self.curr.execute('UPDATE mining_param_track SET lastCapacityType=%s,lastCapacityComm=%s,lastCapacityYear=%s,lastCapacityVal=%s,lastCapacityUnit=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
            rom_capacity = self.convert_to_rom('metal', self.last_data['metal_capacity'])
            self.last_capacity_type = 'ROM Capacity'
            self.last_capacity_year = self.last_data['metal_capacity']['year']
            self.last_capacity_amt = rom_capacity
            self.last_capacity_unit = 'MMT'
            self.last_data['capacity']['type'] = 'ROM Capacity'
            self.last_data['capacity']['year'] = self.last_data['metal_capacity']['year']
            self.last_data['capacity']['value'] = rom_capacity
            self.last_data['capacity']['unit'] = 'MMT'
            self.mines['Capacity type'].append('ROM Capacity')
            self.mines['Capacity year'].append(self.last_data['metal_capacity']['year'])
            self.mines['Capacity'].append(float(rom_capacity))
            self.mines['Capacity unit'].append('MMT')
            self.mines['Capacity Source'].append('EST: Engine Estimation')
            self.first_capacity_year = first_metal_cap_year
            self.capacityFound = True
    
        # get the capacity info for the last year
        if self.debugMode and printCapacity:
            if firstTime and self.debugSQL:
                firstTime = False
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'CAPACITY:'
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '(NewMineId,last_capacity_type,last_capacity_year,last_capacity_amt,last_capacity_unit):', self.NewMineId, self.last_capacity_type, self.last_capacity_year, self.last_capacity_amt, self.last_capacity_unit
            if self.last_ore_cap > 0:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'ORE CAPACITY:'
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '(NewMineId,last_ore_type,last_ore_year,last_ore_cap,last_ore_unit):', self.NewMineId, self.last_ore_type, self.last_ore_year, self.last_ore_cap, self.last_ore_unit
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_resource_data(self):
        self.mining_section = 6.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'Processing resource data ...'
    
        resource_data = ()
        total_resource_data = ()
        meas_resource_data = ()
        ind_resource_data = ()
        inf_resource_data = ()
        metal_resource_data = ()
    
        total_resource_data = self.get_asset_data('resource', 'Total Resources')
        if total_resource_data:
            resource_data = total_resource_data
            self.totalResourcesFound = True
            self.resourcesFound = True
        else:
            meas_resource_data = self.get_asset_data('resource', 'Measured Resources')
            if meas_resource_data:
                resource_data = meas_resource_data
                self.measResourcesFound = True
                self.resourcesFound = True
            else:
                ind_resource_data = self.get_asset_data('resource', 'Indicated Resources')
                if ind_resource_data:
                    resource_data = ind_resource_data
                    self.indResourcesFound = True
                    self.resourcesFound = True
                else:
                    inf_resource_data = self.get_asset_data('resource', 'Inferred Resources')
                    if inf_resource_data:
                        resource_data = inf_resource_data
                        self.infResourcesFound = True
                        self.resourcesFound = True
                    else:
                        metal_resource_data = self.get_asset_data('resource', 'Total Pure Metal Resources')
                        if metal_resource_data:
                            self.metal_comm = self.get_metal_commodity('resource')
                            resource_data = [data for data in metal_resource_data if data[2] == self.metal_comm]
                            self.metalResourcesFound = True
                            self.resourcesFound = True
    
        firstTime = True
        oneFound = False
        lastYear = 0
        for datarow in resource_data:
            self.resourcesFound = True
    
            resourceType, resourceCommodity, resource, resourceYear, resourceUnit, resourceSource = datarow[1:7]
    
            if resource is None or len(str(resource).strip()) == 0:
                resource = 0
                # flag as an error
                mComment = "INVALID DATA - RESOURCE IS BLANK"
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 16")
                self.error_log[5].append("")
                self.error_log[6].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
    
            lastYear = resourceYear
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "-=-" * 25
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "Resource: " + str(resource)
            if self.baseU == resourceUnit:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "BASE U = resourceUnit"
                    pass
            elif self.baseU == "MMT" and resourceUnit == "MTPA":
                # equivalent
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "MMT = MTPA #########"
                    pass
            else:
                # convert
                self.convertFactor = 1.0
                self.convertFactor = self.mining_units(resourceUnit, self.baseU)
                beforeUnit = resourceUnit
                resourceUnit = self.baseU
                resource = float(resource) * float(self.convertFactor)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Original resource: %s' % (float(resource) / float(self.convertFactor))
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'From resource unit %s to base unit %s' % (beforeUnit, self.baseU)
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "3: Conversion Factor"
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'convertFactor:', self.convertFactor
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Converted resource: %s' % resource
    
            if self.convertFactor == 0:
                mComment = "CONVERSION FACTOR FROM " + resourceUnit + " TO " + self.baseU + " NOT FOUND "
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 12")
                self.error_log[5].append("")
                self.error_log[6].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
            else:
                self.convertFactor = 1
                self.convertFactor = float(self.convertFactor)
    
            if self.totalResourcesFound:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Total Resources Found'
                self.last_data['resources']['type'] = resourceType
                self.last_data['resources']['commodity'] = resourceCommodity
                self.last_data['resources']['year'] = resourceYear
                self.last_data['resources']['value'] = resource
                self.last_data['resources']['unit'] = resourceUnit
    
            elif self.measResourcesFound:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Measured Resources Found'
                self.last_data['meas_resources']['type'] = resourceType
                self.last_data['meas_resources']['commodity'] = resourceCommodity
                self.last_data['meas_resources']['year'] = resourceYear
                self.last_data['meas_resources']['value'] = resource
                self.last_data['meas_resources']['unit'] = resourceUnit
    
                resource = self.convert_to_total('resource', 'measured', self.last_data['meas_resources'])
                resourceType = "Total Resources"
                resourceSource = "EST: Engine Estimation"
    
            elif self.indResourcesFound:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Indicated Resources Found'
                self.last_data['ind_resources']['type'] = resourceType
                self.last_data['ind_resources']['commodity'] = resourceCommodity
                self.last_data['ind_resources']['year'] = resourceYear
                self.last_data['ind_resources']['value'] = resource
                self.last_data['ind_resources']['unit'] = resourceUnit
    
                resource = self.convert_to_total('resource', 'indicated', self.last_data['ind_resources'])
                resourceType = "Total Resources"
                resourceSource = "EST: Engine Estimation"
    
            elif self.infResourcesFound:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Inferred Resources Found'
                self.last_data['inf_resources']['type'] = resourceType
                self.last_data['inf_resources']['commodity'] = resourceCommodity
                self.last_data['inf_resources']['year'] = resourceYear
                self.last_data['inf_resources']['value'] = resource
                self.last_data['inf_resources']['unit'] = resourceUnit
    
                resource = self.convert_to_total('resource', 'inferred', self.last_data['inf_resources'])
                resourceType = "Total Resources"
                resourceSource = "EST: Engine Estimation"
    
            elif self.metalResourcesFound:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Metal Resources Found'
                self.last_data['metal_resources']['type'] = resourceType
                self.last_data['metal_resources']['commodity'] = resourceCommodity
                self.last_data['metal_resources']['year'] = resourceYear
                self.last_data['metal_resources']['value'] = resource
                self.last_data['metal_resources']['unit'] = resourceUnit
    
                resource = self.convert_to_total('resource', 'metal', self.last_data['metal_resources'])
                resourceType = "Total Resources"
                resourceSource = "EST: Engine Estimation"

            self.mines['Resource Type'].append(resourceType)
            self.mines['Commodity'].append(resourceCommodity)
            self.mines['Resource Year'].append(resourceYear)
            self.mines['Resource %'].append(float(resource))
            self.mines['Resource unit'].append(resourceUnit)
            self.mines['Resource Source'].append(resourceSource)
            oneFound = True
    
        if oneFound:
            # copy only the last year
            self.resourcesFound = True
            len_resource = len(self.mines['Resource Type'])
    
            for ii in range(len_resource):
                if self.mines['Resource Year'][ii] == lastYear:
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'ii:', ii
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'RESOURCES:'
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'NewMineId:', self.NewMineId
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Resource Type'][%s]:" % ii, self.mines['Resource Type'][ii]
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Commodity'][%s]:" % ii, self.mines['Commodity'][ii]
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Resource Year'][%s]:" % ii, self.mines['Resource Year'][ii]
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Resource %%'][%s]:" % ii, self.mines['Resource %'][ii]
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Resource unit'][%s]:" % ii, self.mines['Resource unit'][ii]
    
        if self.totalResourcesFound:
            last_resc = self.last_data['resources']
            param_vals = (last_resc['type'], last_resc['commodity'], last_resc['year'], last_resc['value'], last_resc['unit'], self.NewMineId, self.mSession_key)
            sql_update = 'UPDATE mining_param_track SET lastResourceType=%s,lastResourceComm=%s,lastResourceYear=%s,lastResourceVal=%s,lastResourceUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
            self.curr.execute(sql_update, param_vals)
            self.curr.execute('COMMIT')
    
        elif self.measResourcesFound:
            last_resc = self.last_data['meas_resources']
            param_vals = (last_resc['type'], last_resc['commodity'], last_resc['year'], last_resc['value'], last_resc['unit'], self.NewMineId, self.mSession_key)
            sql_update = 'UPDATE mining_param_track SET lastResourceType=%s,lastResourceComm=%s,lastResourceYear=%s,lastResourceVal=%s,lastResourceUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
            self.curr.execute(sql_update, param_vals)
            self.curr.execute('COMMIT')
    
        elif self.indResourcesFound:
            last_resc = self.last_data['ind_resources']
            param_vals = (last_resc['type'], last_resc['commodity'], last_resc['year'], last_resc['value'], last_resc['unit'], self.NewMineId, self.mSession_key)
            sql_update = 'UPDATE mining_param_track SET lastResourceType=%s,lastResourceComm=%s,lastResourceYear=%s,lastResourceVal=%s,lastResourceUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
            self.curr.execute(sql_update, param_vals)
            self.curr.execute('COMMIT')
    
        elif self.infResourcesFound:
            last_resc = self.last_data['inf_resources']
            param_vals = (last_resc['type'], last_resc['commodity'], last_resc['year'], last_resc['value'], last_resc['unit'], self.NewMineId, self.mSession_key)
            sql_update = 'UPDATE mining_param_track SET lastResourceType=%s,lastResourceComm=%s,lastResourceYear=%s,lastResourceVal=%s,lastResourceUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
            self.curr.execute(sql_update, param_vals)
            self.curr.execute('COMMIT')
    
        elif self.metalResourcesFound:
            last_resc = self.last_data['metal_resources']
            param_vals = (last_resc['type'], last_resc['commodity'], last_resc['year'], last_resc['value'], last_resc['unit'], self.NewMineId, self.mSession_key)
            sql_update = 'UPDATE mining_param_track SET lastResourceType=%s,lastResourceComm=%s,lastResourceYear=%s,lastResourceVal=%s,lastResourceUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
            self.curr.execute(sql_update, param_vals)
            self.curr.execute('COMMIT')
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_production_data(self):
        self.mining_section = 7.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'Processing production data ...'

        prod_data = ()
        sale_prod_data = ()
        overburden_data = ()
        ore_prod_data = ()
        metal_prod_data = ()
    
        rom_prod_data = self.get_asset_data('production', 'ROM Production')
        if rom_prod_data:
            prod_data = rom_prod_data
            self.romProductionFound = True
            self.productionFound = True
        else:
            sale_prod_data = self.get_asset_data('production', 'Saleable Production')
            if sale_prod_data:
                prod_data = sale_prod_data
                self.saleProductionFound = True
                self.productionFound = True
            else:
                # overburden_data = self.get_asset_data('production', 'Overburden')
                if overburden_data:
                    prod_data = overburden_data
                    self.overburdenFound = True
                    self.productionFound = True
                else:
                    ore_prod_data = self.get_asset_data('production', 'Ore milled/ processed')
                    if ore_prod_data:
                        prod_data = ore_prod_data
                        self.oreProductionFound = True
                        self.productionFound = True
                    else:
                        metal_prod_data = self.get_asset_data('production', 'Metal Production')
                        if metal_prod_data:
                            self.metal_comm = self.get_metal_commodity('production')
                            prod_data = [data for data in metal_prod_data if data[2] == self.metal_comm]
                            self.metalProductionFound = True
                            self.productionFound = True
    
        firstTime = True
        for prod_datarow in prod_data:
            productionType   = prod_datarow[1]
            productCommodity = prod_datarow[2]
            productionValue  = float(prod_datarow[3])
            productionYear   = prod_datarow[4]
            productionUnit   = prod_datarow[5]
            productionSource = prod_datarow[6]
            # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # Convert productionValue from productionUnit to baseU ('MMT' by default)
    
            if self.baseU == productionUnit:
                self.convertFactor = 1.0
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "BASE U = productionUnit"
            elif self.baseU == "MMT" and productionUnit == "MTPA":
                self.convertFactor = 1.0
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "MMT = MTPA #########"
            else:
                self.convertFactor = float(self.mining_units(productionUnit, self.baseU))
            if self.convertFactor == 0:
                mComment = "CONVERSION FACTOR FROM " + productionUnit + " TO " + self.baseU + " NOT FOUND "
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 12")
                self.error_log[5].append("")
                self.error_log[5].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
            else:
                self.convertFactor = float(self.convertFactor)
            beforeUnit = productionUnit
            productionUnit = self.baseU
            productionValue = float(productionValue) * float(self.convertFactor)

            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "-=-" * 25
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'From production unit %s to base unit %s' % (beforeUnit, self.baseU)
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "4: Conversion Factor"
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'convertFactor:', self.convertFactor
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'Converted production: %s' % productionValue
    
            # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # Convert all production data to ROM production in order from least to most granular
            if self.romProductionFound:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'ROM Production Found'
                self.last_data['production']['type']      = productionType
                self.last_data['production']['commodity'] = productCommodity
                self.last_data['production']['year']      = productionYear
                self.last_data['production']['value']     = productionValue
                self.last_data['production']['unit']      = productionUnit
            elif self.saleProductionFound:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Saleable Production Found'
                self.last_data['sale_production']['type']      = productionType
                self.last_data['sale_production']['commodity'] = productCommodity
                self.last_data['sale_production']['year']      = productionYear
                self.last_data['sale_production']['value']     = productionValue
                self.last_data['sale_production']['unit']      = productionUnit
                productionValue = self.convert_to_rom('sale', self.last_data['sale_production'])
                productionType = "ROM Production"
                productionSource = "EST: Engine Estimation"
            elif self.overburdenFound:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Overburden Found'
                self.last_data['overburden']['type'] = productionType
                self.last_data['overburden']['commodity'] = productCommodity
                self.last_data['overburden']['year'] = productionYear
                self.last_data['overburden']['value'] = productionValue
                self.last_data['overburden']['unit'] = productionUnit
                productionValue = self.convert_to_rom('overburden', self.last_data['overburden'])
                productionType = "ROM Production"
                productionSource = "EST: Engine Estimation"
            elif self.oreProductionFound:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Ore Production Found'
                self.last_data['ore_production']['type'] = productionType
                self.last_data['ore_production']['commodity'] = productCommodity
                self.last_data['ore_production']['year'] = productionYear
                self.last_data['ore_production']['value'] = productionValue
                self.last_data['ore_production']['unit'] = productionUnit
                productionValue = self.convert_to_rom('ore', self.last_data['ore_production'])
                productionType = "ROM Production"
                productionSource = "EST: Engine Estimation"
            elif self.metalProductionFound:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'Metal Production Found'
                self.last_data['metal_production']['type'] = productionType
                self.last_data['metal_production']['commodity'] = productCommodity
                self.last_data['metal_production']['year'] = productionYear
                self.last_data['metal_production']['value'] = productionValue
                self.last_data['metal_production']['unit'] = productionUnit
                productionValue = self.convert_to_rom('metal', self.last_data['metal_production'])
                productionType = "ROM Production"
                productionSource = "EST: Engine Estimation"
            # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # Process ROM production data
            if productionType == "ROM Production" and len(productionSource.strip()) > 0:
                productionFound = True
                self.maxProduction = max(productionValue, self.maxProduction)
                self.mTotalProduction += float(productionValue)

                self.mines['Production Type'].append(productionType)
                self.mines['Production Year'].append(productionYear)
                self.mines['Production Value'].append(productionValue)
                self.mines['Production unit'].append(productionUnit)
                self.mines['Production Source'].append(productionSource)
    
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'maxProduction:', self.maxProduction
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "ROM Production -------->", self.mines['Production Type'][-1], self.mines['Production Year'][-1], self.mines['Production Value'][-1], self.mines['Production unit'][-1], self.mines['Production Source'][-1]

                if len(self.mines['Production Value']) > 1:
                    extraWhere = ""
                    extraVars = ""
                    yrs = self.mines['Production Year'][-1] - self.mines['Production Year'][-2]
                    if yrs > 1:
                        # year was skipped
                        fctr = (float(self.mines['Production Value'][-1]) - float(self.mines['Production Value'][-2])) / float(yrs)
                        pos = -2
                        for ii in range(yrs):
                            productionType = self.mines['Production Type'][pos]
                            productionYear = self.mines['Production Year'][pos] + 1
                            productionValue = float(self.mines['Production Value'][pos]) + fctr
                            productionUnit = self.mines['Production unit'][pos]
    
                            if productionUnit != 'MMT':
                                convFactor = self.mining_units(productionUnit, "MMT")
                            else:
                                convFactor = 1.0
    
                            productionValue *= convFactor
                            productionUnit = "MMT"

                            self.mines['Production Type'].append(productionType)
                            self.mines['Production Year'].append(productionYear)
                            self.mines['Production Value'].append(productionValue)
                            self.mines['Production unit'].append(productionUnit)
                            self.mines['Production Source'].append('EST: Forecast Engine')

                            self.maxProduction = max(productionValue, self.maxProduction)
                            self.mTotalProduction += float(productionValue)
                            pos = -1

                    elif len(self.mines['Production Value']) > 1 and float(self.mines['Production Value'][-2]) > 0:
                        prod_change = abs((float(self.mines['Production Value'][-1]) - float(self.mines['Production Value'][-2])) / float(self.mines['Production Value'][-2]))
                        if prod_change > 0.3 and (self.mines['Production Year'][-1] - self.mines['Production Year'][-2] == 1):
                            mComment = "SOURCED PRODUCTION CHANGE OF GREATER THAN 30%"
                            self.error_log[0].append(self.NewMineId)
                            self.error_log[1].append(self.mines['Production Year'][-1])
                            self.error_log[2].append(mComment)
                            self.error_log[3].append(self.mSession_key)
                            self.error_log[4].append("ERROR TYPE 28")
                            self.error_log[5].append(self.mines['Production Value'][-2])
                            self.error_log[6].append(self.mines['Production Value'][-1])

                    elif self.last_capacity_amt > 0 and productionValue > self.last_capacity_amt:
                        if productionSource == "EST: Engine Estimation" and self.mines['Capacity Source'][-1] != "EST: Engine Estimation":
                            mComment = "CONVERTED PRODUCTION VALUE EXCEEDS ROM CAPACITY"
                            self.error_log[0].append(self.NewMineId)
                            self.error_log[1].append(self.mines['Production Year'][-1])
                            self.error_log[2].append(mComment)
                            self.error_log[3].append(self.mSession_key)
                            self.error_log[4].append("ERROR TYPE 32")
                            self.error_log[5].append(self.last_capacity_amt)
                            self.error_log[6].append(productionValue)
                        # outside of tolerance
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    " - PRODUCTION EXCEEDS ROM CAPACITY " * 5
                        mComment = "PRODUCTION EXCEEDS ROM CAPACITY FOR MINE ID " + str(self.NewMineId) + " YEAR " + str(productionYear)
                        if self.include_T3E:
                            if not self.firstType3:
                                self.error_log[0].append(self.NewMineId)
                                self.error_log[1].append(productionYear)
                                self.error_log[2].append(mComment)
                                self.error_log[3].append(self.mSession_key)
                                self.error_log[4].append("ERROR TYPE 03")
                                self.error_log[5].append(str(self.last_capacity_amt))
                                self.error_log[6].append(productionValue)
                                if self.debugMode:
                                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                                self.firstType3 = True
                if self.debugMode:
                    if firstTime and self.debugSQL:
                        firstTime = False
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "PRODUCTION------>", self.NewMineId, productionType, productionYear, productionValue, productionUnit, productCommodity

        if self.romProductionFound or self.saleProductionFound or self.overburdenFound or self.oreProductionFound or self.metalProductionFound:
            sql_update = 'UPDATE mining_param_track SET lastProductionType=%s,lastProductionComm=%s,lastProductionYear=%s,lastProductionVal=%s,lastProductionUnit=%s WHERE NewMineId=%s AND sessionKey=%s'

            if self.romProductionFound:     last_prod = self.last_data['production']
            elif self.saleProductionFound:  last_prod = self.last_data['sale_production']
            elif self.overburdenFound:      last_prod = self.last_data['overburden']
            elif self.oreProductionFound:   last_prod = self.last_data['ore_production']
            elif self.metalProductionFound: last_prod = self.last_data['metal_production']

            param_vals = (last_prod['type'], last_prod['commodity'], last_prod['year'], last_prod['value'], last_prod['unit'], self.NewMineId, self.mSession_key)
            self.curr.execute(sql_update, param_vals)
            self.curr.execute('COMMIT')
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def convert_units(self):
        self.mining_section = 8.0
        unitType = []
        if len(self.mines['Reserve unit']):
            if len(unitType) == 0 or unitType.count(self.mines['Reserve unit'][0]) == 0:
                unitType.append(self.mines['Reserve unit'][0])
            for i in range(len(self.mines['Reserve unit'])):
                unit = self.mines['Reserve unit'][i]
                if unitType.count(unit) == 0:
                    unitType.append(self.mines['Reserve unit'][i])
                    if self.debugMode or self.debugReserves:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "RESERVE MINE UNITS"
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "@" * 25
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Reserve unit'][%s]:" % i, self.mines['Reserve unit'][i]
        # ----------------------------------------
        if len(self.mines['Capacity unit']):
            if len(unitType) == 0 or unitType.count(self.mines['Capacity unit'][0]) == 0:
                unitType.append(self.mines['Capacity unit'][0])
            for i in range(len(self.mines['Capacity unit'])):
                unit = self.mines['Capacity unit'][i]
                if unitType.count(unit) == 0:
                    unitType.append(self.mines['Capacity unit'][i])
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "CAPACITY MINE UNITS"
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "@" * 25
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Capacity unit'][%s]:" % i, self.mines['Capacity unit'][i]
        # ----------------------------------------
        if len(self.mines['Production unit']):
            if len(unitType) == 0 or unitType.count(self.mines['Production unit'][0]) == 0:
                unitType.append(self.mines['Production unit'][0])
            for i in range(len(self.mines['Production unit'])):
                unit = self.mines['Production unit'][i]
                if unitType.count(unit) == 0:
                    unitType.append(self.mines['Production unit'][i])
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "PRODUCTION MINE UNITS"
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "@" * 25
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production unit'][%s]:" % i, self.mines['Production unit'][i]
        # ----------------------------------------
        if len(self.mines['Resource unit']):
            if len(unitType) == 0 or unitType.count(self.mines['Resource unit'][0]) == 0:
                unitType.append(self.mines['Resource unit'][0])
            for i in range(len(self.mines['Resource unit'])):
                unit = self.mines['Resource unit'][i]
                if unitType.count(unit) == 0:
                    unitType.append(self.mines['Resource unit'][i])
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "RESOURCE MINE UNITS"
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "@" * 25
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Resource unit'][%s]:" % i, self.mines['Resource unit'][i]
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "-----------> UNITS: "
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'unitType:', unitType
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'baseU:', self.baseU
            print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
        if unitType.count(self.baseU) == 0:
            pass
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def process_missing_data(self):
        self.mining_section = 8.0
        if self.productionFound and self.capacityFound:
            if self.mines['Production Year'][-1] == self.mines['Capacity year'][-1]:
                lastProdVal = self.mines['Production Value'][-1]
                self.lastProdUnit = self.mines['Production unit'][-1]
                lastCapVal = self.mines['Capacity'][-1]
                lastCapUnit = self.mines['Capacity unit'][-1]
    
                if lastCapUnit == self.lastProdUnit:
                    convFactor = 1.0
                else:
                    convFactor = float(self.mining_units(lastCapUnit, self.lastProdUnit))
                lastCapVal *= convFactor
    
                if lastProdVal < (lastCapVal * 0.7):
                    mComment = "LAST PRODUCTION VALUE SIGNIFICANTLY LESS THAN LAST CAPACITY VALUE"
                    self.error_log[0].append(self.NewMineId)
                    self.error_log[1].append(self.mines['Production Year'][-1])
                    self.error_log[2].append(mComment)
                    self.error_log[3].append(self.mSession_key)
                    self.error_log[4].append("ERROR TYPE 24")
                    self.error_log[5].append(lastCapVal)
                    self.error_log[6].append(lastProdVal)
    
        if not self.reservesFound or not self.resourcesFound:
            # -------------------------------------------------------------------
            extraWhere = ""
            extraVars = ""
            rtr = self.get_param_detail("RESOURCES_TO_RESERVES")
            if self.debugMode or self.debugReserves:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "$" * 30
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "RESOURCE TO RESERVES"
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'rtr:', rtr
            if rtr == 0 or len(rtr.strip()) == 0:
                # use the default and trigger an error
                mComment = "RESOURCES TO RESERVES RATIO NOT FOUND "
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 09")
                self.error_log[5].append("")
                self.error_log[6].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                self.resources_to_reserves = .90
            else:
                self.resources_to_reserves = float(rtr)
            self.curr.execute('UPDATE mining_param_track SET resourcesToReserves=%s WHERE NewMineId=%s AND sessionKey=%s', (self.resources_to_reserves, self.NewMineId, self.mSession_key))
            self.curr.execute('COMMIT')
            # check to see if there are Resource files
            if not self.reservesFound and not self.resourcesFound:
                pass
            elif not self.reservesFound:
                # assusmes you have a resources number
                self.mines['Reserve type'].append("Total Reserves")
                self.mines['Reserve year'].append(self.mines['Resource Year'][-1])
                self.mines['Reserves'].append(float(self.mines['Resource %'][-1]) * self.resources_to_reserves)
                self.mines['Reserve unit'].append(self.mines['Resource unit'][-1])
                self.mines['Reserves Source'].append("EST: Forecast Engine")
                if self.debugReserves:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % ("Total Reserves", "mines['Reserve type']")
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (self.mines['Resource Year'][-1], "mines['Resource Year']")
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (float(self.mines['Resource %'][-1]) * self.resources_to_reserves, "mines['Reserves']")
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (self.mines['Resource unit'][-1], "mines['Reserve unit']")
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % ("EST: Forecast Engine", "mines['Reserves Source']")
            else:
                # assumes that resources were not found
                self.mines['Resource Type'].append("Total Resources")
                self.mines['Resource Year'].append(self.mines['Reserve year'][-1])
                if self.resources_to_reserves > 0:
                    self.mines['Resource %'].append(float(self.mines['Reserves'][-1]) * (1 / self.resources_to_reserves))
                else:
                    self.mines['Resource %'].append(self.mines['Reserves'][-1])
                self.mines['Resource unit'].append(self.mines['Reserve unit'][-1])
                self.mines['Resource Source'].append("EST: Forecast Engine")
    
        if not self.capacityFound:
            # create the capacity record based on the maxproduction
            if self.productionFound and self.maxProduction > 0:
                # look up capacity_to_production
                # -------------------------------------------------------------------
                extraWhere = ""
                extraVars = ""
                ctp_lookup = True
                ctp = self.get_param_detail("CAPACITY_TO_PRODUCTION")
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "$" * 30
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "CAPACITY TO PRODUCTION  "
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'ctp:', ctp
                if ctp == 0 or len(ctp.strip()) == 0:
                    # use the default and trigger an error
                    mComment = "CAPACITY TO PRODUCTION RATIO NOT FOUND "
                    self.error_log[0].append(self.NewMineId)
                    self.error_log[1].append(0)
                    self.error_log[2].append(mComment)
                    self.error_log[3].append(self.mSession_key)
                    self.error_log[4].append("ERROR TYPE 10")
                    self.error_log[5].append("")
                    self.error_log[6].append(0)
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                    capacity_to_production = .90
                else:
                    capacity_to_production = float(ctp)
                self.curr.execute('UPDATE mining_param_track SET capacityToProduction=%s WHERE NewMineId=%s AND sessionKey=%s',(capacity_to_production, self.NewMineId, self.mSession_key))
                self.curr.execute('COMMIT')
                # Create the ROM CAPACITY
                #
                self.mines['Capacity type'].append(self.mines['Production Type'][-1])
                self.mines['Capacity year'].append(self.mines['Production Year'][-1])
                self.mines['Capacity Source'].append("EST: Forecast Engine")
                if capacity_to_production > 0:
                    self.mines['Capacity'].append(float(self.maxProduction) * float((1 / float(capacity_to_production))))
                else:
                    self.mines['Capacity'].append(0)
                self.mines['Capacity unit'].append(self.mines['Production unit'][-1])
    
        if not self.productionFound and self.capacityFound:
            # generate if you can based off of the capacity number
            # look up capacity_to_production
            # -------------------------------------------------------------------
            extraWhere = ""
            extraVars = ""
            ctp_lookup = True
            ctp = self.get_param_detail("CAPACITY_TO_PRODUCTION")
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "$" * 30
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "CAPACITY TO PRODUCTION  "
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'ctp:', ctp
            if ctp == 0 or len(ctp.strip()) == 0:
                # use the default and trigger an error
                mComment = "CAPACITY TO PRODUCTION RATIO NOT FOUND "
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 10")
                self.error_log[5].append("")
                self.error_log[6].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                self.capacity_to_production = .90
            else:
                self.capacity_to_production = float(ctp)
            self.curr.execute('UPDATE mining_param_track SET capacityToProduction=%s WHERE NewMineId=%s AND sessionKey=%s',(self.capacity_to_production, self.NewMineId, self.mSession_key))
            self.curr.execute('COMMIT')
            # Create the production value
            self.mines['Production Type'].append(self.mines['Capacity type'][-1])
            self.mines['Production Year'].append(self.mines['Capacity year'][-1])
            self.mines['Production Source'].append("EST: Forecast Engine")
            zeroTotalProd = False
            if self.mTotalProduction == 0:
                zeroTotalProd = True
            if self.capacity_to_production > 0:
                self.mines['Production Value'].append(float(self.mines['Capacity'][-1]) * float(self.capacity_to_production))
                if zeroTotalProd:
                    self.mTotalProduction += float(self.mines['Production Value'][-1])
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Capacity'][-1]):", self.mines['Capacity'][-1]
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'capacity_to_production:', self.capacity_to_production
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s' % (float(self.mines['Capacity'][-1]) * float(self.capacity_to_production), "mines['Production Value']")
            else:
                self.mines['Production Value'].append(0)
            self.mines['Production unit'].append(self.mines['Capacity unit'][-1])
            self.productionFound = True
    
        if self.reservesFound or self.resourcesFound:
            lastReserveYear = self.mines['Reserve year'][-1]
            if self.discountYear - lastReserveYear > 5:
                mComment = "NO SOURCED RESERVES WITHIN 5 YEARS OF CURRENT YEAR"
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 27")
                self.error_log[5].append(self.discountYear)
                self.error_log[6].append(lastReserveYear)
    
        if (self.productionFound or self.capacityFound) and (self.reservesFound or self.resourcesFound):
            if (self.mines['Production Year'][-1] - self.mines['Reserve year'][-1]) > 5 or (self.mines['Production Year'][-1] - self.mines['Reserve year'][-1]) < -5:
                mComment = "LAST SOURCED PRODUCTION AND LAST SOURCED RESERVES ARE GREATER THAN 5 YEARS APART"
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 25")
                self.error_log[5].append(self.mines['Reserve year'][-1])
                self.error_log[6].append(self.mines['Production Year'][-1])
    
            lastProdVal = self.mines['Production Value'][-1]
            self.lastProdUnit = self.mines['Production unit'][-1]
            lastReserveVal = float(self.mines['Reserves'][-1])
            lastReserveUnit = self.mines['Reserve unit'][-1]
    
            if lastReserveUnit == self.lastProdUnit:
                convFactor = 1.0
            else:
                convFactor = float(self.mining_units(lastReserveUnit, self.lastProdUnit))
            lastReserveVal *= convFactor
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def decide_forecast_process(self):
        self.mining_section = 9.0
        """
        APSY  = actualProductionStartYear
        MEY   = mineEndYear
        TML   = TotalMineLife
        RML   = RemainingMineLife
        APSYS = actualProductionStartYearSource
        MEYS  = mineEndYearSource
        TMLS  = TotalMineLifeSource
        RMLS  = remainingMineLifeSource
        RMLY  = remainingMineLifeYear
        """

        APSYS, MEYS, TMLS, RMLS,  = (False,) * 4
    
        prod_found = False
        scenario = 0
    
        sql_dict = {'APSY': '', 'MEY': '', 'TML': '', 'RML': '', 'APSYS': '', 'MEYS': '', 'TMLS': '', 'RMLS': '', 'RMLY': ''}

        if len(self.mines['Production Value']) >= 1:
            # YES - production data
            prod_found = True
            self.generate_forecast = True
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "**** PRODUCTION AVAILABLE "
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Year']:", self.mines['Production Year']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Value']:", self.mines['Production Value']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production unit']:", self.mines['Production unit']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Type']:", self.mines['Production Type']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
        else:
            self.curr.execute('UPDATE mining_param_track SET forecastEndCause="NO PRODUCTION DATA" WHERE NewMineId=%s AND sessionKey=%s', (self.NewMineId, self.mSession_key))
            self.curr.execute('COMMIT')
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "**** NO PRODUCTION DATA - " * 10
        #
        # The assumption is that if the field is blank than the source must be a mistake and written over with
        # EST: Forecast Engine
        #
        # The numbers presented here are temporary and may be replace in the next section based on
        # if history is filled in or a forecast made
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'ActualProductionStartYear:', self.ActualProductionStartYear
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'ActualProductionStartYearSource:', self.ActualProductionStartYearSource
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'mineEndYear:', self.mineEndYear
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'totalMineLife:', self.totalMineLife
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'remainingMineLife:', self.remainingMineLife
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'remainingMineLifeYear:', self.remainingMineLifeYear
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'APSY:', self.APSY
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'APSYS:', APSYS
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'MEY:', self.MEY
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'MEYS:', MEYS
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'TML:', self.TML
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'TMLS:', TMLS
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'RML:', self.RML
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'RMLS:', RMLS
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'RMLY:', self.RMLY
        if (self.ActualProductionStartYear is None or self.ActualProductionStartYear == 0):
            self.ActualProductionStartYear = 0
            self.APSY = False
        if self.ActualProductionStartYearSource is None or len(self.ActualProductionStartYearSource.strip()) == 0 or self.ActualProductionStartYearSource == "EST: Forecast Engine":
            APSYS = False
        else:
            APSYS = True
        if not (self.APSY or APSYS):
            mComment = "NO SOURCED PRODUCTION START YEAR PROVIDED"
            self.error_log[0].append(self.NewMineId)
            self.error_log[1].append(0)
            self.error_log[2].append(mComment)
            self.error_log[3].append(self.mSession_key)
            self.error_log[4].append("ERROR TYPE 29")
            self.error_log[5].append("")
            self.error_log[6].append(0)
        if (self.mineEndYear is None or self.mineEndYear == 0):
            self.mineEndYear = 0
            self.MEY = False
            MEYS = True
        if (self.totalMineLife is None or self.totalMineLife == 0):
            self.totalMineLife = 0
            self.TML = False
            TMLS = True
        if (self.remainingMineLifeYear is None or self.remainingMineLifeYear == 0):
            self.remainingMineLifeYear = 0
            self.RMLY = False
        if (self.remainingMineLife is None or self.remainingMineLife == 0 or not RMLS or not self.RMLY):
            self.remainingMineLife = 0
            self.RML = False
            RMLS = True
    
        # Without production or capacity you cannot model the asset
        if len(self.mines['Production Value']) == 0 and len(self.mines['Capacity']) == 0:
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "SECTION: DO NOT MODEL" * 12
            pass
        else:
            if not self.APSY and not self.MEY and not self.TML and not self.RML and not self.RMLY:
                scenario = 1
                if prod_found:
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "not APSY and not MEY and not TML and not RML and not RMLY - PRODUCTION - "
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'not actualProductionStartYear and not mineEndYear and not TotalMineLife and not RemainingMineLife and not remainingMineLifeYear'
                    self.ActualProductionStartYear = float(self.mines['Production Year'][0])
                    APSYS = True
                    # set to last year of production temporarily
                    self.mineEndYear = self.discountYear
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "Actual Production Start Year : "
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'ActualProductionStartYear:', self.ActualProductionStartYear
    
                    # At this point the only action you can do is set the ActualProductionStartYear
                    # because there is production history
                    sql_dict["APSY"] = self.ActualProductionStartYear
                    sql_dict["APSYS"] = "EST: Forecast Engine"
                    self.forecast_years = -1

                    self.lastYear = self.mines['Production Year'][-1]
                    self.lastProdType = self.mines['Production Type'][-1]
                    self.lastProdUnit = self.mines['Production unit'][-1]
                    self.newProdUnit = self.lastProdUnit
    
                    if len(self.mines['Production Value']):
                        self.generate_forecast = True
    
                    if self.newProdUnit not in ['MMT', 'MTPA']:
                        convFactor = self.mining_units(self.newProdUnit, "MMT")
                    else:
                        convFactor = 1

                    self.newProdUnit = "MMT"
                    self.newProd = float(self.mines['Production Value'][-1]) * convFactor
                    self.lastProd = self.newProd
                    self.mines['Production unit'][-1] = self.newProdUnit
                    self.mines['Production Value'][-1] = self.newProd
    
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'forecast_years:', self.forecast_years
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "Last production: " + str(self.newProd)
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    " Last Prod Year: " + str(self.lastYear)
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "           Type: " + self.lastProdType
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "         Source: " + self.mines['Production Source'][-1]
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "         Length: " + str(len(self.mines['Production Value']))
                else:
                    # no production
                    # Factors
                    # 1 - is there total reserves?
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "not APSY and not MEY and not TML and not RML and not RMLY - NO PRODUCTION - " * 5
                    if len(self.mines['Reserve type']):
                        # reserve data
                        # print '%s - %s:' % (self.NewMineId, self.mining_section),    the first and last item
                        if self.debugMode or self.debugReserves:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'first_reserve_type,first_reserve_year ,first_reserve_amt ,first_reserve_unit:', self.first_reserve_type, self.first_reserve_year, self.first_reserve_amt, self.first_reserve_unit
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'last_reserve_type,last_reserve_year ,last_reserve_amt ,last_reserve_unit:', self.last_reserve_type, self.last_reserve_year, self.last_reserve_amt, self.last_reserve_unit
                        self.lastYear = self.discountYear
                        if self.first_capacity_year > 0 or self.last_ore_cap > 0:
                            # use the date and the capacity to contruct the history
                            # evaluate the minimum of the first_reserve_year and first_capacity_year
                            if self.first_capacity_year > 0:
                                first_year = min(self.first_reserve_year, self.first_capacity_year)
                                self.historical_years = self.lastYear - first_year
                                self.lastProd = float(self.last_capacity_amt)
                                self.lastProdType = self.last_capacity_type
                                self.lastProdUnit = self.last_capacity_unit
                            else:
                                if self.first_reserve_year > 0:
                                    first_year = min(self.last_ore_year, self.first_reserve_year)
                                else:
                                    first_year = self.last_ore_year
                                self.historical_years = self.lastYear - first_year
                                self.lastProd = float(self.last_ore_cap)
                                self.lastProdType = self.last_ore_type
                                self.lastProdUnit = self.last_ore_unit
                            #
                            self.generate_history = True
                            self.generate_forecast = True
                            self.forecast_years = -1
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'forecast_years:', self.forecast_years
                        else:
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    "NO PRODUCTION - NO CAPACITY DATA - DO NOT MODEL"
                            self.generate_history = False
                            self.generate_forecast = False
                            forecast_end = "NO PRODUCTION - NO CAPACITY DATA "
                            self.curr.execute('UPDATE mining_param_track SET forecastEndCause=%s WHERE NewMineId=%s AND sessionKey=%s',(forecast_end, self.NewMineId, self.mSession_key))
                            self.curr.execute('COMMIT')
                    else:
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "NO PRODUCTION - NO RESERVES DATA - DO NOT MODEL"
                        self.generate_history = False
                        self.generate_forecast = False
                        self.thisWasModelled = False
                        forecast_end = "NO PRODUCTION - NO RESERVES DATA - DO NOT MODEL"
                        self.curr.execute('UPDATE mining_param_track SET forecastEndCause=%s WHERE NewMineId=%s AND sessionKey=%s',(forecast_end, self.NewMineId, self.mSession_key))
                        self.curr.execute('COMMIT')
                    if self.debugMode:
                        print
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "LastYear = " + str(self.lastYear)
            elif self.APSY and not self.MEY and not self.TML and not self.RML and not self.RMLY:
                scenario = 2
                if len(self.mines['Production Year']):
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "APSY and not MEY and not TML and not RML and not RMLY - PRODUCTION - " * 5
                    # if prod_found
                    #
                    # Is there production within the last 5 years?
                    first_year = self.ActualProductionStartYear
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Year']:", self.mines['Production Year']
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "Start year: " + str(self.ActualProductionStartYear)
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Year']:", self.mines['Production Year']
                    if self.discountYear - self.mines['Production Year'][0] > 0:
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "Years ----> " + str(self.discountYear - self.mines['Production Year'][0])
                        self.historical_years = self.discountYear - self.mines['Production Year'][0]
                        self.generate_history = True
                        self.lastProd = float(self.mines['Production Value'][0])
                    else:
                        resourceYr = 0
                        reserveYr = 0
                        self.historical_years = 0
                        if len(self.mines['Resource Year']):
                            resourceYr = self.mines['Resource Year'][-1]
                        if len(self.mines['Reserve year']):
                            reserveYr = self.mines['Reserve year'][-1]
                        if resourceYr > 0 and reserveYr > 0:
                            self.historical_years = self.discountYear - min(reserveYr, resourceYr)
                            self.generate_history = True
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'historical_years = discountYear - min(reserveYr,resourceYr)'
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'discountYear:', self.discountYear
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'reserveYr:', reserveYr
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'resourceYr:', resourceYr
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'min(reserveYr,resourceYr):', min(reserveYr, resourceYr)
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'historical_years:', self.historical_years
                        elif resourceYr > 0:
                            self.historical_years = self.discountYear - resourceYr
                            self.generate_history = True
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'historical_years = discountYear - resourceYr'
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'discountYear:', self.discountYear
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'resourceYr:', resourceYr
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'historical_years:', self.historical_years
                        elif reserveYr > 0:
                            self.historical_years = self.discountYear - reserveYr
                            self.generate_history = True
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'historical_years = discountYear - reserveYr'
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'discountYear:', self.discountYear
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'reserveYr:', reserveYr
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'historical_years:', self.historical_years
                        else:
                            #  both are zero
                            pass
                        if reserveYr > 0:
                            self.generate_forecast = True
                    self.lastYear = self.mines['Production Year'][0]
                    self.lastProdType = self.mines['Production Type'][0]
                    self.lastProdUnit = self.mines['Production unit'][0]

                    self.newProdUnit = self.lastProdUnit
                    self.forecast_years = -1
    
                    if self.newProdUnit not in ['MMT', 'MTPA']:
                        convFactor = self.mining_units(self.newProdUnit, "MMT")
                    else:
                        convFactor = 1

                    self.newProdUnit = "MMT"
                    self.newProd = float(self.mines['Production Value'][0]) * convFactor

                    self.lastProd = self.newProd

                    self.mines['Production unit'][0] = self.newProdUnit
                    self.mines['Production Value'][0] = self.newProd
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'forecast_years:', self.forecast_years
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'convFactor:', convFactor
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "newProd := mines['Production Value'][0] --> ", self.newProd
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "lastYear := mines['Production Year'][0] --> ", self.lastYear
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "lastProdType := mines['Production Type'][0] --> ", self.lastProdType
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "lastProdUnit = mines['Production unit'][0] --> ", self.lastProdUnit
                else:
                    self.generate_history = False
                    self.generate_forecast = False
                    self.forecast_years = 0
                    forecast_end = "NO PRODUCTION - DO NOT MODEL"
                    self.curr.execute('UPDATE mining_param_track SET forecastEndCause=%s WHERE NewMineId=%s AND sessionKey=%s',(forecast_end, self.NewMineId, self.mSession_key))
                    self.curr.execute('COMMIT')
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'forecast_years:', self.forecast_years
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "APSY and not MEY and not TML and not RML and not RMLY - NO PRODUCTION - " * 5
            else:
                scenario = 0
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    " = NOT MAPPED = " * 25
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def generate_historical(self):
        self.mining_section = 10.0
        if self.generate_history:
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    " ** BUILDING HISTORY ** " * 5
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Type']:", self.mines['Production Type']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Year']:", self.mines['Production Year']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Value']:", self.mines['Production Value']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production unit']:", self.mines['Production unit']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Source']:", self.mines['Production Source']
            hLastYear = self.lastYear
            for i in range(0, self.historical_years):
                self.generated_hist = True
                if i <= 5:
                    e_ratio = self.ye_lt5
                elif i <= 10:
                    e_ratio = self.ye_lt10
                else:
                    e_ratio = self.ye_lt20
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'lastProd:', self.lastProd
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'float(1-e_ratio):', float(1 - e_ratio)
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'lastProd *= float(1-e_ratio)'
                self.lastProd *= float(1 - e_ratio)
                #*&* Determine type of production to forecast (ROM, metal, etc.) then use approriate unit (prodUnitROM, prodUnitMetal, etc.) 
                if self.lastProdUnit != 'MMT':
                    convFactor = self.mining_units(self.lastProdUnit, "MMT")
                else:
                    convFactor = 1.0
                self.lastProd *= convFactor
                self.lastProdUnit = "MMT"
    
                hLastYear -= 1
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    pws(str(i), 3), "**** Historical Forecast -----> " + str(self.lastProd) + "   " + str(hLastYear)
    
                # add to the array of values ----------------------------------------
                self.mines['Production Type'].insert(0, self.lastProdType)
                self.mines['Production Year'].insert(0, hLastYear)
                self.mines['Production Value'].insert(0, self.lastProd)
                self.mines['Production unit'].insert(0, self.lastProdUnit)
                self.mines['Production Source'].insert(0, 'EST: Forecast Engine')
                # -------------------------------------------------------------------
                self.mTotalProduction += self.lastProd
                self.lastYear = self.mines['Production Year'][-1]
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "******** Total production: " + str(self.mTotalProduction)
        # ----------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def generate_prod_forecast(self):
        self.mining_section = 11.0
        resourcesLimit = False
        if self.generate_forecast:
            # ----------------------------------------------------------
            # take the last production number and multiply it by a factor for x years
            lastNewProd = 0
            # greater than 1
            extraWhere = ""
            extraVars = ""
            ytp = self.get_param_detail("YEARS_TO_PROJECT")
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "$" * 30
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "YEAR TO PROJECT "
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'ytp:', ytp
            if ytp == 0 or len(ytp.strip()) == 0:
                # use the default and trigger an error
                mComment = "YEARS TO PROJECT NOT FOUND "
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 13")
                self.error_log[5].append("")
                self.error_log[6].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                self.years_to_project = 10
            else:
                self.years_to_project = int(ytp)
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "$-" * 20
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "YEAR TO PROJECT "
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'years_to_project:', self.years_to_project
            self.curr.execute('UPDATE mining_param_track SET yearsToProject=%s WHERE NewMineId=%s AND sessionKey=%s', (self.years_to_project, self.NewMineId, self.mSession_key))
            self.curr.execute('COMMIT')
            # -------------------------------------------------------------------
            extraWhere = ""
            extraVars = ""
            if not self.rr_ran:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'NewMineId:', self.NewMineId
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'mineCountry:', self.mineCountry
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'mineRegion:', self.mineRegion
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'mineStatus:', self.mineStatus
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'mineType:', self.mineType
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'mineMethod:', self.mineMethod
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'key_commodity:', self.key_commodity
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'mOperators:', self.mOperators
                rr = self.get_param_detail("RECOVERY_RATE")
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "$" * 30
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "RECOVERY RATE  "
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'rr:', rr
                if rr == 0 or len(rr.strip()) == 0:
                    # use the default and trigger an error
                    mComment = "RECOVERY RATE NOT FOUND "
                    self.error_log[0].append(self.NewMineId)
                    self.error_log[1].append(0)
                    self.error_log[2].append(mComment)
                    self.error_log[3].append(self.mSession_key)
                    self.error_log[4].append("ERROR TYPE 06")
                    self.error_log[5].append("")
                    self.error_log[6].append(0)
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                    # ytp_flag = False
                    self.recovery_rate = .90
                else:
                    self.recovery_rate = float(rr)
                self.curr.execute('UPDATE mining_param_track SET recoveryRate=%s WHERE NewMineId=%s AND sessionKey=%s', (self.recovery_rate, self.NewMineId, self.mSession_key))
                self.rr_ran = True
            # --------------------------------------------
            if self.forecast_years == 0:
                #
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    " - NO FORECAST " + ("-" * 30)
            # --------------------------------------------
            elif self.forecast_years == -1:
                # pass
                # until exhaustion
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    " - EXHAUST - " * 10
                fLastYear = self.lastYear
                if self.debugMode or self.debugReserves:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "rr " + str(self.recovery_rate)
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "Last total reserves "
    
                if len(self.mines['Reserves']) and len(str(self.recovery_rate).strip()) > 0:
                    # check the units of the reserves
                    baseUnit = self.mines['Reserve unit'][-1]
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Reserve unit'][-1]:", self.mines['Reserve unit'][-1]
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Reserves'][-1]:", self.mines['Reserves'][-1]
                    prodFactor = 1.0
                    if not baseUnit == "MTPA":
                        prodFactor = self.mining_units(baseUnit, "MMT")
                    calcMaxProduction = float(self.mines['Reserves'][-1]) * float(self.recovery_rate) * float(prodFactor)
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'calcMaxProduction:', calcMaxProduction
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "calcMaxProduction := float(mines['Reserves'][-1]) * float(recovery_rate) * float(prodFactor)"
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'recovery_rate:', self.recovery_rate
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'prodFactor:', prodFactor
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Reserves'][-1]:", self.mines['Reserves'][-1]
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Reserves'][-1] * prodFactor = %s" % (float(self.mines['Reserves'][-1]) * float(prodFactor))
                else:
                    # missing reserves numbers
                    # use the resource to reserves number
                    if self.resourcesFound:
                        # what are the units of the resources
                        baseUnit = self.mines['Resource unit'][-1]
                        prodFactor = 1.0
                        if not baseUnit == "MTPA":
                            prodFactor = self.mining_units(baseUnit, "MMT")
                        calcMaxProduction = float(self.resources_to_reserves * self.mines['Resource %'][-1]) * float(self.recovery_rate) * float(prodFactor)
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'calcMaxProduction:', calcMaxProduction
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "calcMaxProduction := float(resources_to_reserves*mines['Resource %'][-1]) * float(recovery_rate) * float(prodFactor)"
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'resources_to_reserves:', self.resources_to_reserves
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'recovery_rate:', self.recovery_rate
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'prodFactor:', prodFactor
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Resource %'][-1]:", self.mines['Resource %'][-1]
                    else:
                        calcMaxProduction = self.mTotalProduction * (1 / float(self.recovery_rate))
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'calcMaxProduction = mTotalProduction * (1/float(recovery_rate))'
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'mTotalProduction:', self.mTotalProduction
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    '1/float(recovery_rate):', 1 / float(self.recovery_rate)
                self.origCalcMaxProduction = calcMaxProduction
                if self.mTotalProduction > calcMaxProduction:
                    mComment = "CUMULATIVE PRODUCTION EXCEEDS RESERVES BEFORE FORECAST"
                    self.error_log[0].append(self.NewMineId)
                    self.error_log[1].append(0)
                    self.error_log[2].append(mComment)
                    self.error_log[3].append(self.mSession_key)
                    self.error_log[4].append("ERROR TYPE 23")
                    self.error_log[5].append(str(calcMaxProduction))
                    self.error_log[6].append(self.mTotalProduction)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "             Max production: " + pws(fwc(str(float(self.maxProduction)).strip()), 20, 'R')
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "Total historical production: " + pws(fwc(str(self.mTotalProduction).strip()), 20, 'R')
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "   Production not to exceed: " + pws(fwc(str(calcMaxProduction).strip()), 20, 'R')

                firstTime = True
                self.generated_FC = True
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'minimumForecastMax:', self.minimumForecastMax

                self.newProd = self.mines['Production Value'][-1]
                calcForecast = True
                forecast_year_count = 1

                while calcForecast:
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'forecast_year_count:', forecast_year_count
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Type']:", self.mines['Production Type']
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Year']:", self.mines['Production Year']
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Value']:", self.mines['Production Value']
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production unit']:", self.mines['Production unit']
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Source']:", self.mines['Production Source']
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Type'][-1]:", self.mines['Production Type'][-1]
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'fLastYear:', fLastYear
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'newProd:', self.newProd
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'newProdUnit:', self.newProdUnit
    
                    if forecast_year_count > 1:
                        self.mines['Production Type'].append(self.mines['Production Type'][-1])
                        self.mines['Production Year'].append(fLastYear)
                        self.mines['Production Value'].append(self.newProd)
                        self.mines['Production unit'].append(self.newProdUnit)
                        self.mines['Production Source'].append('EST: Forecast Engine')
    
                    fLastYear += 1
    
                    # add to the array of values ----------------------------------------
                    self.newProdUnit = self.mines['Production unit'][-1]
    
                    if self.newProdUnit not in ['MMT', 'MTPA']:
                        convFactor = self.mining_units(self.newProdUnit, "MMT")
                    else:
                        convFactor = 1.0

                    self.newProd *= convFactor
                    self.newProdUnit = "MMT"

                    self.newProd *= (1 - self.yearly_effeciency)
    
                    # -------------------------------------------------------------------
                    lastNewProd = self.newProd
                    resourcesLimit = True
                    self.mTotalProduction += self.newProd
    
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s   **** Forecast          -----> %s     %s' % (forecast_year_count, self.newProd, fLastYear)
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s   **** Total Production  -----> %s     %s' % (forecast_year_count, self.mTotalProduction, fLastYear)
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                    if forecast_year_count > self.minimumForecastMax:
                        # then check other conditions
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "**** Is " + str(self.mTotalProduction) + " > " + str(calcMaxProduction) + "? "
                        if self.mTotalProduction > calcMaxProduction:
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'total production: %s exceeds max production: %s -----> End forecast' % (self.mTotalProduction, calcMaxProduction)
                            self.mTotalProduction -= self.newProd
                            calcForecast = False
                            forecast_end = 'total production: %s exceeds max production: %s' % (self.mTotalProduction, calcMaxProduction)
                        elif self.newProd < .00000000001:
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'production value: %s below minimum production threshold: %s -----> End forecast' % (self.newProd, 0.00000000001)
                            calcForecast = False
                            forecast_end = 'production value: %s below minimum production threshold: %s' % (self.newProd, 0.00000000001)
                        elif forecast_year_count >= 200:
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'maximum forecast years: %s reached -----> End forecast' % 200
                            calcForecast = False
                            forecast_end = 'maximum forecast years: %s reached' % 200
    
                    forecast_year_count += 1
    
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "******** Total production: " + str(self.mTotalProduction)
                param_vals = (self.mTotalProduction, calcMaxProduction, forecast_end, self.minimumForecastMax, self.NewMineId, self.mSession_key)
                self.curr.execute('UPDATE mining_param_track SET totalProduction=%s, maxProduction=%s, forecastEndCause=%s, minForecastYears=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
                self.curr.execute('COMMIT')
            # --------------------------------------------
            elif self.forecast_years == 0:
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    " - CLOSED ???? - " * 30
                    pass
            # --------------------------------------------
            else:
                # This might be a field that is planned
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    " - FIXED LIFE - " * 30
                #
                # ----------------------------------------------------------
                #
                fLastYear = self.lastYear + 1
                extraYears = max(0, int(self.discountYear) - int(self.mines['Production Year'][-1]))
                self.forecast_years = self.years_to_project + extraYears
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "Max production: %s" % self.maxProduction  # + str(round(float(maxProduction),prodDecimals))
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "Total historical production: " + str(self.mTotalProduction)
                for i in range(self.forecast_years):
                    # -----------------------------
                    self.generated_FC = True
                    # -----------------------------
                    if i == self.forecast_years - 1:
                        self.newProd *= self.last_year_fctr
                    else:
                        lastNewProd = self.newProd
                    self.newProd *= (1 - self.yearly_effeciency)
    
                    if self.newProdUnit not in ['MMT', 'MTPA']:
                        convFactor = self.mining_units(self.newProdUnit, "MMT")
                    else:
                        convFactor = 1.0

                    self.newProd *= convFactor
                    self.newProdUnit = "MMT"
    
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s\t**** Forecast ----->\t\t%s\t%s' % (i, self.newProd, fLastYear)
    
                    # add to the array of values ----------------------------------------
                    self.mines['Production Type'].append(self.mines['Production Type'][-1])
                    self.mines['Production Year'].append(fLastYear)
                    self.mines['Production Value'].append(self.newProd)
                    self.mines['Production unit'].append(self.newProdUnit)
                    self.mines['Production Source'].append('EST: Forecast Engine')
                    # -------------------------------------------------------------------
                    self.mTotalProduction += self.newProd
                    fLastYear += 1
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "******** Total production: " + str(self.mTotalProduction)
                forecast_end = 'fixed life forecast of %s years complete' % self.forecast_years
                param_vals = (self.mTotalProduction, self.maxProduction, forecast_end, self.NewMineId, self.mSession_key)
                self.curr.execute('UPDATE mining_param_track SET totalProduction=%s, maxProduction=%s, forecastEndCause=%s WHERE NewMineId=%s AND sessionKey=%s',param_vals)
                self.curr.execute('COMMIT')
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def process_forecast_data(self):
        self.mining_section = 12.0
        if self.generated_FC:
            extraWhere = ""
            extraVars = ""
            self.first_year_fctr = 0
            fyf = self.get_param_detail("FIRST_YEAR_FACTOR")
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "$" * 30
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "FIRST_YEAR_FACTOR "
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'fyf:', fyf
            if fyf == 0 or len(fyf.strip()) == 0:
                # use the default and trigger an error
                mComment = "FIRST YEAR FACTOR NOT FOUND "
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 08")
                self.error_log[5].append("")
                self.error_log[6].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                self.first_year_fctr = .5
            else:
                # Did they forget to add the ending comma?
                # if yes add it to make the algoritms work
                if fyf[-1:] == ",":
                    # do nothing
                    pass
                else:
                    # add it
                    fyf = fyf + ","
                # parse the commas
                fy_dict = {}
                commas = 0
                commas = fyf.count(",")
                fy_copy = fyf
                for i in range(0, commas):
                    fy_dict[str(i + 1)] = 1
                    # now parse
                    pos = fy_copy.index(",")
                    cval = fy_copy[:pos]
                    fy_dict[str(i + 1)] = float(cval)
                    fy_copy = fy_copy[pos + 1:]
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "FIRST YEAR FACTOR" + "^-" * 30
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'cval:', cval
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'fy_copy:', fy_copy
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'fy_dict:', fy_dict
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    ""

                self.curr.execute('UPDATE mining_param_track SET firstYearFactor=%s WHERE NewMineId=%s AND sessionKey=%s',(fyf, self.NewMineId, self.mSession_key))
                self.curr.execute('COMMIT')
                #
                # APPLY THE DICTIONARY VALUES RETROACTIVELY ONLY IF
                # THE VALUES ARE ENGINE ESTIMATED
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'mines[Production Year]:', self.mines['Production Year']
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'mines[Production Value]:', self.mines['Production Value']
                if len(self.mines['Production Source']) >= commas + 1 and self.mines['Production Source'][0] == "EST: Forecast Engine" \
                        and self.mines['Production Source'][1] == "EST: Forecast Engine" and self.mines['Production Source'] == "EST: Forecast Engine":
                    origValue = []
                    newValue = []
                    preVal = {}
                    commas = min(commas, len(self.mines['Production Source']))
                    baseNumber = float(self.mines['Production Value'][commas])
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'commas:', commas
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "BASE NUMBER: " + str(baseNumber)
                    for i in range(commas):
                        if self.mines['Production Source'][i] == "EST: Forecast Engine":
                            preVal[str(i)] = self.mines['Production Value'][i]
                            val = float(fy_dict[str(i + 1)]) * baseNumber
                            self.mines['Production Value'][i] = val
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    "!-" * 30
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    "Production year:", self.mines['Production Year'][i]
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    "OLD VAL " + str(preVal[str(i)])
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    "NEW VAL " + str(self.mines['Production Value'][i])
            # check to see if the program generated data after the discount year
            if self.debugMode and self.forecast_years == -1:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "=|" * 25
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'mTotalProduction:', self.mTotalProduction
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'origCalcMaxProduction:', self.origCalcMaxProduction
            if len(self.mines['Production Year']) and (self.mines['Production Year'][-1] < self.discountYear) and (self.mTotalProduction > self.origCalcMaxProduction) and (self.forecast_years == -1):
                # generate more data
                forecast_extend = 10
                fLastYear = self.mines['Production Year'][-1] + 1
                self.forecast_years = (self.discountYear + forecast_extend) - self.mines['Production Year'][-1]
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "Max production 2: " + pws(fwc(str(float(self.maxProduction)).strip()), 15, 'R')
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "Total historical production 2: " + pws(fwc(str(self.mTotalProduction).strip()), 15, 'R')
                # --------------------------------
                # back out the last values
    
                for i in range(self.forecast_years):
                    # -----------------------------
                    self.generated_FC = True
                    # -----------------------------
                    self.newProd *= (1 - self.yearly_effeciency)
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    pws(str(i), 3), "**** Forecast 2 -----> " + pws(fwc(str(self.newProd).strip()), 15, 'R') + "   " + str(fLastYear)
                    # add to the array of values ----------------------------------------
                    self.newProdUnit = self.mines['Production unit'][-1]
                    if self.newProdUnit not in ['MMT', 'MTPA']:
                        convFactor = self.mining_units(self.newProdUnit, "MMT")
                    else:
                        convFactor = 1.0

                    self.newProd *= convFactor
                    self.newProdUnit = "MMT"

                    self.mines['Production Type'].append(self.mines['Production Type'][-1])
                    self.mines['Production Year'].append(fLastYear)
                    self.mines['Production Value'].append(self.newProd)
                    self.mines['Production unit'].append(self.newProdUnit)
                    self.mines['Production Source'].append('EST: Forecast Engine')
                    # -------------------------------------------------------------------

                    self.mTotalProduction += self.newProd
                    fLastYear += 1
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "******** Total production: " + pws(fwc(str(self.mTotalProduction).strip()), 15, 'R')
                forecast_end = 'forecast extended to discount year(%s) + %s' % (self.discountYear, forecast_extend)
                param_vals = (self.mTotalProduction, self.maxProduction, forecast_end, self.NewMineId, self.mSession_key)
                self.curr.execute('UPDATE mining_param_track SET totalProduction=%s, maxProduction=%s, forecastEndCause=%s WHERE NewMineId=%s AND sessionKey=%s',param_vals)
                self.curr.execute('COMMIT')

            # Get the last year factor
            extraWhere = ""
            extraVars = ""
            self.last_year_fctr = 0
            ly_dict = {}
            commas = 0
            lyf = self.get_param_detail("LAST_YEAR_FACTOR")
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "$-" * 30
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "LAST_YEAR_FACTOR "
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'lyf:', lyf
            if lyf == 0 or len(lyf.strip()) == 0:
                # use the default and trigger an error
                mComment = "LAST YEAR FACTOR NOT FOUND "
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 07")
                self.error_log[5].append("")
                self.error_log[6].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                # ytp_flag = False
                lyf = ".5"
                ly_dict['1'] = .5
                commas = 1
            else:
                # Did they forget to add the ending comma?
                # if yes add it to make the algorithms work
                if lyf[-1:] == ",":
                    # do nothing
                    pass
                else:
                    # add it
                    lyf = lyf + ","
                # parse the commas
                #
                sum_factor = 0
                commas = lyf.count(",")
                ly_copy = lyf
                for i in range(0, commas):
                    ly_dict[str(i + 1)] = 1
                    # now parse
                    pos = ly_copy.index(",")
                    cval = ly_copy[:pos]
                    ly_dict[str(i + 1)] = cval
                    ly_copy = ly_copy[pos + 1:]
                    sum_factor += float(cval)
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "LAST YEAR FACTOR" + "!-" * 30
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'cval:', cval
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'ly_copy:', ly_copy
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'sum_factor:', sum_factor

            self.curr.execute('UPDATE mining_param_track SET lastYearFactor=%s WHERE NewMineId=%s AND sessionKey=%s', (lyf, self.NewMineId, self.mSession_key))
            self.curr.execute('COMMIT')
    
            # You can only apply the last year factor if the last production years are forecast
            if (len(self.mines['Production Source']) > (1 + commas)) and self.mines['Production Source'][-1] == "EST: Forecast Engine":
                origValue = []
                newValue = []
                preVal = {}
                commas = min(commas, len(self.mines['Production Source']) + 1)
                baseNumber = float(self.mines['Production Value'][(-1) * commas])
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "LAST YEAR BASE NUMBER (baseNumber): " + str(baseNumber)
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "Commas: " + str(commas)
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'ly_dict:', ly_dict
                x = commas + 1
                for i in range(commas, 0, -1):
                    if self.mines['Production Source'][-i] == "EST: Forecast Engine":
                        preVal[str(i)] = self.mines['Production Value'][-i]
                        val = float(ly_dict[str(x - i)]) * baseNumber
                        self.mines['Production Value'][-i] = val
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "!-" * 30
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'i:', i
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'commas:', commas
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'val = float(ly_dict[str(%s)])' % (x - i), float(ly_dict[str(x - i)])
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "Production year:", self.mines['Production Year'][-i]
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "OLD VAL " + str(preVal[str(i)])
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "NEW VAL (mines['Production Value'][-%s])" % i, str(self.mines['Production Value'][-i])
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def estimate_missing_data(self):
        self.mining_section = 13.0
        # After you have generated a forecast - Does the total production equal
        # to x% of the TOTAL RESERVES?
        # -----------------------------------------------------------------------
        if not self.reservesFound and (self.generated_FC or self.generated_hist) and self.recovery_rate > 0:
            # generate this based on the mTotalProduction
            reserveEstimate = self.mTotalProduction * (1 / self.recovery_rate)

            self.mines['Reserve type'].append("Total Reserves")
            self.mines['Reserve year'].append(self.discountYear)
            self.mines['Reserves'].append(reserveEstimate)
            self.mines['Reserve unit'].append(self.mines['Production unit'][-1])
            self.mines['Reserves Source'].append("EST: Forecast Engine")
    
            if self.debugReserves:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % ("Total Reserves", "mines['Reserve type']")
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (self.discountYear, "mines['Reserve year']")
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (reserveEstimate, "mines['Reserves']")
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % (self.mines['Production unit'][-1], "mines['Reserve unit']")
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to %s list' % ("EST: Forecast Engine", "mines['Reserves Source']")
    
            if self.debugMode or self.debugReserves:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    'reserveEstimate:', reserveEstimate
            #
        # -----------------------------------------------------------------------
        if not self.resourcesFound and (self.generated_FC or self.generated_hist) and len(self.mines['Reserves']):
            # generate based on the reserves number
            resourceEstimate = float(self.mines['Reserves'][-1]) * (1 / self.resources_to_reserves)
            self.mines['Resource Type'].append("Total Resources")
            self.mines['Commodity'].append(self.commodities)
            self.mines['Resource Year'].append(self.discountYear)
            self.mines['Resource %'].append(resourceEstimate)
            self.mines['Resource unit'].append(self.mines['Reserve unit'][-1])
            self.mines['Resource Source'].append("EST: Forecast Engine")
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def log_sources(self):
        self.mining_section = 14.0
        if self.generated_FC or self.generated_hist:
            self.modelled += 1
            self.modelled_commod[self.key_commodity] += 1
        else:
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    " NOT MODELLED == " * 20
            self.not_modelled_commod[self.key_commodity] += 1
            self.not_modelled += 1
            self.thisWasModelled = False
    
            mComment = ""
            if not self.productionFound:
                mComment += "NO PRODUCTION "
            if not self.capacityFound:
                mComment += "NO CAPACITY "
            if not self.reservesFound:
                mComment += "NO RESERVES "
            if not self.resourcesFound:
                mComment += "NO RESOURCES"
            if not self.firstType1:
                self.error_log[0].append(self.NewMineId)
                self.error_log[1].append(0)
                self.error_log[2].append(mComment)
                self.error_log[3].append(self.mSession_key)
                self.error_log[4].append("ERROR TYPE 01")
                self.error_log[5].append("")
                self.error_log[6].append(0)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '!*' * 50
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s: %s' % (self.error_log[4][-1], self.error_log[2][-1])
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ''
                self.firstType1 = True
        #
        # -------------------------------------------------------------------------
        if not self.APSY:
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "** IN APSY " + "*" * 12
            self.ActualProductionStartYearSource = "EST: Forecast Engine"
        # -------------------------------------------------------------------------
        if not self.MEY:
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "** IN MEY " + "*" * 12
            if len(self.mines['Production Year']):
                self.mineEndYear = round(int(self.mines['Production Year'][-1]), 0)
                self.MineEndYearSource = 'EST:Forecast Engine'
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "Mine end year " + "=" * 20
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Year'][-1]:", self.mines['Production Year'][-1]
            else:
                self.mineEndYear = 0
        # -------------------------------------------------------------------------
        if not self.TML:
            if self.mineEndYear > 0:
                self.totalMineLife = self.mineEndYear - self.ActualProductionStartYear
            else:
                self.totalMineLife = 0
            self.TotalMineLifeSource = "EST: Forecast Engine"
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "** IN TML" + "*" * 12
                print '%s - %s:' % (self.NewMineId, self.mining_section),    self.mineEndYear
                print '%s - %s:' % (self.NewMineId, self.mining_section),    self.ActualProductionStartYear
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "Total mine life = " + str(self.totalMineLife)
        # -------------------------------------------------------------------------
        if not self.RML:
            if self.mineEndYear > 0:
                self.remainingMineLife = self.mineEndYear - self.discountYear
            else:
                self.remainingMineLife = 0
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "** IN RML " + "*" * 12
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "RML = " + str(self.remainingMineLife)
            self.remainingMineLife = self.mineEndYear - self.discountYear
            self.RemainingMineLifeSource = "EST: Forecast Engine"
        # -------------------------------------------------------------------------
        if not self.RMLY:
            if self.mineEndYear > 0:
                self.remainingMineLifeYear = round(int(self.discountYear), 0)
            else:
                self.remainingMineLife = 0
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "** IN RMLY " + "*" * 12
                print '%s - %s:' % (self.NewMineId, self.mining_section),    self.remainingMineLifeYear
        # -------------------------------------------------------------------------
        if self.totalMineLife > 100:
            mComment = "TOTAL MINE LIFE EXCEEDS 100 YEARS"
            self.error_log[0].append(self.NewMineId)
            self.error_log[1].append(0)
            self.error_log[2].append(mComment)
            self.error_log[3].append(self.mSession_key)
            self.error_log[4].append("ERROR TYPE 30")
            self.error_log[5].append("")
            self.error_log[6].append(0)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def estimate_recoverable_reserves(self):
        self.mining_section = 15.0
        self.estimated_total_recoverable_reserves = 0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production unit']:", self.mines['Production unit']
        for i in range(len(self.mines['Production Value'])):
            if self.mines['Production unit'][i] == "MMT" or self.mines['Production unit'][i] == "MT":
                prodFactor = 1
            else:
                prodUnit = self.mines['Production unit'][i]
                prodFactor = self.mining_units(prodUnit, "MMT")
            prodValue = float(self.mines['Production Value'][i]) * float(prodFactor)
            self.estimated_total_recoverable_reserves += prodValue
            if self.debugMode or self.debugReserves:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s added to estimated_total_recoverable_reserves' % prodValue
        if self.debugMode or self.debugReserves:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    '\n'
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'estimated_total_recoverable_reserves (final): %s' % self.estimated_total_recoverable_reserves
        param_vals = (self.estimated_total_recoverable_reserves, self.NewMineId, self.mSession_key)
        self.curr.execute('UPDATE mining_param_track SET estRecovReserves=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
        self.curr.execute('COMMIT')
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def calculate_mine_acreage(self):
        self.mining_section = 16.0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "-------- AGREAGE --------"
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'MineAcreageHectares:', self.MineAcreageHectares
        # commodities = commodities.split(';')[0] + ';'
        if self.MineAcreageHectares is None or self.MineAcreageHectares == 0:
    
            # Calculate global average hectares ----------------------------------------------------------------------------------------------------------
            sqlStatement = "SELECT a.minecountry, a.newMineid, b.res, b.reserveUnit, a.MineAcreageHectares, b.res/a.MineAcreageHectares, a.commodities "
            sqlStatement += "FROM mining_assets_daily a JOIN (SELECT reserveyear, newmineid, CAST(reserve AS DECIMAL(16,4)) AS res, reserveUnit FROM mining_reserves_daily "
            sqlStatement += "WHERE  reserveType = 'Total Reserves' AND NOT LENGTH(reserve) = 0 GROUP BY newmineid  "
            sqlStatement += "ORDER BY newmineid,reserveyear DESC)  b ON a.newMineid = b.newMineid WHERE a.MineAcreageHectares > 0 "
            if self.commod_list:
                commod_str = " OR ".join(["a.commodities LIKE '%%%s%%'" % commod for commod in self.commod_list])
                sqlStatement += "AND (%s) " % commod_str
            sqlStatement += ""
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    '\n'
                print '%s - %s:' % (self.NewMineId, self.mining_section),    sqlStatement
            self.curr.execute(sqlStatement)
            acreage_data = self.curr.fetchall()
            Haph = 0
            total_Haph = 0
            avg_Haph_global = 0
            global_count = 0
            for datarow in acreage_data:
                Hreserves = datarow[2]
                HreserveUnit = datarow[3]
                Hacreage = datarow[4]
                Hcommodity = datarow[6]
                # take the average
                if datarow[5] is not None and datarow[5] > 0:
                    Haph = float(datarow[5])
                    total_Haph += Haph
                    global_count += 1
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "** ACREAGE 3----->", pws(str(Hreserves), 18, 'R'), pws(HreserveUnit, 10), pws(str(Hacreage),12, 'R'), pws(str(Haph), 16, 'R'), pws(Hcommodity, 25, 'R')
    
            if global_count:
                avg_Haph_global = float(total_Haph) / float(global_count)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '\n'
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'total_Haph:', total_Haph
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "** Global AVERAGE (avg_Haph_global)----->", avg_Haph_global
    
            # Find the average hectares for this commodity in this country -------------------------------------------------------------------------------
            sqlStatement = "SELECT a.minecountry,a.newMineid,b.res,b.reserveUnit,a.MineAcreageHectares,b.res/a.MineAcreageHectares,a.commodities "
            sqlStatement += "FROM mining_assets_daily a JOIN (SELECT ReserveYear, newmineid, CAST(reserve AS DECIMAL(16,4)) AS res, reserveUnit "
            sqlStatement += "FROM Mining_Reserves_Daily WHERE  reserveType = 'Total Reserves'  AND NOT length(reserve) = 0 GROUP BY newmineid "
            sqlStatement += "ORDER BY newmineid,reserveyear desc ) b ON a.newmineid = b.newmineid WHERE a.MineAcreageHectares > 0 "
            if self.commod_list:
                commod_str = " OR ".join(["a.commodities LIKE '%%%s%%'" % commod for commod in self.commod_list])
                sqlStatement += "AND (%s) " % commod_str
            if self.mineCountry.count("'") > 0:
                sqlStatement += ' AND UCASE(a.minecountry) = "' + self.mineCountry.upper() + '" ' + " ORDER BY b.res DESC "
            else:
                sqlStatement += " AND UCASE(a.minecountry) = '" + self.mineCountry.upper() + "' " + " ORDER BY b.res DESC "
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                print '%s - %s:' % (self.NewMineId, self.mining_section),    sqlStatement
            self.curr.execute(sqlStatement)
            acreage_data = self.curr.fetchall()
            Haph = 0
            total_Haph = 0
            avg_Haph_country = 0
            country_count = 0
            for datarow in acreage_data:
                # Hreserves, HreserveUnit, Hacreage, Haph, Hcommodity = datarow7[2:]
                Hreserves = datarow[2]
                HreserveUnit = datarow[3]
                Hacreage = datarow[4]
                Hcommodity = datarow[6]
                # take the average
                # if Haph and Haph > 0:
                if datarow[5] is not None and datarow[5] > 0:
                    Haph = float(datarow[5])
                    if abs(avg_Haph_global - Haph) > (0.2 * avg_Haph_global):
                        pass
                    else:
                        total_Haph += Haph
                        country_count += 1
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "** ACREAGE----->", pws(str(Hreserves), 18, 'R'), pws(HreserveUnit, 10), pws(str(Hacreage), 12, 'R'), pws(str(Haph), 18, 'R'), pws(Hcommodity, 25, 'R')
    
            if country_count:
                avg_Haph_country = float(total_Haph) / float(country_count)
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '\n'
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'total_Haph:', total_Haph
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'avg_Haph_country = %s/%s' % (total_Haph, country_count)
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "** AVERAGE ratio (avg_Haph_country)----->", avg_Haph_country
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "Last reserves"
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Reserves']:", self.mines['Reserves']
    
                if len(self.mines['Reserves']):
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Reserve unit'][-1]:", self.mines['Reserve unit'][-1]
                    if self.mines['Reserve unit'][-1] == 'THOUSAND OUNCES':
                        self.MineAcreageHectares = (float(self.mines['Reserves'][-1]) * 0.0000000283495) / avg_Haph_country
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'MineAcreageHectares by avg_Haph_country(%s):' % avg_Haph_country, self.MineAcreageHectares
                    else:
                        self.MineAcreageHectares = float(self.mines['Reserves'][-1]) / avg_Haph_country
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    'MineAcreageHectares by avg_Haph_country(%s):' % avg_Haph_country, self.MineAcreageHectares
                    self.mineAcreageSource = "EST: Forecast Engine"
            else:
                # drop down and search by commodity by region
                # Find the average hectares for this commodity in this region
                sqlStatement = "SELECT a.minecountry,a.newMineid,b.res,b.reserveUnit,a.MineAcreageHectares, b.res/a.MineAcreageHectares,a.commodities "
                sqlStatement += "FROM mining_assets_daily a JOIN (select reserveyear,newmineid,CAST(reserve AS DECIMAL(16,4)) "
                sqlStatement += "AS res,reserveUnit FROM mining_reserves_daily WHERE reserveType='Total Reserves' AND NOT LENGTH(reserve)=0 GROUP BY newmineid  "
                sqlStatement += "ORDER BY newmineid,reserveyear desc)  b ON a.newmineid = b.newmineid WHERE a.MineAcreageHectares > 0 "
                if self.commod_list:
                    commod_str = " OR ".join(["a.commodities LIKE '%%%s%%'" % commod for commod in self.commod_list])
                    sqlStatement += "AND (%s) " % commod_str
                if self.mineCountry.count("'") > 0:
                    sqlStatement += ' AND UCASE(a.mineRegion) = "' + self.mineRegion.upper() + '" ' + " ORDER BY b.res DESC "
                else:
                    sqlStatement += " AND UCASE(a.mineRegion) = '" + self.mineRegion.upper() + "' " + " ORDER BY b.res DESC "
    
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    sqlStatement
                self.curr.execute(sqlStatement)
                acreage_data = self.curr.fetchall()
                Haph = 0
                total_Haph = 0
                avg_Haph_region = 0
                region_count = 0
                for datarow in acreage_data:
                    Hreserves = datarow[2]
                    HreserveUnit = datarow[3]
                    Hacreage = datarow[4]
                    Hcommodity = datarow[6]
    
                    # take the average
                    if datarow[5] is not None and datarow[5] > 0:
                        Haph = float(datarow[5])
                        if abs(avg_Haph_global - Haph) > (0.2 * avg_Haph_global):
                            pass
                            # print '%s - %s:' % (self.NewMineId, self.mining_section),    'flag asset %s' % datarow7[1]
                        else:
                            total_Haph += Haph
                            region_count += 1
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    "** ACREAGE 2----->", pws(str(Hreserves), 18, 'R'), pws(HreserveUnit, 10), pws(str(Hacreage), 12, 'R'), pws(str(Haph), 18, 'R'), pws(Hcommodity, 25, 'R')
    
                if region_count:
                    avg_Haph_region = float(total_Haph) / float(region_count)
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    '\n'
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'total_Haph:', total_Haph
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    "** Region AVERAGE (avg_Haph_region)----->", avg_Haph_region
                    if len(self.mines['Reserves']):
                        if self.debugMode:
                            print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Reserve unit'][-1]:", self.mines['Reserve unit'][-1]
                        if self.mines['Reserve unit'][-1] == 'THOUSAND OUNCES':
                            self.MineAcreageHectares = (float(self.mines['Reserves'][-1]) * 0.0000000283495) / avg_Haph_region
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'MineAcreageHectares by avg_Haph_region(%s):' % avg_Haph_region, self.MineAcreageHectares
                        else:
                            self.MineAcreageHectares = float(self.mines['Reserves'][-1]) / avg_Haph_region
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    'MineAcreageHectares by avg_Haph_region(%s):' % avg_Haph_region, self.MineAcreageHectares
                        self.mineAcreageSource = "EST: Forecast Engine"
                else:
                    if global_count:
                        if len(self.mines['Reserves']):
                            if self.debugMode:
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Reserves']:", self.mines['Reserves']
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Reserve unit'][-1]:", self.mines['Reserve unit'][-1]
                                print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                            if self.mines['Reserve unit'][-1] == 'THOUSAND OUNCES':
                                self.MineAcreageHectares = (float(self.mines['Reserves'][-1]) * 0.0000000283495) / avg_Haph_global
                                if self.debugMode:
                                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'MineAcreageHectares by avg_Haph_global(%s):' % avg_Haph_global, self.MineAcreageHectares
                            else:
                                self.MineAcreageHectares = float(self.mines['Reserves'][-1]) / avg_Haph_global
                                if self.debugMode:
                                    print '%s - %s:' % (self.NewMineId, self.mining_section),    'MineAcreageHectares by avg_Haph_global(%s):' % avg_Haph_global, self.MineAcreageHectares
                            self.mineAcreageSource = "EST: Forecast Engine"
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def update_forecasts(self):
        self.mining_section = 17.0
        sqlStatement = "INSERT INTO mining_Assets_Forecast ( "
        sqlData = "("
        for ii in range(len(self.fldAssetsList)):
            sqlStatement += self.fldAssetsList[ii] + ","
            #
            if self.fldAssetsList[ii] == '[mineDepth(Meters)]':
                cVal = self.mineDepth
            else:
                cVal = eval('self.' + self.fldAssetsList[ii])
            if cVal is None:
                cVal = ""
            if self.fldAssetsListDT[ii] == "c":
                if cVal.count("'") > 0:
                    sqlData += '"' + cVal + '",'
                else:
                    sqlData += "'" + cVal + "',"
            elif self.fldAssetsListDT[ii] == "i":
                # integer
                if len(str(cVal).strip()) > 0:
                    sqlData += str(cVal) + ","
                else:
                    sqlData += str(cVal) + "0,"
            else:
                sqlData += str(cVal) + ","
        # remove last char
        sqlStatement = sqlStatement[:-1] + ") VALUES " + sqlData[:-1] + ") "
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "ASSETS DAILY"
            print '%s - %s:' % (self.NewMineId, self.mining_section),    sqlStatement
            print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
        self.curr.execute(sqlStatement)
        self.curr.execute("commit;")
        #
        mining_base = []
        mining_base.append("NewMineId")
        mining_base.append("mineName")
        mining_base.append("mineCountry")
        mining_base.append("state")
        mining_base.append("mineRegion")
        mining_base.append("mineStage")
        mining_baseDT = ['i', 'c', 'c', 'c', 'c', 'c']
        mining_base_data = str(int(self.NewMineId)) + ","
        #
        if self.mineName is None:
            mining_base_data += '"",'
        elif self.mineName.count("'") > 0:
            mining_base_data += '"' + self.mineName + '",'
        else:
            mining_base_data += "'" + self.mineName + "',"
        #
        if self.mineCountry is None:
            mining_base_data += '"",'
        elif self.mineCountry.count("'") > 0:
            mining_base_data += '"' + self.mineCountry + '",'
        else:
            mining_base_data += "'" + self.mineCountry + "',"
        #
        if self.state is None:
            mining_base_data += '"",'
        elif self.state.count("'") > 0:
            mining_base_data += '"' + self.state + '",'
        else:
            mining_base_data += "'" + self.state + "',"
        #
        if self.mineRegion is None:
            mining_base_data += '"",'
        elif self.mineRegion.count("'") > 0:
            mining_base_data += '"' + self.mineRegion + '",'
        else:
            mining_base_data += "'" + self.mineRegion + "',"
        #
        mining_base_data += "'" + self.mineStage + "',"
        # ------------------------------------------------------------------------------------------
        # Update the capacity forecast table based on the values in the array
        if self.createdMetalProduction:
            self.capacityFound = False
        if len(self.mines['Capacity year']) and not self.capacityFound:
            # add capacity data
            sqlStatement_capacity = "INSERT INTO mining_capacity_forecast" + \
                                    "(newMineid,mineName,mineCountry,state,mineRegion,mineStage," + \
                                    "capacityType,CommodityByCapacity,capacityYear,capacity,capacityUnit,source,Mineid) VALUES ("
    
            sqlStatement = sqlStatement_capacity
            for i in range(len(self.mines['Capacity year'])):
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "----> " + str(i), self.mines['Capacity year'][i], self.mines['Capacity'][i], self.mines['Capacity unit'][i]
    
                CommodityByCapacity = self.commodities
                capacityType = self.mines['Capacity type'][i]
                capacityYear = self.mines['Capacity year'][i]
                capacity = self.mines['Capacity'][i]
                source = self.mines['Capacity Source'][i]
    
                if self.mines['Capacity unit'][i] == "MMT" or self.mines['Capacity unit'][i] == "MT":
                    capacityUnit = "MTPA"
                else:
                    capacityUnit = self.mines['Capacity unit'][i]
    
                if capacityType == 'ROM Production':
                    capacityType = 'ROM Capacity'
                    CommodityByCapacity = ''
                    if not capacityUnit == "MTPA":
                        capacityFactor = self.mining_units(capacityUnit, "MMT")
                        capacity = float(self.mines['Capacity'][i]) * float(capacityFactor)
                        capacityUnit = "MTPA"
    
                sqlStatement += mining_base_data + "'" + capacityType + "','" + CommodityByCapacity + "'," + \
                                str(capacityYear) + "," + str(capacity) + ",'" + capacityUnit + "'"
                if source.count("'") > 0:
                    sqlStatement += ', "%s"' % source
                else:
                    sqlStatement += ", '%s'" % source
                sqlStatement += ', %s)' % self.Mineid
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "CAPACITY FORECAST"
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    sqlStatement
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                self.curr.execute(sqlStatement)
                self.curr.execute("commit;")
                sqlStatement = sqlStatement_capacity
        # ------------------------------------------------------------------------------------------
        # Update the reserves forecast table
        # HOWEVER, we only look at the last year.
        # Should we fill in the reserves number until the discount year?
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "RESERVES FORECAST"
            print '%s - %s:' % (self.NewMineId, self.mining_section),    'reservesFound:', self.reservesFound
            print '%s - %s:' % (self.NewMineId, self.mining_section),    '\n'
        if len(self.mines['Reserve year']) > 1 and not self.reservesFound:
            # reserves
            # resources
            sqlStatement_reserve = "INSERT INTO mining_reserves_forecast (newMineid,mineName,mineCountry,state,mineRegion,mineStage,reserveType,"
            # sqlStatement_reserve += "CommodityByReserve,reserveYear,reserve,reserveUnit,source,Mineid) VALUES ("
            sqlStatement_reserve += "reserveYear,reserve,reserveUnit,source,Mineid) VALUES ("
    
            sqlStatement = sqlStatement_reserve
            for i in range(len(self.mines['Reserve year']) - 1):
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "----> " + str(i), self.mines['Reserve year'][i], self.mines['Reserves'][i], self.mines['Reserve unit'][i]
                reserveType = "Total Reserves"
                CommodityByReserve = self.commodities.strip()[:50]
                reserveYear = self.mines['Reserve year'][i]
                reserve = self.mines['Reserves'][i]
                if self.mines['Reserve unit'][i] == "MTPA":
                    reserveUnit = "MMT"
                else:
                    reserveUnit = self.mines['Reserve unit'][i]
                    reserveFactor = self.mining_units(reserveUnit, "MMT")
                    reserve = float(self.mines['Reserves'][i]) * float(reserveFactor)
                    reserveUnit = "MMT"
                source = self.mines['Reserves Source'][i]
                #
                # sqlStatement += mining_base_data+"'"+reserveType+"','"+CommodityByReserve+"',"+str(reserveYear)+","+str(reserve)+",'"+reserveUnit+"'"
    
                sqlStatement += mining_base_data + "'" + reserveType + "'," + str(reserveYear) + "," + str(
                    reserve) + ",'" + reserveUnit + "'"
                if source.count("'") > 0:
                    sqlStatement += ', "%s"' % source
                else:
                    sqlStatement += ", '%s'" % source
                sqlStatement += ', %s)' % self.Mineid
                if self.debugMode or self.debugReserves:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "RESERVES FORECAST"
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    sqlStatement
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    '\n'
                self.curr.execute(sqlStatement)
                self.curr.execute('COMMIT')
                sqlStatement = sqlStatement_reserve
        # ------------------------------------------------------------------------------------------
        # Update the resources forecast table based on the values in the array
        # All are in the array
        if len(self.mines['Resource Year']) and not self.resourcesFound:
            # resources
            sqlStatement_resource = "INSERT INTO mining_resource_forecast (newMineid,mineName,mineCountry,state,mineRegion,mineStage,"
            # sqlStatement_resource += "resourceType,CommodityByResource,resourceYear,resource,resourceUnit,source,Mineid) VALUES ("
            sqlStatement_resource += "resourceType,resourceYear,resource,resourceUnit,source,Mineid) VALUES ("
    
            sqlStatement = sqlStatement_resource
            for i in range(len(self.mines['Resource Type']) - 1):
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "----> " + pws(str(i), 5, 'R'), pws(str(i), 20, self.mines['Resource Type'][i]), \
                        pws(str(i), 6), pws(fwc(str(round(float(self.mines['Resource Year'][i]), 6)).strip()), 15, 'R'), self.mines['Resource %'][i]
                resourceType = "Total Resources"
                CommodityByResource = self.commodities.strip()[:50]
                resourceYear = self.mines['Resource Year'][i]
                resource = self.mines['Resource %'][i]
                resourceUnit = self.mines['Resource unit'][i]
                source = self.mines['Resource Source'][i]
    
                if self.mines['Resource unit'][i] == "MTPA":
                    resourceUnit = "MMT"
                else:
                    resourceUnit = self.mines['Reserve unit'][i]
                    resourceFactor = self.mining_units(resourceUnit, "MMT")
                    resource = float(self.mines['Resource %'][i]) * float(resourceFactor)
                    resourceUnit = "MMT"
                #
                sqlStatement += mining_base_data + "'" + resourceType + "'," + str(resourceYear) + "," + str(resource) + ",'" + resourceUnit + "'"
    
                if source.count("'") > 0:
                    sqlStatement += ', "%s"' % source
                else:
                    sqlStatement += ", '%s'" % source
                sqlStatement += ', %s)' % self.Mineid
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "RESOURCE FORECAST"
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    sqlStatement
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                self.curr.execute(sqlStatement)
                self.curr.execute("commit;")
                sqlStatement = sqlStatement_resource
        # ------------------------------------------------------------------------------------------
        # Update the production forecast table based on the values in the array
        if len(self.mines['Production Year']):
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "=" * 30
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Year']:", self.mines['Production Year']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "LENGTH: " + str(len(self.mines['Production Year']))
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Value']:", self.mines['Production Value']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "LENGTH: " + str(len(self.mines['Production Value']))
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production unit']:", self.mines['Production unit']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "LENGTH: " + str(len(self.mines['Production unit']))
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Source']:", self.mines['Production Source']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "LENGTH: " + str(len(self.mines['Production Source']))
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "=" * 30
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "mines['Production Type']:", self.mines['Production Type']
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "LENGTH: " + str(len(self.mines['Production Type']))
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "=" * 30
            sqlStatement_production = "INSERT INTO mining_production_forecast (newMineid,mineName,mineCountry,state,mineRegion,mineStage,productionType,"
            sqlStatement_production += "productionYear,productionValue,productionUnit,source,Mineid) VALUES ("
    
            sqlStatement = sqlStatement_production
            mining_baseDT.append('c')
            mining_baseDT.append('c')
            mining_baseDT.append('i')
            mining_baseDT.append('i')
            mining_baseDT.append('c')
            mining_baseDT.append('c')
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "len(mines['Production Year']):", len(self.mines['Production Year'])
                print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
            for i in range(len(self.mines['Production Year'])):
                if self.debugMode:
                    print '%s - %s:' % (self.NewMineId, self.mining_section),    "----> " + pws(str(i), 5, 'R'), pws(str(self.mines['Production Year'][i]), 6), pws(
                        fwc(str(float(self.mines['Production Value'][i])).strip()), 15, 'R'), self.mines['Production Source'][i]
                productionType = "ROM Production"
                productionByCommodity = self.commodities
                productionYear = self.mines['Production Year'][i]
    
                if self.mines['Production unit'][i] == "MMT" or self.mines['Production unit'][i] == "MT":
                    productionUnit = "MTPA"
                    prodFactor = 1
                else:
                    # translate back into MTPA
                    productionUnit = self.mines['Production unit'][i]
                    prodFactor = self.mining_units(productionUnit, "MMT")
                    productionUnit = "MTPA"
                productionValue = float(self.mines['Production Value'][i]) * float(prodFactor)
    
                source = self.mines['Production Source'][i]
                sqlStatement += mining_base_data + "'" + productionType + "'," + str(productionYear) + "," + str(productionValue) + ",'" + productionUnit + "'"
    
                if source[-1] == '\\':
                    source += ' '
    
                if source.count("'") > 0:
                    sqlStatement += ', "%s"' % source
                else:
                    sqlStatement += ", '%s'" % source
    
                sqlStatement += ', %s)' % self.Mineid
    
                try:
                    self.curr.execute(sqlStatement)
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'sqlStatement:', sqlStatement
                except:
                    sqlStatement = unicode(sqlStatement.encode('utf-8').strip(), errors='ignore')
                    if self.debugMode:
                        print '%s - %s:' % (self.NewMineId, self.mining_section),    'sqlStatement:', sqlStatement
                    self.curr.execute(sqlStatement)
                self.curr.execute("commit;")
                sqlStatement = sqlStatement_production
            param_vals = (productionYear, self.NewMineId, self.mSession_key)
            self.curr.execute('UPDATE mining_param_track SET mineEndYear=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
            self.curr.execute('COMMIT')
        prevEL4 = ""
        prevMineId = 0
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "%-" * 30
            print '%s - %s:' % (self.NewMineId, self.mining_section),    len(self.error_log[0]), self.error_log[0]
            print '%s - %s:' % (self.NewMineId, self.mining_section),    len(self.error_log[1]), self.error_log[1]
            print '%s - %s:' % (self.NewMineId, self.mining_section),    len(self.error_log[2]), self.error_log[2]
            print '%s - %s:' % (self.NewMineId, self.mining_section),    len(self.error_log[3]), self.error_log[3]
            print '%s - %s:' % (self.NewMineId, self.mining_section),    len(self.error_log[4]), self.error_log[4]
            print '%s - %s:' % (self.NewMineId, self.mining_section),    len(self.error_log[5]), self.error_log[5]
            print '%s - %s:' % (self.NewMineId, self.mining_section),    len(self.error_log[6]), self.error_log[6]
        '''
        self.error_log[0].append(self.NewMineId)
        self.error_log[1].append(self.mines['Production Year'][-1])
        self.error_log[2].append(mComment)
        self.error_log[3].append(self.mSession_key)
        self.error_log[4].append("ERROR TYPE 28")
        self.error_log[5].append(self.mines['Production Value'][-2])
        self.error_log[6].append(self.mines['Production Value'][-1])
        '''
        for ii in range(0, len(self.error_log[4])):
            if ii > 0:
                if self.thisWasModelled:
                    commodity_status = "MODELLED - "
                else:
                    commodity_status = "NOT MODELLED - "
                #if not prevEL4 == self.error_log[4][ii]:
                eSymbol = buildMySQLin(15, "%s")
                self.save_error_log(commodity_status + self.error_log[2][ii], eSymbol, ii)
                #prevEL4 = self.error_log[4][ii]
        # ------------------------------------------------------------------------------------------
        if self.debugMode:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    '\n\n'
        firstTime = True
        #
        self.pt_ran = False
        self.octr_ran = False
        self.rr_ran = False
        # evaluate the asset
        # ------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def conclude_processing(self):
        self.mining_section = 18.0
        del self.mines
        del self.error_log
        self.recsProcessed += 1
        if self.mTotRecs > 0:
            print '%s - %s:' % (self.NewMineId, self.mining_section),    ""
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "Record " + str(self.recsProcessed) + "/" + str(self.mTotRecs) + \
                  " -------> " + str((self.recsProcessed / self.mTotRecs) * 100) + "%"
            print '%s - %s:' % (self.NewMineId, self.mining_section),    "Modelled: " + str(self.modelled) + "  ------  Not Modelled: " + str(self.not_modelled) + \
                  " -      Total time: " + str((time.time() - self.runningTime) / 60)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def generate_records(self):
        self.mining_section = 19.0
        for commodity in self.modelled_commod.keys():
            print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s/%s %s mines modelled' % (self.modelled_commod[commodity], self.all_commodities[commodity], commodity)
        for commodity in self.not_modelled_commod.keys():
            print '%s - %s:' % (self.NewMineId, self.mining_section),    '%s/%s %s mines not modelled' % (self.not_modelled_commod[commodity], self.all_commodities[commodity], commodity)

        for key in self.all_commodities.keys():
            if self.debugMode:
                print '%s - %s:' % (self.NewMineId, self.mining_section),    "Key: " + key
            self.ts = time.time()
            self.st = datetime.fromtimestamp(self.ts).strftime('%Y-%m-%d %H:%M:%S')
            if self.modelled_commod.has_key(key):
                num_modelled = self.modelled_commod[key]
            if self.not_modelled_commod.has_key(key):
                num_not_modelled = self.not_modelled_commod[key]
            # find the modelled number
            sqlStatement = "INSERT INTO mining_metrics (session_key,commodity,modelled,not_modelled,add_by) VALUES (%s, %s, %s, %s, %s)"
            self.curr.execute(sqlStatement, (self.mSession_key, key, num_modelled, num_not_modelled, self.userName))
            self.curr.execute('COMMIT')
        self.curr.close()
        self.conn.close()
        timeEnded = datetime.now()
        self.dt = timeEnded.timetuple()
        self.mProgComment += "\n" + "Mining models Program ended at :" + get_datetime() + "\n"
        self.mProgComment += "\nTotal time: " + str((time.time() - self.runningTime) / 60)
        out_fname = "MINING_MODELS_" + "_" + get_julian_date() + "_" + get_time_string()
        print '%s - %s:' % (self.NewMineId, self.mining_section),    self.mProgComment

        fo = open(self.mOutputLogsDir + out_fname + ".txt", "w")
        fo.write(self.mProgComment + "\n")
        fo.flush()
        fo.close()
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def process_mining_data(self):
        self.get_mining_data()
        for mine_datarow in self.mining_data:
            self.initialize_mining_variables(mine_datarow)
            self.get_equity_data()
            self.get_reserves_data()
            self.get_capacity_data()
            self.get_resource_data()
            self.get_production_data()
            self.convert_units()
            self.process_missing_data()
            self.decide_forecast_process()
            self.generate_historical()
            self.generate_prod_forecast()
            self.process_forecast_data()
            self.estimate_missing_data()
            self.log_sources()
            self.estimate_recoverable_reserves()
            self.calculate_mine_acreage()
            self.update_forecasts()
            self.conclude_processing()
        self.generate_records()
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def mining_main(self):
        if self.importTables:
            self.import_mining_tables()
            self.make_local_data()

        if self.updateTables:
            self.update_mining_ore_grade()
            self.update_saleable_to_rom()
            self.update_total_factors()
    
        if self.processData:
            self.process_mining_data()
    
        if self.lUpdateRemote:
            self.update_forecast()

        if self.updateServer:
            update_servers('mining', export_tables=True, import_tables=True)

if __name__=='__main__':
    Forecast = MiningForecast(mine_list=[], importTables=False, updateTables=True, processData=False, forecastData=False, updateServer=False, debugAll=True)
    Forecast.mining_main()