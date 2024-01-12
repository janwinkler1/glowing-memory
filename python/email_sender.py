import smtplib
from email.mime.text import MIMEText
import os

def send_email_via_gmx(subject, body, to_email):
    gmx_user = os.environ.get('GMX_USER')
    gmx_password = os.environ.get('GMX_PASSWORD')
    smtp_server = "smtp.gmx.com"
    smtp_port = 587  # Use 465 for SSL

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = gmx_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(gmx_user, gmx_password)
        server.send_message(msg)
