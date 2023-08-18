#!/bin/bash

# Check if sudo is being run on command
if [ "$EUID" -ne 0 ]
    then echo "Error: Please run as root"
    exit
fi

# Check if Docker is installed on the machine
which docker

if [ $? -eq 0 ]
    then
        echo "Docker is Installed"
    else
        echo "Docker is not installed. Installing Docker"
        yum install docker-ce -y
        # Start Docker and Enable it so it runs automatically when Host is turned on
        systemctl start docker
        systemctl enable docker
        # Add current user to the docker list of users
        usermod -aG docker $USER

        echo "Docker has been installed, started and enabled. Your user has been added to Docker"
fi

# Check if Git is installed on the machine
which git

if [ $? -eq 0 ]
    then
        echo "Git is installed"
    else
        echo "Git is not installed. Installing Git"
        yum install git -y
fi

# Check if Make is installed on the machine
which make

if [ $? -eq 0 ]
    then
        echo "Make is installed"
    else
        echo "Make is not installed. Installing Make"
        yum install make -y
fi

# Clone the Ayon Docker repository
git clone https://github.com/ynput/ayon-docker
cd ./ayon-docker
docker compose up -d
make setup

# Finished
echo "AYON Server has been successfully setup. You can access it here: http://localhost:5000"
echo "If you would like to access it on another workstation, use this machines IP Address + Port number in your browser"