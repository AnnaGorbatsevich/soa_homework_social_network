FROM python:latest

ADD main.py /content_service/
ADD schemas.py /content_service/

RUN pip install uvicorn
RUN pip install fastapi

WORKDIR /content_service/