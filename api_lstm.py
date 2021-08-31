# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request, abort
from flask_restx import Resource, Namespace

from portfolio.Portfolio import make_portfolio, OptimizeMethod, AssetMethod, get_assets
from lstm_predicted import stock_prediction

ApiPortfolio = Namespace('api_portfoilo')


@ApiPortfolio.route('/<stock_symbol>')
class PredictClosePriceByLSTM(Resource):
    @ApiPortfolio.doc(params={
        'stock_symbol': '종목 코드',
        'start_date': '주가데이터 참조 시작일자 (yyyy-mm-dd)',
        'years': '투자 기간',
        'money': '투자 금액',
        'risk_limit': '감당 리스크',
        'custom_assets': '종목 선택시 종목'
    })
    def post(self, stock_symbol):
        """전략형 포트폴리오를 구성합니다."""
        is_debug = False

        params = request.values
        # 시작 일자
        start_date = params.get('start_date', '2018-01-01', str)

        print(f"""
        [ api api_lstm call ]
        stock_symbol : {stock_symbol}
        start_date : {start_date}
        """)

        if not is_debug:
            predicted = stock_prediction(stock_symbol, start_date)
            # return {'result': rv, 'result_df': df.to_json()}
            return {'predict_close_price': predicted, 'param_stock_symbol': stock_symbol}
        else:
            return {'predict_close_price': 123456, 'param_stock_symbol': stock_symbol}
