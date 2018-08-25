# How to contribute

I'm really glad you're reading this, because we need volunteer developers to help vanellope come to fruition.

## Report an issue  

If you found a bug from the code, or want a feature which vanellope dont have, or just want to give some advice about this project, feel free to submit an issue to our [Github repository](https://github.com/qar/vanellope). 

## Setup development environment

some prerequisite:

1. [Vagrant](https://www.vagrantup.com/)
2. [Docker](https://www.docker.com/) (Only if you want to build a docker image on you machine)
3. [NodeJS](https://nodejs.org/en/) (Only if you want to develop the control-panel part which is a NodeJs sub-project)

To start dev server, you need to run `vagrant up` first in the project root directory. [This docs](https://www.vagrantup.com/docs/) may help if you're not familiar with this Vagrant. This command simply start a ubuntu 16.04 virtual box and mount `.` on the host to the `/data` on the vm and forward `8000` port from the guest to `8000` on the host.

According to the network connection condition, it may took a couple of minutes to download OS image or install updates. After the vm started, you can ssh to the vm by `vagrant ssh`, cd to `/data` and the files are exactly the same on your host machine. If no otherwise specified, the following steps assume you're on the `/data` directory of the virtual machine.

## 1. Install dependencies

run `pip install -r requirements.txt` to install python dependencies.

## 2. Set VANELLOPE_CONTENT environment variable

`VANELLOPE_CONTENT` tell vanellope where to store data you created. Commonly just use `export VANELLOPE_CONTENT=/data/content`.

## 2. Start dev server

run `python vanellope/app.py --debug=True --host=0.0.0.0 --port=8000` to start dev server. Visit [http://localhost:8000](http://localhost:8000).

