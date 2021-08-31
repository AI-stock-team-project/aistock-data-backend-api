# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request, abort
from flask_restx import Resource, Namespace
from lstm_predicted import stock_prediction

api_lstm = Namespace('api_lstm')


@api_lstm.route('/predict_close_price/<stock_symbol>')
class PredictClosePriceByLSTM(Resource):
    @api_lstm.doc(params={
        'stock_symbol': '종목 코드',
        'start_date': '주가데이터 참조 시작일자 (yyyy-mm-dd)'
    })
    def post(self, stock_symbol):
        """전략형 포트폴리오를 구성합니다."""
        is_debug = False

        params = request.values
        # 시작 일자
        start_date = params.get('start_date', '2018-01-01', str)

        print(f"""
        [ api lstm/predict_close_price call ]
        stock_symbol : {stock_symbol}
        start_date : {start_date}
        """)

        if not is_debug:
            prediction_result = stock_prediction(stock_symbol, start_date)

            # return {'result': rv, 'result_df': df.to_json()}
            return {
                'predict_close_price': prediction_result['close_price'],
                'graph_url': prediction_result['graph_url'],
                'param_stock_symbol': stock_symbol
            }
        else:
            return {'predict_close_price': 123456, 'param_stock_symbol': stock_symbol}
