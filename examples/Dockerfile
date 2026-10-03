FROM python:3.10.10-alpine3.17

COPY ./ /tmp/build
WORKDIR /tmp/build
RUN python -m pip install --no-cache-dir . && rm -rf /tmp/build

ENTRYPOINT ["pylint"]
