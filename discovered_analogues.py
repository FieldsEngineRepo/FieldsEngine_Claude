from globaldata import *

use_capex_adj = True

global disc_field
disc_field = 0
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def clear_tables(curr, debug=False):
	curr.execute('DELETE FROM production WHERE add_by="Analogue"')
	curr.execute('TRUNCATE TABLE field_analogues')
	curr.execute('COMMIT')


def convert_values(curr, commodity, comm_prod, comm_unit, debug=False):
	factor = 1
	if commodity in ["Crude Oil", "Condensate", "NGL"]:
		if not comm_unit.upper() in ["BARRELS", "BOE"]:
			factor = convert_to_unit(curr, "Crude Oil", comm_unit)
	elif commodity in ["Natural Gas", "LNG"]:
		factor = convert_to_unit(curr, "Natural Gas", comm_unit)
	boe_prod = comm_prod * factor
	return boe_prod


def convert_to_unit(curr, commodity, unit, debug=False):
	sql_query = 'SELECT factor FROM unit_equals WHERE UPPER(commodity)="%s" and UPPER(unit)="%s" and UPPER(base_unit) = "BOE"'
	sql_query = sql_query % (commodity.upper().strip(), unit.upper().strip())
	curr.execute(sql_query)
	conversion_factor = curr.fetchone()[0]
	return conversion_factor


def save_error(curr, asset_id, comment, error_type, debug=False):
	session_key = get_session_key(curr)
	add_date = get_add_date()
	curr.execute('SELECT asset_name, country, constituent, region, status FROM asset_data WHERE asset_id=%s' % asset_id)
	asset_name, country, constituent, region, status = curr.fetchone()
	sql_insert = 'INSERT INTO error_log (asset_id, asset_name, country, constituent, region, status, comment, session_key, errortype, add_date) '
	sql_insert += 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	params = (asset_id, asset_name, country, constituent, region, status, comment, session_key, error_type, add_date)
	curr.execute(sql_insert, params)


def parse_params(var1, varType, data1, debug=False):
	lReturn = False
	if data1 is None or data1 == 'NULL':
		data1 = '0'
	else:
		if varType == 'R':
			if var1.count("<") > 0:
				pos = var1.index("<")
				val1 = var1[:pos]
				val2 = var1[pos + 1:]
				stmt1 = "int(" + val1 + ") <=  int(" + data1 + ")"
				stmt2 = "int(" + data1 + ") < int(" + val2 + ")"
				if eval(stmt1) and eval(stmt2):
					lReturn = True
			elif var1.count("-"):
				pos = var1.index("-")
				val1 = var1[:pos]
				val2 = var1[pos + 1:]
				stmt1 = "int(" + val1 + ") <=  int(" + data1 + ")"
				stmt2 = "int(" + data1 + ") <  int(" + val2 + ")"
				if eval(stmt1) and eval(stmt2):
					lReturn = True
			elif var1.count(">"):
				pos = var1.index(">")
				val2 = var1[pos + 1:]
				stmt2 = "int(" + data1 + ") >= int(" + val2 + ")"
				if eval(stmt2):
					lReturn = True
		elif varType == 'V':
			if data1.count(var1) > 0:
				lReturn = True
	return lReturn


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_session_key(curr, debug=False):
	curr.execute('SELECT run_id FROM global_variables WHERE id=1')
	run_id = curr.fetchone()[0]
	rand_int = str(random.randint(1000, 9999))
	session_key = 'analogue_%s_%s' % (run_id, rand_int)
	return session_key


def get_last_session_key(curr, asset_id, debug=False):
	sql_query = 'SELECT param_track_key FROM asset_data WHERE asset_id = %s' % asset_id
	curr.execute(sql_query)
	last_session_key = curr.fetchone()[0]
	return last_session_key


def get_in_place_reserve_fields(curr, debug=False):
	in_place_reserve_fields = []
	curr.execute('SELECT DISTINCT asset_id FROM asset_data WHERE NOT in_place_volume IS NULL ')
	in_place_reserve_fields = [int(data[0]) for data in curr.fetchall()]
	if debug:
		print 'in_place_reserve_fields:', in_place_reserve_fields
	return in_place_reserve_fields


def get_calorific_fields(curr, debug=False):
	calorific_fields = []
	curr.execute(
		'SELECT asset_id FROM asset_data WHERE NOT calorific="NULL" AND 950 <= calorific AND calorific <= 1150')
	calorific_fields = [int(data[0]) for data in curr.fetchall()]
	if debug:
		print 'calorific_fields:', calorific_fields
	return calorific_fields


def get_vintage_fields(curr, debug=False):
	vintage_fields = []
	curr.execute('SELECT asset_id FROM asset_data WHERE (field_age IS NULL) OR (field_age > 15)')
	vintage_fields = [int(data[0]) for data in curr.fetchall()]
	if debug:
		print 'vintage_fields:', vintage_fields
	return vintage_fields


def get_auxilary_param_fields(curr, param, debug=False):
	auxilary_param_fields = []
	sql_select = 'SELECT DISTINCT asset_id FROM asset_data WHERE NOT (%s IS NULL OR %s="NULL" OR %s=0.0 OR %s=0)' % (
		param, param, param, param)
	if debug:
		print 'sql_select (get_auxilary_param_fields):', sql_select
	curr.execute(sql_select)
	auxilary_param_fields = [int(data[0]) for data in curr.fetchall()]
	if debug:
		print '%s auxilary_param_fields:' % param, auxilary_param_fields
	return auxilary_param_fields


def get_analogue_fields(curr, asset_id, analogue_type, debug=False):
	sql_query = 'SELECT analogue_id FROM field_analogues WHERE asset_id=%s AND analogue_type="%s" '
	sql_query = sql_query % (asset_id, analogue_type)
	curr.execute(sql_query)
	analogue_fields = [int(field[0]) for field in curr.fetchall()]
	return analogue_fields


def get_analogue_data(curr, asset_id, debug=False):
	sql_query = 'SELECT country, region, terrain, resource_type, constituent, facility_type, operator, status, basin, peak_commodity, peak_prod '
	sql_query += 'FROM asset_data WHERE asset_id=%s'
	if debug:
		print 'sql_query:', (sql_query % asset_id)
	curr.execute(sql_query % asset_id)
	analogue_data = curr.fetchone()
	return analogue_data


def get_closest_analogue(curr, asset_id, analogue_type, rank, debug=False):
	sql_query = 'SELECT analogue_id FROM field_analogues WHERE asset_id=%s AND analogue_type="%s" '
	sql_query += 'ORDER BY analogue_score DESC'
	sql_query = sql_query % (asset_id, analogue_type)
	curr.execute(sql_query)
	closest_analogue = curr.fetchall()[rank - 1][0]
	return closest_analogue


def get_closest_params(curr, asset_id, param, analogue_type, debug=False):
	analogue_found = False
	rank = 1
	closest_params = None
	while not analogue_found:
		analogue_id = get_closest_analogue(curr, asset_id, analogue_type, rank)
		analogue_session_key = get_last_session_key(curr, analogue_id)
		param_list = PROD_PARAM_LISTS[param]
		param_str = ', '.join(param_list)
		sql_query = 'SELECT %s FROM param_track '
		sql_query = sql_query % param_str
		sql_query += 'WHERE session_key LIKE "%%%s" AND asset_id=%s'
		sql_query = sql_query % (analogue_session_key, analogue_id)
		curr.execute(sql_query)
		closest_params = curr.fetchall()[0]
		if None not in closest_params:
			analogue_found = True
		rank += 1
	return closest_params


def get_capacity_values(param_name, ast_id, mCur, mCountry, mRegion, mTerrain, mResource_type, mConstituent,
						mFacility_type, mOperator, mStatus, mBasin, extraWhere, extraVars, debug=False):
	param_type = ""
	debugMode = False
	if debugMode:
		print "In PARAMDETAIL "
		print extraWhere
		print extraVars
		print param_name
		print "+" * 25
		print mOperator
	# ----------------------------------------------------------------------------------------------------
	if extraVars == 'None':
		extraVars2 = 0
	else:
		extraVars2 = extraVars
	max_points = 0
	order_by = ""
	ret_val = ""
	mPoints = 0
	lAsset_id = 0
	lConstituent = 0
	lRegion = 0
	lCommodity = 0
	lResource_type = 0
	lTerrain = 0
	lFacility_type = 0
	lCountry = 0
	lStatus = 0
	lBasin = 0
	capacity_factor = 1
	capacity_target = 0
	param = []
	param_points = []
	param_ans = []
	param_tbl_ids = []
	capacity_vals = []
	# -----------------------------------------------------------------------------
	if debugMode:
		print "CAPEX OR OPEX CAPACITY"
		print "IN SQL----"
		print mStatus
	ret_val = 1
	param_type = "CAPACITY"
	p_num = 6
	id_num = 15
	sql_statement = '''SELECT
	ifnull(asset_id,""),
	ifnull(trim(constituent),""),
	ifnull(trim(region),""),
	ifnull(trim(resource_type),""),
	ifnull(trim(terrain),""),
	ifnull(trim(facility_type),""),
	trim(param_value),
	ifnull(trim(country),""),
	ifnull(trim(param_table),""),
	ifnull(trim(`status`),""),
	ifnull(trim(basin),""),
	ifnull(trim(operators),""),
	ifnull(trim(production_total),""),
	ifnull(trim(production_peak),""),
	ifnull(trim(params_id),""),
	ifnull(id,"")
	FROM model_rules WHERE UPPER(param_name) = %s '''
	order_by = "ORDER BY asset_id, operators, resource_type, facility_type, constituent, production_peak, terrain, country, region"
	sql_statement += order_by
	mCur.execute(sql_statement + ";", (param_name,))
	max_points = 50000 + 4000 + 750 + 600 + 500 + 100 + 100 + 50 + 10
	# -----------------------------------------------------------------------------
	r2 = mCur.fetchall()
	high_points = 0
	
	for datarow in r2:
		points_remaining = max_points
		mPoints = 0
		goAhead = 1
		extraParse = " goAhead "
		if debugMode:
			print "ID:", datarow[id_num]
		if len(datarow[13].strip()) > 0 and len(datarow[14].strip()) > 0 and len(datarow[6].strip()) > 0:
			fldParse = datarow[13]
			if fldParse.count(">") > 0:
				posDash = fldParse.index(">")
				fldVar2 = fldParse[posDash + 1:]
				extraParse += " and float(" + str(extraVars2) + ") > float(" + fldVar2 + ") "
			else:
				extraParse = " goAhead "
			if eval(extraParse):
				mPoints = 100
				if debugMode:
					print extraVars2
					print "CAPACITY PART 2 <--------------"
					print "MATCH FOUND ---> " + str(datarow[6])
				goAhead = 1
			else:
				goAhead = 0
		points_remaining -= 100
		# ------------------------------------------------------------------------------------------------
		if mPoints + points_remaining >= high_points:
			if datarow[0] is None or str(datarow[0]) == '0' or len(datarow[0].strip()) == 0:
				goAhead = 1
			else:
				if str(ast_id) == str(datarow[0]) and eval(extraParse):
					mPoints = 50000
					if debugMode:
						print str(datarow[6]) + " <-->" + datarow[2] + " Points " + str(mPoints)
					lAsset_id = 1
				else:
					goAhead = 0
					mPoints = 0
		else:
			pass
		points_remaining -= 50000
		# ------------------------------------------------------------------------------------------------
		# Operator = 4000 points
		if goAhead and mPoints + points_remaining >= high_points:
			if goAhead and len(datarow[11].strip()) > 0:
				if mOperator.strip().upper() == datarow[11].strip().upper() and eval(extraParse):
					mPoints += 4000
					if debugMode:
						print str(datarow[6]) + " - " + datarow[11] + " Operator phase " + str(mPoints)
				elif parse_params(datarow[11], 'V', mOperator) and eval(extraParse):
					print "Operator phase 2 " + "-^-" * 25
					mPoints += 4000
					if debugMode:
						print str(datarow[6]) + " - " + datarow[11] + " Operator phase " + str(mPoints)
				else:
					goAhead = 0
					mPoints = 0
			else:
				pass
		else:
			pass
		points_remaining -= 4000
		# ------------------------------------------------------------------------------------------------
		# Resource Type = 750 points
		if goAhead and mPoints + points_remaining >= high_points:
			if goAhead and len(datarow[3].strip()) > 0:
				if mResource_type.strip().upper() == datarow[3].strip().upper() and eval(extraParse):
					lResource_type = 1
					mPoints += 750
					if debugMode:
						print str(datarow[6]) + " - " + datarow[3] + " Resource type " + str(mPoints)
				else:
					goAhead = 0
					mPoints = 0
			else:
				pass
		else:
			pass
		points_remaining -= 750
		# ------------------------------------------------------------------------------------------------
		# Facility Type = 600 points
		if goAhead and mPoints + points_remaining >= high_points:
			if goAhead and len(datarow[5].strip()) > 0:
				if mFacility_type.strip().upper() == datarow[5].strip().upper() and eval(extraParse):
					lFacility_type = 1
					mPoints += 600
					if debugMode:
						print str(datarow[6]) + " - " + datarow[5] + " Facility type " + str(mPoints)
				else:
					goAhead = 0
					mPoints = 0
			else:
				pass
		else:
			pass
		points_remaining -= 600
		# ------------------------------------------------------------------------------------------------
		# Constituent = 500 points
		if goAhead and mPoints + points_remaining >= high_points:
			if len(datarow[1].strip()) > 0:
				if mConstituent.strip().upper() == datarow[1].strip().upper() and eval(extraParse):
					lConstituent = 1
					mPoints += 500
					if debugMode:
						print str(datarow[6]) + " - " + datarow[1] + " Constituent " + str(mPoints)
				else:
					goAhead = 0
					mPoints = 0
			else:
				pass
		#
		else:
			pass
		points_remaining -= 500
		# ------------------------------------------------------------------------------------------------
		# Terrain = 100 points
		if goAhead and mPoints + points_remaining >= high_points:
			if len(datarow[4].strip()) > 0:
				if mTerrain.strip().upper() == datarow[4].strip().upper() and eval(extraParse):
					lTerrain = 1
					mPoints += 100
					if debugMode:
						print str(datarow[6]) + " - " + datarow[4] + " Terrain " + str(mPoints)
				else:
					goAhead = 0
					mPoints = 0
			else:
				pass
		else:
			pass
		points_remaining -= 100
		# ------------------------------------------------------------------------------------------------
		# Country = 50 points
		if goAhead and mPoints + points_remaining >= high_points:
			if len(datarow[7].strip()) > 0:
				if mCountry.strip().upper() == datarow[7].strip().upper() and eval(extraParse):
					lCountry = 1
					mPoints += 50
					if debugMode:
						print str(datarow[6]) + " - " + datarow[7] + " Country " + str(mPoints)
				else:
					goAhead = 0
					mPoints = 0
			else:
				pass
		else:
			pass
		points_remaining -= 50
		# ------------------------------------------------------------------------------------------------
		# Region = 10 points
		if goAhead and mPoints + points_remaining >= high_points:
			if len(datarow[2].strip()) > 0:
				if mRegion.strip().upper() == datarow[2].strip().upper() and eval(extraParse):
					lRegion = 1
					mPoints += 10
					if debugMode:
						print str(datarow[6]) + " <-->" + datarow[2] + " Region " + str(mPoints)
				else:
					goAhead = 0
					mPoints = 0
			else:
				pass
		else:
			pass
		points_remaining -= 10
		if mPoints > high_points:
			high_points = mPoints
			param_points.append(mPoints)
			param_ans.append(datarow[p_num])
			param_tbl_ids.append(datarow[id_num])
			if len(datarow[14].strip()) > 0 and len(datarow[6].strip()) > 0:
				capacity_vals.append((datarow[14], float(datarow[6])))
			else:
				capacity_vals.append((1, 1))
			if debugMode:
				print "param_points:", param_points
				print "param_ans:", param_ans
				print "POINTS ----> " + str(mPoints)
				print extraParse
		mPoints = 0
	# ----------------------------------------------------------------------------------------------------
	if len(param_points) > 0:
		mPoints = max(param_points)
		fmIndex = param_points.index(mPoints)
		ret_val = param_ans[fmIndex]
		param_tbl_id = param_tbl_ids[fmIndex]
		
		capacity_target = float(eval(str(extraVars2) + capacity_vals[fmIndex][0]))
		capacity_factor = capacity_vals[fmIndex][1]
		if param_name == "CAPEX_CAPACITY":
			capexCapacityTarget = capacity_target
			capexCapacityFactor = capacity_factor
			if debugMode:
				print "CAPEX " + "#" * 25
				print capexCapacityTarget
				print capexCapacityFactor
		else:
			opexCapacityTarget = capacity_target
			opexCapacityFactor = capacity_factor
			if debugMode:
				print "\nOPEX " + "#" * 25
				print "ID:", datarow[id_num]
				print opexCapacityTarget
				print opexCapacityFactor
		if debugMode:
			print "param_points:", param_points
			print "param_ans:", param_ans
			print "param_tbl_ids:", param_tbl_ids
			print "*" * 25
			print "Param Table ID:", param_tbl_id
			print param_name + " chosen: " + str(ret_val)
			print fmIndex
			print "Points -->" + str(mPoints)
			print "------------------------------------------------------"
	return capacity_factor, capacity_target


def get_param_detail(curr, param_name, asset_id, extraWhere, extraVars, debug=False):
	curr.execute(
		'SELECT country, region, terrain, resource_type, constituent, facility_type, operator, status, basin FROM asset_data WHERE asset_id=%s' % asset_id)
	mCountry, mRegion, mTerrain, mResource_type, mConstituent, mFacility_type, mOperator, mStatus, mBasin = curr.fetchone()
	debugMode = debug
	param_type = ""
	# ----------------------------------------------------------------------------------------------------
	max_points = 0
	order_by = ""
	ret_val = ""
	mPoints = 0
	lAsset_id = 0
	lConstituent = 0
	lRegion = 0
	lCommodity = 0
	lResource_type = 0
	lTerrain = 0
	lFacility_type = 0
	lCountry = 0
	lStatus = 0
	lBasin = 0
	param = []
	param_points = []
	param_ans = []
	param_tbl_ids = []
	capacity_vals = []
	# ----------------------------------------------------------------------------------------------------
	if param_name == "PRICING":
		p_num = 8  # <-------------- if pricing return the table name
		id_num = 13
		mCommodity = extraWhere.upper()
		sql_statement = '''SELECT
		ifnull(asset_id,""),
		ifnull(trim(constituent),""),
		ifnull(trim(region),""),
		ifnull(trim(resource_type),""),
		ifnull(trim(terrain),""),
		ifnull(trim(facility_type),""),
		trim(param_value),
		ifnull(trim(country),""),
		ifnull(trim(param_table),""),
		space(1) as d1,
		space(2) as d2,
		space(3) as d3,
		ifnull(trim(production_total),""),
		ifnull(id,"")
		FROM model_rules WHERE UPPER(param_name) = %s and UPPER(commodity) = %s '''
		order_by = "ORDER BY asset_id, resource_type, facility_type, constituent, terrain, country, region "
		sql_statement += order_by
		curr.execute(sql_statement + ";", (param_name, mCommodity))
		# space(3) as d4
		max_points = 50000 + 750 + 600 + 500 + 100 + 50 + 10
	# ----------------------------------------------------------------------------------------------------
	elif param_name == "FISCAL":
		param_type = "MODEL_RULES"
		p_num = 6
		id_num = 14
		sql_statement = '''SELECT
		ifnull(asset_id, ""),
		ifnull(trim(constituent), ""),
		ifnull(trim(region), ""),
		ifnull(trim(resource_type), ""),
		ifnull(trim(terrain), ""),
		ifnull(trim(facility_type), ""),
		trim(param_value),
		ifnull(trim(country), ""),
		ifnull(trim(param_table), ""),
		ifnull(trim(status), ""),
		ifnull(trim(basin), ""),
		ifnull(trim(operators), ""),
		ifnull(trim(production_total), ""),
		ifnull(trim(production_peak), ""),
		ifnull(id,"")
		FROM model_rules WHERE UPPER(param_name) = %s and region = %s '''
		order_by = "ORDER BY asset_id, operators, resource_type, facility_type, constituent, production_peak, production_total, terrain, country, region, `status`, basin"
		sql_statement += order_by
		curr.execute(sql_statement + ";", (param_name, mRegion))
		max_points = 50000 + 4000 + 750 + 600 + 500 + 100 + 100 + 100 + 50 + 10 + 2 + 2
	# ----------------------------------------------------------------------------------------------------
	elif param_name in ["CAPEX_ALLOC", "CAPEX_REDEV_ALLOC", "ABANDONMENT_ALLOC"]:
		p_num = 6
		id_num = 6
		sql_statement = '''SELECT
		ifnull(asset_id,""),
		ifnull(trim(constituent),""),
		ifnull(trim(region),""),
		ifnull(trim(resource_type),""),
		ifnull(trim(terrain),""),
		ifnull(trim(facility_type),""),
		ifnull(id,""),
		ifnull(trim(country),""),
		space(1) as d0,
		ifnull(trim(status),""),
		ifnull(trim(basin),""),
		ifnull(trim(operators),""),
		ifnull(trim(production_total),""),
		ifnull(trim(production_peak),"")
		FROM '''
		sql_statement += param_name.lower() + ' '
		order_by = "ORDER BY asset_id, operators, production_peak, production_total, resource_type, facility_type, constituent, terrain, country, region, `status`, basin"
		sql_statement += order_by
		curr.execute(sql_statement + ";")
		max_points = 50000 + 4000 + 2020 + 2020 + 750 + 600 + 500 + 100 + 50 + 10 + 2 + 2
	# ----------------------------------------------------------------------------------------------------
	elif param_name == "MINIMUM_DAILY_PRODUCTION":
		p_num = 6
		id_num = 13
		sql_statement = '''SELECT
		ifnull(asset_id,""),
		ifnull(trim(constituent),""),
		ifnull(trim(region),""),
		ifnull(trim(resource_type),""),
		ifnull(trim(terrain),""),
		ifnull(trim(facility_type),""),
		trim(param_value),
		ifnull(trim(country),""),
		ifnull(trim(param_table),""),
		ifnull(trim(params_id),""),
		ifnull(trim(`status`),""),
		ifnull(trim(operators),""),
		ifnull(trim(prod_phase),""),
		ifnull(id,"")
		FROM model_rules WHERE UPPER(param_name) = %s '''
		order_by = "ORDER BY asset_id, params_id, operators, resource_type, facility_type, constituent, terrain, country, region"
		sql_statement += order_by
		curr.execute(sql_statement + ";", (param_name,))
		max_points = 50000 + 5000 + 4000 + 750 + 600 + 500 + 100 + 50 + 10
	# ----------------------------------------------------------------------------------------------------
	else:
		param_type = "MODEL_RULES"
		p_num = 6
		id_num = 14
		sql_statement = '''SELECT
		ifnull(asset_id,""),
		ifnull(trim(constituent),""),
		ifnull(trim(region),""),
		ifnull(trim(resource_type),""),
		ifnull(trim(terrain),""),
		ifnull(trim(facility_type),""),
		trim(param_value),
		ifnull(trim(country),""),
		ifnull(trim(param_table),""),
		ifnull(trim(`status`),""),
		ifnull(trim(basin),""),
		ifnull(trim(operators),""),
		ifnull(trim(production_total),""),
		ifnull(trim(production_peak),""),
		ifnull(id,"")
		FROM model_rules WHERE UPPER(param_name) = %s '''
		order_by = "ORDER BY asset_id, operators, resource_type, facility_type, constituent, production_peak, production_total, terrain, country, region, `status`, basin"
		sql_statement += order_by
		max_points = 50000 + 4000 + 750 + 600 + 500 + 100 + 100 + 100 + 50 + 10 + 2 + 2
		curr.execute(sql_statement + ";", (param_name,))
	# ----------------------------------------------------------------------------------------------------
	r2 = curr.fetchall()
	high_points = 0
	for datarow in r2:
		points_remaining = max_points
		mPoints = 0
		goAhead = 1
		extraParse = " goAhead "
		# ----------------------------------------------- CHECK FOR EVERY LINE
		if param_name == "MINIMUM_DAILY_PRODUCTION":
			# add code to parse the params_id field
			fldParse = datarow[9]
			if fldParse.count(">") > 0:
				#
				posDash = fldParse.index(">")
				fldVar2 = fldParse[posDash + 1:]
				extraParse = " float(" + str(extraWhere) + ") > float(" + fldVar2 + ") "
			elif fldParse.count("<") > 0:
				#
				posDash = fldParse.index("<")
				fldVar2 = fldParse[posDash + 1:]
				extraParse = " float(" + str(extraWhere) + ") < float(" + fldVar2 + ") "
			elif fldParse.count("-") > 0:
				posDash = fldParse.index("-")
				fldVar1 = fldParse[:posDash]
				fldVar2 = fldParse[posDash + 1:]
				extraParse = "  float(" + str(extraWhere) + ") <= float(" + fldVar1 + ") and float(" + \
							 str(extraWhere) + ") > float(" + fldVar2 + ") "
			else:
				extraParse = " goAhead "
			if eval(extraParse):
				mPoints = 5000
				goAhead = 1
			else:
				goAhead = 0
			
			points_remaining -= 5000
		# ------------------------------------------------------------------------------------------------
		elif param_name in ["CAPEX_ALLOC", "CAPEX_REDEV_ALLOC", "ABANDONMENT_ALLOC"]:
			if len(datarow[12].strip()) > 0 or len(datarow[13].strip()) > 0:
				if len(datarow[12].strip()) > 0:
					fldParse = datarow[12]
					col_x = extraWhere.index('-')
					extra1 = extraWhere[0:col_x]
					if fldParse.count(">") > 0:
						#
						posDash = fldParse.index(">")
						fldVar2 = fldParse[posDash + 1:]
						extraParse += " and float(" + str(extra1) + ") > float(" + fldVar2 + ") "
					elif fldParse.count("<") > 0:
						#
						posDash = fldParse.index("<")
						fldVar2 = fldParse[posDash + 1:]
						extraParse += " and float(" + str(extra1) + ") < float(" + fldVar2 + ") "
					elif fldParse.count("-") > 0:
						#
						posDash = fldParse.index("-")
						fldVar1 = fldParse[:posDash]
						fldVar2 = fldParse[posDash + 1:]
						extraParse += " and float(" + str(extra1) + ") <= float(" + fldVar1 + ") and float(" + \
									  str(extra1) + ") > float(" + fldVar2 + ") "
					if eval(extraParse):
						mPoints += 2020
				if len(datarow[13].strip()) > 0:
					fldParse = datarow[13]
					col_x = extraWhere.index('-')
					extra2 = extraWhere[col_x + 1:]
					if fldParse.count(">") > 0:
						#
						posDash = fldParse.index(">")
						fldVar2 = fldParse[posDash + 1:]
						extraParse += " and float(" + str(extra2) + ") > float(" + fldVar2 + ") "
					elif fldParse.count("<") > 0:
						#
						posDash = fldParse.index("<")
						fldVar2 = fldParse[posDash + 1:]
						extraParse += " and float(" + str(extra2) + ") < float(" + fldVar2 + ") "
					elif fldParse.count("-") > 0:
						#
						posDash = fldParse.index("-")
						fldVar1 = fldParse[:posDash]
						fldVar2 = fldParse[posDash + 1:]
						extraParse += " and float(" + str(extra2) + ") <= float(" + fldVar1 + ") and float(" + \
									  str(extra2) + ") > float(" + fldVar2 + ") "
					if eval(extraParse):
						mPoints += 2020
			else:
				goAhead = 1
			points_remaining -= 2020
		# ------------------------------------------------------------------------------------------------
		elif param_type == "MODEL_RULES":
			if len(datarow[12].strip()) > 0:
				fldParse = datarow[12]
				if fldParse.count(">") > 0:
					#
					posDash = fldParse.index(">")
					fldVar2 = fldParse[posDash + 1:]
					extraParse += " and float(" + str(extraWhere) + ") > float(" + fldVar2 + ") "
				elif fldParse.count("<") > 0:
					#
					posDash = fldParse.index("<")
					fldVar2 = fldParse[posDash + 1:]
					extraParse += " and float(" + str(extraWhere) + ") < float(" + fldVar2 + ") "
				elif fldParse.count("-") > 0:
					#
					posDash = fldParse.index("-")
					fldVar1 = fldParse[:posDash]
					fldVar2 = fldParse[posDash + 1:]
					extraParse += " and float(" + str(extraWhere) + ") <= float(" + fldVar1 + ") and float(" + str(
						extraWhere) + ") > float(" + fldVar2 + ") "
				else:
					extraParse = " goAhead "
				if eval(extraParse):
					mPoints = 100
					goAhead = 1
				else:
					goAhead = 0
			if len(datarow[13].strip()) > 0:
				fldParse = datarow[13]
				if fldParse.count(">") > 0:
					#
					posDash = fldParse.index(">")
					fldVar2 = fldParse[posDash + 1:]
					extraParse += " and float(" + str(extraWhere) + ") > float(" + fldVar2 + ") "
				elif fldParse.count("<") > 0:
					#
					posDash = fldParse.index("<")
					fldVar2 = fldParse[posDash + 1:]
					extraParse += " and float(" + str(extraWhere) + ") < float(" + fldVar2 + ") "
				elif fldParse.count("-") > 0:
					#
					posDash = fldParse.index("-")
					fldVar1 = fldParse[:posDash]
					fldVar2 = fldParse[posDash + 1:]
					extraParse += " and float(" + str(extraWhere) + ") <= float(" + fldVar1 + ") and float(" + str(
						extraWhere) + ") > float(" + fldVar2 + ") "
				else:
					extraParse = " goAhead "
				if eval(extraParse):
					mPoints = 100
					goAhead = 1
				else:
					goAhead = 0
			#
			points_remaining -= 200
		# ------------------------------------------------------------------------------------------------
		if mPoints + points_remaining >= high_points:
			if datarow[0] is None or str(datarow[0]) == '0' or len(datarow[0].strip()) == 0:
				goAhead = 1
			else:
				if str(asset_id) == str(datarow[0]) and eval(extraParse):
					mPoints += 50000
					lAsset_id = 1
				else:
					goAhead = 0
					mPoints = 0
		else:
			# continue
			pass
		points_remaining -= 50000
		# ------------------------------------------------------------------------------------------------
		# Operator = 4000 points
		if goAhead and mPoints + points_remaining >= high_points:
			if goAhead and len(datarow[11].strip()) > 0:
				if mOperator and mOperator.strip().upper() == datarow[11].strip().upper() and eval(extraParse):
					mPoints += 4000
				elif parse_params(datarow[11], 'V', mOperator) and eval(extraParse):
					mPoints += 4000
				else:
					# no match, do not advance, erase all points
					goAhead = 0
					mPoints = 0
			else:
				# no points, but move ahead
				pass
		#
		else:
			pass
		# continue
		if param_name != "PRICING":
			points_remaining -= 4000
		# ------------------------------------------------------------------------------------------------
		# Resource Type = 750 points
		if goAhead and mPoints + points_remaining >= high_points:
			if goAhead and len(datarow[3].strip()) > 0:
				if mResource_type and mResource_type.strip().upper() == datarow[3].strip().upper() and eval(extraParse):
					lResource_type = 1
					mPoints += 750
				else:
					# no match, do not advance, erase all points
					goAhead = 0
					mPoints = 0
			else:
				# no points, but move ahead
				pass
		else:
			# continue
			pass
		points_remaining -= 750
		# ------------------------------------------------------------------------------------------------
		# Facility Type = 600 points
		if goAhead and mPoints + points_remaining >= high_points:
			if goAhead and len(datarow[5].strip()) > 0:
				if mFacility_type and mFacility_type.strip().upper() == datarow[5].strip().upper() and eval(extraParse):
					lFacility_type = 1
					mPoints += 600
				else:
					# no match, do not advance, erase all points
					goAhead = 0
					mPoints = 0
			else:
				# no points, but move ahead
				pass
		else:
			# continue
			pass
		points_remaining -= 600
		# ------------------------------------------------------------------------------------------------
		# Constituent = 500 points
		if goAhead and mPoints + points_remaining >= high_points:
			if len(datarow[1].strip()) > 0:
				if mConstituent and mConstituent.strip().upper() == datarow[1].strip().upper() and eval(extraParse):
					lConstituent = 1
					mPoints += 500
				else:
					# no match, do not advance, erase all points
					goAhead = 0
					mPoints = 0
			else:
				# no points, but move ahead
				pass
		#
		else:
			# continue
			pass
		points_remaining -= 500
		# ------------------------------------------------------------------------------------------------
		# Terrain = 100 points
		if goAhead and mPoints + points_remaining >= high_points:
			if len(datarow[4].strip()) > 0:
				if mTerrain and mTerrain.strip().upper() == datarow[4].strip().upper() and eval(extraParse):
					lTerrain = 1
					mPoints += 100
				else:
					# no match, do not advance, erase all points
					goAhead = 0
					mPoints = 0
			else:
				# no points, but move ahead
				pass
		else:
			# continue
			pass
		points_remaining -= 100
		# ------------------------------------------------------------------------------------------------
		# Country = 50 points
		if goAhead and mPoints + points_remaining >= high_points:
			if len(datarow[7].strip()) > 0:
				if mCountry.strip().upper() == datarow[7].strip().upper() and eval(extraParse):
					lCountry = 1
					mPoints += 50
				else:
					# no match, do not advance, erase all points
					goAhead = 0
					mPoints = 0
			else:
				# no points, but move ahead
				pass
		else:
			# continue
			pass
		points_remaining -= 50
		# ------------------------------------------------------------------------------------------------
		# Region = 10 points
		if goAhead and mPoints + points_remaining >= high_points:
			if len(datarow[2].strip()) > 0:
				if mRegion and mRegion.strip().upper() == datarow[2].strip().upper() and eval(extraParse):
					lRegion = 1
					mPoints += 10
				else:
					# no match, do not advance, erase all points
					goAhead = 0
					mPoints = 0
			else:
				# no points, but move ahead
				pass
		else:
			# continue
			pass
		points_remaining -= 10
		# ------------------------------------------------------------------------------------------------
		# Status = 2 points
		if goAhead and mPoints + points_remaining >= high_points:
			if (param_type == "MODEL_RULES" or param_name in ["CAPEX_ALLOC", "CAPEX_REDEV_ALLOC",
															  "ABANDONMENT_ALLOC"]) and len(datarow[9].strip()) > 0:
				if mStatus and mStatus.strip().upper() == datarow[9].strip().upper() and eval(extraParse):
					lStatus = 1
					mPoints += 2
				else:
					# no match, do not advance, erase all points
					goAhead = 0
					mPoints = 0
			else:
				# no points, but move ahead
				pass
		# ------------------------------------------------------------------------------------------
		else:
			# continue
			pass
		if param_type == "MODEL_RULES" or param_name in ["CAPEX_ALLOC", "CAPEX_REDEV_ALLOC", "ABANDONMENT_ALLOC"]:
			points_remaining -= 2
		# ------------------------------------------------------------------------------------------------
		# Basin = 2 points
		if goAhead and mPoints + points_remaining >= high_points:
			if (param_type == "MODEL_RULES" or param_name in ["CAPEX_ALLOC", "CAPEX_REDEV_ALLOC",
															  "ABANDONMENT_ALLOC"]) and len(datarow[10].strip()) > 0:
				if mBasin and mBasin.strip().upper() == datarow[10].strip().upper() and eval(extraParse):
					lBasin = 1
					mPoints += 2
				else:
					# no match, do not advance, erase all points
					goAhead = 0
					mPoints = 0
			else:
				pass
		else:
			# continue
			pass
		if param_type == "MODEL_RULES" or param_name in ["CAPEX_ALLOC", "CAPEX_REDEV_ALLOC", "ABANDONMENT_ALLOC"]:
			points_remaining -= 2
		# ------------------------------------------------------------------------------------------------
		if mPoints > high_points:
			high_points = mPoints
			param_points.append(mPoints)
			param_ans.append(datarow[p_num])
			param_tbl_ids.append(datarow[id_num])
			if debugMode:
				print "param_points:", param_points
				print "param_ans:", param_ans
				print "POINTS ----> " + str(mPoints)
				print extraParse
		# check each criteria against the asset if there is a match add to the array
		mPoints = 0
	# ----------------------------------------------------------------------------------------------------
	if len(param_points) > 0:
		mPoints = max(param_points)
		fmIndex = param_points.index(mPoints)
		ret_val = param_ans[fmIndex]
		param_tbl_id = param_tbl_ids[fmIndex]
		if debugMode:
			print "param_points:", param_points
			print "param_ans:", param_ans
			print "param_tbl_ids:", param_tbl_ids
			print "*" * 25
			print "Param Table ID:", param_tbl_id
			print param_name + " chosen: " + str(ret_val)
			print fmIndex
			print "Points -->" + str(mPoints)
	sql_select = "SELECT year_minus5,year_minus4,year_minus3,year_minus2,year_minus1,year_0,year_1,year_2,year_3,year_4,year_5,year_6 FROM capex_alloc WHERE id = %s "
	
	return ret_val


def get_prod_data(curr, asset_id, prod_year, commodity, debug=False):
	sql_query = 'SELECT production, unit FROM production WHERE asset_id=%s AND period=%s AND NOT sources IN ("EST: Forecast Engine", "EST: Model Extraction") AND casetype="Base Case" '
	sql_query += 'AND commodity="%s" AND asset_relationship="Parent" AND data_source IN ("Engine", "Model") '
	sql_query = sql_query % (asset_id, prod_year, commodity)
	if debug:
		print '{} get_prod_data ({}): {} - {}'.format(asset_id, commodity, prod_year, sql_query)
	curr.execute(sql_query)
	comm_data = curr.fetchone()
	if comm_data is None:
		comm_data = (0, "")
	return comm_data


def get_comm_prod(curr, asset_id, commodity, last_session_key, stage, debug=False):
	if stage == 'first_production':
		sql_where = 'asset_id={} AND commodity="{}" AND sources!="EST: Forecast Engine" AND production > 0'.format(
			asset_id, commodity)
		prod_year = get_data('MIN(period)', 'production', cursor=curr, single_value=True, sql_where=sql_where)
		if debug:
			print' prod_year: {}'.format(prod_year)
		if prod_year != 'None':
			prod_year = int(prod_year)
		else:
			prod_year = get_param_value(curr, asset_id, stage, last_session_key, debug=debug)
	else:
		prod_year = get_param_value(curr, asset_id, stage, last_session_key, debug=debug)
	
	comm_prod, comm_unit = get_prod_data(curr, asset_id, prod_year, commodity, debug=debug)
	if comm_prod > 0:
		boe_prod = convert_values(curr, commodity, comm_prod, comm_unit)
	else:
		boe_prod = comm_prod
	
	return boe_prod


def get_commodity_data(curr, f_resource_type, f_country, f_formation, debug=False):
	formation_list = f_formation.split(';')
	formation_str = ' OR '.join(['formation LIKE "%%%s%%"'] * len(formation_list))
	formation_str = formation_str % tuple(formation_list)
	sql_select = 'SELECT resource_type, api_gravity, 0 AS reserve_volume, terrain, ablock, basin, country, region, status, formation, form_rock_type, trap_type, asset_id FROM asset_data '
	sql_select += 'WHERE asset_id IN (SELECT DISTINCT asset_id FROM assets WHERE upper(data_source) IN ("ENGINE", "MODEL") '
	sql_select += 'AND upper(asset_relation) = "PARENT" AND upper(status) in ("ANNOUNCED","PLANNED","PRODUCING","ABANDONED")) '
	sql_select += 'AND resource_type="%s" AND country="%s" AND (%s) AND peak_commodity IS NOT NULL'
	sql_select = sql_select % (f_resource_type, f_country, formation_str)
	if debug:
		print 'sql_select:', sql_select
	curr.execute(sql_select)
	commodity_assets = curr.fetchall()
	return commodity_assets


def get_analogue_scores(curr, field_id, analogue_id, debug=False):
	sql_select = 'SELECT analogue_id, analogue_score FROM field_analogues WHERE analogue_type="prod" AND asset_id=%s AND analogue_id=%s' % (
		field_id, analogue_id)
	curr.execute(sql_select)
	analogue_data = curr.fetchone()
	if debug:
		print field_id, analogue_data[0], analogue_data[1]
	return analogue_data


def get_analogue_commodities(curr, field_id, in_place, debug=False):
	if int(field_id) in get_calorific_fields(curr):
		commodities = ['Natural Gas']
	else:
		f_api_gravity, f_terrain, f_ablock, f_basin, f_country, f_region, f_status, f_resource_type, f_formation, f_form_rock_type, f_trap_type = get_field_data(
			curr, field_id, 'prod', in_place)
		f_facility_type, f_pipeline, f_gas_processing, f_oil_storage, f_gas_storage = (0, 0, 0, 0, 0)
		prod_asset_data = get_commodity_data(curr, f_resource_type, f_country, f_formation)
		closest_id = get_closest_analogue(curr, field_id, 'prod', 1)
		closest_analogue = (closest_id, 0)
		prod_analogues = get_analogue_fields(curr, field_id, 'prod')
		if prod_asset_data == ():
			comment = 'NO ASSETS FOUND WITH SAME COUNTRY (%s) AND FORMATION (%s) FOR COMMODITY MATCH' % (
				f_country, f_formation)
			error_type = 'ERROR TYPE 51'
			save_error(curr, field_id, comment, error_type)
			print comment
		for asset_data in prod_asset_data:
			if int(asset_data[-1]) in prod_analogues:
				analogue_data = get_analogue_scores(curr, field_id, asset_data[-1])
			else:
				analogue_data = (asset_data[-1], 0)
			if debug:
				print 'analogue_data:', analogue_data
			if analogue_data[1] > closest_analogue[1]:
				closest_analogue = analogue_data
		if debug:
			print 'closest_analogue:', closest_analogue
		closest_analogue_id = closest_analogue[0]
		sql_query = 'SELECT DISTINCT commodity FROM production WHERE asset_id=%s AND production > 0' % closest_analogue_id
		curr.execute(sql_query)
		commodities = [data[0] for data in curr.fetchall()]
	if debug:
		print 'analogue commodities:', commodities
	return commodities


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_param_value(curr, field, param, last_session_key, debug=False):
	PROD_COL_DATA = {
		'crude oil'  : 'crude',
		'natural gas': 'ng',
		'condensate' : 'condensate',
		'lng'        : 'lng',
		'ngl'        : 'ngl'
		
	}
	param_value = 0
	if 'capacity' in param:
		analogue_data = get_analogue_data(curr, field)
		analogue_data = analogue_data[:-1] + (str(analogue_data[-1]),)
		if 'factor' in param:
			param_value = get_capacity_values(param[:-7], field, curr, *analogue_data)[0]
		elif 'target' in param:
			param_value = get_capacity_values(param[:-7], field, curr, *analogue_data)[1]
	elif param in PROD_PARAM_LISTS['total_init_prod']:
		commodity = param[5:]
		comm_col = 'init_{}'.format(PROD_COL_DATA[commodity.lower()])
		# param_value = get_comm_prod(curr, field, commodity, last_session_key, 'first_production', debug=debug)
		param_value = get_data('IFNULL({},0)'.format(comm_col), 'asset_data', cursor=curr, datatype='float',
							   single_value=True, sql_where="asset_id={}".format(field))
	elif param in PROD_PARAM_LISTS['total_peak_prod']:
		commodity = param[5:]
		comm_col = 'peak_{}'.format(PROD_COL_DATA[commodity.lower()])
		# param_value = get_comm_prod(curr, field, commodity, last_session_key, 'peak_year', debug=debug)
		param_value = get_data('IFNULL({},0)'.format(comm_col), 'asset_data', cursor=curr, datatype='float',
							   single_value=True, sql_where="asset_id={}".format(field))
	elif param == 'capex_per_boe' and use_capex_adj:
		# sql_where = "asset_id={} AND session_key LIKE '%{}%'".format(field, last_session_key)
		sql_where = "asset_id={} AND session_key LIKE CONCAT('%',(SELECT DISTINCT run_id FROM global_variables WHERE id=1),'%')".format(field)
		param_value = get_data('IFNULL(capex_per_boe,0)*IFNULL(capex_adj_factor,1)', 'param_track', cursor=curr,
							   single_value=True, datatype='float', sql_where=sql_where, debug=debug)
	else:
		try:
			sql_query = 'SELECT %s FROM asset_data WHERE asset_id=%s AND param_track_key LIKE "%%%s"'
			sql_statement = sql_query % (param, field, last_session_key)
			curr.execute(sql_statement)
		except:
			sql_query = 'SELECT %s FROM param_track WHERE asset_id=%s AND session_key LIKE "%%%s"'
			sql_statement = sql_query % (param, field, last_session_key)
			curr.execute(sql_statement)
		param_val = curr.fetchone()
		if param_val is None:
			param_value = 0
		else:
			param_value = param_val[0]
	if not param_value: param_value = 0
	
	return param_value


def get_param_median(param_vals):
	param_median = 0
	if param_vals:
		param_list = sorted(param_vals, reverse=True)
		param_median = param_list[len(param_list) / 2]
	return param_median


def get_param_avg(curr, asset_id, param, analogue_type, debug=False):
	param_dict = {'capex_per_boe'         : {'total': 0, 'avg': 0},
				  'fixed_opex'            : {'total': 0, 'avg': 0},
				  'variable_opex_per_mmcf': {'total': 0, 'avg': 0},
				  'variable_opex_per_b'   : {'total': 0, 'avg': 0},
				  'abandonment'           : {'total': 0, 'avg': 0},
				  'capex_tangible_pct'    : {'total': 0, 'avg': 0},
				  'capex_redev'           : {'total': 0, 'avg': 0},
				  'opex_capacity_factor'  : {'total': 0, 'avg': 0},
				  'opex_capacity_target'  : {'total': 0, 'avg': 0},
				  'capex_capacity_factor' : {'total': 0, 'avg': 0},
				  'capex_capacity_target' : {'total': 0, 'avg': 0},
				  'recov_factor'          : {'total': 0, 'avg': 0},
				  'total_init_prod'       : {'commodities': {
					  'init_Crude Oil'  : {'total': [], 'avg': 0},
					  'init_Natural Gas': {'total': [], 'avg': 0},
					  'init_Condensate' : {'total': [], 'avg': 0},
					  'init_LNG'        : {'total': [], 'avg': 0},
					  'init_NGL'        : {'total': [], 'avg': 0}}},
				  'total_peak_prod'       : {'commodities': {
					  'peak_Crude Oil'  : {'total': [], 'avg': 0},
					  'peak_Natural Gas': {'total': [], 'avg': 0},
					  'peak_Condensate' : {'total': [], 'avg': 0},
					  'peak_LNG'        : {'total': [], 'avg': 0},
					  'peak_NGL'        : {'total': [], 'avg': 0}}},
				  'years_before_peak'     : {'total': 0, 'avg': 0},
				  'first_production'      : {'total': 0, 'avg': 0}}
	analogue_fields = get_analogue_fields(curr, asset_id, analogue_type, debug)
	num_fields = len(analogue_fields)
	return_val = 'Error'
	value_count = 1
	if debug:
		print 'analogue_fields: {}'.format(analogue_fields)
	for field in analogue_fields:
		if debug:
			print 'analogue field: {}'.format(field)
		last_session_key = get_last_session_key(curr, field)
		if param in ['total_init_prod', 'total_peak_prod']:
			return_val = []
			if debug:
				print '\ncommodities: {}'.format(param_dict[param]['commodities'].keys())
			for commodity in param_dict[param]['commodities'].keys():
				if debug:
					print '%s--commodity: %s' % (asset_id, commodity)
				if get_param_value(curr, field, commodity, last_session_key, debug) != 0:
					if debug: print field, ':', get_param_value(curr, field, commodity, last_session_key)
					param_dict[param]['commodities'][commodity]['total'].append(
						get_param_value(curr, field, commodity, last_session_key))
					param_dict[param]['commodities'][commodity]['avg'] = get_param_median(param_dict[param]['commodities'][commodity]['total'])
					if debug:
						print '{} {} commodity total data: {}'.format(commodity, param,
																	  param_dict[param]['commodities'][commodity][
																		  'total'])
						print '{} {} commodity avg data: {}\n'.format(commodity, param,
																	  param_dict[param]['commodities'][commodity][
																		  'avg'])
				
				if len(param_dict[param]['commodities'][commodity]['total']) > 2:
					return_val.append((round(param_dict[param]['commodities'][commodity]['avg'], 2), commodity[5:]))
				else:
					return_val.append((0.0, commodity[5:]))
		elif param == 'years_before_peak':
			first_production_year = int(get_param_value(curr, field, 'first_production', last_session_key))
			peak_year = int(get_param_value(curr, field, 'peak_year', last_session_key))
			if 0 not in [first_production_year, peak_year]:
				if (peak_year - first_production_year) <= 10:
					param_dict[param]['total'] += (peak_year - first_production_year)
				else:
					param_dict[param]['total'] += 10
				value_count += 1
			param_dict[param]['avg'] = float(param_dict[param]['total']) / float(value_count)
			return_val = int(round(param_dict[param]['avg']))
		else:
			param_val = get_param_value(curr, field, param, last_session_key, debug=debug)
			if param_val is not None:
				if param == 'recov_factor' and param_val >= RECOV_FACTOR_MAX:
					pass
				else:
					param_dict[param]['total'] += param_val
					param_dict[param]['avg'] = float(param_dict[param]['total']) / float(value_count)
					value_count += 1
			return_val = param_dict[param]['avg']
	return return_val


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_discovered_fields(in_place=False, with_analogues=False, country='', region='', limit=None, with_reserves=False,
						  undiscovered=False, not_modelled=False, rerun=False, debug=False):
	conn = start_database()
	curr = conn.cursor()
	sql_query = 'SELECT DISTINCT asset_id FROM asset_data WHERE status="Discovered" '
	if with_reserves:
		sql_query += 'AND IFNULL(reserve_volume,0)!=0 '
	sql_query += 'AND asset_relation="Parent" '
	
	if country:
		sql_query += 'AND country="%s" ' % country
	if region:
		sql_query += 'AND region="%s" ' % region
	if in_place:
		sql_query += 'AND NOT in_place_volume IS NULL '
	if with_analogues:
		sql_query += 'AND asset_id in (SELECT DISTINCT asset_id FROM field_analogues) '
	if rerun:
		sql_query += 'AND model_status="re-run" '
	if undiscovered:
		sql_query += 'AND asset_id >= 9000001 '
	else:
		sql_query += 'AND asset_id < 9000001 '
	if not_modelled:
		sql_query += 'AND NOT asset_id IN (SELECT DISTINCT asset_id FROM econ_data WHERE run_id=(SELECT DISTINCT run_id FROM global_variables WHERE id=1)) '
	sql_query += 'ORDER BY asset_id '
	if limit:
		sql_query += (' LIMIT %s' % limit)
	if debug:
		print 'sql_query:', sql_query
	curr.execute(sql_query)
	discovered_fields = [int(field[0]) for field in curr.fetchall()]
	curr.close()
	conn.close()
	return discovered_fields


def get_field_data(curr, field, score_type, in_place, debug=False):
	sql_select = 'SELECT api_gravity, terrain, ablock, basin, country, region, status, resource_type'
	sql_from = 'FROM asset_data '
	sql_where = 'WHERE asset_id=%s ' % field
	
	if in_place:
		sql_where += 'AND NOT in_place_volume IS NULL '
	if score_type == 'prod':
		sql_select += ', formation, form_rock_type, trap_type '
	elif score_type == 'cost':
		sql_select += ', facility_type, pipeline, gas_processing, oil_storage, gas_storage '
	
	sql_query = sql_select + sql_from + sql_where
	curr.execute(sql_query)
	field_data = curr.fetchone()
	return field_data


def get_asset_data(curr, score_type, in_place=False, analogue_pool=None, debug=False):
	sql_select = 'SELECT api_gravity, terrain, ablock, basin, country, region, status, resource_type, '
	sql_from = 'FROM asset_data '
	sql_where = 'WHERE upper(data_source) IN ("ENGINE","MODEL") AND upper(asset_relation) = "PARENT" AND upper(status) in ("ANNOUNCED","PLANNED","PRODUCING","ABANDONED") '
	# sql_where += 'AND param_track_key LIKE CONCAT("%",(SELECT run_id FROM global_variables WHERE id=1),"%") '
	sql_where += 'AND param_track_key LIKE CONCAT("%",(SELECT run_id FROM global_variables WHERE id=1),"%") '
	sql_where += 'AND NOT (asset_name LIKE "Other %" OR asset_name LIKE "Others %") '
	sql_where += 'AND NOT first_production=last_production '
	sql_where += 'AND NOT recov_reserves IS NULL '
	sql_order_by = 'ORDER BY max_%s_score DESC, recov_reserves ASC ' % score_type
	
	if analogue_pool and score_type == 'prod':
		analogue_pool_str = ', '.join([str(analogue_id) for analogue_id in analogue_pool])
		sql_where += 'AND asset_id IN ({}) '.format(analogue_pool_str)
	if in_place:
		sql_where += 'AND NOT in_place_volume IS NULL '
	if score_type == 'prod':
		sql_select += 'formation, form_rock_type, trap_type, asset_id '
	if score_type == 'cost':
		sql_select += 'facility_type, pipeline, gas_processing, oil_storage, gas_storage, asset_id '
	
	sql_query = sql_select + sql_from + sql_where + sql_order_by
	if debug:
		print sql_query
	curr.execute(sql_query)
	eligible_asset_data = curr.fetchall()
	return eligible_asset_data


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def in_range(range_type, range, f_value, a_value, debug=False):
	param_in_range = False
	if range_type == 'percentage':
		if (float(f_value) * (1 - range)) <= float(a_value) <= (float(f_value) * (1 + range)):
			param_in_range = True
	elif range_type == 'plus_minus':
		if float(f_value) - range <= float(a_value) <= (float(f_value) + range):
			param_in_range = True
	return param_in_range


def get_max_score(score_type, param, debug=False):
	max_points = 0
	params = PARAMS[score_type]
	score_dict = eval(score_type.upper() + '_SCORES')
	param_index = params.index(param)
	remaining_params = params[param_index:]
	for rem_param in remaining_params:
		param_max = 0
		if rem_param in PERCENTAGE_SCORES:
			param_max = max(score_dict[rem_param]['points'])
		elif rem_param in OPTION_SCORES:
			param_max = max(
				[score_dict[rem_param][param_option]['points'] for param_option in score_dict[rem_param].keys()])
		else:
			param_max = score_dict[rem_param]['points']
		max_points += param_max
	return max_points


def get_max_prod_score(debug=False):
	init_param = PARAMS['prod'][0]
	max_prod_score = get_max_score('prod', init_param)
	return int(max_prod_score)


def get_max_cost_score(debug=False):
	init_param = PARAMS['cost'][0]
	max_cost_score = int(get_max_score('cost', init_param))
	max_cost_score -= 900
	return max_cost_score


def get_max_analogue_score(score_type, debug=False):
	max_analogue_score = 0
	if score_type == 'prod':
		max_analogue_score = get_max_prod_score()
	elif score_type == 'cost':
		max_analogue_score = get_max_cost_score()
	return max_analogue_score


def get_error_count(curr, asset_id, debug=False):
	try:
		curr.execute('SELECT last_error_count FROM asset_data WHERE asset_id=%s' % asset_id)
		error_count = fetchone()[0]
	except:
		error_count = 0
	return error_count


def terrain_score(field_terrain, asset_terrain, debug=False):
	terrain_pair = ()
	terrains = [field_terrain.lower(), asset_terrain.lower()]
	if 'shallow water' in terrains:
		terrain_pair += ('shallow',)
	if 'deepwater' in terrains:
		terrain_pair += ('deep',)
	if 'ultra-deepwater' in terrains:
		terrain_pair += ('ultra-deep',)
	if 'onshore' in terrains:
		terrain_pair += ('onshore',)
	terrain_key = [(terrain_1, terrain_2) for (terrain_1, terrain_2) in PROD_SCORES['terrain'].keys() if
				   set((terrain_1, terrain_2)) == set(terrain_pair)][0]
	return PROD_SCORES['terrain'][terrain_key]['points']


def terrain_match(a_terrain, f_terrain, debug=False):
	terrain_match = True
	if (f_terrain.upper().strip() == 'ONSHORE' and a_terrain.upper().strip() != 'ONSHORE') or (
			a_terrain.upper().strip() == 'ONSHORE' and f_terrain.upper().strip() != 'ONSHORE'):
		terrain_match = False
	return terrain_match


def filtered_assets(asset_data, f_resource_type, f_terrain, debug=False):
	filtered_data = [data[:7] + data[8:] for data in asset_data if
					 (data[7] == f_resource_type and terrain_match(data[1], f_terrain))]
	return filtered_data


def infrastructure_scores(resource_type, main_params, debug=False):
	infra_scores = (0, 0, 0, 0)
	infra_params = main_params[1:5]
	if resource_type.upper()[:3] == 'OIL' or resource_type.upper()[-3:] == 'OIL':
		oil_infra_total = sum([infra_params[i] for i in [0, 2]])
		oil_infra_avg = oil_infra_total / 2
		infra_scores = (int(oil_infra_avg / 2), 0, int(oil_infra_avg / 2), 0)
	elif resource_type.upper()[-3:] == 'GAS' or resource_type.upper() == 'CBM':
		gas_infra_total = sum([infra_params[i] for i in [0, 1, 3]])
		gas_infra_avg = gas_infra_total / 3
		infra_scores = (int(gas_infra_avg / 3), int(gas_infra_avg / 3), 0, int(gas_infra_avg / 3))
	return infra_scores


def get_analogue_reserves_score(curr, field_id, analogue_id, score_dict):
	reserves_score = 0
	field_param = 0
	asset_param = 0
	score_factor = 0
	
	param_ranges = score_dict['reserve_volume']['ranges']
	param_scores = score_dict['reserve_volume']['points']
	
	a_in_place_type = get_param('in_place_vol_type', 'asset_data', asset_id=analogue_id, cur=curr)
	f_in_place_type = get_param('in_place_vol_type', 'asset_data', asset_id=field_id, cur=curr)
	f_recov_type = get_param('recov_vol_type', 'asset_data', asset_id=field_id, cur=curr)
	
	if a_in_place_type and f_in_place_type:
		field_param = get_param('in_place_volume', 'asset_data', asset_id=field_id, data_type='float', cur=curr)
		asset_param = get_param('in_place_volume', 'asset_data', asset_id=analogue_id, data_type='float', cur=curr)
		score_factor = float(RESERVE_FACTOR[f_in_place_type])
	elif f_recov_type:
		field_param = get_param('recov_volume', 'asset_data', asset_id=field_id, data_type='float', cur=curr)
		asset_param = get_param('recov_reserves', 'asset_data', asset_id=analogue_id, data_type='float', cur=curr)
		score_factor = float(RESERVE_FACTOR[f_recov_type])
	
	for i in range(len(param_ranges)):
		if in_range('percentage', param_ranges[i], field_param, asset_param) and field_param != 0:
			reserves_score = param_scores[i] * score_factor
			break
	
	return reserves_score


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_similarity_scores(curr, field_id, f_api_gravity, f_terrain, f_ablock, f_basin, f_country, f_region, f_status,
						  f_resource_type, f_formation, f_form_rock_type, f_trap_type,
						  f_facility_type, f_pipeline, f_gas_processing, f_oil_storage, f_gas_storage, score_type,
						  debug_mode, asset_data, analogue_id, debug=False):
	#
	'''
	In place match max 300
	Prospective max 200
	1P, 2P get 300, 3P 250, contingent 200
	'''
	# print 'test 0'
	params = []
	debug_mode = debug
	a_api_gravity, a_terrain, a_ablock, a_basin, a_country, a_region, a_status = asset_data[:7]
	analogue_score_dict = {}
	a_asset_id = 0
	a_asset_id = analogue_id
	if score_type == 'prod':
		# print 'test 2'
		a_formation, a_form_rock_type, a_trap_type, a_asset_id = asset_data[7:]
		score_dict = PROD_SCORES
		params = [param for param in PARAMS['prod'] if param != 'reserve_volume']
		analogue_score_dict = {'api_gravity'   : 0,
							   'reserve_volume': 0,
							   'terrain'       : 0,
							   'ablock'        : 0,
							   'basin'         : 0,
							   'country'       : 0,
							   'region'        : 0,
							   'status'        : 0,
							   'formation'     : 0,
							   'form_rock_type': 0,
							   'trap_type'     : 0,
							   'total'         : 0}
	elif score_type == 'cost':
		# print 'test 3'
		a_facility_type, a_pipeline, a_gas_processing, a_oil_storage, a_gas_storage, a_asset_id = asset_data[7:]
		score_dict = COST_SCORES
		params = [param for param in PARAMS['cost'] if param != 'reserve_volume']
		analogue_score_dict = {'api_gravity'   : 0,
							   'reserve_volume': 0,
							   'terrain'       : 0,
							   'ablock'        : 0,
							   'basin'         : 0,
							   'country'       : 0,
							   'region'        : 0,
							   'status'        : 0,
							   'facility_type' : 0,
							   'pipeline'      : 0,
							   'gas_processing': 0,
							   'oil_storage'   : 0,
							   'gas_storage'   : 0,
							   'total'         : 0}
	# print 'test 4'
	if debug_mode:
		if score_type in ['prod', 'cost']:
			PARAM_LIST = PARAMS[score_type]
		else:
			PARAM_LIST = PARAMS['main']
		for param in PARAM_LIST:
			asset_param = 'a_' + param
			print asset_param + ':', eval(asset_param)
		print ''
	asset_score = 0
	scores = ()
	analogue_score_dict['total'] = 0
	for param in params:
		# print param
		analogue_score_dict[param] = 0
		asset_param = eval('a_' + param)
		field_param = eval('f_' + param)
		
		if param == 'status':
			if is_value(asset_param):
				asset_score += score_dict[param][a_status]['points']
				scores += (score_dict[param][a_status]['points'],)
				analogue_score_dict[param] += score_dict[param][a_status]['points']
			else:
				scores += (0,)
		# print param, scores
		elif is_value(field_param) and is_value(asset_param):
			if param in PLUS_MINUS_SCORES:
				# print param, field_param, asset_param
				param_range = score_dict[param]['range']
				param_score = score_dict[param]['points']
				# print param_range
				if in_range('plus_minus', param_range, field_param, asset_param):
					asset_score += param_score
					scores += (param_score,)
					analogue_score_dict[param] += param_score
				else:
					scores += (0,)
			# print param, scores
			elif param in PERCENTAGE_SCORES:
				param_ranges = score_dict[param]['ranges']
				param_scores = score_dict[param]['points']
				not_in_range = True
				for i in range(len(param_ranges)):
					if in_range('percentage', param_ranges[i], field_param, asset_param) and field_param != 0:
						asset_score += score_dict[param]['points'][i]
						scores += (score_dict[param]['points'][i],)
						analogue_score_dict[param] += score_dict[param]['points'][i]
						not_in_range = False
						break
				if not_in_range:
					scores += (0,)
			# print param, scores
			elif param == 'formation':
				a_formations = set([formation.upper().strip() for formation in asset_param.split(';')])
				f_formations = set([formation.upper().strip() for formation in field_param.split(';')])
				if bool(a_formations & f_formations):
					asset_score += score_dict[param]['points']
					scores += (score_dict[param]['points'],)
					analogue_score_dict[param] += score_dict[param]['points']
				else:
					scores += (0,)
			# print param, scores
			elif param == 'terrain':
				if f_terrain.lower() == a_terrain.lower():
					asset_score += score_dict['terrain'][('match', 'match')]['points']
					scores += (score_dict['terrain'][('match', 'match')]['points'],)
					analogue_score_dict[param] += score_dict['terrain'][('match', 'match')]['points']
				else:
					asset_score += terrain_score(f_terrain, a_terrain)
					scores += (terrain_score(f_terrain, a_terrain),)
					analogue_score_dict[param] += terrain_score(f_terrain, a_terrain)
			# print param, scores
			elif isinstance(score_dict[param]['points'], int) and field_param == asset_param:
				asset_score += score_dict[param]['points']
				scores += (score_dict[param]['points'],)
				analogue_score_dict[param] += score_dict[param]['points']
			# print param, scores
			else:
				scores += (0,)
		# print param, scores
		elif param == 'facility_type' and f_terrain == 'Onshore':
			scores += (score_dict[param]['points'],)
		else:
			scores += (0,)
		# print param, scores
		analogue_score_dict['total'] += analogue_score_dict[param]
	reserves_score = get_analogue_reserves_score(curr, field_id, analogue_id, score_dict)
	analogue_score_dict['reserve_volume'] += reserves_score
	analogue_score_dict['total'] += reserves_score
	asset_score += reserves_score
	scores += (reserves_score,)
	
	if debug and 0:
		print 'params:', params
		print 'scores:', scores
	param_vals = (a_asset_id, asset_score, analogue_score_dict) + scores
	return param_vals


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def enter_similiarity_scores(curr, field_list, score_type=None, clear_table=False, in_place=False, with_tiers=False,
							 analogue_pool=None, debug_mode=False):
	discovered_fields = field_list
	prod_tier_min_threshold = 0
	prod_tier_max_threshold = 0
	cost_tier_min_threshold = 0
	cost_tier_max_threshold = 0
	if with_tiers:
		max_prod_score = get_max_prod_score()
		prod_tier_min_threshold = int(max_prod_score / 3)
		prod_tier_max_threshold = max_prod_score - prod_tier_min_threshold
		
		max_cost_score = get_max_cost_score()
		cost_tier_min_threshold = int(max_cost_score / 3)
		cost_tier_max_threshold = max_cost_score - cost_tier_min_threshold
	
	# Get data for all eligible assets
	prod_asset_data = get_asset_data(curr, 'prod', in_place, analogue_pool, debug=debug_mode)
	cost_asset_data = get_asset_data(curr, 'cost', in_place, analogue_pool, debug=debug_mode)
	
	analogue_ids = list(set([asset_data[-1] for asset_data in prod_asset_data + cost_asset_data]))
	if debug_mode:
		print 'len(prod_asset_data):', len(prod_asset_data)
		print 'len(cost_asset_data):', len(cost_asset_data)
	
	# Calculate similarity scores for all discovered fields assessed
	
	field_count_total = len(discovered_fields)
	current_field_count = 1
	# --------------------------------------------------------------------------------------------
	for field_id in discovered_fields:
		analogue_scores = {}
		for analogue_id in analogue_ids:
			analogue_scores[analogue_id] = {}
		analogue_score_data = []
		# ----------------------------------------------------------------------------------------
		print '-' * 50
		for score_type in ['prod', 'cost']:
			print field_id, 'Getting %s field data ...' % score_type
			field_data = get_field_data(curr, field_id, score_type, in_place)
			
			# Assign variables to discovered field data and optionally display
			f_api_gravity, f_terrain, f_ablock, f_basin, f_country, f_region, f_status, f_resource_type = field_data[:8]
			if score_type == 'prod':
				f_formation, f_form_rock_type, f_trap_type = field_data[8:11]
				f_facility_type, f_pipeline, f_gas_processing, f_oil_storage, f_gas_storage = (0, 0, 0, 0, 0)
			elif score_type == 'cost':
				f_formation, f_form_rock_type, f_trap_type = (0, 0, 0)
				f_facility_type, f_pipeline, f_gas_processing, f_oil_storage, f_gas_storage = field_data[8:13]
			if debug_mode:
				if score_type in ['prod', 'cost']:
					PARAM_LIST = PARAMS[score_type]
				else:
					PARAM_LIST = PARAMS['main']
				for param in [param_name for param_name in PARAM_LIST if param_name != 'reserve_volume']:
					field_param = 'f_' + param
					print field_param + ':', eval(field_param)
				print ''
			# ------------------------------------------------------------------------------------
			print field_id, 'Generating %s similarity scores ...' % score_type
			
			analogue_asset_data = filtered_assets(eval(score_type + '_asset_data'), f_resource_type, f_terrain)
			# print 'test 1', len(analogue_asset_data)
			# ------------------------------------------------------------------------------------
			
			for asset_data in analogue_asset_data:
				analogue_id = asset_data[-1]
				# print analogue_id
				# Get similarity scores for all eligible assets and generate sql statement to update analogue data table
				# params = get_similarity_scores(f_api_gravity,f_reserve_volume,f_terrain,f_ablock,f_basin,f_country,f_region,f_status,f_resource_type,f_formation,f_form_rock_type,f_trap_type,f_facility_type,f_pipeline,f_gas_processing,f_oil_storage,f_gas_storage,score_type,debug_mode,asset_data,analogue_id)
				params = get_similarity_scores(curr, field_id, f_api_gravity, f_terrain, f_ablock, f_basin, f_country,
											   f_region, f_status, f_resource_type, f_formation, f_form_rock_type,
											   f_trap_type, f_facility_type, f_pipeline, f_gas_processing,
											   f_oil_storage, f_gas_storage, score_type, debug_mode, asset_data,
											   analogue_id)
				
				# Enter similarity scores into field_analogues data table
				analogue_id, analogue_score, analogue_score_dict = params[:3]
				
				if with_tiers:
					analogue_tier = 0
				else:
					analogue_tier = 1
				
				main_params = params[3:]
				
				if score_type == 'prod':
					zero_params = (0, 0, 0, 0, 0)
					if with_tiers:
						if analogue_score >= prod_tier_max_threshold:
							analogue_tier = 1
						elif analogue_score < prod_tier_min_threshold:
							analogue_tier = 3
						else:
							analogue_tier = 2
				elif score_type == 'cost':
					zero_params = (0, 0, 0)
					infra_params = infrastructure_scores(f_resource_type, main_params, debug_mode)
					main_params = main_params[:1] + infra_params + main_params[5:]
					analogue_score = sum(main_params)
					if with_tiers:
						if analogue_score >= cost_tier_max_threshold:
							analogue_tier = 1
						elif analogue_score < cost_tier_min_threshold:
							analogue_tier = 3
						else:
							analogue_tier = 2
				param_scores = main_params + zero_params
				
				analogue_scores[analogue_id][score_type] = analogue_score_dict
				analogue_error = get_error_count(curr, analogue_id)
				analogue_score_data.append(
					(field_id, score_type, analogue_id, analogue_score, analogue_tier, analogue_error) + param_scores)
		analogue_min = SCORE_LIMITS['field_min']
		analogue_max = SCORE_LIMITS['field_max']
		# ----------------------------------------------------------------------------------------
		# Enter production scores meeting thresholds set in SCORE_LIMITS dictionary
		prod_score_data = sorted([score_data for score_data in analogue_score_data if score_data[1] == 'prod'],
								 key=lambda prod_data: prod_data[3], reverse=True)
		qual_prod_data = [prod_data for prod_data in prod_score_data if prod_data[5] <= SCORE_LIMITS['error_max']]
		#
		top_prod_data = [prod_data for prod_data in qual_prod_data if prod_data[3] >= SCORE_LIMITS['prod_min']]
		if len(top_prod_data) < analogue_min:
			comment = '%s PRODUCTION ANALOGUE FIELDS FOUND DOES NOT MEET MINIMUM THRESHOLD OF %s' % (
				len(top_prod_data), analogue_min)
			error_type = 'ERROR TYPE 50'
			save_error(curr, field_id, comment, error_type)
			if len(qual_prod_data) >= analogue_min:
				top_prod_data = qual_prod_data[:analogue_min]
			else:
				top_prod_data = prod_score_data[:analogue_min]
		elif len(top_prod_data) >= analogue_max:
			top_prod_data = top_prod_data[:analogue_max]
		
		# ----------------------------------------------------------------------------------------
		# Enter cost scores meeting thresholds set in SCORE_LIMITS dictionary
		cost_score_data = sorted([score_data for score_data in analogue_score_data if score_data[1] == 'cost'],
								 key=lambda cost_data: cost_data[3], reverse=True)
		qual_cost_data = [cost_data for cost_data in cost_score_data if cost_data[5] <= SCORE_LIMITS['error_max']]
		#
		top_cost_data = [cost_data for cost_data in qual_cost_data if cost_data[3] >= SCORE_LIMITS['cost_min']]
		if len(top_cost_data) < analogue_min:
			comment = '%s COST ANALOGUE FIELDS FOUND DOES NOT MEET MINIMUM THRESHOLD OF %s' % (
				len(top_cost_data), analogue_min)
			error_type = 'ERROR TYPE 50'
			save_error(curr, field_id, comment, error_type)
			if len(qual_cost_data) >= analogue_min:
				top_cost_data = qual_cost_data[:analogue_min]
			else:
				top_cost_data = cost_score_data[:analogue_min]
		elif len(top_cost_data) >= analogue_max:
			top_cost_data = top_cost_data[:analogue_max]
		
		# ----------------------------------------------------------------------------------------
		top_score_data = top_prod_data + top_cost_data
		sql_insert = 'INSERT INTO field_analogues (asset_id, analogue_type, analogue_id, analogue_score, analogue_tier, analogue_error, %s) VALUES (%s)'
		
		for datarow in top_score_data:
			# print datarow
			analogue_score_type = datarow[1]
			param_str = ', '.join(PARAM_DICT[analogue_score_type])
			var_str = ', '.join(['%s'] * (6 + len(PARAMS['all'])))
			sql_statement = sql_insert % (param_str, var_str)
			if debug_mode: print sql_statement % datarow
			curr.execute(sql_statement, datarow)
		curr.execute('COMMIT')
		
		print ''
		print '%s/%s discovered fields processed' % (current_field_count, field_count_total)
		print ''
		current_field_count += 1
		
def update_median_recov_factor(curr, debug=False):
	resource_types = get_data('resource_type', 'asset_data', cursor=curr, sql_where="resource_type IS NOT NULL")
	sql_update = "UPDATE asset_data SET avg_recov_factor={} WHERE resource_type='{}' AND `status`='Discovered' AND reserve_type IN ('Gas in Place', 'Oil in Place', 'Prospective');"
	for resource_type in resource_types:
		recov_factors = get_data('recov_factor', 'asset_data', cursor=curr, distinct=False, datatype='float', sql_where="resource_type='{}' AND IFNULL(recov_factor,0)>0".format(resource_type))
		if len(recov_factors):
			median_recov_factor = get_median(recov_factors)
		else:
			median_recov_factor = 0.285
		if debug:
			print sql_update.format(median_recov_factor, resource_type)
		curr.execute(sql_update.format(median_recov_factor, resource_type))
		commit(curr)
		

def enter_production_data(curr, asset_id, debug_mode, in_place, undiscovered=False, debug=False):
	sql_update = 'UPDATE production SET sources="EST: Forecast Engine" WHERE asset_id={}'.format(asset_id)
	commit(curr)
	discount_year = get_discount_year(curr)
	prod_period_data = {'init': {'year': discount_year + 5,
								 'data': []},
						'peak': {'year': 0,
								 'data': []}}
	comm_col_names = \
		{'init': {'Crude Oil'  : 'init_crude',
				  'Natural Gas': 'init_ng',
				  'Condensate' : 'init_condensate',
				  'LNG'        : 'init_lng',
				  'NGL'        : 'init_ngl'},
		
		 'peak': {'Crude Oil'  : 'peak_crude',
				  'Natural Gas': 'peak_ng',
				  'Condensate' : 'peak_condensate',
				  'LNG'        : 'peak_lng',
				  'NGL'        : 'peak_ngl'}}
	
	add_date = get_add_date()
	
	prod_period_data['init']['data'] = get_field_param(curr, asset_id,
													   param='total_init_prod',
													   undiscovered=undiscovered,
													   debug=debug)
	prod_period_data['peak']['year'] = prod_period_data['init']['year'] + get_field_param(curr, asset_id,
																						  param='years_before_peak',
																						  undiscovered=undiscovered,
																						  debug=debug)
	prod_period_data['peak']['data'] = get_field_param(curr, asset_id,
													   param='total_peak_prod',
													   undiscovered=undiscovered,
													   debug=debug)
	
	if debug_mode or debug:
		print 'init_prod_data:', prod_period_data['init']['data']
		print 'peak_prod_year:', prod_period_data['peak']['year']
		print 'peak_prod_data:', prod_period_data['peak']['data']
	
	sql_query = 'SELECT asset_name, country, constituent, region FROM asset_data WHERE asset_id=%s'
	curr.execute(sql_query % asset_id)
	asset_name, country, constituent, region = curr.fetchone()
	all_prod_data = list(set(prod_period_data['init']['data'] + prod_period_data['peak']['data']))
	analogue_commodities_ = get_analogue_commodities(curr, asset_id, in_place)
	analogue_commodities = list(set([comm for (prod, comm) in all_prod_data if prod > 0]))
	if debug_mode or debug:
		print 'analogue_commodities_: {}'.format(analogue_commodities_)
		print 'analogue_commodities: {}'.format(analogue_commodities)

	prod_period_years = (prod_period_data['init']['year'], prod_period_data['peak']['year'], asset_id)
	curr.execute('UPDATE asset_data SET first_production=%s, peak_year=%s WHERE asset_id=%s' % prod_period_years)
	curr.execute('DELETE FROM production WHERE asset_id=%s AND add_by="Analogue"' % asset_id)
	curr.execute('COMMIT')
	
	prod_factor = 1
	vintage_fields = get_vintage_fields(curr)
	if int(asset_id) in vintage_fields:
		prod_factor = float(1 - VINTAGE_FACTOR)
		print 'Vintage factor of %s applied to field %s' % (VINTAGE_FACTOR, asset_id)
	
	in_place_fields = get_in_place_reserve_fields(curr)
	if int(asset_id) not in in_place_fields:
		if prod_factor == 1:
			prod_factor = float(1 - NO_RESERVES_FACTOR)
			print 'No in-place reserves ---> production reduced by %s%%' % (NO_RESERVES_FACTOR * 100)
	
	for prod_period in prod_period_data.keys():
		prod_year = prod_period_data[prod_period]['year']
		prod_data = prod_period_data[prod_period]['data']
		for comm_data in prod_data:
			if debug_mode or debug:
				print 'comm_data:', comm_data
			production, commodity = comm_data
			if commodity in analogue_commodities:
				production *= prod_factor
				if production > 0:
					sql_insert = 'INSERT INTO production (asset_id,asset_name,country,constituent,region,commodity,period,production,unit,casetype,asset_relationship,sources,data_source,add_by,add_date) '
					sql_insert += 'VALUES (%s,"%s","%s","%s","%s","%s",%s,%s,"Boe","Base Case","Parent","EST: Hardcode","Engine","Analogue","%s")'
					sql_insert = sql_insert % (
						asset_id, asset_name, country, constituent, region, commodity, prod_year, production, add_date)
					if debug_mode or debug:
						print sql_insert
					curr.execute(sql_insert)
					comm_col = comm_col_names[prod_period][commodity]
					params = (comm_col, production, asset_id)
					sql_update = 'UPDATE asset_data SET %s=%s WHERE asset_id=%s' % params
					if debug: print sql_update
					curr.execute(sql_update)
					curr.execute('COMMIT')
	curr.execute('UPDATE assets SET data_source="Engine" WHERE asset_id=%s' % asset_id)
	curr.execute('COMMIT')
	if int(asset_id) in get_in_place_reserve_fields(curr):
		avg_recov_factor = get_field_param(curr, asset_id, 'recov_factor', undiscovered=undiscovered)
		print 'Average recovery factor: %s' % avg_recov_factor
	print 'Hardcode production data entered'


def get_field_param(curr, field_id, param, undiscovered=False, debug=False):
	global disc_field
	ANALOGUE_TYPES = {'capex_per_boe'         : 'cost',
					  'fixed_opex'            : 'cost',
					  'variable_opex_per_mmcf': 'cost',
					  'variable_opex_per_b'   : 'cost',
					  'abandonment'           : 'cost',
					  'capex_tangible_pct'    : 'cost',
					  'capex_redev'           : 'cost',
					  'opex_capacity_factor'  : 'cost',
					  'opex_capacity_target'  : 'cost',
					  'capex_capacity_factor' : 'cost',
					  'capex_capacity_target' : 'cost',
					  'total_init_prod'       : 'prod',
					  'total_peak_prod'       : 'prod',
					  'years_before_peak'     : 'prod',
					  'first_production'      : 'prod',
					  'recov_factor'          : 'prod'}
	
	analogue_type = ANALOGUE_TYPES[param]
	return_val = get_param_avg(curr, field_id, param, analogue_type, debug=debug)
	if param in ['total_init_prod', 'total_peak_prod']:
		if debug: print 'param: {} -- return_val: {}'.format(param, return_val)
		update_val = sum([prod for (prod, comm) in return_val])
		if field_id < 9000000:
			crude_pct, ng_pct, cond_pct, ngl_pct, lng_pct = get_data(
				'crude_reserve_pct, ng_reserve_pct, condensate_reserve_pct, ngl_reserve_pct, lng_reserve_pct',
				'asset_data', datatype='plural', single_value=True, cursor=curr,
				sql_where='asset_id={}'.format(field_id))
			comm_pct_cols = {
				'Crude Oil'  : crude_pct,
				'Natural Gas': ng_pct,
				'Condensate' : cond_pct,
				'NGL'        : ngl_pct,
				'LNG'        : lng_pct
			}
			new_return_val = []
			for prod, comm in return_val:
				
				new_prod = float(update_val) * comm_pct_cols[comm]
				new_return_val.append((new_prod, comm))
				if debug:
					print '({}) -- {} -- {} * {} ({}) = {}'.format(disc_field, field_id, update_val, comm_pct_cols[comm], comm, new_prod)
			return_val = new_return_val
			print '(1) return_val: {}'.format(return_val)
	
	else:
		update_val = return_val
	if param == 'recov_factor':
		param = 'avg_recov_factor'
	print param, 'value:', update_val
	if param != 'years_before_peak':
		if debug: print 'UPDATE asset_data SET %s="%s" WHERE asset_id=%s' % (param, update_val, field_id)
		curr.execute('UPDATE asset_data SET %s="%s" WHERE asset_id=%s' % (param, update_val, field_id))
		curr.execute('COMMIT')
	return return_val


def update_reserve_volumes(curr):
	
	curr.execute("UPDATE asset_data SET avg_recov_factor=1 WHERE avg_recov_factor IS NULL;")
	commit(curr)
	curr.execute("UPDATE asset_data SET avg_recov_factor=0 WHERE status='Discovered' AND (NOT avg_recov_factor > 0 OR avg_recov_factor IS NULL)")
	commit(curr)
	curr.execute("UPDATE asset_data SET avg_recov_factor=0.9 WHERE status='Discovered' AND NOT (recov_volume IS NULL AND in_place_volume IS NULL)")
	commit(curr)
	curr.execute("UPDATE asset_data SET avg_recov_factor=0.285 WHERE status='Discovered' AND avg_recov_factor=0")
	commit(curr)
	curr.execute("UPDATE asset_data SET avg_recov_factor=1.0 WHERE asset_id > 9000000")
	commit(curr)
	curr.execute("UPDATE asset_data SET reserve_type=in_place_vol_type, reserve_volume=(in_place_volume*avg_recov_factor) WHERE IFNULL(in_place_volume,0) > 0 AND IFNULL(recov_volume,0) = 0")
	commit(curr)
	curr.execute("UPDATE asset_data SET reserve_type=recov_vol_type, reserve_volume=(recov_volume*avg_recov_factor) WHERE IFNULL(recov_volume,0) > 0")
	commit(curr)
	curr.execute("UPDATE asset_data SET prod_adjust_count=0")
	commit(curr)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_score_min_max(curr, score_type, debug=False):
	score_min = 0
	score_max = 0
	# if score_type == 'facility_type':
	#    sql_select  = 'SELECT MIN(a.facility_type_sum) AS facility_type_min, MAX(a.facility_type_sum) AS facility_type_max FROM '
	#    sql_select += '(SELECT asset_id, SUM(facility_type) AS facility_type_sum FROM field_analogues GROUP BY asset_id) AS a'
	
	if score_type == 'infrastructure':
		sql_select = 'SELECT MIN(a.pipeline_sum + a.gas_processing_sum + a.oil_storage_sum + a.gas_storage_sum) AS infrastructure_min, '
		sql_select += 'MAX(a.pipeline_sum + a.gas_processing_sum + a.oil_storage_sum + a.gas_storage_sum) AS infrastructure_max FROM '
		sql_select += '(SELECT asset_id, SUM(pipeline) AS pipeline_sum, SUM(gas_processing) AS gas_processing_sum, SUM(oil_storage) AS oil_storage_sum, SUM(gas_storage) AS gas_storage_sum '
		sql_select += 'FROM field_analogues GROUP BY asset_id) AS a'
	
	elif score_type == 'reserves':
		sql_select = 'SELECT MIN(a.reserves_sum) AS reserves_min, MAX(a.reserves_sum) AS reserves_max FROM '
		sql_select += '(SELECT asset_id, SUM(reserve_volume) AS reserves_sum FROM field_analogues GROUP BY asset_id) AS a'
	
	elif score_type == 'prod_analogue':
		sql_select = 'SELECT MIN(a.prod_analogue_sum) AS prod_analogue_min, MAX(a.prod_analogue_sum) AS prod_analogue_max FROM '
		sql_select += '(SELECT asset_id, SUM(analogue_score) AS prod_analogue_sum FROM field_analogues WHERE analogue_type="prod" GROUP BY asset_id) AS a'
	
	elif score_type == 'cost_analogue':
		sql_select = 'SELECT MIN(a.cost_analogue_sum) AS cost_analogue_min, MAX(a.cost_analogue_sum) AS cost_analogue_max FROM '
		sql_select += '(SELECT asset_id, SUM(analogue_score) AS cost_analogue_sum FROM field_analogues WHERE analogue_type="cost" GROUP BY asset_id) AS a'
	if debug:
		print 'sql_select (get_score_min_max):', sql_select
	curr.execute(sql_select)
	score_min, score_max = curr.fetchone()
	if debug:
		print 'score_type:', score_type
		print 'score_min:', score_min
		print 'score_max:', score_max
	return score_min, score_max


# def get_facility_type_score(curr, field, score_min, score_max, debug=False):
#    facility_type_score = 0.0
#    curr.execute('SELECT SUM(facility_type) AS facility_type_sum FROM field_analogues WHERE asset_id=%s' % field)
#    facility_type_sum = curr.fetchone()[0]
#    try:
#        facility_type_pct = float(facility_type_sum - score_min)/float(score_max - score_min)
#    except:
#        facility_type_pct = 0.0
#    facility_type_score = facility_type_pct * CONF_SCORE_MAX
#    if debug:
#        print '%s facility_type_score: %s' % (field, facility_type_score)
#    return facility_type_score


def get_infrastructure_score(curr, field, score_min, score_max, debug=False):
	infrastructure_score = 0.0
	sql_select = 'SELECT (a.pipeline_sum + a.gas_processing_sum + a.oil_storage_sum + a.gas_storage_sum) AS infrastructure_sum FROM '
	sql_select += '(SELECT SUM(pipeline) AS pipeline_sum, SUM(gas_processing) AS gas_processing_sum, SUM(oil_storage) AS oil_storage_sum, SUM(gas_storage) AS gas_storage_sum '
	sql_select += 'FROM field_analogues WHERE asset_id=%s) AS a' % field
	curr.execute(sql_select)
	infrastructure_sum = curr.fetchone()[0]
	try:
		infrastructure_pct = float(infrastructure_sum - score_min) / float(score_max - score_min)
	except:
		infrastructure_pct = 1.0
	infrastructure_score = infrastructure_pct * CONF_SCORE_MAX
	if debug:
		print '%s infrastructure_score: %s' % (field, infrastructure_score)
	return infrastructure_score


def get_reserves_score(curr, field, score_min, score_max, debug=False):
	reserves_score = 0.0
	curr.execute('SELECT SUM(reserve_volume) AS reserves_sum FROM field_analogues WHERE asset_id=%s' % field)
	reserves_sum = curr.fetchone()[0]
	try:
		reserves_pct = float(reserves_sum - score_min) / float(score_max - score_min)
	except:
		reserves_pct = 1.0
	reserves_score = reserves_pct * CONF_SCORE_MAX
	if debug:
		print '%s reserves_score: %s' % (field, reserves_score)
	return reserves_score


def get_auxilary_param_score(curr, field, param, debug=False):
	auxilary_param_score = 0.0
	param_fields = get_auxilary_param_fields(curr, param, debug)
	if field in param_fields:
		auxilary_param_score = AUX_SCORE_MAX
	if debug:
		print '%s auxilary_param_score: %s' % (field, auxilary_param_score)
	return auxilary_param_score


def get_prod_analogue_score(curr, field, score_min, score_max, debug=False):
	prod_analogue_score = 0.0
	curr.execute(
		'SELECT SUM(analogue_score) AS prod_analogue_sum FROM field_analogues WHERE analogue_type="prod" AND asset_id=%s' % field)
	prod_analogue_sum = curr.fetchone()[0]
	try:
		prod_analogue_pct = float(prod_analogue_sum - score_min) / float(score_max - score_min)
	except:
		prod_analogue_pct = 1.0
	prod_analogue_score = prod_analogue_pct * CONF_SCORE_MAX
	if debug:
		print '%s prod_analogue_score: %s' % (field, prod_analogue_score)
	return prod_analogue_score


def get_cost_analogue_score(curr, field, score_min, score_max, debug=False):
	cost_analogue_score = 0.0
	curr.execute(
		'SELECT SUM(analogue_score) AS cost_analogue_sum FROM field_analogues WHERE analogue_type="cost" AND asset_id=%s' % field)
	cost_analogue_sum = curr.fetchone()[0]
	try:
		cost_analogue_pct = float(cost_analogue_sum - score_min) / float(score_max - score_min)
	except:
		cost_analogue_pct = 1.0
	cost_analogue_score = cost_analogue_pct * CONF_SCORE_MAX
	if debug:
		print '%s cost_analogue_score: %s' % (field, cost_analogue_score)
	return cost_analogue_score


def enter_field_confidence_score(curr, field_list=None, calc_conf=False, curve_score=False, debug=False):
	if field_list:
		fields = field_list
	else:
		curr.execute('SELECT DISTINCT asset_id FROM field_analogues')
		fields = [int(data[0]) for data in curr.fetchall()]
	
	if calc_conf:
		# facility_score_min,       facility_score_max       = get_score_min_max(curr, 'facility_type', debug)
		infrastructure_score_min, infrastructure_score_max = get_score_min_max(curr, 'infrastructure', debug)
		reserves_score_min, reserves_score_max = get_score_min_max(curr, 'reserves', debug)
		prod_analogue_score_min, prod_analogue_score_max = get_score_min_max(curr, 'prod_analogue', debug)
		cost_analogue_score_min, cost_analogue_score_max = get_score_min_max(curr, 'cost_analogue', debug)
		field_count = len(fields)
		field_num = 1
		for field in fields:
			confidence_score_points = 0.0
			
			# facility_type_score   = get_facility_type_score(curr, field, facility_score_min, facility_score_max, debug)
			infrastructure_score = get_infrastructure_score(curr, field, infrastructure_score_min,
															infrastructure_score_max, debug)
			reserves_score = get_reserves_score(curr, field, reserves_score_min, reserves_score_max, debug)
			sulfur_score = get_auxilary_param_score(curr, field, 'sulfer', debug)
			hsulfur_score = get_auxilary_param_score(curr, field, 'hsulfer', debug)
			api_gravity_score = get_auxilary_param_score(curr, field, 'api_gravity', debug)
			calorific_score = get_auxilary_param_score(curr, field, 'calorific', debug)
			carbon_dioxide_score = get_auxilary_param_score(curr, field, 'carbon_dioxide', debug)
			prod_analogue_score = get_prod_analogue_score(curr, field, prod_analogue_score_min, prod_analogue_score_max,
														  debug)
			cost_analogue_score = get_cost_analogue_score(curr, field, cost_analogue_score_min, cost_analogue_score_max,
														  debug)
			
			# confidence_score_points  = (facility_type_score*CONF_WEIGHTS['facility_type']) + (infrastructure_score*CONF_WEIGHTS['infrastructure']) + (reserves_score*CONF_WEIGHTS['reserves'])
			confidence_score_points = (infrastructure_score * CONF_WEIGHTS['infrastructure']) + (
					reserves_score * CONF_WEIGHTS['reserves'])
			confidence_score_points += (sulfur_score * CONF_WEIGHTS['sulfur']) + (
					hsulfur_score * CONF_WEIGHTS['hsulfur']) + (api_gravity_score * CONF_WEIGHTS['api_gravity'])
			confidence_score_points += (calorific_score * CONF_WEIGHTS['calorific']) + (
					carbon_dioxide_score * CONF_WEIGHTS['carbon_dioxide'])
			confidence_score_points += (prod_analogue_score * CONF_WEIGHTS['prod_analogue']) + (
					cost_analogue_score * CONF_WEIGHTS['cost_analogue'])
			
			auxilary_param_score = sulfur_score + hsulfur_score + api_gravity_score + calorific_score + carbon_dioxide_score
			# point_params = (facility_type_score, infrastructure_score, reserves_score, auxilary_param_score, prod_analogue_score, cost_analogue_score, confidence_score_points, field)
			point_params = (
				infrastructure_score, reserves_score, auxilary_param_score, prod_analogue_score, cost_analogue_score,
				confidence_score_points, field)
			# sql_update  = 'UPDATE asset_data SET facility_type_score=%s, infrastructure_score=%s, reserves_score=%s, auxilary_param_score=%s, '
			sql_update = 'UPDATE asset_data SET infrastructure_score=%s, reserves_score=%s, auxilary_param_score=%s, prod_analogue_score=%s, cost_analogue_score=%s, confidence_score_points=%s WHERE asset_id=%s '
			curr.execute(sql_update % point_params)
			curr.execute('COMMIT')
			
			print '%s/%s - %s confidence score points = %s' % (field_num, field_count, field, confidence_score_points)
			field_num += 1
	
	if curve_score:
		curr.execute('SELECT MAX(confidence_score_points) FROM asset_data')
		max_confidence_points = float(curr.fetchone()[0])
		print 'max_confidence_points:', max_confidence_points
		for field in fields:
			field_confidence_score = 0.0
			curr.execute('SELECT confidence_score_points FROM asset_data WHERE asset_id=%s' % field)
			
			field_confidence_points = float(curr.fetchone()[0])
			field_confidence_pct = field_confidence_points / max_confidence_points
			field_confidence_score = field_confidence_pct * CONF_SCORE_MAX
			
			curr.execute(
				'UPDATE asset_data SET field_confidence_score=%s WHERE asset_id=%s ' % (field_confidence_score, field))
			curr.execute('COMMIT')
			
			print '%s field confidence score = %s' % (field, field_confidence_score)


def create_field_lists(regions=None, undiscovered=False, debug=False):
	DF_lists = []
	#'''
	rest_of_world_regions = {'Rest of World 1': ['Europe', 'Middle East'],
							 'Rest of World 2': ['North America', 'Caribbean', 'Central America'],
							 'Rest of World 3': ['Africa', 'South America']}
	#'''
	
	# rest_of_world_regions = {'Rest of World 1': ['North_America_5', 'Middle East'],
	# 						 'Rest of World 2': ['Former_Soviet_Union_4'],
	# 						 'Rest of World 3': ['North_America_2', 'Caribbean', 'Central America']}
	region_codes = {
		'Africa'               : 'DF_AF',
		'Asia'                 : 'DF_AS',
		'Caribbean'            : 'DF_CR',
		'Central America'      : 'DF_CA',
		'Europe'               : 'DF_EU',
		'Europe_1'             : 'DF_EU_1',
		'Europe_2'             : 'DF_EU_2',
		'Europe_3'             : 'DF_EU_3',
		'Former Soviet Union'  : 'DF_FS',
		'Former_Soviet_Union_1': 'DF_FS_1',
		'Former_Soviet_Union_2': 'DF_FS_2',
		'Former_Soviet_Union_3': 'DF_FS_3',
		'Former_Soviet_Union_4': 'DF_FS_4',
		'Middle East'          : 'DF_ME',
		'North America'        : 'DF_NA',
		'North_America_1'      : 'DF_NA_1',
		'North_America_2'      : 'DF_NA_2',
		'North_America_3'      : 'DF_NA_3',
		'North_America_4'      : 'DF_NA_4',
		'North_America_5'      : 'DF_NA_5',
		'North_America_6'      : 'DF_NA_6',
		'Oceania'              : 'DF_OC',
		'South America'        : 'DF_SA',
		'South_America_1'      : 'DF_SA_1',
		'South_America_2'      : 'DF_SA_2',
		'South_America_3'      : 'DF_SA_3',
		'Rest of World 1'      : 'DF_RW_1',
		'Rest of World 2'      : 'DF_RW_2',
		'Rest of World 3'      : 'DF_RW_3'
	}
	
	if regions:
		region_names = regions
	else:
		region_names = ['Asia', 'Africa', 'Caribbean', 'Central America', 'Europe', 'Middle East', 'North America',
						'South America',
						'Former Soviet Union', 'Oceania']
	for region_name in region_names:
		asset_list = []
		region_file = region_codes[region_name] + '.csv'
		if region_name in ['Rest of World 1', 'Rest of World 2', 'Rest of World 3']:
			for region in rest_of_world_regions[region_name]:
				disc_fields = get_discovered_fields(with_analogues=True, with_reserves=True, region=region,
													undiscovered=undiscovered, debug=debug)
				asset_list += disc_fields
		else:
			disc_fields = get_discovered_fields(with_analogues=True, with_reserves=True, region=region_name,
												undiscovered=undiscovered, debug=debug)
			asset_list += disc_fields
		asset_list = sorted(list(set(asset_list)))
		if debug:
			for asset_id in asset_list:
				print asset_id
		DF_lists.append((asset_list, region_file))
		print len(asset_list), asset_list, region_file
	for DF_list, DF_file in DF_lists:
		with open(TEST_DIR + DF_file, 'w') as csvfile:
			fieldnames = ['ASSET_ID', 'COUNTRY', 'CONSTITUENT', 'REGION', 'STATUS', 'TERRAIN', 'RESOURCE', 'FACILITY',
						  'BASIN', 'OPERATOR']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
			writer.writeheader()
			for asid in DF_list:
				writer.writerow({'ASSET_ID': asid})
		shutil.copy2(TEST_DIR + DF_file, DF_MODEL_DIR + DF_file)


def process_production_data(curr, field, debug_mode):
	sql_select = 'SELECT resource_type,init_crude,init_ng,init_condensate,init_lng,init_ngl,first_production,peak_crude,peak_ng,peak_condensate,peak_lng,peak_ngl,peak_year FROM asset_data WHERE asset_id=%s' % field
	curr.execute(sql_select)
	resource_type, init_crude, init_ng, init_condensate, init_lng, init_ngl, first_production, peak_crude, peak_ng, peak_condensate, peak_lng, peak_ngl, peak_year = curr.fetchone()
	if ' oil' in resource_type.lower() and not init_crude and not peak_crude and init_condensate and peak_condensate:
		init_crude = init_condensate
		peak_crude = peak_condensate
		sql_update = 'UPDATE asset_data SET init_crude=%s, peak_crude=%s, init_condensate=NULL, peak_condensate=NULL WHERE asset_id=%s' % (
			init_crude, peak_crude, field)
		curr.execute(sql_update)
		curr.execute('COMMIT')
		sql_update = 'UPDATE production SET commodity="Crude Oil" WHERE asset_id=%s AND commodity="Condensate" AND period IN (%s, %s) AND add_by="Analogue"' % (
			field, first_production, peak_year)
		curr.execute(sql_update)
		curr.execute('COMMIT')
	# Need to add decline production years
	sql_select = 'SELECT asset_name,country,constituent,region,commodity,production,unit,asset_relationship,sources,data_source,add_date '
	sql_select += 'FROM production WHERE casetype="Base Case" AND asset_id=%s AND add_by="Analogue" AND production > 0 and period=%s'
	curr.execute(sql_select % (field, peak_year))
	
	add_by = "Analogue"
	casetype = "Base Case"
	asset_id = field
	for asset_name, country, constituent, region, commodity, production, unit, asset_relationship, sources, data_source, add_date in curr.fetchall():
		prod_decline_yr1 = production * 0.90
		decline_yr1 = (peak_year + 1)
		param_vals = (
			asset_id, asset_name, country, constituent, region, commodity, decline_yr1, prod_decline_yr1, unit,
			casetype,
			asset_relationship, sources, data_source, add_by, add_date)
		var_str = ', '.join(["%s"] * len(param_vals))
		sql_insert = 'INSERT INTO production (asset_id,asset_name,country,constituent,region,commodity,period,production,unit,casetype,asset_relationship,sources,data_source,add_by,add_date) VALUES (%s)' % var_str
		curr.execute(sql_insert, param_vals)
		
		prod_decline_yr2 = prod_decline_yr1 * 0.9045
		decline_yr2 = (peak_year + 2)
		param_vals = (
			asset_id, asset_name, country, constituent, region, commodity, decline_yr2, prod_decline_yr2, unit,
			casetype,
			asset_relationship, sources, data_source, add_by, add_date)
		var_str = ', '.join(["%s"] * len(param_vals))
		sql_insert = 'INSERT INTO production (asset_id,asset_name,country,constituent,region,commodity,period,production,unit,casetype,asset_relationship,sources,data_source,add_by,add_date) VALUES (%s)' % var_str
		curr.execute(sql_insert, param_vals)
		
		curr.execute('COMMIT')


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def calc_field_analogues(clear_data=False, field_id=None, field_list=None, analogue_list=None, calc_scores=False,
						 enter_prod=False, conf_score=False, calc_conf=False, curve_score=False, in_place=False,
						 gen_lists=False, undiscovered=False, update_reserves=False, debug=False):
	global disc_field
	start_time = get_datetime()
	print 'start time:', start_time
	debug_mode = debug
	conn = start_database()
	curr = conn.cursor()
	if clear_data:
		clear_tables(curr)
	if field_id:
		field_list = [field_id]
	if calc_scores:
		enter_similiarity_scores(curr, field_list, in_place=in_place, with_tiers=False, analogue_pool=analogue_list, debug_mode=debug)
	if enter_prod:
		field_count = len(field_list)
		field_number = 1
		for field in field_list:
			print ''
			print '-=-' * 50
			print 'Entering production values for asset id %s ...' % field
			disc_field = field
			enter_production_data(curr, field, debug_mode, in_place, undiscovered=undiscovered, debug=debug)
			process_production_data(curr, field, debug_mode)
			print field, 'processed (%s/%s)' % (field_number, field_count)
			field_number += 1
	if update_reserves or enter_prod:
		update_reserve_volumes(curr)
		update_median_recov_factor(curr, debug=debug)
	if conf_score:
		enter_field_confidence_score(curr, field_list=field_list, calc_conf=calc_conf, curve_score=curve_score,
									 debug=debug_mode)
	if gen_lists:
		create_field_lists(undiscovered=undiscovered)
	curr.close()
	conn.close()
	end_time = get_datetime()
	print 'end time:', end_time
	print elapsed_time(start_time, end_time)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main(undiscovered=False, undisc_calc=False, undisc_prod=False, disc_calc=False, disc_prod=False,
		 discovered_fields=[], rerun=False, update_reserves=False, debug=False):
	if undiscovered:
		if undisc_calc:
			if len(discovered_fields) == 0:
				discovered_fields = get_data('asset_id', 'asset_data', datatype='int', sql_where='asset_id >= 9000001 AND IFNULL(reserve_volume,0)>0')
			for field in sorted(discovered_fields):
				print field
			calc_field_analogues(clear_data=False, field_list=discovered_fields, analogue_list=None, calc_scores=True,
								 undiscovered=True, update_reserves=update_reserves, debug=debug)
		if undisc_prod:
			if len(discovered_fields) == 0:
				discovered_fields = get_data('asset_id', 'asset_data', datatype='int', sql_where='asset_id >= 9000001 AND asset_id IN (SELECT DISTINCT asset_id FROM field_analogues)')
			for field in sorted(discovered_fields):
				print field
			calc_field_analogues(field_list=discovered_fields, analogue_list=None, enter_prod=True, conf_score=True,
								 calc_conf=True, curve_score=True, gen_lists=True, undiscovered=True, update_reserves=update_reserves, debug=debug)
	else:
		if disc_calc:
			if len(discovered_fields) == 0:
				discovered_fields = get_discovered_fields(with_analogues=False,
														  with_reserves=True,
														  not_modelled=False,
														  rerun=rerun,
														  debug=debug)
			for field in sorted(discovered_fields):
				print field
			calc_field_analogues(field_list=discovered_fields,
								 clear_data=True,
								 calc_scores=True,
								 enter_prod=False,
								 conf_score=False,
								 calc_conf=False,
								 curve_score=False,
								 gen_lists=False,
								 undiscovered=False,
								 update_reserves=update_reserves,
								 debug=debug)
		if disc_prod:
			if len(discovered_fields) == 0:
				discovered_fields = get_discovered_fields(with_analogues=True,
														  with_reserves=True,
														  not_modelled=False,
														  rerun=rerun,
														  debug=debug)
			for field in sorted(discovered_fields):
				print field
			calc_field_analogues(field_list=discovered_fields,
								 clear_data=False,
								 calc_scores=False,
								 enter_prod=True,
								 conf_score=True,
								 calc_conf=True,
								 curve_score=True,
								 gen_lists=True,
								 undiscovered=False,
								 update_reserves=update_reserves,
								 debug=debug)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	discovered_fields = [
		# 318581,
		# 329005,
		# 361903,
		# 501518,
		# 532608,
		# 541436,
		# 621645,
		# 637343,
		# 734284,
		# 999338,
		# 1026891,
		# 1227351,
		# 1483940,
		# 1504406,
		# 9000062,
		# 9001493,
		# 9001694,
		# 9001941,
		# 9001817,
		# 9000689,
		# 9000685,
		# 256727,
		# 9000453,
		# 643166
	
	]
	main(undiscovered=True, undisc_calc=True, undisc_prod=True, debug=False, disc_calc=False, disc_prod=False, update_reserves=False, discovered_fields=[], rerun=False)
	#calc_field_analogues(clear_data=False, field_list=discovered_fields, analogue_list=None, calc_scores=False, undiscovered=False, update_reserves=True, debug=True)