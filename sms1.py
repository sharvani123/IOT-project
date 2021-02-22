from twilio.rest import Client
import twilio

a_sid="ACe6f30f6c65f79df66c5fa4eb38857aa5"    # Twilio SID number
a_token= "182e4e10c57080ce60c6a9eefc2a6548" # Twilio Token number 
to_no= '+919494886210' # mobile number
my_no= '+12017482449'  # Twilio number


client =Client(a_sid, a_token)

f=open('/home/pi/data.txt','r')
my_msg= f.read()
f.close

msg=client.messages.create(to=to_no, from_=my_no, body=my_msg)

print ("your msg has been sent")
