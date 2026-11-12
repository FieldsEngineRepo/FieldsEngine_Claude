import urllib2
import requests
import urllib
import re
import sys
import os
import urlparse
import mechanize
import pyshark
import cookielib
import shutil
import csv
import pandas as pd

from globaldata import *
from well_list import *
from numpy.random import randint
from time import sleep
from lxml import etree
from bs4 import BeautifulSoup
from zipfile import ZipFile

from selenium import webdriver
from sqlalchemy import create_engine
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import presence_of_element_located


# Function configuration data --------------------------------------------------------------------------------------------------------------------------------------------

US_WELL_DATA_DIR = 'D:\\GlobalData\\Data\\wells\\csv\\'

PROD_DATA_DIR = US_WELL_DATA_DIR + 'Load\\'

TABLE_NAME_TEMP = '{}_Well_Production_Data'

TABLE_NAME = 'OH_2017_Production'

CSV_PROD_DIR = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\CO_Well_Data\\prod_reports\\add_source_year\\'

CA_ACCESS_DIR = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\CA_Well_Data\\prod_data\\unprocessed\\'

MONTH_NUMS = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '_ga=GA1.3.2095242512.1525737621; _gid=GA1.3.1361361671.1525737621',
    'Host': 'www.depreportingservices.state.pa.us',
    'Origin': 'http://www.depreportingservices.state.pa.us',
    'Referer':'http://www.depreportingservices.state.pa.us/ReportServer/Pages/ReportViewer.aspx?%2fOil_Gas%2fOil_Gas_Well_Production',
    'User-agent':
    'Mozilla/5.0 Windows NT 10.0; Win64; x64 AppleWebKit/537.36 KHTML, like Gecko Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.64',
    'X-MicrosoftAjax': 'Delta=true'
}

URL_DIR  = 'ftp://ftp.consrv.ca.gov/pub/oil/online_data/production_injection_data/Pre-2018_Data_Format/'

OUT_DIR  = WELL_DATA_DIR + 'CA_Well_Production\\'

WEBDRIVE_CONFIG = {
    'un_prod': {
        'url'  : 'http://data.un.org/Data.aspx?d=EDATA&f=cmID%3aAO',
        'click': [
            ('xpath', "//a[@title='Download this view of the data series']", 0),
            ('id', 'downloadCommaLink', 1)
        ]
    },
    'tx_prod': {
        'url'  : 'http://webapps2.rrc.texas.gov/EWA/wellboreQueryAction.do',
        'click': [
            ('xpath', "//select[@name='searchArgs.wellTypeArg']/option[text()='{}']", 0),
            ('xpath', "//select[@name='searchArgs.districtCodeArg']/option[text()='{}']", 0),
            ('xpath', "//input[@type='submit' and @value='Submit']", 2),
            ('xpath', "//select[@name='pager.pageSize']/option[text()='View All']", 2),
            ('xpath', "//input[@type='button' and @value='Download']", 1)
        ]
    },
    'pa_prod': {
        'url'  : 'http://www.depreportingservices.state.pa.us/ReportServer/Pages/ReportViewer.aspx?%2fOil_Gas%2fOil_Gas_Well_Production',
        'click': [
            ('id', 'ReportViewerControl_ctl04_ctl03_ddDropDownButton', 0),
            ('xpath', '//*[@id="ReportViewerControl_ctl04_ctl05_ddValue"]/option[3]', 0),
            ('id', 'ReportViewerControl_ctl04_ctl00', 0)
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


OK_COUNTIES = [
    "001",
    "003",
    "005",
    "007",
    "009",
    "011",
    "013",
    "015",
    "017",
    "019",
    "021",
    "023",
    "025",
    "027",
    "029",
    "031",
    "033",
    "035",
    "037",
    "039",
    "041",
    "043",
    "045",
    "047",
    "049",
    "051",
    "053",
    "055",
    "057",
    "059",
    "061",
    "063",
    "065",
    "067",
    "069",
    "071",
    "073",
    "075",
    "077",
    "079",
    "081",
    "083",
    "085",
    "087",
    "089",
    "091",
    "093",
    "095",
    "097",
    "099",
    "101",
    "103",
    "105",
    "107",
    "109",
    "111",
    "113",
    "115",
    "117",
    "119",
    "121",
    "123",
    "125",
    "127",
    "129",
    "131",
    "133",
    "135",
    "137",
    "139",
    "141",
    "143",
    "145",
    "147",
    "149",
    "151",
    "153"
]

UN_ENERGY_CODES = [
    'AO',
    'AW',
    'AT',
    'AV',
    'BS',
    'BJ',
    'BD',
    'BI',
    'AL',
    'BT',
    'PU',
    'BG',
    'LB',
    'BB',
    'CH',
    'CT',
    'OK',
    'OG',
    'CC',
    'CR',
    'DG',
    'DS',
    'EC',
    'EA',
    'WF',
    'RF',
    'FW',
    'GK',
    'DL',
    'GJ',
    'GG',
    'EG',
    'CL',
    'ST',
    'HF',
    'EH',
    'IW',
    'JF',
    'LN',
    'LP',
    'LU',
    'MO',
    'MW',
    'NP',
    'NG',
    'GL',
    'EN',
    'ZJ',
    'ZD',
    'ZG',
    'OS',
    'OB',
    'CP',
    'OH',
    'KR',
    'OL',
    'PP',
    'BO',
    'VW',
    'PW',
    'BC',
    'PT',
    'BP',
    'PK',
    'FS',
    'RG',
    'ES',
    'SB',
    'ET',
    'EO',
    'EL',
    'GR',
    'UR',
    'WS',
    'EW'
]

NM_URL     = 'https://wwwapps.emnrd.state.nm.us/ocd/ocdpermitting/Data/WellDetails.aspx?api={}#general_well_info'
NM_URL2    = 'https://wwwapps.emnrd.state.nm.us/ocd/ocdpermitting/Data/ProductionSummaryPrint.aspx?report=excel&api={}'
UT_URL     = 'https://oilgas.ogm.utah.gov/oilgasweb/live-data-search/lds-prod/prod-grid.xhtml?wellno={}'
WY_URL     = 'http://pipeline.wyo.gov/wyodall.cfm?nAPINO={0}&nApi={0}&Oops=1'
AL_URL     = 'http://www2.ogb.state.al.us/ogb/prod_report.aspx?PERMIT={}&API={}'
KY_URL     = 'https://kgs.uky.edu/kygeode/services/oilgas/prodReport.asp?viewType=txtDownload&dlmtr=comma&recNum={}&prodType={}'
UN_URL     = 'http://data.un.org/Handlers/DownloadHandler.ashx?DataFilter=cmID:{}&DataMartId=EDATA&Format=csv&c=2,5,6,7,8&s=_crEngNameOrderBy:asc,_enID:asc,yr:desc'
WV_URL     = 'http://www.wvgs.wvnet.edu/oginfo/pipeline/pipeline2.asp?txtsearchapi={}'


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Configured for PA well production--------------------------------------------------------------------------------------------------------------------------------------

class WellProdScraper(object):
    def __init__(self):
        self.url = "http://www.depreportingservices.state.pa.us/ReportServer/Pages/ReportViewer.aspx?%2fOil_Gas%2fOil_Gas_Well_Production"
        self.br = mechanize.Browser()
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.br.set_debug_http(True)
        self.br.set_debug_redirects(True)
        self.br.set_debug_responses(True)

        self.debug_mode        = False
        self.get_all_pages     = False
        self.cookies           = ''
        self.view_state        = ''''''
        self.event_validation  = ''''''
        self.new_view_state    = ''''''
        self.keep_alive_code   = ''
        self.keep_alive_url    = ''
        self.txt_value         = '''Jan 2017 (PRODUCTION: Unconventional wells)'''
        self.txt_value         = ''''''
        self.hidden_indices    = ''
        self.br.addheaders = \
            [
                ('Accept', ' */*'),
                ('Accept-Encoding', 'gzip, deflate'),
                ('Accept-Language', 'en-US,en;q=0.9'),
                ('Cache-Control', 'no-cache'),
                ('Connection', 'keep-alive'),
                ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
                ('Cookie', self.cookies),
                ('Host', 'www.depreportingservices.state.pa.us'),
                ('Origin', 'http://www.depreportingservices.state.pa.us'),
                ('Referer',
                 'http://www.depreportingservices.state.pa.us/ReportServer/Pages/ReportViewer.aspx?%2fOil_Gas%2fOil_Gas_Well_Production'),
                ('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.99'),
                ('X-MicrosoftAjax', 'Delta=true')
            ]
        self.br.headers = []
        self.controls_add = {}
        self.controls_remove = []
        self.controls_enable = []
        self.items_enable = []
        self.keep_alive_data = {}
        self.response_data = ''
        self.period_option_num = 15

    def make_response(self):
        s = BeautifulSoup(self.br.response().read(), "lxml")
        saved_form = s.find('form', id='SearchCriteriaForm').prettify()
        html = saved_form.encode('utf8')
        resp = mechanize.make_response(html, [("Content-Type", "text/html")], self.br.geturl(), 200, "OK")
        self.br.set_response(resp)

    def show_forms(self):
        for form in self.br.forms():
            print form

    def add_controls(self):
        for control, value in self.controls_add.items():
            self.br.form.new_control('hidden', control, {'value': value})
        self.br.form.fixup()

    def show_controls(self):
        for control in self.br.form.controls:
            print control.type, control.name, control.disabled

    def enable_controls(self):
        for control_name in self.controls_enable:
            ctl = self.br.form.find_control(control_name)
            ctl.disabled = False

    def remove_controls(self):
        for control_name in self.controls_remove:
            ctl = self.br.form.find_control(control_name)
            self.br.form.controls.remove(ctl)

    def show_items(self, control):
        items = self.br.form.find_control(control).get_items()
        for item in items:
            print item

    def enable_items(self):
        for control_name in self.items_enable:
            for item in self.br.form.find_control(control_name).get_items():
                item.disabled = False

    def show_response(self):
        self.response_data = self.br.response().read()
        response_items = iter(self.response_data.split('|'))
        response_params = dict(zip(response_items, response_items))
        print 'response_data:', self.response_data

    def pause(self):
        if self.debug_mode:
            _ = raw_input('continue?')
            if _ == 'n':
                sys.exit(0)

    def prepare_values(self):
        self.txt_value = ''.join(self.txt_value.split()).strip()
        self.hidden_indices = ''.join(self.hidden_indices.split()).strip()
        self.br.form.set_all_readonly(False)

    def enter_form_data(self):
        for argument, value in self.form_data.items():
            self.br.form[argument] = value

    def submit_webform(self, controls_add, controls_remove, controls_enable, items_enable, form_data):
        self.controls_add = controls_add
        self.add_controls()

        self.controls_remove = controls_remove
        self.remove_controls()

        self.controls_enable = controls_enable
        self.enable_controls()

        self.items_enable = items_enable
        self.enable_items()

        self.prepare_values()

        self.form_data = form_data
        self.enter_form_data()

        response = self.br.submit()
        self.show_response()

    def get_session_data(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("user-data-dir=selenium")

        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(self.url)
        cookie_data = driver.get_cookies()
        self.cookies = '; '.join(['{}={}'.format(cookie['name'], cookie['value']) for cookie in cookie_data])
        print cookie_data
        driver.quit()

    def get_session_codes(self):
        hex_code = {'30': '0', '7a': 'z', '7c': '|', '2e': '.', '37': '7', '36': '6', '28': '(', '61': 'a', '62': 'b',
                    '63': 'c', '64': 'd', '65': 'e', '66': 'f', '67': 'g', '68': 'h', '69': 'i', '52': 'R', '4c': 'L',
                    '25': '%', '26': '&', '20': ' ', '48': 'H', '49': 'I', '46': 'F', '47': 'G', '44': 'D', '45': 'E',
                    '42': 'B', '43': 'C', '41': 'A', '35': '5', '3b': ';', '3a': ':', '5f': '_', '5a': 'Z', '3f': '?',
                    '3d': '=', '6a': 'j', '6b': 'k', '6c': 'l', '6d': 'm', '6e': 'n', '6f': 'o', '2c': ',', '77': 'w',
                    '76': 'v', '75': 'u', '74': 't', '73': 's', '72': 'r', '71': 'q', '70': 'p', '29': ')', '79': 'y',
                    '78': 'x', '39': '9', '38': '8', '59': 'Y', '58': 'X', '55': 'U', '54': 'T', '57': 'W', '56': 'V',
                    '51': 'Q', '50': 'P', '53': 'S', '34': '4', '2d': '-', '33': '3', '2f': '/', '0a': '.', '2a': '*',
                    '0d': '.', '32': '2', '4f': 'O', '4d': 'M', '4e': 'N', '4b': 'K', '31': '1', '4a': 'J'}
        capture = pyshark.LiveCapture(interface='1')
        os.system('START /MIN %py2% %engine_drive%:\\python_code\\web_scrape\\production\\penn_webdriver.py {}'.format(self.period_option_num))
        capture.sniff(timeout=20)
        post_requests = []
        for i in range(len(capture)):
            packet = capture[i]
            try:
                post_requests.append(packet.tcp.segment_data)
            except:
                pass

        post_request_str = ''.join(post_requests)
        request_segments = post_request_str.split('7c:')
        event_validations = []
        view_states       = []
        new_view_states   = []

        for i in range(len(request_segments)):
            request = request_segments[i]
            if '5f:5f:45:56:45:4e:54:56:41:4c:49:44:41:54:49:4f:4e:' in request:
                try:
                    if request_segments[i + 1][:2] == '2f':
                        hex_chars = request_segments[i + 1].split(':')
                        hex_str = ''.join(hex_chars)
                        event_validations.append(hex_str.decode('hex'))
                except:
                    pass
            elif '5f:5f:56:49:45:57:53:54:41:54:45:' in request:
                try:
                    if request_segments[i + 1][:2] == '2f':
                        hex_chars = request_segments[i + 1].split(':')
                        hex_str = ''.join(hex_chars)
                        view_states.append(hex_str.decode('hex'))
                except:
                    pass

        if len(event_validations):
            if len(event_validations) > 1:
                print 'len(event_validations)', len(event_validations)
                for event_val in event_validations:
                    print 'event_validation:', event_val
            self.event_validation = event_validations[0]
        if len(view_states):
            if len(view_states) > 1:
                print 'len(view_states)', len(view_states)
                for view_state in view_states:
                    print 'view_state:', view_state
            self.view_state = view_states[0]

        self.view_state = self.view_state.split('|')[0]

    def scrape_prod(self, control_item=None):
        self.get_session_data()
        self.br.addheaders = \
            [
                ('Accept', ' */*'),
                ('Accept-Encoding', 'gzip, deflate'),
                ('Accept-Language', 'en-US,en;q=0.9'),
                ('Cache-Control', 'no-cache'),
                ('Connection', 'keep-alive'),
                ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
                ('Cookie', self.cookies),
                ('Host', 'www.depreportingservices.state.pa.us'),
                ('Origin', 'http://www.depreportingservices.state.pa.us'),
                ('Referer',
                 'http://www.depreportingservices.state.pa.us/ReportServer/Pages/ReportViewer.aspx?%2fOil_Gas%2fOil_Gas_Well_Production'),
                ('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.99'),
                ('X-MicrosoftAjax', 'Delta=true')
            ]
        response = self.br.open(self.url)
        self.response_data = response.read()
        if self.debug_mode:
            print '*+-*'*50
            print self.response_data
            print '*+-*'*50
        s = BeautifulSoup(self.br.response().read(), "lxml")
        saved_form = s.find('form', id='SearchCriteriaForm').prettify()

        r1 = re.compile(r"__VIEWSTATE\" value=\"/.*?\"")
        s1 = re.search(r1, self.response_data)
        self.view_state = s1.group().split('"')[2]
        r2 = re.compile(r"__EVENTVALIDATION\" value=\"/.*?\"")
        s2 = re.search(r2, self.response_data)
        self.event_validation = s2.group().split('"')[2]
        if self.debug_mode:
            print '***' * 50
            print self.view_state
            print self.event_validation
            print '***' * 50

        html = saved_form.encode('utf8')
        resp = mechanize.make_response(html, [("Content-Type", "text/html")], self.br.geturl(), 200, "OK")
        self.br.set_response(resp)
        self.br.select_form('SearchCriteriaForm')
        self.br.form.set_all_readonly(False)
        controls_add    = {'__ASYNCPOST'      : 'true',
                           'AjaxScriptManager': 'AjaxScriptManager|ReportViewerControl$ctl04$ctl00'}
        controls_remove = ['ReportViewerControl$ctl04$ctl03$divDropDown$ctl00',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl01',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl02',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl03',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl04',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl05',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl06',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl07',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl08',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl09',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl10',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl11',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl12',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl13',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl14',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl15',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl16',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl17',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl18',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl19',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl20',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl21',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl22',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl23',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl24',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl25',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl26',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl27',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl28',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl29',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl30',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl31',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl32',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl33',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl34',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl35',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl36',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl37',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl38',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl39',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl40',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl41',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl42',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl43',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl44',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl45',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl46',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl47',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl48',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl49',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl50',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl51',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl52',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl53',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl54',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl55',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl56',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl57',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl58',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl59',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl60',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl61',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl62',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl63',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl64',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl65',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl66',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl67',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl68',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl69',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl70',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl71',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl72',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl73',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl74',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl75',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl76',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl77',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl78',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl79',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl80',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl81',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl82',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl83',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl84',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl85',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$ctl86']
        controls_enable = ['ReportViewerControl$ctl11',
                           'ReportViewerControl$ctl04$ctl03$txtValue',
                           'ReportViewerControl$ctl04$ctl03$divDropDown$HiddenIndices',
                           'ReportViewerControl$ctl09$ReportControl$ctl04',
                           'ReportViewerControl$ctl04$ctl05$ddValue',
                           'ReportViewerControl$ctl04$ctl13$ddValue',
                           'ReportViewerControl$AsyncWait$HiddenCancelField',
                           'ReportViewerControl$ctl04$ctl03$ddDropDownButton',
                           'ReportViewerControl$ctl07$collapse',
                           'ReportViewerControl$ctl04$ctl07$ddValue',
                           'ReportViewerControl$ctl09$VisibilityState$ctl00',
                           'ReportViewerControl$ToggleParam$collapse']
        items_enable    = ['ReportViewerControl$ctl04$ctl09$cbNull',
                           'ReportViewerControl$ctl04$ctl11$cbNull',
                           'ReportViewerControl$ctl04$ctl05$ddValue',
                           'ReportViewerControl$ctl04$ctl07$ddValue',
                           'ReportViewerControl$ctl04$ctl13$ddValue',
                           'ReportViewerControl$ctl04$ctl13$ddValue']
        form_data       = {
                            '__EVENTVALIDATION'                                         : self.event_validation,
                            '__VIEWSTATE'                                               : self.view_state,
                            'ReportViewerControl$ctl11'                                 : 'quirks',
                            'ReportViewerControl$ctl04$ctl03$txtValue'                  : self.txt_value,
                            'ReportViewerControl$ctl04$ctl05$ddValue'                   : ['3'],
                            'ReportViewerControl$ctl04$ctl07$ddValue'                   : ['1'],
                            'ReportViewerControl$ctl04$ctl09$cbNull'                    : ['on'],
                            'ReportViewerControl$ctl04$ctl11$cbNull'                    : ['on'],
                            'ReportViewerControl$ctl04$ctl13$ddValue'                   : ['1'],
                            'ReportViewerControl$ctl04$ctl03$divDropDown$HiddenIndices' : '14',
                            'ReportViewerControl$ctl04$ctl00'                           : 'View Report',
                            'ReportViewerControl$AsyncWait$HiddenCancelField'           : 'False',
                            'ReportViewerControl$ctl09$VisibilityState$ctl00'           : 'None',
                            'ReportViewerControl$ctl09$ReportControl$ctl04'             : '100',
                            'ReportViewerControl$ToggleParam$collapse'                  : 'false',
                            'ReportViewerControl$ctl07$collapse'                        : 'false'
        }
        controls_add    = {}
        controls_remove = {}
        controls_enable = {}
        items_enable    = {}
        form_data       = {
            'viewType':         'Lease',
            'startMonth':       '01',
            'startYear':        '2018',
            'endMonth':         '01',
            'endYear':          '2018',
            'wellType':         'Both',
            'district':         'Statewide',
            'onShoreCounty':    'None Selected',
            'offShoreArea':     'None Selected',
            'fieldNameData':    'None Selected',
            'fieldRegion':      'None Selected',
            'operatorNameData': 'None Selected',
            'operatorValue':    'None Selected',
            'submit':           'Submit'
        }
        self.submit_webform(controls_add, controls_remove, controls_enable, items_enable, form_data)

        r3 = re.compile(r"NavigationCorrector_NewViewState\" value=\"/.*?\"")
        s3 = re.search(r3, self.response_data)
        self.new_view_state = s3.group().split('"')[2]
        self.get_session_codes()
        if self.debug_mode:
            print '***' * 50
            print self.view_state
            print self.event_validation
            print self.new_view_state
            print '***' * 50
        if self.get_all_pages:
            html = saved_form.encode('utf8')
            resp = mechanize.make_response(html, [("Content-Type", "text/html")], self.br.geturl(), 200, "OK")

            self.br.set_response(resp)
            self.br.select_form('SearchCriteriaForm')
            self.br.form.set_all_readonly(False)

            controls_add    = {
                '__ASYNCPOST'                                       : 'true',
                'AjaxScriptManager'                                 : 'AjaxScriptManager|ReportViewerControl$ctl09$Reserved_AsyncLoadTarget',
                'ReportViewerControl$ctl05$ctl00$CurrentPage'       : '',
                'ReportViewerControl$ctl05$ctl03$ctl00'             : '',
                'ReportViewerControl$ctl09$Reserved_AsyncLoadTarget': '',
            }
            controls_remove = ['ReportViewerControl$ctl04$ctl03$divDropDown$ctl00',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl01',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl02',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl03',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl04',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl05',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl06',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl07',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl08',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl09',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl10',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl11',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl12',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl13',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl14',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl15',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl16',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl17',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl18',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl19',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl20',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl21',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl22',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl23',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl24',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl25',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl26',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl27',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl28',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl29',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl30',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl31',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl32',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl33',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl34',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl35',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl36',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl37',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl38',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl39',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl40',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl41',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl42',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl43',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl44',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl45',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl46',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl47',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl48',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl49',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl50',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl51',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl52',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl53',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl54',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl55',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl56',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl57',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl58',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl59',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl60',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl61',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl62',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl63',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl64',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl65',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl66',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl67',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl68',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl69',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl70',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl71',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl72',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl73',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl74',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl75',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl76',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl77',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl78',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl79',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl80',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl81',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl82',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl83',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl84',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl85',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl86',
                               'ReportViewerControl$ctl04$ctl00',
                               'ReportViewerControl$ToggleParam$img',
                               'ReportViewerControl$ctl07$img',
                               'ReportViewerControl$ctl04$ctl03$ddDropDownButton']
            controls_enable = ['ReportViewerControl$ctl11',
                               'ReportViewerControl$ctl10',
                               'ReportViewerControl$ctl04$ctl03$txtValue',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$HiddenIndices',
                               'ReportViewerControl$ctl09$ReportControl$ctl04',
                               'ReportViewerControl$ctl04$ctl05$ddValue',
                               'ReportViewerControl$ctl04$ctl13$ddValue',
                               'ReportViewerControl$AsyncWait$HiddenCancelField',
                               'ReportViewerControl$ctl07$store',
                               'ReportViewerControl$ctl07$collapse',
                               'ReportViewerControl$ctl04$ctl07$ddValue',
                               'ReportViewerControl$ctl08$ClientClickedId',
                               'ReportViewerControl$ctl09$VisibilityState$ctl00',
                               'ReportViewerControl$ToggleParam$collapse',
                               'ReportViewerControl$ToggleParam$store',
                               'ReportViewerControl$ctl05$ctl00$CurrentPage',
                               'ReportViewerControl$ctl05$ctl03$ctl00',
                               'ReportViewerControl$ctl04$ctl09$txtValue',
                               'ReportViewerControl$ctl04$ctl11$txtValue',
                               'ReportViewerControl$ctl09$ScrollPosition']
            items_enable    = ['ReportViewerControl$ctl04$ctl09$cbNull',
                               'ReportViewerControl$ctl04$ctl11$cbNull',
                               'ReportViewerControl$ctl04$ctl05$ddValue',
                               'ReportViewerControl$ctl04$ctl07$ddValue',
                               'ReportViewerControl$ctl04$ctl13$ddValue']
            form_data       = { '__EVENTARGUMENT'                                           : '',
                                '__EVENTTARGET'                                             : 'ReportViewerControl$ctl09$Reserved_AsyncLoadTarget',
                                '__EVENTVALIDATION'                                         : self.event_validation,
                                '__VIEWSTATE'                                               : self.view_state,
                                'NavigationCorrector$NewViewState'                          : self.new_view_state,
                                'ReportViewerControl$ctl10'                                 : 'ltr',
                                'ReportViewerControl$ctl11'                                 : 'quirks',
                                'ReportViewerControl$ctl04$ctl03$txtValue'                  : self.txt_value,
                                'ReportViewerControl$ctl04$ctl05$ddValue'                   : ['3'],
                                'ReportViewerControl$ctl04$ctl07$ddValue'                   : ['1'],
                                'ReportViewerControl$ctl04$ctl09$cbNull'                    : ['on'],
                                'ReportViewerControl$ctl04$ctl11$cbNull'                    : ['on'],
                                'ReportViewerControl$ctl04$ctl13$ddValue'                   : ['1'],
                                'ReportViewerControl$ctl04$ctl03$divDropDown$HiddenIndices' : '14',
                                'ReportViewerControl$AsyncWait$HiddenCancelField'           : 'False',
                                'ReportViewerControl$ctl09$VisibilityState$ctl00'           : 'None',
                                'ReportViewerControl$ctl09$ReportControl$ctl04'             : '100',
                                'ReportViewerControl$ToggleParam$collapse'                  : 'false',
                                'ReportViewerControl$ctl07$collapse'                        : 'false'
            }

            if self.debug_mode:
                for control in self.br.form.controls:
                    print "type=%s name=%s disabled=%s value=%s" % (control.type, control.name, control.disabled, self.br.form[control.name])
            self.debug_mode = True
            self.submit_webform(controls_add, controls_remove, controls_enable, items_enable, form_data)

            #//*[@id="ReportViewerControl_ctl05_ctl00_TotalPages"]
            # Get total number of pages from above XPath then loop through pages extracting self.view_state, self.event_validation, and self.new_view_state from each page
            # Change form_data['__EVENTTARGET'] = 'ReportViewerControl$ctl05$ctl00$Next$ctl00' and controls_add['AjaxScriptManager'] = 'AjaxScriptManager|ReportViewerControl$ctl05$ctl00$Next$ctl00'

            r1 = re.compile(r"__VIEWSTATE\|.*?\|")
            s1 = re.search(r1, self.response_data)
            self.view_state = s1.group().split('|')[1]

            r2 = re.compile(r"__EVENTVALIDATION\|.*?\|")
            s2 = re.search(r2, self.response_data)
            self.event_validation = s2.group().split('|')[1]

            r3 = re.compile(r"NavigationCorrector_NewViewState\" value=\"/.*?\"")
            s3 = re.search(r3, self.response_data)
            self.new_view_state = s3.group().split('"')[2]

            if self.debug_mode:
                print '***' * 50
                print self.view_state
                print self.event_validation
                print self.new_view_state
                print '***' * 50

            html = saved_form.encode('utf8')
            resp = mechanize.make_response(html, [("Content-Type", "text/html")], self.br.geturl(), 200, "OK")

            self.br.set_response(resp)
            self.br.select_form('ReportViewerForm')
            self.br.form.set_all_readonly(False)

            controls_add    = {
                '__ASYNCPOST'                                       : 'true',
                'AjaxScriptManager'                                 : 'AjaxScriptManager|ReportViewerControl$ctl05$ctl00$Next$ctl00',
                'ReportViewerControl$ctl05$ctl00$CurrentPage'       : '1',
                'ReportViewerControl$ctl05$ctl03$ctl00'             : '',
                #'ReportViewerControl$ctl09$Reserved_AsyncLoadTarget': '',
                #'ReportViewerControl$ctl05$ctl00$Next$ctl00'        : ''
            }
            controls_remove = ['ReportViewerControl$ctl04$ctl03$divDropDown$ctl00',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl01',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl02',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl03',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl04',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl05',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl06',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl07',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl08',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl09',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl10',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl11',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl12',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl13',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl14',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl15',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl16',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl17',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl18',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl19',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl20',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl21',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl22',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl23',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl24',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl25',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl26',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl27',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl28',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl29',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl30',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl31',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl32',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl33',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl34',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl35',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl36',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl37',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl38',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl39',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl40',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl41',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl42',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl43',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl44',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl45',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl46',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl47',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl48',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl49',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl50',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl51',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl52',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl53',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl54',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl55',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl56',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl57',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl58',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl59',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl60',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl61',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl62',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl63',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl64',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl65',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl66',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl67',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl68',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl69',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl70',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl71',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl72',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl73',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl74',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl75',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl76',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl77',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl78',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl79',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl80',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl81',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl82',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl83',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl84',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl85',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$ctl86',
                               'ReportViewerControl$ctl04$ctl00',
                               'ReportViewerControl$ToggleParam$img',
                               'ReportViewerControl$ctl07$img',
                               'ReportViewerControl$ctl04$ctl03$ddDropDownButton']
            controls_enable = ['ReportViewerControl$ctl11',
                               'ReportViewerControl$ctl10',
                               'ReportViewerControl$ctl04$ctl03$txtValue',
                               'ReportViewerControl$ctl04$ctl03$divDropDown$HiddenIndices',
                               'ReportViewerControl$ctl09$ReportControl$ctl04',
                               'ReportViewerControl$ctl04$ctl05$ddValue',
                               'ReportViewerControl$ctl04$ctl13$ddValue',
                               'ReportViewerControl$AsyncWait$HiddenCancelField',
                               'ReportViewerControl$ctl07$store',
                               'ReportViewerControl$ctl07$collapse',
                               'ReportViewerControl$ctl04$ctl07$ddValue',
                               'ReportViewerControl$ctl08$ClientClickedId',
                               'ReportViewerControl$ctl09$VisibilityState$ctl00',
                               'ReportViewerControl$ToggleParam$collapse',
                               'ReportViewerControl$ToggleParam$store',
                               'ReportViewerControl$ctl05$ctl00$CurrentPage',
                               'ReportViewerControl$ctl05$ctl03$ctl00',
                               'ReportViewerControl$ctl04$ctl09$txtValue',
                               'ReportViewerControl$ctl04$ctl11$txtValue',
                               'ReportViewerControl$ctl09$ScrollPosition']
            items_enable    = ['ReportViewerControl$ctl04$ctl09$cbNull',
                               'ReportViewerControl$ctl04$ctl11$cbNull',
                               'ReportViewerControl$ctl04$ctl05$ddValue',
                               'ReportViewerControl$ctl04$ctl07$ddValue',
                               'ReportViewerControl$ctl04$ctl13$ddValue']
            form_data       = { '__EVENTARGUMENT'                                           : '',
                                '__EVENTTARGET'                                             : 'ReportViewerControl$ctl05$ctl00$Next$ctl00',
                                '__EVENTVALIDATION'                                         : self.event_validation,
                                '__VIEWSTATE'                                               : self.view_state,
                                'NavigationCorrector$NewViewState'                          : self.new_view_state,
                                'ReportViewerControl$ctl10'                                 : 'ltr',
                                'ReportViewerControl$ctl11'                                 : 'quirks',
                                'ReportViewerControl$ctl04$ctl03$txtValue'                  : self.txt_value,
                                'ReportViewerControl$ctl04$ctl05$ddValue'                   : ['3'],
                                'ReportViewerControl$ctl04$ctl07$ddValue'                   : ['1'],
                                'ReportViewerControl$ctl04$ctl09$cbNull'                    : ['on'],
                                'ReportViewerControl$ctl04$ctl11$cbNull'                    : ['on'],
                                'ReportViewerControl$ctl04$ctl13$ddValue'                   : ['1'],
                                'ReportViewerControl$ctl04$ctl03$divDropDown$HiddenIndices' : '14',
                                'ReportViewerControl$AsyncWait$HiddenCancelField'           : 'False',
                                'ReportViewerControl$ctl09$VisibilityState$ctl00'           : 'ReportPage',
                                'ReportViewerControl$ctl09$ReportControl$ctl04'             : '100',
                                'ReportViewerControl$ToggleParam$collapse'                  : 'false',
                                'ReportViewerControl$ctl07$collapse'                        : 'false'
            }

            if self.debug_mode:
                for control in self.br.form.controls:
                    print "type=%s name=%s disabled=%s value=%s" % (control.type, control.name, control.disabled, self.br.form[control.name])
            self.debug_mode = True
            self.submit_webform(controls_add, controls_remove, controls_enable, items_enable, form_data)


# General web-scraping and data processing functions --------------------------------------------------------------------------------------------------------------------

def load_production_to_sql(data_dir=PROD_DATA_DIR, table_name=TABLE_NAME, header_row=0, header_names=[], column_nums=[], delimit_symbol=None):
    total_rows = 0
    dframes = []
    for data_sheet in os.listdir(data_dir):
        print data_sheet
        df = pd.read_csv(data_dir+data_sheet, low_memory=False, header=header_row, names=header_names, usecols=column_nums, delimiter=delimit_symbol)
        dframes.append(df)

    prod_data = pd.concat(dframes)
    print prod_data.shape[0], 'rows in table'

    engine = create_engine("mysql://root:OilAndGas321@localhost/well_data")
    prod_data.to_sql(name=table_name, con=engine, if_exists="append", chunksize=10000, index=False)

def csv_to_sql(data_dir, data_file, table_name=None):
    if not table_name:
        table_name = '{}_Well_Details'.format(data_file[:2])
    total_rows = 0
    dframes = []
    df = pd.read_csv(data_dir+data_file, low_memory=False)
    dframes.append(df)

    prod_data = pd.concat(dframes)
    print prod_data.shape[0], 'rows in table'

    engine = create_engine("mysql://root:OilAndGas321@localhost/globaldata")
    prod_data.to_sql(name=table_name, con=engine, if_exists="replace", chunksize=10000, index=False)

def load_access_databases(data_dir):
    conn = get_connection(database='globaldata')
    curr = conn.cursor()
    tbl_templates = {
        '{}CaliforniaOilandGasWellInjection'    : 'ca_well_injection_data',
        '{}CaliforniaOilandGasWellProduction'   : 'ca_well_production_data',
        '{}CaliforniaOilandGasWells'            : 'ca_well_data'
    }
    sql_insert = 'INSERT INTO {} VALUES ({})'
    for db_file in [dbfile for dbfile in os.listdir(data_dir) if dbfile[-5:] == 'accdb']:
        print db_file
        file_year = db_file[:4]
        acc_conn = get_connection(server='access', access_file=data_dir+db_file)
        acc_curr = acc_conn.cursor()
        for tbl_name in tbl_templates.keys():
            print tbl_name.format(file_year)
            sql_tbl = tbl_templates[tbl_name]
            acc_curr.execute('SELECT * FROM {}'.format(tbl_name.format(file_year)))
            for datarow in acc_curr.fetchall():
                var_str = ','.join(['%s']*len(datarow))
                #print sql_insert.format(sql_tbl, var_str) % datarow
                curr.execute(sql_insert.format(sql_tbl, var_str), datarow)
            commit(curr)
        acc_curr.close()
        acc_conn.close()
    curr.close()
    conn.close()

def add_source_year(data_dir=CSV_PROD_DIR):
    headers = 'SOURCE_YEAR,REPORT_MONTH,REPORT_YEAR,ST,API_COUNTY_CODE,API_SEQ_NUM,SIDETRACK_NUM,FORMATION_CODE,WELL_STATUS,PROD_DAYS,WATER_DISP_CODE,WATER_VOL,WATER_PRESS_TBG,WATER_PRESS_CSG,BOM_INVENT,OIL_VOL,OIL_SALES,ADJUSTMENT,EOM_INVENT,GRAVITY_SALES,GAS_SALES,FLARED,GAS_VOL,SHRINK,GAS_PROD,BTU_SALES,GAS_PRESS_TBG,GAS_PRESS_CSG,OPERATOR_NUM,OPERATOR,FACILITY_NAME,FACILITY_NUM,ACCEPTED_DATE\n'
    for filename in os.listdir(data_dir):
        file_year = filename[:4]
        print filename
        data_rows = []
        with open(data_dir+filename, 'r+') as csv_infile:
            csv_reader = csv.reader(csv_infile)
            for row in csv_reader:
                row = [file_year] + row
                data_rows.append(row)
        with open(PROD_DATA_DIR+filename, 'a') as csv_outfile:
            csv_outfile.write(headers)
            line_num = 1
            for data_row in data_rows:
                print line_num
                data_str = ','.join(data_row)
                csv_outfile.write(data_str+'\n')
                line_num += 1

def move_files(src_dir, dst_dir, file_extn='xlsx', outfile_code='', asset_list=None):
    for asset_model in [filename for filename in os.listdir(src_dir) if filename.endswith(file_extn)]:
        print src_dir + asset_model
        if asset_list:
            asset_id = int(asset_model.split('_')[1])
            if asset_id in asset_list:
                shutil.move(src_dir + asset_model, dst_dir + outfile_code + asset_model)
        else:
            shutil.move(src_dir + asset_model, dst_dir + asset_model)

def copy_files(src_dir, dst_dir, in_ext='', out_ext='', out_format='{}.{}', fname_indx=None, fname_incr=False):
    if fname_indx == None:
        fname_indx = -(len(in_ext)+1)
    input_files = [filename for filename in os.listdir(src_dir) if filename.endswith(in_ext)]
    input_file_num = 0
    input_file_count = len(input_files)
    for input_file in input_files:
        input_filename = input_file[:fname_indx]
        if fname_incr:
            output_file = out_format.format(input_filename, input_file_num, out_ext)
        else:
            output_file = out_format.format(input_filename,out_ext)
        print '({}/{}): {} ---> {}'.format(input_file_num, input_file_count, src_dir + input_file, dst_dir + output_file)
        shutil.copy2(src_dir+input_file, dst_dir+output_file)
        input_file_num += 1
        
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

def get_prod_year(url):
    '''
    Ex:
        url = 'https://www.data.boem.gov/Production/ProductionData/Default.aspx'
    '''
    response = urllib2.urlopen(url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    prod_year = tree.xpath('//*[@id="ASPxFormLayout2_ASPxGridView1_DXFREditorcol3_I"]/@value')
    return prod_year

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

def download_file(url, output_dir, output_file, output_extn='.txt'):
    '''
    Ex:
        urllib.urlretrieve('https://kgs.uky.edu/kygeode/services/oilgas/prodReport.asp?viewType=txtDownload&dlmtr=comma&recNum=93706&prodType=oil', 'D:\\Globaldata\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\93706_oil.kgs')
    '''
    out_filename = output_dir + output_file + output_extn
    urllib.urlretrieve(url, out_filename)

def retrieve_web_data(url_dir, output_dir, unzip=False, delete_zip=False):
    for web_file_name in [webfilename for webfilename in os.listdir(url_dir) if webfilename[-3:] == 'zip']:
        download_zipfile(url_dir + web_file_name)

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


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Source specific functions ---------------------------------------------------------------------------------------------------------------------------------------------

def convert_KY_prod():
    data_dir = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\unprocessed\\'
    for prod_file in os.listdir(data_dir):
        filename = prod_file[:-4]
        os.rename(data_dir+prod_file, data_dir+filename+'.csv')

def finish_KY_records():
    unprocessed_files = os.listdir('D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\unprocessed\\')
    processed_files   = os.listdir('D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\processed\\')
    no_wells_files    = os.listdir('D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\no_wells\\')
    collected_files = unprocessed_files + processed_files + no_wells_files
    collected_wells = sorted(list(set([filename[4:-4] for filename in collected_files if filename[:3] == 'gas'])))
    uncollected_wells = [well_record for well_record in ky_wells if not well_record in collected_wells]
    for well in uncollected_wells:
        print well
    print len(uncollected_wells), 'wells left to download'

def check_KY_prod():
    unprocessed_dir = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\unprocessed\\'
    processed_dir   = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\processed\\'
    no_wells_dir    = 'D:\\GlobalData\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\no_wells\\'
    no_wells = []
    file_count = 1
    total_file_count = len(os.listdir(unprocessed_dir))
    for prod_file in os.listdir(unprocessed_dir):
        print '{}/{}: {}'.format(file_count, total_file_count, prod_file)
        with open(unprocessed_dir+prod_file) as csv_file:
            csv_lines = csv_file.readlines()
            if 'NO WELLS' in csv_lines[0]:
                no_wells.append(prod_file)
        file_count += 1

    for no_well_file in no_wells:
        shutil.move(unprocessed_dir+no_well_file, no_wells_dir+no_well_file)

    for well_file in os.listdir(unprocessed_dir):
        shutil.move(unprocessed_dir+well_file, processed_dir+well_file)

def TX_webdrive():
    for typewell in TX_DATA['typewells']:
        tx_config = WEBDRIVE_CONFIG.copy()
        tx_config['tx_prod']['click'][0] = ('xpath', "//select[@name='searchArgs.wellTypeArg']/option[text()='{}']".format(typewell), 0)
        for district in TX_DATA['districts']:
            tx_config['tx_prod']['click'][1] = ('xpath', "//select[@name='searchArgs.districtCodeArg']/option[text()='{}']".format(district), 0)
            webdrive_main(webdrive_config=tx_config['tx_prod'], headless=False)

def unzip_UN_energy():
    file_dir = 'D:\\Downloads\\UN_Energy\\'
    unzip_dir = 'D:\\Downloads\\extracted_\\'
    for zipfilename in os.listdir(file_dir):
        print zipfilename
        unzip_file(file_dir+zipfilename, unzip_dir+zipfilename[:2])

def get_KY_well_production(start_indx=0, end_indx=0):
    well_file_data = {
        'gas'           : {'url'    : 'https://kgs.uky.edu/kygeode/services/oilgas/prodReport.asp?viewType=txtDownload&dlmtr=comma&recNum={}&prodType=gas',
                           'records': ky_wells}
    }
    failed_recs = []
    for record_type in ['gas']:
        rec_data = well_file_data[record_type]
        url_temp = rec_data['url']
        well_records = rec_data['records'][start_indx: end_indx]
        total_records = len(well_records)
        rec_count = 1
        for rec_num in well_records:
            print '{}/{}: {}'.format(rec_count, total_records, rec_num)
            url = url_temp.format(rec_num)
            outfile_name = '{}_{}'.format(record_type, rec_num)
            try:
                download_file(url, 'D:\\Globaldata\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\unprocessed\\', outfile_name, '.csv')
                rec_count += 1
            except:
                print 'fail level 1'
                try:
                    sleep(1)
                    download_file(url, 'D:\\Globaldata\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\', outfile_name, '.csv')
                    rec_count += 1
                except:
                    print 'fail level 2'
                    try:
                        sleep(1)
                        download_file(url, 'D:\\Globaldata\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\', outfile_name, '.csv')
                        rec_count += 1
                    except:
                        print 'fail level 3'
                        try:
                            sleep(1)
                            download_file(url, 'D:\\Globaldata\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\', outfile_name, '.csv')
                            rec_count += 1
                        except:
                            print 'fail level 4'
                            try:
                                sleep(1)
                                download_file(url, 'D:\\Globaldata\\Data\\wells\\Well_Data_Files\\KY_Well_Data\\Prod_Data\\', outfile_name, '.csv')
                                rec_count += 1
                            except:
                                print 'fail level 5'
                                rec_count += 1
                                failed_recs.append((record_type, rec_num))

    if failed_recs:
        for rec_type, rec_num in failed_recs:
            print '{}: {}'.format(rec_type, rec_num)
    else:
        print 'All records downloaded'

def get_NM_prod(output_dir):
    well_apis = get_data('well_id', 'nm_well_details')
    url = 'https://wwwapps.emnrd.state.nm.us/ocd/ocdpermitting/Data/ProductionSummaryPrint.aspx?report=excel&api={}'
    for well_api in well_apis[:1]:
        output_file = '{}_well_data'.format(well_api)
        print output_file
        output_file = 'ProductionSummaryReport'
        download_file(url.format(well_api), output_dir, output_file, output_extn='.xls')

def get_UT_data(update_db=False, debug=False):
    ut_data = {}
    conn = get_connection()
    curr = conn.cursor()
    sql_insert = 'INSERT INTO ut_well_production (well_api, prod_year, prod_month, operator, formation, prod_days, oil_prod_bbl, gas_prod_mcf, water_prod_bbl) VALUES ("{}",{},{},"{}","{}",{},{},{},{})'
    for html_datafile in [filename for filename in os.listdir('D:\\GlobalData\\Data\\wells\\web_scrape\\UT_Web_Data\\') if filename.endswith('html')]:
        api = html_datafile[:12]
        ut_data[api] = {'prod': [], 'details': []}
        with open('D:\\GlobalData\\Data\\wells\\web_scrape\\UT_Web_Data\\{}_well_data.html'.format(api)) as html_file:
            print html_datafile
            test_file = BeautifulSoup(html_file, 'lxml')
            data_cells = test_file.find_all('td')
            well_details = ()
            param_vals = ()
            for i in range(len(data_cells)):
                data_cell = data_cells[i]
                if debug:
                    print i, data_cell.get_text()
                row = i - 25
                if i in range(3, 26, 2):
                    well_details += (data_cell.get_text(),)
                elif row >= 0:
                    if row % 11 == 2:
                        prod_year  = int(data_cell.get_text()[-4:])
                        prod_month = int(data_cell.get_text()[:2])
                        param_vals = (api, prod_year, prod_month)
                    elif row % 11 in [3,4]:
                        param_vals += (data_cell.get_text().strip(),)
                    elif row % 11 in [6,7,8]:
                        param_vals += (int(data_cell.get_text()),)
                    elif row % 11 == 9:
                        param_vals += (int(data_cell.get_text()),)
                        ut_data[api]['prod'].append(param_vals)
                    else:
                        pass
                else:
                    pass
            ut_data[api]['details'].append(well_details)
            if update_db:
                for prod_data in ut_data[api]['prod']:
                    if debug:
                        print sql_insert.format(*prod_data)
                    curr.execute(sql_insert.format(*prod_data))
                    commit(curr)
    curr.close()
    conn.close()
    return ut_data

def get_AL_html(url, well_ids=[], state='', sleep_time=0, start_indx=0, end_indx=0):
    if well_ids:
        well_id_list = well_ids
    else:
        well_id_list = get_data('well_id', '{}_well_production_lite'.format(state))
    session = requests.Session()
    if end_indx:
        well_list = well_id_list[:end_indx]
    else:
        well_list = well_id_list
    if start_indx:
        well_list = well_list[start_indx:]
    for permit_id, well_id in well_list:
        print url.format(permit_id, well_id)
        if sleep_time:
            print 'sleep for {} seconds'.format(sleep_time)
            sleep(sleep_time)
        r1 = requests.get(url.format(permit_id, well_id))
        with open(WELL_DATA_DIR + 'web_scrape\\{}_Web_Data\\{}-{}-{}_well_data.html'.format(state.upper(), well_id[:2], well_id[2:5], well_id[5:]), 'w') as web_text:
            print r1.text
            web_text.write(decode_str(r1.text))

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

def load_CO_prod(curr):
    sql_update = \
    '''
    UPDATE CO_well_prod_lite AS a, CO_well_production_ AS b, us_ref_formation AS c
    SET a.GAS_{0}_MCF=IFNULL(b.GAS_PROD,0),
        a.OIL_{0}_BBL=IFNULL(b.OIL_VOL,0),
      a.WATER_{0}_BBL=IFNULL(b.WATER_VOL,0)
    WHERE a.PROD_YEAR=b.REPORT_YEAR AND a.WELL_API=b.WELL_API AND a.FORMATION_ID=c.FORMATION_ID AND b.FORMATION_CODE=c.STATE_FORMATION_ID AND c.STATE_ID=5 AND b.REPORT_MONTH={1} AND b.SOURCE_YEAR={2}
    '''
    for source_year in range(1999,2020):
        for prod_month in MONTH_NUMS.keys():
            month_num = MONTH_NUMS[prod_month]
            print sql_update.format(prod_month, month_num, source_year)
            curr.execute(sql_update.format(prod_month, month_num, source_year))
            commit(curr)
    if 0:
        sql_select = 'SELECT PROD_YEAR, SUM(OIL_PROD_BBL) AS TOTAL_OIL_BBL, SUM(GAS_PROD_MCF) AS TOTAL_GAS_MCF, SUM(WATER_PROD_BBL) AS TOTAL_WATER_BBL FROM CO_well_production GROUP BY PROD_YEAR ORDER BY PROD_YEAR'
        print sql_select
        curr.execute(sql_select)
        print 'YEAR\tOIL_BBL\tGAS_MCF\tWATER_BBL'
        for year, oil, gas, water in curr.fetchall():
            print '{}:\t{}\t{}\t{}'.format(year, oil, gas, water)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#(2019-10-22 20:01:06) -- 4319/6224: O10329047825 - 251691 - 85280300 - 201605 - 201907

if __name__=='__main__':
    schedule_dates = [
        'may-2013',
        'june-2013',
        'july-2013',
        'august-2013',
        'september-2013',
        'october-2013',
        'november-2013',
        'december-2013',
        'january-2014',
        'february-2014',
        'march-2014',
        'april-2014',
        'may-2014',
        'june-2014',
        'july-2014',
        'august-2014',
        'september-2014',
        'october-2014',
        'november-2014',
        'december-2014',
        'january-2015',
        'february-2015',
        'march-2015',
        'april-2015',
        'may-2015',
        'june-2015',
        'july-2015',
        'august-2015',
        'september-2015',
        'october-2015',
        'november-2015',
        'december-2015',
        'january-2016',
        'february-2016',
        'march-2016',
        'april-2016',
        'may-2016',
        'june-2016',
        'july-2016',
        'august-2016',
        'september-2016',
        'october-2016',
        'november-2016',
        'december-2016',
        'january-2017',
        'february-2017',
        'march-2017',
        'april-2017',
        'may-2017',
        'june-2017',
        'july-2017',
        'august-2017',
        'september-2017',
        'october-2017',
        'november-2017',
        'december-2017',
        'january-2018',
        'february-2018',
        'march-2018',
        'april-2018',
        'may-2018',
        'june-2018',
        'july-2018',
        'august-2018',
        'september-2018',
        'october-2018',
        'november-2018',
        'december-2018',
        'january-2019',
        'february-2019',
        'march-2019',
        'april-2019',
        'may-2019',
        'june-2019',
        'july-2019',
        'august-2019',
        'september-2019',
        'october-2019'
    ]
    #url = 'https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17&search=%7B%22item%22%3A%5B%7B%22key%22%3A%22api_ft%22%2C%22value%22%3A%22{}%22%7D%5D%7D'
    #well_ids = get_data('SUBSTRING(api_number,3,8)', 'tx_permit_data', database='us_wells', sql_where='1=1 ORDER BY SUBSTRING(api_number,3,8) DESC')
    #well_ids = ['42935752']

    schedule_urls = [
        "/media/21853/oildist1.txt",
        "/media/21987/oildist1.txt",
        "/media/22052/oildist1.txt",
        "/media/21802/oildist1.txt",
        "/media/21766/oildist1.txt",
        "/media/21827/oildist1.txt",
        "/media/21904/oildist1.txt",
        "/media/22160/oildist1.txt",
        "/media/22113/oildist1.txt",
        "/media/21861/oildist10.txt",
        "/media/21998/oildist10.txt",
        "/media/22062/oildist10.txt",
        "/media/21810/oildist10.txt",
        "/media/21773/oildist10.txt",
        "/media/21833/oildist10.txt",
        "/media/21909/oildist10.txt",
        "/media/22169/oildist10.txt",
        "/media/22144/oildist10.txt",
        "/media/22117/oildist10.txt",
        "/media/21851/oildist2.txt",
        "/media/21986/oildist2.txt",
        "/media/22053/oildist2.txt",
        "/media/21800/oildist2.txt",
        "/media/21765/oildist2.txt",
        "/media/21825/oildist2.txt",
        "/media/21902/oildist2.txt",
        "/media/22161/oildist2.txt",
        "/media/22137/oildist2.txt",
        "/media/22110/oildist2.txt",
        "/media/21857/oildist3.txt",
        "/media/21992/oildist3.txt",
        "/media/22055/oildist3.txt",
        "/media/21807/oildist3.txt",
        "/media/21769/oildist3.txt",
        "/media/21829/oildist3.txt",
        "/media/21903/oildist3.txt",
        "/media/22162/oildist3.txt",
        "/media/22140/oildist3.txt",
        "/media/22115/oildist3.txt",
        "/media/21856/oildist4.txt",
        "/media/21991/oildist4.txt",
        "/media/22059/oildist4.txt",
        "/media/21806/oildist4.txt",
        "/media/21767/oildist4.txt",
        "/media/21830/oildist4.txt",
        "/media/21906/oildist4.txt",
        "/media/22164/oildist4.txt",
        "/media/22138/oildist4.txt",
        "/media/22112/oildist4.txt",
        "/media/21990/oildist5.txt",
        "/media/22054/oildist5.txt",
        "/media/21803/oildist5.txt",
        "/media/21828/oildist5.txt",
        "/media/21828/oildist5.txt",
        "/media/21905/oildist5.txt",
        "/media/22163/oildist5.txt",
        "/media/22136/oildist5.txt",
        "/media/22111/oildist5.txt",
        "/media/21855/oildist6.txt",
        "/media/21994/oildist6.txt",
        "/media/22057/oildist6.txt",
        "/media/21805/oildist6.txt",
        "/media/21768/oildist6.txt",
        "/media/21831/oildist6.txt",
        "/media/21908/oildist6.txt",
        "/media/22165/oildist6.txt",
        "/media/22139/oildist6.txt",
        "/media/22114/oildist6.txt",
        "/media/21858/oildist6e.txt",
        "/media/21993/oildist6e.txt",
        "/media/22056/oildist6e.txt",
        "/media/21804/oildist6e.txt",
        "/media/21770/oildist6e.txt",
        "/media/30285/oildist6e.txt",
        "/media/21832/oildist6e.txt",
        "/media/21907/oildist6e.txt",
        "/media/22166/oildist6e.txt",
        "/media/22141/oildist6e.txt",
        "/media/22116/oildist6e.txt",
        "/media/21859/oildist7b.txt",
        "/media/21997/oildist7b.txt",
        "/media/22060/oildist7b.txt",
        "/media/21808/oildist7b.txt",
        "/media/21771/oildist7b.txt",
        "/media/30286/oildist7b.txt",
        "/media/21838/oildist7b.txt",
        "/media/21912/oildist7b.txt",
        "/media/22168/oildist7b.txt",
        "/media/22142/oildist7b.txt",
        "/media/22119/oildist7b.txt",
        "/media/21860/oildist7c.txt",
        "/media/21995/oildist7c.txt",
        "/media/22058/oildist7c.txt",
        "/media/21809/oildist7c.txt",
        "/media/21772/oildist7c.txt",
        "/media/21834/oildist7c.txt",
        "/media/21911/oildist7c.txt",
        "/media/22167/oildist7c.txt",
        "/media/22143/oildist7c.txt",
        "/media/22118/oildist7c.txt",
        "/media/21863/oildist8.txt",
        "/media/21813/oildist8.txt",
        "/media/21776/oildist8.txt",
        "/media/21837/oildist8.txt",
        "/media/21914/oildist8.txt",
        "/media/22172/oildist8.txt",
        "/media/22146/oildist8.txt",
        "/media/22122/oildist8.txt",
        "/media/21862/oildist8a.txt",
        "/media/21999/oildist8a.txt",
        "/media/22064/oildist8a.txt",
        "/media/21811/oildist8a.txt",
        "/media/21775/oildist8a.txt",
        "/media/21835/oildist8a.txt",
        "/media/21913/oildist8a.txt",
        "/media/22170/oildist8a.txt",
        "/media/22147/oildist8a.txt",
        "/media/22120/oildist8a.txt",
        "/media/23266/oildist8-aug13.txt",
        "/media/21864/oildist9.txt",
        "/media/22000/oildist9.txt",
        "/media/22063/oildist9.txt",
        "/media/21812/oildist9.txt",
        "/media/21774/oildist9.txt",
        "/media/21836/oildist9.txt",
        "/media/21910/oildist9.txt",
        "/media/22171/oildist9.txt",
        "/media/22145/oildist9.txt",
        "/media/22121/oildist9.txt",
        "/media/23485/oildistrict8-dec2013.txt",
        "/media/30296/oilsch1.pdf",
        "/media/27595/oilsch1.txt",
        "/media/39142/oilsch1.txt",
        "/media/44715/oilsch1.txt",
        "/media/51351/oilsch1.txt",
        "/media/22222/oilsch1.txt",
        "/media/29677/oilsch1.txt",
        "/media/41132/oilsch1.txt",
        "/media/46777/oilsch1.txt",
        "/media/53115/oilsch1.txt",
        "/media/25416/oilsch1.txt",
        "/media/31387/oilsch1.txt",
        "/media/42935/oilsch1.txt",
        "/media/48861/oilsch1.txt",
        "/media/48928/oilsch1.txt",
        "/media/26846/oilsch1.txt",
        "/media/38106/oilsch1.txt",
        "/media/43790/oilsch1.txt",
        "/media/50135/oilsch1.txt",
        "/media/26214/oilsch1.txt",
        "/media/37615/oilsch1.txt",
        "/media/43340/oilsch1.txt",
        "/media/49688/oilsch1.txt",
        "/media/21534/oilsch1.txt",
        "/media/29266/oilsch1.txt",
        "/media/40630/oilsch1.txt",
        "/media/46327/oilsch1.txt",
        "/media/52803/oilsch1.txt",
        "/media/19769/oilsch1.txt",
        "/media/28697/oilsch1.txt",
        "/media/40277/oilsch1.txt",
        "/media/45864/oilsch1.txt",
        "/media/52114/oilsch1.txt",
        "/media/27127/oilsch1.txt",
        "/media/38661/oilsch1.txt",
        "/media/44269/oilsch1.txt",
        "/media/50679/oilsch1.txt",
        "/media/21879/oilsch1.txt",
        "/media/28409/oilsch1.txt",
        "/media/39649/oilsch1.txt",
        "/media/45224/oilsch1.txt",
        "/media/51638/oilsch1.txt",
        "/media/24800/oilsch1.txt",
        "/media/30963/oilsch1.txt",
        "/media/42481/oilsch1.txt",
        "/media/48866/oilsch1.txt",
        "/media/24171/oilsch1.txt",
        "/media/30454/oilsch1.txt",
        "/media/42114/oilsch1.txt",
        "/media/47911/oilsch1.txt",
        "/media/54473/oilsch1.txt",
        "/media/23162/oilsch1.txt",
        "/media/29886/oilsch1.txt",
        "/media/41731/oilsch1.txt",
        "/media/47506/oilsch1.txt",
        "/media/53896/oilsch1.txt",
        "/media/27599/oilsch10.txt",
        "/media/39147/oilsch10.txt",
        "/media/44697/oilsch10.txt",
        "/media/51354/oilsch10.txt",
        "/media/22230/oilsch10.txt",
        "/media/29686/oilsch10.txt",
        "/media/41135/oilsch10.txt",
        "/media/46783/oilsch10.txt",
        "/media/53125/oilsch10.txt",
        "/media/25422/oilsch10.txt",
        "/media/31396/oilsch10.txt",
        "/media/42940/oilsch10.txt",
        "/media/48923/oilsch10.txt",
        "/media/26855/oilsch10.txt",
        "/media/38109/oilsch10.txt",
        "/media/43791/oilsch10.txt",
        "/media/50137/oilsch10.txt",
        "/media/26223/oilsch10.txt",
        "/media/37619/oilsch10.txt",
        "/media/43344/oilsch10.txt",
        "/media/49672/oilsch10.txt",
        "/media/21539/oilsch10.txt",
        "/media/29273/oilsch10.txt",
        "/media/40637/oilsch10.txt",
        "/media/46311/oilsch10.txt",
        "/media/52786/oilsch10.txt",
        "/media/19752/oilsch10.txt",
        "/media/28702/oilsch10.txt",
        "/media/40197/oilsch10.txt",
        "/media/45850/oilsch10.txt",
        "/media/52126/oilsch10.txt",
        "/media/27136/oilsch10.txt",
        "/media/38664/oilsch10.txt",
        "/media/44276/oilsch10.txt",
        "/media/50677/oilsch10.txt",
        "/media/21886/oilsch10.txt",
        "/media/28411/oilsch10.txt",
        "/media/39662/oilsch10.txt",
        "/media/45207/oilsch10.txt",
        "/media/51639/oilsch10.txt",
        "/media/24806/oilsch10.txt",
        "/media/30972/oilsch10.txt",
        "/media/42488/oilsch10.txt",
        "/media/48863/oilsch10.txt",
        "/media/24180/oilsch10.txt",
        "/media/30459/oilsch10.txt",
        "/media/42123/oilsch10.txt",
        "/media/47918/oilsch10.txt",
        "/media/54490/oilsch10.txt",
        "/media/23169/oilsch10.txt",
        "/media/29888/oilsch10.txt",
        "/media/41716/oilsch10.txt",
        "/media/47504/oilsch10.txt",
        "/media/53892/oilsch10.txt",
        "/media/26094/oilsch12.txt",
        "/media/30294/oilsch2.pdf",
        "/media/27594/oilsch2.txt",
        "/media/39138/oilsch2.txt",
        "/media/44714/oilsch2.txt",
        "/media/51352/oilsch2.txt",
        "/media/22221/oilsch2.txt",
        "/media/29678/oilsch2.txt",
        "/media/41127/oilsch2.txt",
        "/media/46773/oilsch2.txt",
        "/media/53117/oilsch2.txt",
        "/media/25414/oilsch2.txt",
        "/media/31386/oilsch2.txt",
        "/media/42932/oilsch2.txt",
        "/media/48930/oilsch2.txt",
        "/media/26847/oilsch2.txt",
        "/media/38103/oilsch2.txt",
        "/media/43785/oilsch2.txt",
        "/media/50132/oilsch2.txt",
        "/media/26219/oilsch2.txt",
        "/media/37612/oilsch2.txt",
        "/media/43338/oilsch2.txt",
        "/media/49686/oilsch2.txt",
        "/media/21531/oilsch2.txt",
        "/media/29267/oilsch2.txt",
        "/media/40628/oilsch2.txt",
        "/media/46308/oilsch2.txt",
        "/media/52799/oilsch2.txt",
        "/media/19765/oilsch2.txt",
        "/media/28696/oilsch2.txt",
        "/media/40276/oilsch2.txt",
        "/media/45843/oilsch2.txt",
        "/media/52113/oilsch2.txt",
        "/media/27132/oilsch2.txt",
        "/media/38659/oilsch2.txt",
        "/media/44268/oilsch2.txt",
        "/media/50675/oilsch2.txt",
        "/media/21877/oilsch2.txt",
        "/media/28408/oilsch2.txt",
        "/media/39651/oilsch2.txt",
        "/media/45223/oilsch2.txt",
        "/media/51630/oilsch2.txt",
        "/media/24796/oilsch2.txt",
        "/media/30962/oilsch2.txt",
        "/media/42478/oilsch2.txt",
        "/media/48867/oilsch2.txt",
        "/media/24172/oilsch2.txt",
        "/media/30450/oilsch2.txt",
        "/media/42115/oilsch2.txt",
        "/media/47910/oilsch2.txt",
        "/media/54471/oilsch2.txt",
        "/media/23161/oilsch2.txt",
        "/media/29880/oilsch2.txt",
        "/media/41734/oilsch2.txt",
        "/media/47497/oilsch2.txt",
        "/media/53898/oilsch2.txt",
        "/media/27591/oilsch3.txt",
        "/media/39140/oilsch3.txt",
        "/media/44696/oilsch3.txt",
        "/media/51357/oilsch3.txt",
        "/media/22225/oilsch3.txt",
        "/media/29683/oilsch3.txt",
        "/media/41130/oilsch3.txt",
        "/media/46778/oilsch3.txt",
        "/media/53122/oilsch3.txt",
        "/media/25418/oilsch3.txt",
        "/media/31389/oilsch3.txt",
        "/media/42934/oilsch3.txt",
        "/media/48931/oilsch3.txt",
        "/media/26849/oilsch3.txt",
        "/media/38105/oilsch3.txt",
        "/media/43786/oilsch3.txt",
        "/media/50130/oilsch3.txt",
        "/media/26218/oilsch3.txt",
        "/media/37610/oilsch3.txt",
        "/media/43342/oilsch3.txt",
        "/media/49690/oilsch3.txt",
        "/media/21537/oilsch3.txt",
        "/media/29269/oilsch3.txt",
        "/media/40631/oilsch3.txt",
        "/media/46310/oilsch3.txt",
        "/media/52801/oilsch3.txt",
        "/media/19768/oilsch3.txt",
        "/media/28699/oilsch3.txt",
        "/media/40188/oilsch3.txt",
        "/media/45848/oilsch3.txt",
        "/media/52121/oilsch3.txt",
        "/media/27131/oilsch3.txt",
        "/media/38662/oilsch3.txt",
        "/media/44266/oilsch3.txt",
        "/media/50678/oilsch3.txt",
        "/media/21881/oilsch3.txt",
        "/media/28402/oilsch3.txt",
        "/media/39653/oilsch3.txt",
        "/media/45205/oilsch3.txt",
        "/media/51633/oilsch3.txt",
        "/media/24799/oilsch3.txt",
        "/media/30969/oilsch3.txt",
        "/media/42486/oilsch3.txt",
        "/media/48872/oilsch3.txt",
        "/media/24173/oilsch3.txt",
        "/media/30453/oilsch3.txt",
        "/media/42119/oilsch3.txt",
        "/media/47913/oilsch3.txt",
        "/media/54474/oilsch3.txt",
        "/media/23165/oilsch3.txt",
        "/media/29884/oilsch3.txt",
        "/media/41733/oilsch3.txt",
        "/media/47499/oilsch3.txt",
        "/media/53894/oilsch3.txt",
        "/media/27590/oilsch4.txt",
        "/media/39141/oilsch4.txt",
        "/media/44694/oilsch4.txt",
        "/media/51350/oilsch4.txt",
        "/media/22224/oilsch4.txt",
        "/media/29680/oilsch4.txt",
        "/media/41129/oilsch4.txt",
        "/media/46776/oilsch4.txt",
        "/media/53119/oilsch4.txt",
        "/media/25415/oilsch4.txt",
        "/media/31394/oilsch4.txt",
        "/media/42930/oilsch4.txt",
        "/media/48932/oilsch4.txt",
        "/media/26850/oilsch4.txt",
        "/media/38104/oilsch4.txt",
        "/media/43789/oilsch4.txt",
        "/media/50339/oilsch4.txt",
        "/media/26216/oilsch4.txt",
        "/media/37611/oilsch4.txt",
        "/media/43339/oilsch4.txt",
        "/media/49689/oilsch4.txt",
        "/media/21536/oilsch4.txt",
        "/media/29270/oilsch4.txt",
        "/media/40626/oilsch4.txt",
        "/media/46306/oilsch4.txt",
        "/media/52800/oilsch4.txt",
        "/media/19766/oilsch4.txt",
        "/media/28698/oilsch4.txt",
        "/media/40192/oilsch4.txt",
        "/media/45844/oilsch4.txt",
        "/media/52118/oilsch4.txt",
        "/media/27133/oilsch4.txt",
        "/media/38660/oilsch4.txt",
        "/media/44271/oilsch4.txt",
        "/media/50674/oilsch4.txt",
        "/media/21880/oilsch4.txt",
        "/media/28401/oilsch4.txt",
        "/media/39655/oilsch4.txt",
        "/media/45203/oilsch4.txt",
        "/media/51632/oilsch4.txt",
        "/media/24798/oilsch4.txt",
        "/media/30966/oilsch4.txt",
        "/media/42480/oilsch4.txt",
        "/media/48871/oilsch4.txt",
        "/media/24174/oilsch4.txt",
        "/media/30451/oilsch4.txt",
        "/media/42116/oilsch4.txt",
        "/media/47908/oilsch4.txt",
        "/media/54491/oilsch4.txt",
        "/media/23163/oilsch4.txt",
        "/media/29883/oilsch4.txt",
        "/media/41732/oilsch4.txt",
        "/media/47502/oilsch4.txt",
        "/media/53890/oilsch4.txt",
        "/media/21854/oilsch5.txt",
        "/media/27592/oilsch5.txt",
        "/media/39143/oilsch5.txt",
        "/media/44693/oilsch5.txt",
        "/media/51348/oilsch5.txt",
        "/media/22223/oilsch5.txt",
        "/media/29679/oilsch5.txt",
        "/media/41128/oilsch5.txt",
        "/media/46774/oilsch5.txt",
        "/media/53114/oilsch5.txt",
        "/media/25413/oilsch5.txt",
        "/media/31388/oilsch5.txt",
        "/media/42928/oilsch5.txt",
        "/media/48920/oilsch5.txt",
        "/media/26848/oilsch5.txt",
        "/media/38102/oilsch5.txt",
        "/media/43784/oilsch5.txt",
        "/media/50131/oilsch5.txt",
        "/media/21764/oilsch5.txt",
        "/media/26215/oilsch5.txt",
        "/media/37613/oilsch5.txt",
        "/media/43336/oilsch5.txt",
        "/media/49667/oilsch5.txt",
        "/media/21532/oilsch5.txt",
        "/media/29278/oilsch5.txt",
        "/media/40625/oilsch5.txt",
        "/media/40625/oilsch5.txt",
        "/media/46304/oilsch5.txt",
        "/media/52796/oilsch5.txt",
        "/media/19744/oilsch5.txt",
        "/media/28693/oilsch5.txt",
        "/media/40278/oilsch5.txt",
        "/media/45840/oilsch5.txt",
        "/media/52116/oilsch5.txt",
        "/media/27128/oilsch5.txt",
        "/media/38657/oilsch5.txt",
        "/media/44267/oilsch5.txt",
        "/media/50672/oilsch5.txt",
        "/media/21878/oilsch5.txt",
        "/media/28406/oilsch5.txt",
        "/media/39654/oilsch5.txt",
        "/media/45201/oilsch5.txt",
        "/media/51629/oilsch5.txt",
        "/media/24801/oilsch5.txt",
        "/media/30965/oilsch5.txt",
        "/media/42476/oilsch5.txt",
        "/media/48870/oilsch5.txt",
        "/media/24175/oilsch5.txt",
        "/media/30452/oilsch5.txt",
        "/media/42113/oilsch5.txt",
        "/media/47906/oilsch5.txt",
        "/media/54472/oilsch5.txt",
        "/media/23164/oilsch5.txt",
        "/media/29879/oilsch5.txt",
        "/media/41710/oilsch5.txt",
        "/media/47498/oilsch5.txt",
        "/media/53893/oilsch5.txt",
        "/media/27593/oilsch6.txt",
        "/media/39144/oilsch6.txt",
        "/media/44691/oilsch6.txt",
        "/media/51349/oilsch6.txt",
        "/media/22226/oilsch6.txt",
        "/media/29681/oilsch6.txt",
        "/media/41131/oilsch6.txt",
        "/media/46775/oilsch6.txt",
        "/media/53116/oilsch6.txt",
        "/media/25417/oilsch6.txt",
        "/media/31390/oilsch6.txt",
        "/media/42933/oilsch6.txt",
        "/media/48922/oilsch6.txt",
        "/media/26851/oilsch6.txt",
        "/media/38107/oilsch6.txt",
        "/media/43787/oilsch6.txt",
        "/media/50134/oilsch6.txt",
        "/media/26217/oilsch6.txt",
        "/media/37616/oilsch6.txt",
        "/media/43341/oilsch6.txt",
        "/media/49666/oilsch6.txt",
        "/media/21535/oilsch6.txt",
        "/media/29279/oilsch6.txt",
        "/media/40627/oilsch6.txt",
        "/media/46307/oilsch6.txt",
        "/media/52797/oilsch6.txt",
        "/media/19767/oilsch6.txt",
        "/media/28694/oilsch6.txt",
        "/media/40279/oilsch6.txt",
        "/media/45845/oilsch6.txt",
        "/media/52117/oilsch6.txt",
        "/media/27130/oilsch6.txt",
        "/media/38658/oilsch6.txt",
        "/media/44270/oilsch6.txt",
        "/media/50673/oilsch6.txt",
        "/media/21882/oilsch6.txt",
        "/media/28407/oilsch6.txt",
        "/media/39664/oilsch6.txt",
        "/media/45202/oilsch6.txt",
        "/media/51631/oilsch6.txt",
        "/media/24803/oilsch6.txt",
        "/media/30967/oilsch6.txt",
        "/media/42477/oilsch6.txt",
        "/media/48874/oilsch6.txt",
        "/media/24177/oilsch6.txt",
        "/media/30449/oilsch6.txt",
        "/media/42117/oilsch6.txt",
        "/media/47907/oilsch6.txt",
        "/media/54475/oilsch6.txt",
        "/media/23166/oilsch6.txt",
        "/media/29882/oilsch6.txt",
        "/media/41713/oilsch6.txt",
        "/media/47501/oilsch6.txt",
        "/media/53889/oilsch6.txt",
        "/media/27596/oilsch6e.txt",
        "/media/39145/oilsch6e.txt",
        "/media/44692/oilsch6e.txt",
        "/media/51353/oilsch6e.txt",
        "/media/22227/oilsch6e.txt",
        "/media/29682/oilsch6e.txt",
        "/media/41133/oilsch6e.txt",
        "/media/46779/oilsch6e.txt",
        "/media/53124/oilsch6e.txt",
        "/media/25419/oilsch6e.txt",
        "/media/31391/oilsch6e.txt",
        "/media/42931/oilsch6e.txt",
        "/media/48921/oilsch6e.txt",
        "/media/26852/oilsch6e.txt",
        "/media/38108/oilsch6e.txt",
        "/media/43788/oilsch6e.txt",
        "/media/50133/oilsch6e.txt",
        "/media/26220/oilsch6e.txt",
        "/media/37614/oilsch6e.txt",
        "/media/43343/oilsch6e.txt",
        "/media/49668/oilsch6e.txt",
        "/media/21533/oilsch6e.txt",
        "/media/29268/oilsch6e.txt",
        "/media/40629/oilsch6e.txt",
        "/media/46305/oilsch6e.txt",
        "/media/52795/oilsch6e.txt",
        "/media/19781/oilsch6e.txt",
        "/media/28695/oilsch6e.txt",
        "/media/40181/oilsch6e.txt",
        "/media/45841/oilsch6e.txt",
        "/media/52115/oilsch6e.txt",
        "/media/27129/oilsch6e.txt",
        "/media/38663/oilsch6e.txt",
        "/media/44272/oilsch6e.txt",
        "/media/50676/oilsch6e.txt",
        "/media/21883/oilsch6e.txt",
        "/media/28405/oilsch6e.txt",
        "/media/39656/oilsch6e.txt",
        "/media/45200/oilsch6e.txt",
        "/media/51640/oilsch6e.txt",
        "/media/24802/oilsch6e.txt",
        "/media/30968/oilsch6e.txt",
        "/media/42479/oilsch6e.txt",
        "/media/48862/oilsch6e.txt",
        "/media/24176/oilsch6e.txt",
        "/media/30455/oilsch6e.txt",
        "/media/42118/oilsch6e.txt",
        "/media/47909/oilsch6e.txt",
        "/media/54488/oilsch6e.txt",
        "/media/23167/oilsch6e.txt",
        "/media/29881/oilsch6e.txt",
        "/media/41711/oilsch6e.txt",
        "/media/47500/oilsch6e.txt",
        "/media/53895/oilsch6e.txt",
        "/media/27597/oilsch7b.txt",
        "/media/39146/oilsch7b.txt",
        "/media/44698/oilsch7b.txt",
        "/media/51359/oilsch7b.txt",
        "/media/22228/oilsch7b.txt",
        "/media/29685/oilsch7b.txt",
        "/media/41136/oilsch7b.txt",
        "/media/46780/oilsch7b.txt",
        "/media/53120/oilsch7b.txt",
        "/media/25420/oilsch7b.txt",
        "/media/31392/oilsch7b.txt",
        "/media/42937/oilsch7b.txt",
        "/media/48924/oilsch7b.txt",
        "/media/26853/oilsch7b.txt",
        "/media/38110/oilsch7b.txt",
        "/media/43792/oilsch7b.txt",
        "/media/50136/oilsch7b.txt",
        "/media/26221/oilsch7b.txt",
        "/media/37618/oilsch7b.txt",
        "/media/43345/oilsch7b.txt",
        "/media/49670/oilsch7b.txt",
        "/media/21540/oilsch7b.txt",
        "/media/29275/oilsch7b.txt",
        "/media/40632/oilsch7b.txt",
        "/media/46309/oilsch7b.txt",
        "/media/52779/oilsch7b.txt",
        "/media/19771/oilsch7b.txt",
        "/media/28700/oilsch7b.txt",
        "/media/40190/oilsch7b.txt",
        "/media/45842/oilsch7b.txt",
        "/media/52123/oilsch7b.txt",
        "/media/27134/oilsch7b.txt",
        "/media/38665/oilsch7b.txt",
        "/media/44273/oilsch7b.txt",
        "/media/50688/oilsch7b.txt",
        "/media/21884/oilsch7b.txt",
        "/media/28404/oilsch7b.txt",
        "/media/39657/oilsch7b.txt",
        "/media/45206/oilsch7b.txt",
        "/media/51636/oilsch7b.txt",
        "/media/24809/oilsch7b.txt",
        "/media/30970/oilsch7b.txt",
        "/media/42482/oilsch7b.txt",
        "/media/48864/oilsch7b.txt",
        "/media/24178/oilsch7b.txt",
        "/media/30457/oilsch7b.txt",
        "/media/42121/oilsch7b.txt",
        "/media/47912/oilsch7b.txt",
        "/media/54476/oilsch7b.txt",
        "/media/23170/oilsch7b.txt",
        "/media/29885/oilsch7b.txt",
        "/media/41712/oilsch7b.txt",
        "/media/47509/oilsch7b.txt",
        "/media/53905/oilsch7b.txt",
        "/media/27598/oilsch7c.txt",
        "/media/39149/oilsch7c.txt",
        "/media/44695/oilsch7c.txt",
        "/media/51355/oilsch7c.txt",
        "/media/22229/oilsch7c.txt",
        "/media/29684/oilsch7c.txt",
        "/media/41134/oilsch7c.txt",
        "/media/41134/oilsch7c.txt",
        "/media/46781/oilsch7c.txt",
        "/media/53128/oilsch7c.txt",
        "/media/25421/oilsch7c.txt",
        "/media/31393/oilsch7c.txt",
        "/media/42936/oilsch7c.txt",
        "/media/48925/oilsch7c.txt",
        "/media/26854/oilsch7c.txt",
        "/media/38112/oilsch7c.txt",
        "/media/43793/oilsch7c.txt",
        "/media/50138/oilsch7c.txt",
        "/media/26224/oilsch7c.txt",
        "/media/37617/oilsch7c.txt",
        "/media/43346/oilsch7c.txt",
        "/media/21538/oilsch7c.txt",
        "/media/29271/oilsch7c.txt",
        "/media/40633/oilsch7c.txt",
        "/media/40633/oilsch7c.txt",
        "/media/46314/oilsch7c.txt",
        "/media/52785/oilsch7c.txt",
        "/media/19770/oilsch7c.txt",
        "/media/28701/oilsch7c.txt",
        "/media/40194/oilsch7c.txt",
        "/media/45847/oilsch7c.txt",
        "/media/52119/oilsch7c.txt",
        "/media/27135/oilsch7c.txt",
        "/media/38666/oilsch7c.txt",
        "/media/44275/oilsch7c.txt",
        "/media/50681/oilsch7c.txt",
        "/media/21885/oilsch7c.txt",
        "/media/28400/oilsch7c.txt",
        "/media/39658/oilsch7c.txt",
        "/media/45204/oilsch7c.txt",
        "/media/51635/oilsch7c.txt",
        "/media/24804/oilsch7c.txt",
        "/media/30971/oilsch7c.txt",
        "/media/42483/oilsch7c.txt",
        "/media/48865/oilsch7c.txt",
        "/media/24179/oilsch7c.txt",
        "/media/30456/oilsch7c.txt",
        "/media/42120/oilsch7c.txt",
        "/media/47914/oilsch7c.txt",
        "/media/54487/oilsch7c.txt",
        "/media/23168/oilsch7c.txt",
        "/media/29887/oilsch7c.txt",
        "/media/41714/oilsch7c.txt",
        "/media/47507/oilsch7c.txt",
        "/media/53908/oilsch7c.txt",
        "/media/49778/oilsch7c-2.txt",
        "/media/27601/oilsch8.txt",
        "/media/39150/oilsch8.txt",
        "/media/44705/oilsch8.txt",
        "/media/51360/oilsch8.txt",
        "/media/22233/oilsch8.txt",
        "/media/29689/oilsch8.txt",
        "/media/41149/oilsch8.txt",
        "/media/46797/oilsch8.txt",
        "/media/53138/oilsch8.txt",
        "/media/25425/oilsch8.txt",
        "/media/31398/oilsch8.txt",
        "/media/42939/oilsch8.txt",
        "/media/48929/oilsch8.txt",
        "/media/26858/oilsch8.txt",
        "/media/38114/oilsch8.txt",
        "/media/43800/oilsch8.txt",
        "/media/50145/oilsch8.txt",
        "/media/26225/oilsch8.txt",
        "/media/37622/oilsch8.txt",
        "/media/43349/oilsch8.txt",
        "/media/49677/oilsch8.txt",
        "/media/21543/oilsch8.txt",
        "/media/29274/oilsch8.txt",
        "/media/40635/oilsch8.txt",
        "/media/46328/oilsch8.txt",
        "/media/52802/oilsch8.txt",
        "/media/19778/oilsch8.txt",
        "/media/28705/oilsch8.txt",
        "/media/40203/oilsch8.txt",
        "/media/45846/oilsch8.txt",
        "/media/52133/oilsch8.txt",
        "/media/27139/oilsch8.txt",
        "/media/38669/oilsch8.txt",
        "/media/44289/oilsch8.txt",
        "/media/50696/oilsch8.txt",
        "/media/21889/oilsch8.txt",
        "/media/28403/oilsch8.txt",
        "/media/39661/oilsch8.txt",
        "/media/45220/oilsch8.txt",
        "/media/51648/oilsch8.txt",
        "/media/24808/oilsch8.txt",
        "/media/30975/oilsch8.txt",
        "/media/42485/oilsch8.txt",
        "/media/48873/oilsch8.txt",
        "/media/24183/oilsch8.txt",
        "/media/30460/oilsch8.txt",
        "/media/42129/oilsch8.txt",
        "/media/47915/oilsch8.txt",
        "/media/54493/oilsch8.txt",
        "/media/23173/oilsch8.txt",
        "/media/29891/oilsch8.txt",
        "/media/41727/oilsch8.txt",
        "/media/47521/oilsch8.txt",
        "/media/53913/oilsch8.txt",
        "/media/27602/oilsch8a.txt",
        "/media/39148/oilsch8a.txt",
        "/media/44700/oilsch8a.txt",
        "/media/51356/oilsch8a.txt",
        "/media/22231/oilsch8a.txt",
        "/media/29687/oilsch8a.txt",
        "/media/41148/oilsch8a.txt",
        "/media/46790/oilsch8a.txt",
        "/media/53132/oilsch8a.txt",
        "/media/25423/oilsch8a.txt",
        "/media/31395/oilsch8a.txt",
        "/media/42938/oilsch8a.txt",
        "/media/48927/oilsch8a.txt",
        "/media/26856/oilsch8a.txt",
        "/media/38111/oilsch8a.txt",
        "/media/43794/oilsch8a.txt",
        "/media/50140/oilsch8a.txt",
        "/media/26222/oilsch8a.txt",
        "/media/37621/oilsch8a.txt",
        "/media/43355/oilsch8a.txt",
        "/media/49669/oilsch8a.txt",
        "/media/21541/oilsch8a.txt",
        "/media/29272/oilsch8a.txt",
        "/media/40634/oilsch8a.txt",
        "/media/46315/oilsch8a.txt",
        "/media/52789/oilsch8a.txt",
        "/media/19773/oilsch8a.txt",
        "/media/28704/oilsch8a.txt",
        "/media/40201/oilsch8a.txt",
        "/media/45853/oilsch8a.txt",
        "/media/52127/oilsch8a.txt",
        "/media/27138/oilsch8a.txt",
        "/media/38667/oilsch8a.txt",
        "/media/44285/oilsch8a.txt",
        "/media/50680/oilsch8a.txt",
        "/media/21887/oilsch8a.txt",
        "/media/28410/oilsch8a.txt",
        "/media/39659/oilsch8a.txt",
        "/media/45209/oilsch8a.txt",
        "/media/51641/oilsch8a.txt",
        "/media/24805/oilsch8a.txt",
        "/media/30973/oilsch8a.txt",
        "/media/42484/oilsch8a.txt",
        "/media/48869/oilsch8a.txt",
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


    url = 'https://www.rrc.state.tx.us/oil-gas/research-and-statistics/proration-schedules/field/{}/'
    #url = "https://www.rrc.state.tx.us"
    #get_TX_html(url=url, well_ids=schedule_dates, debug=False)
    download_tx_sched_files()


