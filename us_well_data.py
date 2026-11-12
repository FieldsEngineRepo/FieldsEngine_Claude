import globaldata as gd

class WellData():
    def __init__(self, table_name, database, server='', username='', password='', external=False, create_tbl=False, import_data=False, commit_rows=False, debug=False):
        self.table_name      = table_name
        self.database        = database
        self.server          = server
        self.username        = username
        self.password        = password
        self.external        = external
        self.create_tbl      = create_tbl
        self.import_data     = import_data
        self.commit_rows     = commit_rows
        self.debug           = debug

        self.has_primary_key = False
        self.primary_key_col = ''
        self.primary_key_str = ''
        self.auto_incr_str   = ''
        self.sql_create      = 'CREATE TABLE `{}` ({}{}) ENGINE=InnoDB {}DEFAULT CHARSET=utf8'
        self.col_create      = '\n'

        self.int_conn        = gd.get_connection(server='mysql', database='us_wells')
        self.ext_conn        = gd.get_connection(server='sql_server', database=self.database, external=self.external, server_name=self.server, username=self.username, password=self.password)
        self.int_curr        = self.int_conn.cursor()
        self.ext_curr        = self.ext_conn.cursor()

        self.table_cols      = self.get_table_cols()
        self.column_str      = self.get_column_str()
        self.variable_str    = self.get_variable_str()
        self.insert_str      = self.gen_insert_str()
        self.start_dt        = gd.get_datetime()
        self.end_dt          = ''

    def get_table_cols(self):
        print 'Retrieving table columns for {} ...'.format(self.table_name)
        self.ext_curr.execute("SELECT DISTINCT COLUMN_NAME, ORDINAL_POSITION FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}' ORDER BY ORDINAL_POSITION".format(self.table_name))
        table_cols = ['[{}]'.format(str(data[0])) for data in self.ext_curr.fetchall()]
        if self.debug:
            print '(get_table_cols): {}'.format(table_cols)
        return table_cols

    def get_column_str(self):
        column_str = ", ".join(self.table_cols)
        if self.debug:
            print '(get_column_str): {}'.format(column_str)
        return column_str

    def get_variable_str(self):
        sql_select = "SELECT COUNT(DISTINCT COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}'".format(self.table_name)
        self.ext_curr.execute(sql_select)
        column_count = int(self.ext_curr.fetchone()[0])
        variable_str = ", ".join(["%s"]*column_count)
        return variable_str

    def get_table_data(self):
        sql_select = "SELECT COLUMN_NAME, IS_NULLABLE, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, ORDINAL_POSITION FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}' ORDER BY ORDINAL_POSITION".format(self.table_name)
        if self.debug:
            print '(get_table_data): {}'.format(sql_select)
        self.ext_curr.execute(sql_select)
        table_info = self.ext_curr.fetchall()
        return table_info

    def primary_key_check(self, col_name):
        is_primary_key = 0
        sql_select = "SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME='{}' AND COLUMN_NAME='{}'".format(self.table_name, col_name)
        if self.debug:
            print '(primary_key_check): {}'.format(sql_select)
        self.ext_curr.execute(sql_select)
        return_data = self.ext_curr.fetchall()
        if return_data:
            if self.debug:
                print '(primary_key_check): return_data={}'.format(return_data)
            key_type = return_data[0][0]
            if key_type == 'P':
                is_primary_key = 1
                self.has_primary_key = True
                self.primary_key_col = col_name
        return is_primary_key

    def auto_increment_check(self, col_name):
        is_auto_incr = 0
        sql_select = "SELECT sys.columns.is_identity FROM sys.columns JOIN sys.objects ON sys.columns.object_id=sys.objects.object_id WHERE sys.objects.name='{}' AND sys.columns.name='{}'".format(self.table_name, col_name)
        if self.debug:
            print '(auto_increment_check): {}'.format(sql_select)
        self.ext_curr.execute(sql_select)
        is_auto_incr = int(self.ext_curr.fetchone()[0])
        return is_auto_incr

    def gen_insert_str(self):
        col_str = self.column_str[:]
        col_str = col_str.replace('[', '`')
        col_str = col_str.replace(']', '`')
        sql_insert_str = "INSERT INTO {} ({}) VALUES ({})".format(self.table_name, col_str, self.variable_str)
        if self.debug:
            print '(gen_insert_str): {}'.format(sql_insert_str)
        return sql_insert_str

    def create_table(self):
        print 'Importing table structure data for {} ...'.format(self.table_name)
        table_data = self.get_table_data()
        col_count  = len(table_data)
        col_num    = 1
        self.int_curr.execute('DROP TABLE IF EXISTS {}'.format(self.table_name))
        for col_name, is_nullable, data_type, char_len, ord_pos in table_data:
            if self.debug:
                print '(create_table): {} - {} - {} - {}'.format(col_name, is_nullable, data_type, char_len)
            is_primary_key = 0
            row_end = ''
            null_prefix = 'NOT'
            if not self.has_primary_key:
                is_primary_key = self.primary_key_check(col_name)
                if is_primary_key:
                    self.primary_key_str = 'PRIMARY KEY(`{}`)\n'.format(col_name)
            is_auto_incr = self.auto_increment_check(col_name)
            if char_len:
                data_type = '{}({})'.format(data_type, char_len)
            if is_nullable == 'YES':
                null_prefix = 'DEFAULT'
            if is_auto_incr:
                row_end = ' AUTO_INCREMENT'
                self.auto_incr_str = 'AUTO_INCREMENT=1 '
            if (not col_num == col_count) or self.has_primary_key:
                row_end += ','
            self.col_create += '`{}` {} {} NULL{}\n'.format(col_name, data_type, null_prefix, row_end)
            col_num += 1
        if self.debug:
            print '(create_table): \n{}'.format(self.sql_create.format(self.table_name, self.col_create, self.primary_key_str, self.auto_incr_str))
        print 'Creating table {} ...'.format(self.table_name)
        self.int_curr.execute(self.sql_create.format(self.table_name, self.col_create, self.primary_key_str, self.auto_incr_str))
        gd.commit(self.int_curr)


    def import_ext_data(self):
        print 'Importing data for {} from external server ...'.format(self.table_name)
        if self.debug:
            print '(import_ext_data): {}'.format('SELECT {} FROM {}'.format(self.column_str, self.table_name))
        self.ext_curr.execute('SELECT {} FROM {}'.format(self.column_str, self.table_name))
        ext_data = self.ext_curr.fetchall()
        ext_datarow_count = len(ext_data)
        datarow_num = 0
        print 'Inserting data into {} ...'.format(self.table_name)
        for datarow in ext_data:
            datarow_num += 1
            output_msg = 'processing row {}/{}'.format(datarow_num, ext_datarow_count)
            if self.debug:
                output_msg += ': {}'.format(self.insert_str % datarow)
            print output_msg
            self.int_curr.execute(self.insert_str, datarow)
            if self.commit_rows:
                gd.commit(self.int_curr)
        if not self.commit_rows:
            gd.commit(self.int_curr)


    def main(self):
        if self.create_tbl:
            self.create_table()
        if self.import_data:
            self.import_ext_data()
        self.ext_curr.close()
        self.ext_conn.close()
        self.int_curr.close()
        self.int_conn.close()
        self.end_dt = gd.get_datetime()
        print 'Total processing time: {}'.format(gd.elapsed_time(self.start_dt, self.end_dt))


if __name__ == '__main__':
    conn = gd.get_connection(server='sql_server', database='US_Wells_DataExtract', server_name='220.225.231.116', username='uswellsdata', password='uswellsdata', external=True)
    curr = conn.cursor()
    curr.execute('SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS')
    us_wells_tables = [data[0] for data in curr.fetchall()]
    curr.close()
    conn.close()
    for us_wells_table in us_wells_tables:
        print 'Processing US_Wells_DataExtract.dbo.{} ...'.format(us_wells_table)
        WellData(table_name=us_wells_table, database='US_Wells_DataExtract', server='220.225.231.116', username='uswellsdata', password='uswellsdata', external=True, create_tbl=True, import_data=True).main()
