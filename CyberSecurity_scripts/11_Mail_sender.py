import smtplib 

messaggio = 'Prova: saluti da Python. FB'
my_email = 'fab@fb-engineering.co.uk'
user = my_email
password = 'xxxx'

def prompt(prompt):
    return input(prompt).strip()
fromaddr = prompt("From: ")
toaddrs  = prompt("To: ").split()
print("Enter message, end with ^D (Unix) or ^Z (Windows):")
# Add the From: and To: headers at the start!
msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, ", ".join(toaddrs)))
while True:
    try:
        line = input()
    except EOFError:
        break
    if not line:
        break
    msg = msg + line
print(msg)

server = smtplib.SMTP("smtp.servermx.com", port=587)
#server.ehlo()
server.starttls()
server.login(user, password)
server.sendmail(my_email, my_email, msg)
server.quit()
