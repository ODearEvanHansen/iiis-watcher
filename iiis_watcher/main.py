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
    
    seminars = []
    for item in soup.select('.seminar-item'):
        title = item.select_one('.title').text.strip()
        date = item.select_one('.date').text.strip()
        speaker = item.select_one('.speaker').text.strip()
        abstract = item.select_one('.abstract').text.strip()
        
        seminars.append({
            'title': title,
            'date': date,
            'speaker': speaker,
            'abstract': abstract
        })
    
    return seminars

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
    # Load previously seen seminars
    seen_seminars = set()
    if os.path.exists('seen_seminars.txt'):
        with open('seen_seminars.txt', 'r') as f:
            seen_seminars = set(f.read().splitlines())
    
    current_items = get_seminar_items()
    new_seminars = []
    
    for seminar in current_items:
        seminar_id = f"{seminar['date']}-{seminar['title']}"
        if seminar_id not in seen_seminars:
            new_seminars.append(seminar)
            seen_seminars.add(seminar_id)
    
    # Save updated seen seminars
    with open('seen_seminars.txt', 'w') as f:
        f.write('\n'.join(seen_seminars))
    
    if new_seminars:
        subject = f"New IIIS Seminars Found ({len(new_seminars)})"
        body = "New seminars:\n\n"
        for seminar in new_seminars:
            body += f"Title: {seminar['title']}\n"
            body += f"Date: {seminar['date']}\n"
            body += f"Speaker: {seminar['speaker']}\n"
            body += f"Abstract: {seminar['abstract']}\n\n"
        
        send_email(subject, body)

def main():
    schedule.every().hour.do(check_for_updates)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()