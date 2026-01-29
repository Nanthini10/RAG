#!/bin/bash

docker build -t rag-pipeline:latest .

docker run -it --rm \
  --gpus all \
  --shm-size=8g \
  -v $(pwd):/workspace \
  -w /workspace \
  rag-pipeline:latest \
  /bin/bash
