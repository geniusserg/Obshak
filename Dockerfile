FROM python:3.10

WORKDIR /home

ENV VK_GROUP_ID=""
ENV VK_GROUP_TOKEN=""

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install sqlite3 && mkdir db
COPY requirements.txt ./
RUN pip install -U -r requirements.txt
COPY *.py ./
COPY createdb.sql ./
COPY ./model ./
COPY ./payments ./
COPY ./test ./

ENTRYPOINT ["python", "server.py"]