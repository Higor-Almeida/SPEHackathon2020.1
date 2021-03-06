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
2) **EDA.py:** <br>
   a) Python file same code as app.py, but with a thorough inspection on the columns, grouping by values and categories and other EDA methods.
