FROM python:3.6

RUN pip install --upgrade pip

COPY web/scripts/fpdiff.sh /usr/bin

RUN apt-get update -y

RUN pip3 install pep8 flake8 autopep8

WORKDIR /code

ENTRYPOINT ["/bin/bash", "/usr/bin/fpdiff.sh"]

