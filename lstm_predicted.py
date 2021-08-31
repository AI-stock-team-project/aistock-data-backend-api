from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import numpy as np
import matplotlib.pyplot as plt
import FinanceDataReader as fdr
from datetime import datetime
from pathlib import Path


# noinspection PyPep8Naming
def MinMaxScaler(data):
    """최솟값과 최댓값을 이용하여 0 ~ 1 값으로 변환"""
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # 0으로 나누기 에러가 발생하지 않도록 매우 작은 값(1e-7)을 더해서 나눔
    return numerator / (denominator + 1e-7)


def stock_prediction(ticker, start_date, end_date=datetime.now().strftime('%Y-%m-%d')):
    raw_df = fdr.DataReader(ticker, start_date, end_date)
    window_size = 10
    data_size = 5
    dfx = raw_df[['Open', 'High', 'Low', 'Volume', 'Close']]
    dfx = MinMaxScaler(dfx)
    dfy = dfx[['Close']]

    x = dfx.values.tolist()
    y = dfy.values.tolist()

    data_x = []
    data_y = []
    for i in range(len(y) - window_size):
        _x = x[i: i + window_size]  # 다음 날 종가(i+windows_size)는 포함되지 않음
        _y = y[i + window_size]     # 다음 날 종가
        data_x.append(_x)
        data_y.append(_y)
    # noinspection PyUnboundLocalVariable
    print(_x, "->", _y)

    train_size = int(len(data_y) * 0.7)
    train_x = np.array(data_x[0: train_size])
    train_y = np.array(data_y[0: train_size])

    # noinspection PyUnusedLocal
    test_size = len(data_y) - train_size
    test_x = np.array(data_x[train_size: len(data_x)])
    test_y = np.array(data_y[train_size: len(data_y)])

    # 모델 생성
    model = Sequential()
    model.add(LSTM(units=10, activation='relu', return_sequences=True, input_shape=(window_size, data_size)))
    model.add(Dropout(0.1))
    model.add(LSTM(units=10, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(units=1))
    model.summary()

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(train_x, train_y, epochs=60, batch_size=32)
    pred_y = model.predict(test_x)

    # Visualising the results
    # 경로
    static_path = Path(__file__).resolve().parent / 'static'
    static_url = '/static/'
    # 파일명
    dt_now = datetime.now().strftime('%Y%m%d_%H%M%S')
    image_file_name = f'return_lstm_{dt_now}.png'
    image_file_path = static_path / image_file_name
    image_file_url = static_url + image_file_name
    
    plt.figure()
    plt.plot(test_y, color='red', label='real SEC stock price')
    plt.plot(pred_y, color='blue', label='predicted SEC stock price')
    plt.title('SEC stock price prediction')
    plt.xlabel('time')
    plt.ylabel('stock price')
    plt.legend()
    plt.show()
    # 이미지 저장
    plt.savefig(image_file_path, dpi=100)

    result_close_price = float(raw_df.Close[-1] * pred_y[-1] / dfy.Close[-1])  # 내일 종가
    return {
        'close_price': result_close_price,
        'graph_url': image_file_url
    }
