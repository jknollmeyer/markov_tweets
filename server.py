from flask import Flask, redirect, flash, session, request, url_for
from flask_oauthlib.client import OAuth
app = Flask(__name__)

secret_file = open('api_secret.txt', 'r')
oauth = OAuth()
twitter = oauth.remote_app(
    'twitter',
    base_url="https://api.twitter.com/1.1/",
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    consumer_key='NZX0TxexC0ByKuvWiGvIoFuzb',
    consumer_secret=secret_file.readline().rstrip('\n')

)


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/login')
def login():
    return twitter.authorize('/oauth-authorized')


@app.route('/oauth-authorized')
def oauth_authorized():
    next_url = request.args.get('next') or url_for('hello')
    resp = twitter.authorized_response()
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


@app.route("/")
def hello():
    return "<a href=\"http://localhost:5000/login\">Hello World!</a>"

if __name__ == "__main__":
    app.secret_key = 'wololo'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)
