from globaldata import *


class EconErrorReport:
    def __init__(self):
        # Initialize variables related to Excel report document
        self.run_id             = get_run_id()
        self.report_filename    = ECON_ERR_RPT % self.run_id
        self.econ_error_report  = self.gen_econ_error_report()
        self.econ_error_log     = self.econ_error_report['Economics Error Log']
        self.econ_error_summary = self.econ_error_report['ECO Error Log Summary']
        self.abandoned_errors   = self.econ_error_report['Abandoned Errors']
        self.abandoned_summary  = self.econ_error_report['Abandoned Error Summary']
        self.fiscal_errors      = self.econ_error_report['Fiscal Errors']

        # Initialize variables related to database
        self.conn               = get_connection()
        self.curr               = self.conn.cursor()
        self.econ_data          = self.get_econ_data()

        # Initialize constants used to generate report
        self.IRR_DEV_MIN        = 0.0
        self.IRR_DEV_MAX        = 0.8
        self.CAPEX_BOE_MIN      = 5
        self.CAPEX_BOE_MAX      = 40
        self.OPEX_BOE_MIN       = 10
        self.OPEX_BOE_MAX       = 40
        self.ERROR_FLAG         = 'ERROR TYPE %s'
        self.ERROR_MESSAGE      = '%s IS %s %s WITH A VALUE OF %s'

        # Initialize variables for particular assets
        self.error_num          = None
        self.error_type         = None
        self.error_value        = None
        self.error_flag         = None
        self.error_message      = None
        self.error_param        = None
        self.error_sheet        = None
        #
        self.param_value        = None
        self.min_value          = None
        self.max_value          = None
        #
        self.asset_id           = None
        self.asset_name         = None
        self.country            = None
        self.constituent        = None
        self.terrain            = None
        self.region             = None
        self.status             = None
        self.irr_dev            = None
        self.total_boe          = None
        self.capex_boe_full     = None
        self.opex_boe_full      = None
        self.fiscal_full        = None
        self.fiscal_rem         = None
        #
        self.econ_err_count     = None
        self.abandon_err_count  = None
        #
        self.error_data         = None

    def gen_econ_error_report(self):
        '''Copies report template to :/GlobalData/Reports/ with run_id in new filename then opens file'''
        shutil.copy2(ECON_ERR_TMP, self.report_filename)
        return openpyxl.load_workbook(self.report_filename)

    def get_econ_data(self):
        '''Retrieves all data from last engine run stored in econ_data table'''
        sql_select  = 'SELECT asset_id, asset_name, country, constituent, region, status, terrain, '
        sql_select += 'irr_dev, total_boe, capex_boe_full, opex_boe_full, fiscal_full, fiscal_rem '
        sql_select += 'FROM econ_data WHERE NOT asset_name IS NULL AND session_key LIKE "%%%s%%" '
        sql_select += 'ORDER BY asset_id'
        print sql_select % self.run_id
        self.curr.execute(sql_select % self.run_id)
        return self.curr.fetchall()

    def get_error_data(self):
        err_data = {
                  'IRR': {'val': self.irr_dev,
                          'err': '14',
                          'min': self.IRR_DEV_MIN,
                          'max': self.IRR_DEV_MAX},

        'CAPEX PER BOE': {'val': self.capex_boe_full,
                          'err': '15',
                          'min': self.CAPEX_BOE_MIN,
                          'max': self.CAPEX_BOE_MAX},

         'OPEX PER BOE': {'val': self.opex_boe_full,
                          'err': '16',
                          'min': self.OPEX_BOE_MIN,
                          'max': self.OPEX_BOE_MAX},
        }
        return err_data

    def update_domain_data(self):
        sql_update  = 'UPDATE econ_error_log AS e, analyst_domains AS d SET e.domain=d.domain WHERE e.country=d.country '
        sql_update += 'AND (e.constituent=d.constituent OR (d.constituent="" AND d.terrain="")) '
        sql_update += 'AND (e.terrain=d.terrain OR d.terrain="")'
        self.curr.execute(sql_update)
        self.curr.execute('COMMIT')

    def enter_econ_data(self):
        self.econ_err_count    = 0
        self.abandon_err_count = 0

        for i in range(len(self.econ_data)):
            datarow = self.econ_data[i]
            self.asset_id, self.asset_name, self.country, self.constituent, self.region, self.status, self.terrain    = datarow[:7]
            self.irr_dev, self.total_boe, self.capex_boe_full, self.opex_boe_full, self.fiscal_full, self.fiscal_rem = datarow[7:]
            if self.irr_dev:
                self.irr_dev = round_value(self.irr_dev)
            else:
                self.irr_dev = 0
            self.total_boe = round_value(self.total_boe)
            self.capex_boe_full = round_value(self.capex_boe_full)
            self.opex_boe_full = round_value(self.opex_boe_full)

            fiscal_row = str(i + 4)
            self.enter_fiscal_take(fiscal_row)
            
            self.find_econ_errors()

    def enter_fiscal_take(self, fiscal_row):
        fiscal_data = (self.asset_id, self.asset_name, self.country, self.constituent, self.region, self.status, self.fiscal_full, self.fiscal_rem)
        fiscal_cols = 'ABCDEFGH'
        for j in range(len(fiscal_cols)):
            fiscal_col = fiscal_cols[j]
            fiscal_val = fiscal_data[j]
            self.fiscal_errors[fiscal_col + fiscal_row].value = fiscal_val

    def find_econ_errors(self):
        for err_param in ['IRR', 'CAPEX PER BOE', 'OPEX PER BOE']:
            self.error_param = err_param
            self.error_data  = self.get_error_data()
            self.param_value = self.error_data[self.error_param]['val']
            self.error_num   = self.error_data[self.error_param]['err']
            self.min_value   = self.error_data[self.error_param]['min']
            self.max_value   = self.error_data[self.error_param]['max']
            self.error_type  = 'BELOW'

            try:
                self.param_value = float(self.param_value)
            except:
                self.check_econ_error()
            else:
                if self.param_value < self.min_value:
                    self.check_econ_error()
                elif self.param_value > self.max_value:
                    self.error_type = 'ABOVE'
                    self.check_econ_error()
                else:
                    pass

    def check_econ_error(self):
        if self.error_type == 'BELOW':
            self.error_value = self.min_value
        else:
            self.error_value = self.max_value


        self.error_flag = self.ERROR_FLAG % self.error_num
        self.error_message = self.ERROR_MESSAGE % (self.error_param, self.error_type, self.error_value, self.param_value)

        sql_select = 'SELECT COUNT(*) FROM econ_error_exceptions WHERE asset_id=%s AND error_message LIKE "%s%%" AND error_flag="%s"'
        self.curr.execute(sql_select % (self.asset_id, self.error_message[:-1], self.error_flag))

        is_exception = self.curr.fetchone()[0]

        if not is_exception:
            self.enter_econ_error()
        else:
            pass
            
    def enter_econ_error(self):
        if self.status == "Abandoned":
            self.abandon_err_count += 1
            self.error_sheet = self.abandoned_errors
            error_row = str(self.abandon_err_count + 3)
        else:
            self.econ_err_count += 1
            self.error_sheet = self.econ_error_log
            error_row = str(self.econ_err_count + 3)

        param_vals  = (self.asset_id, self.asset_name, self.country, self.constituent, self.region, self.status, self.error_flag)
        param_vals += (self.error_message, self.irr_dev, self.total_boe, self.capex_boe_full, self.opex_boe_full)

        error_cols = 'ABCDEFGHIJKL'
        for j in range(len(error_cols)):
            error_col = error_cols[j]
            param_val = param_vals[j]
            self.error_sheet[error_col + error_row].value = param_val

        param_vals += (self.terrain, self.run_id)
        sql_insert  = 'INSERT INTO econ_error_log (asset_id, asset_name, country, constituent, region, status, error_flag, error_message, irr_dev, '
        sql_insert += 'total_boe, capex_boe_full, opex_boe_full, terrain, run_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.curr.execute(sql_insert, param_vals)
        self.curr.execute('COMMIT')

    def enter_flag_summary_data(self, summary_sheet):
        summary_sheet['A3'].value = 'Row Labels'
        summary_sheet['B3'].value = 'Count of Flag Number'
        summary_sheet['A7'].value = 'Grand Total'

        sql_status = ''
        if summary_sheet == self.econ_error_summary:
            sql_status = 'NOT '

        sql_select  = 'SELECT error_flag, COUNT(*) FROM econ_error_log WHERE run_id="%s" AND %sstatus="Abandoned" GROUP BY error_flag ORDER BY error_flag'

        self.curr.execute(sql_select % (self.run_id, sql_status))
        flag_summary_data = self.curr.fetchall()

        err_total = 0
        row_num = 4
        for err_flg, err_count in flag_summary_data:
            summary_sheet['A' + str(row_num)].value = err_flg
            summary_sheet['B' + str(row_num)].value = int(err_count)
            err_total += int(err_count)
            row_num += 1
        summary_sheet['B7'].value = err_total

    def enter_country_summary_data(self, summary_sheet):
        summary_sheet['A20'].value = 'Row Labels'
        summary_sheet['A21'].value = 'ERROR TYPE 14'
        summary_sheet['A22'].value = 'ERROR TYPE 15'
        summary_sheet['A23'].value = 'ERROR TYPE 16'
        summary_sheet['A24'].value = 'Grand Total'
        sql_status = ''
        if summary_sheet == self.econ_error_summary:
            sql_status = 'NOT '
        self.curr.execute('SELECT DISTINCT country FROM econ_error_log WHERE run_id="%s" AND %sstatus="Abandoned" ORDER BY country' % (self.run_id, sql_status))
        err_countries = [err_country[0] for err_country in self.curr.fetchall()]
        sql_select = 'SELECT COUNT(*) FROM econ_error_log WHERE run_id="%s" AND error_flag="%s" AND country="%s" AND %sstatus="Abandoned"'
        col_num = 2
        for err_country in err_countries:
            col_name = XL_COLS[col_num]
            summary_sheet[col_name + '20'].value = err_country
            country_total = 0
            row_num = 21
            for err_flag in ['ERROR TYPE 14', 'ERROR TYPE 15', 'ERROR TYPE 16']:
                self.curr.execute(sql_select % (self.run_id, err_flag, err_country, sql_status))
                error_count = self.curr.fetchone()[0]
                summary_sheet[col_name + str(row_num)].value = error_count
                country_total += error_count
                row_num += 1
            summary_sheet[col_name + '24'].value = country_total
            col_num += 1

    def enter_region_summary_data(self, summary_sheet):
        if summary_sheet == self.econ_error_summary:
            sql_status = 'status IN ("Planned", "Announced", "Producing")'
        elif summary_sheet == self.abandoned_summary:
            sql_status = 'status="Abandoned"'
        sql_select = \
        '''
        SELECT a.region,
               (SELECT COUNT(asset_id) AS region_eligible FROM assets WHERE data_source="Engine" AND asset_relation="Parent" AND region=a.region AND %s) AS region_eligible,
               (SELECT COUNT(DISTINCT asset_id) AS region_error FROM econ_error_log WHERE run_id="%s" AND region=a.region AND %s) AS region_error
        FROM assets AS a
        GROUP BY a.region ORDER BY a.region
        '''
        self.curr.execute(sql_select % (sql_status, self.run_id, sql_status))
        row_num = 5
        for region, region_eligible, region_error in self.curr.fetchall():
            summary_sheet['H' + str(row_num)].value = region
            summary_sheet['I' + str(row_num)].value = region_eligible
            summary_sheet['J' + str(row_num)].value = region_error
            row_num += 1

    def enter_asset_summary_data(self, summary_sheet):
        if summary_sheet == self.econ_error_summary:
            sql_status = 'status IN ("Planned", "Announced", "Producing")'
        elif summary_sheet == self.abandoned_summary:
            sql_status = 'status="Abandoned"'

        sql_eligible = 'SELECT COUNT(asset_id) FROM assets WHERE data_source="Engine" AND asset_relation="Parent" AND %s' % sql_status
        self.curr.execute(sql_eligible)
        eligible_count = self.curr.fetchone()[0]
        summary_sheet['F4'].value = eligible_count

        sql_error = 'SELECT COUNT(DISTINCT asset_id) FROM econ_error_log WHERE run_id="%s" AND %s' % (self.run_id, sql_status)
        self.curr.execute(sql_error)
        error_count = self.curr.fetchone()[0]
        summary_sheet['F5'].value = error_count

    def enter_summary_data(self):
        for summary_sheet in [self.econ_error_summary, self.abandoned_summary]:
            self.enter_flag_summary_data(summary_sheet)
            self.enter_country_summary_data(summary_sheet)
            self.enter_region_summary_data(summary_sheet)
            self.enter_asset_summary_data(summary_sheet)


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    econ_report = EconErrorReport()
    econ_report.enter_econ_data()
    econ_report.update_domain_data()
    econ_report.enter_summary_data()
    econ_report.econ_error_report.save(econ_report.report_filename)

if __name__=='__main__':
    main()

