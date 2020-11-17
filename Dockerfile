FROM python:3

RUN apt update ; apt upgrade -y

RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

RUN apt-get update -y
RUN apt-get install -y docker-ce docker-ce-cli containerd.io

COPY requirements.txt /tmp
RUN python -m pip install -r /tmp/requirements.txt

RUN mkdir -p /home/TheExecutor
COPY bot.py /home/TheExecutor

ENV DISCORD_TOKEN="XXX"

CMD ["python", "/home/TheExecutor/bot.py"]