# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4 import QtGui

from geopicardie.utils.plugin_globals import GpicGlobals
from geopicardie.utils.gpic_icons import *



def expandItemAndSubitems(item):
  """
  """

  if not item.isExpanded():
    item.setExpanded(True)

  nb_subitems = item.childCount()

  for i in range(nb_subitems):
    expandItemAndSubitems(item.child(i))


def collapseItemAndSubitems(item):
  """
  """

  if item.isExpanded():
    item.setExpanded(False)

  nb_subitems = item.childCount()

  for i in range(nb_subitems):
    collapseItemAndSubitems(item.child(i))


def containsUnexpandedSubitems(item):
  """
  """

  if not item.isExpanded():
    return True

  nb_subitems = item.childCount()

  for i in range(nb_subitems):
    if containsUnexpandedSubitems(item.child(i)):
      return True

  return False



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
    self.setToolTip (0, gpic_data.description)

    gpicIcons = GpicIcons.Instance()
    icon = None

    if self.gpic_data.status == GpicGlobals.Instance().NODE_STATUS_WARN:
      icon = gpicIcons.warn_icon
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_FOLDER:
      icon = gpicIcons.folder_icon
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER:
      icon = gpicIcons.wms_layer_icon
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER_STYLE:
      icon = gpicIcons.wms_style_icon
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
      icon = gpicIcons.wfs_layer_icon
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE_FILTER:
      icon = gpicIcons.wfs_layer_icon
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_GDAL_WMS_CONFIG_FILE:
      icon = gpicIcons.raster_layer_icon

    if icon != None:
      self.setIcon(0, icon)
      
    self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)


  def runDefaultAction(self):
    """
    """

    if self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_FOLDER:
      pass
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER:
      self.runAddToMapAction()
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER_STYLE:
      self.runAddToMapAction()
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
      self.runAddToMapAction()
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE_FILTER:
      self.runAddToMapAction()
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_GDAL_WMS_CONFIG_FILE:
      self.runAddToMapAction()


  def runAddToMapAction(self):
    """
    Add the resource to the map
    """

    self.gpic_data.runAddToMapAction()


  def runShowMetadataAction(self):
    """
    Displays the resource metadata
    """

    self.gpic_data.runShowMetadataAction()


  def containsUnexpandedSubitems(self):
    """
    Determines if subitems are not expanded
    """

    if not self.isExpanded():
      return True
    else:
      return containsUnexpandedSubitems(self)


  def runExpandAllSubItemsAction(self):
    """
    Expands all subitems
    """

    expandItemAndSubitems(self)


  def runCollapseAllSubItemsAction(self):
    """
    Expands all subitems
    """

    collapseItemAndSubitems(self)


  def runReportIssueAction(self):
    """
    Report an issue
    """
    
    self.gpic_data.runReportIssueAction()



  def createMenu(self):
    """
    Creates a contextual menu
    """

    menu = QtGui.QMenu()

    # report_issue_action = menu.addAction(u"Signaler une anomalie...")
    # report_issue_action.triggered.connect(self.runReportIssueAction)

    if self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_FOLDER:
      pass
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER:
      add_to_map_action = menu.addAction(u"Ajouter à la carte")
      add_to_map_action.triggered.connect(self.runAddToMapAction)
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER_STYLE:
      add_to_map_action = menu.addAction(u"Ajouter à la carte")
      add_to_map_action.triggered.connect(self.runAddToMapAction)
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
      add_to_map_action = menu.addAction(u"Ajouter à la carte")
      add_to_map_action.triggered.connect(self.runAddToMapAction)
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE_FILTER:
      add_to_map_action = menu.addAction(u"Ajouter à la carte")
      add_to_map_action.triggered.connect(self.runAddToMapAction)
    elif self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_GDAL_WMS_CONFIG_FILE:
      add_to_map_action = menu.addAction(u"Ajouter à la carte")
      add_to_map_action.triggered.connect(self.runAddToMapAction)

    if self.gpic_data.metadata_url:
      show_metadata_action = menu.addAction(u"Afficher les métadonnées...")
      show_metadata_action.triggered.connect(self.runShowMetadataAction)

    if self.childCount() > 0 and self.containsUnexpandedSubitems():
      expand_all_subitems_action = menu.addAction(u"Afficher tous les descendants")
      expand_all_subitems_action.triggered.connect(self.runExpandAllSubItemsAction)

    if self.childCount() > 0 and self.isExpanded():
      expand_all_subitems_action = menu.addAction(u"Masquer tous les descendants")
      expand_all_subitems_action.triggered.connect(self.runCollapseAllSubItemsAction)

    return menu