import pandas as pd
import numpy as np
from pandas import ExcelWriter
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

df1 = pd.read_excel('a_list.xlsx')
#print(len(set(df1.FNOT_NUMB)))
df2 = pd.read_excel('b_list.xlsx')
#df = df1.merge(df2, )
common = pd.merge(df1, df2, on=['FNOT_NUMB','FNOT_DATE'])
#print(common)
df3 = df1[(~df1.FNOT_NUMB.isin(common.FNOT_NUMB))&(~df1.FNOT_DATE.isin(common.FNOT_DATE))]
print(df3)

writer = ExcelWriter('out.xlsx')
df3.to_excel(writer, 'Sheet1')
writer.save()
