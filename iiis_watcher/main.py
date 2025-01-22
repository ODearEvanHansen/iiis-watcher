import os
import smtplib
import requests
import json
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
    
    seminar_items = []
    for item in soup.select('.seminar-item'):
        title = item.select_one('.seminar-title').text.strip()
        date = item.select_one('.seminar-date').text.strip()
        speaker = item.select_one('.seminar-speaker').text.strip()
        seminar_items.append({
            'title': title,
            'date': date,
            'speaker': speaker
        })
    
    return seminar_items

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
    previous_items = load_previous_items()
    
    new_items = []
    for item in current_items:
        if item not in previous_items:
            new_items.append(item)
    
    if new_items:
        subject = "New Seminar Updates"
        body = "New seminars found:\n\n"
        for item in new_items:
            body += f"Title: {item['title']}\nDate: {item['date']}\nSpeaker: {item['speaker']}\n\n"
        send_email(subject, body)
        save_previous_items(current_items)

def load_previous_items():
    try:
        with open('previous_items.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_previous_items(items):
    with open('previous_items.json', 'w') as file:
        json.dump(items, file)

def main():
    schedule.every().hour.do(check_for_updates)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()