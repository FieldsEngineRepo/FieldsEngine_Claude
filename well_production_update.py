from globaldata import *

COL_NAMES = [
    'Gas_Total_mcf', 
    'Gas_Jan_mcf', 
    'Gas_Feb_mcf',
    'Gas_Mar_mcf',
    'Gas_Apr_mcf',
    'Gas_May_mcf',
    'Gas_Jun_mcf',
    'Gas_Jul_mcf',
    'Gas_Aug_mcf',
    'Gas_Sep_mcf',
    'Gas_Oct_mcf',
    'Gas_Nov_mcf',
    'Gas_Dec_mcf',
    'Oil_Total_bbl',
    'Oil_Jan_bbl',
    'Oil_Feb_bbl',
    'Oil_Mar_bbl',
    'Oil_Apr_bbl',
    'Oil_May_bbl',
    'Oil_Jun_bbl',
    'Oil_Jul_bbl',
    'Oil_Aug_bbl',
    'Oil_Sep_bbl',
    'Oil_Oct_bbl',
    'Oil_Nov_bbl',
    'Oil_Dec_bbl',
    'Condensate_Total_bbl',
    'Condensate_Jan_bbl',
    'Condensate_Feb_bbl',
    'Condensate_Mar_bbl',
    'Condensate_Apr_bbl',
    'Condensate_May_bbl',
    'Condensate_Jun_bbl',
    'Condensate_Jul_bbl',
    'Condensate_Aug_bbl',
    'Condensate_Sep_bbl',
    'Condensate_Oct_bbl',
    'Condensate_Nov_bbl',
    'Condensate_Dec_bbl',
    'NGL_Total_bbl',
    'NGL_Jan_bbl',
    'NGL_Feb_bbl',
    'NGL_Mar_bbl',
    'NGL_Apr_bbl',
    'NGL_May_bbl',
    'NGL_Jun_bbl',
    'NGL_Jul_bbl',
    'NGL_Aug_bbl',
    'NGL_Sep_bbl',
    'NGL_Oct_bbl',
    'NGL_Nov_bbl',
    'NGL_Dec_bbl',
    'Water_Total_bbl',
    'Water_Jan_bbl',
    'Water_Feb_bbl',
    'Water_Mar_bbl',
    'Water_Apr_bbl',
    'Water_May_bbl',
    'Water_Jun_bbl',
    'Water_Jul_bbl',
    'Water_Aug_bbl',
    'Water_Sep_bbl',
    'Water_Oct_bbl',
    'Water_Nov_bbl',
    'Water_Dec_bbl'
]

def main():
    conn = get_connection(server='sql_server', database='US_Wells')
    curr = conn.cursor()
    sql_update = "UPDATE tblUSWell_Production_Forecast_Archive SET {0}=b.{0} FROM tblUSWell_Production_Forecast a, tblUSWell_Production_ b WHERE b.[Period]=2019 AND a.API_Number=b.API_Number AND a.[Period]=2019 AND NOT ISNULL(b.{0},0)=0"
    for col_name in COL_NAMES:
        print sql_update.format(col_name)
        curr.execute(sql_update.format(col_name))
        commit(curr)
    curr.close()
    conn.close()

if __name__=='__main__':
    main()