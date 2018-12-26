FROM node:9.4.0-wheezy as uibuilder
WORKDIR /data
COPY ./control-panel/package*.json /data/
RUN npm install
COPY ./control-panel /data/
RUN npm run build

########################################

FROM python:2.7-alpine
MAINTAINER Qiao Anran <qiaoanran@gmail.com>
ENV VANELLOPE_CONTENT /vanellope_content
VOLUME ["/vanellope_content"]
WORKDIR /src
COPY ./vanellope /src/vanellope
COPY ./requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
COPY --from=uibuilder /data/dist/assets /src/vanellope/admin/assets
EXPOSE 80
CMD ["python", "vanellope/app.py", "--host=0.0.0.0", "--port=80"]
