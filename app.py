import os
import requests
from flask import Flask, request, jsonify, g
from models import db, User, Inspiration

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///inspiration.db')
db.init_app(app)

# with app.app_context():
# db.create_all()

# 小程序端把 code 发来，后端换 session_key → openid
@app.route('/auth/code2session', methods=['POST'])
def code2session():
    print('Headers:', request.headers)
    print('Body:', request.get_data(as_text=True))
    print('JSON:', request.get_json(silent=True))

    code = (request.json or {}).get('code') \
        or request.form.get('code') \
        or request.args.get('code')

    if not code:
        return jsonify({"errmsg": "缺少用户标识"}), 401

    # TODO: 用 code 调微信接口，拿到真实的 openid/session_key
    return jsonify({"openid": "fake_openid", "session_key": "fake_key"})

@app.route('/login', methods=['POST'])
def login():
    code = request.json.get('code')
    if not code:
        return jsonify({'errmsg': '缺少 code'}), 400

    # 使用云托管环境变量注入的 appid 和 secret
    appid = os.environ['APPID']
    secret = os.environ['APPSECRET']

    # 修正1: 修复缩进问题并优化URL格式
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'

    wx_resp = requests.get(url, timeout=5).json()
    if 'openid' not in wx_resp:
        return jsonify({'errmsg': wx_resp.get('errmsg', 'wx error')}), 400

    openid = wx_resp['openid']
    user = User.query.get(openid)
    if not user:
        user = User(id=openid, nickname=request.json.get('nickname', ''))
        db.session.add(user)
        db.session.commit()
    return jsonify({'openid': openid})

# 统一把 openid 放到 g.user_id


@app.before_request
def set_user():
    # 修正2: 排除/login路由，否则/login请求会被拦截
    if request.path == '/login':
        return

    g.user_id = request.headers.get('X-User-Id')
    if not g.user_id:
        return jsonify({'errmsg': '缺少用户标识'}), 401

# 所有 CRUD 都加 user 过滤


@app.route('/inspirations')
def list_inspirations():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    query = Inspiration.query.filter_by(user_id=g.user_id)\
        .order_by(Inspiration.created_at.desc())\
        .paginate(page=page, per_page=size, error_out=False)
    return jsonify({'items': [i.to_dict()
                   for i in query.items], 'total': query.total})

# 新增记录


@app.route('/inspirations', methods=['POST'])
def add_inspiration():
    data = request.get_json()
    insp = Inspiration(
        user_id=g.user_id,
        title=data['title'],
        content=data.get('content', ''),
        priority=data.get('priority', 3)
    )
    db.session.add(insp)
    db.session.commit()
    return jsonify(insp.to_dict()), 201

# 删除


@app.route('/inspirations/<int:iid>', methods=['DELETE'])
def delete_inspiration(iid):
    # 修正3: 使用更安全的删除方式
    insp = Inspiration.query.filter_by(id=iid, user_id=g.user_id).first()
    if not insp:
        return jsonify({'errmsg': '记录不存在'}), 404

    db.session.delete(insp)
    db.session.commit()
    return '', 204


@app.route('/inspirations/<int:iid>', methods=['PUT'])
def update_inspiration(iid):
    insp = Inspiration.query.filter_by(
        id=iid, user_id=g.user_id).first_or_404()
    data = request.get_json()
    for k in ['title', 'content', 'priority', 'archived']:
        if k in data:
            setattr(insp, k, data[k])
    db.session.commit()
    return jsonify(insp.to_dict())

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
