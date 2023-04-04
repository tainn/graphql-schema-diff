FROM fedora:37 AS builder
WORKDIR /app
ENV PYTHONPATH="/app:$PYTHONPATH"
ENV CONTAINERIZED=true
RUN dnf install python3-pip -y
RUN dnf install git -y
RUN dnf install nodejs -y
RUN npm install -g get-graphql-schema

FROM builder
COPY src /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "-u"]
