FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
RUN pip install --upgrade gevent 
COPY . /code/
CMD [ "./docker-entrypoint.sh" ]