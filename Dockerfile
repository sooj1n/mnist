FROM python:3.11

WORKDIR /code

RUN apt update
RUN apt install -y cron
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob

COPY src/mnist/main.py /code/
COPY run.sh /code/run.sh
COPY img /code/images

RUN pip install --no-cache-dir --upgrade git+https://github.com/sooj1n/mnist.git@0.1.3

CMD ["sh", "run.sh"]
