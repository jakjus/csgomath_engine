FROM python:3.10
COPY . .
RUN pip install -r requirements.txt

CMD gunicorn -b 0.0.0.0:3010 app:app
