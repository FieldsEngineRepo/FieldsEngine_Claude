from globaldata import *


class ImpliedPriceReport:
    def __init__(self):
        # Initialize variables related to database
        self.conn                 = get_connection()
        self.curr                 = self.conn.cursor()

        # Initialize variables related to Excel report document
        self.run_date              = get_date()
        self.report_filename       = self._report_filename()
        self.implied_price_report  = self._implied_price_report()
        self.implied_price_input   = self._implied_price_input()
        self.implied_price_output  = self._implied_price_output()
        self.implied_price_summary = self._implied_price_summary()
        self.ineligible_deals      = self._ineligible_deals()

    def _report_filename(self):
        return IMPLIED_PR_RPT % self.run_date

    def _implied_price_report(self):
        shutil.copy2(IMPLIED_PR_TMP, self.report_filename)
        return openpyxl.load_workbook(self.report_filename)

    def _implied_price_input(self):
        return self.implied_price_report['Input Deals Data']

    def _implied_price_output(self):
        return self.implied_price_report['Implied Price Report Raw Data']

    def _implied_price_summary(self):
        return self.implied_price_report['SUMMARY']

    def _ineligible_deals(self):
        return self.implied_price_report['Ineligible Deals']

    def find_outliers(self):
        update_all_out  = 'UPDATE deals SET implied_oil_outliers=0, implied_gas_outliers=0, value_diff_outliers=0'
        update_oil_out  = 'UPDATE deals SET implied_oil_outliers=1 WHERE (implied_oil > 130.0 OR implied_oil < 20.0) AND (implied_oil < 0.0 OR implied_oil > 0.0)'
        update_gas_out  = 'UPDATE deals SET implied_gas_outliers=1 WHERE (implied_gas > 20.0 OR implied_gas < 0.2) AND (implied_gas < 0.0 OR implied_gas > 0.0)'
        update_diff_out = 'UPDATE deals SET value_diff_outliers=1 WHERE (value_diff > 0.20 OR value_diff < -0.20) AND (value_diff < 0.0 OR value_diff > 0.0)'
        self.curr.execute(update_all_out)
        self.curr.execute('COMMIT')
        self.curr.execute(update_oil_out)
        self.curr.execute('COMMIT')
        self.curr.execute(update_gas_out)
        self.curr.execute('COMMIT')
        self.curr.execute(update_diff_out)
        self.curr.execute('COMMIT')

    def get_input_data(self):
        ext_conn = get_connection(server='sql_server', database='OGEngineDataExtract', external=True)
        ext_curr = ext_conn.cursor()
        sql_select  = 'SELECT [AssetID],[Asset/Target],[Country],[Region],[Asset Status],[DealID],[Deal Type],[Deal Value (US$ mil)],[Deal Effective date], '
        sql_select += '[Announced Date],[Deals Financials -  Acquired],[ExtractDate] FROM [OGEngineDataExtract].[dbo].[tblImpliedOilPriceInput]'
        ext_curr.execute(sql_select)
        input_data = ext_curr.fetchall()
        ext_curr.close()
        ext_conn.close()
        return input_data

    def get_output_data(self):
        sql_select  = 'SELECT IFNULL(d.parent_id,""), IFNULL(d.parent_asset_name,""), IFNULL(d.parent_country,""), IFNULL(a.constituent,""), IFNULL(d.parent_region,""), IFNULL(a.resource_type,""), IFNULL(a.terrain,""), '
        sql_select += 'IFNULL(d.parent_status,""), IFNULL(d.deal_id,""), IFNULL(d.implied_npv,""), IFNULL(d.npv_remain,""), IFNULL(d.implied_oil,""), IFNULL(d.implied_gas,""), '
        sql_select += 'IFNULL(d.value_diff,""), IFNULL(d.implied_oil_outliers,""), IFNULL(d.implied_gas_outliers,""), IFNULL(d.value_diff_outliers,"") FROM deals AS d, assets AS a WHERE d.parent_id=a.asset_id AND d.calc_implied_prices=1'
        self.curr.execute(sql_select)
        return self.curr.fetchall()

    def get_ineligible_deals_data(self):
        params = ['deal_id', 'parent_id', 'parent_asset_name', 'parent_country', 'parent_region', 'parent_status', 'parent_asset_count', 'asset_id', 'asset_name', 'country', 'region', 'asset_status', 'deal_type', 'deal_year', 'deal_value', 'deal_stake', 'implied_npv', 'npv_remain', 'effective_date', 'announced_date ']
        param_str = ', '.join(['IFNULL(%s,"")' % param for param in params])
        sql_select  = 'SELECT %s FROM deals WHERE calc_implied_prices=0' % param_str
        self.curr.execute(sql_select)
        return self.curr.fetchall()

    def get_summary_data(self):
        sql_select = 'SELECT parent_region, IFNULL(SUM(implied_oil_outliers), 0), IFNULL(SUM(implied_gas_outliers), 0), IFNULL(SUM(value_diff_outliers), 0) FROM deals WHERE calc_implied_prices=1 GROUP BY parent_region ORDER BY parent_region'
        self.curr.execute(sql_select)
        return self.curr.fetchall()

    def enter_input_data(self):
        row_num = 2
        cols = 'ABCDEFGHIJKL'
        input_data = self.get_input_data()
        for datarow in input_data:
            for data_indx in range(len(datarow)):
                if decode_str(str(datarow[data_indx])) != 'None':
                    self.implied_price_input[cols[data_indx] + str(row_num)].value = decode_str(str(datarow[data_indx]))
                else:
                    self.implied_price_input[cols[data_indx] + str(row_num)].value = ''
            row_num += 1

    def enter_output_data(self):
        row_num = 2
        cols = 'ABCDEFGHIJKLMNOPQ'
        output_data = self.get_output_data()
        for datarow in output_data:
            for data_indx in range(len(datarow)):
                try:
                    self.implied_price_output[cols[data_indx] + str(row_num)].value = float(decode_str(str(datarow[data_indx])))
                except:
                    self.implied_price_output[cols[data_indx] + str(row_num)].value = decode_str(str(datarow[data_indx]))
            row_num += 1

    def enter_ineligible_deals(self):
        row_num = 2
        cols = 'ABCDEFGHIJKLMNOPQRST'
        ineligible_data = self.get_ineligible_deals_data()
        for datarow in ineligible_data:
            for data_indx in range(len(datarow)):
                self.ineligible_deals[cols[data_indx] + str(row_num)].value = decode_str(str(datarow[data_indx]))
            row_num += 1

    def enter_summary_data(self):
        row_num = 5
        summary_data = self.get_summary_data()
        for datarow in summary_data:
            self.implied_price_summary['A' + str(row_num)].value = datarow[0]
            self.implied_price_summary['B' + str(row_num)].value = datarow[1]
            self.implied_price_summary['C' + str(row_num)].value = datarow[2]
            self.implied_price_summary['D' + str(row_num)].value = datarow[3]
            row_num += 1

    def run(self):
        self.find_outliers()
        self.enter_input_data()
        self.enter_output_data()
        self.enter_ineligible_deals()
        self.enter_summary_data()
        self.implied_price_report.save(self.report_filename)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    implied_price_report = ImpliedPriceReport()
    implied_price_report.run()

if __name__=='__main__':
    main()

