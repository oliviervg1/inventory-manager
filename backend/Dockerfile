FROM centos:centos7
MAINTAINER Olivier Van Goethem <olivier-vg@outlook.com>
RUN yum update -y && yum install python-setuptools -y
RUN easy_install pip
RUN pip install --upgrade pip
ADD requirements.txt /opt/webapp/
ADD ./src /opt/webapp/
WORKDIR /opt/webapp
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
