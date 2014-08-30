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

from geopicardie.utils import plugin_globals
from geopicardie.utils.gpic_node_types import *
from geopicardie.gui.gpic_dock import GpicDockWidget

CONFIG_FILE_NAME = "config.json"
CONFIG_DIR_NAME = "config"


class FavoritesTreeNode:
  """
  """

  def __init__(self, title, node_type=GpicNodeTypes.Instance().NODE_TYPE_FOLDER,
    description=None, params=None, parent_node=None):
    """
    """

    self.parent_node = parent_node
    self.node_type = node_type
    self.title = title
    self.description = description
    self.children = []

    if self.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMS_LAYER:
      self.service_url = params.get("url")
      self.layer_name = params.get("name")
      self.layer_format = params.get("format")
      self.layer_srs = params.get("srs")
      self.layer_style_name = params.get("style", "")

    elif self.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMS_LAYER_STYLE:
      self.layer_style_name = params.get("name")

    elif self.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMTS_LAYER:
      self.service_url = params.get("url")
      self.layer_tilematrixset_name = params.get("tilematrixset_name")
      self.layer_name = params.get("name")
      self.layer_format = params.get("format")
      self.layer_srs = params.get("srs")
      self.layer_style_name = params.get("style", "")

    elif self.node_type == GpicNodeTypes.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
      self.service_url = params.get("url")
      self.feature_type_name = params.get("name")
      self.wfs_version = params.get("version", "1.0.0")
      self.layer_srs = params.get("srs")


  def runAction(self):
    """
    """

    if self.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMS_LAYER:
      self.addWMSLayer()
    elif self.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMS_LAYER_STYLE:
      self.addWMSLayerWithStyle()
    elif self.node_type == GpicNodeTypes.Instance().NODE_TYPE_WMTS_LAYER:
      self.addWMTSLayer()
    elif self.node_type == GpicNodeTypes.Instance().NODE_TYPE_WFS_FEATURE_TYPE:
      self.addWFSLayer()


  def addWMSLayer(self):
    """
    """

    layer_url = u"crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
      self.layer_srs, self.layer_format, self.layer_name, self.layer_style_name, self.service_url)
    plugin_globals.iface.addRasterLayer(layer_url, self.title, "wms")


  def addWMSLayerWithStyle(self):
    """
    """

    if self.parent_node != None:
      layer_url = u"crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
        self.parent_node.layer_srs, self.parent_node.layer_format, self.parent_node.layer_name, self.layer_style_name, self.parent_node.service_url)
      plugin_globals.iface.addRasterLayer(layer_url, self.parent_node.title, "wms")


  def addWMTSLayer(self):
    """
    """

    layer_url = u"tileMatrixSet={}&crs={}&featureCount=10&format={}&layers={}&maxHeight=256&maxWidth=256&styles={}&url={}".format(
      self.layer_tilematrixset_name, self.layer_srs, self.layer_format, self.layer_name, self.layer_style_name, self.service_url)
    plugin_globals.iface.addRasterLayer(layer_url, self.title, "wms")


  def addWFSLayer(self):
    """
    """

    first_param_prefix = '?'
    if '?' in self.service_url:
      first_param_prefix = '&'
    layer_url = u"{}{}SERVICE=WFS&VERSION={}&REQUEST=GetFeature&TYPENAME={}&SRSNAME={}".format(
      self.service_url, first_param_prefix, self.wfs_version, self.feature_type_name, self.layer_srs)
    plugin_globals.iface.addVectorLayer(layer_url, self.title, "WFS")


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

  def build_tree(self, tree_config, parent_node = None):
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
      node = FavoritesTreeNode(node_title, node_type, node_description, node_params, parent_node)

      # Creation of the node children
      node_children = tree_config.get('children', [])
      if len(node_children) > 0:
        for child_config in node_children:
          child_node = self.build_tree(child_config, node)
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
    plugin_globals.iface = iface
    self.iface = iface

    # Read the config file
    config_struct = None
    plugin_globals.plugin_path = os.path.dirname(os.path.abspath(__file__))
    param_file_path = os.path.join(plugin_globals.plugin_path, CONFIG_DIR_NAME, CONFIG_FILE_NAME)
    with open(param_file_path) as f:
      config_string = "".join(f.readlines())
      config_struct = json.loads(config_string)

    self.ressources_tree = FavoriteTreeNodeFactory().build_tree(config_struct)


  def initGui(self):
    """
    Plugin GUI initialisation.
    """

    # Create a menu
    self.createPluginMenu()

    # Create a dockable panel with a tree of resources
    self.dock = GpicDockWidget()
    self.dock.setTreeContents(self.ressources_tree)
    self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)


  def createPluginMenu(self):
    """
    """

    plugin_menu = self.iface.pluginMenu()
    self.gpic_menu = QMenu(u"GéoPicardie", plugin_menu)
    plugin_menu.addMenu(self.gpic_menu)

    show_gpic_panel_action = QAction(u'Afficher le panneau GéoPicardie', self.iface.mainWindow())        
    show_gpic_panel_action.triggered.connect(self.showGpicPanelMenuTriggered)
    self.gpic_menu.addAction(show_gpic_panel_action)

    about_action = QAction(u'À propos…', self.iface.mainWindow())        
    about_action.triggered.connect(self.aboutMenuTriggered)
    self.gpic_menu.addAction(about_action)


  def showGpicPanelMenuTriggered(self):
    """
    """
    self.dock.show()


  def aboutMenuTriggered(self):
    """
    """
    QMessageBox.information(self.iface.mainWindow(),
      u"GéoPicardie",
      u"L'action de ce menu n'est pas encore implémentée",
      QMessageBox.Ok)


  def unload(self):
    self.iface.pluginMenu().removeAction(self.gpic_menu.menuAction())
