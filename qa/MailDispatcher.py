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


def send_mail(send_from, send_to, subject, text, files=[], server="smtp.gmail.com", port = 587):
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
    mailTo = []
    mailTo.append("d.giunchi@scsitaly.com")
    files = []
    files.append("README.txt")
    title= "QA Weekly Report"
    msg = "rapporto che indica stabilita' di governo"
    send_mail("MAFServiceBuild@scsitaly.com", mailTo, title, msg, files)

def usage():
    print "Usage: python MailDispatcher.py [-h] [-l] [-c]"
    print "-h, --help                    show help (this)"
    print 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help",])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            return
        else:
            assert False, "unhandled option"

    param = {}
    run(param)
    
if __name__ == "__main__":
  main()
