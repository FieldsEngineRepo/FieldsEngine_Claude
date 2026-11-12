from globaldata import *
import xlwings as xw

type_well_inputs = {
    'well_1' : {'well num'     : 1,
                'wi col'       : '$H$',
                'ai start row' : 140,
                'ai end row'   : 250,
                'cl start row' : 347,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$N$',
                'cf capex'     : '$P$',
                'cf net wells' : '$AA$',
                'cf prod wells': '$AC$',
                'cf abandon'   : '$AE$'},

    'well_2' : {'well num'     : 2,
                'wi col'       : '$O$',
                'ai start row' : 256,
                'ai end row'   : 366,
                'cl start row' : 460,
                'cf year num'  : 'AG$',
                'cf crude'     : 'AH$',
                'cf year col'  : '$AT$',
                'cf capex'     : '$AV$',
                'cf net wells' : '$BG$',
                'cf prod wells': '$BI$',
                'cf abandon'   : '$BK$'},

    'well_3' : {'well num'     : 3,
                'wi col'       : '$V$',
                'ai start row' : 372,
                'ai end row'   : 482,
                'cl start row' : 573,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$BZ$',
                'cf capex'     : '$CB$',
                'cf net wells' : '$CM$',
                'cf prod wells': '$CO$',
                'cf abandon'   : '$CQ$'},

    'well_4' : {'well num'     : 4,
                'wi col'       : '$AC$',
                'ai start row' : 488,
                'ai end row'   : 598,
                'cl start row' : 686,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$DF$',
                'cf capex'     : '$DH$',
                'cf net wells' : '$DS$',
                'cf prod wells': '$DU$',
                'cf abandon'   : '$DW$'},

    'well_5' : {'well num'     : 5,
                'wi col'       : '$AJ$',
                'ai start row' : 604,
                'ai end row'   : 714,
                'cl start row' : 799,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$EL$',
                'cf capex'     : '$EN$',
                'cf net wells' : '$EY$',
                'cf prod wells': '$FA$',
                'cf abandon'   : '$FC$'},

    'well_6' : {'well num'     : 6,
                'wi col'       : '$AQ$',
                'ai start row' : 720,
                'ai end row'   : 830,
                'cl start row' : 912,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$FR$',
                'cf capex'     : '$FT$',
                'cf net wells' : '$GE$',
                'cf prod wells': '$GG$',
                'cf abandon'   : '$GI$'},

    'well_7' : {'well num'     : 7,
                'wi col'       : '$AX$',
                'ai start row' : 836,
                'ai end row'   : 946,
                'cl start row' : 1025,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$GX$',
                'cf capex'     : '$GZ$',
                'cf net wells' : '$HK$',
                'cf prod wells': '$HM$',
                'cf abandon'   : '$HO$'},

    'well_8' : {'well num'     : 8,
                'wi col'       : '$BE$',
                'ai start row' : 952,
                'ai end row'   : 1062,
                'cl start row' : 1138,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$ID$',
                'cf capex'     : '$IF$',
                'cf net wells' : '$IQ$',
                'cf prod wells': '$IS$',
                'cf abandon'   : '$IU$'},

    'well_9' : {'well num'     : 9,
                'wi col'       : '$BL$',
                'ai start row' : 1068,
                'ai end row'   : 1178,
                'cl start row' : 1251,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$JJ$',
                'cf capex'     : '$JL$',
                'cf net wells' : '$JW$',
                'cf prod wells': '$JY$',
                'cf abandon'   : '$KA$'},

    'well_10': {'well num'     : 10,
                'wi col'       : '$BS$',
                'ai start row' : 1184,
                'ai end row'   : 1294,
                'cl start row' : 1364,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$KP$',
                'cf capex'     : '$KR$',
                'cf net wells' : '$LC$',
                'cf prod wells': '$LE$',
                'cf abandon'   : '$LG$'},

    'well_11': {'well num'     : 11,
                'wi col'       : '$BZ$',
                'ai start row' : 1300,
                'ai end row'   : 1410,
                'cl start row' : 1477,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$LV$',
                'cf capex'     : '$LX$',
                'cf net wells' : '$MI$',
                'cf prod wells': '$MK$',
                'cf abandon'   : '$MM$'},

    'well_12': {'well num'     : 12,
                'wi col'       : '$CG$',
                'ai start row' : 1416,
                'ai end row'   : 1526,
                'cl start row' : 1590,
                'cf year num'  : 'A$',
                'cf crude'     : 'B$',
                'cf year col'  : '$NB$',
                'cf capex'     : '$ND$',
                'cf net wells' : '$NO$',
                'cf prod wells': '$NQ$',
                'cf abandon'   : '$NS$'},
}

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
capex_intangible = \
'''
=IF(OR($A{3}-'Asset Inputs'!$E$10+1>'Well Inputs'!{0}29,$A{3}-'Asset Inputs'!$E$10+1<0),0,IF($A{3}-'Asset Inputs'!$E$10+1=0,'Well Inputs'!{0}49,IF($A{3}-'Asset Inputs'!$E$10+1='Well Inputs'!{0}57+1,'Well Inputs'!{0}56,0)+'Well Inputs'!{0}55))*'Well Inputs'!{0}53
'''
capex_intangible_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
abandonment = \
'''
=IF($A{3}-'Asset Inputs'!$E$10+1='Well Inputs'!{0}29+1,'Well Inputs'!{0}58,0)
'''
abandonment_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
typewell_prod = \
'''
=IFERROR(INDEX('Type Well Cash Flow'!{5}$7:{5}$117,MATCH($A{3}-'Asset Inputs'!$E$10+1,'Type Well Cash Flow'!${4}$7:${4}$117,0)),0)
'''
typewell_prod_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
typewell_expend = \
'''
=IF($A{3}<'Asset Inputs'!$E$10,0,(IF($A{3}>='Asset Inputs'!$E$18,'Asset Inputs'!N{1}*(1+'Asset Inputs'!$E$19)^($A{3}-'Asset Inputs'!$E$18),'Asset Inputs'!N{1})/IF(SUMIF('Type Well Cash Flow'!${6}$7:${6}$117,$A{3},'Type Well Cash Flow'!${9}$7:${9}$117)=0,1,SUMIF('Type Well Cash Flow'!${6}$7:${6}$117,$A{3},'Type Well Cash Flow'!${9}$7:${9}$117))))
'''
typewell_expend_formulas = []
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
abandoned_wells = \
'''
=SUMIF(Calculations!$A$3062:$A$3769,${6}7-'Well Inputs'!{0}29,Calculations!${12}$3062:${12}$3769)+SUMIF(${6}$7:${6}$117,$N7-'Well Inputs'!{0}29,${11}$7:${11}$117)
'''
abandoned_wells_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
producing_wells = \
'''
=ROUND(IF(${6}8<'Asset Inputs'!$E$10,{11}8,SUMIF(Calculations!$A$3062:$A$3769,${6}8,Calculations!${12}$3062:${12}$3769))+{9}7-(SUMIF(Calculations!$A$3062:$A$3769,${6}7-'Well Inputs'!{0}29,Calculations!${12}$3062:${12}$3769)+SUMIF(${6}$7:${6}$117,$N7-'Well Inputs'!{0}29,${11}$7:${11}$117)),6)
'''
producing_wells_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
gross_revenue = \
'''
=IFERROR(INDEX(Calculations!$S${3}:$S${13},MATCH($A7+'Asset Inputs'!$E$10-1,Calculations!$A${3}:$A${13},0)),0)
'''
gross_revenue_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
capex = \
'''
=IFERROR(INDEX(Calculations!$Y${3}:$Y${13},MATCH($A7+'Asset Inputs'!$E$10-1,Calculations!$A${3}:$A${13},0)),0)+IF($A7=1,IFERROR(INDEX(Calculations!$Y${3}:$Y${13},MATCH('Asset Inputs'!$E$10-1,Calculations!$A${3}:$A${13},0)),0),0)
'''
capex_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
fiscal_take = \
'''
=IFERROR(INDEX(Calculations!$AE${3}:$AE${13},MATCH($A7+'Asset Inputs'!$E$10-1,Calculations!$A${3}:$A${13},0)),0)
'''
fiscal_take_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
capex_tangible = \
'''
=IF(OR($A{3}-'Asset Inputs'!$E$10+1>'Well Inputs'!{0}29,$A{3}-'Asset Inputs'!$E$10+1<0),0,IF($A{3}-'Asset Inputs'!$E$10+1=0,'Well Inputs'!{0}49,IF($A{3}-'Asset Inputs'!$E$10+1='Well Inputs'!{0}57+1,'Well Inputs'!{0}56,0)+'Well Inputs'!{0}55))*'Well Inputs'!{0}54
'''
capex_tangible_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
fixed_opex = \
'''
=IF(OR($A{3}-'Asset Inputs'!$E$10+1>'Well Inputs'!{0}29,$A{3}-'Asset Inputs'!$E$10+1<1),0,'Well Inputs'!{0}59)
'''
fixed_opex_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
variable_opex = \
'''
=IF(OR($A{3}-'Asset Inputs'!$E$10+1>'Well Inputs'!{0}29,$A{3}-'Asset Inputs'!$E$10+1<1),0,'Well Inputs'!{0}61*($B{3}+$D{3}+$E{3})+'Well Inputs'!{0}62*($C{3}+$F{3})+'Well Inputs'!{0}64*$E{3}+'Well Inputs'!{0}63*$G{3}+'Well Inputs'!{0}65)
'''
variable_opex_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
opex = \
'''
=IFERROR(INDEX(Calculations!$AB${3}:$AB${13},MATCH($A7+'Asset Inputs'!$E$10-1,Calculations!$A${3}:$A${13},0)),0)
'''
opex_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
capex_tangible_total = \
'''
=IF(A{1} < $E$10, SUMIF('Well Cash Flow'!${6}$7:${6}$117, A{1}, 'Well Cash Flow'!${7}$7:${7}$117) * 'Well Inputs'!${0}$54,'Well Inputs'!${0}$54 * (((('Well Inputs'!${0}$50 + 'Well Inputs'!${0}$51) + ('Well Inputs'!${0}$52/'Well Inputs'!${0}$27)) * SUMIF('Well Cash Flow'!${6}$7:${6}$117,A{1},'Well Cash Flow'!${8}$7:${8}$117)) + ('Well Inputs'!${0}$55 * SUMIF('Well Cash Flow'!${6}$7:${6}$117, A{1}, 'Well Cash Flow'!${18}$7:${18}$117)) + ((('Well Inputs'!${0}$51*'Well Inputs'!${0}$27) + 'Well Inputs'!${0}$52) * SUMIF('Well Cash Flow'!${6}$7:${6}$117, A{1}, 'Well Cash Flow'!${17}$7:${17}$117)))+(IFERROR(SUMIF('Well Cash Flow'!${6}$7:${6}$117,A{1}-'Well Inputs'!${0}$57,'Well Cash Flow'!${8}$7:${8}$117),0) * 'Well Inputs'!${0}$56))))
'''

capex_tangible_total_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
capex_intangible_total = \
'''
=IF(A{1} < $E$10, SUMIF('Well Cash Flow'!${6}$7:${6}$117, A{1}, 'Well Cash Flow'!${7}$7:${7}$117) * 'Well Inputs'!${0}$53,'Well Inputs'!${0}$53 * (((('Well Inputs'!${0}$50 + 'Well Inputs'!${0}$51) + ('Well Inputs'!${0}$52/'Well Inputs'!${0}$27)) * SUMIF('Well Cash Flow'!${6}$7:${6}$117,A{1},'Well Cash Flow'!${8}$7:${8}$117)) + ('Well Inputs'!${0}$55 * SUMIF('Well Cash Flow'!${6}$7:${6}$117, A{1}, 'Well Cash Flow'!${18}$7:${18}$117)) + ((('Well Inputs'!${0}$51*'Well Inputs'!${0}$27) + 'Well Inputs'!${0}$52) * SUMIF('Well Cash Flow'!${6}$7:${6}$117, A{1}, 'Well Cash Flow'!${17}$7:${17}$117)))+(IFERROR(SUMIF('Well Cash Flow'!${6}$7:${6}$117,A{1}-'Well Inputs'!${0}$57,'Well Cash Flow'!${8}$7:${8}$117),0) * 'Well Inputs'!${0}$56))))
'''
capex_intangible_total_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
variable_opex_total = \
'''
=IF(A{1}<$B$10,0,IF(A{1}<$E$10,SUMIF('Well Cash Flow'!${6}$7:${6}$117, A{1}, 'Well Cash Flow'!${14}$7:${14}$117)-R{1}, ((B{1}+D{1}+E{1})*365*'Well Inputs'!${0}$61+(C{1}+F{1})*365*1000*'Well Inputs'!${0}$62+G{1}*365*'Well Inputs'!${0}$63+E{1}*365*'Well Inputs'!${0}$64)+SUMIF('Well Cash Flow'!${6}$7:${6}$117, A{1}, 'Well Cash Flow'!${9}$7:${9}$117)*'Well Inputs'!${0}$65))
'''
variable_opex_total_formulas = []

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
production = \
'''
=IF($A{1}>=$E$10,IF($A{1} > ($E$10 + 'Well Inputs'!${0}$29),0,SUMIF('Well Cash Flow'!${6}$7:${6}$117,$E$10-1,'Well Cash Flow'!{15}$7:{15}$117) * ((1-'Well Inputs'!${0}$21)^($A{1} - ($E$10-1))))+SUMIF('Well Calculations'!$A$9:$A$728,$A{1},'Well Calculations'!{16}$9:{16}$728)/12,SUMIF('Well Cash Flow'!${6}$7:${6}$117,'Asset Inputs'!$A{1},'Well Cash Flow'!{15}$7:{15}$117))
'''

wells_starting = \
'''
=({19}9*{20}9+IF(MOD($B9,12)=1,SUMIF('Well Cash Flow'!${6}$7:${6}$117,$A9,'Well Cash Flow'!${17}$7:${17}$117),0))*'Well Inputs'!${0}$27
'''


cf_cols    = 37
cl_rows    = 113
cl_un_cols = 12
wi_cols    = 6

def sub_refs(formula, show_formula=False):
    formula_list = []
    for i in range(1, 13):
        well_refs = type_well_inputs['well_%s' % i]
        well_refs['wi col']         = XL_COLS[wi_cols * well_refs['well num']]
        well_refs['cf year num']    = XL_COLS[cf_cols * (well_refs['well num'] - 1)]
        well_refs['cf crude']       = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 1]
        well_refs['cf year col']    = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 15]
        well_refs['cf capex']       = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 18]
        well_refs['cf opex']        = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 19]
        well_refs['cf DUCs']        = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 21]
        well_refs['cf hist crude']  = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 22]
        well_refs['cf old wells']   = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 30]
        well_refs['cf new wells']   = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 31]
        well_refs['cf prod wells']  = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 32]
        well_refs['cf abandon']     = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 35]
        well_refs['cl start row']   = 347 + (cl_rows * (well_refs['well num'] - 1))
        well_refs['cl end row']     = well_refs['cl start row'] + 110
        well_refs['cf hist wells']  = XL_COLS[(cf_cols * (well_refs['well num'] - 1)) + 16]
        well_refs['cl wells start'] = XL_COLS[2 + (cl_un_cols * (well_refs['well num'] - 1)) + 2]
        well_refs['cl rig count']   = XL_COLS[2 + (cl_un_cols * (well_refs['well num'] - 1))]
        well_refs['cl wells comp']  = XL_COLS[2 + (cl_un_cols * (well_refs['well num'] - 1)) + 2]
        well_refs['cl crude']       = XL_COLS[2 + (cl_un_cols * (well_refs['well num'] - 1)) + 6]
        well_refs['ai start row']   = 24 + (115*i)
        well_refs['ai end row']     = well_refs['ai start row'] + 110

        params = (
            well_refs[        'wi col'],      # 0
            well_refs[  'ai start row'],      # 1
            well_refs[    'ai end row'],      # 2
            well_refs[  'cl start row'],      # 3
            well_refs[   'cf year num'],      # 4
            well_refs[      'cf crude'],      # 5
            well_refs[   'cf year col'],      # 6
            well_refs[      'cf capex'],      # 7
            well_refs[  'cf new wells'],      # 8
            well_refs[ 'cf prod wells'],      # 9
            well_refs[    'cf abandon'],      # 10
            well_refs[ 'cf hist wells'],      # 11
            well_refs['cl wells start'],      # 12
            well_refs[    'cl end row'],      # 13
            well_refs[       'cf opex'],      # 14
            well_refs[ 'cf hist crude'],      # 15
            well_refs[      'cl crude'],      # 16
            well_refs[       'cf DUCs'],      # 17
            well_refs[  'cf old wells'],      # 18
            well_refs[  'cl rig count'],      # 19
            well_refs[ 'cl wells comp']       # 20
        )
        new_formula = formula.format(*params)
        if show_formula:
            print new_formula
        formula_list.append(new_formula)
    return formula_list


def write_formulas(filepath, formula_template, worksheet, startrow, startcol, row_span, col_span, offset, groups=12, py_lib='openpyxl'):
    formula_list = sub_refs(formula_template)
    if py_lib == 'xlwings':
        xlApp = xw.App(visible=False)
        xlApp.display_alerts = False
        wb = xlApp.books.open(filepath)
        ws = wb.sheets[worksheet]
    else:
        wb = openpyxl.load_workbook(filepath)
        ws = wb.get_sheet_by_name(worksheet)
    output_row = startrow
    for formula in formula_list:
        row_change = row_span + offset
        print formula
        print startcol + str(output_row)
        if py_lib == 'xlwings':
            ws.range(startcol + str(output_row)).raw_value = formula.strip()
        else:
            ws[startcol + str(output_row)].value = formula.strip()
        output_row += row_change
    if py_lib == 'xlwings':
        wb.save()
        wb.close()
        xlApp.quit()
        del xlApp
    else:
        wb.save(filepath)


def print_refs(init_cols, col_span, group_offset, col_count, group_count, worksheet, start_row=1, end_row=1):
    for type_well_num in range(1, group_count+1):
        for comm_num in range(col_count):
            comm_cols = get_cols(init_cols+group_offset+(col_span*(type_well_num-1)), 1, 0, col_count)
        print "Type Well {0} -- {1}{4}{2}:{9}{3} ---> [Crude Oil: {4}, Natural Gas: {5}, Condensate: {6}, NGLs: {7}, LNG: {8}, Water: {9}]".format(type_well_num, worksheet, start_row, end_row, *comm_cols)

def main(filepath=''):
    for formula in ['capex tangible']:
        formula_template = XL_FORMULAS['Asset Inputs'][formula]['template']
        formula_cell = XL_FORMULAS['Asset Inputs'][formula]['cell']
        formula_col = formula_cell[0]
        formula_row = int(formula_cell[1:])
        write_formulas(filepath, formula_template, 'Asset Inputs', formula_row, formula_col, row_span=111, col_span=1, offset=5)


if __name__=='__main__':
    if 1:
        FILEPATH = DATA_DIR + 'US L48 Resource Play [SV].xlsx'
        main(FILEPATH)
