import hou
import os

# Set the root context
root = hou.node('/obj/')

# Create the dictionary that will store the key and value pairs for the dark interface
dark_nw_boxes = {
            'ASSETS': (0.281, 0.281, 0.278), 
            'GEO': (0.529, 0.596, 0.415), 
            'LGT': (0.980, 0.898, 0.533), 
            'FX': (0.455, 0.580, 0.917), 
            'RENDER': (0.709, 0.611, 0.882)
            }

light_nw_boxes = {
            'ASSETS': (1, 1, 1), 
            'GEO': (0.486, 0.772, 0.462), 
            'LGT': (1, 0.960, 0.407), 
            'FX': (0.266, 0.549, 0.796), 
            'RENDER': (0.521, 0.376, 0.658)

}

# Set the order by which the network boxes will be generated
nw_order = ['ASSETS', 'GEO', 'LGT', 'FX', 'RENDER']

# The network boxes will start at this position in the network
pos = 16

# Get the Houdini UI Theme (Generally Light or Dark)
def get_houdini_color_scheme(file_path):
    color_scheme = {}

    with open(file_path, 'r') as file:
        current_section = None

        for line in file:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Identify section
            if line.endswith('";'):
                current_section = line[0:-1]
                if current_section.startswith('colors.scheme'):
                    color_scheme = current_section
                    key, value = color_scheme.split(':=')
                    color_scheme = value.strip()

    return color_scheme

# Get the Houdini home directory and ui file stored in it
hip = hou.homeHoudiniDirectory()
pref = 'ui.pref'
file = os.path.join(hip, pref)
dark = '"Houdini Dark"'

# Store the Houdini UI Theme (Normally Dark or Light)
houdini_color_scheme = get_houdini_color_scheme(file)

# Create Horizontal Network Boxes, set size, comment, positions, and colors
for key in nw_order:
    if (houdini_color_scheme == dark):
        value = dark_nw_boxes[key]
    else:
        value = light_nw_boxes[key]
    nb = root.createNetworkBox(name=key)
    nb.setComment(key)
    nb.setSize([8.0, 4.0])
    nb.setColor(hou.Color(value))
    nb.setPosition([0, pos])

        
    pos -= 5