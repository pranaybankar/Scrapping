# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 16:38:54 2015

@author: plele
"""

import pymssql
import pandas.io.sql as psql
import pandas as pd
import numpy as  np
import pickle

cnxn = pymssql.connect(host='DBPRIVATESQL', user='marketData_reg', password='sync1tup', database='xf') 
cursor = cnxn.cursor()
sql = "SELECT [gvkeyx],CONVERT(VARCHAR(10),[datadate],120),[prccd] FROM [xf].[dbo].[idx_daily] where [gvkeyx]= 000003"

df = psql.read_sql(sql, cnxn)
df.columns=["a","b","c"]
print(list(df.columns.values))
cnxn.close()



cnxn = pymssql.connect(host='DB-TRQA1', user='marketData_reg', password='sync1tup', database='qai')
cursor = cnxn.cursor()
sql = "SELECT [DSIndexCode],CONVERT(VARCHAR(10),[ValueDate],120),[PI_] FROM [qai].[dbo].[DS2IndexData] where [DSIndexCode] = 41620"

df2 = psql.read_sql(sql, cnxn)
df2.columns=["a_2","b","c_2"]
print(list(df2.columns.values))
cnxn.close()

df3=pd.merge(df, df2, on =["b"])
df3["e"]=[0.11]*len(df3["c"])

a=[]
b=[]

for i, row in df3.iterrows():
    a.append(int(np.allclose(row["c"],row["c_2"],rtol=1e-4,atol=0)))
    if (abs(row["c"]-row["c_2"])/abs(row["c"]+row["c_2"]))<1e-4:
        b.append(1)
    else:
        b.append(0)

    
df3["e"]=a
df3["f"]=(abs(df3["c"]-df3["c_2"])/abs(df3["c"]+df3["c_2"]))
df3["g"]=b

df3.columns = ["gvkeyx","dateValue","prccd","DSIndexCode","PI_","Flag","ResultSet","Flag2"]
pickle.dump( df3, open( "SNP500_data_pickle_file.p", "wb" ) )
df3.to_csv("SNP500_data_csv_file.csv")
print(df3)