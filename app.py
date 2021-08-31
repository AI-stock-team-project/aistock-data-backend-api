# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request, send_from_directory
from flask_restx import Api, Resource
from flask_cors import CORS

from api_portfoilo import ApiPortfolio
from api_strategy_rank import api_strategy_rank
from api_lstm import api_lstm

app = Flask(__name__, static_url_path='/static')  # Flask 객체 선언.

# ajax를 위한 CORS 허용
CORS(app)

# Flask 객체에 Api 객체 등록
api = Api(
    app,
    version='0.2',
    title="Aistock's API Server",
    description=""
)

api.add_namespace(ApiPortfolio, '/portfolio')
api.add_namespace(api_strategy_rank, '/strategy_rank')
api.add_namespace(api_lstm, '/lstm')


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


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify(error=str(e)), 404


# flask run -p 5000
if __name__ == '__main__':
    app.run(debug=True)
    # app.run('0.0.0.0', port=5000, debug=True)
