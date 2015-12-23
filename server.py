from flask import Flask
from application_only_auth import Client
import json
import markov_vector_module
app = Flask(__name__)

key_file = open('api_key.txt', 'r')
secret_file = open('api_secret.txt', 'r')
consumer_key = key_file.readline().rstrip('\n')
consumer_secret = secret_file.readline().rstrip('\n')

client = Client(consumer_key, consumer_secret)

oauth_url = 'https://api.twitter.com/oauth2/token'


@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


@app.route("/")
def root():
    api_output = client.request(
        'https://api.twitter.com/1.1/statuses/user_timeline.json?' +
        'screen_name=realdonaldtrump&count=200'
        )
    text_corpus = ''
    for tweet in api_output:
        text_corpus = text_corpus + tweet['text'] + '\n'
    vector = markov_vector_module.markov_vector()
    vector.build_from_corpus(text_corpus)

    return_text = ''
    current = vector.generateTransition((None, None))
    last = None
    while current is not None and len(return_text) < 130:
        return_text = return_text + current + ' '
        temp = current
        current = vector.generateTransition((last, current))
        last = temp
    return return_text


#@app.route("/")
#def root():
#    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.secret_key = 'wololo'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)
