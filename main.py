import imaplib, email, re
import getpass
import quickstart

f = open("Username.txt", "r")
line = f.readlines()
if len(line) == 0:
    f.close()
    f = open("Username.txt", "w")
    user = input("Gmail address: ")
    password = getpass.getpass()
    f.write(user)
else:
    print("Auto login! If you want to change username, you can delete the text in the 'Username.txt' file")
    print("NOTE: Do not delete the file!")
    user = line[0]
    password = getpass.getpass()

f.close()
imapserver = 'imap.gmail.com'

imap = imaplib.IMAP4_SSL(imapserver)
imap.login(user, password)
# If failed then you need to change your setting here: https://myaccount.google.com/lesssecureapps
imap.select('INBOX')

# resultid, dataid = imap.uid('search', None, 'ALL')
resultid, dataid = imap.search(None, 'Subject', '"library checkout receipt"')
mailid = dataid[0].split()
mailList = []
events = []

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

def find_due_date(msg):
    # title = re.findall('Title: [0-9]*/[0-9]*/[0-9]*,[0-9]*:[0-9]*', msg)
    due = re.findall('Due Date: [0-9]*/[0-9]*/[0-9]*,[0-9]*:[0-9]*', msg)
    return((due[0].split()[-1]).split(','))

for id in mailid:
    result, data = imap.fetch(id, '(RFC822)')
    message = email.message_from_bytes(data[0][1])
    mailList.append(get_body(message).decode("utf-8"))

for m in mailList:
    events.append(find_due_date(m))

quickstart.addevent(events)
imap.logout()
input("All Done! Press 'Enter' to quit!")