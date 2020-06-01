#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
  sudo docker pull rabbitmq
  sudo docker pull postgres
  python -m virtualenv .env --prompt "[bci] "
  find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
  .env/bin/pip install -U pip
  .env/bin/pip install -r requirements.txt
  sudo docker build -t bci .
}


main "$@"
