# Utility Scripts v1.0
# Created by John Kesig
# Compatibility Versions for Maya 2022 & 2023
# Python 3 

class utilityScripts(object):
    def __init__(self):
        self.us_window = mc.window(title='Utility Scripts')
        self.us_layout = mc.formLayout(numberOfDivisions=30)
        
        # Arnold Render Settings
        self.us_aiSettings_text = mc.text(label='Arnold Mesh Settings')
        
        # Arnold Subdivisions
        self.us_aiSubdiv_check = mc.checkBoxGrp(label='Turn on Subdivisions? ', numberOfCheckBoxes=1)
        
        self.us_aiSubdiv_iterations = mc.intSliderGrp(label='Arnold Subdiv Iterations', field=True, minValue=1, maxValue=7, value=1)
        self.us_aiSubdiv_button = mc.button(label='Subdivide', recomputeSize=True, command=self.subdivideArnold)
        
        # Turn off objects
        
        # Separators
        self.us_separator01 = mc.separator(style='none')
        
        mc.formLayout(self.us_layout, edit=True,
            attachForm = [ (self.us_aiSettings_text, 'top', 5), 
                          (self.us_aiSubdiv_check, 'left', 5),
                          (self.us_aiSubdiv_iterations, 'left', 5), (self.us_aiSubdiv_iterations, 'right', 5)
                          ],
            
            attachControl = [(self.us_separator01, 'top', 5, self.us_aiSettings_text),
                             (self.us_aiSubdiv_check, 'top', 5, self.us_separator01),
                             (self.us_aiSubdiv_iterations, 'top', 5, self.us_aiSubdiv_check),
                             (self.us_aiSubdiv_button, 'top', 5, self.us_aiSubdiv_iterations)
                            
                             ],
            
            attachPosition = [(self.us_aiSubdiv_button, 'left', 0, 15)
                              ]
            )
    
        
        mc.showWindow(self.us_window)
    
    def subdivideArnold(self, *args):
        selection = mc.ls(sl=True)
        
        aiSubdiv_iterations = mc.intSliderGrp(self.us_aiSubdiv_iterations, query=True, value=True)
        aiSubdiv_check = mc.checkBoxGrp(self.us_aiSubdiv_check, query=True, value1=True)
        
        if aiSubdiv_check == 1:
            
            for sel in selection:
                mc.setAttr("{0}.aiSubdivType".format(sel), 1)
                mc.setAttr("{0}.aiSubdivIterations".format(sel), aiSubdiv_iterations)
        
        return
        
utilityScripts()
