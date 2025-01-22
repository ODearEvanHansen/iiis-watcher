import os
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from dotenv import load_dotenv
import schedule
import time

load_dotenv()

def get_seminar_items():
    url = "https://iiis.tsinghua.edu.cn/seminars/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Add logic to parse seminar items
    return []

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = os.getenv('NOTIFICATION_EMAIL')

    with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)

def check_for_updates():
    current_items = get_seminar_items()
    # Add logic to compare with previous items and send email if new items found
    pass

def main():
    schedule.every().hour.do(check_for_updates)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()