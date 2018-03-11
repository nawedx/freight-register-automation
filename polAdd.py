import pandas as pd
from pandas import ExcelWriter
import numpy as np
df = pd.read_excel('ftreg1.xlsx')
cmdt = pd.read_excel('comm_code_name.xlsx')
df.insert(1, 'TOTAL_WGT', np.nan, allow_duplicates=False)
df.insert(2, 'GROUP_CMDT', np.nan, allow_duplicates=False)
df.insert(3, 'SUB_CMDT_DETAIL', np.nan, allow_duplicates=False)
row_len = df.shape[0]
print(df['CMDT CODE'].unique())
for x in range(0, row_len):
	if np.isnan(df.iat[x, 14]):
		continue


	df['TOTAL_WGT'][x] = df['WEIGHT CHRG'][x] + df['OTHER CHARGE POL1'][x] + df['OTHER CHARGE POL2'][x]
	try:
		cmdt2 = (cmdt.loc[cmdt['SUB COMMODITY DETAIL CODE'] == int(df.iat[x, 14])])
		#cmdt2 = (cmdt.loc[cmdt['SUB COMMODITY DETAIL CODE'] == 2871235])
		df['GROUP_CMDT'][x] = (cmdt2.iat[0, 0])
		df['SUB_CMDT_DETAIL'][x] = (cmdt2.iat[0, 3])
	except:
		continue
	
writer = ExcelWriter('final_register2.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()