from globaldata import *


class ComplexityScoreReport:
    def __init__(self):
        # Initialize variables related to database
        self.conn                 = get_connection()
        self.curr                 = self.conn.cursor()

        # Initialize variables related to Excel report document
        self.run_date             = get_date()
        self.report_filename      = self._report_filename()
        self.complexity_report    = self._complexity_report()

        self.model_rules          = self._model_rules()
        self.alloc_tables         = self._alloc_tables()
        self.excluded_params      = self._excluded_params()
        self.complexity_summary   = self._complexity_summary()

        self.parameter_count      = self._parameter_count()
        self.commodity_count      = self._commodity_count()
        self.covered_comm_count   = self._covered_comm_count()
        self.complete_param_count = self._complete_param_count()

    def _report_filename(self):
        return MINING_CPX_RPT % self.run_date

    def _complexity_report(self):
        shutil.copy2(MINING_CPX_TMP, self.report_filename)
        return openpyxl.load_workbook(self.report_filename)

    def _mining_model_rules(self):
        return self.complexity_report['Mining Model Rules']

    def _assumption_commodity(self):
        return self.complexity_report['Assumption by Commodity']

    def _complexity_summary(self):
        return self.complexity_report['Complexity Summary']

    def _parameter_count(self):
        self.curr.execute('SELECT COUNT(DISTINCT param_name) FROM mining_model_rules WHERE NOT param_name="BASE_UNIT" AND LENGTH(param_name)>0')
        return self.curr.fetchone()[0]

    def _commodity_count(self):
        self.curr.execute('SELECT COUNT(DISTINCT commodity) FROM mining_ore_averages WHERE NOT (commodity LIKE "%,%" OR LENGTH(commodity)=0) ORDER BY commodity')
        return self.curr.fetchone()[0]

    def _covered_comm_count(self):
        sql_select  = 'SELECT COUNT(comm.commodity) FROM '
        sql_select += '(SELECT commodity, COUNT(DISTINCT param_name) AS param_count FROM mining_model_rules WHERE NOT param_name="BASE_UNIT" '
        sql_select += 'AND NOT (commodity IS NULL OR LENGTH(commodity)=0) GROUP BY commodity ORDER BY commodity) AS comm '
        sql_select += 'WHERE comm.param_count=%s'
        self.curr.execute(sql_select % self.parameter_count)
        return self.curr.fetchone()[0]

    def _complete_param_count(self):
        sql_select  = 'SELECT COUNT(param.param_name) FROM '
        sql_select += '(SELECT param_name, COUNT(DISTINCT commodity) AS comm_count FROM mining_model_rules WHERE NOT param_name="BASE_UNIT" '
        sql_select += 'AND NOT (commodity IS NULL OR LENGTH(commodity)=0) GROUP BY commodity ORDER BY commodity) AS param '
        sql_select += 'WHERE param.comm_count=%s'
        self.curr.execute(sql_select % self.commodity_count)
        return self.curr.fetchone()[0]

    def get_model_rules_data(self):
        self.curr.execute('SELECT MineId, mineCountry, mineRegion, mineType, mineMethod, commodity, param_name, param_value, add_by, edit_date FROM mining_model_rules WHERE NOT param_name="BASE_UNIT" ')
        return self.curr.fetchall()

    def get_assumption_commodity_data(self):
        sql_select  = 'SELECT param_name, commodity, COUNT(*) FROM mining_model_rules WHERE NOT param_name="BASE_UNIT" AND NOT '
        sql_select += '(commodity IS NULL OR LENGTH(commodity)=0) GROUP BY param_name, commodity ORDER BY param_name, commodity'
        self.curr.execute(sql_select)
        return self.curr.fetchall()

    def get_summary_data(self):
        sql_select  = 'SELECT param_name, COUNT(*) FROM mining_model_rules WHERE NOT param_name="BASE_UNIT" '
        sql_select += 'AND NOT (commodity IS NULL OR LENGTH(commodity)=0) GROUP BY param_name ORDER BY param_name'
        self.curr.execute(sql_select)
        return self.curr.fetchall()

    def format_cell(self, cell):
        thin_side = openpyxl.styles.borders.Side(style='thin')
        cell_borders = openpyxl.styles.borders.Border(top=thin_side, bottom=thin_side, left=thin_side, right=thin_side)
        cell.border = cell_borders


    def enter_model_rules_data(self):
        row_num = 2
        cols = 'ABCDEFGHIJ'
        model_rules_data = self.get_model_rules_data()
        for datarow in model_rules_data:
            for data_indx in range(len(datarow)):
                self.mining_model_rules[cols[data_indx] + str(row_num)].value = datarow[data_indx]
                self.format_cell(self.mining_model_rules[cols[data_indx] + str(row_num)])
            self.mining_model_rules['K' + str(row_num)].value = get_datetime()
            self.mining_model_rules['L' + str(row_num)] = '=COUNTIF($B%s:F%s,"<>")*(5/5)' % (row_num, row_num)
            self.mining_model_rules['M' + str(row_num)] = '=IF((($K%s-$J%s)/30)>6,((($K%s-$J%s)/30)*-0.01),0)' % ((row_num,)*4)
            self.mining_model_rules['N' + str(row_num)] = '=L%s+M%s' % (row_num, row_num)
            self.format_cell(self.mining_model_rules['K' + str(row_num)])
            self.format_cell(self.mining_model_rules['L' + str(row_num)])
            self.format_cell(self.mining_model_rules['M' + str(row_num)])
            self.format_cell(self.mining_model_rules['N' + str(row_num)])
            row_num += 1

    def enter_commodity_data(self):
        row_num = 2
        commodity_data = self.get_assumption_commodity_data()
        for commodity_row in commodity_data:
            self.assumption_commodity['A' + str(row_num)].value = commodity_row[0]
            self.assumption_commodity['B' + str(row_num)].value = commodity_row[1]
            self.assumption_commodity['C' + str(row_num)].value = commodity_row[2]
            row_num += 1

    def enter_summary_data(self):
        row_num = 4
        summary_data = self.get_summary_data()
        for summary_row in summary_data:
            self.complexity_summary['A' + str(row_num)].value = summary_row[0]
            self.complexity_summary['B' + str(row_num)].value = summary_row[1]
            row_num += 1

    def enter_complexity_metrics(self):
        self.complexity_summary['F3'].value = self.parameter_count
        self.complexity_summary['F4'].value = self.commodity_count
        self.complexity_summary['F5'].value = self.covered_comm_count
        self.complexity_summary['F6'].value = self.complete_param_count

    def run(self):
        self.enter_model_rules_data()
        self.enter_commodity_data()
        self.enter_summary_data()
        self.enter_complexity_metrics()
        self.complexity_report.save(self.report_filename)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    mining_report = MiningComplexityReport()
    mining_report.run()

if __name__=='__main__':
    main()

