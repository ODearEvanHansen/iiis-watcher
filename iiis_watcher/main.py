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
        seminar = {
            'title': item.select_one('.title').text.strip(),
            'date': item.select_one('.date').text.strip(),
            'speaker': item.select_one('.speaker').text.strip(),
            'abstract': item.select_one('.abstract').text.strip()
        }
        seminars.append(seminar)
    
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
    # Get current seminars
    current_items = get_seminar_items()
    
    # Read previously seen seminars
    try:
        with open('seen_seminars.txt', 'r') as f:
            seen_items = set(f.read().splitlines())
    except FileNotFoundError:
        seen_items = set()

    # Find new seminars
    new_items = []
    for item in current_items:
        item_id = f"{item['date']}-{item['title']}"
        if item_id not in seen_items:
            new_items.append(item)
            seen_items.add(item_id)

    # If there are new seminars, send email and update seen file
    if new_items:
        # Prepare email content
        subject = f"New IIIS Seminars Found ({len(new_items)})"
        body = "New seminars:\n\n"
        for item in new_items:
            body += f"Title: {item['title']}\n"
            body += f"Date: {item['date']}\n"
            body += f"Speaker: {item['speaker']}\n"
            body += f"Abstract: {item['abstract']}\n\n"
        
        send_email(subject, body)
        
        # Update seen seminars file
        with open('seen_seminars.txt', 'w') as f:
            f.write('\n'.join(seen_items))

def main():
    schedule.every().hour.do(check_for_updates)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()