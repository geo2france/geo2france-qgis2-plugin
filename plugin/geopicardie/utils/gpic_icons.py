# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from qgis.core import QgsApplication
import os

from geopicardie.utils.plugin_globals import GpicGlobals
from geopicardie.utils.singleton import *


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
    self.folder_icon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_DirClosedIcon),
      QtGui.QIcon.Normal, QtGui.QIcon.Off)

    warn_icon_path = os.path.join(GpicGlobals.Instance().images_dir_path,
      GpicGlobals.Instance().ICON_WARN_FILE_NAME)
    self.warn_icon = QtGui.QIcon(warn_icon_path)

    wms_layer_icon_path = os.path.join(GpicGlobals.Instance().images_dir_path,
      GpicGlobals.Instance().ICON_WMS_LAYER_FILE_NAME)
    self.wms_layer_icon = QtGui.QIcon(wms_layer_icon_path)

    wms_style_icon_path = os.path.join(GpicGlobals.Instance().images_dir_path,
      GpicGlobals.Instance().ICON_WMS_STYLE_FILE_NAME)
    self.wms_style_icon = QtGui.QIcon(wms_style_icon_path)

    wfs_layer_icon_path = os.path.join(GpicGlobals.Instance().images_dir_path,
      GpicGlobals.Instance().ICON_WFS_LAYER_FILE_NAME)
    self.wfs_layer_icon = QtGui.QIcon(wfs_layer_icon_path)

    raster_layer_icon_path = os.path.join(GpicGlobals.Instance().images_dir_path,
      GpicGlobals.Instance().ICON_RASTER_LAYER_FILE_NAME)
    self.raster_layer_icon = QtGui.QIcon(raster_layer_icon_path)
