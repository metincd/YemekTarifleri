FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /usr/src/app
COPY requirements.txt /code/
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
RUN pip install --upgrade gevent 
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "./docker-entrypoint.sh" ]