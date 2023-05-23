import random
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"




def chatbot(user_input):
    # List of random replies
    replies = [
        "Hello!",
        "How are you?",
        "Tell me more.",
        "That's interesting.",
        "I'm not sure.",
        "What do you think?",
        "Let's change the topic.",
        "Goodbye!",
    ]
    
    # Generate a random reply
    reply = random.choice(replies)
    
    return reply

# Example usage
@app.route("/sms", methods=['POST'])

def sms_reply():
#    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    user_input = request.form.get('Body')
    response = chatbot(user_input)
    # Create reply
    resp = MessagingResponse()
    resp.message(response)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)    
    
    
    
