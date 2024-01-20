import smtplib
from email.mime.text import MIMEText
import os

def send_email_via_gmx(subject, body, to_email):
    """
    Sends an email using GMX's SMTP server.

    Parameters:
    subject (str): Subject line of the email.
    body (str): Body of the email.
    to_email (str): Recipient's email address.

    Environment Variables:
    GMX_USER (str): GMX email account username.
    GMX_PASSWORD (str): GMX email account password.
    """

    # Retrieve GMX account credentials from environment variables
    gmx_user = os.environ.get("GMX_USER")
    gmx_password = os.environ.get("GMX_PASSWORD")

    # GMX SMTP server details
    smtp_server = "smtp.gmx.com"
    smtp_port = 587  # Standard port for SMTP, use 465 for SSL

    # Create a MIMEText object for the email
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = gmx_user
    msg["To"] = to_email

    # Establish a connection with the GMX SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Upgrade the connection to secure TLS
        server.login(gmx_user, gmx_password)  # Log in to the GMX SMTP server
        server.send_message(msg)  # Send the email

