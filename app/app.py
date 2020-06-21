import argparse
import os
from flask import Flask
from flask import request
from markupsafe import escape
import functions as F


var_path = os.path.abspath(os.path.dirname(__file__)) + '../var/'
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/user/')
@app.route('/user/<user_name>')
def hello_user(user_name=None):
    # `user_name=None` 으로 초기화를 하면 위의 두 route 를 모두 이용 가능
    # user_name 의 초기값이 지정되지 않으면 `@app.route('/user/<user_name>')` 만 이용 가능
    if (user_name is None):
        return 'Hello, annonymous'
    return f'Hello, {escape(user_name)}'


@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    a = int(a)
    b = int(b)
    # return type must be `str`
    return str(a + b)


@app.route('/external_add/<int:a>/<int:b>')
def external_add(a, b):
    a = int(a)
    b = int(b)
    # return type must be `str`
    return str(F.external_add(a, b))


@app.route('/add_get/')
def add_get():
    print(type(request.args))  # <class 'werkzeug.datastructures.ImmutableMultiDict'>
    print(request.args)        # ImmutableMultiDict([('a', '3'), ('b', '5')])
    a = int(request.args.get('a', '0'))
    b = int(request.args.get('b', '0'))
    return str(a + b)


@app.route('/hello_user_post/', methods=['POST'])
def hello_user2():
    # request.form    # form value in HTML
    # request.files   # attached files
    # requests.json   # parsed JSON format data
    # requests.json == request.get_json(force=True)
    print(request.json)
    print(request.get_json(force=True))

    json_data = request.get_json(force=True)
    name = json_data.get('name', 'annonymous')
    koname = json_data.get('ko_name', '익명자')
    return f'{name} ({koname})'

# def dynamic_method():
#    if request.method == 'get':
#    if request.method == 'post':

@app.route('/return_json/', methods=['POST'])
def return_json():
    json_data = request.get_json(force=True)
    name = json_data.get('name', 'annonymous')
    koname = json_data.get('ko_name', '익명자')

    response = {
        'concatenated_name': f'{name} ({koname})'
    }
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Flask option arguments')
    parser.add_argument('--host', type=str, default=None, help='Default is localhost')
    parser.add_argument('--port', type=int, default=None, help='Default is :5000')

    args = parser.parse_args()
    host = args.host
    port = args.port

    print('Flask practice')
    app.run(host=host, port=port)
