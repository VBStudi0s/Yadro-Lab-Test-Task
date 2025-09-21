FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install python3 pip wget dpkg default-jre-headless -y

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --break-system-packages --upgrade pip \
  && pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY ./tests ./tests/

RUN mkdir -p /app/allure
RUN wget -O /tmp/allure.deb "https://github.com/allure-framework/allure2/releases/download/2.35.1/allure_2.35.1-1_all.deb" && \
  dpkg -i /tmp/allure.deb

ENTRYPOINT ["pytest", "-vv", "-s", "--alluredir=/app/reportallure"]

