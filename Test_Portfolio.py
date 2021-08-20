from Portfolio import make_portfolio, OptimizeMethod, AssetMethod


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
    test_custom_eff()
    test_custom_sharp()
    test_dual_eff()
    test_dual_sharp()
    test_instant_eff()
    test_instant_sharp()
    test_mo1_eff()
    test_mo1_sharp()
    test_mo3_eff()
    test_mo3_eff()
    test_up_eff()
    test_up_sharp()


def test_custom_eff():
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.CUSTOM
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3
    custom_assets = ['005930', '000660', '035720', '035420', '051910']

    make_portfolio(
        optimize=optimize_method,
        asset_method=asset_method,
        year=year,
        money=money,
        risk_limit=risk_limit,
        custom_assets=custom_assets
    )


def test_custom_sharp():
    optimize_method = OptimizeMethod.MaxSharp
    asset_method = AssetMethod.CUSTOM
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3
    custom_assets = ['005930', '000660', '035720', '035420', '051910']

    make_portfolio(
        optimize=optimize_method,
        asset_method=asset_method,
        year=year,
        money=money,
        risk_limit=risk_limit,
        custom_assets=custom_assets
    )


def test_dual_eff():
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.DUAL
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    make_portfolio(
        optimize=optimize_method,
        asset_method=asset_method,
        year=year,
        money=money,
        risk_limit=risk_limit,
    )


def test_dual_sharp():
    optimize_method = OptimizeMethod.MaxSharp
    asset_method = AssetMethod.DUAL
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    make_portfolio(
        optimize=optimize_method,
        asset_method=asset_method,
        year=year,
        money=money,
        risk_limit=risk_limit,
    )


def test_instant_eff():
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.SOARING
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    make_portfolio(
        optimize=optimize_method,
        asset_method=asset_method,
        year=year,
        money=money,
        risk_limit=risk_limit,
    )


def test_instant_sharp():
    optimize_method = OptimizeMethod.MaxSharp
    asset_method = AssetMethod.SOARING
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    make_portfolio(
        optimize=optimize_method,
        asset_method=asset_method,
        year=year,
        money=money,
        risk_limit=risk_limit,
    )


def test_mo1_eff():
    optimize_method = OptimizeMethod.Efficient
    asset_method = AssetMethod.MOMENTUM_1MONTH
    year = 3
    money = 15 * 1000000
    risk_limit = 0.3

    make_portfolio(
        optimize=optimize_method,
        asset_method=asset_method,
        year=year,
        money=money,
        risk_limit=risk_limit,
    )


def test_mo1_sharp():
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


def test_mo3_eff():
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

def test_mo3_sharp():
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


def test_up_eff():
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

def test_up_sharp():
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


if __name__ == '__main__':
    test()
