# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4 import QtGui

from geopicardie.utils.gpic_node_types import *
from geopicardie.utils.gpic_icons import *



class GpicTreeWidgetItem(QtGui.QTreeWidgetItem):
  """
  """

  def __init__(self, parent, gpic_data = None):
    """
    """

    QtGui.QTreeWidgetItem.__init__(self, parent)

    self.gpic_data = gpic_data
    self.setText(0, gpic_data.title)

    if gpic_data.node_type == GpicNodeTypes.Instance().NODE_TYPE_FOLDER:
      self.setIcon(0, GpicIcon.Instance().getFolderIcon())

    self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)


  def runAction(self):
    """
    """

    self.gpic_data.runAction()