from twilio.rest import Client
# put your own credentials here
account_sid = "AC9919c5215893c6732fe195a1f70c3fb6"
auth_token = "ea8472b1f33b7e84c842702f175505b2"
client = Client(account_sid, auth_token)
client.messages.create(
  to="15138396035",
  from_="+17864654228",
  body="testing")
