FROM python:3.7-alpine

LABEL "com.github.actions.name"="GitHub Action for pylint"
LABEL "com.github.actions.description"="Run pylint commands"
LABEL "com.github.actions.icon"="upload-cloud"
LABEL "com.github.actions.color"="green"

RUN apk add --no-cache bash build-base gcc
RUN pip install --upgrade pip
RUN pip install pylint
RUN python --version ; pip --version ; pylint --version

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
