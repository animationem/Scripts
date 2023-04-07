import hou
from collections import OrderedDict

# Set the root context
root = hou.node('/obj/')

# Create the dictionary that will store the key and value pairs
nw_boxes = {'ASSETS': (0.281, 0.281, 0.278), 'GEO': (0.529, 0.596, 0.415), 'LGT': (0.980, 0.898, 0.533), 'FX': (0.455, 0.580, 0.917), 'RENDER': (0.709, 0.611, 0.882)}

# Set the order by which the network boxes will be generated
nw_order = ['ASSETS', 'GEO', 'LGT', 'FX', 'RENDER']

# The network boxes will start at this position in the network
pos = 16

# Create Horizontal Network Boxes, set size, comment, positions, and colors
for key in nw_order:
    value = nw_boxes[key]
    nb = root.createNetworkBox(name=key)
    nb.setComment(key)
    nb.setSize([8.0, 4.0])
    nb.setColor(hou.Color(value))
    nb.setPosition([0, pos])

        
    pos -= 5