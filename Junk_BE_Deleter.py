import os
import re

# Folder path where your Excel files are stored
folder_path = r"D:\TitanJobs\Titan1\GlobalData\Macros\BreakevenMacros"

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if it's an Excel file
    if filename.lower().endswith(('.xlsm')):
        # Remove extension
        name_part = os.path.splitext(filename)[0]
        parts = name_part.split('_')

        # Check if last part is a 4-digit number
        if len(parts) > 1 and re.match(r'^\d{4}$', parts[-1]):
            file_path = os.path.join(folder_path, filename)
            try:
                os.remove(file_path)
                print("Deleted:", filename)
            except Exception as e:
                print("Error deleting {}: {}".format(filename, e))
print("Removed Junk BE files ..")
