from globaldata import *


mach_daily_cols = ['NewMineId', 'MineID', 'MineName', 'MineCountry', 'State', 'MineRegion', 'MineStage', 'MachineryType', 'EquipmentType',
                   'Make', 'Model', 'SizeClass', 'EquipmentCost', 'NumberInstalled', 'EquipmentVintage', 'EquipmentVintageSource',
                   'EstimatedReplacementTiming', 'EstimatedAdditionsNumber', 'EstimatedAdditionsYear', 'ReportedYear', 'Source']

mach_data_cols = ['NewMineId', 'MineID', 'MineName', 'MineCountry', 'State', 'MineRegion', 'MineStage', 'MachineryType', 'EquipmentType',
                  'Make', 'Model', 'EquipmentSizeLow', 'EquipmentSizeHigh', 'EquipmentUnit', 'EquipmentCost', 'NumberInstalled',
                  'EquipmentVintage', 'EquipmentVintageSource', 'EstimatedReplacementTiming', 'EstimatedAdditionsNumber', 'EstimatedAdditionsYear',
                  'ReportedYear', 'Source']


daily_col_str = ', '.join(mach_daily_cols)
data_col_str  = ', '.join(mach_data_cols)
data_col_str  = ', '.join([col_name + '=%s' for col_name in mach_data_cols])
data_var_str  = ', '.join(['%s']*len(mach_data_cols))

def create_rom_capacity_view(curr):
    print 'Creating new last_rom_capacity view ...'
    curr.execute('DROP VIEW last_rom_capacity')
    curr.execute('COMMIT')

    sql_create  = 'CREATE VIEW last_rom_capacity AS '
    sql_create += '(SELECT NewMineId, MineName, MAX(capacityYear) AS maxCapacityYear, capacity, capacityUnit '
    sql_create += 'FROM mining_capacity_daily WHERE capacityType="ROM Capacity" GROUP BY NewMineId) '
    curr.execute(sql_create)
    curr.execute('COMMIT')


def enter_machinery_data(curr, clr_tbl):
    if clr_tbl:
        curr.execute('TRUNCATE TABLE mining_machinery_data')

    sql_select  = 'SELECT %s FROM mining_machinery_daily WHERE LENGTH(SizeClass) > 0 AND EquipmentType="Mining Truck" ' % daily_col_str
    sql_select += 'AND NewMineId IN (SELECT DISTINCT NewMineId FROM last_rom_capacity)'
    curr.execute(sql_select)
    for datarow in curr.fetchall():
        sql_update = 'UPDATE mining_machinery_daily SET EquipmentSizeLow=%s, EquipmentSizeHigh=%s, EquipmentUnit=%s WHERE '
        sql_update += 'NewMineId=%s AND machineryType=%s AND EquipmentType=%s AND Make=%s AND Model=%s AND SizeClass=%s'

        NewMineId, MineID, MineName, MineCountry, State, MineRegion, MineStage, MachineryType, EquipmentType = datarow[:9]
        Make, Model, SizeClass, EquipmentCost, NumberInstalled, EquipmentVintage, EquipmentVintageSource     = datarow[9:16]
        EstimatedReplacementTiming, EstimatedAdditionsNumber, EstimatedAdditionsYear, ReportedYear, Source   = datarow[16:]

        print '%s SizeClass:' % NewMineId, SizeClass

        if 'tonnes' in SizeClass.lower():
            equipment_data = SizeClass.lower().split('tonnes')
        elif 'tones' in SizeClass.lower():
            equipment_data = SizeClass.lower().split('tones')

        if len(equipment_data) == 2:
            EquipmentSize = float(equipment_data[0].strip())
        else:
            EquipmentSize = float(equipment_data[0].split())
        EquipmentUnit = 'Tonnes'

        param_vals = (EquipmentSize, EquipmentSize, EquipmentUnit, NewMineId, MachineryType, EquipmentType, Make, Model, SizeClass)
        curr.execute(sql_update, param_vals)
        curr.execute('COMMIT')

def enter_capacity_data(curr):
    print 'Retreiving equipment and capacity data ...'
    sql_select  = 'SELECT rom.NewMineId, mac.Make, mac.Model, mac.EquipmentUnit, rom.capacity AS ROMcapacity, '
    sql_select += 'ROUND(SUM(mac.EquipmentSizeLow * mac.NumberInstalled),2) AS EquipCapacity, '
    sql_select += 'ROUND((SUM(mac.EquipmentSizeLow * mac.NumberInstalled)/rom.capacity),2) AS EquipROMratio '
    sql_select += 'FROM last_rom_capacity AS rom, mining_machinery_daily AS mac '
    sql_select += 'WHERE NOT mac.NumberInstalled IS NULL AND NOT mac.EquipmentUnit IS NULL AND mac.EquipmentType="Mining Truck" '
    sql_select += 'AND NOT EquipmentUnit IS NULL AND rom.NewMineId=mac.NewMineId GROUP BY NewMineId ORDER BY NewMineId'
    curr.execute(sql_select)

    print 'Entering equipment and capacity data ...'
    for NewMineId, Make, Model, EquipmentUnit, ROMcapacity, EquipCapacity, EquipROMratio in curr.fetchall():
        print NewMineId
        sql_insert  = 'INSERT INTO mining_machinery_data (NewMineId, ROMcapacity, EquipCapacity, EquipROMratio) VALUES (%s, %s, %s, %s)'
        param_vals = (NewMineId, ROMcapacity, EquipCapacity, EquipROMratio)
        print sql_insert % param_vals
        curr.execute(sql_insert, param_vals)
        curr.execute('COMMIT')

def update_machinery_asset_data(curr):
    update_str = ', '.join(['a.%s=b.%s' % (col_name, col_name) for col_name in mach_data_cols[1:]])
    sql_update = 'UPDATE mining_machinery_data AS a, mining_machinery_daily AS b SET %s WHERE a.NewMineId=b.NewMineId' % update_str
    print sql_update
    curr.execute(sql_update)
    curr.execute('COMMIT')

def main(clr_tbl=False, rom_view=False, mach_data=True, cap_data=True, update_data=False):
    conn = get_connection(server='mysql', database='miningengineextract')
    curr = conn.cursor()
    if rom_view:  create_rom_capacity_view(curr)
    if mach_data: enter_machinery_data(curr, clr_tbl=clr_tbl)
    if cap_data:  enter_capacity_data(curr)
    if update_data: update_machinery_asset_data(curr)
    curr.close()
    conn.close()


if __name__=='__main__':
    main(clr_tbl=False, rom_view=False, mach_data=False, cap_data=False, update_data=True)
