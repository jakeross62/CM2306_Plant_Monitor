import smtplib, ssl

admin_email = 'vhs.beyouapp@gmail.com' #stores the email that is used to send out emails to users
admin_password = '' #password for the email in order to login in and send emails - password was removed before submission for security
user = "dahege6663@syinxun.com"
message = "Hello"

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()

#with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(admin_email, admin_password)
server.sendmail(admin_email,user,message)#sends the email by calling a method
