from flask import Flask
from application_only_auth import Client
import json
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
    tweet = client.request(
        'https://api.twitter.com/1.1/statuses/show.json?id=316683059296624640'
        )
    return json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ':'))
    # return app.send_static_file('index.html')


if __name__ == "__main__":
    app.secret_key = 'wololo'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)
