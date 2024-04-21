import os
import re
from typing import Union

# import resend
# resend.api_key = os.environ["RESENDAPIKEY"]
from django.forms import EmailField

from account.models import User



def send_email(html_email, to_email: User.email, subject: str, email_from: str):
    params = {
        "from": email_from,
        "to": [to_email],
        "subject": subject,
        "html": html_email,
    }
    return resend.Emails.send(params)
