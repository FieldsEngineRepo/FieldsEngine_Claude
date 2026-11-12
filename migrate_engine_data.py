from globaldata import *


ENGINE_INPUT_TBLS = ['abandonment_alloc',
                     'assets',
                     'auxilary_param',
                     'capex_alloc',
                     'capex_redev_alloc',
                     'econ_error_exceptions',
                     'equity',
                     'error_log_exception',
                     'inflation',
                     'model_rules',
                     'operators',
                     'parent_companies',
                     'prices',
                     'prices_values',
                     'production',
                     'reserves',
                     'well_params',
                     'wells']

def get_sql_create(table_name, table_suffix='', create_tbl=False):
    conn = get_connection()
    curr = conn.cursor()
    col_str = ''
    sql_create = ''

    template = '''
CREATE TABLE %s (
  id int(11) NOT NULL AUTO_INCREMENT,%s
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8'''

    sql_select = 'SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS WHERE NOT COLUMN_NAME="id" AND TABLE_SCHEMA="globaldata" AND TABLE_NAME="%s" ORDER BY ORDINAL_POSITION'
    if curr.execute(sql_select % table_name):
        for column_name, column_type, is_nullable in curr.fetchall():
            column_type = column_type.upper()
            if column_type == 'TIMESTAMP':
                column_type += ' NULL'
            col_str += '\n  %s %s' % (column_name, column_type)
            if is_nullable:
                col_str += ' DEFAULT NULL'
            col_str += ','
        old_table = table_name + table_suffix
        sql_create += template % (old_table, col_str)
    if create_tbl and sql_create:
        print 'Creating %s table ...' % (old_table)
        print 'sql_create:', sql_create
        curr.execute(sql_create)
        curr.execute('COMMIT')
    curr.close()
    conn.close()
    return sql_create

def migrate_table(table_name, table_suffix):
    print 'Migrating data from %s to %s ...' % (table_name, table_name + table_suffix)
    conn = get_connection()
    curr = conn.cursor()
    old_table = table_name + table_suffix
    sql_insert = 'INSERT INTO %s (SELECT * FROM %s)' % (old_table, table_name)
    curr.execute(sql_insert)
    curr.execute('COMMIT')
    curr.close()
    conn.close()

'''
# Check assets table for removed assets
SELECT DISTINCT asset_id FROM old_assets WHERE NOT asset_id IN (SELECT DISTINCT asset_id FROM new_assets);

# Check assets table for new assets
SELECT DISTINCT asset_id FROM new_assets WHERE NOT asset_id IN (SELECT DISTINCT asset_id FROM old_assets);

# Check assets table for changed assets
SELECT DISTINCT asset_id FROM old_assets AS old, new_assets AS new WHERE NOT (new.asset_name=old.asset_name OR ... OR new.data_source=old.data_source) AND new.asset_id=old.asset_id;
'''


def find_added_data(table_name, table_suffix, no_id, data_only):
    conn = get_connection()
    curr = conn.cursor()
    added_data = []
    old_table = table_name + table_suffix
    table_columns = tuple(get_columns(table_name, no_id=no_id, data_only=data_only))
    row_count = 1
    if curr.execute('SELECT * FROM %s' % table_name):
        for datarow in curr.fetchall():
            print 'row num: %s' % row_count
            where_str = ''
            where_str_list = []

            if no_id:
                if data_only:
                    data_vals = datarow[1:-4]
                else:
                    data_vals = datarow[1:]
            else:
                if data_only:
                    data_vals = datarow[:-4]
                else:
                    data_vals = datarow[:]

            null_indxs = [indx for indx in range(len(data_vals)) if data_vals[indx] is None]
            non_null_indxs = [indx for indx in range(len(data_vals)) if not indx in null_indxs]
            for indx in range(len(data_vals)):
                col_name = table_columns[indx]
                if indx in null_indxs:
                    where_str_list.append('%s IS NULL ' % col_name)
                else:
                    where_str_list.append(col_name + '=%s ')
            where_str = 'AND '.join(where_str_list)
            sql_select = 'SELECT * FROM %s WHERE %s' % (old_table, where_str)
            non_null_vals = tuple([data_vals[indx] for indx in non_null_indxs])
            if not curr.execute(sql_select, non_null_vals):
                added_data.append(data_vals)
            row_count += 1
    curr.close()
    conn.close()
    return added_data

def find_removed_data(table_name, table_suffix):
    sql_select = 'SELECT DISTINCT id FROM %s WHERE NOT id IN (SELECT DISTINCT id FROM %s)'

def find_changed_data(table_name, table_suffix):
    pass

def main():
    for table_name in ENGINE_INPUT_TBLS:
        table_suffix = '_temp'
        drop_table(table=(table_name + table_suffix))
        get_sql_create(table_name, table_suffix, create_tbl=True)
        migrate_table(table_name, table_suffix)


if __name__=='__main__':
    #main()
    added_data = find_added_data('capex_alloc', '_temp', no_id=True, data_only=True)
    print len(added_data)
    print added_data

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





