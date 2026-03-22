import os
import smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright

URL = "https://www.choicehotels.com/wisconsin/eau-claire/sleep-inn-hotels/wi139?checkInDate=2026-06-19&checkOutDate=2026-06-20"

EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
TO_EMAIL = os.environ["TO_EMAIL"]


def is_sold_out(page_content: str) -> bool:
    return "sold out" in page_content.lower()


def send_email():
    msg = MIMEText(preview)
    msg["Subject"] = "Hotel Availability Alert"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


def fetch_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        page.goto(URL, wait_until="networkidle", timeout=60000)
        content = page.content()

        browser.close()
        return content


def main():
    html = fetch_page()

    preview = html.lower()[:20000]
    print(preview)

    if not is_sold_out(html):
        print("✅ Availability found!")
        send_email()
    else:
        print("❌ Still sold out")


if __name__ == "__main__":
    main()