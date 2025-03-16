from flask import Flask, request, jsonify, redirect
import json
import os

app = Flask(__name__)

# File to store the shortened URLs
URL_FILE = 'urls.json'

# Load the URLs from the JSON file
def load_urls():
    try:
        if os.path.exists(URL_FILE):
            with open(URL_FILE, 'r') as file:
                return json.load(file)
        return {}  # If no file exists, return an empty dictionary
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {URL_FILE}: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error loading {URL_FILE}: {e}")
        return {}

# Save the URLs to the JSON file
def save_urls(urls):
    try:
        with open(URL_FILE, 'w') as file:
            json.dump(urls, file, indent=4)
    except Exception as e:
        print(f"Error saving URLs to {URL_FILE}: {e}")

# URL Shortening Route (POST)
@app.route('/shorten', methods=['POST'])
def shorten_url():
    try:
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

        # Update the URL to point to your Netlify URL (or other appropriate domain)
        short_url = f"https://your-netlify-subdomain.netlify.app/{short_code}"

        return jsonify({"short_url": short_url})
    except Exception as e:
        print(f"Error in /shorten route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# URL Redirect Route (GET)
@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    try:
        urls = load_urls()

        # Find the original URL from the shortened URL
        original_url = urls.get(short_code)

        if original_url:
            return redirect(original_url)
        else:
            return "Short URL not found!", 404
    except Exception as e:
        print(f"Error in /{short_code} route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# This is necessary for the serverless function to run correctly
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
