import globaldata as gd
import os
import random
import shutil

IMPORT_CSV_DIR = 'D:\\GlobalData\\Data\\import_csv\\'
EXPORT_CSV_DIR = 'D:\\GlobalData\\Data\\export_csv\\'
RERUN_CSV_DIR  = 'D:\\GlobalData\\Data\\tx_permit_rerun\\'

def remove_title_lines():
    for permit_filename in os.listdir(IMPORT_CSV_DIR):
        print permit_filename
        with open(IMPORT_CSV_DIR + permit_filename) as permit_file:
            output = ''
            filelines = permit_file.readlines()
            for i in range(len(filelines)):
                if i > 3:
                    output += filelines[i]
            outfile_name = '{}{}_{}.csv'.format(EXPORT_CSV_DIR,permit_filename[:-4],random.randint(1000000,9999999))
            with open(outfile_name,'w') as permit_outfile:
                permit_outfile.write(output)

#County: MCMULLEN, Well Type: Oil Well,
#https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17&search=%7B"item"%3A%5B%7B"key"%3A"api_ft"%2C"value"%3A"00101692"%7D%5D%7D

def extract_search_data():
    for in_filename in os.listdir(RERUN_CSV_DIR):
        if in_filename[-3:] == 'csv':
            out_filename = in_filename
        else:
            out_filename = '{}_{}.csv'.format(in_filename.split('.csv')[0],random.randint(1000000,9999999))
        print '{}{} ---> {}{}'.format(RERUN_CSV_DIR, in_filename, IMPORT_CSV_DIR, out_filename)

        shutil.copy2(RERUN_CSV_DIR+in_filename, IMPORT_CSV_DIR+out_filename)
    for permit_filename in os.listdir(IMPORT_CSV_DIR):
        with open(IMPORT_CSV_DIR + permit_filename) as permit_file:
            #print permit_filename
            output = []
            filelines = permit_file.readlines()
            search_line = filelines[2]
            search_parts = search_line.split(',')
            for search_part in search_parts[:2]:
                #print search_part
                search_data = search_part.split(': ')[1]
                output.append(search_data)
            print "('{}','{}')".format(*output)

def extract_operator_data(debug=False):
    sql_update = "UPDATE tx_permit_data SET operator='{}', operator_no={} WHERE id={}"
    conn = gd.get_connection(database='US_Wells_Texas', server='sql_server')
    curr = conn.cursor()
    well_operator_data = gd.get_data('id, operator_data', 'tx_permit_data', database='US_Wells_Texas', server='sql_server', cursor=curr, datatype='plural', sql_where='process_code=9')
    data_count = len(well_operator_data)
    data_num = 1
    for id, operator_data in well_operator_data:
        try:
            data_parts = operator_data.split(' (')
            operator = ' ('.join(data_parts[:-1])
            operator_no = data_parts[-1]
            operator = operator.replace('.','').replace(',','')
            operator_no = int(operator_no[:-1])
            print '{}/{}  operator name: {} --- operator no: {}'.format(data_num, data_count, operator, operator_no)
            if debug: print sql_update.format(operator, operator_no, id)
            curr.execute(sql_update.format(operator, operator_no, id))
            gd.commit(curr)
        except:
            print operator_data
        data_num += 1
    curr.close()
    conn.close()



if __name__=='__main__':
    extract_operator_data(debug=False)
    #extract_search_data()
    #remove_title_lines()