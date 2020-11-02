import pandas as pd #requirement for dataframes
import pathlib #requirement to find working directory

#oil production in bpd
#gas in Mscfd

path = str(pathlib.Path().absolute()) + "\\files\\colombia_consolidado.xlsx" #get the working directory and find the raw file
df_real = pd.read_excel(path,thousands=',')  #create a df with pandas

def process_file(entry_df):
    #Function to create processed file with production by trimester, total, year and fluid. Also correct typos
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

    entry_df['Operadora'] = entry_df['Operadora'].replace(comp_mapper)
    outside_path = str(pathlib.Path().absolute()) + "\\files\\"
    print("File was created.")
    entry_df.to_excel(str(outside_path)+"processado.xlsx")
    return entry_df

df = process_file(df_real) #create our new processed file