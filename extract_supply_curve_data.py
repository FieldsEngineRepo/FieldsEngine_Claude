import shutil

import xlwings as xw

from globaldata import *

PHASE_1_YEAR = 2020
SUPPLY_CURVE_DATA_DIR = DATA_DIR + 'extract_breakeven_data\\'
SUPPLY_CURVE_DATA_COLS = [
	('asset_id', 0),
	('asset_status', ''),
	('country', ''),
	('region', ''),
	('constituent', ''),
	('brent_be_usd_bbl_2020', 0.0),
	('gas_be_usd_mcf_2020', 0.0),
	('LNG_be_usd_mcf_2020', 0.0),
	('breakeven_factor_1', 0.0),
	('brent_be_usd_bbl_2025', 0.0),
	('gas_be_usd_mcf_2025', 0.0),
	('LNG_be_usd_mcf_2025', 0.0),
	('breakeven_factor_2', 0.0),
	('npv_brent_be_usd_bbl', 0.0),
	('npv_gas_be_usd_mcf', 0.0),
	('npv_LNG_be_usd_mcf', 0.0),
	('npv_factor', 0.0)
]

SUPPLY_CURVE_PROD_COLS = [
	'asset_id',
	'prod_year',
	'oil_prod_bbl',
	'gas_prod_mcf',
	'cond_prod_bbl',
	'lng_prod_mcf',
	'run_id'
]
SQL_EXPORT     = """SELECT * FROM globaldata.supply_breakeven_data_output WHERE run_id='{0}' INTO OUTFILE '{1}' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'"""


def copy_macro_files(run_id):
	breakeven_files = [
		'Breakeven_Africa.xlsm',
		'Breakeven_Asia.xlsm',
		'Breakeven_Caribbean.xlsm',
		'Breakeven_Central_America.xlsm',
		'Breakeven_Europe.xlsm',
		'Breakeven_Former_Soviet_Union.xlsm',
		'Breakeven_Middle_East.xlsm',
		'Breakeven_North_America_1.xlsm',
		'Breakeven_North_America_2.xlsm',
		'Breakeven_Oceania.xlsm',
		'Breakeven_South_America.xlsm',
		'Breakeven_Unconventional.xlsm'
	]
	for macrofile in breakeven_files:
		outfilename = '{}_{}{}'.format(macrofile[:-5], run_id, macrofile[-5:])
		shutil.copy2(BREAKEVEN_DIR + macrofile, SUPPLY_CURVE_DATA_DIR + outfilename)


def extract_breakeven_data(curr, run_id):
	xlApp = xw.App(visible=False)
	print 1
	data_col_str = ', '.join([col_name for (col_name, default_val) in SUPPLY_CURVE_DATA_COLS])
	data_var_str = ', '.join(['%s'] * len(SUPPLY_CURVE_DATA_COLS))
	sql_insert = 'INSERT INTO supply_breakeven_data_output ({}) VALUES ({}) '.format(data_col_str, data_var_str)
	print sql_insert
	for macrofile in [fname for fname in os.listdir(SUPPLY_CURVE_DATA_DIR) if run_id in fname]:
		wb = xlApp.books.open('{}{}'.format(SUPPLY_CURVE_DATA_DIR, macrofile))
		wb.app.screen_updating = False
		output = wb.sheets['Output']
		row_num = 2
		while output.range('A{}'.format(row_num)).raw_value is not None and len(
				str(output.range('A{}'.format(row_num)).raw_value)) > 0:
			print macrofile, int(output.range('A{}'.format(row_num)).raw_value)
			row_data_vals = ()
			for col_indx in range(len(SUPPLY_CURVE_DATA_COLS)):
				col = XL_COLS[col_indx]
				default_val = SUPPLY_CURVE_DATA_COLS[col_indx][1]
				datacell = '{}{}'.format(col, row_num)
				try:
					row_data_vals += (output.range(datacell).raw_value,)
				except:
					row_data_vals += (default_val,)
			#print sql_insert % row_data_vals
			curr.execute(sql_insert, row_data_vals)
			commit(curr)
			row_num += 1
		wb.close()
	xlApp.quit()
	del xlApp


def update_asset_data(curr, run_id):
	curr.execute('UPDATE supply_breakeven_data_output SET run_id="{}" WHERE run_id IS NULL'.format(run_id))
	commit(curr)
	curr.execute('UPDATE supply_breakeven_data_output AS a, assets AS b SET a.resource_type=b.resource_type WHERE a.asset_id=b.asset_id AND a.resource_type IS NULL AND a.run_id="{}"'.format(run_id))
	commit(curr)
	curr.execute('UPDATE globaldata.supply_breakeven_data_output AS a, globaldata.param_track AS b SET a.ngls_bm = b.ngls_benchmark WHERE a.asset_id=b.asset_id AND b.session_key LIKE CONCAT("%",a.run_id,"%") AND a.run_id="{}"'.format(run_id))
	commit(curr)
	curr.execute('UPDATE globaldata.supply_breakeven_data_output AS a, globaldata.param_track AS b SET a.lng_bm = b.lng_benchmark WHERE a.asset_id=b.asset_id AND b.session_key LIKE CONCAT("%",a.run_id,"%") AND a.run_id="{}"'.format(run_id))
	commit(curr)
	curr.execute('UPDATE globaldata.supply_breakeven_data_output AS a, globaldata.param_track AS b SET a.condensate_bm = b.condensate_benchmark WHERE a.asset_id=b.asset_id AND b.session_key LIKE CONCAT("%",a.run_id,"%") AND a.run_id="{}"'.format(run_id))
	commit(curr)
	curr.execute('UPDATE globaldata.supply_breakeven_data_output AS a, globaldata.param_track AS b SET a.ng_bm = b.ng_benchmark WHERE a.asset_id=b.asset_id AND b.session_key LIKE CONCAT("%",a.run_id,"%") AND a.run_id="{}"'.format(run_id))
	commit(curr)
	curr.execute('UPDATE globaldata.supply_breakeven_data_output AS a, globaldata.param_track AS b SET a.crude_bm = b.crude_benchmark WHERE a.asset_id=b.asset_id AND b.session_key LIKE CONCAT("%",a.run_id,"%") AND a.run_id="{}"'.format(run_id))
	commit(curr)
	curr.execute('UPDATE globaldata.supply_breakeven_data_output AS a, globaldata.param_track AS b SET a.production_end_year = b.cutoff_year WHERE a.asset_id=b.asset_id AND b.session_key LIKE CONCAT("%",a.run_id,"%") AND a.run_id="{}"'.format(run_id))
	commit(curr)
	
	sql_update = \
	"""
	UPDATE supply_breakeven_data_output AS a,
	       (SELECT DISTINCT asset_id, run_id, MIN(prod_year) AS development_start_year FROM supply_capex_data WHERE total_capex > 0 GROUP BY asset_id, run_id) AS b
	  SET a.development_start_year=b.development_start_year
	  WHERE a.asset_id=b.asset_id AND a.run_id=b.run_id;
	"""
	curr.execute(sql_update)
	commit(curr)
	sql_update_2 = \
	"""
	UPDATE supply_breakeven_data_output SET asset_status='UNDISCOVERED' WHERE asset_id > 9000000;
	"""
	curr.execute(sql_update_2)
	commit(curr)

def update_phase_prod_values(curr, run_id):
	supply_data_asset_ids = sorted(
		get_assets(table='supply_production_data', sql_where='run_id="{}" AND asset_id > 9000000'.format(run_id)))
	asset_count = 1
	for asset_id in supply_data_asset_ids:
		print '{}/{}: {}'.format(asset_count, len(supply_data_asset_ids), asset_id)
		start_year = 2020
		if asset_id in get_data('asset_id', 'development_start_year', datatype='int'):
			start_year = get_data('prod_year', 'development_start_year', datatype='int',
								  sql_where='asset_id={}'.format(asset_id), single_value=True)
		phase_years = [start_year, start_year + 5]
		sql_where = 'prod_year IN ({0}, {0}+5) AND run_id="{1}"'.format(start_year, run_id)
		curr.execute('SELECT DISTINCT prod_year FROM supply_production_data WHERE asset_id={} AND {}'.format(asset_id,
																											 sql_where))
		phase_prod_years = sorted([int(data[0]) for data in curr.fetchall()])
		sql_insert = 'INSERT INTO supply_production_data (asset_id, prod_year, oil_prod_bbl, gas_prod_mcf, cond_prod_bbl, lng_prod_mcf, run_id) VALUES ({}, {}, 0, 0, 0, 0, "{}")'
		for phase_year in phase_years:
			if phase_year not in phase_prod_years:
				curr.execute(sql_insert.format(asset_id, phase_year, run_id))
				commit(curr)
		phase_num = 1
		sql_update = \
			'''
			UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.phase_{0}_oil_bbl=(b.oil_prod_bbl+b.cond_prod_bbl), a.phase_{0}_gas_mcf=b.gas_prod_mcf, a.phase_{0}_lng_mcf=b.lng_prod_mcf
			WHERE b.prod_year={1} AND a.asset_id={2} AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id="{3}"
			'''
		for phase_prod_year in phase_prod_years:
			curr.execute(sql_update.format(phase_num, phase_prod_year, asset_id, run_id))
			commit(curr)
			phase_num += 1
		asset_count += 1


def update_prod_data(curr, run_id):
	print 'Updating production and capex values ...'
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_0=0 WHERE b.prod_year=a.development_start_year+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_1=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year=a.development_start_year+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_2=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year=a.development_start_year+1 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_3=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year=a.development_start_year+2 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_4=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year=a.development_start_year+3 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_5=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year=a.development_start_year+4 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_6=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year=a.development_start_year+5 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_7=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year=a.development_start_year+6 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_8=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year=a.development_start_year+7 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_9=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year=a.development_start_year+8 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_10=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year=a.development_start_year+9 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	print 'Update 1 complete'
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_0=0 WHERE b.prod_year=a.development_start_year+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_1=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_2=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+1 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_3=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+2 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_4=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+3 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_5=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+4 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_6=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+5 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_7=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+6 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_8=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+7 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_9=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+8 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_10=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+9 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	print 'Update 2 complete'
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_0=0 WHERE b.prod_year=a.development_start_year+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_1=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_2=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+1 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_3=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+2 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_4=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+3 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_5=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+4 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_6=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+5 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_7=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+6 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_8=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+7 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_9=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+8 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_10=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year=a.development_start_year+9 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	print 'Update 3 complete'
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_0=0 WHERE b.prod_year=a.development_start_year+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_1=b.total_capex WHERE b.prod_year=a.development_start_year+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_2=b.total_capex WHERE b.prod_year=a.development_start_year+1 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_3=b.total_capex WHERE b.prod_year=a.development_start_year+2 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_4=b.total_capex WHERE b.prod_year=a.development_start_year+3 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_5=b.total_capex WHERE b.prod_year=a.development_start_year+4 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_6=b.total_capex WHERE b.prod_year=a.development_start_year+5 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_7=b.total_capex WHERE b.prod_year=a.development_start_year+6 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_8=b.total_capex WHERE b.prod_year=a.development_start_year+7 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_9=b.total_capex WHERE b.prod_year=a.development_start_year+8 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_10=b.total_capex WHERE b.prod_year=a.development_start_year+9 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{0}' AND a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(run_id))
	commit(curr)
	print 'Update 4 complete'
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_0=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_1=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+1 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_2=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+2 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_3=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+3 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_4=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+4 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_5=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+5 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_6=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+6 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_7=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+7 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_8=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+8 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_9=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+9 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.oil_cond_bd_yr_10=ROUND((b.oil_prod_bbl+b.cond_prod_bbl)/365.242,2) WHERE b.prod_year={0}+10 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	print 'Update 5 complete'
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_0=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_1=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+1 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_2=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+2 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_3=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+3 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_4=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+4 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_5=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+5 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_6=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+6 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_7=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+7 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_8=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+8 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_9=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+9 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.gas_mmcfd_yr_10=ROUND((b.gas_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+10 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	print 'Update 6 complete'
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_0=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_1=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+1 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_2=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+2 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_3=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+3 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_4=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+4 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_5=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+5 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_6=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+6 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_7=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+7 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_8=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+8 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_9=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+9 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_production_data AS b SET a.LNG_mmcfd_yr_10=ROUND((b.lng_prod_mcf/1000.0)/365.242,2) WHERE b.prod_year={0}+10 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	print 'Update 7 complete'
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_0=b.total_capex WHERE b.prod_year={0}+0 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_1=b.total_capex WHERE b.prod_year={0}+1 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_2=b.total_capex WHERE b.prod_year={0}+2 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_3=b.total_capex WHERE b.prod_year={0}+3 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_4=b.total_capex WHERE b.prod_year={0}+4 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_5=b.total_capex WHERE b.prod_year={0}+5 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_6=b.total_capex WHERE b.prod_year={0}+6 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_7=b.total_capex WHERE b.prod_year={0}+7 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_8=b.total_capex WHERE b.prod_year={0}+8 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_9=b.total_capex WHERE b.prod_year={0}+9 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	curr.execute("UPDATE supply_breakeven_data_output AS a, supply_capex_data AS b SET a.capex_mm_usd_yr_10=b.total_capex WHERE b.prod_year={0}+10 AND a.asset_id=b.asset_id AND a.run_id=b.run_id AND a.run_id='{1}' AND NOT a.asset_status IN ('DISCOVERED', 'STALLED', 'UNDISCOVERED')".format(PHASE_1_YEAR, run_id))
	commit(curr)
	sql_update_1 = \
		"""
		UPDATE globaldata.supply_breakeven_data_output AS a, assets AS b
		  SET a.constituent=b.constituent
		  WHERE a.asset_id=b.asset_id AND a.constituent IS NULL;
		"""
	sql_update_2 = \
		"""
		UPDATE supply_breakeven_data_output 
		  SET npv_factor=ROUND(npv_factor, 2),
			  npv_brent_be_usd_bbl=ROUND(npv_brent_be_usd_bbl, 2),
			  npv_gas_be_usd_mcf=ROUND(npv_gas_be_usd_mcf, 2),
			  npv_LNG_be_usd_mcf=ROUND(npv_LNG_be_usd_mcf, 2),
			  breakeven_factor_1=ROUND(breakeven_factor_1, 2),
			  brent_be_usd_bbl_2020=ROUND(brent_be_usd_bbl_2020, 2),
			  gas_be_usd_mcf_2020=ROUND(gas_be_usd_mcf_2020, 2),
			  LNG_be_usd_mcf_2020=ROUND(LNG_be_usd_mcf_2020, 2),
			  breakeven_factor_2=ROUND(breakeven_factor_2, 2),
			  brent_be_usd_bbl_2025=ROUND(brent_be_usd_bbl_2025, 2),
			  gas_be_usd_mcf_2025=ROUND(gas_be_usd_mcf_2025, 2),
			  LNG_be_usd_mcf_2025=ROUND(LNG_be_usd_mcf_2025, 2),
			  oil_cond_bd_yr_0=ROUND(oil_cond_bd_yr_0, 2),
			  oil_cond_bd_yr_1=ROUND(oil_cond_bd_yr_1, 2),
			  oil_cond_bd_yr_2=ROUND(oil_cond_bd_yr_2, 2),
			  oil_cond_bd_yr_3=ROUND(oil_cond_bd_yr_3, 2),
			  oil_cond_bd_yr_4=ROUND(oil_cond_bd_yr_4, 2),
			  oil_cond_bd_yr_5=ROUND(oil_cond_bd_yr_5, 2),
			  oil_cond_bd_yr_6=ROUND(oil_cond_bd_yr_6, 2),
			  oil_cond_bd_yr_7=ROUND(oil_cond_bd_yr_7, 2),
			  oil_cond_bd_yr_8=ROUND(oil_cond_bd_yr_8, 2),
			  oil_cond_bd_yr_9=ROUND(oil_cond_bd_yr_9, 2),
			  oil_cond_bd_yr_10=ROUND(oil_cond_bd_yr_10, 2),
			  gas_mmcfd_yr_0=ROUND(gas_mmcfd_yr_0, 2),
			  gas_mmcfd_yr_1=ROUND(gas_mmcfd_yr_1, 2),
			  gas_mmcfd_yr_2=ROUND(gas_mmcfd_yr_2, 2),
			  gas_mmcfd_yr_3=ROUND(gas_mmcfd_yr_3, 2),
			  gas_mmcfd_yr_4=ROUND(gas_mmcfd_yr_4, 2),
			  gas_mmcfd_yr_5=ROUND(gas_mmcfd_yr_5, 2),
			  gas_mmcfd_yr_6=ROUND(gas_mmcfd_yr_6, 2),
			  gas_mmcfd_yr_7=ROUND(gas_mmcfd_yr_7, 2),
			  gas_mmcfd_yr_8=ROUND(gas_mmcfd_yr_8, 2),
			  gas_mmcfd_yr_9=ROUND(gas_mmcfd_yr_9, 2),
			  gas_mmcfd_yr_10=ROUND(gas_mmcfd_yr_10, 2),
			  LNG_mmcfd_yr_0=ROUND(LNG_mmcfd_yr_0, 2),
			  LNG_mmcfd_yr_1=ROUND(LNG_mmcfd_yr_1, 2),
			  LNG_mmcfd_yr_2=ROUND(LNG_mmcfd_yr_2, 2),
			  LNG_mmcfd_yr_3=ROUND(LNG_mmcfd_yr_3, 2),
			  LNG_mmcfd_yr_4=ROUND(LNG_mmcfd_yr_4, 2),
			  LNG_mmcfd_yr_5=ROUND(LNG_mmcfd_yr_5, 2),
			  LNG_mmcfd_yr_6=ROUND(LNG_mmcfd_yr_6, 2),
			  LNG_mmcfd_yr_7=ROUND(LNG_mmcfd_yr_7, 2),
			  LNG_mmcfd_yr_8=ROUND(LNG_mmcfd_yr_8, 2),
			  LNG_mmcfd_yr_9=ROUND(LNG_mmcfd_yr_9, 2),
			  LNG_mmcfd_yr_10=ROUND(LNG_mmcfd_yr_10, 2),
			  capex_mm_usd_yr_0=ROUND(capex_mm_usd_yr_0, 2),
			  capex_mm_usd_yr_1=ROUND(capex_mm_usd_yr_1, 2),
			  capex_mm_usd_yr_2=ROUND(capex_mm_usd_yr_2, 2),
			  capex_mm_usd_yr_3=ROUND(capex_mm_usd_yr_3, 2),
			  capex_mm_usd_yr_4=ROUND(capex_mm_usd_yr_4, 2),
			  capex_mm_usd_yr_5=ROUND(capex_mm_usd_yr_5, 2),
			  capex_mm_usd_yr_6=ROUND(capex_mm_usd_yr_6, 2),
			  capex_mm_usd_yr_7=ROUND(capex_mm_usd_yr_7, 2),
			  capex_mm_usd_yr_8=ROUND(capex_mm_usd_yr_8, 2),
			  capex_mm_usd_yr_9=ROUND(capex_mm_usd_yr_9, 2),
			  capex_mm_usd_yr_10=ROUND(capex_mm_usd_yr_10, 2);
		"""
	curr.execute(sql_update_1)
	commit(curr)
	curr.execute(sql_update_2)
	commit(curr)


def update_undisc_reserves_data(curr, run_id):
	sql_insert = \
		'''
		INSERT INTO supply_breakeven_data_output (asset_id, asset_status, development_start_year, run_id)
		  (SELECT DISTINCT a.asset_id, 'Undiscovered', a.period, '{0}'
		   FROM country_reserves_forecast AS a,
		   	   (SELECT DISTINCT asset_id, development_start_year FROM supply_breakeven_data_output WHERE asset_id > 9000000 AND run_id='{0}') AS b
		   WHERE a.period >= 2020 AND a.period <= 2029 AND a.asset_id=b.asset_id AND a.period!=b.development_start_year);
		'''
	sql_update_0 = \
	'''
	DELETE FROM supply_breakeven_data_output WHERE asset_id IN (SELECT DISTINCT asset_id FROM basin_country_data WHERE IFNULL(total_reserves_boe,0)=0);
	'''
	sql_update_1 = \
		'''
		UPDATE supply_breakeven_data_output AS a, supply_breakeven_data_output AS b
		  SET a.asset_status=b.asset_status,
			  a.country=b.country,
			  a.region=b.region,
			  a.constituent=b.constituent,
			  a.resource_type=b.resource_type,
			  a.crude_bm=b.crude_bm,
			  a.ng_bm=b.ng_bm,
			  a.condensate_bm=b.condensate_bm,
			  a.lng_bm=b.lng_bm,
			  a.ngls_bm=b.ngls_bm,
			  a.production_end_year=b.production_end_year,
			  a.npv_factor=b.npv_factor,
			  a.npv_brent_be_usd_bbl=b.npv_brent_be_usd_bbl,
			  a.npv_gas_be_usd_mcf=b.npv_gas_be_usd_mcf,
			  a.npv_LNG_be_usd_mcf=b.npv_LNG_be_usd_mcf,
			  a.breakeven_factor_1=b.breakeven_factor_1,
			  a.brent_be_usd_bbl_2020=b.brent_be_usd_bbl_2020,
			  a.gas_be_usd_mcf_2020=b.gas_be_usd_mcf_2020,
			  a.LNG_be_usd_mcf_2020=b.LNG_be_usd_mcf_2020,
			  a.breakeven_factor_2=b.breakeven_factor_2,
			  a.brent_be_usd_bbl_2025=b.brent_be_usd_bbl_2025,
			  a.gas_be_usd_mcf_2025=b.gas_be_usd_mcf_2025,
			  a.LNG_be_usd_mcf_2025=b.LNG_be_usd_mcf_2025,
			  a.oil_cond_bd_yr_0=b.oil_cond_bd_yr_0,
			  a.oil_cond_bd_yr_1=b.oil_cond_bd_yr_1,
			  a.oil_cond_bd_yr_2=b.oil_cond_bd_yr_2,
			  a.oil_cond_bd_yr_3=b.oil_cond_bd_yr_3,
			  a.oil_cond_bd_yr_4=b.oil_cond_bd_yr_4,
			  a.oil_cond_bd_yr_5=b.oil_cond_bd_yr_5,
			  a.oil_cond_bd_yr_6=b.oil_cond_bd_yr_6,
			  a.oil_cond_bd_yr_7=b.oil_cond_bd_yr_7,
			  a.oil_cond_bd_yr_8=b.oil_cond_bd_yr_8,
			  a.oil_cond_bd_yr_9=b.oil_cond_bd_yr_9,
			  a.oil_cond_bd_yr_10=b.oil_cond_bd_yr_10,
			  a.gas_mmcfd_yr_0=b.gas_mmcfd_yr_0,
			  a.gas_mmcfd_yr_1=b.gas_mmcfd_yr_1,
			  a.gas_mmcfd_yr_2=b.gas_mmcfd_yr_2,
			  a.gas_mmcfd_yr_3=b.gas_mmcfd_yr_3,
			  a.gas_mmcfd_yr_4=b.gas_mmcfd_yr_4,
			  a.gas_mmcfd_yr_5=b.gas_mmcfd_yr_5,
			  a.gas_mmcfd_yr_6=b.gas_mmcfd_yr_6,
			  a.gas_mmcfd_yr_7=b.gas_mmcfd_yr_7,
			  a.gas_mmcfd_yr_8=b.gas_mmcfd_yr_8,
			  a.gas_mmcfd_yr_9=b.gas_mmcfd_yr_9,
			  a.gas_mmcfd_yr_10=b.gas_mmcfd_yr_10,
			  a.LNG_mmcfd_yr_0=b.LNG_mmcfd_yr_0,
			  a.LNG_mmcfd_yr_1=b.LNG_mmcfd_yr_1,
			  a.LNG_mmcfd_yr_2=b.LNG_mmcfd_yr_2,
			  a.LNG_mmcfd_yr_3=b.LNG_mmcfd_yr_3,
			  a.LNG_mmcfd_yr_4=b.LNG_mmcfd_yr_4,
			  a.LNG_mmcfd_yr_5=b.LNG_mmcfd_yr_5,
			  a.LNG_mmcfd_yr_6=b.LNG_mmcfd_yr_6,
			  a.LNG_mmcfd_yr_7=b.LNG_mmcfd_yr_7,
			  a.LNG_mmcfd_yr_8=b.LNG_mmcfd_yr_8,
			  a.LNG_mmcfd_yr_9=b.LNG_mmcfd_yr_9,
			  a.LNG_mmcfd_yr_10=b.LNG_mmcfd_yr_10,
			  a.capex_mm_usd_yr_0=b.capex_mm_usd_yr_0,
			  a.capex_mm_usd_yr_1=b.capex_mm_usd_yr_1,
			  a.capex_mm_usd_yr_2=b.capex_mm_usd_yr_2,
			  a.capex_mm_usd_yr_3=b.capex_mm_usd_yr_3,
			  a.capex_mm_usd_yr_4=b.capex_mm_usd_yr_4,
			  a.capex_mm_usd_yr_5=b.capex_mm_usd_yr_5,
			  a.capex_mm_usd_yr_6=b.capex_mm_usd_yr_6,
			  a.capex_mm_usd_yr_7=b.capex_mm_usd_yr_7,
			  a.capex_mm_usd_yr_8=b.capex_mm_usd_yr_8,
			  a.capex_mm_usd_yr_9=b.capex_mm_usd_yr_9,
			  a.capex_mm_usd_yr_10=b.capex_mm_usd_yr_10
		  WHERE a.asset_id=b.asset_id
		  AND b.country IS NOT NULL
		  AND a.country IS NULL
		  AND a.asset_status='Undiscovered'
		  AND a.run_id=b.run_id;
		'''
	

	sql_update_2 = \
		'''
		UPDATE supply_breakeven_data_output AS c,
			 (SELECT DISTINCT a.asset_id, ROUND(a.proj_reserves_boe/b.avg_field_reserves, 5) AS proj_reserves_pct, a.period
                FROM country_reserves_forecast AS a,
                	 basin_country_data AS b
			    WHERE a.asset_id=b.asset_id
			  	  AND a.period >= 2020
			  	  AND a.period <= 2029
			  	  AND b.avg_field_reserves > 0
			    ORDER BY a. asset_id, a.period) AS d
		  SET c.oil_cond_bd_yr_0=d.proj_reserves_pct*c.oil_cond_bd_yr_0,
			  c.oil_cond_bd_yr_1=d.proj_reserves_pct*c.oil_cond_bd_yr_1,
			  c.oil_cond_bd_yr_2=d.proj_reserves_pct*c.oil_cond_bd_yr_2,
			  c.oil_cond_bd_yr_3=d.proj_reserves_pct*c.oil_cond_bd_yr_3,
			  c.oil_cond_bd_yr_4=d.proj_reserves_pct*c.oil_cond_bd_yr_4,
			  c.oil_cond_bd_yr_5=d.proj_reserves_pct*c.oil_cond_bd_yr_5,
			  c.oil_cond_bd_yr_6=d.proj_reserves_pct*c.oil_cond_bd_yr_6,
			  c.oil_cond_bd_yr_7=d.proj_reserves_pct*c.oil_cond_bd_yr_7,
			  c.oil_cond_bd_yr_8=d.proj_reserves_pct*c.oil_cond_bd_yr_8,
			  c.oil_cond_bd_yr_9=d.proj_reserves_pct*c.oil_cond_bd_yr_9,
			  c.oil_cond_bd_yr_10=d.proj_reserves_pct*c.oil_cond_bd_yr_10,
			  c.gas_mmcfd_yr_0=d.proj_reserves_pct*c.gas_mmcfd_yr_0,
			  c.gas_mmcfd_yr_1=d.proj_reserves_pct*c.gas_mmcfd_yr_1,
			  c.gas_mmcfd_yr_2=d.proj_reserves_pct*c.gas_mmcfd_yr_2,
			  c.gas_mmcfd_yr_3=d.proj_reserves_pct*c.gas_mmcfd_yr_3,
			  c.gas_mmcfd_yr_4=d.proj_reserves_pct*c.gas_mmcfd_yr_4,
			  c.gas_mmcfd_yr_5=d.proj_reserves_pct*c.gas_mmcfd_yr_5,
			  c.gas_mmcfd_yr_6=d.proj_reserves_pct*c.gas_mmcfd_yr_6,
			  c.gas_mmcfd_yr_7=d.proj_reserves_pct*c.gas_mmcfd_yr_7,
			  c.gas_mmcfd_yr_8=d.proj_reserves_pct*c.gas_mmcfd_yr_8,
			  c.gas_mmcfd_yr_9=d.proj_reserves_pct*c.gas_mmcfd_yr_9,
			  c.gas_mmcfd_yr_10=d.proj_reserves_pct*c.gas_mmcfd_yr_10,
			  c.LNG_mmcfd_yr_0=d.proj_reserves_pct*c.LNG_mmcfd_yr_0,
			  c.LNG_mmcfd_yr_1=d.proj_reserves_pct*c.LNG_mmcfd_yr_1,
			  c.LNG_mmcfd_yr_2=d.proj_reserves_pct*c.LNG_mmcfd_yr_2,
			  c.LNG_mmcfd_yr_3=d.proj_reserves_pct*c.LNG_mmcfd_yr_3,
			  c.LNG_mmcfd_yr_4=d.proj_reserves_pct*c.LNG_mmcfd_yr_4,
			  c.LNG_mmcfd_yr_5=d.proj_reserves_pct*c.LNG_mmcfd_yr_5,
			  c.LNG_mmcfd_yr_6=d.proj_reserves_pct*c.LNG_mmcfd_yr_6,
			  c.LNG_mmcfd_yr_7=d.proj_reserves_pct*c.LNG_mmcfd_yr_7,
			  c.LNG_mmcfd_yr_8=d.proj_reserves_pct*c.LNG_mmcfd_yr_8,
			  c.LNG_mmcfd_yr_9=d.proj_reserves_pct*c.LNG_mmcfd_yr_9,
			  c.LNG_mmcfd_yr_10=d.proj_reserves_pct*c.LNG_mmcfd_yr_10,
			  c.capex_mm_usd_yr_0=d.proj_reserves_pct*c.capex_mm_usd_yr_0,
			  c.capex_mm_usd_yr_1=d.proj_reserves_pct*c.capex_mm_usd_yr_1,
			  c.capex_mm_usd_yr_2=d.proj_reserves_pct*c.capex_mm_usd_yr_2,
			  c.capex_mm_usd_yr_3=d.proj_reserves_pct*c.capex_mm_usd_yr_3,
			  c.capex_mm_usd_yr_4=d.proj_reserves_pct*c.capex_mm_usd_yr_4,
			  c.capex_mm_usd_yr_5=d.proj_reserves_pct*c.capex_mm_usd_yr_5,
			  c.capex_mm_usd_yr_6=d.proj_reserves_pct*c.capex_mm_usd_yr_6,
			  c.capex_mm_usd_yr_7=d.proj_reserves_pct*c.capex_mm_usd_yr_7,
			  c.capex_mm_usd_yr_8=d.proj_reserves_pct*c.capex_mm_usd_yr_8,
			  c.capex_mm_usd_yr_9=d.proj_reserves_pct*c.capex_mm_usd_yr_9,
			  c.capex_mm_usd_yr_10=d.proj_reserves_pct*c.capex_mm_usd_yr_10
		  WHERE c.asset_id=d.asset_id AND c.development_start_year=d.period AND c.asset_status='Undiscovered';
		'''
	print sql_insert.format(run_id)
	curr.execute(sql_insert.format(run_id))
	commit(curr)
	print sql_update_0.format(run_id)
	curr.execute(sql_update_0.format(run_id))
	commit(curr)
	print sql_update_1.format(run_id)
	curr.execute(sql_update_1.format(run_id))
	commit(curr)
	print sql_update_2
	curr.execute(sql_update_2)
	commit(curr)

'''
/* (SELECT DISTINCT a.asset_id, a.terrain, a.resource_type, a.period, a.proj_reserves_boe/b.total_proj_reserves AS proj_reserves_pct
   FROM country_reserves_forecast AS a,
	   (SELECT DISTINCT d.asset_id, d.terrain, d.resource_type, e.total_reserves_boe AS total_proj_reserves
		  FROM globaldata.country_reserves_forecast AS d,
			   globaldata.basin_country_data AS e
		  WHERE d.asset_id=e.asset_id) AS b
   WHERE b.total_proj_reserves > 0 AND a.asset_id=b.asset_id AND a.terrain=b.terrain AND a.resource_type=b.resource_type) AS d */
 '''

def export_supply_curve_data(curr, run_id):
	outfile = REPORTS_DIR + 'supply_breakeven_data_output_{}.csv'.format(run_id)
	print 'Exporting supply_breakeven_data_output >> {} ...'.format(outfile)
	outfile = outfile.replace('\\', '\\\\')
	curr.execute(SQL_EXPORT.format(run_id, outfile))


def main(run_id=None, copy_data=False, extract=False, update=False, update_prod=False, export_data=False, undisc=False, extract_prod=False):
	if run_id:
		runid = run_id
	else:
		runid = get_run_id()
	print get_datetime()
	
	conn = get_connection()
	curr = conn.cursor()
	
	if copy_data:
		copy_macro_files(runid)
	if extract:
		extract_breakeven_data(curr=curr, run_id=runid)
	if update:
		update_asset_data(curr=curr, run_id=runid)
	if update_prod:
		update_prod_data(curr, run_id=runid)
	if undisc:
		update_undisc_reserves_data(curr, run_id=run_id)
	if export_data:
		export_supply_curve_data(curr, run_id=runid)
	print get_datetime()
	curr.close()
	conn.close()


if __name__ == '__main__':
	main(run_id='20210111_100752', copy_data=False, extract=True, update=True, update_prod=True, undisc=False, export_data=False)
