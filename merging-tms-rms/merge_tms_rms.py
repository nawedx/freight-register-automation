import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)
df = pd.read_table('MisOwtdFrgtRgtr.xls', skiprows=2)
df.columns = df.columns.str.replace(' ', '_')
df['RR_NUMBER'] = df['RR_NUMBER'].fillna(0).astype(int)
df['CMDT_CODE'] = df['CMDT_CODE'].fillna(0).astype(int)
df['INVOICE_NO.'] = df['INVOICE_NO.'].fillna(0).astype(int)
#pd.to_numeric(df['RR_NUMBER'], downcast='int32', errors='ignore')
#df.RR_NUMBER - df.RR_NUMBER.astype(int)
print('TMS')
#print(df.head())
#print(df.dtypes)
df2 = pd.read_table('rms.xls', skiprows=2)
df2.columns = df2.columns.str.replace(' ', '_')
print('RMS')
#print(df2.head())
#print(df2.dtypes)
df3 = df.merge(df2, left_on='RR_NUMBER', right_on='RR_NUMB', how='left')
print('MERGED')
#print(df3.head())
df4 = df3[['DVSN', 'STATION_FROM', 'STATION_TO', 'RR_NUMBER', 'RR_DATE_x', 'CMDT', 'CNSR', 'CNSG', 'FRGT(RS)', 'WGHT(Tons)']]
writer = ExcelWriter('merged_tms_rms.xls')
df4.to_excel(writer,'Sheet1')
writer.save()


