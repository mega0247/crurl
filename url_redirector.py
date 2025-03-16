from flask import Flask, request, jsonify, redirect
import json
import os

app = Flask(__name__)

# File to store the shortened URLs
URL_FILE = 'urls.json'

# Load the URLs from the JSON file
def load_urls():
    if os.path.exists(URL_FILE):
        with open(URL_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save the URLs to the JSON file
def save_urls(urls):
    with open(URL_FILE, 'w') as file:
        json.dump(urls, file, indent=4)

# Homepage Route
@app.route('/')
def home():
    return "Welcome to the URL Redirector API!", 200

# URL Shortening Route (POST)
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get("original_url")

    if not original_url:
        return jsonify({"error": "Missing original_url"}), 400

    urls = load_urls()

    # Generate a unique short code (for demo purposes, hardcoded to "abc123")
    short_code = "abc123"  # You should generate a real unique code here
    
    # Store the mapping in memory (and save it to the file)
    urls[short_code] = original_url
    save_urls(urls)

    short_url = f"https://{request.host}/{short_code}"

    return jsonify({"short_url": short_url})

# URL Redirect Route (GET)
@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    urls = load_urls()

    # Find the original URL from the shortened URL
    original_url = urls.get(short_code)

    if original_url:
        return redirect(original_url)
    else:
        return "Short URL not found!", 404

if __name__ == '__main__':
    app.run(debug=True)
