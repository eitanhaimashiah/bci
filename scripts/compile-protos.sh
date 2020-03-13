#!/bin/bash

python -m grpc.tools.protoc -I=protos --python_out=bci/utils/sample sample.proto
