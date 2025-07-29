from flask import Flask, request, jsonify

app = Flask(__name__)

# GET /hello?name=Tom
@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name', 'World')
    return jsonify({"message": f"Hello, {name}!"})

# POST /add
@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    result = data['a'] + data['b']
    return jsonify({"sum": result})

if __name__ == '__main__':
    app.run(debug=True)   # 默认 http://127.0.0.1:5000