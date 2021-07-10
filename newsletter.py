import smtplib, ssl
from string import Template
from email.mime.text import MIMEText

my_address = 'ta9980842@gmail.com'
password = 'Bluetooth@02'

def get_template(filename):
    template_file = open(filename, mode='r', encoding='utf-8')
    template_file_content = template_file.read()
    return Template(template_file_content)

def get_usercontacts(filename):
    names = []
    emails = []
    user_list = open(filename, mode='r', encoding='utf-8')
    for user in user_list:
        names.append(user.split()[0])
        emails.append(user.split()[1])
    return names, emails

names, emails = get_usercontacts('contacts.txt')
message_template = get_template('template.txt')

for i in range(len(names)):
    message_body = message_template.substitute(PERSON_NAME = names[i].title())
    msg = MIMEText(message_body, 'html')
    msg['Subject'] = 'this is a test email'
    msg['From'] = my_address
    msg['To'] = emails[i]

s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
s.login(user = my_address, password = password)                             #check if variable assignment necessary
s.sendmail(my_address, emails, msg.as_string())
s.quit()