from django.core.mail.backends.base import BaseEmailBackend

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SendGridEmailpipBackEnd(BaseEmailBackend):
    def send_messages(self, email_messages):
        for email_message in email_messages:
            sendgrid_mail = Mail(
                from_email = 'kumo@GraduateTrackingSystem.com',
                to_emails = email_message.to,
                subject = email_message.subject,
                html_content = email_message.body)
            try:
                sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sendgrid_client.send(sendgrid_mail)
                ''' For Debug
                print(response.status_code)
                print(response.body)
                print(response.headers)
                '''
            except Exception as e:
                raise e