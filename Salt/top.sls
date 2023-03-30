# This salt script is what gets checked and run by the Salt minion. 
# Keep in mind, salt really does best on unix based machines because you can run these via command line/terminal
# There is a salt for Windows but not a lot of people make commands for a cli based installation on Windows
# You also may want to separate out the Windows machines from the others just to make sure there are no conflicts

base:
    # Salt Master
    '# salt master node fqdn goes here':
        - # PLACE ALL NECESSARY SCRIPTS YOU WANT TO RUN ON THIS MACHINE HERE
        - # EVERY NEW SLS SCRIPT NEEDS A NEW LINE

    # File Server
    '# file server fqdn goes here':
        - # PLACE ALL NECESSARY SCRIPTS YOU WANT TO RUN ON THIS MACHINE HERE
        - # EVERY NEW SLS SCRIPT NEEDS A NEW LINE

    # Deadline Master (can be VM)
    '# deadline fqdn goes here':
        - # PLACE ALL NECESSARY SCRIPTS YOU WANT TO RUN ON THIS MACHINE HERE
        - # EVERY NEW SLS SCRIPT NEEDS A NEW LINE

    # Virtual Machines
    '((hostname)|(hostname)|(hostname))...).(domain pathi applicable)':
        - # PLACE ALL NECESSARY SCRIPTS YOU WANT TO RUN ON THIS MACHINE HERE
        - # EVERY NEW SLS SCRIPT NEEDS A NEW LINE

    # Render Nodes (thought this is best when you separate them by CPU and GPU since one needs graphics drivers and the others don't)
    '((machinename1)|(machinename2)|(machinename3))...).(domain path if applicable)'
    # OR if they have a similar naming convention like: r11, r12, r21, r22, etc
    'r[1-2][1-2].(domain path if applicable)':
        - # PLACE ALL NECESSARY SCRIPTS YOU WANT TO RUN ON THIS MACHINE HERE
        - # EVERY NEW SLS SCRIPT NEEDS A NEW LINE
    
    # Workstations
    '((hostname)|(hostname)|(hostname))...).(domain path if applicable)':
        - # PLACE ALL NECESSARY SCRIPTS YOU WANT TO RUN ON THIS MACHINE HERE
        - # EVERY NEW SLS SCRIPT NEEDS A NEW LINE

##EXAMPLE
#    base:
#        # Workstations
#        'aster':
#        - match: pcre
#        - osconfig.alma_baseutils
#        - osconfig.smb_client
#        - software.maya
#        - software.renderman
#        - software.Houdini
#        - software.nuke 