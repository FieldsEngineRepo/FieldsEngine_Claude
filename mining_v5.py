from __future__ import division

import platform
import time
import pymysql
import pymysql.cursors
import datetime
import sys
import os
import math
import operator
import pypyodbc

import numpy as np

from time import sleep
from os import listdir
from os.path import isfile, join
from datetime import datetime,date,timedelta

from globaldata import *
from data_export import update_servers

curpath = os.path.dirname(__file__)


# ======================================= #
                                          #
mine_ID              = 0                  #
minimumForecastMax   = 8                  #
prodDecimals         = 2                  #
discountYear         = 2019               #
years_to_project     = 7                  #
pct_of_capacity      = 0.90               #
production_tolerance = 0.2                #
last_year_fctr       = 0.5                #
ore_cap_to_rom       = 0.96               #
reserve_tot_resource = 0.80               #
yearly_effeciency    = 0.0025             #
ye_lt5               = 0.025              #
ye_lt10              = 0.0025             #
ye_lt20              = 0.00025            #
sale_yield           = 0.75               #
resc_to_resv         = 0.5                #
meas_to_total        = 0.5/resc_to_resv   #
ind_to_total         = 0.4/resc_to_resv   #
inf_to_total         = 0.3/resc_to_resv   #
                                          #
# ======================================= #

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def mining_units(curr,fromUnit,toUnit,printSQL=False):
    conv_factor = 0.0
    sql_select = 'SELECT unitFactor FROM mining_unit_conversion WHERE fromUnit="%s" AND toUnit="%s"' % (fromUnit, toUnit)
    curr.execute(sql_select)
    ret_val = curr.fetchone()
    if ret_val:
        conv_factor = float(ret_val[0])
    return conv_factor
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def check_exception_log(curr,conn,mine_id,mMine_name,mCountry,mState,mRegion,mComment,mCommodities,mPeriod,mSessionKey,mErrorType):
    ret_val = False
    sql_statement = ""
    if len(mErrorType.strip()) > 0:
        sql_statement += "error_Type = '" + mErrorType + "' AND "
    if len(mComment.strip()) > 0:
        sql_statement += "comment = '" + mComment + "' AND "
    if len(sql_statement) > 0:
        sql_statement = "SELECT * FROM mining_error_log_exceptions WHERE " + sql_statement[:-4]
        curr.execute(sql_statement)
        r2 = curr.fetchall()
        for datarow in r2:
            ret_val = True
    return ret_val
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def save_error_log(curr,conn,new_mine_id,mMineid,mMine_name,mCountry,mState,mRegion,mComment,mCommodities,mPeriod,mSessionKey,mErrorType,eSymbol,mParam,mParam_value):
    if check_exception_log(curr,conn,new_mine_id,mMine_name,mCountry,mState,mRegion,mComment,mCommodities,mPeriod,mSessionKey,mErrorType):
        pass
    else:
        ts = time.time()
        userName = getpass.getuser()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')          
        fieldList = "newMineid,Mineid,minename,minecountry,state,mineregion,comment,commodities,period,param_value,nparam_value,session_key,Error_Type,add_by,add_date"  # add terrain back in
        sql_statement = "INSERT INTO mining_error_log (" +fieldList+") VALUES " + eSymbol # (?,?,?,?,?,?,?,?,?,?)" # --
        
        curr.execute(sql_statement,(int(new_mine_id),mMineid,mMine_name,mCountry,mState,mRegion,mComment,mCommodities,mPeriod,mParam,float(mParam_value),mSessionKey,mErrorType,userName,st))
        conn.commit()

#========================================================================================================================================================================

def get_param_detail(curr,param_name,mineid,mCountry,mRegion,mStage,mMineType,mMineMethod,mCommodity,mOperators,extraWhere,extraVars,debugMode=False):
    param_type = ""
    if param_name == "FIRST_YEAR_FACTOR" or param_name == "LAST_YEAR_FACTOR":
        pass
    if debugMode:
        print "In PARAMDETAIL "
        print 'extraWhere:', extraWhere
        print 'extraVars:', extraVars
        print 'param_name:', param_name
        print "+"*25
    # ----------------------------------------------------------------------------------------------------
    ret_val = ""
    mPoints = 0
    lmineid = 0
    lRegion = 0
    lCommodity = 0
    param = []
    param_points = []  # <----------------- Score
    param_ans = []
    if param_name in ("YEARS_TO_PROJECT","PRODUCTION_TOLERANCE","LAST_YEAR_FACTOR","ORE_CAPACITY_TO_ROM","RECOVERY_RATE","RESOURCES_TO_RESERVES",
                      "CAPACITY_TO_PRODUCTION","BASE_UNIT","FIRST_YEAR_FACTOR","SALEABLE_PRODUCTION_YIELD_FACTOR","METALLURGICAL_RECOVERY_FACTOR","ORE_GRADE"):
        if debugMode:
            print 'param_name:', param_name+" ""+^"*20
        p_num = 0      # <-------------- 
        param_type = "MODEL_RULES"
        sql_statement = '''SELECT
rtrim(param_value) as pvalue,
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
        if debugMode:
            print sql_statement
            print 'param_name:', param_name
            print "$="*20        
        curr.execute(sql_statement) 
    # ----------------------------------------------------------------------------------------------------
    else:
        if debugMode:
            print "ALL OTHER PARAM NAMES"
            print "IN SQL----"
            print 'mStatus:', mStatus
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
        curr.execute(sql_statement+";",(param_name,))
    # ----------------------------------------------------------------------------------------------------
    r2 = curr.fetchall()
    for datarow in r2:
        mPoints = 0
        goAhead = 1
        extraParse = " goAhead "
        # ----------------------------------------------- CHECK FOR EVERY LINE
        if param_name == "XFIRST_YEAR_FACTOR" or param_name == "XLAST_YEAR_FACTOR":
            # if debugMode:
            #    print "in FIRST_YEAR_FACTOR"
            # add code to parde the params_id field
            fldParse = datarow[1]
            if fldParse.count("=") > 0:
                posDash = fldParse.index("=")
                fldVar2 = fldParse[posDash+1:]                        
                extraParse = " float(" + str(extraWhere) + ") == float(" + fldVar2 + ") "                
            elif fldParse.count(">") > 0:
                #
                posDash = fldParse.index(">")
                fldVar2 = fldParse[posDash+1:]                        
                extraParse = " float(" + str(extraWhere) + ") > float(" + fldVar2 + ") "
            elif fldParse.count("<") > 0:
                #
                posDash = fldParse.index("<")
                fldVar2 = fldParse[posDash+1:]                        
                extraParse = " float(" + str(extraWhere) + ") < float(" + fldVar2 + ") "
            elif fldParse.count("-") > 0:
                #
                posDash = fldParse.index("-")
                fldVar1 = fldParse[:posDash]
                fldVar2 = fldParse[posDash+1:]
                extraParse = "  float(" + str(extraWhere) + ") <= float(" + fldVar1 + ") and float("  + \
                             str(extraWhere) + ") > float(" + fldVar2 + ") "
            else:
                extraParse = " goAhead "
            if eval(extraParse):
                mPoints = 15000
                goAhead = 1
            else:
                goAhead = 0
        # --------------------------------------------------------------------------
        # MineId
        if datarow[2] is None or str(datarow[2]) =='0' or len(datarow[2].strip()) == 0:
            goAhead = 1
        else:
            if str(mineid) == str(datarow[2]) and eval(extraParse) :
                mPoints = 10000                    
                if debugMode:
                    print str(datarow[0]) +" <-->" + datarow[2] + " Points " + str(mPoints)
                lAsset_id = 1
                goAhead = 0
        # ----------------------------------------------------------------------
        # Mine Region
        if goAhead and len(datarow[4].strip()) > 0   :
            if mRegion.strip().upper() == datarow[4].strip().upper() and eval(extraParse):
                lRegion = 1
                mPoints += 10
                if debugMode:
                    print str(datarow[0]) +" <-->" + datarow[4] + " Region " + str(mPoints)
            else:
                # no match, do not advance, erase all points
                goAhead = 0
                mPoints = 0
        else:
            # no points, but move ahead
            pass
        # ------------------------------------------------------------------------------------------
        # Mine Country
        if goAhead and len(datarow[3].strip()) > 0   :
            if mCountry.strip().upper() == datarow[3].strip().upper() and eval(extraParse):
                lCountry = 1
                mPoints += 50
                if debugMode:
                    print str(datarow[0]) +" - " + datarow[3] + " Country "  + str(mPoints)                  
            else:
                # no match, do not advance, erase all points
                goAhead = 0
                mPoints = 0
        else:
            # no points, but move ahead
            pass
        # ------------------------------------------------------------------------------------------
        # Mine State
        if goAhead and len(datarow[5].strip()) > 0  :
            if mState.strip().upper() == datarow[5].strip().upper() and eval(extraParse):
                lState = 1
                mPoints += 100
                if debugMode:
                    print str(datarow[0]) +" - " + datarow[5] + " State "+ str(mPoints)
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
        if goAhead and len(datarow[6].strip()) > 0   :
            if mStage.strip().upper() == datarow[6].strip().upper() and eval(extraParse):
                lStage = 1
                mPoints += 200
                if debugMode:
                    print str(datarow[6]) +" - " + datarow[6] + " Stage "   + str(mPoints)
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
        if goAhead  and len(datarow[7].strip()) > 0:
            if debugMode:
                print extraParse
                print param_name
                print "="*25
            if datarow[7] is None or eval(extraParse) is None or mMineType is None:
                goAhead = 0
                mPoints = 0
            elif mMineType.strip().upper() == datarow[7].strip().upper() and eval(extraParse) :
                lMineType = 1
                mPoints += 600
                if debugMode:
                    print str(datarow[0]) +" - " + datarow[7] + " Mine Type "   + str(mPoints)
            else:
                # no match, do not advance, erase all points
                goAhead = 0
                mPoints = 0
        else:
            # no points, but move ahead
            pass
        # ------------------------------------------------------------------------------------------
        # Mine Method
        if goAhead and len(datarow[8].strip()) > 0 :
            if mMineMethod.strip().upper() == datarow[8].strip().upper() and eval(extraParse) :
                lMineMethod = 1
                mPoints += 800
                if debugMode:
                    print str(datarow[0]) +" - " + datarow[8] + " Mine Method "   + str(mPoints)
            else:
                # no match, do not advance, erase all points
                goAhead = 0
                mPoints = 0
        else:
            # no points, but move ahead
            pass
        # ------------------------------------------------------------------------------------------
        # Mine Commodity
        if goAhead and len(datarow[9].strip()) > 0 :
            if mCommodity.strip().upper() == datarow[9].strip().upper() and eval(extraParse):
                lCommodity = 1
                mPoints += 1000
                if debugMode:
                    print str(datarow[0]) +" - " + datarow[9] + " Mine Commodity "   + str(mPoints)
            else:
                # no match, do not advance, erase all points
                goAhead = 0
                mPoints = 0
        else:
            # no points, but move ahead
            pass
        # ------------------------------------------------------------------------------------------
        # Mine Operator
        if goAhead and len(datarow[10].strip()) > 0 :
            if mCommodity.strip().upper() == datarow[10].strip().upper() and eval(extraParse):
                lOperator = 1
                mPoints += 3000
                if debugMode:
                    print str(datarow[0]) +" - " + datarow[9] + " Mine operator "   + str(mPoints)
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
                if debugMode:
                    print str(datarow[0]) +" ***** " + datarow[11] + " BASE PARAMETER FOUND "   + str(mPoints)
            else:
                # no match, do not advance, erase all points
                goAhead = 0
                mPoints = 0
        else:
            # no points, but move ahead
            pass
        # ------------------------------------------------------------------------------------------
        if mPoints > 0 :
            param_points.append(mPoints)
            param_ans.append(datarow[p_num])
            if debugMode:
                print "POINTS ----> " + str(mPoints)
                print extraParse
        # check each criteria against the asset if there is a match add to the array
        mPoints = 0
    # ----------------------------------------------------------------------------------------------------
    if len(param_points) > 0:
        mPoints = max(param_points)
        fmIndex = param_points.index(mPoints)
        ret_val = param_ans[fmIndex]
        if debugMode:
            print param_name + " (param_name) chosen(ret_val): "+str(ret_val)
            print 'fmIndex:', fmIndex
            print "Points -->" + str(mPoints)
            print "------------------------------------------------------"  
    return ret_val

#========================================================================================================================================================================

def get_asset_data(curr,mine_id,data_table,data_type):
    data_names = {
    'production':{     'type': 'productionType',
                  'commodity': 'productionByCommodity',
                      'value': 'productionValue',
                       'year': 'productionYear',
                       'unit': 'productionUnit'},

      'capacity':{     'type': 'capacityType',
                  'commodity': 'CommodityByCapacity',
                      'value': 'capacity',
                       'year': 'capacityYear',
                       'unit': 'capacityUnit'},

      'reserves':{     'type': 'reserveType',
                  'commodity': 'CommodityByReserve',
                      'value': 'reserve',
                       'year': 'reserveYear',
                       'unit': 'reserveUnit'},

      'resource':{     'type': 'resourceType',
                  'commodity': 'CommodityByResource',
                      'value': 'resource',
                       'year': 'resourceYear',
                       'unit': 'resourceUnit'}
    }
    data = data_names[data_table]
    params = (data['type'], data['commodity'], data['value'], data['year'], data['unit'], data_table, mine_id, data['type'], data_type, data['value'])

    sql_select  = "SELECT NewMineId,%s,%s,%s,%s,%s,source FROM mining_%s_daily WHERE NewMineId=%s AND %s='%s' AND %s > 0 " % params
    sql_select += "AND LENGTH(source) > 0 AND NOT (source='EST: Forecast Engine ' OR source LIKE '%GlobalData Estimation%') "

    if data_table in []:
        discount_year = get_discount_year(curr)
        sql_select += "AND %s < %s " % (data['year'], discount_year)

    sql_select += ""
    sql_select += "ORDER BY %s,%s,%s ASC " % (data['type'], data['commodity'], data['year'])
    curr.execute(sql_select)
    asset_data = curr.fetchall()

    if not asset_data:
        asset_data = ()

    return asset_data
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_asset_datatypes(curr,mine_id,data_table):
    data_names = {
    'production':{     'type': 'productionType',
                  'commodity': 'productionByCommodity',
                      'value': 'productionValue',
                       'year': 'productionYear',
                       'unit': 'productionUnit'},

      'capacity':{     'type': 'capacityType',
                  'commodity': 'CommodityByCapacity',
                      'value': 'capacity',
                       'year': 'capacityYear',
                       'unit': 'capacityUnit'},

      'reserves':{     'type': 'reserveType',
                  'commodity': 'CommodityByReserve',
                      'value': 'reserve',
                       'year': 'reserveYear',
                       'unit': 'reserveUnit'},

      'resource':{     'type': 'resourceType',
                  'commodity': 'CommodityByResource',
                      'value': 'resource',
                       'year': 'resourceYear',
                       'unit': 'resourceUnit'}
    }
    data = data_names[data_table]
    params = (data['type'], data_table, mine_id, data['value'])

    sql_select  = "SELECT DISTINCT {0} FROM mining_{1}_daily WHERE NewMineId={2} AND {3} > 0 AND LENGTH(source) > 0 AND NOT (source='EST: Forecast Engine ' OR source LIKE '%GlobalData Estimation%') ".format(*params)

    if data_table in []:
        discount_year = get_discount_year(curr)
        sql_select += "AND %s < %s " % (data['year'], discount_year)

    curr.execute(sql_select)
    asset_datatypes = curr.fetchall()
    if not asset_datatypes:
        asset_datatypes = []
    else:
        asset_datatypes = [str(data[0]) for data in asset_datatypes]
    return asset_datatypes

#========================================================================================================================================================================

def get_mine_element(curr,commodity):
    mine_element = ''
    curr.execute('SELECT elementName FROM mining_compounds WHERE commodity="%s"' % commodity)
    mine_element = curr.fetchone()[0]
    return mine_element
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_param_avg(curr, value_col, param_table, param_col='', param='', commodity_col='', commodity='', ore_grade_unit='', range_col='', range='', data_type_col='', data_type='', sql_where=''):
    param_avg = 0.0
    sql_select = 'SELECT {} FROM {} WHERE {}="{}" AND {}="{}" '.format(value_col, param_table, param_col, param, commodity_col, commodity, ore_grade_unit)
    if range_col:
        sql_select += 'AND {}="{}" '.format(range_col, range)
    if sql_where:
        sql_select += sql_where
    if data_type_col:
        sql_select += 'AND {}="{}" '.format(data_type_col, data_type)
    print sql_select
    curr.execute(sql_select)
    param_vals = [float(data[0]) for data in curr.fetchall()]
    if len(param_vals) > 0:
        val_count = float(len(param_vals))
        param_avg = float(sum(param_vals))/float(val_count)
    return param_avg
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ore_country_avg(curr, commodity, country, ore_grade_unit):
    sql_extra = 'AND oreGradeUnit="{}"'.format(ore_grade_unit)
    ore_grade = get_param_avg(curr, 'oreGrade', 'mining_ore_grade', 'mineCountry', country, 'commodity', commodity, ore_grade_unit=ore_grade_unit, sql_where=sql_extra)
    return ore_grade
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ore_region_avg(curr, commodity, region, ore_grade_unit):
    sql_extra = 'AND oreGradeUnit="{}"'.format(ore_grade_unit)
    ore_grade = get_param_avg(curr, 'oreGrade', 'mining_ore_grade', 'mineRegion', region, 'commodity', commodity, ore_grade_unit=ore_grade_unit, sql_where=sql_extra)
    return ore_grade
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ore_global_avg(curr, commodity, ore_grade_unit):
    sql_extra = 'AND oreGradeUnit="{}"'.format(ore_grade_unit)
    ore_grade = get_param_avg(curr, value_col='oreGrade', param_table='mining_ore_grade', param_col='commodity', param=commodity, commodity_col='commodity', commodity=commodity, ore_grade_unit=ore_grade_unit, sql_where=sql_extra)
    return ore_grade
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ore_grade_default(curr):
    curr.execute('SELECT globalAvg FROM mining_ore_averages GROUP BY commodity ORDER BY globalAvg')
    global_avgs = [data[0] for data in curr.fetchall()]
    global_avg_count = len(global_avgs)
    avg_mid_indx = int(global_avg_count/2)
    ore_grade_default = global_avgs[avg_mid_indx]
    return ore_grade_default
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_saleable_factor(curr, mineid, commodity, operators, debug=False):
    saleable_factor = sale_yield
    curr.execute('SELECT mineCountry, mineRegion, mineStage, mineType, mineMethod FROM mining_assets_daily WHERE NewMineId=%s' % mineid)
    mCountry, mRegion, mStage, mineType, mineMethod = curr.fetchone()
    saleable_yield = get_param_detail(curr, 'SALEABLE_PRODUCTION_YIELD_FACTOR', mineid, mCountry, mRegion, mStage, mineType, mineMethod, commodity, operators, '', '')
    if saleable_yield:
        saleable_factor = float(saleable_yield)
    return saleable_factor
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ore_capacity_to_rom(curr, mineid, commodity, operators, debug=False):
    ore_capacity_to_rom = ore_cap_to_rom
    curr.execute('SELECT mineCountry, mineRegion, mineStage, mineType, mineMethod FROM mining_assets_daily WHERE NewMineId=%s' % mineid)
    mCountry, mRegion, mStage, mineType, mineMethod = curr.fetchone()
    ore_cap = get_param_detail(curr, 'ORE_CAPACITY_TO_ROM', mineid, mCountry, mRegion, mStage, mineType, mineMethod, commodity, operators, '', '')
    if ore_cap:
        ore_capacity_to_rom = float(ore_cap)
    return ore_capacity_to_rom
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_recov_factor(curr, mineid, commodity, operators, debug=False):
    curr.execute('SELECT mineCountry, mineRegion, mineStage, mineType, mineMethod FROM mining_assets_daily WHERE NewMineId=%s' % mineid)
    mCountry, mRegion, mStage, mineType, mineMethod = curr.fetchone()
    recov_factor = get_param_detail(curr, 'METALLURGICAL_RECOVERY_FACTOR', mineid, mCountry, mRegion, mStage, mineType, mineMethod, commodity, operators, '', '')
    if recov_factor:
        recov_factor = float(recov_factor)
    else:
        recov_factor = 0.9
    return recov_factor
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ore_grade(curr, mineid, commodity, operators, mine_year=None, debug=False):
    if mine_year:
        sql_select = 'SELECT oreGrade, oreGradeUnit FROM mining_ore_grade WHERE NewMineId={} AND commodity="{}" AND sourceYear>={} ORDER BY sourceYear LIMIT 1'.format(mineid, commodity, mine_year)
    else:
        sql_select = 'SELECT oreGrade, oreGradeUnit FROM mining_ore_grade WHERE NewMineId={} AND commodity="{}" AND sourceYear=9999'.format(mineid, commodity)
    if debug or 1:
        print sql_select
    curr.execute(sql_select)
    ore_grade, ore_grade_unit = curr.fetchone()
    return ore_grade, ore_grade_unit

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ore_grade_(curr, mineid, commodity, operators, mine_year=None, debug=False):
    curr.execute('SELECT mineCountry, mineRegion, mineStage, mineType, mineMethod FROM mining_assets_daily WHERE NewMineId=%s' % mineid)
    mCountry, mRegion, mStage, mineType, mineMethod = curr.fetchone()

    if mine_year:
        sql_select  = 'SELECT DISTINCT NewMineId, productionByCommodity FROM mining_production_daily WHERE productionType IN ("Ore Grade", "Ore milled grade") '
        sql_select += 'AND NOT (UCASE(source) LIKE "EST:%" or UCASE(source) LIKE "%ESTIMATION%") AND productionYear>={} '.format(mine_year)
    else:
        sql_select  = 'SELECT DISTINCT NewMineId, productionByCommodity FROM mining_production_daily WHERE productionType IN ("Ore Grade", "Ore milled grade") '
        sql_select += 'AND NOT (UCASE(source) LIKE "EST:%" or UCASE(source) LIKE "%ESTIMATION%")'
    curr.execute(sql_select)
    ore_data = curr.fetchall()
    if (mineid, commodity) in ore_data:
        if mine_year:
            sql_select = 'SELECT productionValue, productionUnit FROM mining_production_daily WHERE productionType IN ("Ore Grade", "Ore milled grade") '
            sql_select += 'AND NewMineId=%s AND productionByCommodity="%s" AND productionYear>={} ORDER BY productionYear '.format(mine_year)
        else:
            sql_select = 'SELECT productionValue, productionUnit FROM mining_production_daily WHERE productionType IN ("Ore Grade", "Ore milled grade") '
            sql_select += 'AND NewMineId=%s AND productionByCommodity="%s" ORDER BY productionYear DESC'

        curr.execute(sql_select % (mineid, commodity))
        prod_val, prod_unit = curr.fetchone()

        if prod_unit == '%':
            ore_grade = float(prod_val)
        else:
            conv_factor = mining_units(curr, prod_unit.upper(), '%', False)
            prod_val = float(prod_val) * conv_factor
            ore_grade = prod_val
    else:
        ore_grade = ''

    if ore_grade:
        ore_grade = float(ore_grade) / 100.0
    else:
        curr.execute('SELECT DISTINCT NewMineId FROM mining_ore_grade WHERE commodity="%s" ' % commodity)
        ore_avg_data = [data[0] for data in curr.fetchall()]
        if mineid in ore_avg_data:
            curr.execute('SELECT oreGrade FROM mining_ore_grade WHERE NewMineId=%s AND commodity="%s" ' % (mineid, commodity))
            ore_grade = curr.fetchone()[0]
        else:
            ore_grade = ''
        if ore_grade:
            ore_grade = float(ore_grade)/100.0
        else:
            curr.execute('SELECT DISTINCT mineCountry FROM mining_ore_averages WHERE commodity="%s" ' % commodity)
            ore_avg_data = [data[0] for data in curr.fetchall()]
            if mCountry in ore_avg_data:
                curr.execute('SELECT countryAvg FROM mining_ore_averages WHERE mineCountry="%s" AND commodity="%s" ' % (mCountry, commodity))
                ore_grade = curr.fetchone()[0]
            else:
                ore_grade = ''
            if ore_grade:
                ore_grade = float(ore_grade) / 100.0
            else:
                curr.execute('SELECT DISTINCT mineRegion FROM mining_ore_averages WHERE commodity="%s" ' % commodity)
                ore_avg_data = [data[0] for data in curr.fetchall()]
                if mRegion in ore_avg_data:
                    curr.execute('SELECT regionAvg FROM mining_ore_averages WHERE mineRegion="%s" AND commodity="%s" ' % (mRegion, commodity))
                    ore_grade = curr.fetchone()[0]
                else:
                    ore_grade = ''
                if ore_grade:
                    ore_grade = float(ore_grade) / 100.0
                else:
                    curr.execute('SELECT DISTINCT commodity FROM mining_ore_averages')
                    ore_avg_data = [data[0] for data in curr.fetchall()]
                    if commodity in ore_avg_data:
                        curr.execute('SELECT globalAvg FROM mining_ore_averages WHERE commodity="%s" ' % commodity)
                        ore_grade = curr.fetchone()[0]
                    else:
                        ore_grade = ''
                    if ore_grade:
                        ore_grade = float(ore_grade) / 100.0
                    else:
                        # Check mining_model_rules for ORE_GRADE
                        ore_grade = get_param_detail(curr, 'ORE_GRADE', mineid, mCountry, mRegion, mStage, mineType,mineMethod, commodity, operators, '', '')
                        if ore_grade:
                            ore_grade = float(ore_grade)/100.0
                        else:
                            # Get average ore grade for commodity by country
                            sql_and = 'AND param_value < 100 '
                            ore_grade = get_param_avg(curr, 'param_value', 'mining_model_rules', 'param_name', 'ORE_GRADE', 'commodity', commodity, ore_grade_unit='%', range_col='mineCountry', range=mCountry, sql_where=sql_and)
                            if ore_grade:
                                ore_grade = float(ore_grade)/100.0
                            else:
                                # Get average ore grade for commodity by region
                                sql_and  = 'AND mineCountry IN (SELECT DISTINCT mineCountry FROM mining_assets_daily WHERE mineRegion="%s") ' % mRegion
                                sql_and += 'AND param_value < 100 '
                                ore_grade = get_param_avg(curr, 'param_value', 'mining_model_rules', 'param_name', 'ORE_GRADE', 'commodity', commodity, ore_grade_unit='%', sql_where=sql_and)
                                if ore_grade:
                                    ore_grade = float(ore_grade)/100.0
                                else:
                                    # Get average ore grade for commodity globally
                                    #sql_and = 'AND param_value < 100 '
                                    #ore_grade = get_param_avg(curr, 'param_value', 'mining_model_rules', 'param_name', 'ORE_GRADE', 'commodity', commodity, sql_where=sql_and)
                                    ore_grade = get_ore_grade_default(curr)
                                    ore_grade = float(ore_grade)/100.0

    return ore_grade
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_metal_grade(curr, mineid, data_table, commodity, year, operators, session_key, debug=False, updateParamTrk=False):
    data_names = {
        'reserves': {     'year': 'reserveYear',
                         'value': 'reserve',
                          'unit': 'reserveUnit',
                          'type': 'reserveType',
                     'data type': 'Total Reserves - Metal Grade',
                     'commodity': 'CommodityByReserve'},
        'resource': {     'year': 'resourceYear',
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

    #sql_select  = "SELECT %s, %s FROM mining_%s_daily WHERE %s=%s AND %s='%s' AND %s='%s' " % (value_name, unit_name, data_table, year_name, year, type_name, data_type, comm_name, commodity)
    #sql_select += "AND NOT (UCASE(source) LIKE 'EST:%' OR UCASE(source) LIKE '%ESTIMATION%' OR source='') "
    #curr.execute(sql_select)
    #metal_ore_grade = curr.fetchone()
    #if metal_ore_grade:
    #    metal_grade = float(metal_ore_grade[0])/100.0
    #else:
    metal_grade, metal_grade_unit = get_ore_grade(curr, mineid, commodity, operators, year)
    param_vals = (value_name, metal_grade, value_name, commodity, mineid, session_key)
    if updateParamTrk:
        curr.execute('UPDATE mining_param_track SET %sOreGrade=%s, %sOreCommodity="%s" WHERE NewMineId=%s AND sessionKey="%s"' % param_vals)
        curr.execute('COMMIT')
    return metal_grade, metal_grade_unit
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_metal_commodity(curr, mineid, data_table, debug=False):
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

    sql_select = "SELECT MAX(%s) FROM mining_%s_daily WHERE NewMineId=%s " % (data_year, data_table, mineid)
    sql_query  = "AND %s='%s' " % (data_type, type_name)
    sql_query += "AND NOT (UCASE(source) LIKE 'EST:%' OR UCASE(source) LIKE '%ESTIMATION%' OR source='') "
    curr.execute(sql_select + sql_query)
    max_metal_year = curr.fetchone()[0]

    sql_select  = "SELECT DISTINCT %s FROM mining_%s_daily WHERE NewMineId=%s " % (data_comm, data_table, mineid)
    sql_query += "AND %s=%s " % (data_year, max_metal_year)
    curr.execute(sql_select + sql_query)
    metal_comms = [data[0] for data in curr.fetchall()]
    metal_commodity = metal_comms[0]
    return metal_commodity
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_saleable_commodity(curr, mineid, data_table, debug=False):
    data_names = {
    'production': {     'type': 'productionType',
                   'commodity': 'productionByCommodity',
                        'year': 'productionYear',
                   'type name': 'Saleable Production'},

      'capacity': {     'type': 'capacityType',
                   'commodity': 'commodityByCapacity',
                        'year': 'capacityYear',
                   'type name': 'Saleable Capacity'}
    }

    data_year = data_names[data_table]['year']
    data_type = data_names[data_table]['type']
    data_comm = data_names[data_table]['commodity']
    type_name = data_names[data_table]['type name']

    sql_select = "SELECT MAX(%s) FROM mining_%s_daily WHERE NewMineId=%s " % (data_year, data_table, mineid)
    sql_query  = "AND %s='%s' " % (data_type, type_name)
    sql_query += "AND NOT (UCASE(source) LIKE 'EST:%' OR UCASE(source) LIKE '%ESTIMATION%' OR source='') "
    curr.execute(sql_select + sql_query)
    max_saleable_year = curr.fetchone()[0]

    sql_select  = "SELECT DISTINCT %s FROM mining_%s_daily WHERE NewMineId=%s " % (data_comm, data_table, mineid)
    sql_query += "AND %s=%s " % (data_year, max_saleable_year)
    curr.execute(sql_select + sql_query)
    saleable_comms = [data[0] for data in curr.fetchall()]
    saleable_commodity = saleable_comms[0]
    return saleable_commodity
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_total_factor(curr, data_table, data_type, debug=False):
    total_factor = 0
    data_names = {
        'reserves': { 'year': 'reserveYear',
                               'value': 'reserve',
                                'unit': 'reserveUnit',
                                'type': 'reserveType'},
        'resource': { 'year': 'resourceYear',
                               'value': 'resource',
                                'unit': 'resourceUnit',
                                'type': 'resourceType'}
                  }

    year_name  = data_names[data_table]['year' ]
    value_name = data_names[data_table]['value']
    unit_name  = data_names[data_table]['unit' ]
    type_name  = data_names[data_table]['type' ]

    sql_select  = "SELECT AVG(c.type_to_total) FROM (SELECT (a.%s/b.%s) AS type_to_total FROM mining_%s_daily AS a, mining_%s_daily AS b " % (value_name, value_name, data_table, data_table)
    sql_select += "WHERE a.%s='%s' AND b.%s ='total %ss' AND a.NewMineId = b.NewMineId AND a.%s=b.%s AND a.%s=b.%s " % (type_name, data_type, type_name, value_name, unit_name, unit_name, year_name, year_name)
    sql_select += "AND NOT (UCASE(a.source) LIKE 'EST:%' OR UCASE(a.source) LIKE '%ESTIMATION%' OR a.source='') AND NOT (UCASE(b.source) LIKE 'EST:%' OR UCASE(b.source) LIKE '%ESTIMATION%' OR b.source='') "
    sql_select += "AND a.%s <= b.%s) AS c " % (value_name, value_name)

    curr.execute(sql_select)
    total_factor = float(curr.fetchone()[0])
    return total_factor

#========================================================================================================================================================================

def metal_to_rom(curr, last_data, mineid, operators, session_key, recov_factor=None, debug=False, updateParamTrk=False):
    rom_value = 0
    data_commodity = last_data['commodity']
    data_value = float(last_data['value'])
    data_unit = last_data['unit']
    data_year = int(last_data['year'])

    if not recov_factor:
        recov_factor = float(get_recov_factor(curr, mineid, data_commodity, operators))

    ore_grade, ore_grade_unit = get_ore_grade(curr, mineid, data_commodity, operators, data_year)

    param_vals = ('{} {}'.format(ore_grade, ore_grade_unit), data_commodity, recov_factor, mineid, session_key)
    if updateParamTrk:
        curr.execute('UPDATE mining_param_track SET oreGrade=%s, oreGradeCommodity=%s, recoveryFactor=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
        curr.execute('COMMIT')

    if ore_grade_unit.upper() == 'GMS/TONNE':
        conv_factor = float(mining_units(curr, data_unit, 'GRAMS', False))
        prod_value = float(data_value * conv_factor)
        rom_value = prod_value / (float(ore_grade) * float(recov_factor) * 1000000)

    elif ore_grade_unit.upper() == 'CPT':
        conv_factor = float(mining_units(curr, data_unit, 'CARATS', False))
        prod_value = float(data_value * conv_factor)
        rom_value = prod_value / (float(ore_grade) * float(recov_factor) * 1000000)

    else:
        conv_factor = float(mining_units(curr, data_unit, 'MMT', False))
        prod_value = float(data_value * conv_factor)
        rom_value = prod_value / (float(ore_grade) * float(recov_factor))

    if debug:
        print 'conv_factor   :', conv_factor
        print 'data_commodity:', data_commodity
        print 'data_value    :', data_value
        print 'prod_value    :', prod_value
        print 'rom_value     :', rom_value
        print 'data_unit     :', data_unit
        print 'recov_factor  :', recov_factor
        print 'ore_grade     :', ore_grade
        print 'ore_grade_unit:', ore_grade_unit

    return rom_value
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def saleable_to_rom(curr, last_data, mineid, operators, session_key, debug=False, updateParamTrk=False):
    rom_value = 0
    data_commodity = last_data['commodity']
    data_value = float(last_data['value'])
    data_unit = last_data['unit']
    if data_unit.upper() in ['MMT', 'MTPA']:
        conv_factor = 1.0
    else:
        conv_factor = float(mining_units(curr, data_unit, 'MMT', False))
        data_unit = 'MMT'
        data_value = float(data_value) * conv_factor
    saleable_factor = float(get_saleable_factor(curr, mineid, data_commodity, operators))
    if updateParamTrk:
        curr.execute('UPDATE mining_param_track SET saleableYieldFactor=%s WHERE NewMineId=%s AND sessionKey=%s', (saleable_factor, mineid, session_key))
        curr.execute('COMMIT')
    rom_value = float(data_value) / float(saleable_factor)
    return rom_value
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def ore_to_rom(curr, last_data, mineid, operators, session_key, debug=False, updateParamTrk=False):
    rom_value = 0
    data_commodity = last_data['commodity']
    data_value = float(last_data['value'])
    data_unit = last_data['unit']
    if debug:
        print 'data_commodity:', data_commodity
        print 'data_value:', data_value
        print 'data_unit:', data_unit
    if data_unit.upper() in ['MMT', 'MTPA']:
        conv_factor = 1.0
    else:
        conv_factor = float(mining_units(curr, data_unit, 'MMT', False))
        data_unit = 'MMT'
        data_value = float(data_value) * conv_factor
    ore_capacity_to_rom = float(get_ore_capacity_to_rom(curr, mineid, data_commodity, operators))
    param_vals = (ore_capacity_to_rom, mineid, session_key)
    if updateParamTrk:
        curr.execute('UPDATE mining_param_track SET oreCapacityToROM=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
        curr.execute('COMMIT')
    rom_value = float(data_value) / float(ore_capacity_to_rom)
    if debug:
        print ''
        print 'ore_capacity_to_rom:', ore_capacity_to_rom
        print 'rom_value (ore_to_rom) = {}/{}: {}'.format(data_value, ore_capacity_to_rom, rom_value)
        print ''
    return rom_value
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def probable_to_total(curr, last_data, mineid, operators, session_key, debug=False, updateParamTrk=False):
    '''Use probable reserves to estimate total reserves'''
    total_value = 0
    data_commodity = last_data['commodity']
    data_value = float(last_data['value'])
    data_unit = last_data['unit']
    if data_unit.upper() in ['MMT', 'MTPA']:
        conv_factor = 1.0
    else:
        conv_factor = float(mining_units(curr, data_unit, 'MMT', False))
        data_unit = 'MMT'
        data_value = float(data_value) * conv_factor
    curr.execute('SELECT param_value FROM mining_model_rules WHERE param_name="PROBABLE_TO_TOTAL"')
    probable_factor = curr.fetchone()[0]
    if probable_factor:
        total_value = float(data_value)/float(probable_factor)
    if updateParamTrk:
        curr.execute('UPDATE mining_param_track SET probableToTotal=%s WHERE NewMineId=%s AND sessionKey=%s',(probable_factor, mineid, session_key))
        curr.execute('COMMIT')
    return total_value
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def proved_to_total(curr, last_data, mineid, operators, session_key, debug=False, updateParamTrk=False):
    '''Use proved reserves to estimate total reserves'''
    total_value = 0
    data_commodity = last_data['commodity']
    data_value = float(last_data['value'])
    data_unit = last_data['unit']
    if data_unit.upper() in ['MMT', 'MTPA']:
        conv_factor = 1.0
    else:
        conv_factor = float(mining_units(curr, data_unit, 'MMT', False))
        data_unit = 'MMT'
        data_value = float(data_value) * conv_factor
    curr.execute('SELECT param_value FROM mining_model_rules WHERE param_name="PROVED_TO_TOTAL"')
    proved_factor = curr.fetchone()[0]
    if proved_factor:
        total_value = float(data_value) / float(proved_factor)
    if updateParamTrk:
        curr.execute('UPDATE mining_param_track SET provedToTotal=%s WHERE NewMineId=%s AND sessionKey=%s',(proved_factor, mineid, session_key))
        curr.execute('COMMIT')
    return total_value
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def metal_to_total(curr, data_table, last_data, mineid, operators, session_key, debug=False):
    '''Use metal reserves or resources to estimate total reserves or resources'''
    total_value = 0
    conv_factor = 1
    comm_value  = 0
    data_commodity = last_data['commodity']
    data_value = float(last_data['value'])
    data_unit = last_data['unit']
    data_year = last_data['year']

    recov_factor = float(get_recov_factor(curr, mineid, data_commodity, operators))
    ore_grade, ore_grade_unit = get_metal_grade(curr, mineid, data_table, data_commodity, data_year, operators, session_key, debug)
    if ore_grade and recov_factor:
        if ore_grade_unit.upper() == 'GMS/TONNE':
            conv_factor = float(mining_units(curr, data_unit, 'GRAMS', False))
            comm_value = float(data_value * conv_factor)
            total_value = comm_value / (float(ore_grade) * float(recov_factor) * 1000000)

        elif ore_grade_unit.upper() == 'CPT':
            conv_factor = float(mining_units(curr, data_unit, 'CARATS', False))
            comm_value = float(data_value * conv_factor)
            total_value = comm_value / (float(ore_grade) * float(recov_factor) * 1000000)

        else:
            conv_factor = float(mining_units(curr, data_unit, 'MMT', False))
            comm_value = float(data_value * conv_factor)
            total_value = comm_value / (float(ore_grade) * float(recov_factor))

    if debug:
        print 'conv_factor   :', conv_factor
        print 'data_commodity:', data_commodity
        print 'data_value    :', data_value
        print 'comm_value    :', comm_value
        print 'total_value   :', total_value
        print 'data_unit     :', data_unit
        print 'recov_factor  :', recov_factor
        print 'ore_grade     :', ore_grade
        print 'ore_grade_unit:', ore_grade_unit

    return total_value
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def measured_to_total(curr, last_data, mineid, operators, session_key, debug=False, updateParamTrk=False):
    '''Use measured resources to estimate total resources'''
    total_value = 0
    data_commodity = last_data['commodity']
    data_value = float(last_data['value'])
    data_unit = last_data['unit']
    if data_unit.upper() in ['MMT', 'MTPA']:
        conv_factor = 1.0
    else:
        conv_factor = float(mining_units(curr, data_unit, 'MMT', False))
        data_unit = 'MMT'
        data_value = float(data_value) * conv_factor
    curr.execute('SELECT param_value FROM mining_model_rules WHERE param_name="MEASURED_TO_TOTAL"')
    measured_factor = curr.fetchone()[0]
    if measured_factor:
        total_value = float(data_value) / float(measured_factor)
    if debug:
        print 'measured_factor:', measured_factor
        print 'measured resources:', data_value
        print 'estimated total resources:', total_value
    if updateParamTrk:
        curr.execute('UPDATE mining_param_track SET measuredToTotal=%s WHERE NewMineId=%s AND sessionKey=%s',(measured_factor, mineid, session_key))
        curr.execute('COMMIT')
    return total_value
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def indicated_to_total(curr, last_data, mineid, operators, session_key, debug=False, updateParamTrk=False):
    '''Use indicated resources to estimate total resources'''
    total_value = 0
    data_commodity = last_data['commodity']
    data_value = float(last_data['value'])
    data_unit = last_data['unit']
    if data_unit.upper() in ['MMT', 'MTPA']:
        conv_factor = 1.0
    else:
        conv_factor = float(mining_units(curr, data_unit, 'MMT', False))
        data_unit = 'MMT'
        data_value = float(data_value) * conv_factor
    curr.execute('SELECT param_value FROM mining_model_rules WHERE param_name="INDICATED_TO_TOTAL"')
    indicated_factor = curr.fetchone()[0]
    if indicated_factor:
        total_value = float(data_value) / float(indicated_factor)
    if debug:
        print 'indicated_factor:', indicated_factor
        print 'indicated resources:', data_value
        print 'estimated total resources:', total_value
    if updateParamTrk:
        curr.execute('UPDATE mining_param_track SET indicatedToTotal=%s WHERE NewMineId=%s AND sessionKey=%s',(indicated_factor, mineid, session_key))
        curr.execute('COMMIT')
    return total_value
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def inferred_to_total(curr, last_data, mineid, operators, session_key, debug=False, updateParamTrk=False):
    '''Use inferred resources to estimate total resources'''
    total_value = 0
    data_commodity = last_data['commodity']
    data_value = float(last_data['value'])
    data_unit = last_data['unit']
    if data_unit.upper() in ['MMT', 'MTPA']:
        conv_factor = 1.0
    else:
        conv_factor = float(mining_units(curr, data_unit, 'MMT', False))
        data_unit = 'MMT'
        data_value = float(data_value) * conv_factor
    curr.execute('SELECT param_value FROM mining_model_rules WHERE param_name="INFERRED_TO_TOTAL"')
    inferred_factor = curr.fetchone()[0]
    if inferred_factor:
        total_value = float(data_value) / float(inferred_factor)
    if debug:
        print 'inferred_factor:', inferred_factor
        print 'inferred resources:', data_value
        print 'estimated total resources:', total_value
    if updateParamTrk:
        curr.execute('UPDATE mining_param_track SET inferredToTotal=%s WHERE NewMineId=%s AND sessionKey=%s',(inferred_factor, mineid, session_key))
        curr.execute('COMMIT')
    return total_value
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def convert_to_total(curr, data_table, data_type, last_data, mineid, mCountry, mRegion, mStage, mineType, mineMethod, operators, session_key, debug=False):
    '''Convert reserve and resource data to estimated total values'''
    total_value = 0
    
    if data_table == 'reserves':
        if data_type == 'probable':
            total_value = probable_to_total(curr, last_data, mineid, operators, session_key, debug)
            if debug:
                print 'total_value (probable_to_total):', total_value
                
        elif data_type == 'proved':
            total_value = proved_to_total(curr, last_data, mineid, operators, session_key, debug)
            if debug:
                print 'total_value (proved_to_total):', total_value
                
        elif data_type == 'metal':
            total_value = metal_to_total(curr, data_table, last_data, mineid, operators, session_key, debug)
            if debug:
                print 'total_value (metal_to_total):', total_value
                
    elif data_table == 'resource':
        if data_type == 'measured':
            total_value = measured_to_total(curr, last_data, mineid, operators, session_key, debug)
            if debug:
                print 'total_value (measured_to_total):', total_value
                
        elif data_type == 'indicated':
            total_value = indicated_to_total(curr, last_data, mineid, operators, session_key, debug)
            if debug:
                print 'total_value (indicated_to_total):', total_value
                
        elif data_type == 'inferred':
            total_value = inferred_to_total(curr, last_data, mineid, operators, session_key, debug)
            if debug:
                print 'total_value (inferred_to_total):', total_value
                
        elif data_type == 'metal':
            total_value = metal_to_total(curr, data_table, last_data, mineid, operators, session_key, debug)
            if debug:
                print 'total_value (metal_to_total):', total_value
                
    return total_value
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def convert_to_rom(curr, data_table, data_type, last_data, mineid, mCountry, mRegion, mStage, mineType, mineMethod, operators, session_key, recov_factor=None, debug=False):
    '''Convert production and capacity data to estimated ROM values'''
    rom_value = 0

    if data_type == 'metal':
        rom_value = metal_to_rom(curr, last_data, mineid, operators, session_key, recov_factor, debug)
        if debug:
            print 'rom_value (metal_to_rom):', rom_value

    elif data_type == 'sale':
        rom_value = saleable_to_rom(curr, last_data, mineid, operators, session_key, debug)
        if debug:
            print 'rom_value (saleable_to_rom):', rom_value

    elif data_type == 'ore':
        rom_value = ore_to_rom(curr, last_data, mineid, operators, session_key, debug)
        if debug:
            print 'rom_value (ore_to_rom):', rom_value

    return rom_value
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#========================================================================================================================================================================

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def import_mining_tables():
    MINING_DIR = DATA_DIR + 'mining\\mining_db\\'
    command = 'sqlcmd -S localhost -d MiningEngineextract -i %s'
    os.system('cd %s' % MINING_DIR)
    for sql_file in [filename for filename in os.listdir(MINING_DIR) if filename[-3:] == 'sql']:
        filename = sql_file[:-4]
        new_filename = filename.replace('.', '_')
        sql_filename = new_filename + '.sql'
        os.rename(MINING_DIR+sql_file, MINING_DIR+sql_filename)
        print command % (MINING_DIR + sql_filename)
        os.system(command % (MINING_DIR + sql_filename))
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_forecast(Session_key, debugMode=False):
    #--------------------------------------------------------
    #
    #  Connection string to local data
    #--------------------------------------------------------
    userName = getpass.getuser()
    mysqlHost = 'localhost'
    mysqlUser = 'root'
    mysqlPassword = 'OilAndGas321'
    mysqlDB = 'MiningEngineExtract'
    connLocal = pymysql.connect(host = mysqlHost, user = mysqlUser, passwd = mysqlPassword, db = mysqlDB, charset='utf8', use_unicode=True)
    currLocal = connLocal.cursor()
    currLocal.execute("USE MiningEngineExtract")

    #--------------------------------------------------------
    #
    #  Connection string to SQL SERVER
    #--------------------------------------------------------
    print 'Connecting to SQL server ...'

    #conn = pypyodbc.connect('Driver={SQL Server}; Server=115.112.83.122\energy,1450; Database=MiningEngineextract; uid=ogtest;pwd=Pass@3$58')
    conn = pypyodbc.connect('Driver={SQL Server}; Server=(local); Database=MiningEngineextract; Trusted_Connection=True; unicode_results=True;')

    '''
    # Update MineID values for all forecast tables
    print 'Updating MineID values ...'

    currLocal.execute('UPDATE mining_assets_forecast AS f, mining_assets_daily AS d SET f.Mineid = d.Mineid WHERE f.NewMineid = d.NewMineid')
    currLocal.execute('UPDATE mining_capacity_forecast AS f, mining_capacity_daily AS d SET f.Mineid = d.Mineid WHERE f.NewMineid = d.NewMineid')
    currLocal.execute('UPDATE mining_production_forecast AS f, mining_production_daily AS d SET f.Mineid = d.Mineid WHERE f.NewMineid = d.NewMineid')
    currLocal.execute('UPDATE mining_reserves_forecast AS f, mining_reserves_daily AS d SET f.Mineid = d.Mineid WHERE f.NewMineid = d.NewMineid')
    currLocal.execute('UPDATE mining_resource_forecast AS f, mining_resource_daily AS d SET f.Mineid = d.Mineid WHERE f.NewMineid = d.NewMineid')
    currLocal.execute('UPDATE mining_error_log AS e, mining_assets_daily AS d SET e.Mineid = d.Mineid WHERE e.NewMineid = d.NewMineid')
    currLocal.execute('COMMIT')
    '''

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    #  MINING ASSET FORECAST
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    # Open the remote site table mining_asstes_daily
    # 1 - truncate the table
    # 2 - Count the number of records to be updated
    # 3 - Update from local to remote table
    mCur = conn.cursor()
    # 1
    truncate_tables(mCur,'mining_assets_forecast')
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # 2
    mSQLWhereExtra = ""

    sql_statement = "SELECT count(*) from Mining_Assets_Forecast "

    currLocal.execute(sql_statement)
    r1 = currLocal.fetchall()
    for datarow in r1:
        mTotRecs = datarow[0]

    # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
    mFields  = 'NewMineid,Mineid,mineName,mineCountry,state,mineRegion,mineStage,commodities,mineType,mineMethod,projectType,mineSubStage,mineSubStageStatus,totalMineLife,mineEndYear,'
    mFields += 'mineAcreageHectares,mineDepth,prefeasibilityStartYear,prefeasibilityStartQuarter,feasibilityStartYear,feasibilityStartQuarter,constructionStartYear,constructionStartQuarter,'
    mFields += 'originalProductionStartYear,originalProductionStartQuarter,actualProductionStartYear,actualProductionStartQuarter,plannedProductionStartYear,plannedProductionStartQuarter,'
    mFields += 'mineLocationSource,remainingMineLife,remainingMineLifeYear,MineAcreageSource,ActualProductionStartYearSource,TotalMineLifeSource,RemainingMineLifeSource,'
    mFields += 'MineEndYearSource,estimated_total_recoverable_reserves'

    sql_statement  = 'SELECT %s FROM Mining_Assets_Forecast ORDER BY Newmineid ' % mFields

    if debugMode:
        print sql_statement
        print ''
    currLocal.execute(sql_statement)
    recsProcessed = 0
    asset_forecast_data = currLocal.fetchall()

    # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
    mFields  = 'NewMineID,MineID,MineName,MineCountry,State,MineRegion,MineStage,Commodities,MineType,MineMethod,ProjectType,MineSubStage,MineSubStageStatus,TotalMineLife,MineEndYear,'
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
    if debugMode:
        print sql_statement

    DataExtractedOn = st
    for datarow in asset_forecast_data:
        MineId = 0
        param_values = datarow + (DataExtractedOn,)
        mCur.execute(sql_statement, param_values)
        mCur.execute('COMMIT')
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_assets_forecast - " + str(round(recsProcessed/mTotRecs,2)*100)

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    #  ERROR LOG
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    truncate_tables(mCur,'mining_error_log')
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # 2
    mSQLWhereExtra = ""
    sql_statement = "SELECT count(*) from Mining_Error_log "
    currLocal.execute(sql_statement)
    r1 = currLocal.fetchall()
    for datarow in r1:
        mTotRecs = datarow[0]

    # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
    mFields = 'NewMineid,Mineid,mineName,mineCountry,mineRegion,state,mineStage,Commodities,period,comment,session_key,error_type,nParam_value,Param_value'

    sql_statement = 'SELECT %s FROM Mining_Error_log ORDER BY Newmineid ' % mFields

    if debugMode:
        print sql_statement
        print ""
    currLocal.execute(sql_statement)
    recsProcessed = 0
    error_log_data = currLocal.fetchall()

    # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
    mFields = 'NewMineID,MineID,MineName,MineCountry,MineRegion,State,MineStage,Commodities,Period,Comment,Session_key,Error_type,nParam_value,Param_value'

    eSymbol = buildMySQLin(14, "?")

    sql_statement = 'INSERT INTO Mining_Error_log (%s) VALUES %s' % (mFields, eSymbol)
    if debugMode:
        print sql_statement

    DataExtractedOn = st
    for datarow in error_log_data:
        MineId = 0
        mCur.execute(sql_statement, datarow)
        mCur.execute('COMMIT')
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_error_log - " + str(round(recsProcessed/mTotRecs,2)*100)

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    #  MINING RESERVES FORECAST
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    # Open the remote site table mining_production_forecast
    # 1 - truncate the table
    # 2 - Count the number of records to be updated
    # 3 - Update from local to remote table
    # mCur = conn.cursor()
    # 1
    tableType = "Reserves"
    truncate_tables(mCur,"mining_" + tableType + "_forecast")
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # 2
    mSQLWhereExtra = ""
    sql_statement = "SELECT count(*) from Mining_" + tableType + "_Forecast "
    currLocal.execute(sql_statement)
    r1 = currLocal.fetchall()
    for datarow in r1:
        mTotRecs = datarow[0]

    # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
    mFields = 'NewmineId,Mineid,mineName,mineCountry,state,mineRegion,mineStage,ReserveType,CommodityByReserve,ReserveYear,Reserve,ReserveUnit,source,Session_key'

    sql_statement = 'SELECT %s FROM Mining_%s_Forecast ORDER BY Newmineid ' % (mFields, tableType)

    if debugMode:
        print sql_statement
        print ""
    currLocal.execute(sql_statement)
    recsProcessed = 0
    reserves_forecast_data = currLocal.fetchall()

    # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
    mFields = 'NewMineID,MineID,MineName,MineCountry,MineRegion,State,MineStage,ReserveType,CommodityByReserve,ReserveYear,Reserve,ReserveUnit,Source,Session_key,DataExtractedOn'

    eSymbol = buildMySQLin(15, "?")

    sql_statement = "INSERT INTO Mining_%s_Forecast (%s) VALUES %s" % (tableType, mFields, eSymbol)
    if debugMode:
        print sql_statement

    DataExtractedOn = st
    for datarow in reserves_forecast_data:
        MineId = 0
        param_values = datarow + (DataExtractedOn,)
        mCur.execute(sql_statement, param_values)
        mCur.execute('COMMIT')
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_" + tableType +  "_forecast - " + str(round(recsProcessed/mTotRecs,2)*100)


    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    #  MINING RESOURCE FORECAST
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    # Open the remote site table mining_production_forecast
    # 1 - truncate the table
    # 2 - Count the number of records to be updated
    # 3 - Update from local to remote table
    # mCur = conn.cursor()
    # 1
    tableType = "Resource"
    truncate_tables(mCur,"mining_" + tableType + "_forecast")
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # 2
    mSQLWhereExtra = ""
    sql_statement = "SELECT count(*) from Mining_" + tableType + "_Forecast "
    currLocal.execute(sql_statement)
    r1 = currLocal.fetchall()
    for datarow in r1:
        mTotRecs = datarow[0]

    # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
    mFields = 'NewmineId,Mineid,mineName,mineCountry,state,mineRegion,mineStage,ResourceType,CommodityByResource,ResourceYear,Resource,ResourceUnit,source,Session_key'

    sql_statement = 'SELECT %s FROM Mining_%s_Forecast ORDER BY Newmineid ' % (mFields, tableType)

    if debugMode:
        print sql_statement
        print ""
    currLocal.execute(sql_statement)
    recsProcessed = 0
    resource_forecast_data = currLocal.fetchall()

    # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
    mFields = 'NewMineID,MineID,MineName,MineCountry,State,MineRegion,MineStage,ResourceType,CommodityByResource,ResourceYear,Resource,ResourceUnit,Source,Session_key,DataExtractedOn'

    eSymbol = buildMySQLin(15, "?")

    sql_statement = "INSERT INTO Mining_%s_Forecast (%s) VALUES %s" % (tableType, mFields, eSymbol)
    if debugMode:
        print sql_statement

    for datarow in resource_forecast_data:
        MineId = 0
        DataExtractedOn = st
        param_values = datarow + (DataExtractedOn,)
        mCur.execute(sql_statement, param_values)
        mCur.execute('COMMIT')
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_" + tableType +  "_forecast - " + str(round(recsProcessed/mTotRecs,2)*100)

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    #  MINING CAPACITY FORECAST
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    # Open the remote site table mining_production_forecast
    # 1 - truncate the table
    # 2 - Count the number of records to be updated
    # 3 - Update from local to remote table
    # mCur = conn.cursor()
    # 1
    tableType = "Capacity"
    truncate_tables(mCur,"mining_" + tableType + "_forecast")
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # 2
    mSQLWhereExtra = ""
    sql_statement = "SELECT count(*) from Mining_" + tableType + "_Forecast "
    currLocal.execute(sql_statement)
    r1 = currLocal.fetchall()
    for datarow in r1:
        mTotRecs = datarow[0]

    # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
    mFields = 'NewmineId,Mineid,mineName,mineCountry,state,mineRegion,mineStage,CapacityType,CommodityByCapacity,CapacityYear,Capacity,CapacityUnit,source,Session_key'

    sql_statement = 'SELECT %s FROM Mining_%s_Forecast ORDER BY Newmineid ' % (mFields, tableType)

    if debugMode:
        print sql_statement
        print ""
    currLocal.execute(sql_statement)
    recsProcessed = 0
    capacity_forecast_data = currLocal.fetchall()

    # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
    mFields = 'NewMineID,MineID,MineName,MineCountry,State,MineRegion,MineStage,CapacityType,CommodityByCapacity,CapacityYear,Capacity,CapacityUnit,Source,Session_key,DataExtractedOn'

    eSymbol = buildMySQLin(15, "?")

    sql_statement = 'INSERT INTO Mining_%s_Forecast (%s) VALUES %s' % (tableType, mFields, eSymbol)
    if debugMode:
        print sql_statement

    DataExtractedOn = st
    for datarow in capacity_forecast_data:
        MineId = 0
        param_values = datarow + (DataExtractedOn,)
        mCur.execute(sql_statement, param_values)
        mCur.execute('COMMIT')
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_" + tableType +  "_forecast - " + str(round(recsProcessed/mTotRecs,2)*100)


    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    #  MINING PRODUCTION FORECAST
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    # Open the remote site table mining_production_forecast
    # 1 - truncate the table
    # 2 - Count the number of records to be updated
    # 3 - Update from local to remote table
    # mCur = conn.cursor()
    # 1
    truncate_tables(mCur,'mining_production_forecast')
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # 2
    mSQLWhereExtra = ""
    sql_statement = "SELECT count(*) from Mining_Production_Forecast "
    currLocal.execute(sql_statement)
    r1 = currLocal.fetchall()
    for datarow in r1:
        mTotRecs = datarow[0]
    #
    # Get data from local database -------------------------------------------------------------------------------------------------------------------------------------------------------
    mFields = 'NewmineId,Mineid,mineName,mineCountry,state,mineRegion,mineStage,productionType,productionByCommodity,productionYear,productionValue,productionUnit,source,session_key'

    sql_statement = 'SELECT %s FROM Mining_Production_Forecast ORDER BY Newmineid ' % mFields

    if debugMode:
        print sql_statement
        print ""
    currLocal.execute(sql_statement)
    recsProcessed = 0
    production_forecast_data = currLocal.fetchall()

    # Insert data into external database -------------------------------------------------------------------------------------------------------------------------------------------------
    mFields = 'NewMineID,MineID,MineName,MineCountry,State,MineRegion,MineStage,ProductionType,ProductionByCommodity,ProductionYear,ProductionValue,ProductionUnit,Source,Session_key,DataExtractedOn'

    eSymbol = buildMySQLin(15, "?")

    sql_statement = 'INSERT INTO Mining_Production_Forecast (%s) VALUES %s' % (mFields, eSymbol)
    if debugMode:
        print sql_statement

    DataExtractedOn = st
    for datarow in production_forecast_data:
        MineId = 0
        param_values = datarow + (DataExtractedOn,)
        mCur.execute(sql_statement, param_values)
        mCur.execute('COMMIT')
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_production_forecast - %s%% " % str(round(recsProcessed/mTotRecs,2)*100)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_local_data(debugMode=False):
    #--------------------------------------------------------
    #
    #  Connection string to local data
    #--------------------------------------------------------
    userName = getpass.getuser()
    mysqlHost = 'localhost'
    mysqlUser = 'root'
    mysqlPassword = 'OilAndGas321'
    mysqlDB = 'MiningEngineExtract'
    connLocal = pymysql.connect(host = mysqlHost, user = mysqlUser, passwd = mysqlPassword, db = mysqlDB, charset='utf8', use_unicode=True)
    currLocal = connLocal.cursor()
    currLocal.execute("USE MiningEngineExtract")
    #--------------------------------------------------------
    #
    #  Connection string to SQL SERVER
    #--------------------------------------------------------

    #conn = pypyodbc.connect('Driver={SQL Server}; Server=115.112.83.122\energy,1450; Database=MiningEngineextract; uid=ogtest;pwd=Pass@3$58')
    conn = pypyodbc.connect('Driver={SQL Server}; Server=(local); Database=MiningEngineextract; Trusted_Connection=True; unicode_results=True;')
    #------------------------------------------------------------------------------------
    #
    #  MINING ASSET DAILY TABLE
    #--------------------------------------------------------------------------------------
    # wipe out the existing DB
    truncate_tables(currLocal,'mining_assets_daily')

    #Remove comment to prevent specified mines from modelling 20181129
    #mSQLWhereExtra = 'AND NOT (mineSubStage="Care & Maintenance" AND mineSubStageStatus="On hold") '
    mSQLWhereExtra = ''
    sql_statement  = "SELECT COUNT(*) FROM dbo.Mining_Assets_Daily "
    mSQLOrderBy    = "ORDER BY Newmineid "
    mSQLWhere      = "WHERE mineStage='Operation' %s " % mSQLWhereExtra
    sql_statement += mSQLWhere
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r1 = mCur.fetchall()
    for datarow in r1:
        #
        mTotRecs = datarow[0]
    #--------------------------------------------------------------------
    mFields = "NewMineId,mineStage,ActualProductionStartYear,totalMineLife,remainingMineLife,"
    mFields += "MineAcreageHectares,mineName,mineCountry,state,mineRegion,"
    mFields += "commodities,mineType,mineMethod,projectType,mineSubStage,"
    mFields += "mineSubStageStatus,constructionStartYear,mineEndYear,[mineDepth(Meters)],mineLocationSource,"
    mFields += "remainingMineLifeYear,originalProductionStartYear,TotalMineLifeSource,RemainingMineLifeSource,MineEndYearSource,"
    #mFields += "mineAcreageSource,ActualProductionStartYearSource"
    mFields += "mineAcreageSource,ActualProductionStartYearSource,MineID"
    sql_statement = "select " + mFields + " from dbo.Mining_Assets_Daily"
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = " WHERE mineStage = 'Operation' " + mSQLWhereExtra
    #print sql_statement
    sql_statement += mSQLWhere + mSQLOrderBy
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r2 = mCur.fetchall()
    recsProcessed = 0
    if debugMode:
        print "*"*25
        print sql_statement
    for datarow in r2:
        NewMineId = datarow[0]
        mineStage = datarow[1]
        if datarow[2] is None :
            ActualProductionStartYear = 0
        else:
            ActualProductionStartYear = datarow[2]
        if datarow[3] is None :
            totalMineLife = 0
        else:
            totalMineLife = datarow[3]
        if datarow[4] is None :
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
        if datarow[16] is None :
            constructionStartYear = 0
        else:
            constructionStartYear = datarow[16]
        mineEndYear = datarow[17]
        mineDepth = datarow[18]
        mineLocationSource = datarow[19]
        if mineLocationSource:
            mineLocationSource += ' '

        if datarow[20] is None :
            remainingMineLifeYear = 0
        else:
            remainingMineLifeYear = datarow[20]
        originalProductionStartYear = datarow[21]

        TotalMineLifeSource = datarow[22]
        if TotalMineLifeSource:
            TotalMineLifeSource += ' '

        RemainingMineLifeSource = datarow[23]
        if RemainingMineLifeSource:
            RemainingMineLifeSource += ' '

        MineEndYearSource = datarow[24]
        if MineEndYearSource:
            MineEndYearSource += ' '

        mineAcreageSource = datarow[25]
        if mineAcreageSource:
            mineAcreageSource += ' '

        ActualProductionStartYearSource = datarow[26]
        if ActualProductionStartYearSource:
            ActualProductionStartYearSource += ' '
        MineID = datarow[27]
        #--------------------------------------------------------------
        #
        # LOGIC to erase sources that do not belong
        # Examine the following fields:
        # ActualProductionStartYearSource
        # MineEndYearSource
        # RemainingMineLifeSource
        # TotalMineLifeSource
        # and
        # mineAcreageSource
        #---------------------------------------------------------------
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
        sqlStatement = "INSERT INTO mining_assets_daily ("+\
                       "NewMineId,mineStage,ActualProductionStartYear,totalMineLife,remainingMineLife,"+\
                       "MineAcreageHectares,mineName,mineCountry,state,mineRegion,"+\
                       "commodities,mineType,mineMethod,projectType,mineSubStage,"+\
                       "mineSubStageStatus,constructionStartYear,mineEndYear,mineDepth,mineLocationSource,"+\
                       "remainingMineLifeYear,originalProductionStartYear,TotalMineLifeSource,RemainingMineLifeSource,MineEndYearSource,"+\
                       "mineAcreageSource,ActualProductionStartYearSource,Mineid)"+\
                       "VALUES ("+\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s ) "

        currLocal.execute(sqlStatement,(NewMineId,mineStage,ActualProductionStartYear,totalMineLife,remainingMineLife,\
                                        MineAcreageHectares,mineName,mineCountry,state,mineRegion,\
                                        commodities,mineType,mineMethod,projectType,mineSubStage,\
                                        mineSubStageStatus,constructionStartYear,mineEndYear,mineDepth,mineLocationSource,\
                                        remainingMineLifeYear,originalProductionStartYear,TotalMineLifeSource,RemainingMineLifeSource,MineEndYearSource,\
                                        mineAcreageSource,ActualProductionStartYearSource,MineID))
        currLocal.execute("commit;")
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_assets_daily - " + str(round(recsProcessed/mTotRecs,2)*100)


    #------------------------------------------------------------------------------------
    #
    #  CAPACITY TABLE
    #--------------------------------------------------------------------------------------
    # wipe out the existing DB
    truncate_tables(currLocal,'mining_capacity_daily')

    mSQLWhereExtra = ""
    sql_statement = "select count (*) from dbo.Mining_Capacity_Daily "
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = "  " + mSQLWhereExtra
    sql_statement += mSQLWhere
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r1 = mCur.fetchall()
    for datarow in r1:
        #
        mTotRecs = datarow[0]
    #--------------------------------------------------------------------
    mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
    mFields += "mineStage,capacityType,commodityByCapacity,capacityYear,capacity,"
    mFields += "capacityUnit,source,MineID"
    sql_statement = "select " + mFields + " from Mining_Capacity_Daily"
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = " " + mSQLWhereExtra
    #print sql_statement
    sql_statement += mSQLWhere + mSQLOrderBy
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r2 = mCur.fetchall()
    #
    recsProcessed = 0
    if debugMode:
        print "*"*25
        print sql_statement
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
        source= datarow[11]
        if source:
            source += ' '
        MineID = datarow[12]
        #
        sqlStatement = "INSERT INTO mining_Capacity_daily ("+\
                       "NewMineId,mineName,mineCountry,state,mineRegion,"+\
                       "mineStage,capacityType,commodityByCapacity,capacityYear,capacity,"+\
                       "capacityUnit,source,Mineid) "+\
                       "VALUES ("+\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s )"
        currLocal.execute(sqlStatement,(NewMineId,mineName,mineCountry,state,mineRegion,mineStage,capacityType,commodityByCapacity,capacityYear,capacity,capacityUnit,source,MineID))
        currLocal.execute("commit;")
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_capacity_daily - " + str(round(recsProcessed/mTotRecs,2)*100)

    #------------------------------------------------------------------------------------
    #
    #  EQUITY TABLE
    #--------------------------------------------------------------------------------------
    # wipe out the existing DB
    truncate_tables(currLocal,'mining_equity_daily')
    mSQLWhereExtra = ""
    sql_statement = "select count (*) from dbo.Mining_Equity_Daily "
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = "  " + mSQLWhereExtra
    sql_statement += mSQLWhere
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r1 = mCur.fetchall()
    for datarow in r1:
        #
        mTotRecs = datarow[0]
    #--------------------------------------------------------------------
    mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
    mFields += "mineStage,equityPartnerStatus,equityCompany,equityPartnerStake,equityPartnerBeginningYear,"
    mFields += "source,MineID"
    sql_statement = "select " + mFields + " from Mining_equity_daily"
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = " " + mSQLWhereExtra
    #print sql_statement
    sql_statement += mSQLWhere + mSQLOrderBy
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r2 = mCur.fetchall()
    #
    recsProcessed = 0
    if debugMode:
        print "*"*25
        print sql_statement
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
        source= datarow[10]
        if source:
            source += ' '
        MineID = datarow[11]
        #
        sqlStatement = "INSERT INTO mining_Equity_daily ("+\
                       "NewMineId,mineName,mineCountry,state,mineRegion,"+\
                       "mineStage,equityPartnerStatus,equityCompany,equityPartnerStake,equityPartnerBeginningYear,"+\
                       "source,MineID) "+\
                       "VALUES ("+\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s )"
        currLocal.execute(sqlStatement,(NewMineId,mineName,mineCountry,state,mineRegion,mineStage,equityPartnerStatus,equityCompany,equityPartnerStake,equityPartnerBeginningYear,source,MineID))
        currLocal.execute("commit;")
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_Equity_daily - " + str(round(recsProcessed/mTotRecs,2)*100)
    #------------------------------------------------------------------------------------
    #
    #  MODEL RULES TABLE
    #--------------------------------------------------------------------------------------
    # wipe out the existing DB
    truncate_tables(currLocal,'mining_model_rules')
    mSQLWhereExtra = ""
    sql_statement = "SELECT COUNT(*) FROM dbo.Mining_Model_Rules "
    mSQLOrderBy = " ORDER BY param_name "
    mSQLWhere = "  " + mSQLWhereExtra
    sql_statement += mSQLWhere
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r1 = mCur.fetchall()
    for datarow in r1:
        mTotRecs = datarow[0]
    #--------------------------------------------------------------------
    field_names = ['NewmineId', 'MineID', 'mineName', 'mineCountry', 'state', 'mineRegion', 'mineStage', 'mineType', 'mineMethod', 'commodity', 'production_total',
                   'production_peak', 'production_units', 'operators', 'param_name', 'param_value', 'param_table', 'param_range', 'Add_by', 'Edit_date']
    mFields = ','.join(field_names)
    varStr = ','.join(["%s"]*len(field_names))
    sql_statement = "SELECT %s FROM Mining_Model_Rules ORDER BY param_name " % mFields
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    mining_data = mCur.fetchall()
    #
    recsProcessed = 0
    for datarow in mining_data:
        sqlStatement  = 'INSERT INTO mining_Model_Rules (%s) VALUES (%s)' % (mFields, varStr)
        currLocal.execute(sqlStatement,datarow)
        currLocal.execute('COMMIT')
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_model_rules - " + str(round(recsProcessed/mTotRecs,2)*100)
    #------------------------------------------------------------------------------------
    #
    #  MODEL RULES PENDING TABLE
    #--------------------------------------------------------------------------------------
    # wipe out the existing DB
    truncate_tables(currLocal,'mining_model_rulespending')
    mSQLWhereExtra = ""
    sql_statement = "select count (*) from dbo.Mining_Model_RulesPending "
    mSQLOrderBy = " order by param_name "
    mSQLWhere = "  " + mSQLWhereExtra
    sql_statement += mSQLWhere
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r1 = mCur.fetchall()
    for datarow in r1:
        #
        mTotRecs = datarow[0]
    #--------------------------------------------------------------------
    mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
    mFields += "mineStage,mineType,mineMethod,commodity,production_total,"
    mFields += "production_peak,production_units,operators,param_name,param_value,"
    mFields += "param_table,param_range,MineID"
    sql_statement = "select " + mFields + " from Mining_Model_RulesPending"
    mSQLOrderBy = " order by param_name "
    mSQLWhere = " " + mSQLWhereExtra
    #print sql_statement
    sql_statement += mSQLWhere + mSQLOrderBy
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r2 = mCur.fetchall()
    #
    recsProcessed = 0
    if debugMode:
        print "*"*25
        print sql_statement
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
        sqlStatement = "INSERT INTO mining_Model_RulesPending ("+\
                       "NewMineId,mineName,mineCountry,state,mineRegion,"+\
                       "mineStage,mineType,mineMethod,commodity,production_total,"+\
                       "production_peak,production_units,operators,param_name,param_value,"+\
                       "param_table,param_range,MineID) "+\
                       "VALUES ("+\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s)"
        currLocal.execute(sqlStatement,(NewMineId,mineName,mineCountry,state,mineRegion,\
                                        mineStage,mineType,mineMethod,commodity,production_total,\
                                        production_peak,production_units,operators,param_name,param_value,\
                                        param_table,param_range,MineID))
        currLocal.execute("commit;")
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_model_rulespending - " + str(round(recsProcessed/mTotRecs,2)*100)
    #------------------------------------------------------------------------------------
    #
    #  CAPACITY DAILY TABLE
    #--------------------------------------------------------------------------------------
    # wipe out the existing DB
    truncate_tables(currLocal,'mining_operator_daily')
    mSQLWhereExtra = ""
    sql_statement = "select count (*) from dbo.Mining_Operator_daily "
    mSQLOrderBy = " order by newmineid "
    mSQLWhere = "  " + mSQLWhereExtra
    sql_statement += mSQLWhere
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r1 = mCur.fetchall()
    for datarow in r1:
        #
        mTotRecs = datarow[0]
    #--------------------------------------------------------------------
    mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
    mFields += "mineStage,operatorType,OperatorCompany,operatorBeginningYear,operatorSources,MineID"
    sql_statement = "select " + mFields + " from Mining_Operator_daily"
    mSQLOrderBy = " order by NewMineId "
    mSQLWhere = " " + mSQLWhereExtra
    sql_statement += mSQLWhere + mSQLOrderBy
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r2 = mCur.fetchall()
    #
    recsProcessed = 0
    if debugMode:
        print "*"*25
        print sql_statement
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
        if operatorSources:
            operatorSources += ' '
        MineID = datarow[10]
        #
        sqlStatement = "INSERT INTO mining_Operator_daily ("+\
                       "NewMineId,mineName,mineCountry,state,mineRegion,"+\
                       "mineStage,operatorType,equityCompany,operatorBeginningYear,operatorSources,Mineid) "+\
                       "VALUES ("+\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," \
                       "%s )"
        currLocal.execute(sqlStatement,(NewMineId,mineName,mineCountry,state,mineRegion,\
                                        mineStage,operatorType,equityCompany,operatorBeginningYear,operatorSources,MineID))
        currLocal.execute("commit;")
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_operator_daily - " + str(round(recsProcessed/mTotRecs,2)*100)
    #------------------------------------------------------------------------------------
    #
    #  ORE QUALITY TABLE
    #--------------------------------------------------------------------------------------
    # wipe out the existing DB
    truncate_tables(currLocal,'mine_ore_quality')

    mSQLWhereExtra = ""
    sql_statement = "select count (*) from dbo.Mine_Ore_Quality "
    mSQLOrderBy = " order by newmineid "
    mSQLWhere = "  " + mSQLWhereExtra
    sql_statement += mSQLWhere
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r1 = mCur.fetchall()
    for datarow in r1:
        #
        mTotRecs = datarow[0]
    #--------------------------------------------------------------------
    mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
    mFields += "mineStage,elementName,grade,gradeUnits,source,MineID"
    sql_statement = "select " + mFields + " from Mine_ore_quality"
    mSQLOrderBy = " order by NewMineId "
    mSQLWhere = " " + mSQLWhereExtra
    sql_statement += mSQLWhere + mSQLOrderBy
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r2 = mCur.fetchall()
    #
    recsProcessed = 0
    if debugMode:
        print "*"*25
        print sql_statement
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
        if source:
            source += ' '
        MineID = datarow[10]
        #
        sqlStatement = "INSERT INTO Mine_Ore_Quality ("+\
                       "NewMineId,mineName,mineCountry,state,mineRegion,"+\
                       "mineStage,elementName,grade,gradeUnits,source,MineID) "+\
                       "VALUES ("+\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," \
                       "%s )"
        currLocal.execute(sqlStatement,(NewMineId,mineName,mineCountry,state,mineRegion,\
                                        mineStage,elementName,grade,gradeUnits,source,MineID))
        currLocal.execute("commit;")
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_ore_quality - " + str(round(recsProcessed/mTotRecs,2)*100)
    #------------------------------------------------------------------------------------
    #
    #  MINING PRODUCTION DAILY TABLE
    #--------------------------------------------------------------------------------------
    # wipe out the existing DB
    truncate_tables(currLocal,'mining_production_daily')
    mSQLWhereExtra = ""
    sql_statement = "select count (*) from dbo.Mining_Production_Daily "
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = "  " + mSQLWhereExtra
    sql_statement += mSQLWhere
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r1 = mCur.fetchall()
    for datarow in r1:
        #
        mTotRecs = datarow[0]
    #--------------------------------------------------------------------
    mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
    mFields += "mineStage,productionType,productionByCommodity,productionYear,productionValue,"
    mFields += "productionUnit,source,MineID"
    sql_statement = "select " + mFields + " from Mining_Production_Daily"
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = " " + mSQLWhereExtra
    sql_statement += mSQLWhere + mSQLOrderBy
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r2 = mCur.fetchall()
    #
    recsProcessed = 0
    if debugMode:
        print "*"*25
        print sql_statement
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
        source= datarow[11]
        if source:
            source += ' '
        MineID = datarow[12]
        #
        sqlStatement = "INSERT INTO Mining_Production_Daily ("+\
                       "NewMineId,mineName,mineCountry,state,mineRegion,"+\
                       "mineStage,productionType,productionByCommodity,productionYear,productionValue,"+\
                       "productionUnit,source,Mineid) "+\
                       "VALUES ("+\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s )"
        currLocal.execute(sqlStatement,(NewMineId,mineName,mineCountry,state,mineRegion,\
                                        mineStage,productionType,productionByCommodity,productionYear,productionValue,\
                                        productionUnit,source,MineID))
        currLocal.execute("commit;")
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_production_daily - " + str(round(recsProcessed/mTotRecs,2)*100)
    #------------------------------------------------------------------------------------
    #
    #  MINING RESERVES DAILY TABLE
    #--------------------------------------------------------------------------------------
    # wipe out the existing DB
    truncate_tables(currLocal,'mining_reserves_daily')
    mSQLWhereExtra = ""
    sql_statement = "select count (*) from dbo.Mining_Reserves_Daily "
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = "  " + mSQLWhereExtra
    sql_statement += mSQLWhere
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r1 = mCur.fetchall()
    for datarow in r1:
        #
        mTotRecs = datarow[0]
    #--------------------------------------------------------------------
    mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
    mFields += "mineStage,reserveType,commodityByReserve,reserveYear,reserve,"
    mFields += "reserveUnit,source,MineID"
    sql_statement = "select " + mFields + " from Mining_Reserves_Daily"
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = " " + mSQLWhereExtra
    #print sql_statement
    sql_statement += mSQLWhere + mSQLOrderBy
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r2 = mCur.fetchall()
    #
    recsProcessed = 0
    if debugMode:
        print "*"*25
        print sql_statement
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
        source= datarow[11]
        if source:
            source += ' '
        MineID = datarow[12]
        #
        sqlStatement = "INSERT INTO Mining_Reserves_Daily ("+\
                       "NewMineId,mineName,mineCountry,state,mineRegion,"+\
                       "mineStage,reserveType,commodityByReserve,reserveYear,reserve,"+\
                       "reserveUnit,source,Mineid) "+\
                       "VALUES ("+\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s )"
        currLocal.execute(sqlStatement,(NewMineId,mineName,mineCountry,state,mineRegion,\
                                        mineStage,reserveType,commodityByReserve,reserveYear,reserve,\
                                        reserveUnit,source,MineID))
        currLocal.execute("commit;")
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_reserves_daily - " + str(round(recsProcessed/mTotRecs,2)*100)
    #------------------------------------------------------------------------------------
    #
    #  MINING RESOURCES DAILY TABLE
    #--------------------------------------------------------------------------------------
    # wipe out the existing DB
    truncate_tables(currLocal,'mining_resource_daily')
    mSQLWhereExtra = ""
    sql_statement = "select count (*) from dbo.Mining_Resource_Daily "
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = "  " + mSQLWhereExtra
    sql_statement += mSQLWhere
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r1 = mCur.fetchall()
    for datarow in r1:
        #
        mTotRecs = datarow[0]
    #--------------------------------------------------------------------
    mFields = "NewmineId,mineName,mineCountry,state,mineRegion,"
    mFields += "mineStage,resourceType,commodityByResource,resourceYear,resource,"
    mFields += "resourceUnit,source,MineID"
    sql_statement = "select " + mFields + " from Mining_Resource_Daily"
    mSQLOrderBy = " order by Newmineid "
    mSQLWhere = " " + mSQLWhereExtra
    #print sql_statement
    sql_statement += mSQLWhere + mSQLOrderBy
    mCur = conn.cursor()
    mCur.execute(sql_statement)
    r2 = mCur.fetchall()
    #
    recsProcessed = 0
    if debugMode:
        print "*"*25
        print sql_statement
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
        source= datarow[11]
        if source:
            source += ' '
        MineID = datarow[12]
        #
        sqlStatement = "INSERT INTO Mining_Resource_Daily ("+\
                       "NewMineId,mineName,mineCountry,state,mineRegion,"+\
                       "mineStage,resourceType,commodityByResource,resourceYear,resource,"+\
                       "resourceUnit,source,MineID) "+\
                       "VALUES ("+\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s, %s, %s," +\
                       "%s, %s, %s )"
        currLocal.execute(sqlStatement,(NewMineId,mineName,mineCountry,state,mineRegion,\
                                        mineStage,resourceType,commodityByResource,resourceYear,resource,\
                                        resourceUnit,source, MineID))
        currLocal.execute("commit;")
        recsProcessed += 1
        if recsProcessed % 100 == 0:
            print "Table: mining_resource_daily - " + str(round(recsProcessed/mTotRecs,2)*100)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def truncate_tables(currLocal,tableName):
    sqlStatement = "TRUNCATE TABLE  " + tableName
    currLocal.execute(sqlStatement)
    currLocal.execute("commit;")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_total_factors(debug=False):
    conn = start_database(database='miningengineextract')
    curr = conn.cursor()
    table_names = {
        'reserves': {  'Probable Reserves': {'param_name': 'PROBABLE_TO_TOTAL'},
                         'Proved Reserves': {'param_name': 'PROVED_TO_TOTAL'}},

        'resource': { 'Measured Resources': {'param_name': 'MEASURED_TO_TOTAL'},
                     'Indicated Resources': {'param_name': 'INDICATED_TO_TOTAL'},
                      'Inferred Resources': {'param_name': 'INFERRED_TO_TOTAL'}}
    }
    for data_table in table_names.keys():
        for data_type in table_names[data_table]:
            print 'Updating %s to total average ...' % data_type.lower()
            param_name = table_names[data_table][data_type]['param_name']
            param_value = get_total_factor(curr, data_table, data_type, debug)
            sql_insert  = 'INSERT INTO mining_model_rules (NewMineId, MineId, production_total, production_peak, param_name, param_value) '
            sql_insert += 'VALUES (0, 0, 0, 0, "%s", %s)' % (param_name, param_value)
            curr.execute(sql_insert)
            conn.commit()
    curr.close()
    conn.close()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_mining_ore_grade(clear_tbl=False, ore_data=False, comm_names=False, update_avgs=False, country_avg=False, region_avg=False, global_avg=False, ore_default=False, update_ranks=False, debugMode=False):
    debug = debugMode
    conn = start_database(database='miningengineextract')
    curr = conn.cursor()
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if clear_tbl:
        print 'Clearing mining_ore_table ...'
        curr.execute("TRUNCATE TABLE mining_ore_grade")
        curr.execute("TRUNCATE TABLE mining_ore_grade_temp")
        conn.commit()
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if ore_data:
        print 'Inserting data from mine_ore_quality table ...'
        curr.execute('SELECT DISTINCT NewMineId, mineCountry, mineRegion, elementName, grade, gradeUnits FROM mine_ore_quality')
        ore_quality_data = curr.fetchall()
        for mine_id, country, region, element, grade, gradeUnit in ore_quality_data:
            if '-' in grade:
                continue
            grade = grade.replace(' ', '')
            grade = grade.replace(',', '')
            grade = grade.replace('..', '.')
            if grade[-1] == '%':
                grade = grade[:-1]
            if 'to' in grade:
                grade_low = min([float(grade_num.strip()) for grade_num in grade.split('to')])
                grade_high = max([float(grade_num.strip()) for grade_num in grade.split('to')])
                grade = float((grade_high + grade_low)/2.0)
            elif grade.count('.') > 1:
                grade = float('{}.{}{}'.format(grade.strip().split('.')[0], grade.strip().split('.')[1], grade.strip().split('.')[2]))
            else:
                grade = float(grade.strip())
            params = (mine_id, country, region, element, grade, gradeUnit)
            curr.execute('INSERT INTO mining_ore_grade_temp (NewMineId, mineCountry, mineRegion, elementName, sourceType, oreGrade, oreGradeUnit) VALUES (%s, %s, %s, %s, "Mine_Ore_Quality", %s, %s)', params)
            conn.commit()
        # --------------------------------------------------------------------------------------------------
        print 'Inserting data from mining_production_daily table ...'
        curr.execute('SELECT DISTINCT NewMineId, mineCountry, mineRegion, commodity, sourceType, sourceYear FROM mining_ore_grade_temp')
        ore_grade_data = curr.fetchall()
        curr.execute('SELECT DISTINCT NewMineId, mineCountry, mineRegion, productionByCommodity, productionType, productionYear, productionValue, productionUnit FROM mining_production_daily WHERE NOT productionValue LIKE "%.%.%" AND productionType IN ("Ore Grade", "Ore milled grade") ')
        ore_prod_data = curr.fetchall()
        for mine_id, country, region, commodity, source_type, source_year, grade, gradeUnit in ore_prod_data:
            params = (mine_id, country, region, commodity, source_type, source_year)
            if not params in ore_grade_data:
                if grade and ' ' not in grade.strip():
                    grade = grade.replace('..', '.')
                    params += (grade, gradeUnit)
                    if debug:
                        print 'INSERT INTO mining_ore_grade_temp (NewMineId, mineCountry, mineRegion, commodity, sourceType, sourceYear, oreGrade, oreGradeUnit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)' % params
                    curr.execute('INSERT INTO mining_ore_grade_temp (NewMineId, mineCountry, mineRegion, commodity, sourceType, sourceYear, oreGrade, oreGradeUnit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', params)
                    conn.commit()
        # --------------------------------------------------------------------------------------------------
        print 'Inserting data from mining_reserves_daily table ...'
        curr.execute('SELECT DISTINCT NewMineId, mineCountry, mineRegion, commodity, sourceType, sourceYear FROM mining_ore_grade_temp')
        ore_grade_data = curr.fetchall()
        curr.execute('SELECT DISTINCT NewMineId, mineCountry, mineRegion, CommodityByReserve, reserveType, reserveYear, reserve, reserveUnit FROM mining_reserves_daily WHERE NOT reserve LIKE "%.%.%" AND reserveType LIKE "%Metal Grade" ')
        ore_reserves_data = curr.fetchall()
        for mine_id, country, region, commodity, source_type, source_year, grade, gradeUnit in ore_reserves_data:
            params = (mine_id, country, region, commodity, source_type, source_year)
            if not params in ore_grade_data:
                if grade and ' ' not in grade.strip():
                    grade = grade.replace('..', '.')
                    params += (grade, gradeUnit)
                    if debug:
                        print 'INSERT INTO mining_ore_grade_temp (NewMineId, mineCountry, mineRegion, commodity, sourceType, sourceYear, oreGrade, oreGradeUnit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)' % params
                    curr.execute('INSERT INTO mining_ore_grade_temp (NewMineId, mineCountry, mineRegion, commodity, sourceType, sourceYear, oreGrade, oreGradeUnit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', params)
                    conn.commit()
        # --------------------------------------------------------------------------------------------------
        print 'Inserting data from mining_resource_daily table ...'
        curr.execute('SELECT DISTINCT NewMineId, mineCountry, mineRegion, commodity, sourceType, sourceYear FROM mining_ore_grade_temp')
        ore_grade_data = curr.fetchall()
        curr.execute('SELECT DISTINCT NewMineId, mineCountry, mineRegion, CommodityByResource, resourceType, resourceYear, resource, resourceUnit FROM mining_resource_daily WHERE NOT resource LIKE "%.%.%" AND resourceType LIKE "%Metal Grade" ')
        ore_reserves_data = curr.fetchall()
        for mine_id, country, region, commodity, source_type, source_year, grade, gradeUnit in ore_reserves_data:
            params = (mine_id, country, region, commodity, source_type, source_year)
            if not params in ore_grade_data:
                if grade and ' ' not in grade.strip():
                    grade = grade.replace('..', '.')
                    params += (grade, gradeUnit)
                    if debug:
                        print 'INSERT INTO mining_ore_grade_temp (NewMineId, mineCountry, mineRegion, commodity, sourceType, sourceYear, oreGrade, oreGradeUnit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)' % params
                    curr.execute('INSERT INTO mining_ore_grade_temp (NewMineId, mineCountry, mineRegion, commodity, sourceType, sourceYear, oreGrade, oreGradeUnit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', params)
                    conn.commit()
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
        # New processing steps added 20190502
        # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        print "Updating commodity and elementName columns ..."
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp AS a, miningengineextract.mining_compounds AS b SET a.commodity=b.commodity WHERE a.elementName=b.elementName AND a.commodity IS NULL")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp AS a, miningengineextract.mining_compounds AS b SET a.elementName=b.elementName WHERE a.commodity=b.commodity AND a.elementName IS NULL")
        conn.commit()

        # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        print "Updating sourceRank column ..."
        curr.execute("UPDATE miningengineextract.mining_ore_grade SET oreGrade=99.9 WHERE oreGradeUnit='%' AND oreGrade>=100")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp SET sourceRank=1  WHERE sourceType='Ore Grade'")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp SET sourceRank=2  WHERE sourceType='Ore milled grade'")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp SET sourceRank=3  WHERE sourceType='Total Reserves - Metal Grade'")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp SET sourceRank=4  WHERE sourceType='Probable Reserves - Metal Grade'")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp SET sourceRank=5  WHERE sourceType='Proved Reserves - Metal Grade'")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp SET sourceRank=6  WHERE sourceType='Total Resources Metal Grade'")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp SET sourceRank=7  WHERE sourceType='Measured Resources Metal Grade'")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp SET sourceRank=8  WHERE sourceType='Indicated Resources Metal Grade'")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp SET sourceRank=9  WHERE sourceType='Inferred Resources Metal Grade'")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade_temp SET sourceRank=10 WHERE sourceType='mine_ore_quality'")
        conn.commit()

        # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        print "Inserting highest ranking ore grade for each year for each commodity into mining_ore_grade from temp table ..."
        sql_insert = \
            '''
            INSERT INTO mining_ore_grade (NewMineId, mineCountry, mineRegion, commodity, sourceType, sourceYear, sourceRank, oreGrade, oreGradeUnit)
             (SELECT DISTINCT a.NewMineId, a.mineCountry, a.mineRegion, a.commodity, a.sourceType, a.sourceYear, a.sourceRank, a.oreGrade AS oreGradeDefault, a.oreGradeUnit 
                FROM miningengineextract.mining_ore_grade_temp AS a, (SELECT DISTINCT NewMineId, commodity, sourceYear, MIN(sourceRank) AS oreRank FROM miningengineextract.mining_ore_grade_temp GROUP BY NewMineID, commodity, sourceYear) AS b 
                WHERE a.sourceYear=b.sourceYear AND a.sourceRank=b.oreRank AND a.NewMineId=b.NewMineId AND a.commodity=b.commodity 
                GROUP BY NewMineId, sourceYear, oreGradeUnit
                ORDER BY NewMineId, commodity, oreGradeUnit, sourceYear, sourceRank ASC);
            '''
        curr.execute(sql_insert)
        conn.commit()

        # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        print "Updating mining_ore_commodities table ..."
        curr.execute("DROP TABLE IF EXISTS mining_ore_commodities")

        sql_create = \
            '''
            CREATE TABLE `mining_ore_commodities` (
              `NewMineId` int(11) DEFAULT NULL,
              `mineCountry` varchar(200) DEFAULT NULL,
              `mineRegion` varchar(200) DEFAULT NULL,
              `commodity` varchar(200) DEFAULT NULL,
              `sourceType` varchar(50) DEFAULT NULL,
              `sourceYear` int(11) DEFAULT NULL,
              KEY `mine_id_indx` (`NewMineId`),
              KEY `mine_country_indx` (`mineCountry`),
              KEY `mine_region_indx` (`mineRegion`),
              KEY `commodity_indx` (`commodity`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            '''
        curr.execute(sql_create)
        conn.commit()

        comm_cols = [('production', 'productionByCommodity'), ('capacity', 'commodityByCapacity'), ('reserves', 'commodityByReserve'), ('resource', 'commodityByResource')]
        sql_insert = "INSERT INTO mining_ore_commodities (NewMineId,mineCountry,mineRegion,commodity,sourceType,sourceYear) (SELECT DISTINCT NewMineId,mineCountry,mineRegion,{1},'Mine Default',9999 FROM mining_{0}_daily WHERE LENGTH({1}) > 0 ORDER BY NewMineId, {1})"
        for data_table, data_col in comm_cols:
            curr.execute(sql_insert.format(data_table, data_col))
            conn.commit()

        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------

        print "Inserting data into mining_ore_grade from mining_ore_commodities table ..."
        curr.execute("INSERT INTO mining_ore_grade (NewMineId,mineCountry,mineRegion,commodity,sourceType,sourceYear) (SELECT DISTINCT NewMineId,mineCountry,mineRegion,commodity,sourceType,sourceYear FROM mining_ore_commodities ORDER BY NewMineId, commodity)")
        conn.commit()

        # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        print "Updating Mine Defaults with highest ranking most recent sourced data ..."
        sql_update = \
            '''
            UPDATE miningengineextract.mining_ore_grade AS aa,
               (SELECT DISTINCT a.NewMineId, a.mineCountry, a.mineRegion, a.commodity, a.sourceType, a.sourceYear, a.sourceRank, a.oreGrade AS oreGradeDefault, a.oreGradeUnit 
                 FROM miningengineextract.mining_ore_grade_temp AS a, 
                      (SELECT DISTINCT NewMineId, MAX(sourceYear) AS max_ore_grade_year FROM miningengineextract.mining_ore_grade_temp GROUP BY NewMineID) AS b 
                   WHERE a.sourceYear=b.max_ore_grade_year 
                   AND a.NewMineId=b.NewMineId 
                   AND NOT oreGradeUnit IS NULL 
                   GROUP BY NewMineId, commodity, oreGradeUnit 
                   ORDER BY NewMineId, commodity, oreGradeUnit, sourceRank ASC) AS bb
              SET aa.oreGrade=bb.oreGradeDefault, aa.oreGradeUnit=bb.oreGradeUnit, aa.sourceYear=bb.sourceYear WHERE aa.NewMineId=bb.NewMineId AND aa.mineCountry=bb.mineCountry AND aa.mineRegion=bb.mineRegion AND aa.commodity=bb.commodity AND aa.sourceType='Mine Default' AND aa.oreGrade IS NULL;
            '''
        curr.execute(sql_update)
        conn.commit()

        # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if update_avgs:
        curr.execute('TRUNCATE mining_ore_averages')
        conn.commit()
        curr.execute('INSERT INTO mining_ore_averages (mineCountry, mineRegion, commodity, oreGradeUnit) (SELECT DISTINCT mineCountry, mineRegion, commodity, oreGradeUnit FROM mining_ore_grade WHERE NOT oreGrade IS NULL)')
        conn.commit()
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if country_avg:
        print 'Updating average ore-grade for each commodity by country ...'
        curr.execute('SELECT DISTINCT mineCountry, commodity, oreGradeUnit FROM mining_ore_grade WHERE NOT oreGrade IS NULL')
        ore_country_data = curr.fetchall()
        for country, commodity, ore_grade_unit in ore_country_data:
            ore_country_avg = get_ore_country_avg(curr, commodity, country, ore_grade_unit=ore_grade_unit)
            curr.execute('UPDATE mining_ore_averages SET countryAvg=%s WHERE commodity="%s" AND mineCountry="%s" AND oreGradeUnit="%s" ' % (ore_country_avg, commodity, country, ore_grade_unit))
            conn.commit()
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if region_avg:
        print 'Updating average ore-grade for each commodity by region ...'
        curr.execute('SELECT DISTINCT mineRegion, commodity, oreGradeUnit FROM mining_ore_grade WHERE NOT oreGrade IS NULL')
        ore_region_data = curr.fetchall()
        for region, commodity, ore_grade_unit in ore_region_data:
            ore_region_avg = get_ore_region_avg(curr, commodity, region, ore_grade_unit=ore_grade_unit)
            curr.execute('UPDATE mining_ore_averages SET regionAvg=%s WHERE commodity="%s" AND mineRegion="%s" AND oreGradeUnit="%s" ' % (ore_region_avg, commodity, region, ore_grade_unit))
            conn.commit()
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if global_avg:
        print 'Updating global average ore-grade for each commodity ...'
        curr.execute('SELECT DISTINCT commodity, oreGradeUnit FROM mining_ore_grade WHERE NOT oreGrade IS NULL')
        ore_commodity_data = curr.fetchall()
        for commodity, ore_grade_unit in ore_commodity_data:
            ore_global_avg = get_ore_global_avg(curr, commodity, ore_grade_unit=ore_grade_unit)
            curr.execute('UPDATE mining_ore_averages SET globalAvg=%s WHERE commodity="%s" AND oreGradeUnit="%s" ' % (ore_global_avg, commodity, ore_grade_unit))
            conn.commit()
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if ore_default:
        print 'Updating global average ore-grade for each commodity ...'
        commodities = []
        curr.execute('SELECT DISTINCT commodityByCapacity FROM mining_capacity_daily WHERE NOT commodityByCapacity IN (SELECT DISTINCT commodity FROM mining_ore_averages)')
        capacity_comms = [data[0] for data in curr.fetchall()]
        commodities += capacity_comms
        curr.execute('SELECT DISTINCT productionByCommodity FROM mining_production_daily WHERE NOT productionByCommodity IN (SELECT DISTINCT commodity FROM mining_ore_averages)')
        production_comms = [data[0] for data in curr.fetchall()]
        commodities += production_comms
        commodities = list(set(commodities))
        ore_grade_default = get_ore_grade_default(curr)
        for commodity in commodities:
            curr.execute('INSERT INTO mining_ore_averages (commodity, globalAvg) VALUES ("%s", %s)' % (commodity, ore_grade_default))
            conn.commit()

    if update_avgs:
        # 11 Update miningengineextract.mining_ore_averages ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        print "Updating mining_ore_averages from data in mining_ore_grade table ..."

        curr.execute("UPDATE miningengineextract.mining_ore_averages SET countryAvg=ROUND(countryAvg, 5), regionAvg=ROUND(regionAvg, 5), globalAvg=ROUND(globalAvg, 5)")
        conn.commit()

        # 12 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        print "Filling in data missing from mining_ore_grade with averages from mining_ore_averages ..."

        curr.execute("UPDATE mining_ore_grade AS a, mining_ore_averages AS b SET a.oreGrade=b.countryAvg, a.oreGradeUnit=b.oreGradeUnit WHERE a.oreGrade IS NULL AND a.mineCountry=b.mineCountry AND a.commodity=b.commodity AND a.sourceType='Mine Default'")
        conn.commit()
        curr.execute("UPDATE mining_ore_grade AS a, mining_ore_averages AS b SET a.oreGrade=b.regionAvg, a.oreGradeUnit=b.oreGradeUnit WHERE a.oreGrade IS NULL AND a.mineRegion=b.mineRegion AND a.commodity=b.commodity AND a.sourceType='Mine Default'")
        conn.commit()
        curr.execute("UPDATE mining_ore_grade AS a, mining_ore_averages AS b SET a.oreGrade=b.globalAvg, a.oreGradeUnit=b.oreGradeUnit WHERE a.oreGrade IS NULL AND a.commodity=b.commodity AND a.sourceType='Mine Default'")
        conn.commit()

        # 13 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        print "Cleaning oreGrade and oreGradeUnit data ..."
        curr.execute("UPDATE miningengineextract.mining_ore_grade SET oreGradeUnit='%' WHERE oreGradeUnit IS NULL")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade SET oreGrade=oreGrade/100 WHERE oreGradeUnit='%'")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade SET oreGrade=ROUND(oreGrade,5)")
        conn.commit()
        curr.execute("UPDATE miningengineextract.mining_ore_grade SET sourceYear=9999 WHERE sourceType='Mine Default'")
        conn.commit()
    curr.close()
    conn.close()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_saleable_to_rom(debug=False):
    conn = start_database(database='miningengineextract')
    curr = conn.cursor()
    curr.execute('DELETE FROM mining_model_rules WHERE param_name="SALEABLE_PRODUCTION_YIELD_FACTOR"')
    conn.commit()
    sql_select  = "SELECT a.productionByCommodity, a.productionValue/b.productionValue AS sale_to_rom FROM mining_production_daily AS a, mining_production_daily AS b "
    sql_select += "WHERE a.NewMineId=b.NewMineId AND a.productionType='Saleable Production' AND b.productionType='ROM Production' "
    sql_select += "AND a.productionYear=b.productionYear AND a.productionUnit=b.productionUnit "
    sql_select += "AND NOT (UCASE(a.source) LIKE 'EST:%' OR UCASE(a.source) LIKE '%ESTIMATION%' OR a.source='') "
    sql_select += "AND NOT (UCASE(b.source) LIKE 'EST:%' OR UCASE(b.source) LIKE '%ESTIMATION%' OR b.source='') "
    #
    curr.execute(sql_select)
    sale_prod_ratios = curr.fetchall()
    if debug:
        print 'sale_prod_ratios:', sale_prod_ratios
    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    sql_select  = "SELECT a.CommodityByCapacity, a.capacity/b.capacity AS sale_to_rom FROM mining_capacity_daily AS a, mining_capacity_daily AS b "
    sql_select += "WHERE a.NewMineId=b.NewMineId AND a.capacityType='Saleable Capacity' AND b.capacityType='ROM Capacity' "
    sql_select += "AND a.capacityYear=b.capacityYear AND a.capacityUnit=b.capacityUnit "
    sql_select += "AND NOT (UCASE(a.source) LIKE 'EST:%' OR UCASE(a.source) LIKE '%ESTIMATION%' OR a.source='') "
    sql_select += "AND NOT (UCASE(b.source) LIKE 'EST:%' OR UCASE(b.source) LIKE '%ESTIMATION%' OR b.source='') "
    #
    curr.execute(sql_select)
    sale_cap_ratios = curr.fetchall()
    if debug:
        print 'sale_cap_ratios:', sale_cap_ratios
    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    commodities = list(set([data[0] for data in (sale_prod_ratios + sale_cap_ratios)]))
    saleable_ratios = {commodity: [sale_avg for (sale_comm, sale_avg) in (sale_prod_ratios + sale_cap_ratios) if (sale_comm == commodity) if sale_avg > 0] for commodity in commodities}
    saleable_avgs = {commodity: sum(ratios)/float(len(ratios)) for (commodity, ratios) in saleable_ratios.items()}
    if debug:
        print 'saleable_avgs:', saleable_avgs
    for commodity, saleable_avg in saleable_avgs.items():
        sql_insert = 'INSERT INTO mining_model_rules (NewMineid, Mineid, commodity, production_total, production_peak, param_name, param_value) VALUES (0, 0, "%s", 0, 0, "SALEABLE_PRODUCTION_YIELD_FACTOR", %s)'
        sql_insert = sql_insert % (commodity.upper(), round(saleable_avg,4))
        if debug:
            print sql_insert
        curr.execute(sql_insert)
        conn.commit()
    curr.close()
    conn.close()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#========================================================================================================================================================================
def mining_main(export_data=False, dev_mode=False, debug_mines=[]):
    mOutputLogsDir = ENGINE_DIR + 'Projects\\Mining\\'
    mSession_key   = create_session_key()
    ts             = time.time()
    st             = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    runningTime    = time.time()
    timeStarted    = datetime.now()
    dt             = timeStarted.timetuple()

    mProgComment   = 'Mining Models Program Started at: %s\n' % (get_datetime())
    print mProgComment

    mine_list = []

    devMode        = dev_mode

    forecastData   = True
    exportData     = export_data
    debugAll       = False
    paramOverride  = False

    importTables   = False
    updateOreGrade = False
    updateSaleable = False
    updateFactors  = False

    removeForecast = False
    processData    = True
    lUpdateRemote  = False
    lCopyDataLocal = False
    useLocalData   = True
    updateParamTrk = False

    debugMode      = False
    debugSQL       = False
    debugReserves  = False

    include_T2E    = True
    include_T3E    = True
    ytp_flag       = True

    #===============================
    if devMode:
        importTables   = False
        lCopyDataLocal = False
        updateOreGrade = False
        updateSaleable = False
        updateFactors  = False
        updateParamTrk = False
        debugAll       = True

        paramOverride  = False
        forecastData   = False
        processData    = True
        removeForecast = True
        mine_list      = debug_mines

    if forecastData:
        removeForecast = True
        processData    = True
        lUpdateRemote  = True
        lCopyDataLocal = True
        useLocalData   = True
        importTables   = True
        updateOreGrade = True
        updateSaleable = True
        updateFactors  = True
        exportData     = True
        updateParamTrk = False
        mine_list = []

    if debugAll:
        debugMode      = True
        debugSQL       = True
        debugReserves  = True

    if paramOverride:
        importTables   = False
        updateOreGrade = False
        updateSaleable = False
        updateFactors  = False
        lCopyDataLocal = False
        processData    = True
        lUpdateRemote  = False
        exportData     = False
        removeForecast = False
        mine_list      = [106946]

    #===============================

    mine_ID              = 0
    minimumForecastMax   = 8
    max_forecast_years   = 200
    prodDecimals         = 2
    discountYear         = 2019
    years_to_project     = 7
    pct_of_capacity      = 0.90
    production_tolerance = 0.2
    last_year_fctr       = 0.5
    ore_cap_to_rom       = 0.96
    reserve_tot_resource = 0.80
    yearly_effeciency    = 0.0025
    ye_lt5               = 0.025
    ye_lt10              = 0.0025
    ye_lt20              = 0.00025

    #===============================

    MINES = {'Mine id': [],'Start year': [],'Mine life': [],'Remaining life': [],'Acreage': [],'Reserve type': [],'Reserve year': [],'Reserves': [],'Reserve unit': [], 'Capacity type': [],
             'Capacity year': [],'Capacity': [],'Capacity unit': [],'Production Type': [],'Production Year': [],'Production Value': [],'Production unit': [], 'Resource Type': [],'Commodity': [],
             'Resource Year': [],'Resource %': [],'Resource unit': [],'Production Source': [],'Resource Source': [],'Capacity Source': [], 'Reserves Source': [],'Production Source': []}

    mTotRecs = 0

    yr_range = []
    for i in range(1940,2200):
        yr_range.append(i)

    if importTables:
        import_mining_tables()

    if lCopyDataLocal:
        make_local_data()

    if updateOreGrade:
        update_mining_ore_grade(clear_tbl=True, ore_data=True, comm_names=True, update_ranks=True, update_avgs=True, country_avg=True, region_avg=True, global_avg=True, ore_default=True, debugMode=debugMode)

    if updateSaleable:
        update_saleable_to_rom(debug=debugMode)

    if updateFactors:
        update_total_factors(debug=debugMode)

    if processData:
        # Connect to local mysql database
        if useLocalData:
            mysqlHost = 'localhost'
            mysqlUser = 'root'
            mysqlPassword = 'OilAndGas321'
            mysqlDB = 'MiningEngineExtract'
            conn = pymysql.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPassword, db=mysqlDB, charset='utf8', use_unicode=True)
            curr = conn.cursor()
            curr.execute('USE MiningEngineExtract')
            prefixDB = ''
            sqlCount = 'COUNT(1)'
            param_symbol_pf = buildMySQLin(11,"%s")
            if debugMode:
                print "*"*5 + "  " + param_symbol_pf
            param_symbol_mm =  buildMySQLin(5,"%s")
            eSymbol = buildMySQLin(15,"%s")
        # Connect to external sqlserver database
        else:
            prefixDB = 'dbo.'
            sqlCount = 'COUNT(*)'
            param_symbol_pf = buildMySQLin(11,"?")
            param_symbol_mm = buildMySQLin(5,"?")
            eSymbol = buildMySQLin(15,"?")
        userName = getpass.getuser()
        # ------------------------------------------------------------------
        mSQLWhereExtra = ' AND NOT (mineSubStage="Care & Maintenance" AND mineSubStageStatus="On Hold") '
        if mine_list:
            mine_list_str = ','.join([str(mine_id) for mine_id in mine_list])
            mSQLWhereExtra += 'AND NewMineId IN (%s) ' % mine_list_str
        else:
            if mine_ID:
                mSQLWhereExtra += 'AND NewMineId = %s ' % mine_ID
        sqlExclude = 'AND NOT (UCASE(source) LIKE "EST:%" OR UCASE(source) LIKE "%ESTIMATION%" OR source="") '

        mFields  = 'NewmineId, mineStage, ActualProductionStartYear, totalMineLife, remainingMineLife, '
        mFields += 'MineAcreageHectares, mineName, mineCountry, state, mineRegion, commodities, mineType, Mineid, '

        sql_statement = 'SELECT %s FROM %sMining_Assets_Daily ' % (sqlCount, prefixDB)

        mSQLWhere = "WHERE mineStage='Operation' %s " % mSQLWhereExtra

        sql_statement += mSQLWhere

        mProgComment += '\n%s\n' % sql_statement

        if debugMode:
            print sql_statement
            print ''
        mCur1 = conn.cursor()
        mCur1.execute(sql_statement)
        mTotRecs = mCur1.fetchone()[0]
        mProgComment += '\n%s Records processsed\n' % mTotRecs

        #--------------------------------------------------------------------
        '''
        fldAssetsList2 = ['NewMineId', 'mineStage', 'ActualProductionStartYear', 'totalMineLife', 'remainingMineLife', 'MineAcreageHectares', 'mineName', 'mineCountry, state',
                          'mineRegion', 'commodities', 'mineType', 'mineMethod', 'projectType', 'mineSubStage', 'mineSubStageStatus', 'constructionStartYear', 'mineEndYear',
                          'mineDepth', 'mineLocationSource', 'remainingMineLifeYear', 'originalProductionStartYear', 'TotalMineLifeSource', 'RemainingMineLifeSource',
                          'MineEndYearSource', 'mineAcreageSource', 'ActualProductionStartYearSource', 'estimated_total_recoverable_reserves', 'Mineid']
    
        fldAssetsListDT2 = ['i','c','i','i','i','i','c','c','c','c','c','c','c','c','c','c','i','i','i','c','i','i','c','c','c','c','c','i','i']
    
        fldAssetData = {fldAssetsList2[i]: fldAssetsListDT2[i] for i in range(len(fldAssetsList2))}
        #
        '''
        fldAssetsList = []
        fldAssetsListDT = []

        fldAssets   = 'NewMineId,mineStage,ActualProductionStartYear,totalMineLife,remainingMineLife,MineAcreageHectares,mineName,mineCountry,state,'
        fldAssets  += 'mineRegion,commodities,mineType,mineMethod,projectType,mineSubStage,mineSubStageStatus,constructionStartYear,mineEndYear,'
        fldAssets  += 'mineDepth,'
        fldAssets  += 'mineLocationSource,remainingMineLifeYear,originalProductionStartYear,TotalMineLifeSource,RemainingMineLifeSource,'
        fldAssets  += 'MineEndYearSource,mineAcreageSource,ActualProductionStartYearSource,estimated_total_recoverable_reserves,Mineid,'

        fldAssetsDT = 'i,c,i,i,i,i,c,c,c,c,c,c,c,c,c,c,i,i,i,c,i,i,c,c,c,c,c,i,i,'
        #--------------------------------------------------------------------
        # Turn the line into a list
        commas = fldAssets.count(",")
        fldAssets2 = fldAssets
        fldAssetsDT2 = fldAssetsDT
        for i in range(commas):
            pos = fldAssets2.index(",")
            fldAssetsList.append(fldAssets2[:pos])
            fldAssets2 = fldAssets2[pos+1:]
            #
            posDT = fldAssetsDT2.index(",")
            fldAssetsListDT.append(fldAssetsDT2[:posDT])
            fldAssetsDT2 = fldAssetsDT2[posDT+1:]
        mFields = ""
        for i in range(len(fldAssetsList)):
            mFields += fldAssetsList[i] + ","
        # Remove last comma
        mFields = mFields[:-1]
        sql_statement = "SELECT %s FROM %sMining_Assets_Daily " % (mFields, prefixDB)
        mSQLWhere     = "WHERE mineStage = 'Operation' %s" % mSQLWhereExtra
        mSQLOrderBy   = "ORDER BY Newmineid "
        sql_statement += mSQLWhere + mSQLOrderBy
        mCur1.execute(sql_statement)
        mining_data = mCur1.fetchall()
        #
        print ''
        if debugMode:
            print sql_statement
        print ''
        print '!-' * 45
        print ''

        otherFilter = " True "

        forecastTables = \
            ['Mining_Assets_Forecast','Mining_Production_Forecast','Mining_Capacity_Forecast','Mining_Resource_Forecast','Mining_Reserves_Forecast','Mining_Error_log','Mining_metrics']

        if removeForecast:
            for table in forecastTables:
                if debugMode:
                    print 'Removing forecast data from %s ...' % table
                truncate_tables(mCur1,table)

        updateQAsite = False
        all_commodities = {}
        modelled_commod = {}
        not_modelled_commod = {}
        modelled = 0
        not_modelled = 0

        recsProcessed = 0
        if debugMode:
            print "*"*50
            print sql_statement

        for datarow in mining_data:
            mCur = conn.cursor()
            print ''
            print "=-=" * 50
            print 'NewMineID:', datarow[0]

            mines = \
            {          'Mine id': [],
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
            mine_data = {
                'resources' : {
                     0: {
                         'raw': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''},
                         'tot': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''}
                     }
                 },
                'reserves'  : {
                    0: {
                        'raw': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''},
                        'tot': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''}
                    }                  },
                'capacity'  : {
                    0: {
                        'raw': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''},
                        'rom': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''}
                    }                  },
                'production': {
                    0: {
                        'raw': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''},
                        'rom': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''}
                    }                }
            }

            error_log = []
            error_log.append([])
            error_log[0].append('Mine id')
            error_log.append([])
            error_log[1].append('Period')
            error_log.append([])
            error_log[2].append('Comment')
            error_log.append([])
            error_log[3].append('Session_key')
            error_log.append([])
            error_log[4].append('Error type')
            error_log.append([])
            error_log[5].append('Error Param')
            error_log.append([])
            error_log[6].append('Error Value')
            #
            #%^ determine function of each boolean variable
            firstType1           = False
            firstType2           = False
            firstType3           = False
            #pt_ran              = False
            octr_ran             = False
            rr_ran               = False
            thisWasModelled      = True
            store_unit_type      = False
            #
            productionFound      = False
            romProductionFound   = False
            metalProductionFound = False
            oreProductionFound   = False
            overburdenFound      = False
            saleProductionFound  = False

            resourcesFound       = False
            totalResourcesFound  = False
            measResourcesFound   = False
            indResourcesFound    = False
            infResourcesFound    = False
            metalResourcesFound  = False

            capacityFound        = False
            romCapacityFound     = False
            metalCapacityFound   = False
            oreCapacityFound     = False
            saleCapacityFound    = False

            reservesFound        = False
            totalReservesFound   = False
            provReservesFound    = False
            probReservesFound    = False
            metalReservesFound   = False
            #
            maxProduction        = 0
            peakProduction       = 0
            #
            mine_prod            = {}
            srcd_prod            = {}
            hist_prod            = {}
            fcst_prod            = {}
            #
            metal_comm = ''
            mCommodities = datarow[10]
            last_data = {
                    'capacity': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
                'rom_capacity': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
                'ore_capacity': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
               'sale_capacity': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
              'metal_capacity': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},

                    'reserves': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
                'tot_reserves': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
               'prob_reserves': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
               'prov_reserves': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
              'metal_reserves': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},

                   'resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
               'tot_resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
              'meas_resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
               'ind_resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
               'inf_resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
             'metal_resources': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},

                  'production': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
              'rom_production': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
            'metal_production': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
              'ore_production': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
             'sale_production': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
                  'overburden': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''}
            }
            #
            first_data = {
                'capacity'  : {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
                'reserves'  : {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
                'resources' : {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''},
                'production': {'type': '', 'commodity': '', 'year': 0, 'value': 0, 'unit': ''}
            }
            #
            first_reserve_type = ""
            first_reserve_year = 0
            first_reserve_amt = 0
            first_reserve_unit = ""
            #
            first_capacity_type = ""
            first_capacity_year = 0
            first_capacity_amt = 0
            first_capacity_unit = ""
            first_ore_cap = 0
            #
            last_reserve_type = ""
            last_reserve_year = 0
            last_reserve_amt = 0
            last_reserve_unit = ""
            #
            last_capacity_type = ""
            last_capacity_year = 0
            last_capacity_amt = 0
            last_capacity_unit = ""
            last_ore_cap = 0
            #
            last_ore_type = ""
            last_ore_year = 0
            last_ore_cap = 0
            last_ore_unit = ""
            #
            lastHistProdYear = 0
            max_additional_production = 20
            #
            NewMineId = int(datarow[0])
            if datarow[28]:
                Mineid = int(datarow[28])
            else:
                Mineid = mine_ID
            mineStatus = datarow[1]
            if debugMode:
                print ''
                print 'mines:', mines

            if mineStatus.upper() == "OPERATION" and eval(otherFilter):
                if debugMode:
                    print datarow
                convertFactor = float(1)
                #
                mTotalProduction                = 0

                total_mine_prod                 = 0
                total_hist_prod                 = 0
                total_srcd_prod                 = 0
                total_fcst_prod                 = 0
                #
                total_rem_reserves              = 0
                total_rec_reserves              = 0

                # Store the data
                mineStage                       = datarow[1]
                #
                startYear                       = datarow[2]
                ActualProductionStartYear       = datarow[2]
                #
                mineLife                        = datarow[3]
                totalMineLife                   = datarow[3]
                #
                remainingLife                   = datarow[4]
                remainingMineLife               = datarow[4]
                #
                acreage                         = datarow[5]
                MineAcreageHectares             = datarow[5]
                #
                mineName                        = datarow[6]
                mineCountry                     = datarow[7]
                state                           = datarow[8]
                mineRegion                      = datarow[9]
                commodities                     = datarow[10]
                mineType                        = datarow[11]
                mineMethod                      = datarow[12]
                projectType                     = datarow[13]
                mineSubStage                    = datarow[14]
                mineSubStageStatus              = datarow[15]
                constructionStartYear           = datarow[16]
                mineEndYear                     = datarow[17]
                mineDepth                       = datarow[18]
                mineLocationSource              = datarow[19]
                remainingMineLifeYear           = datarow[20]
                originalProductionStartYear     = datarow[21]
                TotalMineLifeSource             = datarow[22]
                RemainingMineLifeSource         = datarow[23]
                MineEndYearSource               = datarow[24]
                mineAcreageSource               = datarow[25]
                ActualProductionStartYearSource = datarow[26]

                estimated_total_recoverable_reserves = 0

                firstMineYear = int(discountYear - 10)
                if MineAcreageHectares:
                    mComment = "MINE ACREAGE PROVIDED WITHOUT SOURCE"
                    error_log[0].append(NewMineId)
                    error_log[1].append(0)
                    error_log[2].append(mComment)
                    error_log[3].append(mSession_key)
                    error_log[4].append("ERROR TYPE 31")
                    error_log[5].append("")
                    error_log[6].append(MineAcreageHectares)
                #
                if mineAcreageSource is None:
                    mineAcreageSource = ""

                #if mineAcreageSource.count("EST:") > 0 or mineAcreageSource.upper().count("ESTIMATI") > 0:
                if "EST:" in mineAcreageSource or "ESTIMATI" in mineAcreageSource.upper():
                    MineAcreageHectares = 0
                    mineAcreageSource = ""
                param_vals = (NewMineId, Mineid, mineName, mineCountry, mineRegion,mSession_key)

                if updateParamTrk:
                    mCur.execute('INSERT INTO mining_param_track (NewMineId, MineId, mineName, mineCountry, mineRegion, sessionKey) VALUES (%s, %s, %s, %s, %s, %s)', param_vals)
                    mCur.execute('COMMIT')


                mines['Mine id'].append(NewMineId)
                mines['Start year'].append(startYear)
                mines['Mine life'].append(mineLife)
                mines['Remaining life'].append(remainingLife)
                mines['Acreage'].append(acreage)

                if debugMode:
                    print "-"*40
                    print "Session key: " + str(mSession_key)
                    print "ID: " + str(NewMineId), pws("- Start Year: " + str(startYear),18), pws("- Mine Life: " + str(mineLife),18,'R'), pws("- Remaining: "+ str(remainingLife),18,'R'), pws("- Acreage: " + str(acreage),18,'R')," - Commodities: " + mCommodities

                # -------------------------------------------------------------------------------------------------------------
                # EQUITY
                #
                if debugMode:
                    print 'Processing equity data ...'
                mOperators = ""

                mCFields = 'newMineId, mineName, operatorType, equityCompany, operatorBeginningYear  '

                sql_statement  = 'SELECT %s FROM %sMining_Operator_daily ' % (mCFields, prefixDB)
                sql_statement += 'WHERE newmineId = %s ORDER BY operatorBeginningYear DESC ' % NewMineId
                mCur5 = conn.cursor()
                mCur5.execute(sql_statement)
                Res5 = mCur5.fetchall()
                #
                firstTime = True
                oneFound = False
                lastYear = 0
                for datarow5 in Res5:
                    if not oneFound:
                        operatorType = datarow5[2]
                        if  datarow5[3] is None:
                           equityCompany = ""
                        else:
                            equityCompany = datarow5[3]
                        mOperators = equityCompany
                        operatorBeginningYear = datarow5[4]
                        if debugMode:
                            print ""
                            print " ** OPERATOR ** " + mOperators
                            print ""
                        oneFound = True
                # parse each commodity
                commod_list = []
                temp_commod = mCommodities
                num_commod = mCommodities.count(";")
                begin = 0
                for ii in range(num_commod):
                    pos = temp_commod.index(";")
                    commod_list.append(temp_commod[0:pos])
                    temp_commod = temp_commod[pos+1:]
                if debugMode:
                    print 'commod_list, len(commod_list):', commod_list,len(commod_list)
                # =======================================================
                # Add to the dictionary if it is not already there
                # - Also set up the modelled not modelled by commodity
                # modelled, not_modelled
                # ==========================================================
                if len(commod_list) == 1:
                    key = commod_list[ii]
                else:
                    key = "Multi Commodity"
                key_commodity = key
                if key in all_commodities:
                    all_commodities[key_commodity] += 1
                else:
                    all_commodities[key_commodity] = 1
                    not_modelled_commod[key_commodity] = 0
                    modelled_commod[key_commodity] = 0

                if debugMode:
                    print 'all_commodities:', all_commodities

                # Remember 'MTPA' = is metric tonnes per annum
                # Look for the 'BASE_UNIT' in the model rules table
                extraWhere = ""
                extraVars = ""
                baseU = ""
                if debugMode:
                    print "$" * 30
                    print "BASE UNIT (equity)"
                    print 'baseU:', baseU
                if baseU == "" or len(baseU.strip()) == 0:
                    mComment = "BASE UNIT NOT FOUND FOR COMMODITY " + commodities
                    '''
                    error_log[0].append(int(NewMineId))
                    error_log[1].append(0)
                    error_log[2].append(mComment)
                    error_log[3].append(mSession_key)
                    error_log[4].append("ERROR TYPE 19")
                    error_log[5].append("")
                    error_log[6].append(0)
                    '''
                    baseU  = "MMT"
                    if debugMode:
                        print '!*' * 50
                        print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                        print ''

                # -------------------------------------------------------------------------------------------------------------
                # RESERVES
                #
                if debugMode:
                    print 'Processing reserves data ...'
                    print ''
                reserves_data = ()
                total_reserves_data = ()
                prob_reserves_data = ()
                prov_reserves_data = ()
                metal_reserves_data = ()

                asset_datatypes = get_asset_datatypes(mCur,NewMineId,'reserves')
                if debugMode:
                    print 'reserves:', asset_datatypes
                if asset_datatypes:
                    if 'Total Reserves' in asset_datatypes:
                        total_reserves_data = get_asset_data(mCur, NewMineId, 'reserves', 'Total Reserves')
                        reserves_data = total_reserves_data
                        totalReservesFound = True
                        reservesFound = True
                    else:
                        if 'Probable Reserves' in asset_datatypes:
                            prob_reserves_data = get_asset_data(mCur, NewMineId, 'reserves', 'Probable Reserves')
                            reserves_data = prob_reserves_data
                            probReservesFound = True
                            reservesFound = True
                        else:
                            if 'Proved Reserves' in asset_datatypes:
                                prov_reserves_data = get_asset_data(mCur, NewMineId, 'reserves', 'Proved Reserves')
                                reserves_data = prov_reserves_data
                                provReservesFound = True
                                reservesFound = True
                            else:
                                if 'Pure Metal Total Reserves' in asset_datatypes:
                                    metal_reserves_data = get_asset_data(mCur, NewMineId, 'reserves', 'Pure Metal Total Reserves')
                                    metal_comm = get_metal_commodity(mCur, NewMineId, 'reserves')
                                    reserves_data = [data for data in metal_reserves_data if data[2] == metal_comm]
                                    metalReservesFound = True
                                    reservesFound = True

                first_reserves_data = True
                for datarow in reserves_data:
                    reservesFound    = True
                    reserveType      = datarow[1]
                    reserveCommodity = datarow[2]
                    reserves         = datarow[3]
                    reserveYear      = datarow[4]
                    reserveUnit      = datarow[5]
                    reserveSource    = datarow[6]
                    reserves = float(reserves)
                    if baseU == reserveUnit:
                        if debugMode or debugReserves:
                            print "BASE U = reserveUnit"
                            pass
                    elif baseU == "MMT" and reserveUnit == "MTPA":
                        if debugMode or debugReserves:
                            print "MMT = MTPA #########"
                            pass
                    else:
                        # convert
                        beforeUnit = reserveUnit
                        convertFactor = mining_units(mCur,reserveUnit,baseU,True)
                        reserveUnit = baseU
                        reserves  =  float(reserves) * float(convertFactor)
                        if debugMode or debugReserves:
                            print "-=-"*25
                            print
                            #print 'Original reserves: %s' % (float(reserves)/float(convertFactor))
                            print 'From reserve unit %s to base unit %s' % (beforeUnit, baseU)
                            print "1: Conversion Factor"
                            print 'convertFactor:', convertFactor
                            print 'Converted reserves: %s' % reserves
                    if convertFactor == 0:
                        mComment = "CONVERSION FACTOR FROM " + reserveUnit + " TO " + baseU + " NOT FOUND "
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 12")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''
                    else:
                        convertFactor = float(convertFactor)

                    if totalReservesFound:
                        if debugMode:
                            print 'Total Reserves Found'
                        last_data['tot_reserves']['type'] = reserveType
                        last_data['tot_reserves']['commodity'] = reserveCommodity
                        last_data['tot_reserves']['year'] = reserveYear
                        last_data['tot_reserves']['value'] = reserves
                        last_data['tot_reserves']['unit'] = reserveUnit
                    elif probReservesFound:
                        if debugMode:
                            print 'Probable Reserves Found'
                        last_data['prob_reserves']['type'] = reserveType
                        last_data['prob_reserves']['commodity'] = reserveCommodity
                        last_data['prob_reserves']['year'] = reserveYear
                        last_data['prob_reserves']['value'] = reserves
                        last_data['prob_reserves']['unit'] = reserveUnit
                        
                        reserves = convert_to_total(curr, 'reserves', 'probable', last_data['prob_reserves'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key)
                        reserveType = "Total Reserves"
                        reserveSource = "EST: Engine Estimation"
                    elif provReservesFound:
                        if debugMode:
                            print 'Proved Reserves Found'
                        last_data['prov_reserves']['type'] = reserveType
                        last_data['prov_reserves']['commodity'] = reserveCommodity
                        last_data['prov_reserves']['year'] = reserveYear
                        last_data['prov_reserves']['value'] = reserves
                        last_data['prov_reserves']['unit'] = reserveUnit

                        reserves = convert_to_total(curr, 'reserves', 'proved', last_data['prov_reserves'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key)
                        reserveType = "Total Reserves"
                        reserveSource = "EST: Engine Estimation"
                    elif metalReservesFound:
                        if debugMode:
                            print 'Metal Reserves Found'
                        last_data['metal_reserves']['type'] = reserveType
                        last_data['metal_reserves']['commodity'] = reserveCommodity
                        last_data['metal_reserves']['year'] = reserveYear
                        last_data['metal_reserves']['value'] = reserves
                        last_data['metal_reserves']['unit'] = reserveUnit

                        reserves = convert_to_total(curr, 'reserves', 'metal', last_data['metal_reserves'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key)
                        reserveType = "Total Reserves"
                        reserveSource = "EST: Engine Estimation"

                    mines['Reserve type'].append(reserveType)
                    mines['Reserve year'].append(reserveYear)
                    mines['Reserves'].append(float(reserves))
                    mines['Reserve unit'].append(reserveUnit)
                    mines['Reserves Source'].append(reserveSource)

                    last_data['reserves']['type']      = reserveType
                    last_data['reserves']['commodity'] = reserveCommodity
                    last_data['reserves']['year']      = reserveYear
                    last_data['reserves']['value']     = float(reserves)
                    last_data['reserves']['unit']      = reserveUnit

                    last_reserve_type = reserveType
                    last_reserve_year = reserveYear
                    last_reserve_amt  = float(reserves)
                    last_reserve_unit = reserveUnit

                    if first_reserves_data:
                        first_reserve_type = reserveType
                        first_reserve_year = reserveYear
                        first_reserve_amt  = float(reserves)
                        first_reserve_unit = reserveUnit
                        first_data['reserves']['type'] = reserveType
                        first_data['reserves']['commodity'] = reserveCommodity
                        first_data['reserves']['year'] = reserveYear
                        first_data['reserves']['value'] = float(reserves)
                        first_data['reserves']['unit'] = reserveUnit
                        first_reserves_data = False

                    if debugMode or debugReserves:
                        print "RESERVES (NewMineId,reserveType,reserveYear,reserves,reserveUnit)------>", NewMineId, reserveType, reserveYear, reserves, reserveUnit
                        print ''
                        print '%s added to %s list' % (reserveType, "mines['Reserve type']")
                        print '%s added to %s list' % (reserveYear, "mines['Reserve year']")
                        print '%s added to %s list' % (reserves, "mines['Reserves']")
                        print '%s added to %s list' % (reserveUnit, "mines['Reserve unit']")
                        print '%s added to %s list' % (reserveSource, "mines['Reserves Source']")

                last_reserve_type = last_data['reserves']['type']
                last_reserve_year = last_data['reserves']['year']
                last_reserve_amt  = last_data['reserves']['value']
                last_reserve_unit = last_data['reserves']['unit']

                if updateParamTrk:
                    if totalReservesFound:
                        last_resv = last_data['tot_reserves']
                        param_vals = (last_resv['type'], last_resv['commodity'], last_resv['year'], last_resv['value'], last_resv['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastReservesType=%s,lastReservesComm=%s,lastReservesYear=%s,lastReservesVal=%s,lastReservesUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')
                    elif probReservesFound:
                        last_resv = last_data['prob_reserves']
                        param_vals = (last_resv['type'], last_resv['commodity'], last_resv['year'], last_resv['value'], last_resv['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastReservesType=%s,lastReservesComm=%s,lastReservesYear=%s,lastReservesVal=%s,lastReservesUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')
                    elif provReservesFound:
                        last_resv = last_data['prov_reserves']
                        param_vals = (last_resv['type'], last_resv['commodity'], last_resv['year'], last_resv['value'], last_resv['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastReservesType=%s,lastReservesComm=%s,lastReservesYear=%s,lastReservesVal=%s,lastReservesUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update, param_vals)
                        mCur.execute('COMMIT')
                    elif metalReservesFound:
                        last_resv = last_data['metal_reserves']
                        param_vals = (last_resv['type'], last_resv['commodity'], last_resv['year'], last_resv['value'], last_resv['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastReservesType=%s,lastReservesComm=%s,lastReservesYear=%s,lastReservesVal=%s,lastReservesUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')

                # -------------------------------------------------------------------------------------------------------------
                # CAPACITY
                #
                if debugMode:
                    print 'Processing capacity data ...'
                    print ''
                cap_recov_factor = None
                cap_ore_grade    = None

                capacity_data  = ()
                rom_cap_data   = ()
                sale_cap_data  = ()
                ore_cap_data   = ()
                metal_cap_data = ()

                asset_datatypes = get_asset_datatypes(mCur, NewMineId, 'capacity')
                if asset_datatypes:
                    if 'ROM Capacity' in asset_datatypes:
                        rom_cap_data = get_asset_data(curr, NewMineId, 'capacity', 'ROM Capacity')
                        capacity_data = rom_cap_data
                        romCapacityFound = True
                        capacityFound = True
                    else:
                        if 'Saleable Capacity' in asset_datatypes:
                            sale_cap_data = get_asset_data(curr, NewMineId, 'capacity', 'Saleable Capacity')
                            saleable_comm = get_saleable_commodity(curr, NewMineId, 'capacity')
                            capacity_data = [data for data in sale_cap_data if data[2] == saleable_comm]
                            saleCapacityFound = True
                            capacityFound = True
                        else:
                            if 'Ore Processed Capacity' in asset_datatypes:
                                ore_cap_data = get_asset_data(curr, NewMineId, 'capacity', 'Ore Processed Capacity')
                                capacity_data = ore_cap_data
                                oreCapacityFound = True
                                capacityFound = True
                            else:
                                if 'Metal Capacity' in asset_datatypes:
                                    metal_cap_data = get_asset_data(curr, NewMineId, 'capacity', 'Metal Capacity')
                                    metal_comm = get_metal_commodity(curr, NewMineId, 'capacity')
                                    cap_recov_factor = float(get_recov_factor(mCur, NewMineId, metal_comm, mOperators))
                                    capacity_data = [data for data in metal_cap_data if data[2] == metal_comm]
                                    metalCapacityFound = True
                                    capacityFound = True

                first_capacity_data = True
                for datarow in capacity_data:
                    capacityType, capacityCommodity, capacityValue, capacityYear, capacityUnit, capacitySource = datarow[1:]
                    capacityValue = float(capacityValue)

                    mine_data['capacity'][int(capacityYear)] = {
                         'raw': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''},
                         'rom': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''}
                    }
                    capacity_data = mine_data['capacity'][int(capacityYear)]

                    capacity_data['raw']['type']      = capacityType
                    capacity_data['raw']['commodity'] = capacityCommodity
                    capacity_data['raw']['value']     = capacityValue
                    capacity_data['raw']['unit']      = capacityUnit
                    capacity_data['raw']['source']    = capacitySource[:25]

                    if debugMode:
                        print "-=-" * 25
                        print ''
                        print "mine_data['capacity'][{}]['value']: {}".format(int(capacityYear), capacityValue)

                    if baseU == capacityUnit:
                        convertFactor = 1.0
                        capacityValue = float(capacityValue)
                        if debugMode:
                            print "BASE U = capacityUnit"
                    elif baseU == "MMT" and capacityUnit == "MTPA":
                        convertFactor = 1.0
                        capacityValue = float(capacityValue)
                        if debugMode:
                            print "MMT = MTPA #########"
                    else:
                        beforeUnit = capacityUnit
                        convertFactor = float(mining_units(mCur,capacityUnit,baseU,True))
                        capacityUnit = baseU
                        capacityValue = float(capacityValue * convertFactor)
                        if debugMode:
                            print 'From capacity unit %s to base unit %s' % (beforeUnit, baseU)
                            print "2: Conversion Factor"
                            print 'convertFactor:', convertFactor
                            print 'Converted capacity: %s' % capacityValue

                    if convertFactor == 0:
                        mComment = "CONVERSION FACTOR FROM " + capacityUnit + " TO " + baseU + " NOT FOUND "
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 12")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''

                    #capacityValue *= convertFactor
                    #capacityValue = float(capacityValue)
                    #
                    if debugMode:
                        print 'capacityType:', capacityType
                        print 'capacityYear:', capacityYear
                        print 'capacityValue:', capacityValue
                        print 'convertFactor:', convertFactor
                        print 'capacityUnit:', capacityUnit
                        print "mine_data['capacity'][{}]['value']: {}".format(int(capacityYear), capacityValue)
                        print ''
                    if romCapacityFound:
                        if debugMode:
                            print 'ROM Capacity Found'
                        last_data['rom_capacity']['type'] = capacityType
                        last_data['rom_capacity']['year'] = capacityYear
                        last_data['rom_capacity']['value'] = capacityValue
                        last_data['rom_capacity']['unit'] = capacityUnit
                    elif saleCapacityFound:
                        if debugMode:
                            print 'Saleable Capacity Found'
                        last_data['sale_capacity']['type'] = capacityType
                        last_data['sale_capacity']['commodity'] = capacityCommodity
                        last_data['sale_capacity']['year'] = capacityYear
                        last_data['sale_capacity']['value'] = capacityValue
                        last_data['sale_capacity']['unit'] = capacityUnit
                        capacityValue = convert_to_rom(mCur, 'capacity', 'sale', last_data['sale_capacity'], NewMineId, mineCountry, mineRegion, mineStatus, mineType, mineMethod, mOperators, mSession_key, debug=debugMode)
                        capacityType = 'ROM Capacity'
                        capacitySource = 'EST: Engine Estimation'
                    elif oreCapacityFound:
                        if debugMode:
                            print 'Ore Processed Capacity Found'
                        last_data['ore_capacity']['type']  = capacityType
                        last_data['ore_capacity']['year']  = capacityYear
                        last_data['ore_capacity']['value'] = capacityValue
                        last_data['ore_capacity']['unit']  = capacityUnit
                        capacityValue = convert_to_rom(mCur, 'capacity', 'ore', last_data['ore_capacity'], NewMineId, mineCountry, mineRegion, mineStatus, mineType, mineMethod, mOperators, mSession_key, debug=debugMode)
                        capacityType = 'ROM Capacity'
                        capacitySource = 'EST: Engine Estimation'
                    elif metalCapacityFound:
                        if debugMode:
                            print 'Metal Capacity Found'
                        last_data['metal_capacity']['type'] = capacityType
                        last_data['metal_capacity']['commodity'] = capacityCommodity
                        last_data['metal_capacity']['year'] = capacityYear
                        last_data['metal_capacity']['value'] = capacityValue
                        last_data['metal_capacity']['unit'] = capacityUnit
                        capacityValue = convert_to_rom(mCur, 'capacity', 'metal', last_data['metal_capacity'], NewMineId, mineCountry, mineRegion, mineStatus, mineType, mineMethod, mOperators, mSession_key, recov_factor=cap_recov_factor, debug=debugMode)
                        capacityType = 'ROM Capacity'
                        capacitySource = 'EST: Engine Estimation'

                    mines['Capacity type'].append(capacityType)
                    mines['Capacity year'].append(capacityYear)
                    mines['Capacity'].append(float(capacityValue))
                    mines['Capacity unit'].append(capacityUnit)
                    mines['Capacity Source'].append(capacitySource)

                    capacity_data['rom']['type']      = capacityType
                    capacity_data['rom']['commodity'] = capacityCommodity
                    capacity_data['rom']['value']     = capacityValue
                    capacity_data['rom']['unit']      = capacityUnit
                    capacity_data['rom']['source']    = capacitySource[:25]

                    last_capacity_type = capacityType
                    last_capacity_year = capacityYear
                    last_capacity_amt  = float(capacityValue)
                    last_capacity_unit = capacityUnit

                    last_data['capacity']['type']  = capacityType
                    last_data['capacity']['year']  = capacityYear
                    last_data['capacity']['value'] = float(capacityValue)
                    last_data['capacity']['unit']  = capacityUnit

                    if first_capacity_data:
                        first_capacity_type = capacityType
                        first_capacity_year = capacityYear
                        first_capacity_amt = float(capacityValue)
                        first_capacity_unit = capacityUnit

                        first_data['capacity']['type'] = capacityType
                        first_data['capacity']['year'] = capacityYear
                        first_data['capacity']['value'] = float(capacityValue)
                        first_data['capacity']['unit'] = capacityUnit
                        first_capacity_data = False

                if updateParamTrk:
                    if romCapacityFound:
                        last_cap = last_data['rom_capacity']
                        param_vals = (last_cap['type'], last_cap['commodity'], last_cap['year'], last_cap['value'], last_cap['unit'], NewMineId, mSession_key)
                        mCur.execute('UPDATE mining_param_track SET lastCapacityType=%s,lastCapacityComm=%s,lastCapacityYear=%s,lastCapacityVal=%s,lastCapacityUnit=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
                        commit(mCur)
                    elif saleCapacityFound:
                        last_cap = last_data['sale_capacity']
                        param_vals = (last_cap['type'], last_cap['commodity'], last_cap['year'], last_cap['value'], last_cap['unit'], NewMineId, mSession_key)
                        mCur.execute('UPDATE mining_param_track SET lastCapacityType=%s,lastCapacityComm=%s,lastCapacityYear=%s,lastCapacityVal=%s,lastCapacityUnit=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
                        commit(mCur)
                    elif oreCapacityFound:
                        last_cap = last_data['ore_capacity']
                        param_vals = (last_cap['type'], last_cap['commodity'], last_cap['year'], last_cap['value'], last_cap['unit'], NewMineId, mSession_key)
                        mCur.execute('UPDATE mining_param_track SET lastCapacityType=%s,lastCapacityComm=%s,lastCapacityYear=%s,lastCapacityVal=%s,lastCapacityUnit=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
                        commit(mCur)
                    elif metalCapacityFound:
                        last_cap = last_data['metal_capacity']
                        param_vals = (last_cap['type'], last_cap['commodity'], last_cap['year'], last_cap['value'], last_cap['unit'], NewMineId, mSession_key)
                        mCur.execute('UPDATE mining_param_track SET lastCapacityType=%s,lastCapacityComm=%s,lastCapacityYear=%s,lastCapacityVal=%s,lastCapacityUnit=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
                        commit(mCur)

                # get the capacity info for the last year
                if debugMode:
                    print ''
                    print 'CAPACITY:'
                    print '(NewMineId,last_capacity_type,last_capacity_year,last_capacity_amt,last_capacity_unit):', NewMineId,last_capacity_type,last_capacity_year,last_capacity_amt,last_capacity_unit
                    for cap_year in sorted(mine_data['capacity'].keys()):
                        print '{}(raw): {}'.format(cap_year, mine_data['capacity'][cap_year]['raw'])
                        print '{}(rom): {}'.format(cap_year, mine_data['capacity'][cap_year]['rom'])

                # -------------------------------------------------------------------------------------------------------------
                # RESOURCE
                #
                if debugMode:
                    print 'Processing resource data ...'
                    print ''
                resource_data = ()
                total_resource_data = ()
                meas_resource_data = ()
                ind_resource_data = ()
                inf_resource_data = ()
                metal_resource_data = ()

                asset_datatypes = get_asset_datatypes(mCur, NewMineId, 'resource')
                if asset_datatypes:
                    if 'Total Resources' in asset_datatypes:
                        total_resource_data = get_asset_data(mCur, NewMineId, 'resource', 'Total Resources')
                        resource_data = total_resource_data
                        totalResourcesFound = True
                        resourcesFound = True
                    else:
                        if 'Measured Resources' in asset_datatypes:
                            meas_resource_data = get_asset_data(mCur, NewMineId, 'resource', 'Measured Resources')
                            resource_data = meas_resource_data
                            measResourcesFound = True
                            resourcesFound = True
                        else:
                            if 'Indicated Resources' in asset_datatypes:
                                ind_resource_data = get_asset_data(mCur, NewMineId, 'resource', 'Indicated Resources')
                                resource_data = ind_resource_data
                                indResourcesFound = True
                                resourcesFound = True
                            else:
                                if 'Inferred Resources' in asset_datatypes:
                                    inf_resource_data = get_asset_data(mCur, NewMineId, 'resource', 'Inferred Resources')
                                    resource_data = inf_resource_data
                                    infResourcesFound = True
                                    resourcesFound = True
                                else:
                                    if 'Total Pure Metal Resources' in asset_datatypes:
                                        metal_resource_data = get_asset_data(mCur, NewMineId, 'resource', 'Total Pure Metal Resources')
                                        metal_comm = get_metal_commodity(mCur, NewMineId, 'resource')
                                        resource_data = [data for data in metal_resource_data if data[2] == metal_comm]
                                        metalResourcesFound = True
                                        resourcesFound = True

                lastYear = 0
                first_resource_data = True
                for datarow in resource_data:
                    resourcesFound = True
                    resourceType         = datarow[1]
                    resourceCommodity    = datarow[2]
                    resource             = datarow[3]
                    resourceYear         = datarow[4]
                    resourceUnit         = datarow[5]
                    resourceSource       = datarow[6]

                    if resource is None or len(str(resource).strip()) == 0:
                        resource = 0
                        # flag as an error
                        mComment = "INVALID DATA - RESOURCE IS BLANK"
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 16")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''
                    resource = float(resource)
                    lastYear = resourceYear
                    if debugMode:
                        print "-=-" * 25
                        print "Resource: " + str(resource)
                    if baseU == resourceUnit:
                        if debugMode:
                            print "BASE U = resourceUnit"
                            pass
                    elif baseU == "MMT" and resourceUnit == "MTPA":
                        # equivalent
                        if debugMode:
                            print "MMT = MTPA #########"
                            pass
                    else:
                        # convert
                        convertFactor = 1
                        convertFactor = mining_units(mCur,resourceUnit,baseU,True)
                        beforeUnit = resourceUnit
                        resourceUnit = baseU
                        resource = float(resource) * float(convertFactor)
                        if debugMode:
                            print 'Original resource: %s' % (float(resource) / float(convertFactor))
                            print 'From resource unit %s to base unit %s' % (beforeUnit, baseU)
                            print "3: Conversion Factor"
                            print 'convertFactor:', convertFactor
                            print 'Converted resource: %s' % resource
                    # if convertFactor not found
                    # write to error log
                    if convertFactor == 0:
                        mComment = "CONVERSION FACTOR FROM " + resourceUnit + " TO " + baseU + " NOT FOUND "
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 12")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''
                    else:
                        convertFactor = 1
                        convertFactor = float(convertFactor)

                    if totalResourcesFound:
                        if debugMode:
                            print 'Total Resources Found'
                        last_data['tot_resources']['type'] = resourceType
                        last_data['tot_resources']['commodity'] = resourceCommodity
                        last_data['tot_resources']['year'] = resourceYear
                        last_data['tot_resources']['value'] = resource
                        last_data['tot_resources']['unit'] = resourceUnit

                    elif measResourcesFound:
                        if debugMode:
                            print 'Measured Resources Found'
                        last_data['meas_resources']['type'] = resourceType
                        last_data['meas_resources']['commodity'] = resourceCommodity
                        last_data['meas_resources']['year'] = resourceYear
                        last_data['meas_resources']['value'] = resource
                        last_data['meas_resources']['unit'] = resourceUnit

                        resource = convert_to_total(mCur, 'resource', 'measured', last_data['meas_resources'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key, debugMode)
                        resourceType = "Total Resources"
                        resourceSource = "EST: Engine Estimation"

                    elif indResourcesFound:
                        if debugMode:
                            print 'Indicated Resources Found'
                        last_data['ind_resources']['type'] = resourceType
                        last_data['ind_resources']['commodity'] = resourceCommodity
                        last_data['ind_resources']['year'] = resourceYear
                        last_data['ind_resources']['value'] = resource
                        last_data['ind_resources']['unit'] = resourceUnit

                        resource = convert_to_total(mCur, 'resource', 'indicated', last_data['ind_resources'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key, debugMode)
                        resourceType = "Total Resources"
                        resourceSource = "EST: Engine Estimation"

                    elif infResourcesFound:
                        if debugMode:
                            print 'Inferred Resources Found'
                        last_data['inf_resources']['type'] = resourceType
                        last_data['inf_resources']['commodity'] = resourceCommodity
                        last_data['inf_resources']['year'] = resourceYear
                        last_data['inf_resources']['value'] = resource
                        last_data['inf_resources']['unit'] = resourceUnit

                        resource = convert_to_total(mCur, 'resource', 'inferred', last_data['inf_resources'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key, debugMode)
                        resourceType = "Total Resources"
                        resourceSource = "EST: Engine Estimation"

                    elif metalResourcesFound:
                        if debugMode:
                            print 'Metal Resources Found'
                        last_data['metal_resources']['type'] = resourceType
                        last_data['metal_resources']['commodity'] = resourceCommodity
                        last_data['metal_resources']['year'] = resourceYear
                        last_data['metal_resources']['value'] = resource
                        last_data['metal_resources']['unit'] = resourceUnit
                        resource = convert_to_total(mCur, 'resource', 'metal', last_data['metal_resources'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key, debugMode)
                        resourceType = "Total Resources"
                        resourceSource = "EST: Engine Estimation"

                    mines['Resource Type'].append(resourceType)
                    mines['Commodity'].append(resourceCommodity)
                    mines['Resource Year'].append(resourceYear)
                    mines['Resource %'].append(float(resource))
                    mines['Resource unit'].append(resourceUnit)
                    mines['Resource Source'].append(resourceSource)

                    last_data['resources']['type'] = resourceType
                    last_data['resources']['commodity'] = resourceCommodity
                    last_data['resources']['year'] = resourceYear
                    last_data['resources']['value'] = float(resource)
                    last_data['resources']['unit'] = resourceUnit

                    if first_resource_data:
                        first_data['resources']['type'] = resourceType
                        first_data['resources']['commodity'] = resourceCommodity
                        first_data['resources']['year'] = resourceYear
                        first_data['resources']['value'] = float(resource)
                        first_data['resources']['unit'] = resourceUnit
                        first_resource_data = False
                if updateParamTrk:
                    if totalResourcesFound:
                        last_resc = last_data['tot_resources']
                        param_vals = (last_resc['type'], last_resc['commodity'], last_resc['year'], last_resc['value'], last_resc['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastResourceType=%s,lastResourceComm=%s,lastResourceYear=%s,lastResourceVal=%s,lastResourceUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')
                    elif measResourcesFound:
                        last_resc = last_data['meas_resources']
                        param_vals = (last_resc['type'], last_resc['commodity'], last_resc['year'], last_resc['value'], last_resc['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastResourceType=%s,lastResourceComm=%s,lastResourceYear=%s,lastResourceVal=%s,lastResourceUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')
                    elif indResourcesFound:
                        last_resc = last_data['ind_resources']
                        param_vals = (last_resc['type'], last_resc['commodity'], last_resc['year'], last_resc['value'], last_resc['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastResourceType=%s,lastResourceComm=%s,lastResourceYear=%s,lastResourceVal=%s,lastResourceUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')
                    elif infResourcesFound:
                        last_resc = last_data['inf_resources']
                        param_vals = (last_resc['type'], last_resc['commodity'], last_resc['year'], last_resc['value'], last_resc['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastResourceType=%s,lastResourceComm=%s,lastResourceYear=%s,lastResourceVal=%s,lastResourceUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')
                    elif metalResourcesFound:
                        last_resc = last_data['metal_resources']
                        param_vals = (last_resc['type'], last_resc['commodity'], last_resc['year'], last_resc['value'], last_resc['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastResourceType=%s,lastResourceComm=%s,lastResourceYear=%s,lastResourceVal=%s,lastResourceUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')

                # -------------------------------------------------------------------------------------------------------------
                # PRODUCTION
                #
                if debugMode:
                    print 'Processing production data ...'
                    print ''
                createdMetalProduction = False
                productionFound = False
                romProductionFound = False

                prod_ore_grade = None
                prod_recov_factor = None
                prod_data = ()
                sale_prod_data = ()
                overburden_data = ()
                ore_prod_data = ()
                metal_prod_data = ()

                asset_datatypes = get_asset_datatypes(mCur, NewMineId, 'production')
                if debugMode:
                    print 'production:', asset_datatypes
                if asset_datatypes:
                    if 'ROM Production' in asset_datatypes:
                        rom_prod_data = get_asset_data(curr, NewMineId, 'production', 'ROM Production')
                        prod_data = rom_prod_data
                        romProductionFound = True
                        productionFound = True
                    else:
                        if 'Saleable Production' in asset_datatypes:
                            sale_prod_data = get_asset_data(curr, NewMineId, 'production', 'Saleable Production')
                            saleable_comm = get_saleable_commodity(curr, NewMineId, 'production')
                            prod_data = [data for data in sale_prod_data if data[2] == saleable_comm]
                            saleProductionFound = True
                            productionFound = True
                        else:
                            if 'Overburden' in asset_datatypes and 0:
                                # overburden_data = get_asset_data(curr, NewMineId, 'production', 'Overburden')
                                prod_data = overburden_data
                                overburdenFound = True
                                productionFound = True
                            else:
                                if 'Ore milled/ processed'  in asset_datatypes:
                                    ore_prod_data = get_asset_data(curr, NewMineId, 'production', 'Ore milled/ processed')
                                    prod_data = ore_prod_data
                                    oreProductionFound = True
                                    productionFound = True
                                else:
                                    if 'Metal Production' in asset_datatypes:
                                        metal_prod_data = get_asset_data(curr, NewMineId, 'production', 'Metal Production')
                                        metal_comm = get_metal_commodity(curr, NewMineId, 'production')
                                        prod_recov_factor = float(get_recov_factor(mCur, NewMineId, metal_comm, mOperators))
                                        prod_data = [data for data in metal_prod_data if data[2] == metal_comm]
                                        metalProductionFound = True
                                        productionFound = True

                firstTime = True
                first_production_data = True
                for prod_datarow in prod_data:
                    productionType   = prod_datarow[1]
                    productCommodity = prod_datarow[2]
                    productionValue  = float(prod_datarow[3])
                    productionYear   = prod_datarow[4]
                    productionUnit   = prod_datarow[5]
                    productionSource = prod_datarow[6]

                    mine_data['production'][int(productionYear)] = {
                         'raw': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''},
                         'rom': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''}
                    }
                    production_data = mine_data['production'][int(productionYear)]

                    production_data['raw']['type']      = productionType
                    production_data['raw']['commodity'] = productCommodity
                    production_data['raw']['value']     = productionValue
                    production_data['raw']['unit']      = productionUnit
                    production_data['raw']['source']    = productionSource[:25]
                    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    # Convert productionValue from productionUnit to baseU ('MMT' by default)

                    if baseU == productionUnit:
                        convertFactor = 1.0
                        if debugMode:
                            print "BASE U = productionUnit"
                    elif baseU == "MMT" and productionUnit == "MTPA":
                        convertFactor = 1.0
                        if debugMode:
                            print "MMT = MTPA #########"
                    else:
                        convertFactor = float(mining_units(mCur,productionUnit,baseU,True))

                    if convertFactor == 0:
                        mComment = "CONVERSION FACTOR FROM " + productionUnit + " TO " + baseU + " NOT FOUND "
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 12")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''
                    else:
                        convertFactor = float(convertFactor)
                    beforeUnit = productionUnit
                    productionUnit = baseU
                    productionValue = float(productionValue) * float(convertFactor)
                    if debugMode:
                        print "-=-" * 25
                        print
                        print 'Production year: %s' % productionYear
                        if not metalProductionFound:
                            print 'From production unit %s to base unit %s' % (beforeUnit, baseU)
                            print "4: Conversion Factor"
                            print 'convertFactor             :', convertFactor
                            print 'Converted production      : %s' % productionValue
                        else:
                            print 'Metal Production unit     : %s' % production_data['raw']['unit']
                            print 'Metal Production          : %s' % production_data['raw']['value']
                            print 'Metal Production Commodity: %s' % productCommodity


                    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    # Convert all production data to ROM production in order from least to most granular
                    if romProductionFound:
                        if debugMode:
                            print 'ROM Production Found'
                        last_data['rom_production']['type'] = productionType
                        last_data['rom_production']['commodity'] = productCommodity
                        last_data['rom_production']['year'] = productionYear
                        last_data['rom_production']['value'] = productionValue
                        last_data['rom_production']['unit'] = productionUnit
                    elif saleProductionFound:
                        if debugMode:
                            print 'Saleable Production Found'
                        last_data['sale_production']['type'] = productionType
                        last_data['sale_production']['commodity'] = productCommodity
                        last_data['sale_production']['year'] = productionYear
                        last_data['sale_production']['value'] = productionValue
                        last_data['sale_production']['unit'] = productionUnit
                        productionValue = convert_to_rom(curr, 'production', 'sale', last_data['sale_production'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key, debug=debugMode)
                        productionType = "ROM Production"
                        productionSource = "EST: Engine Estimation"
                    elif overburdenFound:
                        if debugMode:
                            print 'Overburden Found'
                        last_data['overburden']['type'] = productionType
                        last_data['overburden']['commodity'] = productCommodity
                        last_data['overburden']['year'] = productionYear
                        last_data['overburden']['value'] = productionValue
                        last_data['overburden']['unit'] = productionUnit
                        productionValue = convert_to_rom(curr, 'production', 'overburden', last_data['overburden'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key, debug=debugMode)
                        productionType = "ROM Production"
                        productionSource = "EST: Engine Estimation"
                    elif oreProductionFound:
                        if debugMode:
                            print 'Ore Production Found'
                        last_data['ore_production']['type'] = productionType
                        last_data['ore_production']['commodity'] = productCommodity
                        last_data['ore_production']['year'] = productionYear
                        last_data['ore_production']['value'] = productionValue
                        last_data['ore_production']['unit'] = productionUnit
                        productionValue = convert_to_rom(curr, 'production', 'ore', last_data['ore_production'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key, debug=debugMode)
                        productionType = "ROM Production"
                        productionSource = "EST: Engine Estimation"
                    elif metalProductionFound:
                        if debugMode:
                            print 'Metal Production Found'
                        #last_data['metal_production']['type'] = productionType
                        #last_data['metal_production']['commodity'] = productCommodity
                        #last_data['metal_production']['year'] = productionYear
                        #last_data['metal_production']['value'] = productionValue
                        #last_data['metal_production']['unit'] = productionUnit
                        last_data['metal_production']['type']      = productionType
                        last_data['metal_production']['commodity'] = productCommodity
                        last_data['metal_production']['year']      = productionYear
                        last_data['metal_production']['value']     = production_data['raw']['value']
                        last_data['metal_production']['unit']      = production_data['raw']['unit']
                        productionValue = convert_to_rom(curr, 'production', 'metal', last_data['metal_production'], NewMineId, mineCountry, mineRegion, mineStage, mineType, mineMethod, mOperators, mSession_key, recov_factor=prod_recov_factor, debug=debugMode)
                        productionType = "ROM Production"
                        productionSource = "EST: Engine Estimation"

                    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    # Process ROM production data
                    if debugMode:
                        if len(mines['Production Value']) >= 1:
                            print ""
                            print "!!! ### **** PRODUCTION AVAILABLE "
                            print "!!! ### mines['Production Year']:", mines['Production Year']
                            print "!!! ### mines['Production Value']:", mines['Production Value']
                            print "!!! ### mines['Production unit']:", mines['Production unit']
                            print "!!! ### mines['Production Type']:", mines['Production Type']
                            print ""
                    if productionType == "ROM Production"  and len(productionSource.strip()) > 0:
                        productionFound = True
                        maxProduction   = max(productionValue,maxProduction)
                        peakProduction  = max(productionValue,peakProduction)

                        # Store cumulative production numbers but distinguish between production datatypes (total, historical, sourced, and forecasted)
                        mTotalProduction += float(productionValue)
                        #
                        total_mine_prod  += float(productionValue)
                        total_srcd_prod  += float(productionValue)
                        total_hist_prod  += float(productionValue)

                        # Store annual production numbers by production datatype
                        mine_prod[int(productionYear)] = float(productionValue)
                        srcd_prod[int(productionYear)] = float(productionValue)
                        hist_prod[int(productionYear)] = float(productionValue)

                        mines['Production Type'  ].append(productionType)
                        mines['Production Year'  ].append(productionYear)
                        mines['Production Value' ].append(float(productionValue))
                        mines['Production unit'  ].append(productionUnit)
                        mines['Production Source'].append(productionSource)

                        production_data['rom']['type'     ] = productionType
                        production_data['rom']['commodity'] = productCommodity
                        production_data['rom']['value'    ] = productionValue
                        production_data['rom']['unit'     ] = productionUnit
                        production_data['rom']['source'   ] = productionSource[:25]

                        last_data['production']['type'     ] = productionType
                        last_data['production']['commodity'] = productCommodity
                        last_data['production']['year'     ] = productionYear
                        last_data['production']['value'    ] = float(productionValue)
                        last_data['production']['unit'     ] = productionUnit

                        if first_production_data:
                            first_data['production']['type'     ] = productionType
                            first_data['production']['commodity'] = productCommodity
                            first_data['production']['year'     ] = productionYear
                            first_data['production']['value'    ] = float(productionValue)
                            first_data['production']['unit'     ] = productionUnit
                            first_production_data = False
                        if debugMode:
                            print 'maxProduction:', maxProduction
                            print "ROM Production -------->",mines['Production Type'][-1],mines['Production Year'][-1],mines['Production Value'][-1],mines['Production unit'][-1],mines['Production Source'][-1]

                        # CHECK for skipping of years
                        # CHECK for exceeding x% over ROM capacity
                        if len(mines['Production Value']) > 1:
                            # --------------------------------------------------------
                            # Get production tolerance -  production_tolerance
                            extraWhere = ""
                            extraVars = ""
                            yrs = mines['Production Year'][-1] - mines['Production Year'][-2]
                            if yrs > 1:
                                # year was skipped
                                fctr = (float(mines['Production Value'][-1]) - float(mines['Production Value'][-2]))/float(yrs)
                                pos = -2
                                for ii in range(yrs-1):
                                    productionSkipType  = mines['Production Type'][pos]
                                    productionSkipYear  = mines['Production Year'][pos] + 1
                                    productionSkipValue = float(mines['Production Value'][pos]) + fctr
                                    productionSkipUnit  = mines['Production unit'][pos]

                                    mine_data['production'][int(productionSkipYear)] = {
                                        'raw': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''},
                                        'rom': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''}
                                    }
                                    production_skip_data = mine_data['production'][int(productionSkipYear)]

                                    production_skip_data['raw']['type' ] = productionSkipType
                                    production_skip_data['raw']['value'] = productionSkipValue
                                    production_skip_data['raw']['unit' ] = productionSkipUnit

                                    if productionSkipUnit != 'MMT':
                                        convFactor = mining_units(mCur, productionSkipUnit, "MMT", True)
                                    else:
                                        convFactor = 1.0

                                    productionSkipValue *= convFactor
                                    productionSkipUnit = "MMT"

                                    #mines['Production Type'].append(productionSkipType)
                                    #mines['Production Year'].append(productionSkipYear)
                                    #mines['Production Value'].append(float(productionSkipValue))
                                    #mines['Production unit'].append(productionSkipUnit)
                                    #mines['Production Source'].append('EST: Forecast Engine')

                                    mines['Production Type'  ] = mines['Production Type'  ][:-1] + [productionSkipType]         + mines['Production Type'  ][-1:]
                                    mines['Production Year'  ] = mines['Production Year'  ][:-1] + [productionSkipYear]         + mines['Production Year'  ][-1:]
                                    mines['Production Value' ] = mines['Production Value' ][:-1] + [float(productionSkipValue)] + mines['Production Value' ][-1:]
                                    mines['Production unit'  ] = mines['Production unit'  ][:-1] + [productionSkipUnit]         + mines['Production unit'  ][-1:]
                                    mines['Production Source'] = mines['Production Source'][:-1] + ['EST: Forecast Engine']     + mines['Production Source'][-1:]

                                    maxProduction     = max(float(productionSkipValue),maxProduction)
                                    peakProduction    = max(float(productionSkipValue),peakProduction)
                                    mTotalProduction += float(productionSkipValue)

                                    total_mine_prod  += float(productionSkipValue)
                                    total_hist_prod  += float(productionSkipValue)

                                    mine_prod[int(productionSkipYear)] = float(productionSkipValue)
                                    hist_prod[int(productionSkipYear)] = float(productionSkipValue)

                                    production_skip_data['rom']['type'] = productionSkipType
                                    production_skip_data['rom']['value'] = productionSkipValue
                                    production_skip_data['rom']['unit'] = productionSkipUnit

                                    #pos += 1
                            if len(mines['Production Value']) > 1 and float(mines['Production Value'][-2]) > 0:
                                prod_change = abs((float(mines['Production Value'][-1]) - float(mines['Production Value'][-2])) / float(mines['Production Value'][-2]))
                                # Move up in code to yearly production data processing
                                if prod_change > 0.3 and (mines['Production Year'][-1] - mines['Production Year'][-2] == 1):
                                    mComment = "SOURCED PRODUCTION CHANGE OF GREATER THAN 30%"
                                    error_log[0].append(NewMineId)
                                    error_log[1].append(mines['Production Year'][-1])
                                    error_log[2].append(mComment)
                                    error_log[3].append(mSession_key)
                                    error_log[4].append("ERROR TYPE 28")
                                    error_log[5].append(mines['Production Value'][-2])
                                    error_log[6].append(mines['Production Value'][-1])

                            if last_capacity_amt > 0 and productionValue > last_capacity_amt:
                                if productionSource == "EST: Engine Estimation" and mines['Capacity Source'][-1] != "EST: Engine Estimation":
                                    mComment = "CONVERTED PRODUCTION VALUE EXCEEDS ROM CAPACITY"
                                    error_log[0].append(NewMineId)
                                    error_log[1].append(mines['Production Year'][-1])
                                    error_log[2].append(mComment)
                                    error_log[3].append(mSession_key)
                                    error_log[4].append("ERROR TYPE 32")
                                    error_log[5].append(last_capacity_amt)
                                    error_log[6].append(productionValue)
                            if int(productionYear) in mine_data['capacity'].keys() and mine_data['capacity'][int(productionYear)]['rom']['value'] < productionValue:
                                if debugMode:
                                    print ""
                                    print "PRODUCTION EXCEEDS ROM CAPACITY FOR YEAR {}".format(productionYear)
                                mComment = "PRODUCTION EXCEEDS ROM CAPACITY"
                                error_log[0].append(NewMineId)
                                error_log[1].append(productionYear)
                                error_log[2].append(mComment)
                                error_log[3].append(mSession_key)
                                error_log[4].append("ERROR TYPE 03")
                                error_log[5].append(str(mine_data['capacity'][int(productionYear)]['rom']['value']))
                                error_log[6].append(float(productionValue))
                                if debugMode:
                                    print '!*' * 50
                                    print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                                    print ''
                        if debugMode:
                            if firstTime and debugSQL:
                                print sql_statement
                                firstTime = False
                            if debugMode:
                                print "PRODUCTION------>",NewMineId,productionType,productionYear,productionValue,productionUnit,productCommodity
                if updateParamTrk:
                    if romProductionFound:
                        last_prod = last_data['rom_production']
                        param_vals = (last_prod['type'], last_prod['commodity'], last_prod['year'], last_prod['value'], last_prod['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastProductionType=%s,lastProductionComm=%s,lastProductionYear=%s,lastProductionVal=%s,lastProductionUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')
                    elif saleProductionFound:
                        last_prod = last_data['sale_production']
                        param_vals = (last_prod['type'], last_prod['commodity'], last_prod['year'], last_prod['value'], last_prod['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastProductionType=%s,lastProductionComm=%s,lastProductionYear=%s,lastProductionVal=%s,lastProductionUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')
                    elif overburdenFound:
                        last_prod = last_data['overburden']
                        param_vals = (last_prod['type'], last_prod['commodity'], last_prod['year'], last_prod['value'], last_prod['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastProductionType=%s,lastProductionComm=%s,lastProductionYear=%s,lastProductionVal=%s,lastProductionUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update, param_vals)
                        mCur.execute('COMMIT')
                    elif oreProductionFound:
                        last_prod = last_data['ore_production']
                        param_vals = (last_prod['type'], last_prod['commodity'], last_prod['year'], last_prod['value'], last_prod['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastProductionType=%s,lastProductionComm=%s,lastProductionYear=%s,lastProductionVal=%s,lastProductionUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update,param_vals)
                        mCur.execute('COMMIT')
                    elif metalProductionFound:
                        last_prod = last_data['metal_production']
                        param_vals = (last_prod['type'], last_prod['commodity'], last_prod['year'], last_prod['value'], last_prod['unit'],NewMineId, mSession_key)
                        sql_update = 'UPDATE mining_param_track SET lastProductionType=%s,lastProductionComm=%s,lastProductionYear=%s,lastProductionVal=%s,lastProductionUnit=%s WHERE NewMineId=%s AND sessionKey=%s'
                        mCur.execute(sql_update, param_vals)
                        mCur.execute('COMMIT')
                    if debugMode:
                        if len(mines['Production Value']) >= 1:
                            print ""
                            print "### **** PRODUCTION AVAILABLE "
                            print "### mines['Production Year']:", mines['Production Year']
                            print "### mines['Production Value']:", mines['Production Value']
                            print "### mines['Production unit']:", mines['Production unit']
                            print "### mines['Production Type']:", mines['Production Type']
                            print ""
                # ----------------------------------------------------------------------------------------------------------------------------
                if store_unit_type:
                    unitType = []
                    if len(mines['Reserve unit']):
                        if len(unitType) == 0 or unitType.count(mines['Reserve unit'][0]) == 0:
                            unitType.append(mines['Reserve unit'][0])
                        for i in range(len(mines['Reserve unit'])):
                            unit = mines['Reserve unit'][i]
                            if unitType.count(unit) == 0:
                                unitType.append(mines['Reserve unit'][i])
                                if debugMode or debugReserves:
                                    print "RESERVE MINE UNITS"
                                    print "@"*25
                                    print "mines['Reserve unit'][%s]:" % i, mines['Reserve unit'][i]
                    # ----------------------------------------
                    if len(mines['Capacity unit']):
                        if len(unitType) == 0 or unitType.count(mines['Capacity unit'][0]) == 0:
                            unitType.append(mines['Capacity unit'][0])
                        for i in range(len(mines['Capacity unit'])):
                            unit = mines['Capacity unit'][i]
                            if unitType.count(unit) == 0:
                                unitType.append(mines['Capacity unit'][i])
                                if debugMode:
                                    print "CAPACITY MINE UNITS"
                                    print "@"*25
                                    print "mines['Capacity unit'][%s]:" % i, mines['Capacity unit'][i]
                    # ----------------------------------------
                    if len(mines['Production unit']):
                        if len(unitType) == 0 or unitType.count(mines['Production unit'][0]) == 0:
                            unitType.append(mines['Production unit'][0])
                        for i in range(len(mines['Production unit'])):
                            unit = mines['Production unit'][i]
                            if unitType.count(unit) == 0:
                                unitType.append(mines['Production unit'][i])
                                if debugMode:
                                    print "PRODUCTION MINE UNITS"
                                    print "@"*25
                                    print "mines['Production unit'][%s]:" % i, mines['Production unit'][i]
                    # ----------------------------------------
                    if len(mines['Resource unit']):
                        if len(unitType) == 0 or unitType.count(mines['Resource unit'][0]) == 0:
                            unitType.append(mines['Resource unit'][0])
                        for i in range(len(mines['Resource unit'])):
                            unit = mines['Resource unit'][i]
                            if unitType.count(unit) == 0:
                                unitType.append(mines['Resource unit'][i])
                                if debugMode:
                                    print "RESOURCE MINE UNITS"
                                    print "@"*25
                                    print "mines['Resource unit'][%s]:" % i, mines['Resource unit'][i]
                    if debugMode:
                        print "-----------> UNITS: "
                        print 'unitType:', unitType
                        print 'baseU:', baseU
                        print ""
                    if unitType.count(baseU) == 0:
                        pass
                # -------------------------------------------------------------------------------------------------------------
                # Generate the missing values for the following tables
                # mining_capacity_daily
                # mining_resource_daily
                # mining_reserves_daily
                # mining_production_daily
                #
                if debugMode:
                    print 'productionFound: {}'.format(productionFound)
                    print 'capacityFound: {}'.format(capacityFound)
                    print 'reservesFound: {}'.format(reservesFound)
                    print 'resourcesFound: {}'.format(resourcesFound)
                    print ''

                if productionFound and capacityFound:
                    if mines['Production Year'][-1] == mines['Capacity year'][-1]:
                        lastHistProdYear = max(int(mines['Production Year'][-1]), lastHistProdYear)
                        if debugMode:
                            print ''
                            print '(1) lastHistProdYear: {}'.format(lastHistProdYear)
                            print ''
                        lastProdValue = mines['Production Value'][-1]
                        lastProdUnit  = mines['Production unit'][-1]
                        lastCapValue  = mines['Capacity'][-1]
                        lastCapUnit   = mines['Capacity unit'][-1]

                        if lastCapUnit == lastProdUnit:
                            convFactor = 1.0
                        else:
                            convFactor = float(mining_units(mCur, lastCapUnit, lastProdUnit, False))
                        lastCapValue *= convFactor

                        if lastProdValue < (lastCapValue*0.7):
                            mComment = "LAST PRODUCTION VALUE SIGNIFICANTLY LESS THAN LAST CAPACITY VALUE"
                            error_log[0].append(NewMineId)
                            error_log[1].append(mines['Production Year'][-1])
                            error_log[2].append(mComment)
                            error_log[3].append(mSession_key)
                            error_log[4].append("ERROR TYPE 24")
                            error_log[5].append(lastCapValue)
                            error_log[6].append(lastProdValue)
                if not reservesFound or not resourcesFound:
                    # -------------------------------------------------------------------
                    extraWhere = ""
                    extraVars = ""
                    rtr = get_param_detail(mCur,"RESOURCES_TO_RESERVES",NewMineId,mineCountry,mineRegion,mineStatus,mineType,mineMethod,key_commodity,mOperators,extraWhere,extraVars )
                    if debugMode or debugReserves:
                        print "$" * 30
                        print "RESOURCE TO RESERVES"
                        print 'rtr:', rtr
                    if rtr == 0 or len(rtr.strip()) == 0:
                        # use the default and trigger an error
                        mComment = "RESOURCES TO RESERVES RATIO NOT FOUND "
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 09")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''
                        resources_to_reserves  = .50
                    else:
                        resources_to_reserves  = float(rtr)
                    if updateParamTrk:
                        mCur.execute('UPDATE mining_param_track SET resourcesToReserves=%s WHERE NewMineId=%s AND sessionKey=%s', (resources_to_reserves, NewMineId, mSession_key))
                        mCur.execute('COMMIT')
                    # check to see if there are Resource files

                    if resourcesFound:
                        # assusmes you have a resources number
                        if debugMode:
                            print "last_data['resources']['value']: ({}) {}".format(type(last_data['resources']['value']),last_data['resources']['value'])
                            print "resources_to_reserves: {}".format(resources_to_reserves)
                        mines['Reserve type'].append("Total Reserves")
                        mines['Reserve year'].append(mines['Resource Year'][-1])
                        mines['Reserves'].append(float(mines['Resource %'][-1]) * resources_to_reserves)
                        mines['Reserve unit'].append(mines['Resource unit'][-1])
                        mines['Reserves Source'].append("EST: Forecast Engine")

                        last_data['reserves']['type']  = "Total Reserves"
                        last_data['reserves']['year']  = last_data['resources']['year']
                        last_data['reserves']['value'] = (float(last_data['resources']['value']) * resources_to_reserves)
                        last_data['reserves']['unit']  = last_data['resources']['unit']

                        last_reserve_type = last_data['reserves']['type']
                        last_reserve_year = last_data['reserves']['year']
                        last_reserve_amt  = last_data['reserves']['value']
                        last_reserve_unit = last_data['reserves']['unit']

                        if debugReserves:
                            print ''
                            print '%s added to %s list' % ("Total Reserves", "mines['Reserve type']")
                            print '%s added to %s list' % (mines['Resource Year'][-1], "mines['Resource Year']")
                            print '%s added to %s list' % (float(mines['Resource %'][-1]) * resources_to_reserves, "mines['Reserves']")
                            print '%s added to %s list' % (mines['Resource unit'][-1], "mines['Reserve unit']")
                            print '%s added to %s list' % ("EST: Forecast Engine", "mines['Reserves Source']")
                    elif reservesFound:
                        # assumes that resources were not found
                        mines['Resource Type'].append("Total Resources")
                        mines['Resource Year'].append(mines['Reserve year'][-1])
                        if resources_to_reserves > 0:
                            mines['Resource %'].append(float(mines['Reserves'][-1]) * (1/resources_to_reserves))
                        else:
                            mines['Resource %'].append(mines['Reserves'][-1])
                        mines['Resource unit'].append(mines['Reserve unit'][-1])
                        mines['Resource Source'].append("EST: Forecast Engine")

                        last_data['resources']['type'] = "Total Resources"
                        last_data['resources']['year'] = last_data['reserves']['year']
                        last_data['resources']['value'] = mines['Resource %']
                        last_data['resources']['unit'] = last_data['reserves']['unit']
                    lastReserveYear   = last_data['reserves']['year']
                    last_reserve_year = last_data['reserves']['year']
                    lastHistProdYear = max(last_reserve_year, lastHistProdYear)
                    if debugMode:
                        print ''
                        print '(2) lastHistProdYear: {}'.format(lastHistProdYear)
                        print ''
                if not capacityFound:
                    # create the capacity record based on the maxproduction
                    if productionFound and maxProduction > 0:
                        # look up capacity_to_production
                        # -------------------------------------------------------------------
                        extraWhere = ""
                        extraVars = ""
                        ctp_lookup = True
                        ctp = get_param_detail(mCur,"CAPACITY_TO_PRODUCTION",NewMineId,mineCountry,mineRegion,mineStatus,mineType,mineMethod,key_commodity,mOperators,extraWhere,extraVars )
                        if debugMode:
                            print "$" * 30
                            print "CAPACITY TO PRODUCTION  "
                            print 'ctp:', ctp
                        if ctp == 0 or len(ctp.strip()) == 0:
                            # use the default and trigger an error
                            mComment = "CAPACITY TO PRODUCTION RATIO NOT FOUND "
                            error_log[0].append(NewMineId)
                            error_log[1].append(0)
                            error_log[2].append(mComment)
                            error_log[3].append(mSession_key)
                            error_log[4].append("ERROR TYPE 10")
                            error_log[5].append("")
                            error_log[6].append(0)
                            if debugMode:
                                print '!*' * 50
                                print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                                print ''
                            capacity_to_production  = .90
                        else:
                            capacity_to_production  = float(ctp)
                        if updateParamTrk:
                            mCur.execute('UPDATE mining_param_track SET capacityToProduction=%s WHERE NewMineId=%s AND sessionKey=%s', (capacity_to_production, NewMineId, mSession_key))
                            mCur.execute('COMMIT')
                        # Create the ROM CAPACITY
                        #
                        mines['Capacity type'].append(mines['Production Type'][-1])
                        mines['Capacity year'].append(mines['Production Year'][-1])
                        mines['Capacity Source'].append("EST: Forecast Engine")
                        if capacity_to_production > 0:
                            mines['Capacity'].append(float(maxProduction)*float((1.0/float(capacity_to_production))))
                        else:
                            mines['Capacity'].append(0)
                        mines['Capacity unit'].append(mines['Production unit'][-1])

                        mine_data['capacity'][int(mines['Production Year'][-1])] = {
                            'raw': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''},
                            'rom': {'type': '', 'commodity': '', 'value': 0, 'unit': '', 'source': ''}
                        }
                        mine_data['capacity'][int(mines['Production Year'][-1])]['rom']['type']   = mines['Production Type'][-1]
                        mine_data['capacity'][int(mines['Production Year'][-1])]['rom']['source'] = "EST: Forecast Engine"
                        mine_data['capacity'][int(mines['Production Year'][-1])]['rom']['value']  = mines['Capacity'][-1]
                        mine_data['capacity'][int(mines['Production Year'][-1])]['rom']['unit']   = mines['Production unit'][-1]

                        last_data['capacity']['type']  = last_data['production']['type']
                        last_data['capacity']['year']  = last_data['production']['year']
                        last_data['capacity']['value'] = mines['Capacity'][-1]
                        last_data['capacity']['unit']  = last_data['production']['unit']

                        last_capacity_type = last_data['capacity']['type']
                        last_capacity_year = last_data['capacity']['year']
                        last_capacity_amt  = last_data['capacity']['value']
                        last_capacity_unit = last_data['capacity']['unit']
                        lastHistProdYear = max(int(last_capacity_year), lastHistProdYear)
                        if debugMode:
                            print ''
                            print '(3) lastHistProdYear: {}'.format(lastHistProdYear)
                            print ''
                        capacityFound = True
                if not productionFound and capacityFound:
                    # generate if you can based off of the capacity number
                    # look up capacity_to_production
                    # -------------------------------------------------------------------
                    extraWhere = ""
                    extraVars = ""
                    ctp_lookup = True
                    ctp = get_param_detail(mCur,"CAPACITY_TO_PRODUCTION",NewMineId,mineCountry,mineRegion,mineStatus,mineType,mineMethod,key_commodity,mOperators,extraWhere,extraVars )
                    if debugMode:
                        print "$" * 30
                        print "CAPACITY TO PRODUCTION  "
                        print 'ctp:', ctp
                    if ctp == 0 or len(ctp.strip()) == 0:
                        # use the default and trigger an error
                        mComment = "CAPACITY TO PRODUCTION RATIO NOT FOUND "
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 10")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''
                        capacity_to_production  = .90
                    else:
                        capacity_to_production  = float(ctp)
                    if updateParamTrk:
                        mCur.execute('UPDATE mining_param_track SET capacityToProduction=%s WHERE NewMineId=%s AND sessionKey=%s',(capacity_to_production, NewMineId, mSession_key))
                        mCur.execute('COMMIT')
                    
                    # Create the production value
                    # Ensure last capacity values are accurate and consistent with last_data['capacity'] values 20181128
                    assert mines['Capacity year'][-1] == last_data['capacity']['year']
                    assert mines['Capacity year'][-1] == last_capacity_year
                    assert mines['Capacity'][-1] == last_data['capacity']['value']
                    assert mines['Capacity'][-1] == last_capacity_amt

                    mines['Production Type'].append(mines['Capacity type'][-1])
                    mines['Production Year'].append(mines['Capacity year'][-1])
                    mines['Production Source'].append("EST: Forecast Engine")

                    zeroTotalProd = False
                    if mTotalProduction == 0:
                        zeroTotalProd = True

                    # Duplicating code above until transition to new variables is complete 20181128
                    if total_mine_prod == 0:
                        zeroTotalProd = True

                    if capacity_to_production > 0:
                        capEstProdValue = float(mines['Capacity'][-1])*float(capacity_to_production)
                        mines['Production Value'].append(capEstProdValue)
                        if zeroTotalProd:
                            mTotalProduction += capEstProdValue

                            total_mine_prod += capEstProdValue
                            total_srcd_prod += capEstProdValue
                            total_hist_prod += capEstProdValue

                            mine_prod[int(last_capacity_year)] = float(capEstProdValue)
                            srcd_prod[int(last_capacity_year)] = float(capEstProdValue)
                            hist_prod[int(last_capacity_year)] = float(capEstProdValue)

                        if debugMode:
                            print "mines['Capacity'][-1]):", mines['Capacity'][-1]
                            print 'capacity_to_production:', capacity_to_production
                            print '%s added to %s' % (float(mines['Capacity'][-1])*float(capacity_to_production), "mines['Production Value']")
                    else:
                        mines['Production Value'].append(0)
                    mines['Production unit'].append(mines['Capacity unit'][-1])

                    last_data['production']['type']      = mines['Production Type'][-1]
                    last_data['production']['commodity'] = ''
                    last_data['production']['year']      = mines['Production Year'][-1]
                    last_data['production']['value']     = mines['Production Value'][-1]
                    last_data['production']['unit']      = mines['Production unit'][-1]

                    first_data['production']['type']      = mines['Production Type'][0]
                    first_data['production']['commodity'] = ''
                    first_data['production']['year']      = mines['Production Year'][0]
                    first_data['production']['value']     = mines['Production Value'][0]
                    first_data['production']['unit']      = mines['Production unit'][0]
                    lastHistProdYear = max(int(last_data['production']['year']), lastHistProdYear)
                    if debugMode:
                        print ''
                        print '(4) lastHistProdYear: {}'.format(lastHistProdYear)
                        print ''
                    productionFound = True
                if reservesFound or resourcesFound:
                    lastReserveYear = mines['Reserve year'][-1]
                    assert lastReserveYear == last_reserve_year
                    assert lastReserveYear == last_data['reserves']['year']
                    lastHistProdYear = max(int(lastReserveYear), lastHistProdYear)
                    if debugMode:
                        print ''
                        print '(5) lastHistProdYear: {}'.format(lastHistProdYear)
                        print ''
                    if discountYear - lastReserveYear > 5:
                        mComment = "NO SOURCED RESERVES WITHIN 5 YEARS OF CURRENT YEAR"
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 27")
                        error_log[5].append(discountYear)
                        error_log[6].append(lastReserveYear)
                if (productionFound or capacityFound) and (reservesFound or resourcesFound):
                    if mines['Production Year'][-1] - mines['Reserve year'][-1] > 5 or mines['Production Year'][-1] - mines['Reserve year'][-1] < -5:
                        mComment = "LAST SOURCED PRODUCTION AND LAST SOURCED RESERVES ARE GREATER THAN 5 YEARS APART"
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 25")
                        error_log[5].append(mines['Reserve year'][-1])
                        error_log[6].append(mines['Production Year'][-1])

                    lastProdValue   = mines['Production Value'][-1]
                    lastProdUnit    = mines['Production unit'][-1]
                    lastReserveVal  = float(mines['Reserves'][-1])
                    lastReserveUnit = mines['Reserve unit'][-1]

                    if lastReserveUnit == lastProdUnit:
                        convFactor = 1.0
                    else:
                        convFactor = float(mining_units(mCur, lastReserveUnit, lastProdUnit, False))

                    lastReserveUnit = lastProdUnit
                    lastReserveVal *= convFactor
                    lastHistProdYear = max(max(int(mines['Production Year'][-1]), int(mines['Reserve year'][-1])), lastHistProdYear)
                    if debugMode:
                        print ''
                        print '(6) lastHistProdYear: {}'.format(lastHistProdYear)
                        print ''
                # ---------------------------------------------------------------
                # is there production
                generate_history = False
                generate_forecast = False
                forecast_years = 1
                historical_years = 0
                total_reserves = 0
                last_cap = 0
                #lastProd = 0

                lastProdValue = 0
                lastProdYear  = discountYear
                lastProdUnit  = 'MMT'
                lastProdType  = ''

                firstProdValue = 0
                firstProdYear = 0
                firstProdUnit = 'MMT'
                firstProdType = ''
                #
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
                APSY, MEY, TML, RML, APSYS, MEYS, TMLS, RMLS, RMLY  = (True,)*9

                prod_found = False
                scenario = 0

                sqlList = []
                sql_dict = {'APSY': '', 'MEY': '', 'TML': '', 'RML': '', 'APSYS': '', 'MEYS': '', 'TMLS': '', 'RMLS': '', 'RMLY': ''}
                sql_i = 0

                # Check for production
                # The main question is there production data?
                
                # Test if condition below is accurately tracked with productionFound flag
                assert (len(mines['Production Value']) >= 1) == productionFound
                
                if len(mines['Production Value']) >= 1:
                    prod_found = True
                    generate_forecast = True
                    if debugMode:
                        print ""
                        print "**** PRODUCTION AVAILABLE "
                        print "mines['Production Year']:", mines['Production Year']
                        print "mines['Production Value']:", mines['Production Value']
                        print "mines['Production unit']:", mines['Production unit']
                        print "mines['Production Type']:", mines['Production Type']
                        print ""
                else:
                    if updateParamTrk:
                        mCur.execute('UPDATE mining_param_track SET forecastEndCause="NO PRODUCTION DATA" WHERE NewMineId=%s AND sessionKey=%s', (NewMineId, mSession_key))
                        mCur.execute('COMMIT')
                    if debugMode:
                        print ""
                        print "**** NO PRODUCTION DATA - " *10

                if debugMode:
                    print 'ActualProductionStartYear      :', ActualProductionStartYear
                    print 'ActualProductionStartYearSource:', ActualProductionStartYearSource
                    print 'mineEndYear                    :', mineEndYear
                    print 'totalMineLife                  :', totalMineLife
                    print 'remainingMineLife              :', remainingMineLife
                    print 'remainingMineLifeYear          :', remainingMineLifeYear
                    print 'APSY                           :', APSY
                    print 'APSYS                          :', APSYS
                    print 'MEY                            :', MEY
                    print 'MEYS                           :', MEYS
                    print 'TML                            :', TML
                    print 'TMLS                           :', TMLS
                    print 'RML                            :', RML
                    print 'RMLS                           :', RMLS
                    print 'RMLY                           :', RMLY

                # Check data sources for missing or engine-generated values
                # ---------------------------------------------------------------------------------------------
                if ActualProductionStartYearSource is None or len(ActualProductionStartYearSource.strip()) == 0 or ActualProductionStartYearSource == "EST: Forecast Engine":
                    APSYS = False
                # ---------------------------------------------------------------------------------------------
                if (RemainingMineLifeSource is None or len(RemainingMineLifeSource.strip()) == 0 or RemainingMineLifeSource == "EST: Forecast Engine"):
                    RMLS = False
                # ---------------------------------------------------------------------------------------------
                if (TotalMineLifeSource is None or len(TotalMineLifeSource.strip()) == 0 or TotalMineLifeSource == "EST: Forecast Engine"):
                    TMLS = False
                # ---------------------------------------------------------------------------------------------
                if (MineEndYearSource is None or len(MineEndYearSource.strip()) == 0 or MineEndYearSource == "EST: Forecast Engine"):
                    MEYS = False
                # ---------------------------------------------------------------------------------------------

                # Check parameter data and calculate missing values when possible
                # ---------------------------------------------------------------------------------------------
                if (ActualProductionStartYear is None or ActualProductionStartYear == 0 or not APSYS):
                    ActualProductionStartYear = 0
                    APSY = False

                # ---------------------------------------------------------------------------------------------
                if (mineEndYear is None or mineEndYear == 0 or not MEYS):
                    mineEndYear = 0
                    MEY = False
                else:
                    remainingMineLife = max(0, mineEndYear-discountYear)
                    if ActualProductionStartYear:
                        totalMineLife = max(0, mineEndYear-ActualProductionStartYear)
                        TML = True
                        TMLS = True
                    elif totalMineLife:
                        ActualProductionStartYear = mineEndYear - totalMineLife
                        APSY = True
                        APSYS = True

                # ---------------------------------------------------------------------------------------------
                if (totalMineLife is None or totalMineLife == 0 or not TMLS):
                    totalMineLife = 0
                    TML = False
                else:
                    if ActualProductionStartYear:
                        mineEndYear = ActualProductionStartYear + totalMineLife
                        remainingMineLife = max(0, mineEndYear - discountYear)
                        MEY = True
                        MEYS = True
                        RML = True
                        RMLS = True
                    elif mineEndYear:
                        ActualProductionStartYear = mineEndYear - totalMineLife
                        remainingMineLife = max(0, mineEndYear - discountYear)
                        APSY = True
                        APSYS = True
                        RML = True
                        RMLS = True

                # ---------------------------------------------------------------------------------------------
                if (remainingMineLifeYear is None or remainingMineLifeYear == 0):
                    remainingMineLifeYear = 0
                    RMLY = False

                # ---------------------------------------------------------------------------------------------
                if (remainingMineLife is None or not RMLS):
                    remainingMineLife = 0
                    RML = False
                else:
                    mineEndYear = discountYear + max(remainingMineLife, 0)
                    MEY = True
                    MEYS = True
                    if totalMineLife:
                        ActualProductionStartYear = mineEndYear - totalMineLife
                        APSY = True
                        APSYS = True
                    elif ActualProductionStartYear:
                        totalMineLife = max(0,discountYear-ActualProductionStartYear) + remainingMineLife
                        TML = True
                        TMLS = True
                if debugMode:
                    print '-=-' * 30
                    print 'actualProductionStartYear       --->  APSY: %s ---> %s' % (ActualProductionStartYear, APSY)
                    print 'actualProductionStartYearSource ---> APSYS: %s ---> %s' % (ActualProductionStartYearSource, APSYS)
                    print 'mineEndYear                     --->   MEY: %s ---> %s' % (mineEndYear, MEY)
                    print 'mineEndYearSource               --->  MEYS: %s ---> %s' % (MineEndYearSource, MEYS)
                    print 'TotalMineLife                   --->   TML: %s ---> %s' % (totalMineLife, TML)
                    print 'TotalMineLifeSource             --->  TMLS: %s ---> %s' % (TotalMineLifeSource, TMLS)
                    print 'RemainingMineLife               --->   RML: %s ---> %s' % (remainingMineLife, RML)
                    print 'remainingMineLifeSource         --->  RMLS: %s ---> %s' % (RemainingMineLifeSource, RMLS)
                    print 'remainingMineLifeYear           --->  RMLY: %s ---> %s' % (remainingMineLifeYear, RMLY)

                if not (APSY or APSYS):
                    mComment = "NO SOURCED PRODUCTION START YEAR PROVIDED"
                    error_log[0].append(NewMineId)
                    error_log[1].append(0)
                    error_log[2].append(mComment)
                    error_log[3].append(mSession_key)
                    error_log[4].append("ERROR TYPE 29")
                    error_log[5].append("")
                    error_log[6].append(0)

                # Should be same because missing values would be filled by other
                assert (len(mines['Production Value']) == 0) == (len(mines['Capacity']) == 0)
                # Alternative way of expressing above test
                assert productionFound == capacityFound

                # Without production or capacity you cannot model the asset
                if len(mines['Production Value']) == 0 and len(mines['Capacity']) == 0:
                    # DO NOT MODEL
                    forecast_years = 0
                    if debugMode:
                        print "SECTION: DO NOT MODEL" * 12
                    pass
                else:
                    if not APSY:
                        scenario = 1
                        # forecast_years --> -1
                        if prod_found or productionFound:
                            if debugMode:
                                print "not APSY and not MEY and not TML and not RML and not RMLY - PRODUCTION - "
                                print 'not actualProductionStartYear and not mineEndYear and not TotalMineLife and not RemainingMineLife and not remainingMineLifeYear'

                            ActualProductionStartYear = int(first_data['production']['year'])
                            assert ActualProductionStartYear == int(mines['Production Year'][0])

                            APSYS = True
                            # set to last year of production temporarily
                            if not MEY:
                                mineEndYear = discountYear
                            if debugMode:
                                print "Actual Production Start Year : "
                                print 'ActualProductionStartYear:', ActualProductionStartYear
                                print 'mineEndYear: {}'.format(mineEndYear)

                            # At this point the only action you can do is set the ActualProductionStartYear
                            # because there is production history

                            forecast_years = -1

                            lastProdYear  = mines['Production Year'][-1]
                            lastProdType  = mines['Production Type'][-1]
                            lastProdUnit  = mines['Production unit'][-1]
                            lastProdValue = mines['Production Value'][-1]

                            if lastProdUnit not in ['MMT', 'MTPA']:
                                newProdUnit = "MMT"
                                convFactor = mining_units(mCur, lastProdUnit, newProdUnit, True)
                                lastProdValue = float(lastProdValue) * convFactor
                                mines['Production unit'][-1] = newProdUnit
                                mines['Production Value'][-1] = lastProdValue
                                last_data['production']['unit'] = newProdUnit
                                last_data['production']['value'] = lastProdValue
                                lastProdUnit = newProdUnit

                            generate_forecast = True

                            firstProdValue = first_data['production']['value']
                            firstProdYear  = first_data['production']['year']
                            firstMineYear  = first_data['production']['year']
                            if debugMode:
                                print 'forecast_years:', forecast_years
                                print "Last production: " + str(lastProdValue)
                                print " Last Prod Year: " + str(lastProdYear)
                                print "           Type: " + lastProdType
                                print "         Source: " + mines['Production Source'][-1]
                                print "         Length: " + str(len(mines['Production Value']))
                        # forecast_years --> 0
                        else:
                            # no production
                            # Factors
                            # 1 - is there total reserves?
                            if debugMode:
                                print "not APSY and not MEY and not TML and not RML and not RMLY - NO PRODUCTION - " * 5
                            if len(mines['Reserve type']):
                                firstMineYear = first_data['reserves']['year']
                                if debugMode or debugReserves:
                                    print ''
                                    print 'first_reserve_type,first_reserve_year ,first_reserve_amt ,first_reserve_unit:', first_reserve_type,first_reserve_year ,first_reserve_amt ,first_reserve_unit
                                    print 'last_reserve_type,last_reserve_year ,last_reserve_amt ,last_reserve_unit:', last_reserve_type,last_reserve_year ,last_reserve_amt ,last_reserve_unit
                                lastProdYear = discountYear
                                # forecast_years --> -1
                                if first_capacity_year > 0:
                                    # use the date and the capacity to contruct the history
                                    # evaluate the minimum of the first_reserve_year and first_capacity_year
                                    firstMineYear    = min(first_reserve_year, first_capacity_year)
                                    historical_years = lastProdYear - firstMineYear
                                    lastProdValue    = last_data['capacity']['value']
                                    lastProdType     = last_data['capacity']['type']
                                    lastProdUnit     = last_data['capacity']['unit']

                                    firstProdValue = first_data['capacity']['value']
                                    firstProdYear  = first_data['capacity']['year']
                                    firstProdUnit  = first_data['capacity']['unit']
                                    #
                                    generate_history = True
                                    generate_forecast = True
                                    forecast_years = -1
                                    if debugMode:
                                        print 'forecast_years:', forecast_years
                                # forecast_years --> 0
                                else:
                                    if debugMode:
                                        print "NO PRODUCTION - NO CAPACITY DATA - DO NOT MODEL"
                                    forecast_years = 0
                                    generate_history = False
                                    generate_forecast = False
                                    forecast_end = "NO PRODUCTION - NO CAPACITY DATA "
                                    if updateParamTrk:
                                        mCur.execute('UPDATE mining_param_track SET forecastEndCause=%s WHERE NewMineId=%s AND sessionKey=%s', (forecast_end, NewMineId, mSession_key))
                                        mCur.execute('COMMIT')
                            # forecast_years --> 0
                            else:
                                if debugMode:
                                    print "NO PRODUCTION - NO RESERVES DATA - DO NOT MODEL"
                                generate_history = False
                                generate_forecast = False
                                thisWasModelled = False
                                forecast_years = 0
                                forecast_end = "NO PRODUCTION - NO RESERVES DATA - DO NOT MODEL"
                                if updateParamTrk:
                                    mCur.execute('UPDATE mining_param_track SET forecastEndCause=%s WHERE NewMineId=%s AND sessionKey=%s',(forecast_end, NewMineId, mSession_key))
                                    mCur.execute('COMMIT')
                            if debugMode:
                                print
                                print "LastYear = " + str(lastProdYear)
                    else:
                        scenario = 2
                        # forecast_years --> -1
                        if len(mines['Production Year']):
                            lastProdYear  = mines['Production Year'][-1]
                            lastProdType  = mines['Production Type'][-1]
                            lastProdUnit  = mines['Production unit'][-1]
                            lastProdValue = mines['Production Value'][-1]

                            if debugMode:
                                print "APSY and not MEY and not TML and not RML and not RMLY - PRODUCTION - " * 5
                                print "mines['Production Year'][0]:", type(mines['Production Year'][0]), mines['Production Year'][0]
                                print 'first_data[production][year]: {} {}'.format(type(first_data['production']['year']), first_data['production']['year'])
                            firstMineYear = ActualProductionStartYear
                            firstProdYear = mines['Production Year'][0]

                            assert firstProdYear == first_data['production']['year']

                            if debugMode:
                                print "mines['Production Year'][0]:", firstProdYear
                                print "Start year: " + str(ActualProductionStartYear)
                            if  firstProdYear - firstMineYear >= 0:
                                if debugMode:
                                    print "Years ----> " + str(firstProdYear - firstMineYear)
                                historical_years = firstProdYear - firstMineYear
                                generate_history = True
                                firstProdValue = float(mines['Production Value'][0])
                            else:
                                resourceYr = 0
                                reserveYr = 0
                                historical_years = 0
                                if len(mines['Resource Year']):
                                    resourceYr = last_data['resources']['year']
                                if len(mines['Reserve year']):
                                    reserveYr = last_data['reserves']['year']
                                    if reserveYr > 0:
                                        generate_forecast = True

                            assert first_data['production']['unit'] == mines['Production unit'][0]

                            if first_data['production']['unit'] not in ['MMT', 'MTPA']:
                                oldProdUnit = mines['Production unit'][0]
                                oldProdValue = mines['Production Value'][0]
                                newProdUnit = "MMT"
                                convFactor = mining_units(mCur, oldProdUnit, newProdUnit, True)
                                newProdValue = float(oldProdValue) * convFactor
                                mines['Production unit'][0] = newProdUnit
                                mines['Production Value'][0] = newProdValue
                                first_data['production']['unit'] = newProdUnit
                                first_data['production']['value'] = newProdValue

                            firstProdYear  = mines['Production Year'][0]
                            firstProdType  = mines['Production Type'][0]
                            firstProdValue = mines['Production Value'][0]
                            firstProdUnit  = mines['Production unit'][0]

                            assert firstProdYear == first_data['production']['year']
                            assert firstProdType == first_data['production']['type']
                            assert firstProdValue == first_data['production']['value']
                            assert firstProdUnit == first_data['production']['unit']

                            forecast_years = -1
                            if debugMode:
                                print 'forecast_years:', forecast_years
                                print "firstProdValue := mines['Production Value'][0] --> ", firstProdValue
                                print "firstProdYear := mines['Production Year'][0] --> ", firstProdYear
                                print "firstProdType := mines['Production Type'][0] --> ", firstProdType
                                print "firstProdUnit := mines['Production unit'][0] --> ", firstProdUnit
                        # forecast_years --> 0
                        else:
                            generate_history = False
                            generate_forecast = False
                            forecast_years = 0
                            forecast_end = "NO PRODUCTION - DO NOT MODEL"
                            if updateParamTrk:
                                mCur.execute('UPDATE mining_param_track SET forecastEndCause=%s WHERE NewMineId=%s AND sessionKey=%s', (forecast_end, NewMineId, mSession_key))
                                mCur.execute('COMMIT')
                            if debugMode:
                                print 'forecast_years:', forecast_years
                                print "APSY and not MEY and not TML and not RML and not RMLY - NO PRODUCTION - " * 5

                # Is the miningAcreage calculated?
                #=====================================================================
                #
                cap_to_prod = get_param_detail(mCur, "CAPACITY_TO_PRODUCTION", NewMineId, mineCountry, mineRegion, mineStatus, mineType, mineMethod, key_commodity, mOperators, extraWhere, extraVars)
                if not cap_to_prod:
                    cap_to_prod = 0.9
                #----------------------------------------------------------------------------------
                generated_hist = False
                generated_FC   = False
                if generate_history:
                    if debugMode:
                        print " ** BUILDING HISTORY ** " * 5
                        print "mines['Production Type']:", mines['Production Type']
                        print "mines['Production Year']:", mines['Production Year']
                        print "mines['Production Value']:", mines['Production Value']
                        print "mines['Production unit']:", mines['Production unit']
                        print "mines['Production Source']:", mines['Production Source']
                        print ''
                        print "mines['Capacity type'  ]:", mines['Capacity type']
                        print "mines['Capacity year'  ]:", mines['Capacity year']
                        print "mines['Capacity'       ]:", mines['Capacity']
                        print "mines['Capacity unit'  ]:", mines['Capacity unit']
                        print "mines['Capacity Source']:", mines['Capacity Source']
                    hLastYear     = firstProdYear
                    hLastProd     = firstProdValue
                    hLastProdUnit = firstProdUnit
                    hLastProdType = firstProdType
                    if hLastProdUnit != 'MMT':
                        convFactor = mining_units(mCur, hLastProdUnit, "MMT", True)
                        hLastProd *= convFactor
                        hLastProdUnit = "MMT"
                    for i in range(historical_years):
                        generated_hist = True
                        if i <= 5:
                            e_ratio = ye_lt5
                        elif i <= 10:
                            e_ratio = ye_lt10
                        else:
                            e_ratio = ye_lt20
                        if debugMode:
                            print 'hLastProd:', hLastProd
                            print 'float(1-e_ratio):', float(1-e_ratio)
                            print 'hLastProd *= float(1-e_ratio)'
                        hLastProd *= float(1-e_ratio)
                        hLastYear -= 1
                        if hLastYear in mine_data['capacity'].keys():
                            hLastCapacity = mine_data['capacity'][hLastYear]['rom']['value']
                            hMaxCapacity = float(hLastCapacity)*float(cap_to_prod)
                            if debugMode:
                                print '    hLastYear: {}'.format(hLastYear)
                                print 'hLastCapacity: {}'.format(hLastCapacity)
                                print ' hMaxCapacity: {}'.format(hMaxCapacity)
                                print '    hLastProd = min({},{})'.format(hLastProd, hMaxCapacity)
                            hLastProd = min(hLastProd, hMaxCapacity)
                        if debugMode:
                            print pws(str(i),3),"**** Historical Forecast -----> " + str(hLastProd) + "   " + str(hLastYear)
                            print ''

                        # add to the array of values ----------------------------------------
                        mines['Production Type'].insert(0,hLastProdType)
                        mines['Production Year'].insert(0,hLastYear)
                        mines['Production Value'].insert(0,hLastProd)
                        mines['Production unit'].insert(0,hLastProdUnit)
                        mines['Production Source'].insert(0,'EST: Forecast Engine')
                        # -------------------------------------------------------------------
                        mTotalProduction += hLastProd

                        total_mine_prod += hLastProd
                        mine_prod[int(hLastYear)] = float(hLastProd)

                        total_hist_prod += hLastProd
                        hist_prod[int(hLastYear)] = float(hLastProd)
                    lastProdYear = mines['Production Year'][-1]
                    if debugMode:
                        print "******** Total historical production: " + str(mTotalProduction)
                #----------------------------------------------------------------------------------
                recovery_rate = 0
                resourcesLimit = False
                if generate_forecast:
                    # ----------------------------------------------------------
                    # take the last production number and multiply it by a factor for x years
                    lastNewProd = 0
                    years_to_project = 0
                    extraWhere = ""
                    extraVars = ""
                    ytp = get_param_detail(mCur,"YEARS_TO_PROJECT",NewMineId,mineCountry,mineRegion,mineStatus,mineType,mineMethod,key_commodity,mOperators,extraWhere,extraVars )
                    if debugMode:
                        print "$" * 30
                        print "YEAR TO PROJECT "
                        print 'ytp:', ytp
                    if ytp == 0 or len(ytp.strip()) == 0:
                        # use the default and trigger an error
                        mComment = "YEARS TO PROJECT NOT FOUND "
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 13")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''
                        # ytp_flag = False
                        years_to_project = 7
                    else:
                        years_to_project = int(ytp)
                    if debugMode:
                        print "$-" * 20
                        print "YEAR TO PROJECT "
                        print 'years_to_project:', years_to_project
                    if updateParamTrk:
                        mCur.execute('UPDATE mining_param_track SET yearsToProject=%s WHERE NewMineId=%s AND sessionKey=%s',(years_to_project, NewMineId, mSession_key))
                        mCur.execute('COMMIT')
                    # -------------------------------------------------------------------
                    extraWhere = ""
                    extraVars = ""
                    if not rr_ran:
                        if debugMode:
                            print 'NewMineId:', NewMineId
                            print 'mineCountry:', mineCountry
                            print 'mineRegion:', mineRegion
                            print 'mineStatus:', mineStatus
                            print 'mineType:', mineType
                            print 'mineMethod:', mineMethod
                            print 'key_commodity:', key_commodity
                            print 'mOperators:', mOperators
                        rr = get_param_detail(mCur,"RECOVERY_RATE",NewMineId,mineCountry,mineRegion,mineStatus,mineType,mineMethod,key_commodity,mOperators,extraWhere,extraVars)
                        if debugMode:
                            print "$" * 30
                            print "RECOVERY RATE  "
                            print 'rr:', rr
                        if rr == 0 or len(rr.strip()) == 0:
                            # use the default and trigger an error
                            mComment = "RECOVERY RATE NOT FOUND "
                            error_log[0].append(NewMineId)
                            error_log[1].append(0)
                            error_log[2].append(mComment)
                            error_log[3].append(mSession_key)
                            error_log[4].append("ERROR TYPE 06")
                            error_log[5].append("")
                            error_log[6].append(0)
                            if debugMode:
                                print '!*' * 50
                                print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                                print ''
                            # ytp_flag = False
                            recovery_rate  = .90
                        else:
                            recovery_rate  = float(rr)
                        if updateParamTrk:
                            mCur.execute('UPDATE mining_param_track SET recoveryRate=%s WHERE NewMineId=%s AND sessionKey=%s', (recovery_rate, NewMineId, mSession_key))
                            mCur.execute('COMMIT')
                        rr_ran = True
                    # --------------------------------------------
                    if forecast_years == 0:
                        if debugMode:
                            print " - NO FORECAST " + ("-" * 30)
                    # --------------------------------------------
                    elif forecast_years == -1:
                        # pass
                        # until exhaustion
                        if debugMode:
                            print " - EXHAUST - " * 10
                        fLastYear = lastProdYear
                        if debugMode or debugReserves:
                            print "rr " + str(recovery_rate)
                            print "Last total reserves "

                        if len(mines['Reserves']) and len(str(recovery_rate).strip()) > 0:
                            # check the units of the reserves
                            baseUnit = mines['Reserve unit'][-1]
                            if debugMode:
                                print "mines['Reserve unit'][-1]:", mines['Reserve unit'][-1]
                                print "mines['Reserves'][-1]:", mines['Reserves'][-1]
                            prodFactor = 1.0
                            if not baseUnit == "MTPA":
                                prodFactor = mining_units(mCur,baseUnit,"MMT",True)
                            calcMaxProduction = float(mines['Reserves'][-1]) * float(recovery_rate) * float(prodFactor)
                            maxRemainingProduction = float(mines['Reserves'][-1]) * float(recovery_rate) * float(prodFactor)
                            if debugMode:
                                print 'maxRemainingProduction   :', maxRemainingProduction
                                print 'calcMaxProduction        :', calcMaxProduction
                                print "calcMaxProduction := float(mines['Reserves'][-1]) * float(recovery_rate) * float(prodFactor)"
                                print 'recovery_rate            :', recovery_rate
                                print 'prodFactor               :', prodFactor
                                print 'lastReserveYear          : {}'.format(lastReserveYear)
                                print 'last_reserve_year        : {}'.format(last_reserve_year)
                                print "mines['Reserve year'][-1]:", mines['Reserve year'][-1]
                                print "mines['Reserves'][-1]    :", mines['Reserves'][-1]
                                print "mines['Reserves'][-1] * prodFactor = %s" % (float(mines['Reserves'][-1]) * float(prodFactor))
                        else:
                            # missing reserves numbers
                            # use the resource to reserves number
                            if resourcesFound:
                                # what are the units of the resources
                                baseUnit = mines['Resource unit'][-1]
                                prodFactor = 1.0
                                if not baseUnit == "MTPA":
                                    prodFactor = mining_units(mCur, baseUnit, "MMT", True)
                                calcMaxProduction      = float(resources_to_reserves*mines['Resource %'][-1]) * float(recovery_rate) * float(prodFactor)
                                maxRemainingProduction = float(resources_to_reserves*mines['Resource %'][-1]) * float(recovery_rate) * float(prodFactor)
                                if debugMode:
                                    print 'maxRemainingProduction:', maxRemainingProduction
                                    print 'calcMaxProduction:', calcMaxProduction
                                    print "calcMaxProduction := float(resources_to_reserves*mines['Resource %'][-1]) * float(recovery_rate) * float(prodFactor)"
                                    print 'resources_to_reserves:', resources_to_reserves
                                    print 'recovery_rate:', recovery_rate
                                    print 'prodFactor:', prodFactor
                                    print 'lastReserveYear: {}'.format(lastReserveYear)
                                    print 'last_reserve_year: {}'.format(last_reserve_year)
                                    print "mines['Resource Year'][-1]:", mines['Resource Year'][-1]
                                    print "mines['Resource %'][-1]:", mines['Resource %'][-1]
                            else:
                                calcMaxProduction      = float(mTotalProduction) * (1.0/float(recovery_rate))
                                maxRemainingProduction = float(mTotalProduction) * (1.0/float(recovery_rate))
                                if debugMode:
                                    print 'NO reserves or resources!!??'
                                    print 'calcMaxProduction = mTotalProduction * (1/float(recovery_rate))'
                                    print 'mTotalProduction:', mTotalProduction
                                    print '1/float(recovery_rate):', 1/float(recovery_rate)
                        origCalcMaxProduction = calcMaxProduction
                        origMaxRemainingProduction = maxRemainingProduction
                        if debugMode:
                            print '                 Peak Production:', peakProduction
                            print "                  Max production: " + pws(fwc(str(float(maxProduction)).strip()),20,'R')
                            print "     Total historical production: " + pws(fwc(str(mTotalProduction).strip()),20,'R')
                            print 'Remaining production total limit: ', maxRemainingProduction
                            print "        Production not to exceed: " + pws(fwc(str(calcMaxProduction).strip()),20,'R')
                        # newProd =  *= (1 - yearly_effeciency)
                        # and fLastYear > discountYear + 10
                        firstTime = True
                        #-----------------------------
                        generated_FC   = True
                        #-----------------------------
                        # if mTotalProduction < calcMaxProduction and newProd > .001
                        if debugMode:
                            print 'minimumForecastMax:', minimumForecastMax
                        lastProdYear = mines['Production Year'][-1]
                        lastProdValue = mines['Production Value'][-1]
                        calcForecast = True
                        forecast_year_count = 1
                        lastProdUnit = mines['Production unit'][-1]
                        newProdUnit = "MMT"

                        if lastProdUnit not in ['MMT', 'MTPA']:
                            convFactor = mining_units(mCur, lastProdUnit, "MMT", True)
                            lastProdValue *= convFactor
                            mines['Production unit'][-1] = "MMT"
                            mines['Production Value'][-1] = lastProdValue
                        fLastYear = lastProdYear
                        while calcForecast:
                            if forecast_year_count > 1:
                                mines['Production Type'].append(mines['Production Type'][-1])
                                mines['Production Year'].append(fLastYear)
                                mines['Production Value'].append(lastProdValue)
                                mines['Production unit'].append(newProdUnit)
                                mines['Production Source'].append('EST: Forecast Engine')

                            if debugMode:
                                print ''
                                print '         forecast_year_count:', forecast_year_count
                                print "    mines['Production Year']:", mines['Production Year']
                                print "   mines['Production Value']:", mines['Production Value']
                                print "    mines['Production unit']:", mines['Production unit']
                                print "  mines['Production Source']:", ['{}...'.format(source[:25]) for source in mines['Production Source']]
                                print "mines['Production Type'][-1]:", mines['Production Type'][-1]
                                print '                   fLastYear:', fLastYear
                                print '               lastProdValue:', lastProdValue
                                print '                 newProdUnit:', newProdUnit
                            fLastYear += 1

                            # add to the array of values ----------------------------------------
                            lastProdValue *= (1 - yearly_effeciency)

                            # -------------------------------------------------------------------
                            lastNewProd = lastProdValue
                            resourcesLimit = True

                            mTotalProduction += lastProdValue
                            total_mine_prod += lastProdValue

                            if int(fLastYear) <= lastHistProdYear:
                                total_hist_prod += lastProdValue
                                hist_prod[int(fLastYear)] = float(lastProdValue)
                            else:
                                total_fcst_prod += lastProdValue
                                fcst_prod[int(fLastYear)] = float(lastProdValue)

                            mine_prod[int(fLastYear)] = float(lastProdValue)
                            if debugMode:
                                print '%s   **** Forecast          -----> %s     %s' % (forecast_year_count, lastProdValue, fLastYear)
                                print '%s   **** Total Production  -----> %s     %s' % (forecast_year_count, mTotalProduction, fLastYear)
                                print '%s **** Total Forecasted Production  -----> %s %s' % (forecast_year_count, total_fcst_prod, fLastYear)
                                print "**** Is " + str(total_fcst_prod) + " > " + str(maxRemainingProduction) + "? "
                                print ''

                            if total_fcst_prod > maxRemainingProduction:
                                if debugMode:
                                    print 'total forecasted production: %s exceeds max remaining production: %s -----> End forecast' % (total_fcst_prod, maxRemainingProduction)
                                forecast_end = 'forecasted production: %s exceeds max remaining production: %s' % (total_fcst_prod, maxRemainingProduction)
                                excess_prod = total_fcst_prod - maxRemainingProduction

                                mTotalProduction -= excess_prod
                                total_mine_prod  -= excess_prod
                                total_fcst_prod  -= excess_prod
                                lastProdValue    -= excess_prod

                                mine_prod[int(fLastYear)] = lastProdValue
                                fcst_prod[int(fLastYear)] = lastProdValue

                                mines['Production Type'].append(mines['Production Type'][-1])
                                mines['Production Year'].append(fLastYear)
                                mines['Production Value'].append(lastProdValue)
                                mines['Production unit'].append(newProdUnit)
                                mines['Production Source'].append('EST: Forecast Engine')

                                calcForecast = False

                            if MEY and fLastYear > mineEndYear:
                                if debugMode:
                                    print 'flastYear: {} >= mineEndYear: {}'.format(fLastYear, mineEndYear)
                                calcForecast = False
                                forecast_end = 'mine end year: {} reached'.format(mineEndYear)

                            if forecast_year_count > minimumForecastMax:
                                # then check other conditions
                                if debugMode:
                                    print ''
                                    print "**** Is " + str(mTotalProduction) + " > " + str(calcMaxProduction) + "? "

                                if lastProdValue < .00000000001:
                                    if debugMode:
                                        print 'production value: %s below minimum production threshold: %s -----> End forecast' % (lastProdValue, 0.00000000001)
                                    calcForecast = False
                                    forecast_end = 'production value: %s below minimum production threshold: %s' % (lastProdValue, 0.00000000001)

                                elif forecast_year_count >= max_forecast_years:
                                    if debugMode:
                                        print 'maximum forecast years: %s reached -----> End forecast' % 200
                                    calcForecast = False
                                    forecast_end = 'maximum forecast years: %s reached' % 200

                            forecast_year_count += 1

                        if debugMode:
                            print "******** Total production: " + str(mTotalProduction)
                            print 'Total Historical Production: {}'.format(total_hist_prod)
                            print '   Total Sourced Production: {}'.format(total_srcd_prod)
                            print 'Total Forecasted Production: {}'.format(total_fcst_prod)
                            print '      Total Mine Production: {}'.format(total_mine_prod)
                        param_vals = (mTotalProduction, calcMaxProduction, forecast_end, minimumForecastMax, NewMineId, mSession_key)
                        if updateParamTrk:
                            mCur.execute('UPDATE mining_param_track SET totalProduction=%s, maxProduction=%s, forecastEndCause=%s, minForecastYears=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
                            mCur.execute('COMMIT')
                    # --------------------------------------------
                    else:
                        # This might be a field that is planned
                        if debugMode:
                            print " - FIXED LIFE - " * 30
                        # ----------------------------------------------------------
                        fLastYear = lastProdYear + 1
                        extraYears = max(0,int(discountYear) - int(mines['Production Year'][-1]))
                        forecast_years = years_to_project + extraYears
                        if debugMode:
                            print "Max production: %s" % maxProduction # + str(round(float(maxProduction),prodDecimals))
                            print 'Peak production: {}'.format(peakProduction)
                            print "Total historical production: " + str(total_hist_prod)
                            print 'Total mine production: {}'.format(total_mine_prod)

                        for i in range(forecast_years):
                            #-----------------------------
                            generated_FC   = True
                            #-----------------------------
                            if i == (forecast_years-1):
                                lastProdValue *= last_year_fctr

                            lastProdValue *= (1 - yearly_effeciency)

                            if newProdUnit not in ['MMT', 'MTPA']:
                                convFactor = mining_units(mCur, newProdUnit, "MMT", True)
                            else:
                                convFactor = 1.0

                            lastProdValue *= convFactor
                            newProdUnit = "MMT"

                            if fLastYear in mine_data['capacity'].keys():
                                fLastCapacity = mine_data['capacity'][fLastYear]['rom']['value']
                                fMaxCapacity = float(fLastCapacity) * float(cap_to_prod)
                                if debugMode:
                                    print '    fLastYear: {}'.format(fLastYear)
                                    print 'fLastCapacity: {}'.format(fLastCapacity)
                                    print ' fMaxCapacity: {}'.format(fMaxCapacity)
                                    print 'lastProdValue = min({},{})'.format(lastProdValue, fMaxCapacity)
                                lastProdValue = min(lastProdValue, fMaxCapacity)

                            if debugMode:
                                print '%s\t**** Forecast ----->\t\t%s\t%s' % (i, lastProdValue, fLastYear)

                            # add to the array of values ----------------------------------------
                            mines['Production Type'].append(mines['Production Type'][-1])
                            mines['Production Year'].append(fLastYear)
                            mines['Production Value'].append(lastProdValue)
                            mines['Production unit'].append(newProdUnit)
                            mines['Production Source'].append('EST: Forecast Engine')
                            # -------------------------------------------------------------------
                            mTotalProduction += lastProdValue
                            total_mine_prod += lastProdValue
                            total_fcst_prod += lastProdValue

                            mine_prod[int(fLastYear)] = float(lastProdValue)
                            fcst_prod[int(fLastYear)] = float(lastProdValue)
                            fLastYear += 1
                        if debugMode:
                            print "******** Total production: " + str(mTotalProduction)
                        forecast_end = 'fixed life forecast of %s years complete' % forecast_years
                        param_vals = (mTotalProduction, maxProduction, forecast_end, NewMineId, mSession_key)
                        if updateParamTrk:
                            mCur.execute('UPDATE mining_param_track SET totalProduction=%s, maxProduction=%s, forecastEndCause=%s WHERE NewMineId=%s AND sessionKey=%s',param_vals)
                            mCur.execute('COMMIT')
                # -------------------------------------------------------------------------------
                if generated_FC:
                    # -----------------------------------------------------------------
                    #
                    # Get the first year factor(s)
                    #
                    # -----------------------------------------------------------------
                    extraWhere = ""
                    extraVars = ""
                    first_year_fctr = 0
                    fyf = get_param_detail(mCur,"FIRST_YEAR_FACTOR",NewMineId,mineCountry,mineRegion,mineStatus,mineType,mineMethod,key_commodity,mOperators,extraWhere,extraVars )
                    if debugMode:
                        print "$" * 30
                        print "FIRST_YEAR_FACTOR "
                        print 'fyf:', fyf
                    if fyf == 0 or len(fyf.strip()) == 0:
                        # use the default and trigger an error
                        mComment = "FIRST YEAR FACTOR NOT FOUND "
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 08")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''
                        first_year_fctr  = .5
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
                        for i in range(0,commas):
                            fy_dict[str(i+1)] = 1
                            # now parse
                            pos = fy_copy.index(",")
                            cval = fy_copy[:pos]
                            fy_dict[str(i+1)] = float(cval)
                            fy_copy = fy_copy[pos+1:]
                            if debugMode:
                                print "FIRST YEAR FACTOR" + "^-"*30
                                print 'cval:', cval
                                print 'fy_copy:', fy_copy
                                print 'fy_dict:', fy_dict
                                print ""

                        if updateParamTrk:
                            mCur.execute('UPDATE mining_param_track SET firstYearFactor=%s WHERE NewMineId=%s AND sessionKey=%s',(fyf, NewMineId, mSession_key))
                            mCur.execute('COMMIT')
                        #
                        # APPLY THE DICTIONARY VALUES RETROACTIVELY ONLY IF
                        # THE VALUES ARE ENGINE ESTIMATED
                        if debugMode:
                            print 'mines[Production Year]:', mines['Production Year']
                            print 'mines[Production Value]:', mines['Production Value']
                        if len(mines['Production Source']) >= commas+1 and mines['Production Source'][0] == "EST: Forecast Engine" and mines['Production Source'][1] == "EST: Forecast Engine":
                            origValue = []
                            newValue = []
                            preVal = {}
                            commas = min(commas, len(mines['Production Source']))
                            baseNumber = float(mines['Production Value'][commas])
                            if debugMode:
                                print 'commas:', commas
                                print "BASE NUMBER: " + str(baseNumber)
                            for i in range(commas):
                                if mines['Production Source'][i] == "EST: Forecast Engine":
                                    preVal[str(i)] = mines['Production Value'][i]
                                    val = float(fy_dict[str(i+1)]) * baseNumber
                                    mines['Production Value'][i] = val

                                    val_diff = float(preVal[str(i)]) - float(val)

                                    mTotalProduction -= val_diff

                                    total_mine_prod  -= val_diff
                                    total_hist_prod  -= val_diff
                                    mine_prod[int(mines['Production Year'][i])] = val
                                    hist_prod[int(mines['Production Year'][i])] = val

                                    if debugMode:
                                        print "!-"*30
                                        print "Production year:", mines['Production Year'][i]
                                        print "OLD VAL " + str(preVal[str(i)])
                                        print "NEW VAL " + str(mines['Production Value'][i])
                    # check to see if the program generated data after the discount year
                    if debugMode and forecast_years == -1:
                        print "=|"*25
                        print 'mTotalProduction:', mTotalProduction
                        print 'origCalcMaxProduction:', origCalcMaxProduction
                        print 'total_mine_prod: {}'.format(total_mine_prod)
                        print 'total_hist_prod: {}'.format(total_hist_prod)
                        print 'mine_prod: {}'.format(mine_prod)
                        print 'hist_prod: {}'.format(hist_prod)
                    #*&* 20181203 if len(mines['Production Year']) and (mines['Production Year'][-1] < discountYear) and (total_fcst_prod >= maxRemainingProduction) and (forecast_years == -1):
                    if len(mines['Production Year']) and (mines['Production Year'][-1] < discountYear) and (total_fcst_prod < maxRemainingProduction) and (forecast_years == -1):

                        # generate more data
                        forecast_extend = 7
                        fLastYear = mines['Production Year'][-1] + 1
                        forecast_years = (discountYear + forecast_extend) - mines['Production Year'][-1]
                        forecast_end = 'forecast extended to discount year(%s) + %s' % (discountYear, forecast_extend)
                        if debugMode:
                            print "Max production 2: " +              pws(fwc(str(float(maxProduction)).strip()),15,'R')
                            print "Total historical production 2: " + pws(fwc(str(mTotalProduction).strip()),15,'R')
                        #--------------------------------
                        # back out the last values
                        calcForecast2 = True
                        for i in range(forecast_years):
                            #-----------------------------
                            generated_FC   = True
                            #-----------------------------
                            if calcForecast2:
                                lastProdValue *= (1 - yearly_effeciency)
                                if debugMode:
                                    print pws(str(i),3),"**** Forecast 2 -----> " + pws(fwc(str(lastProdValue).strip()),15,'R') + "   " + str(fLastYear)
                                # add to the array of values ----------------------------------------
                                newProdUnit = mines['Production unit'][-1]
                                if newProdUnit not in ['MMT', 'MTPA']:
                                    convFactor = mining_units(mCur, newProdUnit, "MMT", True)
                                else:
                                    convFactor = 1.0

                                lastProdValue *= convFactor
                                newProdUnit = "MMT"

                                if fLastYear in mine_data['capacity'].keys():
                                    fLastCapacity = mine_data['capacity'][fLastYear]['rom']['value']
                                    fMaxCapacity = float(fLastCapacity) * float(cap_to_prod)
                                    if debugMode:
                                        print '    fLastYear: {}'.format(fLastYear)
                                        print 'fLastCapacity: {}'.format(fLastCapacity)
                                        print ' fMaxCapacity: {}'.format(fMaxCapacity)
                                        print 'lastProdValue = min({},{})'.format(lastProdValue, fMaxCapacity)
                                        print ''
                                    lastProdValue = min(lastProdValue, fMaxCapacity)

                                mines['Production Type'].append(mines['Production Type'][-1])
                                mines['Production Year'].append(fLastYear)
                                mines['Production Value'].append(lastProdValue)
                                mines['Production unit'].append(newProdUnit)
                                mines['Production Source'].append('EST: Forecast Engine')
                                # -------------------------------------------------------------------

                                mTotalProduction += lastProdValue
                                total_mine_prod  += lastProdValue
                                total_fcst_prod  += lastProdValue
                                mine_prod[int(fLastYear)] = float(lastProdValue)
                                fcst_prod[int(fLastYear)] = float(lastProdValue)

                                if total_fcst_prod > maxRemainingProduction:
                                    if debugMode:
                                        print 'total forecasted production: %s exceeds max remaining production: %s -----> End forecast 2' % (total_fcst_prod, maxRemainingProduction)
                                    forecast_end = 'forecasted production: %s exceeds max remaining production: %s' % (total_fcst_prod, maxRemainingProduction)
                                    excess_prod = total_fcst_prod - maxRemainingProduction

                                    mTotalProduction -= excess_prod
                                    total_mine_prod  -= excess_prod
                                    total_fcst_prod  -= excess_prod
                                    lastProdValue    -= excess_prod

                                    mine_prod[int(fLastYear)] = lastProdValue
                                    fcst_prod[int(fLastYear)] = lastProdValue

                                    mines['Production Type'].append(mines['Production Type'][-1])
                                    mines['Production Year'].append(fLastYear)
                                    mines['Production Value'].append(lastProdValue)
                                    mines['Production unit'].append(newProdUnit)
                                    mines['Production Source'].append('EST: Forecast Engine')

                                    calcForecast2 = False
                                fLastYear += 1
                        if debugMode:
                            print "******** Total production: " +  pws(fwc(str(mTotalProduction).strip()),15,'R')
                        param_vals = (mTotalProduction, maxProduction, forecast_end, NewMineId, mSession_key)
                        if updateParamTrk:
                            mCur.execute('UPDATE mining_param_track SET totalProduction=%s, maxProduction=%s, forecastEndCause=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
                            mCur.execute('COMMIT')
                    # -----------------------------------------------------------------
                    #
                    # Get the last year factor
                    #
                    # -----------------------------------------------------------------
                    extraWhere = ""
                    extraVars = ""
                    last_year_fctr = 0
                    ly_dict = {}
                    commas = 0
                    lyf = get_param_detail(mCur,"LAST_YEAR_FACTOR",NewMineId,mineCountry,mineRegion,mineStatus,mineType,mineMethod,key_commodity,mOperators,extraWhere,extraVars )
                    if debugMode:
                        print "$-" * 30
                        print "LAST_YEAR_FACTOR "
                        print 'lyf:', lyf
                    if lyf == 0 or len(lyf.strip()) == 0:
                        # use the default and trigger an error
                        mComment = "LAST YEAR FACTOR NOT FOUND "
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 07")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''
                        # ytp_flag = False
                        lyf  = ".5"
                        ly_dict['1'] = .5
                        commas = 1
                    else:
                        # Did they forget to add the ending comma?
                        # if yes add it to make the algorithms work
                        if lyf[-1:] == ",":
                            pass
                        else:
                            lyf = lyf + ","
                        # parse the commas
                        #
                        sum_factor = 0
                        commas = lyf.count(",")
                        ly_copy = lyf
                        for i in range(0,commas):
                            ly_dict[str(i+1)] = 1
                            # now parse
                            pos = ly_copy.index(",")
                            cval = ly_copy[:pos]
                            ly_dict[str(i+1)] = cval
                            ly_copy = ly_copy[pos+1:]
                            sum_factor += float(cval)
                            if debugMode:
                                print "LAST YEAR FACTOR" + "!-"*30
                                print 'cval:', cval
                                print 'ly_copy:', ly_copy
                                print 'sum_factor:', sum_factor

                    if updateParamTrk:
                        mCur.execute('UPDATE mining_param_track SET lastYearFactor=%s WHERE NewMineId=%s AND sessionKey=%s', (lyf, NewMineId, mSession_key))
                        mCur.execute('COMMIT')

                    # You can only apply the last year factor if the last production years are forecast

                    # APPLY THE DICTIONARY VALUES RETROACTIVELY ONLY IF
                    # THE VALUES ARE ENGINE ESTIMATED

                    if (len(mines['Production Source']) > (1 + commas)) and mines['Production Source'][-1] == "EST: Forecast Engine":
                        origValue = []
                        newValue = []
                        preVal = {}
                        commas = min(commas, len(mines['Production Source']) + 1)
                        baseNumber = float(mines['Production Value'][(-1)*commas])
                        if debugMode:
                            print "LAST YEAR BASE NUMBER (baseNumber): " + str(baseNumber)
                            print "Commas: " + str(commas)
                            print 'ly_dict:', ly_dict
                        x = commas + 1
                        for i in range(commas,0,-1):
                            if mines['Production Source'][-i] == "EST: Forecast Engine":
                                preVal[str(i)] = mines['Production Value'][-i]
                                val = float(ly_dict[str(x - i)]) * baseNumber
                                mines['Production Value'][-i] = val

                                val_diff = float(preVal[str(i)]) - float(val)
                                mTotalProduction -= val_diff
                                total_mine_prod -= val_diff
                                total_fcst_prod -= val_diff

                                mine_prod[int(mines['Production Year'][-i])] = val
                                fcst_prod[int(mines['Production Year'][-i])] = val

                                if debugMode:
                                    print "!-"*30
                                    print 'i:', i
                                    print 'commas:', commas
                                    print 'val = float(ly_dict[%s])' % (x-i), float(ly_dict[str(x-i)])
                                    print "Production year:", mines['Production Year'][-i]
                                    print "OLD VAL " + str(preVal[str(i)])
                                    print "NEW VAL (mines['Production Value'][-%s])" % i, str(mines['Production Value'][-i])

                param_vals = (mTotalProduction, NewMineId, mSession_key)
                if updateParamTrk:
                    mCur.execute('UPDATE mining_param_track SET totalProduction=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
                    mCur.execute('COMMIT')
                # -------------------------------------------------------------------------------
                # After you have generated a forecast - Does the total production equal
                # to x% of the TOTAL RESERVES?
                #-----------------------------------------------------------------------
                if not reservesFound and (generated_FC or generated_hist) and recovery_rate > 0:
                    # generate this based on the mTotalProduction
                    reserveEstimate = mTotalProduction * (1/recovery_rate)

                    mines['Reserve type'].append("Total Reserves")
                    mines['Reserve year'].append(discountYear)
                    mines['Reserves'].append(reserveEstimate)
                    mines['Reserve unit'].append(mines['Production unit'][-1])
                    mines['Reserves Source'].append("EST: Forecast Engine")

                    if debugReserves:
                        print ''
                        print '%s added to %s list' % ("Total Reserves", "mines['Reserve type']")
                        print '%s added to %s list' % (discountYear, "mines['Reserve year']")
                        print '%s added to %s list' % (reserveEstimate, "mines['Reserves']")
                        print '%s added to %s list' % (mines['Production unit'][-1], "mines['Reserve unit']")
                        print '%s added to %s list' % ("EST: Forecast Engine", "mines['Reserves Source']")

                    if debugMode or debugReserves:
                        print 'reserveEstimate:', reserveEstimate
                    #
                #-----------------------------------------------------------------------
                if not resourcesFound and (generated_FC or generated_hist) and len(mines['Reserves']):
                    # generate based on the reserves number
                    resourceEstimate = float(mines['Reserves'][-1]) * (1/resources_to_reserves)
                    mines['Resource Type'].append("Total Resources")
                    mines['Commodity'].append(commodities)
                    mines['Resource Year'].append(discountYear)
                    mines['Resource %'].append(resourceEstimate)
                    mines['Resource unit'].append(mines['Reserve unit'][-1])
                    mines['Resource Source'].append("EST: Forecast Engine")
                    #
                #-----------------------------------------------------------------------
                if generated_FC or generated_hist:
                    modelled += 1
                    modelled_commod[key_commodity] += 1
                else:
                    if debugMode:
                        print " NOT MODELLED == " * 20
                    not_modelled_commod[key_commodity] += 1
                    not_modelled += 1
                    thisWasModelled = False

                    # write to error log
                    mComment = ""
                    if not productionFound:
                        mComment += "NO PRODUCTION "
                    if not capacityFound:
                        mComment += "NO CAPACITY "
                    if not reservesFound:
                        mComment += "NO RESERVES "
                    if not resourcesFound:
                        mComment += "NO RESOURCES"
                    if not firstType1:
                        error_log[0].append(NewMineId)
                        error_log[1].append(0)
                        error_log[2].append(mComment)
                        error_log[3].append(mSession_key)
                        error_log[4].append("ERROR TYPE 01")
                        error_log[5].append("")
                        error_log[6].append(0)
                        if debugMode:
                            print '!*' * 50
                            print '%s: %s' % (error_log[4][-1], error_log[2][-1])
                            print ''
                        firstType1 = True
                #-------------------------------------------------------------------------
                # All bookkeeping is done here
                # update all fields with the correct source
                if not APSY:
                    if debugMode:
                        print "** IN APSY " + "*" *12
                    ActualProductionStartYearSource = "EST: Forecast Engine"
                #-------------------------------------------------------------------------
                if not MEY:
                    if debugMode:
                        print "** IN MEY " + "*" *12
                        print 'mineEndYear: {}'.format(mineEndYear)
                    if RML:
                        mineEndYear = int(discountYear + remainingMineLife)
                        if debugMode:
                            print "** IN MEY (RML) " + "*" * 12
                            print 'mineEndYear: {}'.format(mineEndYear)
                    elif len(mines['Production Year']):
                        mineEndYear =  round(int(mines['Production Year'][-1]),0)
                        MineEndYearSource = 'EST:Forecast Engine'
                        if debugMode:
                            print "Mine end year " + "="*20
                            print 'mineEndYear: {}'.format(mineEndYear)
                            print "mines['Production Year'][-1]:", mines['Production Year'][-1]
                    else:
                        mineEndYear = 0
                #-------------------------------------------------------------------------
                if not TML:
                    if mineEndYear > 0:
                        totalMineLife = mineEndYear - ActualProductionStartYear
                    else:
                        totalMineLife = 0
                    TotalMineLifeSource = "EST: Forecast Engine"
                    if debugMode:
                        print "** IN TML" + "*" *12
                        print 'mineEndYear: {}'.format(mineEndYear)
                        print 'ActualProductionStartYear: {}'.format(ActualProductionStartYear)
                        print "Total mine life = " + str(totalMineLife)
                #-------------------------------------------------------------------------
                if not RML:
                    if mineEndYear > 0:
                        remainingMineLife = mineEndYear - discountYear
                    else:
                        remainingMineLife = 0
                    if debugMode:
                        print "** IN RML " + "*" *12
                        print "RML = " +str(remainingMineLife)
                    remainingMineLife = mineEndYear - discountYear
                    RemainingMineLifeSource = "EST: Forecast Engine"
                #-------------------------------------------------------------------------
                if not RMLY:
                    if mineEndYear > 0:
                        remainingMineLifeYear = round(int(discountYear),0)
                    else:
                        remainingMineLife = 0
                    if debugMode:
                        print "** IN RMLY " + "*" *12
                        print remainingMineLifeYear
                # -------------------------------------------------------------------------
                if totalMineLife > 100:
                    mComment = "TOTAL MINE LIFE EXCEEDS 100 YEARS"
                    error_log[0].append(NewMineId)
                    error_log[1].append(0)
                    error_log[2].append(mComment)
                    error_log[3].append(mSession_key)
                    error_log[4].append("ERROR TYPE 30")
                    error_log[5].append("")
                    error_log[6].append(0)

                # SUM the recoverable reserves here
                estimated_total_recoverable_reserves = 0
                if debugMode:
                    print "mines['Production unit']:", mines['Production unit']
                    print ' mines[Production Year]: {}'.format(mines['Production Year'])
                    print 'mines[Production Value]: {}'.format(mines['Production Value'])
                    for prod_year in sorted(mine_prod.keys()):
                        print '{}: {}'.format(prod_year, mine_prod[prod_year])

                    print 'mine_prod: {}'.format(mine_prod)

                for i in range(len(mines['Production Value'])):
                    if mines['Production unit'][i] == "MMT" or mines['Production unit'][i] == "MTPA":
                        prodFactor = 1
                    else:
                        prodUnit = mines['Production unit'][i]
                        prodFactor = mining_units(mCur, prodUnit, "MMT", True)
                    prodValue = float(mines['Production Value'][i]) * float(prodFactor)
                    estimated_total_recoverable_reserves += prodValue
                    if debugMode or debugReserves:
                        print '%s added to estimated_total_recoverable_reserves' % prodValue
                if debugMode or debugReserves:
                    print '\n'
                    print 'estimated_total_recoverable_reserves (final): %s' % estimated_total_recoverable_reserves
                param_vals = (estimated_total_recoverable_reserves, NewMineId, mSession_key)
                if updateParamTrk:
                    mCur.execute('UPDATE mining_param_track SET estRecovReserves=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
                    mCur.execute('COMMIT')
                if debugMode:
                    print ""
                    print "-------- AGREAGE --------"
                    print 'MineAcreageHectares:', MineAcreageHectares
                #commodities = commodities.split(';')[0] + ';'
                if MineAcreageHectares is None or MineAcreageHectares == 0:

                    # Calculate global average hectares ----------------------------------------------------------------------------------------------------------
                    sqlStatement  = "SELECT a.minecountry, a.newMineid, b.res, b.reserveUnit, a.MineAcreageHectares, b.res/a.MineAcreageHectares, a.commodities "
                    sqlStatement += "FROM mining_assets_daily a JOIN (SELECT reserveyear, newmineid, CAST(reserve AS DECIMAL(16,4)) AS res, reserveUnit FROM mining_reserves_daily "
                    sqlStatement += "WHERE  reserveType = 'Total Reserves' AND NOT LENGTH(reserve) = 0 GROUP BY newmineid  "
                    sqlStatement += "ORDER BY newmineid,reserveyear DESC)  b ON a.newMineid = b.newMineid WHERE a.MineAcreageHectares > 0 "
                    if commod_list:
                        commod_str = " OR ".join(["a.commodities LIKE '%%%s%%'" % commod for commod in commod_list])
                        sqlStatement += "AND (%s) " % commod_str
                    sqlStatement += ""
                    if debugMode:
                        print '\n'
                        print sqlStatement
                    mCur7 = conn.cursor()
                    mCur7.execute(sqlStatement)
                    Res7 = mCur7.fetchall()
                    Haph = 0
                    total_Haph = 0
                    avg_Haph_global = 0
                    global_count = 0
                    for datarow7 in Res7:
                        Hreserves = datarow7[2]
                        HreserveUnit = datarow7[3]
                        Hacreage = datarow7[4]
                        Hcommodity = datarow7[6]

                        # take the average
                        if datarow7[5] is not None and datarow7[5] > 0:
                            Haph = float(datarow7[5])
                            total_Haph += Haph
                            global_count += 1
                            if debugMode:
                                print "** ACREAGE 3----->", pws(str(Hreserves), 18, 'R'), pws(HreserveUnit, 10), pws(str(Hacreage), 12, 'R'), pws(str(Haph), 16, 'R'), pws(Hcommodity, 25, 'R')

                    if global_count:
                        avg_Haph_global = float(total_Haph) / float(global_count)
                        if debugMode:
                            print '\n'
                            print 'total_Haph:', total_Haph
                            print "** Global AVERAGE (avg_Haph_global)----->", avg_Haph_global


                    # Find the average hectares for this commodity in this country -------------------------------------------------------------------------------
                    sqlStatement  = "SELECT a.minecountry,a.newMineid,b.res,b.reserveUnit,a.MineAcreageHectares,b.res/a.MineAcreageHectares,a.commodities "
                    sqlStatement += "FROM mining_assets_daily a JOIN (SELECT ReserveYear, newmineid, CAST(reserve AS DECIMAL(16,4)) AS res, reserveUnit "
                    sqlStatement += "FROM Mining_Reserves_Daily WHERE  reserveType = 'Total Reserves'  AND NOT length(reserve) = 0 GROUP BY newmineid "
                    sqlStatement += "ORDER BY newmineid,reserveyear desc ) b ON a.newmineid = b.newmineid WHERE a.MineAcreageHectares > 0 "
                    if commod_list:
                        commod_str = " OR ".join(["a.commodities LIKE '%%%s%%'" % commod for commod in commod_list])
                        sqlStatement += "AND (%s) " % commod_str
                    if mineCountry.count("'") > 0:
                        sqlStatement += ' AND UCASE(a.minecountry) = "' + mineCountry.upper() + '" ' + " ORDER BY b.res DESC "
                    else:
                        sqlStatement += " AND UCASE(a.minecountry) = '" + mineCountry.upper() + "' " + " ORDER BY b.res DESC "

                    if debugMode:
                        print ""
                        print sqlStatement
                    mCur7 = conn.cursor()
                    mCur7.execute(sqlStatement)
                    Res7 = mCur7.fetchall()
                    Haph = 0
                    total_Haph = 0
                    avg_Haph_country = 0
                    country_count = 0
                    for datarow7 in Res7:
                        # Hreserves, HreserveUnit, Hacreage, Haph, Hcommodity = datarow7[2:]
                        Hreserves = datarow7[2]
                        HreserveUnit = datarow7[3]
                        Hacreage = datarow7[4]
                        Hcommodity = datarow7[6]

                        # take the average
                        # if Haph and Haph > 0:
                        if datarow7[5] is not None and datarow7[5] > 0:
                            Haph = float(datarow7[5])
                            if abs(avg_Haph_global - Haph) > (0.2*avg_Haph_global):
                                pass
                            else:
                                total_Haph += Haph
                                country_count += 1
                                if debugMode:
                                    print "** ACREAGE----->",pws(str(Hreserves),18,'R'),pws(HreserveUnit,10),pws(str(Hacreage),12,'R'),pws(str(Haph),18,'R'),pws(Hcommodity,25,'R')

                    if country_count:
                        avg_Haph_country = float(total_Haph)/float(country_count)
                        if debugMode:
                            print '\n'
                            print 'total_Haph:', total_Haph
                            print 'avg_Haph_country = %s/%s' % (total_Haph, country_count)
                            print "** AVERAGE ratio (avg_Haph_country)----->", avg_Haph_country
                            print "Last reserves"
                            print "mines['Reserves']:", mines['Reserves']

                        if len(mines['Reserves']):
                            if debugMode:
                                print "mines['Reserve unit'][-1]:", mines['Reserve unit'][-1]
                            if mines['Reserve unit'][-1] == 'THOUSAND OUNCES':
                                MineAcreageHectares = (float(mines['Reserves'][-1])*0.0000000283495) / avg_Haph_country
                                if debugMode:
                                    print 'MineAcreageHectares by avg_Haph_country(%s):' % avg_Haph_country, MineAcreageHectares
                            else:
                                MineAcreageHectares = float(mines['Reserves'][-1]) / avg_Haph_country
                                if debugMode:
                                    print 'MineAcreageHectares by avg_Haph_country(%s):' % avg_Haph_country, MineAcreageHectares
                            mineAcreageSource = "EST: Forecast Engine"
                    else:
                        # drop down and search by commodity by region
                        # Find the average hectares for this commodity in this region
                        sqlStatement  = "SELECT a.minecountry,a.newMineid,b.res,b.reserveUnit,a.MineAcreageHectares, b.res/a.MineAcreageHectares,a.commodities "
                        sqlStatement += "FROM mining_assets_daily a JOIN (select reserveyear,newmineid,CAST(reserve AS DECIMAL(16,4)) "
                        sqlStatement += "AS res,reserveUnit FROM mining_reserves_daily WHERE reserveType='Total Reserves' AND NOT LENGTH(reserve)=0 GROUP BY newmineid  "
                        sqlStatement += "ORDER BY newmineid,reserveyear desc)  b ON a.newmineid = b.newmineid WHERE a.MineAcreageHectares > 0 "
                        if commod_list:
                            commod_str = " OR ".join(["a.commodities LIKE '%%%s%%'" % commod for commod in commod_list])
                            sqlStatement += "AND (%s) " % commod_str
                        if mineCountry.count("'") > 0:
                            sqlStatement += ' AND UCASE(a.mineRegion) = "' + mineRegion.upper() + '" ' + " ORDER BY b.res DESC "
                        else:
                            sqlStatement += " AND UCASE(a.mineRegion) = '" + mineRegion.upper() + "' " + " ORDER BY b.res DESC "

                        if debugMode:
                            print ""
                            print sqlStatement
                        mCur7 = conn.cursor()
                        mCur7.execute(sqlStatement)
                        Res7 = mCur7.fetchall()
                        Haph = 0
                        total_Haph = 0
                        avg_Haph_region = 0
                        region_count = 0
                        for datarow7 in Res7:
                            Hreserves = datarow7[2]
                            HreserveUnit = datarow7[3]
                            Hacreage = datarow7[4]
                            Hcommodity = datarow7[6]

                            # take the average
                            if datarow7[5] is not None and datarow7[5] > 0:
                                Haph  = float(datarow7[5])
                                if abs(avg_Haph_global - Haph) > (0.2 * avg_Haph_global):
                                    pass
                                    #print 'flag asset %s' % datarow7[1]
                                else:
                                    total_Haph += Haph
                                    region_count += 1
                                    if debugMode:
                                        print "** ACREAGE 2----->",pws(str(Hreserves),18,'R'),pws(HreserveUnit,10),pws(str(Hacreage),12,'R'),pws(str(Haph),18,'R'),pws(Hcommodity,25,'R')

                        if region_count:
                            avg_Haph_region = float(total_Haph)/float(region_count)
                            if debugMode:
                                print '\n'
                                print 'total_Haph:', total_Haph
                                print "** Region AVERAGE (avg_Haph_region)----->",avg_Haph_region
                            if len(mines['Reserves']):
                                if debugMode:
                                    print "mines['Reserve unit'][-1]:", mines['Reserve unit'][-1]
                                if mines['Reserve unit'][-1] == 'THOUSAND OUNCES':
                                    MineAcreageHectares = (float(mines['Reserves'][-1])*0.0000000283495) / avg_Haph_region
                                    if debugMode:
                                        print 'MineAcreageHectares by avg_Haph_region(%s):' % avg_Haph_region, MineAcreageHectares
                                else:
                                    MineAcreageHectares = float(mines['Reserves'][-1]) / avg_Haph_region
                                    if debugMode:
                                        print 'MineAcreageHectares by avg_Haph_region(%s):' % avg_Haph_region, MineAcreageHectares
                                mineAcreageSource = "EST: Forecast Engine"
                        else:
                            if global_count:
                                if len(mines['Reserves']):
                                    if debugMode:
                                        print ""
                                        print "mines['Reserves']:", mines['Reserves']
                                        print "mines['Reserve unit'][-1]:", mines['Reserve unit'][-1]
                                        print ""
                                    if mines['Reserve unit'][-1] == 'THOUSAND OUNCES':
                                        MineAcreageHectares = (float(mines['Reserves'][-1])*0.0000000283495) / avg_Haph_global
                                        if debugMode:
                                            print 'MineAcreageHectares by avg_Haph_global(%s):' % avg_Haph_global, MineAcreageHectares
                                    else:
                                        MineAcreageHectares = float(mines['Reserves'][-1]) / avg_Haph_global
                                        if debugMode:
                                            print 'MineAcreageHectares by avg_Haph_global(%s):' % avg_Haph_global, MineAcreageHectares
                                    mineAcreageSource = "EST: Forecast Engine"
                #---------------------------------------------------------------------------
                #
                #
                #
                #
                #
                #
                #
                #-------------------------------------------------------------------------
                sqlStatement = "INSERT INTO "  + prefixDB +  "mining_Assets_Forecast ( "
                sqlData = "("
                for ii in range(len(fldAssetsList)):
                    sqlStatement += fldAssetsList[ii] + ","
                    #
                    if fldAssetsList[ii] == '[mineDepth(Meters)]':
                        cVal = mineDepth
                    else:
                        cVal = eval(fldAssetsList[ii])
                    if cVal is None:
                        cVal = ""
                    if fldAssetsListDT[ii] == "c":
                        if cVal.count("'") > 0:
                            sqlData  += '"'+cVal+'",'
                        else:
                            sqlData  += "'"+cVal+"',"
                    elif fldAssetsListDT[ii] == "i":
                        # integer
                        if len(str(cVal).strip())> 0:
                            sqlData += str(cVal) + ","
                        else:
                            sqlData += str(cVal) + "0,"
                    else:
                        sqlData += str(cVal) + ","
                # remove last char
                sqlStatement = sqlStatement[:-1] + ") VALUES " + sqlData[:-1] + ") "
                if debugMode:
                    print "ASSETS DAILY"
                    print sqlStatement
                    print ""
                mCur.execute(sqlStatement)
                mCur.execute("commit;")
                #
                mining_base = []
                mining_base.append("NewMineId")
                mining_base.append("mineName")
                mining_base.append("mineCountry")
                mining_base.append("state")
                mining_base.append("mineRegion")
                mining_base.append("mineStage")
                mining_baseDT = ['i','c','c','c','c','c']
                mining_base_data = str(int(NewMineId)) + ","
                #
                if mineName is None:
                    mining_base_data += '"",'
                elif mineName.count("'") > 0:
                    mining_base_data += '"'+mineName+'",'
                else:
                    mining_base_data += "'"+mineName+"',"
                #
                if mineCountry is None:
                    mining_base_data += '"",'
                elif mineCountry.count("'") > 0:
                    mining_base_data += '"'+mineCountry+'",'
                else:
                    mining_base_data += "'"+mineCountry+"',"
                #
                if state is None:
                    mining_base_data += '"",'
                elif state.count("'") > 0:
                    mining_base_data += '"'+state+'",'
                else:
                    mining_base_data += "'"+state+"',"
                #
                if mineRegion is None:
                    mining_base_data += '"",'
                elif mineRegion.count("'") > 0:
                    mining_base_data += '"'+mineRegion+'",'
                else:
                    mining_base_data += "'"+mineRegion+"',"
                #
                mining_base_data += "'"+mineStage+"',"
                # ------------------------------------------------------------------------------------------
                # Update the capacity forecast table based on the values in the array
                if createdMetalProduction:
                    capacityFound = False
                if len(mines['Capacity year']) and not capacityFound:
                    # add capacity data
                    sqlStatement_capacity = "INSERT INTO " + prefixDB + "mining_capacity_forecast" + \
                                   "(newMineid,mineName,mineCountry,state,mineRegion,mineStage,"+\
                                   "capacityType,CommodityByCapacity,capacityYear,capacity,capacityUnit,source,Mineid) VALUES ("

                    sqlStatement = sqlStatement_capacity
                    for i in range(len(mines['Capacity year'])):
                        if debugMode:
                            print "----> " + str(i),mines['Capacity year'][i],mines['Capacity'][i],mines['Capacity unit'][i]

                        CommodityByCapacity = commodities
                        capacityType = mines['Capacity type'][i]
                        capacityYear = mines['Capacity year'][i]
                        capacity = mines['Capacity'][i]
                        source = mines['Capacity Source'][i]

                        if mines['Capacity unit'][i] == "MMT" or mines['Capacity unit'][i] == "MT":
                            capacityUnit = "MTPA"
                        else:
                            capacityUnit = mines['Capacity unit'][i]

                        if capacityType == 'ROM Production':
                            capacityType = 'ROM Capacity'
                            CommodityByCapacity = ''
                            if not capacityUnit == "MTPA":
                                capacityFactor = mining_units(mCur, capacityUnit, "MMT", True)
                                capacity = float(mines['Capacity'][i]) * float(capacityFactor)
                                capacityUnit = "MTPA"

                        sqlStatement += mining_base_data+"'"+capacityType+"','"+CommodityByCapacity+"',"+\
                                        str(capacityYear)+","+str(capacity)+",'"+capacityUnit+"'"
                        if source.count("'") > 0:
                            sqlStatement += ', "%s"' % source
                        else:
                            sqlStatement += ", '%s'" % source
                        sqlStatement += ', %s)' % Mineid
                        if debugMode:
                            print "CAPACITY FORECAST"
                            print sqlStatement
                            print ""
                        mCur.execute(sqlStatement)
                        mCur.execute("commit;")
                        sqlStatement = sqlStatement_capacity
                # ------------------------------------------------------------------------------------------
                # Update the reserves forecast table
                # HOWEVER, we only look at the last year.
                # Should we fill in the reserves number until the discount year?
                if debugMode:
                    print "RESERVES FORECAST"
                    print 'reservesFound:', reservesFound
                    print '\n'
                if len(mines['Reserve year']) > 1 and not reservesFound :
                    # reserves
                    # resources
                    sqlStatement_reserve = "INSERT INTO " + prefixDB + "mining_reserves_forecast (newMineid,mineName,mineCountry,state,mineRegion,mineStage,reserveType,"
                    #sqlStatement_reserve += "CommodityByReserve,reserveYear,reserve,reserveUnit,source,Mineid) VALUES ("
                    sqlStatement_reserve += "reserveYear,reserve,reserveUnit,source,Mineid) VALUES ("

                    sqlStatement = sqlStatement_reserve
                    for i in range(len(mines['Reserve year']) - 1):
                        if debugMode:
                            print "----> " + str(i),mines['Reserve year'][i],mines['Reserves'][i],mines['Reserve unit'][i]
                        reserveType = "Total Reserves"
                        CommodityByReserve = commodities.strip()[:50]
                        reserveYear = mines['Reserve year'][i]
                        reserve = mines['Reserves'][i]
                        if mines['Reserve unit'][i] == "MTPA":
                            reserveUnit = "MMT"
                        else:
                            reserveUnit = mines['Reserve unit'][i]
                            reserveFactor = mining_units(mCur, reserveUnit, "MMT", True)
                            reserve = float(mines['Reserves'][i]) * float(reserveFactor)
                            reserveUnit = "MMT"
                        source = mines['Reserves Source'][i]
                        #
                        #sqlStatement += mining_base_data+"'"+reserveType+"','"+CommodityByReserve+"',"+str(reserveYear)+","+str(reserve)+",'"+reserveUnit+"'"

                        sqlStatement += mining_base_data + "'" + reserveType + "'," + str(reserveYear) + "," + str(reserve) + ",'" + reserveUnit + "'"
                        if source.count("'") > 0:
                            sqlStatement += ', "%s"' % source
                        else:
                            sqlStatement += ", '%s'" % source
                        sqlStatement += ', %s)' % Mineid
                        if debugMode or debugReserves:
                            print "RESERVES FORECAST"
                            print sqlStatement
                            print '\n'
                        mCur.execute(sqlStatement)
                        mCur.execute('COMMIT')
                        sqlStatement = sqlStatement_reserve
                # ------------------------------------------------------------------------------------------
                # Update the resources forecast table based on the values in the array
                # All are in the array
                if len(mines['Resource Year']) and not resourcesFound :
                    # resources
                    sqlStatement_resource = "INSERT INTO " + prefixDB + "mining_resource_forecast (newMineid,mineName,mineCountry,state,mineRegion,mineStage,"
                    #sqlStatement_resource += "resourceType,CommodityByResource,resourceYear,resource,resourceUnit,source,Mineid) VALUES ("
                    sqlStatement_resource += "resourceType,resourceYear,resource,resourceUnit,source,Mineid) VALUES ("

                    sqlStatement = sqlStatement_resource
                    for i in range(len(mines['Resource Type']) - 1):
                        if debugMode:
                            print "----> " + pws(str(i),5,'R'),pws(str(i),20,mines['Resource Type'][i]),\
                                  pws(str(i),6),pws(fwc(str(round(float(mines['Resource Year'][i]),6)).strip()),15,'R'),mines['Resource %'][i]
                        resourceType = "Total Resources"
                        CommodityByResource = commodities.strip()[:50]
                        resourceYear = mines['Resource Year'][i]
                        resource = mines['Resource %'][i]
                        resourceUnit = mines['Resource unit'][i]
                        source = mines['Resource Source'][i]

                        if mines['Resource unit'][i] == "MTPA":
                            resourceUnit = "MMT"
                        else:
                            resourceUnit = mines['Reserve unit'][i]
                            resourceFactor = mining_units(mCur, resourceUnit, "MMT", True)
                            resource = float(mines['Resource %'][i]) * float(resourceFactor)
                            resourceUnit = "MMT"
                        #
                        sqlStatement += mining_base_data+"'"+resourceType+"',"+str(resourceYear)+","+str(resource)+",'"+resourceUnit+"'"

                        if source.count("'") > 0:
                            sqlStatement += ', "%s"' % source
                        else:
                            sqlStatement += ", '%s'" % source
                        sqlStatement += ', %s)' % Mineid
                        if debugMode:
                            print "RESOURCE FORECAST"
                            print sqlStatement
                            print ""
                        mCur.execute(sqlStatement)
                        mCur.execute("commit;")
                        sqlStatement = sqlStatement_resource
                # ------------------------------------------------------------------------------------------
                # Update the production forecast table based on the values in the array
                if len(mines['Production Year']):
                    if debugMode:
                        print "="*30
                        print ""
                        print ""
                        print "mines['Production Year']:", mines['Production Year']
                        print "LENGTH: " + str(len(mines['Production Year']))
                        print "mines['Production Value']:", mines['Production Value']
                        print "LENGTH: " + str(len(mines['Production Value']))
                        print "mines['Production unit']:", mines['Production unit']
                        print "LENGTH: " + str(len(mines['Production unit']))
                        print "mines['Production Source']:", mines['Production Source']
                        print "LENGTH: " + str(len(mines['Production Source']))
                        print "="*30
                        print "mines['Production Type']:", mines['Production Type']
                        print "LENGTH: " + str(len(mines['Production Type']))
                        print "="*30
                    sqlStatement_production = "INSERT INTO " + prefixDB + "mining_production_forecast (newMineid,mineName,mineCountry,state,mineRegion,mineStage,productionType,"
                    sqlStatement_production += "productionYear,productionValue,productionUnit,source,Mineid,session_key) VALUES ("

                    sqlStatement = sqlStatement_production
                    mining_baseDT.append('c')
                    mining_baseDT.append('c')
                    mining_baseDT.append('i')
                    mining_baseDT.append('i')
                    mining_baseDT.append('c')
                    mining_baseDT.append('c')
                    if debugMode:
                        print ""
                        print "len(mines['Production Year']):", len(mines['Production Year'])
                        print ""
                    for i in range(len(mines['Production Year'])):
                        if debugMode:
                            print "----> " + pws(str(i),5,'R'),pws(str(mines['Production Year'][i]),6),pws(fwc(str(float(mines['Production Value'][i])).strip()),15,'R'),mines['Production Source'][i]
                        productionType = "ROM Production"
                        productionByCommodity = commodities
                        productionYear = mines['Production Year'][i]
                        if 'OIL SANDS' in commodities.upper():
                            if mines['Production unit'][i] == "MBPD":
                                prodFactor = 1.0
                            else:
                                prodUnit = mines['Production unit'][i]
                                prodFactor = mining_units(mCur,prodUnit,"MBPD",True)
                            productionUnit = "MBPD"
                        else:
                            if mines['Production unit'][i] == "MMT" or mines['Production unit'][i] == "MT":
                                productionUnit = "MTPA"
                                prodFactor = 1
                            else:
                                # translate back into MTPA
                                productionUnit = mines['Production unit'][i]
                                prodFactor = mining_units(mCur,productionUnit,"MMT",True)
                                productionUnit = "MTPA"
                        productionValue = float(mines['Production Value'][i]) * float(prodFactor)

                        source = mines['Production Source'][i]
                        sqlStatement += mining_base_data+"'"+productionType+"',"+str(productionYear)+","+str(productionValue)+",'"+productionUnit+"'"

                        if source[-1] == '\\':
                            source += ' '

                        if source.count("'") > 0:
                            sqlStatement += ', "%s"' % source
                        else:
                            sqlStatement += ", '%s'" % source

                        sqlStatement += ', %s,"%s")' % (Mineid,mSession_key)

                        try:
                            mCur.execute(sqlStatement)
                            if debugMode:
                                print 'sqlStatement:', sqlStatement
                        except:
                            sqlStatement = unicode(sqlStatement.encode('utf-8').strip(), errors='ignore')
                            if debugMode:
                                print 'sqlStatement:', sqlStatement
                            mCur.execute(sqlStatement)
                        mCur.execute("commit;")
                        sqlStatement = sqlStatement_production
                    param_vals = (productionYear, NewMineId, mSession_key)
                    if updateParamTrk:
                        mCur.execute('UPDATE mining_param_track SET mineEndYear=%s WHERE NewMineId=%s AND sessionKey=%s', param_vals)
                        mCur.execute('COMMIT')
                prevEL4 = ""
                prevMineId = 0
                if debugMode:
                    print "%-" * 30
                    print len(error_log[0]), error_log[0]
                    print len(error_log[1]), error_log[1]
                    print len(error_log[2]), error_log[2]
                    print len(error_log[3]), error_log[3]
                    print len(error_log[4]), error_log[4]
                    print len(error_log[5]), error_log[5]
                    print len(error_log[6]), error_log[6]
                for ii in range(0,len(error_log[4])):
                    if ii > 0:
                        if thisWasModelled:
                            commodity_status = "MODELLED - "
                        else:
                            commodity_status = "NOT MODELLED - "
                        #if not prevEL4 == error_log[4][ii]:
                        save_error_log(mCur,conn,NewMineId,Mineid,mineName,mineCountry,state,mineRegion,commodity_status + error_log[2][ii],key_commodity,error_log[1][ii],mSession_key,error_log[4][ii],eSymbol,error_log[5][ii],error_log[6][ii])
                        #prevEL4 = error_log[4][ii]
                # ------------------------------------------------------------------------------------------
                if debugMode:
                    print '\n\n'
                # RESET
                firstTime = True
                #
                #pt_ran = False
                octr_ran = False
                rr_ran = False
                # evaluate the asset
                # ------------------------------------------------------------------------------------------
            mCur.close()
            del mines
            del error_log
            recsProcessed += 1
            if mTotRecs > 0:
                print ""
                print "Record " + str(recsProcessed) + "/" + str(mTotRecs) + \
                      " -------> " + str((recsProcessed/mTotRecs)*100)+ "%"
                print "Modelled: " + str(modelled) + "  ------  Not Modelled: " + str(not_modelled) + \
                      " -      Total time: "+str((time.time() - runningTime)/60)
        #==================================================================================================================================================================
        if mTotRecs > 0:
            print ""
            print "Record " + str(recsProcessed) + "/" + str(mTotRecs) + \
                  " -------> " + str((recsProcessed/mTotRecs)*100)+ "%"
            print "Modelled: " + str(modelled) + "  ------  Not Modelled: " + str(not_modelled) + \
                  " -      Total time: "+str((time.time() - runningTime)/60)

        for commodity in modelled_commod.keys():
            print '%s/%s %s mines modelled' % (modelled_commod[commodity], all_commodities[commodity], commodity)
        for commodity in not_modelled_commod.keys():
            print '%s/%s %s mines not modelled' % (not_modelled_commod[commodity], all_commodities[commodity], commodity)

        for key in all_commodities.keys():
            if debugMode:
                print "Key: " + key
            ts = time.time()
            st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            if modelled_commod.has_key(key):
                num_modelled = modelled_commod[key]
            if not_modelled_commod.has_key(key):
                num_not_modelled = not_modelled_commod[key]
            # find the modelled number
            sqlStatement = "INSERT INTO mining_metrics (session_key,commodity,modelled,not_modelled,add_by) VALUES " + param_symbol_mm
            mCur1.execute(sqlStatement,(mSession_key,key,num_modelled,num_not_modelled,userName))
            mCur1.execute('COMMIT')
        conn.close()
        timeEnded = datetime.now()
        dt = timeEnded.timetuple()
        mProgComment += "\n"+"Mining models Program ended at :" + get_datetime() +"\n"
        mProgComment += "\nTotal time: "+str((time.time() - runningTime)/60)
        out_fname = "MINING_MODELS_"+"_"+get_julian_date()+"_"+get_time_string()
        print mProgComment
        if lUpdateRemote:
            update_forecast(mSession_key)
        if exportData:
            update_servers('mining', export_tables=True, import_tables=True)
        fo = open(mOutputLogsDir + out_fname +".txt","w")
        fo.write(mProgComment+"\n")
        fo.flush()
        fo.close()
    else:
        if lUpdateRemote:
            update_forecast(mSession_key)
#========================================================================================================================================================================


if __name__=='__main__':
    dev_mode    = True
    export_data = False
    debug_mines = [148347]
    mining_main(export_data, dev_mode, debug_mines)