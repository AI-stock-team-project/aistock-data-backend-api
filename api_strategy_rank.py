from flask_restx import Resource, Namespace

import aistock.StrategyStock as StrategyStock

api_strategy_rank = Namespace('api_strategy_rank')


def convert_df(df):
    df = df[['ticker', 'rank']]
    return df.to_dict(orient='records')


@api_strategy_rank.route('/')
class ApiStrategyTopRank(Resource):
    @api_strategy_rank.doc()
    def post(self):
        """전략형 포트폴리오를 구성합니다."""
        # is_debug = False

        mo_1 = StrategyStock.retrive_strategy_stocks_rank('mo_1')
        mo_3 = StrategyStock.retrive_strategy_stocks_rank('mo_3')
        soaring = StrategyStock.retrive_strategy_stocks_rank('soaring')
        up_freq = StrategyStock.retrive_strategy_stocks_rank('up_freq')
        dual_mo = StrategyStock.retrive_strategy_stocks_rank('dual_mo')

        return {
            'mo_1': convert_df(mo_1),
            'mo_3': convert_df(mo_3),
            'soaring': convert_df(soaring),
            'up_freq': convert_df(up_freq),
            'dual_mo': convert_df(dual_mo),
        }
