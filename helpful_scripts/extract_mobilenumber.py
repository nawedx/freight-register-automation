import pandas as pd
from pandas import ExcelWriter
numbers=[]
with open('pass.txt','r') as f:
    for line in f:
        for word in line.split():
           if len(word) == 10 and word[0] == '9' or word[0] == '8' or word[0] == '7':
           	print(word)
           	numbers.append(word)

#print(numbers)
numbers = set(numbers)
numbers = list(numbers)
df = pd.DataFrame({'Mobile_Number':numbers})
print (df)

writer = ExcelWriter('extracted_mobile_numbers.xls')
df.to_excel(writer, 'Sheet1')
writer.save()