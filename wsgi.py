from flask import Flask, Response, request
import subprocess
import threading
import time
import requests
import os

app = Flask(__name__)

# Start Streamlit in a background thread
def run_streamlit():
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    subprocess.run([
        'streamlit', 'run', 'app.py', 
        '--server.port=8501', 
        '--server.headless=true',
        '--server.enableCORS=false'
    ])

# Start Streamlit when the module loads
streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
streamlit_thread.start()

# Wait for Streamlit to start
time.sleep(5)

@app.route('/')
def index():
    try:
        response = requests.get('http://localhost:8501', timeout=10)
        return Response(response.content, response.status_code, dict(response.headers))
    except:
        return Response("Streamlit is starting...", 200)

@app.route('/<path:path>')
def proxy(path):
    try:
        response = requests.get(f'http://localhost:8501/{path}', timeout=10)
        return Response(response.content, response.status_code, dict(response.headers))
    except:
        return Response("Streamlit is starting...", 200)

def handler(environ, start_response):
    return app(environ, start_response)
