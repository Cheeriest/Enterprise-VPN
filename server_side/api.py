from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os, json


app = Flask(__name__)
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'database.db')
db = SQLAlchemy(app)
app.config['PROXY_IP'] = '192.168.1.107'
app.config['PROXY_PORT'] = 50002




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    report_type = db.Column(db.String(50))
    report_data = db.Column(db.String(100))
    

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print data
            current_user = User.query.filter_by(public_id=data['public_id']).first()
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message' : 'Token is Out of date. Please get a new one'}), 401
        
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/log', methods=['GET', 'POST'])
@token_required
def print_vpn_traffic(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    if request.method == 'POST':
        data = request.get_json()
        new_report = Report(public_id=str(uuid.uuid4()), name=data['name'], report_type=data['report_type'], report_data=data['report_data'])
        db.session.add(new_report)
        db.session.commit()
        return jsonify({'message' : 'New Report Added!'})
        
    elif request.method == 'GET':
        reports = Report.query.all()
        output = []
        for report in reports:
            report_dict = {}
            report_dict['public_id'] = report.public_id
            report_dict['name'] = report.name
            report_dict['report_type'] = report.report_type
            report_dict['report_data'] = report.report_data
            output.append(report_dict)
        
        return jsonify({'reports' : output})

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    #if not current_user.admin:
    #    return jsonify({'message' : 'Cannot perform that function!'})

    users = User.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user=None):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})

@app.route('/user/<public_id>', methods=["DELETE"])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})


@app.route('/vpn', methods = ['GET'])
@token_required
def get_proxy(current_user):
    print current_user
    return jsonify({'ip': app.config['PROXY_IP'], 'port': app.config['PROXY_PORT']})

@app.route('/check_token', methods = ['POST'])
def check_token():
    token = request.get_json().get('token')
    try: 
        data = jwt.decode(token, app.config['SECRET_KEY'])
        return jsonify({'Valid' : 'True'}), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'Valid' : 'False'}), 200

    except:
        return jsonify({'Valid' : 'False'}), 200

@app.route('/login', methods= ['POST', 'GET'])
def login():
    
    auth = request.get_json()
    print type(auth)
    
    if not auth or not auth['name'] or not auth['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth['name']).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.now() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
def main():
    app.run(debug=True)# ssl_context = ('cert.pem', ))    

if __name__ == '__main__':
    main()
    
