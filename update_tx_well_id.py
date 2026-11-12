from globaldata import *

wellbore_nums = ['00','01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(wellbore_num) for wellbore_num in range(10,100)]
wellbore_nums = sorted(wellbore_nums)


def main():
    conn = get_connection(database='US_Wells_Texas', server='sql_server')
    curr = conn.cursor()
    tx_well_data = get_data('api_number, id, oil_gas_code', 'dbo.tx_ref_well_id', database='US_Wells_Texas', server='sql_server', sql_where="wellbore_no='98' AND oil_gas_code IS NOT NULL", datatype='plural', cursor=curr)
    sql_update = "UPDATE dbo.tx_ref_well_id SET wellbore_no='{}' WHERE api_number='{}' AND id={} AND oil_gas_code='{}'"
    well_data_count = len(tx_well_data)
    well_data_num = 1
    for api_number, well_id, oil_gas_code in tx_well_data:
        print '{}/{}: {} - {} - {}'.format(well_data_num, well_data_count, api_number, well_id, oil_gas_code)
        sql_where = "wellbore_no!='98' AND api_number='{}' AND oil_gas_code='{}'"
        try:
            max_wellbore_no = get_data('MAX(wellbore_no)', 'dbo.tx_ref_well_id', database='US_Wells_Texas', server='sql_server', sql_where=sql_where.format(api_number, oil_gas_code), single_value=True)
            max_wellbore_indx = wellbore_nums.index(max_wellbore_no)
        except:
            max_wellbore_indx = -1
        wellbore_no = wellbore_nums[max_wellbore_indx + 1]
        curr.execute(sql_update.format(wellbore_no, api_number, well_id, oil_gas_code))
        commit(curr)
        well_data_num += 1
    curr.execute("UPDATE dbo.tx_ref_well_id SET tx_well_id=CONCAT(api_number,'00',wellbore_no) WHERE oil_gas_code='O' AND tx_well_id IS NULL AND LEN(wellbore_no)=2")
    commit(curr)
    curr.execute("UPDATE dbo.tx_ref_well_id SET tx_well_id=CONCAT(api_number,'01',wellbore_no) WHERE oil_gas_code='G' AND tx_well_id IS NULL AND LEN(wellbore_no)=2")
    commit(curr)
    curr.close()
    conn.close()


def main2():
    conn = get_connection(database='US_Wells_Texas', server='sql_server')
    curr = conn.cursor()
    tx_well_data = get_data('WellID, well_name', 'dbo.Need_TX_Well_ID', database='US_Wells_Texas', server='sql_server', sql_where="well_name IS NOT NULL", datatype='plural', cursor=curr)
    sql_update = "UPDATE dbo.Need_TX_Well_ID SET well_no='{}' WHERE WellID={}"
    well_data_count = len(tx_well_data)
    well_data_num = 1
    for well_id, well_name in tx_well_data:
        well_no  = ''
        well_num = well_name.split()[-1]
        well_no  = well_num.replace(' ','').replace('-','').replace('_','')
        print '{}/{}: {} - {} - {}'.format(well_data_num, well_data_count, well_id, well_name, well_no)
        curr.execute(sql_update.format(well_no, well_id))
        commit(curr)
        well_data_num += 1
    curr.close()
    conn.close()



if __name__=='__main__':
    main()