import requests, json


def test():
    url = 'http://localhost:15000/portfolio/efficient/momentum_1month'
    params = {
        'years': 3,
        'money': 15 * 1000000,
        'risk_limit': 0.3,
        'assets': ['202020', '004050']
    }
    response = requests.post(url, data=params)
    # response = requests.post(url, data=params)
    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    test()
