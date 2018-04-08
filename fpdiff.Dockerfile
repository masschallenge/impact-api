FROM python:3.6

RUN pip install --upgrade pip

COPY web/scripts/fpdiff.sh /usr/bin

RUN pip3 install \
    flake8 \
    pycodestyle

WORKDIR /code

ENTRYPOINT ["/bin/bash", "/usr/bin/fpdiff.sh"]

