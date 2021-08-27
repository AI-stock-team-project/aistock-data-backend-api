# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request
from flask_restx import Resource, Namespace

from portfolio.Portfolio import make_portfolio, OptimizeMethod, AssetMethod

ApiPortfolio = Namespace('api_portfoilo')


@ApiPortfolio.route('/<string:optimize>/<string:asset_method>')
class MakePortfolio(Resource):
    @ApiPortfolio.doc(params={
        'optimize': '포트폴리오 최적화 방법 선택',
        'asset_method': '종목 가져오는 방법 선택',
        'years': '투자 기간',
        'money': '투자 금액',
        'risk_limit': '감당 리스크',
        'custom_assets': '종목 선택시 종목'
    })
    def post(self, optimize, asset_method):
        """전략형 포트폴리오를 구성합니다."""
        # return { "optimize": optimize, "method": asset_method }

        # params = request.json
        # return {'assetss':request.values.getlist('assets') }

        params = request.values
        years = params.get('years', 1, int)
        money = params.get('money', 15 * 1000000, int)
        risk_limit = params.get('risk_limit', 0.3, float)
        assets = params.get('assets')

        if optimize == 'efficient':
            optimize_method = OptimizeMethod.Efficient
        elif optimize == 'maxsharp'
        asset_method = AssetMethod.CUSTOM
        # year = 3
        # money = 15 * 1000000
        # risk_limit = 0.3
        custom_assets = ['005930', '000660', '035720', '035420', '051910']

        """
        make_portfolio(
            optimize_method=optimize_method,
            asset_method=asset_method,
            years=years,
            money=money,
            risk_limit=risk_limit,
            custom_assets=custom_assets
        )
        """

        return {"hello": "world!"}
