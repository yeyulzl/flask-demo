import os

from flask import Flask, request, jsonify
from models import db, Inspiration

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inspiration.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# 列表（支持分页 / 过滤）
@app.route('/inspirations')
def list_inspirations():
    page  = request.args.get('page', 1, type=int)
    size  = request.args.get('size', 10, type=int)
    archived = request.args.get('archived', 'false') == 'true'
    query = Inspiration.query.filter_by(archived=archived)\
             .order_by(Inspiration.created_at.desc())\
             .paginate(page=page, per_page=size, error_out=False)
    return jsonify({
        'items': [i.to_dict() for i in query.items],
        'total': query.total
    })

# 新建
@app.route('/inspirations', methods=['POST'])
def add_inspiration():
    data = request.get_json()
    insp = Inspiration(
        title=data['title'],
        content=data.get('content', ''),
        priority=data.get('priority', 3)
    )
    db.session.add(insp)
    db.session.commit()
    return jsonify(insp.to_dict()), 201

# 更新
@app.route('/inspirations/<int:iid>', methods=['PUT'])
def update_inspiration(iid):
    insp = Inspiration.query.get_or_404(iid)
    data = request.get_json()
    insp.title    = data.get('title', insp.title)
    insp.content  = data.get('content', insp.content)
    insp.priority = data.get('priority', insp.priority)
    insp.archived = data.get('archived', insp.archived)
    db.session.commit()
    return jsonify(insp.to_dict())

# 删除
@app.route('/inspirations/<int:iid>', methods=['DELETE'])
def delete_inspiration(iid):
    Inspiration.query.filter_by(id=iid).delete()
    db.session.commit()
    return '', 204

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
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
