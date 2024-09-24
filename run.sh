#service cron start;uvicorn src.mnist.main:app --host 127.0.0.1 --port 8000 --reload
env >> /etc/enviorment
service cron start;uvicorn main:app --host 0.0.0.0 --port 8080 --reload
