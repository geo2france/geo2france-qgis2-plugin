# -*- coding: utf-8 -*-

import sys
import os
from geopicardie.utils.singleton import *
from PyQt4.QtCore import QSettings


@Singleton
class GpicGlobals():
  """
  """

  iface = None
  plugin_path = None

  # Plugin infos
  PLUGIN_TAG = u"GéoPicardie"
  PLUGIN_VERSION = u"0.4.2"
  PLUGIN_SOURCE_REPOSITORY = u"https://github.com/bchartier/geopicardie-qgis-plugin/"

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
  CONFIG_FILES_DOWNLOAD_AT_STARTUP = 0 # 1 for yes, 0 for no
  CONFIG_DIR_NAME = "config"
  CONFIG_FILE_NAMES = ["config.json"]
  CONFIG_FILE_URLS = ["https://raw.githubusercontent.com/bchartier/qgis-favorites-resources-trees/master/geopicardie.json"]

  # Mask resources with status = warn
  MASK_RESOURCES_WITH_WARN_STATUS = 1 # 1 for yes, 0 for no

  # Flag to signal that the resources tree need to be reloaded
  RESOURCES_TREE_NEED_RELOAD = False

  # Flag to signal that the resources tree need to be downloaded
  RESOURCES_TREE_NEED_DOWNLOAD = False

  def __init__(self):
    """
    """
    pass


  def setPluginPath(self, plugin_path):
    """
    """

    system_encoding = sys.getfilesystemencoding()
    self.plugin_path = plugin_path.decode(system_encoding)


  def setPluginIFace(self, iface):
    """
    """

    self.iface=iface


  def reloadGlobalsFromQgisSettings(self):
    """
    Reloads the global variables of the plugin
    """
    
    # Read the qgis plugin settings
    s = QSettings()
    self.CONFIG_FILES_DOWNLOAD_AT_STARTUP = s.value(u"{0}/config_files_download_at_startup".format(self.PLUGIN_TAG), self.CONFIG_FILES_DOWNLOAD_AT_STARTUP)
    self.CONFIG_DIR_NAME = s.value(u"{0}/config_dir_name".format(self.PLUGIN_TAG), self.CONFIG_DIR_NAME)
    self.CONFIG_FILE_NAMES = s.value(u"{0}/config_file_names".format(self.PLUGIN_TAG), self.CONFIG_FILE_NAMES)
    self.CONFIG_FILE_URLS = s.value(u"{0}/config_file_urls".format(self.PLUGIN_TAG), self.CONFIG_FILE_URLS)
    self.MASK_RESOURCES_WITH_WARN_STATUS = s.value(u"{0}/mask_resources_with_warn_status".format(self.PLUGIN_TAG), self.MASK_RESOURCES_WITH_WARN_STATUS)

    self.config_dir_path = os.path.join(self.plugin_path, self.CONFIG_DIR_NAME)
    self.config_file_path = os.path.join(self.config_dir_path, self.CONFIG_FILE_NAMES[0])

    self.images_dir_path = os.path.join(self.plugin_path, self.IMAGES_DIR_NAME)
    self.geopic_logo_file_path = os.path.join(self.images_dir_path, self.LOGO_FILE_NAME)


  def resetToDefaults(self):
    """
    Reset global variables to default values
    """

    s = QSettings()
    s.setValue(u"{0}/mask_resources_with_warn_status".format(self.PLUGIN_TAG), 1)
    s.setValue(u"{0}/config_files_download_at_startup".format(self.PLUGIN_TAG), 0)
    s.setValue(u"{0}/config_file_names".format(self.PLUGIN_TAG), ["config.json"])
    s.setValue(u"{0}/config_file_urls".format(self.PLUGIN_TAG), ["https://raw.githubusercontent.com/bchartier/qgis-favorites-resources-trees/master/geopicardie.json"])


  def setQgisSettingsValue(self, setting, value):
    """
    Update a settings value
    """

    s = QSettings()
    s.setValue(u"{0}/{1}".format(self.PLUGIN_TAG, setting), value)
    self.reloadGlobalsFromQgisSettings()

    if setting in ("config_file_urls", "config_dir_name", "config_file_names"):
      self.RESOURCES_TREE_NEED_DOWNLOAD = True
      self.RESOURCES_TREE_NEED_RELOAD = True

    if setting in ("mask_resources_with_warn_status"):
      self.RESOURCES_TREE_NEED_RELOAD = True


  def resetFlags(self):
    """
    Reset the RESOURCES_TREE_NEED_DOWNLOAD and RESOURCES_TREE_NEED_RELOAD flags
    """

    self.RESOURCES_TREE_NEED_DOWNLOAD = False
    self.RESOURCES_TREE_NEED_RELOAD = False
