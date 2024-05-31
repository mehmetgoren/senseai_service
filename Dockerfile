FROM ubuntu:22.04
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -qq update && apt-get upgrade -y
RUN apt-get install -y apt-utils
RUN apt-get install -y tzdata
RUN apt-get install -y curl
RUN apt-get -qq install --no-install-recommends -y python3-pip
RUN apt-get install ffmpeg libsm6 libxext6 -y

RUN pip3 install docker
RUN pip3 install psutil
RUN pip3 install redis
RUN pip3 install requests
RUN pip3 install pybase64

COPY . .

CMD ["python3", "main.py"]