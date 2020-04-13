#!/bin/bash

python -m grpc.tools.protoc -I=protos --python_out=bci/protocol sample.proto
