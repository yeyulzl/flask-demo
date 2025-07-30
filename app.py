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
    # 生产环境端口由环境变量 PORT 决定，缺省用 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)