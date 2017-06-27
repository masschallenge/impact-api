FROM python:3.6

WORKDIR /wwwroot

COPY impact /wwwroot

COPY scripts/start.sh /usr/bin

COPY scripts/start-nodaemon.sh /usr/bin

RUN apt-get update -y

# python2.7 is required to run supervisor
RUN apt-get install -y netcat mysql-client python2.7 python-setuptools nginx

RUN pip install --upgrade pip

RUN easy_install-2.7 supervisor

RUN pip3 install -r requirements/dev.txt

RUN useradd -s /bin/bash -u 3000 -M impact_user

RUN chown impact_user /usr/bin/start.sh

RUN chown -R impact_user /wwwroot

RUN apt-get install -y gettext

USER impact_user

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["/bin/bash" , "/usr/bin/start.sh"]
