# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4 import QtGui

from geopicardie.utils.gpic_node_types import *
from geopicardie.utils.gpic_icons import *



class GpicTreeWidgetItem(QtGui.QTreeWidgetItem):
  """
  An item of tree view.
  """

  def __init__(self, parent, gpic_data = None):
    """
    """

    QtGui.QTreeWidgetItem.__init__(self, parent)

    self.gpic_data = gpic_data
    self.setText(0, gpic_data.title)

    gpicIcons = GpicIcons.Instance()
    icon = None

    if self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_FOLDER:
      icon = gpicIcons.folder_icon
    elif self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMS_LAYER:
      icon = gpicIcons.wms_layer_icon
    elif self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMS_LAYER_STYLE:
      icon = gpicIcons.wms_style_icon
    elif self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
      icon = gpicIcons.wfs_layer_icon

    if icon != None:
      self.setIcon(0, icon)
      
    self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)


  def runDefaultAction(self):
    """
    """

    if self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_FOLDER:
      pass
    elif self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMS_LAYER:
      self.runAddToMapAction()
    elif self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMS_LAYER_STYLE:
      self.runAddToMapAction()
    elif self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
      self.runAddToMapAction()


  def runAddToMapAction(self):
    """
    """

    self.gpic_data.runAddToMapAction()


  def runShowMetadataAction(self):
    """
    """

    pass


  def createMenu(self):
    """
    Creates a contextual menu
    """

    menu = QtGui.QMenu()

    if self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_FOLDER:
      menu.addAction(u"Envoyer des chouquettes à l'administrateur de GéoPicardie...")
    elif self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMS_LAYER:
      add_to_map_action = menu.addAction(u"Ajouter à la carte")
      add_to_map_action.triggered.connect(self.runAddToMapAction)
      show_metadata_action = menu.addAction(u"Afficher les métadonnées...")
      show_metadata_action.triggered.connect(self.runShowMetadataAction)
    elif self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMS_LAYER_STYLE:
      add_to_map_action = menu.addAction(u"Ajouter à la carte")
      add_to_map_action.triggered.connect(self.runAddToMapAction)
    elif self.gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
      add_to_map_action = menu.addAction(u"Ajouter à la carte")
      add_to_map_action.triggered.connect(self.runAddToMapAction)
      show_metadata_action = menu.addAction(u"Afficher les métadonnées...")
      show_metadata_action.triggered.connect(self.runShowMetadataAction)

    return menu