#!/bin/bash

# 이 스크립트는 docker-compose 로 구성하였을 때에 사용되는 스크립트입니다.
# 단순 도커 이용시에는 사용하지 않습니다.

# db 서버 기다리기
echo "wait db server"
dockerize -wait tcp://db:3306 -timeout 20s

# web 서버 기다리기
echo "wait web server"
dockerize -wait tcp://data-api:5000 -timeout 20s

# create stock data
python update_stock_table.py

# 주가 정보 가져오기 (기본값만)
python import_stock_prices.py

# 주가 정보 가져오기 (최근 것까지)
python update_stock_price.py

# echo "run django server"
# python manage.py runserver 0.0.0.0:8000
python -m flask run --host=0.0.0.0