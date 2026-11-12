from globaldata import *
import xlwings as xw

def extract_data(region, BE_REGION_DIR=BE_REGIONS):
    start_time = get_datetime()
    xlApp = xw.App(visible=False)
    region_name = '_'.join(region.split(' '))
    print region_name
    wb_out = xlApp.books.open(r'%s%s' % (BREAKEVEN_DIR, 'Breakeven_{}_0000.xlsm'.format(region_name)))
    output = wb_out.sheets['Output']
    outrow = 2
    asset_models = [model for model in os.listdir(BE_REGION_DIR + region) if model[:8] == 'MODELLED' and not ('~$' + model) in os.listdir(BE_REGION_DIR + region)]
    total_asset_count = len(asset_models)
    asset_num = 1
    for file_name in asset_models:
        date_time = get_datetime()
        wb = xlApp.books.open(r'%s/%s/%s' % (BE_REGION_DIR, region, file_name))
        asset_inputs  = wb.sheets['Asset Inputs']
        asset_summary = wb.sheets['Asset Summary']
        asset_id = int(asset_inputs.range('B1').value)
        print '%s/%s asset_id: %s' % (asset_num, total_asset_count, asset_id)
        asset_num +=1
        baseRemainBEOil = asset_summary.range((83, 4)).raw_value
        baseDevBEOil    = asset_summary.range((83, 2)).raw_value
        highRemainBEOil = asset_summary.range((84, 4)).raw_value
        highDevBEOil    = asset_summary.range((84, 2)).raw_value
        lowRemainBEOil  = asset_summary.range((85, 4)).raw_value
        lowDevBEOil     = asset_summary.range((85, 2)).raw_value
        baseRemainBEgas = asset_summary.range((83, 5)).raw_value
        baseDevBEgas    = asset_summary.range((83, 3)).raw_value
        highRemainBEgas = asset_summary.range((84, 5)).raw_value
        highDevBEgas    = asset_summary.range((84, 3)).raw_value
        lowRemainBEgas  = asset_summary.range((85, 5)).raw_value
        lowDevBEgas     = asset_summary.range((85, 3)).raw_value
        param_vals = [asset_id, file_name, baseRemainBEOil, baseRemainBEgas, baseDevBEOil, baseDevBEgas, highRemainBEOil, highRemainBEgas, highDevBEOil, highDevBEgas, lowRemainBEOil, lowRemainBEgas, lowDevBEOil, lowDevBEgas]
        output.range('A{}'.format(outrow)).value = param_vals
        output.range('U{}'.format(outrow)).value = date_time
        wb.close()
        wb_out.save()
        outrow += 1
    wb_out.save()
    wb_out.close()
    xlApp.quit()
    end_time = get_datetime()
    total_time = elapsed_time(start_time, end_time)
    print ''
    print 'Total Time: %s' % total_time
    print ''

def main(region):
    extract_data(region)


if __name__=='__main__':
    regions = ['Europe', 'North_America_2']
    for region in regions:
        main(region)


