FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install apache2 openssh-server -y

ARG SSH_TARGET_USER
ARG SSH_TARGET_PASSWORD

RUN mkdir /var/run/sshd
RUN useradd -m -s /bin/bash ${SSH_TARGET_USER}
RUN echo "${SSH_TARGET_USER}:${SSH_TARGET_PASSWORD}" | chpasswd

COPY ./index/index.html /var/www/html/index.html

RUN service apache2 restart

RUN chown -R ${SSH_TARGET_USER} /var/log/apache2

# port for http-requests to request hosted page
EXPOSE 80

CMD service ssh start && apache2ctl -D FOREGROUND
