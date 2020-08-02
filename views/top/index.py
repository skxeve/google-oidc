from flask import (
    Blueprint,
    current_app,
    render_template,
    session,
    redirect,
    request,
    jsonify,
)
from flask_gcp_wand.consts.oauth import (
    AUTHORIZATION_ENDPOINT,
    TOKEN_ENDPOINT,
    SCOPES_SUPPORTED,
)
from flask_gcp_wand.appengine.env import GaeEnv
from requests_oauthlib import OAuth2Session


top = Blueprint("top", __name__)


@top.route("/hello")
def echo():
    current_app.logger.debug(
        f"top hello{current_app.config.get('OIDC_CLIENT_ID')}"
    )
    current_app.logger.info(
        f"url:{request.url} instance:{GaeEnv.gae_instance}"
    )
    return render_template(
        "hello.html", title="Hello Today!", name=session.get("user_name")
    )


@top.route("/dummy-login/<user_name>")
def login(user_name):
    current_app.logger.debug(
        f"login test{current_app.config.get('OIDC_CLIENT_SECRET')}"
    )
    session["user_name"] = user_name
    current_app.logger.info("session: {}".format(dict(session)))
    return redirect("/hello")


@top.route("/login/google/oauth")
def google_login():
    redirect_uri = (
        current_app.config.get("APP_DOMAIN") + "/login/google/callback"
    )
    oauth = OAuth2Session(
        current_app.config.get("GOOGLE_CLIENT_ID"),
        redirect_uri=redirect_uri,
        scope=SCOPES_SUPPORTED,
    )
    authorization_url, state = oauth.authorization_url(AUTHORIZATION_ENDPOINT)
    session["oauth_state"] = state
    return redirect(authorization_url)


@top.route("/login/google/callback")
def google_callback():
    redirect_uri = (
        current_app.config.get("APP_DOMAIN") + "/login/google/callback"
    )
    oauth = OAuth2Session(
        current_app.config.get("GOOGLE_CLIENT_ID"),
        redirect_uri=redirect_uri,
        scope=SCOPES_SUPPORTED,
        state=session["oauth_state"],
    )
    access_token = oauth.fetch_token(
        TOKEN_ENDPOINT,
        client_secret=current_app.config.get("GOOGLE_CLIENT_SECRET"),
        authorization_response=request.url,
    )
    session["access_token"] = access_token
    userinfo = oauth.get(
        "https://www.googleapis.com/oauth2/v1/userinfo"
    ).json()
    current_app.logger.info(f"google-userinfo:{userinfo}")
    try:
        session["google_email"] = userinfo["email"]
        session["google_id"] = userinfo["id"]
        session["google_locale"] = userinfo["locale"]
        session["google_verified"] = userinfo["verified_email"]
    except Exception as e:
        current_app.logger.error(e)

    session["user_name"] = session["google_email"]
    return redirect("/hello")
