FROM python:3.9-alpine



EXPOSE 8000

RUN apk add --no-cache gcc python3-dev musl-dev

ADD . /codomatest

WORKDIR /codomatest

RUN pip install -r requirements.txt

RUN python docmanv2-main/manage.py makemigrations

RUN python docmanv2-main/manage.py migrate



CMD [ "python", "docmanv2-main/manage.py", "runserver", "0.0.0.0:8000" ]
