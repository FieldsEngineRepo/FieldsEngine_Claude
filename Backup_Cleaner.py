import os
from glob import glob
folder_path = "D:\TitanJobs\Titan1\GlobalData\Regions\Backup"
for i in glob(os.path.join(folder_path,"*")):
    files = glob(os.path.join(i,"*.xlsx"))
    [os.remove(i) for i in files]
print("Removed Old Model Files from Backup")