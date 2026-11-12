import ftputil
import urllib2, shutil
from time import sleep
import os

from globaldata import get_data
OUTPUT_DIR = 'D:\\GlobalData\\Data\\tx_data\\csv_files\\'

def get_completion_data():
    with ftputil.FTPHost('ftp.rrc.texas.gov', 'subdata', 'WGn4t7SM') as ftp_host:
        ftp_host.chdir('CMPL_Data')
        cmpl_dirs = ftp_host.listdir(ftp_host.curdir)
        for cmpl_dir in cmpl_dirs:
            print cmpl_dir
            ftp_host.chdir(cmpl_dir)
            zipfiles = ftp_host.listdir(ftp_host.curdir)
            for zipfile in zipfiles:
                print '\t', zipfile
                if ftp_host.path.isfile(zipfile):
                    ftp_host.download(zipfile, OUTPUT_DIR+zipfile)
            ftp_host.chdir('..')

def get_well_data():
    url = 'ftp://ftpe.rrc.texas.gov/shpapidb/api/api{}.dbf'
    county_nos = get_data('county_no', 'dbo.tx_ref_well_id', database='US_Wells_Texas', server='sql_server')
    print sorted(county_nos)
    for county_no in sorted(county_nos):
        sleep(1)
        print 'Downloading well data file for county no: {} ...'.format(county_no)
        ftpfile = urllib2.urlopen(url.format(county_no))
        with open(OUTPUT_DIR+'api{}.dbf'.format(county_no), "wb") as localfile:
            shutil.copyfileobj(ftpfile, localfile)

def rename_api_dbf_files():
    for api_dbf_filename in os.listdir(OUTPUT_DIR):
        os.rename(OUTPUT_DIR+api_dbf_filename, OUTPUT_DIR+'')

if __name__=='__main__':
    #get_completion_data()
    get_well_data()