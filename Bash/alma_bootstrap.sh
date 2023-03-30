#!/bin/bash

## This script is used to bootstrap a machine and get it configured for Salt. An admin on the domain needs to input their credentials themselves and choose whether or not to install Salt Minion or Salt Master & Minion.
## We relied on Salt to install our Linux NVIDIA drivers but that is something you could do through here, you may end up with a mismatch in driver implementation later down the road though. Be careful.

# Gather user account for the domain
read -p 'Username for domain admin: ' ADUSER
while True
    do
        read -s -p 'Password for domain admin: ' ADPASS
        echo
        read -s -p 'Please re-enter domain admin password: ' ADPASS2
        echo

        if [[ "$ADPASS" = "$ADPASS2"]]; then
            break
        else
            echo "Passwords did not match, please try again"
        fi
done

while true;
do
    read -p 'Installing Salt Master or Minion? [M/m]'
    echo
    read SALT

    case $SALT in
        [M]* ) useMaster=True; break;;
        [m]* ) useMinion=false; break;;
        * ) echo "Please use either 'M' to indicate Master or 'm' to indicate minion"
    esac
done


PROXY= #REPLACE WITH PROXY "PATH:PORT"

# # Install Certificates
scp `# username@machinePath:/path/to/grab/certificate /destination/path/to/install/certificate`
update-ca-trust

# # Add proxy
echo "proxy=" "$PROXY" >> /etc/yum.conf

# # Install Updates
yum check-update
yum -y upgrade

# # Install EPEL Repo
yum -y install epel-release
yum check-update

# # Distable Firewall (This is your choice, for the env we ran we didn't need it)
systemctl stop firewalld
systemctl disable firewalld

# # Disable SELinux (Again this was our choice, you can change this)
sed -i '7s/.*/SELINUX=disabled/' /etc/selinux/config
setenforce 0

# # Setup Salt (We used salt instead of Ansible, you can take this out if you want)
curl --proxy $PROXY -o bootstrap-salt.sh -L https://bootstrap.saltproject.io
chmod 775 ./bootstrap-salt.sh
if [[ $SALT = true]]; then
    while true;
        do
            ./boostrap-salt.sh -M -H $PROXY stable
    done
fi

if [[ $SALT = false]]; then
    while false;
        do
            ./bootstrap-salt.sh -H $PROXY stable
    done
fi

sed -i '16s/.*/master: /' `# ADD SALT MASTER IP ADDRESS TO THE LEFT OF THE /`  /etc/salt/minion
systemctl enable salt-minion.service
systemctl restart salt-minion.service

# Join domain
# You may not be able to log in via your AD credentials on a new machine build
# because this smb.conf file has changed, and uses a different kerberos method
# for instance. Please check it here, and match it in the salt smb_client config.
yum -y install realmd oddjob-mkhomedir oddjob samba-winbind-clients samba-winbind samba-common-tools samba-winbind-krb5-locator
mv /etc/samba/smb.conf /etc/samba/smb.conf.orig
echo "$ADPASS" | realm join --client-software=winbind --user=$ADUSER `#ADD DOMAIN PATH HERE`
sed -i '4s/.*/template homedir= \/home\/%U/' /etc/samba/smb.conf
sed -i '13s/.*/winbind use default domain = yes/' /etc/samba/smb.conf
systemctl restart winbind.service
# test that adding to the domain worked
id $ADUSER