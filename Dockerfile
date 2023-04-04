FROM fedora:37 AS builder
WORKDIR /app
ENV PYTHONPATH="/app:$PYTHONPATH"
ENV CONTAINERIZED=true
RUN dnf install nodejs -y
RUN npm install -g get-graphql-schema

FROM builder
COPY src /app
ENTRYPOINT ["python3", "-u"]
