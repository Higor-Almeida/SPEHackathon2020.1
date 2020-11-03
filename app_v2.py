import pandas as pd #requirement for dataframes
import pathlib #requirement to find working directory
import sqlite3

import sqlalchemy 
from sqlalchemy import create_engine

#oil production in bpd
#gas in Mscfd

path = str(pathlib.Path().absolute()) + "\\files\\colombia_consolidado.xlsx" #get the working directory and find the raw file
df_real = pd.read_excel(path,thousands=',')  #create a df with pandas

def process_file(entry_df):
    #Function to create processed file with production by trimester, total, year and fluid. Also correct typos
    """
    This parts reads the excel, creates new columns and maps wrong variable names
    """
    z = 1
    entry_df['prod_anual'] = entry_df.iloc[:,5:17].sum(axis=1)
    for i in range(5,17,3):
        entry_df[str('trimestre_')+str(z)] = entry_df.iloc[:,i:(i+3)].sum(axis=1)
        z += 1

    comp_mapper = {"AMERISUR EXPLORACION COLOMBIA LTD.":"AMERISUR EXPLORACION COLOMBIA LTD",
              "CNE OIL & GAS S.A.S":"CNE OIL & GAS S A S",
              "CNE OIL & GAS S.A.S.":"CNE OIL & GAS S A S",
              "COLOMBIA ENERGY DEVELOPMENT CO ":"COLOMBIA ENERGY DEVELOPMENT CO",
              "TPL COLOMBIA LTD - SUCURSAL COLOMBIA ANTES PANATLANTIC COLOMBIA LTD SUCURSAL EN COLOMBIA":"TPL COLOMBIA LTD - SUCURSAL COLOMBIA"}

    entry_df['Operadora'] = entry_df['Operadora'].replace(comp_mapper) #replaces typos
    outside_path = str(pathlib.Path().absolute()) + "\\files\\" #Get a folder named "files/" where files should be at
    entry_df.to_csv(str(outside_path)+"processado.csv") #Saves a .csv file from the read df
    print("CSV file was created.")

    #SQLite3 part
    conn = sqlite3.connect('hackaton.db') #connect to db
    c = conn.cursor()
    #Create the table with headers
    c.execute('''CREATE TABLE HackatonDB
    ([id] INTEGER PRIMARY KEY,
    [Departamento] text,
    [Municipio] text,
    [Operadora] text,
    [Contrato] text,
    [Campo] text,
    [Enero] real, [Febrero] real, [Marzo] real, [Abril] real,
    [Mayo] real, [Junio] real, [Julio] real, [Agosto] real,
    [Septiembre] real, [Octubre] real, [Noviembre] real,
    [Diciembre] real,
    [Year] int, [Fluido] text, [prod_anual] real,
    [trimestre_1] real, [trimestre_2] real,
    [trimestre_3] real, [trimestre_4] real)''')
    
    conn.commit() #Commit to changes

    #Convert CSV to SQL
    df_csv = pd.read_csv(str(outside_path)+"processado.csv")
    df_csv.index.name = 'id'
    df_csv = df_csv.drop(labels='Unnamed: 0',axis=1)
    df_csv.to_sql('hackaton', conn, if_exists="append",index=True)
    print('SQL file was created')

    return entry_df

df = process_file(df_real) #create our new processed file