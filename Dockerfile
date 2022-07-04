FROM python:3.10.0-alpine3.15

COPY ./ /tmp/build
WORKDIR /tmp/build
RUN python -m pip install . && rm -rf /tmp/build

ENTRYPOINT ["pylint"]
