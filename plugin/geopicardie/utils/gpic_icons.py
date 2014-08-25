# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from qgis.core import QgsApplication

from geopicardie.utils.singleton import *



@Singleton
class GpicIcon():
  """
  """

  def __init__(self):
    """
    """

    # Folder icon
    QgsApplication.initQgis()
    style = QgsApplication.style()
    self.folder_icon = QtGui.QIcon()
    self.folder_icon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_DirClosedIcon), QtGui.QIcon.Normal, QtGui.QIcon.Off)


  def getFolderIcon(self):
    """
    """

    return self.folder_icon
