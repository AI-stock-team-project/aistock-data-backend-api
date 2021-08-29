"""
만들어진 Flask API에 대한 성능 테스트.
"""
import requests, json


def test():
    url = 'http://localhost:15000/portfolio/efficient/custom'
    # url = 'http://localhost:15000/portfol22io'
    # url = 'http://localhost:15000/portfolio/effff'
    params = {
        'years': 3,
        'money': 15 * 1000000,
        'risk_limit': 0.3,
        'assets': ['005930', '000660', '035720', '035420', '051910']
    }
    response = requests.post(url, data=params)
    # response = requests.post(url, data=params)
    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    test()
