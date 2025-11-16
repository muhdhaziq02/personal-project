# rest_server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Helper Function (same as gRPC server) ---
def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

# --- API Endpoints ---
@app.route('/process', methods=['POST'])
def process_data():
    # 1. Map (square) and Reduce (sum)
    data = request.json['numbers']
    mapped = [n * n for n in data]
    reduced = sum(mapped)
    return jsonify({"value": reduced})

@app.route('/wordcount', methods=['POST'])
def word_count():
    # 2. Word Count
    content = request.json['content']
    words = content.split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return jsonify({"counts": counts})

@app.route('/minmax', methods=['POST'])
def get_min_max():
    # 3. Find Min/Max
    data = request.json['numbers']
    return jsonify({"min": min(data), "max": max(data)})

@app.route('/sort', methods=['POST'])
def get_sorted():
    # 4. Sort Numbers
    data = request.json['numbers']
    asc = sorted(data)
    desc = sorted(data, reverse=True)
    return jsonify({"ascending": asc, "descending": desc})

@app.route('/primes', methods=['POST'])
def get_primes():
    # 5. List Primes
    data = request.json['numbers']
    primes = [n for n in data if is_prime(n)]
    return jsonify({"numbers": primes})

if __name__ == '__main__':
    print("Starting REST server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)