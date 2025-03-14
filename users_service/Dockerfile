FROM python:latest

ADD main.py /users_service/
ADD auth/* /users_service/auth/
ADD database/* /users_service/database/
ADD profiles/* /users_service/profiles/
ADD config.py /users_service/

RUN pip install uvicorn
RUN pip install fastapi
RUN pip install pydantic[email]
RUN pip install httpx
RUN pip install passlib
RUN pip install sqlalchemy
RUN pip install pydantic_settings
RUN pip install asyncpg
RUN pip install python-jose
RUN pip install bcrypt

WORKDIR /users_service/