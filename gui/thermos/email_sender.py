import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename


class Email:
    ExchangeServer = 'exchange.gam.com'

    @staticmethod
    def send(subject: str, sender: str, recipients: list, body_text: str = None, Body_html: str = None) -> None:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)

        if (body_text is not None) and (body_text != ""):
            part1 = MIMEText(body_text, 'plain')
            msg.attach(part1)
        if (Body_html is not None) and (Body_html != ""):
            part2 = MIMEText(Body_html, 'html')
            msg.attach(part2)

        s = smtplib.SMTP(Email.ExchangeServer)
        s.sendmail(sender, recipients, msg.as_string())
