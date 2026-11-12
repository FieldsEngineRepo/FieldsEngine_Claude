from globaldata import *
import os
import xlwings as xw

FISCAL_MODEL_DIR = ENGINE_DIR + "Fiscal\\UltraLight\\"

def extract_data():
	start_time = get_datetime()
	xlApp = xw.App(visible=False)

	all_asset_files = os.listdir(FISCAL_MODEL_DIR)
	for asset_file in all_asset_files:
		if asset_file[:2] == '~$':
			os.remove(asset_file)

	fiscal_models = [model for model in all_asset_files if model[-4:] == 'xlsx']
	model_count = len(fiscal_models)
	model_num = 1
	check_models = []

	for fiscal_model in fiscal_models:
		wb = xlApp.books.open(r'%s%s' % (FISCAL_MODEL_DIR, fiscal_model))
		wb.app.calculation = 'semiautomatic'
		fiscal_inputs  = wb.sheets['Fiscal Inputs']
		fx_unit = fiscal_inputs.range('J5').value
		if len(str(fx_unit).strip()) < 1:
			check_models.append(fiscal_model)
		print '{}/{}: {}\t{}'.format(model_num, model_count, fiscal_model, fx_unit)
		wb.close()
		model_num += 1

	xlApp.quit()
	end_time = get_datetime()
	total_time = elapsed_time(start_time, end_time)

	print ''
	print 'Check Models:'
	for check_model in check_models:
		print check_model
	print ''
	print 'Total Time: %s' % total_time
	print ''


if __name__ == '__main__':
	extract_data()
