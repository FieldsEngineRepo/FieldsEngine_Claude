from globaldata import *

TITAN_TASK_DIR = 'Y:\\GlobalData\\Tasks\\CreateModelTasks\\'

for task_file in [task for task in os.listdir(TITAN_TASK_DIR) if task[-3:] in ['bat', 'cmd']]:
    task_text = ''
    with open(TITAN_TASK_DIR + task_file, 'r') as task:
        for task_command in task.readlines():
            cmd_parts = task_command.split()
            if len(cmd_parts) > 4 and cmd_parts[2] == 'engine' and cmd_parts[3] == 'create_model':
                task_text += (' '.join([cmd_parts[0],cmd_parts[1],cmd_parts[3],cmd_parts[2],' '.join(cmd_parts[4:])]))
            else:
                task_text += task_command
    with open(TITAN_TASK_DIR + task_file, 'w') as task:
        print task_text
        task.write(task_text)
