import smtplib
import ssl
from string import Template
from email.mime.text import MIMEText

sender_mail = open("sender_credentials.txt", mode="r")
sender = sender_mail.read()
my_address = sender.split()[0]
password = sender.split()[1]


def get_template(filename):
    template_file = open(filename, mode="r", encoding="utf-8")
    template_file_content = template_file.read()
    return Template(template_file_content)


def get_usercontacts(filename):
    names = []
    emails = []
    user_list = open(filename, mode="r", encoding="utf-8")
    for user in user_list:
        names.append(user.split()[0])
        emails.append(user.split()[1])
    return names, emails


names, emails = get_usercontacts("contacts.txt")
message_template = get_template("template.txt")

s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
s.login(user=my_address, password=password)

for i in range(len(names)):
    message_body = message_template.substitute(PERSON_NAME=names[i].title())
    msg = MIMEText(message_body, "html")
    msg["Subject"] = "this is a test email"
    msg["From"] = my_address
    msg["To"] = emails[i]
    s.sendmail(my_address, emails[i], msg.as_string())
s.quit()
