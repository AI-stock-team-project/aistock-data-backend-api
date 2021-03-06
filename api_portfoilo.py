# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request, abort
from flask_restx import Resource, Namespace

from portfolio.Portfolio import make_portfolio, OptimizeMethod, AssetMethod, get_assets

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
        is_debug = False

        # 최적화 방법
        optimize_method = OptimizeMethod.Efficient  # 기본값
        if optimize == 'efficient':
            optimize_method = OptimizeMethod.Efficient
        elif optimize == 'maxsharpe':
            optimize_method = OptimizeMethod.MaxSharpe
        else:
            abort(404)

        # 주식 종목 선택 방법
        _asset_method = AssetMethod.DUAL_MOMENTUM  # 기본값
        if asset_method == 'custom':
            _asset_method = AssetMethod.CUSTOM
        elif asset_method == 'dual_momentum':
            _asset_method = AssetMethod.DUAL_MOMENTUM
        elif asset_method == 'momentum_1month':
            _asset_method = AssetMethod.MOMENTUM_1MONTH
        elif asset_method == 'momentum_3month':
            _asset_method = AssetMethod.MOMENTUM_3MONTH
        elif asset_method == 'soaring':
            _asset_method = AssetMethod.SOARING
        elif asset_method == 'up_freq':
            _asset_method = AssetMethod.UP_FREQ
        else:
            abort(404)

        # return { "optimize": optimize, "method": asset_method }

        # params = request.json
        # return {'assetss':request.values.getlist('assets') }

        params = request.values
        # 투자 기간
        years = params.get('years', 1, int)
        # 투자 금액
        money = params.get('money', 15 * 1000000, int)
        # 감당 리스크
        risk_limit = params.get('risk_limit', 0.3, float)
        # assets
        custom_assets = params.getlist('assets')  # list형으로 반환됨.

        print(f"""
        [ api portfolio call ]
        optimize method : {optimize_method}
        asset method : {asset_method}
        money : {money}
        years : {years}
        risk_limit : {risk_limit}
        """)
        # assets = ['005930', '000660', '035720', '035420', '051910']
        assets = get_assets(_asset_method, custom_assets)

        if len(assets) == 0:
            abort(400)

        if not is_debug:
            rv, df = make_portfolio(
                optimize_method=optimize_method,
                asset_method=_asset_method,
                years=years,
                money=money,
                risk_limit=risk_limit,
                assets=assets
            )

            # return {'result': rv, 'result_df': df.to_json()}
            return {'result': rv, 'result_df': df.to_dict(orient='records')}
        else:
            rv = {'expected_annual_return': 0.60400610535409, 'annual_volatility': 0.3000171478073243, 'sharpe_ratio': 1.946575752827128, 'balance': 56700.0}
            df = [
                {"name": "NAVER", "symbol": "035420", "number": 30.0, "money": 12600000.0, "weight": 0.8431872478},
                {"name": "\uc0bc\uc131\uc804\uc790", "symbol": "005930", "number": 21.0, "money": 1560300.0,
                 "weight": 0.1044146875}
            ]
            return {'result': rv, 'result_df': df}
