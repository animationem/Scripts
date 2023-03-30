## RUN ANY COMMAND OR TRANSFER ANY FILE YOU WANT RELATED TO HOUDINI HERE IN THIS SCRIPT
## SALT WILL RUN OVER ALL OF THE COMMANDS AND CHECK TO SEE IF ITS THERE. THE 'CREATES'
## COMMAND WILL BE USED AS A CHECK. IF IT SEES THAT THERE IS SOMETHING THERE, IT WILL SKIP THE STEP 

### SET HOUDINI EVNIRONMENT VARIABLES --------

# This command will transfer the houdini_setup.sh file to the target directory in profile.d 
# The salt:// you see there is a representation of where Salt looks for all the files it needs to transfer or install 
# Think of it like a master directory for all things Salt needs to do. You can go out of this btw, you just have to make sure 
# Salt can access the files. If you are an NFS based infrastructure its pretty nice and easy. 

houdini_license_host:
    file.managed:
        - name: /etc/profile.d/houdini_setup.sh 
        - source: salt://files/env-variables/houdini_setup.sh
        - user: root 
        - group: root 
        - mode: 644

### ------------------------------------------


### HOUDINI INSTALLATION ---------------------

#This name is not important but its just the name of the command the Salt Minion will run
install_houdini_19_5_435:
    cmd.run:
        - name: /path/to/houdini/installation/houdini.install --auto-install --accept-EULA --no-license 
        - creates: /opt/hfs19.0.435/bin 

### ------------------------------------------