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
            col_str += '\n  %s %s' % (column_name, column_type)
            if is_nullable:
                col_str += ' DEFAULT NULL'
            col_str += ','
        new_table = table_name + table_suffix
        sql_create += template % (new_table, col_str)
    if create_tbl and sql_create:
        print 'Creating %s table ...' % (new_table)
        curr.execute(sql_create)
        curr.execute('COMMIT')
    curr.close()
    conn.close()
    return sql_create

def migrate_table(table_name, table_suffix):
    print 'Migrating data from %s to %s ...' % (table_name, table_name + table_suffix)
    conn = get_connection()
    curr = conn.cursor()
    new_table = tale_name + table_suffix
    sql_insert = 'INSERT INTO %s (SELECT * FROM %s)' % (new_table, table_name)
    curr.execute(sql_insert)
    curr.execute('COMMIT')
    curr.close()
    conn.close()

def main():
    for table_name in ENGINE_INPUT_TBLS:
        table_suffix = '_temp'
        drop_table(table=(table_name + table_suffix))
        get_sql_create(table_name, table_suffix, create_tbl=True)
        migrate_table(table_name, table_suffix)


if __name__=='__main__':
    main()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
TBL_CREATE = {
'abandonment_alloc': '''
CREATE TABLE `abandonment_alloc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `commodity` varchar(150) DEFAULT NULL,
  `resource_type` varchar(100) DEFAULT NULL,
  `terrain` varchar(50) DEFAULT NULL,
  `facility_type` varchar(100) DEFAULT NULL,
  `production_total` varchar(100) DEFAULT NULL,
  `production_peak` varchar(100) DEFAULT NULL,
  `operators` varchar(100) DEFAULT NULL,
  `basin` varchar(200) DEFAULT NULL,
  `year_minus10` double DEFAULT NULL,
  `year_minus9` double DEFAULT NULL,
  `year_minus8` double DEFAULT NULL,
  `year_minus7` double DEFAULT NULL,
  `year_minus6` double DEFAULT NULL,
  `year_minus5` double DEFAULT NULL,
  `year_minus4` double DEFAULT NULL,
  `year_minus3` double DEFAULT NULL,
  `year_minus2` double DEFAULT NULL,
  `year_minus1` double DEFAULT NULL,
  `year_0` double DEFAULT NULL,
  `year_1` double DEFAULT NULL,
  `year_2` double DEFAULT NULL,
  `year_3` double DEFAULT NULL,
  `year_4` double DEFAULT NULL,
  `year_5` double DEFAULT NULL,
  `year_6` double DEFAULT NULL,
  `year_7` double DEFAULT NULL,
  `year_8` double DEFAULT NULL,
  `year_9` double DEFAULT NULL,
  `year_10` double DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25188 DEFAULT CHARSET=utf8;
''',
'assets': '''
CREATE TABLE `assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `asset_name` longtext,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `terrain` varchar(100) DEFAULT NULL,
  `basin` varchar(100) DEFAULT NULL,
  `resource_type` varchar(100) DEFAULT NULL,
  `prod_phase` varchar(100) DEFAULT NULL,
  `recover_factor` varchar(100) DEFAULT NULL,
  `assoc_asset_id` varchar(30) DEFAULT NULL,
  `assoc_asset_name` varchar(150) DEFAULT NULL,
  `assoc_region` varchar(100) DEFAULT NULL,
  `assoc_country` varchar(100) DEFAULT NULL,
  `assoc_area` varchar(150) DEFAULT NULL,
  `trap_type` varchar(50) DEFAULT NULL,
  `api_gravity` varchar(20) DEFAULT NULL,
  `sulfer` varchar(20) DEFAULT NULL,
  `lic_no` varchar(100) DEFAULT NULL,
  `county` varchar(100) DEFAULT NULL,
  `calorific` varchar(50) DEFAULT NULL,
  `hsulfer` varchar(50) DEFAULT NULL,
  `gor` varchar(50) DEFAULT NULL,
  `ablock` varchar(100) DEFAULT NULL,
  `ablock_region` varchar(150) DEFAULT NULL,
  `ablock_country` varchar(100) DEFAULT NULL,
  `ablock_constituent` varchar(150) DEFAULT NULL,
  `asset_relation` varchar(100) DEFAULT NULL,
  `irr` varchar(20) DEFAULT NULL,
  `payback_years` varchar(20) DEFAULT NULL,
  `capex` varchar(20) DEFAULT NULL,
  `opex` varchar(20) DEFAULT NULL,
  `reserve_status` varchar(100) DEFAULT NULL,
  `npv` varchar(20) DEFAULT NULL,
  `bc_npv` varchar(45) DEFAULT NULL,
  `lc_npv` varchar(45) DEFAULT NULL,
  `hc_npv` varchar(45) DEFAULT NULL,
  `facility_type` varchar(100) DEFAULT NULL,
  `formation` text,
  `water_depth` varchar(20) DEFAULT NULL,
  `discovery_date` varchar(50) DEFAULT NULL,
  `license_num` text,
  `license_effective` varchar(50) DEFAULT NULL,
  `license_expire` varchar(20) DEFAULT NULL,
  `porosity` varchar(10) DEFAULT NULL,
  `permeability` varchar(10) DEFAULT NULL,
  `measured_depth` varchar(10) DEFAULT NULL,
  `carbon_dioxide` varchar(10) DEFAULT NULL,
  `form_rock_type` varchar(100) DEFAULT NULL,
  `data_source` varchar(45) DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `asset_id` (`asset_id`),
  KEY `assets_status` (`status`),
  KEY `assets_region` (`region`)
) ENGINE=InnoDB AUTO_INCREMENT=31798 DEFAULT CHARSET=utf8;
''',
'auxilary_param': '''
CREATE TABLE `auxilary_param` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `resource_type` varchar(100) DEFAULT NULL,
  `param_name` varchar(100) DEFAULT NULL,
  `field_name` varchar(100) DEFAULT NULL,
  `data_range` varchar(100) DEFAULT NULL,
  `factor` double DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2355 DEFAULT CHARSET=utf8;
''',
'capex_alloc': '''
CREATE TABLE `capex_alloc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `params_values_id` int(11) DEFAULT NULL,
  `asset_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `commodity` varchar(150) DEFAULT NULL,
  `resource_type` varchar(100) DEFAULT NULL,
  `terrain` varchar(50) DEFAULT NULL,
  `facility_type` varchar(100) DEFAULT NULL,
  `operators` varchar(100) DEFAULT NULL,
  `basin` varchar(200) DEFAULT NULL,
  `production_total` varchar(100) DEFAULT NULL,
  `production_peak` varchar(100) DEFAULT NULL,
  `year_minus10` double DEFAULT NULL,
  `year_minus9` double DEFAULT NULL,
  `year_minus8` double DEFAULT NULL,
  `year_minus7` double DEFAULT NULL,
  `year_minus6` double DEFAULT NULL,
  `year_minus5` double DEFAULT NULL,
  `year_minus4` double DEFAULT NULL,
  `year_minus3` double DEFAULT NULL,
  `year_minus2` double DEFAULT NULL,
  `year_minus1` double DEFAULT NULL,
  `year_0` double DEFAULT NULL,
  `year_1` double DEFAULT NULL,
  `year_2` double DEFAULT NULL,
  `year_3` double DEFAULT NULL,
  `year_4` double DEFAULT NULL,
  `year_5` double DEFAULT NULL,
  `year_6` double DEFAULT NULL,
  `year_7` double DEFAULT NULL,
  `year_8` double DEFAULT NULL,
  `year_9` double DEFAULT NULL,
  `year_10` double DEFAULT NULL,
  `years_remaining` double DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=294249 DEFAULT CHARSET=utf8;
''',
'capex_redev_alloc': '''
CREATE TABLE `capex_redev_alloc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `params_values_id` int(11) DEFAULT NULL,
  `asset_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `commodity` varchar(150) DEFAULT NULL,
  `resource_type` varchar(100) DEFAULT NULL,
  `terrain` varchar(50) DEFAULT NULL,
  `facility_type` varchar(100) DEFAULT NULL,
  `production_total` varchar(100) DEFAULT NULL,
  `production_peak` varchar(100) DEFAULT NULL,
  `operators` varchar(100) DEFAULT NULL,
  `basin` varchar(200) DEFAULT NULL,
  `year_minus10` double DEFAULT NULL,
  `year_minus9` double DEFAULT NULL,
  `year_minus8` double DEFAULT NULL,
  `year_minus7` double DEFAULT NULL,
  `year_minus6` double DEFAULT NULL,
  `year_minus5` double DEFAULT NULL,
  `year_minus4` double DEFAULT NULL,
  `year_minus3` double DEFAULT NULL,
  `year_minus2` double DEFAULT NULL,
  `year_minus1` double DEFAULT NULL,
  `year_0` double DEFAULT NULL,
  `year_1` double DEFAULT NULL,
  `year_2` double DEFAULT NULL,
  `year_3` double DEFAULT NULL,
  `year_4` double DEFAULT NULL,
  `year_5` double DEFAULT NULL,
  `year_6` double DEFAULT NULL,
  `year_7` double DEFAULT NULL,
  `year_8` double DEFAULT NULL,
  `year_9` double DEFAULT NULL,
  `year_10` double DEFAULT NULL,
  `years_remaining` double DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22515 DEFAULT CHARSET=utf8;
''',
'econ_error_exceptions': '''
CREATE TABLE `econ_error_exceptions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `error_message` varchar(255) DEFAULT NULL,
  `error_flag` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `asset_id` (`asset_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
''',
'equity': '''
CREATE TABLE `equity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `asset_name` longtext,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `entity_name` varchar(150) DEFAULT NULL,
  `equity_pct` varchar(10) DEFAULT NULL,
  `equity_date` varchar(100) DEFAULT NULL,
  `operator` varchar(150) DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `equity_asset_id` (`asset_id`)
) ENGINE=InnoDB AUTO_INCREMENT=109344 DEFAULT CHARSET=utf8;
''',
'error_log_exception': '''
CREATE TABLE `error_log_exception` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `errorType` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `asset_id` (`asset_id`)
) ENGINE=InnoDB AUTO_INCREMENT=246593 DEFAULT CHARSET=utf8;
''',
'inflation': '''
CREATE TABLE `inflation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `commodity` varchar(150) DEFAULT NULL,
  `resource_type` varchar(100) DEFAULT NULL,
  `terrain` varchar(50) DEFAULT NULL,
  `facility_type` varchar(100) DEFAULT NULL,
  `production_total` varchar(100) DEFAULT NULL,
  `production_peak` varchar(100) DEFAULT NULL,
  `prod_phase` varchar(50) DEFAULT NULL,
  `operators` varchar(100) DEFAULT NULL,
  `basin` varchar(200) DEFAULT NULL,
  `param_name` varchar(100) DEFAULT NULL,
  `params_id` varchar(25) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `param_value` varchar(100) DEFAULT NULL,
  `case_type` varchar(100) DEFAULT NULL,
  `param_table` varchar(25) DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `model_rules_param_name` (`param_name`)
) ENGINE=InnoDB AUTO_INCREMENT=20272 DEFAULT CHARSET=utf8;
''',
'model_rules': '''
CREATE TABLE `model_rules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `commodity` varchar(150) DEFAULT NULL,
  `resource_type` varchar(100) DEFAULT NULL,
  `terrain` varchar(50) DEFAULT NULL,
  `facility_type` varchar(100) DEFAULT NULL,
  `production_total` varchar(100) DEFAULT NULL,
  `production_peak` varchar(100) DEFAULT NULL,
  `prod_phase` varchar(50) DEFAULT NULL,
  `operators` varchar(100) DEFAULT NULL,
  `basin` varchar(200) DEFAULT NULL,
  `param_name` varchar(100) DEFAULT NULL,
  `params_id` varchar(25) DEFAULT NULL,
  `param_value` varchar(100) DEFAULT NULL,
  `param_table` varchar(25) DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `model_rules_param_name` (`param_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1021437 DEFAULT CHARSET=utf8;
''',
'operators': '''
CREATE TABLE `operators` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32768 DEFAULT CHARSET=utf8;
''',
'parent_companies': '''
CREATE TABLE `parent_companies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_name` varchar(200) DEFAULT NULL,
  `parent_company` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42169 DEFAULT CHARSET=utf8;
''',
'prices': '''
CREATE TABLE `prices` (
  `id` int(11) NOT NULL,
  `price_code` varchar(25) DEFAULT NULL,
  `price_name` varchar(100) DEFAULT NULL,
  `unit` longtext,
  `commodity` varchar(50) DEFAULT NULL,
  `source` longtext,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
''',
'prices_values': '''
CREATE TABLE `prices_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prices_id` int(11) DEFAULT NULL,
  `period` double DEFAULT NULL,
  `prices_valuescol` varchar(45) DEFAULT NULL,
  `price_value` double DEFAULT NULL,
  `case_type` varchar(100) DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2109766 DEFAULT CHARSET=utf8;
''',
'production': '''
CREATE TABLE `production` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `asset_name` longtext,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `commodity` varchar(100) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `production` double DEFAULT NULL,
  `unit` varchar(25) DEFAULT NULL,
  `casetype` varchar(45) DEFAULT NULL,
  `asset_relationship` varchar(45) DEFAULT NULL,
  `sources` longtext,
  `data_source` longtext,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `prod_asset` (`asset_id`),
  KEY `prod_period` (`period`),
  KEY `prod_commod` (`commodity`),
  KEY `prod_ctype` (`casetype`),
  KEY `prod_region` (`region`)
) ENGINE=InnoDB AUTO_INCREMENT=6449424 DEFAULT CHARSET=utf8;
''',
'reserves': '''
CREATE TABLE `reserves` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `asset_name` longtext,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(100) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `field_status` varchar(45) DEFAULT NULL,
  `reserve_status` varchar(45) DEFAULT NULL,
  `reserve_type` varchar(45) DEFAULT NULL,
  `commodity` varchar(100) DEFAULT NULL,
  `reserve_pub_date` datetime DEFAULT NULL,
  `reserve_volume` float DEFAULT NULL,
  `unit` varchar(45) DEFAULT NULL,
  `reserve_source` text,
  `casetype` varchar(45) DEFAULT NULL,
  `data_source` varchar(45) DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reserves_asset_id` (`asset_id`),
  KEY `reserves_reserve_type` (`reserve_type`)
) ENGINE=InnoDB AUTO_INCREMENT=363223 DEFAULT CHARSET=utf8;
''',
'well_params': '''
CREATE TABLE `well_params` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `asset_name` longtext,
  `status` varchar(45) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `commodity` varchar(100) DEFAULT NULL,
  `resource_type` varchar(100) DEFAULT NULL,
  `terrain` varchar(100) DEFAULT NULL,
  `facility_type` varchar(100) DEFAULT NULL,
  `operator` varchar(150) DEFAULT NULL,
  `decline_rate` double DEFAULT NULL,
  `capex_maintenance` double DEFAULT NULL,
  `facility_cost` double DEFAULT NULL,
  `fixed_opex_rate` double DEFAULT NULL,
  `rig_years` double DEFAULT NULL,
  `well_life` double DEFAULT NULL,
  `drilling_split` double DEFAULT NULL,
  `dc_days` double DEFAULT NULL,
  `dc_cost` double DEFAULT NULL,
  `rig_count` double DEFAULT NULL,
  `opex_liquids` double DEFAULT NULL,
  `opex_gas` double DEFAULT NULL,
  `opex_trans_liquids` double DEFAULT NULL,
  `opex_trans_gas` double DEFAULT NULL,
  `abandonment` double DEFAULT NULL,
  `rig_mobilization_days` int(11) DEFAULT NULL,
  `duc_life` double DEFAULT NULL,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33310 DEFAULT CHARSET=utf8;
''',
'wells': '''
CREATE TABLE `wells` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `asset_name` longtext,
  `country` varchar(100) DEFAULT NULL,
  `constituent` varchar(150) DEFAULT NULL,
  `commodity` varchar(15) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `datatype` varchar(100) DEFAULT NULL,
  `period` varchar(100) DEFAULT NULL,
  `production_count` double DEFAULT NULL,
  `unit` varchar(25) DEFAULT NULL,
  `casetype` varchar(45) DEFAULT NULL,
  `asset_relationship` varchar(45) DEFAULT NULL,
  `sources` longtext,
  `data_source` longtext,
  `add_by` varchar(45) DEFAULT NULL,
  `add_date` timestamp NULL DEFAULT NULL,
  `edit_by` varchar(45) DEFAULT NULL,
  `edit_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27266 DEFAULT CHARSET=utf8;
'''
}
"""





