import os
import sys
from globaldata import *

TBL_CREATE = \
'''
CREATE TABLE `%s` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `%s` varchar(255) DEFAULT NULL,
  `%s` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `asset_id` (`asset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

SQL_TEMPLATE = \
'''
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP TABLE IF EXISTS `%s`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;

%s

/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `%s` WRITE;

/*!40000 ALTER TABLE `%s` DISABLE KEYS */;

INSERT INTO `%s` VALUES %s;

/*!40000 ALTER TABLE `%s` ENABLE KEYS */;

UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
'''


def get_data_str(input_file):
    data_str_list = []
    with open(input_file) as infile:
        line_count = 0
        for line in infile.readlines()[1:]:
            line_count += 1
            line = line.strip().strip()
            print line_count
            line_vals = tuple(line.split(','))
            data_val_str = "(%s, %s, '%s', '%s')" % line_vals
            data_str_list.append("%s" % data_val_str)
        data_str = ','.join(data_str_list)
    return data_str


if __name__=='__main__':
    tbl_name   = sys.argv[1]
    filename   = ERR_TBL_DATA[tbl_name]['filename']
    msg_col    = ERR_TBL_DATA[tbl_name]['msg_col']
    flg_col    = ERR_TBL_DATA[tbl_name]['flg_col']
    date       = get_date()
    csv_file   = DATA_DIR + filename % date
    sql_file   = DATA_DIR + '%s_%s.sql' % (tbl_name, date)

    create_tbl = TBL_CREATE % (tbl_name, msg_col, flg_col)
    data_str   = get_data_str(csv_file)
    params     = (tbl_name, create_tbl, tbl_name, tbl_name, tbl_name, data_str, tbl_name)
    sql_output = SQL_TEMPLATE % params

    with open(sql_file, 'w') as outfile:
        outfile.write(sql_output)

