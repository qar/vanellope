FROM node:10.15.3-stretch as uibuilder
WORKDIR /data
COPY ./control-panel/package*.json /data/
RUN npm install --production
COPY ./control-panel /data/
RUN npm run build

########################################

FROM python:3.8.0-slim-buster
MAINTAINER Qiao Anran <qiaoanran@gmail.com>
ENV VANELLOPE_CONTENT /vanellope_content
VOLUME ["/vanellope_content"]
WORKDIR /src
COPY ./vanellope /src/vanellope
COPY ./requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
COPY --from=uibuilder /data/dist/assets /src/vanellope/admin/assets
COPY --from=uibuilder /data/dist/index.html /src/vanellope/admin/templates/controlpanel.html
EXPOSE 80
CMD ["python", "vanellope/app.py", "--host=0.0.0.0", "--port=80"]
