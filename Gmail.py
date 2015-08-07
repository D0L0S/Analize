import smtplib, os, re, sys, glob, string, datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import sys

class Email:

        def __init__(self):
                username = "EMAIL_ADDRESS"
                password = "PASSWORD"

        def SendMail(self, User, Email):
                global Attachments
                Attachments = ['Flask/static/img/Charts/png/TopBrowsers-{date}.png'.format(date=str(date.today())), 'Flask/static/img/Charts/png/IEVersions-{date}.png'.format(date=str(date.today())), 'Flask/static/img/Charts/png/AndroidVersions-{date}.png'.format(date=str(date.today()))] #path to an attachment, if you wish
                username = 'EMAIL_ADDRESS'
                password = "PASSWORD"
                fromaddr = username#'Some Guy <someguy@mygoogleapps-or-gmail.com>' #must be a vaild 'from' addy in your GApps account
                toaddr  = Email
                replyto = fromaddr #unless you want a different reply-to
                msgsubject = 'Analize Monthly Email'
                htmlmsgtext = """Hi {user},<br/><br/>
                                        This is the monthly Analize email. Attached are the charts for:<br/>
                                        <b>Top5 Browsers</b><br/>
                                        <b>Internet Explorer versions</b><br/>
                                        <b>Android versions</b><br/>
                                        <br/>
                                        <b>Thanks!</a><br/><br/>""".format(user=User, attach="icon.png")

                #ok, here goes nothing
                try:

                        msgtext = htmlmsgtext.replace('<b>','').replace('</b>','').replace('<br>',"\r").replace('</br>',"\r").replace('<br/>',"\r").replace('</a>','')
                        msgtext = re.sub('<.*?>','',msgtext)

                        #pain the ass mimey stuff
                        msg = MIMEMultipart()
                        msg.preamble = 'This is a multi-part message in MIME format.\n'
                        msg.epilogue = ''

                        body = MIMEMultipart('alternative')
                        body.attach(MIMEText(msgtext))
                        body.attach(MIMEText(htmlmsgtext, 'html'))
                        msg.attach(body)

                        for attachment in Attachments:

                                #if 'attachment' in globals(): #DO WE HAZ ATTACHMENT?
                                f = attachment
                                part = MIMEBase('application', "octet-stream")
                                part.set_payload( open(f,"rb").read() )
                                Encoders.encode_base64(part)
                                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
                                msg.attach(part)

                        msg.add_header('From', fromaddr)
                        msg.add_header('To', toaddr)
                        ##msg.add_header('Cc', ccaddy)    #doesn't work apparently
                        ##msg.add_header('Bcc', bccaddy)  #doesn't work apparently
                        msg.add_header('Subject', msgsubject)
                        msg.add_header('Reply-To', replyto)

                        # The actual email sendy bits
                        server = smtplib.SMTP('smtp.gmail.com:587')
                        server.set_debuglevel(True) #commenting this out, changing to False will make the script give NO output at all upon successful completion
                        server.starttls()
                        server.login(username,password)
                        server.sendmail(msg['From'], [msg['To']], msg.as_string())

                        server.quit()

                except Exception as error:
                        print (" [-] Error   : {err}".format(err=error))

if __name__ == "__main__":
        sys.stdout = Logger("Logs/Email.log")
        sys.stderr = Logger("Logs/EmailError.log")
        Email.SendMail()
