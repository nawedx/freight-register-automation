import pandas as pd
from pandas import ExcelWriter
from operator import itemgetter
numbers=[]
dates=[]
num_date=[]
filename = '22866_PSGN_BKG'
with open(filename+'.TXT','r',encoding="utf8", errors='ignore') as f:
    #contents = f.read()
    #print(contents)
    for line in f:
        kuber = line.split()
        #print(kuber)
        for word in range(len(kuber)):
            #print(kuber[word])
            #numbers.append(word)
            if(len(kuber[word]) == 10 and \
            	(kuber[word][0] == '6' or kuber[word][0] == '7' or kuber[word][0] == '8' or kuber[word][0] == '9') and \
            	(kuber[word-1] == 'E' or kuber[word-1] == 'B' or kuber[word-1] == 'S')):
                #print(kuber[word])
                num_date.append([kuber[word], kuber[word-8]])
            #if len(word) == 10 and (word[0] == '9' or word[0] == '8' or word[0] == '7'):
           	    #print(word)
           	    #numbers.append(word)
            

print(num_date)
print(len(num_date))
unique_data = [list(x) for x in set(tuple(x) for x in num_date)]
unique_data = sorted(unique_data, key = itemgetter(1)) 
print(unique_data)
print(len(unique_data))


df = pd.DataFrame(unique_data, columns =['MOB_NUB', 'BRD_DATE']) 
#df = pd.DataFrame({'MOB_NUM':numbers, 'BRD_DATE':dates})
print (df)

writer = ExcelWriter(filename+'_mobile_numbers.xls')
df.to_excel(writer, 'Sheet1')
writer.save()
