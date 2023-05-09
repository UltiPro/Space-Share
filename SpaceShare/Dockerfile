FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install setuptools==57.5.0
RUN pip install -r requirements.txt