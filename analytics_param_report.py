from globaldata import *
from openpyxl import Workbook
from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.styles import colors
from openpyxl.cell import Cell


class AnalyticsParameterReport:
    def __init__(self, run_id):
        # Initialize variables related to Excel report document
        self.run_id                  = run_id
        self.report_filename         = ANALYTICS_RPT % self.run_id
        self.regions                 = MAIN_REGIONS
        self.analytics_param_report  = self.gen_analytics_param_report()
        self.analytics_param_data    = self.analytics_param_report['Analytics Parameter Data']
        self.analytics_param_summary = self.analytics_param_report['Analytics Parameter Summary']

        # Initialize variables related to database
        self.conn      = get_connection()
        self.curr      = self.conn.cursor()
        self.econ_data = self.get_econ_data()

        # Initialize constants used to generate report
        self.parameter_col_data = {
            'A' : {'name':'ASSET_ID',            'min': None,   'max': None},
            'B' : {'name':'ASSET_NAME',          'min': None,   'max': None},
            'C' : {'name':'COUNTRY',             'min': None,   'max': None},
            'D' : {'name':'CONSTITUENT',         'min': None,   'max': None},
            'E' : {'name':'REGION',              'min': None,   'max': None},
            'F' : {'name':'FORMATION',           'min': None,   'max': None},
            'G' : {'name':'POSITION',            'min': None,   'max': None},
            'H' : {'name':'FACILITY_TYPE',       'min': None,   'max': None},
            'I' : {'name':'TERRAIN',             'min': None,   'max': None},
            'J' : {'name':'BASIN',               'min': None,   'max': None},
            'K' : {'name':'STATUS',              'min': None,   'max': None},
            'L' : {'name':'OPERATOR',            'min': None,   'max': None},
            'M' : {'name':'PARENT_COMPANY',      'min': None,   'max': None},
            'N' : {'name':'RESOURCE_TYPE',       'min': None,   'max': None},
            'O' : {'name':'LIQUID_RECOV_TOT',    'min': None,   'max': None},
            'P' : {'name':'NATGAS_RECOV_TOT',    'min': None,   'max': None},
            'Q' : {'name':'NGLS_RECOV_TOT',      'min': None,   'max': None},
            'R' : {'name':'TOTAL_RECOV',         'min': None,   'max': None},
            'S' : {'name':'LIQUID_RECOV_REM',    'min': None,   'max': None},
            'T' : {'name':'NATGAS_RECOV_REM',    'min': None,   'max': None},
            'U' : {'name':'NGLS_RECOV_REM',      'min': None,   'max': None},
            'V' : {'name':'TOTAL_RECOV_REM',     'min': None,   'max': None},
            'W' : {'name':'IRR_FULL',            'min': 0,      'max': 80},
            'X' : {'name':'TOTAL_BOE',           'min': None,   'max': None},
            'Y' : {'name':'OPEX_REM',            'min': None,   'max': None},
            'Z' : {'name':'OPEX_FULL',           'min': None,   'max': None},
            'AA': {'name':'ABANDON_REM',         'min': None,   'max': None},
            'AB': {'name':'ABANDON_FULL',        'min': None,   'max': None},
            'AC': {'name':'CAPEX_OPEX_BOE_REM',  'min': None,   'max': None},
            'AD': {'name':'CAPEX_BOE_REM',       'min': 5,      'max': 40},
            'AE': {'name':'CAPEX_BOE_FULL',      'min': 5,      'max': 40},
            'AF': {'name':'OPEX_BOE_REM',        'min': 10,     'max': 40},
            'AG': {'name':'OPEX_BOE_FULL',       'min': 10,     'max': 40},
            'AH': {'name':'FISCAL_TAKE',         'min': 0,      'max': None},
            'AI': {'name':'FISCAL_FULL',         'min': 0,      'max': 200},
            'AJ': {'name':'FISCAL_REM',          'min': 0,      'max': 200},
            'AK': {'name':'NPV_REM',             'min': 100000, 'max': None},
            'AL': {'name':'NPV_DEV',             'min': 1000,   'max': None},
            'AM': {'name':'NPV_REM_PER_BOE',     'min': 1,      'max': None},
            'AN': {'name':'NPV_DEV_PER_BOE',     'min': 1,      'max': None},
            'AO': {'name':'BE_GAS_REM',          'min': 0,      'max': 50},
            'AP': {'name':'BE_OIL_REM',          'min': 0,      'max': 250},
            'AQ': {'name':'BE_GAS_DEV',          'min': 0,      'max': 50},
            'AR': {'name':'BE_OIL_DEV',          'min': 0,      'max': 250},
            'AS': {'name':'CAPEX_REM',           'min': None,   'max': None},
            'AT': {'name':'CAPEX_FULL',          'min': None,   'max': None},
            'AU': {'name':'FIRST_PRODUCTION',    'min': None,   'max': None},
            'AV': {'name':'PEAK_YEAR',           'min': None,   'max': None},
            'AW': {'name':'PEAK_PROD',           'min': None,   'max': None},
            'AX': {'name':'PEAK_PROD_UNIT',      'min': None,   'max': None},
            'AY': {'name':'CUTOFF_YEAR',         'min': None,   'max': None},
            'AZ': {'name':'IRR_DEV',             'min': 0,      'max': 80},
            'BA': {'name':'EUR_TOTAL',           'min': None,   'max': None},
            'BB': {'name':'POST_TAX_IRR',        'min': None,   'max': None},
            'BC': {'name':'BE_OIL_POST_TAX',     'min': None,   'max': None},
            'BD': {'name':'BE_GAS_POST_TAX',     'min': None,   'max': None},
            'BE': {'name':'CAPEX_WELL',          'min': None,   'max': None},
            'BF': {'name':'OPEX_WELL',           'min': None,   'max': None},
            'BG': {'name':'WELL_BOE',            'min': None,   'max': None},
            'BH': {'name':'CAPEX_WELL_BOE',      'min': None,   'max': None},
            'BI': {'name':'OPEX_WELL_BOE',       'min': None,   'max': None},
            'BJ': {'name':'IP30_RATE',           'min': None,   'max': None},
            'BK': {'name':'RIG_COUNT',           'min': None,   'max': None},
            'BL': {'name':'LAST_RIG_YEAR',       'min': None,   'max': None},
            'BM': {'name':'WELL_LIFE',           'min': None,   'max': None},
            'BN': {'name':'NEW_WELLS',           'min': None,   'max': None},
            'BO': {'name':'NEW_WELLS_REM',       'min': None,   'max': None},
            'BP': {'name':'DRILL_COMP_DAYS',     'min': None,   'max': None},
            'BQ': {'name':'CRUDE_BM',            'min': None,   'max': None},
            'BR': {'name':'NG_BM',               'min': None,   'max': None},
            'BS': {'name':'CONDENSATE_BM',       'min': None,   'max': None},
            'BT': {'name':'LNG_BM',              'min': None,   'max': None},
            'BU': {'name':'NGLS_BM',             'min': None,   'max': None},
            'BV': {'name':'FISCAL_MODEL',        'min': None,   'max': None}
        }
        self.region_outliers   = {REGIONS[region_name]: 0 for region_name in self.regions}

    def gen_analytics_param_report(self):
        '''Copies report template to :/GlobalData/Reports/ with run_id in new filename then opens file'''
        shutil.copy2(ANALYTICS_TMP, self.report_filename)
        return openpyxl.load_workbook(self.report_filename)

    def format_cell(self, cell):
        thin_side = openpyxl.styles.borders.Side(style='thin')
        cell_borders = openpyxl.styles.borders.Border(left=thin_side, right=thin_side)
        cell.border = cell_borders

    def highlight_cell(self, cell):
        cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

    def get_econ_data(self):
        '''Retrieves all data from last engine run stored in econ_data table'''
        sql_select = \
            '''
            SELECT asset_id, asset_name, country, constituent, region, formation, position, facility_type, terrain, basin, status, operator, parent_company, resource_type, liquid_recov_tot, natgas_recov_tot, ngls_recov_tot, total_recov, 
                   liquid_recov_rem, natgas_recov_rem, ngls_recov_rem, total_recov_rem, (irr_full*100), total_boe, opex_rem, opex_full, abandon_rem, abandon_full, capex_opex_boe_rem, capex_boe_rem, capex_boe_full, opex_boe_rem, opex_boe_full, 
                   fiscal_take, (fiscal_full*100), (fiscal_rem*100), npv_rem, npv_dev, npv_rem_per_boe, npv_dev_per_boe, be_gas_rem, be_oil_rem, be_gas_dev, be_oil_dev, capex_rem, capex_full, first_production, peak_year, 
                   peak_prod, peak_prod_unit, cutoff_year, (irr_dev*100), eur_total, (post_tax_irr*100), be_oil_post_tax, be_gas_post_tax, capex_well, opex_well, well_boe, capex_well_boe, opex_well_boe, ip30_rate, rig_count, last_rig_year, 
                   well_life, new_wells, new_wells_rem, drill_comp_days, crude_bm, ng_bm, condensate_bm, lng_bm, ngls_bm, fiscal_model 
            FROM econ_data WHERE run_id="{}" AND NOT fiscal_model IS NULL
            ORDER BY region, asset_id
            '''
        self.curr.execute(sql_select.format(self.run_id))
        return self.curr.fetchall()

    def enter_econ_data(self):
        asset_row = 2

        for param_vals in self.econ_data:
            is_outlier = False
            asset_region = param_vals[4]
            param_cols = XL_COLS[:len(param_vals)]
            for j in range(len(param_cols)):
                param_col = param_cols[j]
                param_val = param_vals[j]
                asset_id_cell   = self.analytics_param_data['A' + str(asset_row)]
                asset_name_cell = self.analytics_param_data['B' + str(asset_row)]
                param_data_cell = self.analytics_param_data[param_col + str(asset_row)]
                param_data_cell.value = param_val
                # Check for outliers
                col_data   = self.parameter_col_data[param_col]
                param_min  = col_data['min']
                param_max  = col_data['max']
                if not (param_min is None and param_max is None):
                    outside_param_range = False
                    if param_min is not None and param_val < param_min:
                        outside_param_range = True
                    if param_max is not None and param_val > param_max:
                        outside_param_range = True
                    # If outside acceptable range of values then highlight and add to outlier count for country
                    if outside_param_range:
                        self.highlight_cell(param_data_cell)
                        self.highlight_cell(asset_id_cell)
                        self.highlight_cell(asset_name_cell)
                        is_outlier = True
                self.format_cell(param_data_cell)
            if is_outlier:
                self.region_outliers[asset_region] += 1
            asset_row += 1

    def enter_region_summary_data(self):
        sql_select = '''SELECT region, COUNT(asset_id) FROM assets WHERE data_source="Engine" AND asset_relation="Parent" AND status IN ("Planned", "Announced", "Producing", "Abandoned", "Stalled") GROUP BY region ORDER BY region'''
        self.curr.execute(sql_select)
        row_num = 4
        for region, region_eligible in self.curr.fetchall():
            self.analytics_param_summary['A' + str(row_num)].value = region
            self.analytics_param_summary['B' + str(row_num)].value = region_eligible
            self.analytics_param_summary['C' + str(row_num)].value = self.region_outliers[region]
            row_num += 1

    def generate_report(self):
        self.enter_econ_data()
        self.enter_region_summary_data()
        self.analytics_param_report.save(self.report_filename)

def main(run_id=''):
    if not run_id:
        run_id = get_run_id()
    analytics = AnalyticsParameterReport(run_id)
    analytics.generate_report()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    run_ids = ('20190213_154221', '20190220_155151', '20190306_195034')
    for run_id in run_ids:
        main(run_id)

