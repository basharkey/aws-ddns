FROM registry.hub.docker.com/library/python:3.12-rc-slim-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./aws-ddns.py" ]
CMD [ "--help" ]
