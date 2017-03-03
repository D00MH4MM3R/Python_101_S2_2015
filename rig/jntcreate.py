import maya.cmds as cmds

rig_info = {}

## Creating the joint chains ##
def jointCreation(prefix, chainTypes, name, position):
    # an empty list to store joints in the function
    joints = []
    for n in name:
        #For each chain created, it then creates each joint specified in the name argument #            
        joints.append(cmds.joint(n = prefix + '_' + chainTypes + '_' + n + '_jnt', p = position[name.index(n)]))
        if name.index(n) != 0:
            # If the joint isnt the first one, it will orient it's parent #
            joints.append(cmds.joint(prefix + '_' + chainTypes + '_' + name[name.index(n)-1] + '_jnt', e = True, zso = True, oj = 'xyz', sao = 'yup'))
    cmds.select(d=True)
    
    # dont forget return
    return joints

rig_info['ikJnts'] = jointCreation('c', 'IK', ['shoulder', 'elbow', 'wrist', 'endWrist'], [[0, 0, 0], [7, 0, -1], [14, 0, 0], [15, 0, 0]])