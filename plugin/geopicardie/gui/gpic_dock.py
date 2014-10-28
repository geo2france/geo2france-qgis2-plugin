# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from geopicardie.gui.gpic_tree_widget import GpicTreeWidget


class GpicDockWidget(QDockWidget):
  """
  The dock widget containing the tree view displaying the GéoPicardie resources
  """


  def __init__(self, parent = None):
    """
    """

    super(GpicDockWidget, self).__init__()
    objectName = 'GpicDock'
    self.initGui()


  def initGui(self):
    """
    """

    self.setWindowTitle(u'GéoPicardie')
    self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

    self.treeWidget = GpicTreeWidget()

    self.layout = QVBoxLayout()
    self.layout.setSpacing(2)
    self.layout.setMargin(0)
    self.layout.addWidget(self.treeWidget)

    self.dockWidgetContents = QWidget()
    self.dockWidgetContents.setLayout(self.layout)
    self.setWidget(self.dockWidgetContents)  


  def setTreeContents(self, resources_tree):
    """
    Creates the items of the tree widget
    """

    self.treeWidget.setTreeContents(resources_tree)


  def dockStateChanged(self, floating):
    """
    """

    if floating:
      self.resize(300, 450)
    else:
      pass

