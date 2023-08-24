FROM python:3.10

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

