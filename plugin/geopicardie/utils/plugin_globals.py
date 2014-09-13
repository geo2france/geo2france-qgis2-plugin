# -*- coding: utf-8 -*-

import os
from geopicardie.utils.singleton import *



@Singleton
class GpicGlobals():
  """
  """

  iface = None
  plugin_path = None

  # Tree nodes types
  NODE_TYPE_FOLDER = "folder"
  NODE_TYPE_WS = "web_service"
  NODE_TYPE_WMS_LAYER = "wms_layer"
  NODE_TYPE_WMTS_LAYER = "wmts_layer"
  NODE_TYPE_WMS_LAYER_STYLE = "wms_layer_style"
  NODE_TYPE_WFS_FEATURE_TYPE = "wfs_feature_type"
  NODE_TYPE_WFS_FEATURE_TYPE_FILTER = "wfs_feature_type_filter"
  NODE_TYPE_GDAL_WMS_CONFIG_FILE = "gdal_wms_config_file"

  # Node status values
  NODE_STATUS_WARN = 'warn'

  # Images dir
  IMAGES_DIR_NAME = "images"
  LOGO_FILE_NAME = "logo_geopicardie.png"

  ICON_WARN_FILE_NAME = "Icon_Simple_Warn.png"
  ICON_WMS_LAYER_FILE_NAME = "mIconWms.svg"
  ICON_WMS_STYLE_FILE_NAME = "mIconWmsStyle.svg"
  ICON_WFS_LAYER_FILE_NAME = "mIconWfs.svg"
  ICON_RASTER_LAYER_FILE_NAME = "mIconRaster.svg"

  # Config files dir
  CONFIG_DIR_NAME = "config"
  CONFIG_FILE_NAME = "config.json"


  def __init__(self):
    """
    """
    pass


  def updateGlobals(self, plugin_path, iface):
    """
    """
    
    self.iface=iface
    self.plugin_path=plugin_path

    self.config_dir_path = os.path.join(self.plugin_path, self.CONFIG_DIR_NAME)
    self.config_file_path = os.path.join(self.config_dir_path, self.CONFIG_FILE_NAME)

    self.images_dir_path = os.path.join(self.plugin_path, self.IMAGES_DIR_NAME)
    self.geopic_logo_file_path = os.path.join(self.images_dir_path, self.LOGO_FILE_NAME)
