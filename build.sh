cd control-panel && npm run build
cd ..
docker build . -t registry.gitlab.com/qar/vanellope:latest
