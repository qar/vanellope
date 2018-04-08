FROM python:2.7-alpine
MAINTAINER Qiao Anran <qiaoanran@gmail.com>
ENV VANELLOPE_CONTENT /vanellope_content
VOLUME ["/vanellope_content"]
WORKDIR /src
COPY ./vanellope /src/vanellope 
COPY ./requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "vanellope/app.py", "--host=0.0.0.0", "--port=80"]
