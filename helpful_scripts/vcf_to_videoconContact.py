import pandas as pd

df = pd.read_csv('/home/nawedx/Downloads/google.csv')
with open("video_contacts.txt", "w+") as text_file:
	for i in range(df.shape[0]):
		print("NAME\n{}\nTEL\n{}\nHOME\n\nCOMPANY NAME\n\nEMAIL\n\nOFFICE NUMBER\n\nFAX NUMBER\n\nBIRTHDAY\n".format(df.Name[i], df.Mobile[i]), file=text_file)