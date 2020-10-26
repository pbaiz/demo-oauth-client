from flask import Flask, url_for, session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')

#CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='exate',
    client_id='{{ your-github-client-id }}',
    client_secret='{{ your-github-client-secret }}',
    access_token_url='https://auth.dev.exate.co',
    access_token_params=None,
    authorize_url='https://auth.dev.exate.co/account/login',
    authorize_params=None,
    api_base_url='https://auth.dev.exate.co',
    #server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.exate.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.exate.authorize_access_token()
    user = oauth.exate.parse_id_token(token)
    session['user'] = user
    return redirect('/')


@app.route('/another_end')
def another_end():
    user = session.get('user')
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run()
