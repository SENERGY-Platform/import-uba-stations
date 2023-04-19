FROM python:3-slim-buster
RUN apt-get update && apt-get install git -y

ADD . /opt/app
WORKDIR /opt/app
RUN pip install --no-cache-dir -r pip-requirements.txt
LABEL org.opencontainers.image.source https://github.com/SENERGY-Platform/import-uba-stations
CMD [ "python", "./main.py" ]
