FROM python:3.6

WORKDIR /wwwroot

COPY impact /wwwroot
COPY scripts/start.sh /usr/bin
COPY scripts/start-nodaemon.sh /usr/bin

COPY scripts/mysqlwait.sh /usr/bin

RUN apt-get update -y
# python2.7 is required to run supervisor
RUN apt-get install -y gettext mysql-client netcat nginx python-setuptools python2.7

# Install remote_syslog2 to talk to papertrail
RUN cd /tmp/ && curl -LOs https://github.com/papertrail/remote_syslog2/releases/download/v0.20/remote-syslog2_0.20_amd64.deb
RUN dpkg -i /tmp/remote-syslog2_0.20_amd64.deb

# Copy config files after installation so installers don't get tripped up
COPY log_files.yml /etc/log_files.yml
COPY nginx/nginx.conf /etc/nginx

RUN pip install --upgrade pip
RUN easy_install-2.7 supervisor
RUN useradd -s /bin/bash -u 3000 -m impact_user
RUN pip3 install -r /wwwroot/requirements/dev.txt

# place django-accelerator's source where it will be overriden by the mounted
# volume, and then install in an editable mode, so code changes in the project's
# directory will be reflected immediately.
WORKDIR /packages
WORKDIR src
RUN git clone https://github.com/masschallenge/django-accelerator.git
WORKDIR /wwwroot
RUN pip3 install -e /packages/src/django-accelerator


RUN chown impact_user /usr/bin/start.sh
RUN chown -R impact_user /wwwroot
RUN chown -R impact_user /home/impact_user

USER impact_user
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

CMD ["/bin/bash", "/usr/bin/start.sh"]
