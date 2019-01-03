import smtplib, sys
import credentials 
from datetime import date, timedelta
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

currDate = (str(date.today().day)+'-'+str(date.today().month)+'-'+str(date.today().year))

def getContacts(filename):
       
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            conlist = a_contact.split(',')
            #print(conlist)
            names.append(conlist[0])
            emails.append(conlist[1])
            
    return names, emails

def sendMail():
    names, emails = getContacts('mycontacts2.txt') # read contacts
    with open('invoice_generated_datewise.txt', 'r', encoding='utf-8') as template_file:
        message = template_file.read()
        print(message)
    

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.office365.com', port=587)
    s.ehlo()
    s.starttls()
    s.login(credentials.MY_ADDRESS, credentials.PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        print(name, email)
        msg = MIMEMultipart()       # create a message

        # Prints out the message body for our sake
        #print(message)

        # setup the parameters of the message
        msg['From']=credentials.MY_ADDRESS
        msg['To']=email
        msg['Subject']="Goods Morning Position - " + currDate
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

sendMail()    