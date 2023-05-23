  
from flask import Flask, request, jsonify
import numpy as np
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

@app.route("/sms", methods=['POST'])
def generate_chatbot_response(user_input):
    # Move the chatbot code here
    # ...
    f = open('chatbot.txt','r',errors = "ignore")
    raw_doc = f.read()
    raw_doc = raw_doc.lower()  #converts text to lower case
    nltk.download('punkt') #punkt tokeniser
    nltk.download('wordnet')  #wordnet dictionary
    sent_tokens = nltk.sent_tokenize(raw_doc) #converts doc to list of sentences
    word_tokens = nltk.word_tokenize(raw_doc) #converts doc to lisgt of words

##text preprocessing

    lemmer = nltk.stem.WordNetLemmatizer()
#wordnet is semantically-oriented dictionary of english included in NLTK
    def LemTokens(tokens):
        return[lemmer.lemmatize(token) for token in tokens]
    remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)
    def LemNormalize(text):    #check vector normalisation
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

#defining the greeting function

    GREET_INPUTS = ("Hello","Hi","Greetings","sup","what's up", "hey")
    GREET_RESPONSES = ["Hi","hey","nods","hi there","hello","I am glad! you are talking to me"]
    def greet(sentence):
        for word in sentence.split():
            if word.lower() in GREET_INPUTS:
                return random.choice(GREET_RESPONSES)
        
    from sklearn.feature_extraction.text import TfidfVectorizer
#Tdidf = Term frequency , which gives the number of times each word is repeated in corpus
#idf,inverse document frequency,how rare is occurance of a word in corpus 

    from sklearn.metrics.pairwise import cosine_similarity
#once words are ready in terms of 0s and 1s,it provides a normalised vector
#provide understanding to the machine of what the user is doing

    def response(user_response):
        robo1_response=''
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec. fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf==0):
            robo1_response = robo1_response+"I am sorry!I don't understand you"
            return robo1_response
        else:
            robo1_response = robo1_response + sent_tokens[idx]
        return robo1_response
    
##defining conversation start/end protocols
    flag=True
    print("BOT: My name is Stark. Let's have a conversation! Also, if you want to exit any time, just type Bye!")
    while(flag==True):
        user_response = input()
        user_response=user_response.lower()
        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you' ):
                flag=False
                print ("BOT: You are welcome..")
            else:
                if(greet (user_response)!=None):
                    print("BOT: "+greet(user_response))
                else:
                    sent_tokens.append (user_response)
                    word_tokens=word_tokens+nltk.word_tokenize(user_response)
                    final_words=list(set(word_tokens))
                    print("BOT: ",end="")
                    print(response(user_response))
                    sent_tokens.remove(user_response)
        else:
            flag=False
            print("BOT: Goodbye! Take care <3 ")
    
        return robo1_response
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
    
    
    
