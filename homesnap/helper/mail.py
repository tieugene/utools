"""Mail helper"""
import logging
from typing import Union
import smtplib
from email.message import EmailMessage
# 3. local


def send_mail(smtp: str, mailfrom: str, creditentials: tuple, mailto: Union[str, list], subj: str, body: str):
    """Mail result.
    :todo: handle exceptions"""
    msg = EmailMessage()
    msg['From'] = mailfrom
    msg['To'] = mailto if isinstance(mailto, str) else ', '.join(mailto)
    msg['Subject'] = subj
    msg.set_content(body)
    # send it
    with smtplib.SMTP_SSL(smtp) as server:
        server.login(creditentials[0], creditentials[1])  # SMTPAuthenticationError
        server.sendmail(mailfrom, mailto, msg.as_string())
        server.quit()
        logging.debug("Mail sent")
