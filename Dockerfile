FROM python:3.6

ENV APP_DIR /admin_auth_client

RUN mkdir -p ${APP_DIR}
WORKDIR APP_DIR

# We copy just the requirements.txt first to leverage Docker cache
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD . .

RUN python manage.py makemigrations
RUN python manage.py migrate

ENTRYPOINT [ "python" ]

CMD [ "manage.py", "runserver", "0.0.0.0:8080"]