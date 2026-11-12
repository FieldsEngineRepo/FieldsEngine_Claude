import globaldata as gd

def main(debug=False):
	start_time = gd.get_datetime()
	print 'start: {}'.format(start_time)
	conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
	curr = conn.cursor()
	
	col_names = gd.get_data("COLUMN_NAME", "INFORMATION_SCHEMA.COLUMNS", sql_where="TABLE_NAME='tx_well_details' AND TABLE_SCHEMA='dbo' AND COLUMN_NAME!='id'", cursor=curr, debug=debug)
	col_str = ', '.join(col_names)

	sql_create = \
	"""
	DROP TABLE IF EXISTS tx_well_details_;
	CREATE TABLE tx_well_details_ (
	  id                     INT IDENTITY,
	  lease_prod_id          INT         DEFAULT NULL,
	  well_id                BIGINT      DEFAULT NULL,
	  api_number             VARCHAR(20) DEFAULT NULL,
	  tx_well_id             VARCHAR(15) DEFAULT NULL,
	  lease_id               VARCHAR(20) DEFAULT NULL,
	  lease_no               VARCHAR(6)  DEFAULT NULL,
	  lease_name             VARCHAR(100)DEFAULT NULL,
	  district_no            VARCHAR(2)  DEFAULT NULL,
	  county_no              VARCHAR(3)  DEFAULT NULL,
	  county                 VARCHAR(50) DEFAULT NULL,
	  well_no                VARCHAR(10) DEFAULT NULL,
	  commodity              VARCHAR(30) DEFAULT NULL,
	  well_status            VARCHAR(50) DEFAULT NULL,
	  engine_well_status     VARCHAR(50) DEFAULT NULL,
	  well_type              INT         DEFAULT NULL,
	  well_direction         VARCHAR(50) DEFAULT NULL,
	  wellbore_profile       INT         DEFAULT NULL,
	  state_well_direction   VARCHAR(50) DEFAULT NULL,
	  resource_play          VARCHAR(250)DEFAULT NULL,
	  formation              VARCHAR(250)DEFAULT NULL,
	  basin                  VARCHAR(100)DEFAULT NULL,
	  operator_no            INT         DEFAULT NULL,
	  operator               VARCHAR(150)DEFAULT NULL,
	  field_no               INT         DEFAULT NULL,
	  true_vertical_depth    FLOAT       DEFAULT NULL,
	  measured_depth         FLOAT       DEFAULT NULL,
	  lateral_length         FLOAT       DEFAULT NULL,
	  total_depth            FLOAT       DEFAULT NULL,
	  api_depth              FLOAT       DEFAULT NULL,
	  top_perforation        FLOAT       DEFAULT NULL,
	  bottom_perforation     FLOAT       DEFAULT NULL,
	  perforation_diff       FLOAT       DEFAULT NULL,
	  measured_vertical_diff FLOAT       DEFAULT NULL,
	  spud_date              VARCHAR(20) DEFAULT NULL,
	  completion_date        VARCHAR(20) DEFAULT NULL,
	  shut_in_date           VARCHAR(20) DEFAULT NULL,
	  plug_date              VARCHAR(15) DEFAULT NULL,
	  first_production_date  VARCHAR(15) DEFAULT NULL,
	  last_production_date   VARCHAR(15) DEFAULT NULL,
	  process_code           TINYINT     DEFAULT NULL,
	  lease_start_date       VARCHAR(16) DEFAULT NULL,
	  lease_end_date         VARCHAR(16) DEFAULT NULL,
	  prev_well_start        VARCHAR(12) DEFAULT NULL,
	  well_root_id           INT         DEFAULT NULL,
	  drill_permit_no        VARCHAR(6)  DEFAULT NULL,
	  PRIMARY KEY (id));

	CREATE INDEX api_number_indx ON tx_well_details_ (api_number);
	CREATE INDEX county_no_indx ON tx_well_details_ (county_no);
	CREATE INDEX district_no_indx ON tx_well_details_ (district_no);
	CREATE INDEX lease_no_indx ON tx_well_details_ (lease_no);
	CREATE INDEX lease_prod_id_indx ON tx_well_details_ (lease_prod_id);
	CREATE INDEX lease_id_indx ON tx_well_details_ (lease_id);
	CREATE INDEX lease_well_district_indx ON tx_well_details_ (lease_no, well_no, district_no);
	CREATE INDEX lease_well_district_og_code_county_indx ON tx_well_details_ (lease_no, well_no, district_no, commodity, county_no);
	CREATE INDEX lease_well_district_og_code_indx ON tx_well_details_ (lease_no, well_no, district_no, commodity);
	CREATE INDEX commodity_indx ON tx_well_details_ (commodity);
	CREATE INDEX tx_well_id_indx ON tx_well_details_ (tx_well_id);
	CREATE INDEX well_no_indx ON tx_well_details_ (well_no);
	CREATE INDEX process_code_indx ON tx_well_details_ (process_code);

	INSERT INTO tx_well_details_ (tx_well_id) 
	  (SELECT DISTINCT tx_well_id FROM tx_well_details WHERE tx_well_id IS NOT NULL AND LEN(tx_well_id)=14);

	UPDATE tx_well_details_ SET well_id=b.WellID FROM tx_well_details_ a, US_Wells.dbo.tblUSWell_Details b WHERE a.tx_well_id=b.API_14;
	UPDATE tx_well_details_ SET well_id=(90000000+id) WHERE ISNULL(well_id,0)=0;
	UPDATE US_Wells.dbo.tblUSWell_Parameters SET WellID=b.well_id FROM US_Wells.dbo.tblUSWell_Parameters a, tx_well_details_ b WHERE a.API_Number=b.tx_well_id;
	UPDATE US_Wells.dbo.tblUSWell_Production SET WellID=b.well_id FROM US_Wells.dbo.tblUSWell_Production a, tx_well_details_ b WHERE a.API_Number=b.tx_well_id;
	UPDATE US_Wells.dbo.tblUSWell_Production_Forecast SET WellID=b.well_id FROM US_Wells.dbo.tblUSWell_Production_Forecast a, tx_well_details_ b WHERE a.API_Number=b.tx_well_id;
	UPDATE US_Wells.dbo.tblUSWell_Economics_Forecast SET WellID=b.well_id FROM US_Wells.dbo.tblUSWell_Economics_Forecast a, tx_well_details_ b WHERE a.API_Number=b.tx_well_id;
		"""
	if debug: print 'sql_create: \n{}'.format(sql_create)
	curr.execute(sql_create)
	gd.commit(curr)

	sql_update = \
		"""
		UPDATE US_Wells_Texas.dbo.tx_well_details_ SET {0}=b.{0}
		  FROM US_Wells_Texas.dbo.tx_well_details_ a, US_Wells_Texas.dbo.tx_well_details b 
		  WHERE a.well_id=b.well_id AND a.tx_well_id=b.tx_well_id AND b.{0} IS NOT NULL;
		"""
	for col_name in col_names:
		print col_names.index(col_name), sql_update.format(col_name)
		if debug: 'update: \n{}'
		curr.execute(sql_update.format(col_name))
		gd.commit(curr)
	curr.close()
	conn.close()
	end_time = gd.get_datetime()
	print 'end: {}'.format(end_time)
	print 'total time: {}'.format(gd.elapsed_time(start_time, end_time))


if __name__ == '__main__':
	main()

