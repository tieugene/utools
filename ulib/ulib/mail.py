"""Mail ulib"""
import logging
from typing import Union, Optional, List, Tuple
import smtplib
from email.message import EmailMessage
# 3. local


def send_mail(smtp: str, mailfrom: str, creditentials: Tuple[str], mailto: Union[str, List[str]], subj: str,
              body: Optional[str] = None):
    """Mail result.
    :todo: handle exceptions"""
    msg = EmailMessage()
    msg['From'] = mailfrom
    msg['To'] = mailto if isinstance(mailto, str) else ', '.join(mailto)
    msg['Subject'] = subj
    if body:
        msg.set_content(body)
    # send it
    with smtplib.SMTP_SSL(smtp) as server:
        server.login(creditentials[0], creditentials[1])  # SMTPAuthenticationError
        server.sendmail(mailfrom, mailto, msg.as_string())
        server.quit()
        logging.debug("Mail sent")
