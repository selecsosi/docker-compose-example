FROM python:3.7

# Setup user
RUN groupadd -r development && useradd --no-log-init -r -g development celery

# Setup app directory, and user directory
RUN mkdir -p /app
RUN mkdir -p /home/celery

RUN chown -R celery:development /home/celery
RUN chmod -R 775 /home/celery

# Install dependcencies
WORKDIR /app/
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

# Setup app
COPY ./example /app/example
COPY ./bin /app/bin
RUN chown -R root:development /app
RUN chmod -R 770 /app

#Setup fixtures dir

USER celery
ENTRYPOINT ["bin/entrypoint.sh"]
CMD ["flower"]