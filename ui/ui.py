from PySide import QtCore
from PySide import QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import system.utils as utils
import os

class RDojo_UI(object):
    def __init__(self, *args):
        print "In RDojo_UI"
        mi = cmds.window("MayaWindow", ma=True, q=True)
        for m in mi:
            if m == 'RDojo_Menu':
                cmds.deleteUI('RDojo_Menu', m=True)

        myMenu = cmds.menu('RDojo_Menu', l='RDMenu', to=True, p='MayaWindow')
        cmds.menuItem(l='Rig Tool', p=myMenu, command=self.LaunchUI)

    def LaunchUI(self, *args):
        print "Attempting To Launch..."
        print "...we live in: ", __name__
        # Development workaround for winEvent error when running
        # the script multiple times
        try:
            ui.close()
            ui.deleteLater()
        except:
            pass
        ui = RiggingToolUi()
        ui.show()

# *********************** #
# UI - PySide Experiments #
# *********************** #
def MayaMainWindow():
    # get 'pointer' for main Maya from omui
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QtGui.QWidget)
    else:
        print "ERROR OBTAINING POINTER"

class RiggingToolUi(QtGui.QDialog):
    def __init__(self, parent=MayaMainWindow()):
        super(RiggingToolUi, self).__init__(parent)

        self.setWindowTitle("Rigging Tool")
        self.setWindowFlags(QtCore.Qt.Tool)

        # Delete UI on close to avoid winEvent error
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        jsonFilePath = os.path.join(os.environ['RIGGING_TOOL'], 'layout', 'layout.json')
        self.jsonData = utils.readJson(jsonFilePath)
        self.projectRigData = self.jsonData['default']

        import rig.rig_arm as ra
        self.classyArm = ra.RigArm()

        self.create_layout()
        self.create_connections()


    def create_layout(self):
        # MenuBar is populated by Menus that are populated by Actions
        self.testMenu = QtGui.QMenuBar()
        self.fileMenu = QtGui.QMenu("File")
        self.fileMenu.addAction(QtGui.QAction("New", self, shortcut=QtGui.QKeySequence.New, statusTip="Create a new file", triggered=self.ThisDoesNothing))
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(QtGui.QAction("Open", self, shortcut=QtGui.QKeySequence.Open, statusTip="Open a file", triggered=self.ThisDoesNothing))
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(QtGui.QAction("Save", self, shortcut=QtGui.QKeySequence.Save, statusTip="Save current file", triggered=self.ThisDoesNothing))
        self.fileMenu.addAction(QtGui.QAction("As...", self, shortcut=QtGui.QKeySequence.SaveAs, statusTip="Save current file as...", triggered=self.ThisDoesNothing))
        self.testMenu.addMenu(self.fileMenu)

        # Buttons
        self.btn_rigFromJson = QtGui.QPushButton("Rig From JSON")
        self.btn_rigFromLocators = QtGui.QPushButton("Rig from LOCATORS")
        self.btn_saveLocatorsAsJson = QtGui.QPushButton("Save LOCATORS as JSON")
        self.btn_thisDoesNothing = QtGui.QPushButton("This Button Does Nothing")

        # Dropdowns
        self.lbl_projectsDrop = QtGui.QLabel("Project")
        self.dropDown_projects = QtGui.QComboBox()
        for k, v in self.jsonData.iteritems():
            self.dropDown_projects.addItem(k)
            #print k, v
        self.dropDown_projects.setToolTip("Set Your Project Root Here!")

        self.lbl_rigsDrop = QtGui.QLabel("Rigs")
        self.dropDown_rigs = QtGui.QComboBox()
        for k, v in self.jsonData.iteritems():
            self.dropDown_rigs.addItem(k)
            #print v
        self.dropDown_rigs.setToolTip("This currently does nothing...")

        # Bring it all together
        main_layout = QtGui.QVBoxLayout()

        project_dropDown_layout = QtGui.QHBoxLayout()
        project_dropDown_layout.addWidget(self.lbl_projectsDrop)
        project_dropDown_layout.addWidget(self.dropDown_projects)
        project_dropDown_layout.setStretch(0, 1)
        project_dropDown_layout.setStretch(1, 2)

        rigs_dropDown_layout = QtGui.QHBoxLayout()
        rigs_dropDown_layout.addWidget(self.lbl_rigsDrop)
        rigs_dropDown_layout.addWidget(self.dropDown_rigs)
        rigs_dropDown_layout.setStretch(0, 1)
        rigs_dropDown_layout.setStretch(1, 2)

        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(5)
        main_layout.addWidget(self.testMenu)
        main_layout.addLayout(project_dropDown_layout)
        main_layout.addLayout(rigs_dropDown_layout)
        main_layout.addWidget(self.btn_rigFromJson)
        main_layout.addWidget(self.btn_rigFromLocators)
        main_layout.addWidget(self.btn_saveLocatorsAsJson)
        main_layout.addWidget(self.btn_thisDoesNothing)
        main_layout.addStretch()

        self.setLayout(main_layout)


    def create_connections(self):
        self.dropDown_projects.currentIndexChanged.connect(self.ChangedProject)
        self.btn_rigFromJson.clicked.connect(self.RigFromJson)
        self.btn_rigFromLocators.clicked.connect(self.RigFromLocators)
        self.btn_saveLocatorsAsJson.clicked.connect(self.SaveLocatorsAsJson)
        self.btn_thisDoesNothing.clicked.connect(self.ThisDoesNothing)


    def ChangedProject(self):
        sender = self.sender()
        # currentIndex = sender.currentIndex()
        currentText = sender.currentText()
        # print "{0}, {1}, {2}".format(sender, currentIndex, currentText)
        self.projectRigData = self.jsonData[currentText]

    def RigFromJson(self):
        print "Rig From JSON"
        self.classyArm.DebugPrint()
        self.classyArm.rig_arm(self.projectRigData)


    def RigFromLocators(self):
        print "RIG FROM LOCATORS!"


    def SaveLocatorsAsJson(self):
        print "SAVE LOCATORS TO JSON!"


    def ThisDoesNothing(self):
        print "Ze Goggles..."
