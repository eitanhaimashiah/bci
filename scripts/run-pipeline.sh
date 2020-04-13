#!/bin/bash

# TODO Complete a script to run everything
# I'd like to be able to simply run this script,
# then manually invoke the client to upload a sample,
# and then use the CLI to see the results, and a browser to visualize them in the GUI.

# Run a docker of RabbitMQ
docker run -d -p 5672:5672 --name mq rabbitmq

# Run a docker of PostgreSQL
docker run -d -p 5432:5432 --name=db postgres
