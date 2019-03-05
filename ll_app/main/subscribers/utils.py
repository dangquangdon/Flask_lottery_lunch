import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import current_app
from datetime import datetime

def send_email_now(pair):
    port = current_app.config.get('MAIL_PORT')
    sender_email = current_app.config.get('SENDER_EMAIL')
    sender_password = current_app.config.get('SENDER_PASSWORD')
    smtp_server = current_app.config.get('SMTP_SERVER')

    message = MIMEMultipart('alternative')
    message['Subject'] = "The Shortcut Lottery Lunch"
    for each in pair:
        receiver_email = each.email
        message["From"] = sender_email
        message["To"] = receiver_email
        text = f"""\
        <html>
            <body>
                <p>Hi {pair[0].first_name} and {pair[1].first_name},</p>
                <p>
                It is {datetime.utcnow().strftime('%B')} and friends day is coming up! What a great occasion to meet old and new friends :) The two of you have been paired for #LotteryLunch this month.</p>
                <p>Have fun meeting up for lunch, breakfast, a cup of coffee, or maybe hot cocoa! And, if you aren't in the same place this month, no worries, schedule a Lottery Skype!</p>
                <p>When you do meet, take a selfie during the meeting, which you can post along with a brief story about your meetup to <a href="https://www.facebook.com/groups/theshortcut.org/" target="_blank"> The Shortcut Community Group on Facebook </a>, using the hashtags #lottery lunch and #theshortcut.</p>
                <p>Check out our <a href="https://www.facebook.com/pg/theshortcut/events/" target="_blank">upcoming events </a> for this month and join us for example for one of our <a href="https://www.facebook.com/events/1884339015211390/" target="_blank"> Friday Lunch Mingles </a>. Hope to see you there and if you want to stay informed about what else is happening this winter get our <a href="https://theshortcut.us12.list-manage.com/subscribe?u=4dd5200f27d975e60d3f59cd1&id=1686534547" target="_blank"> newsletter</a>!</p>
                <p>P.S. If you don't hear from your pair this month, or you no longer wish to participate, just let me know!</p>
                <p>Have a great weekend!</p>
            </body>
        </html>
        """
        part1 = MIMEText(text, "html")

        message.attach(part1)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

