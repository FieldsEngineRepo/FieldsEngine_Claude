from globaldata import *
import xlwings as xw
from time import sleep


debug_mode = True


def read_scenario_input_data(scenario_conf):
    scenario_data_file = scenario_conf['data file']
    scenario_table     = scenario_conf['table']
    scenario_data_cols = scenario_conf['data cols']

    xlApp = xw.App(visible=False)
    xlApp.display_alerts = False
    wb = xlApp.books.open(scenario_data_file)
    wb.app.calculation = 'semiautomatic'
    ws = wb.sheets['Data']
    table_cols = get_columns(scenario_table, no_id=True)
    col_prod_data = {}
    for col in XL_COLS[:len(table_cols)]:
        if ws.range(col+str(1)).raw_value:
            try:
                col_name = ws.range(col+str(1)).raw_value.lower()
                col_name = '_'.join(col_name.split())
                if col_name in scenario_data_cols:
                    col_prod_data[col] = col_name
            except:
                pass
    row_num = 2
    while row_num <= max_row(scenario_data_file, 'Data'):
        prod_data = {data_col_name: None for data_col_name in scenario_data_cols}
        for data_col in col_prod_data.keys():
            col_name = col_prod_data[data_col]
            prod_data[col_name] = ws.range(data_col + str(row_num)).raw_value
        scenario_conf['data'].append(prod_data)
        row_num += 1
    wb.close()
    xlApp.quit()
    return scenario_conf



def update_scenario_data(curr, scenario_conf):
    scenario_table = scenario_conf['table']
    id_cols        = scenario_conf['id cols']
    change_cols    = scenario_conf['change cols']
    data_cols      = scenario_conf['data cols']
    scenario_data  = scenario_conf['data']

    sql_update = 'UPDATE {} SET {} WHERE {}'

    sql_where = get_update_str(id_cols)
    if debug_mode:
        print 'sql_where: {}'.format(sql_where)

    sql_set = get_set_str(change_cols)
    if debug_mode:
        print 'sql_set: {}'.format(sql_set)

    sql_update = 'UPDATE {} SET {} WHERE {}'.format(scenario_table, sql_set, sql_where)
    if debug_mode:
        print 'sql_update: {}'.format(sql_update)

    for prod_data in scenario_data:
        param_vals = ()
        for data_col in data_cols:
            param_vals += (prod_data[data_col],)
        if debug_mode:
            print 'param_vals: {}'.format(param_vals)
        curr.execute(sql_update, param_vals)
        commit(curr)
    return scenario_conf

def make_scenario_dirs(scenario_conf):
    print 'Creating Scenario Directories ...'
    scenario_num = scenario_conf['num']
    region_count = scenario_conf['region count']
    if not os.path.exists(SCENARIO_DIR):
        os.mkdir(SCENARIO_DIR)

    if not os.path.exists(SCENARIO_DIR+'scenario_{}\\'.format(scenario_num)):
        os.mkdir(SCENARIO_DIR+'scenario_{}\\'.format(scenario_num))

    if not os.path.exists(SCENARIO_DIR+'scenario_{}\\engine\\'.format(scenario_num)):
        os.mkdir(SCENARIO_DIR+'scenario_{}\\engine\\'.format(scenario_num))

    for region_num in range(1, region_count + 1):
        if not os.path.exists(SCENARIO_DIR+'scenario_{}\\region_{}\\'.format(scenario_num, region_num)):
            os.mkdir(SCENARIO_DIR + 'scenario_{}\\region_{}\\'.format(scenario_num, region_num))
        shutil.copy2(SCENARIO_DIR + 'Breakeven_Scenario_.xlsm',
                     SCENARIO_DIR + 'scenario_{}\\Breakeven_Scenario_{}.xlsm'.format(scenario_num,region_num))
        breakeven_config('engine', scenario_num, region_num)


def create_scenario_models(scenario_conf, command, run_cmd=False):
    scenario_data = scenario_conf['data']
    scenario_num  = scenario_conf['num']
    region_count  = scenario_conf['region count']
    asset_ids = sorted(list(set([str(int(scenario_data[i]['asset_id'])) for i in range(len(scenario_data))])))
    cmd = '%cmd% create_model -scnr-"{}|{}|{}" \n\n'.format(scenario_num, region_count, ','.join(asset_ids))
    if run_cmd:
        os.system(cmd)
        cmd = '::' + cmd
    command += cmd
    if debug_mode:
        print command
    return command

def update_scenario_econ_data(command, run_cmd=False):
    cmd = 'ECHO Updating econ_data table with asset data...\n'
    cmd += '%cmd% update_econ_data -ab %*\n\n'
    if run_cmd:
        os.system(cmd)
        cmd = '::' + cmd
    command += cmd
    if debug_mode:
        print command
    return command

def copy_scenario_models(scenario_conf):
    print 'Copying Scenario models...'
    scenario_num = scenario_conf['num']
    region_count = scenario_conf['region count']
    scenario_models = [mod for mod in os.listdir(SCENARIO_DIR+'scenario_{}\\engine\\'.format(scenario_num)) if mod[0] != "~" and mod[:8] == "MODELLED"]
    scenario_model_count = len(scenario_models)
    scenario_region_dist = scenario_model_count/region_count
    for region_num in range(1,region_count+1):
        model_start = scenario_region_dist*(region_num-1)
        model_end = scenario_region_dist*region_num
        region_models = scenario_models[model_start: model_end]
        if region_num == region_count:
            region_models = scenario_models[model_start:]
        for model in region_models:
            shutil.copy2(SCENARIO_DIR+'scenario_{}\\engine\\{}'.format(scenario_num,model), SCENARIO_DIR+'scenario_{}\\region_{}\\{}'.format(scenario_num,region_num, model))

def run_scenario_breakeven_macro(command, scenario_conf, run_cmd=False):
    command_list = []
    copy_scenario_models(scenario_conf)
    scenario_num = scenario_conf['num']
    region_count = scenario_conf['region count']
    cmd = 'ECHO Running Scenario %s Breakeven Macro...\n' % (scenario_num)
    command_list.append(cmd)
    for region_num in range(1,region_count+1):
        cmd = '''powershell -Command "& {$app = New-Object -comobject Excel.Application; $wb = $app.Workbooks.Open('%s:\GlobalData\Regions\Scenarios\scenario_%s\Breakeven_Scenario_%s.xlsm'); $app.Run('ProcessFolderBreakevens'); $wb.Save(); $app.Quit();}"\n\n'''
        cmd = cmd % ("%engine_drive%",scenario_num, region_num)
        if run_cmd:
            os.system(cmd)
            cmd = '::' + cmd
            sleep(10)
        command_list.append(cmd)
    for cmd_ in command_list:
        command += cmd_
    if debug_mode:
        print command
    return command

def extract_scenario_econ_data(command, scenario_conf, run_cmd=False):
    scenario_num = scenario_conf['num']
    region_count = scenario_conf['region count']
    cmd = 'ECHO Extracting Model Data for econ_data Table...\n'
    for region_num in range(1,region_count+1):
        cmd += '''%cmd% extract_econ_data "scenario_{}\\region_{}" %*\n\n'''.format(scenario_num, region_num)
        cmd = cmd.format(scenario_num, region_num)
        if run_cmd:
            os.system(cmd)
            cmd = '::' + cmd
            sleep(10)
        command += cmd
    if debug_mode:
        print command
    return command

def extract_scenario_export_data(command, scenario_conf, run_cmd=False):
    scenario_num = scenario_conf['num']
    region_count = scenario_conf['region count']
    cmd = 'ECHO Extracting Export Data from Scenario Models ...\n'
    for region_num in range(1,region_count+1):
        cmd += '''%cmd% scenario_extract {}:{} %*\n\n'''.format(scenario_num, region_num)
        if run_cmd:
            os.system(cmd)
            cmd = '::' + cmd
            sleep(10)
        command += cmd
    return command

def generate_scenario_reports():
    pass

def main(scenario_conf, update_db=False, run_task=False, create_models=False, run_create_cmd=False, update_econ_data=False, run_update_cmd=False, run_breakevens=False, run_breakeven_cmd=False, extract_econ_data=False, run_econ_cmd=False, extract_export_data=False, run_extract_cmd=False, generate_reports=False):
    conn = get_connection()
    curr = conn.cursor()
    task_commands = '@ECHO OFF\n\n'
    if update_db:
        scenario_conf = read_scenario_input_data(scenario_conf)
        scenario_conf = update_scenario_data(curr, scenario_conf)
    if run_task:
        make_scenario_dirs(scenario_conf)
        if create_models:
            task_commands = create_scenario_models(scenario_conf, task_commands, run_cmd=run_create_cmd)
        if update_econ_data:
            task_commands = update_scenario_econ_data(task_commands, run_cmd=run_update_cmd)
        if run_breakevens:
            task_commands = run_scenario_breakeven_macro(task_commands, scenario_conf, run_cmd=run_breakeven_cmd)
        if extract_econ_data:
            task_commands = extract_scenario_econ_data(task_commands, scenario_conf, run_cmd=run_econ_cmd)
        if extract_export_data:
            task_commands = extract_scenario_export_data(task_commands, scenario_conf, run_cmd=run_extract_cmd)
        task_commands += 'EXIT\n'
        scenario_date = scenario_conf['date']
        scenario_num  = scenario_conf['num']
        with open(CMD_TASK_DIR+'scenario_{}_{}.bat'.format(scenario_num, scenario_date), 'w') as scenario_task:
            scenario_task.write(task_commands)
        command = 'START ' + CMD_TASK_DIR+'scenario_{}_{}.bat'.format(scenario_num, scenario_date)
        if debug_mode:
            print 'command: {}'.format(command)
        os.system(command)
    if generate_reports:
        generate_scenario_reports()
    curr.close()
    conn.close()

if __name__=='__main__':
    scenario_conf = {
        'table'       : 'production',
        'date'        : get_date(),
        'num'         : 2,
        'region count': 2,
        'filename'    : '',
        'data file'   : '',
        'change cols' : ['production', 'unit'],
        'id cols'     : ['asset_id', 'casetype', 'period', 'commodity']
    }
    scenario_conf['filename']  = '{}_scenario_{}.xlsx'.format(scenario_conf['date'], scenario_conf['num'])
    scenario_conf['data file'] = DATA_DIR + scenario_conf['filename']
    scenario_conf['data cols'] = [col_name.lower() for col_name in (scenario_conf['change cols'] + scenario_conf['id cols'])]
    scenario_conf['data']      = []
    main(scenario_conf, update_db=True, run_task=True, create_models=True, update_econ_data=True, run_breakevens=True, extract_econ_data=True, extract_export_data=True)






