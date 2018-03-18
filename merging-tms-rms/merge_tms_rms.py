import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)
df = pd.read_table('tms.xls', skiprows=2)
df.columns = df.columns.str.replace(' ', '_')
df['RR_NUMBER'] = df['RR_NUMBER'].fillna(0).astype(int)
df['CMDT_CODE'] = df['CMDT_CODE'].fillna(0).astype(int)
df['INVOICE_NO.'] = df['INVOICE_NO.'].fillna(0).astype(int)
df = df[df.RR_NUMBER !=0 ]
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
df3 = df.merge(df2, left_on=['RR_NUMBER', 'RR_DATE'], right_on=['RR_NUMB', 'RR_DATE'], how='left')
print('MERGED')
#print(df3.head())

df3 = df3[['DVSN', 'STATION_FROM', 'STATION_TO', 'RR_NUMBER', 'RR_DATE', 'CMDT', 'CNSR', 'CNSG', 'RK_PM', 'UNTS', '8W', 'INVC_NUMB', 'INVC_DATE', 'DEMAND_NUMB', 'DEMAND_DATE', 'FRGT(RS)', 'WGHT(Tons)', 'RR_E-RR', 'TRFC_TYPE_x', 'PAID_TYPE', 'F/L/I_FLAG', 'INVOICE_NO.', 'INVOICE_DATE', 'CMDT_CODE', '8-WHLR', 'PYMT_MODE', 'DISTANCE_CHRG', 'WEIGHT_CHRG', 'WEIGHT_ACTL', 'CHBL_CLASS', 'RATE_/T', 'BASIC_FRGT', 'OTHER_CHARGE_POL1', 'OTHER_CHARGE_POL2', 'OTHER_CHARGE_DS', 'OTHER_CHARGE_SD', 'OTHER_CHARGE_FAUC', 'OTHER_CHARGE_DPO', 'OTHER_CHARGE_ENHC', 'OTHER_CHARGE_DPCM', 'OTHER_CHARGE_RR', 'OTHER_CHARGE_TOTAL', 'REBATE_GR', 'REBATE_GR2', 'REBATE_GR1', 'REBATE_TOTAL', 'TOTAL_FRGT', 'SRVC_TAX_DETAILS_SRVC_TAX', 'SRVC_TAX_DETAILS_ECESS', 'SRVC_TAX_DETAILS_HECESS', 'SRVC_TAX_DETAILS_SBCESS', 'SRVC_TAX_DETAILS_KKCESS', 'SRVC_TAX_DETAILS_T.SRVC_TAX', 'GST_DETAILS_IGST', 'GST_DETAILS_CGST', 'GST_DETAILS_SGST', 'GST_DETAILS_UTGST', 'GST_DETAILS_TOTL_GST', 'FINAL_FRGT_(incl.SrvcTax/GST)', 'EPAYMENT_ID', 'LDNG_STTN', 'LDNG_DATE']]
writer = ExcelWriter('merged_tms_rms.xls')
df3.to_excel(writer,'Sheet1')
writer.save()


