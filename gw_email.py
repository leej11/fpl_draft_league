from fpl_draft_league import charts
import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

port = 465
password = ''
sender_email = "sender@blah.com"
receiver_email = "receiver@blah.com"
message = """This is a test python email yippee!"""

message = MIMEMultipart("alternative")
message["Subject"] = "FPL Draft League - GW 28 Newsletter"
message["From"] = sender_email
message["To"] = receiver_email

text = """this is just the plain text version"""

html = html = f"""\
<html>
  <body>
    <h1>Welcome to the latest FPL Draft League - Gameweek Update</h1>
    <br>
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
    <h2>Transfers</h2>
    <p>New for this week is the <i>Net transfer value chart</i> which shows transfer-out:transfer-in and
    the net points from that transfer!
    <br>
    <img src="cid:transfers">
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
    
with open('data/transfers.png', 'rb') as image:
    msgImage4 = MIMEImage(image.read())
    
    
msgImage.add_header('Content-ID', '<standings>')
msgImage2.add_header('Content-ID', '<topnplayers>')
msgImage3.add_header('Content-ID', '<streaks>')
msgImage4.add_header('Content-ID', '<transfers>')
message.attach(msgImage)
message.attach(msgImage2)
message.attach(msgImage3)
message.attach(msgImage4)

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
