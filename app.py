  
from flask import Flask, request
import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

def generate_chatbot_response(user_input):
    # Move the chatbot code here
    # ...
    f = open('chatbot.txt', 'r', errors="ignore")
    raw_doc = f.read()
    raw_doc = raw_doc.lower()
    nltk.download('punkt')
    nltk.download('wordnet')
    sent_tokens = nltk.sent_tokenize(raw_doc)
    word_tokens = nltk.word_tokenize(raw_doc)

    lemmer = nltk.stem.WordNetLemmatizer()

    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]

    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    GREET_INPUTS = ("Hello", "Hi", "Greetings", "sup", "what's up", "hey")
    GREET_RESPONSES = ["Hi", "hey", "nods", "hi there", "hello", "I am glad! you are talking to me"]

    def greet(sentence):
        for word in sentence.split():
            if word.lower() in GREET_INPUTS:
                return random.choice(GREET_RESPONSES)

    def response(user_response):
        robo1_response = ''
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            robo1_response = robo1_response + "I am sorry! I don't understand you"
            return robo1_response
        else:
            robo1_response = robo1_response + sent_tokens[idx]
            return robo1_response

    flag = True
    robo1_response = "BOT: My name is Stark. Let's have a conversation! Also, if you want to exit at any time, just type Bye!"
    while flag:
        user_response = user_input.lower()
        if user_response != 'bye':
            if user_response == 'thanks' or user_response == 'thank you':
                flag = False
                robo1_response = "BOT: You are welcome."
            else:
                if greet(user_response) is not None:
                    robo1_response = "BOT: " + greet(user_response)
                else:
                    sent_tokens.append(user_response)
                    word_tokens = word_tokens + nltk.word_tokenize(user_response)
                    final_words = list(set(word_tokens))
                    robo1_response = "BOT: " + response(user_response)
                    sent_tokens.remove(user_response)
        else:
            flag = False
            robo1_response = "BOT: Goodbye! Take care <3"

    return robo1_response

@app.route("/sms", methods=['POST'])
def sms():
    user_input = request.form.get('Body')
    response = generate_chatbot_response(user_input)

    twilio_response = MessagingResponse()
    twilio_response.message(response)

    return str(twilio_response)

#def sms_reply():
#    """Respond to incoming calls with a simple text message."""
    # Fetch the message
#    msg = request.form.get('Body')

    # Create reply
 #   resp = MessagingResponse()
 #   resp.message("You said: {}".format(msg))

  #  return str(resp)

if __name__ == "__main__":
    app.run(debug=True)    
    
    
    
