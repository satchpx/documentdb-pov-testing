FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    curl git wget curl sudo libcurl4 openssl
RUN git clone https://github.com/mongodb/mongo-perf.git
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# RUN wget https://repo.mongodb.org/apt/ubuntu/dists/xenial/mongodb-org/4.2/multiverse/binary-amd64/mongodb-org-shell_4.2.6_amd64.deb
RUN wget https://repo.mongodb.org/apt/ubuntu/dists/xenial/mongodb-org/5.0/multiverse/binary-amd64/mongodb-database-tools_100.8.0_amd64.deb
# RUN dpkg -i mongodb-org-shell_4.2.6_amd64.deb
RUN dpkg -i mongodb-database-tools_100.8.0_amd64.deb 
# Download the Amazon DocumentDB Certificate Authority (CA) certificate required to authenticate to your cluster
RUN wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

COPY bin/run /mongo-perf/
COPY bin/analyze.py /mongo-perf/

RUN chmod +x /mongo-perf/run
RUN chmod +x /mongo-perf/analyze.py

WORKDIR /mongo-perf

CMD ["/bin/bash"]