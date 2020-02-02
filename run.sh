#!/bin/bash
docker pull richardchien/cqhttp:latest
mkdir coolq
docker run -ti -d --rm --name cqhttp-test \
    -v $(pwd)/coolq:/home/user/coolq \
    -p 9000:9000 \
    -p 5700:5700 \
    -e CQHTTP_POST_URL=http://172.18.0.1:8080 \
    -e CQHTTP_SERVE_DATA_FILES=yes \
    richardchien/cqhttp:latest
echo "已完成"