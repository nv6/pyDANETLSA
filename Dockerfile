FROM python:slim-buster

RUN apt-get update && apt-get -y install cron

WORKDIR /usr/src/app

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab

COPY src/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/*.py .
COPY src/libs/*.py libs/

# CMD ./monitor.py --fqdn smtp.koeroo.net --port 25 --protocol SMTP
CMD ["cron", "-f"]