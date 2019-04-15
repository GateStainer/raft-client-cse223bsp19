#! /bin/bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./kvstore.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./chaosmonkey.proto