import win32com.client
import pandas as pd

from openpyxl import load_workbook
from openpyxl.workbook.properties import CalcProperties

from globaldata import *

FULL_MODEL_DIR = ENGINE_DIR + 'CreateLightModels\\'
LIGHT_MODEL_DIR = FULL_MODEL_DIR + 'UltraLight\\'

debug=False


def change_calc():
    orig_model = None
    for fiscal_model in [mod for mod in os.listdir(LIGHT_MODEL_DIR) if mod[0] != "~" and mod[-5:] == ".xlsx"]:
        orig_model = load_workbook(LIGHT_MODEL_DIR + fiscal_model)
        calc_mode = CalcProperties(calcMode='autoNoTable', fullCalcOnLoad=False, calcOnSave=False)
        orig_model.save(LIGHT_MODEL_DIR + fiscal_model)
    del orig_model

def copy_format():
    print 'Formatting models ...'
    xlApp = win32com.client.Dispatch("Excel.Application")
    wb = xlApp.Workbooks.Open(Filename=MACRO_DIR + 'ChangeCalcMacro.xlsm')
    xlApp.Application.Run('ChangeCalcMacro.xlsm!Module2.CreateLightModels')
    wb.SaveAs(MACRO_DIR + 'ChangeCalcMacro.xlsm')
    xlApp.Application.Quit()
    del xlApp


def convert_filenames():
    print 'Converting filenames ...'
    models = [mod for mod in os.listdir(LIGHT_MODEL_DIR) if mod[0] != "~" and mod[-5:] == ".xlsx"]
    for model in models:
        print model
        model_orig = model
        model = model.replace("999", " ")
        #model = model[:-13] + " Conventional" + model[-13:]
        os.rename(LIGHT_MODEL_DIR + model_orig, LIGHT_MODEL_DIR + model)

def create_excel_df(workbook=None, worksheet_name=None):
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    col_names = list(alpha) + sorted([x + y for (x, y) in itertools.product(alpha, repeat=2)])
    try:
        ws = workbook[worksheet_name]
    except:
        ws = workbook.get_sheet_by_name(worksheet_name)
    if debug:
        print 'Creating input dataframe for %s ...' % worksheet_name
    df_in = pd.DataFrame(ws.values)
    rows = range(1,df_in.shape[0] + 1)
    cols = col_names[:df_in.shape[1]]
    if debug:
        print 'Creating output dataframe for %s ...' % worksheet_name
        print 'rows:', rows
        print 'cols:', cols
    xldf = pd.DataFrame(ws.values, columns=cols, index=rows)
    del ws
    return xldf

def copy_formulas():
    for fiscal_model in [mod for mod in os.listdir(FULL_MODEL_DIR) if mod[0] != "~" and mod[-5:] == ".xlsx"]:
        print fiscal_model
        worksheets = ['Asset Inputs', 'Asset Sensitivity', 'Fiscal Inputs', 'Asset Summary', 'Cash Flow', 'Calculations']

        if 'resource' in fiscal_model.lower():
            worksheets += ['Type Well Inputs', 'Development Inputs', 'Well Calculations']
        ws_data = {worksheet: {'ws': None, 'array dict': None, 'df': None} for worksheet in worksheets}
        if debug:
            print 'Loading fiscal model ...'
        # Load fiscal model and change calculation mode
        orig_model = load_workbook(FULL_MODEL_DIR + fiscal_model)
        calc_mode = CalcProperties(calcMode='autoNoTable', fullCalcOnLoad=False, calcOnSave=False)
        orig_model.save(FULL_MODEL_DIR + fiscal_model)
        if debug:
            print 'Storing formula arrays for each worksheet ...'
        # Store formula arrays for each worksheet in dictionary
        for ws_name in ws_data.keys():
            try:
                ws_data[ws_name]['ws'] = orig_model[ws_name]
            except:
                ws_data[ws_name]['ws'] = orig_model.get_sheet_by_name(ws_name)
            ws_data[ws_name]['array dict'] = ws_data[ws_name]['ws'].formula_attributes
        if debug:
            print 'Reassigning IRR reference away from data table ...'
        # Reassign IRR reference away from data table
        ws_data['Asset Sensitivity']['ws']['D49'].value = '=B33'
        formula = "=(C21+SUMPRODUCT(--(Calculations!A8:A118 >= 'Asset Inputs'!B$9), Calculations!Y8:Y118, 1/(1+'Asset Inputs'!$E$11)^(Calculations!A8:A118 - 'Asset Inputs'!B$9))) / "
        formula += "SUMPRODUCT(--(Calculations!A8:A118 >= 'Asset Inputs'!B$9), Calculations!Y8:Y118, 1 / (1 + 'Asset Inputs'!$E$11) ^ (Calculations!A8:A118 - 'Asset Inputs'!B$9))"
        ws_data['Asset Summary']['ws']['C24'].value = formula

        if debug:
            print 'Creating dataframes to store fiscal model data and formulas ...'
        # Create dataframes to store fiscal model data and formulas
        for ws_name in ws_data.keys():
            ws_data[ws_name]['df'] = create_excel_df(workbook=orig_model, worksheet_name=ws_name)

        if debug:
            print 'Using dataframes to create light models ...'
            __=raw_input('model names correct?')
        # Use dataframes to create light fiscal models
        alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        col_names = list(alpha) + sorted([x + y for (x, y) in itertools.product(alpha, repeat=2)])
        new_wb = load_workbook(LIGHT_MODEL_DIR + fiscal_model)
        for ws_name in worksheets:
            print 'worksheet: ', ws_name
            df = ws_data[ws_name]['df']
            try:
                ws = new_wb[ws_name]
            except:
                ws = new_wb.get_sheet_by_name(ws_name)

            orig_ws_name = ws_name

            try:
                ws1 = orig_model[orig_ws_name]
            except:
                ws1 = orig_model.get_sheet_by_name(orig_ws_name)
            row_max = min(df.shape[0] + 1, 5000)
            for i in range(1, row_max):
                for j in range(df.shape[1]):
                    if debug:
                        print 'row %s col %s' % (i, j)
                    ws[col_names[j] + str(i)].value = ws1[col_names[j] + str(i)].value
        del orig_model
        if debug:
            print 'Loading new model to correct array formulas ...'
        # Load new model to correct arrary formulas
        for ws_name in ws_data.keys():
            try:
                new_ws = new_wb[ws_name]
            except:
                new_ws = new_wb.get_sheet_by_name(ws_name)
            for cell in ws_data[ws_name]['array dict'].keys():
                new_ws.formula_attributes[cell] = ws_data[ws_name]['array dict'][cell]
        new_wb.save(LIGHT_MODEL_DIR + fiscal_model)
        del new_wb

def create_models(calc=False, format=False, filenames=False, formulas=False):
    if calc:
        change_calc()
    if format:
        copy_format()
    if filenames:
        convert_filenames()
    if formulas:
        copy_formulas()


if __name__ == '__main__':
    create_models(calc=True, format=True, filenames=True, formulas=True)
