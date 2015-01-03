# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4 import QtGui

from geopicardie.utils.plugin_globals import GpicGlobals



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
  An item of the GéoPicardie tree view
  """

  def __init__(self, parent, gpic_data = None):
    """
    """

    QtGui.QTreeWidgetItem.__init__(self, parent)

    # Item data
    self.gpic_data = gpic_data

    # Item title and description
    self.setText(0, gpic_data.title)
    self.setToolTip (0, gpic_data.description)

    #Item icon
    icon = self.gpic_data.icon
    if icon != None:
      self.setIcon(0, icon)
    
    # QT flags
    # Enable selection and drag of the item
    if self.gpic_data.can_be_added_to_map:
      self.setFlags(Qt.ItemIsDragEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
    else:
      self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)


  def runDefaultAction(self):
    """
    """

    if self.gpic_data.can_be_added_to_map:
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

    if self.gpic_data.can_be_added_to_map:
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


  def isAnEmptyGroup(self):
    """
    Indicates if this tem is an empty group
    """

    child_count = self.childCount()

    if child_count == 0:
      return self.gpic_data.node_type == GpicGlobals.Instance().NODE_TYPE_FOLDER
    else:
      for i in range(child_count):
        if not self.child(i).isAnEmptyGroup(): return False
      return True

    return False