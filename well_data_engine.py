import os

import globaldata as gd
import well_forecast as forecast
from vertical_well_cost import update_vertical_well_costs as update_vert_well_costs

# import ftputil

'''
Forecast Well Codes

0 - no recent production and non-producing status
1 - recent production and producing status vertical wells with lateral length value
2 - recent production and non-producing status
3 - no recent production and producing status
4 - recent production and producing status vertical wells without true vertical depth value
5 - recent production and producing status horizontal wells without lateral length value
6 - recent production and producing status vertical wells with true vertical depth
9 - recent production and producing status new vertical wells with lateral length value
'''

WELL_ENGINE_STAGES = {
	1: 'Engine Data Import',
	2: 'Engine Database Update',
	3: 'Engine Pre-processing',
	4: 'Engine Forecast',
	5: 'Engine Post-processing',
	6: 'Engine Data Export'
}

WELL_ENGINE_PROCESS_CODES = {
	1.1: 'Import well details data',
	1.2: 'Import well production data',
	2.1: 'Update US_Wells.dbo.tblUSWell_Details',
	2.2: 'Update US_Wells.dbo.tblUSWell_Production',
	2.3: 'Update US_Wells.dbo.tblUSWell_Production_Forecast',
	2.4: 'Update US_Wells.dbo.tblUSWell_Parameters',
	2.5: 'Update US_Wells.dbo.tblUSWell_Assumptions',
	3.1: 'Update pre-engine well parameters',
	3.2: 'Choose well assumptions',
	3.3: 'Estimate length parameters',
	3.4: 'Update vertical well costs',
	4.1: 'Forecast well production',
	4.2: 'Forecast well economics',
	5.1: 'Update post-engine well parameters',
	5.2: 'Save original US_Wells.dbo.USWell_Parameters',
	5.3: 'Remove outliers from US_Wells.dbo.USWell_Parameters',
	5.4: 'Update US_Wells.dbo.tblUSWell_Last_Prod_Data',
	5.5: 'Update US_Wells.dbo.Well_Error_Log',
	6.1: 'Export well parameters data',
	6.2: 'Export well economics forecast',
	6.3: 'Export well production forecast',
	6.4: 'Export well error log'
}

MONTH_NAMES = {
	1 : 'Jan',
	2 : 'Feb',
	3 : 'Mar',
	4 : 'Apr',
	5 : 'May',
	6 : 'Jun',
	7 : 'Jul',
	8 : 'Aug',
	9 : 'Sep',
	10: 'Oct',
	11: 'Nov',
	12: 'Dec'
}

ASSUMPTION_PARAMS = {
	'Vertical'  : {
		'Completion cost breakdown': 'Vert_Completion_Cost_pct',
		'Drilling cost breakdown'  : 'Vert_Drilling_Cost_pct',
		'Drilling cost premium'    : 'Vert_Drilling_Cost_Premium_pct',
		'Facilities cost breakdown': 'Vert_Facilities_Cost_pct',
		'Well Cost'                : 'Vert_Well_Cost_usd_ft'
	},
	
	'Horizontal': {
		'Drilling cost breakdown': 'Horiz_Drilling_Cost_pct',
		'Well Cost'              : 'Horiz_Well_Cost_usd_ft'
	}
}

WELL_ASSUM_DATA = [
	('Vertical', ['Well Cost',
				  'Facilities cost breakdown',
				  'Drilling cost premium',
				  'Completion cost breakdown',
				  'Drilling cost breakdown']),
	
	('Horizontal', ['Well Cost',
					'Drilling cost breakdown'])
]


def get_well_assumption(curr, operator, resource_play, state_name, well_direction, param_list=[], debug=False):
	resource_play_str = "''"
	operator_str = "''"
	
	param_values = []
	
	if operator:
		operator_str = operator
	
	if resource_play:
		if ';' in resource_play:
			resource_plays = ["'{}'".format(play.strip()) for play in resource_play.split(';')]
			resource_play_str = ', '.join(resource_plays)
		else:
			resource_play_str = "'{}'".format(resource_play)
	
	for param_name in param_list:
		if debug: print '(get_well_assumption()) -- param_list: {}'.format(param_list)
		param_choice = 0
		sql_where = "Well_Direction='{}' AND (Operator='{}' OR Operator IS NULL) AND (Resource_Play IN ({}) OR Resource_Play IS NULL) AND (State_Name='{}' OR State_Name IS NULL) AND Param_Name='{}' AND ISNULL(Param_Value,0) > 0 "
		if param_name.lower() == 'well cost' and well_direction.lower() == 'vertical':
			sql_where += "AND ISNULL(Well_Cost_usd_ft,0) > 0 "
		sql_where += "ORDER BY Well_Direction DESC, State_Name DESC, Resource_Play DESC, Operator DESC"
		param_data = gd.get_data \
			('TOP 1 Param_Value, Well_Cost_usd_ft, Well_Direction, State_Name, Resource_Play, Operator',
			 'tblUSWell_Assumptions', database='US_Wells', server='sql_server', cursor=curr, datatype='plural',
			 single_value=True,
			 sql_where=sql_where.format(well_direction, operator_str, resource_play_str, state_name, param_name),
			 debug=debug, us_wells=True)
		if debug: print '(get_well_assumption()) -- param_data: {}'.format(param_data)
		if param_data is not None:
			param_value, well_cost_usd_ft = param_data[:2]
			if param_name.lower == 'well cost':
				if (well_direction.lower() == 'horizontal') and param_value:
					param_choice = param_value
				elif (well_direction.lower() == 'vertical') and well_cost_usd_ft:
					param_choice = well_cost_usd_ft
			elif param_value:
				param_choice = param_value
		param_values.append(param_choice)
		if debug: print '(get_well_assumption()) -- param_name: {} -- param_choice: {} -- param_values: {}'.format \
			(param_name, param_choice, param_values)
	
	if debug: print '(get_well_assumption()) -- ret_val: {}'.format(param_values)
	return param_values


def update_well_engine_log(debug=False):
	'''Update US_Wells.dbo.Well_Engine_Process_Log at the start and completion of each engine phase'''
	pass


def read_state_list():
	run_state_list = []
	with open(gd.DATA_DIR + "well_engine_config\\state_list.csv") as state_list_file:
		for fileline in state_list_file.readlines()[1:]:
			state_id, state_abbrv, state_name, run_state = fileline.split(',')
			if int(run_state.strip()) == 1:
				run_state_list.append(int(state_id.strip()))
	return run_state_list


def read_well_list():
	run_well_list = []
	with open(gd.DATA_DIR + "well_engine_config\\well_id_list.csv") as well_list_file:
		for fileline in well_list_file.readlines():
			if len(fileline.strip()) > 0:
				well_id = int(fileline.strip())
				run_well_list.append(well_id)
	return run_well_list


def get_well_list_data(forecast_codes=[], debug=False):
	assert len(forecast_codes) >= 1
	forecast_code_str = ','.join([str(forecast_code) for forecast_code in forecast_codes])
	well_id_list = gd.get_data('API_Number, WellID, Well_ParametersID', 'dbo.tblUSWell_Parameters',
							   sql_where="Forecast_Well IN ({}) ORDER BY API_Number".format(forecast_code_str),
							   server='sql_server', database='US_Wells', datatype='plural', debug=debug, us_wells=True)
	forecast_count = int(len(well_id_list) / 5)
	if debug: print well_id_list, forecast_count
	return well_id_list, forecast_count


def import_well_data(curr, source_table, target_table, sql_query, extract_data, import_data, clear_data=False, debug=False):
	target_server = gd.SERVER_NAME
	outfile_name = "{}{}_{}.txt".format(gd.DATABASE_DIR, source_table, gd.get_run_id())
	extract_txt_cmd = 'bcp "{}" queryout {} -c -S 63.33.172.39 -U uswellsdata -P uswellsdata'
	import_txt_cmd = 'bcp {} in {} -c -S {} -T'
	
	if clear_data:
		print 'Clearing data from local {} ...'.format(target_table)
		curr.execute("TRUNCATE TABLE {}".format(target_table))
		gd.commit(curr)
	
	if extract_data:
		print 'Extracting data from external {} table to txt file {} ...'.format(source_table, outfile_name)
		if debug:
			print extract_txt_cmd.format(sql_query, outfile_name)
		os.system(extract_txt_cmd.format(sql_query, outfile_name))
	
	if import_data:
		print 'Importing data from txt file {} to local {} table ...'.format(outfile_name, target_table)
		if debug:
			print import_txt_cmd.format(target_table, outfile_name, target_server)
		os.system(import_txt_cmd.format(target_table, outfile_name, target_server))


def export_well_data(source_table, target_table, sql_query, clear_data=False, debug=False):
	source_server = gd.SERVER_NAME
	outfile_name = "{}{}_{}.txt".format(gd.DATABASE_DIR, source_table, gd.get_run_id())
	extract_txt_cmd = 'bcp "{}" queryout "{}" -S {} -T -c'
	import_txt_cmd = 'bcp {} in "{}" -S 63.33.172.39 -U uswellsdata -P uswellsdata -c'
	if clear_data:
		conn = get_connection(server='sql_server', server_name='63.33.172.39', database='US_Wells_DataExtract',
							  username='uswellsdata', password='uswellsdata', external=True)
		curr = conn.cursor()
		print 'Clearing data from external {} table ...'.format(target_table)
		curr.execute("TRUNCATE TABLE {}".format(target_table))
		gd.commit(curr)
		curr.close()
		conn.close()
	
	print 'Extracting data from local {} table to txt file {} ...'.format(source_table, outfile_name)
	if debug:
		print extract_txt_cmd.format(sql_query, outfile_name, source_server)
	os.system(extract_txt_cmd.format(sql_query, outfile_name, source_server))
	
	print 'Importing data from txt file {} to external {} table ...'.format(outfile_name, target_table)
	if debug:
		print import_txt_cmd.format(target_table, outfile_name)
	os.system(import_txt_cmd.format(target_table, outfile_name))


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Stage 1 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 1.1 Import well details data

def import_well_details(curr, extract, import_data, update, debug=False):
	'''Import well data from US_Wells.dbo.tblUSWell_Details on external server
       to US_Wells.dbo.tblUSWell_Details on local server
       '''
	# if extract or import_data:
	# 	sql_query = \
	# 		"SELECT REPLACE([WellID],'	',''),REPLACE([API_Number],'	',''),REPLACE([Well_Name],'	',''),REPLACE([Permit_Number],'	','')," \
	# 		"REPLACE([Operator],'	',''),REPLACE([County],'	',''),REPLACE([Region],'	',''),REPLACE([Country],'	',''),REPLACE([State],'	','')," \
	# 		"REPLACE([Field_Name],'	',''),REPLACE([Lease_Name],'	',''),REPLACE([Well_Pad],'	',''),REPLACE([Target_Formation],'	','')," \
	# 		"REPLACE([Producing_Formation],'	',''),REPLACE([Shale],'	',''),REPLACE([Basin],'	',''),REPLACE([Well_Terrain],'	','')," \
	# 		"REPLACE([Top_Hole_Latitude],'	',''),REPLACE([Top_Hole_Longitude],'	',''),REPLACE([Bottom_Hole_Latitude],'	','')," \
	# 		"REPLACE([Bottom_Hole_Longitude],'	',''),REPLACE([Well_Status],'	',''),REPLACE([Well_Type],'	',''),REPLACE([Well_Direction],'	','')," \
	# 		"REPLACE([Well_Classification],'	',''),REPLACE([Resource_Type],'	',''),REPLACE([Commodity],'	',''),REPLACE([Measured_Depth_FT],'	','')," \
	# 		"REPLACE([True_Vertical_Depth_FT],'	',''),REPLACE([Discovery_Date],'	',''),REPLACE([Spud_date],'	',''),REPLACE([Completion_start_date],'	','')," \
	# 		"REPLACE([First_Production_Date],'	',''),REPLACE([First_Production_Rate],'	',''),REPLACE([Peak_Production_Date],'	','')," \
	# 		"REPLACE([Peak_Production_Rate],'	',''),REPLACE([Last_Historical_Production_date],'	',''),REPLACE([Top_Perforation],'	','')," \
	# 		"REPLACE([Bottom_Perforation],'	',''),REPLACE([Notes],'	',''),REPLACE([Source],'	',''),REPLACE([CreatedBy],'	',''),REPLACE([CreatedOn],'	','')," \
	# 		"REPLACE([ModifiedBy],'	',''),REPLACE([ModifiedOn],'	',''),REPLACE([pkgId],'	',''),REPLACE([Last_Production_Date],'	','')," \
	# 		"REPLACE([Last_Production_Rate],'	',''),REPLACE([ParentOperator],'	',''),REPLACE([Lease_Number],'	',''),REPLACE([operatorlegalname],'	','')," \
	# 		"REPLACE([Lateral_Length_Ft],'	',''),REPLACE([Reported_API_Number],'	',''),REPLACE([Well_Status_Details],'	',''),REPLACE([tx_well_id],'	','')," \
	# 		"REPLACE([API_14],'	','') FROM US_Wells.dbo.tblUSWell_Details"
	# 	source_table = "US_Wells.dbo.tblUSWell_Details"
	# 	target_table = "US_Wells.dbo.tblUSWell_Details_temp"
	# 	import_well_data(curr, source_table, target_table, sql_query, extract_data=extract, import_data=import_data, clear_data=True, debug=debug)
	#
	# well_details_count = gd.get_data('COUNT(*)', 'dbo.tblUSWell_Details', cursor=curr, datatype='int', single_value=True)
	# well_details_temp_count = gd.get_data('COUNT(*)', 'dbo.tblUSWell_Details_temp', cursor=curr, datatype='int', single_value=True)
	#
	# # Ensure updated table is at least as large as original table
	# assert well_details_count <= well_details_temp_count
	#
	# if update:
	# 	print 'Clearing data from US_Wells.dbo.tblUSWell_Details ...'
	# 	curr.execute('TRUNCATE TABLE US_Wells.dbo.tblUSWell_Details')
	# 	gd.commit(curr)
	#
	# 	print 'Updating US_Wells.dbo.tblUSWell_Details with latest data ...'
	# 	sql_insert = \
	# 		"""
    #     SET IDENTITY_INSERT US_Wells.dbo.tblUSWell_Details ON;
    #     INSERT INTO US_Wells.dbo.tblUSWell_Details ([WellID], [API_Number], [Well_Name], [Permit_Number], [Operator], [County], [Region], [Country], [State], [Field_Name], [Lease_Name], [Well_Pad], [Target_Formation], [Producing_Formation], [Shale], [Basin], [Well_Terrain], [Top_Hole_Latitude], [Top_Hole_Longitude], [Bottom_Hole_Latitude], [Bottom_Hole_Longitude], [Well_Status], [Well_Type], [Well_Direction], [Well_Classification], [Resource_Type], [Commodity], [Measured_Depth_FT], [True_Vertical_Depth_FT], [Discovery_Date], [Spud_date], [Completion_start_date], [First_Production_Date], [First_Production_Rate], [Peak_Production_Date], [Peak_Production_Rate], [Last_Historical_Production_date], [Top_Perforation], [Bottom_Perforation], [Notes], [Source], [CreatedBy], [CreatedOn], [ModifiedBy], [ModifiedOn], [pkgId], [Last_Production_Date], [Last_Production_Rate], [ParentOperator], [Lease_Number], [operatorlegalname], [Lateral_Length_Ft], [Reported_API_Number], [Well_Status_Details], [tx_well_id], [API_14])
    #      (SELECT [WellID], [API_Number], [Well_Name], [Permit_Number], [Operator], [County], [Region], [Country], [State], [Field_Name], [Lease_Name], [Well_Pad], [Target_Formation], [Producing_Formation], [Shale], [Basin], [Well_Terrain], [Top_Hole_Latitude], [Top_Hole_Longitude], [Bottom_Hole_Latitude], [Bottom_Hole_Longitude], [Well_Status], [Well_Type], [Well_Direction], [Well_Classification], [Resource_Type], [Commodity], [Measured_Depth_FT], [True_Vertical_Depth_FT], [Discovery_Date], [Spud_date], [Completion_start_date], [First_Production_Date], [First_Production_Rate], [Peak_Production_Date], [Peak_Production_Rate], [Last_Historical_Production_date], [Top_Perforation], [Bottom_Perforation], [Notes], [Source], [CreatedBy], [CreatedOn], [ModifiedBy], [ModifiedOn], [pkgId], [Last_Production_Date], [Last_Production_Rate], [ParentOperator], [Lease_Number], [operatorlegalname], [Lateral_Length_Ft], [Reported_API_Number], [Well_Status_Details], [tx_well_id], [API_14] FROM [US_Wells].[dbo].[tblUSWell_Details_temp]);
    #     SET IDENTITY_INSERT US_Wells.dbo.tblUSWell_Details OFF;
    #     """
	# 	curr.execute(sql_insert)
	# 	gd.commit(curr)


# 1.2 Import well production data

def import_well_production(curr, debug=False):
	'''Import production data from US_Wells.dbo.tblUSWell_Production_Historic_New on external server
       to US_Wells.dbo.tblUSWell_Production_Historical_Update on local server
       '''
	# max_pkg_id = gd.get_data('MAX(pkgId)', 'tblUSWell_Production_Historical', cursor=curr, server='sql_server',
	# 						 database='US_Wells', datatype='int', single_value=True)
	# sql_query = \
	# 	"""SELECT DISTINCT WellID, API_Number, ProductionDate, Production_Year, Production_Month,
    #      ISNULL(Oil_bbl,0.0) AS Oil_bbl, ISNULL(Gas_mcf,0.0) AS Gas_mcf, ISNULL(Condensate_bbl,0.0) AS Condensate_bbl,
	#      ISNULL(NGL_bbl,0.0) AS NGL_bbl, ISNULL(Water_bbl,0.0) AS Water_bbl, ModifiedOn, Pkgid FROM US_Wells.dbo.tblUSWell_Production_Historic_New WHERE PkgId > {}
	# 	"""
	# source_table = "US_Wells.dbo.tblUSWell_Production_Historic_New"
	# target_table = "US_Wells.dbo.tblUSWell_Production_Historical_Update_temp"
	# import_well_data(curr, source_table, target_table, sql_query.format(max_pkg_id), clear_data=True, debug=debug)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Stage 2 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 2.1 Update US_Wells.dbo.tblmaster_WellID_API_Number

def update_well_id_api_table(curr, debug=False):
	print '\tUpdating US_Wells.dbo.tblmaster_WellID_API_Number table ...'
	"""
    UPDATE tblmaster_WellID_API_Number SET process_code=0;
	
	UPDATE tblmaster_WellID_API_Number
		SET Well_ParametersID=b.Well_ParametersID, process_code=1
		FROM tblmaster_WellID_API_Number a, tblUSWell_Parameters b
		WHERE a.WellID=b.WellID AND a.API_Number=b.API_Number;
	
	UPDATE tblmaster_WellID_API_Number
		SET Well_ParametersID=b.Well_ParametersID, process_code=2, API_Number=b.API_Number
		FROM tblmaster_WellID_API_Number a, tblUSWell_Parameters b
		WHERE a.WellID=b.WellID AND a.API_Number IS NULL AND a.process_code=0 AND b.State_Name!='Texas';
	
	UPDATE tblmaster_WellID_API_Number
		SET Well_ParametersID=b.Well_ParametersID, process_code=3
		FROM tblmaster_WellID_API_Number a, tblUSWell_Parameters b
		WHERE a.WellID=b.WellID AND a.API_Number!=b.API_Number AND a.process_code=0 AND b.State_Name!='Texas';
	
	UPDATE tblmaster_WellID_API_Number
		SET Well_ParametersID=b.Well_ParametersID, process_code=4
		FROM tblmaster_WellID_API_Number a, tblUSWell_Parameters b
		WHERE a.WellID!=b.WellID AND a.API_Number=b.API_Number AND a.process_code=0 AND b.State_Name!='Texas';
	
	UPDATE tblmaster_WellID_API_Number
		SET process_code=10
		WHERE WellID IN (SELECT DISTINCT WellID FROM tblUSWell_Details WHERE [State]='Texas')
	
	UPDATE tblUSWell_Parameters
	  SET API_Number=b.API_Number
	  FROM tblUSWell_Parameters a, tblmaster_WellID_API_Number b
	  WHERE b.process_code=3 AND a.WellID=b.WellID;
	
	UPDATE tblUSWell_Parameters
	  SET WellID=b.WellID
	  FROM tblUSWell_Parameters a, tblmaster_WellID_API_Number b
	  WHERE b.process_code=4 AND a.API_Number=b.API_Number;
    """
	
	well_id_table_updates = [
		"UPDATE US_Wells.dbo.tblUSWell_Details \
			SET API_14=b.API_Number \
			FROM tblUSWell_Details a, tblUSWell_Parameters b \
			WHERE a.WellID=b.WellID AND a.API_14!=b.API_Number AND b.API_Number IS NOT NULL;",
		
		"UPDATE US_Wells.dbo.tblUSWell_Details \
			SET API_14=CONCAT(API_Number,'0000') \
			WHERE API_14 IS NULL AND LEN(API_Number)=10 AND [State]!='Texas';",
		
		"TRUNCATE TABLE tblmaster_WellID_API_Number;",
		
		"INSERT INTO tblmaster_WellID_API_Number (Well_ParametersID, WellID, API_Number, process_code) \
			(SELECT DISTINCT 0, WellID, API_14, 0 FROM tblUSWell_Details);",
		
		"UPDATE tblmaster_WellID_API_Number \
			SET Well_ParametersID=b.Well_ParametersID, process_code=1 \
			FROM tblmaster_WellID_API_Number a, tblUSWell_Parameters b \
			WHERE a.WellID=b.WellID AND a.API_Number=b.API_Number;",
		
		"UPDATE tblmaster_WellID_API_Number \
			SET Well_ParametersID=b.Well_ParametersID, process_code=2, API_Number=b.API_Number \
			FROM tblmaster_WellID_API_Number a, tblUSWell_Parameters b \
			WHERE a.WellID=b.WellID AND a.API_Number IS NULL AND a.process_code=0 AND b.State_Name!='Texas';",
		
		"UPDATE tblmaster_WellID_API_Number \
			SET Well_ParametersID=b.Well_ParametersID, process_code=3\
			FROM tblmaster_WellID_API_Number a, tblUSWell_Parameters b \
			WHERE a.WellID=b.WellID AND a.API_Number!=b.API_Number AND a.process_code=0 AND b.State_Name!='Texas';",
		
		"UPDATE tblmaster_WellID_API_Number \
			SET Well_ParametersID=b.Well_ParametersID, process_code=4\
			FROM tblmaster_WellID_API_Number a, tblUSWell_Parameters b \
			WHERE a.WellID!=b.WellID AND a.API_Number=b.API_Number AND a.process_code=0 AND b.State_Name!='Texas';",
		
		"UPDATE tblmaster_WellID_API_Number \
			SET process_code=11 \
			WHERE WellID IN (SELECT DISTINCT WellID FROM tblUSWell_Details WHERE [State]='Texas');",
		
		"UPDATE tblmaster_WellID_API_Number \
			SET process_code=21 \
			WHERE WellID IN (SELECT DISTINCT WellID FROM tblmasterAPIWellID);",
		
		"INSERT INTO tblmasterAPIWellID (WellID, API_Number) \
			(SELECT DISTINCT WellID, API_Number FROM tblmaster_WellID_API_Number WHERE process_code=0);"
	]
	for sql_update in well_id_table_updates:
		if debug:
			print sql_update
		curr.execute(sql_update)
		gd.commit(curr)


# 2.2 Update US_Wells.dbo.tblUSWell_Production

# def update_production_tables_(curr, insert=False, update=False, debug=False):
# 	sql_update_hist = \
# 		"""
#     UPDATE tblUSWell_Production_Historical SET LastPkgId=b.PkgId
#       FROM tblUSWell_Production_Historical a, tblUSWell_Production_Historical_Update b
#       WHERE a.WellProdID=CONCAT(b.WellID,'-',b.Production_Year) AND a.Production_Month=b.Production_Month;
#
#     DELETE FROM tblUSWell_Production_Historical WHERE PkgId!=LastPkgId;
#     """
# 	sql_insert_1 = \
# 		"""
#     INSERT INTO US_Wells.dbo.tblUSWell_Production_Historical (WellID, API_Number, ProductionDate, Production_Year, Production_Month, Oil_bbl, Gas_mcf, Condensate_bbl, NGL_bbl, Water_bbl, Source, CreatedBy, CreatedOn, ModifiedOn, Pkgid, WellProdID, WellProdDateID)
#       (SELECT DISTINCT WellID, API_Number, ProductionDate, Production_Year, Production_Month, Oil_bbl, Gas_mcf, Condensate_bbl, NGL_bbl, Water_bbl, Source, CreatedBy, CreatedOn, ModifiedOn, Pkgid, WellProdID, WellProdDateID
#        FROM US_Wells.dbo.tblUSWell_Production_Historical_Update);
#
#     TRUNCATE TABLE US_Wells.dbo.tblUSWell_Production_Historical_Update;
#
#     UPDATE US_Wells.dbo.tblUSWell_Production_Historical SET WellProdID=CONCAT(WellID,'-',Production_Year) WHERE ISNULL(WellID,0) > 0 AND WellProdID IS NULL;
#     """
# 	sql_insert_2 = \
# 	"""
#     INSERT INTO US_Wells.dbo.tblUSWell_Production (WellID, API_Number, [Period], WellProdID) (SELECT DISTINCT WellID, API_Number, Production_Year, WellProdID FROM US_Wells.dbo.tblUSWell_Production_Historical);
#
#     UPDATE US_Wells.dbo.tblUSWell_Production SET WellProdID=CONCAT(WellID,'-',[Period]) WHERE ISNULL(WellID,0) > 0 AND WellProdID IS NULL;
#     """
# 	sql_update = \
# 		'''
#     UPDATE US_Wells.dbo.tblUSWell_Production
#       SET Gas_{0}_MCF=ISNULL(b.Gas_mcf,0),
#           Oil_{0}_BBL=ISNULL(b.Oil_bbl,0),
#           NGL_{0}_BBL=ISNULL(b.NGL_bbl,0),
#           Condensate_{0}_BBL=ISNULL(b.Condensate_bbl,0),
#           Water_{0}_BBL=ISNULL(b.Water_bbl,0)
#       FROM US_Wells.dbo.tblUSWell_Production a, US_Wells.dbo.tblUSWell_Production_Historical b
#       WHERE a.WellProdID=b.WellProdID AND a.API_Number=b.API_Number AND b.Production_Month={1};
#     '''
# 	sql_update_pkgid_data = \
# 		'''
#     UPDATE US_Wells.dbo.tblUSWell_Production
#       SET PkgId=b.Max_PkgId,
#           WellProductionID=b.Max_HistoricID,
#           Source='Historical',
#           CreatedBy='Engine',
#           CreatedOn='{}'
#       FROM US_Wells.dbo.tblUSWell_Production a,
#            (SELECT DISTINCT WellID, Production_Year, MAX(PkgId) AS Max_PkgId, MAX(WellProductionHistoricID) AS Max_HistoricID FROM US_Wells.dbo.tblUSWell_Production_Historical GROUP BY WellID, Production_Year) b
#       WHERE a.WellID=b.WellID AND a.[Period]=b.Production_Year;
#     '''
# 	sql_update_api = \
# 		'''
#     UPDATE US_Wells.dbo.tblUSWell_Production
#       SET API_14=b.API_14
#       FROM US_Wells.dbo.tblUSWell_Production a, US_Wells.dbo.tblUSWell_Details b
#       WHERE a.WellID=b.WellID AND a.API_14 IS NULL;
#
#     UPDATE US_Wells.dbo.tblUSWell_Production
#       SET API_14=API_Number
#       WHERE API_14 IS NULL AND LEN(API_Number)=14;
#     '''
# 	sql_update_prod_totals = \
# 		'''
#     UPDATE US_Wells.dbo.tblUSWell_Production
#       SET Gas_TOTAL_mcf=ROUND(ISNULL(Gas_Jan_mcf,0) + ISNULL(Gas_Feb_mcf,0) + ISNULL(Gas_Mar_mcf,0) + ISNULL(Gas_Apr_mcf,0) + ISNULL(Gas_May_mcf,0) + ISNULL(Gas_Jun_mcf,0) + ISNULL(Gas_Jul_mcf,0) + ISNULL(Gas_Aug_mcf,0) + ISNULL(Gas_Sep_mcf,0) + ISNULL(Gas_Oct_mcf,0) + ISNULL(Gas_Nov_mcf,0) + ISNULL(Gas_Dec_mcf,0),2),
#           Oil_TOTAL_bbl=ROUND(ISNULL(Oil_Jan_bbl,0) + ISNULL(Oil_Feb_bbl,0) + ISNULL(Oil_Mar_bbl,0) + ISNULL(Oil_Apr_bbl,0) + ISNULL(Oil_May_bbl,0) + ISNULL(Oil_Jun_bbl,0) + ISNULL(Oil_Jul_bbl,0) + ISNULL(Oil_Aug_bbl,0) + ISNULL(Oil_Sep_bbl,0) + ISNULL(Oil_Oct_bbl,0) + ISNULL(Oil_Nov_bbl,0) + ISNULL(Oil_Dec_bbl,0),2),
#           Water_TOTAL_bbl=ROUND(ISNULL(Water_Jan_bbl,0) + ISNULL(Water_Feb_bbl,0) + ISNULL(Water_Mar_bbl,0) + ISNULL(Water_Apr_bbl,0) + ISNULL(Water_May_bbl,0) + ISNULL(Water_Jun_bbl,0) + ISNULL(Water_Jul_bbl,0) + ISNULL(Water_Aug_bbl,0) + ISNULL(Water_Sep_bbl,0) + ISNULL(Water_Oct_bbl,0) + ISNULL(Water_Nov_bbl,0),0) + ISNULL(Water_Dec_bbl,2),
#           NGL_TOTAL_bbl=ROUND(ISNULL(NGL_Jan_bbl,0) + ISNULL(NGL_Feb_bbl,0) + ISNULL(NGL_Mar_bbl,0) + ISNULL(NGL_Apr_bbl,0) + ISNULL(NGL_May_bbl,0) + ISNULL(NGL_Jun_bbl,0) + ISNULL(NGL_Jul_bbl,0) + ISNULL(NGL_Aug_bbl,0) + ISNULL(NGL_Sep_bbl,0) + ISNULL(NGL_Oct_bbl,0) + ISNULL(NGL_Nov_bbl,0) + ISNULL(NGL_Dec_bbl,0),2),
#           Condensate_TOTAL_bbl=ROUND(ISNULL(Condensate_Jan_bbl,0) + ISNULL(Condensate_Feb_bbl,0) + ISNULL(Condensate_Mar_bbl,0) + ISNULL(Condensate_Apr_bbl,0) + ISNULL(Condensate_May_bbl,0) + ISNULL(Condensate_Jun_bbl,0) + ISNULL(Condensate_Jul_bbl,0) + ISNULL(Condensate_Aug_bbl,0) + ISNULL(Condensate_Sep_bbl,0) + ISNULL(Condensate_Oct_bbl,0) + ISNULL(Condensate_Nov_bbl,0) + ISNULL(Condensate_Dec_bbl,0),2);
#     '''
#
# 	if insert:
# 		print '\t{} Updating Historical Monthly Production Data ...'.format(gd.get_datetime())
# 		if debug:
# 			print sql_update_hist
# 		curr.execute(sql_update_hist)
# 		gd.commit(curr)
# 		print '\t{} Historical Monthly Production Data Update Complete\n'.format(gd.get_datetime())
#
# 		# ---------------------------------------------------------------------------------------------------------------------------
#
# 		print '\t{} Inserting Monthly Production Data into US_Wells.dbo.tblUSWell_Production_Historical ...'.format(
# 			gd.get_datetime())
# 		if debug:
# 			print sql_insert_1
# 		curr.execute(sql_insert_1)
# 		gd.commit(curr)
# 		print '\t{} Monthly Production Data Insert Complete\n'.format(gd.get_datetime())
#
# 		print '\t{} Inserting Annual Production Data into US_Wells.dbo.tblUSWell_Production ...'.format(
# 			gd.get_datetime())
# 		if debug:
# 			print sql_insert_2
# 		curr.execute(sql_insert_2)
# 		gd.commit(curr)
# 		print '\t{} Annual Production Data Insert Complete\n'.format(gd.get_datetime())
#
# 	if update:
# 		for prod_month in sorted(MONTH_NAMES.keys()):
# 			print '\t{} Updating Production Data for {} ...'.format(gd.get_datetime(), MONTH_NAMES[prod_month])
# 			if debug:
# 				print sql_update.format(MONTH_NAMES[prod_month], prod_month)
# 			curr.execute(sql_update.format(MONTH_NAMES[prod_month], prod_month))
# 			gd.commit(curr)
# 			print '\t{} Production Data Update Complete for {}\n'.format(gd.get_datetime(), MONTH_NAMES[prod_month])
# 		# -------------------------------------------------------------------------------------------------------------------
# 		update_time = gd.get_datetime()
# 		print '\t{} Updating Production ID Data ...'.format(update_time)
# 		if debug:
# 			print sql_update_pkgid_data.format(update_time)
# 		curr.execute(sql_update_pkgid_data.format(update_time))
# 		gd.commit(curr)
# 		print '\t{} Production ID Data Update Complete\n'.format(gd.get_datetime())
# 		# -------------------------------------------------------------------------------------------------------------------
# 		print '\t{} Updating API 14 Data ...'.format(gd.get_datetime())
# 		if debug:
# 			print sql_update_api
# 		curr.execute(sql_update_api)
# 		gd.commit(curr)
# 		print '\t{} API 14 Data Update Complete\n'.format(gd.get_datetime())
# 		# -------------------------------------------------------------------------------------------------------------------
# 		print '\t{} Updating Production Totals ...'.format(gd.get_datetime())
# 		if debug:
# 			print sql_update_prod_totals
# 		curr.execute(sql_update_prod_totals)
# 		gd.commit(curr)
# 		print '\t{} Production Totals Update Complete\n'.format(gd.get_datetime())


def update_production_tables(curr, insert=False, update=False, debug=False):
	sql_insert_1 = \
		"""
    	UPDATE US_Wells.dbo.tblUSWell_Production_Historical SET WellProdID=CONCAT(WellID,'-',Production_Year) WHERE ISNULL(WellID,0) > 0 AND WellProdID IS NULL;
    	"""
	
	sql_insert_2 = \
		"""
		UPDATE US_Wells.dbo.tblUSWell_Production SET WellProdID=CONCAT(WellID,'-',[Period]) WHERE ISNULL(WellID,0) > 0 AND WellProdID IS NULL;
		"""
	
	sql_insert_3 = \
		"""
		INSERT INTO US_Wells.dbo.tblUSWell_Production (WellID, API_Number, [Period], Source, CreatedBy, CreatedOn, WellProdID)
		  (SELECT DISTINCT WellID, API_Number, Production_Year, 'Historical', 'Engine', '{}', WellProdID
		     FROM US_Wells.dbo.tblUSWell_Production_Historical
		     WHERE NOT WellProdID IN (SELECT DISTINCT WellProdID FROM US_Wells.dbo.tblUSWell_Production)
		     AND NOT WellID IN (SELECT DISTINCT WellID FROM tblUSWell_Details WHERE [State]='Texas') GROUP BY WellProdID);
		"""
	sql_update = \
		'''
    UPDATE US_Wells.dbo.tblUSWell_Production
      SET Gas_{0}_MCF=IIF(ISNULL(a.Gas_{0}_mcf,0)=0, ISNULL(b.Gas_mcf, 0), a.Gas_{0}_mcf),
          Oil_{0}_BBL=IIF(ISNULL(a.Oil_{0}_bbl,0)=0, ISNULL(b.Oil_bbl, 0), a.Oil_{0}_bbl),
          NGL_{0}_BBL=IIF(ISNULL(a.NGL_{0}_bbl,0)=0, ISNULL(b.NGL_bbl, 0), a.NGL_{0}_bbl),
          Condensate_{0}_BBL=IIF(ISNULL(a.Condensate_{0}_bbl,0)=0, ISNULL(b.Condensate_bbl, 0), a.Condensate_{0}_bbl),
          Water_{0}_BBL=IIF(ISNULL(a.Water_{0}_bbl,0)=0, ISNULL(b.Water_bbl,0), a.Water_{0}_bbl)
      FROM US_Wells.dbo.tblUSWell_Production a,
           US_Wells.dbo.tblUSWell_Production_Historical b
      WHERE a.WellProdID=b.WellProdID AND a.WellID=b.WellID AND b.Production_Month={1};
    '''
	# sql_update_pkgid_data = \
	# 	'''
    # UPDATE US_Wells.dbo.tblUSWell_Production
    #   SET PkgId=b.Max_PkgId,
    #       WellProductionID=b.Max_HistoricID,
    #       Source='Historical',
    #       CreatedBy='Engine',
    #       CreatedOn='{}'
    #   FROM US_Wells.dbo.tblUSWell_Production a,
    #        (SELECT DISTINCT WellID, Production_Year, MAX(PkgId) AS Max_PkgId, MAX(WellProductionHistoricID) AS Max_HistoricID FROM US_Wells.dbo.tblUSWell_Production_Historical GROUP BY WellID, Production_Year) b
    #   WHERE a.WellID=b.WellID AND a.[Period]=b.Production_Year;
    # '''
	sql_update_api = \
		'''
    UPDATE US_Wells.dbo.tblUSWell_Production
      SET API_14=b.API_14
      FROM US_Wells.dbo.tblUSWell_Production a, US_Wells.dbo.tblUSWell_Details b
      WHERE a.WellID=b.WellID AND a.API_14 IS NULL;

    UPDATE US_Wells.dbo.tblUSWell_Production
      SET API_14=API_Number
      WHERE API_14 IS NULL AND LEN(API_Number)=14;
    '''
	sql_update_prod_totals = \
		'''
    UPDATE US_Wells.dbo.tblUSWell_Production
      SET Gas_TOTAL_mcf=ROUND(ISNULL(Gas_Jan_mcf,0) + ISNULL(Gas_Feb_mcf,0) + ISNULL(Gas_Mar_mcf,0) + ISNULL(Gas_Apr_mcf,0) + ISNULL(Gas_May_mcf,0) + ISNULL(Gas_Jun_mcf,0) + ISNULL(Gas_Jul_mcf,0) + ISNULL(Gas_Aug_mcf,0) + ISNULL(Gas_Sep_mcf,0) + ISNULL(Gas_Oct_mcf,0) + ISNULL(Gas_Nov_mcf,0) + ISNULL(Gas_Dec_mcf,0),2),
          Oil_TOTAL_bbl=ROUND(ISNULL(Oil_Jan_bbl,0) + ISNULL(Oil_Feb_bbl,0) + ISNULL(Oil_Mar_bbl,0) + ISNULL(Oil_Apr_bbl,0) + ISNULL(Oil_May_bbl,0) + ISNULL(Oil_Jun_bbl,0) + ISNULL(Oil_Jul_bbl,0) + ISNULL(Oil_Aug_bbl,0) + ISNULL(Oil_Sep_bbl,0) + ISNULL(Oil_Oct_bbl,0) + ISNULL(Oil_Nov_bbl,0) + ISNULL(Oil_Dec_bbl,0),2),
          Water_TOTAL_bbl=ROUND(ISNULL(Water_Jan_bbl,0) + ISNULL(Water_Feb_bbl,0) + ISNULL(Water_Mar_bbl,0) + ISNULL(Water_Apr_bbl,0) + ISNULL(Water_May_bbl,0) + ISNULL(Water_Jun_bbl,0) + ISNULL(Water_Jul_bbl,0) + ISNULL(Water_Aug_bbl,0) + ISNULL(Water_Sep_bbl,0) + ISNULL(Water_Oct_bbl,0) + ISNULL(Water_Nov_bbl,0),0) + ISNULL(Water_Dec_bbl,2),
          NGL_TOTAL_bbl=ROUND(ISNULL(NGL_Jan_bbl,0) + ISNULL(NGL_Feb_bbl,0) + ISNULL(NGL_Mar_bbl,0) + ISNULL(NGL_Apr_bbl,0) + ISNULL(NGL_May_bbl,0) + ISNULL(NGL_Jun_bbl,0) + ISNULL(NGL_Jul_bbl,0) + ISNULL(NGL_Aug_bbl,0) + ISNULL(NGL_Sep_bbl,0) + ISNULL(NGL_Oct_bbl,0) + ISNULL(NGL_Nov_bbl,0) + ISNULL(NGL_Dec_bbl,0),2),
          Condensate_TOTAL_bbl=ROUND(ISNULL(Condensate_Jan_bbl,0) + ISNULL(Condensate_Feb_bbl,0) + ISNULL(Condensate_Mar_bbl,0) + ISNULL(Condensate_Apr_bbl,0) + ISNULL(Condensate_May_bbl,0) + ISNULL(Condensate_Jun_bbl,0) + ISNULL(Condensate_Jul_bbl,0) + ISNULL(Condensate_Aug_bbl,0) + ISNULL(Condensate_Sep_bbl,0) + ISNULL(Condensate_Oct_bbl,0) + ISNULL(Condensate_Nov_bbl,0) + ISNULL(Condensate_Dec_bbl,0),2);
    '''
	
	if insert:
		
		print '\t{} Inserting Monthly Production Data into US_Wells.dbo.tblUSWell_Production_Historical ...'.format(
			gd.get_datetime())
		if debug:
			print sql_insert_1
		curr.execute(sql_insert_1)
		gd.commit(curr)
		print '\t{} Monthly Production Data Insert Complete\n'.format(gd.get_datetime())
		
		print '\t{} Inserting Annual Production Data into US_Wells.dbo.tblUSWell_Production ...'.format(
			gd.get_datetime())
		if debug:
			print sql_insert_2
		curr.execute(sql_insert_2)
		gd.commit(curr)
		update_time = gd.get_datetime()
		if debug:
			print sql_insert_3.format(update_time)
		curr.execute(sql_insert_3.format(update_time))
		gd.commit(curr)
		print '\t{} Annual Production Data Insert Complete\n'.format(gd.get_datetime())
	
	if update:
		for prod_month in sorted(MONTH_NAMES.keys()):
			print '\t{} Updating Production Data for {} ...'.format(gd.get_datetime(), MONTH_NAMES[prod_month])
			if debug:
				print sql_update.format(MONTH_NAMES[prod_month], prod_month)
			curr.execute(sql_update.format(MONTH_NAMES[prod_month], prod_month))
			gd.commit(curr)
			print '\t{} Production Data Update Complete for {}\n'.format(gd.get_datetime(), MONTH_NAMES[prod_month])
		# -------------------------------------------------------------------------------------------------------------------
		# update_time = gd.get_datetime()
		# print '\t{} Updating Production ID Data ...'.format(update_time)
		# if debug:
		# 	print sql_update_pkgid_data.format(update_time)
		# curr.execute(sql_update_pkgid_data.format(update_time))
		# gd.commit(curr)
		# print '\t{} Production ID Data Update Complete\n'.format(gd.get_datetime())
		# -------------------------------------------------------------------------------------------------------------------
		print '\t{} Updating API 14 Data ...'.format(gd.get_datetime())
		if debug:
			print sql_update_api
		curr.execute(sql_update_api)
		gd.commit(curr)
		print '\t{} API 14 Data Update Complete\n'.format(gd.get_datetime())
		# -------------------------------------------------------------------------------------------------------------------
		print '\t{} Updating Production Totals ...'.format(gd.get_datetime())
		if debug:
			print sql_update_prod_totals
		curr.execute(sql_update_prod_totals)
		gd.commit(curr)
		print '\t{} Production Totals Update Complete\n'.format(gd.get_datetime())


# 2.3 Update US_Wells.dbo.tblUSWell_Production_Forecast

def get_sql_where(api_col_name):
	engine_list = gd.get_engine_list()
	state_list = []
	well_list = []
	sql_where = "SUBSTRING({},1,2)!='42'".format(api_col_name)
	
	if engine_list == 'states':
		state_list = read_state_list()
		state_list_str = ','.join(["'{}'".format(state_id) for state_id in state_list])
		sql_where = "SUBSTRING({},1,2) IN ({})".format(api_col_name, state_list_str)
	
	elif engine_list == 'wells':
		well_list = read_well_list()
		sql_where = "WellID IN ({})".format(','.join(["{}".format(api_num) for api_num in well_list]))
	
	elif engine_list == 'tx':
		sql_where = "SUBSTRING({},1,2)='42'".format(api_col_name)
	
	return sql_where


def update_production_forecast_table(curr, insert=False, update=False, debug=False):
	sql_insert = \
		"""
        TRUNCATE TABLE US_Wells.dbo.tblUSWell_Production_Forecast;
        TRUNCATE TABLE US_Wells.dbo.tblUSWell_Economics_Forecast;
    
        INSERT INTO US_Wells.dbo.tblUSWell_Production_Forecast (WellID, API_Number, StateID, [Period], Gas_Total_mcf, Gas_Jan_mcf, Gas_Feb_mcf, Gas_Mar_mcf, Gas_Apr_mcf, Gas_May_mcf, Gas_Jun_mcf, Gas_Jul_mcf, Gas_Aug_mcf, Gas_Sep_mcf, Gas_Oct_mcf, Gas_Nov_mcf, Gas_Dec_mcf, Oil_Total_bbl, Oil_Jan_bbl, Oil_Feb_bbl, Oil_Mar_bbl, Oil_Apr_bbl, Oil_May_bbl, Oil_Jun_bbl, Oil_Jul_bbl, Oil_Aug_bbl, Oil_Sep_bbl, Oil_Oct_bbl, Oil_Nov_bbl, Oil_Dec_bbl, Condensate_Total_bbl, Condensate_Jan_bbl, Condensate_Feb_bbl, Condensate_Mar_bbl, Condensate_Apr_bbl, Condensate_May_bbl, Condensate_Jun_bbl, Condensate_Jul_bbl, Condensate_Aug_bbl, Condensate_Sep_bbl, Condensate_Oct_bbl, Condensate_Nov_bbl, Condensate_Dec_bbl, NGL_Total_bbl, NGL_Jan_bbl, NGL_Feb_bbl, NGL_Mar_bbl, NGL_Apr_bbl, NGL_May_bbl, NGL_Jun_bbl, NGL_Jul_bbl, NGL_Aug_bbl, NGL_Sep_bbl, NGL_Oct_bbl, NGL_Nov_bbl, NGL_Dec_bbl, Water_Total_bbl, Water_Jan_bbl, Water_Feb_bbl, Water_Mar_bbl, Water_Apr_bbl, Water_May_bbl, Water_Jun_bbl, Water_Jul_bbl, Water_Aug_bbl, Water_Sep_bbl, Water_Oct_bbl, Water_Nov_bbl, Water_Dec_bbl, Reported_API_Number, Sources)
          (SELECT DISTINCT ISNULL(WellID,0), ISNULL(API_14,'00000000000000'), SUBSTRING(API_14,1,2), [Period], Gas_Total_mcf, Gas_Jan_mcf, Gas_Feb_mcf, Gas_Mar_mcf, Gas_Apr_mcf, Gas_May_mcf, Gas_Jun_mcf, Gas_Jul_mcf, Gas_Aug_mcf, Gas_Sep_mcf, Gas_Oct_mcf, Gas_Nov_mcf, Gas_Dec_mcf, Oil_Total_bbl, Oil_Jan_bbl, Oil_Feb_bbl, Oil_Mar_bbl, Oil_Apr_bbl, Oil_May_bbl, Oil_Jun_bbl, Oil_Jul_bbl, Oil_Aug_bbl, Oil_Sep_bbl, Oil_Oct_bbl, Oil_Nov_bbl, Oil_Dec_bbl, Condensate_Total_bbl, Condensate_Jan_bbl, Condensate_Feb_bbl, Condensate_Mar_bbl, Condensate_Apr_bbl, Condensate_May_bbl, Condensate_Jun_bbl, Condensate_Jul_bbl, Condensate_Aug_bbl, Condensate_Sep_bbl, Condensate_Oct_bbl, Condensate_Nov_bbl, Condensate_Dec_bbl, NGL_Total_bbl, NGL_Jan_bbl, NGL_Feb_bbl, NGL_Mar_bbl, NGL_Apr_bbl, NGL_May_bbl, NGL_Jun_bbl, NGL_Jul_bbl, NGL_Aug_bbl, NGL_Sep_bbl, NGL_Oct_bbl, NGL_Nov_bbl, NGL_Dec_bbl, Water_Total_bbl, Water_Jan_bbl, Water_Feb_bbl, Water_Mar_bbl, Water_Apr_bbl, Water_May_bbl, Water_Jun_bbl, Water_Jul_bbl, Water_Aug_bbl, Water_Sep_bbl, Water_Oct_bbl, Water_Nov_bbl, Water_Dec_bbl, API_Number, [Source]
           FROM US_Wells.dbo.tblUSWell_Production WHERE {});
        """
	sql_update = \
		"""
        UPDATE US_Wells.dbo.tblUSWell_Production_Forecast
          SET Gas_Total_mcf=ISNULL(Gas_Total_mcf,0),
              Oil_Total_bbl=ISNULL(Oil_Total_bbl,0),
              Condensate_Total_bbl=ISNULL(Condensate_Total_bbl,0),
              NGL_Total_bbl=ISNULL(NGL_Total_bbl,0),
              Water_Total_bbl=ISNULL(Water_Total_bbl,0),
              Gas_Jan_mcf=ISNULL(Gas_Jan_mcf,0),
              Gas_Feb_mcf=ISNULL(Gas_Feb_mcf,0),
              Gas_Mar_mcf=ISNULL(Gas_Mar_mcf,0),
              Gas_Apr_mcf=ISNULL(Gas_Apr_mcf,0),
              Gas_May_mcf=ISNULL(Gas_May_mcf,0),
              Gas_Jun_mcf=ISNULL(Gas_Jun_mcf,0),
              Gas_Jul_mcf=ISNULL(Gas_Jul_mcf,0),
              Gas_Aug_mcf=ISNULL(Gas_Aug_mcf,0),
              Gas_Sep_mcf=ISNULL(Gas_Sep_mcf,0),
              Gas_Oct_mcf=ISNULL(Gas_Oct_mcf,0),
              Gas_Nov_mcf=ISNULL(Gas_Nov_mcf,0),
              Gas_Dec_mcf=ISNULL(Gas_Dec_mcf,0),
              Oil_Jan_bbl=ISNULL(Oil_Jan_bbl,0),
              Oil_Feb_bbl=ISNULL(Oil_Feb_bbl,0),
              Oil_Mar_bbl=ISNULL(Oil_Mar_bbl,0),
              Oil_Apr_bbl=ISNULL(Oil_Apr_bbl,0),
              Oil_May_bbl=ISNULL(Oil_May_bbl,0),
              Oil_Jun_bbl=ISNULL(Oil_Jun_bbl,0),
              Oil_Jul_bbl=ISNULL(Oil_Jul_bbl,0),
              Oil_Aug_bbl=ISNULL(Oil_Aug_bbl,0),
              Oil_Sep_bbl=ISNULL(Oil_Sep_bbl,0),
              Oil_Oct_bbl=ISNULL(Oil_Oct_bbl,0),
              Oil_Nov_bbl=ISNULL(Oil_Nov_bbl,0),
              Oil_Dec_bbl=ISNULL(Oil_Dec_bbl,0),
              Condensate_Jan_bbl=ISNULL(Condensate_Jan_bbl,0),
              Condensate_Feb_bbl=ISNULL(Condensate_Feb_bbl,0),
              Condensate_Mar_bbl=ISNULL(Condensate_Mar_bbl,0),
              Condensate_Apr_bbl=ISNULL(Condensate_Apr_bbl,0),
              Condensate_May_bbl=ISNULL(Condensate_May_bbl,0),
              Condensate_Jun_bbl=ISNULL(Condensate_Jun_bbl,0),
              Condensate_Jul_bbl=ISNULL(Condensate_Jul_bbl,0),
              Condensate_Aug_bbl=ISNULL(Condensate_Aug_bbl,0),
              Condensate_Sep_bbl=ISNULL(Condensate_Sep_bbl,0),
              Condensate_Oct_bbl=ISNULL(Condensate_Oct_bbl,0),
              Condensate_Nov_bbl=ISNULL(Condensate_Nov_bbl,0),
              Condensate_Dec_bbl=ISNULL(Condensate_Dec_bbl,0),
              NGL_Jan_bbl=ISNULL(NGL_Jan_bbl,0),
              NGL_Feb_bbl=ISNULL(NGL_Feb_bbl,0),
              NGL_Mar_bbl=ISNULL(NGL_Mar_bbl,0),
              NGL_Apr_bbl=ISNULL(NGL_Apr_bbl,0),
              NGL_May_bbl=ISNULL(NGL_May_bbl,0),
              NGL_Jun_bbl=ISNULL(NGL_Jun_bbl,0),
              NGL_Jul_bbl=ISNULL(NGL_Jul_bbl,0),
              NGL_Aug_bbl=ISNULL(NGL_Aug_bbl,0),
              NGL_Sep_bbl=ISNULL(NGL_Sep_bbl,0),
              NGL_Oct_bbl=ISNULL(NGL_Oct_bbl,0),
              NGL_Nov_bbl=ISNULL(NGL_Nov_bbl,0),
              NGL_Dec_bbl=ISNULL(NGL_Dec_bbl,0),
              Water_Jan_bbl=ISNULL(Water_Jan_bbl,0),
              Water_Feb_bbl=ISNULL(Water_Feb_bbl,0),
              Water_Mar_bbl=ISNULL(Water_Mar_bbl,0),
              Water_Apr_bbl=ISNULL(Water_Apr_bbl,0),
              Water_May_bbl=ISNULL(Water_May_bbl,0),
              Water_Jun_bbl=ISNULL(Water_Jun_bbl,0),
              Water_Jul_bbl=ISNULL(Water_Jul_bbl,0),
              Water_Aug_bbl=ISNULL(Water_Aug_bbl,0),
              Water_Sep_bbl=ISNULL(Water_Sep_bbl,0),
              Water_Oct_bbl=ISNULL(Water_Oct_bbl,0),
              Water_Nov_bbl=ISNULL(Water_Nov_bbl,0),
              Water_Dec_bbl=ISNULL(Water_Dec_bbl,0)
          WHERE {0};

		UPDATE US_Wells.dbo.tblUSWell_Production_Forecast
		  SET Gas_Total_mcf=ROUND(ISNULL(Gas_Jan_mcf,0) + ISNULL(Gas_Feb_mcf,0) + ISNULL(Gas_Mar_mcf,0) + ISNULL(Gas_Apr_mcf,0) + ISNULL(Gas_May_mcf,0) + ISNULL(Gas_Jun_mcf,0) + ISNULL(Gas_Jul_mcf,0) + ISNULL(Gas_Aug_mcf,0) + ISNULL(Gas_Sep_mcf,0) + ISNULL(Gas_Oct_mcf,0) + ISNULL(Gas_Nov_mcf,0) + ISNULL(Gas_Dec_mcf,0),2),
			  Oil_Total_bbl=ROUND(ISNULL(Oil_Jan_bbl,0) + ISNULL(Oil_Feb_bbl,0) + ISNULL(Oil_Mar_bbl,0) + ISNULL(Oil_Apr_bbl,0) + ISNULL(Oil_May_bbl,0) + ISNULL(Oil_Jun_bbl,0) + ISNULL(Oil_Jul_bbl,0) + ISNULL(Oil_Aug_bbl,0) + ISNULL(Oil_Sep_bbl,0) + ISNULL(Oil_Oct_bbl,0) + ISNULL(Oil_Nov_bbl,0) + ISNULL(Oil_Dec_bbl,0),2),
			  Water_Total_bbl=ROUND(ISNULL(Water_Jan_bbl,0) + ISNULL(Water_Feb_bbl,0) + ISNULL(Water_Mar_bbl,0) + ISNULL(Water_Apr_bbl,0) + ISNULL(Water_May_bbl,0) + ISNULL(Water_Jun_bbl,0) + ISNULL(Water_Jul_bbl,0) + ISNULL(Water_Aug_bbl,0) + ISNULL(Water_Sep_bbl,0) + ISNULL(Water_Oct_bbl,0) + ISNULL(Water_Nov_bbl,0),0) + ISNULL(Water_Dec_bbl,2),
			  NGL_Total_bbl=ROUND(ISNULL(NGL_Jan_bbl,0) + ISNULL(NGL_Feb_bbl,0) + ISNULL(NGL_Mar_bbl,0) + ISNULL(NGL_Apr_bbl,0) + ISNULL(NGL_May_bbl,0) + ISNULL(NGL_Jun_bbl,0) + ISNULL(NGL_Jul_bbl,0) + ISNULL(NGL_Aug_bbl,0) + ISNULL(NGL_Sep_bbl,0) + ISNULL(NGL_Oct_bbl,0) + ISNULL(NGL_Nov_bbl,0) + ISNULL(NGL_Dec_bbl,0),2),
			  Condensate_Total_bbl=ROUND(ISNULL(Condensate_Jan_bbl,0) + ISNULL(Condensate_Feb_bbl,0) + ISNULL(Condensate_Mar_bbl,0) + ISNULL(Condensate_Apr_bbl,0) + ISNULL(Condensate_May_bbl,0) + ISNULL(Condensate_Jun_bbl,0) + ISNULL(Condensate_Jul_bbl,0) + ISNULL(Condensate_Aug_bbl,0) + ISNULL(Condensate_Sep_bbl,0) + ISNULL(Condensate_Oct_bbl,0) + ISNULL(Condensate_Nov_bbl,0) + ISNULL(Condensate_Dec_bbl,0),2)
		  WHERE {0};
		"""
	if insert:
		print '\t{} Inserting historical production data into US_Wells.dbo.tblUSWell_Production_Forecast ...'.format(
			gd.get_datetime())
		sql_where = get_sql_where('API_14')
		if debug:
			print sql_insert.format(sql_where)
		curr.execute(sql_insert.format(sql_where))
		gd.commit(curr)
		print
	if update:
		print '\t{} Updating production data US_Wells.dbo.tblUSWell_Production_Forecast ...'.format(gd.get_datetime())
		sql_where = get_sql_where('API_Number')
		if debug:
			print sql_update.format(sql_where)
		curr.execute(sql_update.format(sql_where))
		gd.commit(curr)


# 2.4 Update US_Wells.dbo.tblUSWell_Parameters

def update_parameters_table(curr, insert=False, update=False, last_prod=False, engine_group='non_tx', all_tx=False,debug=False):
	sql_insert_non_tx = \
		"""
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Forecast_Well=10;
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Forecast_Well=0 WHERE {};
    
        INSERT INTO tblUSWell_Parameters (WellID,API_Number,StateID,Basin,State_Name,Well_Terrain,Well_Direction,Operator,Commodity,Resource_Play,First_Production_Date,True_Vertical_Depth_ft,Lateral_Length_ft,Well_Status,State_Well_Direction,Forecast_Well)
          (SELECT WellID,API_14,SUBSTRING(API_14,1,2),Basin,State,Well_Terrain,Well_Direction,ParentOperator,Commodity,Shale,First_Production_Date,True_Vertical_Depth_ft,Lateral_Length_ft,Well_Status,Well_Direction,9
           FROM tblUSWell_Details WHERE WellID IN (SELECT DISTINCT WellID FROM tblmaster_WellID_API_Number WHERE process_code=0));
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Oil_Decline_Rate_Type='avg', Gas_Decline_Rate_Type='avg', Cond_Decline_Rate_Type='avg', NGL_Decline_Rate_Type='avg', Years_Before_Terminal=3, Capex_Tangible_Split_pct=0.67
          WHERE Forecast_Well=9;
        """
	sql_insert_tx = \
		"""
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Forecast_Well=0 WHERE State_Name='Texas';
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Forecast_Well=10 WHERE State_Name!='Texas';
    
        INSERT INTO tblUSWell_Parameters (WellID,API_Number,StateID,Basin,State_Name,Well_Terrain,Well_Direction,Operator,Commodity,Resource_Play,First_Production_Date,True_Vertical_Depth_ft,Lateral_Length_ft,Well_Status,State_Well_Direction,Forecast_Well)
          (SELECT WellID,API_14,SUBSTRING(API_14,1,2),Basin,State,Well_Terrain,Well_Direction,ParentOperator,Commodity,Shale,First_Production_Date,True_Vertical_Depth_ft,Lateral_Length_ft,Well_Status,Well_Direction,9
           FROM tblUSWell_Details WHERE WellID IN (SELECT DISTINCT WellID FROM tblmaster_WellID_API_Number WHERE process_code=0));
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Oil_Decline_Rate_Type='avg', Gas_Decline_Rate_Type='avg', Cond_Decline_Rate_Type='avg', NGL_Decline_Rate_Type='avg', Years_Before_Terminal=3, Capex_Tangible_Split_pct=0.67
          WHERE Forecast_Well=9;
        """
	sql_update = \
		"""
        UPDATE US_Wells.dbo.tblUSWell_Details SET Basin=NULL WHERE LEN(Basin)=0;
        UPDATE US_Wells.dbo.tblUSWell_Details SET Well_Status=NULL WHERE LEN(Well_Status)=0;
        UPDATE US_Wells.dbo.tblUSWell_Details SET Well_Direction=NULL WHERE LEN(Well_Direction)=0;
        UPDATE US_Wells.dbo.tblUSWell_Details SET Shale=NULL WHERE LEN(Shale)=0;
        UPDATE US_Wells.dbo.tblUSWell_Details SET ParentOperator=NULL WHERE LEN(ParentOperator)=0;
        UPDATE US_Wells.dbo.tblUSWell_Details SET Lateral_Length_ft=NULL WHERE LEN(CONVERT(VARCHAR(25),Lateral_Length_ft))=0;
        UPDATE US_Wells.dbo.tblUSWell_Details SET Measured_Depth_ft=NULL WHERE LEN(CONVERT(VARCHAR(25),Measured_Depth_ft))=0;
        UPDATE US_Wells.dbo.tblUSWell_Details SET True_Vertical_Depth_ft=NULL WHERE LEN(CONVERT(VARCHAR(25),True_Vertical_Depth_ft))=0;
    
        UPDATE tblUSWell_Parameters SET WellID=b.WellID
          FROM tblUSWell_Parameters a, tblUSWell_Details b
          WHERE a.API_Number=b.API_14 AND a.Forecast_Well < 10 AND a.WellID!=b.WellID;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters
          SET Basin=b.Basin
          FROM tblUSWell_Parameters a, tblUSWell_Details b
          WHERE a.WellID=b.WellID AND a.Forecast_Well < 10;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters
          SET Well_Status=b.Well_Status
          FROM tblUSWell_Parameters a, tblUSWell_Details b
          WHERE a.WellID=b.WellID AND a.Forecast_Well < 10;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters
          SET State_Well_Direction=b.Well_Direction
          FROM tblUSWell_Parameters a, tblUSWell_Details b
          WHERE a.WellID=b.WellID AND a.Forecast_Well < 10;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters
          SET Resource_Play=b.Shale
          FROM tblUSWell_Parameters a, tblUSWell_Details b
          WHERE a.WellID=b.WellID AND a.Forecast_Well < 10;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters
          SET Operator=b.ParentOperator
          FROM tblUSWell_Parameters a, tblUSWell_Details b
          WHERE a.WellID=b.WellID AND a.Forecast_Well < 10;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET County_Code=SUBSTRING(API_Number,3,3) WHERE County_Code IS NULL;
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Operator=REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(Operator,'''',''),'#',''),'(',''),')',''),'-',''),'"',''),'.',''),'%',''),',',''),'  ',' '),'  ',' ');
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Commodity='GAS' WHERE Commodity='G';
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Commodity='OIL' WHERE Commodity='O';
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET commodity='GAS' WHERE commodity='Gas';
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET commodity='OIL' WHERE commodity='Oil';
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Production_Start_Year=b.Min_Prod_Year
          FROM US_Wells.dbo.tblUSWell_Parameters a,
               (SELECT DISTINCT WellID, MIN([Period]) AS Min_Prod_Year FROM US_Wells.dbo.tblUSWell_Production WHERE (ISNULL(Gas_Total_mcf,0)+ISNULL(Oil_Total_bbl,0)) > 0 GROUP BY WellID) b
          WHERE a.WellID=b.WellID;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction=State_Well_Direction WHERE Well_Direction IS NULL AND State_Well_Direction IS NOT NULL;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction=NULL WHERE LEN(Well_Direction) < 1;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Vertical'
          WHERE Resource_Type='Conventional' AND (Well_Direction IS NULL OR Well_Direction='Directional');
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Horizontal'
          WHERE Resource_Type='Unconventional' AND (Well_Direction IS NULL OR Well_Direction='Directional');
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Vertical'
          WHERE Well_Direction='Horizontal' AND Lateral_Length_ft IS NULL AND Measured_Depth_ft IS NOT NULL AND Measured_Depth_ft < 12000;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Vertical'
          WHERE ISNULL(Lateral_Length_ft,0)>0 AND Lateral_Length_ft <= 1000;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Horizontal'
          WHERE ISNULL(Lateral_Length_ft,0)>0 AND Lateral_Length_ft > 1000;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Vertical'
          WHERE Well_Direction IS NULL AND Production_Start_Year < 2005;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Horizontal'
          WHERE Well_Direction IS NULL AND Production_Start_Year >= 2005;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Vertical', State_Well_Direction='Default Vertical'
          WHERE Well_Direction NOT IN ('Vertical', 'Horizontal');
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET True_Vertical_Depth_ft=b.True_Vertical_Depth_ft
          FROM US_Wells.dbo.tblUSWell_Parameters a, US_Wells.dbo.tblUSWell_Details b
          WHERE b.True_Vertical_Depth_ft IS NOT NULL AND a.WellID=b.WellID;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Measured_Depth_ft=b.Measured_Depth_ft
          FROM US_Wells.dbo.tblUSWell_Parameters a, US_Wells.dbo.tblUSWell_Details b
          WHERE b.Measured_Depth_ft IS NOT NULL AND a.WellID=b.WellID;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Lateral_Length_ft=b.Lateral_Length_ft
          FROM US_Wells.dbo.tblUSWell_Parameters a, US_Wells.dbo.tblUSWell_Details b
          WHERE b.Lateral_Length_ft IS NOT NULL AND a.WellID=b.WellID;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET True_Vertical_Depth_ft=Measured_Depth_ft
          WHERE ISNULL(True_Vertical_Depth_Ft,0)=0 AND ISNULL(Measured_Depth_ft,0) > 0
          AND Well_Direction='Vertical';
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Measured_Depth_ft=ROUND(True_Vertical_Depth_ft,2)
          WHERE ISNULL(Measured_Depth_ft,0)=0 AND ISNULL(True_Vertical_Depth_Ft,0) > 0
          AND Well_Direction='Vertical';
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Measured_Depth_ft=(True_Vertical_Depth_ft + Lateral_Length_ft)
          WHERE ISNULL(Measured_Depth_ft,0)=0 AND ISNULL(True_Vertical_Depth_ft,0) > 0
          AND ISNULL(Lateral_length_ft,0) > 0 AND Well_Direction='Horizontal';
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET True_Vertical_Depth_ft=(Measured_Depth_ft - Lateral_Length_ft)
          WHERE ISNULL(Measured_Depth_ft,0) > 0 AND ISNULL(True_Vertical_Depth_ft,0)=0
          AND ISNULL(Lateral_length_ft,0) > 0 AND Well_Direction='Horizontal';
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Lateral_Length_ft=(Measured_Depth_ft-True_Vertical_Depth_ft)
          WHERE Well_Direction='Horizontal' AND ISNULL(Lateral_Length_ft,0)=0
          AND ISNULL(Measured_Depth_ft,0) > 0 AND ISNULL(True_Vertical_Depth_ft,0) > 0
          AND (ISNULL(Measured_Depth_ft,0) > ISNULL(True_Vertical_Depth_ft,0));
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Vertical'
          WHERE Well_Direction='Horizontal' AND Lateral_Length_ft IS NULL AND Measured_Depth_ft IS NOT NULL AND Measured_Depth_ft < 12000;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Vertical'
          WHERE ISNULL(Lateral_Length_ft,0)>0 AND Lateral_Length_ft <= 1000;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Horizontal'
          WHERE ISNULL(Lateral_Length_ft,0)>0 AND Lateral_Length_ft > 1000;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Vertical'
          WHERE Well_Direction IS NULL AND Production_Start_Year < 2005;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Horizontal'
          WHERE Well_Direction IS NULL AND Production_Start_Year >= 2005;
    
        UPDATE US_Wells.dbo.tblUSWell_Parameters SET Well_Direction='Vertical', State_Well_Direction='Default Vertical'
          WHERE Well_Direction NOT IN ('Vertical', 'Horizontal');
        """
	forecast_well_update = \
		"""
		UPDATE tblUSWell_Parameters SET Forecast_Well=0;
		UPDATE tblUSWell_Parameters SET Forecast_Well=10 WHERE State_Name='Texas';
        UPDATE tblUSWell_Parameters SET Forecast_Well=1 WHERE Forecast_Well < 10 AND WellID IN (SELECT DISTINCT WellID FROM tblUSWell_Production_Forecast WHERE [Period] >= 2019 AND (ISNULL(Gas_Total_mcf,0)+ISNULL(Oil_Total_bbl,0)) > 0);
        UPDATE tblUSWell_Parameters SET Forecast_Well=2 WHERE Forecast_Well IN (1,9) AND Well_Status!='Producing';
        UPDATE tblUSWell_Parameters SET Forecast_Well=3 WHERE Forecast_Well=0 AND Well_Status='Producing';
        UPDATE tblUSWell_Parameters SET Forecast_Well=4 WHERE Forecast_Well IN (1,9) AND Well_Direction='Vertical' AND ISNULL(True_Vertical_Depth_ft,0)=0;
        UPDATE tblUSWell_Parameters SET Forecast_Well=5 WHERE Forecast_Well IN (1,9) AND Well_Direction='Horizontal' AND ISNULL(Lateral_length_ft,0)=0;
        UPDATE tblUSWell_Parameters SET Forecast_Well=6 WHERE Forecast_Well IN (1,9) AND Well_Direction='Vertical';
        """
	forecast_well_update_all_tx = \
		"""
		UPDATE tblUSWell_Parameters SET Forecast_Well=0;
		UPDATE tblUSWell_Parameters SET Forecast_Well=10 WHERE State_Name!='Texas';
        UPDATE tblUSWell_Parameters SET Forecast_Well=1 WHERE Forecast_Well < 10 AND WellID IN (SELECT DISTINCT WellID FROM tblUSWell_Production_Forecast WHERE [Period] >= 2019 AND (ISNULL(Gas_Total_mcf,0)+ISNULL(Oil_Total_bbl,0)) > 0)
        UPDATE tblUSWell_Parameters SET Forecast_Well=2 WHERE Forecast_Well IN (1, 9) AND Well_Status!='Producing';
        UPDATE tblUSWell_Parameters SET Forecast_Well=3 WHERE Forecast_Well=0 AND Well_Status='Producing';
        UPDATE tblUSWell_Parameters SET Forecast_Well=4 WHERE Forecast_Well IN (1,9) AND Well_Direction='Vertical' AND ISNULL(True_Vertical_Depth_ft,0)=0;
        UPDATE tblUSWell_Parameters SET Forecast_Well=5 WHERE Forecast_Well IN (1,9) AND Well_Direction='Horizontal' AND ISNULL(Lateral_length_ft,0)=0;
        UPDATE tblUSWell_Parameters SET Forecast_Well=6 WHERE Forecast_Well IN (1,9) AND Well_Direction='Vertical';
        """
	
	if insert:
		print '\tInserting well details data into US_Wells.dbo.tblUSWell_Parameters ...'
		if engine_group == 'tx':
			sql_insert = sql_insert_tx
		else:
			sql_where = get_sql_where('API_Number')
			sql_insert = sql_insert_non_tx.format(sql_where)
		if debug: print sql_insert
		curr.execute(sql_insert)
		gd.commit(curr)
	
	if update:
		if debug: print sql_update
		curr.execute(sql_update)
		gd.commit(curr)
		if all_tx is True:
			print '\tUpdating texas engine parameters in US_Wells.dbo.tblUSWell_Parameters ...'
			if debug: print forecast_well_update_all_tx
			curr.execute(forecast_well_update_all_tx)
			gd.commit(curr)
		else:
			print '\tUpdating engine parameters in US_Wells.dbo.tblUSWell_Parameters ...'
			if debug: print forecast_well_update
			curr.execute(forecast_well_update)
			gd.commit(curr)
	if last_prod:
		forecast.main(well_list=[], update_params=True, update_last_prod_date=True, debug=debug)


# 2.5 Update US_Wells.dbo.tblUSWell_Assumptions

def update_assumptions_table(export_data=False, import_data=False, update=False, debug=False):
	print 'Updating US_Wells.dbo.tblUSWell_Assumptions ...'
	if export_data:
		pass
	if import_data:
		pass
	if update:
		forecast.main(well_list=[], update_assumptions=True, update_avgs=True, update_cols=True, update_prod_costs=True,
					  update_well_cost_data=True, update_decline_avgs=True, debug=debug)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Stage 3 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 3.1 Update pre-engine well parameters

def update_well_parameters(well_id_list, forecast_count, split_well_list=False, engine_group=0, debug=False):
	if split_well_list:
		well_list = well_id_list[engine_group * forecast_count: (engine_group + 1) * forecast_count]
	else:
		well_list = well_id_list
	forecast.main(well_list=well_list, update_params=True, update_max_prod=True, update_term_decline=True, debug=debug)


# 3.2 Choose well assumptions

def choose_well_assumptions(well_id_list, forecast_count, split_well_list=False, engine_group=0, debug=False):
	if split_well_list:
		well_list = well_id_list[engine_group * forecast_count: (engine_group + 1) * forecast_count]
	else:
		well_list = well_id_list
	forecast.main(well_list=well_list, update_assumptions=True, update_choices=True, update_decline_choices=True,
				  debug=debug)


# 3.3 Estimate length parameters

def est_length_params(well_id_list, forecast_count, length_param, split_well_list=False, engine_group=0, debug=False):
	if length_param == 'lateral_length_ft':
		if split_well_list:
			well_list = well_id_list[engine_group * forecast_count: (engine_group + 1) * forecast_count]
		else:
			well_list = well_id_list
		forecast.main(well_list=well_list, update_assumptions=True, update_est_lengths=True, est_lat_len=True,
					  debug=debug)
	
	else:
		if split_well_list:
			well_list = well_id_list[engine_group * forecast_count: (engine_group + 1) * forecast_count]
		else:
			well_list = well_id_list
		forecast.main(well_list=well_list, update_assumptions=True, update_est_lengths=True, est_tvd=True, debug=debug)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Stage 4 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 4.1 Forecast well production

def forecast_production(well_id_list, forecast_count, split_well_list=False, engine_group=0, debug=False):
	if split_well_list:
		well_list = well_id_list[engine_group * forecast_count: (engine_group + 1) * forecast_count]
	else:
		well_list = well_id_list
	forecast.main(well_list=well_list, calc_prod=True, dec_month_min=0, store_data=True, null_well_type=True,
				  debug=debug)


# 4.2 Forecast well economics

def forecast_economics(well_id_list, forecast_count, split_well_list=False, engine_group=0, debug=False):
	if split_well_list:
		well_list = well_id_list[engine_group * forecast_count: (engine_group + 1) * forecast_count]
	else:
		well_list = well_id_list
	forecast.main(well_list=well_list, calc_econ=True, dec_month_min=0, store_data=True, null_well_type=True,
				  debug=debug)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Stage 5 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 5.1 Update post-engine well parameters

def update_post_engine_parameters(curr, debug=False):
	sql_update = \
		"""
    UPDATE tblUSWell_Parameters SET Forecast_Well=7 WHERE Forecast_Well IN (1, 4, 5, 6, 9) AND WellID IN (SELECT DISTINCT WellID FROM tblUSWell_Economics_Forecast);

    UPDATE tblUSWell_Parameters SET Total_Variable_Opex_MM_usd=b.total_var_opex
      FROM tblUSWell_Parameters a,
           (SELECT API_Number, ROUND(SUM(ISNULL(Variable_Opex_usd,0))/1000000,3) AS total_var_opex FROM tblUSWell_Economics_Forecast WHERE API_Number IN (SELECT DISTINCT API_Number FROM tblUSWell_Parameters WHERE Forecast_Well=12) GROUP BY API_Number) b
      WHERE a.API_Number=b.API_Number AND a.Forecast_Well=7;
    
    UPDATE tblUSWell_Parameters SET Payback_Period=b.Payback_val
      FROM tblUSWell_Parameters a,
           (SELECT API_Number, MAX(IIF(Payback_Period='-',0,CONVERT(FLOAT,Payback_Period))) AS Payback_val FROM tblUSWell_Economics_Forecast WHERE API_Number IN (SELECT DISTINCT API_Number FROM tblUSWell_Parameters WHERE Forecast_Well=12) GROUP BY API_Number) b
      WHERE a.API_Number=b.API_Number AND a.Forecast_Well=7;
    """
	print '\t5.1 Updating Post-Engine Parameters ...'
	if debug: print '\t', sql_update
	curr.execute(sql_update)
	gd.commit(curr)
	print '\t5.1 Post-Engine Parameter Update Complete'


# 5.2 Copy original US_Wells.dbo.USWell_Parameters to new table

def copy_engine_parameters_data(curr, engine_run_date, debug=False):
	sql_update_1 = \
		"""
    CREATE TABLE tblUSWell_Parameters_{0} (
      Well_ParametersID                BIGINT       IDENTITY,
      WellID                           BIGINT       DEFAULT NULL,
      API_Number                       VARCHAR(50)  DEFAULT NULL,
      StateID                          INT          DEFAULT NULL,
      State_Name                       VARCHAR(100) DEFAULT NULL,
      Well_Terrain                     VARCHAR(150) DEFAULT NULL,
      Well_Direction                   VARCHAR(50)  DEFAULT NULL,
      Operator                         VARCHAR(350) DEFAULT NULL,
      Resource_Type                    VARCHAR(100) DEFAULT NULL,
      Resource_Play                    VARCHAR(250) DEFAULT NULL,
      Peak_Oil_Prod_Rate_bd            FLOAT        DEFAULT NULL,
      Peak_Gas_Prod_Rate_mmcfd         FLOAT        DEFAULT NULL,
      First_Production_Date            VARCHAR(16)  DEFAULT NULL,
      Peak_Oil_Prod_Date               VARCHAR(16)  DEFAULT NULL,
      Peak_Gas_Prod_Date               VARCHAR(16)  DEFAULT NULL,
      Last_Production_Date             VARCHAR(16)  DEFAULT NULL,
      True_Vertical_Depth_ft           FLOAT        DEFAULT NULL,
      Measured_Depth_ft                FLOAT        DEFAULT NULL,
      Lateral_Length_ft                FLOAT        DEFAULT NULL,
      Well_Cost_usd_ft                 FLOAT        DEFAULT NULL,
      Well_EUR_Oil_bbl                 FLOAT        DEFAULT NULL,
      Well_EUR_Gas_mmcf                FLOAT        DEFAULT NULL,
      Well_EUR_Condensate_bbl          FLOAT        DEFAULT NULL,
      Well_EUR_NGLs_bbl                FLOAT        DEFAULT NULL,
      Well_EUR_Total_boe               FLOAT        DEFAULT NULL,
      Pre_tax_NPV_usd                  FLOAT        DEFAULT NULL,
      Pre_tax_IRR_pct                  FLOAT        DEFAULT NULL,
      Pre_tax_BE_Oil_usd_bbl           FLOAT        DEFAULT NULL,
      Pre_tax_BE_Gas_usd_mcf           FLOAT        DEFAULT NULL,
      Pre_Tax_Cashflow_Total_usd       FLOAT        DEFAULT NULL,
      Post_tax_NPV_usd                 FLOAT        DEFAULT NULL,
      Post_tax_IRR_pct                 FLOAT        DEFAULT NULL,
      Post_tax_BE_Oil_usd_bbl          FLOAT        DEFAULT NULL,
      Post_tax_BE_Gas_usd_mcf          FLOAT        DEFAULT NULL,
      Post_Tax_Cashflow_Total_usd      FLOAT        DEFAULT NULL,
      Total_Opex_MM_usd                FLOAT        DEFAULT NULL,
      Cost_Capex_Drilling_MM_usd       FLOAT        DEFAULT NULL,
      Cost_Capex_Completion_MM_usd     FLOAT        DEFAULT NULL,
      Cost_Capex_Facilities_MM_usd     FLOAT        DEFAULT NULL,
      Cost_Capex_Abandonment_usd       FLOAT        DEFAULT NULL,
      Cost_Capex_Maintenance_usd       FLOAT        DEFAULT NULL,
      Cost_Opex_LOE_usd_boe            FLOAT        DEFAULT NULL,
      Cost_Opex_Water_usd_boe          FLOAT        DEFAULT NULL,
      Cost_Opex_GPT_usd_boe            FLOAT        DEFAULT NULL,
      Cost_Opex_NGL_usd_boe            FLOAT        DEFAULT NULL,
      Cost_Opex_Fixed_usd              FLOAT        DEFAULT NULL,
      Royalty_Rate_pct                 FLOAT        DEFAULT NULL,
      Capex_Tangible_Split_pct         FLOAT        DEFAULT NULL,
      Decline_Param_Oil_Qi             FLOAT        DEFAULT NULL,
      Decline_Param_Oil_Di             FLOAT        DEFAULT NULL,
      Decline_Param_Oil_b              FLOAT        DEFAULT NULL,
      Decline_Param_Gas_Qi             FLOAT        DEFAULT NULL,
      Decline_Param_Gas_Di             FLOAT        DEFAULT NULL,
      Decline_Param_Gas_b              FLOAT        DEFAULT NULL,
      Years_Before_Terminal            FLOAT        DEFAULT NULL,
      Economic_Well_Life               FLOAT        DEFAULT NULL,
      Payback_Period                   FLOAT        DEFAULT NULL,
      Initial_Water_Cut_pct            FLOAT        DEFAULT NULL,
      Hist_Oil_Decline_pct             FLOAT        DEFAULT NULL,
      Hist_Gas_Decline_pct             FLOAT        DEFAULT NULL,
      Hist_Cond_Decline_pct            FLOAT        DEFAULT NULL,
      Hist_NGL_Decline_pct             FLOAT        DEFAULT NULL,
      Relative_Peak_Oil_Date           VARCHAR(10)  DEFAULT NULL,
      Relative_Peak_Gas_Date           VARCHAR(10)  DEFAULT NULL,
      Relative_Peak_Cond_Date          VARCHAR(10)  DEFAULT NULL,
      Relative_Peak_NGL_Date           VARCHAR(10)  DEFAULT NULL,
      Oil_Prod_Decline_Months          INT          DEFAULT NULL,
      Gas_Prod_Decline_Months          INT          DEFAULT NULL,
      Cond_Prod_Decline_Months         INT          DEFAULT NULL,
      NGL_Prod_Decline_Months          INT          DEFAULT NULL,
      Oil_Decline_Rate_Type            CHAR(3)      DEFAULT NULL,
      Gas_Decline_Rate_Type            CHAR(3)      DEFAULT NULL,
      Cond_Decline_Rate_Type           CHAR(3)      DEFAULT NULL,
      NGL_Decline_Rate_Type            CHAR(3)      DEFAULT NULL,
      Completion_Cost_pct              FLOAT        DEFAULT NULL,
      Drilling_Cost_pct                FLOAT        DEFAULT NULL,
      Facilities_Cost_pct              FLOAT        DEFAULT NULL,
      Total_Well_Cost_MM_usd           FLOAT        DEFAULT NULL,
      LOE_Primary_usd_boe              FLOAT        DEFAULT NULL,
      GPT_Primary_usd_boe              FLOAT        DEFAULT NULL,
      Well_Status                      VARCHAR(150) DEFAULT NULL,
      Total_Fiscal_Take_usd            FLOAT        DEFAULT NULL,
      Total_Fiscal_Take_pct            FLOAT        DEFAULT NULL,
      Formation                        VARCHAR(400),
      Basin                            VARCHAR(100),
      Forecast_Well                    TINYINT,
      Last_Econ_Year                   INT,
      State_Well_Direction             VARCHAR(50),
      Avg_LOE_pct                      FLOAT        DEFAULT NULL,
      AVG_GPT_pct                      FLOAT        DEFAULT NULL,
      Cost_Opex_Production_usd_boe     FLOAT        DEFAULT NULL,
      Avg_Lateral_Length_ft            FLOAT        DEFAULT NULL,
      Avg_Well_Cost_mm_usd             FLOAT        DEFAULT NULL,
      Cost_Capex_Abandonment_usd_ft    FLOAT        DEFAULT NULL,
      Production_Start_Year            INT          DEFAULT NULL,
      Last_Sourced_Date                VARCHAR(15)  DEFAULT NULL,
      Last_Sourced_Oil_Prod_bbl        FLOAT        DEFAULT NULL,
      Last_Sourced_Gas_Prod_mcf        FLOAT        DEFAULT NULL,
      Last_Sourced_Condensate_Prod_bbl FLOAT        DEFAULT NULL,
      Last_Sourced_NGL_Prod_bbl        FLOAT        DEFAULT NULL,
      Drilling_Cost_Premium_pct        FLOAT        DEFAULT NULL,
      Peak_Cond_Prod_Rate_bd           FLOAT        DEFAULT NULL,
      Peak_NGL_Prod_Rate_bd            FLOAT        DEFAULT NULL,
      Calc_Lateral_Length_ft           FLOAT        DEFAULT NULL,
      County_Code                      VARCHAR(3)   DEFAULT NULL,
      Commodity                        VARCHAR(30)  DEFAULT NULL,
      Positive_Cash_Flow               VARCHAR(25)  DEFAULT NULL,
      Years_Since_Start                VARCHAR(25)  DEFAULT NULL,
      Cumulative_Cash_Flow             VARCHAR(25)  DEFAULT NULL,
      Payback_Determination            VARCHAR(25)  DEFAULT NULL,
      Total_Capex_MM_usd               FLOAT        DEFAULT NULL,
      Last_Sourced_Year                INT          DEFAULT NULL,
      Last_Prod_Date                   VARCHAR(15)  DEFAULT NULL,
      Total_Variable_Opex_MM_usd       FLOAT        DEFAULT NULL,
      Est_Lateral_Length               TINYINT      DEFAULT NULL,
      Est_Vertical_Depth               TINYINT      DEFAULT NULL,
      PRIMARY KEY (Well_ParametersID));
    
    CREATE INDEX well_api_indx ON tblUSWell_Parameters_{0} (API_Number);
    CREATE INDEX well_id_indx ON tblUSWell_Parameters_{0} (WellID);
    CREATE INDEX state_id_indx ON tblUSWell_Parameters_{0} (StateID);
    CREATE INDEX well_direction_indx ON tblUSWell_Parameters_{0} (Well_Direction);
    CREATE INDEX resource_play_indx ON tblUSWell_Parameters_{0} (Resource_Play);
    CREATE INDEX operator_indx ON tblUSWell_Parameters_{0} (Operator);
    """
	sql_update_2 = \
		"""
    SET IDENTITY_INSERT tblUSWell_Parameters_{0} ON;
    
    INSERT INTO tblUSWell_Parameters_{0} (Well_ParametersID,WellID,API_Number,StateID,State_Name,Well_Terrain,Well_Direction,Operator,Resource_Type,Resource_Play,Peak_Oil_Prod_Rate_bd,Peak_Gas_Prod_Rate_mmcfd,First_Production_Date,Peak_Oil_Prod_Date,Peak_Gas_Prod_Date,Last_Production_Date,True_Vertical_Depth_ft,Measured_Depth_ft,Lateral_Length_ft,Well_Cost_usd_ft,Well_EUR_Oil_bbl,Well_EUR_Gas_mmcf,Well_EUR_Condensate_bbl,Well_EUR_NGLs_bbl,Well_EUR_Total_boe,Pre_tax_NPV_usd,Pre_tax_IRR_pct,Pre_tax_BE_Oil_usd_bbl,Pre_tax_BE_Gas_usd_mcf,Pre_Tax_Cashflow_Total_usd,Post_tax_NPV_usd,Post_tax_IRR_pct,Post_tax_BE_Oil_usd_bbl,Post_tax_BE_Gas_usd_mcf,Post_Tax_Cashflow_Total_usd,Total_Opex_MM_usd,Cost_Capex_Drilling_MM_usd,Cost_Capex_Completion_MM_usd,Cost_Capex_Facilities_MM_usd,Cost_Capex_Abandonment_usd,Cost_Capex_Maintenance_usd,Cost_Opex_LOE_usd_boe,Cost_Opex_Water_usd_boe,Cost_Opex_GPT_usd_boe,Cost_Opex_NGL_usd_boe,Cost_Opex_Fixed_usd,Royalty_Rate_pct,Capex_Tangible_Split_pct,Decline_Param_Oil_Qi,Decline_Param_Oil_Di,Decline_Param_Oil_b,Decline_Param_Gas_Qi,Decline_Param_Gas_Di,Decline_Param_Gas_b,Years_Before_Terminal,Economic_Well_Life,Payback_Period,Initial_Water_Cut_pct,Hist_Oil_Decline_pct,Hist_Gas_Decline_pct,Hist_Cond_Decline_pct,Hist_NGL_Decline_pct,Relative_Peak_Oil_Date,Relative_Peak_Gas_Date,Relative_Peak_Cond_Date,Relative_Peak_NGL_Date,Oil_Prod_Decline_Months,Gas_Prod_Decline_Months,Cond_Prod_Decline_Months,NGL_Prod_Decline_Months,Oil_Decline_Rate_Type,Gas_Decline_Rate_Type,Cond_Decline_Rate_Type,NGL_Decline_Rate_Type,Completion_Cost_pct,Drilling_Cost_pct,Facilities_Cost_pct,Total_Well_Cost_MM_usd,LOE_Primary_usd_boe,GPT_Primary_usd_boe,Well_Status,Total_Fiscal_Take_usd,Total_Fiscal_Take_pct,Formation,Basin,Forecast_Well,Last_Econ_Year,State_Well_Direction,Avg_LOE_pct,AVG_GPT_pct,Cost_Opex_Production_usd_boe,Avg_Lateral_Length_ft,Avg_Well_Cost_mm_usd,Cost_Capex_Abandonment_usd_ft,Production_Start_Year,Last_Sourced_Date,Last_Sourced_Oil_Prod_bbl,Last_Sourced_Gas_Prod_mcf,Last_Sourced_Condensate_Prod_bbl,Last_Sourced_NGL_Prod_bbl,Drilling_Cost_Premium_pct,Peak_Cond_Prod_Rate_bd,Peak_NGL_Prod_Rate_bd,Calc_Lateral_Length_ft,County_Code,Commodity,Positive_Cash_Flow,Years_Since_Start,Cumulative_Cash_Flow,Payback_Determination,Total_Capex_MM_usd,Last_Sourced_Year,Last_Prod_Date,Total_Variable_Opex_MM_usd,Est_Lateral_Length,Est_Vertical_Depth)
      (SELECT DISTINCT Well_ParametersID,WellID,API_Number,StateID,State_Name,Well_Terrain,Well_Direction,Operator,Resource_Type,Resource_Play,Peak_Oil_Prod_Rate_bd,Peak_Gas_Prod_Rate_mmcfd,First_Production_Date,Peak_Oil_Prod_Date,Peak_Gas_Prod_Date,Last_Production_Date,True_Vertical_Depth_ft,Measured_Depth_ft,Lateral_Length_ft,Well_Cost_usd_ft,Well_EUR_Oil_bbl,Well_EUR_Gas_mmcf,Well_EUR_Condensate_bbl,Well_EUR_NGLs_bbl,Well_EUR_Total_boe,Pre_tax_NPV_usd,Pre_tax_IRR_pct,Pre_tax_BE_Oil_usd_bbl,Pre_tax_BE_Gas_usd_mcf,Pre_Tax_Cashflow_Total_usd,Post_tax_NPV_usd,Post_tax_IRR_pct,Post_tax_BE_Oil_usd_bbl,Post_tax_BE_Gas_usd_mcf,Post_Tax_Cashflow_Total_usd,Total_Opex_MM_usd,Cost_Capex_Drilling_MM_usd,Cost_Capex_Completion_MM_usd,Cost_Capex_Facilities_MM_usd,Cost_Capex_Abandonment_usd,Cost_Capex_Maintenance_usd,Cost_Opex_LOE_usd_boe,Cost_Opex_Water_usd_boe,Cost_Opex_GPT_usd_boe,Cost_Opex_NGL_usd_boe,Cost_Opex_Fixed_usd,Royalty_Rate_pct,Capex_Tangible_Split_pct,Decline_Param_Oil_Qi,Decline_Param_Oil_Di,Decline_Param_Oil_b,Decline_Param_Gas_Qi,Decline_Param_Gas_Di,Decline_Param_Gas_b,Years_Before_Terminal,Economic_Well_Life,Payback_Period,Initial_Water_Cut_pct,Hist_Oil_Decline_pct,Hist_Gas_Decline_pct,Hist_Cond_Decline_pct,Hist_NGL_Decline_pct,Relative_Peak_Oil_Date,Relative_Peak_Gas_Date,Relative_Peak_Cond_Date,Relative_Peak_NGL_Date,Oil_Prod_Decline_Months,Gas_Prod_Decline_Months,Cond_Prod_Decline_Months,NGL_Prod_Decline_Months,Oil_Decline_Rate_Type,Gas_Decline_Rate_Type,Cond_Decline_Rate_Type,NGL_Decline_Rate_Type,Completion_Cost_pct,Drilling_Cost_pct,Facilities_Cost_pct,Total_Well_Cost_MM_usd,LOE_Primary_usd_boe,GPT_Primary_usd_boe,Well_Status,Total_Fiscal_Take_usd,Total_Fiscal_Take_pct,Formation,Basin,Forecast_Well,Last_Econ_Year,State_Well_Direction,Avg_LOE_pct,AVG_GPT_pct,Cost_Opex_Production_usd_boe,Avg_Lateral_Length_ft,Avg_Well_Cost_mm_usd,Cost_Capex_Abandonment_usd_ft,Production_Start_Year,Last_Sourced_Date,Last_Sourced_Oil_Prod_bbl,Last_Sourced_Gas_Prod_mcf,Last_Sourced_Condensate_Prod_bbl,Last_Sourced_NGL_Prod_bbl,Drilling_Cost_Premium_pct,Peak_Cond_Prod_Rate_bd,Peak_NGL_Prod_Rate_bd,Calc_Lateral_Length_ft,County_Code,Commodity,Positive_Cash_Flow,Years_Since_Start,Cumulative_Cash_Flow,Payback_Determination,Total_Capex_MM_usd,Last_Sourced_Year,Last_Prod_Date,Total_Variable_Opex_MM_usd,Est_Lateral_Length,Est_Vertical_Depth
       FROM tblUSWell_Parameters WHERE Forecast_Well=7);
    
    SET IDENTITY_INSERT tblUSWell_Parameters_{0} OFF;
    """
	print '\t5.2 Copying Output Engine Parameters to table ...'
	if debug: print '\t', sql_update_1.format(engine_run_date)
	curr.execute(sql_update_1.format(engine_run_date))
	gd.commit(curr)
	
	if debug: print '\t', sql_update_2.format(engine_run_date)
	curr.execute(sql_update_2.format(engine_run_date))
	gd.commit(curr)
	print '\t5.2 Output Engine Parameters Copied'


# 5.3 Remove outliers from US_Wells.dbo.USWell_Parameters

def remove_outlier_data(curr, debug=False):
	sql_update = \
		"""
    UPDATE tblUSWell_Parameters SET True_Vertical_Depth_ft=NULL WHERE (True_Vertical_Depth_ft >= 35000) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Measured_Depth_ft=NULL WHERE (Measured_Depth_ft >= 35000) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Lateral_Length_ft=NULL WHERE (Lateral_Length_ft >= 35000) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Total_Well_Cost_MM_usd=NULL WHERE (Total_Well_Cost_MM_usd >= 20) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Cost_Capex_Abandonment_usd=NULL WHERE (Cost_Capex_Abandonment_usd >= 1000000) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Pre_Tax_NPV_usd=NULL WHERE (Pre_Tax_NPV_usd < -30000000 OR Pre_Tax_NPV_usd >= 50000000) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Post_Tax_NPV_usd=NULL WHERE (Post_Tax_NPV_usd < -30000000 OR Post_Tax_NPV_usd >= 50000000) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Pre_Tax_IRR_pct=NULL WHERE (-2 > Pre_Tax_IRR_pct OR Pre_Tax_IRR_pct >= 2) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Post_Tax_IRR_pct=NULL WHERE (-2 > Pre_Tax_IRR_pct OR Pre_Tax_IRR_pct >= 2) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Pre_Tax_BE_Oil_usd_bbl=NULL WHERE (-100 > Pre_Tax_BE_Oil_usd_bbl OR Pre_Tax_BE_Oil_usd_bbl >= 300) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Post_Tax_BE_Oil_usd_bbl=NULL WHERE (-100 > Post_Tax_BE_Oil_usd_bbl OR Post_Tax_BE_Oil_usd_bbl >= 300) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Pre_Tax_BE_Gas_usd_mcf=NULL WHERE (-30 > Pre_Tax_BE_Gas_usd_mcf OR Pre_Tax_BE_Gas_usd_mcf >= 100) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Post_Tax_BE_Gas_usd_mcf=NULL WHERE (-30 > Post_Tax_BE_Gas_usd_mcf OR Post_Tax_BE_Gas_usd_mcf >= 100) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Pre_Tax_Cashflow_Total_usd=NULL WHERE (Pre_Tax_Cashflow_Total_usd >= 50000000) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Post_Tax_Cashflow_Total_usd=NULL WHERE (Post_Tax_Cashflow_Total_usd >= 50000000) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Total_Fiscal_Take_usd=NULL WHERE (Total_Fiscal_Take_usd >= 50000000) AND Forecast_Well=7;
    UPDATE tblUSWell_Parameters SET Total_Fiscal_Take_pct=NULL WHERE (Total_Fiscal_Take_pct >= 2) AND Forecast_Well=7;
    """
	print '\t5.3 Removing Outliers from US_Wells.dbo.tblUSWell_Parameters table ...'
	if debug: print '\t', sql_update
	curr.execute(sql_update)
	gd.commit(curr)
	print '\t5.3 Outliers Removed from US_Wells.dbo.tblUSWell_Parameters'


# 5.4 Update US_Wells.dbo.tblUSWell_Last_Prod_Data

def update_last_prod_data_table(curr, debug=False):
	sql_update = \
		"""
    TRUNCATE TABLE tblUSWell_Last_Prod_Data;
    
    INSERT INTO tblUSWell_Last_Prod_Data (WellID, API_Number, Last_Sourced_Date, Last_Sourced_Prod)
      (SELECT DISTINCT WellID, API_Number, '2019-12-01', Last_Production_Date
       FROM tblUSWell_Parameters WHERE Forecast_Well=7);
    
    UPDATE tblUSWell_Last_Prod_Data SET API_Number=b.API_Number FROM tblUSWell_Last_Prod_Data a, tblUSWell_Parameters b WHERE a.WellID=b.WellID AND a.API_Number IS NULL;
    
    UPDATE tblUSWell_Last_Prod_Data SET Last_Sourced_Prod=b.Last_Prod_Date
      FROM tblUSWell_Last_Prod_Data a,
           (SELECT DISTINCT WellID, MAX(ProductionDate) AS Last_Prod_Date FROM tblUSWell_Production_Historical WHERE (ISNULL(Oil_bbl,0)+ISNULL(Gas_mcf,0)+ISNULL(Condensate_bbl,0)+ISNULL(Water_bbl,0))>0 GROUP BY WellID) b
      WHERE a.WellID=b.WellID;
    """
	print '\t5.4 Updating US_Wells.dbo.tblUSWell_Last_Prod_Data table...'
	if debug: print '\t', sql_update
	curr.execute(sql_update)
	gd.commit(curr)
	print '\t5.4 US_Wells.dbo.tblUSWell_Last_Prod_Data table Update Complete'


# 5.5 Update US_Wells.dbo.Well_Error_Log

def update_well_error_log(curr, engine_run_date, debug=False):
	print '\t5.5 Updating Well Error Log ...'
	forecast.main(error_report=True, error_date=engine_run_date, outliers=True, lateral_length=True, sourced_prod=True,
				  debug=debug)
	sql_update = \
		"""
    UPDATE Well_Error_Log SET Param_Value=b.Cost_Capex_Abandonment_usd
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Cost_Capex_Abandonment_usd' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Lateral_Length_ft
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Lateral_Length_ft' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Measured_Depth_ft
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Measured_Depth_ft' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Post_Tax_BE_Gas_usd_mcf
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Post_Tax_BE_Gas_usd_mcf' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Post_Tax_BE_Oil_usd_bbl
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Post_Tax_BE_Oil_usd_bbl' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Post_Tax_Cashflow_Total_usd
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Post_Tax_Cashflow_Total_usd' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Post_Tax_NPV_usd
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Post_Tax_NPV_usd' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Pre_Tax_BE_Gas_usd_mcf
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Pre_Tax_BE_Gas_usd_mcf' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Pre_Tax_BE_Oil_usd_bbl
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Pre_Tax_BE_Oil_usd_bbl' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Pre_Tax_Cashflow_Total_usd
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Pre_Tax_Cashflow_Total_usd' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Pre_Tax_IRR_pct
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Pre_Tax_IRR_pct' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Pre_Tax_NPV_usd
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Pre_Tax_NPV_usd' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Total_Fiscal_Take_pct
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Total_Fiscal_Take_pct' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Total_Fiscal_Take_usd
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Total_Fiscal_Take_usd' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.Total_Well_Cost_MM_usd
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='Total_Well_Cost_MM_usd' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    
    UPDATE Well_Error_Log SET Param_Value=b.True_Vertical_Depth_ft
      FROM Well_Error_Log a, tblUSWell_Parameters_{0} b
      WHERE a.Param_Name='True_Vertical_Depth_ft' AND a.WellID=b.WellID AND a.Error_Date='{0}';
    """
	if debug: print '\t', sql_update.format(engine_run_date)
	curr.execute(sql_update.format(engine_run_date))
	gd.commit(curr)
	
	sql_delete = \
		"""
    DELETE FROM Well_Error_Log WHERE Error_Code='01' AND Param_Value IS NULL;
    DELETE FROM Well_Error_Log WHERE Param_Name='True_Vertical_Depth_ft' AND Well_Direction='Horizontal';
    DELETE FROM Well_Error_Log WHERE Param_Name='Measured_Depth_ft' AND Well_Direction='Horizontal';
    DELETE FROM Well_Error_Log WHERE Param_Name='Lateral_length_ft' AND Well_Direction='Vertical';
    """
	curr.execute(sql_delete)
	gd.commit(curr)
	print '\t5.5 Well Error Log Complete'


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Stage 6 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 6.1 Export well parameters data

def export_well_parameters_data(show_query, texas_well_data=False, debug=False):
	if texas_well_data:
		export_query = \
			"""
		SELECT DISTINCT Well_ParametersID, WellID, API_Number, StateID, State_Name, Well_Terrain, Well_Direction, Operator, Resource_Type, Resource_Play, True_Vertical_Depth_ft, Measured_Depth_ft, Lateral_Length_ft, Well_Cost_usd_ft, Well_EUR_Oil_bbl, Well_EUR_Gas_mmcf, Well_EUR_Condensate_bbl, Well_EUR_NGLs_bbl, Well_EUR_Total_boe, Pre_tax_NPV_usd, Pre_tax_IRR_pct, Pre_tax_BE_Oil_usd_bbl, Pre_tax_BE_Gas_usd_mcf, Pre_Tax_Cashflow_Total_usd, Post_tax_NPV_usd, Post_tax_IRR_pct, Post_tax_BE_Oil_usd_bbl, Post_tax_BE_Gas_usd_mcf, Post_Tax_Cashflow_Total_usd, Total_Opex_MM_usd, Total_Capex_MM_usd, Cost_Capex_Drilling_MM_usd, Cost_Capex_Completion_MM_usd, Cost_Capex_Facilities_MM_usd, Cost_Capex_Abandonment_usd, Cost_Capex_Maintenance_usd, Cost_Opex_LOE_usd_boe, Cost_Opex_Water_usd_boe, Cost_Opex_GPT_usd_boe, Cost_Opex_NGL_usd_boe, Cost_Opex_Fixed_usd, Royalty_Rate_pct, Capex_Tangible_Split_pct, Decline_Param_Oil_Qi, Decline_Param_Oil_Di, Decline_Param_Oil_b, Decline_Param_Gas_Qi, Decline_Param_Gas_Di, Decline_Param_Gas_b, Years_Before_Terminal, Economic_Well_Life, Relative_Peak_Oil_Date, Relative_Peak_Gas_Date, Relative_Peak_Cond_Date, Relative_Peak_NGL_Date, Completion_Cost_pct, Drilling_Cost_pct, Facilities_Cost_pct, Total_Well_Cost_MM_usd, LOE_Primary_usd_boe, GPT_Primary_usd_boe, Well_Status, Total_Fiscal_Take_usd, Total_Fiscal_Take_pct, Formation, Basin, Last_Econ_Year, Last_Production_Date, Payback_Period, Total_Variable_Opex_MM_usd, IIF(WellID>90000000,1,0) AS New_Well
		   FROM US_Wells.dbo.tblUSWell_Parameters
		   WHERE Forecast_Well=7
		   AND API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Economics_Forecast)
		   AND API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Production_Forecast WHERE Sources IN ('EST: Forecast Engine'));
		"""
		if show_query: print 'US_Wells.dbo.tblUSWell_Parameters:\n{}'.format(export_query)
	else:
		export_query = \
			"""
		SELECT DISTINCT Well_ParametersID, WellID, API_Number, StateID, State_Name, Well_Terrain, Well_Direction, Operator, Resource_Type, Resource_Play, True_Vertical_Depth_ft, Measured_Depth_ft, Lateral_Length_ft, Well_Cost_usd_ft, Well_EUR_Oil_bbl, Well_EUR_Gas_mmcf, Well_EUR_Condensate_bbl, Well_EUR_NGLs_bbl, Well_EUR_Total_boe, Pre_tax_NPV_usd, Pre_tax_IRR_pct, Pre_tax_BE_Oil_usd_bbl, Pre_tax_BE_Gas_usd_mcf, Pre_Tax_Cashflow_Total_usd, Post_tax_NPV_usd, Post_tax_IRR_pct, Post_tax_BE_Oil_usd_bbl, Post_tax_BE_Gas_usd_mcf, Post_Tax_Cashflow_Total_usd, Total_Opex_MM_usd, Total_Capex_MM_usd, Cost_Capex_Drilling_MM_usd, Cost_Capex_Completion_MM_usd, Cost_Capex_Facilities_MM_usd, Cost_Capex_Abandonment_usd, Cost_Capex_Maintenance_usd, Cost_Opex_LOE_usd_boe, Cost_Opex_Water_usd_boe, Cost_Opex_GPT_usd_boe, Cost_Opex_NGL_usd_boe, Cost_Opex_Fixed_usd, Royalty_Rate_pct, Capex_Tangible_Split_pct, Decline_Param_Oil_Qi, Decline_Param_Oil_Di, Decline_Param_Oil_b, Decline_Param_Gas_Qi, Decline_Param_Gas_Di, Decline_Param_Gas_b, Years_Before_Terminal, Economic_Well_Life, Relative_Peak_Oil_Date, Relative_Peak_Gas_Date, Relative_Peak_Cond_Date, Relative_Peak_NGL_Date, Completion_Cost_pct, Drilling_Cost_pct, Facilities_Cost_pct, Total_Well_Cost_MM_usd, LOE_Primary_usd_boe, GPT_Primary_usd_boe, Well_Status, Total_Fiscal_Take_usd, Total_Fiscal_Take_pct, Formation, Basin, Last_Econ_Year, Last_Sourced_Date, Payback_Period, Total_Variable_Opex_MM_usd
		   FROM US_Wells.dbo.tblUSWell_Parameters
		   WHERE Forecast_Well=7
		   AND API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Economics_Forecast)
		   AND API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Production_Forecast WHERE Sources IN ('EST: Forecast Engine'));
		"""
		if show_query: print 'US_Wells.dbo.tblUSWell_Parameters:\n{}'.format(export_query)
	
	source_table = 'US_Wells.dbo.tblUSWell_Parameters'
	target_table = 'US_Wells_DataExtract.dbo.tblUSWell_Parameters'
	export_well_data(source_table, target_table, export_query, clear_data=True, debug=debug)


# 6.2 Export well economics forecast

def export_well_economics_forecast(show_query, texas_well_data=False, debug=False):
	if texas_well_data:
		export_query = \
			"""
        SELECT DISTINCT WellEconID, WellID, API_Number, State_Name, Prod_Year, Oil_Prod_bbl, Gas_Prod_mcf, Cond_Prod_bbl, NGL_Prod_bbl, Water_Prod_bbl, Total_Prod_boe, Gross_Revenue_usd, Capital_Expenditure_usd, Operating_Expenditure_usd, Pre_Tax_Cashflow_usd, Post_Tax_Cashflow_usd, Discount_Pre_Tax_Cashflow_usd, Discount_Post_Tax_Cashflow_usd, Oil_Revenue_usd, Gas_Revenue_usd, Condensate_Revenue_usd, NGL_Revenue_usd, Net_Revenue_usd, Production_Tax_Value_usd, Depreciation_Value_usd, Tangible_Capex_usd, Intangible_Capex_usd, Abandonment_usd, Variable_Opex_usd, Fixed_Opex_usd, Net_Income_usd, State_Tax_Rate_pct, State_Tax_Value_usd, Federal_Tax_Value_usd, Fiscal_Take_usd, NGL_Price_usd_bbl, Oil_Price_usd_bbl, Gas_Price_usd_mcf, Cond_Price_usd_bbl, Positive_Cash_Flow, Years_Since_Start, Cumulative_Cash_Flow, Payback_Determination, Payback_Period, IIF(WellID>90000000,1,0) AS New_Well
        FROM US_Wells.dbo.tblUSWell_Economics_Forecast
          WHERE API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Parameters
                               WHERE Forecast_Well=7
                               AND API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Production_Forecast WHERE Sources='EST: Forecast Engine'));
        """
	else:
		export_query = \
			"""
        SELECT * FROM US_Wells.dbo.tblUSWell_Economics_Forecast
          WHERE API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Parameters
                               WHERE Forecast_Well=7
                               AND API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Production_Forecast WHERE Sources='EST: Forecast Engine'));
        """
	if show_query: print 'US_Wells.dbo.tblUSWell_Economics_Forecast:\n{}'.format(export_query)
	
	source_table = 'US_Wells.dbo.tblUSWell_Economics_Forecast'
	target_table = 'US_Wells_DataExtract.dbo.tblUSWell_Economics_Forecast'
	export_well_data(source_table, target_table, export_query, clear_data=True, debug=debug)


# 6.3 Export well production forecast

def export_well_production_forecast(show_query, texas_well_data=False, debug=False):
	if texas_well_data:
		export_query = \
			"""
			SELECT WellProductionID,WellID,API_Number,StateID,Period,Gas_Total_mcf,Oil_Total_bbl,Water_Total_bbl,NGL_Total_bbl,Condensate_Total_bbl,Gas_Jan_mcf,Gas_Feb_mcf,Gas_Mar_mcf,Gas_Apr_mcf,Gas_May_mcf,Gas_Jun_mcf,Gas_Jul_mcf,Gas_Aug_mcf,Gas_Sep_mcf,Gas_Oct_mcf,Gas_Nov_mcf,Gas_Dec_mcf,Oil_Jan_bbl,Oil_Feb_bbl,Oil_Mar_bbl,Oil_Apr_bbl,Oil_May_bbl,Oil_Jun_bbl,Oil_Jul_bbl,Oil_Aug_bbl,Oil_Sep_bbl,Oil_Oct_bbl,Oil_Nov_bbl,Oil_Dec_bbl,Water_Jan_bbl,Water_Feb_bbl,Water_Mar_bbl,Water_Apr_bbl,Water_May_bbl,Water_Jun_bbl,Water_Jul_bbl,Water_Aug_bbl,Water_Sep_bbl,Water_Oct_bbl,Water_Nov_bbl,Water_Dec_bbl,NGL_Jan_bbl,NGL_Feb_bbl,NGL_Mar_bbl,NGL_Apr_bbl,NGL_May_bbl,NGL_Jun_bbl,NGL_Jul_bbl,NGL_Aug_bbl,NGL_Sep_bbl,NGL_Oct_bbl,NGL_Nov_bbl,NGL_Dec_bbl,Condensate_Jan_bbl,Condensate_Feb_bbl,Condensate_Mar_bbl,Condensate_Apr_bbl,Condensate_May_bbl,Condensate_Jun_bbl,Condensate_Jul_bbl,Condensate_Aug_bbl,Condensate_Sep_bbl,Condensate_Oct_bbl,Condensate_Nov_bbl,Condensate_Dec_bbl,Sources, IIF(WellID>90000000,1,0) AS New_Well
			FROM US_Wells.dbo.tblUSWell_Production_Forecast
			  WHERE API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Parameters
								   WHERE Forecast_Well=7
								   AND API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Economics_Forecast)) AND Sources='EST: Forecast Engine';
			"""
	else:
		export_query = \
			"""
			SELECT WellProductionID,WellID,API_Number,StateID,Period,Gas_Total_mcf,Oil_Total_bbl,Water_Total_bbl,NGL_Total_bbl,Condensate_Total_bbl,Gas_Jan_mcf,Gas_Feb_mcf,Gas_Mar_mcf,Gas_Apr_mcf,Gas_May_mcf,Gas_Jun_mcf,Gas_Jul_mcf,
			       Gas_Aug_mcf,Gas_Sep_mcf,Gas_Oct_mcf,Gas_Nov_mcf,Gas_Dec_mcf,Oil_Jan_bbl,Oil_Feb_bbl,Oil_Mar_bbl,Oil_Apr_bbl,Oil_May_bbl,Oil_Jun_bbl,Oil_Jul_bbl,Oil_Aug_bbl,Oil_Sep_bbl,Oil_Oct_bbl,Oil_Nov_bbl,Oil_Dec_bbl,Water_Jan_bbl,
			       Water_Feb_bbl,Water_Mar_bbl,Water_Apr_bbl,Water_May_bbl,Water_Jun_bbl,Water_Jul_bbl,Water_Aug_bbl,Water_Sep_bbl,Water_Oct_bbl,Water_Nov_bbl,Water_Dec_bbl,NGL_Jan_bbl,NGL_Feb_bbl,NGL_Mar_bbl,NGL_Apr_bbl,NGL_May_bbl,
			       NGL_Jun_bbl,NGL_Jul_bbl,NGL_Aug_bbl,NGL_Sep_bbl,NGL_Oct_bbl,NGL_Nov_bbl,NGL_Dec_bbl,Condensate_Jan_bbl,Condensate_Feb_bbl,Condensate_Mar_bbl,Condensate_Apr_bbl,Condensate_May_bbl,Condensate_Jun_bbl,Condensate_Jul_bbl,
			       Condensate_Aug_bbl,Condensate_Sep_bbl,Condensate_Oct_bbl,Condensate_Nov_bbl,Condensate_Dec_bbl,Sources
			  FROM US_Wells.dbo.tblUSWell_Production_Forecast
			  WHERE API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Parameters
								   WHERE Forecast_Well=7
								   AND API_Number IN (SELECT DISTINCT API_Number FROM US_Wells.dbo.tblUSWell_Economics_Forecast)) AND Sources='EST: Forecast Engine';
			"""
	if show_query: print 'US_Wells.dbo.tblUSWell_Production_Forecast:\n{}'.format(export_query)
	
	source_table = 'US_Wells.dbo.tblUSWell_Production_Forecast'
	target_table = 'US_Wells_DataExtract.dbo.tblUSWell_Production_Forecast'
	export_well_data(source_table, target_table, export_query, clear_data=True, debug=debug)


# 6.4 Export well error log

def export_well_error_log(show_query, engine_run_date, debug=False):
	export_query = \
		"""
    SELECT DISTINCT ID, WellID, API_Number, State_Name, Well_Direction, Well_Status, Basin, Formation, Resource_Play, Operator, Commodity, Error_Code, Error_Name, Param_Name, Param_Min, Param_Value, Param_Max, Error_Date
      FROM Well_Error_Log
      WHERE Error_Date='{}';
    """
	if show_query: print 'US_Wells.dbo.Well_Error_Log: \n{}'.format(export_query.format(engine_run_date))
	
	source_table = 'US_Wells.dbo.Well_Error_Log'
	target_table = 'US_Wells_DataExtract.dbo.tblUSWell_Error_Log_{}'.format(gd.get_date())
	export_well_data(source_table, target_table, export_query, clear_data=False, debug=debug)


def export_new_texas_well_details(show_query, texas_well_data=False, debug=False):
	export_query = \
		"""
    SELECT DISTINCT well_id AS WellID, api_number, drill_permit_no AS Permit_Number, Operator, county, 'Texas' AS [State], lease_name, 
                    formation AS Target_Formation, resource_play AS Shale, 'Onshore' AS Well_Terrain, well_status, well_direction, 'Oil & Gas Well' AS Well_Classification,
                    14 AS Well_Classification_ID, IIF(commodity='O','Oil',IIF(commodity='G','Gas',NULL)) AS Commodity, measured_depth AS Measured_Depth_ft,
                    true_vertical_depth AS true_vertical_depth_ft, spud_date, completion_date AS completion_start_date, first_production_date, last_production_date AS Last_Historical_Production_Date,
                    top_perforation, bottom_perforation, operator AS ParentOperator, lease_no AS Lease_number, lateral_length AS lateral_length_ft, tx_well_id
      FROM US_Wells_Texas.dbo.tx_well_details WHERE well_id > 90000000 AND well_id IN (SELECT DISTINCT WellID FROM tblUSWell_Parameters WHERE Forecast_Well=7);
    """
	if show_query: print 'US_Wells_DataExtract.dbo.tblUSWell_Texas_New_Well_Details: {}'.format(export_query)
	
	source_table = 'US_Wells.dbo.tblUSWell_Parameters'
	target_table = 'US_Wells_DataExtract.dbo.tblUSWell_Parameters'
	export_well_data(source_table, target_table, export_query, clear_data=True, debug=debug)


# -----------------------------------------------------------------------------------------------------------------------------

def main(
		import_details=False, extract_details=False, import_data=False, update_details=False,
		import_prod=False,
		update_well_id_api=False,
		update_prod=False, update_prod_insert=False, update_prod_data=False,
		update_forecast=False, update_forecast_insert=False, update_forecast_data=False,
		update_params=False, update_params_insert=False, update_params_data=False, update_params_last_prod=False,
		engine_group='non_tx', all_tx=False,
		update_assum=False, update_assum_export=False, update_assum_import=False, update_assum_data=False,
		pre_engine_params=False,
		choose_assum=False,
		est_len_params=False, est_len_params_lat_len=False, est_len_params_tvd=False,
		update_well_costs=False, well_cost_update=False, well_cost_calc=False,
		forecast_prod=False,
		forecast_econ=False,
		post_engine_params=False,
		copy_engine_params=False,
		remove_outliers=False,
		update_last_prod_data=False,
		update_error_log=False,
		export_params=False,
		export_econ=False,
		export_prod=False,
		export_error_log=False,
		texas_well_data=False,
		forecast_codes=[1, 4, 5, 6, 9],
		split_well_list=False,
		show_export_queries=False,
		debug=False):
	conn = gd.get_connection(server='sql_server', database='US_Wells', us_wells=True)
	curr = conn.cursor()
	
	well_id_list = []
	forecast_count = 0
	engine_group_num = 0
	engine_run_date = gd.get_date()
	start_time = gd.get_datetime()
	
	print 'Engine Start Time: {}'.format(start_time)
	
	if split_well_list and (pre_engine_params or choose_assum or est_len_params or forecast_prod or forecast_econ):
		# Get current engine group to split well list and increment for next concurrent engine task
		engine_group_num = gd.get_engine_group()
		gd.incr_engine_group()
	
	# ------------------------------------------------------------------------------
	# Stage 1 ----------------------------------------------------------------------
	
	# 1.1 Import well details data -------------------------------------------------
	if import_details:
		import_details_start = gd.get_datetime()
		print '1.1 Importing well details data ...'
		print '\t1.1 Start time: {}'.format(import_details_start)
		
		import_well_details(curr, extract=extract_details, import_data=import_data, update=update_details, debug=debug)
		
		import_details_end = gd.get_datetime()
		print '\t1.1 End time: {}'.format(import_details_end)
		print '\t1.1 Total processing time: {}\n'.format(gd.elapsed_time(import_details_start, import_details_end))
	
	# 1.2 Import well production data ----------------------------------------------
	if import_prod:
		update_details_start = gd.get_datetime()
		print '1.2 Importing well production data ...'
		print '\t1.2 Start time: {}'.format(update_details_start)
		
		import_well_production(curr, debug=debug)
		
		update_details_end = gd.get_datetime()
		print '\t1.2 End time: {}'.format(update_details_end)
		print '\t1.2 Total processing time: {}\n'.format(gd.elapsed_time(update_details_start, update_details_end))
	
	# ------------------------------------------------------------------------------
	# Stage 2 ----------------------------------------------------------------------
	
	# 2.1 Update US_Wells.dbo.tblmaster_WellID_API_Number
	if update_well_id_api:
		# 00:01:24 total processing time 20200712
		update_well_id_api_start = gd.get_datetime()
		print '2.1 Updating US_Wells.dbo.tblmaster_WellID_API_Number ...'
		print '\t2.1 Start time: {}'.format(update_well_id_api_start)
		
		update_well_id_api_table(curr, debug=debug)
		
		update_well_id_api_end = gd.get_datetime()
		print '\t2.1 End time: {}'.format(update_well_id_api_end)
		print '\t2.1 Total processing time: {}\n'.format(
			gd.elapsed_time(update_well_id_api_start, update_well_id_api_end))
	
	# 2.2 Update US_Wells.dbo.tblUSWell_Production ---------------------------------
	if update_prod:
		# 03:31:44 total processing time 20200606
		# 02:10:00 total processing time 20200712
		update_prod_start = gd.get_datetime()
		print '2.2 Updating US_Wells.dbo.tblUSWell_Production table ...'
		print '\t2.2 Start time: {}'.format(update_prod_start)
		
		update_production_tables(curr, insert=update_prod_insert, update=update_prod_data, debug=debug)
		
		update_prod_end = gd.get_datetime()
		print '\t2.2 End time: {}'.format(update_prod_end)
		print '\t2.2 Total processing time: {}\n'.format(gd.elapsed_time(update_prod_start, update_prod_end))
	
	# 2.3 Update US_Wells.dbo.tblUSWell_Production_Forecast ------------------------
	if update_forecast:
		# 00:15:09 total processing time 20200606
		update_forecast_start = gd.get_datetime()
		print 'Updating US_Wells.dbo.tblUSWell_Production_Forecast ...'
		print '\tStart time: {}'.format(update_forecast_start)
		
		update_production_forecast_table(curr, insert=update_forecast_insert, update=update_forecast_data, debug=debug)
		
		update_forecast_end = gd.get_datetime()
		print '\tEnd time: {}'.format(update_forecast_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(update_forecast_start, update_forecast_end))
	
	# 2.4 Update US_Wells.dbo.tblUSWell_Parameters ---------------------------------
	if update_params:
		# 00:08:28 total processing time 20200606
		# 00:11:51 total processing time 20200712
		update_params_start = gd.get_datetime()
		print 'Updating US_Wells.dbo.tblUSWell_Parameters ...'
		print '\tStart time: {}'.format(update_params_start)
		
		update_parameters_table(curr, insert=update_params_insert, update=update_params_data,
								last_prod=update_params_last_prod, engine_group=engine_group, all_tx=all_tx, debug=debug)
		
		update_params_end = gd.get_datetime()
		print '\tEnd time: {}'.format(update_params_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(update_params_start, update_params_end))
	
	# 2.5 Update US_Wells.dbo.tblUSWell_Assumptions --------------------------------
	if update_assum:
		update_assum_start = gd.get_datetime()
		print 'Updating US_Wells.dbo.tblUSWell_Assumptions ...'
		print '\tStart time: {}'.format(update_assum_start)
		
		update_assumptions_table(export_data=update_assum_export, import_data=update_assum_import,
								 update=update_assum_data, debug=debug)
		
		update_assum_end = gd.get_datetime()
		print '\tEnd time: {}'.format(update_assum_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(update_assum_start, update_assum_end))
	
	# ------------------------------------------------------------------------------
	# Stage 3 ----------------------------------------------------------------------
	
	# 3.1 Update pre-engine well parameters ----------------------------------------
	if pre_engine_params:
		pre_engine_params_start = gd.get_datetime()
		print 'Updating pre-engine well parameters ...'
		print '\tStart time: {}'.format(pre_engine_params_start)
		
		well_id_list, forecast_count = get_well_list_data(forecast_codes=forecast_codes, debug=debug)
		update_well_parameters(well_id_list, forecast_count, split_well_list, engine_group_num, debug=debug)
		
		pre_engine_params_end = gd.get_datetime()
		print '\tEnd time: {}'.format(pre_engine_params_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(pre_engine_params_start, pre_engine_params_end))
	
	# 3.2 Choose well assumptions --------------------------------------------------
	if choose_assum:
		pre_engine_params_start = gd.get_datetime()
		print 'Choosing well assumptions ...'
		print '\tStart time: {}'.format(pre_engine_params_start)
		
		well_id_list, forecast_count = get_well_list_data(forecast_codes=[1, 4, 5, 6, 9], debug=debug)
		choose_well_assumptions(well_id_list, forecast_count, split_well_list, engine_group_num, debug=debug)
		
		pre_engine_params_end = gd.get_datetime()
		print '\tEnd time: {}'.format(pre_engine_params_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(pre_engine_params_start, pre_engine_params_end))
	
	# 3.3 Estimate length parameters -----------------------------------------------
	if est_len_params:
		est_len_params_start = gd.get_datetime()
		print 'Estimating length parameters ...'
		print '\tStart time: {}'.format(est_len_params_start)
		
		if est_len_params_lat_len:
			well_id_list, forecast_count = get_well_list_data(forecast_codes=[5], debug=debug)
			est_length_params(well_id_list, forecast_count, length_param='lateral_length_ft',
							  split_well_list=split_well_list, engine_group=engine_group_num, debug=debug)
		
		if est_len_params_tvd:
			well_id_list, forecast_count = get_well_list_data(forecast_codes=[4], debug=debug)
			est_length_params(well_id_list, forecast_count, length_param='true_vertical_depth_ft',
							  split_well_list=split_well_list, engine_group=engine_group_num, debug=debug)
		
		est_len_params_end = gd.get_datetime()
		print '\tEnd time: {}'.format(est_len_params_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(est_len_params_start, est_len_params_end))
	
	# 3.4 Update vertical well costs -----------------------------------------------
	if update_well_costs:
		update_well_costs_start = gd.get_datetime()
		print 'Updating vertical well costs ...'
		print '\tStart time: {}'.format(update_well_costs_start)
		
		well_id_list, forecast_count = get_well_list_data(forecast_codes=[4, 6], debug=debug)
		update_vert_well_costs(update_cost_data=well_cost_update, calc_well_costs=well_cost_calc, debug=debug)
		
		update_well_costs_end = gd.get_datetime()
		print '\tEnd time: {}'.format(update_well_costs_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(update_well_costs_start, update_well_costs_end))
	
	# ------------------------------------------------------------------------------
	# Stage 4 ----------------------------------------------------------------------
	
	# 4.1 Forecast well production -------------------------------------------------
	if forecast_prod:
		forecast_prod_start = gd.get_datetime()
		print 'Forecasting well production ...'
		print '\tStart time: {}'.format(forecast_prod_start)
		
		sql_update = \
			"""
        UPDATE US_Wells.dbo.tblUSWell_Parameters 
          SET Last_Sourced_Year=b.Last_Sourced_Year
          FROM US_Wells.dbo.tblUSWell_Parameters a, 
               (SELECT DISTINCT WellID, API_Number, MAX([Period]) AS Last_Sourced_Year 
                 FROM US_Wells.dbo.tblUSWell_Production_Forecast
                 WHERE (ISNULL(Gas_Total_mcf,0)+ISNULL(Oil_Total_bbl,0)) > 0 AND Sources='Historical' GROUP BY WellID, API_Number) b 
          WHERE a.API_Number=b.API_Number AND a.WellID=b.WellID AND a.Forecast_Well IN (1,4,5,6,9) AND a.Last_Sourced_Year IS NULL;
        
        UPDATE US_Wells.dbo.tblUSWell_Parameters 
          SET Last_Sourced_Year=b.Last_Sourced_Year
          FROM US_Wells.dbo.tblUSWell_Parameters a, 
               (SELECT DISTINCT WellID, MAX([Period]) AS Last_Sourced_Year 
                 FROM US_Wells.dbo.tblUSWell_Production_Forecast
                 WHERE (ISNULL(Gas_Total_mcf,0)+ISNULL(Oil_Total_bbl,0)) > 0 AND Sources='Historical' GROUP BY WellID) b 
          WHERE a.WellID=b.WellID AND a.Forecast_Well IN (1,4,5,6,9) AND a.Last_Sourced_Year IS NULL;
        """
		curr.execute(sql_update)
		gd.commit(curr)
		
		well_id_list, forecast_count = get_well_list_data(forecast_codes=[1, 4, 5, 6, 9], debug=debug)
		forecast_production(well_id_list, forecast_count, split_well_list=split_well_list,
							engine_group=engine_group_num, debug=debug)
		
		forecast_prod_end = gd.get_datetime()
		print '\tEnd time: {}'.format(forecast_prod_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(forecast_prod_start, forecast_prod_end))
	
	# 4.2 Forecast well economics --------------------------------------------------
	if forecast_econ:
		forecast_econ_start = gd.get_datetime()
		print 'Forecasting well economics ...'
		print '\tStart time: {}'.format(forecast_econ_start)
		
		well_id_list, forecast_count = get_well_list_data(forecast_codes=[1, 4, 5, 6, 9], debug=debug)
		forecast_economics(well_id_list, forecast_count, split_well_list=split_well_list, engine_group=engine_group_num,
						   debug=debug)
		
		forecast_econ_end = gd.get_datetime()
		print '\tEnd time: {}'.format(forecast_econ_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(forecast_econ_start, forecast_econ_end))
	
	# ------------------------------------------------------------------------------
	# Stage 5 ----------------------------------------------------------------------
	
	# 5.1 Update post-engine well parameters ---------------------------------------
	if post_engine_params:
		# Reset well_engine_group to 0 for next engine run
		gd.reset_engine_group()
		
		post_engine_params_start = gd.get_datetime()
		print 'Updating post-engine well parameters ...'
		print '\tStart time: {}'.format(post_engine_params_start)
		
		update_post_engine_parameters(curr, debug=debug)
		
		post_engine_params_end = gd.get_datetime()
		print '\tEnd time: {}'.format(post_engine_params_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(post_engine_params_start, post_engine_params_end))
	
	# 5.2 Copy original US_Wells.dbo.USWell_Parameters to new table ----------------
	if copy_engine_params:
		copy_engine_params_start = gd.get_datetime()
		print 'Copying original US_Wells.dbo.USWell_Parameters to new table ...'
		print '\tStart time: {}'.format(copy_engine_params_start)
		
		copy_engine_parameters_data(curr, engine_run_date, debug=debug)
		
		copy_engine_params_end = gd.get_datetime()
		print '\tEnd time: {}'.format(copy_engine_params_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(copy_engine_params_start, copy_engine_params_end))
	
	# 5.3 Remove outliers from US_Wells.dbo.USWell_Parameters ----------------------
	if remove_outliers:
		remove_outliers_start = gd.get_datetime()
		print 'Removing outliers from US_Wells.dbo.USWell_Parameters ...'
		print '\tStart time: {}'.format(remove_outliers_start)
		
		remove_outlier_data(curr, debug=debug)
		
		remove_outliers_end = gd.get_datetime()
		print '\tEnd time: {}'.format(remove_outliers_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(remove_outliers_start, remove_outliers_end))
	
	# 5.4 Update US_Wells.dbo.tblUSWell_Last_Prod_Data -----------------------------
	if update_last_prod_data:
		update_last_prod_data_start = gd.get_datetime()
		print 'Updating US_Wells.dbo.tblUSWell_Last_Prod_Data ...'
		print '\tStart time: {}'.format(update_last_prod_data_start)
		
		update_last_prod_data_table(curr, debug=debug)
		
		update_last_prod_data_end = gd.get_datetime()
		print '\tEnd time: {}'.format(update_last_prod_data_end)
		print '\tTotal processing time: {}\n'.format(
			gd.elapsed_time(update_last_prod_data_start, update_last_prod_data_end))
	
	# 5.5 Update US_Wells.dbo.Well_Error_Log ---------------------------------------
	if update_error_log:
		update_error_log_start = gd.get_datetime()
		print 'Updating US_Wells.dbo.Well_Error_Log ...'
		print '\tStart time: {}'.format(update_error_log_start)
		
		update_well_error_log(curr, engine_run_date, debug=debug)
		
		update_error_log_end = gd.get_datetime()
		print '\tEnd time: {}'.format(update_error_log_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(update_error_log_start, update_error_log_end))
	
	# ------------------------------------------------------------------------------
	# Stage 6 ----------------------------------------------------------------------
	
	# 6.1 Export well parameters data ----------------------------------------------
	if export_params:
		export_params_start = gd.get_datetime()
		print 'Exporting well parameters data ...'
		print '\tStart time: {}'.format(export_params_start)
		
		export_well_parameters_data(show_query=show_export_queries, texas_well_data=texas_well_data, debug=debug)
		
		export_params_end = gd.get_datetime()
		print '\tEnd time: {}'.format(export_params_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(export_params_start, export_params_end))
	
	# 6.2 Export well economics forecast -------------------------------------------
	if export_econ:
		export_econ_start = gd.get_datetime()
		print 'Exporting well economics forecast ...'
		print '\tStart time: {}'.format(export_econ_start)
		
		export_well_economics_forecast(show_query=show_export_queries, debug=debug)
		
		export_econ_end = gd.get_datetime()
		print '\tEnd time: {}'.format(export_econ_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(export_econ_start, export_econ_end))
	
	# 6.3 Export well production forecast ------------------------------------------
	if export_prod:
		export_prod_start = gd.get_datetime()
		print 'Exporting well production forecast ...'
		print '\tStart time: {}'.format(export_prod_start)
		
		export_well_production_forecast(show_query=show_export_queries, debug=debug)
		
		export_prod_end = gd.get_datetime()
		print '\tEnd time: {}'.format(export_prod_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(export_prod_start, export_prod_end))
	
	# 6.4 Export well error log ----------------------------------------------------
	if export_error_log:
		export_error_log_start = gd.get_datetime()
		print 'Exporting well error log ...'
		print '\tStart time: {}'.format(export_error_log_start)
		
		export_well_error_log(show_query=show_export_queries, engine_run_date=engine_run_date, debug=debug)
		
		export_error_log_end = gd.get_datetime()
		print '\tEnd time: {}'.format(export_error_log_end)
		print '\tTotal processing time: {}\n'.format(gd.elapsed_time(export_error_log_start, export_error_log_end))
	
	# ------------------------------------------------------------------------------
	
	end_time = gd.get_datetime()
	print 'Engine End Time: {}'.format(end_time)
	print 'Total Engine Time: {}'.format(gd.elapsed_time(start_time, end_time))
	curr.close()
	conn.close()


if __name__ == '__main__':
	main(
		# Update tables
		import_details=False, extract_details=False, import_data=False, update_details=False,
		import_prod=False,
		update_well_id_api=False,
		update_prod=False, update_prod_insert=False, update_prod_data=True,
		update_forecast=False, update_forecast_insert=True, update_forecast_data=True,
		update_params=False, update_params_insert=True, update_params_data=True, update_params_last_prod=True,
		engine_group='non_tx', all_tx=False,
		
		# If assumptions need to be updated
		update_assum=False, update_assum_export=False, update_assum_import=False, update_assum_data=False,
		
		# Update Well parameters
		pre_engine_params=True,
		choose_assum=False,
		est_len_params=False, est_len_params_lat_len=False, est_len_params_tvd=False,
		
		# Update Well costs
		update_well_costs=False, well_cost_update=False, well_cost_calc=False,
		
		# Forecast well data
		forecast_prod=False,
		forecast_econ=False,
		
		# Post-process data
		post_engine_params=False,
		copy_engine_params=False,
		remove_outliers=False,
		update_last_prod_data=False,
		update_error_log=False,
		
		# Export data
		export_params=False,
		export_econ=False,
		export_prod=False,
		export_error_log=False,
		
		# Misc
		texas_well_data=False,
		forecast_codes=[1, 4, 5, 6, 9],
		split_well_list=True,
		show_export_queries=False,
		debug=False)
