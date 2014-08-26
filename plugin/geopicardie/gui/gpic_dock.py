# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from geopicardie.gui.gpic_tree_items import GpicTreeWidgetItem
   
class GpicDockWidget(QDockWidget):
  """
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

    self.explorerWidget = QTreeWidget()
    self.explorerWidget.setHeaderLabel('')
    self.explorerWidget.setHeaderHidden(True)
    self.explorerWidget.itemDoubleClicked.connect(self.itemDoubleClicked)

    self.layout = QVBoxLayout()
    self.layout.setSpacing(2)
    self.layout.setMargin(0)
    self.layout.addWidget(self.explorerWidget)

    self.dockWidgetContents = QWidget()
    self.dockWidgetContents.setLayout(self.layout)
    self.setWidget(self.dockWidgetContents)  


  def setTreeContents(self, resources_tree):
    """
    """

    def createSubItem(subtree, parent_item = self.explorerWidget):
      """
      """

      subitem = GpicTreeWidgetItem(parent_item, subtree)

      if subtree.children != None and len(subtree.children) > 0:
        for child in subtree.children:
          createSubItem(child, subitem)

    if resources_tree.children != None and len(resources_tree.children) > 0:
      for child in resources_tree.children:
        createSubItem(child, self.explorerWidget)

  def itemDoubleClicked(self, item, column):
    """
    """

    # QMessageBox.information(self, 'Info Message', 'double-clic',
    #       QMessageBox.Ok)
    item.runAction()


  def dockStateChanged(self, floating):
    """
    """

    if floating:
      self.resize(300, 450)
    else:
      pass

