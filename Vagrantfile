# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 8000, host: 8000 
  config.vm.synced_folder ".", "/data"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "1024"
  end

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get update
    sudo apt-get install build-essential checkinstall
    sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
    cd /usr/src
    sudo wget https://www.python.org/ftp/python/2.7.14/Python-2.7.14.tgz
    sudo tar xzf Python-2.7.14.tgz
    cd Python-2.7.14
    sudo ./configure --enable-optimizations
    sudo make altinstall
    sudo ln -s $(which python2.7) /usr/bin/python
    sudo apt-get intall python-pip
    echo "exoprt LC_ALL=C" >> ~/.bashrc
    sudo mkdir /vanellope_content
    sudo chown -R ubuntu:ubuntu /vanellope_content
    echo "export bashVANELLOPE_CONTENT=/vanellope_content" >> ~/.bashrc
  SHELL
end
