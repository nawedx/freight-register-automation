import smtplib
import credentials 

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_contacts(filename):
       
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
            
    return names, emails

def main():
    names, emails = get_contacts('mycontacts.txt') # read contacts
    with open('invoice_generated_datewise.txt', 'r', encoding='utf-8') as template_file:
        message = template_file.read()
    

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
        msg['Subject']="Goods Morning Position"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()