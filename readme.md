# 개요

기존의 data-api 와 portfolioOpt 를 병합.

일 단위로 스크립트를 실행하거나, 시간 단위로 스크립트를 실행하는 등의 부분 추가.


# 기능 개요
1. 일, 특정 시간 단위의 스크립트 실행
2. 포트폴리오 만들기 시 결과를 api 로 리턴
3. 메인웹의 mysql에 데이터를 배치 처리


# 설치되는 패키지

패키지 목록
1. `pip install PyPortfolioOpt` : cvxpy, numpy, pandas, scipy
2. `pip install matplotlib` : cycler, kiwisolver, numpy, pillow, pyparsing, python-dateutil
3. ~`pip install scikit-learn`~ : 
4. `pip install finance-datareader` : lxml, pandas, requests, requests-file, tqdm
5. `pip install pykrx` : datetime, deprecated, numpy, pandas, requests, xlrd
6. `pip install beautifulsoup4` : soupsieve
    * finance-datareader 에서 필요로 함.
8. `pip install mysql-connector-python sqlalchemy`
   - mysql-connector-python : protobuf
   - sqlalchemy : greenlet
9. `pip install flask-restx` : ansio8601, Flask, jsonschema, pytz, six, werkzeug


# Docker 생성 및 컨테이너 실행
```console
docker build --force-rm --no-cache -t aistock-stockdata-api .
docker run --env-file ./.local.env --name aistock-stockdata-api -d -p 26000:5000 -v "%cd%:/app" aistock-stockdata-api
```


기존에 만든 것이 있었다면 중간에 rm 을 먼저 한 번 해주고 실행한다.
```console
docker rm -f aistock-stockdata-api

docker build --force-rm --no-cache -t aistock-stockdata-api .
docker run --env-file ./.local.env --name aistock-stockdata-api -d -p 26000:5000 -v "%cd%:/app" aistock-stockdata-api
```


