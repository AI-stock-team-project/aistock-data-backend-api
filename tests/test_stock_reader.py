import aistock.StockReader as StockReader


def test():
    df = StockReader.read_index_by('kospi', '2021-08-01', '2021-08-10')
    print(df)


if __name__ == '__main__':
    test()
