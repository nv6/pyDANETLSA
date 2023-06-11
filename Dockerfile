FROM python:slim-buster
WORKDIR /usr/src/app

COPY src/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/*.py .
COPY src/libs/*.py libs/

CMD ./monitor.py --fqdn smtp.koeroo.net --port 25 --protocol SMTP