#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."

function main {
  docker build -t bci .
  cd "deploy"
  docker-compose up
}


main "$@"
