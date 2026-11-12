from .constants import *

def get_check_cmd(task_config, region=''):
    cmd_args = ()
    check_process = task_config['check_process']

    if check_process == 'check_breakeven': cmd_args = (REGIONS[region], region)
    elif check_process == 'check_disc_fields': cmd_args = (REGIONS[region])
    elif check_process == 'temp_log': cmd_args = (region,)

    if cmd_args: check_cmd = task_config['check_cmd'] % cmd_args
    else: check_cmd = task_config['check_cmd']

    return check_cmd


def get_subtasks(task_config, region=''):
    subtasks = []
    py_version = 'python2'
    for cmd_name in task_config['cmd_names']:
        if cmd_name == 'create_model':
            arg_str = '-stat-nlrb -regn-%s'
            if region == 'Rest_of_World_1':
                subtasks.append((py_version, cmd_name, arg_str % 'north_america_1'))
                subtasks.append((py_version, cmd_name, (arg_str % 'middle_east') + ' -delt-e'))
            elif region == 'Rest_of_World_2':
                region_str = ','.join([region_name.lower() for region_name in task_config['region_chains'][region]])
                subtasks.append((py_version, cmd_name, (arg_str % region_str) + ' -delt-e'))
            elif region in ['North_America_1', 'North_America_2']:
                subtasks.append((py_version, cmd_name, arg_str % region.lower()))
            else:
                subtasks.append((py_version, cmd_name, (arg_str % region.lower()) + ' -delt-e'))
        elif cmd_name == 'data_extract':
            arg_str = 'regn-%s e'
            if region == 'Rest_of_World_1':
                for region_code in REGION_CODES[region]:
                    subtasks.append((py_version, cmd_name, arg_str % region_code))
            elif region == 'Rest_of_World_2':
                region_str = ','.join([region_code for region_code in REGION_CODES[region]])
                subtasks.append((py_version, cmd_name, arg_str % region_str))
            else:
                subtasks.append((py_version, cmd_name, arg_str % REGION_CODES[region]))
    return subtasks


DISK_FIELD_CONFIGS = {
    'DiscFieldMacro': {
             'task_form': '',
             'task_type': 'command',
            'task_group': 'DiscField',
             'task_name': '%s%s_%s',                                        # % (task_group, subtask_name, region_name)
              'task_dir': DF_MACROS_DIR + '%s%s\\',                         # % (task_group, subtask_name)
              'num_cols': 60,
              'num_rows': 20,
         'program_drive': '%engine_drive%',
              'gd_drive': '%engine_drive%',
             'macro_dir': DISC_FIELD_DIR,
            'macro_name': ['MinimumEconReserve',
                           'MaximumDevCost',
                           'ProcessFolderBreakevens'],
            'macro_file': '%s_%s.xlsm',                                     # % (task_group, region_name)
          'task_comment': ['Calculating Minimum Economic Reserves %s',      # % region_name
                           'Running MaximumDevCost Macro %s',               # % region_name
                           'Running Breakeven Macro %s'],                   # % region_name
          'process_name': '%s%s_%s',                                        # % (task_group, subtask_name, region_name)
           'log_comment': ['MinimumEconReserve Macro %s',                   # % region_name
                           'MaximumDevCost Macro %s',                       # % region_name
                           'Breakeven Macro %s'],                           # % region_name
             'log_start': False,
               'log_end': False,
         'check_process': 'check_disc_fields',
             'check_cmd': '-%s -%s',                                        # % (subtask_name, "REGIONS[region_name]")
            'py_version': '%py2%',
           'region_name': '%s',
               'regions': DISC_REGIONS,
              'subtasks': [[('%py2%', 'calc_min_econ',   '"%s"')],        # % REGIONS[region_name]
                           [('%py2%', 'calc_max_dev',    '"%s"')],        # % REGIONS[region_name]
                           [('%py2%', 'calc_breakevens', '"%s"')]],       # % REGIONS[region_name]
         'subtask_names': ['Macro1', 'Macro2', 'Macro3'],
         'region_chains': {'RegionA': ['Asia'],
                           'RegionB': ['Former_Soviet_Union'],
                           'RegionC': ['Oceania'],
                           'RegionD': ['Europe',
                                       'Middle_East'],
                           'RegionE': ['Caribbean',
                                       'Central_America',
                                       'North_America'],
                           'RegionF': ['Africa', 'South_America']}
    }
}

COMMAND_CONFIGS = {
    'CreateModel': {
            'task_form': '',
            'task_type': 'command',
           'task_group': 'CreateModel',
            'task_name': '%s_%s',
             'task_dir': MODEL_TASK_DIR,
             'num_cols': 60,
             'num_rows': 20,
        'program_drive': '%engine_drive%',
             'gd_drive': '%engine_drive%',
            'macro_dir': '',
           'macro_name': '',
           'macro_file': '%s_%s.xlsm',
         'task_comment': 'Create Models %s',
         'process_name': '%s_%s',
          'log_comment': 'Create Model %s',
            'log_start': True,
              'log_end': True,
        'check_process': 'temp_log',
            'check_cmd': 'create_model %s',
           'py_version': '%py2%',
          'region_name': '%s',
              'regions': REGIONS.keys(),
            'cmd_names': ['create_model'],
             'subtasks': [],
        'subtask_names': [],
        'region_chains': {     'Unconventional': ['Unconventional'],
                          'Former_Soviet_Union': ['Former_Soviet_Union'],
                              'North_America_2': ['North_America_2'],
                                       'Europe': ['Europe'],
                              'Rest_of_World_1': ['North_America_1', 'Middle_East'],
                              'Rest_of_World_2': ['Africa', 'Asia', 'Caribbean', 'Central_America', 'Oceania'],
                                'South_America': ['South_America']}
    },
    'DataExtract': {
            'task_form': '',
            'task_type': 'command',
           'task_group': 'DataExtract',
            'task_name': '%s_%s',
             'task_dir': TASK_DIR + 'ExtractTasks\\',
             'num_cols': 60,
             'num_rows': 20,
        'program_drive': '%engine_drive%',
             'gd_drive': '%engine_drive%',
            'macro_dir': '',
           'macro_name': '',
           'macro_file': '%s_%s.xlsm',
         'task_comment': 'Extracting Data %s',
         'process_name': '%s_%s',
          'log_comment': 'Engine Data Extract %s',
            'log_start': True,
              'log_end': True,
        'check_process': 'check_extract',
            'check_cmd': '',
           'py_version': '%py2%',
          'region_name': '%s',
              'regions': REGIONS.keys(),
            'cmd_names': ['data_extract'],
             'subtasks': [],
        'subtask_names': [],
        'region_chains': {}
    }
}

MACRO_CONFIGS = {
    'Breakeven': {
             'task_form': '',
             'task_type': 'macro',
            'task_group': 'Breakeven',
             'task_name': '%s_%s',
              'task_dir': BE_TASK_DIR,
              'num_cols': 50,
              'num_rows': 10,
         'program_drive': '%engine_drive%',
              'gd_drive': '%engine_drive%',
             'macro_dir': BREAKEVEN_DIR,
            'macro_name': 'ProcessFolderBreakevens',
            'macro_file': '%s_%s.xlsm',
          'task_comment': 'Running Breakeven %s',
          'process_name': '%s_%s',
           'log_comment': 'Breakeven %s',
             'log_start': False,
               'log_end': False,
         'check_process': 'check_breakeven',
             'check_cmd': '"%s" %s',
            'py_version': '%py2%',
           'region_name': '%s',
               'regions': CHECK_REGION_SET,
             'cmd_names': [],
              'subtasks': [],
         'subtask_names': [],
         'region_chains': {'RegionA': ['Africa',
                                       'Asia',
                                       'Caribbean',
                                       'Central_America',
                                       'Oceania'],
                           'RegionB': ['Former_Soviet_Union',
                                       'Unconventional'],
                           'RegionC': ['South_America'],
                           'RegionD': ['North_America_2'],
                           'RegionE': ['Europe' ],
                           'RegionF': ['North_America_1',
                                       'Middle_East']}
    }
}

