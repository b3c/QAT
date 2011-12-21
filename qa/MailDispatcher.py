import smtplib
import sys
import os
import getopt
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

#try:
#    from qa import mafPath
#except ImportError:
#    import mafPath


def send_mail(send_from, send_to, subject, text, files=[], server="localhost", port = 587):
  assert type(send_to)==list
  assert type(files)==list

  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = COMMASPACE.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject

  msg.attach( MIMEText(text) )

  for f in files:
    print f
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(f,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)

  smtpserver = smtplib.SMTP(server, port)
  smtpserver.ehlo()
  smtpserver.starttls()
  smtpserver.ehlo
  user = "" #insert value
  pwd = "" #insert value
  smtpserver.login(user, pwd)
  smtpserver.sendmail(send_from, send_to, msg.as_string())
  smtpserver.close()
  
def run(param):
    mailFrom = param["from"]
    mailTo = param["to"].split(",")
    files = param["attachments"].split(",")
    title= param["subject"]
    msg = param["message"]
    send_mail(mailFrom, mailTo, title, msg, files)

def usage():
    print "Usage: python MailDispatcher.py [-h] [-f] [-t] [-s] [-m] [-a]"
    print "-h, --help                    show help (this)"
    print "-f, --from=                   address from"
    print "-t, --to=                     address to, comma separated value without spaces"
    print "-s, --subject=                mail subject"
    print "-m, --message=                mail message"
    print "-a, --attachments=            mail attachments, comma separated value without spaces"
    print 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:t:s:m:a:", ["help","from","to","subject","message","attachments"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    param = {}    
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            return
        elif o in ("-f", "--from"):
            param["from"] = a
        elif o in ("-t", "--to"):
            param["to"] = a
        elif o in ("-s", "--subject"):
            param["subject"] = a
        elif o in ("-m", "--message"):
            param["message"] = a
        elif o in ("-a", "--attachments"):
            param["attachments"] = a
        
    run(param)
    
if __name__ == "__main__":
  main()
