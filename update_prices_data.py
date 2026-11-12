from globaldata import *
import os
import shutil

def update_prices_data_file():
    output_filename = 'prices_data_{}.csv'.format(get_date())
    prices_filename = os.listdir(CSV_IMPORT_DIR)[0]
    output_lines = ''
    with open(CSV_IMPORT_DIR + prices_filename) as prices_file:
        for prices_file_line in prices_file.readlines():
            if '(%)' in prices_file_line:
                output_lines += (prices_file_line.replace(' (%)', '_pct'))
            else:
                output_lines += prices_file_line
    shutil.move(CSV_IMPORT_DIR + prices_filename, DATA_DIR + prices_filename)

    with open(CSV_IMPORT_DIR + output_filename, 'w') as output_file:
        output_file.write(output_lines)



if __name__=='__main__':
    main()