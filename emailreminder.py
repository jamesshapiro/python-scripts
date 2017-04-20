import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#Note: I found this helpful: http://naelshiab.com/tutorial-send-email-python/
def emailReminder(reminder):
    #[redacted, but it's a gmail account I set up just to send
    # myself email remainders]
    fromaddr = "[redacted-1]@gmail.com"
    # My e-mail address
    toaddr = "[redacted-2]@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = reminder

    body = "Friendly reminder of the following: " + reminder
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("[redacted-1].com", "remindme")
    text = msg.as_string()
    server.sendmail("[redacted-1]@gmail.com", "[redacted-2]", text)
