import os
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import schedule

load_dotenv()

class IIISWatcher:
    def __init__(self):
        self.url = "https://iiis.tsinghua.edu.cn/seminars/"
        self.last_content = None
        self.initialize_email_settings()
        
    def initialize_email_settings(self):
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.notification_email = os.getenv('NOTIFICATION_EMAIL')

    def fetch_seminars(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching seminars: {e}")
            return None

    def parse_seminars(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        seminars = []
        # Add parsing logic here
        return seminars

    def send_notification(self, new_seminars):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = self.notification_email
            msg['Subject'] = "New IIIS Seminars Available"
            
            body = "New seminars have been added:\n\n"
            body += "\n".join([str(seminar) for seminar in new_seminars])
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            print("Notification email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")

    def check_for_updates(self):
        current_content = self.fetch_seminars()
        if current_content and current_content != self.last_content:
            new_seminars = self.parse_seminars(current_content)
            if new_seminars:
                self.send_notification(new_seminars)
            self.last_content = current_content

def main():
    watcher = IIISWatcher()
    schedule.every(1).hours.do(watcher.check_for_updates)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()