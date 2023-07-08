import hou, os, glob, re

# We need to grab hip file path, the path to the scenes, and scene name
hip_name = hou.hipFile.path()
scene_name = hip_name.split('/')[-1].split('_')[0]
path_to_scenes = os.path.dirname(hip_name)

# Get all the scene files associated with .hip, store them in a list with their names
get_scenes = glob.glob(os.path.join(path_to_scenes, scene_name + '*_v*.hip'))
scenes = []
for version in get_scenes:
    scenes.append(os.path.basename(version))

# Split the extension off from the names, and store it
split_ext = scenes[-1].split('.')
ext = os.path.splitext(scenes[0])[1]
split = re.split(r'(_v)', split_ext[0])
user = hip_name.split('_')[-1].split('.')[0]

# Store the standard name in a variable
common = split[0] + split[1]

# Store the version number in a variable and increment it by 1, including some padding
versions = [int(file.split('_v')[1].split('.')[0].split('_')[0]) for file in scenes]
max_version = f'{max(versions) + 1:03}'

# Rebuild the name of the file
new_save_name = common + max_version + '_' + user + ext

# Save the file
hou.hipFile.save(file_name=path_to_scenes + '/' + new_save_name)

#------------------------------------------------------------------