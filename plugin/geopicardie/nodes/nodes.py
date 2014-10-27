# -*- coding: utf-8 -*-

import os

from geopicardie.utils.plugin_globals import GpicGlobals
from geopicardie.utils.gpic_icons import *


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
    """

    pass


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


  def runAddToMapAction(self):
    """
    Add the WMS layer with the specified style to the map
    """

    layer_url = u"crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
      self.layer_srs, self.layer_format, self.layer_name, self.layer_style_name, self.service_url)
    GpicGlobals.Instance().iface.addRasterLayer(layer_url, self.title, "wms")


  def layerMimeData(self):
    """
    """

    layerType = "raster"
    layerProvider = "wms"
    escapedLayerName = self.title.replace( ":", "\\:" )
    layerUrl = u"crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
    self.layer_srs, self.layer_format, self.layer_name, self.layer_style_name, self.service_url)
    escapedLayerUrl = layerUrl.replace( ":", "\\:" )
    layerMimeData = ':'.join([layerType, layerProvider, escapedLayerName, escapedLayerUrl])

    return layerMimeData


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


  def runAddToMapAction(self):
    """
    Add the WMS layer with the specified style to the map
    """

    if self.parent_node != None:
      layer_url = u"crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
        self.parent_node.layer_srs, self.parent_node.layer_format, self.parent_node.layer_name, self.layer_style_name, self.parent_node.service_url)
      GpicGlobals.Instance().iface.addRasterLayer(layer_url, self.parent_node.title, "wms")



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


  def runAddToMapAction(self):
    """
    Add the WMTS layer to the map
    """

    layer_url = u"tileMatrixSet={}&crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
      self.layer_tilematrixset_name, self.layer_srs, self.layer_format, self.layer_name, self.layer_style_name, self.service_url)
    GpicGlobals.Instance().iface.addRasterLayer(layer_url, self.title, "wms")


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


  def runAddToMapAction(self):
    """
    Add the WFS feature type to the map
    """
    
    first_param_prefix = '?'
    if '?' in self.service_url:
      first_param_prefix = '&'
    layer_url = u"{}{}SERVICE=WFS&VERSION={}&REQUEST=GetFeature&TYPENAME={}&SRSNAME={}".format(
      self.service_url, first_param_prefix, self.wfs_version, self.feature_type_name, self.layer_srs)
    if self.filter:
      layer_url += "&Filter={}".format(self.filter)
    GpicGlobals.Instance().iface.addVectorLayer(layer_url, self.title, "WFS")


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


  def runAddToMapAction(self):
    """
    Add the WFS feature type to the map with a filter
    """
    
    if self.parent_node != None:
      first_param_prefix = '?'
      if '?' in self.parent_node.service_url:
        first_param_prefix = '&'
      layer_url = u"{}{}SERVICE=WFS&VERSION={}&REQUEST=GetFeature&TYPENAME={}&SRSNAME={}".format(
        self.parent_node.service_url, first_param_prefix, self.parent_node.wfs_version, self.parent_node.feature_type_name, self.parent_node.layer_srs)
      if self.filter:
        layer_url += "&Filter={}".format(self.filter)
      GpicGlobals.Instance().iface.addVectorLayer(layer_url, self.title, "WFS")


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
      

  def runAddToMapAction(self):
    """
    Add the preconfigured TMS layer to the map
    """

    GpicGlobals.Instance().iface.addRasterLayer(self.gdal_config_file_path, self.title)



class FavoriteTreeNodeFactory:
  """
  Class used to build FavoritesTreeNode instances
  """

  def build_tree(self, tree_config, parent_node = None):
    """
    Function that do the job
    """

    # Read the node attributes
    node_title = tree_config.get('title', None)
    node_description = tree_config.get('description', None)
    node_type = tree_config.get('type', None)
    node_status = tree_config.get('status', None)
    node_metadata_url = tree_config.get('metadata_url', None)
    node_params = tree_config.get('params', None)

    if node_title:
      # Creation of the node
      if node_type == GpicGlobals.Instance().NODE_TYPE_FOLDER:
        node = FolderTreeNode(node_title, node_type, node_description, node_status, node_metadata_url, node_params, parent_node)

      elif node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER:
        node = WmsLayerTreeNode(node_title, node_type, node_description, node_status, node_metadata_url, node_params, parent_node)

      elif node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER_STYLE:
        node = WmsStyleLayerTreeNode(node_title, node_type, node_description, node_status, node_metadata_url, node_params, parent_node)

      elif node_type == GpicGlobals.Instance().NODE_TYPE_WMTS_LAYER:
        node = WmtsLayerTreeNode(node_title, node_type, node_description, node_status, node_metadata_url, node_params, parent_node)

      elif node_type == GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
        node = WfsFeatureTypeTreeNode(node_title, node_type, node_description, node_status, node_metadata_url, node_params, parent_node)

      elif node_type == GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE_FILTER:
        node = WfsFeatureTypeFilterTreeNode(node_title, node_type, node_description, node_status, node_metadata_url, node_params, parent_node)

      elif node_type == GpicGlobals.Instance().NODE_TYPE_GDAL_WMS_CONFIG_FILE:
        node = GdalWmsConfigFileTreeNode(node_title, node_type, node_description, node_status, node_metadata_url, node_params, parent_node)

      else:
        node = FavoritesTreeNode(node_title, node_type, node_description, node_status, node_metadata_url, node_params, parent_node)

      # Creation of the node children
      node_children = tree_config.get('children', [])
      if len(node_children) > 0:
        for child_config in node_children:
          child_node = self.build_tree(child_config, node)
          node.children.append(child_node)

      return node

    else:
      return None
