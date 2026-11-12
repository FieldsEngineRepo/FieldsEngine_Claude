from globaldata import *


class MiningErrorReport:
    def __init__(self):
        # Initialize variables related to database
        self.conn                 = get_connection(database='miningengineextract')
        self.curr                 = self.conn.cursor()

        # Initialize variables related to Excel report document
        self.run_date             = get_date()
        self.report_filename      = self._report_filename()
        self.mining_error_report  = self._mining_error_report()
        self.mining_error_log     = self._mining_error_log()
        self.mining_error_summary = self._mining_error_summary()
        self.commodity_summary    = self._commodity_summary()
        self.date_str             = self._date_str()
        self.modelled_count       = self._modelled_count()
        self.not_modelled_count   = self._not_modelled_count()
        self.error_mine_count     = self._error_mine_count()
        self.eligible_mine_count  = self._eligible_mine_count()

    def _report_filename(self):
        return MINING_ERR_RPT % self.run_date

    def _mining_error_report(self):
        shutil.copy2(MINING_ERR_TMP, self.report_filename)
        return openpyxl.load_workbook(self.report_filename)

    def _mining_error_log(self):
        return self.mining_error_report['Mining Error Log']

    def _mining_error_summary(self):
        return self.mining_error_report['Mining Error Summary']

    def _commodity_summary(self):
        return self.mining_error_report['Commodity Summary']

    def _date_str(self):
        run_year, run_month, run_day = self.run_date[:4], self.run_date[4:6], self.run_date[6:8]
        month_name = get_month_name(run_month)
        return '(%s %s, %s)' % (month_name, run_day, run_year)

    def _modelled_count(self):
        self.curr.execute('SELECT SUM(modelled) FROM mining_metrics')
        return int(self.curr.fetchone()[0])

    def _not_modelled_count(self):
        self.curr.execute('SELECT SUM(not_modelled) FROM mining_metrics')
        return int(self.curr.fetchone()[0])

    def _error_mine_count(self):
        self.curr.execute('SELECT COUNT(DISTINCT MineId) FROM mining_error_log')
        return int(self.curr.fetchone()[0])

    def _eligible_mine_count(self):
        return (self.modelled_count + self.not_modelled_count)

    def get_error_data(self):
        sql_select = 'SELECT MineId, MineName, mineRegion, Commodities, period, error_type, comment FROM mining_error_log ORDER BY error_type, MineId'
        self.curr.execute(sql_select)
        return self.curr.fetchall()

    def get_commodity_data(self):
        self.curr.execute('SELECT commodity, modelled, not_modelled FROM mining_metrics ORDER BY commodity')
        return self.curr.fetchall()

    def get_summary_data(self, detailed=False):
        if detailed:
            sql_select = 'SELECT error_type, comment, COUNT(*) AS total_errors FROM mining_error_log GROUP BY error_type, comment ORDER BY error_type, comment'
        else:
            sql_select = 'SELECT error_type, COUNT(*) AS total_errors FROM mining_error_log GROUP BY error_type ORDER BY error_type'
        self.curr.execute(sql_select)
        return self.curr.fetchall()

    def enter_error_log_data(self):
        row_num = 2
        cols = 'ABCDEFG'
        error_data = self.get_error_data()
        for error_row in error_data:
            for data_indx in range(len(error_row)):
                self.mining_error_log[cols[data_indx] + str(row_num)].value = error_row[data_indx]
            row_num += 1

    def enter_commodity_summary(self):
        row_num = 2
        commodity_data = self.get_commodity_data()
        for commodity_row in commodity_data:
            self.commodity_summary['A' + str(row_num)].value = commodity_row[0]
            self.commodity_summary['B' + str(row_num)].value = commodity_row[1]
            self.commodity_summary['C' + str(row_num)].value = commodity_row[2]
            row_num += 1

    def enter_summary_data(self):
        row_num = 20
        detailed_summary_data = self.get_summary_data(detailed=True)
        for detailed_summary_row in detailed_summary_data:
            self.mining_error_summary['A' + str(row_num)].value = detailed_summary_row[0]
            self.mining_error_summary['B' + str(row_num)].value = detailed_summary_row[1]
            self.mining_error_summary['F' + str(row_num)].value = detailed_summary_row[2]
            row_num += 1

        row_num = 4
        summary_data = self.get_summary_data()
        for summary_row in summary_data:
            self.mining_error_summary['A' + str(row_num)].value = summary_row[0]
            self.mining_error_summary['B' + str(row_num)].value = summary_row[1]
            row_num += 1

    def enter_mining_metrics(self):
        self.mining_error_summary['E3'].value += self.date_str
        self.mining_error_summary['F3'].value = self.eligible_mine_count
        self.mining_error_summary['F4'].value = self.modelled_count
        self.mining_error_summary['F5'].value = self.not_modelled_count
        self.mining_error_summary['F6'].value = self.error_mine_count

    def run(self):
        self.enter_error_log_data()
        self.enter_commodity_summary()
        self.enter_summary_data()
        self.enter_mining_metrics()
        self.mining_error_report.save(self.report_filename)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def mining_error_main():
    mining_report = MiningErrorReport()
    mining_report.run()

if __name__=='__main__':
    mining_error_main()

