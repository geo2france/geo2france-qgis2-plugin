# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from qgis.core import QgsApplication
import os

from geopicardie.utils import plugin_globals
from geopicardie.utils.singleton import *

IMAGE_DIR_NAME = "images"
ICON_WMS_LAYER_FILE_NAME = "mIconWms.svg"
ICON_WFS_LAYER_FILE_NAME = "mIconWfs.svg"


@Singleton
class GpicIcons():
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

    wms_layer_icon_path = os.path.join(plugin_globals.plugin_path, IMAGE_DIR_NAME, ICON_WMS_LAYER_FILE_NAME)
    self.wms_layer_icon = QtGui.QIcon(wms_layer_icon_path)

    wfs_layer_icon_path = os.path.join(plugin_globals.plugin_path, IMAGE_DIR_NAME, ICON_WFS_LAYER_FILE_NAME)
    self.wfs_layer_icon = QtGui.QIcon(wfs_layer_icon_path)