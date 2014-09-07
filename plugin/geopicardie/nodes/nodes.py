# -*- coding: utf-8 -*-

from geopicardie.utils.plugin_globals import GpicGlobals


class FavoritesTreeNode:
  """
  """

  def __init__(self, title, node_type=GpicGlobals.Instance().NODE_TYPE_FOLDER,
    description=None, icon = None, params=None, parent_node=None):
    """
    """

    self.parent_node = parent_node
    self.node_type = node_type
    self.title = title
    self.description = description
    self.icon = icon
    self.children = []

    if self.node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER:
      self.service_url = params.get("url")
      self.layer_name = params.get("name")
      self.layer_format = params.get("format")
      self.layer_srs = params.get("srs")
      self.layer_style_name = params.get("style", "")

    elif self.node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER_STYLE:
      self.layer_style_name = params.get("name")

    elif self.node_type == GpicGlobals.Instance().NODE_TYPE_WMTS_LAYER:
      self.service_url = params.get("url")
      self.layer_tilematrixset_name = params.get("tilematrixset_name")
      self.layer_name = params.get("name")
      self.layer_format = params.get("format")
      self.layer_srs = params.get("srs")
      self.layer_style_name = params.get("style", "")

    elif self.node_type == GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
      self.service_url = params.get("url")
      self.feature_type_name = params.get("name")
      self.wfs_version = params.get("version", "1.0.0")
      self.layer_srs = params.get("srs")


  def runAddToMapAction(self):
    """
    """

    if self.node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER:
      self.addWMSLayer()
    elif self.node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER_STYLE:
      self.addWMSLayerWithStyle()
    elif self.node_type == GpicGlobals.Instance().NODE_TYPE_WMTS_LAYER:
      self.addWMTSLayer()
    elif self.node_type == GpicGlobals.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
      self.addWFSLayer()


  def addWMSLayer(self):
    """
    """

    layer_url = u"crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
      self.layer_srs, self.layer_format, self.layer_name, self.layer_style_name, self.service_url)
    GpicGlobals.Instance().iface.addRasterLayer(layer_url, self.title, "wms")


  def addWMSLayerWithStyle(self):
    """
    """

    if self.parent_node != None:
      layer_url = u"crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
        self.parent_node.layer_srs, self.parent_node.layer_format, self.parent_node.layer_name, self.layer_style_name, self.parent_node.service_url)
      GpicGlobals.Instance().iface.addRasterLayer(layer_url, self.parent_node.title, "wms")


  def addWMTSLayer(self):
    """
    """

    layer_url = u"tileMatrixSet={}&crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
      self.layer_tilematrixset_name, self.layer_srs, self.layer_format, self.layer_name, self.layer_style_name, self.service_url)
    GpicGlobals.Instance().iface.addRasterLayer(layer_url, self.title, "wms")


  def addWFSLayer(self):
    """
    """

    first_param_prefix = '?'
    if '?' in self.service_url:
      first_param_prefix = '&'
    layer_url = u"{}{}SERVICE=WFS&VERSION={}&REQUEST=GetFeature&TYPENAME={}&SRSNAME={}".format(
      self.service_url, first_param_prefix, self.wfs_version, self.feature_type_name, self.layer_srs)
    GpicGlobals.Instance().iface.addVectorLayer(layer_url, self.title, "WFS")


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
    node_icon = tree_config.get('icon', None)
    node_params = tree_config.get('params', None)

    if node_title:
      # Creation of the node
      node = FavoritesTreeNode(node_title, node_type, node_description, node_icon, node_params, parent_node)

      # Creation of the node children
      node_children = tree_config.get('children', [])
      if len(node_children) > 0:
        for child_config in node_children:
          child_node = self.build_tree(child_config, node)
          node.children.append(child_node)

      return node

    else:
      return None
