import hou
root = hou.node('/obj/')

# This should be added to the 123.py script in your Houdini Documents folder. On Windows it is: "C:\Users\(User)\Documents\houdini19.0\scripts\123.py"
# On Linux this most likely located in your home folder: /home/(user)/(houdini_version)/scripts/123.py
# If the scripts folder isn't there, go ahead and create it. Same goes for the 123.py

# Create Vertical Network Boxes, set poitions and colors
### Create Import Network Box
nb_import = root.createNetworkBox(name='Import')
nb_import.setComment('Import')
nb_import.setSize([5.0, 8.0])
nb_import.setPosition([-10, 0])

### Create Geometry Network Box
nb_geo = root.createNetworkBox()
nb_geo.setName('Geo')
nb_geo.setComment('Geometry')
nb_geo.setSize([5.0, 8.0])
nb_geo.setColor(hou.Color(0.6, 1, 0.25))
nb_geo.setPosition([-4, 0])

### Create Lighting Network Box
nb_lgt = root.createNetworkBox()
nb_lgt.setName('Lighting')
nb_lgt.setComment('Lighting')
nb_lgt.setSize([5.0, 8.0])
nb_lgt.setColor(hou.Color(0.75, 0.75, 0))
nb_lgt.setPosition([2, 0])

### Create FX Network Box
nb_fx = root.createNetworkBox()
nb_fx.setName('FX')
nb_fx.setComment('FX')
nb_fx.setSize([5.0, 8.0])
nb_fx.setColor(hou.Color(0, 0.35, 0.75))
nb_fx.setPosition([8, 0])

### Create Render Network Box
nb_ren = root.createNetworkBox()
nb_ren.setName('Render')
nb_ren.setComment('Render')
nb_ren.setSize([5.0, 8.0])
nb_ren.setColor(hou.Color(0.37, 0.205, 1))
nb_ren.setPosition([14, 0])

