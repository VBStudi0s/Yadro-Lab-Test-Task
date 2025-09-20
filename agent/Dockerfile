FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install python3 pip -y

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --break-system-packages --upgrade pip \
  && pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY ./tests ./tests/

CMD ["pytest", "-vv", "-s"]

