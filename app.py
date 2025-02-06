from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v2/monitor')
def monitor():
    return jsonify({"status": "Running smoothly"})

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 