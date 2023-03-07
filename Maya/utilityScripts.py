# Utility Scripts v1.0
# Created by John Kesig
# Compatibility Versions for Maya 2022 & 2023
# Python 3 

class utilityScripts(object):
    def __init__(self):
        us_window = mc.window(title='Utility Scripts')
        us_form = mc.formLayout(numberOfDivisions=30)
        us_tabs = mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        mc.formLayout(us_form, edit=True, attachForm=[(us_tabs, 'top', 2), (us_tabs, 'left', 3), (us_tabs, 'bottom', 0),(us_tabs, 'right', 3)])
        
        # Arnold
        us_tab_arnold = mc.rowColumnLayout(numberOfColumns=1)
        
        # aiSubdivisions
        mc.separator(style='single', height=5, visible=False)
        mc.text(label='Subdivide')
        mc.separator(style='single', height=5, visible=True)
        self.us_aiSubdiv_check = mc.checkBoxGrp(label='Turn on Subdivisions? ', numberOfCheckBoxes=1, columnAttach=[1,'left', 3])
        mc.separator(style='single', height=2, visible=False)
        self.us_aiSubdiv_iterations = mc.intSliderGrp(label='Arnold Subdiv Iterations', field=True, columnAttach=[1,'left', 3], minValue=1, maxValue=7, value=1)
        mc.separator(style='single', height=10, visible=False)
        self.us_aiSubdiv_button = mc.button(label='Subdivide', recomputeSize=True, command=self.subdivideArnold)
        mc.setParent('..')
        
        # prman
        us_tab_prman = mc.rowColumnLayout(numberOfColumns=1)
        mc.text(label='Not yet worked out')
        
        mc.tabLayout( us_tabs, edit=True, tabLabel=((us_tab_arnold, 'Arnold'), (us_tab_prman, 'Renderman')) )
        
        mc.showWindow(us_window)
    
    def subdivideArnold(self, *args):
        selection = mc.ls(sl=True)
        
        aiSubdiv_iterations = mc.intSliderGrp(self.us_aiSubdiv_iterations, query=True, value=True)
        aiSubdiv_check = mc.checkBoxGrp(self.us_aiSubdiv_check, query=True, value1=True)
        
        if aiSubdiv_check == 1:
            
            for sel in selection:
                mc.setAttr("{0}.aiSubdivType".format(sel), 1)
                mc.setAttr("{0}.aiSubdivIterations".format(sel), aiSubdiv_iterations)
        else: 
            for sel in selection:
                mc.setAttr("{0}.aiSubdivType".format(sel), 0)
        
        return
        
utilityScripts()
