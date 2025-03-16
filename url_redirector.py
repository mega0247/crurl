from flask import Flask, request, jsonify, redirect
import json
import os

app = Flask(__name__)

URL_FILE = 'urls.json'

# Function to load the URLs from the JSON file
def load_urls():
    try:
        if os.path.exists(URL_FILE):
            with open(URL_FILE, 'r') as file:
                return json.load(file)
        return {}
    except Exception as e:
        print(f"Error loading URLs: {e}")
        return {}

# Function to save the URLs to the JSON file
def save_urls(urls):
    try:
        with open(URL_FILE, 'w') as file:
            json.dump(urls, file, indent=4)
    except Exception as e:
        print(f"Error saving URLs: {e}")

@app.route('/')
def home():
    return "Welcome to the URL Redirector API!", 200

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get("original_url")
    if not original_url:
        return jsonify({"error": "Missing original_url"}), 400

    urls = load_urls()
    short_code = "abc123"  # Hardcoded for simplicity

    urls[short_code] = original_url
    save_urls(urls)

    short_url = f"http://127.0.0.1:5000/{short_code}"
    return jsonify({"short_url": short_url})

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    urls = load_urls()
    original_url = urls.get(short_code)

    if original_url:
        return redirect(original_url)
    else:
        return "Short URL not found!", 404

if __name__ == '__main__':
    app.run(debug=True)
