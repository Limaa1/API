FROM python:3.10

COPY ./requirements.txt /ips/requirements.txt

WORKDIR /ips

RUN pip install -r requirements.txt

COPY . /ips

ENTRYPOINT [ "python" ]

CMD [ "endpoints.py" ]