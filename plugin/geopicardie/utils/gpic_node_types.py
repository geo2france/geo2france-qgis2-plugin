# -*- coding: utf-8 -*-

from geopicardie.utils.singleton import *



@Singleton
class GpicNodeTypes():
  """
  """

  NODE_TYPE_FOLDER = "folder"
  NODE_TYPE_WS = "web_service"
  NODE_TYPE_WMS_LAYER = "wms_layer"
  NODE_TYPE_WMS_LAYER_STYLE = "wms_layer-style"
  NODE_TYPE_WFS_FEATURE_TYPE = "wfs_feature_type"

  def __init__(self):
    """
    """
    pass
