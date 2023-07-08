import hou, os, glob, shutil

# Get the caching node, name of the hip file, and full path to the hip file
node = hou.node('..')
hip_name = hou.hipFile.basename()
scene_path = hou.hipFile.path()

# Gather and Retreieve the Output paramter path, then check to see if it exists
dir_path = node.evalParm('sopoutput')
path = os.path.exists(dir_path)    


# This function is designed to save the current scene but save a backup in the versioned folder
def save_scene(scene_path, dir_path):
    # We need to get the last folder so we can save the current versioned scene into it
    splitPath_toSimulation = (dir_path.split('/'))[:-1]
    fullPath_toSimulation = '/'.join(splitPath_toSimulation)

    # Store backup folder and scene location and check to see if it already exists
    backup_folder = fullPath_toSimulation + '/backup'
    backup_scene = backup_folder + '/' + hip_name
    folder_check = os.path.exists(backup_folder)
    
    # If the backup folder exists, save the scene
    if folder_check:
        hou.hipFile.save()
        shutil.copy2(scene_path,backup_scene)
        
    # If the backup folder does not exist, create it then save a new version
    if folder_check == False:
        os.makedirs(backup_folder)
        hou.hipFile.save()
        shutil.copy2(scene_path,backup_scene)
        

# If the path returns True, it will prompt the user to decide whether or not they want to Version Up or Overwrite the simulation version
if path:
    buttons = ('Version Up', 'Overwrite', 'Cancel')
    details = '''If you choose to version up, it will go to the next available version rather than \nthe next number in sequential order. \n\nIf you choose to Overwrite this version, you will need to confirm your choice.'''
    version_option = hou.ui.displayMessage('This version already exists, do you want to Overwrite it or Version up?', buttons=buttons, details=details, default_choice=0, close_choice=-1)
    
    
    # If they choose to Version Up, it will version up the code based on the next available number rather than the next number in sequential order
    if version_option == 0:
        # Gather the version parameter of the node, and retreive the current value
        p_version = node.parm('version')        
        v_version = node.evalParm('version')
        
        # Split the path based on the characters '/v' for versions
        path_toVersions = dir_path.split('/v')[0]
        
        # Concatenate the versions and the basename
        list_versions = glob.glob(os.path.join(path_toVersions, 'v*'))

        # Find the max version in the list of versioned folders and increase it by 1
        max_version = max([int(os.path.splitext(os.path.basename(version))[0][1:]) for version in list_versions])
        new_version = f'v{max_version + 1}'

        new_dir_path = path_toVersions + '/' + new_version
        os.makedirs(new_dir_path)
        
        # Store the new version number and set it to the parameter 
        n_version = int(new_version.split('v')[1])
        p_version.set(n_version)
        print('Versioning up to ' + str(n_version))
        
        backup_folder = new_dir_path + '/backup'
        backup_scene = backup_folder + '/' + hip_name
        os.makedirs(backup_folder)
        hou.hipFile.save()
        shutil.copy2(scene_path, backup_scene)
        
        
    # If the user chooses to overwrite the simulation version, it will prompt them to confirm they want to do this before moving on
    if version_option == 1:
        d_buttons = ('Yes', 'WAIT NO')
        double_option = hou.ui.displayMessage('Are you sure you want to Overwrite this version?', buttons=d_buttons, default_choice=1, close_choice=1)
        
        # Let the user know that you will be overwriting the simulation and then move on to saving the scene
        if double_option == 0:
            print('Overwriting Current Simulation Version')
            
            save_scene(scene_path, dir_path)

                
    if version_option == 2:
        print('Canceled')

# If path doesn't exist, save the scene, store backup and simulate
if path == False:
    save_scene(scene_path, dir_path)