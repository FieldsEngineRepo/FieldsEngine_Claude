import win32com.client
import openpyxl
import sys
import subprocess
import datetime as dt
import implied_price_report as ip
from globaldata import *
from cmd_main import get_time



def get_deals_id(in_curr):
    in_curr.execute('SELECT MAX(run_id) FROM deals')
    run_id = in_curr.fetchone()[0]
    return run_id


def convert_values_to_null(in_curr):
    sql_update = 'UPDATE deals SET implied_oil=NULL, implied_gas=NULL, value_diff=NULL WHERE calc_implied_prices=1 AND deal_value IS NULL'
    in_curr.execute(sql_update)
    in_curr.execute('COMMIT')


def get_export_data(in_curr):
    convert_values_to_null(in_curr)
    sql_select  = 'SELECT asset_id, asset_name, country, region, asset_status, deal_id, implied_npv, implied_oil, implied_gas, value_diff '
    sql_select += 'FROM deals WHERE calc_implied_prices=1'
    in_curr.execute(sql_select)
    deals_data = in_curr.fetchall()
    return deals_data


def export_data(out_curr, deals_data):
    add_date = get_add_date()
    out_curr.execute('TRUNCATE TABLE tblImpliedOilPriceOutput')
    out_curr.execute('COMMIT')
    for asset_id, asset_name, country, region, asset_status, deal_id, implied_npv, implied_oil, implied_gas, value_diff in deals_data:
        if implied_oil:
            implied_oil = round(implied_oil, 2)
        if implied_gas:
            implied_gas = round(implied_gas, 2)
        params = (asset_id, asset_name, country, region, asset_status, deal_id, implied_npv, implied_oil, implied_gas, value_diff, add_date)
        sql_update  = 'INSERT INTO tblImpliedOilPriceOutput (Asset_ID, Asset_Name, Country, Region, Asset_Status, Deal_ID, [Implied_NPV ($)], '
        sql_update += '[Implied_Oil_Price (US$/bbl)], [Implied_Gas_Price (US$/mcf)], [Deal Differential (premium/discount)], OUTPUT_Date) '
        sql_update += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        out_curr.execute(sql_update, params)
    out_curr.execute('COMMIT')


def get_deal_year(effective_date, announced_date):
    deal_year = 0
    try:
        if effective_date:
            if '/' in effective_date:
                effective_date_list = effective_date.split('/')
                effective_month = int(effective_date_list[0])
                effective_year = int(effective_date_list[2])
                if effective_month > 6:
                    deal_year = effective_year + 1
                else:
                    deal_year = effective_year
            elif '-' in announced_date:
                pass
        else:
            if '/' in announced_date:
                announced_date_list = announced_date.split('/')
                announced_month = int(announced_date_list[0])
                announced_year = int(announced_date_list[2])
                if announced_month > 6:
                    deal_year = announced_year + 1
                else:
                    deal_year = announced_year
            elif '-' in announced_date:
                pass
    except:
        pass
    return deal_year


def get_modelled_assets(curr):
    curr.execute('SELECT DISTINCT asset_id FROM last_session_key WHERE model_status="modelled"')
    asset_list = [asset[0] for asset in curr.fetchall()]
    return asset_list


def get_import_data(out_curr, debug=False):
    sql_select = \
    """
    SELECT AssetID, [Asset/Target], Country, Region, [Asset Status], DealID, [Deal Type], [Deal Value (US$ mil)], [Deal Effective date], [Announced Date], [Deals Financials -  Acquired] 
    FROM tblImpliedOilPriceInput WHERE NOT [Asset Status] IN ('Unlicensed', 'Licensed', 'Split', 'Unitized') AND ExtractDate = (SELECT MAX(ExtractDate) FROM tblImpliedOilPriceInput)
    AND NOT ([Asset/Target] LIKE 'Other %' OR [Asset/Target] LIKE 'Others %') AND NOT DealID IN (1709667,1709697,901738,1072655,1072772,241573,237446,244129,1734569,1102993) 
    """
    if debug: print sql_select
    out_curr.execute(sql_select)
    deals_data = out_curr.fetchall()
    processed_data = ()
    deals_data_count = len(deals_data)
    deals_data_num = 1
    print deals_data
    for data_row in deals_data:
        print '{}/{}'.format(deals_data_num, deals_data_count)
        processed_row = ()
        for data_point in data_row:
            if isinstance(data_point,str):
                data_point = unicode(data_point.strip(), errors='ignore')
            processed_row += (data_point,)
        processed_data += (processed_row,)
        deals_data_num += 1
    return processed_data

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def clear_deals_table(in_curr):
    in_curr.execute('TRUNCATE deals')
    in_curr.execute('COMMIT')


def process_deal_value(deal_value):
    if deal_value in [None, 'None', 'NULL', '']:
        deal_value = None
    else:
        deal_value = round(float(deal_value) * 1000000, 2)
    return deal_value


def process_date(date):
    if date is None:
        processed_date = date
    else:
        processed_date = str(date).split()[0]
    return processed_date


def process_deal_stake(deal_stake):
    if deal_stake is None:
        deal_stake = None
    else:
        deal_stake = round(float(deal_stake) / 100, 2)
    return deal_stake


def get_parent_id(in_curr, asset_id):
    sql_select = 'SELECT IF(asset_relation="Child", assoc_asset_id, asset_id) AS parent_id FROM assets WHERE asset_id=%s' % asset_id
    in_curr.execute(sql_select)
    try:
        parent_id = in_curr.fetchone()[0]
    except:
        parent_id = asset_id
    return parent_id


def get_implied_npv(deal_value, deal_stake):
    if deal_stake in [0, None] or deal_value in [0, None]:
        implied_npv = 0
    else:
        implied_npv = round(float(deal_value) / float(deal_stake), 2)
    return implied_npv


def get_parent_data(in_curr, parent_id):
    in_curr.execute('SELECT asset_name, country, region, status FROM assets WHERE asset_id=%s' % parent_id)
    parent_data = in_curr.fetchone()
    return parent_data


def import_deals_sql(in_curr, deals_data, detailed=False, debug=False):
    clear_deals_table(in_curr)
    run_id    = get_run_id(in_curr)
    edit_date = get_add_date().split()[0]
    # edit_date = 'null' #comment after Debug
    sql_statement  = 'INSERT INTO deals (asset_id, asset_name, country, region, asset_status, deal_id, deal_type, deal_value, effective_date, announced_date, deal_stake, '
    sql_statement += 'parent_id, parent_asset_name, parent_country, parent_region, parent_status, deal_year, data_source, run_id, edit_date) '
    sql_statement += 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    for asset_id, asset_name, country, region, asset_status, deal_id, deal_type, deal_value, eff_date, ann_date, deal_stake in deals_data:
        deal_value  = process_deal_value(deal_value)
        eff_date    = process_date(eff_date)
        ann_date    = process_date(ann_date)
        deal_stake  = process_deal_stake(deal_stake)

        parent_id   = get_parent_id(in_curr, asset_id)
        try:
            parent_asset_name, parent_country, parent_region, parent_status = get_parent_data(in_curr, parent_id)
        except:
            continue
        deal_year   = get_deal_year(eff_date, ann_date)

        data_source = 'EST: Forecast Engine'
        params  = (asset_id,asset_name,country,region,asset_status,deal_id,deal_type,deal_value,eff_date,ann_date,deal_stake)
        params += (parent_id,parent_asset_name,parent_country,parent_region,parent_status,deal_year,data_source,run_id,edit_date)
        in_curr.execute(sql_statement,params)
    sql_update  = 'UPDATE deals AS a, (SELECT deal_id, COUNT(DISTINCT parent_id) AS parent_asset_count FROM deals GROUP BY deal_id) AS b '
    sql_update += 'SET a.parent_asset_count=b.parent_asset_count WHERE a.deal_id=b.deal_id'
    in_curr.execute(sql_update)
    check_if_calc(in_curr)
    in_curr.execute('COMMIT')
    if not detailed:
        sql_select = 'SELECT DISTINCT parent_id FROM deals WHERE calc_implied_prices=1'
    else:
        sql_select = 'SELECT DISTINCT parent_id FROM deals WHERE calc_implied_prices=1 AND NOT asset_id IN (SELECT DISTINCT asset_id FROM detailed_models)'
    in_curr.execute(sql_select)
    deals_assets = list(set([str(data[0]) for data in in_curr.fetchall()]))
    return deals_assets


def check_if_calc(in_curr):
    sql_update = 'UPDATE deals SET calc_implied_prices=0 WHERE id > 0'
    in_curr.execute(sql_update)
    in_curr.execute('COMMIT')
    sql_update  = 'UPDATE deals SET calc_implied_prices=1 WHERE NOT asset_status="Discovered" AND deal_type="Asset Transactions" '
    sql_update += 'AND NOT deal_stake IS NULL AND parent_asset_count=1 AND (NOT effective_date IS NULL OR NOT announced_date IS NULL) '
    sql_update += 'AND asset_id IN (SELECT DISTINCT asset_id FROM assets WHERE data_source="Engine" AND asset_relation="Parent")'
    in_curr.execute(sql_update)


def create_deals_models(deals_assets):
    asset_str = ','.join(deals_assets)
    # asset_str='642385,393477,1800484,1856373,925499,254738,851255,849256,393479,385215,909895,156328,258522,739314,734667,913362,523129,523128,326096,918395,326090,570813,723038,740485,867424,134036,621638,852331,133563,631022,907179,628597,636330,1775924,734441,388698,851645,738800,722303,737364,523058,897783,410410,410411,410412,625955,252555,734250,135738,530312,129092,738145,129786,376812,819649,521878,261518,740806,129300,921774,322239,1512739,498231,129878,1651143,136014,135368,258186,627957,848265,737750,237703,747241,851261,729792,960448,878958,642184,736717,208851,208850,747503,851307,879844,1594087,134187,851301,361903,270045,738381,136081,225626,270233,3820096,904567,256347,133694,778963,267681,913515,322657,135966,921780,136068,522276,237638,1636792,897352,253176,254071,901229,1010674,383959,383957,737682,254706,254705,261079,1820848,746753,738517,734521,781403,257273,734951,257277,742238,897102,738684,523153,735331,282188,738966,738961,625349,738787,999361,622042,269648,737879,740444,637787,135541,498265,926327,319661,319660,630046,999339,248692,383604,398714,917991,248735,128949,220583,465677,844444,734413,502343,268682,253354,319947,739420,1858766,257859,136119,319403,319402,319406,128795,320961,261520,851344,256722,136590,922456,740494,521116,136598,208483,526648,897302,320686,865572,637743,362119,414580,329078,282251,414585,135438,848548,134822,282258,135808,322005,740714,737700,734121,136182,734875,135802,851644,851332,844691,734648,393765,134627,738672,734224,134230,282437,630988,282434,630986,321223,996763,739089,914032,499336,319234,843762,729239,322723,1027111,322721,734013,501512,253432,252419,849935,252415,530001,849931,849932,134437,643255,740390,209110,740394,747059,241443,383647,241447,734975,261747,220637,383886,734906,358055,318050,358057,358056,851652,734264,734518,851278,880796,738819,880795,737761,642601,626552,740471,734306,880817,2031026,495197,253722,1797480,746833,778969,271695,741284,736791,270759,270758,589061,270751,252505,256172,323890,741579,1563271,845149,323512,133846,129682,257860,136579,747975,267601,282215,851273,851272,851271,851276,741458,738476,925949,625291,134270,327347,736708,630785,729909,734598,747491,318890,393788,642742,397061,393424,844177,1027655,381680,253168,237232,330387,256767,207988,135399,987994,747261,394021,136381,254067,254066,128738,338560,743662,269807,568894,734498,382246,136208,921759,738695,397923,523147,386939,741848,408668,735511,534740,134797,629974,627877,637587,858141,324287,1511381,746967,322260,282312,318025,845781,1607784,261012,920767,257968,208710,270946,583006,649871,604085,734339,742470,381127,734721,257716,534962,846664,625156,526984,747635,254242,734117,637176,254531,1515827,628092,1563300,819367,908513,923361,1027161,1532089,135421,399885,256720,925511,738483,737045,912023,253125,254022,271965,271964,393774,851323,254182,496095,851246,851247,630291,851682,135883,129559,324919,630109,628895,129928,129885,271569,271207,271205,271208,729719,254757,911035,134591,729204,918729,533592,319229,734389,253365,880958,1029715,133480,392857,530017,1543607,134115,134116,338555,627307,133645,1788675,921114,257444,257443,734931,465627,532607,735002,851662,851664,557114,739069,523177,734274,851669,734505,531560,627374,271193,397650,462405,629809,207987,637385,737912,780354,386592,848181,257692,729119,741514,736780,496509,322258,129776,1783959,533588,911662,322252,271423,394255,851269,959860,959594,740210,319616,921239,135308,741031,258044,270038,134640,695600,781739,924296,628902,134647,730180,851289,737678,325813,325815,209095,261275,136141,135462,136143,376837,880569,1016258,747645,324814,387377,134800,742455,282177,681063,742451,862468,851303,739783,134410,135418,851295,849949,849945,738344,845734,133601,134095,777888,134097,851291,338459,136285,625609,256804,207448,135460,851293,364138,922548,851292,361906,134730,630965,734977,851629,134737,424592,216488,255907,739301,216483,216482,1651138,920769,527721,625424,624565,530065,523130,738921,134383,1012127,735308,642890,630158,134784,1012125,1645896,398296,248689,208707,208704,241461,241460,505113,568877,208709,739159,913717,738259,411018,637460,1748437,734325,896341,1225340,252546,253624,568888,739407,530242,1026742,1524359,583131,748005,959573,738051,746731,1645422,261133,562859,1622749,261137,253934,135521,216503,260849,741497,535076,216504,734856,535077,136003,681435,739271,135455,338497,237713,642840,465268,256734,392688,392684,208844,623780,851314,851316,851251,733941,208336,734665,208335,135735,578342,630119,129267,254347,254342,390945,225635,582743,271217,318674,338300,739994,252863,1805391,739610,628202,256832,1029815,253419,1276873,1026270,636669,1651581,728820,253416,1227351,728730,133679,630233,642994,206288,622490,338548,1630507,642262,921598,851670,866487,133512,851679,922158,630706,257265,133583,864300,135352,907650,271180,134776,733976,1645095,134773,734049,734861,734365,1903706,629836,852118,1014245,741505,386562,921856,777308,256731,533595,466134,322242,128832,851685,252609,1012066,624074,129909,1479808,734818,282599,729958,208714,319410,134398,851299,530359,381101,1527618,2044415,381105,381104,209089,330302,128788,135380,851656,261147,534514,261149,630408,130129,779360,879301,257285,257281,129534,135771,880792,563485,642492,282249,849959,880791,849953,849950,282244,636293,747032,733991,207470,737673,321800,321801,1516169,747139,385440,851250,625575,1601129,630573,267783'
    # command = '%py2% %engine_drive%:\\TitanJobs\\Titan1\\python_code\\cmd_main.py '
    # command = 'py -2 D:\\TitanJobs\\Titan1\\python_code\\cmd_main.py '
    # command += 'create_model -deal- -asid-%s' % asset_str
    # os.system(command)
    command = [
        "py",
        "-2",
        r"D:\TitanJobs\Titan1\python_code\cmd_main.py",
        "create_model",
        "-deal-",
        "-asid-%s" % asset_str
    ]
    subprocess.call(command)



def run_implied_price_macro():
    print('Running Implied Price Macro...')
    os.system(TASK_DIR + 'Commands\\calc_implied_prices.bat')


def import_deals(source, external_server=False, calc_detailed_models=False, debug=False):
    in_conn = get_connection()
    in_curr = in_conn.cursor()
    out_conn = get_connection(server='sql_server', database='OGEngineDataExtract', external=external_server)
    out_curr = out_conn.cursor()
    deals_assets = []
    if source == 'file':
        deals_assets = import_deals_excel(in_curr)
    elif source == 'server':
        deals_data = get_import_data(out_curr, debug=debug)
        deals_assets = import_deals_sql(in_curr, deals_data, detailed=calc_detailed_models, debug=debug)
    out_curr.close()
    out_conn.close()
    in_curr.close()
    in_conn.close()
    return deals_assets


def export_deals(external_server=False):
    in_conn = get_connection()
    in_curr = in_conn.cursor()
    out_conn = get_connection(server='sql_server', database='OGEngineDataExtract', external=external_server)
    out_curr = out_conn.cursor()
    deals_data = get_export_data(in_curr)
    export_data(out_curr, deals_data)
    in_curr.close()
    in_conn.close()
    out_curr.close()
    out_conn.close()


def process_deals_assets(import_deals_data=False, import_source='server', create_models=False, calc_implied_prices=False, export_deals_data=False, generate_report=False, external=False, detailed=False, debug=False):
    conn = get_connection()
    curr = conn.cursor()
    if import_deals_data:
        print 'Importing deals data...'
        deals_assets = import_deals(source=import_source, external_server=external, calc_detailed_models=detailed, debug=debug)
        if create_models:
            print 'Creating models ...'
            print len(deals_assets)
            # deals_assets=''
            create_deals_models(deals_assets)
    if calc_implied_prices:
        print 'Calculating implied prices ...'
        run_implied_price_macro()
    if export_deals_data:
        print 'Exporting deals data ...'
        export_deals(external)
    if generate_report:
        print 'Generating implied price report ...'
        ip.main()
    curr.close()
    conn.close()


if __name__=='__main__':
    process_deals_assets(import_deals_data=True, create_models=False, calc_implied_prices=False, export_deals_data=False, generate_report=False, external=True, detailed=False, debug=True)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
