from flask_restx import Resource, Namespace, fields
from flask import request, redirect, session, jsonify, make_response
import requests
import secrets

auth_ns = Namespace('auth', description="A namespace for Authentication")

# Spotify API credentials
CLIENT_ID = "eabd68e3d6d94d698c4f91470c3f9c37"
CLIENT_SECRET = "03b3cdcd63874050b86f321620586d27"
REDIRECT_URI = "http://localhost:5000/auth/callback"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Generate a random state for CSRF protection
def generate_state():
    return secrets.token_urlsafe(16)

@auth_ns.route("/del")
class CheckState(Resource):
    def get(self):
        # Delete the state cookie
        response = make_response(jsonify({"deleted": "deleted"}))
        response.delete_cookie("state")
        return response
    
@auth_ns.route("/check")
class CheckState(Resource):
    def get(self):
        # Retrieve the state from the cookie
        state = request.cookies.get("state")
        return jsonify({"cookie_state": state})

# Home route - initiate the authorization process
@auth_ns.route("/login")
class Login(Resource):
  def get(self):
    state = generate_state()

    # Set the state in a cookie
    response = make_response(jsonify({"authUrl": authorize_url}))
    response.set_cookie("state", state)

    authorize_url = (
        f"{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}"
        f"&response_type=code&redirect_uri={REDIRECT_URI}"
        f"&scope=user-read-private user-read-email user-top-read user-read-recently-played&state={state}"
    )

    return response
  
# Callback route - handle the redirect from Spotify after authorization
@auth_ns.route("/callback")
class Callback(Resource):
  def get(self):
    code = request.args.get("code")
    state = request.args.get("state")

    # Retrieve the state from the cookie
    cookie_state = request.cookies.get("state")

    # Check if the state parameter matches the cookie value (CSRF protection)
    if cookie_state != state:
        return "Invalid state parameter", 400

    # Exchange authorization code for access token
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)
    access_token = response.json().get("access_token")
    
    redirect_url = f'http://localhost:3000/dashboard?access_token={access_token}&state={state}'
    return redirect(redirect_url)
