# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from api_portfoilo import ApiPortfolio

app = Flask(__name__)  # Flask 객체 선언.
# Flask 객체에 Api 객체 등록
api = Api(
    app,
    version='0.1',
    title="Aistock's API Server",
    description=""
)

api.add_namespace(ApiPortfolio, '/portfolio')


@api.route('/hello')
class HelloWorld(Resource):

    # noinspection PyMethodMayBeStatic
    def get(self):
        return {"hello": "world!"}

    # noinspection PyMethodMayBeStatic
    def post(self):
        return {"hello": "world!", "method": "post"}


@api.route('/test2')
class Test2(Resource):
    @api.doc(params={'name': '파라미터 테스트 값 입력..'})
    def get(self):
        # name = request.json.get('name')
        name = request.args.get('name')
        return {"message": "test2", "name": name}

    @api.param('name', '파라미터 테스트 값 입력..')
    @api.param('name2', '파라미터 테스트 값 입력...')
    @api.response(404, 'not found')
    def post(self):
        """post 방식의 테스트 api 입니다."""
        name = request.args.get('name')
        return {"message": "test2", "method": "post", "name": name}


# flask run -p 5000
if __name__ == '__main__':
    app.run(debug=True)
    # app.run('0.0.0.0', port=5000, debug=True)
