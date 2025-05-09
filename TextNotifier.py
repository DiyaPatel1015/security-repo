from twilio.rest import Client
from keys import ACC_SID, AUTH_TOKEN, FROM_NUMBER, TO_NUMBER


class TextNotifier:
    def __init__(self):
        self.client = Client(ACC_SID, AUTH_TOKEN)
        self.from_number = FROM_NUMBER
        self.to_number = TO_NUMBER

    def send_alert(self, message_body):
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=self.to_number
            )
            print(f"Message sent, status: {message.status}")
        except Exception as e:
            print(f"Failed to send message: {e}")


    def message_user(self):
        try:
            message = self.client.messages.create(
                body="Warning, there is an intruder!",
                from_=FROM_NUMBER,
                to=TO_NUMBER
            )
            print(message.status)
        except Exception as e:
            print(f"Failed to send message: {e}")


    def test_message(self, message_body):
        client = Client(ACC_SID, AUTH_TOKEN)
        if client:
            print("client created")
        print("sending message")

