#!/bin/bash
# This is a script based on RHEL distros. For DEB based distros, replace the yum with apt-get

ARGS=$(getopt --options 'bfhd:' --longoptions 'backend,frontend,help,destination:' -- "$@")
eval set --"$ARGS"

backend=false
frontend=false
help=false
destination=false

while true; do
    case "$1" in
        -b|--backend)
            backend="true"
            shift;;
        -f|--frontend)
            frontend="true"
            shift;;
        -h|--help)
            help="true"
            shift;;
        -d|--destination)
            destination="true";
            dvalue="$2";
            shift 2;;
        --)
            break;;
        *)
            echo -e "Error: Unknown option:" "$1"
            exit 1;;
    esac
done

if [ "$help" == true ]
    then 
        echo "$(basename "$0") options available: [-b, --backend] [-f, --frontend] [-d, --destination <directory path>] [-h, --help]"
        exit
fi

if [ "$dvalue" == "" ]
then
    echo "Please input a destination directory"
    echo "$dvalue"
    exit
fi

# Check if sudo is being run on command
if [ "$EUID" -ne 0 ]
    then 
        echo "Error: Please run as root"
        exit
fi

# Check if Docker is installed on the machine
which docker &> /dev/null

if [ $? -ne 0 ]
    then
        echo "Docker is not installed. Installing Docker"
        yum config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo -y
        yum update -y
        yum install docker-ce docker-ce-cli containerd.io -y
        
        # Start Docker and Enable it so it runs automatically when Host is turned on
        systemctl start docker
        systemctl enable docker
        
        # Add current user to the docker list of users
        usermod -aG docker $USER

        echo "Docker has been installed, started and enabled. Your user has been added to Docker"
fi

# Check if Git is installed on the machine
which git &> /dev/null

if [ $? -ne 0 ]
    then
        echo "Git is not installed. Installing Git"
        yum install git -y
fi

# Check if Make is installed on the machine
which make &> /dev/null

if [ $? -ne 0 ]
    then
        echo "Make is not installed. Installing Make"
        yum install make -y
fi

# Clone the Ayon Docker repository
repo_url="https://github.com/ynput/ayon-docker"
if [ "$destination" == "true" ]
    then
        mkdir "$dvalue/ayon"
        git clone "$repo_url" "$dvalue/ayon"
    else
        git clone "$repo_url"
fi
cd "$dvalue/ayon"
docker compose up -d
make setup

# Run the make commands on the developer backend/frontend
if [ "$backend" == true ] && [ "$frontend" == true ]
    then
        make backend && make frontend
    elif [ "$frontend" == true ]
        then
            make frontend
    elif [ "$backend" == true ]
        then
            make backend
fi

# Finishing closing messages
if [ "$backend" == true ] && [ "$frontend" == true ]
    then
        echo -e "\nThe developer backend & frontend have also been setup\n"
elif [ "$backend" == true ]
    then
        echo -e "\nThe Backend has also been setup\n"
elif [ "$frontend" == true ]
    then
        echo -e "\nThe Frontend has also been setup\n"
fi
echo -e "Access your AYON Server here: http://localhost:5000"
echo -e "To access on another workstation, use this machines IP Address + Port number in your browser\n"
