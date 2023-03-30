import hou
root = hou.node('/obj/')

# This should be added to the 123.py script in your Houdini Documents folder. On Windows it is: "C:\Users\(User)\Documents\houdini19.0\scripts\123.py"
# On Linux this most likely located in your home folder: /home/(user)/(houdini_version)/scripts/123.py
# If the scripts folder isn't there, go ahead and create it. Same goes for the 123.py


nw_boxes = {'Import' : (), 'Geo' : (0.6, 1, 0.25), 'Lighting' : (0.75, 0.75, 0), 'FX' : (0, 0.35, 0.75), 'Render' : (0.37, 0.205, 1)}
nb_count = len(nw_boxes)
pos = 10

# Create Vertical Network Boxes, set poitions and colors
for key, value in nw_boxes.items():
    nb = root.createNetworkBox(name=key)
    nb.setComment(key)
    nb.setSize([8.0, 4.0])
    nb.setColor(hou.Color(value))
    nb.setPosition([0,pos])
        
    pos -= 5