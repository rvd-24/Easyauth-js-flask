# Backend: app.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/data')
def protected_data():
    # Verify the access token
    token = request.headers.get('X-MS-TOKEN-AAD-ACCESS-TOKEN')
    if not token:
        return jsonify({"error": "No token provided"}), 401
    
    # Validate the token (in a production app, you'd want to cache this)
    validation_url = "https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token"
    response = requests.get(validation_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code != 200:
        return jsonify({"error": "Invalid token"}), 401
    
    # Token is valid, return protected data
    return jsonify({"message": "This is protected data!"})


@app.route('/api/user')
def get_user_info():
    # Get the access token from the request header
    access_token = request.headers.get('X-MS-TOKEN-AAD-ACCESS-TOKEN')
    
    if not access_token:
        return jsonify({"error": "No access token provided"}), 401

    # Use the access token to get user info from Microsoft Graph API
    graph_api_url = "https://graph.microsoft.com/v1.0/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(graph_api_url, headers=headers)
    
    if response.status_code == 200:
        user_info = response.json()
        return jsonify(user_info)
    else:
        return jsonify({"error": "Failed to fetch user info"}), 400

if __name__ == '__main__':
    app.run()