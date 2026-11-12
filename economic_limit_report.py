import globaldata as gd
import os
import shutil

def move_files(src_dir, dst_dir, outfile_code, asset_list=None):
    for asset_model in [filename for filename in os.listdir(src_dir) if filename[-3:] == 'csv']:
        print src_dir + asset_model
        if asset_list:
            asset_id = int(asset_model.split('_')[1])
            if asset_id in asset_list:
                shutil.move(src_dir + asset_model, dst_dir + outfile_code + asset_model)
        else:
            shutil.move(src_dir + asset_model, dst_dir + asset_model)

def copy_files(src_dir, dst_dir, in_ext='', out_ext='', out_format='{}.{}', fname_indx=None, fname_incr=False):
    if fname_indx == None:
        fname_indx = -(len(in_ext)+1)
    input_files = [filename for filename in os.listdir(src_dir) if filename.endswith(in_ext)]
    input_file_num = 0
    input_file_count = len(input_files)
    for input_file in input_files:
        input_filename = input_file[:fname_indx]
        if fname_incr:
            output_file = out_format.format(input_filename, input_file_num, out_ext)
        else:
            output_file = out_format.format(input_filename,out_ext)
        print '({}/{}): {} ---> {}'.format(input_file_num, input_file_count, src_dir + input_file, dst_dir + output_file)
        shutil.copy2(src_dir+input_file, dst_dir+output_file)
        input_file_num += 1

def find_econ_limit_files(run_id):
    conn = gd.get_connection()
    curr = conn.cursor()
    economic_limit_ids = gd.get_data(param='asset_id', table='economic_limit', sql_where='econ_limit_code=1 AND run_id="{}"'.format(run_id), datatype='int')
    for region in os.listdir(gd.BE_REGIONS):
        region_dir = gd.BE_REGIONS + '{}\\'.format(region)
        for asset_model in [filename for filename in os.listdir(region_dir) if filename[-4:] == 'xlsx']:
            print region_dir + asset_model
            asset_id = int(asset_model.split('_')[1])
            if not asset_id in economic_limit_ids:
                shutil.move(region_dir + asset_model, gd.BE_REGIONS + asset_model)
    curr.close()
    conn.close()



if __name__ == '__main__':
   find_econ_limit_files('20190110_165036')

