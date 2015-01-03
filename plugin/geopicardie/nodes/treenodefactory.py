# -*- coding: utf-8 -*-

import os
import json
import urllib2

from qgis.gui import *
from qgis.core import *

from geopicardie.utils.plugin_globals import GpicGlobals
from nodes import *


def downloadResourcesTreeFile(file_url):
  """
  Download the resources tree file
  """

  try:

    # Download the config file
    http_req = urllib2.Request(file_url)
    http_req.add_header("Cache-Control", "no-cache")
    config_file = urllib2.urlopen(http_req)
    with open(GpicGlobals.Instance().config_file_path, 'wb') as f:
      f.write(config_file.read())


  except Exception as e:
    short_message = u"Le téléchargement du fichier de configuration du plugin {0} a échoué.".format(GpicGlobals.Instance().PLUGIN_TAG)
    GpicGlobals.Instance().iface.messageBar().pushMessage("Erreur", short_message, level=QgsMessageBar.CRITICAL)

    long_message = u"{0}\nUrl du fichier : {1}\n{2}\n{3}".format(short_message, file_url, e.__doc__, e.message)
    QgsMessageLog.logMessage(long_message, tag=GpicGlobals.Instance().PLUGIN_TAG, level=QgsMessageLog.CRITICAL)


class FavoriteTreeNodeFactory:
  """
  Class used to build FavoritesTreeNode instances
  """

  def __init__(self, file_path):
    self.file_path = file_path
    self.root_node = None

    if not os.path.isfile(self.file_path):
      message = u"Le fichier de configuration du plugin {0} n'a pas pu être trouvé.".format(GpicGlobals.Instance().PLUGIN_TAG)
      GpicGlobals.Instance().iface.messageBar().pushMessage("Erreur", message, level=QgsMessageBar.CRITICAL)
      QgsMessageLog.logMessage(message, tag=GpicGlobals.Instance().PLUGIN_TAG, level=QgsMessageLog.CRITICAL)
      return


    try:

      # Read the config file
      with open(self.file_path) as f:
        config_string = "".join(f.readlines())
        config_struct = json.loads(config_string)
        self.root_node = self.build_tree(config_struct)

    except Exception as e:
      short_message = u"La lecture du fichier de configuration du plugin {0} a produit des erreurs.".format(GpicGlobals.Instance().PLUGIN_TAG)
      GpicGlobals.Instance().iface.messageBar().pushMessage("Erreur", short_message, level=QgsMessageBar.CRITICAL)

      long_message = u"{0}\n{1}\n{2}".format(short_message, e.__doc__, e.message)
      QgsMessageLog.logMessage(long_message, tag=GpicGlobals.Instance().PLUGIN_TAG, level=QgsMessageLog.CRITICAL)




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
      if node_type == GpicGlobals.Instance().NODE_TYPE_WMS_LAYER:
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
        node = FolderTreeNode(node_title, node_type, node_description, node_status, node_metadata_url, node_params, parent_node)

      # Creation of the node children
      node_children = tree_config.get('children', [])
      if len(node_children) > 0:
        for child_config in node_children:
          child_node = self.build_tree(child_config, node)
          node.children.append(child_node)

      return node

    else:
      return None
