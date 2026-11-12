import itertools as it
import json
import os
from Tkinter import *
from datetime import datetime
from tkFileDialog import *

import cmd_main as cmd

# Set directory to store batch files -----------------------------------------------------------------------------------

PROGRAM_DRIVE = cmd.PROGRAM_DRIVE
TASK_DIR = cmd.TASK_DIR
PROGRAM_DIR = cmd.PROGRAM_DIR
DATA_DIR = cmd.DATA_DIR

tasklist = []
task_names = []

chainlist = []
chain_names = []


# Store list of all task and task-chain configurations in json format --------------------------------------------------

if os.path.exists(DATA_DIR + 'conf\\'):
    if os.path.isfile(DATA_DIR + 'conf\\tasks.json'):
        with open(DATA_DIR + 'conf\\tasks.json') as f:
            tasklist = json.load(f)
else:
    os.mkdir(DATA_DIR + 'conf\\')
    with open(DATA_DIR + 'conf\\tasks.json', 'w') as f:
        json.dump(tasklist, f)

if os.path.exists(DATA_DIR + 'conf\\'):
    if os.path.isfile('conf\\chains.json'):
        with open(DATA_DIR + 'conf\\chains.json') as f:
            chainlist = json.load(f)
else:
    os.mkdir(DATA_DIR + 'conf\\')
    with open(DATA_DIR + 'conf\\chains.json', 'w') as f:
        json.dump(chainlist, f)


CURRENT_YEAR = datetime.now().year
MAIN_WINDOW_SIZE = '675x300'

# Generate list of times at 30 minute intervals ------------------------------------------------------------------------

TIMES = [h + r for (h, r) in list(it.product([str(hour) for hour in range(1, 13)], [':00', ':30']))]

master = Tk()
master.geometry(MAIN_WINDOW_SIZE)
master.title('Task Scheduler')
window_height = '100'

# Initialize variables -------------------------------------------------------------------------------------------------

task_name = StringVar()
taskname = StringVar()
view_taskname = StringVar()
schedule = IntVar()
action = StringVar()
lead_task = StringVar()
follow_task = StringVar()
chain_name = StringVar()
run_task = StringVar()
delete_task = StringVar()

month = StringVar()
day = IntVar()
time = StringVar()
am_pm = IntVar()
recurring = StringVar()
task_event = StringVar()

chk_sun = IntVar()
chk_mon = IntVar()
chk_tue = IntVar()
chk_wed = IntVar()
chk_thu = IntVar()
chk_fri = IntVar()
chk_sat = IntVar()

roundTo = IntVar()
roundTo.set(4)

generalMsg = StringVar()
generalMsg.set("")

assetId = StringVar()
assetId.set("")

countryName = StringVar()
countryName.set("")

assetCountryName = StringVar()
assetCountryName.set("")

constituentName = StringVar()
constituentName.set("")

regionName = StringVar()
regionName.set("")

statusName = StringVar()
statusName.set("")

terrainName = StringVar()
terrainName.set("")

resourceName = StringVar()
resourceName.set("")

facilityTypeName = StringVar()
facilityTypeName.set("")

basinName = StringVar()
basinName.set("")

operatorName = StringVar()
operatorName.set("")

chkAll = IntVar()
chkAll.set(1)

chkDebugMode = IntVar()
chkDebugMode.set(0)

chkDeleteExistingFiles = IntVar()
chkDeleteExistingFiles.set(0)

chkDeleteForecastData = IntVar()
chkDeleteForecastData.set(0)

chkTestNewModule = IntVar()
chkTestNewModule.set(0)

chkBEModule = IntVar()
chkBEModule.set(0)

chkFEATModule = IntVar()
chkFEATModule.set(0)

chkExternalAssetFile = IntVar()
chkExternalAssetFile.set(0)

chkAfrica = IntVar()
chkAsia = IntVar()
chkCaribbean = IntVar()
chkCentralAmerica = IntVar()
chkEurope = IntVar()
chkMiddleEast = IntVar()
chkNorthAmerica = IntVar()
chkOceania = IntVar()
chkSouthAmerica = IntVar()
chkFormerSovietUnion = IntVar()

chkAfrica.set(0)
chkAsia.set(0)
chkCaribbean.set(0)
chkCentralAmerica.set(0)
chkEurope.set(0)
chkMiddleEast.set(0)
chkNorthAmerica.set(0)
chkOceania.set(0)
chkSouthAmerica.set(0)
chkFormerSovietUnion.set(0)

msgAll = StringVar()
msgAfrica = StringVar()
msgAsia = StringVar()
msgCaribbean = StringVar()
msgCentralAmerica = StringVar()
msgEurope = StringVar()
msgMiddleEast = StringVar()
msgNorthAmerica = StringVar()
msgOceania = StringVar()
msgSouthAmerica = StringVar()
msgFormerSovietUnion = StringVar()

msgAll.set('')
msgAfrica.set('')
msgAsia.set('')
msgCaribbean.set('')
msgCentralAmerica.set('')
msgEurope.set('')
msgMiddleEast.set('')
msgNorthAmerica.set('')
msgOceania.set('')
msgSouthAmerica.set('')
msgFormerSovietUnion.set('')

chkStatusAbandoned = IntVar()
chkStatusAbandoned.set(0)

chkStatusAnnounced = IntVar()
chkStatusAnnounced.set(1)

chkStatusPlanned = IntVar()
chkStatusPlanned.set(1)

chkStatusProducing = IntVar()
chkStatusProducing.set(1)

new_task = True
config_complete = False
task_row = 0

asset_param_dict = {'terrain': ['Shallow Water','Onshore','Deepwater','Ultra-Deepwater'],
                    'resource_type': ['Heavy Oil','Conventional Oil','Conventional Gas','CBM','Unconventional Gas',
                                      'Unconventional Oil','Oil Shale','Oil Sands'],
                    'facility_type': ['Fixed Platform','Wellhead Platform','FPSO','FSO','Mobile Offshore Production Unit (MOPU)',
                                      'Compliant Tower','Gravity Based Platform','Subsea System','Semi-submersible',
                                      'Satellite Platform','Tension Leg Platform','FLNG','FPU','Spar','Mini Tension Leg Platform']}


# Store individual task and task-chain configurations-------------------------------------------------------------------

task_config = {'task name': '', 'schedule type': '', 'action': '', 'event': '', 'month': '', 'day': '', 'time': '',
               'am pm': '', 'recurring': '1', 'days of week': (0, 0, 0, 0, 0, 0, 0)}
chain_config = {'lead task': '', 'follow tasks': []}


# Update configuration lists -------------------------------------------------------------------------------------------


def update_tasklist():
    global tasklist
    global task_names
    with open(DATA_DIR + 'conf\\tasks.json', 'w') as tasks:
        json.dump(tasklist, tasks)
    with open(DATA_DIR + 'conf\\tasks.json') as tasks:
        tasklist = json.load(tasks)
    if not tasklist:
        task_names = ['No Tasks Created']
    else:
        taskname.set('                           ')
        task_names = [task['task name'] for task in tasklist]
    #print task_names


def update_chainlist():
    global chainlist
    global chain_names
    with open(DATA_DIR + 'conf\\chains.json', 'w') as chains:
        json.dump(chainlist, chains)
    with open(DATA_DIR + 'conf\\chains.json') as chains:
        chainlist = json.load(chains)
    if not chainlist:
        chain_names = ['No Chains Created']
    else:
        chain_names = [chain['chain name'] for chain in chainlist]


# Reset configurations and display -------------------------------------------------------------------------------------

def reset_config_display():
    global task_config
    task_config = {'task name': '                                                          ',
                   'schedule type': '                                   ',
                   'action': '                                                              ',
                   'event': '                                                    ',
                   'month': '                                   ',
                   'day': '           ',
                   'time': '           ',
                   'am pm': '    ',
                   'recurring': '1',
                   'days of week': (0, 0, 0, 0, 0, 0, 0)}
    display_config()


def reset_task_config():
    global task_config
    global new_task
    global config_complete
    reset_config_display()
    display_config()
    task_config = {'task name': '', 'schedule type': '', 'action': '', 'event': '', 'month': '', 'day': '',
                   'time': '', 'am pm': '', 'recurring': '1', 'days of week': (0, 0, 0, 0, 0, 0, 0)}
    task_name.set('')
    taskname.set('                                                          ')
    view_taskname.set('                                                          ')
    schedule.set(0)
    month.set('')
    day.set(0)
    time.set('')
    am_pm.set(0)
    recurring.set('')
    task_event.set('Choose Event')
    chk_sun.set(0)
    chk_mon.set(0)
    chk_tue.set(0)
    chk_wed.set(0)
    chk_thu.set(0)
    chk_fri.set(0)
    chk_sat.set(0)
    new_task = True
    config_complete = False
    display_config()


def reset_chain_config():
    global chain_config
    global config_complete
    chain_config = {'chain name': '', 'lead task': '', 'follow tasks': []}
    lead_task.set('')
    follow_task.set('')
    chain_name.set('')
    config_complete = False
    display_config()


def delete_task_now():
    global delete_task
    cmd.delete_task(delete_task.get())
    remove_task(delete_task.get())


def clear_tasks():
    global tasklist
    global task_names
    cmd.delete_all_tasks(task_names)
    with open(DATA_DIR + 'conf\\tasks.json', 'w') as tasks:
        json.dump([], tasks)
    with open(DATA_DIR + 'conf\\tasks.json') as tasks:
        tasklist = json.load(tasks)
    new_task_main()


def clear_chains():
    global chainlist
    with open(DATA_DIR + 'conf\\chains.json', 'w') as chains:
        json.dump([], chains)
    with open(DATA_DIR + 'conf\\chains.json') as chains:
        chainlist = json.load(chains)


def remove_task(taskname):
    tasklist.remove([task for task in tasklist if task['task name'] == taskname][0])
    update_tasklist()


def cancel_config(window, config_type='task'):
    global chain_config
    if config_type == 'task':
        task_config['schedule type'] = ''
    else:
        chain_config = {'chain name': '', 'lead task': '', 'follow tasks': []}
    window.destroy()


# ----------------------------------------------------------------------------------------------------------------------


def is_leap_year():
    leap_year = False
    if (CURRENT_YEAR - 2000) % 4 == 0:
        leap_year = True
    return leap_year


def convert_time(in_time, in_am_pm):
    hours = in_time.split(':')[0]
    minutes = in_time.split(':')[1]
    if in_am_pm == 'pm':
        hours = str(int(hours) + 12)
    return hours + ':' + minutes


# Get values of chosen variables ---------------------------------------------------------------------------------------

def get_task_name(event=None):
    global task_name
    task_config['task name'] = task_name.get()
    display_config()
    return task_name.get()


def get_action():
    global action
    action = askopenfilename(initialdir=TASK_DIR)
    task_config['action'] = action
    display_config()
    return action


def get_month():
    global month
    task_config['month'] = month.get()
    return month.get()


def get_day(*args):
    global day
    task_config['day'] = str(day.get())
    return str(day.get())


def get_time():
    global time
    task_config['time'] = time.get()
    return time.get()


def get_am_pm():
    global am_pm
    if am_pm.get() == 1:
        task_config['am pm'] = 'am'
    if am_pm.get() == 2:
        task_config['am pm'] = 'pm'
    return am_pm.get()


def get_recurring(event=None):
    global recurring
    task_config['recurring'] = recurring.get()
    return recurring.get()


def get_event(event=None):
    global task_event
    global task_names
    global task_config
    update_tasklist()
    update_task_options(7,1)
    if task_event.get() in task_names:
        task_config['event'] = task_event.get()
    if task_config['schedule type'] != 'Event':
        task_config['event'] = ''
    display_config()
    #print task_config
    return task_event.get()


def get_days_of_week():
    global chk_sun
    global chk_mon
    global chk_tue
    global chk_wed
    global chk_thu
    global chk_fri
    global chk_sat

    sun = chk_sun.get()
    mon = chk_mon.get()
    tue = chk_tue.get()
    wed = chk_wed.get()
    thu = chk_thu.get()
    fri = chk_fri.get()
    sat = chk_sat.get()

    task_config['days of week'] = sun, mon, tue, wed, thu, fri, sat
    return sun, mon, tue, wed, thu, fri, sat


def get_run_task(event=None):
    global run_task
    return run_task.get()


def get_delete_task(event=None):
    global delete_task
    return delete_task.get()


def get_schedule(schedule_type):
    global task_event
    if schedule_type == 'Event':
        update_tasklist()
        task_config['schedule type'] = 'Event'
        task_event.set('Choose Event')
        get_event()
        display_config()
        #task_options.grid_forget()
    else:
        top = Toplevel()
        top.title('Choose Task Schedule')
        if schedule_type == 'Daily':
            task_config['schedule type'] = 'Daily'
            top.geometry('350x150')
            choose_date(top)
            choose_recurring(top)
            Label(top, text='days', padx=10, pady=5).grid(row=3, column=2, sticky=W)
            Label(top, text="").grid(row=4)
        elif schedule_type == 'Weekly':
            task_config['schedule type'] = 'Weekly'
            top.geometry('450x200')
            choose_date(top)
            choose_recurring(top)
            Label(top, text='weeks', padx=10, pady=5).grid(row=3, column=2, sticky=W)
            choose_day(top)
            Label(top, text="").grid(row=7)
        elif schedule_type == 'Once':
            task_config['schedule type'] = 'Once'
            top.geometry('300x120')
            choose_date(top)
        Button(top, text='Select', command=(lambda: set_config(top))).grid(row=8, column=2, sticky=E)
        Button(top, text='Cancel', command=(lambda: cancel_config(top))).grid(row=8, column=3, sticky=W)
        top.mainloop()

def view_all_tasks():
    global tasklist
    top = Toplevel()
    hgt = 300
    task_info = ""
    param_list = ['task name', 'event']

    task_info += param_list[0].upper() + (24 - len(param_list[0])) * " " + " \t\t| "
    task_info += param_list[1].upper()
    task_info += '\n'
    task_info += '-'*60 + '\n'
    for task in tasklist:
        hgt += 4
        for i in range(len(param_list)):
            if i == 0:
                if len(str(task[param_list[i]])) == 0:
                    task_info += str(task[param_list[i]]) + (24 - len(str(task[param_list[i]]))) * " " + " \t\t\t| "
                elif len(str(task[param_list[i]])) > 22:
                    task_info += str(task[param_list[i]]) + (24 - len(str(task[param_list[i]]))) * " " + " \t| "
                else:
                    task_info += str(task[param_list[i]]) + (24 - len(str(task[param_list[i]]))) * " " + " \t\t| "
            else:
                task_info += str(task[param_list[i]])
        task_info += '\n'
    Message(top, text=task_info, width=500).pack(fill=BOTH, expand=1)
    top.geometry('400x' + str(hgt))
    top.mainloop()

# ----------------------------------------------------------------------------------------------------------------------


def print_days():
    days_of_week = ["Sundays", "Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays", "Sundays"]
    week_string = ""
    for i in range(len(get_days_of_week())):
        if get_days_of_week()[i] > 0:
            week_string += days_of_week[i] + ','
    if week_string:
        days = week_string.split(',')
        days.remove('')
        if len(days) > 2:
            last = days[-1]
            last = 'and ' + last
            days.remove(days[-1])
            days.append(last)
            week_string = ', '.join(days)
        elif len(days) > 1:
            week_string = ' and '.join(days)
        else:
            week_string = days[0]
    return week_string


# Generate windows and create widgets to choose task parameters --------------------------------------------------------

def choose_date(window):
    global time
    day.set(1)
    month_list = ["January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December"]

    month.set('            ')
    Label(window, text='Start Date: ', padx=10, pady=5).grid(row=0, column=0, sticky=W)

    def update_month(*args):
        range(1, 31)
        new_month = month.get()
        if new_month == "February":
            if is_leap_year():
                num_days = range(1, 30)
            else:
                num_days = range(1, 29)
        elif new_month in ["January", "March", "May", "July", "August", "October", "December"]:
            num_days = range(1, 32)
        else:
            num_days = range(1, 31)
        day.set('   ')
        OptionMenu(window, day, *num_days).grid(row=0, column=2, sticky=W)

    OptionMenu(window, month, *month_list, command=update_month).grid(row=0, column=1, sticky=W)
    Label(window, text='Start Time: ', padx=10, pady=5).grid(row=1, column=0, sticky=W)
    time.set('      ')
    OptionMenu(window, time, *TIMES).grid(row=1, column=1, sticky=W)
    Radiobutton(window, text="AM", variable=am_pm, value=1, pady=5).grid(row=1, column=2, sticky=W)
    Radiobutton(window, text='PM', variable=am_pm, value=2, pady=5).grid(row=1, column=3, sticky=W)


def choose_recurring(window):
    Label(window, text='Recurring every ', padx=10, pady=5).grid(row=3, column=0, sticky=W)
    recurring_entry = Entry(window, textvariable=recurring)
    recurring_entry.grid(row=3, column=1, pady=5, sticky=W)
    recurring_entry.bind('<Return>', get_recurring)


def choose_day(window):
    Checkbutton(window, text="Sunday", variable=chk_sun, padx=10).grid(row=5, column=0, sticky=W)
    Checkbutton(window, text="Monday", variable=chk_mon, padx=10).grid(row=5, column=1, sticky=W)
    Checkbutton(window, text="Tuesday", variable=chk_tue, padx=10).grid(row=5, column=2, sticky=W)
    Checkbutton(window, text="Wednesday", variable=chk_wed, padx=10).grid(row=5, column=3, sticky=W)
    Checkbutton(window, text="Thursday", variable=chk_thu, padx=10).grid(row=6, column=0, sticky=W)
    Checkbutton(window, text="Friday", variable=chk_fri, padx=10).grid(row=6, column=1, sticky=W)
    Checkbutton(window, text="Saturday", variable=chk_sat, padx=10).grid(row=6, column=2, sticky=W)


# ----------------------------------------------------------------------------------------------------------------------


def run_task_now():
    global run_task
    task_action = [config['action'] for config in tasklist if config['task name'] == run_task.get()][0]
    #print task_action
    cmd.run_task(run_task.get(), task_action)


def config_change(event=None):
    global new_task
    global taskname
    reset_config_display()
    new_task = False
    display_config()
    taskname.set('                                                          ')


def set_config(window=None, config_type='task'):
    if config_type == 'task':
        get_month()
        get_day()
        get_time()
        get_am_pm()
        get_days_of_week()
        get_recurring()
        get_event()
        display_config()
        if not window:
            if task_config['task name'] in task_names:
                remove_task(task_config['task name'])
            tasklist.append(task_config)
            update_tasklist()
            for k,v in task_config.items():
                print k, ':', v
            reset_config_display()
            new_task_main()
    else:
        chain_config['chain name'] = chain_name.get()
        create_task_chain()
    if window:
        window.destroy()


# Show task parameters chosen and check if configuration is ready to finalize into a scheduled task

def display_config(event=None):
    global new_task
    global task_config
    global view_taskname
    global tasklist
    update_tasklist()
    update_chainlist()

    if not new_task:
        config_name = view_taskname.get()
        config = [task for task in tasklist if task['task name'] == config_name][0]
        task_config = config

    Label(master, text='Task Name:   ', padx=10).grid(row=1, column=4, sticky=E)
    Label(master, text=task_config['task name'], padx=10).grid(row=1, column=5, sticky=W)

    Label(master, text='Schedule:   ', padx=10).grid(row=3, column=4, sticky=E)
    Label(master, text=task_config['schedule type'], padx=10).grid(row=3, column=5, sticky=W)

    Label(master, text='Start Date:   ', padx=10).grid(row=4, column=4, sticky=E)

    if task_config['day'] != '0':
        date = task_config['month'] + ' ' + task_config['day']
    else:
        date = task_config['month']
    Label(master, text=date, padx=10).grid(row=4, column=5, sticky=W)

    Label(master, text='Start Time:   ', padx=10).grid(row=5, column=4, sticky=E)
    Label(master, text=task_config['time'] + ' ' + task_config['am pm'], padx=10).grid(row=5, column=5, sticky=W)

    if get_recurring():
        if task_config['recurring'] == '1':
            if task_config['schedule type'] == 'Weekly':
                Label(master, text='Recurs every:   ', padx=10).grid(row=6, column=4, sticky=E)
                Label(master, text='week on ' + print_days(), padx=10).grid(row=6, column=5, sticky=W)
            else:
                Label(master, text='Recurs every day', padx=10).grid(row=6, column=4, sticky=E)
        else:
            if task_config['schedule type'] == 'Weekly':
                Label(master, text='Recurs every:   ', padx=10).grid(row=6, column=4, sticky=E)
                Label(master, text=task_config['recurring']+' weeks on '+print_days(), padx=10).grid(row=6,
                                                                                                     column=5, sticky=E)
            else:
                Label(master, text='Recurs every:   ', padx=10).grid(row=6, column=4, sticky=E)
                Label(master, text=task_config['recurring'] + ' days', padx=10).grid(row=6, column=5, sticky=E)
    Label(master, text='Event:   ', padx=10).grid(row=7, column=4, sticky=E)
    Label(master, text=task_config['event'], padx=10).grid(row=7, column=5, sticky=W)
    action_filename = task_config['action'].split('/')[-1]
    Label(master, text='Action:   ', padx=10).grid(row=8, column=4, sticky=E)
    Label(master, text=action_filename, padx=10).grid(row=8, column=5, sticky=W)
    if new_task:
        config_check()
    new_task = True


# View or edit created task configurations -----------------------------------------------------------------------------

def get_config(option, event=None):
    global task_names
    global taskname
    global view_taskname
    global choose_task_option
    global task_options
    update_tasklist()
    update_chainlist()
    if option == 'edit':
        new_task_main()
    reset_config_display()
    task_name_label.grid_forget()
    task_name_entry.grid_forget()
    choose_task_label.grid_forget()
    choose_task_option.grid_forget()
    view_taskname.set('                                                          ')
    choose_task_option = OptionMenu(master, view_taskname, *task_names, command=config_change)
    task_options.grid_forget()
    if option == 'view':
        master.geometry('350x235')
        master.title('View Task')
        choose_task_option.grid_forget()
        choose_task_label.grid(row=0, column=4, sticky=E)
        choose_task_option.grid(row=0, column=5, sticky=W)
        schedule_label.grid_forget()
        daily_radio.grid_forget()
        weekly_radio.grid_forget()
        once_radio.grid_forget()
        event_radio.grid_forget()
        task_options.grid_forget()
        action_label.grid_forget()
        action_button.grid_forget()
        finish_button.grid_forget()
        create_batch_button.grid_forget()
        task_options.grid_forget()
        space.grid(row=11, column=4)
        exit_button.grid(row=12, column=5, sticky=W)
        save_button.grid_forget()
        back_button.grid(row=12, column=4, sticky=E)
    else:
        master.title('Edit Task')
        choose_task_label.grid(row=1, column=0, sticky=E)
        choose_task_option.grid(row=1, column=1, sticky=W)
        update_task_options(7,1)


# Create a task-chain from existing tasks-------------------------------------------------------------------------------

def choose_chain():
    global task_row
    global task_names
    global window_height
    window_height = '100'
    update_chainlist()
    update_tasklist()
    follow_options = []
    task_row = 1
    top = Toplevel()
    top.geometry('300x' + window_height)
    top.title('Create Task Chain')

    # Choose tasks to follow lead task ---------------------------------------------------------------------------------

    def choose_follow_task(event=None):
        global task_row
        global lead_task
        global window_height
        global task_names
        window_height = str(31 + int(window_height))
        top.geometry('300x' + window_height)
        chain_config['lead task'] = lead_task.get()
        lead_option.grid_forget()
        Label(top, text=chain_config['lead task'] + '        ', padx=10, pady=3).grid(row=1, column=1, sticky=W)
        task_row += 1
        Label(top, text="Follow Task " + str(task_row - 1) + ": ", padx=10, pady=3).grid(row=task_row, column=0, sticky=E)
        follow_task.set("")
        update_tasklist()
        follow_task.set('Choose Task')
        follow_option = OptionMenu(top, follow_task, *task_names, command=get_follow_task)
        follow_option.grid(row=task_row, column=1, sticky=W)
        follow_options.append(follow_option)

    # Replace follow task OptionMenu with name of chosen task ----------------------------------------------------------

    def get_follow_task(event=None):
        global follow_task
        chain_config['follow tasks'].append(follow_task.get())
        follow_options[task_row - 2].grid_forget()
        Label(top, text=chain_config['follow tasks'][task_row - 2]+'        ', padx=10, pady=3).grid(row=task_row,
                                                                                                     column=1, sticky=W)
        choose_follow_task()

    Label(top, text="Choose Lead Task: ", padx=10, pady=3).grid(row=1, column=0, sticky=E)
    lead_task.set('Choose Task')
    lead_task.set('                                   ')
    lead_option = OptionMenu(top, lead_task, *task_names, command=choose_follow_task)
    lead_option.grid(row=1, column=1, sticky=W)
    Label(top, text="").grid(row=49, column=0)
    Button(top, text='Finish', command=(lambda: set_config(top, config_type='chain')), padx=10).grid(row=50, column=0, sticky=E)
    Button(top, text='Cancel', command=(lambda: cancel_config(top, 'chain')), padx=10).grid(row=50, column=1, sticky=W)
    top.mainloop()


# Check if time or event based configuration is complete ---------------------------------------------------------------

def config_check():
    global config_complete
    if chain_config['lead task'] and chain_config['follow tasks']:
        config_complete = True
    if task_config['task name'] and task_config['action']:
        if task_config['schedule type'] == 'Event':
            config_complete = True
        if task_config['month'] and task_config['day'] and task_config['time'] and task_config['am pm']:
            if task_config['schedule type'] in ['Once', 'Daily']:
                config_complete = True
            elif task_config['schedule type'] == 'Weekly' and 1 in task_config['days of week']:
                config_complete = True
    if config_complete:
        space.grid(row=11, column=4)
        save_button.grid_forget()
        finish_button.grid(row=12, column=4, sticky=E)
    return config_complete


# Finalize task schedule process and store configuration ---------------------------------------------------------------

def create_task():
    global config_complete
    global tasklist
    global task_config
    if config_check():
        if task_config['task name'] in [task['task name'] for task in tasklist]:
            remove_task(task_config['task name'])
            update_tasklist()
        if task_config['schedule type'] == 'Event':
            task_config['month'] = ''
            task_config['day'] = ''
            task_config['time'] = ''
            task_config['am pm'] = ''
            task_config['recurring'] = ''
            task_config['days of week'] = (0, 0, 0, 0, 0, 0, 0)
            cmd.create_triggered_task(task_config['task name'], task_config['event'], task_config['action'])
        else:
            for k,v in task_config.items():
                print k,":",v
            task_config['event'] = ''
            start_time = convert_time(task_config['time'], task_config['am pm'])
            cmd.create_scheduled_task(task_config['task name'], task_config['schedule type'].upper(), start_time, task_config['action'], days_of_week=task_config['days of week'])
        tasklist.append(task_config)
        reset_task_config()
        new_task_main()


def create_task_chain():
    global config_complete
    global chainlist
    global task_config
    if config_check():
        previous_task = ''
        chainlist.append(chain_config)
        update_chainlist()
        for i in range(len(chain_config['follow tasks'])):
            reset_task_config()
            follow_task_name = chain_config['follow tasks'][i]
            follow_action = [_task['action'] for _task in tasklist if _task['task name'] == follow_task_name][0]
            task_config['task name'] = follow_task_name
            task_config['schedule type'] = 'Event'
            task_config['action'] = follow_action
            if i == 0:
                task_config['event'] = chain_config['lead task']
            else:
                task_config['event'] = previous_task
            previous_task = follow_task_name
            create_task()
        reset_chain_config()


def choose_run_task():
    top = Toplevel()
    top.geometry('350x90')
    top.title('Run Task')
    run_task.set('                      ')
    Label(top, text='Choose Task', padx=10).grid(row=0, column=0, sticky=E)
    OptionMenu(top, run_task, *task_names, command=get_run_task).grid(row=0, column=1, sticky=W)
    Label(top, text="          ").grid(row=1, column=1)
    Button(top, text='Run', command=run_task_now).grid(row=2, column=0, sticky=E)
    Button(top, text='Cancel', command=top.destroy).grid(row=2, column=1, sticky=W)
    top.mainloop()


def choose_delete_task():
    top = Toplevel()
    top.geometry('240x85')
    top.title('Delete Task')
    delete_task.set('                      ')
    Label(top, text='Choose Task', padx=10).grid(row=0, column=0, sticky=E)
    OptionMenu(top, delete_task, *task_names, command=get_delete_task).grid(row=0, column=1, sticky=W)
    Label(top, text="          ").grid(row=1, column=1)
    Button(top, text='Delete', command=delete_task_now).grid(row=2, column=0, sticky=E)
    Button(top, text='Cancel', command=top.destroy).grid(row=2, column=1, sticky=W)
    top.mainloop()


def update_task_options(row_num=None, col_num=None):
    global task_options
    update_tasklist()
    task_options = OptionMenu(master, task_event, *task_names, command=get_event)
    if row_num and col_num:
        task_options.grid_forget()
        task_options.grid(row=row_num, column=col_num, sticky=W)


def create_batch_file(window, file_type):
    global task_name
    batch_str = "@ECHO OFF\n\n"

    batch_str += "SET drive=" + PROGRAM_DRIVE + "\n\n"
    if file_type == "create_model":

        batch_str += "python %drive%:\python_code\cmd_main.py create_model"

        if chkStatusAbandoned.get() + chkStatusAnnounced.get() + chkStatusPlanned.get() + chkStatusProducing.get() > 0:
            batch_str += " -stat-"
            if chkStatusAbandoned.get():
                batch_str += "b"
            if chkStatusAnnounced.get():
                batch_str += "n"
            if chkStatusPlanned.get():
                batch_str += "l"
            if chkStatusProducing.get():
                batch_str += "r"

        if chkAfrica.get() + chkAsia.get() + chkCaribbean.get() + chkCentralAmerica.get() + chkEurope.get() + chkMiddleEast.get() + \
                chkNorthAmerica.get() + chkOceania.get() + chkSouthAmerica.get() + chkFormerSovietUnion.get() > 0:
            batch_str += " -regn-"
            if chkAfrica.get():
                batch_str += "africa,"
            if chkAsia.get():
                batch_str += "asia,"
            if chkCaribbean.get():
                batch_str += "caribbean,"
            if chkCentralAmerica.get():
                batch_str += "central_america,"
            if chkEurope.get():
                batch_str += "europe,"
            if chkMiddleEast.get():
                batch_str += "middle_east,"
            if chkNorthAmerica.get():
                batch_str += "north_america,"
            if chkOceania.get():
                batch_str += "oceania,"
            if chkSouthAmerica.get():
                batch_str += "south_america,"
            if chkFormerSovietUnion.get():
                batch_str += "former_soviet_union,"
            batch_str = batch_str[:-1]

        if chkDeleteExistingFiles.get() + chkDeleteForecastData.get() > 0:
            batch_str += " -delt-"
            if chkDeleteExistingFiles.get():
                batch_str += "e"
            if chkDeleteForecastData.get():
                batch_str += "f"

        if assetId.get():
            batch_str += ' -asid-"'  + assetId.get() + '"'
        if assetCountryName.get():
            batch_str += ' -ctry-"' + assetCountryName.get() + '"'
        if constituentName.get():
            batch_str += ' -cnst-"' + constituentName.get() + '"'
        if terrainName.get():
            batch_str += ' -trrn-"' + terrainName.get() + '"'
        if resourceName.get():
            batch_str += ' -rsrc-"' + resourceName.get() + '"'
        if facilityTypeName.get():
            batch_str += ' -fcty-"' + facilityTypeName.get() + '"'
        if basinName.get():
            batch_str += ' -basn-"' + basinName.get() + '"'
        if operatorName.get():
            batch_str += ' -optr-"' + operatorName.get() + '"'

        batch_str += " %*\n\n"
        batch_str += "EXIT"

        batch_file = open(str(TASK_DIR) + str(task_name.get()) + ".bat", "w")
        batch_file.write(batch_str)
        batch_file.close()

        task_config['action'] = str(TASK_DIR) + str(task_name.get()) + ".bat"
        display_config()
    window.destroy()


def choose_batch_file():
    createModels()


def checkboxRegionStatus(option):
    allStatus = chkAll.get()
    generalMsg.set("")

    if option == "MASTER":
        if allStatus == 1:
            chkAfrica.set(0)
            chkAsia.set(0)
            chkCaribbean.set(0)
            chkCentralAmerica.set(0)
            chkEurope.set(0)
            chkMiddleEast.set(0)
            chkNorthAmerica.set(0)
            chkOceania.set(0)
            chkSouthAmerica.set(0)
            chkFormerSovietUnion.set(0)
        else:
            chkAfrica.set(1)
            chkAsia.set(1)
            chkCaribbean.set(1)
            chkCentralAmerica.set(1)
            chkEurope.set(1)
            chkMiddleEast.set(1)
            chkNorthAmerica.set(1)
            chkOceania.set(1)
            chkSouthAmerica.set(1)
            chkFormerSovietUnion.set(1)
    else:
        chk1 = chkAfrica.get()
        chk2 = chkAsia.get()
        chk3 = chkCaribbean.get()
        chk4 = chkCentralAmerica.get()
        chk5 = chkEurope.get()
        chk6 = chkMiddleEast.get()
        chk7 = chkNorthAmerica.get()
        chk8 = chkOceania.get()
        chk9 = chkSouthAmerica.get()
        chk10 = chkFormerSovietUnion.get()
        if chk1 + chk2 + chk3 + chk4 + chk5 + chk6 + chk7 + chk8 + chk9 + chk10 > 0:
            chkAll.set(0)

    msgAll.set('')
    msgAfrica.set('')
    msgAsia.set('')
    msgCaribbean.set('')
    msgCentralAmerica.set('')
    msgEurope.set('')
    msgMiddleEast.set('')
    msgNorthAmerica.set('')
    msgOceania.set('')
    msgSouthAmerica.set('')
    msgFormerSovietUnion.set('')


def createModels():
    master = Toplevel()
    master.title("Create Batch File")
    master.geometry("450x600+250+150")

    Label(master, text="Enter Task Name:   ", padx=10, pady=10).grid(row=0, column=0, sticky=E)
    task_name_ent = Entry(master, textvariable=task_name, bd=1)
    task_name_ent.grid(row=0, column=1, sticky=W)
    task_name_ent.bind('<Return>', get_task_name)

    Checkbutton(master, text="All", variable=chkAll, command=lambda: checkboxRegionStatus("MASTER")).grid(row=1, column=1, sticky=W)

    Checkbutton(master, text="Abandoned", variable=chkStatusAbandoned).grid(row=1, column=0, sticky=W)
    Checkbutton(master, text="Announced", variable=chkStatusAnnounced).grid(row=2, column=0, sticky=W)
    Checkbutton(master, text="Planned", variable=chkStatusPlanned).grid(row=3, column=0, sticky=W)
    Checkbutton(master, text="Producing", variable=chkStatusProducing).grid(row=4, column=0, sticky=W)

    Checkbutton(master, text="Delete Forecast Data", variable=chkDeleteForecastData).grid(row=6, column=0, sticky=W)
    Checkbutton(master, text="Delete Existing Files", variable=chkDeleteExistingFiles).grid(row=7, column=0, sticky=W)

    Label(master, text="Terrain: ").grid(row=9, column=0, padx=5, sticky=E)
    OptionMenu(master, terrainName, *asset_param_dict['terrain']).grid(row=9, column=1,  sticky=W, columnspan=2)

    Label(master, text="Resource Type: ").grid(row=10, column=0, padx=5,sticky=E)
    OptionMenu(master, resourceName, *asset_param_dict['resource_type']).grid(row=10, column=1,  sticky=W, columnspan=2)

    Label(master, text="Facility Type: ").grid(row=11, column=0, padx=5, sticky=E)
    OptionMenu(master, facilityTypeName, *asset_param_dict['facility_type']).grid(row=11, column=1,  sticky=W, columnspan=2)

    Checkbutton(master, text="Africa", variable=chkAfrica,
                command=lambda: checkboxRegionStatus("OPTION"), state=NORMAL).grid(row=3, column=1, sticky=W)
    Checkbutton(master, text="Asia", variable=chkAsia,
                command=lambda: checkboxRegionStatus("OPTION"), state=NORMAL).grid(row=4, column=1, sticky=W)
    Checkbutton(master, text="Caribbean", variable=chkCaribbean,
                command=lambda: checkboxRegionStatus("OPTION"), state=NORMAL).grid(row=5, column=1, sticky=W)
    Checkbutton(master, text="Central America", variable=chkCentralAmerica,
                command=lambda: checkboxRegionStatus("OPTION"), state=NORMAL).grid(row=6, column=1, sticky=W)
    Checkbutton(master, text="Europe", variable=chkEurope,
                command=lambda: checkboxRegionStatus("OPTION"), state=NORMAL).grid(row=7, column=1, sticky=W)
    Checkbutton(master, text="Middle East", variable=chkMiddleEast,
                command=lambda: checkboxRegionStatus("OPTION"), state=NORMAL).grid(row=3, column=2, sticky=W)
    Checkbutton(master, text="North America", variable=chkNorthAmerica,
                command=lambda: checkboxRegionStatus("OPTION"), state=NORMAL).grid(row=4, column=2, sticky=W)
    Checkbutton(master, text="Oceania", variable=chkOceania,
                command=lambda: checkboxRegionStatus("OPTION"), state=NORMAL).grid(row=5, column=2, sticky=W)
    Checkbutton(master, text="South America", variable=chkSouthAmerica,
                command=lambda: checkboxRegionStatus("OPTION"), state=NORMAL).grid(row=6, column=2, sticky=W)
    Checkbutton(master, text="Former Soviet Union", variable=chkFormerSovietUnion,
                command=lambda: checkboxRegionStatus("OPTION"), state=NORMAL).grid(row=7, column=2, sticky=W)

    lastRow = 12

    Label(master, textvariable=msgAfrica).grid(row=3, column=2, sticky=W)
    Label(master, textvariable=msgAsia).grid(row=4, column=2, sticky=W)
    Label(master, textvariable=msgCaribbean).grid(row=5, column=2, sticky=W)
    Label(master, textvariable=msgCentralAmerica).grid(row=6, column=2, sticky=W)
    Label(master, textvariable=msgEurope).grid(row=7, column=2, sticky=W)
    Label(master, textvariable=msgMiddleEast).grid(row=8, column=2, sticky=W)
    Label(master, textvariable=msgNorthAmerica).grid(row=9, column=2, sticky=W)
    Label(master, textvariable=msgOceania).grid(row=10, column=2, sticky=W)
    Label(master, textvariable=msgSouthAmerica).grid(row=11, column=2, sticky=W)
    Label(master, textvariable=msgFormerSovietUnion).grid(row=12, column=22, sticky=W)

    Label(master, text="Asset id: ").grid(row=lastRow + 2, column=0, sticky=E)
    Entry(master, textvariable=assetId, width=45).grid(row=lastRow + 2, column=1, sticky=W, pady=4, columnspan=2)
    Checkbutton(master, text="From file", variable=chkExternalAssetFile,
                command=lambda: getAssetFile()).grid(row=1, column=2, sticky=W)

    Label(master, text="Country: ").grid(row=lastRow + 3, column=0, sticky=E)
    Entry(master, textvariable=countryName, width=45).grid(row=lastRow + 3, column=1, sticky=W, pady=4, columnspan=2)
    Label(master, text="Constituent: ").grid(row=lastRow + 4, column=0, sticky=E)
    Entry(master, textvariable=constituentName, width=45).grid(row=lastRow + 4, column=1, sticky=W, pady=4, columnspan=2)
    Label(master, text="Basin: ").grid(row=lastRow + 5, column=0, sticky=E)
    Entry(master, textvariable=basinName, width=45).grid(row=lastRow + 5, column=1, sticky=W, pady=4, columnspan=2)
    Label(master, text="Operator: ").grid(row=lastRow + 6, column=0, sticky=E)
    Entry(master, textvariable=operatorName, width=45).grid(row=lastRow + 6, column=1, sticky=W, pady=4, columnspan=2)

    Button(master, text="Create Batch File", command=lambda: create_batch_file(master, "create_model")).grid(row=lastRow + 7, column=1, sticky=W, pady=4, padx=4)

    Button(master, text='Quit', command=master.destroy).grid(row=lastRow + 7, column=2, columnspan=2, sticky=W, pady=4, padx=4)
    Label(master, textvariable=generalMsg).grid(row=lastRow + 4, column=1, sticky=W)

# Generate main display window -----------------------------------------------------------------------------------------
def getAssetFile():
    pass

def new_task_main():
    master.geometry(MAIN_WINDOW_SIZE)
    master.title('Create New Task')


    update_chainlist()
    reset_task_config()
    reset_config_display()

    choose_task_option.grid_forget()
    choose_task_label.grid_forget()
    back_button.grid_forget()
    finish_button.grid_forget()

    task_name_label.grid(row=1, column=0, sticky=W)
    task_name_entry.grid(row=1, column=1, sticky=W)
    task_name_entry.bind('<Return>', get_task_name)
    schedule_label.grid(row=3, column=0, sticky=W)
    daily_radio.grid(row=3, column=1, sticky=W)
    weekly_radio.grid(row=4, column=1, sticky=W)
    once_radio.grid(row=5, column=1, sticky=W)
    event_radio.grid(row=6, column=1, sticky=W)
    action_label.grid(row=8, column=0, sticky=W)
    action_button.grid(row=8, column=1, sticky=W)
    save_button.grid(row=12, column=4, sticky=E)
    exit_button.grid(row=12, column=5, sticky=W)
    update_task_options(7, 1)
    task_event.set('Choose Event')
    display_config()


# Create Options menu in menubar ---------------------------------------------------------------------------------------

menubar = Menu(master)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Run Task", command=choose_run_task)
filemenu.add_command(label="Create New Task", command=new_task_main)
filemenu.add_command(label="Create Task Chain", command=choose_chain)
filemenu.add_command(label="Create Batch File", command=(lambda: choose_batch_file()))
filemenu.add_command(label="View Task", command=(lambda: get_config('view')))
filemenu.add_command(label="View All Tasks", command=view_all_tasks)
filemenu.add_command(label="Edit Task", command=(lambda: get_config('edit')))
filemenu.add_command(label="Delete Task", command=choose_delete_task)
filemenu.add_command(label="Delete All Tasks", command=(lambda: clear_tasks()))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.quit)

menubar.add_cascade(label='Options', menu=filemenu)
master.config(menu=menubar)

update_tasklist()
task_options = OptionMenu(master, task_event, *task_names, command=lambda: get_event)
#update_task_options()
update_chainlist()
# Initialize dynamic widgets -------------------------------------------------------------------------------------------

task_event.set('Choose Event')
choose_task_label = Label(master, text="Choose Task:   ", padx=10)
choose_task_option = OptionMenu(master, taskname, *task_names, command=config_change)

space = Label(master, text="")

finish_button = Button(master, text='Finish', command=create_task, padx=10)
exit_button = Button(master, text='Exit', command=master.destroy, padx=10)
exit_button.grid(row=12, column=5, sticky=W)
back_button = Button(master, text='Back', command=new_task_main, padx=10)
save_button = Button(master, text='Save', command=(lambda: set_config()), padx=10)
save_button.grid(row=12, column=4, sticky=E)


# Create widgets for main display --------------------------------------------------------------------------------------

task_name_label = Label(master, text="Enter Task Name:   ", padx=10, pady=10)
task_name_label.grid(row=1, column=0, sticky=E)

task_name_entry = Entry(master, textvariable=task_name, bd=1)
task_name_entry.grid(row=1, column=1, sticky=W)
task_name_entry.bind('<Return>', get_task_name)

schedule_label = Label(master, text='Choose Schedule:   ', padx=10)
schedule_label.grid(row=3, column=0, sticky=E)

daily_radio = Radiobutton(master, text='Daily', variable=schedule, value=1,command=(lambda: get_schedule('Daily')))
daily_radio.grid(row=3, column=1, sticky=W)

weekly_radio = Radiobutton(master, text='Weekly', variable=schedule, value=2, command=(lambda: get_schedule('Weekly')))
weekly_radio.grid(row=4, column=1, sticky=W)

once_radio = Radiobutton(master, text='Once', variable=schedule, value=3, command=(lambda: get_schedule('Once')))
once_radio.grid(row=5, column=1, sticky=W)

event_radio = Radiobutton(master, text='After Event', variable=schedule, value=4, command=(lambda: get_schedule('Event')))
event_radio.grid(row=6, column=1, sticky=W)

action_label = Label(master, text='Choose Action:   ', padx=10, pady=10)
action_label.grid(row=8, column=0, sticky=E)

action_button = Button(master, text='Find Batch File', command=get_action)
action_button.grid(row=8, column=1, sticky=W)

create_batch_button = Button(master, text="Create Batch File", command=(lambda: choose_batch_file()))
create_batch_button.grid(row=9,column=1, sticky=W)

display_config()
update_task_options()

master.mainloop()

# ----------------------------------------------------------------------------------------------------------------------
