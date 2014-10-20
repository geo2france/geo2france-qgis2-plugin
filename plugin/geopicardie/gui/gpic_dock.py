# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from geopicardie.gui.gpic_tree_items import GpicTreeWidgetItem
from geopicardie.utils.plugin_globals import GpicGlobals

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

    self.explorerWidget = QTreeWidget()
    self.explorerWidget.setHeaderLabel('')
    self.explorerWidget.setHeaderHidden(True)
    self.explorerWidget.itemDoubleClicked.connect(self.itemDoubleClicked)

    # context menu of the tree widget
    self.explorerWidget.setContextMenuPolicy(Qt.CustomContextMenu)
    self.explorerWidget.customContextMenuRequested.connect(self.openMenu)

    self.layout = QVBoxLayout()
    self.layout.setSpacing(2)
    self.layout.setMargin(0)
    self.layout.addWidget(self.explorerWidget)

    self.dockWidgetContents = QWidget()
    self.dockWidgetContents.setLayout(self.layout)
    self.setWidget(self.dockWidgetContents)  


  def setTreeContents(self, resources_tree):
    """
    Creates the items of the explorer widget
    """

    def createSubItem(subtree, parent_item = self.explorerWidget):
      """
      """

      if (not GpicGlobals.Instance().MASK_RESOURCES_WITH_WARN_STATUS or subtree.status != GpicGlobals.Instance().NODE_STATUS_WARN):
        subitem = GpicTreeWidgetItem(parent_item, subtree)
        if subtree.children != None and len(subtree.children) > 0:
          for child in subtree.children:
            createSubItem(child, subitem)

    self.explorerWidget.clear()

    if resources_tree == None:
      QgsMessageLog.logMessage(u"Faute de fichier de configuration valide, aucune ressource ne peut être chargée dans le panneau de l'extension GéoPicardie.", tag=u"GéoPicardie", level=QgsMessageLog.WARNING)
    elif resources_tree.children != None and len(resources_tree.children) > 0:
      for child in resources_tree.children:

        createSubItem(child, self.explorerWidget)


  def itemDoubleClicked(self, item, column):
    """
    Handles double clic on an item of the tre view
    """
    item.runDefaultAction()


  def openMenu(self, position):
    """
    Handles contextual menu in the tree view
    """
    selected_item = self.explorerWidget.currentItem()
    menu = selected_item.createMenu()
    menu.exec_(self.explorerWidget.viewport().mapToGlobal(position))


  def dockStateChanged(self, floating):
    """
    """

    if floating:
      self.resize(300, 450)
    else:
      pass

