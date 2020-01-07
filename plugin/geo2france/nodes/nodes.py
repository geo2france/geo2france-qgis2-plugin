# -*- coding: utf-8 -*-

import os

from geo2france.utils.plugin_globals import GpicGlobals
from geo2france.utils.gpic_icons import *


class FavoritesTreeNode:
  """
  """

  def __init__(self, title, node_type=GpicGlobals.Instance().NODE_TYPE_FOLDER,
    description=None, status = None, metadata_url = None, params=None, parent_node=None):
    """
    """

    self.parent_node = parent_node
    self.node_type = node_type
    self.title = title
    self.description = description
    self.status = status
    self.metadata_url = metadata_url
    self.children = []
    self.can_be_added_to_map = False
    self.icon = None


  def layerMimeData(self):
    """
    Return the mime data used by the drag and drop process
    and needed by QGIS to add the right layer to the map
    """

    qgis_layer_details = self.getQgisLayerDetails()
    layerMimeData = ':'.join([
      qgis_layer_details["type"],
      qgis_layer_details["provider"],
      qgis_layer_details["title"].replace( ":", "\\:" ),
      qgis_layer_details["uri"].replace( ":", "\\:" )])

    return layerMimeData


  def runAddToMapAction(self):
    """
    """

    pass


  def runShowMetadataAction(self):
    """
    Opens in the default user web browser the web page displaying the resource metadata
    """

    import webbrowser
    if self.metadata_url:
      webbrowser.open_new_tab(self.metadata_url)


  def runReportIssueAction(self):
    """
    Opens the default mail client to let the user send an issue report by email
    """

    # import webbrowser
    # webbrowser.open('mailto:')
    pass


# Subclasses of FavoritesTreeNode

class FolderTreeNode(FavoritesTreeNode):
  """
  Tree node for a folder containing other nodes
  """

  def __init__(self, title, node_type=GpicGlobals.Instance().NODE_TYPE_FOLDER,
    description=None, status=None, metadata_url=None, params=None, parent_node=None):
    """
    """

    FavoritesTreeNode.__init__(self, title, node_type, description, status, metadata_url, params, parent_node)

    # Icon
    gpicIcons = GpicIcons.Instance()
    self.icon = gpicIcons.folder_icon
    if self.status == GpicGlobals.Instance().NODE_STATUS_WARN:
      self.icon = gpicIcons.warn_icon


class WmsLayerTreeNode(FavoritesTreeNode):
  """
  Tree node for a WMS layer
  """

  def __init__(self, title, node_type=GpicGlobals.Instance().NODE_TYPE_WMS_LAYER,
    description=None, status=None, metadata_url=None, params=None, parent_node=None):
    """
    """

    FavoritesTreeNode.__init__(self, title, node_type, description, status, metadata_url, params, parent_node)

    self.service_url = params.get("url")
    self.layer_name = params.get("name")
    self.layer_format = params.get("format")
    self.layer_srs = params.get("srs")
    self.layer_style_name = params.get("style", "")
    self.can_be_added_to_map = True

    # Icon
    gpicIcons = GpicIcons.Instance()
    self.icon = gpicIcons.wms_layer_icon
    if self.status == GpicGlobals.Instance().NODE_STATUS_WARN:
      self.icon = gpicIcons.warn_icon


  def getQgisLayerDetails(self):
    """
    Return the details of the layer used by QGIS to add the layer to the map.
    This dictionary is used by the runAddToMapAction and layerMimeData methods.
    """

    qgis_layer_uri_details = {
      "type": "raster",
      "provider": "wms",
      "title": self.title,
      "uri": u"crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
      self.layer_srs, self.layer_format, self.layer_name, self.layer_style_name, self.service_url)
    }

    return qgis_layer_uri_details


  def runAddToMapAction(self):
    """
    Add the WMS layer with the specified style to the map
    """

    qgis_layer_details = self.getQgisLayerDetails()
    GpicGlobals.Instance().iface.addRasterLayer(
      qgis_layer_details["uri"],
      qgis_layer_details["title"],
      qgis_layer_details["provider"])


class WmsStyleLayerTreeNode(FavoritesTreeNode):
  """
  Tree node for a WMS layer with a specific style
  """

  def __init__(self, title, node_type=GpicGlobals.Instance().NODE_TYPE_WMS_LAYER_STYLE,
    description=None, status=None, metadata_url=None, params=None, parent_node=None):
    """
    """

    FavoritesTreeNode.__init__(self, title, node_type, description, status, metadata_url, params, parent_node)

    self.layer_style_name = params.get("name")
    self.can_be_added_to_map = True

    # Icon
    gpicIcons = GpicIcons.Instance()
    self.icon = gpicIcons.wms_style_icon
    if self.status == GpicGlobals.Instance().NODE_STATUS_WARN:
      self.icon = gpicIcons.warn_icon


  def getQgisLayerDetails(self):
    """
    Return the details of the layer used by QGIS to add the layer to the map.
    This dictionary is used by the runAddToMapAction and layerMimeData methods.
    """

    if self.parent_node == None:
      return None

    qgis_layer_uri_details = {
      "type": "raster",
      "provider": "wms",
      "title": self.title,
      "uri": u"crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
        self.parent_node.layer_srs, self.parent_node.layer_format, self.parent_node.layer_name, self.layer_style_name, self.parent_node.service_url)
    }

    return qgis_layer_uri_details


  def runAddToMapAction(self):
    """
    Add the WMS layer with the specified style to the map
    """

    qgis_layer_details = self.getQgisLayerDetails()
    if qgis_layer_details != None:
      GpicGlobals.Instance().iface.addRasterLayer(
        qgis_layer_details["uri"],
        qgis_layer_details["title"],
        qgis_layer_details["provider"])


class WmtsLayerTreeNode(FavoritesTreeNode):
  """
  Tree node for a WMTS layer
  """

  def __init__(self, title, node_type=GpicGlobals.Instance().NODE_TYPE_WMTS_LAYER,
    description=None, status=None, metadata_url=None, params=None, parent_node=None):
    """
    """

    FavoritesTreeNode.__init__(self, title, node_type, description, status, metadata_url, params, parent_node)

    self.service_url = params.get("url")
    self.layer_tilematrixset_name = params.get("tilematrixset_name")
    self.layer_name = params.get("name")
    self.layer_format = params.get("format")
    self.layer_srs = params.get("srs")
    self.layer_style_name = params.get("style", "")
    self.can_be_added_to_map = True

    # Icon
    gpicIcons = GpicIcons.Instance()
    self.icon = gpicIcons.wms_style_icon
    if self.status == GpicGlobals.Instance().NODE_STATUS_WARN:
      self.icon = gpicIcons.warn_icon


  def getQgisLayerDetails(self):
    """
    Return the details of the layer used by QGIS to add the layer to the map.
    This dictionary is used by the runAddToMapAction and layerMimeData methods.
    """

    qgis_layer_uri_details = {
      "type": "raster",
      "provider": "wms",
      "title": self.title,
      "uri": u"tileMatrixSet={}&crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
      self.layer_tilematrixset_name, self.layer_srs, self.layer_format, self.layer_name, self.layer_style_name, self.service_url)
    }

    return qgis_layer_uri_details


  def runAddToMapAction(self):
    """
    Add the WMTS layer to the map
    """

    qgis_layer_details = self.getQgisLayerDetails()
    if qgis_layer_details != None:
      GpicGlobals.Instance().iface.addRasterLayer(
        qgis_layer_details["uri"],
        qgis_layer_details["title"],
        qgis_layer_details["provider"])


class WfsFeatureTypeTreeNode(FavoritesTreeNode):
  """
  Tree node for a WFS feature type
  """

  def __init__(self, title, node_type=GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE,
    description=None, status=None, metadata_url=None, params=None, parent_node=None):
    """
    """

    FavoritesTreeNode.__init__(self, title, node_type, description, status, metadata_url, params, parent_node)

    self.service_url = params.get("url")
    self.feature_type_name = params.get("name")
    self.filter = params.get("filter")
    self.wfs_version = params.get("version", "1.0.0")
    self.layer_srs = params.get("srs")
    self.can_be_added_to_map = True

    # Icon
    gpicIcons = GpicIcons.Instance()
    self.icon = gpicIcons.wfs_layer_icon
    if self.status == GpicGlobals.Instance().NODE_STATUS_WARN:
      self.icon = gpicIcons.warn_icon


  def getQgisLayerDetails(self):
    """
    Return the details of the layer used by QGIS to add the layer to the map.
    This dictionary is used by the runAddToMapAction and layerMimeData methods.
    """

    first_param_prefix = '?'
    if '?' in self.service_url:
      first_param_prefix = '&'

    uri = u"{}{}SERVICE=WFS&VERSION={}&REQUEST=GetFeature&TYPENAME={}&SRSNAME={}".format(
      self.service_url, first_param_prefix, self.wfs_version, self.feature_type_name, self.layer_srs)

    if self.filter:
      uri += "&Filter={}".format(self.filter)

    qgis_layer_uri_details = {
      "type": "vector",
      "provider": "WFS",
      "title": self.title,
      "uri": uri
    }

    return qgis_layer_uri_details


  def runAddToMapAction(self):
    """
    Add the WFS feature type to the map
    """

    qgis_layer_details = self.getQgisLayerDetails()
    if qgis_layer_details != None:
      GpicGlobals.Instance().iface.addVectorLayer(
        qgis_layer_details["uri"],
        qgis_layer_details["title"],
        qgis_layer_details["provider"])


class WfsFeatureTypeFilterTreeNode(FavoritesTreeNode):
  """
  Tree node for a WFS feature type filter
  """

  def __init__(self, title, node_type=GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE_FILTER,
    description=None, status=None, metadata_url=None, params=None, parent_node=None):
    """
    """

    FavoritesTreeNode.__init__(self, title, node_type, description, status, metadata_url, params, parent_node)

    self.filter = params.get("filter")
    self.can_be_added_to_map = True

    # Icon
    gpicIcons = GpicIcons.Instance()
    self.icon = gpicIcons.wfs_layer_icon
    if self.status == GpicGlobals.Instance().NODE_STATUS_WARN:
      self.icon = gpicIcons.warn_icon


  def getQgisLayerDetails(self):
    """
    Return the details of the layer used by QGIS to add the layer to the map.
    This dictionary is used by the runAddToMapAction and layerMimeData methods.
    """

    if self.parent_node == None:
      return None

    first_param_prefix = '?'
    if '?' in self.parent_node.service_url:
      first_param_prefix = '&'

    uri = u"{}{}SERVICE=WFS&VERSION={}&REQUEST=GetFeature&TYPENAME={}&SRSNAME={}".format(
        self.parent_node.service_url, first_param_prefix, self.parent_node.wfs_version, self.parent_node.feature_type_name, self.parent_node.layer_srs)

    if self.filter:
      uri += "&Filter={}".format(self.filter)

    qgis_layer_uri_details = {
      "type": "vector",
      "provider": "WFS",
      "title": self.title,
      "uri": uri
    }

    return qgis_layer_uri_details


  def runAddToMapAction(self):
    """
    Add the WFS feature type to the map with a filter
    """
    
    qgis_layer_details = self.getQgisLayerDetails()
    if qgis_layer_details != None:
      GpicGlobals.Instance().iface.addVectorLayer(
        qgis_layer_details["uri"],
        qgis_layer_details["title"],
        qgis_layer_details["provider"])


class GdalWmsConfigFileTreeNode(FavoritesTreeNode):
  """
  Tree node for a GDAL WMS config file
  """

  def __init__(self, title, node_type=GpicGlobals.Instance().NODE_TYPE_GDAL_WMS_CONFIG_FILE,
    description=None, status=None, metadata_url=None, params=None, parent_node=None):
    """
    """

    FavoritesTreeNode.__init__(self, title, node_type, description, status, metadata_url, params, parent_node)

    self.gdal_config_file_path = os.path.join(
      GpicGlobals.Instance().config_dir_path,
      params.get("file_path"))
    self.can_be_added_to_map = True

    # Icon
    gpicIcons = GpicIcons.Instance()
    self.icon = gpicIcons.raster_layer_icon
    if self.status == GpicGlobals.Instance().NODE_STATUS_WARN:
      self.icon = gpicIcons.warn_icon


  def getQgisLayerDetails(self):
    """
    Return the details of the layer used by QGIS to add the layer to the map.
    This dictionary is used by the runAddToMapAction and layerMimeData methods.
    """

    qgis_layer_uri_details = {
      "type": "raster",
      "provider": "gdal",
      "title": self.title,
      "uri": self.gdal_config_file_path.replace("\\", "/")
    }

    return qgis_layer_uri_details


  def runAddToMapAction(self):
    """
    Add the preconfigured TMS layer to the map
    """

    # GpicGlobals.Instance().iface.addRasterLayer(self.gdal_config_file_path, self.title)
    qgis_layer_details = self.getQgisLayerDetails()
    if qgis_layer_details != None:
      GpicGlobals.Instance().iface.addRasterLayer(
        qgis_layer_details["uri"],
        qgis_layer_details["title"])