from globaldata import *
import os

multi_folders = ['DiscFieldConfTasks', 'DiscFieldMacroTasks']

def change_drive_letter(old_drive, new_drive):
	for task_folder in [foldername for foldername in os.listdir(DF_TASKS) if foldername[-4:] != '.bat']:
		task_dir = DF_TASKS + '{}\\'.format(task_folder)
		if task_folder in multi_folders:
			for subtask_folder in os.listdir(task_dir):
				subtask_dir = task_dir+'{}\\'.format(subtask_folder)
				for taskfile_name in os.listdir(subtask_dir):
					taskfile_path = subtask_dir+'{}'.format(taskfile_name)
					print taskfile_name
					with open(taskfile_path, 'r+') as taskfile:
						output = ''
						for txtline in taskfile.readlines():
							if 'drive=C' in txtline:
								output += txtline.replace('drive=C', 'drive=D')
							else:
								output += txtline
						taskfile.seek(0)
						taskfile.write(output)
						taskfile.truncate()
		else:
			for taskfile_name in os.listdir(task_dir):
				taskfile_path = task_dir + '{}'.format(taskfile_name)
				print taskfile_name
				with open(taskfile_path, 'r+') as taskfile:
					output = ''
					for txtline in taskfile.readlines():
						if 'drive=C' in txtline:
							output += txtline.replace('drive={}'.format(old_drive), 'drive={}'.format(new_drive))
						else:
							output += txtline
					taskfile.seek(0)
					taskfile.write(output)
					taskfile.truncate()


if __name__=='__main__':
	change_drive_letter('C', 'D')


