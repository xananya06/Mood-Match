"""
Email Sender
Sends actual emails using Gmail SMTP for demo
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailSender:
    def __init__(self):
        self.from_email = os.getenv("GMAIL_ADDRESS")  # Your Gmail
        self.app_password = os.getenv("GMAIL_APP_PASSWORD")  # Gmail App Password
        
    def send_match_notification(self, to_email: str, subject: str, body: str) -> bool:
        """
        Send email notification using Gmail SMTP
        
        Args:
            to_email: Recipient email
            subject: Email subject
            body: Email body (HTML)
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"BU Mood Match <{self.from_email}>"
            msg['To'] = to_email
            
            # Attach HTML body
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)
            
            # Send via Gmail SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.from_email, self.app_password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
        
        