import smtplib
from email.message import EmailMessage
import os


class EmailNotifier:
    def __init__(self):
        self.sender_email = 'diyu1015@gmail.com'
        self.sender_password = 'jgvq eppq ftmb vjkk'  # app password

    def send_email_with_attachment(self, to_email, subject, body, attachment_path=None):
        # Create the email message
        msg = EmailMessage()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.set_content(body)

        # Attach an image if the attachment_path is provided and valid
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(attachment_path)
                msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)

        # Connect to the Gmail SMTP server and send the email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.sender_email, self.sender_password)
                smtp.send_message(msg)
            print('Email sent successfully!')
        except Exception as e:
            print(f'Failed to send email: {e}')

