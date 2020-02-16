from fpl_draft_league import charts
import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

port = 465
password = os.environ['MY_PASSWORD']
sender_email = "leejghd@gmail.com"
receiver_email = "lee.gower17@gmail.com"
message = """This is a test python email yippee!"""

message = MIMEMultipart("alternative")
message["Subject"] = "A test email"
message["From"] = sender_email
message["To"] = receiver_email

text = """this is just the plain text version"""

html = html = f"""\
<html>
  <body>
    <h1>Welcome to the latest FPL Draft League - Gameweek Update
    <br>
    <h2>Standings</h2>
    <p>After the latest gameweek, here are how the standings are evolving:
    <br>
    <img src="cid:standings">
    <br>
    <h2>Top Football Players</h2>
    <p>Which football players made a big impact this week for your teams?
    <br>
    <img src="cid:topnplayers">
    <br>
    <h2>Streaks</h2>
    <p>After the latest gameweek, who is on the hot streak now? Who's having a rough patch?
    <br>
    <img src="cid:streaks">
    <br>
    That's it for this week. Please feedback any ideas you have for charts to add, or things to tweak! You can visit the <a href="https://github.com/leej11/fpl_draft_league">Github repo here</a> to make pull requests or just browse the code!
    </p>
  </body>
</html>
"""

part2 = MIMEText(html, "html")

message.attach(part2)

with open('data/standings.png', 'rb') as image:
    msgImage = MIMEImage(image.read())
    
with open('data/topnplayers.png', 'rb') as image:
    msgImage2 = MIMEImage(image.read())

with open('data/streaks.png', 'rb') as image:
    msgImage3 = MIMEImage(image.read())
    
    
msgImage.add_header('Content-ID', '<standings>')
msgImage2.add_header('Content-ID', '<topnplayers>')
msgImage3.add_header('Content-ID', '<streaks>')
message.attach(msgImage)
message.attach(msgImage2)
message.attach(msgImage3)

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("leejghd@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message.as_string())