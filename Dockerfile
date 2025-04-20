FROM ubuntu:22.04

RUN apt update && apt install -y openssh-server sudo curl && \
    mkdir /var/run/sshd && \
    echo 'root:lpnodes' | chpasswd && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "Port 22\nPort 443\nPort 80\nPort 8080\nPort 2022\nPort 5080\nPort 3001" >> /etc/ssh/sshd_config

EXPOSE 22 443 80 8080 2022 5080 3001

CMD ["/usr/sbin/sshd", "-D"]
