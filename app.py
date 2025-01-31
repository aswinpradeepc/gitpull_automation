from flask import Flask, jsonify, request
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
app.debug = False

def authenticate_request(req):
    key = req.headers.get("X-API-KEY")
    return key == API_KEY

@app.route('/git/pull/', methods=['POST'])
def git_pull():
    if not authenticate_request(request):
        return jsonify(detail='error', message='Unauthorized'), 403
    try:
        # Navigate to marine-sc directory and run git pull
        subprocess.run(["git", "-C", "../marine-sc", "pull"], check=True)
        subprocess.run(["docker", "compose", "down"], check=True)
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
        return jsonify(detail='success')
    except subprocess.CalledProcessError as e:
        return jsonify(detail='error', message=str(e)), 500

@app.route('/docker/start/', methods=['POST'])
def start_docker():
    if not authenticate_request(request):
        return jsonify(detail='error', message='Unauthorized'), 403
    try:
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
        return jsonify(detail='success')
    except subprocess.CalledProcessError as e:
        return jsonify(detail='error', message=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
