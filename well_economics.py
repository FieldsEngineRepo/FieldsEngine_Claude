import json
import sys
import numpy as np
from globaldata import *

class WellEconomics(object):
    def __init__(self):
        self.PROD_COMMS = ["OIL", "GAS", "CONDENSATE", "NGL", "WATER"]
        self.CURRENT_YEAR = 2019
        self.GOAL = 0
        self.INIT_GUESS = 10
        self.INIT_INCR = 15
        self.INCR_MIN = 0.1
        self.ZERO_range = 0.1
        self.ITER_MAX = 100
        self.OUT_DEFAULT = 999999999
        self.IRR_INIT_GUESS = 0
        self.IRR_INIT_INCR = 0.05
        self.IRR_INCR_MIN = 0.001
        self.IRR_ZERO_range = 0.1
        self.IRR_ITER_MAX = 50
        self.IRR_OUT_DEFAULT = 0.0
        self.IRR_INCR_MAX = 1
        self.CURRENT_YEAR = 2019
        self.AVG_STATE_TAX_RATE = 0.0688
        self.FEDERAL_TAX_RATE = 0.21
        self.USE_PRICE_DEFAULTS = True
        self.COMM_PRICE_DEFAULTS = {
            'Natural Gas': 2.64,
            'NGLs'       : 24.71,
            'Condensate' : 44.78,
            'Crude Oil'  : 55.94
        }
        self.MAIN_COMM_NAME = {
            1: "OIL",
            2: "GAS"
        }
        self.INFLATION_DATA = {
            'capex': {
                1900: 0.104719236,
                1901: 0.104719236,
                1902: 0.104719236,
                1903: 0.104719236,
                1904: 0.104719236,
                1905: 0.104719236,
                1906: 0.104719236,
                1907: 0.104719236,
                1908: 0.104719236,
                1909: 0.104719236,
                1910: 0.104719236,
                1911: 0.104719236,
                1912: 0.104719236,
                1913: 0.104719236,
                1914: 0.104719236,
                1915: 0.104719236,
                1916: 0.104719236,
                1917: 0.104719236,
                1918: 0.104719236,
                1919: 0.104719236,
                1920: 0.104719236,
                1921: 0.104719236,
                1922: 0.104719236,
                1923: 0.104719236,
                1924: 0.104719236,
                1925: 0.104719236,
                1926: 0.104719236,
                1927: 0.104193008,
                1928: 0.103140554,
                1929: 0.104193008,
                1930: 0.101561872,
                1931: 0.094194689,
                1932: 0.093142235,
                1933: 0.091037326,
                1934: 0.091037326,
                1935: 0.092616008,
                1936: 0.09208978,
                1937: 0.09208978,
                1938: 0.090511098,
                1939: 0.070251347,
                1940: 0.07051446,
                1941: 0.072093142,
                1942: 0.076829188,
                1943: 0.076829188,
                1944: 0.076566074,
                1945: 0.077092302,
                1946: 0.08130212,
                1947: 0.089353398,
                1948: 0.101667117,
                1949: 0.103140554,
                1950: 0.105245463,
                1951: 0.114401818,
                1952: 0.115454273,
                1953: 0.119032619,
                1954: 0.119874582,
                1955: 0.122295228,
                1956: 0.127873238,
                1957: 0.134819438,
                1958: 0.136187629,
                1959: 0.137240084,
                1960: 0.136608611,
                1961: 0.135661402,
                1962: 0.134608947,
                1963: 0.133661738,
                1964: 0.132819774,
                1965: 0.133556493,
                1966: 0.134819438,
                1967: 0.136292875,
                1968: 0.137766311,
                1969: 0.140713184,
                1970: 0.144607266,
                1971: 0.152290185,
                1972: 0.155868531,
                1973: 0.148045285,
                1974: 0.204088494,
                1975: 0.241099815,
                1976: 0.257325157,
                1977: 0.276269341,
                1978: 0.293459433,
                1979: 0.35388787,
                1980: 0.456589901,
                1981: 0.541751021,
                1982: 0.526227316,
                1983: 0.501319223,
                1984: 0.498512677,
                1985: 0.488952881,
                1986: 0.397213919,
                1987: 0.422122012,
                1988: 0.425893307,
                1989: 0.462816924,
                1990: 0.499477427,
                1991: 0.477638993,
                1992: 0.467991493,
                1993: 0.463606265,
                1994: 0.466237402,
                1995: 0.491671722,
                1996: 0.516755224,
                1997: 0.505529041,
                1998: 0.446766991,
                1999: 0.469131652,
                2000: 0.570079592,
                2001: 0.535874816,
                2002: 0.523245361,
                2003: 0.59007623,
                2004: 0.711810149,
                2005: 0.87037998,
                2006: 0.973169716,
                2007: 1.046139903,
                2008: 1.310218311,
                2009: 0.929054326,
                2010: 0.973915204,
                2011: 1.170526885,
                2012: 1.171710897,
                2013: 1.155989856,
                2014: 1.118496159,
                2015: 0.845252626,
                2016: 0.77579062,
                2017: 0.872616446,
                2018: 1,
                2019: 1,
                2020: 1,
                2021: 1,
                2022: 1,
                2023: 1,
                2024: 1,
                2025: 1,
                2026: 1,
                2027: 1,
                2028: 1,
                2029: 1,
                2030: 1,
                2031: 1,
                2032: 1,
                2033: 1,
                2034: 1,
                2035: 1,
                2036: 1,
                2037: 1,
                2038: 1,
                2039: 1,
                2040: 1,
                2041: 1,
                2042: 1,
                2043: 1,
                2044: 1,
                2045: 1,
                2046: 1,
                2047: 1,
                2048: 1,
                2049: 1,
                2050: 1,
                2051: 1,
                2052: 1,
                2053: 1,
                2054: 1,
                2055: 1,
                2056: 1,
                2057: 1,
                2058: 1,
                2059: 1,
                2060: 1,
                2061: 1,
                2062: 1,
                2063: 1,
                2064: 1,
                2065: 1,
                2066: 1,
                2067: 1,
                2068: 1,
                2069: 1,
                2070: 1,
                2071: 1,
                2072: 1,
                2073: 1,
                2074: 1,
                2075: 1,
                2076: 1,
                2077: 1,
                2078: 1,
                2079: 1,
                2080: 1,
                2081: 1,
                2082: 1,
                2083: 1,
                2084: 1,
                2085: 1,
                2086: 1,
                2087: 1,
                2088: 1,
                2089: 1,
                2090: 1,
                2091: 1,
                2092: 1,
                2093: 1,
                2094: 1,
                2095: 1,
                2096: 1,
                2097: 1,
                2098: 1,
                2099: 1,
                2100: 1,
                2101: 1,
                2102: 1,
                2103: 1,
                2104: 1,
                2105: 1,
                2106: 1,
                2107: 1,
                2108: 1,
                2109: 1,
                2110: 1,
                2111: 1,
                2112: 1,
                2113: 1,
                2114: 1,
                2115: 1,
                2116: 1,
                2117: 1,
                2118: 1,
                2119: 1,
                2120: 1,
                2121: 1,
                2122: 1,
                2123: 1,
                2124: 1,
                2125: 1,
                2126: 1,
                2127: 1,
                2128: 1,
                2129: 1,
                2130: 1,
                2131: 1,
                2132: 1
            },
            'opex' : {
                1900: 0.036679248,
                1901: 0.036679248,
                1902: 0.036679248,
                1903: 0.036679248,
                1904: 0.036679248,
                1905: 0.036679248,
                1906: 0.036679248,
                1907: 0.036679248,
                1908: 0.036679248,
                1909: 0.036679248,
                1910: 0.036679248,
                1911: 0.036679248,
                1912: 0.036679248,
                1913: 0.036679248,
                1914: 0.036067928,
                1915: 0.036679248,
                1916: 0.044932079,
                1917: 0.061743401,
                1918: 0.069079251,
                1919: 0.073052836,
                1920: 0.081305667,
                1921: 0.051350948,
                1922: 0.051045287,
                1923: 0.05287925,
                1924: 0.051656608,
                1925: 0.054407552,
                1926: 0.052573589,
                1927: 0.050433967,
                1928: 0.051045287,
                1929: 0.050128306,
                1930: 0.0455434,
                1931: 0.038513211,
                1932: 0.034233965,
                1933: 0.034845286,
                1934: 0.039430192,
                1935: 0.042181136,
                1936: 0.042486796,
                1937: 0.0455434,
                1938: 0.041264154,
                1939: 0.040652834,
                1940: 0.041264154,
                1941: 0.046154721,
                1942: 0.051962269,
                1943: 0.054407552,
                1944: 0.054713212,
                1945: 0.055630193,
                1946: 0.063577364,
                1947: 0.078249063,
                1948: 0.093013757,
                1949: 0.092060556,
                1950: 0.091737212,
                1951: 0.094837238,
                1952: 0.096468345,
                1953: 0.101263154,
                1954: 0.103520086,
                1955: 0.103208591,
                1956: 0.106988877,
                1957: 0.114052423,
                1958: 0.114957601,
                1959: 0.113033432,
                1960: 0.114325609,
                1961: 0.114750611,
                1962: 0.114463016,
                1963: 0.114463016,
                1964: 0.114151002,
                1965: 0.114208049,
                1966: 0.115884541,
                1967: 0.118545231,
                1968: 0.121263682,
                1969: 0.127906624,
                1970: 0.132205039,
                1971: 0.138512982,
                1972: 0.140034533,
                1973: 0.150654371,
                1974: 0.2017294,
                1975: 0.225137561,
                1976: 0.233445551,
                1977: 0.250345994,
                1978: 0.270917836,
                1979: 0.3172307,
                1980: 0.401960724,
                1981: 0.496724855,
                1982: 0.491754589,
                1983: 0.474565311,
                1984: 0.475060133,
                1985: 0.463381647,
                1986: 0.500878119,
                1987: 0.53031095,
                1988: 0.511425834,
                1989: 0.558781025,
                1990: 0.61743024,
                1991: 0.603230418,
                1992: 0.585271024,
                1993: 0.561555089,
                1994: 0.552247791,
                1995: 0.584320295,
                1996: 0.637022243,
                1997: 0.632737633,
                1998: 0.530374561,
                1999: 0.600423162,
                2000: 0.729175396,
                2001: 0.708103837,
                2002: 0.700939602,
                2003: 0.786360938,
                2004: 0.91776005,
                2005: 1.130121304,
                2006: 1.283956881,
                2007: 1.403111918,
                2008: 1.5091894,
                2009: 1.211637294,
                2010: 1.340086056,
                2011: 1.479586382,
                2012: 1.45197164,
                2013: 1.430854665,
                2014: 1.347610647,
                2015: 0.992497957,
                2016: 0.872777754,
                2017: 0.936004352,
                2018: 1.023847467,
                2019: 1,
                2020: 1,
                2021: 1,
                2022: 1,
                2023: 1,
                2024: 1,
                2025: 1,
                2026: 1,
                2027: 1,
                2028: 1,
                2029: 1,
                2030: 1,
                2031: 1,
                2032: 1,
                2033: 1,
                2034: 1,
                2035: 1,
                2036: 1,
                2037: 1,
                2038: 1,
                2039: 1,
                2040: 1,
                2041: 1,
                2042: 1,
                2043: 1,
                2044: 1,
                2045: 1,
                2046: 1,
                2047: 1,
                2048: 1,
                2049: 1,
                2050: 1,
                2051: 1,
                2052: 1,
                2053: 1,
                2054: 1,
                2055: 1,
                2056: 1,
                2057: 1,
                2058: 1,
                2059: 1,
                2060: 1,
                2061: 1,
                2062: 1,
                2063: 1,
                2064: 1,
                2065: 1,
                2066: 1,
                2067: 1,
                2068: 1,
                2069: 1,
                2070: 1,
                2071: 1,
                2072: 1,
                2073: 1,
                2074: 1,
                2075: 1,
                2076: 1,
                2077: 1,
                2078: 1,
                2079: 1,
                2080: 1,
                2081: 1,
                2082: 1,
                2083: 1,
                2084: 1,
                2085: 1,
                2086: 1,
                2087: 1,
                2088: 1,
                2089: 1,
                2090: 1,
                2091: 1,
                2092: 1,
                2093: 1,
                2094: 1,
                2095: 1,
                2096: 1,
                2097: 1,
                2098: 1,
                2099: 1,
                2100: 1,
                2101: 1,
                2102: 1,
                2103: 1,
                2104: 1,
                2105: 1,
                2106: 1,
                2107: 1,
                2108: 1,
                2109: 1,
                2110: 1,
                2111: 1,
                2112: 1,
                2113: 1,
                2114: 1,
                2115: 1,
                2116: 1,
                2117: 1,
                2118: 1,
                2119: 1,
                2120: 1,
                2121: 1,
                2122: 1,
                2123: 1,
                2124: 1,
                2125: 1,
                2126: 1,
                2127: 1,
                2128: 1,
                2129: 1,
                2130: 1,
                2131: 1,
                2132: 1
            }
        }



    def init_econ_variables(self, Profile_ID, forecast_type):
        self.forecast_type = forecast_type
        self.well_api = Profile_ID
        self.curr = None
        self.prod_year_num = 0
        self.well_forecast_data = {}
        self.annual_prod_data = {}
        self.comm_price_data = {}
        self.disc_pre_tax_cashflows = []
        self.disc_post_tax_cashflows = []
        self.cash_flows = []
        self.oil_prod = 0
        self.gas_prod = 0
        self.cond_prod = 0
        self.ngls_prod = 0
        self.water_prod = 0
        self.total_prod = 0
        self.main_comm = ""
        self.prod_comm = ""
        self.total_well_cost = 0
        self.net_income = 0
        self.state_tax_value = 0
        self.state_tax_rate = 0
        self.state_id = ""
        self.last_econ_year = self.CURRENT_YEAR
        self.tax_year = self.CURRENT_YEAR
        self.cost_inputs = {
            'type-well'  : {
                "cost_capex_abandonment_usd"  : 0.0,
                "cost_capex_maintenance_usd"  : 0.0,
                "cost_opex_loe_usd_boe"       : 0.0,
                "cost_opex_water_usd_boe"     : 0.0,
                "cost_opex_gpt_usd_boe"       : 0.0,
                "cost_opex_ngl_usd_boe"       : 0.0,
                "cost_opex_fixed_usd"         : 0.0,
                "royalty_rate_pct"            : 0.0,
                "capex_tangible_split_pct"    : 0.0,
                "state_id"                    : 0,
                "main_comm"                   : 1,
                "oil_price"                   : 55.94,
                "gas_price"                   : 2.64,
                "cond_price"                  : 44.78,
                "ngls_price"                  : 24.71,
                "proportional_liquids_rate"   : 0,
                "proportional_gas_rate"       : 0,
                "reduced_liquids_rate"        : 0,
                "reduced_gas_rate"            : 0,
                "state_tax_rate"              : 0.0688,
                "well_life"                   : 25,
                "type_curve"                  : 2.0,
                "total_well_cost_mm_usd"      : 0,
                "cost_capex_drilling_mm_usd"  : 0,
                "cost_capex_completion_mm_usd": 0,
                "cost_capex_facilities_mm_usd": 0
            },
            'single-well': {
                "completion_cost_pct"       : 0.0,
                "drilling_cost_pct"         : 0.0,
                "facilities_cost_pct"       : 0.0,
                "lateral_length_ft"         : 0.0,
                "measured_depth_ft"         : 0.0,
                "well_cost_usd_ft"          : 0.0,
                "cost_capex_abandonment_usd": 0.0,
                "cost_capex_maintenance_usd": 0.0,
                "cost_opex_loe_usd_boe"     : 0.0,
                "cost_opex_water_usd_boe"   : 0.0,
                "cost_opex_gpt_usd_boe"     : 0.0,
                "cost_opex_ngl_usd_boe"     : 0.0,
                "cost_opex_fixed_usd"       : 0.0,
                "royalty_rate_pct"          : 0.0,
                "capex_tangible_split_pct"  : 0.0,
                "state_id"                  : 0,
                "main_comm"                 : 1,
                "oil_price"                 : 55.94,
                "gas_price"                 : 2.64,
                "cond_price"                : 44.78,
                "ngls_price"                : 24.71,
                "proportional_liquids_rate" : 0,
                "proportional_gas_rate"     : 0,
                "reduced_liquids_rate"      : 0,
                "reduced_gas_rate"          : 0,
                "state_tax_rate"            : 0.0688,
                "well_life"                 : 25,
                "cost_abandonment_usd_ft"   : 0.0
            }

        }
        self.econ_summary_params = [
            'royalty_rate_pct',
            'well_eur_oil_bbl',
            'well_eur_gas_mmcf',
            'well_eur_condensate_bbl',
            'well_eur_ngls_bbl',
            'well_eur_total_boe',
            'pre_tax_npv_usd',
            'pre_tax_irr_pct',
            'post_tax_irr_pct',
            'post_tax_npv_usd',
            'pre_tax_cashflow_total_usd',
            'post_tax_cashflow_total_usd',
            'pre_tax_BE_oil_usd_bbl',
            'pre_tax_BE_gas_usd_mcf',
            'post_tax_BE_oil_usd_bbl',
            'post_tax_BE_gas_usd_mcf',
            'total_opex_mm_usd',
            'total_well_cost_mm_usd',
            'cost_capex_drilling_mm_usd',
            'cost_capex_completion_mm_usd',
            'cost_capex_facilities_mm_usd',
            'total_fiscal_take_usd',
            'total_fiscal_take_pct',
            'last_econ_year',
            # *** Added the following output values 20190819 Jason
            'cost_capex_maintenance_usd',  # Corresponds to Annual Maintainance capital expenditure ($)
            'cost_capex_abandonment_usd',  # Corresponds to Abandonment($)
            'cost_opex_fixed_usd',  # Corresponds to Fixed Operating Expenditure($)
            'cost_opex_loe_usd_boe',  # Corresponds to Lease Operating Expenditure($/boe)
            'cost_opex_water_usd_boe',  # Corresponds to Water disposal cost included, else($/boe)
            'cost_opex_gpt_usd_boe',  # Corresponds to Gathering, Processing and Transportation($/boe)
            'cost_opex_ngl_usd_boe',  # Corresponds to NGL Processing fee included, else($/boe)
            'avg_production_cost_usd_boe',  # Corresponds to Average Cost of Production($/boe)
            'total_capex_usd_boe',  # Corresponds to Capex/boe (US$)
            'total_opex_usd_boe'  # Corresponds to Opex/boe (US$)
        ]
        self.econ_annual_params = [
            'year',
            'Oil_Prod_bbl',
            'Gas_Prod_mcf',
            'Cond_Prod_bbl',
            'NGL_Prod_bbl',
            'Water_Prod_bbl',
            'Total_Prod_boe',
            'Gross_Revenue_usd',
            'Capital_Expenditure_usd',
            'Operating_Expenditure_usd',
            'Pre_Tax_Cashflow_usd',
            'Post_Tax_Cashflow_usd',
            'Discount_Pre_Tax_Cashflow_usd',
            'Discount_Post_Tax_Cashflow_usd',
            'Oil_Revenue_usd',
            'Gas_Revenue_usd',
            'Condensate_Revenue_usd',
            'NGL_Revenue_usd',
            'Net_Revenue_usd',
            'Production_Tax_Value_usd',
            'Depreciation_Value_usd',
            'Tangible_Capex_usd',
            'Intangible_Capex_usd',
            'Abandonment_usd',
            'Variable_Opex_usd',
            'Fixed_Opex_usd',
            'Net_Income_usd',
            'State_Tax_Rate_pct',
            'State_Tax_Value_usd',
            'Federal_Tax_Value_usd',
            'Fiscal_Take_usd',
            'Positive_Cash_Flow',
            'Years_Since_Start',
            'Cumulative_Cash_Flow',
            'Payback_Determination',
            'Payback_Period'
        ]

    def calculate_annual_production(self):
        conv_factor = {
            "OIL"       : 1.0,
            "GAS"       : 1.0 / 6.0,
            "CONDENSATE": 1.0,
            "NGL"       : 1.0,
            "WATER"     : 1.0
        }

        # Since the prod_date format is 'YYYYMM' (ex. '201907'), then prod_date[:4] = '2019' and int(prod_date[:4]) = 2019
        prod_years = sorted(list(set([int(month) for month in self.well_forecast_data[self.well_forecast_data.keys()[0]].keys()])))

        self.annual_prod_data = {prod_comm: {prod_year: 0 for prod_year in prod_years} for prod_comm in self.PROD_COMMS}
        self.annual_prod_data["TOTAL"] = {prod_year: 0 for prod_year in prod_years}

        for prod_comm in self.PROD_COMMS:
            for prod_year in prod_years:
                prod_value = sum([self.well_forecast_data[prod_comm][month] for month in self.well_forecast_data[prod_comm].keys() if int(month) == prod_year])
                self.annual_prod_data[prod_comm][prod_year] += prod_value
                if prod_comm != "WATER":
                    self.annual_prod_data["TOTAL"][prod_year] += (conv_factor[prod_comm] * prod_value)
        return self.annual_prod_data

        # Functions for retrieving cost inputs, assumptions, and calculations -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_cost_inputs(self):
        conn = get_connection(server='sql_server', database='US_Wells')
        curr = conn.cursor()
        try:
            # *** Added self.forecast_type as a key to ensure the correct input values are used
            cost_params = sorted(self.cost_inputs[self.forecast_type].keys())
            param_names = ", ".join(["'{}'".format(cost_param) for cost_param in cost_params])
            param_str = ",".join(['ISNULL({},0)'.format(cost_param) for cost_param in cost_params])
            curr.execute("SELECT MainType, production FROM US_Wells.dbo.tblSave_ForecastTypeWellData WITH(NOLOCK) WHERE profile_id='{}' AND GroupType= 'cost inputs' AND MainType IN ({})".format(self.well_api, param_names))
            cost_input_data = curr.fetchall()
            for param_name, param_val in cost_input_data:
                self.cost_inputs[self.forecast_type][param_name.lower()] = param_val
                if self.forecast_type == 'type-well' and param_name.lower() in ["total_well_cost_mm_usd", "cost_capex_drilling_mm_usd", "cost_capex_completion_mm_usd", "cost_capex_facilities_mm_usd"]:
                    self.cost_inputs[self.forecast_type][param_name.lower()] *= 1000000.0

            # *** Added condition to prevent calculation of abandonment for type-well forecasting, since it is provided as an input
            if self.forecast_type == 'single-well':
                if self.cost_inputs[self.forecast_type]["measured_depth_ft"] is not None and self.cost_inputs[self.forecast_type]["measured_depth_ft"] > 0:
                    well_length = float(self.cost_inputs[self.forecast_type]["measured_depth_ft"])
                else:
                    well_length = float(self.cost_inputs[self.forecast_type]["lateral_length_ft"])
                self.cost_inputs[self.forecast_type]["cost_capex_abandonment_usd"] = round(float(self.cost_inputs[self.forecast_type]["cost_abandonment_usd_ft"]) * well_length, 2)
            self.state_id = self.cost_inputs[self.forecast_type]["state_id"]
            self.main_comm = self.cost_inputs[self.forecast_type]["main_comm"]
            return self.cost_inputs

        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print("Unexpected error:", sys.exc_info()[2])
        finally:
            try:
                conn.close()
                curr.close()
            except:
                pass

    def get_capex_tangible(self):
        capex_tangible = 0
        #print 'capex_tangible -- self.prod_year_num: {}'.format(self.prod_year_num)
        if self.prod_year_num == 0:
            # *** Added different conditions for single-well and type-wells forecasts
            if self.forecast_type == 'single-well':
                completion_cost = self.total_well_cost * self.cost_inputs[self.forecast_type]["completion_cost_pct"]
                facilities_cost = self.total_well_cost * self.cost_inputs[self.forecast_type]["facilities_cost_pct"]
            else:
                completion_cost = self.cost_inputs[self.forecast_type]["cost_capex_completion_mm_usd"]
                facilities_cost = self.cost_inputs[self.forecast_type]["cost_capex_facilities_mm_usd"]
            tangible_split = self.cost_inputs[self.forecast_type]["capex_tangible_split_pct"]
            capex_tangible = round(float(completion_cost) + (float(tangible_split) * facilities_cost), 2)
        return capex_tangible

    def get_capex_intangible(self):
        capex_intangible = 0
        #print 'capex_intangible -- self.prod_year_num: {}'.format(self.prod_year_num)
        if self.prod_year_num == 0:
            # *** Added different conditions for single-well and type-wells forecasts
            if self.forecast_type == 'single-well':
                drilling_cost = self.total_well_cost * self.cost_inputs[self.forecast_type]["drilling_cost_pct"]
                facilities_cost = self.total_well_cost * self.cost_inputs[self.forecast_type]["facilities_cost_pct"]
            else:
                drilling_cost = self.cost_inputs[self.forecast_type]["cost_capex_drilling_mm_usd"]
                facilities_cost = self.cost_inputs[self.forecast_type]["cost_capex_facilities_mm_usd"]
            intangible_split = 1 - self.cost_inputs[self.forecast_type]["capex_tangible_split_pct"]
            capex_intangible = round(float(drilling_cost) + (float(intangible_split) * facilities_cost), 2)
        else:
            capex_intangible = round(self.cost_inputs[self.forecast_type]["cost_capex_maintenance_usd"], 2)
        return capex_intangible

    def get_total_loe_cost(self, total_prod, cost_inputs):
        total_loe_cost = 0
        if self.cost_inputs[self.forecast_type]["cost_opex_loe_usd_boe"] > 0:
            total_loe_cost = round(float(self.total_prod) * self.cost_inputs[self.forecast_type]["cost_opex_loe_usd_boe"], 2)
        elif self.cost_inputs[self.forecast_type]["loe_primary_usd_boe"] > 0:
            total_loe_cost = round((float(self.total_prod) * self.cost_inputs[self.forecast_type]["loe_primary_usd_boe"]) + (float(self.water_prod) * self.cost_inputs[self.forecast_type]["cost_opex_water_usd_boe"]), 2)
        return total_loe_cost

    def get_total_gpt_cost(self, ngls_prod, total_prod):
        total_gpt_cost = 0
        if self.cost_inputs[self.forecast_type]["cost_opex_gpt_usd_boe"] > 0:
            total_gpt_cost = round(float(self.total_prod) * self.cost_inputs[self.forecast_type]["cost_opex_gpt_usd_boe"], 2)
        elif self.cost_inputs[self.forecast_type]["gpt_primary_usd_boe"] > 0:
            total_gpt_cost = round((float(self.total_prod) * self.cost_inputs[self.forecast_type]["gpt_primary_usd_boe"]) + (float(self.ngls_prod) * self.cost_inputs[self.forecast_type]["cost_opex_ngl_usd_boe"]), 2)
        return total_gpt_cost

    def get_variable_opex(self):
        variable_opex = 0
        if self.prod_year_num:
            total_loe_cost = self.get_total_loe_cost(self.water_prod, self.total_prod)
            total_gpt_cost = self.get_total_gpt_cost(self.ngls_prod, self.total_prod)
            variable_opex = total_loe_cost + total_gpt_cost
        return float(variable_opex)

    def get_fixed_opex(self):
        fixed_opex = 0
        if self.prod_year_num:
            fixed_opex = self.cost_inputs[self.forecast_type]["cost_opex_fixed_usd"]
        return float(fixed_opex)

    def get_abandonment(self):
        abandonment = 0
        if self.prod_year_num:
            abandonment = self.cost_inputs[self.forecast_type]["cost_capex_abandonment_usd"]
        return float(abandonment)

    def get_inflation_factor(self, prod_year, factor_type):
        inflation_factor = 1.0
        if self.forecast_type == 'single-well':
            try:
                inflation_factor = float(self.INFLATION_DATA[factor_type][prod_year])
            except:
                pass
        return inflation_factor

    def get_production_tax(self):
        production_tax = 0
        if self.prod_year_num:
            royalty_rate = self.cost_inputs[self.forecast_type]["royalty_rate_pct"]
            proportional_liquids_rate = self.cost_inputs[self.forecast_type]["proportional_liquids_rate"]
            proportional_gas_rate = self.cost_inputs[self.forecast_type]["proportional_gas_rate"]
            reduced_liquids_rate = self.cost_inputs[self.forecast_type]["reduced_liquids_rate"]
            reduced_gas_rate = self.cost_inputs[self.forecast_type]["reduced_gas_rate"]

            liquids_revenue = (self.oil_prod * self.oil_price) + (self.cond_prod * self.cond_price)
            liquids_production = self.oil_prod + self.cond_prod
            gas_revenue = (self.gas_prod * self.gas_price) + (self.ngls_prod * self.ngls_price)
            gas_production = self.gas_prod

            liquids_production_tax = float((proportional_liquids_rate * liquids_revenue) + (reduced_liquids_rate * liquids_production))
            gas_production_tax = float((proportional_gas_rate * gas_revenue) + (reduced_gas_rate * gas_production))

            production_tax = (liquids_production_tax + gas_production_tax) * (1 - float(royalty_rate))
        return float(production_tax)

    def get_depreciation(self):
        depreciation = 0
        if self.prod_year_num == 1:
            self.prod_year_num = 0
            #*** Added intangible capex to depreciation
            total_capex = self.get_capex_tangible() + self.get_capex_intangible()
            self.prod_year_num = 1
            depreciation = total_capex
        return float(depreciation)

    def get_state_tax_value(self):
        state_tax_value = 0
        if self.prod_year_num and self.net_income > 0:
            state_tax_value = round(float(self.net_income * self.state_tax_rate), 2)
        return state_tax_value

    def get_federal_tax_value(self):
        federal_tax_value = 0
        if self.prod_year_num and self.net_income > 0:
            federal_tax_value = round(float((self.net_income - self.state_tax_value) * self.FEDERAL_TAX_RATE), 2)
        return federal_tax_value

    def get_cumulative_cash_flow_year(self):
        cumulative_cash_flow_year = 0
        if self.prod_year_num:
            cumulative_cash_flow_year = self.prod_year_num - 1
        return cumulative_cash_flow_year

    def get_royalty_rate(self):
        try:
            royalty_rate = self.cost_inputs[self.forecast_type]["royalty_rate_pct"]
        except:
            royalty_rate = 0
        return royalty_rate

    # Calculate well economics data ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def calc_well_economics(self):
        drilling_cost           = 0
        completion_cost         = 0
        facility_cost           = 0

        ngls_proc_fee           = 0
        water_disp_fee          = 0
        fixed_opex_rate         = 0
        abandonment             = 0
        royalty_rate            = 0
        total_prod              = 0
        pre_tax_NPV             = 0
        post_tax_NPV            = 0

        total_oil_revenue       = 0
        total_gas_revenue       = 0
        total_cond_revenue      = 0
        total_ngls_revenue      = 0
        total_gross_revenue     = 0
        total_net_revenue       = 0
        total_capex_tangible    = 0
        total_capex_intangible  = 0
        total_capex             = 0
        total_variable_opex     = 0
        total_fixed_opex        = 0
        total_opex              = 0
        total_abandonment       = 0
        total_production_tax    = 0
        total_depreciation      = 0
        total_net_income        = 0
        total_state_tax         = 0
        total_federal_tax       = 0
        total_pre_tax_cf        = 0
        total_post_tax_cf       = 0
        total_disc_pre_tax_cf   = 0
        total_disc_post_tax_cf  = 0
        total_fiscal_take_usd   = 0
        total_fiscal_take_pct   = 0

        positive_cash_flow      = 0
        years_since_start       = 0
        cumulative_cash_flow    = 0
        payback_determination   = 0
        payback_period          = 0

        # Determine the years to include in economic forecast
        prod_years = sorted(self.annual_prod_data["TOTAL"].keys())
        development_year = prod_years[0] - 1
        prod_years = [development_year] + prod_years

        self.last_econ_year = max(prod_years)
        prod_years = [prod_year for prod_year in prod_years if prod_year <= self.last_econ_year]

        well_econ_data = {
            "prod_years"                    : prod_years,
            "param_data"                    : {
                "drilling_cost"  : 0,
                "completion_cost": 0,
                "facility_cost"  : 0,
                "ngls_proc_fee"  : 0,
                "water_disp_fee" : 0,
                "fixed_opex_rate": 0,
                "abandonment"    : 0,
                "oil_price"      : 0,
                "gas_price"      : 0,
                "cond_price"     : 0,
                "ngls_price"     : 0,
                "royalty_rate"   : 0
            },
            "Oil_Prod_bbl"                  : {prod_year: 0 for prod_year in prod_years},
            "Gas_Prod_mcf"                  : {prod_year: 0 for prod_year in prod_years},
            "Cond_Prod_bbl"                 : {prod_year: 0 for prod_year in prod_years},
            "NGL_Prod_bbl"                  : {prod_year: 0 for prod_year in prod_years},
            "Water_Prod_bbl"                : {prod_year: 0 for prod_year in prod_years},
            "Total_Prod_boe"                : {prod_year: 0 for prod_year in prod_years},
            "Gross_Revenue_usd"             : {prod_year: 0 for prod_year in prod_years},
            "Capital_Expenditure_usd"       : {prod_year: 0 for prod_year in prod_years},
            "Operating_Expenditure_usd"     : {prod_year: 0 for prod_year in prod_years},
            "Pre_Tax_Cashflow_usd"          : {prod_year: 0 for prod_year in prod_years},
            "Post_Tax_Cashflow_usd"         : {prod_year: 0 for prod_year in prod_years},
            "Discount_Pre_Tax_Cashflow_usd" : {prod_year: 0 for prod_year in prod_years},
            "Discount_Post_Tax_Cashflow_usd": {prod_year: 0 for prod_year in prod_years},
            "Oil_Revenue_usd"               : {prod_year: 0 for prod_year in prod_years},
            "Gas_Revenue_usd"               : {prod_year: 0 for prod_year in prod_years},
            "Condensate_Revenue_usd"        : {prod_year: 0 for prod_year in prod_years},
            "NGL_Revenue_usd"               : {prod_year: 0 for prod_year in prod_years},
            "Net_Revenue_usd"               : {prod_year: 0 for prod_year in prod_years},
            "Production_Tax_Value_usd"      : {prod_year: 0 for prod_year in prod_years},
            "Depreciation_Value_usd"        : {prod_year: 0 for prod_year in prod_years},
            "Tangible_Capex_usd"            : {prod_year: 0 for prod_year in prod_years},
            "Intangible_Capex_usd"          : {prod_year: 0 for prod_year in prod_years},
            "Abandonment_usd"               : {prod_year: 0 for prod_year in prod_years},
            "Variable_Opex_usd"             : {prod_year: 0 for prod_year in prod_years},
            "Fixed_Opex_usd"                : {prod_year: 0 for prod_year in prod_years},
            "Net_Income_usd"                : {prod_year: 0 for prod_year in prod_years},
            "State_Tax_Rate_pct"            : {prod_year: 0 for prod_year in prod_years},
            "State_Tax_Value_usd"           : {prod_year: 0 for prod_year in prod_years},
            "Federal_Tax_Value_usd"         : {prod_year: 0 for prod_year in prod_years},
            "Fiscal_Take_usd"               : {prod_year: 0 for prod_year in prod_years},
            "Positive_Cash_Flow"            : {prod_year: 0 for prod_year in prod_years},
            "Years_Since_Start"	            : {prod_year: 0 for prod_year in prod_years},
            "Cumulative_Cash_Flow"	        : {prod_year: 0 for prod_year in prod_years},
            "Payback_Determination"	        : {prod_year: None for prod_year in prod_years},
            "Payback_Period"                : {prod_year: None for prod_year in prod_years},

            "last_econ_year"                : self.last_econ_year,
            "well_api"                      : self.well_api,
            "state_id"                      : int(self.state_id),
            "total_oil_revenue"             : 0,
            "total_gas_revenue"             : 0,
            "total_cond_revenue"            : 0,
            "total_ngls_revenue"            : 0,
            "total_gross_revenue"           : 0,
            "total_net_revenue"             : 0,
            "total_capex_tangible"          : 0,
            "total_capex_intangible"        : 0,
            "total_capex"                   : 0,
            "total_variable_opex"           : 0,
            "total_fixed_opex"              : 0,
            "total_abandonment"             : 0,
            "total_production_tax"          : 0,
            "total_depreciation"            : 0,
            "total_net_income"              : 0,
            "total_state_tax"               : 0,
            "total_federal_tax"             : 0,
            "total_disc_pre_tax_cf"         : 0,
            "total_disc_post_tax_cf"        : 0,
            "total_fiscal_take_usd"         : 0,
            "total_fiscal_take_pct"         : 0,

            "royalty_rate_pct"              : 0,
            "pre_tax_cashflow_total_usd"    : 0,
            "post_tax_cashflow_total_usd"   : 0,
            "pre_tax_BE_oil_usd_bbl"        : 0,
            "pre_tax_BE_gas_usd_mcf"        : 0,
            "post_tax_BE_oil_usd_bbl"       : 0,
            "post_tax_BE_gas_usd_mcf"       : 0,
            "well_eur_oil_bbl"              : 0,
            "well_eur_gas_mmcf"             : 0,
            "well_eur_condensate_bbl"       : 0,
            "well_eur_ngls_bbl"             : 0,
            "well_eur_total_boe"            : 0,
            "pre_tax_npv_usd"               : 0,
            "pre_tax_irr_pct"               : 0,
            "post_tax_npv_usd"              : 0,
            "post_tax_irr_pct"              : 0,
            "total_opex_mm_usd"             : 0,
            "total_well_cost_mm_usd"        : 0,
            "cost_capex_drilling_mm_usd"    : 0,
            "cost_capex_completion_mm_usd"  : 0,
            "cost_capex_facilities_mm_usd"  : 0,
            "cost_capex_maintenance_usd"    : 0,
            "cost_capex_abandonment_usd"    : 0,
            "cost_opex_fixed_usd"           : 0,
            "cost_opex_loe_usd_boe"         : 0,
            "cost_opex_water_usd_boe"       : 0,
            "cost_opex_gpt_usd_boe"         : 0,
            "cost_opex_ngl_usd_boe"         : 0,
            "avg_production_cost_usd_ft"    : 0,
            "total_capex_usd_boe"           : 0,
            "total_opex_usd_boe"            : 0
        }

        self.oil_price  = self.cost_inputs[self.forecast_type]["oil_price"]
        self.gas_price  = self.cost_inputs[self.forecast_type]["gas_price"]
        self.cond_price = self.cost_inputs[self.forecast_type]["cond_price"]
        self.ngls_price = self.cost_inputs[self.forecast_type]["ngls_price"]

        well_econ_data["param_data"]["oil_price"]  = self.oil_price
        well_econ_data["param_data"]["gas_price"]  = self.gas_price
        well_econ_data["param_data"]["cond_price"] = self.cond_price
        well_econ_data["param_data"]["ngls_price"] = self.ngls_price

        royalty_rate = self.get_royalty_rate()

        well_econ_data["param_data"]["royalty_rate"] = royalty_rate
        well_econ_data["royalty_rate_pct"]           = royalty_rate

        # *** Added different conditions for single-well and type-wells forecasts
        if self.forecast_type == 'type-well':
            self.total_well_cost = self.cost_inputs[self.forecast_type]["total_well_cost_mm_usd"]

            well_econ_data["param_data"]["drilling_cost"]   = self.cost_inputs[self.forecast_type]["cost_capex_drilling_mm_usd"]
            drilling_cost = well_econ_data["param_data"]["drilling_cost"]

            well_econ_data["param_data"]["completion_cost"] = self.cost_inputs[self.forecast_type]["cost_capex_completion_mm_usd"]
            completion_cost = well_econ_data["param_data"]["completion_cost"]

            well_econ_data["param_data"]["facilities_cost"] = self.cost_inputs[self.forecast_type]["cost_capex_facilities_mm_usd"]
            facility_cost = well_econ_data["param_data"]["facilities_cost"]
        else:
            self.total_well_cost = self.cost_inputs[self.forecast_type]["well_cost_usd_ft"] * self.cost_inputs[self.forecast_type]["lateral_length_ft"]

            if self.cost_inputs[self.forecast_type]["drilling_cost_pct"] is not None:
                drilling_cost = self.total_well_cost * self.cost_inputs[self.forecast_type]["drilling_cost_pct"]
                well_econ_data["param_data"]["drilling_cost"] = drilling_cost

            if self.cost_inputs[self.forecast_type]["completion_cost_pct"] is not None:
                completion_cost = self.total_well_cost * self.cost_inputs[self.forecast_type]["completion_cost_pct"]
                well_econ_data["param_data"]["completion_cost"] = completion_cost

            if self.cost_inputs[self.forecast_type]["facilities_cost_pct"] is not None:
                facility_cost = self.total_well_cost * self.cost_inputs[self.forecast_type]["facilities_cost_pct"]
                well_econ_data["param_data"]["facility_cost"] = facility_cost

        if self.cost_inputs[self.forecast_type]["cost_opex_ngl_usd_boe"] is not None:
            ngls_proc_fee = self.cost_inputs[self.forecast_type]["cost_opex_ngl_usd_boe"]
            well_econ_data["param_data"]["ngls_proc_fee"]   = ngls_proc_fee
            well_econ_data["cost_opex_ngl_usd_boe"]         = ngls_proc_fee

        if self.cost_inputs[self.forecast_type]["cost_opex_water_usd_boe"] is not None:
            water_disp_fee = self.cost_inputs[self.forecast_type]["cost_opex_water_usd_boe"]
            well_econ_data["param_data"]["water_disp_fee"] = water_disp_fee
            well_econ_data["cost_opex_water_usd_boe"]      = water_disp_fee

        if self.cost_inputs[self.forecast_type]["cost_opex_fixed_usd"] is not None:
            fixed_opex_rate = self.cost_inputs[self.forecast_type]["cost_opex_fixed_usd"]
            well_econ_data["param_data"]["fixed_opex_rate"] = fixed_opex_rate
            well_econ_data["cost_opex_fixed_usd"]           = fixed_opex_rate

        if self.cost_inputs[self.forecast_type]["cost_capex_abandonment_usd"] is not None:
            abandonment = self.cost_inputs[self.forecast_type]["cost_capex_abandonment_usd"]
            well_econ_data["param_data"]["abandonment"] = abandonment
            well_econ_data["cost_capex_abandonment_usd"]= abandonment

        well_econ_data["cost_capex_maintenance_usd"]  = self.cost_inputs[self.forecast_type]["cost_capex_maintenance_usd"]
        well_econ_data["cost_opex_loe_usd_boe"]       = self.cost_inputs[self.forecast_type]["cost_opex_loe_usd_boe"]
        well_econ_data["cost_opex_gpt_usd_boe"]       = self.cost_inputs[self.forecast_type]["cost_opex_gpt_usd_boe"]
        well_econ_data["avg_production_cost_usd_boe"] = well_econ_data["cost_opex_loe_usd_boe"] + well_econ_data["cost_opex_gpt_usd_boe"]

        econ_limit_threshold = 2
        if self.forecast_type == 'single-well':
            econ_limit_threshold = self.CURRENT_YEAR + 2

        forecast_econ = True
        econ_year = 0
        for prod_year in prod_years:
            self.tax_year = prod_year
            self.prod_year_num = prod_year - development_year
            if self.prod_year_num:
                self.oil_prod   = self.annual_prod_data["OIL"][prod_year]
                self.gas_prod   = self.annual_prod_data["GAS"][prod_year]
                self.cond_prod  = self.annual_prod_data["CONDENSATE"][prod_year]
                self.ngls_prod  = self.annual_prod_data["NGL"][prod_year]
                self.water_prod = self.annual_prod_data["WATER"][prod_year]
                self.total_prod = self.annual_prod_data["TOTAL"][prod_year]
            else:
                self.oil_prod   = 0
                self.gas_prod   = 0
                self.cond_prod  = 0
                self.ngls_prod  = 0
                self.water_prod = 0
                self.total_prod = 0
            if (self.total_prod or not self.prod_year_num) and forecast_econ:
                oil_revenue = (self.oil_prod * self.oil_price)
                gas_revenue = (self.gas_prod * self.gas_price)
                cond_revenue = (self.cond_prod * self.cond_price)
                ngls_revenue = (self.ngls_prod * self.ngls_price)
                gross_revenue = round(float((self.oil_prod * self.oil_price) + (self.gas_prod * self.gas_price) + (self.cond_prod * self.cond_price) + (self.ngls_prod * self.ngls_price)), 2)
                net_revenue = round(float(gross_revenue * (1 - royalty_rate)), 2)
                prod_tax_value = self.get_production_tax()
                depreciation = self.get_depreciation()

                capex_inflation  = self.get_inflation_factor(prod_year, 'capex')
                capex_tangible   = self.get_capex_tangible() * capex_inflation
                capex_intangible = self.get_capex_intangible() * capex_inflation
                capex            = round(float(capex_tangible + capex_intangible), 2)

                opex_inflation   = self.get_inflation_factor(prod_year, 'opex')
                variable_opex    = self.get_variable_opex() * opex_inflation
                fixed_opex       = self.get_fixed_opex() * opex_inflation
                opex             = round(float(variable_opex + fixed_opex), 2)

                self.net_income = round(float(net_revenue - (prod_tax_value + capex + opex + depreciation)), 2)
                self.state_tax_rate = self.cost_inputs[self.forecast_type]["state_tax_rate"]
                self.state_tax_value = self.get_state_tax_value()
                federal_tax_value = self.get_federal_tax_value()

                post_tax_cf = round(float(net_revenue - (capex + opex + prod_tax_value + self.state_tax_value + federal_tax_value)), 2)
                pre_tax_cf = round(float(gross_revenue - capex - opex), 2)
                disc_pre_tax_cf = round(float(pre_tax_cf / float(1.1 ** (self.prod_year_num))), 2)
                disc_post_tax_cf = round(float(post_tax_cf / float(1.1 ** (self.prod_year_num))), 2)
                royalty_rate_value = round(float(gross_revenue) * float(royalty_rate), 2)
                fiscal_take_value = round(float(prod_tax_value + self.state_tax_value + federal_tax_value + royalty_rate_value), 2)

                cumulative_cash_flow = well_econ_data["Cumulative_Cash_Flow"][prod_years[self.get_cumulative_cash_flow_year()]] + post_tax_cf

                positive_cash_flow = 1 if cumulative_cash_flow > 0 else 0
                years_since_start = self.prod_year_num + 1

                if pre_tax_cf > 0 or prod_year < econ_limit_threshold:
                    econ_year = prod_year
                    self.disc_pre_tax_cashflows.append(disc_pre_tax_cf)
                    self.disc_post_tax_cashflows.append(disc_post_tax_cf)

                    pre_tax_NPV            += disc_pre_tax_cf
                    post_tax_NPV           += disc_post_tax_cf
                    total_oil_revenue      += oil_revenue
                    total_gas_revenue      += gas_revenue
                    total_cond_revenue     += cond_revenue
                    total_ngls_revenue     += ngls_revenue
                    total_gross_revenue    += gross_revenue
                    total_net_revenue      += net_revenue
                    total_capex_tangible   += capex_tangible
                    total_capex_intangible += capex_intangible
                    total_capex            += capex
                    total_variable_opex    += variable_opex
                    total_fixed_opex       += fixed_opex
                    total_opex             += opex
                    total_abandonment      += 0
                    total_production_tax   += prod_tax_value
                    total_depreciation     += depreciation
                    total_net_income       += self.net_income
                    total_state_tax        += self.state_tax_value
                    total_federal_tax      += federal_tax_value
                    total_pre_tax_cf       += pre_tax_cf
                    total_post_tax_cf      += post_tax_cf
                    total_disc_pre_tax_cf  += disc_pre_tax_cf
                    total_disc_post_tax_cf += disc_post_tax_cf
                    total_fiscal_take_usd  += fiscal_take_value

                    well_econ_data["Oil_Prod_bbl"][prod_year] = self.oil_prod
                    well_econ_data["Gas_Prod_mcf"][prod_year] = self.gas_prod
                    well_econ_data["Cond_Prod_bbl"][prod_year] = self.cond_prod
                    well_econ_data["NGL_Prod_bbl"][prod_year] = self.ngls_prod
                    well_econ_data["Water_Prod_bbl"][prod_year] = self.water_prod
                    well_econ_data["Total_Prod_boe"][prod_year] = self.total_prod
                    well_econ_data["Oil_Revenue_usd"][prod_year] = self.oil_price * self.oil_prod
                    well_econ_data["Gas_Revenue_usd"][prod_year] = self.gas_price * self.gas_prod
                    well_econ_data["Condensate_Revenue_usd"][prod_year] = self.cond_price * self.cond_prod
                    well_econ_data["NGL_Revenue_usd"][prod_year] = self.ngls_price * self.ngls_prod
                    well_econ_data["Gross_Revenue_usd"][prod_year] = gross_revenue
                    well_econ_data["Net_Revenue_usd"][prod_year] = net_revenue
                    well_econ_data["Production_Tax_Value_usd"][prod_year] = prod_tax_value
                    well_econ_data["Depreciation_Value_usd"][prod_year] = depreciation
                    well_econ_data["Capital_Expenditure_usd"][prod_year] = capex
                    well_econ_data["Tangible_Capex_usd"][prod_year] = capex_tangible
                    well_econ_data["Intangible_Capex_usd"][prod_year] = capex_intangible
                    well_econ_data["Abandonment_usd"][prod_year] = 0
                    well_econ_data["Operating_Expenditure_usd"][prod_year] = opex
                    well_econ_data["Variable_Opex_usd"][prod_year] = variable_opex
                    well_econ_data["Fixed_Opex_usd"][prod_year] = fixed_opex
                    well_econ_data["Net_Income_usd"][prod_year] = self.net_income
                    well_econ_data["State_Tax_Rate_pct"][prod_year] = self.state_tax_rate
                    well_econ_data["State_Tax_Value_usd"][prod_year] = self.state_tax_value
                    well_econ_data["Federal_Tax_Value_usd"][prod_year] = federal_tax_value
                    well_econ_data["Post_Tax_Cashflow_usd"][prod_year] = post_tax_cf
                    well_econ_data["Pre_Tax_Cashflow_usd"][prod_year] = pre_tax_cf
                    well_econ_data["Discount_Pre_Tax_Cashflow_usd"][prod_year] = disc_pre_tax_cf
                    well_econ_data["Discount_Post_Tax_Cashflow_usd"][prod_year] = disc_post_tax_cf
                    well_econ_data["Fiscal_Take_usd"][prod_year] = fiscal_take_value
                    well_econ_data["Positive_Cash_Flow"][prod_year] = positive_cash_flow
                    well_econ_data["Years_Since_Start"	][prod_year] = years_since_start
                    well_econ_data["Cumulative_Cash_Flow"][prod_year] = cumulative_cash_flow
                else:
                    forecast_econ = False
                    self.last_econ_year = econ_year

        econ_year += 1
        self.tax_year = econ_year
        self.prod_year_num = econ_year - development_year
        oil_revenue             = 0
        gas_revenue             = 0
        cond_revenue            = 0
        ngls_revenue            = 0
        gross_revenue           = 0
        net_revenue             = 0
        variable_opex           = 0
        fixed_opex              = 0
        prod_tax_value          = 0
        capex_intangible        = 0
        capex_tangible          = 0
        depreciation            = 0
        royalty_rate_value      = 0
        self.state_tax_rate     = 0
        self.net_income         = 0
        self.state_tax_value    = 0
        federal_tax_value       = 0
        opex                    = 0
        fiscal_take_value       = 0

        abandonment             = self.get_abandonment()
        capex                   = round(float(abandonment), 2)
        pre_tax_cf              = round(float(-abandonment), 2)
        post_tax_cf             = round(float(-abandonment), 2)
        disc_pre_tax_cf         = round(float(pre_tax_cf / float(1.1 ** (self.prod_year_num))), 2)
        disc_post_tax_cf        = round(float(post_tax_cf / float(1.1 ** (self.prod_year_num))), 2)

        self.disc_pre_tax_cashflows.append(disc_pre_tax_cf)
        self.disc_post_tax_cashflows.append(disc_post_tax_cf)

        pre_tax_NPV            += disc_pre_tax_cf
        post_tax_NPV           += disc_post_tax_cf
        total_capex            += capex
        total_abandonment      += abandonment
        total_pre_tax_cf       += pre_tax_cf
        total_post_tax_cf      += post_tax_cf
        total_disc_pre_tax_cf  += disc_pre_tax_cf
        total_disc_post_tax_cf += disc_post_tax_cf
        total_fiscal_take_pct   = round(float(total_fiscal_take_usd) / float(1 if total_pre_tax_cf == 0 else total_pre_tax_cf), 2)

        if well_econ_data["Positive_Cash_Flow"][econ_year-1] == 1:
            first_positive_year     = min([prod_year for prod_year in well_econ_data["Positive_Cash_Flow"].keys() if well_econ_data["Positive_Cash_Flow"][prod_year] == 1])
            first_positive_cf       = float(well_econ_data["Cumulative_Cash_Flow"][first_positive_year])
            last_negative_cf        = float(well_econ_data["Cumulative_Cash_Flow"][first_positive_year -1])
            payback_det_years       = well_econ_data["Years_Since_Start"][first_positive_year]
            payback_det_months      = 12 - int((first_positive_cf / (first_positive_cf - last_negative_cf)) * 12)
            well_econ_data["Payback_Determination"          ][prod_years[0]] = payback_det_years
            well_econ_data["Payback_Determination"          ][prod_years[1]] = payback_det_months
            well_econ_data["Payback_Period"                 ][prod_years[0]] = round((payback_det_years - 1) + (float(payback_det_months ) /12.0), 1)
        else:
            first_positive_year     = 0

        well_econ_data["Oil_Prod_bbl"                   ][econ_year] = 0
        well_econ_data["Gas_Prod_mcf"                   ][econ_year] = 0
        well_econ_data["Cond_Prod_bbl"                  ][econ_year] = 0
        well_econ_data["NGL_Prod_bbl"                   ][econ_year] = 0
        well_econ_data["Water_Prod_bbl"                 ][econ_year] = 0
        well_econ_data["Total_Prod_boe"                 ][econ_year] = 0
        well_econ_data["Oil_Revenue_usd"                ][econ_year] = 0
        well_econ_data["Gas_Revenue_usd"                ][econ_year] = 0
        well_econ_data["Condensate_Revenue_usd"         ][econ_year] = 0
        well_econ_data["NGL_Revenue_usd"                ][econ_year] = 0
        well_econ_data["Gross_Revenue_usd"              ][econ_year] = 0
        well_econ_data["Net_Revenue_usd"                ][econ_year] = 0
        well_econ_data["Production_Tax_Value_usd"       ][econ_year] = 0
        well_econ_data["Depreciation_Value_usd"         ][econ_year] = 0
        well_econ_data["Tangible_Capex_usd"             ][econ_year] = 0
        well_econ_data["Intangible_Capex_usd"           ][econ_year] = 0
        well_econ_data["Abandonment_usd"                ][econ_year] = abandonment
        well_econ_data["Capital_Expenditure_usd"        ][econ_year] = capex
        well_econ_data["Variable_Opex_usd"              ][econ_year] = 0
        well_econ_data["Fixed_Opex_usd"                 ][econ_year] = 0
        well_econ_data["Operating_Expenditure_usd"      ][econ_year] = 0
        well_econ_data["Net_Income_usd"                 ][econ_year] = 0
        well_econ_data["State_Tax_Rate_pct"             ][econ_year] = 0
        well_econ_data["State_Tax_Value_usd"            ][econ_year] = 0
        well_econ_data["Federal_Tax_Value_usd"          ][econ_year] = 0
        well_econ_data["Pre_Tax_Cashflow_usd"           ][econ_year] = pre_tax_cf
        well_econ_data["Post_Tax_Cashflow_usd"          ][econ_year] = post_tax_cf
        well_econ_data["Discount_Pre_Tax_Cashflow_usd"  ][econ_year] = disc_pre_tax_cf
        well_econ_data["Discount_Post_Tax_Cashflow_usd" ][econ_year] = disc_post_tax_cf
        well_econ_data["Fiscal_Take_usd"                ][econ_year] = 0
        well_econ_data["Cumulative_Cash_Flow"           ][econ_year] = None
        well_econ_data["Positive_Cash_Flow"             ][econ_year] = None
        well_econ_data["Payback_Determination"          ][econ_year] = None
        well_econ_data["Payback_Period"                 ][econ_year] = None
        well_econ_data["Years_Since_Start"              ][econ_year] = self.prod_year_num + 1


        # Parameters not stored in database for each well
        well_econ_data["total_oil_revenue"	         ] = total_oil_revenue
        well_econ_data["total_gas_revenue"	         ] = total_gas_revenue
        well_econ_data["total_cond_revenue"	         ] = total_cond_revenue
        well_econ_data["total_ngls_revenue"	         ] = total_ngls_revenue
        well_econ_data["total_gross_revenue"         ] = total_gross_revenue
        well_econ_data["total_net_revenue"	         ] = total_net_revenue
        well_econ_data["total_capex_tangible"        ] = total_capex_tangible
        well_econ_data["total_capex_intangible"      ] = total_capex_intangible
        well_econ_data["total_capex"		         ] = total_capex
        well_econ_data["total_variable_opex"         ] = total_variable_opex
        well_econ_data["total_fixed_opex"	         ] = total_fixed_opex
        well_econ_data["total_abandonment"	         ] = total_abandonment
        well_econ_data["total_production_tax"        ] = total_production_tax
        well_econ_data["total_depreciation"	         ] = total_depreciation
        well_econ_data["total_net_income"	         ] = total_net_income
        well_econ_data["total_state_tax"	         ] = total_state_tax
        well_econ_data["total_federal_tax"	         ] = total_federal_tax
        well_econ_data["total_disc_pre_tax_cf"       ] = total_disc_pre_tax_cf
        well_econ_data["total_disc_post_tax_cf"      ] = total_disc_post_tax_cf
        well_econ_data["last_econ_year"              ] = self.last_econ_year
        well_econ_data["prod_years"                  ] = [prod_year for prod_year in prod_years if prod_year <= self.last_econ_year]

        # Parameters stored in tblUSWell_Parameters for each well
        well_econ_data["pre_tax_cashflow_total_usd"	 ] = total_pre_tax_cf
        well_econ_data["post_tax_cashflow_total_usd" ] = total_post_tax_cf
        well_econ_data["total_opex_mm_usd"			 ] = total_opex
        well_econ_data["post_tax_npv_usd"            ] = post_tax_NPV
        well_econ_data["pre_tax_npv_usd"             ] = pre_tax_NPV
        well_econ_data["total_well_cost_mm_usd"      ] = self.total_well_cost
        well_econ_data["cost_capex_drilling_mm_usd"  ] = drilling_cost
        well_econ_data["cost_capex_completion_mm_usd"] = completion_cost
        well_econ_data["cost_capex_facilities_mm_usd"] = facility_cost
        well_econ_data["total_fiscal_take_usd"       ] = total_fiscal_take_usd
        well_econ_data["total_fiscal_take_pct"       ] = total_fiscal_take_pct

        print [well_econ_data['Capital_Expenditure_usd'][prod_year] for prod_year in prod_years]

        return well_econ_data

    def get_eur_totals(self, well_econ_data):
        eur_params = {
            "Oil_Prod_bbl"  : "well_eur_oil_bbl",
            "Gas_Prod_mcf"  : "well_eur_gas_mmcf",
            "Cond_Prod_bbl" : "well_eur_condensate_bbl",
            "NGL_Prod_bbl"  : "well_eur_ngls_bbl",
            "Total_Prod_boe": "well_eur_total_boe"
        }
        for prod_col in eur_params.keys():
            prod_years = sorted([prod_year for prod_year in well_econ_data[prod_col].keys() if prod_year <= self.last_econ_year])
            for prod_year in prod_years:
                if prod_col == 'Gas_Prod_mcf':
                    well_econ_data[eur_params[prod_col]] += round(float(well_econ_data[prod_col][prod_year]) / 1000.0, 2)
                else:
                    well_econ_data[eur_params[prod_col]] += round(float(well_econ_data[prod_col][prod_year]), 2)

        # *** Added following lines to calculate capex and opex per boe after total well eur is calculated 20190819 Jason
        well_econ_data["total_capex_usd_boe"] = round(float(well_econ_data["total_capex"])/float(well_econ_data["well_eur_total_boe"]))
        well_econ_data["total_opex_usd_boe" ] = round(float(well_econ_data["total_opex_mm_usd"])/float(well_econ_data["well_eur_total_boe"]))
        return well_econ_data

    def calc_pre_tax_breakeven(self, well_econ_data, debug=False):
        main_comm_name = self.MAIN_COMM_NAME[self.main_comm]
        pre_tax_be = {"OIL": 0, "GAS": 0}
        prod_years = well_econ_data["prod_years"][1:]
        prod_year_nums = range(len(prod_years))
        prod_units = {"OIL": "bbl", "GAS": "mcf"}

        capital_expenditure = (well_econ_data["param_data"]["drilling_cost"] + well_econ_data["param_data"]["completion_cost"] + well_econ_data["param_data"]["facility_cost"])
        if debug:
            print 'drilling_cost  : {}'.format(well_econ_data["param_data"]["drilling_cost"])
            print 'completion_cost: {}'.format(well_econ_data["param_data"]["completion_cost"])
            print 'facilities_cost: {}'.format(well_econ_data["param_data"]["facility_cost"])
            print 'drilling_cost  : {}'.format(well_econ_data["cost_capex_drilling_mm_usd"])
            print 'completion_cost: {}'.format(well_econ_data["cost_capex_completion_mm_usd"])
            print 'facilities_cost: {}'.format(well_econ_data["cost_capex_facilities_mm_usd"])
            print 'capex: {}'.format(capital_expenditure)
            print 'well_cost: {}'.format(well_econ_data["total_well_cost_mm_usd"])


        abandonment_costs = float(well_econ_data["param_data"]["abandonment"]) / float((1.1) ** (self.cost_inputs[self.forecast_type]["well_life"] + 1))

        discount_vector = np.array([1.0 / (1.1 ** (prod_year_num)) for prod_year_num in prod_year_nums])
        total_opex_vector = np.array([float(well_econ_data["Operating_Expenditure_usd"][prod_year]) for prod_year in prod_years])

        discounted_opex = np.dot(discount_vector, total_opex_vector)

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if main_comm_name == "OIL" or sum([well_econ_data["Oil_Prod_bbl"][prod_year] for prod_year in prod_years]) == 0:
            discounted_oil = 0
        else:
            oil_revenue_vector = np.array([well_econ_data["Oil_Revenue_usd"][prod_year] for prod_year in prod_years])
            discounted_oil = np.dot(discount_vector, oil_revenue_vector)
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if main_comm_name == "GAS" or sum([well_econ_data["Gas_Prod_mcf"][prod_year] for prod_year in prod_years]) == 0:
            discounted_gas = 0
        else:
            gas_revenue_vector = np.array([well_econ_data["Gas_Revenue_usd"][prod_year] for prod_year in prod_years])
            discounted_gas = np.dot(discount_vector, gas_revenue_vector)
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if sum([well_econ_data["Cond_Prod_bbl"][prod_year] for prod_year in prod_years]) == 0:
            discounted_cond = 0
        else:
            cond_revenue_vector = np.array([well_econ_data["Condensate_Revenue_usd"][prod_year] for prod_year in prod_years])
            discounted_cond = np.dot(discount_vector, cond_revenue_vector)
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if sum([well_econ_data["NGL_Prod_bbl"][prod_year] for prod_year in prod_years]) == 0:
            discounted_ngls = 0
        else:
            ngls_revenue_vector = np.array([well_econ_data["NGL_Revenue_usd"][prod_year] for prod_year in prod_years])
            discounted_ngls = np.dot(discount_vector, ngls_revenue_vector)
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        discounted_revenue = ((discounted_oil + discounted_gas + discounted_cond + discounted_ngls) * (1 - well_econ_data["param_data"]["royalty_rate"]))

        premium_vector = np.array([(0.9 ** (prod_year_num)) for prod_year_num in prod_year_nums])
        main_comm_prod_vector = [well_econ_data["{}_Prod_{}".format(main_comm_name.title(), prod_units[main_comm_name])][prod_year] for prod_year in prod_years]
        production_premium = np.dot(premium_vector, main_comm_prod_vector) * (1 - well_econ_data["param_data"]["royalty_rate"])
        if debug:
            print 'prod_years           : {}'.format(prod_years)
            print ''
            print 'capital_expenditure  : {}'.format(capital_expenditure)
            print 'workovers-recomp     : {}'.format(0)
            print 'abandonment_costs    : {}'.format(abandonment_costs)
            print 'discounted_opex      : {}'.format(discounted_opex)
            print 'discounted_oil       : {}'.format(discounted_oil)
            print 'discounted_gas       : {}'.format(discounted_gas)
            print 'discounted_cond      : {}'.format(discounted_cond)
            print 'discounted_ngls      : {}'.format(discounted_ngls)
            print 'discounted_revenue   : {}'.format(discounted_revenue)
            print 'discounted_costs     : {}'.format((capital_expenditure + abandonment_costs + discounted_opex) - discounted_revenue)
            print 'gross_prod_prem      : {}'.format(np.dot(premium_vector, main_comm_prod_vector))
            print 'production_premium   : {}'.format(production_premium)
            print 'pre-tax breakeven    : {}'.format(round(float((capital_expenditure + abandonment_costs + discounted_opex) - discounted_revenue) / float(production_premium), 2))
            print ''
            print 'discount_vector      : {}'.format(discount_vector)
            print 'total_opex_vector    : {}'.format(total_opex_vector)
            print 'premium_vector       : {}'.format(premium_vector)
            print 'main_comm_prod_vector: {}'.format(main_comm_prod_vector)
            print 'royalty_rate         : {}'.format(well_econ_data["param_data"]["royalty_rate"])
        try:
            pre_tax_be[main_comm_name] = round(float((capital_expenditure + abandonment_costs + discounted_opex) - discounted_revenue) / float(production_premium), 2)
        except:
            pre_tax_be[main_comm_name] = 0

        pre_tax_BE_oil_usd_bbl = pre_tax_be["OIL"]
        pre_tax_BE_gas_usd_mcf = pre_tax_be["GAS"]

        return pre_tax_BE_oil_usd_bbl, pre_tax_BE_gas_usd_mcf


    # Used as support functions for post-tax breakeven process ----------------------------------------------------------------------------------------------------------------------------------------------------------
    def calc_post_tax_npv(self):
        post_tax_NPV = 0
        disc_post_tax_cash_flows = []

        prod_years = sorted(self.annual_prod_data["TOTAL"].keys())
        development_year = prod_years[0] - 1
        prod_years = [development_year] + prod_years
        prod_years = [prod_year for prod_year in prod_years if prod_year <= self.last_econ_year]

        self.oil_price = self.comm_price_data["Crude Oil"]
        self.gas_price = self.comm_price_data["Natural Gas"]
        self.cond_price = self.comm_price_data["Condensate"]
        self.ngls_price = self.comm_price_data["NGLs"]

        royalty_rate = self.get_royalty_rate()

        econ_year = 0
        for prod_year in prod_years:
            self.tax_year = prod_year
            self.prod_year_num = prod_year - development_year
            if self.prod_year_num:
                self.oil_prod = self.annual_prod_data["OIL"][prod_year]
                self.gas_prod = self.annual_prod_data["GAS"][prod_year]
                self.cond_prod = self.annual_prod_data["CONDENSATE"][prod_year]
                self.ngls_prod = self.annual_prod_data["NGL"][prod_year]
                self.water_prod = self.annual_prod_data["WATER"][prod_year]
                self.total_prod = self.annual_prod_data["TOTAL"][prod_year]
            else:
                self.oil_prod = 0
                self.gas_prod = 0
                self.cond_prod = 0
                self.ngls_prod = 0
                self.water_prod = 0
                self.total_prod = 0
            if (self.total_prod or not self.prod_year_num):
                oil_revenue = (self.oil_prod * self.oil_price)
                gas_revenue = (self.gas_prod * self.gas_price)
                cond_revenue = (self.cond_prod * self.cond_price)
                ngls_revenue = (self.ngls_prod * self.ngls_price)
                gross_revenue = round(float((self.oil_prod * self.oil_price) + (self.gas_prod * self.gas_price) + (self.cond_prod * self.cond_price) + (self.ngls_prod * self.ngls_price)), 2)
                net_revenue = round(float(gross_revenue * (1 - royalty_rate)), 2)
                prod_tax_value = self.get_production_tax()
                depreciation = self.get_depreciation()

                #Added inflation factors for single-well forecasts
                capex_inflation  = self.get_inflation_factor(prod_year, 'capex')
                capex_tangible   = self.get_capex_tangible() * capex_inflation
                capex_intangible = self.get_capex_intangible() * capex_inflation
                capex            = round(float(capex_tangible + capex_intangible), 2)

                opex_inflation   = self.get_inflation_factor(prod_year, 'opex')
                variable_opex    = self.get_variable_opex() * opex_inflation
                fixed_opex       = self.get_fixed_opex() * opex_inflation
                opex             = round(float(variable_opex + fixed_opex), 2)

                self.net_income = round(float(net_revenue - (prod_tax_value + capex + opex + depreciation)), 2)
                self.state_tax_rate = self.cost_inputs[self.forecast_type]["state_tax_rate"]
                self.state_tax_value = self.get_state_tax_value()
                federal_tax_value = self.get_federal_tax_value()

                post_tax_cf = round(float(net_revenue - (capex + opex + prod_tax_value + self.state_tax_value + federal_tax_value)), 2)
                disc_post_tax_cf = round(float(post_tax_cf / float(1.1 ** (self.prod_year_num))), 2)

                econ_year = prod_year
                #disc_post_tax_cash_flows.append(disc_post_tax_cf)
                post_tax_NPV += disc_post_tax_cf

        econ_year += 1
        self.prod_year_num = econ_year - development_year
        self.tax_year = econ_year
        abandonment = self.get_abandonment()
        post_tax_cf = round(float(-abandonment), 2)
        disc_post_tax_cf = round(float(post_tax_cf / float(1.1 ** (self.prod_year_num))), 2)
        #disc_post_tax_cash_flows.append(disc_post_tax_cf)
        post_tax_NPV += disc_post_tax_cf
        return post_tax_NPV

    def get_outcome_sign(self, outcome):
        sign = 1
        if abs(outcome - self.GOAL) < self.ZERO_range:
            sign = 0
        elif outcome < self.GOAL:
            sign = -1
        return sign

    def check_plus_minus(self, guess):
        check_val = False
        guess_plus = self.check_guess(guess + self.INCR_MIN)
        guess_minus = self.check_guess(guess - self.INCR_MIN)
        if self.get_outcome_sign(guess_plus) == -self.get_outcome_sign(guess_minus):
            check_val = True
        return check_val

    def check_guess(self, guess):
        print 'guess: {}'.format(guess)
        outcome = self.OUT_DEFAULT
        self.comm_price_data = self.COMM_PRICE_DEFAULTS.copy()
        print 'main_comm: {}'.format(self.main_com)
        if self.MAIN_COMM_NAME[self.main_comm] == "OIL":
            self.comm_price_data["Crude Oil"] = guess
            self.comm_price_data["Condensate"] = guess
        else:
            self.comm_price_data["Natural Gas"] = guess
        outcome = self.calc_post_tax_npv()
        print 'outcome: {}'.format(outcome)
        try:
            ret_val = float(outcome)
        except:
            ret_val = self.OUT_DEFAULT
        return ret_val

    def goal_seek(self):
        increment = self.INCR_MIN
        goal_reached = False
        breakeven_val = self.OUT_DEFAULT
        last_outcome = 0
        iter_count = 1
        while not goal_reached:
            print 'iter_count: {}'.format(iter_count)
            if iter_count == 1:
                last_outcome = self.check_guess(self.INIT_GUESS)
                outcome = self.check_guess(self.INIT_GUESS + self.INIT_INCR)
                last_guess = self.INIT_GUESS
                last_increment = self.INIT_INCR
                print 'last_outcome: {}'.format(last_outcome)
                print 'outcome: {}'.format(outcome)
                try:
                    increment = float(last_increment * outcome) / float(last_outcome - outcome)
                except:
                    iter_count = self.ITER_MAX
                guess = last_guess + increment
            outcome = self.check_guess(guess)
            sign = self.get_outcome_sign(outcome)
            if self.check_plus_minus(guess):
                breakeven_val = guess
                print '(1) breakeven_val: {}'.format(breakeven_val)
                goal_reached = True
            if sign == 0:
                breakeven_val = guess
                print '(2) breakeven_val: {}'.format(breakeven_val)
                goal_reached = True
            elif iter_count >= self.ITER_MAX:
                breakeven_val = self.OUT_DEFAULT
                print '(3) breakeven_val: {}'.format(breakeven_val)
                goal_reached = True
            else:
                last_guess = guess
                last_increment = increment
                try:
                    increment = float(last_increment * outcome) / float(last_outcome - outcome)
                except:
                    print '***!!!***'
                    iter_count = self.ITER_MAX
                last_outcome = outcome
                guess = last_guess + increment
                iter_count += 1
                print 'last_outcome: {}'.format(last_outcome)
                print 'guess: {}'.format(guess)
                print 'increment: {}'.format(increment)
                print 'iter_count: {}'.format(iter_count)
        return breakeven_val


    # Main function to calculate post-tax breakeven values ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    def calc_post_tax_breakeven(self):
        post_tax_be = {"OIL": 0.0, "GAS": 0.0}
        post_tax_be[self.MAIN_COMM_NAME[self.main_comm]] = self.goal_seek()
        post_tax_BE_oil_usd_bbl = round(float(post_tax_be["OIL"]), 2)
        post_tax_BE_gas_usd_mcf = round(float(post_tax_be["GAS"]), 2)
        return post_tax_BE_oil_usd_bbl, post_tax_BE_gas_usd_mcf


    # All functions to calculate irr values -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def irr_check_guess(self, guess):
        outcome = self.IRR_OUT_DEFAULT
        cash_flow_vector = np.array(self.cash_flows)
        try:
            irr_guess_vector = np.array([1.0 / (1 + guess) ** (prod_year_num) for prod_year_num in range(len(self.cash_flows))])
            outcome = np.dot(cash_flow_vector, irr_guess_vector)
            ret_val = float(outcome)
        except:
            ret_val = self.IRR_OUT_DEFAULT
        return ret_val

    def irr_get_outcome_sign(self, outcome):
        sign = 1
        if abs(outcome - self.GOAL) < self.IRR_ZERO_range:
            sign = 0
        elif outcome < self.GOAL:
            sign = -1
        return sign

    def irr_check_plus_minus(self, guess):
        check_val = False
        guess_plus = self.irr_check_guess(guess + self.IRR_INCR_MIN)
        guess_minus = self.irr_check_guess(guess - self.IRR_INCR_MIN)
        if self.irr_get_outcome_sign(guess_plus) == -self.irr_get_outcome_sign(guess_minus):
            check_val = True
        return check_val

    def irr_goal_seek(self):
        increment = self.IRR_INCR_MIN
        goal_reached = False
        breakeven_val = self.IRR_OUT_DEFAULT
        last_outcome = 0
        iter_count = 1
        while not goal_reached:
            if iter_count == 1:
                last_outcome = self.irr_check_guess(self.IRR_INIT_GUESS)
                outcome = self.irr_check_guess(self.IRR_INIT_GUESS + self.IRR_INIT_INCR)
                last_guess = self.IRR_INIT_GUESS
                last_increment = self.IRR_INIT_INCR
                try:
                    increment = float(last_increment * outcome) / float(last_outcome - outcome)
                    increment = min(max(-self.IRR_INCR_MAX, increment), self.IRR_INCR_MAX)
                except:
                    iter_count = self.IRR_ITER_MAX
                guess = last_guess + increment
            outcome = self.irr_check_guess(guess)
            sign = self.irr_get_outcome_sign(outcome)
            if self.irr_check_plus_minus(guess):
                breakeven_val = guess
                goal_reached = True
            if sign == 0:
                breakeven_val = guess
                goal_reached = True
            elif iter_count >= self.IRR_ITER_MAX:
                breakeven_val = self.IRR_OUT_DEFAULT
                goal_reached = True
            else:
                last_guess = guess
                last_increment = increment
                try:
                    increment = float(last_increment * outcome) / float(last_outcome - outcome)
                    increment = min(max(-self.IRR_INCR_MAX, increment), self.IRR_INCR_MAX)
                except:
                    iter_count = self.IRR_ITER_MAX
                last_outcome = outcome
                guess = last_guess + increment
                iter_count += 1
        return breakeven_val

    def calc_irr(self):
        self.cash_flows = self.disc_pre_tax_cashflows
        #self.disc_pre_tax_cashflows = []
        print '1 - self.cash_flows: {}'.format(self.cash_flows)
        pre_tax_irr     = round(float(self.irr_goal_seek()), 3)

        self.cash_flows = self.disc_post_tax_cashflows
        #self.disc_post_tax_cashflows = []
        print '2 - self.cash_flows: {}'.format(self.cash_flows)
        post_tax_irr    = round(float(self.irr_goal_seek()), 3)
        return pre_tax_irr, post_tax_irr


    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def on_get(self, Profile_ID, forecast_type='type-well'):
        self.init_econ_variables(Profile_ID, forecast_type)
        conn = get_connection(server='sql_server', database='US_Wells')
        cursor = conn.cursor()
        try:
            print("Profile_ID:" ,self.well_api)
            data_comms =[]
            #ProfileID = str(self.well_api)

            self.cost_inputs = self.get_cost_inputs()

            # Get the Type Well Forecast Production Data
            cursor.execute("SELECT DISTINCT UPPER(MainType) AS MainType FROM US_Wells.dbo.tblSave_ForecastTypeWellData WITH(NOLOCK) WHERE profile_id='{}' AND GroupType= 'production' ".format(Profile_ID))
            commodities = [data[0] for data in cursor.fetchall()]

            production_data = {prod_comm: {} for prod_comm in commodities}
            for commodity in commodities:
                cursor.execute("SELECT Year_num, production FROM US_Wells.dbo.tblSave_ForecastTypeWellData WITH(NOLOCK) WHERE profile_id='{}' AND  MainType = '{}' AND GroupType= 'production' ORDER BY Year_num ".format(Profile_ID, commodity))
                prod_data = cursor.fetchall()
                # *** Added condition below to run wells with production years (2006, 2007, etc) as type-wells --- Jason 20190827
                year_num = 1
                for datarow in prod_data:
                    for period, value in [datarow]:
                        if self.forecast_type == 'type-well':
                            production_data[commodity][year_num] = value
                            year_num += 1
                        else:
                            production_data[commodity][period] = value

            # Convert monthly production forecast to annual forecast
            self.well_forecast_data = production_data
            self.calculate_annual_production()

            # Calculate time-series economics data
            well_econ_data = self.calc_well_economics()

            # Get the EUR values by Commodity
            well_econ_data = self.get_eur_totals(well_econ_data)

            # Calculate Pre-tax and Post-tax breakevens
            pre_tax_BE_oil_usd_bbl, pre_tax_BE_gas_usd_mcf   = self.calc_pre_tax_breakeven(well_econ_data, debug=True)
            post_tax_BE_oil_usd_bbl, post_tax_BE_gas_usd_mcf = self.calc_post_tax_breakeven()

            # Calculate IRR percentages
            pre_tax_irr_pct, post_tax_irr_pct                = self.calc_irr()

            # Store calculated values in well_econ_data dictionary
            well_econ_data["pre_tax_BE_oil_usd_bbl"]  = pre_tax_BE_oil_usd_bbl
            well_econ_data["pre_tax_BE_gas_usd_mcf"]  = pre_tax_BE_gas_usd_mcf
            well_econ_data["post_tax_BE_oil_usd_bbl"] = post_tax_BE_oil_usd_bbl
            well_econ_data["post_tax_BE_gas_usd_mcf"] = post_tax_BE_gas_usd_mcf
            well_econ_data["pre_tax_irr_pct"]         = pre_tax_irr_pct
            well_econ_data["post_tax_irr_pct"]        = post_tax_irr_pct

            for summary_param in ['total_opex_mm_usd', 'total_well_cost_mm_usd', 'cost_capex_drilling_mm_usd', 'cost_capex_completion_mm_usd', 'cost_capex_facilities_mm_usd']:
                well_econ_data[summary_param] = round(float(well_econ_data[summary_param])/1000000.0, 2)

            # Format output data
            jsonRows = [
                # Engine outputs summary data to US_Wells.dbo.tblUSWell_Parameters
                {'summary data': {summary_param: well_econ_data[summary_param] for summary_param in self.econ_summary_params}},

                # Engine outputs annual data to US_Wells.dbo.tblUSWell_Economics_Forecast
                {'annual data': []}
            ]
            print '\t'.join(self.econ_annual_params)
            well_econ_data["prod_years"].append(max(well_econ_data["prod_years"]) + 1)
            for i in range(len(well_econ_data["prod_years"])):
                prod_year = well_econ_data["prod_years"][i]
                jsonRows[1]['annual data'].append({annual_param: 0 for annual_param in self.econ_annual_params})
                jsonRows[1]['annual data'][i]['year'] = prod_year
                output_row = '{}\t'.format(prod_year)
                for annual_param in [param for param in self.econ_annual_params if param != 'year']:
                    jsonRows[1]['annual data'][i][annual_param] = well_econ_data[annual_param][prod_year]
                    output_row += '{}\t'.format(well_econ_data[annual_param][prod_year],)
                print output_row
            #print json.dumps(jsonRows, ensure_ascii=False)
            print '\n'
            for summary_param in self.econ_summary_params:
                print '{}\t{}'.format(summary_param, jsonRows[0]['summary data'][summary_param])

        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print("Unexpected error:", sys.exc_info()[2])
        finally:
            try:
                curr.close()
                conn.close()
            except:
                pass

if __name__=='__main__':
    well_econ_engine = WellEconomics()
    well_econ_engine.on_get('3308', 'single-well')
