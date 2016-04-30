FROM centos:6
FROM python:2.7
MAINTAINER Qiao Anran <qiaoanran@gmail.com>
COPY . /src
RUN cd /src && python setup.py install
CMD ["vanellope", "--host=0.0.0.0", ,"--port=80"]
