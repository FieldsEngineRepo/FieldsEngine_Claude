import re
import sys
import os
import urlparse
import mechanize
import pyshark
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import cookielib


class WellProdScraper(object):
    def __init__(self):
        #self.url = "http://www.depreportingservices.state.pa.us/ReportServer/Pages/ReportViewer.aspx?%2fOil_Gas%2fOil_Gas_Well_Production"
        self.url = "http://webapps.rrc.texas.gov/PDQ/generalReportAction.do"
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
        self.cookies           = ''
        self.view_state        = ''''''
        self.event_validation  = ''''''
        self.new_view_state    = ''''''
        self.keep_alive_code   = ''
        self.keep_alive_url    = ''
        #self.txt_value         = '''Jan 2017 (PRODUCTION: Unconventional wells)'''
        self.txt_value         = ''''''
        self.hidden_indices    = ''
        #self.br.addheaders = \
        #    [
        #        ('Accept', ' */*'),
        #        ('Accept-Encoding', 'gzip, deflate'),
        #        ('Accept-Language', 'en-US,en;q=0.9'),
        #        ('Cache-Control', 'no-cache'),
        #        ('Connection', 'keep-alive'),
        #        ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
        #        ('Cookie', self.cookies),
        #        ('Host', 'www.depreportingservices.state.pa.us'),
        #        ('Origin', 'http://www.depreportingservices.state.pa.us'),
        #        ('Referer',
        #         'http://www.depreportingservices.state.pa.us/ReportServer/Pages/ReportViewer.aspx?%2fOil_Gas%2fOil_Gas_Well_Production'),
        #        ('User-agent',
        #         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.99'),
        #        ('X-MicrosoftAjax', 'Delta=true')
        #    ]
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
        saved_form = s.find('form', id='DateRangeForm').prettify()
        html = saved_form.encode('utf8')
        resp = mechanize.make_response(html, [("Content-Type", "text/html")], self.br.geturl(), 200, "OK")
        self.br.set_response(resp)

    def show_forms(self):
        if self.br.forms():
            for form in self.br.forms():
                print form
        else:
            print 'no forms'

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
        if 1:
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
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
                ('Accept-Encoding', 'gzip, deflate'),
                ('Accept-Language', 'en-US,en;q=0.9'),
                ('Cache-Control', 'max-age=0'),
                ('Connection', 'keep-alive'),
                ('Content-Length', 283),
                ('Content-Type', 'application/x-www-form-urlencoded'),
                ('Cookie', self.cookies),
                #('Cookie', '_ga=GA1.2.2011161746.1537473747; JSESSIONID=me0OumW8YITkr4pbFthW7yJbzw5PGK7STcZkVvNslk_xOZ4JD46e!-1518085327; _gid=GA1.2.1001459166.1542140653'),
                ('Host', 'webapps.rrc.texas.gov'),
                ('Origin', 'http://webapps.rrc.texas.gov'),
                ('Referer',
                 'http://webapps.rrc.texas.gov/PDQ/generalReportAction.do'),
                ('Upgrade-Insecure-Requests', 1),
                ('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.99'),
                ('X-MicrosoftAjax', 'Delta=true')
            ]
        response = self.br.open(self.url)
        self.show_forms()
        s = BeautifulSoup(self.br.response().read(), "lxml")
        saved_form = s.find('form', id='MainReportForm').prettify()

        html = saved_form.encode('utf8')
        resp = mechanize.make_response(html, [("Content-Type", "text/html")], self.br.geturl(), 200, "OK")
        self.br.set_response(resp)
        self.br.select_form('MainReportForm')
        self.br.form.set_all_readonly(False)
        self.response_data = response.read()
        if 1:
            print '*+-*'*50
            print self.response_data
            print '*+-*'*50


        #r1 = re.compile(r"__VIEWSTATE\" value=\"/.*?\"")
        #s1 = re.search(r1, self.response_data)
        #self.view_state = s1.group().split('"')[2]

        #r2 = re.compile(r"__EVENTVALIDATION\" value=\"/.*?\"")
        #s2 = re.search(r2, self.response_data)
        #self.event_validation = s2.group().split('"')[2]
        #if self.debug_mode:
        #    print '***' * 50
        #    print self.view_state
        #    print self.event_validation
        #    print '***' * 50


        '''
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
        '''
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

        #r3 = re.compile(r"NavigationCorrector_NewViewState\" value=\"/.*?\"")
        #s3 = re.search(r3, self.response_data)
        #self.new_view_state = s3.group().split('"')[2]

        #self.get_session_codes()
        #if self.debug_mode:
        #    print '***' * 50
        #    print self.view_state
        #    print self.event_validation
        #    print self.new_view_state
        #    print '***' * 50

        # ------------------------------------------------------------------------------------------------------------------------------------------------------------
        if 0:
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

            if 0:
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

            if 0:
                for control in self.br.form.controls:
                    print "type=%s name=%s disabled=%s value=%s" % (control.type, control.name, control.disabled, self.br.form[control.name])
            self.debug_mode = True
            self.submit_webform(controls_add, controls_remove, controls_enable, items_enable, form_data)




if __name__ == '__main__':
    scraper = WellProdScraper()
    scraper.scrape_prod()

