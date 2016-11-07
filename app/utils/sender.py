# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText

from app.settings import EMAIL_SMTP, SITE_TITLE


def send_email(to, subject, text):
    from_addr = EMAIL_SMTP['FROM_NAME']
    # to = 'lombek@gmail.com'
    to_addrs = to if type(to) is list else [to]

    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = subject + ' - ' + SITE_TITLE
    msg['From'] = from_addr

    server = smtplib.SMTP(EMAIL_SMTP['HOST'], EMAIL_SMTP['PORT'])
    server.ehlo()
    server.starttls()
    server.login(EMAIL_SMTP['USERNAME'], EMAIL_SMTP['PASSWORD'])
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()