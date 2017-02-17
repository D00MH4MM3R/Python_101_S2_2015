'''
Rhonda Ray

Description:  creates different shapes for controls

'''

import pymel.core as pm 

def circle(self, ctrlName):
	ctrl = pm.circle(name=ctrlName, normal=(1,0,0), center=(0,0,0), radius=1.5, constructionHistory=False)
	
	return ctrl


def square(self, ctrlName):
	ctrl = pm.curve(name=ctrlName, degree=1, point=[(0.5,0,0.5), (0.5,0,-0.5), (-0.5,0,-0.5), (-0.5,0,0.5), (0.5,0,0.5)], knot=[0, 1, 2, 3, 4])
	pm.xform(scale=(1.5, 1.5, 1.5), rotation=(0, 0, 90), preserve=True, centerPivots=True)
	pm.makeIdentity(apply=True, translate=True, rotate=True, scale=True, normal=False, preserveNormals=True)
	
	return ctrl 
	

def pointer(self, ctrlName):
	ctrl = pm.circle(name=ctrlName, normal=(0,1,0), radius=1)[0]
	pm.select(ctrlName+'.ep[2:3]', ctrlName+'.ep[5:6]', replace=True)
	pm.xform(scale=[.318733, 1, 1])
	pm.select(ctrlName+'.ep[3]', ctrlName+'.ep[5]', replace=True)
	pm.xform(scale=[.400636, 1, 1])

	return ctrl


def text(self, ctrlName, txt):
	ctrl = pm.textCurves(name=ctrlName, font='Courier', text=txt)

	# get curves
	nurbsShapes = pm.ls(pm.listRelatives(ctrl, allDescendents=True), type='nurbsCurve')

	# parent shapes to a single transform
	for letter in nurbsShapes:
	    nurbsTransforms = pm.listRelatives(letter, parent=True)[0]
	    nurbsTransforms = pm.parent(nurbsTransforms, world=True)
	    pm.makeIdentity(nurbsTransforms, apply=True, translate=True, rotate=True, scale=True, normal=False)

	    pm.parent(letter, ctrl[0], relative=True, shape=True)
	    pm.delete(nurbsTransforms)

	# delete unused transforms
	txtChildren = pm.listRelatives(ctrl, children=True, type='transform')
	if txtChildren:
		pm.delete(txtChildren)

	return ctrl