sudo apt-get update
sudo apt-get install build-essential checkinstall -y
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y
cd /usr/src
sudo wget https://www.python.org/ftp/python/2.7.14/Python-2.7.14.tgz
sudo tar xzf Python-2.7.14.tgz
cd Python-2.7.14
sudo ./configure --enable-optimizations
sudo make install
sudo ln -s $(which python2.7) /usr/bin/python
sudo apt-get install python-pip -y
echo "exoprt LC_ALL=C" >> ~/.bashrc
sudo mkdir /vanellope_content
sudo chown -R ubuntu:ubuntu /vanellope_content
echo "export VANELLOPE_CONTENT=/vanellope_content" >> ~/.bashrc
