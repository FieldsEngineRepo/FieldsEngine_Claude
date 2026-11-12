# main_template filled with (drive_letter, task_comment, task_body)
main_template = \
'''
@ECHO OFF
mode con: cols=60 lines=30

SET drive=%s

ECHO %s
%s

EXIT
'''

macro_template_1 = \
'''
@ECHO OFF
mode con: cols=50 lines=10

SET drive=%s

ECHO %s ...
powershell -Command "& {$app = New-Object -comobject Excel.Application; $wb = $app.Workbooks.Open('%%drive%%:%s%s'); $app.Run('%s'); $wb.Save(); $app.Quit();}"
python %%drive%%:\python_code\cmd_main.py %s %%*

EXIT
'''

# drive_letter = 'C'
# task_comment = 'Running Breakeven Asia'

# task_body --------------------------------------------
# macro_dir = '\GlobalData\Macros\BreakevenMacros\'
# macro_file = 'Breakeven_Asia'
# macro_name = 'ProcessFolderBreakevens'
# check_cmd = 'check_breakeven Asia Asia'
# ------------------------------------------------------

# task_values = (drive_letter, task_comment, macro_dir, macro_file, macro_name, check_cmd)

macro_template_2 = \
'''
@ECHO OFF
mode con: cols=50 lines=10

SET drive=C

ECHO Running Breakeven Africa ...
python %drive%:\python_code\cmd_main.py log -s Breakeven_Africa "Breakeven Africa" %*
powershell -Command "& {$app = New-Object -comobject Excel.Application; $wb = $app.Workbooks.Open('%drive%:\GlobalData\Macros\BreakevenMacros\Breakeven_Africa.xlsm'); $app.Run('ProcessFolderBreakevens'); $wb.Save(); $app.Quit();}"
python %drive%:\python_code\cmd_main.py check_breakeven Africa Africa %*

ECHO Running Breakeven Asia ...
python %drive%:\python_code\cmd_main.py log -s Breakeven_Asia "Breakeven Asia" %*
powershell -Command "& {$app = New-Object -comobject Excel.Application; $wb = $app.Workbooks.Open('%drive%:\GlobalData\Macros\BreakevenMacros\Breakeven_Asia.xlsm'); $app.Run('ProcessFolderBreakevens'); $wb.Save(); $app.Quit();}"
python %drive%:\python_code\cmd_main.py check_breakeven Asia Asia %*

ECHO Running Breakeven Caribbean ...
python %drive%:\python_code\cmd_main.py log -s Breakeven_Caribbean "Breakeven Caribbean" %*
powershell -Command "& {$app = New-Object -comobject Excel.Application; $wb = $app.Workbooks.Open('%drive%:\GlobalData\Macros\BreakevenMacros\Breakeven_Caribbean.xlsm'); $app.Run('ProcessFolderBreakevens'); $wb.Save(); $app.Quit();}"
python %drive%:\python_code\cmd_main.py check_breakeven Caribbean Caribbean %*

ECHO Running Breakeven Central America ...
python %drive%:\python_code\cmd_main.py log -s Breakeven_Central_America "Breakeven Central_America" %*
powershell -Command "& {$app = New-Object -comobject Excel.Application; $wb = $app.Workbooks.Open('%drive%:\GlobalData\Macros\BreakevenMacros\Breakeven_Central_America.xlsm'); $app.Run('ProcessFolderBreakevens'); $wb.Save(); $app.Quit();}"
python %drive%:\python_code\cmd_main.py check_breakeven "Central America" Central_America %*

ECHO Running Breakeven Oceania ...
python %drive%:\python_code\cmd_main.py log -s Breakeven_Oceania "Breakeven Oceania" %*
powershell -Command "& {$app = New-Object -comobject Excel.Application; $wb = $app.Workbooks.Open('%drive%:\GlobalData\Macros\BreakevenMacros\Breakeven_Oceania.xlsm'); $app.Run('ProcessFolderBreakevens'); $wb.Save(); $app.Quit();}"
python %drive%:\python_code\cmd_main.py check_breakeven Oceania Oceania %*

EXIT
'''
# task_values = (drive_letter,)
# for task in task_list:
#    task_values +=  (task_comment, macro_dir, macro_file_name, macro_name, check_command)

macro_template_3 = \
'''
@ECHO OFF
mode con: cols=50 lines=10

SET drive=C

ECHO Running Breakeven South America ...
python %drive%:\python_code\cmd_main.py log -s Breakeven_South_America "Breakeven South America" %*
powershell -Command "& {$app = New-Object -comobject Excel.Application; $wb = $app.Workbooks.Open('%drive%:\GlobalData\Macros\BreakevenMacros\Breakeven_South_America.xlsm'); $app.Run('ProcessFolderBreakevens'); $wb.Save(); $app.Quit();}"
python %drive%:\python_code\cmd_main.py check_breakeven "South America" South_America %*

EXIT
'''

macro_template_4 = \
'''
@ECHO OFF
mode con: cols=50 lines=10

SET drive=C
SET python_command=python %drive%:\python_code\cmd_main.py

CALL:runBreakeven Africa

EXIT


:runBreakeven
ECHO Running Breakeven %~1 ...
%python_command% log -s Breakeven_%~1 "Breakeven %~1" %*
%python_command% breakeven %~1 %*
%python_command% check_breakeven "%~1" %~1 %*
GOTO:EOF
'''

macro_template_5 = \
'''
@ECHO OFF
mode con: cols=50 lines=10

SET drive=C
SET python_command=python %drive%:\python_code\cmd_main.py

ECHO Running Breakeven Region A

CALL:runBreakeven "Africa" Africa
CALL:runBreakeven "Asia" Asia
CALL:runBreakeven "Caribbean" Caribbean
CALL:runBreakeven "Central America" Central_America
CALL:runBreakeven "Middle East" Middle_East
CALL:runBreakeven "Oceania" Oceania

EXIT


:runBreakeven
ECHO Running Breakeven %~1 ...
%python_command% log -s Breakeven_%~2 "Breakeven %~1" %*
%python_command% breakeven %~2 %*
%python_command% check_breakeven "%~1" %~2 %*
GOTO:EOF
'''

command_template_1 = \
'''
@ECHO OFF

SET drive=C

python %drive%:\python_code\cmd_main.py log -s CreateModel_Africa "Create Model Africa" %*
python %drive%:\python_code\cmd_main.py create_model -stat-nlrb -regn-africa -delt-e %*
python %drive%:\python_code\cmd_main.py log -e CreateModel_Africa %*
python %drive%:\python_code\cmd_main.py temp_log create_model Africa %*

EXIT
'''

command_template_2 = \
'''
@ECHO OFF

SET drive=C

python %drive%:\python_code\cmd_main.py log -s CreateModel_Rest_of_World_2 "Create Model Rest of World 2" %*
python %drive%:\python_code\cmd_main.py create_model -stat-nlrb -regn-africa,asia,caribbean,central_america,oceania -delt-e %*
python %drive%:\python_code\cmd_main.py log -e CreateModel_Rest_of_World_2 %*
python %drive%:\python_code\cmd_main.py temp_log create_model Rest_of_World_2 %*

EXIT
'''

command_template_3 = \
'''
@ECHO OFF

SET drive=C

python %drive%:\python_code\cmd_main.py log -s CreateModel_Rest_of_World_1 "Create Model Rest of World 1" %*
python %drive%:\python_code\cmd_main.py create_model -stat-nlrb -regn-north_america_1 %*
python %drive%:\python_code\cmd_main.py create_model -stat-nlrb -delt-e -regn-middle_east %*
python %drive%:\python_code\cmd_main.py log -e CreateModel_Rest_of_World_1 %*
python %drive%:\python_code\cmd_main.py temp_log create_model Rest_of_World_1 %*

EXIT
'''

command_template_4 = \
'''
@ECHO OFF

SET drive=C

python %drive%:\python_code\cmd_main.py log -s CreateModel_North_America_1 "Create Model NorthAmerica 1" %*
python %drive%:\python_code\cmd_main.py create_model -stat-nlrb -regn-north_america_1 %*
python %drive%:\python_code\cmd_main.py log -e CreateModel_North_America_1 %*
python %drive%:\python_code\cmd_main.py temp_log create_model North_America_1 %*

EXIT
'''

command_template_5 = \
'''
@ECHO OFF
mode con: cols=60 lines=30

SET drive=C

python %drive%:\python_code\cmd_main.py log -s AutomatedPanoramas "Generate Automated Panoramas" %*
python %drive%:\python_code\cmd_main.py generate_panoramas %*
python %drive%:\python_code\cmd_main.py log -e AutomatedPanoramas %*

EXIT
'''

multitask_template = \
'''
@ECHO OFF
mode con: cols=50 lines=10

SET drive=C
SET wait_time=5

python %drive%:\python_code\cmd_main.py log -s DataExport "Data Export Process" %*
python %drive%:\python_code\cmd_main.py data_export regns-X,X ce %*

START %drive%:\GlobalData\Tasks\ExportTasks\DataExport_Former_Soviet_Union
TIMEOUT %wait_time%

START %drive%:\GlobalData\Tasks\ExportTasks\DataExport_North_America_2
TIMEOUT %wait_time%

START %drive%:\GlobalData\Tasks\ExportTasks\DataExport_Europe
TIMEOUT %wait_time%

START %drive%:\GlobalData\Tasks\ExportTasks\DataExport_Rest_of_World_1
TIMEOUT %wait_time%

START %drive%:\GlobalData\Tasks\ExportTasks\DataExport_Rest_of_World_2
TIMEOUT %wait_time%

START %drive%:\GlobalData\Tasks\ExportTasks\DataExport_South_America
TIMEOUT %wait_time%

EXIT
'''

simpletask_template_1 = \
'''
@ECHO OFF
EXIT
'''

simpletask_template_2 = \
'''
@ECHO OFF
mode con: cols=60 lines=30

SET drive=C

python %drive%:\python_code\cmd_main.py log -e Run %*

EXIT
'''

simpletask_template_3 = \
'''
@ECHO OFF
ECHO Create Model Process Complete
'''
