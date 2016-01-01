from flask import Flask, request
from redis import Redis
from application_only_auth import Client
import markov_vector_module
import json
app = Flask(__name__)

redis = Redis()

# import the key and secret from locally stored files (so they aren't in git)
key_file = open('api_key.txt', 'r')
secret_file = open('api_secret.txt', 'r')
consumer_key = key_file.readline().rstrip('\n')
consumer_secret = secret_file.readline().rstrip('\n')

client = Client(consumer_key, consumer_secret)

oauth_url = 'https://api.twitter.com/oauth2/token'


@app.route('/<path:path>')  # Set up static routing to serve the front end
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


@app.route("/tweets", methods=['POST'])  # Route to activate tweet generation
def tweets():
    maxid = userImageUrl = profileName = None

    # paginate through the tweets, getting 200 at a time
    for i in xrange(16):
        requestString = (
            'https://api.twitter.com/1.1/statuses/user_timeline.json?' +
            'screen_name=' + request.form['username'] +
            '&count=200' +
            '&include_rts=false'
        )
        # use id from the previous oldest tweet to allow us to paginate
        if maxid is not None:
            requestString += ('&max_id=' + str(maxid - 1))
        # Exception handling for API requests i.e. HTTP 400 errors
        try:
            api_output = client.request(requestString)
        except Exception, err:
            if err.code == 404:
                return str(404)
            elif err.code == 401:
                return str(401)
            else:
                return "UNKNOWN"
        # Handle a request that returns no tweets
        if api_output == []:
            # If this first batch of tweets is empty, send 204 no content
            if i == 1:
                return str(204)
            else:
                break
        if userImageUrl is None:
            userImageUrl = api_output[0]['user']['profile_image_url']
        if profileName is None:
            profileName = api_output[0]['user']['name']
        # make sure the request isn't already cached
        if redis.exists(request.form['username']):
            user_tweets = redis.hgetall(request.form['username'])
            if len(api_output) and str(api_output[0]['id']) in user_tweets:
                break
        else:
            user_tweets = dict()

        # go through the tweets and add them to the redis cache
        for tweet in api_output:
            user_tweets[tweet['id']] = tweet['text']
            maxid = tweet['id']
        redis.hmset(request.form['username'], user_tweets)

    user_tweets = redis.hgetall(request.form['username'])
    text_corpus = "\n".join([text.decode('utf-8') for id, text in user_tweets.items()])

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
    data = json.dumps({
        'tweet': return_text,
        'pic': userImageUrl,
        'name': profileName
    })
    return data


@app.route("/")
def root():
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.secret_key = 'wololo'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)
