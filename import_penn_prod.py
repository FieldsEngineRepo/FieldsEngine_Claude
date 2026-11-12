from globaldata import *
import pandas as pd
import os
from sqlalchemy import create_engine


FRAC_FOCUS_DIR = 'D:\\GlobalData\\Data\\wells\\FracFocus\\FracFocusRegistry\\'

def load_production_to_sql():
    total_rows = 0
    dframes = []
    for data_sheet in os.listdir(FRAC_FOCUS_DIR):
        df = pd.read_csv(FRAC_FOCUS_DIR+data_sheet, low_memory=False)
        dframes.append(df)

    prod_data = pd.concat(dframes)
    print prod_data.shape[0], 'rows in table'

    engine = create_engine("mysql://root:OilAndGas321@localhost/globaldata")
    prod_data.to_sql(name='us_frac_focus_registry', con=engine, if_exists="replace", chunksize=10000, index=False)

def load_formation_data():
    formation_data = pd.read_csv(UNCON_DATA_DIR + 'OG_Well_Formations.csv')
    print formation_data.shape[0], 'rows in table'
    engine = create_engine("mysql://root:OilAndGas321@localhost/globaldata")
    formation_data.to_sql(name='wells_pa_formations', con=engine, if_exists="replace", chunksize=10000, index=False)

def csv_to_sql(data_dir, data_file, table_name=None):
    if not table_name:
        table_name = data_file[:-4]
    total_rows = 0
    dframes = []
    df = pd.read_csv(data_dir+data_file, low_memory=False)
    dframes.append(df)

    prod_data = pd.concat(dframes)
    print prod_data.shape[0], 'rows in table'

    engine = create_engine("mysql://root:OilAndGas321@localhost/globaldata")
    prod_data.to_sql(name=table_name, con=engine, if_exists="replace", chunksize=10000, index=False)


if __name__=='__main__':
    load_production_to_sql()
    if 0:
        data_files = os.listdir(FRAC_FOCUS_DIR)
        for data_file in data_files:
            csv_to_sql(FRAC_FOCUS_DIR, data_file, 'us_frac_focus_registry')
    elif 0:
        csv_to_sql(PA_DATA_DIR, 'PA_Completion_Index.csv')