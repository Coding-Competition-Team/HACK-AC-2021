FROM python:3.8

RUN mkdir -p /problem
WORKDIR /problem

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y socat

RUN pip install pycryptodome

COPY *.py /problem
COPY flag.txt /problem

CMD [ "socat", "tcp-l:3000,fork,reuseaddr", "EXEC:\"python3 server.py\"" ]