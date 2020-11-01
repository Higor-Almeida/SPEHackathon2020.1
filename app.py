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

print(df.head())

#demo = solution(df, modes="all")

def solution(df_entry, modes=""):
    #Our main function that operates everything
    base, super_list = base_block(df_entry, modes)
    special = special_block(base,super_list)
    time = time_block(special)
    return time

def base_block(x,modes="all"):
    #Initial function to filter user's preferences and create standard dataframe
    """
    base blocks are contracts, fields, operators, etc. Everything else
    except production and time-related columns.
    """
    if 'all' in modes:
        df_out = x
        in_list = [modes]
        return df_out, in_list
    else:
        in_list = modes.split(',') #The macro-categories our user wants to see
        std_cols = ['Enero','Febrero','Marzo','Abril','Mayo',
                    'Junio','Julio','Agosto','Septiembre','Octubre',
                    'Noviembre','Diciembre','Year','trimestre_1','trimestre_2',
                    'trimestre_3','trimestre_4','prod_anual','Fluido'] #Add this to keep production
        in_list.extend(std_cols) #add above columns to user's selections
        df_out = x[x.columns & in_list]
        return df_out, in_list

def special_block(x,in_list):
    #Function to select special cases of our groups
    """
    Special blocks are specific operators, contracts, fields, etc.
    """
    if 'all' in in_list:
        special_ops = input("Which special cases do you want? ") #Selected supra-categories if all cols selected
        special_ops = special_ops.split(',')
        if 'all' in special_ops:
            return x
        else:
            supra_ops = []
            df_int = x
            for ops in special_ops: #The macro-category from all the chosen ones
                special_category = input("Which {}s do you want?".format(ops))
                special_category = special_category.split(',')
                supra_ops.append(special_category)
                df_int = df_int[df_int[str(ops)].isin(supra_ops[special_ops.index(ops)])]
                df_out = df_int
            return df_out
    else:
        supra_list = []
        for supra in in_list[:-19]:
            options = input("Which {} do you want? ".format(supra))
            split_option = options.split(',')
            int_list= []
            for split in split_option:
                if split != "":
                    int_list.append(split)
                else:
                    pass
            supra_list.append(int_list)
        df_out = pd.DataFrame(columns=in_list)
        df_int = x
        for supper in in_list[:-19]: #We will filter the macro-categories
            df_demo = df_int[df_int[str(supper)].isin(supra_list[in_list.index(supper)])]
            if df_demo.empty == True:
                pass
            else:
                df_int = df_int[df_int[str(supper)].isin(supra_list[in_list.index(supper)])]
                df_out = df_int
        return df_out

def time_block(x):
    #Function to select the time period the user wants the information
    """
    Choose years (whole) of trimestre or specific months of years.
    """
    years = input("Which years do you want? ")
    years = years.split(',')
    for year in years:
        if year == "": #remove "" from the list in case user makes mistake
            years.pop(year)
    if not years: #check if list is empty to create standard query
        years = [2020] #Standard query year
        df_out = x[x['Year'].isin(years)]
        return df_out
    if "all" in years:
        return x
    else:
        df_out = x[x['Year'].isin(years)]
        df_out.info()
        return df_out
