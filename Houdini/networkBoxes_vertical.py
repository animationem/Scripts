import hou
from collections import OrderedDict

root = hou.node('/obj/')

# Create the dictionary that will be ordered by first come first serve
nw_boxes = OrderedDict()

# Create the keys and values that will be added to the dictionary variable above
nw_boxes["Assets"] = (0.281, 0.281, 0.278)
nw_boxes["GEO"] = (0.529, 0.596, 0.415)
nw_boxes["LGT"] = (0.980, 0.898, 0.533)
nw_boxes["FX"] = (0.455, 0.580, 0.917)
nw_boxes["RENDER"] = (0.709, 0.611, 0.882)

# The network boxes will start at this position in the network
pos = -16

# Create Vertical Network Boxes, set size, comment, positions, and colors
for key, value in nw_boxes.items():
    nb = root.createNetworkBox(name=key)
    nb.setComment(key)
    nb.setSize([4.0, 8.0])
    nb.setColor(hou.Color(value))
    nb.setPosition([pos,0])
        
    pos += 5