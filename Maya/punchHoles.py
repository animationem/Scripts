# Punch Holes Script v1.0
# Created by John Kesig
# Compatibility Versions for Maya 2022 & 2023
# Python 3 

import maya.cmds as mc

class punchHolesUI(object):
    def __init__(self):
        #Create Script Window
        self.ph_window = mc.window(title='Punch Holes', menuBar=True)
        self.ph_layout = mc.formLayout(numberOfDivisions=100)

        #Create variables for User Control Settings
        #Circularize
        self.ph_circ_text = mc.text(label='Circularize')
        self.ph_circ_offset = mc.floatSliderGrp(label='Offset', field=True, minValue=-100.0, maxValue=100.0, fieldMinValue=-1000.0, fieldMaxValue=1000.0, value=0.0)

        #Bevel
        self.ph_bevel_text = mc.text(label='Bevel')
        self.ph_bevel_fraction = mc.floatSliderGrp(label='Fraction', field=True, precision=3, minValue=0.0, maxValue=1.0, value=0.2)
        self.ph_bevel_divisions = mc.intSliderGrp(label='Divisions', field=True, minValue=1, maxValue=5, value=1)
        self.ph_bevel_chamfer = mc.checkBoxGrp(label='Chamfer  ', numberOfCheckBoxes=1)

        #Extrude
        self.ph_ext_text = mc.text(label='Extrude')
        self.ph_ext_check = mc.checkBoxGrp(label='Extrude?  ', numberOfCheckBoxes=1)
        self.ph_ext_thickness = mc.floatSliderGrp(label='Thickness', field=True, minValue=-100.0, maxValue=100.0, fieldMinValue=-1000.0, fieldMaxValue=1000.0, value=-10.0)
        self.ph_ext_divisions = mc.intSliderGrp(label='Divisions', field=True, minValue=1, maxValue=5, value=1)
        self.ph_ext_offset = mc.floatSliderGrp(label='Offset', field=True, minValue=-100.0, maxValue=100.0, fieldMinValue=-1000.0, fieldMaxValue=1000.0, value=0.0)

        #Create buttons for the different methods
        self.pvh_button = mc.button(label='Punch Holes by Vertex', backgroundColor=[0.25,0.36,0.466], command=self.punchVertHoles)
        self.pfh_button = mc.button(label='Punch Holes by Face', backgroundColor=[0.25,0.46,0.36], command=self.punchFaceHoles)
        self.b_button = mc.button(label='Bevel Edges', backgroundColor=[0.67,0.29,0.29], command=self.ph_Bevel)
        self.e_button = mc.button(label='Extrude', backgroundColor=[0.80,0.80,1.00], command=self.ph_extrude)
        
        #Create Separators
        self.ph_circ_sep = mc.separator(h=5)
        self.ph_ext_sep = mc.separator(h=5)
        self.ph_bevel_sep = mc.separator(h=5)
        
        #Layout the window
        mc.formLayout(self.ph_layout, edit=True, 
                    attachForm = [ (self.ph_circ_text, 'top', 5),
                                    (self.ph_circ_offset, 'left',5), (self.ph_circ_offset, 'right',5),
                                    (self.ph_circ_sep, 'top', 5),(self.ph_circ_sep, 'left', 5), (self.ph_circ_sep, 'right', 5),
                                    
                                    (self.ph_ext_text, 'left', 5),
                                    (self.ph_ext_check, 'left', 5),
                                    (self.ph_ext_thickness, 'left', 5), (self.ph_ext_thickness, 'right', 5),
                                    (self.ph_ext_divisions, 'left', 5), (self.ph_ext_divisions, 'right', 5),
                                    (self.ph_ext_offset, 'left', 5), (self.ph_ext_offset, 'right', 5),
                                    (self.ph_ext_sep, 'top', 5),(self.ph_ext_sep, 'left', 5), (self.ph_ext_sep, 'right', 5),
                                    
                                    (self.ph_bevel_text, 'left', 5),
                                    (self.ph_bevel_fraction, 'left', 5), (self.ph_bevel_fraction, 'right', 5),
                                    (self.ph_bevel_divisions, 'left', 5), (self.ph_bevel_divisions, 'right', 5),
                                    (self.ph_bevel_chamfer, 'left', 5), (self.ph_bevel_chamfer, 'right', 5),
                                    (self.ph_bevel_sep, 'left', 5), (self.ph_bevel_sep, 'right', 5),
                                    
                                    (self.ph_bevel_sep, 'top', 5),(self.ph_bevel_sep, 'left', 5), (self.ph_bevel_sep, 'right', 5),
                                    (self.pvh_button, 'bottom', 5), (self.pvh_button, 'left', 5), (self.pvh_button, 'right', 5),
                                    (self.pfh_button, 'bottom', 5), (self.pfh_button, 'left', 5), (self.pfh_button, 'right', 5),
                                    (self.e_button, 'bottom', 5), (self.e_button, 'left', 5), (self.e_button, 'right', 5),
                                    (self.b_button, 'bottom', 5), (self.b_button, 'left', 5), (self.b_button, 'right', 5),
                    ],
                
                    attachControl = [ (self.ph_circ_offset, 'top', 5, self.ph_circ_text),
                                        (self.ph_circ_sep,'top', 5, self.ph_circ_offset),
                                        
                                        (self.ph_ext_text, 'top', 5, self.ph_circ_sep),
                                        (self.ph_ext_check, 'top', 5, self.ph_ext_text),
                                        (self.ph_ext_thickness, 'top', 5, self.ph_ext_check),
                                        (self.ph_ext_divisions, 'top', 5, self.ph_ext_thickness),
                                        (self.ph_ext_offset, 'top', 5, self.ph_ext_divisions),
                                        (self.ph_ext_sep, 'top', 5, self.ph_ext_offset),
                    
                                        (self.ph_bevel_text, 'top', 5, self.ph_ext_sep),
                                        (self.ph_bevel_fraction, 'top', 5, self.ph_bevel_text),
                                        (self.ph_bevel_divisions, 'top', 5, self.ph_bevel_fraction),
                                        (self.ph_bevel_chamfer, 'top', 5, self.ph_bevel_divisions),
                                        (self.ph_bevel_sep, 'top', 5, self.ph_bevel_chamfer),
                                        
                                        (self.pvh_button, 'top', 5, self.ph_bevel_sep),
                                        (self.pfh_button, 'top', 5, self.ph_bevel_sep),
                                        (self.e_button, 'top', 5, self.pvh_button),
                                        (self.b_button, 'top', 5, self.e_button),
                    ],
                    
                    attachPosition = [                                 
                                        (self.pvh_button, 'left', 5, 50), (self.pvh_button, 'bottom', 5, 65),
                                        (self.pfh_button, 'right', 5, 50),
                                        (self.e_button, 'left', 5, 50), (self.e_button, 'bottom', 5, 35),
                                        (self.b_button, 'left', 5, 50)                   
                    ]
                    )
        
        
        mc.menu(label='Documentation')
        mc.menuItem(label='Help', command=self.docs_help)
        mc.menuItem(label='About', command=self.docs_about)
        
        #Display the window
        mc.showWindow(self.ph_window)


    def docs_about(self, *args):
        about = mc.confirmDialog(
            title='About',
            ma='center',
            message='Punch Holes Script v1.0\n\n'
                'Created By John Kesig\n\n'
                'If you have any questions, would like to request a feature, might be able to make it better, or report an issue just let me know by sending me an email at: john.d.kesig@gmail.com\n\n'
                '\n\n\n\nThanks for using it!',
            button=['Done'],
            cancelButton='Done')
        return
        
    def docs_help(self, *args):
        doc_help = mc.confirmDialog(
            title='Help',
            message='Need a little assistance with the script? That\'s fine! I\'m here to help.\n\n'
            'You have essentially two ways of creating holes: Faces or Vertices\n\n'
            'All you need to do is configure your options how you want them to be used in the script, and then click either the following'
            'buttons: "Punch Holes by Face" or "Punch Holes by Vertex" \n\n'
            'Faces\n'
            'Configure your settings and the script will run over the following steps:\n'
            '\t1. Subdivide the face -> Triangulate the faces\n\t2. Chamfer the vertex at the center of the face -> Circularize vertices'
            '\n\t3. Select & Extrude triangular faces'
            '\n\t4. Bevel the edges'
            '\n\t5. Quadrangulate the extruded faces' 
            '\n\n\nVertices\n'
            'Configure your settings and the script will run over the following steps:\n'
            '\t1. Select the edges attached the vertex'
            '\n\t2. Poke the newly created face'
            '\n\t3. Select the center vertex -> Chamfer it -> Circularize components'
            '\n\t4. Select all faces with triangles and blast them away'
            '\n\t5. Select all Quad faces and extrude the geometry'
            '\n\t6. Select all border edges'
            '\n\n\nYou might be asking why I chose to keep beveling out of the Vertex side of the script. I did it for a couple of reasons.\n'
            '\t1. I do not have a good way of selecting the corner edges.'
            '\n\t2. Allow you to deselect the outside border edges before beveling. \n\nNow you may be asking'
            '"Why didn\'t you just deselect the borders of the geometry?" Well... I can\'t... Not with this method at least.'
            ' For now this is what I have and I am open for ideas on how to make this better! You could also think of it this way:'
            'It is a quick way of getting pieces beveled if you don\'t need to use the whole script!\n\n\n'
            '-John Kesig'
            '\n\n\n\n\nWhat\'s your favorite video game?',
            button=['Done'],
            cancelButton='Done')
            
        return
        
        
    def punchFaceHoles(self, *args):
        #Gather users face selection
        selection = mc.ls(sl=True)
        test_selection = str(selection)
        
        if '.f' not in test_selection:
            selection_check = mc.framelessDialog( title='Whoops', message='Your selection contains vertex(es)\\edge(s), or you do not have any components selected. \n\nPlease select only faces.',
	            button=['OK'], primary=['OK'])
        
        else:
            #We need to get the face to have a star formation of edges in the mesh. We subdivide for quads, then triangulate them for a star
            mc.polySubdivideFacet(cch=True, ch=True)
            mc.polyTriangulate()

            #Store the faces in a variables
            faces = mc.ls(sl=True)
            
            #Select the vertice directly in the middle of the star
            mc.polySelectConstraint(dis=True, mode=3, type=0x0001, order=1, orderbound=(8,20))
            vert = mc.ls(sl=True)

            #Chamfer the vertice and circularize the components
            mc.polyExtrudeVertex(width = 0.25)
            pfh_circ_offset=mc.floatSliderGrp(self.ph_circ_offset, query=True, value=True)
            
            version = int(mc.about(mjv=True))
            if version < 2023:
                mc.polyCircularizeEdge(radialOffset=pfh_circ_offset)
            else:
                mc.polyCircularize(radialOffset=pfh_circ_offset)
            
            #Select the inner triangular faces and store in them in a variable, then remove the constraint
            mc.polySelectConstraint(dis=True, mode=3, type=0x0008, size=1)
            triFaces = mc.ls(sl=True)
            mc.polySelectConstraint(mode=0, size=0)
            
            #Store the inner edges of the triangular faces, we need it as a reference for beveling later
            circIE = mc.polyListComponentConversion(triFaces, te=True, internal=True)

            #Select the triangular faces from before and extrude them to however deep they need to go
            mc.select(triFaces)
            pfh_ext_thickness = mc.floatSliderGrp(self.ph_ext_thickness, query=True, value=True)
            pfh_ext_divisions = mc.intSliderGrp(self.ph_ext_divisions, query=True, value=True)
            pfh_ext_offset = mc.floatSliderGrp(self.ph_ext_offset, query=True, value=True)
            mc.polyExtrudeFacet(thickness=pfh_ext_thickness, divisions=pfh_ext_divisions, offset=pfh_ext_offset)
            
            #Save the extruded border edge the script just created and bevel both the extruded edge and the inner edge
            circEE = mc.polyListComponentConversion(triFaces, te=True, bo=True)
            mc.select(circEE + circIE)
            pfh_bevel_chamfer = mc.checkBoxGrp(self.ph_bevel_chamfer, query=True, value1=True)
            pfh_bevel_fraction = mc.floatSliderGrp(self.ph_bevel_fraction, query=True, value=True)
            pfh_bevel_divisions = mc.intSliderGrp(self.ph_bevel_divisions, query=True, value=True)
            mc.polyBevel3(chamfer=pfh_bevel_chamfer, offsetAsFraction=True, fraction=pfh_bevel_fraction, segments=pfh_bevel_divisions)

            #Select the triangular faces on the inside of the bevel and run a Quadrangulate on them
            #I wish this worked a little more consistently but sadly it doesn't. You will need to go over the bad ones until I can figure out a way to make it more consistent
            mc.polySelectConstraint(mode=3, type=0x0008, size=1)
            mc.polySelectConstraint(mode=0)
            innerTriFaces = mc.ls(sl=True)
            mc.polyQuad(worldSpace=False)


            #Need this command in order for the user to go about their work
            mc.polySelectConstraint(mode=0)

        return
        
    def punchVertHoles(self, *args):
        #Gather users vertice selection
        selection = mc.ls(sl=True)
        test_selection = str(selection)

        if '.vtx' not in test_selection:
            mc.framelessDialog( title='Whoops', message='Your selection contains edge(s)\\face(s), or you do not have any components selected. \n\nPlease select only vertices.',
	            button=['OK'], primary=['OK'])    
        else:
            #Store the edge of the vertex in a variable and then delete the edges
            surEdges = mc.polyListComponentConversion(selection, fv=True, te=True, bo=True)
            mc.select(surEdges)
            mc.polyDelEdge()
            
            #Select the now newly created n-gon face from the deleted edges and poke the face to get the star formation
            mc.polySelectConstraint(mode=3, type=0x0008, size=3)
            mc.polySelectConstraint(mode=0, size=0)
            mc.polyPoke()
            
            #Select the center vertex in the star formation, chamfer the vertex, and circularize the components
            mc.polySelectConstraint(mode=3, type=0x0001, order=1, orderbound=(8,20))
            mc.polyExtrudeVertex(width=0.25)
            
            #Circularize components wasn't working as intended in versions of Maya previous to 2023. This should fix that
            version = int(mc.about(mjv=True))
            pvh_circ_offset = mc.floatSliderGrp(self.ph_circ_offset, query=True, value=True)
            
            if version < 2023:
                mc.polyCircularizeEdge(radialOffset=pvh_circ_offset)
            else:
                mc.polyCircularize(radialOffset=pvh_circ_offset)
            
            mc.polySelectConstraint(mode=0, size=0)
            
            #Select faces that have triangles and store them in a variable
            mc.polySelectConstraint(mode=3, type=0x0008, size=1)
            pvh_triFaces = mc.ls(sl=True)
            mc.polySelectConstraint(mode=0)
            
            #Using the triangular faces variable store a the star shaped edges in a new variable. Select the newly created edges and delete them.
            pvh_triEdges = mc.polyListComponentConversion(pvh_triFaces, ff=True, te=True, internal=True)
            mc.select(pvh_triEdges)
            mc.polyDelEdge()
            
            #Now we can select the newly created n-gon and select the border edges from it. We do this because it maintains edge count later in the process. Store the n-gon face and the border edges in a variable
            mc.polySelectConstraint(mode=3, type=0x0008, size=3)
            pvh_blastFace = mc.ls(sl=True)
            pvh_bEdge = mc.polyListComponentConversion(pvh_blastFace, ff=True, te=True, bo=True)
            
            #Select the n-gon face and blast it away. 
            mc.select(pvh_blastFace)
            mc.polyDelFacet()
            mc.polySelectConstraint(mode=0, size=0)
        
        return

    def ph_extrude(self, *args):
        
        #Select all the quad faces from the object and store them in a variable so that we can store the border edges in another variable
        mc.polySelectConstraint(mode=3, type=0x0008, size=2)
        pvh_bExtFaces = mc.ls(sl=True)
        pvh_bExtEdges = mc.polyListComponentConversion(pvh_bExtFaces, ff=True, te=True, bo=True)
            
        #Extrude the quad faces and store the extruded faces in a new variable and the new extruded border edges in a new variable 
        pvh_ext_check = mc.checkBoxGrp(self.ph_ext_check, query=True, value1=True)
        pvh_ext_thickness = mc.floatSliderGrp(self.ph_ext_thickness, query=True, value=True)
        pvh_ext_divisions = mc.intSliderGrp(self.ph_ext_divisions, query=True, value=True)
        pvh_ext_offset = mc.floatSliderGrp(self.ph_ext_offset, query=True, value=True)
        
        
        #Don't extrude if thickness is 0. This is to prevent issues with the mesh
        if pvh_ext_thickness == 0:
            return
        
        if pvh_ext_check == 1:
            mc.polyExtrudeFacet(thickness=pvh_ext_thickness, divisions=pvh_ext_divisions, offset=pvh_ext_offset)
            pvh_extGeo = mc.ls(sl=True)
            pvh_extEdges = mc.polyListComponentConversion(pvh_extGeo, ff=True, te=True, bo=True)
            
             #Reverse Normals if Extrusion Thickness is below 0
            if pvh_ext_thickness < 0:
                 mc.polySelectConstraint(mode=3, type=0x0008, size=2)
                 mc.polyNormal(normalMode=0)
     
            #Select all of the border edges from the variables we have declared and bevel them
        mc.select(pvh_bExtEdges + pvh_extEdges)
            
        mc.polySelectConstraint(mode=0, w=0)
            
        return
    
    def ph_Bevel(self, *args):
        #Gather the attributes you need from the UI, and apply them to the Bevel command
        ph_b_chamfer = mc.checkBoxGrp(self.ph_bevel_chamfer, query=True, value1=True)
        ph_b_fraction = mc.floatSliderGrp(self.ph_bevel_fraction, query=True, value=True)
        ph_b_divisions = mc.intSliderGrp(self.ph_bevel_divisions, query=True, value=True)
        mc.polyBevel3(chamfer=ph_b_chamfer, offsetAsFraction=True, fraction=ph_b_fraction, segments=ph_b_divisions)
        
        #Need this command in order for the user to go about their work
        mc.polySelectConstraint(mode=0)
        
        return
        
ph = punchHolesUI()