import pandas as pd

from openpyxl import load_workbook
from openpyxl.workbook.properties import CalcProperties

from globaldata import *

MODEL_DIR = DATA_DIR + 'change_calc\\'

def change_calc():
    for fiscal_model in [mod for mod in os.listdir(LIGHT_MODEL_DIR) if mod[0] != "~" and mod[-5:] == ".xlsx"]:
        orig_model = load_workbook(LIGHT_MODEL_DIR + fiscal_model)
        calc_mode = CalcProperties(calcMode='autoNoTable', fullCalcOnLoad=False, calcOnSave=False)
        orig_model.save(LIGHT_MODEL_DIR + fiscal_model)
        orig_model.close()
    del orig_model

if __name__ == '__main__':
    change_calc()
