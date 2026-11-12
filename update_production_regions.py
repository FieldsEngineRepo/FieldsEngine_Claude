from globaldata import *

regions = ['Africa', 'Asia', 'Caribbean', 'Central America', 'Europe', 'Former Soviet Union', 'Middle East', 'North America', 'Oceania', 'South America']

'''
CREATE TABLE production_%s (
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
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
TRUNCATE production_north_america;

INSERT INTO production_north_america (asset_id, asset_name, country, constituent, region, commodity, period, production, unit, casetype, asset_relationship, sources, 
data_source, last_update, add_by, add_date, edit_by, edit_date)
(SELECT asset_id, asset_name, country, constituent, region, commodity, period, production, unit, casetype, asset_relationship, sources, 
data_source, last_update, add_by, add_date, edit_by, edit_date FROM production WHERE region='North America' AND casetype='Base Case' AND NOT sources='EST: Forecast Engine');
'''

def generate_region_tables(curr):
    pass