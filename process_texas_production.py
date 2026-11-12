import shutil
import os


# Set location of DATA_DIR

DATA_DIR = ""
'''
DATA_DIR/
	-tx_data/
    	-tx_api_dbf/
    		-archive/
    			-output/
    		-output/
    	-tx_completion_data/
    		-archive/
    		-tx_completion_files/
    		-tx_completion_zipfiles/
    	-tx_permit_data/
    	-tx_production/
    		-archive/
    		-output/
    		-prod_files/
    	-tx_schedule_data/
    		-archive/
    		-process/
    	-tx_wellbore_data/
    		-archive/

'''


TX_DATA_DIR       = DATA_DIR + "tx_data\\"
TX_PROD_DIR       = TX_DATA_DIR + "tx_production\\"
TX_PROD_OUT_DIR   = TX_PROD_DIR + "output\\"
TX_PROD_ARCHIVE   = TX_PROD_DIR + "archive\\"
TX_PROD_FILES_DIR = TX_PROD_DIR + "prod_files\\"


def retrieve_prod_file():
	download_file(url=TX_PROD_URL, output_dir=TX_DATA_DIR, output_file=TX_PROD_FILES_ZIP)


def configure_prod_file(input_dir=TX_PROD_DIR, output_dir=TX_PROD_OUT_DIR, output_filename=OUTPUT_FILE):
	for prod_file in [in_file for in_file in os.listdir(input_dir) if in_file[-3:]=='dsv']:
		output_txt = ''
		with open(input_dir+prod_file) as input_prod_file:
			output_txt = input_prod_file.read()
			output_txt = output_txt.replace(',','')
			output_txt = output_txt.replace('.', '')
			output_txt = output_txt.replace('"', '')
			output_txt = output_txt.replace("'","")
			output_txt = output_txt.replace('}',',')
		with open(output_dir+output_filename, 'a') as output_prod_file:
			output_prod_file.write(output_txt)

if __name__=='__main__':
	retrieve_prod_file()
	configure_prod_file()
