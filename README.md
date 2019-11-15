# Docker Compose Example App

This app demonstrates a simple flask application that integrates with celery
to provide the ability to run background tasks. Rabbitmq is used as a broker
to dispatch tasks to workers and results of tasks can be stored in the a backend
using redis (rabbitmq doesn't allow for storing results of tasks)

## Setup

1. Copy the `.env.example` file to `.env` which will provide some defaults
for a build
    ```
    cp .env.example .env
    ```
  
2. Next source that environment file
    ```
    source .env
    ```

3. Build the docker images using docker-compose
    ```
    docker-compose build
    ```

4. Start the services
    ```
    docker-compose up
    ```
5. Now you can open up a browser and navigate to http://0.0.0.0:5000/, http://0.0.0.0:5000/ping, and http://0.0.0.0:5000/do_work.
The last link there will create a background task using celery and return the taskId in the response

 