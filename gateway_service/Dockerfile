FROM python:latest

ADD main.py /gateway_service/
ADD schemas.py /gateway_service/

RUN pip install uvicorn
RUN pip install fastapi
RUN pip install pydantic[email]
RUN pip install httpx

WORKDIR /gateway_service/