FROM python:3.7.6

# Expose ports
EXPOSE 80 8000

# Disable debian warnings!
ENV DEBIAN_FRONTEND noninteractive

# Set the default directory where CMD will execute
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# System Deps
# RUN apt-get update && apt-get install && apt-get clean

ADD requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

ADD . /usr/src/app/

ENTRYPOINT ["python", "/usr/src/app/manage.py"]