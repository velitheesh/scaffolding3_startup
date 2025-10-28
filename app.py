"""
app.py
Flask application template for the warm-up assignment

Students need to implement the API endpoints as specified in the assignment.
"""

from flask import Flask, request, jsonify, render_template
from starter_preprocess import TextPreprocessor
import traceback  # Good for debugging

app = Flask(__name__)
preprocessor = TextPreprocessor()


@app.route('/')
def home():
    """Render a simple HTML form for URL input"""
    return render_template('index.html')


@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Text preprocessing service is running"
    })


@app.route('/api/clean', methods=['POST'])
def clean_text():
    """
    API endpoint that accepts a URL and returns cleaned text,
    statistics, and a summary.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON payload provided."}), 400
            
        url = data.get('url')
        if not url:
            return jsonify({"success": False, "error": "No 'url' key found in JSON payload."}), 400

        # 1. Fetch
        raw_text = preprocessor.fetch_from_url(url) 
        
        # 2. Clean Gutenberg headers/footers
        cleaned_text = preprocessor.clean_gutenberg_text(raw_text)
        
        # --- THIS IS THE NEW LOGIC ---
        
        # 3. Get stats from the CLEANED text (this method now does its own normalization)
        statistics = preprocessor.get_text_statistics(cleaned_text)
        
        # 4. Create summary from the CLEANED text (which has punctuation)
        summary = preprocessor.create_summary(cleaned_text)
        
        # 5. Normalize text *only* for the final output
        normalized_text = preprocessor.normalize_text(cleaned_text)

        # 6. Return the successful JSON response
        return jsonify({
            "success": True,
            "cleaned_text": normalized_text, # Return the final processed text
            "statistics": statistics,
            "summary": summary
        }), 200
        
    except Exception as e:
        print(traceback.format_exc()) 
        return jsonify({
            "success": False,
            "error": f"An error occurred: {str(e)}" 
        }), 400

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    API endpoint that accepts raw text and returns statistics only
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON payload provided."}), 400
            
        text = data.get('text')
        if text is None:
            return jsonify({"success": False, "error": "No 'text' key found in JSON payload."}), 400

        # Run stats directly on the raw text
        statistics = preprocessor.get_text_statistics(text)
        
        return jsonify({
            "success": True,
            "statistics": statistics
        }), 200
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }), 400

# Error handlers


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    # This will catch unhandled exceptions in Flask itself
    print(traceback.format_exc())
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("🚀 Starting Text Preprocessing Web Service...")
    print("📖 Available endpoints:")
    print("   GET  /           - Web interface")
    print("   GET  /health     - Health check")
    print("   POST /api/clean  - Clean text from URL")
    print("   POST /api/analyze - Analyze raw text")
    print()
    print("🌐 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")

    # host='0.0.0.0' makes it accessible within Codespaces
    app.run(debug=True, port=5000, host='0.0.0.0')
