FROM python:3.9.6-buster AS builder
COPY requirements.txt .

# requirements.txt를 복사함. 
RUN pip install --user -r requirements.txt

# slim-buster 는 데비안의 경량화 버전을 말함
FROM python:3.9.6-slim-buster

# wget (dockerize에 필요) 설치, cron (스케쥴링) 설치
RUN  apt-get update \
    && apt-get install -y wget cron \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# DB 연결에 대기시킬 수 있는 기능을 하는 Dockerize 를 이용
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# pip 패키지 복사
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# requirements.txt 를 먼저 복사함. 
# COPY requirements.txt .

# pip 의존성 설치
# RUN pip install -r requirements.txt

# cron 스케쥴링 추가
# RUN echo "*/30 * * * * /bin/sh nobody -c 'cd /app && /usr/bin/git pull -q origin develop' >> /var/log/cron.log 2>&1" | crontab -
#
ADD cronjob.sh /etc/cron.d/aistock-cron
RUN chmod 0644 /etc/cron.d/aistock-cron
RUN touch /var/log/cron.log

# RUN touch /etc/crontab /etc/cron.*/*
# RUN service cron start

# working dir
WORKDIR /app

# ENTRYPOINT [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
CMD /usr/sbin/cron -f