FROM python:3.11.17-alpine3.24

COPY ./ /tmp/build
WORKDIR /tmp/build
RUN python -m pip install --no-cache-dir . && rm -rf /tmp/build

ENTRYPOINT ["pylint"]
