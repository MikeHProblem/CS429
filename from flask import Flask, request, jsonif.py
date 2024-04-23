from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask-Based Query Processor!"

@app.route('/query', methods=['POST'])
def query():
    if request.is_json:
        data = request.get_json()
        query = data.get('query', '')
        # Here you would integrate your search functionality
        return jsonify({"message": f"Received query: {query}"})
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True)
