#!/bin/sh
dapr run --app-id liked-tweets --app-port 8000 --app-protocol grpc --components-path ./dapr-components python3 main.py