import smtplib
import time
import imaplib
import email
import json

with open ('/home/pi/lab/config.json') as json_data_file:
    jdata = json.load(json_data_file)

FROM_EMAIL  = jdata["email"]
FROM_PWD    = jdata["email_password"]
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

bodytext = []

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        #all emails by number, don't need unique ids
        mail_ids = data[0]

        #full list of ids
        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    if msg.is_multipart():
                        for part in msg.get_payload():
                            if part.get_content_type() == "text/plain":
                                bodytext.append(msg['subject'] + ' ' + part.get_payload().encode('UTF-8'))
                    else:
                        bodytext.append(msg['subject']+ ' '+ msg.get_payload().encode('UTF-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    #print 'From : ' + email_from + '\n'
                    #print 'Subject : ' + email_subject + '\n'
                    #print msg

        print len(bodytext)
        print bodytext

    except Exception, e:
        print str(e)

read_email_from_gmail()
