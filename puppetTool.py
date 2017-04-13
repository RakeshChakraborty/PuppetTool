import maya.cmds as cmds

if (cmds.window("repoWindow", exists=True)):
    cmds.deleteUI("repoWindow")

repoWindow = cmds.window("repoWindow" ,title="Puppet" , widthHeight=(600, 300))


cmds.columnLayout( "firstColumn",adjustableColumn=True )

#__________Record Anim Window________

cmds.frameLayout ("recAnimFrame", label="Record animation" ,cll=1, parent = "firstColumn")
cmds.columnLayout( adjustableColumn=True )
cmds.text( label='It will delete previous puppet data if you have any' ,align='left', h=20, parent = "recAnimFrame")
recordRange = cmds.radioButtonGrp( "recordOption",label='Record Range : ', labelArray2=['time slider range', 'custom'], numberOfRadioButtons=2 , sl=1 , cc="enableButton()",parent = "recAnimFrame")
#recordRange = cmds.checkBox(label = "Use time slider" , value=1, ofc="enableButton()" , onc="disableButton()", parent = "recAnimFrame")
cmds.rowLayout("newRow", numberOfColumns=3, columnWidth3 = ( 100 ,30 ,100 ), h=50, parent = "recAnimFrame")
myRecRange1 = cmds.intField( editable=True, en=False, parent = "newRow" )
cmds.text( label=' To ' ,align='left', parent = "newRow")
myRecRange2 = cmds.intField( editable=True, en=False, parent = "newRow" )
cmds.button( label = 'Record animation' , parent = "recAnimFrame" , w=200, c= "recordAnimation()")

#_________Apply Anim Window___________

cmds.columnLayout( "secondColumn",adjustableColumn=True , parent = "firstColumn")
cmds.frameLayout ("applyAnimFrame", label="Apply animation" , cll=1, parent = "secondColumn")
cmds.columnLayout("aaColumn1", adjustableColumn=True, parent = "applyAnimFrame" )
cmds.text( label='Select specific controllers or it applies to all' ,align='left', parent = "aaColumn1")
applyRange = cmds.radioButtonGrp("applyAnimRange", label='Apply Range : ', labelArray2=['time slider range', 'custom'], numberOfRadioButtons=2 , sl=1 ,  cc="enableApplyButton()", parent = "applyAnimFrame")
cmds.rowLayout("newRow2", numberOfColumns=3, columnWidth3 = ( 100 ,30 ,100 ), h=50, parent = "applyAnimFrame")
myAppRange1 = cmds.intField( editable=True, en=False, parent = "newRow2" )
cmds.text( label=' To ' ,align='left', parent = "newRow2")
myAppRange2 = cmds.intField( editable=True, en=False, parent = "newRow2" )

applyRange = cmds.radioButtonGrp("applyAnimOption", label='Apply Range : ', labelArray2=['Smart apply', 'Bake'], numberOfRadioButtons=2 , sl=1 ,  cc="applyOptionField()", parent = "applyAnimFrame")
cmds.rowLayout("smartRow", numberOfColumns=2, columnWidth2 = ( 100 ,100 ), h=50, parent = "applyAnimFrame")
framePaddingT = cmds.text( label=' Frame padding :' ,align='left', parent = "smartRow", en=False)
framePadding = cmds.intField( editable=True, en=False, parent = "smartRow")
cmds.button( label = 'Apply animation' , parent = "applyAnimFrame" , w=200, c="applyAnimation()")

#__________Delete Repo data____________

cmds.columnLayout( "thirdColumn",adjustableColumn=True , parent = "firstColumn")
cmds.frameLayout ("deleteRepoData", label="Delete Puppet data" , cll=1, parent = "thirdColumn")
cmds.text( label=' It will delete all puppet data generated ' ,align='left', parent = "deleteRepoData")
cmds.button( label = 'Delete data' , parent = "deleteRepoData" , w=200, c="deleteRepoData()")




cmds.showWindow(repoWindow)


#______________________________________________________________

def enableButton():
    if cmds.radioButtonGrp ("recordOption", q=1, sl=1) == 1 :
        cmds.intField( myRecRange1, e=True , en=False )
        cmds.intField( myRecRange2, e=True , en=False )
    else:
        cmds.intField( myRecRange1, e=True , en=True )
        cmds.intField( myRecRange2, e=True , en=True )


#______________________________________________________________

def enableApplyButton():
    if cmds.radioButtonGrp ("applyAnimRange", q=1, sl=1) == 1 :
        cmds.intField( myAppRange1, e=True , en=False )
        cmds.intField( myAppRange2, e=True , en=False )
    else:
        cmds.intField( myAppRange1, e=True , en=True )
        cmds.intField( myAppRange2, e=True , en=True )
        
#_______________________________________________________________

def applyOptionField():
    if cmds.radioButtonGrp ("applyAnimOption", q=1, sl=1) == 1 :
        cmds.intField( framePadding, e=True , en=False )
        cmds.text( framePaddingT, e=True , en=False )
    else:
        cmds.intField( framePadding, e=True , en=True )
        cmds.text( framePaddingT, e=True , en=True )

#_______________________________________________________________


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def recordAnimation(): #getting the value of frame range specified by user
    #global tminRec = 0
    #global tmaxRec = 0
    if (cmds.objExists('cogGroupParent')):
        cmds.delete ("cogGroupParent*")
        
    if cmds.radioButtonGrp ("recordOption", q=1, sl=1) == 2:
        print "we are here"
        tminRec = cmds.intField(myRecRange1, v=1 ,q=1)
        tmaxRec = cmds.intField(myRecRange2, v=1 ,q=1)
    else:
        tminRec = cmds.playbackOptions( q=1,min=1 )
        tmaxRec = cmds.playbackOptions( q=1,max=1 )



    #______________RECORD ANIMATION_____________

    cogObjSel = cmds.ls(sl=1)
    global varSelect
    varSelect = cogObjSel
    
    avgPos = cmds.ls( sl=1, fl=1)
    
    xPosSum = 0
    yPosSum = 0
    zPosSum = 0
    
    # find average world position of selected objects
    for obj in avgPos: # adding xyz values
        worldSpacePos = cmds.xform(obj ,ws=1 , q=1 , t=1)
        xPosSum += worldSpacePos[0]
        yPosSum += worldSpacePos[1]
        zPosSum += worldSpacePos[2]
        
    avgWorldPos = [ xPosSum / len(avgPos) , yPosSum / len(avgPos) , zPosSum / len(avgPos) ] # dividing added values by number of object selected
    
    cmds.circle(center=(avgWorldPos[0],avgWorldPos[1],avgWorldPos[2]) , sw=360 , ch=1 , n = 'cogGroupParent')
    cmds.CenterPivot()
    
    for obj in cogObjSel : #duplicating selected objects
        
        parentflagTrans = []  # checking if attributes are locked or unlocked
        if cmds.getAttr(obj+".translateX", l=1):
            parentflagTrans.extend(["x"])
        else:
            parentflagTrans.extend(["none"])
        if cmds.getAttr(obj+".translateY", l=1):
            parentflagTrans.extend(["y"])
        else:
            parentflagTrans.extend(["none"])
        if cmds.getAttr(obj+".translateZ", l=1):
            parentflagTrans.extend(["z"])
        else:
            parentflagTrans.extend(["none"])
            
        parentflagRot = []
        if cmds.getAttr(obj+".rotateX", l=1):
            parentflagRot.extend(["x"])
        else:
            parentflagRot.extend(["none"])
        if cmds.getAttr(obj+".rotateY", l=1):
            parentflagRot.extend(["y"])
        else:
            parentflagRot.extend(["none"])
        if cmds.getAttr(obj+".rotateZ", l=1):
            parentflagRot.extend(["z"])
        else:
            parentflagRot.extend(["none"])
        
        
        cmds.duplicate( obj ,n=obj+'_cogCtrl', rc = True)
        unwantedChild = cmds.listRelatives(obj+'_cogCtrl', ad = True) # lists all the child of selected parent objects
        lockParentName = cmds.listRelatives(obj+'_cogCtrl', ad = True)
        del unwantedChild[0] # Removes the parent from the list
        cmds.delete(unwantedChild) # deletes all the child
        #dele = cmds.duplicate( obj ,n=obj+'_S' , un=0) 
        #cmds.parent( obj+'_SShape' , obj+'_cogCtrl' , r=1 , s=1) # avoiding duplicates of child
        #cmds.delete (dele[0]) # avoiding duplicates of child
        cmds.setAttr (lockParentName[0]+".overrideEnabled",1)
        cmds.setAttr (lockParentName[0]+".overrideDisplayType" ,2)
        cmds.parent( obj+'_cogCtrl', 'cogGroupParent' )
        cmds.parentConstraint( obj , obj+'_cogCtrl' , mo = 0, w = 1 , st= parentflagTrans , sr=parentflagRot )
        cmds.bakeResults( obj+'_cogCtrl', simulation=0 , smart=1 , t=(tminRec,tmaxRec) )
        cmds.delete(cn=True)
        del unwantedChild[:]
        del parentflagRot[:]
        del parentflagTrans[:]
        
    cmds.select("cogGroupParent")     
      
        
#///////////////////////////////////////////////////////APPLY ANIMATION/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////        
        
def applyAnimation():
    
    
    
    if cmds.radioButtonGrp ("applyAnimRange", q=1, sl=1) == 2:
        
        tminApp = cmds.intField(myAppRange1, v=1 ,q=1)
        tmaxApp = cmds.intField(myAppRange2, v=1 ,q=1)
    else:
        tminApp = cmds.playbackOptions( q=1,min=1 )
        tmaxApp = cmds.playbackOptions( q=1,max=1 )
        
        

    if cmds.radioButtonGrp ("applyAnimOption", q=1, sl=1) == 1:
        smartValue = 1
    else:
        smartValue = 0
        
        
        
    cogObjSelApply = cmds.ls(sl=1)
    applyObjNum = len(cogObjSelApply)
    
    print smartValue
    
    if len(cogObjSelApply) == 0 : # this will apply to previous selected objects
        
        cogObjSelApply = varSelect
        
        
        for obj in cogObjSelApply:
            
            samplebyValue = cmds.intField(framePadding, v=1 ,q=1)
            
            parentflagTransApply = []
            if cmds.getAttr(obj+".translateX", l=1):
                parentflagTransApply.extend(["x"])
            else:
                parentflagTransApply.extend(["none"])
            if cmds.getAttr(obj+".translateY", l=1):
                parentflagTransApply.extend(["y"])
            else:
                parentflagTransApply.extend(["none"])
            if cmds.getAttr(obj+".translateZ", l=1):
                parentflagTransApply.extend(["z"])
            else:
                parentflagTransApply.extend(["none"])
                
            parentflagRotApply = []
            if cmds.getAttr(obj+".rotateX", l=1):
                parentflagRotApply.extend(["x"])
            else:
                parentflagRotApply.extend(["none"])
            if cmds.getAttr(obj+".rotateY", l=1):
                parentflagRotApply.extend(["y"])
            else:
                parentflagRotApply.extend(["none"])
            if cmds.getAttr(obj+".rotateZ", l=1):
                parentflagRotApply.extend(["z"])
            else:
                parentflagRotApply.extend(["none"])
                
            constrainApply = cmds.parentConstraint( obj+'_cogCtrl', obj , mo = 0, w = 1 , st= parentflagTransApply , sr=parentflagRotApply)
            
            
            if cmds.radioButtonGrp ("applyAnimOption", q=1, sl=1) == 1:
            
                cmds.bakeResults( obj, sm=0 , smart = smartValue , t=(tminApp,tmaxApp) , pok=1)
                cmds.delete(constrainApply)
            else:
                cmds.bakeResults( obj, sm=0  , t=(tminApp,tmaxApp) , pok=1 , sb = samplebyValue)
                cmds.delete(constrainApply)
            
            
            del parentflagRotApply[:]
            del parentflagTransApply[:]
            
            
            
    else: # this will apply to selected objects only
        
        for obj in cogObjSelApply:
            
            
            samplebyValue = cmds.intField(framePadding, v=1 ,q=1)
            print samplebyValue
            
            parentflagTransApply = []
            if cmds.getAttr(obj+".translateX", l=1):
                parentflagTransApply.extend(["x"])
            else:
                parentflagTransApply.extend(["none"])
            if cmds.getAttr(obj+".translateY", l=1):
                parentflagTransApply.extend(["y"])
            else:
                parentflagTransApply.extend(["none"])
            if cmds.getAttr(obj+".translateZ", l=1):
                parentflagTransApply.extend(["z"])
            else:
                parentflagTransApply.extend(["none"])
                
            parentflagRotApply = []
            if cmds.getAttr(obj+".rotateX", l=1):
                parentflagRotApply.extend(["x"])
            else:
                parentflagRotApply.extend(["none"])
            if cmds.getAttr(obj+".rotateY", l=1):
                parentflagRotApply.extend(["y"])
            else:
                parentflagRotApply.extend(["none"])
            if cmds.getAttr(obj+".rotateZ", l=1):
                parentflagRotApply.extend(["z"])
            else:
                parentflagRotApply.extend(["none"])
            
            
            constrainApply = cmds.parentConstraint( obj+'_cogCtrl', obj , mo = 0, w = 1 , st= parentflagTransApply , sr=parentflagRotApply)
            
            if cmds.radioButtonGrp ("applyAnimOption", q=1, sl=1) == 1:
            
                cmds.bakeResults( obj, sm=0 , smart = smartValue , t=(tminApp,tmaxApp) , pok=1)
                cmds.delete(constrainApply)
            else:
                cmds.bakeResults( obj, sm=0  , t=(tminApp,tmaxApp) , pok=1 , sb = samplebyValue)
                cmds.delete(constrainApply)
            
            del parentflagRotApply[:]
            del parentflagTransApply[:]

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



def deleteRepoData():
    if (cmds.objExists('cogGroupParent')):
        cmds.delete ("cogGroupParent*")
    else:
        print "Nothing to delete"
