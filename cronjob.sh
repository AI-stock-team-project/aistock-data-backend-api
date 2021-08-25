# 평일 새벽 3시. 종목 테이블 갱신
0 3 * * 1-5 root python /app/update_stock_table.py >> /var/log/cron.log 2>&1

# 매일 새벽 4시. 주가 테이블 갱신
0 4 * * 1-5 root python /app/update_stock_price.py >> /var/log/cron.log 2>&1

