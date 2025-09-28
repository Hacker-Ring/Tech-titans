"""
ShelfScanner Flask App for Hugging Face Spaces
A modern web application for book discovery through camera scanning, text search, and recommendations.
"""

import os
import json
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY', '')
GOOGLE_CLOUD_VISION_API_KEY = os.getenv('GOOGLE_CLOUD_VISION_API_KEY', '')

@app.route('/')
def index():
    """Serve the main application page"""
    return send_from_directory('.', 'index.html')

@app.route('/genre.html')
def genre():
    """Serve the genre page"""
    return send_from_directory('.', 'genre.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"ok": True})

@app.route('/api/books/search', methods=['GET'])
def search_books():
    """Search books using Google Books API"""
    try:
        query = request.args.get('q', '')
        max_results = min(int(request.args.get('maxResults', 10)), 40)
        start_index = max(int(request.args.get('startIndex', 0)), 0)
        
        # Build Google Books API URL
        url = f"https://www.googleapis.com/books/v1/volumes"
        params = {
            'q': query,
            'printType': 'books',
            'maxResults': max_results,
            'startIndex': start_index
        }
        
        if GOOGLE_BOOKS_API_KEY:
            params['key'] = GOOGLE_BOOKS_API_KEY
            
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return jsonify(data)
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch books", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/api/vision/ocr', methods=['POST'])
def vision_ocr():
    """Extract text from images using Google Cloud Vision API"""
    try:
        if not GOOGLE_CLOUD_VISION_API_KEY:
            return jsonify({"error": "Vision API key not configured"}), 400
            
        data = request.get_json()
        image_base64 = data.get('imageBase64')
        
        if not image_base64:
            return jsonify({"error": "imageBase64 is required"}), 400
            
        # Prepare Vision API request
        vision_request = {
            "requests": [
                {
                    "image": {"content": image_base64},
                    "features": [{"type": "TEXT_DETECTION", "maxResults": 5}]
                }
            ]
        }
        
        url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_CLOUD_VISION_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, json=vision_request, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return jsonify(result)
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Vision OCR failed", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/api/books/openlibrary', methods=['GET'])
def search_openlibrary():
    """Search books using Open Library API"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400
            
        url = f"https://openlibrary.org/search.json"
        params = {'q': query, 'limit': 10}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Transform Open Library data to match our format
        books = []
        for doc in data.get('docs', [])[:10]:
            book = {
                'title': doc.get('title', 'Unknown Title'),
                'author': ', '.join(doc.get('author_name', ['Unknown Author'])),
                'source': 'Open Library',
                'image': f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-M.jpg" if doc.get('cover_i') else None,
                'isbn': doc.get('isbn', [None])[0] if doc.get('isbn') else None,
                'publish_year': doc.get('first_publish_year'),
                'subject': doc.get('subject', [])[:3] if doc.get('subject') else []
            }
            books.append(book)
            
        return jsonify({"books": books})
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch from Open Library", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # For Hugging Face Spaces
    port = int(os.environ.get('PORT', 7860))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
