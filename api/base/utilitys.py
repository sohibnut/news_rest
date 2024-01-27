import re

import re
import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

email_regex = r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]{2,7}\b'
username_regex = r'^[a-z0-9_-]{3,15}$'


def check_email(email):
    return re.fullmatch(email_regex, email)

def check_username(username):
    return re.fullmatch(username_regex, username)




class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()

class Email:
    @staticmethod
    def sent_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body = data['body'],
            to = [data['to_email']]
        )        

        if data.get('content_type') == "html":
            email.content_subtype = 'html'

        EmailThread(email).start()    

def sent_email(email, code):
    html_content = render_to_string(
        template_name='auth/sent_email_password.html',
        context={'username' : code}
    )
    Email.sent_email(
        {
            'subject' : 'parolni esdan chiqarish',
            'body' : html_content,
            'to_email' : email,
            'content_type' : 'html'
        }
        
    )