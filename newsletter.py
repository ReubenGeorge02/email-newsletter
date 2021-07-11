import smtplib
import ssl
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import dotenv_values

config = dotenv_values(".env")

my_address = config["EMAIL"]
password = config["PASSWORD"]


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

p = MIMEBase('application', 'octet-stream')

if ((input("Attach files? (y/n): ")).lower() == "y"):
    attachment = open(
        input("Enter the path of the attachment file: "), mode='rb')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition',
                 "attachment; filename= %s" % attachment)
else:
    attachment = False


for i in range(len(names)):
    message_body = message_template.substitute(PERSON_NAME=names[i].title())
    msg = MIMEMultipart()
    msg.attach(MIMEText(message_body, 'html'))
    msg["Subject"] = "this is a test email"
    msg["From"] = my_address
    msg["To"] = emails[i]
    if(attachment):
        msg.attach(p)
    s.sendmail(my_address, emails[i], msg.as_string())
s.quit()
