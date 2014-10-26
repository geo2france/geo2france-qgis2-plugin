# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from geopicardie.gui.gpic_tree_items import GpicTreeWidgetItem
from geopicardie.utils.plugin_globals import GpicGlobals

class GpicTreeWidget(QTreeWidget):
  """
  The tree widget used in the GéoPicardie dock
  """

  def __init__(self):

    objectName = 'GpicTreeWidget'

    super(GpicTreeWidget, self).__init__()
    # QTreeWidget.__init__(self, None)

    # Selection
    self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    # Columns and headers
    self.setColumnCount(1)
    self.setHeaderLabel('')
    self.setHeaderHidden(True)

    # Events
    self.itemDoubleClicked.connect(self.treeItemDoubleClicked)
    # self.itemExpanded.connect(self.treeItemExpanded)
    # self.itemClicked.connect(self.treeItemClicked)

    # Context menu
    self.setContextMenuPolicy(Qt.CustomContextMenu)
    self.customContextMenuRequested.connect(self.openMenu)

    # Drag and drop mode
    self.setDragDropMode(QTreeWidget.DragDrop)
    # self.setAcceptDrops(True)
    # self.setDropIndicatorShown(True)
    # self.setAutoScroll(True)


  def setTreeContents(self, resources_tree):
    """
    Creates the items of the tree widget
    """

    def createSubItem(subtree, parent_item = self):
      """
      """

      if (not GpicGlobals.Instance().MASK_RESOURCES_WITH_WARN_STATUS or subtree.status != GpicGlobals.Instance().NODE_STATUS_WARN):
        subitem = GpicTreeWidgetItem(parent_item, subtree)
        if subtree.children != None and len(subtree.children) > 0:
          for child in subtree.children:
            createSubItem(child, subitem)

    self.clear()

    if resources_tree == None:
      QgsMessageLog.logMessage(u"Faute de fichier de configuration valide, aucune ressource ne peut être chargée dans le panneau de l'extension GéoPicardie.", tag=u"GéoPicardie", level=QgsMessageLog.WARNING)
    elif resources_tree.children != None and len(resources_tree.children) > 0:
      for child in resources_tree.children:
        createSubItem(child, self)


  def treeItemDoubleClicked(self, item, column):
    """
    Handles double clic on an item
    """
    item.runDefaultAction()


  def openMenu(self, position):
    """
    Handles context menu in the tree
    """
    selected_item = self.currentItem()
    menu = selected_item.createMenu()
    menu.exec_(self.viewport().mapToGlobal(position))

