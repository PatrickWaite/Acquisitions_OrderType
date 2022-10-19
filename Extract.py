#imports 
import os
import sys
from datetime import datetime
from dbConnect import get_connectionString
from queries import get_OrderInvoiceQuery, helloworld
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from collections import Counter
import tkinter as tk
from tkinter import filedialog
import re

def callQuery(query):
    try:
        # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
        engine = create_engine(
            url=get_connectionString()) #pull connection string from dbConnect.py so that connection isn't hard coded in main file
        print(
            f"Connection created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)

#create connection and execute query from quries.py
    with engine.connect() as conn: 
            #Note call the text() from sqlachemy to turn the text string result from get_inventoryQuery() into
            #an executable SQL
        df_queryOutput = pd.DataFrame(conn.execute(text(query)))
        #print(df_queryOutput.keys())
    return df_queryOutput
        


#be aware of 'mark for delete record', surpression flag in item and holdings.  "discovery_suppress"(may need to look more into this) "item status"(only on item record) 

def SendFileOutput(dataframe,month,year):
     #check to see if output path exists
    outputDir = './outputAccquistions' #define output folder, should it not exist it will be created 
    isExist = os.path.exists(outputDir)
    print(isExist)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(outputDir)
        print("The new directory is created!")
#save dataframe outputs to output directory with a date
    date = datetime.now()
    dt = date.strftime("%d%m%Y")
    dataframe.to_csv(f'{outputDir}/ByOrderType_expt_{month}{year}_{dt}.csv', index=False)
    dataframe.to_excel(f'{outputDir}/ByOrderType_expt_{month}{year}_{dt}.xlsx', index=False) 

    


def main():
    #Assing global varables 
    #month an year variables are submitted though the bat file runner
    month = sys.argv[1] #07
    year = sys.argv[2] #"2022"
    query = get_OrderInvoiceQuery(year,month)
    
    #call query though the callQuery fucntion this allows you to easily change out the query that is being run or
    #run multiple times 
    x = callQuery(query)
    #

    #send dataframe out to output file 
    SendFileOutput(x,month,year)
    #store output files in "R(coll_managment (\\libr-file1.library.umass.edu))):\Acquisitions\FOLIO Reports" folders

    

if __name__ == '__main__':
    main()
    