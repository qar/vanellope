FROM python:2.7-alpine
MAINTAINER Qiao Anran <qiaoanran@gmail.com>
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "vanellope/app.py", "--host=0.0.0.0", "--port=80"]
