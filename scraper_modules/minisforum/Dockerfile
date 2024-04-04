FROM python:slim-bookworm
MAINTAINER Simon Thiel

WORKDIR /opt/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]