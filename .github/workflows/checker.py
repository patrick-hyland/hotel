import requests
import smtplib
from email.mime.text import MIMEText
import os

URL = "https://www.choicehotels.com/wisconsin/eau-claire/sleep-inn-hotels/wi139?checkInDate=2026-06-19&checkOutDate=2026-06-20"

EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
TO_EMAIL = os.environ["TO_EMAIL"]

def is_sold_out(html):
    return "sold out" in html.lower()

def send_email():
    msg = MIMEText(f"Rooms are available!\n\n{URL}")
    msg["Subject"] = "Hotel Availability Alert 🚨"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    response = requests.get(URL, timeout=15)
    html = response.text

    if not is_sold_out(html):
        print("✅ Availability found!")
        send_email()
    else:
        print("❌ Still sold out")

if __name__ == "__main__":
    main()
