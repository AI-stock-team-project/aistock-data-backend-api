"""
포트폴리오를 만드는 기능에 대한 테스트.

잘 호출하고, DataFrame으로 리턴받아서, 원하는 결과가 나오는지 확인하는 부분.
"""
from portfolio.Portfolio import make_portfolio, OptimizeMethod, AssetMethod, get_assets


def test():
    """
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.DUAL
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3
    # custom_assets = ['005930', '000660', '035720', '035420', '051910']

    # print(asset_method)

    make_portfolio(
        optimize=optimize_method,
        asset_method=asset_method,
        year=year,
        money=money,
        risk_limit=risk_limit,
        # custom_assets=custom_assets
    )
    """
    # a = AssetMethod.DUAL
    # print(a)

    test_custom_eff()
    # test_custom_sharpe()
    # test_dual_eff()
    # test_dual_sharpe()
    # test_instant_eff()
    # test_instant_sharpe()
    # test_mo1_eff()
    # test_mo1_sharpe()
    # test_mo3_eff()
    # test_mo3_sharpe()
    # test_up_eff()
    # test_up_sharpe()


def test_custom_eff():
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.CUSTOM
    year = 1
    money = 15 * 1000000
    risk_limit = 0.3
    custom_assets = ['005930', '000660', '035720', '035420', '051910']

    assets = get_assets(asset_method, custom_assets)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    print(rv)
    # print(df)
    print(df.to_json(orient='records'))


def test_custom_sharpe():
    optimize_method = OptimizeMethod.MaxSharpe
    asset_method = AssetMethod.CUSTOM
    year = 1
    money = 15 * 1000000
    risk_limit = 0.3
    custom_assets = ['005930', '000660', '035720', '035420', '051910']

    assets = get_assets(asset_method, custom_assets)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


def test_dual_eff():
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.DUAL_MOMENTUM
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    assets = get_assets(asset_method)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


def test_dual_sharpe():
    optimize_method = OptimizeMethod.MaxSharpe
    asset_method = AssetMethod.DUAL_MOMENTUM
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    assets = get_assets(asset_method)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


def test_instant_eff():
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.SOARING
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    assets = get_assets(asset_method)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


def test_instant_sharpe():
    optimize_method = OptimizeMethod.MaxSharpe
    asset_method = AssetMethod.SOARING
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    assets = get_assets(asset_method)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


def test_mo1_eff():
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.MOMENTUM_1MONTH
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    assets = get_assets(asset_method)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


def test_mo1_sharpe():
    optimize_method = OptimizeMethod.MaxSharpe
    asset_method = AssetMethod.MOMENTUM_1MONTH
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    assets = get_assets(asset_method)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


def test_mo3_eff():
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.MOMENTUM_3MONTH
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    assets = get_assets(asset_method)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


def test_mo3_sharpe():
    optimize_method = OptimizeMethod.MaxSharpe
    asset_method = AssetMethod.MOMENTUM_3MONTH
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    assets = get_assets(asset_method)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


def test_up_eff():
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.UP_FREQ
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    assets = get_assets(asset_method)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


def test_up_sharpe():
    optimize_method = OptimizeMethod.MaxSharpe
    asset_method = AssetMethod.UP_FREQ
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    assets = get_assets(asset_method)

    rv, df = make_portfolio(
        optimize_method=optimize_method,
        asset_method=asset_method,
        years=year,
        money=money,
        risk_limit=risk_limit,
        assets=assets
    )
    # print(rv)
    print(df.to_json())


if __name__ == '__main__':
    test()
