import smtplib 

my_email = 'fabrizio.bernini1978@gmail.com'
password = 'xxxx'

server = smtplib.SMTP("smtp.gmail.com", port=587)
server.ehlo()
server.starttls()

try:
    server.login(my_email, password)
    print('login riuscito')
except smtplib.SMTPAuthenticationError:
    print('login non riuscito')
    
server.quit()
