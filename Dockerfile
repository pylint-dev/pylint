FROM python:3.9.0-alpine3.12

COPY ./ /tmp/build
WORKDIR /tmp/build
RUN python setup.py install && rm -rf /tmp/build

ENTRYPOINT ["pylint"]
