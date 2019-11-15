FROM python:3.7

RUN groupadd -r development && useradd --no-log-init -r -g development flask

RUN apt-get update
RUN apt-get install -y postgresql-client

# Setup app directory, and user directory
RUN mkdir -p /app
RUN mkdir -p /home/flask

RUN chown -R flask:development /home/flask
RUN chmod -R 770 /home/flask

# Install dependcencies
WORKDIR /app/

ENV PORT 5000
EXPOSE $PORT

# OR swap this to pipenv
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

# Copy over app code
COPY ./example /app/example
COPY ./bin /app/bin

RUN chown -R root:development /app
RUN chmod -R 770 /app

USER flask
ENTRYPOINT ["bin/entrypoint.sh"]
CMD ["web"]