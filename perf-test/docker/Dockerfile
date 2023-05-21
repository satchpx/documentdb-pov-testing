FROM ubuntu:16.04
RUN apt-get update && apt-get install -y \
    python python3 python-pip python3-pip \
    curl git wget curl sudo libcurl3 openssl
RUN git clone https://github.com/mongodb/mongo-perf.git
RUN pip3 install tornado numpy tabulate
RUN pip3 install -r mongo-perf/requirements.txt
RUN wget https://repo.mongodb.org/apt/ubuntu/dists/xenial/mongodb-org/4.2/multiverse/binary-amd64/mongodb-org-shell_4.2.6_amd64.deb
RUN dpkg -i mongodb-org-shell_4.2.6_amd64.deb

COPY bin/run /mongo-perf/
COPY bin/analyze.py /mongo-perf/

RUN chmod +x /mongo-perf/run
RUN chmod +x /mongo-perf/analyze.py

WORKDIR /mongo-perf

CMD ["/bin/bash"]