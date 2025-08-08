from app import app

if __name__ == '__main__':
    # Use 0.0.0.0 for compatibility with different environments
    app.run(host='0.0.0.0', port=8080, debug=True)