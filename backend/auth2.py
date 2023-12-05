from flask_restx import Resource, Namespace, fields
from flask import request, redirect, session, jsonify, url_for, make_response
from flask_cors import cross_origin
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
        del session["state"]
        return jsonify({"deleted": "deleted"})
    
@auth_ns.route("/check")
class CheckState(Resource):
    def get(self):
        state = session["state"]
        return jsonify({"session_state": state})

# Home route - initiate the authorization process
@auth_ns.route("/login")
class Login(Resource):
  def get(self):
    state = generate_state()
    session["state"] = state  # Store the state in the session for later verification
    
    authorize_url = (
        f"{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}"
        f"&response_type=code&redirect_uri={REDIRECT_URI}"
        f"&scope=user-read-private user-read-email user-top-read user-read-recently-played&state={state}"
    )
    # return jsonify({"authUrl": authorize_url})
    response = make_response(jsonify({"authUrl": authorize_url}))

    return response
  
  
# Callback route - handle the redirect from Spotify after authorization
@auth_ns.route("/callback")
class Callback(Resource):
  def get(self):
    code = request.args.get("code")
    state = request.args.get("state")
    session_state = session["state"]
    
    # Check if the state parameter matches (CSRF protection)
    # if session_state != state:
    #     return "Invalid state parameter", 400

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



@auth_ns.route("/top")
class Top(Resource):
  def get(self):
    access_token = request.args.get("accessToken")
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': 10}
    api_url = 'https://api.spotify.com/v1/me/top/tracks'
    
    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
      top_tracks = response.json()['items']
      return top_tracks
    else:
      return jsonify({"error": error})
    
    
