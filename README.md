# SPEHackathon2020.1

## Team Composition
Higor Esmeraldo and Marco Gemaque - Niterói, Rio de Janeiro, Brasil - Universidade Federal Fluminense

## Methodology
This is a Dash App which runs on Flask, hosted on PythonAnywhere and uses SQL as reference. <br>
Files inside are as description: <br>
1) **app.py:** <br>
   a) Processes a raw excel file and returns a valid dataframe which can be used for calculation, containing production values and removed typos. <br>
   b) Main function which takes user's inputs and returns the solution dataframe. The following logic applies to it: <br>
      b.1) User inputs what main information he wants: department, contract, operator, etc. All categories, no numbers. --> **Base Block**<br>
      b.2) User inputs specific base block information: which departments, which operators, which contracts, etc. --> **Special Block** <br>
      b.3) User inputs time specifics. Which year he wants, which trimester, which month, etc. --> **Time Block** <br>
2) **spyder.py:** <br>
   a) Python file same code as app.py, but with a thorough inspection on the columns, grouping by values and categories and other EDA methods.
      
## Input format
Here is a description of the **solution()** method which answers the Hackaton's Questions. <br>
1) **def solution(df, modes="")**: <br>
   df --> Processed dataframe. This is automatically ran when the code is executed. <br>
   modes --> String separated by a comma, **no blanks space**. <br>
      *Example of modes:* 'all', 'Contract,Municipio' or 'Operadora' or any other **categorical column, non-numeric* <br>
2) **def base_block(solution, modes="")**: <br>
   solution --> Output from the **solution()** method. <br>
   *This function will ask for the following intern variables: <br>
      2.a) if 'all' in **solution()** method:
         --> **Special Category**: Which of all the macro-categories do you want to filter by? <br>
         --> **Supra Category**: Which specific field from the special category do you want to choose? <br>
         *Example:* if **special category** is **Departamento**, then you could choose as supra: **ANTIOQUIA,ARAUCO,ATLANTICO** or any other. 'all' is also a possibility.<br>
3) **def time_block(base_block):**: <br>
      base_block --> Automatic input from **base_block** method.
      *This function will ask for the following intern variables*: <br>
         3.a) if 'all' in **time_block()** then will filter every year.
              if specific year (2020, 2019, 2018) then will filter that year.
              if years, **separated by comma and no blankspace** such as: '2019,2020' or '2018,2020' or any other.
