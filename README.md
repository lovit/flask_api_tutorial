# Flask 를 이용하여 API 만들기

## REST API

REpresentational State Transfer (REST) API 의 약어로, Uniform Resource Identifier (URI) 를 통하여 자연을 명시하고, 처리된 결과를 보통 JSON 이나 XML 로 return 한다.
보통 Uniform Resource Locator (URL) 은 자원의 위치를 나타내지만, URI 는 그 안에 데이터 정보가 포함된다.
자원의 위치도 데이터 정보이기 때문에 URI 가 URL 을 포함하는 더 큰 단위의 개념이다.

`GET` 은 URI 에 패러매터를 추가하여 요청하는 방식으로, query string 에 그 값을 추가한다.
`https://127.0.0.1:5000/test?name=lovit&koname=%EA%B9%80%ED%98%84%EC%A4%91'` 에서 `?` 뒤의 부분이 query string 이다.
마치 데이터베이스에서 어떤 값을 조회하기 위한 attributes 를 입력하는 구조인데, 이는 `GET` 이 서버로부터 값을 조회하기 위해 만들어졌기 때문이다.

## URL encoding

URL 은 ASCII 로만 기술할 수 있으며, ASCII 에 포함되지 않는 언어와 특수문자를 표현하기 위해 URL Encoding 을 이용한다.
즉 non-ASCII 글자들을 적절히 변형해야 하는데, `%EA` 처럼 `%` 다음의 16진수로 이 값들을 나타낸다.

```python
import urllib.parse
params = {'name': 'lovit', 'koname': '김현중'}
data = urllib.parse.urlencode(params, doseq=True)
print(data)
```

```
'name=lovit&koname=%EA%B9%80%ED%98%84%EC%A4%91'
```

non-ASCII 에 대한 인코딩 방식을 설정할 수 있는데, 기본값 `None` 은 `encoding='utf-8'` 이다.
만약 이 값을 `cp949` (처음 파이썬으로 한글을 접할 때 맨붕을 일으키는 그..) 를 이용하여 URL 로 변경한다면 다음과 같은 값이 된다.
그 외 더 많은 사용 가능한 인코딩은 [Python docs](https://docs.python.org/2.4/lib/standard-encodings.html) 에서 확인할 수 있다.

```python
urllib.parse.urlencode(params, doseq=True, encoding='cp949')
```

```
'name=lovit&koname=%B1%E8%C7%F6%C1%DF'
```

## URL decoding

ASCII 로 기술된 값을 본래의 encoding 으로 되돌릴 수 있다.
앞서 ASCII 로 변경한 `data` 를 다시 `utf-8` 로 변경하면 다음의 값을 얻을 수 있다.
그러나 `urllib.parse.unquote` 함수는 인코딩만 변경할 뿐, query string 을 파싱을 하지는 않는다.
이를 위해서는 `urllib.parse.parse_qs` 함수를 이용한다.
단 주의할 점은 `str` 의 값도 query string parsing 을 거치면 `list of str` 으로 반환된다.

```python
decoded_data = urllib.parse.unquote(data, encoding='utf-8')
print(decoded_data)

parsed_data = urllib.parse.parse_qs(decoded_data)
print(parsed_data)
```

```
'name=lovit&koname=김현중'
{'name': ['lovit'], 'koname': ['김현중']}
```

사실 `utf-8` 에는 ASCII 가 포함되어 있기 때문에 위의 두 단계의 과정을 한번에 해결할 수도 있다.
하지만 `data` 를 `ASCII` 로 파싱하면 잘못된 결과가 출력된다.

```python
print(urllib.parse.unquote(data))
print(urllib.parse.unquote(data, encoding='utf-8'))
print(urllib.parse.unquote(data, encoding='ASCII'))
```

```
{'name': ['lovit'], 'koname': ['김현중']}
{'name': ['lovit'], 'koname': ['김현중']}
{'name': ['lovit'], 'koname': ['���������']}
```

`GET` 으로 URL 을 받은 뒤, `?` 로 split 한 뒤, query string 을 값으로 복원하는 과정까지 살펴보았다.

## Flask app

`app.py`

```python
from flask import Flask
from flask import request


var_path = os.path.abspath(os.path.dirname(__file__)) + '../var/'
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()
```

```
$ python app.py

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Data in URL

`app.py`

```python
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
```

IPython notebook 을 하나 켠다.

`agent.ipynb`

```python
import requests

get_url = 'http://127.0.0.1:5000/add/3/5'
response = requests.get(url=get_url)
print(response.status_code)  # 200
print(response.text)         # 8
```

## Package import

`functions.py` 파일에 다음의 함수를 구현해둔다.

```python
def external_add(a: int, b: int):
    print('called external function')
    return a + b
```

```python
import functions as F

@app.route('/external_add/<int:a>/<int:b>')
def external_add(a, b):
    a = int(a)
    b = int(b)
    # return type must be `str`
    return str(F.external_add(a, b))
```

## GET

`app.py`

```python
@app.route('/add_get/')
def add_get():
    print(type(request.args))  # <class 'werkzeug.datastructures.ImmutableMultiDict'>
    print(request.args)        # ImmutableMultiDict([('a', '3'), ('b', '5')])
    a = int(request.args.get('a', '0'))
    b = int(request.args.get('b', '0'))
    return str(a + b)
```

`agent.ipynb`

```python
import requests

get_url = 'http://127.0.0.1:5000/add_get?a=3&b=5'
response = requests.get(url=get_url)
print(response.status_code)  # 200
print(response.text)         # 8
```


## POST

`GET` 방법은 긴 데이터를 입력하는데 적절하지 않을 수도 있다.
`POST` 는 HTTP Body 에 데이터를 추가하여 요청하는 방식으로, 길이의 제한이 없기 때문에 훨씬 많은 양의 데이터를 서버로 보낼 수 있다.
또한 URL 에 직접 데이터를 입력하지 않기 때문에 URL 에 민감한 값들이 보이지 않는 장점도 있다.

`POST` 는 서버에서 리소스의 값을 생성/변경하기 위해 만들어진 방법이다.
그렇기 때문에 `GET` 은 항상 같은 결과값을 출력 (idempotent) 하는데 반하여, `POST` 는 실행 순서에 따라 다른 값이 출력될 수도 (non-idempotent) 있다.
예를 들어 특정 값을 데이터베이스에 추가한다면, 서버의 리소스가 변경되기 때문이다.
대표적인 예시로 게시판의 글을 웹서버 데이터베이스에 입력하는 행위는 `POST` 이다.

`app.py`

```python
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
```

`agent.ipynb`

```python
# data: list of tuple, bytes or file-like
# json: json data to send in the body
json_data = {'name': 'lovit', 'ko_name': '김현중'}
post_url = 'http://127.0.0.1:5000/hello_user_post'
response = requests.post(url=post_url, json=json_data)
print(response.status_code)  # 200
print(response.text)         # lovit (김현중)
```

## Return as JSON

`app.py`

```python
@app.route('/return_json/', methods=['POST'])
def return_json():
    json_data = request.get_json(force=True)
    name = json_data.get('name', 'annonymous')
    koname = json_data.get('ko_name', '익명자')

    response = {
        'concatenated_name': f'{name} ({koname})'
    }
    return response
```

`agent.ipynb`

```python
import json

json_data = {'name': 'lovit', 'ko_name': '김현중'}
url = 'http://127.0.0.1:5000/return_json'
response = requests.post(url=url, json=json_data)
print(response.status_code)       # 200
print(response.text.strip())      # {"concatenated_name":"lovit (\uae40\ud604\uc911)"}
print(json.loads(response.text))  # {'concatenated_name': 'lovit (김현중)'}
```

## Run server with specific IP and port

`app.py`

```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Flask option arguments')
    parser.add_argument('--host', type=str, default=None, help='Default is localhost')
    parser.add_argument('--port', type=int, default=None, help='Default is :5000')

    args = parser.parse_args()
    host = args.host
    port = args.port

    print('Flask practice')
    app.run(host=host, port=port)
```

```
$ python app.py --port 5050

Flask practice
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5050/ (Press CTRL+C to quit)
```

Localhost 로 실행할 때는 `run(host=None)` 혹은 `run(host='0.0.0.0')` 으로 실행합니다.
할당된 고정 IP, 'abc.def.ghi.jkh' 로 실행할 때는 `run(host='abc.def.ghi.jkh')` 혹은 `run(host='0.0.0.0')` 으로 실행합니다.

```
$ python app.py --host 0.0.0.0 --port 5050
```

## More

- 웹페이지에서 데이터 받아 처리하는 걸로 만들기
  - https://medium.com/@mystar09070907/%EC%9B%B9-%ED%8E%98%EC%9D%B4%EC%A7%80-client-%EC%97%90%EC%84%9C-%EC%A0%95%EB%B3%B4-%EB%B3%B4%EB%82%B4%EA%B8%B0-bf3aff952d3d
- file upload example
  - https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
