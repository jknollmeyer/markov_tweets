from flask import Flask, request
from application_only_auth import Client
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


@app.route("/tweets", methods=['POST'])
def tweets():
    text_corpus = ''
    maxid = None
    # paginate through the tweets, getting 200 at a time
    for i in xrange(1):
        requestString = (
            'https://api.twitter.com/1.1/statuses/user_timeline.json?' +
            'screen_name=' + request.form['username'] +
            '&count=200' +
            '&include_rts=false'
        )
        # use id from the previous oldest tweet to allow us to paginate
        if maxid is not None:
            requestString += ('&max_id=' + str(maxid))
        try:
            api_output = client.request(requestString)
        except Exception, err:
            if err.code == 404:
                return str(404)
            else:
                return "UNKNOWN"

        # go through the tweets and add them to the text corpus
        for tweet in api_output:
            text_corpus += tweet['text'] + '\n'
            maxid = tweet['id']
    # initialize the markov chain
    vector = markov_vector_module.markov_vector()
    vector.build_from_corpus(text_corpus)
    return_text = ''
    # build then chain, but re-do process if the result is too short
    while len(return_text) < 30:
        return_text = ''
        current = vector.generateTransition((None, None))
        last = None
        # get new words until we hit a "None" result
        while current is not None:
            return_text = return_text + current + ' '
            temp = current
            current = vector.generateTransition((last, current))
            last = temp
    return return_text


@app.route("/test")
def test():
    return "adsasdasdasd"


@app.route("/")
def root():
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.secret_key = 'wololo'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)
