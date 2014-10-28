# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from geopicardie.gui.gpic_tree_items import GpicTreeWidgetItem
from geopicardie.utils.plugin_globals import GpicGlobals


class GpicTreeWidget(QTreeWidget):
  """
  The tree widget used in the GéoPicardie dock
  """

  def __init__(self):

    objectName = 'GpicTreeWidget'

    super(GpicTreeWidget, self).__init__()

    # Selection
    self.setSelectionMode(QAbstractItemView.SingleSelection)

    # Columns and headers
    self.setColumnCount(1)
    self.setHeaderLabel('')
    self.setHeaderHidden(True)

    # Events
    self.itemDoubleClicked.connect(self.treeItemDoubleClicked)

    # Context menu
    self.setContextMenuPolicy(Qt.CustomContextMenu)
    self.customContextMenuRequested.connect(self.openMenu)

    # Enable drag of tree items
    self.setDragEnabled(True)


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


  # Constant and methods used for drag and drop of tree items onto the map

  QGIS_URI_MIME = "application/x-vnd.qgis.qgis.uri"

  def mimeTypes(self):
    """
    """

    return [self.QGIS_URI_MIME]


  def mimeData(self, items):
    """
    """

    mimeData = QTreeWidget.mimeData(self, items)
    encodedData = QByteArray()
    stream = QDataStream(encodedData, QIODevice.WriteOnly)

    for item in items:
      layerMimeData = item.gpic_data.layerMimeData()
      stream.writeQString(layerMimeData)

    mimeData.setData(self.QGIS_URI_MIME, encodedData)
    return mimeData
