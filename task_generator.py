from globaldata import *

class TaskGenerator(object):
    '''Abstract class to create task from templates'''
    def __init__(self, task_config):
        self.task_config   = task_config
        self.task_form     = self.task_config['task_form']
        self.task_type     = self.task_config['task_type']
        self.task_group    = self.task_config['task_group']
        self.task_name     = self.task_config['task_name']
        self.task_dir      = self.task_config['task_dir']
        self.num_cols      = self.task_config['num_cols']
        self.num_rows      = self.task_config['num_rows']
        self.program_drive = self.task_config['program_drive']
        self.gd_drive      = self.task_config['gd_drive']
        self.macro_dir     = self.task_config['macro_dir']
        self.macro_file    = self.task_config['macro_file']
        self.macro_name    = self.task_config['macro_name']
        self.task_comment  = self.task_config['task_comment']
        self.process_name  = self.task_config['process_name']
        self.log_comment   = self.task_config['log_comment']
        self.log_start     = self.task_config['log_start']
        self.log_end       = self.task_config['log_end']
        self.check_process = self.task_config['check_process']
        self.check_cmd     = self.task_config['check_cmd']
        self.py_version    = self.task_config['py_version']
        self.region_name   = self.task_config['region_name']
        self.subtasks      = self.task_config['subtasks']
        self.region_chains = self.task_config['region_chains']
        self.task_body     = ''

    def task_gen(self):
        '''A factory method for deciding the task generator class to return'''
        if self.task_form == 'basic':
            _task = BasicTask(task_config=self.task_config)
        elif self.task_form == 'chain':
            _task = ChainTask(task_config=self.task_config)
        elif self.task_form == 'multi':
            _task = MultiTask(task_config=self.task_config)
        return _task

    def create_task(self):
        task_filepath = self.task_dir + self.task_name + '.bat'
        self.task_body = self.gen_task_body()
        with open(task_filepath, 'w') as task:
            task.write(self.template())

    def template(self):
        task_template  = self.echo_off()
        task_template += self.mode_con(self.num_cols, self.num_rows)
        task_template += self.set_program_drive(self.program_drive)
        task_template += self.set_gd_drive(self.gd_drive)
        task_template += self.task_body
        task_template += self.exit_cmd()
        return task_template

    def gen_task_body(self):
        return self.task_body

    def echo_off(self):
        return '@ECHO OFF\n'

    def mode_con(self, num_cols, num_rows):
        return 'mode con: cols=%s lines=%s\n\n' % (num_cols, num_rows)

    def set_program_drive(self, drive_letter):
        return 'SET program_drive=%s\n' % drive_letter

    def set_gd_drive(self, drive_letter):
        return 'SET gd_drive=%s\n' % drive_letter

    def set_wait(self, wait_time):
        return 'SET wait_time=%s\n' % wait_time

    def comment(self, task_comment):
        return '\nECHO %s ...\n' % task_comment

    def run_macro(self, macro_dir, macro_file, macro_name):
        macro_cmd  = '''powershell -Command "& {$app = New-Object -comobject Excel.Application; '''
        macro_cmd += '''$wb = $app.Workbooks.Open('%%gd_drive%%:\%s%s'); $app.Run('%s'); $wb.Save(); $app.Quit();}"\n'''
        return macro_cmd % (macro_dir[3:], macro_file, macro_name)

    def py_cmd(self, py_version, cmd_name, arg_str, py_file='cmd_main.py'):
        return '%s %%program_drive%%:\python_code\%s %s %s %%*\n' % (py_version, py_file, cmd_name, arg_str)

    def start_task(self, start_task_dir, start_task_name):
        return '\nSTART %%gd_drive%%:\%s%s\n' % (start_task_dir, start_task_name)

    def time_out(self):
        return 'TIMEOUT %wait_time%\n'

    def pause_cmd(self):
        return 'PAUSE\n'

    def exit_cmd(self):
        return '\nEXIT\n'

class BasicTask(TaskGenerator):
    def gen_task_body(self):
        self.task_body = self.comment(self.task_comment)

        if self.log_start:
            cmd_name = 'log'
            arg_str = '-s %s "%s"' % (self.process_name, self.log_comment)
            self.task_body += self.py_cmd(py_version=self.py_version, cmd_name=cmd_name, arg_str=arg_str)

        if self.task_type == 'command':
            for subtask in self.subtasks:
                self.task_body += self.py_cmd(*subtask)

        elif self.task_type == 'macro':
            self.task_body += self.run_macro(self.macro_dir, self.macro_file, self.macro_name)

        if self.log_end:
            cmd_name = 'log'
            arg_str = '-e %s' % self.process_name
            self.task_body += self.py_cmd(py_version=self.py_version, cmd_name=cmd_name, arg_str=arg_str)

        if self.check_process:
            cmd_name = self.check_process
            arg_str = self.check_cmd
            self.task_body += self.py_cmd(py_version=self.py_version, cmd_name=cmd_name, arg_str=arg_str)
        return self.task_body

class ChainTask(TaskGenerator):
    def gen_task_body(self):
        self.task_body = ''
        for region in self.region_chains[self.region_name]:
            macro_file   = self.macro_file % (self.task_group, region)
            task_comment = self.task_comment % REGIONS[region]
            process_name = self.process_name % (self.task_group, region)
            log_comment  = self.log_comment % REGIONS[region]
            check_cmd    = self.check_cmd % check_cmd_args(self.task_config, region)

            self.task_body += self.comment(task_comment)

            if self.log_start:
                cmd_name = 'log'
                arg_str = '-s %s "%s"' % (process_name, log_comment)
                self.task_body += self.py_cmd(py_version=self.py_version, cmd_name=cmd_name, arg_str=arg_str)

            if self.task_type == 'command':
                self.subtasks = get_subtasks(self.task_config, region)
                for py_version, cmd_name, arg_str in self.subtasks:
                    subtask = (py_version, cmd_name, arg_str % REGIONS[region])
                    self.task_body += self.py_cmd(*subtask)
            elif self.task_type == 'macro':
                self.task_body += self.run_macro(self.macro_dir, macro_file, self.macro_name)

            if self.log_end:
                cmd_name = 'log'
                arg_str = '-e %s' % process_name
                self.task_body += self.py_cmd(py_version=self.py_version, cmd_name=cmd_name, arg_str=arg_str)

            if self.check_process:
                cmd_name = self.check_process
                arg_str = check_cmd
                self.task_body += self.py_cmd(py_version=self.py_version, cmd_name=cmd_name, arg_str=arg_str)
        return self.task_body

class MultiTask(TaskGenerator):
    pass


def main(config, regions=False, chain=False):
    if regions:
        for region in config['regions']:
            region_config = config.copy()
            region_config['task_form']    = 'basic'
            region_config['region_name']  = region
            region_config['task_name']    = region_config['task_name'] % (region_config['task_group'], region)
            region_config['macro_file']   = region_config['macro_file'] % (region_config['task_group'], region)
            region_config['task_comment'] = region_config['task_comment'] % REGIONS[region]
            region_config['process_name'] = region_config['process_name'] % (region_config['task_group'], region)
            region_config['log_comment']  = region_config['log_comment'] % REGIONS[region]
            region_config['check_cmd']    = get_check_cmd(region_config, region)
            region_config['subtasks']     = get_subtasks(region_config, region)
            region_task = TaskGenerator(task_config=region_config).task_gen()
            region_task.create_task()
    if chain:
        for region_chain in config['region_chains'].keys():
            chain_config = config.copy()
            chain_config['task_form']   = 'chain'
            chain_config['task_name']   = chain_config['task_name'] % (chain_config['task_group'], region_chain)
            chain_config['log_start']   = True
            chain_config['region_name'] = region_chain
            chain_task = TaskGenerator(task_config=chain_config).task_gen()
            chain_task.create_task()
    else:
        basic_config = config.copy()
        basic_config['task_form'] = 'basic'
        basic_task = TaskGenerator(task_config=basic_config).task_gen()
        basic_task.create_task()


if __name__=='__main__':
    task_config = MACRO_CONFIGS['Breakeven']
    main(config=task_config, regions=True, chain=True)
