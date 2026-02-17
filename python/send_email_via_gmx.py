import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

logger = logging.getLogger("newsletter.email")

def send_email_via_gmx(subject, body, to_email, html=False):
    """
    Sends an email using GMX's SMTP server, with support for plain text or HTML content.

    Parameters:
    subject (str): Subject line of the email.
    body (str): Body of the email, in plain text or HTML.
    to_email (str): Recipient's email address.
    html (bool): If True, the email body is treated as HTML. Otherwise, plain text.

    Environment Variables:
    GMX_USER (str): GMX email account username.
    GMX_PASSWORD (str): GMX email account password.
    """

    gmx_user = os.environ.get("GMX_USER")
    gmx_password = os.environ.get("GMX_PASSWORD")
    smtp_server = "smtp.gmx.com"
    smtp_port = 587  # Use 465 for SSL

    # Create a MIMEMultipart message object for adding both text and HTML content
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmx_user
    msg["To"] = to_email

    # Attach the email body as either plain text or HTML
    if html:
        part = MIMEText(body, "html")
    else:
        part = MIMEText(body, "plain")
    msg.attach(part)

    # Connect to the SMTP server and send the email
    logger.info("Connecting to SMTP server %s:%d...", smtp_server, smtp_port)
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        logger.info("TLS established, logging in as %s...", gmx_user)
        server.login(gmx_user, gmx_password)
        server.send_message(msg)
        logger.info("Email sent to %s", to_email)

# Example usage:
#send_email_via_gmx("Test Subject", "<h1>This is an HTML Email</h1>", "janwinkler91@gmail.com", html=True)

