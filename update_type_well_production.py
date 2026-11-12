from globaldata import *


def main():
    conn = get_connection()
    curr = conn.cursor()
    well_ids = get_data('well_permit_num', 'wells_pa')
    for well_id in well_ids:
        asset_id = int(well_id[:-3])
        print well_id, asset_id
        curr.execute('UPDATE type_well_production SET asset_id={} WHERE well_id="{}" AND asset_id IS NULL'.format(asset_id, well_id))
        commit(curr)

    curr.close()
    conn.close()

if __name__=='__main__':
    main()