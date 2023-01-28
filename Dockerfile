FROM python:3.9-alpine



EXPOSE 8000

RUN apk add --no-cache gcc python3-dev musl-dev

ADD . /codomatest

WORKDIR /codomatest

RUN pip install -r requirements.txt

RUN python docmanv2-main/manage.py makemigrations

RUN python docmanv2-main/manage.py migrate


ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

ENV DB_NAME=$DB_NAME
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
CMD [ "python", "docmanv2-main/manage.py", "runserver", "0.0.0.0:8000" ]
