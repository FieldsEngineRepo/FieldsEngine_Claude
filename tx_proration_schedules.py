import globaldata as gd
import os


INPUT_FILE_DIR  = 'D:\\GlobalData\\Data\\web_scrape\\TX_web_data\\field_schedules\\'
OUTPUT_FILE_DIR = gd.DATA_DIR + 'web_scrape\\TX_Web_Data\\schedule_txts\\'
OIL_SCHED_DIR   = 'C:\\Texas_Well_Data\\tx_schedule_data\\process\\'

MONTH_NOS  = {
    'JAN': '01',
    'FEB': '02',
    'MAR': '03',
    'APR': '04',
    'MAY': '05',
    'JUN': '06',
    'JUL': '07',
    'AUG': '08',
    'SEP': '09',
    'OCT': '10',
    'NOV': '11',
    'DEC': '12'
}
MONTH_NUMS = {
    'JANUARY'  : '01',
    'FEBRUARY' : '02',
    'MARCH'    : '03',
    'APRIL'    : '04',
    'MAY'      : '05',
    'JUNE'     : '06',
    'JULY'     : '07',
    'AUGUST'   : '08',
    'SEPTEMBER': '09',
    'OCTOBER'  : '10',
    'NOVEMBER' : '11',
    'DECEMBER' : '12'
}

def extract_schedule_urls():
    for in_fname in os.listdir(INPUT_FILE_DIR):
        with open(INPUT_FILE_DIR + in_fname) as in_file:
            filelines = in_file.readlines()
            for fileline in filelines:
                if fileline.startswith('<td><a href='):
                    print in_fname, fileline[12:]


def parse_oil_field_schedules(debug=False):
    conn = gd.get_connection(server='sql_server', database='US_Wells_Texas')
    curr = conn.cursor()
    sched_count = len(os.listdir(OIL_SCHED_DIR))
    sched_num   = 1
    sql_insert = "INSERT INTO tx_oil_field_schedule (process_code, well_record, source_line, source_file, sched_date, district_no, field_name, field_no, operator, operator_no, lease_name, lease_no) VALUES (0, '{}', {}, '{}', '{}', '{}', '{}', {}, '{}', {}, '{}', '{}')"
    for oil_field_sched in os.listdir(OIL_SCHED_DIR):
        in_data_group    = False
        last_district_line = 0
        last_header_line   = 0
        last_operator_line = 0
        last_lease_line    = 0
        last_well_line     = 0
        full_sched_date    = ''
        sched_date         = ''
        district_no        = ''
        field_name         = ''
        field_no           = 0
        operator           = ''
        operator_no        = 0
        lease_name         = ''
        lease_no           = ''
        exit               = 0
        exit_data          = []
        header_data = ()
        with open(OIL_SCHED_DIR + oil_field_sched) as sched_file:
            filelines = sched_file.readlines()
            line_count = len(filelines)
            if line_count == 1:
                filelines = filelines[0].split('\r')
                line_count = len(filelines)
                print line_count
            for line_num in range(line_count):
                fileline = filelines[line_num]
                if fileline.startswith('EXHIBIT A - OIL PRORATION SCHEDULE'):
                    exit = 1
                    last_district_line = line_num
                    full_sched_date = fileline[53:71].strip()
                    sched_date = full_sched_date[-4:] + MONTH_NOS[full_sched_date[:3]]
                    district_no = fileline.split()[-1].strip()[-2:]
                    header_data = (sched_date, district_no,)
                elif len(fileline.strip()) > 0 and (((last_district_line == (line_num - 3)) and len(filelines[line_num-1].strip()) == 0) or ((line_num+1 < line_count) and (((last_district_line == (line_num - 2)) and filelines[line_num+1][75:].startswith('MVBAL')) or filelines[line_num+1].startswith('* *') or filelines[line_num+1].startswith(' * *')))):
                    exit = 2
                    field_name = fileline[:33].rstrip().replace('"', '').replace(',', '').replace("'","")
                    field_no = fileline[33:41]
                    header_data += (field_name, field_no)
                elif fileline.startswith('  WELL   DEPTH  POTE') or fileline.startswith('  WELL    POTE'):
                    exit = 3
                    last_header_line = line_num
                elif last_header_line and (last_header_line == (line_num - 2)) and len(fileline.strip()) > 0:
                    exit = 4
                    last_operator_line = line_num
                    in_data_group = True
                    operator    = fileline[:33].rstrip().replace('"', '').replace(',', '').replace("'","")
                    operator_no = fileline[33:39]
                    header_data += (operator, operator_no)
                elif fileline.startswith('WELLS: ') or fileline.startswith('UNIT " " TOTALS') or fileline.startswith(' * * *') or fileline.startswith('* * *') or fileline.startswith('DISC:') or fileline.startswith('WELL STATUS TEST') or fileline.startswith('ACRES:')  or fileline.startswith('ALLOC:'):
                    exit = 5
                    in_data_group = False
                elif in_data_group and len(fileline.strip()) > 0 and (fileline[0] not in ['-', ' ', '*', '|']):
                    exit = 6
                    last_operator_line = line_num
                    operator    = fileline[:33].rstrip().replace('"', '').replace(',', '').replace("'","")
                    operator_no = fileline[33:39]
                    header_data = (sched_date, district_no, field_name, field_no, operator, operator_no)
                elif in_data_group and (last_operator_line and (last_operator_line == (line_num - 1))) and not fileline.startswith('- - - - -') and (len(fileline.strip()) == 0):
                    exit = 7
                    last_lease_line = line_num
                    lease_no   = '0'+fileline[1:6]
                    lease_name = fileline[8:45].rstrip().replace('"', '').replace(',', '').replace("'","")
                    header_data += (lease_name, lease_no)
                elif in_data_group and ((len(fileline.strip()) == 122) or (fileline[45:].startswith('(CONT)'))) and (fileline[1] != ' '):
                    exit = 8
                    last_lease_line = line_num
                    lease_no   = '0'+fileline[1:6]
                    lease_name = fileline[8:45].rstrip().replace('"', '').replace(',', '').replace("'","")
                    header_data = (sched_date, district_no, field_name, field_no, operator, operator_no, lease_name, lease_no)
                elif in_data_group and (len(fileline.rstrip()) == 132) and not (fileline.startswith('- -') or fileline.startswith(' - -')):
                    exit = 9
                    well_record = fileline.rstrip().replace('"', ' ').replace(',', ' ').replace("'"," ")
                    curr.execute(sql_insert.format(well_record,line_num,oil_field_sched,*header_data))
                    gd.commit(curr)
                elif in_data_group and (len(fileline.strip()) == 0):
                    exit = 10
                    in_data_group = False
                elif in_data_group and fileline.startswith('- - - - -'):
                    exit = 11
                    in_data_group = False
                else:
                    exit = 12
                    pass
                if debug:
                    print '{} >> ({}/{}) --- {}/{} --- {}: {} --> {}'.format(oil_field_sched, sched_num, sched_count, line_num, line_count, exit, fileline.strip(), header_data)
                else:
                    print '{} >> ({}/{}) --- {}/{}'.format(oil_field_sched, sched_num, sched_count, line_num, line_count)
            sched_num += 1
    curr.close()
    conn.close()


def parse_oil_operator_schedules(debug=False):
    conn = gd.get_connection(database='us_wells')
    curr = conn.cursor()
    sched_count = len(os.listdir(OIL_SCHED_DIR))
    sched_num   = 1
    sql_insert = 'INSERT INTO tx_oil_operator_schedule (process_code, well_record, source_line, source_file, sched_date, operator, district_no, field_name, lease_name, lease_no) VALUES (0, "{}", {}, "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
    for oil_operator_sched in os.listdir(OIL_SCHED_DIR):
        in_data_group      = False
        in_oil_data_group  = False
        in_gas_data_group  = False
        in_operator_group  = False
        well_record        = ''
        full_sched_date    = ''
        sched_date         = ''
        district_no        = ''
        field_name         = ''
        operator           = ''
        lease_name         = ''
        lease_no           = ''
        exit               = 0
        exit_data          = []
        header_data        = ()
        with open(OIL_SCHED_DIR + oil_operator_sched) as sched_file:
            filelines = sched_file.readlines()
            line_count = len(filelines)
            if line_count == 1:
                filelines = filelines[0].split('\r')
                line_count = len(filelines)
                print line_count
            for line_num in range(line_count):
                fileline = filelines[line_num]
                if fileline.startswith('         OIL AND GAS PRORATION SCHEDULE LISTED BY OPERATOR'):
                    exit               = 1
                    full_sched_date    = fileline[64:].strip().split()
                    sched_date         = full_sched_date[1] + MONTH_NUMS[full_sched_date[0].upper()]
                    in_operator_group  = True
                    in_data_group      = False
                    in_oil_data_group  = False
                    in_gas_data_group  = False
                    district_no        = ''
                    field_name         = ''
                    operator           = ''
                    lease_name         = ''
                    lease_no           = ''
                    header_data        = (sched_date,)
                elif in_operator_group and fileline.upper()[55:].startswith('STATUS DATE'):
                    exit               = 2
                    operator = fileline[8:55].upper().strip().replace('"', '').replace(',', '').replace("'","")
                    in_operator_group  = False
                    in_data_group      = True
                    header_data        = (sched_date, operator)
                elif in_data_group and not in_operator_group and fileline.upper().startswith('OIL-WELLS'):
                    exit               = 3
                    in_oil_data_group  = True
                    in_gas_data_group  = False
                elif in_data_group and not in_operator_group and fileline.upper().startswith('GAS-WELLS'):
                    exit               = 4
                    in_gas_data_group  = True
                    in_oil_data_group  = False
                elif in_data_group and not in_operator_group and len(fileline.strip()) == 0:
                    exit               = 5
                    in_gas_data_group  = False
                    in_oil_data_group  = False
                elif in_oil_data_group and not in_operator_group and fileline.upper()[:4] in ['01  ','02  ','03  ','04  ','05  ','06  ','6E  ','7B  ','7C  ','08  ','8A  ','8B  ','09  ','10  ']:
                    exit               = 6
                    district_no        = fileline.upper()[:2]
                    field_name         = fileline.upper()[4:].rstrip().replace('"', '').replace(',', '').replace("'","")
                    header_data        = (sched_date, operator, district_no, field_name)
                elif in_oil_data_group and not in_operator_group and len(fileline.strip()) > 0 and (fileline[:7] == '       ') and (fileline[24] in ['0','1','2','3','4','5','6','7','8','9']):
                    exit               = 7
                    line_len           = len(fileline)
                    lease_name         = fileline[7:24].strip().replace('"', ' ').replace(',', ' ').replace("'"," ")
                    lease_no           = '0' + fileline[24:29]
                    well_record        = gd.encode_str(fileline.replace('"', ' ').replace(',', ' ').replace("'"," "))
                    well_rec_len       = len(well_record)
                    well_record        = (' '*(line_len-well_rec_len)) + well_record
                    header_data        = (sched_date, operator, district_no, field_name, lease_name, lease_no)
                    curr.execute(sql_insert.format(well_record,line_num,oil_operator_sched,*header_data))
                    gd.commit(curr)
                elif in_oil_data_group and not in_operator_group and len(fileline.strip()) > 0 and (fileline[:38] == (' '*38)) and not fileline[42:].upper().startswith('LEASE TOTALS'):
                    exit               = 8
                    line_len           = len(fileline)
                    well_record        = gd.encode_str(fileline.replace('"', ' ').replace(',', ' ').replace("'"," "))
                    well_rec_len       = len(well_record)
                    well_record        = (' '*(line_len-well_rec_len)) + well_record
                    curr.execute(sql_insert.format(well_record,line_num,oil_operator_sched,*header_data))
                    gd.commit(curr)
                else:
                    exit               = 9

                if debug:
                    print '{} >> ({}/{}) --- {}/{} --- {}: {} --> {}'.format(oil_operator_sched, sched_num, sched_count, line_num, line_count, exit, fileline.strip(), header_data)
                else:
                    print '{} >> ({}/{}) --- {}/{}'.format(oil_operator_sched, sched_num, sched_count, line_num, line_count)
            sched_num += 1
    curr.close()
    conn.close()




if __name__=='__main__':
    parse_oil_field_schedules(debug=False)