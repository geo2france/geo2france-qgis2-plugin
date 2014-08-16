#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
try:
	from PyQt4.QtCore import QString
except:
	QString = type("")

from PyQt4.QtGui import *
from qgis.core import *

NODE_TYPE_FOLDER = "folder"
NODE_TYPE_WS = "web_service"
NODE_TYPE_WMS_LAYER = "wms_layer"
NODE_TYPE_WMS_LAYER_STYLE = "wms_layer-style"
NODE_TYPE_WFS_FEATURE_TYPE = "wfs_feature_type"

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
		# QMessageBox.information(None, "DEBUG:", layer_url) 
		self.iface.addRasterLayer(layer_url, self.layer_name, "wms")


class PluginGeoPicardie:
	"""
	"""

	def __init__(self,iface):
		"""
		"""
		self.iface = iface
		
		self.favorites_tree = FavoritesTreeNode(iface, u"GéoPicardie")

		raster_tree_node = FavoritesTreeNode(iface=iface, title="Raster",
			node_type=NODE_TYPE_FOLDER, description="Couches raster courantes")

		raster_tree_node.children.append(FavoritesTreeNode(
			iface=iface,
			title=u"Vue aérienne 2001-2002",
			node_type=NODE_TYPE_WMS_LAYER,
			description=u"Orthophotographie aérienne de la Picardie de 2001-2002 (résolution de 1,25 m)",
			params={
				"url": u"http://www.geopicardie.fr/geoserver/wms",
				"name": u"geopicardie:picardie_ortho_2002",
				"format": u"image/jpeg",
				"srs": u"epsg:2154",
				"style": u""
			}))

		raster_tree_node.children.append(FavoritesTreeNode(
			iface=iface,
			title=u"Vue aérienne 2008-2009",
			node_type=NODE_TYPE_WMS_LAYER,
			description=u"Orthophotographie aérienne composite de la Picardie de 2008-2009 (résolution de 0,25 m)",
			params={
				"url": u"http://www.geopicardie.fr/geoserver/wms",
				"name": u"geopicardie:picardie_ortho_composite_2008_2009_vis",
				"format": u"image/jpeg",
				"srs": u"epsg:2154",
				"style": u""
			}))

		raster_tree_node.children.append(FavoritesTreeNode(
			iface=iface,
			title=u"Scan 25 - IGN",
			node_type=NODE_TYPE_WMS_LAYER,
			description=u"Scan25 de l'IGN de la Picardie",
			params={
				"url": u"http://www.geopicardie.fr/geoserver/wms",
				"name": u"geopicardie:picardie_scan25",
				"format": u"image/png",
				"srs": u"epsg:2154",
				"style": u""
			}))

		self.favorites_tree.children.append(raster_tree_node)

	def initGui(self):
		"""
		"""

		self.createSubMenuForFavorite(self.favorites_tree, self.iface.pluginMenu())


	def createSubMenuForFavorite(self, favorite_tree_node, parent_menu):
		"""
		"""

		if self.favorites_tree.children != None and len(favorite_tree_node.children) > 0:
			sub_menu = QMenu(favorite_tree_node.title, parent_menu)
			for child in favorite_tree_node.children:
				self.createSubMenuForFavorite(child, sub_menu)

			parent_menu.addMenu(sub_menu)

		else:
			action = QAction(favorite_tree_node.title, self.iface.mainWindow())
			QObject.connect(action, SIGNAL("triggered()"), favorite_tree_node.runAction)
			parent_menu.addAction(action)

	def unload(self):
		pass
