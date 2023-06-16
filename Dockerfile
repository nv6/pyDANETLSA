FROM python:slim-buster

RUN apt-get update && apt-get -y install rsyslog

WORKDIR /usr/src/app

COPY src/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/*.py .
COPY src/libs/*.py libs/

RUN echo '*.*  action(type="omfwd" target="syslog.koeroo.lan" port="514" protocol="udp")' \
    > /etc/rsyslog.d/10-syslog.koeroo.lan.conf


# CMD ./monitor.py --fqdn smtp.koeroo.net --port 25 --protocol SMTP --syslog-ident danetlsa

#ENTRYPOINT [ "cron", "-f" ]

ENTRYPOINT [ "/bin/bash" ]
#CMD /bin/bash