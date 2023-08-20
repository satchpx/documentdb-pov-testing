FROM python:3 
WORKDIR /app 
COPY bin/app.py . 
RUN python3 -m pip install --upgrade pip 
RUN wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
RUN cp global-bundle.pem rds-combined-ca-bundle.pem
CMD ["python3", "app.py"]