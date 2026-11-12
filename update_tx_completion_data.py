import globaldata as gd


def main():
    conn = gd.get_connection(database='us_wells')
    curr = conn.cursor()
    tracking_nos = gd.get_data('tracking_no', 'tx_completion_data', database='us_wells', cursor=curr, datatype='int', sql_where='tx_well_id IS NULL AND tracking_no > 180000')
    tracking_no_count = len(tracking_nos)
    tracking_no_num = 1
    for tracking_no in tracking_nos:
        print '{}/{}: {}'.format(tracking_no_num, tracking_no_count, tracking_no)
        comp_records = gd.get_data('comp_record', 'tx_comp_data_records', database='us_wells', cursor=curr, sql_where='tracking_no={} AND record_code="PACKET"'.format(tracking_no))
        well_nos = []
        for comp_record in comp_records:
            well_no = comp_record.split('{')[9].strip()
            well_nos.append(well_no)
        well_nums = list(set(well_nos))
        if len(well_nums) == 1:
            well_num = well_nums[0]
            print 'UPDATE tx_completion_data SET well_no="{}" WHERE tracking_no={} AND tx_well_id IS NULL'.format(well_num, tracking_no)
            curr.execute('UPDATE tx_completion_data SET well_no="{}" WHERE tracking_no={} AND tx_well_id IS NULL'.format(well_num, tracking_no))
            gd.commit(curr)
        tracking_no_num += 1
    curr.close()
    conn.close()

if __name__=='__main__':
    main()
