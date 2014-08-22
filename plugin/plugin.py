# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
try:
  from PyQt4.QtCore import QString
except:
  QString = type("")

from PyQt4.QtGui import *
from qgis.core import *
import os
import json

NODE_TYPE_FOLDER = "folder"
NODE_TYPE_WS = "web_service"
NODE_TYPE_WMS_LAYER = "wms_layer"
NODE_TYPE_WMS_LAYER_STYLE = "wms_layer-style"
NODE_TYPE_WFS_FEATURE_TYPE = "wfs_feature_type"

CONFIG_FILE_NAME = "favorites.json"

class FavoritesTreeNode:
  """
  """

  def __init__(self, iface, title, node_type=NODE_TYPE_FOLDER,
    description=None, params=None):
    """
    """

    self.iface = iface
    self.node_type = node_type
    self.title = title
    self.description = description
    self.children = []

    if self.node_type == NODE_TYPE_WMS_LAYER:
      self.service_url = params.get("url")
      self.layer_name = params.get("name")
      self.layer_format = params.get("format")
      self.layer_srs = params.get("srs")
      self.layer_style = params.get("style", "")

  def runAction(self):
    if self.node_type == NODE_TYPE_WMS_LAYER:
      self.addWMSLayer()

  def addWMSLayer(self):
    layer_url = u"crs={}&dpiMode=7&featureCount=10&format={}&layers={}&styles={}&url={}".format(
      self.layer_srs, self.layer_format, self.layer_name, self.layer_style, self.service_url)
    self.iface.addRasterLayer(layer_url, self.layer_name, "wms")


  def __str__(self):
    result = u"{} (description: {}, type: {}, children: {})".format(self.title, self.description, self.node_type, len(self.children))
    return

  def __unicode__(self):
    result = u"{} (description: {}, type: {}, children: {})".format(self.title, self.description, self.node_type, len(self.children))
    return

  def __repr__(self):
    result = u"{} (description: {}, type: {}, children: {})".format(self.title, self.description, self.node_type, len(self.children))
    return

class FavoriteTreeNodeFactory:
  """
  Class used to build FavoritesTreeNode instances
  """

  def build_tree(self, iface, tree_config):
    """
    Function that do the job
    """

    # Read the node attributes
    node_title = tree_config.get('title', None)
    node_description = tree_config.get('description', None)
    node_type = tree_config.get('type', None)
    node_params = tree_config.get('params', None)

    if node_title:
      # Creation of the node
      node = FavoritesTreeNode(iface, node_title, node_type, node_description, node_params)

      # Creation of the node children
      node_children = tree_config.get('children', [])
      if len(node_children) > 0:
        for child_config in node_children:
          child_node = self.build_tree(iface, child_config)
          node.children.append(child_node)

      return node

    else:
      return None


class PluginGeoPicardie:
  """
  Plugin class.
  """

  def __init__(self, iface):
    """
    Plugin initialisation.
    A json config file is read in order to configure the plugin GUI.
    """
    self.iface = iface

    # Read config file
    config_struct = None
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    param_file_path = os.path.join(current_dir_path, CONFIG_FILE_NAME)
    with open(param_file_path) as f:
      config_string = "".join(f.readlines())
      config_struct = json.loads(config_string)

    self.ressources_tree = FavoriteTreeNodeFactory().build_tree(self.iface, config_struct)


  def initGui(self):
    """
    Plugin GUI initialisation.
    """

    self.createSubMenuForFavorite(self.ressources_tree, self.iface.pluginMenu())


  def createSubMenuForFavorite(self, tree, parent_menu):
    """
    """

    if tree.children != None and len(tree.children) > 0:
      sub_menu = QMenu(tree.title, parent_menu)
      for child in tree.children:
        self.createSubMenuForFavorite(child, sub_menu)

      parent_menu.addMenu(sub_menu)

    else:
      action = QAction(tree.title, self.iface.mainWindow())
      QObject.connect(action, SIGNAL("triggered()"), tree.runAction)
      parent_menu.addAction(action)

  def unload(self):
    pass
